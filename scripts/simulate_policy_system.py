"""Integrated policy + persistent review-queue simulator.

This module bridges scenario-specific risk scores with shared fraud-management
policy, queue and analyst-capacity mechanics.

It is a research simulator, not a production fraud-decision engine.
"""

from __future__ import annotations

from typing import Protocol

import pandas as pd

from scripts.fraud_policies import Action, PolicyContext


class Policy(Protocol):
    def decide(self, context: PolicyContext) -> Action:
        ...


REQUIRED_COLUMNS = {
    "TransactionId",
    "TransactionStartTime",
    "Value",
    "FraudResult",
    "risk_probability",
}


def _validate_transactions(transactions: pd.DataFrame) -> pd.DataFrame:
    missing = REQUIRED_COLUMNS.difference(transactions.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    df = transactions.copy()
    df["TransactionStartTime"] = pd.to_datetime(
        df["TransactionStartTime"], utc=True
    )
    df = df.sort_values(
        ["TransactionStartTime", "TransactionId"],
        kind="stable",
    ).reset_index(drop=True)

    if not df["risk_probability"].between(0.0, 1.0).all():
        raise ValueError("risk_probability must be in [0, 1]")
    if (df["Value"] < 0).any():
        raise ValueError("Value must be non-negative")

    return df


def _choose_queue_index(queue: list[dict], discipline: str) -> int:
    if discipline == "fifo":
        return min(
            range(len(queue)),
            key=lambda i: (queue[i]["arrival"], queue[i]["sequence"]),
        )
    if discipline == "risk_priority":
        return min(
            range(len(queue)),
            key=lambda i: (
                -queue[i]["risk_probability"],
                queue[i]["arrival"],
                queue[i]["sequence"],
            ),
        )
    raise ValueError("discipline must be 'fifo' or 'risk_priority'")


def simulate_policy_system(
    transactions: pd.DataFrame,
    policy: Policy,
    pooled_service_rate_per_hour: float,
    discipline: str = "fifo",
    horizon_end: pd.Timestamp | None = None,
) -> tuple[dict, pd.DataFrame, pd.DataFrame]:
    """Replay transactions through policy, queue and analyst service.

    Baseline outcome semantics:
    - APPROVE fraud -> immediately exposed/successful fraud value.
    - BLOCK fraud -> prevented/intercepted fraud value.
    - REVIEW -> enters persistent queue.
    - A REVIEWed fraud is counted as intercepted only if analyst service starts
      within the observation horizon.
    - A fraud still waiting in REVIEW at the horizon is unresolved exposure,
      not yet counted as either prevented or successful.
    - Analyst review is perfect in this baseline; analyst error is a later
      sensitivity mechanism.

    The policy observes only current/past queue state at decision time.
    """

    if pooled_service_rate_per_hour < 0:
        raise ValueError("pooled_service_rate_per_hour must be non-negative")

    df = _validate_transactions(transactions)
    if df.empty:
        empty = pd.DataFrame()
        return {
            "transactions": 0,
            "alerts": 0,
            "backlog_end": 0,
            "successful_fraud_value": 0.0,
            "unresolved_fraud_value": 0.0,
            "fraud_exposure_at_horizon": 0.0,
            "prevented_fraud_value": 0.0,
            "fraud_intercepted_within_horizon": 0,
            "fraud_intercept_rate": None,
        }, empty, empty

    if horizon_end is None:
        horizon_end = df["TransactionStartTime"].max()
    horizon_end = pd.to_datetime(horizon_end, utc=True)

    if pooled_service_rate_per_hour > 0:
        service_duration = pd.Timedelta(
            hours=1.0 / pooled_service_rate_per_hour
        )
    else:
        service_duration = None

    queue: list[dict] = []
    decisions: list[dict] = []
    reviews: list[dict] = []
    server_available = df["TransactionStartTime"].min()
    sequence = 0

    def drain_until(time_limit: pd.Timestamp) -> None:
        nonlocal server_available

        if service_duration is None:
            return

        while queue:
            idx = _choose_queue_index(queue, discipline)
            item = queue[idx]
            service_start = max(server_available, item["arrival"])

            if service_start > time_limit:
                break

            queue.pop(idx)
            service_end = service_start + service_duration
            wait_minutes = (
                service_start - item["arrival"]
            ).total_seconds() / 60.0

            reviews.append(
                {
                    **item,
                    "service_start": service_start,
                    "service_end": service_end,
                    "waiting_minutes": wait_minutes,
                    "review_started_within_horizon": int(
                        service_start <= horizon_end
                    ),
                }
            )
            server_available = service_end

    for row in df.itertuples(index=False):
        event_time = row.TransactionStartTime

        drain_until(event_time)

        context = PolicyContext(
            risk_probability=float(row.risk_probability),
            transaction_value=float(row.Value),
            queue_size=len(queue),
            service_rate_per_hour=pooled_service_rate_per_hour,
        )
        action = policy.decide(context)

        decision = {
            "TransactionId": row.TransactionId,
            "TransactionStartTime": event_time,
            "Value": float(row.Value),
            "FraudResult": int(row.FraudResult),
            "risk_probability": float(row.risk_probability),
            "queue_size_at_decision": len(queue),
            "backlog_hours_at_decision": context.backlog_hours,
            "action": action.value,
        }
        if hasattr(row, "CustomerId"):
            decision["CustomerId"] = row.CustomerId
        decisions.append(decision)

        if action == Action.REVIEW:
            queue.append(
                {
                    "TransactionId": row.TransactionId,
                    "arrival": event_time,
                    "Value": float(row.Value),
                    "FraudResult": int(row.FraudResult),
                    "risk_probability": float(row.risk_probability),
                    "sequence": sequence,
                }
            )
            sequence += 1
            drain_until(event_time)

    drain_until(horizon_end)

    decisions_df = pd.DataFrame(decisions)
    reviews_df = pd.DataFrame(reviews)

    reviewed_ids = set()
    if not reviews_df.empty:
        reviewed_ids = set(
            reviews_df.loc[
                reviews_df["review_started_within_horizon"].eq(1),
                "TransactionId",
            ]
        )

    fraud_mask = decisions_df["FraudResult"].eq(1)
    legit_mask = ~fraud_mask
    approved = decisions_df["action"].eq(Action.APPROVE.value)
    blocked = decisions_df["action"].eq(Action.BLOCK.value)
    review_action = decisions_df["action"].eq(Action.REVIEW.value)
    reviewed_within = decisions_df["TransactionId"].isin(reviewed_ids)

    fraud_total = int(fraud_mask.sum())
    fraud_intercepted = int(
        (fraud_mask & (blocked | (review_action & reviewed_within))).sum()
    )
    unresolved_fraud_count = int(
        (fraud_mask & review_action & ~reviewed_within).sum()
    )

    successful_fraud_value = float(
        decisions_df.loc[fraud_mask & approved, "Value"].sum()
    )
    prevented_fraud_value = float(
        decisions_df.loc[
            fraud_mask & (blocked | (review_action & reviewed_within)),
            "Value",
        ].sum()
    )
    unresolved_fraud_value = float(
        decisions_df.loc[
            fraud_mask & review_action & ~reviewed_within,
            "Value",
        ].sum()
    )
    fraud_exposure_at_horizon = (
        successful_fraud_value + unresolved_fraud_value
    )

    waiting = (
        reviews_df.loc[
            reviews_df["review_started_within_horizon"].eq(1),
            "waiting_minutes",
        ]
        if not reviews_df.empty
        else pd.Series(dtype=float)
    )

    summary = {
        "transactions": int(len(decisions_df)),
        "fraud_transactions": fraud_total,
        "approve_count": int(approved.sum()),
        "review_count": int(review_action.sum()),
        "block_count": int(blocked.sum()),
        "alerts": int(review_action.sum()),
        "reviewed_within_horizon": int(reviewed_within.sum()),
        "backlog_end": int((review_action & ~reviewed_within).sum()),
        "fraud_intercepted_within_horizon": fraud_intercepted,
        "fraud_intercept_rate": (
            fraud_intercepted / fraud_total if fraud_total else None
        ),
        "unresolved_fraud_count": unresolved_fraud_count,
        "successful_fraud_value": successful_fraud_value,
        "unresolved_fraud_value": unresolved_fraud_value,
        "fraud_exposure_at_horizon": fraud_exposure_at_horizon,
        "prevented_fraud_value": prevented_fraud_value,
        "legitimate_review_count": int(
            (legit_mask & review_action).sum()
        ),
        "legitimate_block_count": int((legit_mask & blocked).sum()),
        "legitimate_intervention_rate": (
            float(
                (legit_mask & (review_action | blocked)).sum()
                / legit_mask.sum()
            )
            if legit_mask.sum()
            else None
        ),
        "mean_wait_minutes": (
            float(waiting.mean()) if len(waiting) else None
        ),
        "p95_wait_minutes": (
            float(waiting.quantile(0.95)) if len(waiting) else None
        ),
        "pooled_service_rate_per_hour": pooled_service_rate_per_hour,
        "discipline": discipline,
        "horizon_end": horizon_end.isoformat(),
    }

    return summary, decisions_df, reviews_df
