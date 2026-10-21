"""Closed-loop fraud-policy simulator with strategy feedback.

The simulator consumes an already-scored empirical event stream. Legitimate
transactions are replayed as observed. Historical fraud timestamps are treated as
fraud-attempt opportunities; their score/value can be replaced by a
scenario-specific empirical template selected by a Static or Adaptive fraudster.

This is a counterfactual stress-test mechanism, not a reconstruction of observed
fraudster cognition.
"""

from __future__ import annotations

import random
from typing import Protocol

import pandas as pd

from scripts.fraud_policies import Action, PolicyContext


class Fraudster(Protocol):
    def choose_strategy(self, step: int) -> str | None:
        ...

    def observe(
        self,
        response: str,
        amount: float,
        step: int,
    ) -> float:
        ...


class FraudGenerator(Protocol):
    @property
    def strategies(self) -> tuple[str, ...]:
        ...

    def sample(
        self,
        strategy: str,
        rng: random.Random,
    ) -> dict:
        ...


def _queue_index(queue: list[dict], discipline: str) -> int:
    if discipline == "fifo":
        return min(
            range(len(queue)),
            key=lambda i: (
                queue[i]["arrival"],
                queue[i]["sequence"],
            ),
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
    raise ValueError(
        "discipline must be 'fifo' or 'risk_priority'"
    )


def simulate_adaptive_policy_system(
    transactions: pd.DataFrame,
    policy,
    fraudster: Fraudster,
    fraud_generator: FraudGenerator,
    pooled_service_rate_per_hour: float,
    *,
    discipline: str = "risk_priority",
    seed: int = 0,
    horizon_end: pd.Timestamp | None = None,
) -> tuple[dict, pd.DataFrame, pd.DataFrame]:
    required = {
        "TransactionId",
        "TransactionStartTime",
        "Value",
        "FraudResult",
        "risk_probability",
    }
    missing = required.difference(transactions.columns)
    if missing:
        raise ValueError(
            f"Missing required columns: {sorted(missing)}"
        )
    if pooled_service_rate_per_hour <= 0:
        raise ValueError(
            "pooled_service_rate_per_hour must be positive"
        )

    df = transactions.copy()
    df["TransactionStartTime"] = pd.to_datetime(
        df["TransactionStartTime"],
        utc=True,
    )
    df = df.sort_values(
        ["TransactionStartTime", "TransactionId"],
        kind="stable",
    ).reset_index(drop=True)

    if horizon_end is None:
        horizon_end = df["TransactionStartTime"].max()
    horizon_end = pd.to_datetime(horizon_end, utc=True)

    service_duration = pd.Timedelta(
        hours=1.0 / pooled_service_rate_per_hour
    )
    rng = random.Random(seed)

    queue: list[dict] = []
    reviews: list[dict] = []
    decisions: list[dict] = []
    server_available = df["TransactionStartTime"].min()
    sequence = 0
    fraud_step = 0

    strategy_counts = {
        strategy: 0 for strategy in fraud_generator.strategies
    }

    def drain_until(limit: pd.Timestamp) -> None:
        nonlocal server_available
        while queue:
            idx = _queue_index(queue, discipline)
            item = queue[idx]
            service_start = max(
                server_available,
                item["arrival"],
            )
            if service_start > limit:
                break

            queue.pop(idx)
            service_end = service_start + service_duration
            reviews.append(
                {
                    **item,
                    "service_start": service_start,
                    "service_end": service_end,
                    "waiting_minutes": (
                        service_start - item["arrival"]
                    ).total_seconds() / 60.0,
                    "review_started_within_horizon": int(
                        service_start <= horizon_end
                    ),
                }
            )
            server_available = service_end

    for row in df.itertuples(index=False):
        event_time = row.TransactionStartTime
        drain_until(event_time)

        is_fraud = int(row.FraudResult) == 1
        value = float(row.Value)
        risk_probability = float(row.risk_probability)
        strategy = None

        if is_fraud:
            strategy = fraudster.choose_strategy(fraud_step)
            current_step = fraud_step
            fraud_step += 1

            if strategy is None:
                decisions.append(
                    {
                        "TransactionId": row.TransactionId,
                        "TransactionStartTime": event_time,
                        "FraudResult": 1,
                        "strategy": None,
                        "action": "DORMANT_SKIP",
                        "queue_size_at_decision": len(queue),
                    }
                )
                continue

            template = fraud_generator.sample(
                strategy,
                rng,
            )
            value = float(template["Value"])
            risk_probability = float(
                template["risk_probability"]
            )
            strategy_counts[strategy] += 1

        context = PolicyContext(
            risk_probability=risk_probability,
            transaction_value=value,
            queue_size=len(queue),
            service_rate_per_hour=(
                pooled_service_rate_per_hour
            ),
        )
        action = policy.decide(context)

        decisions.append(
            {
                "TransactionId": row.TransactionId,
                "TransactionStartTime": event_time,
                "FraudResult": int(row.FraudResult),
                "Value": value,
                "risk_probability": risk_probability,
                "strategy": strategy,
                "action": action.value,
                "queue_size_at_decision": len(queue),
                "backlog_hours_at_decision": (
                    context.backlog_hours
                ),
            }
        )

        if action == Action.REVIEW:
            queue.append(
                {
                    "TransactionId": row.TransactionId,
                    "arrival": event_time,
                    "FraudResult": int(row.FraudResult),
                    "Value": value,
                    "risk_probability": risk_probability,
                    "sequence": sequence,
                }
            )
            sequence += 1
            drain_until(event_time)

        if is_fraud:
            fraudster.observe(
                action.value,
                value,
                current_step,
            )

    drain_until(horizon_end)

    decisions_df = pd.DataFrame(decisions)
    reviews_df = pd.DataFrame(reviews)

    routing = decisions_df[
        decisions_df["action"].isin(
            [
                Action.APPROVE.value,
                Action.REVIEW.value,
                Action.BLOCK.value,
            ]
        )
    ].copy()

    reviewed_ids: set = set()
    if not reviews_df.empty:
        reviewed_ids = set(
            reviews_df.loc[
                reviews_df[
                    "review_started_within_horizon"
                ].eq(1),
                "TransactionId",
            ]
        )

    fraud = routing["FraudResult"].eq(1)
    legitimate = routing["FraudResult"].eq(0)
    approve = routing["action"].eq(Action.APPROVE.value)
    review = routing["action"].eq(Action.REVIEW.value)
    block = routing["action"].eq(Action.BLOCK.value)
    reviewed = routing["TransactionId"].isin(reviewed_ids)

    fraud_attempts = int(fraud.sum())
    intercepted = int(
        (
            fraud
            & (
                block
                | (review & reviewed)
            )
        ).sum()
    )

    waiting = (
        reviews_df.loc[
            reviews_df[
                "review_started_within_horizon"
            ].eq(1),
            "waiting_minutes",
        ]
        if not reviews_df.empty
        else pd.Series(dtype=float)
    )

    summary = {
        "transactions_routed": int(len(routing)),
        "fraud_attempts": fraud_attempts,
        "dormant_skips": int(
            decisions_df["action"].eq(
                "DORMANT_SKIP"
            ).sum()
        ),
        "approve_count": int(approve.sum()),
        "review_count": int(review.sum()),
        "block_count": int(block.sum()),
        "reviewed_within_horizon": int(reviewed.sum()),
        "backlog_end": int(
            (review & ~reviewed).sum()
        ),
        "fraud_intercepted": intercepted,
        "fraud_intercept_rate": (
            intercepted / fraud_attempts
            if fraud_attempts
            else None
        ),
        "successful_fraud_value": float(
            routing.loc[
                fraud & approve,
                "Value",
            ].sum()
        ),
        "unresolved_fraud_value": float(
            routing.loc[
                fraud & review & ~reviewed,
                "Value",
            ].sum()
        ),
        "legitimate_review_count": int(
            (legitimate & review).sum()
        ),
        "legitimate_block_count": int(
            (legitimate & block).sum()
        ),
        "mean_wait_minutes": (
            float(waiting.mean())
            if len(waiting)
            else None
        ),
        "p95_wait_minutes": (
            float(waiting.quantile(0.95))
            if len(waiting)
            else None
        ),
    }

    for strategy in fraud_generator.strategies:
        summary[f"strategy_count_{strategy}"] = int(
            strategy_counts[strategy]
        )
        summary[f"strategy_share_{strategy}"] = (
            strategy_counts[strategy] / fraud_attempts
            if fraud_attempts
            else None
        )

    return summary, decisions_df, reviews_df
