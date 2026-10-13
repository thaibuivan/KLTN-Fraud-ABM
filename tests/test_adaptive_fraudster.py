from scripts.adaptive_fraudster import (
    AdaptiveFraudster,
    StaticFraudster,
    StaticMixtureFraudster,
)


def test_adaptive_updates_value_after_approve():
    fraudster = AdaptiveFraudster(
        ["a", "b"],
        learning_rate=0.5,
        epsilon=0.0,
        seed=1,
    )
    fraudster.current_strategy = "a"
    reward = fraudster.observe(
        "APPROVE",
        amount=100.0,
        step=0,
    )

    assert reward == 100.0
    assert fraudster.states["a"].attempts == 1
    assert fraudster.states["a"].successes == 1
    assert fraudster.states["a"].value == 50.0


def test_static_keeps_fixed_strategy():
    fraudster = StaticFraudster(
        ["a", "b"],
        fixed_strategy="b",
        consecutive_block_limit=99,
        seed=1,
    )

    assert all(
        fraudster.choose_strategy(step) == "b"
        for step in range(10)
    )


def test_static_mixture_is_reproducible_and_nonadaptive():
    weights = {"a": 0.7, "b": 0.3}
    first = StaticMixtureFraudster(
        weights,
        seed=7,
    )
    second = StaticMixtureFraudster(
        weights,
        seed=7,
    )

    seq_first = []
    seq_second = []

    for step in range(20):
        seq_first.append(
            first.choose_strategy(step)
        )
        first.observe(
            "BLOCK",
            amount=100.0,
            step=step,
        )

        seq_second.append(
            second.choose_strategy(step)
        )
        second.observe(
            "APPROVE",
            amount=100.0,
            step=step,
        )

    assert seq_first == seq_second


def test_repeated_blocks_trigger_dormancy():
    fraudster = AdaptiveFraudster(
        ["a"],
        consecutive_block_limit=2,
        dormancy_steps=3,
        epsilon=0.0,
        seed=1,
    )

    fraudster.choose_strategy(0)
    fraudster.observe(
        "BLOCK",
        amount=10.0,
        step=0,
    )
    fraudster.choose_strategy(1)
    fraudster.observe(
        "BLOCK",
        amount=10.0,
        step=1,
    )

    assert fraudster.choose_strategy(2) is None
    assert fraudster.choose_strategy(4) is None
    assert fraudster.choose_strategy(5) == "a"


def test_unknown_response_raises():
    fraudster = AdaptiveFraudster(
        ["a"],
        seed=1,
    )

    try:
        fraudster.observe(
            "UNKNOWN",
            amount=10.0,
            step=0,
        )
    except ValueError:
        pass
    else:
        raise AssertionError(
            "Expected ValueError"
        )
