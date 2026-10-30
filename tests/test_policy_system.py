import pandas as pd

from scripts.fraud_policies import (
    Action,
    FixedThresholdPolicy,
)
from scripts.simulate_policy_system import simulate_policy_system


def scored_frame():
    t0 = pd.Timestamp("2026-01-01T00:00:00Z")
    return pd.DataFrame(
        [
            {
                "TransactionId": "T1",
                "CustomerId": "C1",
                "TransactionStartTime": t0,
                "Value": 100.0,
                "FraudResult": 0,
                "risk_probability": 0.10,
            },
            {
                "TransactionId": "T2",
                "CustomerId": "C2",
                "TransactionStartTime": t0 + pd.Timedelta(minutes=1),
                "Value": 200.0,
                "FraudResult": 1,
                "risk_probability": 0.60,
            },
            {
                "TransactionId": "T3",
                "CustomerId": "C3",
                "TransactionStartTime": t0 + pd.Timedelta(minutes=2),
                "Value": 300.0,
                "FraudResult": 1,
                "risk_probability": 0.95,
            },
        ]
    )


def test_fixed_policy_routes_without_using_fraud_label():
    df = scored_frame()
    policy = FixedThresholdPolicy(0.40, 0.90)

    summary_a, decisions_a, _ = simulate_policy_system(
        df,
        policy,
        pooled_service_rate_per_hour=60.0,
        discipline="fifo",
    )

    swapped = df.copy()
    swapped["FraudResult"] = 1 - swapped["FraudResult"]
    _, decisions_b, _ = simulate_policy_system(
        swapped,
        policy,
        pooled_service_rate_per_hour=60.0,
        discipline="fifo",
    )

    assert decisions_a["action"].tolist() == [
        Action.APPROVE.value,
        Action.REVIEW.value,
        Action.BLOCK.value,
    ]
    assert decisions_a["action"].tolist() == decisions_b["action"].tolist()
    assert summary_a["review_count"] == 1


def test_blocked_and_approved_transactions_never_enter_review_queue():
    df = scored_frame()
    policy = FixedThresholdPolicy(0.40, 0.90)

    _, _, reviews = simulate_policy_system(
        df,
        policy,
        pooled_service_rate_per_hour=60.0,
        discipline="fifo",
    )

    assert reviews["TransactionId"].tolist() == ["T2"]


def test_review_never_starts_before_alert_arrival():
    df = scored_frame()
    policy = FixedThresholdPolicy(0.0, 1.0)

    _, _, reviews = simulate_policy_system(
        df,
        policy,
        pooled_service_rate_per_hour=2.0,
        discipline="fifo",
        horizon_end=df["TransactionStartTime"].max()
        + pd.Timedelta(hours=2),
    )

    assert (reviews["service_start"] >= reviews["arrival"]).all()


def test_zero_capacity_creates_backlog_and_unresolved_fraud_exposure():
    df = scored_frame()
    policy = FixedThresholdPolicy(0.0, 1.0)

    summary, _, reviews = simulate_policy_system(
        df,
        policy,
        pooled_service_rate_per_hour=0.0,
        discipline="fifo",
    )

    assert reviews.empty
    assert summary["review_count"] == 3
    assert summary["backlog_end"] == 3
    assert summary["unresolved_fraud_count"] == 2
    assert summary["unresolved_fraud_value"] == 500.0
    assert summary["fraud_exposure_at_horizon"] == 500.0


def test_high_capacity_removes_backlog():
    df = scored_frame()
    policy = FixedThresholdPolicy(0.0, 1.0)

    summary, _, _ = simulate_policy_system(
        df,
        policy,
        pooled_service_rate_per_hour=120.0,
        discipline="fifo",
        horizon_end=df["TransactionStartTime"].max()
        + pd.Timedelta(minutes=10),
    )

    assert summary["backlog_end"] == 0
    assert summary["fraud_exposure_at_horizon"] == 0.0


def test_fraud_intercept_counts_block_or_review_started_in_horizon():
    df = scored_frame()
    policy = FixedThresholdPolicy(0.40, 0.90)

    summary, _, _ = simulate_policy_system(
        df,
        policy,
        pooled_service_rate_per_hour=60.0,
        discipline="fifo",
        horizon_end=df["TransactionStartTime"].max()
        + pd.Timedelta(minutes=10),
    )

    assert summary["fraud_transactions"] == 2
    assert summary["fraud_intercepted_within_horizon"] == 2
    assert summary["fraud_intercept_rate"] == 1.0
    assert summary["fraud_exposure_at_horizon"] == 0.0
