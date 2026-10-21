import pandas as pd

from scripts.simulate_alert_queue import simulate


def scored_frame():
    t0 = pd.Timestamp("2026-01-01T00:00:00Z")
    rows = []
    specs = [
        ("T1", 0, 0.20, 0),
        ("T2", 1, 0.95, 1),
        ("T3", 2, 0.30, 0),
        ("T4", 3, 0.80, 1),
        ("T5", 4, 0.10, 0),
        ("T6", 5, 0.70, 0),
    ]
    for txn, hour, score, fraud in specs:
        rows.append(
            {
                "TransactionId": txn,
                "CustomerId": f"C{txn}",
                "TransactionStartTime": t0 + pd.Timedelta(hours=hour),
                "Value": 100.0,
                "FraudResult": fraud,
                "risk_probability": score,
                "seen_in_train_customer": 1,
            }
        )
    return pd.DataFrame(rows)


def test_no_service_before_arrival():
    df = scored_frame()
    _, reviewed = simulate(
        df,
        threshold=0.0,
        capacity_ratio=1.0,
        discipline="fifo",
    )
    assert (reviewed["service_start"] >= reviewed["arrival"]).all()


def test_priority_changes_order_not_total_capacity():
    df = scored_frame()
    fifo_summary, _ = simulate(
        df,
        threshold=0.0,
        capacity_ratio=0.75,
        discipline="fifo",
    )
    risk_summary, _ = simulate(
        df,
        threshold=0.0,
        capacity_ratio=0.75,
        discipline="risk_priority",
    )
    assert (
        fifo_summary["reviewed_within_horizon"]
        == risk_summary["reviewed_within_horizon"]
    )
    assert fifo_summary["backlog_end"] == risk_summary["backlog_end"]


def test_risk_priority_order_does_not_use_fraud_label():
    df = scored_frame()
    _, reviewed_a = simulate(
        df,
        threshold=0.0,
        capacity_ratio=0.75,
        discipline="risk_priority",
    )
    swapped = df.copy()
    swapped["FraudResult"] = 1 - swapped["FraudResult"]
    _, reviewed_b = simulate(
        swapped,
        threshold=0.0,
        capacity_ratio=0.75,
        discipline="risk_priority",
    )
    assert (
        reviewed_a["TransactionId"].tolist()
        == reviewed_b["TransactionId"].tolist()
    )


def test_stochastic_service_is_seed_reproducible():
    df = scored_frame()
    summary_a, reviewed_a = simulate(
        df,
        threshold=0.0,
        capacity_ratio=1.0,
        discipline="fifo",
        service_cv=0.5,
        seed=42,
    )
    summary_b, reviewed_b = simulate(
        df,
        threshold=0.0,
        capacity_ratio=1.0,
        discipline="fifo",
        service_cv=0.5,
        seed=42,
    )
    assert (
        reviewed_a["service_minutes"].tolist()
        == reviewed_b["service_minutes"].tolist()
    )
    assert (
        summary_a["fraud_capture_within_horizon"]
        == summary_b["fraud_capture_within_horizon"]
    )


def test_fixed_service_rate_is_independent_of_threshold():
    df = scored_frame()
    summary_all, _ = simulate(
        df,
        threshold=0.0,
        capacity_ratio=1.0,
        discipline="fifo",
        pooled_service_rate_per_hour=1.2,
    )
    summary_strict, _ = simulate(
        df,
        threshold=0.5,
        capacity_ratio=1.0,
        discipline="fifo",
        pooled_service_rate_per_hour=1.2,
    )
    assert summary_all["pooled_service_rate_per_hour"] == 1.2
    assert summary_strict["pooled_service_rate_per_hour"] == 1.2
    assert (
        summary_all["capacity_mode"]
        == "fixed_external_service_rate"
    )
    assert (
        summary_strict["capacity_mode"]
        == "fixed_external_service_rate"
    )


def test_variable_team_capacity_is_seed_reproducible():
    df = scored_frame()
    summary_a, reviewed_a = simulate(
        df,
        threshold=0.0,
        capacity_ratio=1.0,
        discipline="fifo",
        team_capacity_cv=0.4,
        seed=7,
    )
    summary_b, reviewed_b = simulate(
        df,
        threshold=0.0,
        capacity_ratio=1.0,
        discipline="fifo",
        team_capacity_cv=0.4,
        seed=7,
    )
    assert (
        reviewed_a["team_capacity_multiplier"].tolist()
        == reviewed_b["team_capacity_multiplier"].tolist()
    )
    assert (
        summary_a["backlog_end"]
        == summary_b["backlog_end"]
    )
