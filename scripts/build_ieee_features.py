"""Build a memory-conscious, leakage-safe IEEE-CIS feature table.

This is the executable implementation of decisions already made in the completed
IEEE-CIS EDA. It does not redo EDA.

Core boundary:
- card1+addr1 is an entity proxy, never called a true customer;
- TransactionDT is relative time;
- masked C/D/M/V fields may feed Detection but are not interpreted as actions;
- history features use only earlier events for the proxy entity.
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
    "card1",
    "card4",
    "card6",
    "addr1",
    "dist1",
    "P_emaildomain",
    "R_emaildomain",
    *C_COLUMNS,
    *D_COLUMNS,
    *M_COLUMNS,
    *SELECTED_V,
]

IDENTITY_NUMERIC = [
    "id_01", "id_02", "id_05", "id_06",
]
IDENTITY_CATEGORICAL = [
    "id_12", "id_15", "id_16",
    "id_31", "id_33",
    "DeviceType", "DeviceInfo",
]
IDENTITY_COLUMNS = [
    "TransactionID",
    *IDENTITY_NUMERIC,
    *IDENTITY_CATEGORICAL,
]

TRANSACTION_DTYPES: dict[str, str] = {
    "TransactionID": "int64",
    "isFraud": "int8",
    "TransactionDT": "int64",
    "TransactionAmt": "float32",
    "card1": "float32",
    "addr1": "float32",
    "dist1": "float32",
}
for column in C_COLUMNS + D_COLUMNS + SELECTED_V:
    TRANSACTION_DTYPES[column] = "float32"
for column in [
    "ProductCD", "card4", "card6",
    "P_emaildomain", "R_emaildomain",
    *M_COLUMNS,
]:
    TRANSACTION_DTYPES[column] = "category"

IDENTITY_DTYPES: dict[str, str] = {
    "TransactionID": "int64",
}
for column in IDENTITY_NUMERIC:
    IDENTITY_DTYPES[column] = "float32"
for column in IDENTITY_CATEGORICAL:
    IDENTITY_DTYPES[column] = "category"


def make_entity_proxy(
    card1: pd.Series,
    addr1: pd.Series,
) -> pd.Series:
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
    return (card + "|" + addr).astype("category")


def build_features(
    transactions: pd.DataFrame,
    identity: pd.DataFrame,
) -> pd.DataFrame:
    identity = identity.copy()
    identity["identity_available"] = np.int8(1)

    data = transactions.merge(
        identity,
        on="TransactionID",
        how="left",
        validate="one_to_one",
        sort=False,
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

    data["entity_proxy"] = make_entity_proxy(
        data["card1"],
        data["addr1"],
    )

    data["day_index"] = (
        data["TransactionDT"] // 86400
    ).astype("int16")
    data["hour_proxy"] = (
        (data["TransactionDT"] % 86400) / 3600.0
    ).astype("float32")
    data["log_transaction_amt"] = np.log1p(
        data["TransactionAmt"].clip(lower=0)
    ).astype("float32")

    proxy = data["entity_proxy"]
    data["prior_tx_count"] = (
        data.groupby(
            "entity_proxy",
            sort=False,
            observed=True,
        ).cumcount()
        .astype("int32")
    )

    amount = data["TransactionAmt"].astype("float64")
    prior_sum = (
        amount.groupby(
            proxy,
            sort=False,
            observed=True,
        ).cumsum()
        - amount
    )
    amount_sq = amount * amount
    prior_sumsq = (
        amount_sq.groupby(
            proxy,
            sort=False,
            observed=True,
        ).cumsum()
        - amount_sq
    )

    count = data["prior_tx_count"].astype("float64")
    prior_mean = np.where(
        count > 0,
        prior_sum / count,
        np.nan,
    )
    prior_var = np.where(
        count > 0,
        prior_sumsq / count - prior_mean**2,
        np.nan,
    )

    data["prior_amount_mean"] = prior_mean.astype("float32")
    data["prior_amount_std"] = np.sqrt(
        np.maximum(prior_var, 0)
    ).astype("float32")

    data["gap_seconds"] = (
        data.groupby(
            "entity_proxy",
            sort=False,
            observed=True,
        )["TransactionDT"]
        .diff()
        .astype("float32")
    )

    same_product = (
        data.groupby(
            ["entity_proxy", "ProductCD"],
            sort=False,
            observed=True,
        ).cumcount()
    )
    data["prior_product_share"] = np.where(
        data["prior_tx_count"] > 0,
        same_product / data["prior_tx_count"],
        0.0,
    ).astype("float32")

    data["log_prior_tx_count"] = np.log1p(
        data["prior_tx_count"]
    ).astype("float32")
    data["log_prior_amount_mean"] = np.log1p(
        data["prior_amount_mean"].clip(lower=0)
    ).astype("float32")
    data["log_prior_amount_std"] = np.log1p(
        data["prior_amount_std"].clip(lower=0)
    ).astype("float32")
    data["log_gap_seconds"] = np.log1p(
        data["gap_seconds"].clip(lower=0)
    ).astype("float32")

    ratio = (
        data["TransactionAmt"]
        / data["prior_amount_mean"]
    ).replace([np.inf, -np.inf], np.nan)
    data["amount_ratio_clip"] = ratio.clip(
        upper=20
    ).astype("float32")

    data["cold_start_entity"] = (
        data["prior_tx_count"].eq(0).astype("int8")
    )

    identity_features = [
        column
        for column in IDENTITY_COLUMNS
        if column != "TransactionID"
    ]
    data["identity_missing_count"] = (
        data[identity_features]
        .isna()
        .sum(axis=1)
        .astype("int8")
    )

    detector_context = (
        C_COLUMNS
        + D_COLUMNS
        + M_COLUMNS
        + SELECTED_V
    )
    data["detector_missing_count"] = (
        data[detector_context]
        .isna()
        .sum(axis=1)
        .astype("int8")
    )

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
    parser = argparse.ArgumentParser()
    parser.add_argument("--transaction", required=True)
    parser.add_argument("--identity", required=True)
    parser.add_argument(
        "--output",
        default="data/interim/ieee_features.pkl",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    transactions = pd.read_csv(
        args.transaction,
        usecols=TRANSACTION_COLUMNS,
        dtype=TRANSACTION_DTYPES,
        low_memory=False,
    )
    identity = pd.read_csv(
        args.identity,
        usecols=IDENTITY_COLUMNS,
        dtype=IDENTITY_DTYPES,
        low_memory=False,
    )

    features = build_features(
        transactions,
        identity,
    )

    output = Path(args.output)
    output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    if output.suffix.lower() in {".pkl", ".pickle"}:
        features.to_pickle(output)
    else:
        features.to_csv(output, index=False)

    print(
        f"Wrote {output}: "
        f"{len(features):,} rows × "
        f"{features.shape[1]} columns"
    )
    print(
        "unique_entity_proxies=",
        features["entity_proxy"].nunique(),
    )
    print(
        "fraud_rate=",
        features["isFraud"].mean(),
    )


if __name__ == "__main__":
    main()
