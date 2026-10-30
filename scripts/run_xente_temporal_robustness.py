"""Run expanding-window temporal robustness checks for the Xente baseline.

The full logistic specification is retrained on an expanding prefix and
assessed on the immediately following 10% chronological block. This is not a
hyperparameter-selection procedure; it is a temporal stability diagnostic.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    average_precision_score,
    brier_score_loss,
    roc_auc_score,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


NUMERIC_FEATURES = [
    "log_value",
    "is_credit",
    "hour",
    "weekday",
    "PricingStrategy",
    "log_prior_tx_count",
    "log_prior_value_mean",
    "log_prior_value_std",
    "log_gap_minutes",
    "log_tx_count_1h",
    "log_tx_count_24h",
    "log_tx_count_7d",
    "value_ratio_clip",
    "prior_product_share",
    "prior_channel_share",
]
CATEGORICAL_FEATURES = [
    "ProductCategory",
    "ChannelId",
    "ProviderId",
    "ProductId",
]


def build_model() -> Pipeline:
    numeric = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    preprocessor = ColumnTransformer(
        [
            ("numeric", numeric, NUMERIC_FEATURES),
            (
                "categorical",
                OneHotEncoder(handle_unknown="ignore"),
                CATEGORICAL_FEATURES,
            ),
        ]
    )
    return Pipeline(
        [
            ("preprocessor", preprocessor),
            (
                "classifier",
                LogisticRegression(
                    max_iter=2000,
                    C=0.5,
                    solver="liblinear",
                ),
            ),
        ]
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument(
        "--output-dir",
        default="outputs/local/temporal_robustness",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(args.input)
    df["TransactionStartTime"] = pd.to_datetime(
        df["TransactionStartTime"],
        utc=True,
        errors="raise",
    )
    df = df.sort_values(
        ["TransactionStartTime", "TransactionId"]
    ).reset_index(drop=True)
    features = NUMERIC_FEATURES + CATEGORICAL_FEATURES

    rows: list[dict] = []
    n = len(df)
    for train_fraction in (
        0.50,
        0.60,
        0.70,
        0.80,
        0.90,
    ):
        train_end = int(n * train_fraction)
        eval_end = int(
            n * min(train_fraction + 0.10, 1.0)
        )
        train = df.iloc[:train_end]
        evaluation = df.iloc[train_end:eval_end]

        model = build_model()
        model.fit(
            train[features],
            train["FraudResult"],
        )
        p = model.predict_proba(
            evaluation[features]
        )[:, 1]
        y = evaluation[
            "FraudResult"
        ].to_numpy(dtype=int)

        seen_train_customers = set(
            train["CustomerId"].astype(str)
        )
        seen = (
            evaluation["CustomerId"]
            .astype(str)
            .isin(seen_train_customers)
            .to_numpy()
        )

        rows.append(
            {
                "train_fraction": train_fraction,
                "train_rows": int(len(train)),
                "train_fraud": int(
                    train["FraudResult"].sum()
                ),
                "evaluation_rows": int(
                    len(evaluation)
                ),
                "evaluation_fraud": int(y.sum()),
                "evaluation_fraud_rate": float(
                    y.mean()
                ),
                "evaluation_start": str(
                    evaluation[
                        "TransactionStartTime"
                    ].min()
                ),
                "evaluation_end": str(
                    evaluation[
                        "TransactionStartTime"
                    ].max()
                ),
                "average_precision": float(
                    average_precision_score(y, p)
                ),
                "roc_auc": float(
                    roc_auc_score(y, p)
                ),
                "brier_score": float(
                    brier_score_loss(y, p)
                ),
                "unseen_transaction_share": float(
                    (~seen).mean()
                ),
                "unseen_fraud": int(
                    y[~seen].sum()
                ),
                "seen_fraud": int(
                    y[seen].sum()
                ),
            }
        )

    result = pd.DataFrame(rows)
    result.to_csv(
        output_dir
        / "expanding_window_metrics.csv",
        index=False,
    )
    (
        output_dir
        / "expanding_window_metrics.json"
    ).write_text(
        json.dumps(
            rows,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    print(result.to_string(index=False))


if __name__ == "__main__":
    main()
