"""Run Xente risk-model structural robustness checks.

Compares three intentionally different score generators on the same
chronological 70/15/15 split:

1. full_logistic: current Value + temporal/context + past-only customer history
2. no_current_value: removes the strongest current-transaction value signals
3. amount_only: deliberately simple current Value/sign baseline

The goal is not leaderboard optimization. It is to test whether downstream
policy conclusions depend on an unusually strong fraud score model.
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
from sklearn.metrics import average_precision_score, brier_score_loss, roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


FULL_NUMERIC = [
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
FULL_CATEGORICAL = ["ProductCategory", "ChannelId", "ProviderId", "ProductId"]
NO_CURRENT_VALUE_NUMERIC = [
    feature
    for feature in FULL_NUMERIC
    if feature not in {"log_value", "value_ratio_clip"}
]
AMOUNT_ONLY_NUMERIC = ["log_value", "is_credit"]

MODEL_SPECS = {
    "full_logistic": (FULL_NUMERIC, FULL_CATEGORICAL),
    "no_current_value": (NO_CURRENT_VALUE_NUMERIC, FULL_CATEGORICAL),
    "amount_only": (AMOUNT_ONLY_NUMERIC, []),
}


def build_model(
    numeric_features: list[str],
    categorical_features: list[str],
) -> Pipeline:
    transformers = []
    if numeric_features:
        numeric = Pipeline(
            [
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
            ]
        )
        transformers.append(("numeric", numeric, numeric_features))
    if categorical_features:
        transformers.append(
            (
                "categorical",
                OneHotEncoder(handle_unknown="ignore"),
                categorical_features,
            )
        )

    preprocessor = ColumnTransformer(transformers)
    classifier = LogisticRegression(max_iter=2000, C=0.5, solver="liblinear")
    return Pipeline(
        [("preprocessor", preprocessor), ("classifier", classifier)]
    )


def safe_metrics(y: np.ndarray, p: np.ndarray) -> dict[str, float | None]:
    out: dict[str, float | None] = {
        "average_precision": None,
        "roc_auc": None,
        "brier_score": None,
    }
    if len(y):
        out["brier_score"] = float(brier_score_loss(y, p))
    if len(y) and y.sum() > 0:
        out["average_precision"] = float(average_precision_score(y, p))
    if len(np.unique(y)) == 2:
        out["roc_auc"] = float(roc_auc_score(y, p))
    return out


def operating_points(y: np.ndarray, p: np.ndarray) -> list[dict]:
    rows = []
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


def evaluate_split(
    model_name: str,
    split_name: str,
    frame: pd.DataFrame,
    p: np.ndarray,
    seen_train_customers: set[str],
) -> tuple[list[dict], pd.DataFrame]:
    y = frame["FraudResult"].to_numpy(dtype=int)
    seen = (
        frame["CustomerId"]
        .astype(str)
        .isin(seen_train_customers)
        .to_numpy()
    )

    rows: list[dict] = []
    for subgroup_name, mask in [
        ("all", np.ones(len(frame), dtype=bool)),
        ("seen", seen),
        ("unseen", ~seen),
    ]:
        yy = y[mask]
        pp = p[mask]
        metrics = safe_metrics(yy, pp)
        rows.append(
            {
                "model": model_name,
                "split": split_name,
                "subgroup": subgroup_name,
                "rows": int(mask.sum()),
                "fraud": int(yy.sum()),
                "fraud_rate": float(yy.mean()) if len(yy) else None,
                "mean_predicted_probability": (
                    float(pp.mean()) if len(pp) else None
                ),
                **metrics,
            }
        )

    scored = frame[
        [
            "TransactionId",
            "CustomerId",
            "TransactionStartTime",
            "Value",
            "FraudResult",
            "prior_tx_count",
        ]
    ].copy()
    scored["risk_probability"] = p
    scored["seen_in_train_customer"] = seen.astype(int)

    all_row = next(row for row in rows if row["subgroup"] == "all")
    all_row["operating_points"] = operating_points(y, p)
    return rows, scored


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument(
        "--output-dir",
        default="outputs/local/model_robustness",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(args.input)
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
    validation = df.iloc[train_end:valid_end]
    test = df.iloc[valid_end:]
    seen_train_customers = set(train["CustomerId"].astype(str))

    metric_rows: list[dict] = []
    operating_point_rows: list[dict] = []

    for model_name, (
        numeric_features,
        categorical_features,
    ) in MODEL_SPECS.items():
        features = numeric_features + categorical_features
        model = build_model(numeric_features, categorical_features)
        model.fit(train[features], train["FraudResult"])

        for split_name, frame in [
            ("validation", validation),
            ("test", test),
        ]:
            p = model.predict_proba(frame[features])[:, 1]
            rows, scored = evaluate_split(
                model_name,
                split_name,
                frame,
                p,
                seen_train_customers,
            )
            for row in rows:
                ops = row.pop("operating_points", None)
                metric_rows.append(row)
                if ops:
                    for op in ops:
                        operating_point_rows.append(
                            {
                                "model": model_name,
                                "split": split_name,
                                **op,
                            }
                        )

            scored.to_csv(
                output_dir
                / f"{model_name}_{split_name}_scores.csv",
                index=False,
            )

    metrics = pd.DataFrame(metric_rows)
    operating_points_df = pd.DataFrame(operating_point_rows)
    metrics.to_csv(
        output_dir / "model_subgroup_metrics.csv",
        index=False,
    )
    operating_points_df.to_csv(
        output_dir / "operating_points.csv",
        index=False,
    )

    payload = {
        "split_rule": "chronological 70/15/15",
        "model_specs": {
            name: {
                "numeric": num,
                "categorical": cat,
            }
            for name, (num, cat) in MODEL_SPECS.items()
        },
        "metrics": metrics.to_dict(orient="records"),
        "operating_points": operating_points_df.to_dict(
            orient="records"
        ),
    }
    (
        output_dir / "model_robustness.json"
    ).write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(metrics.to_string(index=False))


if __name__ == "__main__":
    main()
