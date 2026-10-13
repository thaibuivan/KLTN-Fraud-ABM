"""Train the first chronological IEEE-CIS risk baseline for Scenario B.

The goal is a stable probability score for policy simulation, not Kaggle
leaderboard optimization.

Design boundaries inherited from the completed EDA:
- card1+addr1 is an entity proxy, not a true CustomerId;
- high-cardinality identifiers are frequency-encoded using TRAIN ONLY;
- low-cardinality context is one-hot encoded;
- masked C/D/M/V fields support Detection but are not interpreted causally;
- chronological 70/15/15 validation is used.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import joblib
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
from sklearn.preprocessing import (
    OneHotEncoder,
    StandardScaler,
)

from scripts.build_ieee_features import (
    C_COLUMNS,
    D_COLUMNS,
    IDENTITY_NUMERIC,
    M_COLUMNS,
    SELECTED_V,
)


BASE_NUMERIC = [
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
]

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
    "id_28",
    "id_29",
    "id_34",
    "id_35",
    "id_36",
    "id_37",
    "id_38",
]


def load_features(path: str) -> pd.DataFrame:
    p = Path(path)
    if p.suffix.lower() in {".pkl", ".pickle"}:
        return pd.read_pickle(p)
    return pd.read_csv(p, low_memory=False)


def fit_frequency_maps(
    train: pd.DataFrame,
) -> dict[str, dict]:
    maps: dict[str, dict] = {}
    n = len(train)
    for column in FREQUENCY_COLUMNS:
        key = train[column].astype("string").fillna(
            "__MISSING__"
        )
        maps[column] = (
            key.value_counts(dropna=False)
            .div(n)
            .to_dict()
        )
    return maps


def apply_frequency_maps(
    frame: pd.DataFrame,
    maps: dict[str, dict],
) -> pd.DataFrame:
    out = frame.copy()
    for column, mapping in maps.items():
        key = out[column].astype("string").fillna(
            "__MISSING__"
        )
        out[f"freq_{column}"] = (
            key.map(mapping).fillna(0.0).astype(float)
        )
    return out


def build_model(
    numeric_features: list[str],
    categorical_features: list[str],
) -> Pipeline:
    numeric = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    categorical = Pipeline(
        [
            (
                "imputer",
                SimpleImputer(
                    strategy="constant",
                    fill_value="__MISSING__",
                ),
            ),
            (
                "onehot",
                OneHotEncoder(
                    handle_unknown="ignore",
                    min_frequency=100,
                ),
            ),
        ]
    )

    preprocessor = ColumnTransformer(
        [
            ("numeric", numeric, numeric_features),
            (
                "categorical",
                categorical,
                categorical_features,
            ),
        ]
    )

    classifier = LogisticRegression(
        max_iter=500,
        C=0.5,
        solver="saga",
        tol=1e-4,
        random_state=0,
    )

    return Pipeline(
        [
            ("preprocessor", preprocessor),
            ("classifier", classifier),
        ]
    )


def operating_points(
    y: np.ndarray,
    p: np.ndarray,
) -> list[dict]:
    rows = []
    positives = int(y.sum())
    for rate in (0.005, 0.01, 0.02, 0.05):
        k = max(1, int(np.ceil(len(y) * rate)))
        idx = np.argpartition(-p, k - 1)[:k]
        tp = int(y[idx].sum())
        rows.append(
            {
                "review_rate": rate,
                "reviewed": k,
                "true_fraud_reviewed": tp,
                "precision": tp / k,
                "recall": (
                    tp / positives
                    if positives
                    else None
                ),
            }
        )
    return rows


def safe_metrics(
    y: np.ndarray,
    p: np.ndarray,
) -> dict:
    return {
        "rows": int(len(y)),
        "fraud": int(y.sum()),
        "fraud_rate": float(y.mean()),
        "average_precision": float(
            average_precision_score(y, p)
        ),
        "roc_auc": float(
            roc_auc_score(y, p)
        ),
        "brier_score": float(
            brier_score_loss(y, p)
        ),
        "mean_predicted_probability": float(
            p.mean()
        ),
        "operating_points": operating_points(
            y,
            p,
        ),
    }


def score_frame(
    frame: pd.DataFrame,
    model: Pipeline,
    model_features: list[str],
    seen_train_entities: set[str],
) -> tuple[dict, pd.DataFrame]:
    y = frame["isFraud"].to_numpy(dtype=int)
    p = model.predict_proba(
        frame[model_features]
    )[:, 1]

    metrics = safe_metrics(y, p)

    scored_columns = [
        "TransactionID",
        "TransactionDT",
        "TransactionAmt",
        "isFraud",
        "entity_proxy",
        "prior_tx_count",
        "ProductCD",
        "card1",
        "addr1",
        "DeviceType",
        "DeviceInfo",
    ]
    scored = frame[scored_columns].copy()
    scored["risk_probability"] = p
    scored["seen_in_train_entity"] = (
        scored["entity_proxy"]
        .astype(str)
        .isin(seen_train_entities)
        .astype("int8")
    )

    return metrics, scored


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument(
        "--output-dir",
        default="outputs/local/ieee_baseline",
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    df = load_features(args.input)
    df = df.sort_values(
        ["TransactionDT", "TransactionID"],
        kind="stable",
    ).reset_index(drop=True)

    n = len(df)
    train_end = int(n * 0.70)
    valid_end = int(n * 0.85)

    train_raw = df.iloc[:train_end].copy()
    valid_raw = df.iloc[train_end:valid_end].copy()
    test_raw = df.iloc[valid_end:].copy()

    freq_maps = fit_frequency_maps(train_raw)
    train = apply_frequency_maps(
        train_raw,
        freq_maps,
    )
    valid = apply_frequency_maps(
        valid_raw,
        freq_maps,
    )
    test = apply_frequency_maps(
        test_raw,
        freq_maps,
    )

    numeric_features = (
        BASE_NUMERIC
        + [
            f"freq_{column}"
            for column in FREQUENCY_COLUMNS
        ]
    )
    categorical_features = LOW_CARD_CATEGORICAL
    model_features = (
        numeric_features
        + categorical_features
    )

    model = build_model(
        numeric_features,
        categorical_features,
    )
    model.fit(
        train[model_features],
        train["isFraud"],
    )

    seen_train_entities = set(
        train_raw["entity_proxy"].astype(str)
    )

    results = {}
    for split_name, frame in [
        ("validation", valid),
        ("test", test),
    ]:
        metrics, scored = score_frame(
            frame,
            model,
            model_features,
            seen_train_entities,
        )
        results[split_name] = metrics
        scored.to_csv(
            output_dir
            / f"{split_name}_scores.csv",
            index=False,
        )

    bundle = {
        "model": model,
        "frequency_maps": freq_maps,
        "numeric_features": numeric_features,
        "categorical_features": categorical_features,
        "model_features": model_features,
        "split_rule": "chronological 70/15/15",
        "entity_proxy": "card1+addr1",
    }
    joblib.dump(
        bundle,
        output_dir / "model_bundle.joblib",
    )

    payload = {
        "split_rule": "chronological 70/15/15",
        "entity_proxy": "card1+addr1",
        "frequency_columns": FREQUENCY_COLUMNS,
        "numeric_features": numeric_features,
        "categorical_features": categorical_features,
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

    print(
        json.dumps(
            payload["results"],
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
