"""Alternative, assumption-explicit fraud outcomes from policy replay.

This is a *sensitivity accounting layer*, NOT a bank loss estimator.
A review is eligible for assumed prevention only if service completed by
horizon. Direct blocks and completed reviews are kept separate.
Pending review is *exposure at horizon*, not observed loss.
"""

from __future__ import annotations

import pandas as pd


REQUIRED_DECISIONS = {"TransactionId", "FraudResult", "Value", "action"}
REQUIRED_REVIEWS = {"TransactionId", "service_end"}


def expected_outcomes_by_horizon(
    decisions: pd.DataFrame,
    reviews: pd.DataFrame,
    horizon_end,
    *,
    review_prevention_probability: float,
) -> dict:
    """Return scenario-dependent expected amounts, not realized bank losses.

    REVIEW with service_end after the observation horizon remains unresolved.
    A completed fraud review prevents the fraud value with hypothetical
    probability q in [0,1]; no true prevention/recovery rate is estimated.
    """
    q = float(review_prevention_probability)
    if not 0 <= q <= 1:
        raise ValueError("review_prevention_probability must be in [0,1]")
    missing = REQUIRED_DECISIONS.difference(decisions.columns)
    if missing:
        raise ValueError(f"Missing decisions fields: {sorted(missing)}")
    if not reviews.empty:
        missing = REQUIRED_REVIEWS.difference(reviews.columns)
        if missing:
            raise ValueError(f"Missing reviews fields: {sorted(missing)}")
    if decisions["TransactionId"].duplicated().any():
        raise ValueError("Transaction IDs must be unique")
    if not decisions["action"].isin(["APPROVE", "REVIEW", "BLOCK"]).all():
        raise ValueError("Unknown policy action")
    if not decisions["FraudResult"].isin([0, 1]).all():
        raise ValueError("FraudResult must be binary")
    if (decisions["Value"] < 0).any():
        raise ValueError("Value must be nonnegative")

    horizon = pd.to_datetime(horizon_end, utc=True)
    completed = set()
    if not reviews.empty:
        end = pd.to_datetime(reviews["service_end"], utc=True)
        completed = set(reviews.loc[end.le(horizon), "TransactionId"])

    fraud = decisions.loc[decisions["FraudResult"].eq(1)]
    blocked = fraud["action"].eq("BLOCK")
    approved = fraud["action"].eq("APPROVE")
    reviewed = fraud["action"].eq("REVIEW")
    done = fraud["TransactionId"].isin(completed)

    blocked_value = float(fraud.loc[blocked, "Value"].sum())
    approved_value = float(fraud.loc[approved, "Value"].sum())
    resolved_review_value = float(fraud.loc[reviewed & done, "Value"].sum())
    unresolved_value = float(fraud.loc[reviewed & ~done, "Value"].sum())
    expected_prevented = blocked_value + q * resolved_review_value
    exposure = approved_value + (1 - q) * resolved_review_value + unresolved_value
    total = float(fraud["Value"].sum())
    if abs((expected_prevented + exposure) - total) > 1e-6 * max(1, total):
        raise AssertionError("Fraud value accounting must balance")
    return {
        "review_prevention_probability_assumed": q,
        "directly_blocked_fraud_value": blocked_value,
        "approved_fraud_value": approved_value,
        "review_completed_fraud_value": resolved_review_value,
        "unresolved_fraud_value_at_horizon": unresolved_value,
        "expected_prevented_fraud_value_under_assumption": expected_prevented,
        "fraud_exposure_upper_bound_at_horizon_under_assumption": exposure,
        "total_attempted_fraud_value": total,
    }
