import pandas as pd
import pytest

from scripts.outcome_semantics import expected_outcomes_by_horizon


def data():
    decisions = pd.DataFrame({
        "TransactionId": ["approve", "block", "pending", "completed", "legit"],
        "FraudResult": [1, 1, 1, 1, 0],
        "Value": [100.0, 200.0, 300.0, 500.0, 600.0],
        "action": ["APPROVE", "BLOCK", "REVIEW", "REVIEW", "REVIEW"],
    })
    reviews = pd.DataFrame({
        "TransactionId": ["pending", "completed", "legit"],
        "service_end": ["2026-01-03T12:00Z", "2026-01-02T12:00Z", "2026-01-02T12:00Z"],
    })
    return decisions, reviews


def test_accounting_is_conservative_and_explicit():
    decisions, reviews = data()
    res = expected_outcomes_by_horizon(
        decisions, reviews, "2026-01-03T00:00Z",
        review_prevention_probability=0.5,
    )
    assert res["directly_blocked_fraud_value"] == 200
    assert res["review_completed_fraud_value"] == 500
    assert res["unresolved_fraud_value_at_horizon"] == 300
    assert res["expected_prevented_fraud_value_under_assumption"] == 450
    assert res["fraud_exposure_upper_bound_at_horizon_under_assumption"] == 650
    assert res["total_attempted_fraud_value"] == 1100


def test_q_sensitivity_and_no_reviews():
    decisions, reviews = data()
    result0 = expected_outcomes_by_horizon(decisions, reviews, "2026-01-03T00:00Z", review_prevention_probability=0)
    result1 = expected_outcomes_by_horizon(decisions, reviews, "2026-01-03T00:00Z", review_prevention_probability=1)
    assert result0["expected_prevented_fraud_value_under_assumption"] == 200
    assert result1["expected_prevented_fraud_value_under_assumption"] == 700
    assert result1["fraud_exposure_upper_bound_at_horizon_under_assumption"] == 400


def test_invalid_probability_or_duplicate_id_raises():
    d, r = data()
    with pytest.raises(ValueError, match=r"\[0,1\]"):
        expected_outcomes_by_horizon(d, r, "2026-01-03", review_prevention_probability=1.5)
    d.loc[1, "TransactionId"] = "approve"
    with pytest.raises(ValueError, match="unique"):
        expected_outcomes_by_horizon(d, r, "2026-01-03", review_prevention_probability=0.5)
