"""Build leakage-safe IEEE-CIS features for the thesis Scenario B.

This script implements the decisions already established in 02_EDA_IEEE_CIS:
- IEEE has no true CustomerId;
- card1 + addr1 is used only as a persistent ENTITY PROXY;
- TransactionDT is relative time;
- masked C/D/M/V fields may support Detection but are not interpreted as
  explicit fraudster actions;
- entity-history features use only earlier transactions.

Raw competition data remain local and are not committed to GitHub.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


SELECTED_V = [
    "V45", "V257", "V44", "V86", "V87",
    "V246", "V244", "V158", "V242", "V156",
    "V149", "V52", "V51", "V201", "V200",
]
C_COLUMNS = [f"C{i}" for i in range(1, 15)]
D_COLUMNS = [f"D{i}" for i in range(1, 16)]
M_COLUMNS = [f"M{i}" for i in range(1, 10)]

TRANSACTION_COLUMNS = [
    "TransactionID",
    "isFraud",
    "TransactionDT",
    "TransactionAmt",
    "ProductCD",
    "card1", "card2", "card3", "card4", "card5", "card6",
    "addr1", "addr2",
    "dist1", "dist2",
    "P_emaildomain", "R_emaildomain",
    *C_COLUMNS,
    *D_COLUMNS,
    *M_COLUMNS,
    *SELECTED_V,
]

IDENTITY_NUMERIC = [
    "id_01", "id_02", "id_05", "id_06", "id_11",
    "id_13", "id_17", "id_19", "id_20",
]
IDENTITY_CATEGORICAL = [
    "id_12", "id_15", "id_16", "id_28", "id_29",
    "id_31", "id_33", "id_34", "id_35", "id_36",
    "id_37", "id_38",
    "DeviceType", "DeviceInfo",
]
IDENTITY_COLUMNS = [
    "TransactionID",
    *IDENTITY_NUMERIC,
    *IDENTITY_CATEGORICAL,
]


def entity_proxy(
    card1: pd.Series,
    addr1: pd.Series,
) -> pd.Series:
    """Create a card1+addr1 proxy without claiming true customer identity."""
    card = (
        card1.astype("Int64")
        .astype("string")
        .fillna("__MISSING_CARD1__")
    )
    addr = (
        addr1.astype("Int64")
        .astype("string")
        .fillna("__MISSING_ADDR1__")
    )
    return card + "|" + addr


def build_features(
    transactions: pd.DataFrame,
    identity: pd.DataFrame,
) -> pd.DataFrame:
    data = transactions.copy()

    identity_small = identity.copy()
    identity_small["identity_available"] = 1
    data = data.merge(
        identity_small,
        on="TransactionID",
        how="left",
        validate="one_to_one",
    )
    data["identity_available"] = (
        data["identity_available"]
        .fillna(0)
        .astype("int8")
    )

    data = data.sort_values(
        ["TransactionDT", "TransactionID"],
        kind="stable",
    ).reset_index(drop=True)

    data["entity_proxy"] = entity_proxy(
        data["card1"],
        data["addr1"],
    )

    # Relative-time features. They preserve timing structure but have no
    # calendar-date interpretation.
    data["day_index"] = (
        data["TransactionDT"] // 86400
    ).astype("int32")
    data["hour_proxy"] = (
        (data["TransactionDT"] % 86400) / 3600.0
    )
    data["log_transaction_amt"] = np.log1p(
        data["TransactionAmt"].clip(lower=0)
    )

    # Past-only persistent entity state.
    grouped = data.groupby(
        "entity_proxy",
        sort=False,
        observed=True,
    )
    data["prior_tx_count"] = grouped.cumcount()

    prior_sum = (
        grouped["TransactionAmt"].cumsum()
        - data["TransactionAmt"]
    )
    prior_sumsq = (
        data.assign(
            _amt_sq=data["TransactionAmt"] ** 2
        )
        .groupby(
            "entity_proxy",
            sort=False,
            observed=True,
        )["_amt_sq"]
        .cumsum()
        - data["TransactionAmt"] ** 2
    )

    count = data["prior_tx_count"].astype(float)
    data["prior_amount_mean"] = np.where(
        count > 0,
        prior_sum / count,
        np.nan,
    )
    prior_var = np.where(
        count > 0,
        prior_sumsq / count
        - data["prior_amount_mean"] ** 2,
        np.nan,
    )
    data["prior_amount_std"] = np.sqrt(
        np.maximum(prior_var, 0)
    )

    data["gap_seconds"] = grouped[
        "TransactionDT"
    ].diff()

    # Prior same-product share for the proxy entity.
    data["prior_same_product_count"] = (
        data.groupby(
            ["entity_proxy", "ProductCD"],
            sort=False,
            observed=True,
        ).cumcount()
    )
    data["prior_product_share"] = np.where(
        data["prior_tx_count"] > 0,
        data["prior_same_product_count"]
        / data["prior_tx_count"],
        0.0,
    )

    data["log_prior_tx_count"] = np.log1p(
        data["prior_tx_count"]
    )
    data["log_prior_amount_mean"] = np.log1p(
        data["prior_amount_mean"].clip(lower=0)
    )
    data["log_prior_amount_std"] = np.log1p(
        data["prior_amount_std"].clip(lower=0)
    )
    data["log_gap_seconds"] = np.log1p(
        data["gap_seconds"].clip(lower=0)
    )
    data["amount_ratio_prior_mean"] = (
        data["TransactionAmt"]
        / data["prior_amount_mean"]
    ).replace([np.inf, -np.inf], np.nan)
    data["amount_ratio_clip"] = data[
        "amount_ratio_prior_mean"
    ].clip(upper=20)

    data["cold_start_entity"] = (
        data["prior_tx_count"].eq(0).astype("int8")
    )

    # Missingness is itself empirically informative in IEEE-CIS.
    identity_feature_cols = [
        c for c in IDENTITY_COLUMNS
        if c != "TransactionID"
    ]
    data["identity_missing_count"] = data[
        identity_feature_cols
    ].isna().sum(axis=1)

    detector_context = (
        C_COLUMNS
        + D_COLUMNS
        + M_COLUMNS
        + SELECTED_V
    )
    data["detector_missing_count"] = data[
        detector_context
    ].isna().sum(axis=1)

    data["email_both_missing"] = (
        data["P_emaildomain"].isna()
        & data["R_emaildomain"].isna()
    ).astype("int8")
    data["email_match"] = (
        data["P_emaildomain"].notna()
        & data["R_emaildomain"].notna()
        & data["P_emaildomain"].eq(
            data["R_emaildomain"]
        )
    ).astype("int8")

    return data


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--transaction", required=True)
    p.add_argument("--identity", required=True)
    p.add_argument(
        "--output",
        default="data/interim/ieee_features.pkl",
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()

    transactions = pd.read_csv(
        args.transaction,
        usecols=TRANSACTION_COLUMNS,
        low_memory=False,
    )
    identity = pd.read_csv(
        args.identity,
        usecols=IDENTITY_COLUMNS,
        low_memory=False,
    )

    features = build_features(
        transactions,
        identity,
    )

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    if output.suffix.lower() in {".pkl", ".pickle"}:
        features.to_pickle(output)
    else:
        features.to_csv(output, index=False)

    print(
        f"Wrote {output} with "
        f"{len(features):,} rows and "
        f"{features.shape[1]} columns"
    )
    print(
        "Unique entity proxies:",
        features["entity_proxy"].nunique(),
    )
    print(
        "Fraud rate:",
        features["isFraud"].mean(),
    )


if __name__ == "__main__":
    main()
