"""Train an interpretable chronological Xente risk-model baseline.

This is a thesis baseline, not a production fraud model.

Usage:
    python scripts/train_xente_baseline.py \
        --input data/interim/xente_features.csv \
        --output-dir outputs/local/xente_baseline
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
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


def operating_points(y: np.ndarray, p: np.ndarray) -> list[dict]:
    rows: list[dict] = []
    positives = int(y.sum())
    for review_rate in (0.005, 0.01, 0.02, 0.05):
        k = max(1, int(len(y) * review_rate))
        idx = np.argpartition(-p, k - 1)[:k]
        tp = int(y[idx].sum())
        rows.append(
            {
                "review_rate": review_rate,
                "reviewed": k,
                "true_fraud_reviewed": tp,
                "precision": tp / k,
                "recall": tp / positives if positives else None,
            }
        )
    return rows


def evaluate(name: str, frame: pd.DataFrame, model: Pipeline) -> dict:
    x = frame[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
    y = frame["FraudResult"].to_numpy(dtype=int)
    p = model.predict_proba(x)[:, 1]
    return {
        "split": name,
        "rows": int(len(frame)),
        "fraud": int(y.sum()),
        "fraud_rate": float(y.mean()),
        "average_precision": float(average_precision_score(y, p)),
        "roc_auc": float(roc_auc_score(y, p)),
        "brier_score": float(brier_score_loss(y, p)),
        "mean_predicted_probability": float(p.mean()),
        "operating_points": operating_points(y, p),
    }


def build_model() -> Pipeline:
    numeric = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    categorical = OneHotEncoder(handle_unknown="ignore")

    preprocessor = ColumnTransformer(
        [
            ("numeric", numeric, NUMERIC_FEATURES),
            ("categorical", categorical, CATEGORICAL_FEATURES),
        ]
    )

    classifier = LogisticRegression(
        max_iter=2000,
        C=0.5,
        solver="liblinear",
    )

    return Pipeline(
        [
            ("preprocessor", preprocessor),
            ("classifier", classifier),
        ]
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument(
        "--output-dir", default="outputs/local/xente_baseline"
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_path = Path(args.input)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(input_path)
    df["TransactionStartTime"] = pd.to_datetime(
        df["TransactionStartTime"], utc=True, errors="raise"
    )
    df = df.sort_values(
        ["TransactionStartTime", "TransactionId"]
    ).reset_index(drop=True)

    n = len(df)
    train_end = int(n * 0.70)
    valid_end = int(n * 0.85)

    train = df.iloc[:train_end]
    valid = df.iloc[train_end:valid_end]
    test = df.iloc[valid_end:]

    model = build_model()
    model.fit(
        train[NUMERIC_FEATURES + CATEGORICAL_FEATURES],
        train["FraudResult"],
    )

    metrics = {
        "split_rule": "chronological 70/15/15",
        "features": {
            "numeric": NUMERIC_FEATURES,
            "categorical": CATEGORICAL_FEATURES,
        },
        "results": [
            evaluate("train", train, model),
            evaluate("validation", valid, model),
            evaluate("test", test, model),
        ],
    }

    path = output_dir / "metrics.json"
    path.write_text(
        json.dumps(metrics, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
