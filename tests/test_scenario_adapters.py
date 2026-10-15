import pandas as pd
import pytest

from scripts.scenario_adapters import (
    normalize_ieee_scores,
    normalize_xente_scores,
    validate_canonical_scores,
)


def test_xente_adapter_preserves_core_fields():
    df = pd.DataFrame(
        {
            "TransactionId": ["T1", "T2"],
            "TransactionStartTime": [
                "2026-01-01T00:00:00Z",
                "2026-01-01T01:00:00Z",
            ],
            "Value": [100, 200],
            "FraudResult": [0, 1],
            "risk_probability": [0.1, 0.9],
        }
    )

    out = normalize_xente_scores(df)
    validate_canonical_scores(out)

    assert out["TransactionId"].tolist() == ["T1", "T2"]
    assert out["Value"].tolist() == [100.0, 200.0]
    assert out["FraudResult"].tolist() == [0, 1]


def test_ieee_adapter_preserves_relative_order_and_intervals():
    df = pd.DataFrame(
        {
            "TransactionID": [10, 11, 12],
            "TransactionDT": [100, 160, 400],
            "TransactionAmt": [20.0, 30.0, 40.0],
            "isFraud": [0, 1, 0],
            "risk_probability": [0.05, 0.80, 0.10],
            "ProductCD": ["W", "C", "W"],
        }
    )

    out = normalize_ieee_scores(df)
    validate_canonical_scores(out)

    gaps = (
        out["TransactionStartTime"]
        .sort_values()
        .diff()
        .dropna()
        .dt.total_seconds()
        .tolist()
    )
    assert gaps == [60.0, 240.0]
    assert out["TransactionId"].tolist() == [10, 11, 12]
    assert out["Value"].tolist() == [20.0, 30.0, 40.0]
    assert out["FraudResult"].tolist() == [0, 1, 0]
    assert "ProductCD" in out.columns


def test_ieee_adapter_does_not_require_true_customer_id():
    df = pd.DataFrame(
        {
            "TransactionID": [1],
            "TransactionDT": [1],
            "TransactionAmt": [10.0],
            "isFraud": [0],
            "risk_probability": [0.1],
        }
    )

    out = normalize_ieee_scores(df)

    assert "CustomerId" not in out.columns
    validate_canonical_scores(out)


def test_adapter_rejects_invalid_probability():
    df = pd.DataFrame(
        {
            "TransactionID": [1],
            "TransactionDT": [1],
            "TransactionAmt": [10.0],
            "isFraud": [0],
            "risk_probability": [1.2],
        }
    )

    with pytest.raises(ValueError):
        normalize_ieee_scores(df)


def test_adapter_rejects_nonbinary_label():
    df = pd.DataFrame(
        {
            "TransactionID": [1],
            "TransactionDT": [1],
            "TransactionAmt": [10.0],
            "isFraud": [2],
            "risk_probability": [0.2],
        }
    )

    with pytest.raises(ValueError):
        normalize_ieee_scores(df)
