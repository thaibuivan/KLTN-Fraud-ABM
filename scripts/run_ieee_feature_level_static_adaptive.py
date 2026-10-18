"""Run IEEE-CIS Static/Adaptive counterfactual policy simulation.

Main loop: pre-test past-only entity state -> chronological test events ->
fresh per-event IEEE model score -> fraud policy -> persistent analyst queue ->
fraudster feedback -> next strategy. Test fraud labels determine attempt slots,
NEVER validation donor pools or learned fraud strategies.

This runner is computationally expensive in exact scoring mode: first use
--max-test-events and --seeds 1, then verify invariants and scale carefully.
No proprietary/company data. Do not commit the prepared raw CSV inputs.
"""

from __future__ import annotations

import argparse
from copy import deepcopy
import json
from pathlib import Path
import random

import joblib
import pandas as pd

from scripts.adaptive_fraudster import AdaptiveFraudster, StaticMixtureFraudster
from scripts.fraud_policies import FixedThresholdPolicy, TieredCapacityAwarePolicy
from scripts.ieee_feature_level_fraud import IEEEFeatureLevelFraudGenerator
from scripts.ieee_online_scorer import IEEEOnlineRiskScorer
from scripts.ieee_fast_online_scorer import FastIEEEOnlineRiskScorer
from scripts.outcome_semantics import expected_outcomes_by_horizon
from scripts.policy_queue_engine import PolicyQueueEngine
from scripts.simulate_alert_queue import threshold_for_target_rate
from scripts.scenario_adapters import normalize_ieee_scores


def calibration(validation_scores: pd.DataFrame, review_rates=(0.01, 0.0075, 0.005), block_rate=0.001) -> dict:
    """Use the frozen validation score stream only for operating points."""
    validation = normalize_ieee_scores(validation_scores)
    thresholds = [
        float(threshold_for_target_rate(validation, float(rate)))
        for rate in review_rates
    ]
    block = float(threshold_for_target_rate(validation, float(block_rate)))
    if not (thresholds[0] <= thresholds[1] <= thresholds[2] <= block):
        raise ValueError("Degenerate or non-nested IEEE validation tail thresholds")
    alerts = validation.loc[
        validation["risk_probability"].ge(thresholds[0])
    ]
    if len(alerts) < 2:
        raise ValueError("Too few base validation alerts")
    hours = (
        alerts["TransactionStartTime"].max()
        - alerts["TransactionStartTime"].min()
    ).total_seconds() / 3600.0
    if hours <= 0:
        raise ValueError("No positive validation alert observation window")
    return {
        "base": thresholds[0],
        "soft": thresholds[1],
        "hard": thresholds[2],
        "block": block,
        "reference_rate_per_hour": float(len(alerts) / hours),
        "review_rates": list(review_rates),
        "block_rate": block_rate,
    }


