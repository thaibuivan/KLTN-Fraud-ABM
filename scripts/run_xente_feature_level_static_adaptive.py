"""Run the feature-level Xente Static vs Adaptive integration pilot.

Compared with the earlier score/value-template pilot, generated fraud events now:
- resample raw fraud context from chronological validation fraud rows;
- build past-only synthetic-fraudster history online;
- are rescored through the saved Xente baseline model.

Observed legitimate test transactions retain their empirical precomputed risk
scores. Historical test fraud timestamps are used only as fraud-attempt
opportunity slots.

This remains a counterfactual stress test, not observed fraudster cognition.
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
from scripts.policy_queue_engine import (
    PolicyQueueEngine,
)
from scripts.simulate_alert_queue import (
    threshold_for_target_rate,
)
from scripts.train_xente_baseline import (
    CATEGORICAL_FEATURES,
    NUMERIC_FEATURES,
)
from scripts.xente_feature_level_fraud import (
    XenteFeatureLevelFraudGenerator,
)
from scripts.xente_online_features import (
    XenteOnlineFeatureBuilder,
)


def mean_arrival_rate_per_hour(
    alerts: pd.DataFrame,
) -> float:
    if len(alerts) <= 1:
        return 0.0

    hours = (
        alerts["TransactionStartTime"].max()
        - alerts["TransactionStartTime"].min()
    ).total_seconds() / 3600.0

    return len(alerts) / max(hours, 1e-9)


def aggregate(runs: pd.DataFrame) -> pd.DataFrame:
    keys = [
        "fraudster_mode",
        "policy",
        "capacity_ratio",
    ]
    metrics = [
        "fraud_intercept_rate",
        "fraud_exposure_at_horizon",
        "successful_fraud_value",
        "unresolved_fraud_value",
        "backlog_end",
        "legitimate_intervention_rate",
        "mean_wait_minutes",
        "p95_wait_minutes",
        "strategy_share_low_value",
        "strategy_share_medium_value",
        "strategy_share_high_value",
    ]

    rows = []
    for group_key, group in runs.groupby(keys):
        row = dict(zip(keys, group_key))
        for metric in metrics:
            values = group[metric].dropna()
            row[f"{metric}_mean"] = (
                float(values.mean())
                if len(values)
                else None
            )
            row[f"{metric}_sd"] = (
                float(values.std(ddof=1))
                if len(values) > 1
                else 0.0
            )
        rows.append(row)

    return pd.DataFrame(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--raw-training",
        required=True,
    )
    parser.add_argument(
        "--validation-scores",
        required=True,
    )
    parser.add_argument(
        "--test-scores",
        required=True,
    )
    parser.add_argument(
        "--model",
        required=True,
    )

    parser.add_argument(
        "--base-review-rate",
        type=float,
        default=0.01,
    )
    parser.add_argument(
        "--soft-review-rate",
        type=float,
        default=0.0075,
    )
    parser.add_argument(
        "--hard-review-rate",
        type=float,
        default=0.005,
    )
    parser.add_argument(
        "--block-rate",
        type=float,
        default=0.001,
    )

    parser.add_argument(
        "--capacity-ratios",
        default="0.75,1.0,1.25",
    )
    parser.add_argument(
        "--soft-backlog-hours",
        type=float,
        default=24.0,
    )
    parser.add_argument(
        "--hard-backlog-hours",
        type=float,
        default=72.0,
    )
    parser.add_argument(
        "--discipline",
        default="fifo",
    )

    parser.add_argument(
        "--learning-rate",
        type=float,
        default=0.15,
    )
    parser.add_argument(
        "--epsilon",
        type=float,
        default=0.10,
    )
    parser.add_argument(
        "--seeds",
        type=int,
        default=5,
    )
    parser.add_argument(
        "--output-dir",
        default=(
            "outputs/local/"
            "xente_feature_level_adaptive"
        ),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

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
    validation_raw = raw.iloc[
        train_end:valid_end
    ].copy()

    validation = pd.read_csv(
        args.validation_scores
    )
    test = pd.read_csv(
        args.test_scores
    )
    for frame in (validation, test):
        frame["TransactionStartTime"] = pd.to_datetime(
            frame["TransactionStartTime"],
            utc=True,
        )

    model = joblib.load(args.model)
    generator = (
        XenteFeatureLevelFraudGenerator
        .from_validation_raw(
            validation_raw
        )
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
    block_threshold = threshold_for_target_rate(
        validation,
        args.block_rate,
    )

    reference_alerts = validation.loc[
        validation["risk_probability"]
        >= base_threshold
    ]
    reference_rate = mean_arrival_rate_per_hour(
        reference_alerts
    )

    horizon_end = test[
        "TransactionStartTime"
    ].max()

    legitimate = test.loc[
        test["FraudResult"].eq(0)
    ].copy()
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
        for slot, timestamp in enumerate(
            fraud_slots
        )
    )
    timeline.sort(
        key=lambda item: (
            item[0],
            item[1],
        )
    )

    capacity_ratios = [
        float(value)
        for value in args.capacity_ratios.split(",")
    ]

    rows = []

    for seed in range(args.seeds):
        for fraudster_mode in (
            "static",
            "adaptive",
        ):
            for policy_name in (
                "fixed",
                "capacity_aware",
            ):
                for capacity_ratio in capacity_ratios:
                    feature_builder = (
                        XenteOnlineFeatureBuilder()
                    )
                    rng = random.Random(
                        seed + 100_000
                    )

                    if fraudster_mode == "static":
                        fraudster = (
                            StaticMixtureFraudster(
                                generator.strategy_weights,
                                reward_scale=(
                                    generator.reward_scale
                                ),
                                seed=seed,
                            )
                        )
                    else:
                        fraudster = AdaptiveFraudster(
                            generator.strategies,
                            learning_rate=(
                                args.learning_rate
                            ),
                            epsilon=args.epsilon,
                            # Dormancy is not core because it changes
                            # the number of fraud attempts.
                            consecutive_block_limit=1_000_000,
                            dormancy_steps=0,
                            reward_scale=(
                                generator.reward_scale
                            ),
                            seed=seed,
                        )

                    if policy_name == "fixed":
                        policy = FixedThresholdPolicy(
                            review_threshold=(
                                base_threshold
                            ),
                            block_threshold=(
                                block_threshold
                            ),
                        )
                    else:
                        policy = (
                            TieredCapacityAwarePolicy(
                                base_review_threshold=(
                                    base_threshold
                                ),
                                soft_review_threshold=(
                                    soft_threshold
                                ),
                                hard_review_threshold=(
                                    hard_threshold
                                ),
                                block_threshold=(
                                    block_threshold
                                ),
                                soft_backlog_hours=(
                                    args.soft_backlog_hours
                                ),
                                hard_backlog_hours=(
                                    args.hard_backlog_hours
                                ),
                            )
                        )

                    engine = PolicyQueueEngine(
                        policy,
                        reference_rate
                        * capacity_ratio,
                        discipline=args.discipline,
                        horizon_end=horizon_end,
                    )

                    strategy_counts = {
                        name: 0
                        for name in generator.strategies
                    }
                    fraud_step = 0

                    for (
                        timestamp,
                        event_type,
                        payload,
                    ) in timeline:
                        if event_type == 0:
                            row = payload
                            engine.process_event(
                                {
                                    "TransactionId": (
                                        row.TransactionId
                                    ),
                                    "CustomerId": (
                                        row.CustomerId
                                    ),
                                    "TransactionStartTime": (
                                        row.TransactionStartTime
                                    ),
                                    "Value": float(
                                        row.Value
                                    ),
                                    "FraudResult": 0,
                                    "risk_probability": float(
                                        row.risk_probability
                                    ),
                                    "strategy": None,
                                }
                            )
                            continue

                        strategy = (
                            fraudster.choose_strategy(
                                fraud_step
                            )
                        )

                        raw_event = (
                            generator.sample_raw(
                                strategy,
                                rng,
                                timestamp,
                                fraud_step,
                            )
                        )

                        features = (
                            feature_builder
                            .transform_and_update(
                                raw_event
                            )
                        )
                        x = pd.DataFrame(
                            [features]
                        )[
                            NUMERIC_FEATURES
                            + CATEGORICAL_FEATURES
                        ]
                        probability = float(
                            model.predict_proba(x)[
                                :, 1
                            ][0]
                        )

                        action = engine.process_event(
                            {
                                "TransactionId": (
                                    raw_event[
                                        "TransactionId"
                                    ]
                                ),
                                "CustomerId": (
                                    raw_event[
                                        "CustomerId"
                                    ]
                                ),
                                "TransactionStartTime": (
                                    timestamp
                                ),
                                "Value": float(
                                    raw_event["Value"]
                                ),
                                "FraudResult": 1,
                                "risk_probability": (
                                    probability
                                ),
                                "strategy": strategy,
                            }
                        )

                        fraudster.observe(
                            action.value,
                            float(
                                raw_event["Value"]
                            ),
                            fraud_step,
                        )
                        strategy_counts[strategy] += 1
                        fraud_step += 1

                    summary, _, _ = (
                        engine.finalize(
                            horizon_end
                        )
                    )
                    summary.update(
                        {
                            "seed": seed,
                            "fraudster_mode": (
                                fraudster_mode
                            ),
                            "policy": policy_name,
                            "capacity_ratio": (
                                capacity_ratio
                            ),
                            "base_threshold": (
                                base_threshold
                            ),
                            "soft_threshold": (
                                soft_threshold
                            ),
                            "hard_threshold": (
                                hard_threshold
                            ),
                            "block_threshold": (
                                block_threshold
                            ),
                            "learning_rate": (
                                args.learning_rate
                            ),
                            "epsilon": args.epsilon,
                        }
                    )

                    for strategy in (
                        generator.strategies
                    ):
                        count = strategy_counts[
                            strategy
                        ]
                        summary[
                            f"strategy_count_{strategy}"
                        ] = count
                        summary[
                            f"strategy_share_{strategy}"
                        ] = (
                            count / fraud_step
                            if fraud_step
                            else None
                        )

                    rows.append(summary)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    runs = pd.DataFrame(rows)
    summary = aggregate(runs)

    runs.to_csv(
        output_dir / "runs.csv",
        index=False,
    )
    summary.to_csv(
        output_dir / "summary.csv",
        index=False,
    )

    regime_summary = pd.DataFrame(
        [
            {
                "strategy": strategy,
                "n": len(
                    generator.pools[strategy]
                ),
                "weight": (
                    generator.strategy_weights[
                        strategy
                    ]
                ),
                "median_value": float(
                    generator.pools[
                        strategy
                    ]["Value"].median()
                ),
            }
            for strategy in generator.strategies
        ]
    )
    regime_summary.to_csv(
        output_dir / "regimes.csv",
        index=False,
    )

    print(
        "Thresholds",
        {
            "block": block_threshold,
            "base": base_threshold,
            "soft": soft_threshold,
            "hard": hard_threshold,
        },
    )
    print(
        "Value regime cuts",
        generator.lower_cut,
        generator.upper_cut,
    )
    print(
        "Reward scale",
        generator.reward_scale,
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
