import random

import pandas as pd
import pytest

from scripts.ieee_feature_level_fraud import (
    IEEEFeatureLevelFraudGenerator,
    STRATEGIES,
)


def donors():
    amounts = [10, 15, 20, 30, 35, 40, 70, 80, 90, 130, 160, 200]
    data = pd.DataFrame({
        "TransactionID": range(100, 112),
        "TransactionDT": range(200, 212),
        "TransactionAmt": amounts,
        "ProductCD": ["W", "C"] * 6,
        "card1": range(1000, 1012),
        "addr1": [100.0] * 12,
        "isFraud": [1] * 12,
        "V1": list(range(12)),
        "DeviceType": ["mobile", "desktop"] * 6,
    })
    return data


def test_generator_keeps_entire_validation_donor_context():
    validation = donors()
    gen = IEEEFeatureLevelFraudGenerator.from_validation_raw(validation)
    assert set(gen.strategies) == set(STRATEGIES)
    assert abs(sum(gen.strategy_weights.values()) - 1) < 1e-12
    for j, strategy in enumerate(gen.strategies):
        event = gen.sample_raw(strategy, random.Random(3), 10_000 + j, j)
        donor = validation.loc[validation["card1"].eq(event["card1"])].iloc[0]
        assert event["TransactionAmt"] == donor["TransactionAmt"]
        assert event["V1"] == donor["V1"]
        assert event["DeviceType"] == donor["DeviceType"]
        assert event["TransactionID"] == -1 - j
        assert event["TransactionDT"] == 10_000 + j
        assert event["isFraud"] == 1


def test_generator_never_resamples_legitimate_validation_rows():
    data = donors()
    legit = data.iloc[[0]].copy()
    legit["TransactionID"] = 999
    legit["isFraud"] = 0
    legit["TransactionAmt"] = 999_999
    gen = IEEEFeatureLevelFraudGenerator.from_validation_raw(
        pd.concat([data, legit], ignore_index=True)
    )
    values = [v for pool in gen.pools.values() for v in pool["TransactionAmt"]]
    assert 999_999 not in values


def test_generator_rejects_empty_or_degenerate_regime():
    with pytest.raises(ValueError, match="nine"):
        IEEEFeatureLevelFraudGenerator.from_validation_raw(donors().iloc[:8])
    data = donors()
    data["TransactionAmt"] = 10
    with pytest.raises(ValueError, match="degenerate"):
        IEEEFeatureLevelFraudGenerator.from_validation_raw(data)


def test_reproducibility_and_fail_closed():
    gen = IEEEFeatureLevelFraudGenerator.from_validation_raw(donors())
    a = gen.sample_raw("low_amount", random.Random(9), 1000, 0)
    b = gen.sample_raw("low_amount", random.Random(9), 1000, 0)
    assert a == b
    with pytest.raises(ValueError, match="Unknown strategy"):
        gen.sample_raw("fake", random.Random(1), 1000, 0)
    with pytest.raises(ValueError, match="non-negative"):
        gen.sample_raw("low_amount", random.Random(1), -1, 0)
