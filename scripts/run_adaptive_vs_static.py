"""Toy smoke experiment for the adaptive-fraudster mechanism.

This is intentionally NOT an empirical thesis result. The response probabilities
below are synthetic and exist only to verify that the mechanism can be run,
replicated and compared before integration with IEEE-CIS/Xente scenarios.
"""

from __future__ import annotations

import argparse
import random
import statistics

from adaptive_fraudster import AdaptiveFraudster, StaticFraudster


STRATEGY_PROFILES = {
    "low_amount": {
        "amount": 50.0,
        "approve_p": 0.70,
        "challenge_p": 0.15,
        "review_p": 0.10,
    },
    "high_amount": {
        "amount": 200.0,
        "approve_p": 0.30,
        "challenge_p": 0.25,
        "review_p": 0.15,
    },
    "timing_shift": {
        "amount": 120.0,
        "approve_p": 0.55,
        "challenge_p": 0.15,
        "review_p": 0.15,
    },
}


def system_response(profile: dict, rng: random.Random) -> str:
    u = rng.random()
    approve = profile["approve_p"]
    challenge = approve + profile["challenge_p"]
    review = challenge + profile["review_p"]

    if u < approve:
        return "APPROVE"
    if u < challenge:
        return "CHALLENGE"
    if u < review:
        return "REVIEW"
    return "BLOCK"


def run_once(kind: str, steps: int, seed: int) -> dict:
    rng = random.Random(seed)
    strategies = list(STRATEGY_PROFILES)

    if kind == "adaptive":
        fraudster = AdaptiveFraudster(
            strategies,
            learning_rate=0.15,
            epsilon=0.10,
            seed=seed,
        )
    elif kind == "static":
        fraudster = StaticFraudster(
            strategies,
            fixed_strategy="low_amount",
            seed=seed,
        )
    else:
        raise ValueError("kind must be 'adaptive' or 'static'")

    successful_fraud_value = 0.0
    attempts = 0

    for step in range(steps):
        strategy = fraudster.choose_strategy(step)
        if strategy is None:
            continue

        profile = STRATEGY_PROFILES[strategy]
        response = system_response(profile, rng)
        attempts += 1

        if response == "APPROVE":
            successful_fraud_value += profile["amount"]

        fraudster.observe(response, profile["amount"], step)

    return {
        "kind": kind,
        "seed": seed,
        "attempts": attempts,
        "successful_fraud_value": successful_fraud_value,
    }


def summarize(kind: str, seeds: list[int], steps: int) -> dict:
    rows = [run_once(kind, steps, seed) for seed in seeds]
    losses = [row["successful_fraud_value"] for row in rows]

    return {
        "kind": kind,
        "runs": len(rows),
        "mean_loss": statistics.mean(losses),
        "std_loss": statistics.stdev(losses) if len(losses) > 1 else 0.0,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--steps", type=int, default=200)
    parser.add_argument("--seeds", type=int, default=30)
    args = parser.parse_args()

    seeds = list(range(args.seeds))
    for kind in ("static", "adaptive"):
        summary = summarize(kind, seeds, args.steps)
        print(
            f"{summary['kind']}: n={summary['runs']}, "
            f"mean successful fraud value={summary['mean_loss']:.2f}, "
            f"sd={summary['std_loss']:.2f}"
        )


if __name__ == "__main__":
    main()
