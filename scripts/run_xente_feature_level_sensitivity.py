"""Run targeted sensitivity analysis for the Xente feature-level closed loop.

This script intentionally avoids a full factorial explosion. It varies one
uncertain mechanism at a time around the current baseline while holding the
other shared settings fixed.

Sensitivity families:
1. BLOCK review-rate threshold;
2. adaptive learning rate alpha;
3. exploration epsilon;
4. capacity-aware congestion triggers.

The empirical Xente feature/risk groundwork is reused; this is not new EDA.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import random

import joblib
import pandas as pd

from scripts.adaptive_fraudster import (
    AdaptiveFraudster,
    StaticMixtureFraudster,
)
from scripts.fraud_policies import (
    FixedThresholdPolicy,
    TieredCapacityAwarePolicy,
)
from scripts.policy_queue_engine import PolicyQueueEngine
from scripts.simulate_alert_queue import threshold_for_target_rate
from scripts.xente_fast_scorer import FastXenteLogisticScorer
from scripts.xente_feature_level_fraud import (
    XenteFeatureLevelFraudGenerator,
)
from scripts.xente_online_features import XenteOnlineFeatureBuilder


def parse_float_list(text: str) -> list[float]:
    return [float(x) for x in text.split(",") if x.strip()]


def parse_trigger_pairs(text: str) -> list[tuple[float, float]]:
    pairs: list[tuple[float, float]] = []
    for chunk in text.split(","):
        soft, hard = chunk.split(":")
        pair = (float(soft), float(hard))
        if pair[1] < pair[0]:
            raise ValueError("hard congestion trigger must be >= soft trigger")
        pairs.append(pair)
    return pairs


def mean_arrival_rate_per_hour(alerts: pd.DataFrame) -> float:
    if len(alerts) <= 1:
        return 0.0
    hours = (
        alerts["TransactionStartTime"].max()
        - alerts["TransactionStartTime"].min()
    ).total_seconds() / 3600.0
    return len(alerts) / max(hours, 1e-9)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--raw-training", required=True)
    p.add_argument("--validation-scores", required=True)
    p.add_argument("--test-scores", required=True)
    p.add_argument("--model", required=True)

    p.add_argument("--seeds", type=int, default=10)

    p.add_argument("--base-review-rate", type=float, default=0.01)
    p.add_argument("--soft-review-rate", type=float, default=0.0075)
    p.add_argument("--hard-review-rate", type=float, default=0.005)

    p.add_argument("--baseline-block-rate", type=float, default=0.001)
    p.add_argument("--baseline-alpha", type=float, default=0.15)
    p.add_argument("--baseline-epsilon", type=float, default=0.10)
    p.add_argument(
        "--baseline-soft-backlog-hours",
        type=float,
        default=24.0,
    )
    p.add_argument(
        "--baseline-hard-backlog-hours",
        type=float,
        default=72.0,
    )

    p.add_argument(
        "--block-rates",
        default="0.0005,0.001,0.002",
    )
    p.add_argument(
        "--alphas",
        default="0.05,0.15,0.30",
    )
    p.add_argument(
        "--epsilons",
        default="0.05,0.10,0.20",
    )
    p.add_argument(
        "--congestion-triggers",
        default="12:48,24:72,48:120",
    )

    p.add_argument(
        "--output",
        default=(
            "outputs/local/"
            "xente_feature_level_sensitivity/runs.csv"
        ),
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()
    if args.seeds < 1:
        raise ValueError("--seeds must be >= 1")

    raw = pd.read_csv(args.raw_training)
    raw["TransactionStartTime"] = pd.to_datetime(
        raw["TransactionStartTime"],
        utc=True,
    )
    raw = raw.sort_values(
        ["TransactionStartTime", "TransactionId"]
    ).reset_index(drop=True)

    n = len(raw)
    train_end = int(n * 0.70)
    valid_end = int(n * 0.85)
    validation_raw = raw.iloc[train_end:valid_end].copy()

    validation = pd.read_csv(args.validation_scores)
    test = pd.read_csv(args.test_scores)
    for frame in (validation, test):
        frame["TransactionStartTime"] = pd.to_datetime(
            frame["TransactionStartTime"],
            utc=True,
        )

    model = joblib.load(args.model)
    scorer = FastXenteLogisticScorer(model)
    generator = XenteFeatureLevelFraudGenerator.from_validation_raw(
        validation_raw
    )

    base_threshold = threshold_for_target_rate(
        validation,
        args.base_review_rate,
    )
    soft_threshold = threshold_for_target_rate(
        validation,
        args.soft_review_rate,
    )
    hard_threshold = threshold_for_target_rate(
        validation,
        args.hard_review_rate,
    )

    reference_alerts = validation.loc[
        validation["risk_probability"] >= base_threshold
    ]
    reference_rate = mean_arrival_rate_per_hour(reference_alerts)
    if reference_rate <= 0:
        raise ValueError("validation reference service rate must be positive")

    horizon_end = test["TransactionStartTime"].max()
    legitimate_all = test.loc[test["FraudResult"].eq(0)].copy()
    legitimate = legitimate_all.loc[
        legitimate_all["risk_probability"] >= base_threshold
    ].copy()
    skipped_legitimate = len(legitimate_all) - len(legitimate)

    fraud_slots = (
        test.loc[
            test["FraudResult"].eq(1),
            "TransactionStartTime",
        ]
        .sort_values()
        .tolist()
    )

    timeline = [
        (row.TransactionStartTime, 0, row)
        for row in legitimate.itertuples(index=False)
    ]
    timeline.extend(
        (timestamp, 1, slot)
        for slot, timestamp in enumerate(fraud_slots)
    )
    timeline.sort(key=lambda item: (item[0], item[1]))

    def run_one(
        *,
        mode: str,
        policy_name: str,
        capacity_ratio: float,
        seed: int,
        alpha: float,
        epsilon: float,
        block_rate: float,
        soft_trigger: float,
        hard_trigger: float,
    ) -> dict:
        block_threshold = threshold_for_target_rate(
            validation,
            block_rate,
        )
        rng = random.Random(seed + 100_000)
        feature_builder = XenteOnlineFeatureBuilder()

        if mode == "static":
            fraudster = StaticMixtureFraudster(
                generator.strategy_weights,
                reward_scale=generator.reward_scale,
                seed=seed,
            )
        elif mode == "adaptive":
            fraudster = AdaptiveFraudster(
                generator.strategies,
                learning_rate=alpha,
                epsilon=epsilon,
                consecutive_block_limit=1_000_000,
                dormancy_steps=0,
                reward_scale=generator.reward_scale,
                seed=seed,
            )
        else:
            raise ValueError("mode must be static or adaptive")

        if policy_name == "fixed":
            policy = FixedThresholdPolicy(
                review_threshold=base_threshold,
                block_threshold=block_threshold,
            )
        elif policy_name == "capacity_aware":
            policy = TieredCapacityAwarePolicy(
                base_review_threshold=base_threshold,
                soft_review_threshold=soft_threshold,
                hard_review_threshold=hard_threshold,
                block_threshold=block_threshold,
                soft_backlog_hours=soft_trigger,
                hard_backlog_hours=hard_trigger,
            )
        else:
            raise ValueError("unknown policy")

        engine = PolicyQueueEngine(
            policy,
            reference_rate * capacity_ratio,
            discipline="fifo",
            horizon_end=horizon_end,
        )

        counts = {
            strategy: 0
            for strategy in generator.strategies
        }
        fraud_step = 0

        for timestamp, event_type, payload in timeline:
            if event_type == 0:
                row = payload
                engine.process_event(
                    {
                        "TransactionId": row.TransactionId,
                        "CustomerId": row.CustomerId,
                        "TransactionStartTime": row.TransactionStartTime,
                        "Value": float(row.Value),
                        "FraudResult": 0,
                        "risk_probability": float(row.risk_probability),
                        "strategy": None,
                    }
                )
                continue

            strategy = fraudster.choose_strategy(fraud_step)
            raw_event = generator.sample_raw(
                strategy,
                rng,
                timestamp,
                fraud_step,
            )
            features = feature_builder.transform_and_update(raw_event)
            probability = scorer.predict_proba_one(features)

            action = engine.process_event(
                {
                    "TransactionId": raw_event["TransactionId"],
                    "CustomerId": raw_event["CustomerId"],
                    "TransactionStartTime": timestamp,
                    "Value": float(raw_event["Value"]),
                    "FraudResult": 1,
                    "risk_probability": probability,
                    "strategy": strategy,
                }
            )
            fraudster.observe(
                action.value,
                float(raw_event["Value"]),
                fraud_step,
            )
            counts[strategy] += 1
            fraud_step += 1

        summary, _, _ = engine.finalize(horizon_end)
        summary["transactions"] += skipped_legitimate
        summary["approve_count"] += skipped_legitimate
        summary["legitimate_intervention_rate"] = (
            (
                summary["legitimate_review_count"]
                + summary["legitimate_block_count"]
            )
            / len(legitimate_all)
            if len(legitimate_all)
            else None
        )

        summary.update(
            {
                "mode": mode,
                "policy": policy_name,
                "capacity": capacity_ratio,
                "seed": seed,
                "alpha": alpha,
                "epsilon": epsilon,
                "block_rate": block_rate,
                "block_threshold": block_threshold,
                "soft_trigger": soft_trigger,
                "hard_trigger": hard_trigger,
            }
        )
        for strategy in generator.strategies:
            summary[f"strategy_count_{strategy}"] = counts[strategy]
            summary[f"strategy_share_{strategy}"] = (
                counts[strategy] / fraud_step
                if fraud_step
                else None
            )
        return summary

    rows: list[dict] = []

    # BLOCK sensitivity: both modes x both policies, Medium capacity.
    for block_rate in parse_float_list(args.block_rates):
        for seed in range(args.seeds):
            for mode in ("static", "adaptive"):
                for policy in ("fixed", "capacity_aware"):
                    row = run_one(
                        mode=mode,
                        policy_name=policy,
                        capacity_ratio=1.0,
                        seed=seed,
                        alpha=args.baseline_alpha,
                        epsilon=args.baseline_epsilon,
                        block_rate=block_rate,
                        soft_trigger=args.baseline_soft_backlog_hours,
                        hard_trigger=args.baseline_hard_backlog_hours,
                    )
                    row["sensitivity"] = "block_rate"
                    row["level"] = str(block_rate)
                    rows.append(row)

    # Alpha sensitivity: adaptive only, both policies, Medium capacity.
    for alpha in parse_float_list(args.alphas):
        for seed in range(args.seeds):
            for policy in ("fixed", "capacity_aware"):
                row = run_one(
                    mode="adaptive",
                    policy_name=policy,
                    capacity_ratio=1.0,
                    seed=seed,
                    alpha=alpha,
                    epsilon=args.baseline_epsilon,
                    block_rate=args.baseline_block_rate,
                    soft_trigger=args.baseline_soft_backlog_hours,
                    hard_trigger=args.baseline_hard_backlog_hours,
                )
                row["sensitivity"] = "alpha"
                row["level"] = str(alpha)
                rows.append(row)

    # Epsilon sensitivity: adaptive only, both policies, Medium capacity.
    for epsilon in parse_float_list(args.epsilons):
        for seed in range(args.seeds):
            for policy in ("fixed", "capacity_aware"):
                row = run_one(
                    mode="adaptive",
                    policy_name=policy,
                    capacity_ratio=1.0,
                    seed=seed,
                    alpha=args.baseline_alpha,
                    epsilon=epsilon,
                    block_rate=args.baseline_block_rate,
                    soft_trigger=args.baseline_soft_backlog_hours,
                    hard_trigger=args.baseline_hard_backlog_hours,
                )
                row["sensitivity"] = "epsilon"
                row["level"] = str(epsilon)
                rows.append(row)

    # Congestion-trigger sensitivity: both modes, CA only, Low capacity.
    for soft_trigger, hard_trigger in parse_trigger_pairs(
        args.congestion_triggers
    ):
        label = f"{soft_trigger:g}/{hard_trigger:g}"
        for seed in range(args.seeds):
            for mode in ("static", "adaptive"):
                row = run_one(
                    mode=mode,
                    policy_name="capacity_aware",
                    capacity_ratio=0.75,
                    seed=seed,
                    alpha=args.baseline_alpha,
                    epsilon=args.baseline_epsilon,
                    block_rate=args.baseline_block_rate,
                    soft_trigger=soft_trigger,
                    hard_trigger=hard_trigger,
                )
                row["sensitivity"] = "congestion"
                row["level"] = label
                rows.append(row)

    out = pd.DataFrame(rows)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(output, index=False)
    print(f"Wrote {output} with {len(out):,} runs")


if __name__ == "__main__":
    main()
