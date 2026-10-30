"""Memory-bounded chronological IEEE-CIS baseline.

This is the canonical executable baseline for Scenario B. It converts the
completed IEEE EDA/Data-to-ABM decisions into a streaming feature/state pipeline
without materializing a 590k-row wide feature table in memory.

Three passes over train_transaction.csv:
1. fit train-only frequency maps and categorical vocabularies;
2. fit train-only numeric scaling while replaying past-only entity history;
3. train SGD log-loss on the first 70%, then score the next/final 15%.

Boundary:
- card1+addr1 is an entity proxy, not a true customer;
- TransactionDT is relative time;
- masked C/D/M/V fields are detector context, not fraudster actions.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
import math
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from scipy import sparse
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import (
    average_precision_score,
    brier_score_loss,
    roc_auc_score,
)
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from scripts.build_ieee_features import (
    C_COLUMNS,
    D_COLUMNS,
    IDENTITY_CATEGORICAL,
    IDENTITY_NUMERIC,
    M_COLUMNS,
    SELECTED_V,
    TRANSACTION_COLUMNS,
)

FREQUENCY_COLUMNS = [
    "card1",
    "entity_proxy",
    "DeviceInfo",
    "id_31",
    "id_33",
    "P_emaildomain",
    "R_emaildomain",
]

LOW_CARD_CATEGORICAL = [
    "ProductCD",
    "card4",
    "card6",
    "DeviceType",
    *M_COLUMNS,
    "id_12",
    "id_15",
    "id_16",
]

NUMERIC_FEATURES = [
    "log_transaction_amt",
    "day_index",
    "hour_proxy",
    "addr1",
    "dist1",
    *C_COLUMNS,
    *D_COLUMNS,
    *SELECTED_V,
    *IDENTITY_NUMERIC,
    "identity_available",
    "identity_missing_count",
    "detector_missing_count",
    "email_both_missing",
    "email_match",
    "log_prior_tx_count",
    "log_prior_amount_mean",
    "log_prior_amount_std",
    "log_gap_seconds",
    "amount_ratio_clip",
    "prior_product_share",
    "cold_start_entity",
    *[f"freq_{column}" for column in FREQUENCY_COLUMNS],
]

IDENTITY_COLUMNS = [
    "TransactionID",
    *IDENTITY_NUMERIC,
    *IDENTITY_CATEGORICAL,
]


def count_rows(path: str) -> int:
    with open(path, "rb") as handle:
        return sum(1 for _ in handle) - 1


def load_identity(path: str) -> pd.DataFrame:
    identity = pd.read_csv(
        path,
        usecols=IDENTITY_COLUMNS,
        low_memory=False,
    )
    identity["identity_available"] = np.int8(1)
    return identity


def make_entity_proxy(
    card1: pd.Series,
    addr1: pd.Series,
) -> pd.Series:
    card = (
        pd.to_numeric(card1, errors="coerce")
        .round()
        .astype("Int64")
        .astype("string")
        .fillna("__MISSING_CARD1__")
    )
    addr = (
        pd.to_numeric(addr1, errors="coerce")
        .round()
        .astype("Int64")
        .astype("string")
        .fillna("__MISSING_ADDR1__")
    )
    return (card + "|" + addr).astype("string")


def join_identity(
    chunk: pd.DataFrame,
    identity: pd.DataFrame,
) -> pd.DataFrame:
    out = chunk.merge(
        identity,
        on="TransactionID",
        how="left",
        validate="many_to_one",
        sort=False,
    )
    out["identity_available"] = (
        out["identity_available"]
        .fillna(0)
        .astype("int8")
    )
    out["entity_proxy"] = make_entity_proxy(
        out["card1"],
        out["addr1"],
    )
    return out


def key_series(series: pd.Series) -> pd.Series:
    return (
        series.astype("string")
        .fillna("__MISSING__")
    )


class EntityHistoryState:
    """Past-only state for the card1+addr1 proxy."""

    def __init__(self) -> None:
        self.count = defaultdict(int)
        self.sum_amount = defaultdict(float)
        self.sumsq_amount = defaultdict(float)
        self.last_time: dict[str, int] = {}
        self.product_count = defaultdict(
            lambda: defaultdict(int)
        )

    def features_then_update(
        self,
        entities,
        amounts,
        times,
        products,
    ):
        n = len(entities)
        prior_count = np.empty(n, dtype=np.float32)
        prior_mean = np.full(
            n, np.nan, dtype=np.float32
        )
        prior_std = np.full(
            n, np.nan, dtype=np.float32
        )
        gap = np.full(
            n, np.nan, dtype=np.float32
        )
        prior_product_share = np.zeros(
            n, dtype=np.float32
        )

        for i, (entity, amount, time, product) in enumerate(
            zip(
                entities,
                amounts,
                times,
                products,
            )
        ):
            entity = str(entity)
            product = str(product)
            count = self.count[entity]
            prior_count[i] = count

            if count:
                mean = self.sum_amount[entity] / count
                variance = max(
                    self.sumsq_amount[entity]
                    / count
                    - mean * mean,
                    0.0,
                )
                prior_mean[i] = mean
                prior_std[i] = math.sqrt(variance)
                prior_product_share[i] = (
                    self.product_count[entity][product]
                    / count
                )
                if entity in self.last_time:
                    gap[i] = (
                        int(time)
                        - self.last_time[entity]
                    )

            self.count[entity] = count + 1
            self.sum_amount[entity] += float(amount)
            self.sumsq_amount[entity] += (
                float(amount) * float(amount)
            )
            self.last_time[entity] = int(time)
            self.product_count[entity][product] += 1

        return (
            prior_count,
            prior_mean,
            prior_std,
            gap,
            prior_product_share,
        )


def iter_chunks(
    transaction_path: str,
    identity: pd.DataFrame,
    chunksize: int,
):
    for chunk in pd.read_csv(
        transaction_path,
        usecols=TRANSACTION_COLUMNS,
        chunksize=chunksize,
        low_memory=False,
    ):
        yield join_identity(
            chunk,
            identity,
        )


def fit_train_metadata(
    transaction_path: str,
    identity: pd.DataFrame,
    train_end: int,
    chunksize: int,
):
    frequency_counts = {
        column: Counter()
        for column in FREQUENCY_COLUMNS
    }
    categories = {
        column: {"__MISSING__"}
        for column in LOW_CARD_CATEGORICAL
    }

    seen = 0
    for chunk in iter_chunks(
        transaction_path,
        identity,
        chunksize,
    ):
        if seen >= train_end:
            break

        take = min(
            len(chunk),
            train_end - seen,
        )
        part = chunk.iloc[:take]

        for column in FREQUENCY_COLUMNS:
            frequency_counts[column].update(
                key_series(part[column]).tolist()
            )

        for column in LOW_CARD_CATEGORICAL:
            categories[column].update(
                key_series(part[column])
                .unique()
                .tolist()
            )

        seen += take

    frequency_maps = {
        column: {
            key: count / train_end
            for key, count
            in counter.items()
        }
        for column, counter
        in frequency_counts.items()
    }

    category_lists = []
    for column in LOW_CARD_CATEGORICAL:
        values = sorted(
            str(value)
            for value in categories[column]
        )
        category_lists.append(values)

    return frequency_maps, category_lists


def build_chunk_features(
    part: pd.DataFrame,
    state: EntityHistoryState,
    frequency_maps: dict,
):
    amount = pd.to_numeric(
        part["TransactionAmt"],
        errors="coerce",
    ).to_numpy(dtype=float)
    transaction_dt = pd.to_numeric(
        part["TransactionDT"],
        errors="coerce",
    ).to_numpy(dtype=np.int64)
    products = (
        key_series(part["ProductCD"])
        .to_numpy()
    )
    entities = (
        part["entity_proxy"]
        .astype("string")
        .to_numpy()
    )

    (
        prior_count,
        prior_mean,
        prior_std,
        gap_seconds,
        prior_product_share,
    ) = state.features_then_update(
        entities,
        amount,
        transaction_dt,
        products,
    )

    numeric = pd.DataFrame(
        index=part.index
    )
    numeric["log_transaction_amt"] = np.log1p(
        np.clip(amount, 0, None)
    )
    numeric["day_index"] = (
        transaction_dt // 86400
    )
    numeric["hour_proxy"] = (
        transaction_dt % 86400
    ) / 3600.0
    numeric["addr1"] = pd.to_numeric(
        part["addr1"],
        errors="coerce",
    ).to_numpy()
    numeric["dist1"] = pd.to_numeric(
        part["dist1"],
        errors="coerce",
    ).to_numpy()

    for column in (
        C_COLUMNS
        + D_COLUMNS
        + SELECTED_V
        + IDENTITY_NUMERIC
    ):
        numeric[column] = pd.to_numeric(
            part[column],
            errors="coerce",
        ).to_numpy()

    numeric["identity_available"] = (
        part["identity_available"]
        .to_numpy(dtype=float)
    )
    numeric["identity_missing_count"] = (
        part[
            IDENTITY_NUMERIC
            + IDENTITY_CATEGORICAL
        ]
        .isna()
        .sum(axis=1)
        .to_numpy(dtype=float)
    )
    numeric["detector_missing_count"] = (
        part[
            C_COLUMNS
            + D_COLUMNS
            + M_COLUMNS
            + SELECTED_V
        ]
        .isna()
        .sum(axis=1)
        .to_numpy(dtype=float)
    )

    payer_email = part["P_emaildomain"]
    receiver_email = part["R_emaildomain"]
    numeric["email_both_missing"] = (
        payer_email.isna()
        & receiver_email.isna()
    ).to_numpy(dtype=float)
    numeric["email_match"] = (
        payer_email.notna()
        & receiver_email.notna()
        & payer_email.astype("string").eq(
            receiver_email.astype("string")
        )
    ).to_numpy(dtype=float)

    numeric["log_prior_tx_count"] = np.log1p(
        prior_count
    )
    numeric["log_prior_amount_mean"] = np.log1p(
        np.clip(prior_mean, 0, None)
    )
    numeric["log_prior_amount_std"] = np.log1p(
        np.clip(prior_std, 0, None)
    )
    numeric["log_gap_seconds"] = np.log1p(
        np.clip(gap_seconds, 0, None)
    )

    ratio = amount / prior_mean
    ratio[~np.isfinite(ratio)] = np.nan
    numeric["amount_ratio_clip"] = np.minimum(
        ratio,
        20,
    )
    numeric["prior_product_share"] = (
        prior_product_share
    )
    numeric["cold_start_entity"] = (
        prior_count == 0
    ).astype(float)

    for column in FREQUENCY_COLUMNS:
        numeric[f"freq_{column}"] = (
            key_series(part[column])
            .map(frequency_maps[column])
            .fillna(0.0)
            .to_numpy(dtype=float)
        )

    categorical = pd.DataFrame(
        {
            column: (
                key_series(part[column])
                .astype(str)
                .to_numpy()
            )
            for column in LOW_CARD_CATEGORICAL
        },
        index=part.index,
    )

    return (
        numeric[NUMERIC_FEATURES],
        categorical,
    )


def make_encoder(
    category_lists: list[list[str]],
) -> OneHotEncoder:
    encoder = OneHotEncoder(
        categories=category_lists,
        handle_unknown="ignore",
        sparse_output=True,
        dtype=np.float32,
    )
    dummy = pd.DataFrame(
        {
            column: [
                category_lists[i][0]
            ]
            for i, column
            in enumerate(
                LOW_CARD_CATEGORICAL
            )
        }
    )
    encoder.fit(dummy)
    return encoder


def make_matrix(
    numeric: pd.DataFrame,
    categorical: pd.DataFrame,
    scaler: StandardScaler,
    encoder: OneHotEncoder,
):
    numeric_matrix = scaler.transform(
        numeric.to_numpy(dtype=np.float64)
    )
    numeric_matrix = np.nan_to_num(
        numeric_matrix,
        nan=0.0,
        posinf=0.0,
        neginf=0.0,
    ).astype(np.float32)

    categorical_matrix = encoder.transform(
        categorical[
            LOW_CARD_CATEGORICAL
        ]
    )

    return sparse.hstack(
        [
            sparse.csr_matrix(
                numeric_matrix
            ),
            categorical_matrix,
        ],
        format="csr",
    )


def operating_points(
    y: np.ndarray,
    p: np.ndarray,
):
    rows = []
    positives = int(y.sum())

    for rate in (
        0.005,
        0.01,
        0.02,
        0.05,
    ):
        k = max(
            1,
            int(
                np.ceil(
                    len(y) * rate
                )
            ),
        )
        idx = np.argpartition(
            -p,
            k - 1,
        )[:k]
        true_positive = int(
            y[idx].sum()
        )
        rows.append(
            {
                "review_rate": rate,
                "reviewed": k,
                "true_fraud_reviewed": true_positive,
                "precision": (
                    true_positive / k
                ),
                "recall": (
                    true_positive / positives
                    if positives
                    else None
                ),
            }
        )

    return rows


def metrics(
    y: np.ndarray,
    p: np.ndarray,
):
    return {
        "rows": int(len(y)),
        "fraud": int(y.sum()),
        "fraud_rate": float(y.mean()),
        "average_precision": float(
            average_precision_score(
                y,
                p,
            )
        ),
        "roc_auc": float(
            roc_auc_score(
                y,
                p,
            )
        ),
        "brier_score": float(
            brier_score_loss(
                y,
                p,
            )
        ),
        "mean_predicted_probability": float(
            p.mean()
        ),
        "operating_points": operating_points(
            y,
            p,
        ),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--transaction",
        required=True,
    )
    parser.add_argument(
        "--identity",
        required=True,
    )
    parser.add_argument(
        "--output-dir",
        default=(
            "outputs/local/"
            "ieee_streaming_baseline"
        ),
    )
    parser.add_argument(
        "--chunksize",
        type=int,
        default=20_000,
    )
    parser.add_argument(
        "--alpha",
        type=float,
        default=1e-3,
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_dir = Path(
        args.output_dir
    )
    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    row_count = count_rows(
        args.transaction
    )
    train_end = int(
        row_count * 0.70
    )
    validation_end = int(
        row_count * 0.85
    )

    identity = load_identity(
        args.identity
    )

    (
        frequency_maps,
        category_lists,
    ) = fit_train_metadata(
        args.transaction,
        identity,
        train_end,
        args.chunksize,
    )

    encoder = make_encoder(
        category_lists
    )

    # Pass 2: fit numeric scaling on TRAIN only.
    scaler = StandardScaler()
    state = EntityHistoryState()
    seen = 0

    for part in iter_chunks(
        args.transaction,
        identity,
        args.chunksize,
    ):
        numeric, _ = build_chunk_features(
            part,
            state,
            frequency_maps,
        )

        if seen < train_end:
            take = min(
                len(part),
                train_end - seen,
            )
            scaler.partial_fit(
                numeric.iloc[:take]
                .to_numpy(dtype=np.float64)
            )

        seen += len(part)
        if seen >= train_end:
            break

    # Pass 3: train first 70%, then freeze model and score later periods.
    classifier = SGDClassifier(
        loss="log_loss",
        penalty="l2",
        alpha=args.alpha,
        max_iter=1,
        tol=None,
        average=True,
        random_state=0,
    )

    state = EntityHistoryState()
    seen = 0
    fitted = False

    validation_y = []
    validation_p = []
    test_y = []
    test_p = []
    validation_parts = []
    test_parts = []

    train_entities = set(
        frequency_maps[
            "entity_proxy"
        ]
    )

    for part in iter_chunks(
        args.transaction,
        identity,
        args.chunksize,
    ):
        numeric, categorical = (
            build_chunk_features(
                part,
                state,
                frequency_maps,
            )
        )

        start = seen
        end = seen + len(part)

        ranges = [
            (
                "train",
                start,
                min(
                    end,
                    train_end,
                ),
            ),
            (
                "validation",
                max(
                    start,
                    train_end,
                ),
                min(
                    end,
                    validation_end,
                ),
            ),
            (
                "test",
                max(
                    start,
                    validation_end,
                ),
                end,
            ),
        ]

        for split_name, global_start, global_end in ranges:
            if global_end <= global_start:
                continue

            local_start = (
                global_start - start
            )
            local_end = (
                global_end - start
            )

            matrix = make_matrix(
                numeric.iloc[
                    local_start:local_end
                ],
                categorical.iloc[
                    local_start:local_end
                ],
                scaler,
                encoder,
            )
            y = (
                part["isFraud"]
                .iloc[
                    local_start:local_end
                ]
                .to_numpy(dtype=int)
            )

            if split_name == "train":
                if not fitted:
                    classifier.partial_fit(
                        matrix,
                        y,
                        classes=np.array(
                            [0, 1]
                        ),
                    )
                    fitted = True
                else:
                    classifier.partial_fit(
                        matrix,
                        y,
                    )
                continue

            probability = (
                classifier.predict_proba(
                    matrix
                )[:, 1]
            )

            scored = part.iloc[
                local_start:local_end
            ][
                [
                    "TransactionID",
                    "TransactionDT",
                    "TransactionAmt",
                    "isFraud",
                    "entity_proxy",
                    "ProductCD",
                    "card1",
                    "addr1",
                    "DeviceType",
                    "DeviceInfo",
                ]
            ].copy()
            scored[
                "risk_probability"
            ] = probability
            scored[
                "seen_in_train_entity"
            ] = (
                scored["entity_proxy"]
                .astype(str)
                .isin(train_entities)
                .astype("int8")
            )

            if split_name == "validation":
                validation_parts.append(
                    scored
                )
                validation_y.append(y)
                validation_p.append(
                    probability
                )
            else:
                test_parts.append(
                    scored
                )
                test_y.append(y)
                test_p.append(
                    probability
                )

        seen = end

    validation_y_array = np.concatenate(
        validation_y
    )
    validation_p_array = np.concatenate(
        validation_p
    )
    test_y_array = np.concatenate(
        test_y
    )
    test_p_array = np.concatenate(
        test_p
    )

    pd.concat(
        validation_parts,
        ignore_index=True,
    ).to_csv(
        output_dir
        / "validation_scores.csv",
        index=False,
    )
    pd.concat(
        test_parts,
        ignore_index=True,
    ).to_csv(
        output_dir
        / "test_scores.csv",
        index=False,
    )

    results = {
        "validation": metrics(
            validation_y_array,
            validation_p_array,
        ),
        "test": metrics(
            test_y_array,
            test_p_array,
        ),
    }

    payload = {
        "split_rule": (
            "chronological 70/15/15"
        ),
        "entity_proxy": (
            "card1+addr1"
        ),
        "model": (
            "streaming SGD log-loss"
        ),
        "alpha": args.alpha,
        "numeric_features": (
            NUMERIC_FEATURES
        ),
        "categorical_features": (
            LOW_CARD_CATEGORICAL
        ),
        "results": results,
    }

    (
        output_dir / "metrics.json"
    ).write_text(
        json.dumps(
            payload,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    joblib.dump(
        {
            "classifier": classifier,
            "scaler": scaler,
            "encoder": encoder,
            "frequency_maps": (
                frequency_maps
            ),
            "category_lists": (
                category_lists
            ),
            "numeric_features": (
                NUMERIC_FEATURES
            ),
            "categorical_features": (
                LOW_CARD_CATEGORICAL
            ),
            "entity_proxy": (
                "card1+addr1"
            ),
            "alpha": args.alpha,
        },
        output_dir
        / "model_bundle.joblib",
    )

    print(
        json.dumps(
            results,
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
