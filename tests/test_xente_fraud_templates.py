import random

import pandas as pd

from scripts.xente_fraud_templates import (
    STRATEGIES,
    XenteFraudTemplateGenerator,
)


def sample_scores():
    values = [
        10, 20, 30,
        100, 110, 120,
        1000, 1100, 1200,
    ]
    return pd.DataFrame(
        {
            "Value": values,
            "FraudResult": [1] * len(values),
            "risk_probability": [
                0.01, 0.02, 0.03,
                0.10, 0.11, 0.12,
                0.80, 0.85, 0.90,
            ],
        }
    )


def test_builds_three_nonempty_regimes():
    generator = (
        XenteFraudTemplateGenerator
        .from_validation_scores(
            sample_scores()
        )
    )

    assert set(generator.pools) == set(
        STRATEGIES
    )
    assert all(
        len(generator.pools[name]) > 0
        for name in STRATEGIES
    )


def test_weights_sum_to_one():
    generator = (
        XenteFraudTemplateGenerator
        .from_validation_scores(
            sample_scores()
        )
    )

    assert abs(
        sum(generator.strategy_weights.values())
        - 1.0
    ) < 1e-12


def test_sampling_is_reproducible():
    generator = (
        XenteFraudTemplateGenerator
        .from_validation_scores(
            sample_scores()
        )
    )
    first = random.Random(5)
    second = random.Random(5)

    a = [
        generator.sample(
            "low_value",
            first,
        )
        for _ in range(10)
    ]
    b = [
        generator.sample(
            "low_value",
            second,
        )
        for _ in range(10)
    ]

    assert a == b
