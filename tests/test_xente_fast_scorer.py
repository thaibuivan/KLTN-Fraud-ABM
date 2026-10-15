import numpy as np
import pandas as pd

from scripts.build_xente_features import (
    build_features,
)
from scripts.train_xente_baseline import (
    CATEGORICAL_FEATURES,
    NUMERIC_FEATURES,
    build_model,
)
from scripts.run_xente_model_robustness import (
    build_model as build_variant_model,
    NO_CURRENT_VALUE_NUMERIC,
    AMOUNT_ONLY_NUMERIC,
)
from scripts.xente_fast_scorer import (
    FastXenteLogisticScorer,
)


def synthetic_training():
    rows = []
    for i in range(80):
        rows.append(
            {
                "TransactionId": f"T{i}",
                "CustomerId": f"C{i % 8}",
                "Amount": float(
                    (i + 1)
                    * (-1 if i % 7 == 0 else 1)
                ),
                "Value": float(i + 1),
                "TransactionStartTime": (
                    pd.Timestamp(
                        "2026-01-01T00:00:00Z"
                    )
                    + pd.Timedelta(
                        minutes=15 * i
                    )
                ),
                "ProductCategory": (
                    "A" if i % 2 else "B"
                ),
                "ChannelId": (
                    "CH1" if i % 3 else "CH2"
                ),
                "ProviderId": (
                    "P1" if i % 4 else "P2"
                ),
                "ProductId": (
                    "X" if i % 5 else "Y"
                ),
                "PricingStrategy": i % 3,
                "FraudResult": int(
                    i in {
                        12,
                        25,
                        38,
                        51,
                        64,
                        77,
                    }
                ),
            }
        )
    return pd.DataFrame(rows)


def test_fast_scorer_matches_pipeline():
    features = build_features(
        synthetic_training()
    )

    model = build_model()
    x = features[
        NUMERIC_FEATURES
        + CATEGORICAL_FEATURES
    ]
    y = features["FraudResult"]
    model.fit(x, y)

    scorer = FastXenteLogisticScorer(
        model
    )

    sample = features.iloc[
        [3, 14, 31, 55, 79]
    ]

    expected = model.predict_proba(
        sample[
            NUMERIC_FEATURES
            + CATEGORICAL_FEATURES
        ]
    )[:, 1]

    actual = np.asarray(
        [
            scorer.predict_proba_one(
                row
            )
            for row in sample.to_dict(
                "records"
            )
        ]
    )

    assert np.allclose(
        expected,
        actual,
        rtol=1e-12,
        atol=1e-12,
    )


def test_fast_scorer_matches_no_current_value_variant():
    features = build_features(
        synthetic_training()
    )
    model = build_variant_model(
        NO_CURRENT_VALUE_NUMERIC,
        CATEGORICAL_FEATURES,
    )
    x = features[
        NO_CURRENT_VALUE_NUMERIC
        + CATEGORICAL_FEATURES
    ]
    y = features["FraudResult"]
    model.fit(x, y)

    scorer = FastXenteLogisticScorer(model)
    sample = features.iloc[[5, 18, 41, 73]]
    expected = model.predict_proba(
        sample[
            NO_CURRENT_VALUE_NUMERIC
            + CATEGORICAL_FEATURES
        ]
    )[:, 1]
    actual = np.asarray(
        [
            scorer.predict_proba_one(row)
            for row in sample.to_dict("records")
        ]
    )

    assert np.allclose(
        expected,
        actual,
        rtol=1e-12,
        atol=1e-12,
    )


def test_fast_scorer_matches_amount_only_variant():
    features = build_features(
        synthetic_training()
    )
    model = build_variant_model(
        AMOUNT_ONLY_NUMERIC,
        [],
    )
    x = features[AMOUNT_ONLY_NUMERIC]
    y = features["FraudResult"]
    model.fit(x, y)

    scorer = FastXenteLogisticScorer(model)
    sample = features.iloc[[1, 21, 44, 70]]
    expected = model.predict_proba(
        sample[AMOUNT_ONLY_NUMERIC]
    )[:, 1]
    actual = np.asarray(
        [
            scorer.predict_proba_one(row)
            for row in sample.to_dict("records")
        ]
    )

    assert np.allclose(
        expected,
        actual,
        rtol=1e-12,
        atol=1e-12,
    )
