from __future__ import annotations

import pandas as pd

from scripts.fraud_policies import Action, PolicyContext


class PolicyQueueEngine:
    """Stateful policy + persistent queue engine for adaptive simulation."""

    def __init__(
        self,
        policy,
        pooled_service_rate_per_hour: float,
        discipline: str = "fifo",
        horizon_end=None,
    ) -> None:
        if pooled_service_rate_per_hour < 0:
            raise ValueError("service rate must be non-negative")
        if discipline not in {"fifo", "risk_priority"}:
            raise ValueError("unknown discipline")

        self.policy = policy
        self.service_rate = float(pooled_service_rate_per_hour)
        self.discipline = discipline
        self.horizon_end = (
            pd.to_datetime(horizon_end, utc=True)
            if horizon_end is not None
            else None
        )

        self.queue: list[dict] = []
        self.decisions: list[dict] = []
        self.reviews: list[dict] = []
        self.server_available = None
        self.sequence = 0

        self.service_duration = (
            pd.Timedelta(hours=1.0 / self.service_rate)
            if self.service_rate > 0
            else None
        )

    def _choose_queue_index(self) -> int:
        if self.discipline == "fifo":
            return min(
                range(len(self.queue)),
                key=lambda i: (
                    self.queue[i]["arrival"],
                    self.queue[i]["sequence"],
                ),
            )

        return min(
            range(len(self.queue)),
            key=lambda i: (
                -self.queue[i]["risk_probability"],
                self.queue[i]["arrival"],
                self.queue[i]["sequence"],
            ),
        )

    def drain_until(self, time_limit) -> None:
        if not isinstance(time_limit, pd.Timestamp):
            time_limit = pd.to_datetime(time_limit, utc=True)

        if self.service_duration is None:
            return

        if self.server_available is None:
            self.server_available = time_limit

        while self.queue:
            idx = self._choose_queue_index()
            item = self.queue[idx]
            service_start = max(
                self.server_available,
                item["arrival"],
            )

            if service_start > time_limit:
                break

            self.queue.pop(idx)
            service_end = service_start + self.service_duration
            wait_minutes = (
                service_start - item["arrival"]
            ).total_seconds() / 60.0

            self.reviews.append(
                {
                    **item,
                    "service_start": service_start,
                    "service_end": service_end,
                    "waiting_minutes": wait_minutes,
                    "review_started_within_horizon": int(
                        self.horizon_end is None
                        or service_start <= self.horizon_end
                    ),
                }
            )
            self.server_available = service_end

    def process_event(self, event: dict) -> Action:
        event_time = event["TransactionStartTime"]
        if not isinstance(event_time, pd.Timestamp):
            event_time = pd.to_datetime(
                event_time,
                utc=True,
            )

        if self.server_available is None:
            self.server_available = event_time

        self.drain_until(event_time)

        context = PolicyContext(
            risk_probability=float(event["risk_probability"]),
            transaction_value=float(event["Value"]),
            queue_size=len(self.queue),
            service_rate_per_hour=self.service_rate,
        )
        action = self.policy.decide(context)

        decision = {
            **event,
            "TransactionStartTime": event_time,
            "queue_size_at_decision": len(self.queue),
            "backlog_hours_at_decision": context.backlog_hours,
            "action": action.value,
        }
        self.decisions.append(decision)

        if action == Action.REVIEW:
            self.queue.append(
                {
                    "TransactionId": event["TransactionId"],
                    "arrival": event_time,
                    "Value": float(event["Value"]),
                    "FraudResult": int(event["FraudResult"]),
                    "risk_probability": float(
                        event["risk_probability"]
                    ),
                    "sequence": self.sequence,
                    "strategy": event.get("strategy"),
                }
            )
            self.sequence += 1

            # If service is idle, a just-arrived alert may start immediately.
            self.drain_until(event_time)

        return action

    def finalize(self, horizon_end=None):
        if horizon_end is not None:
            self.horizon_end = pd.to_datetime(
                horizon_end,
                utc=True,
            )

        if self.horizon_end is None and self.decisions:
            self.horizon_end = max(
                row["TransactionStartTime"]
                for row in self.decisions
            )

        if self.horizon_end is not None:
            self.drain_until(self.horizon_end)

        decisions = pd.DataFrame(self.decisions)
        reviews = pd.DataFrame(self.reviews)

        if decisions.empty:
            return {}, decisions, reviews

        reviewed_ids = set()
        if not reviews.empty:
            reviewed_ids = set(
                reviews.loc[
                    reviews["review_started_within_horizon"].eq(1),
                    "TransactionId",
                ]
            )

        fraud = decisions["FraudResult"].eq(1)
        legit = ~fraud
        approved = decisions["action"].eq(Action.APPROVE.value)
        blocked = decisions["action"].eq(Action.BLOCK.value)
        review_action = decisions["action"].eq(
            Action.REVIEW.value
        )
        reviewed_within = decisions["TransactionId"].isin(
            reviewed_ids
        )

        successful = float(
            decisions.loc[
                fraud & approved,
                "Value",
            ].sum()
        )
        unresolved = float(
            decisions.loc[
                fraud & review_action & ~reviewed_within,
                "Value",
            ].sum()
        )
        prevented = float(
            decisions.loc[
                fraud
                & (
                    blocked
                    | (review_action & reviewed_within)
                ),
                "Value",
            ].sum()
        )

        waiting = (
            reviews.loc[
                reviews["review_started_within_horizon"].eq(1),
                "waiting_minutes",
            ]
            if not reviews.empty
            else pd.Series(dtype=float)
        )

        fraud_count = int(fraud.sum())
        intercepted_count = int(
            (
                fraud
                & (
                    blocked
                    | (review_action & reviewed_within)
                )
            ).sum()
        )

        summary = {
            "transactions": int(len(decisions)),
            "fraud_transactions": fraud_count,
            "approve_count": int(approved.sum()),
            "review_count": int(review_action.sum()),
            "block_count": int(blocked.sum()),
            "reviewed_within_horizon": int(
                reviewed_within.sum()
            ),
            "backlog_end": int(
                (review_action & ~reviewed_within).sum()
            ),
            "fraud_intercepted_within_horizon": intercepted_count,
            "fraud_intercept_rate": (
                intercepted_count / fraud_count
                if fraud_count
                else None
            ),
            "unresolved_fraud_count": int(
                (
                    fraud
                    & review_action
                    & ~reviewed_within
                ).sum()
            ),
            "successful_fraud_value": successful,
            "unresolved_fraud_value": unresolved,
            "fraud_exposure_at_horizon": (
                successful + unresolved
            ),
            "prevented_fraud_value": prevented,
            "legitimate_review_count": int(
                (legit & review_action).sum()
            ),
            "legitimate_block_count": int(
                (legit & blocked).sum()
            ),
            "legitimate_intervention_rate": (
                float(
                    (
                        legit
                        & (review_action | blocked)
                    ).sum()
                    / legit.sum()
                )
                if legit.sum()
                else None
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
            "pooled_service_rate_per_hour": self.service_rate,
            "discipline": self.discipline,
            "horizon_end": (
                self.horizon_end.isoformat()
                if self.horizon_end is not None
                else None
            ),
        }

        return summary, decisions, reviews
