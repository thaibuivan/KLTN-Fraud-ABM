"""Shared fraud-management policy definitions for the thesis simulator.

These policies are research mechanisms, not production banking rules.
They deliberately expose assumptions as parameters so they can be stress-tested.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from math import inf


class Action(str, Enum):
    APPROVE = "APPROVE"
    REVIEW = "REVIEW"
    BLOCK = "BLOCK"


@dataclass(frozen=True)
class PolicyContext:
    risk_probability: float
    transaction_value: float
    queue_size: int = 0
    service_rate_per_hour: float = 0.0

    def __post_init__(self) -> None:
        if not 0.0 <= self.risk_probability <= 1.0:
            raise ValueError("risk_probability must be in [0, 1]")
        if self.transaction_value < 0:
            raise ValueError("transaction_value must be non-negative")
        if self.queue_size < 0:
            raise ValueError("queue_size must be non-negative")
        if self.service_rate_per_hour < 0:
            raise ValueError("service_rate_per_hour must be non-negative")

    @property
    def backlog_hours(self) -> float:
        if self.queue_size == 0:
            return 0.0
        if self.service_rate_per_hour == 0:
            return inf
        return self.queue_size / self.service_rate_per_hour


def _validate_thresholds(review_threshold: float, block_threshold: float) -> None:
    if not 0.0 <= review_threshold <= 1.0:
        raise ValueError("review_threshold must be in [0, 1]")
    if not 0.0 <= block_threshold <= 1.0:
        raise ValueError("block_threshold must be in [0, 1]")
    if review_threshold > block_threshold:
        raise ValueError("review_threshold must be <= block_threshold")


@dataclass(frozen=True)
class FixedThresholdPolicy:
    review_threshold: float
    block_threshold: float

    def __post_init__(self) -> None:
        _validate_thresholds(self.review_threshold, self.block_threshold)

    def decide(self, context: PolicyContext) -> Action:
        p = context.risk_probability
        if p >= self.block_threshold:
            return Action.BLOCK
        if p >= self.review_threshold:
            return Action.REVIEW
        return Action.APPROVE


@dataclass(frozen=True)
class CapacityAwarePolicy:
    """Raise the review threshold when the review queue is congested.

    Congestion is measured using backlog-hours = queue_size / service_rate_per_hour.
    This is an experimental policy mechanism, not a claimed bank rule.
    """

    base_review_threshold: float
    block_threshold: float
    soft_backlog_hours: float
    hard_backlog_hours: float
    soft_increment: float
    hard_increment: float

    def __post_init__(self) -> None:
        _validate_thresholds(self.base_review_threshold, self.block_threshold)
        if self.soft_backlog_hours < 0:
            raise ValueError("soft_backlog_hours must be non-negative")
        if self.hard_backlog_hours < self.soft_backlog_hours:
            raise ValueError(
                "hard_backlog_hours must be >= soft_backlog_hours"
            )
        if self.soft_increment < 0 or self.hard_increment < 0:
            raise ValueError("threshold increments must be non-negative")
        if self.hard_increment < self.soft_increment:
            raise ValueError("hard_increment must be >= soft_increment")

    def effective_review_threshold(self, context: PolicyContext) -> float:
        backlog = context.backlog_hours
        threshold = self.base_review_threshold

        if backlog >= self.hard_backlog_hours:
            threshold += self.hard_increment
        elif backlog >= self.soft_backlog_hours:
            threshold += self.soft_increment

        return min(threshold, self.block_threshold)

    def decide(self, context: PolicyContext) -> Action:
        p = context.risk_probability
        if p >= self.block_threshold:
            return Action.BLOCK
        if p >= self.effective_review_threshold(context):
            return Action.REVIEW
        return Action.APPROVE


@dataclass(frozen=True)
class CostSensitivePolicy:
    """Choose the action with the lowest explicit expected cost.

    This policy is an extension until its cost parameters are sufficiently grounded.
    All cost values must use the same unit.
    """

    review_cost: float
    review_friction_cost: float
    review_detection_rate: float
    false_positive_block_cost: float

    def __post_init__(self) -> None:
        if self.review_cost < 0:
            raise ValueError("review_cost must be non-negative")
        if self.review_friction_cost < 0:
            raise ValueError("review_friction_cost must be non-negative")
        if not 0.0 <= self.review_detection_rate <= 1.0:
            raise ValueError("review_detection_rate must be in [0, 1]")
        if self.false_positive_block_cost < 0:
            raise ValueError("false_positive_block_cost must be non-negative")

    def expected_costs(self, context: PolicyContext) -> dict[Action, float]:
        p = context.risk_probability
        value = context.transaction_value

        approve_cost = p * value
        review_cost = (
            self.review_cost
            + (1.0 - p) * self.review_friction_cost
            + p * (1.0 - self.review_detection_rate) * value
        )
        block_cost = (1.0 - p) * self.false_positive_block_cost

        return {
            Action.APPROVE: approve_cost,
            Action.REVIEW: review_cost,
            Action.BLOCK: block_cost,
        }

    def decide(self, context: PolicyContext) -> Action:
        costs = self.expected_costs(context)
        # Stable tie-break: APPROVE -> REVIEW -> BLOCK.
        order = [Action.APPROVE, Action.REVIEW, Action.BLOCK]
        return min(order, key=lambda action: costs[action])