def run_experiments(
    validation_scores: pd.DataFrame,
    validation_donors: pd.DataFrame,
    test_context: pd.DataFrame,
    scorer_factory,
    *,
    seeds: int = 1,
    capacity_ratios=(0.75, 1.0, 1.25),
    review_feedback: str = "policy_action",
    reward_amount_mode: str = "value",
    learning_rate: float = 0.15,
    epsilon: float = 0.10,
    soft_backlog_hours: float = 24.0,
    hard_backlog_hours: float = 72.0,
    max_test_events: int | None = None,
) -> pd.DataFrame:
    """Shared scenario logic, deterministic under fixed inputs/seeds."""
    if seeds < 1 or not (0 < learning_rate <= 1) or not (0 <= epsilon <= 1):
        raise ValueError("Invalid seeds/learning parameters")
    if review_feedback not in {"policy_action", "no_review_observation"}:
        raise ValueError("Unknown REVIEW observability assumption")
    if reward_amount_mode not in {"value", "unit"}:
        raise ValueError("Unknown reward amount mode")
    if any(float(c) <= 0 for c in capacity_ratios):
        raise ValueError("Capacity ratios must be positive")
    cal = calibration(validation_scores)
    gen = IEEEFeatureLevelFraudGenerator.from_validation_raw(validation_donors)

    stream = test_context.sort_values(["TransactionDT", "TransactionID"], kind="stable").copy()
    if max_test_events is not None:
        if max_test_events < 1:
            raise ValueError("max_test_events must be positive")
        stream = stream.head(max_test_events).copy()
    if stream.empty:
        raise ValueError("Empty IEEE test stream")
    if not stream["isFraud"].isin([0, 1]).all():
        raise ValueError("Test fraud labels must be binary")
    if not pd.to_numeric(stream["TransactionDT"]).is_monotonic_increasing:
        raise ValueError("IEEE test timestamps must be chronological")
    if stream["TransactionID"].duplicated().any():
        raise ValueError("Duplicate IEEE transaction IDs")
    if (pd.to_numeric(stream["TransactionID"]) < 0).any():
        raise ValueError("Raw transaction IDs must not clash with synthetic negatives")

    horizon = pd.Timestamp("1970-01-01T00:00:00Z") + pd.to_timedelta(
        int(stream["TransactionDT"].max()), unit="s"
    )
    rows = []
    slots = int(stream["isFraud"].sum())
    # Do not materialize 88k wide event dictionaries per configuration.
    column_names = list(stream.columns)
    for seed in range(seeds):
        for mode in ("static", "adaptive"):
            for policy_name in ("fixed", "capacity_aware"):
                for capacity_ratio in capacity_ratios:
                    scorer = scorer_factory()
                    rng = random.Random(seed + 100_000)
                    if mode == "static":
                        fraudster = StaticMixtureFraudster(
                            gen.strategy_weights, reward_scale=gen.reward_scale, seed=seed
                        )
                    else:
                        fraudster = AdaptiveFraudster(
                            gen.strategies,
                            learning_rate=learning_rate,
                            epsilon=epsilon,
                            reward_scale=gen.reward_scale,
                            consecutive_block_limit=1_000_000,
                            dormancy_steps=0,
                            seed=seed,
                        )
                    if policy_name == "fixed":
                        policy = FixedThresholdPolicy(
                            review_threshold=cal["base"], block_threshold=cal["block"]
                        )
                    else:
                        policy = TieredCapacityAwarePolicy(
                            base_review_threshold=cal["base"],
                            soft_review_threshold=cal["soft"],
                            hard_review_threshold=cal["hard"],
                            block_threshold=cal["block"],
                            soft_backlog_hours=soft_backlog_hours,
                            hard_backlog_hours=hard_backlog_hours,
                        )
                    engine = PolicyQueueEngine(
                        policy,
                        cal["reference_rate_per_hour"] * capacity_ratio,
                        discipline="fifo",
                        horizon_end=horizon,
                    )
                    count = {name: 0 for name in gen.strategies}
                    attempt = 0
                    for values in stream.itertuples(index=False, name=None):
                        raw = dict(zip(column_names, values))
                        is_fraud = bool(raw["isFraud"])
                        strategy = None
                        if is_fraud:
                            strategy = fraudster.choose_strategy(attempt)
                            if strategy is None:
                                raise AssertionError("Dormancy must be disabled in core")
                            event = gen.sample_raw(
                                strategy, rng, int(raw["TransactionDT"]), attempt
                            )
                            count[strategy] += 1
                        else:
                            event = raw
                        p = scorer.score_and_update(event)
                        at = pd.Timestamp("1970-01-01T00:00:00Z") + pd.to_timedelta(
                            int(event["TransactionDT"]), unit="s"
                        )
                        action = engine.process_event({
                            "TransactionId": int(event["TransactionID"]),
                            "TransactionStartTime": at,
                            "Value": float(event["TransactionAmt"]),
                            "FraudResult": int(is_fraud),
                            "risk_probability": p,
                            "strategy": strategy,
                        })
                        if is_fraud:
                            if review_feedback == "policy_action" or action.value != "REVIEW":
                                reward_input_amount = (float(event["TransactionAmt"])
                                    if reward_amount_mode == "value" else gen.reward_scale)
                                fraudster.observe(
                                    action.value, reward_input_amount, attempt
                                )
                            attempt += 1
                    summary, decisions, reviews = engine.finalize(horizon)
                    if attempt != slots:
                        raise AssertionError("Fraud attempt slots were changed")
                    summary.update({
                        "dataset": "IEEE-CIS",
                        "seed": seed,
                        "fraudster_mode": mode,
                        "policy": policy_name,
                        "capacity_ratio": float(capacity_ratio),
                        "fraud_attempt_slots": slots,
                        "review_feedback_assumption": review_feedback,
                        "reward_amount_mode": reward_amount_mode,
                        "alpha": learning_rate,
                        "epsilon": epsilon,
                        "max_test_events": len(stream),
                        "validation_review_threshold": cal["base"],
                        "validation_block_threshold": cal["block"],
                    })
                    for strategy, n in count.items():
                        summary[f"strategy_share_{strategy}"] = n / max(1, attempt)
                    # Make outcome semantics sensitivity explicit. These are
                    # hypothetical conditional expectations, NOT bank loss.
                    for q in (0.0, 0.5, 1.0):
                        extra = expected_outcomes_by_horizon(
                            decisions, reviews, horizon,
                            review_prevention_probability=q,
                        )
                        label = str(q).replace(".", "p")
                        summary[f"assumed_q_{label}_prevented_value"] = extra[
                            "expected_prevented_fraud_value_under_assumption"
                        ]
                        summary[f"assumed_q_{label}_exposure_value"] = extra[
                            "fraud_exposure_upper_bound_at_horizon_under_assumption"
                        ]
                    rows.append(summary)
    return pd.DataFrame(rows)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--validation-scores", required=True)
    p.add_argument("--validation-donors", required=True)
    p.add_argument("--test-context", required=True)
    p.add_argument("--history-context", required=True)
    p.add_argument("--model-bundle", required=True)
    p.add_argument("--output-dir", required=True)
    p.add_argument("--seeds", type=int, default=1)
    p.add_argument("--max-test-events", type=int, default=None)
    p.add_argument("--review-feedback", default="policy_action",
                   choices=["policy_action", "no_review_observation"])
    p.add_argument("--capacities", default="0.75,1.0,1.25")
    p.add_argument("--alpha", type=float, default=0.15)
    p.add_argument("--epsilon", type=float, default=0.10)
    p.add_argument("--reward-amount-mode", choices=["value", "unit"], default="value")
    p.add_argument("--scorer", choices=["reference", "fast"], default="reference",
                   help="Use fast only after empirical equivalence audit")
    args = p.parse_args()

    bundle = joblib.load(args.model_bundle)
    scorer_class = (IEEEOnlineRiskScorer if args.scorer == "reference"
                    else FastIEEEOnlineRiskScorer)
    baseline = scorer_class(bundle)
    history = pd.read_csv(args.history_context, low_memory=False)
    baseline.warm_history(history)
    frozen_state = baseline.state
    del history

    def scorer_factory():
        scorer = scorer_class(bundle)
        scorer.state = deepcopy(frozen_state)
        return scorer

    output = run_experiments(
        pd.read_csv(args.validation_scores),
        pd.read_csv(args.validation_donors, low_memory=False),
        pd.read_csv(args.test_context, low_memory=False),
        scorer_factory,
        seeds=args.seeds,
        capacity_ratios=tuple(float(x) for x in args.capacities.split(",")),
        review_feedback=args.review_feedback,
        reward_amount_mode=args.reward_amount_mode,
        learning_rate=args.alpha,
        epsilon=args.epsilon,
        max_test_events=args.max_test_events,
    )
    folder = Path(args.output_dir)
    folder.mkdir(parents=True, exist_ok=True)
    output.to_csv(folder / "ieee_closed_loop_runs.csv", index=False)
    (folder / "experiment_metadata.json").write_text(
        json.dumps({
            "mode": "counterfactual feature-level online re-score",
            "risk_model": str(args.model_bundle),
            "scorer": args.scorer,
            "mandatory_condition": "run IEEE online equivalence audit before interpretation",
            "seeds": args.seeds,
            "max_test_events": args.max_test_events,
            "review_feedback": args.review_feedback,
            "reward_amount_mode": args.reward_amount_mode,
            "alpha": args.alpha,
            "epsilon": args.epsilon,
            "validation_generator_only": True,
            "pretest_history_warmup": True,
            "claim_boundary": "research stress scenario, not real-world bank loss",
        }, indent=2), encoding="utf-8"
    )
    print(output[[
        "seed", "fraudster_mode", "policy", "capacity_ratio",
        "fraud_attempt_slots", "fraud_intercept_rate", "backlog_end"
    ]].to_string(index=False))


if __name__ == "__main__":
    main()
