import pytest

from scripts.fraud_policies import (
    Action,
    CapacityAwarePolicy,
    CostSensitivePolicy,
    FixedThresholdPolicy,
    PolicyContext,
)


def test_fixed_threshold_routes_three_actions():
    policy = FixedThresholdPolicy(
        review_threshold=0.4,
        block_threshold=0.8,
    )

    assert policy.decide(PolicyContext(0.2, 100.0)) == Action.APPROVE
    assert policy.decide(PolicyContext(0.5, 100.0)) == Action.REVIEW
    assert policy.decide(PolicyContext(0.9, 100.0)) == Action.BLOCK


def test_fixed_threshold_rejects_invalid_order():
    with pytest.raises(ValueError):
        FixedThresholdPolicy(
            review_threshold=0.9,
            block_threshold=0.5,
        )


def test_backlog_hours_uses_current_queue_and_service_rate():
    context = PolicyContext(
        risk_probability=0.5,
        transaction_value=100.0,
        queue_size=12,
        service_rate_per_hour=4.0,
    )
    assert context.backlog_hours == 3.0


def test_capacity_aware_becomes_more_selective_under_congestion():
    policy = CapacityAwarePolicy(
        base_review_threshold=0.40,
        block_threshold=0.90,
        soft_backlog_hours=2.0,
        hard_backlog_hours=5.0,
        soft_increment=0.15,
        hard_increment=0.30,
    )

    p = 0.50
    uncongested = PolicyContext(
        p, 100.0, queue_size=0, service_rate_per_hour=2.0
    )
    soft_congestion = PolicyContext(
        p, 100.0, queue_size=6, service_rate_per_hour=2.0
    )

    assert policy.decide(uncongested) == Action.REVIEW
    assert policy.decide(soft_congestion) == Action.APPROVE


def test_capacity_aware_never_raises_review_threshold_above_block_threshold():
    policy = CapacityAwarePolicy(
        base_review_threshold=0.70,
        block_threshold=0.80,
        soft_backlog_hours=1.0,
        hard_backlog_hours=2.0,
        soft_increment=0.20,
        hard_increment=0.40,
    )
    context = PolicyContext(
        risk_probability=0.79,
        transaction_value=100.0,
        queue_size=10,
        service_rate_per_hour=1.0,
    )

    assert policy.effective_review_threshold(context) == 0.80
    assert policy.decide(context) == Action.APPROVE


def test_cost_sensitive_can_prefer_review():
    policy = CostSensitivePolicy(
        review_cost=5.0,
        review_friction_cost=2.0,
        review_detection_rate=0.95,
        false_positive_block_cost=100.0,
    )
    context = PolicyContext(
        risk_probability=0.50,
        transaction_value=100.0,
    )

    assert policy.decide(context) == Action.REVIEW


def test_cost_sensitive_can_prefer_approve_for_low_risk_low_value():
    policy = CostSensitivePolicy(
        review_cost=5.0,
        review_friction_cost=2.0,
        review_detection_rate=0.95,
        false_positive_block_cost=100.0,
    )
    context = PolicyContext(
        risk_probability=0.01,
        transaction_value=10.0,
    )

    assert policy.decide(context) == Action.APPROVE


def test_cost_sensitive_can_prefer_block_for_high_risk_high_value():
    policy = CostSensitivePolicy(
        review_cost=50.0,
        review_friction_cost=5.0,
        review_detection_rate=0.50,
        false_positive_block_cost=20.0,
    )
    context = PolicyContext(
        risk_probability=0.99,
        transaction_value=10_000.0,
    )

    assert policy.decide(context) == Action.BLOCK
