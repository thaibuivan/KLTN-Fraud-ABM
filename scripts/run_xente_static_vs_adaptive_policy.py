"""Run the first Xente-grounded Static vs Adaptive policy pilot.

This runner uses:
- chronological validation fraud score/value pairs as empirical strategy templates;
- test fraud timestamps as fraud-attempt opportunities;
- observed legitimate test transactions as the background stream;
- the shared Fixed / Capacity-aware policy logic;
- the shared persistent review queue.

It is a counterfactual integration pilot, not a final thesis result.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from scripts.adaptive_fraudster import (
    AdaptiveFraudster,
    StaticMixtureFraudster,
)
from scripts.fraud_policies import (
    CapacityAwarePolicy,
    FixedThresholdPolicy,
)
from scripts.simulate_adaptive_policy_system import (
    simulate_adaptive_policy_system,
)
from scripts.simulate_alert_queue import (
    threshold_for_target_rate,
)
from scripts.xente_fraud_templates import (
    XenteFraudTemplateGenerator,
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--validation-scores",
        required=True,
    )
    parser.add_argument(
        "--test-scores",
        required=True,
    )
    parser.add_argument(
        "--target-review-rate",
        type=float,
        default=0.01,
    )
    parser.add_argument(
        "--capacity-ratios",
        default="0.75,1.0,1.25",
    )
    parser.add_argument(
        "--seeds",
        type=int,
        default=30,
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
        "--discipline",
        default="risk_priority",
    )
    parser.add_argument(
        "--block-threshold",
        type=float,
        default=1.0,
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
        "--soft-increment",
        type=float,
        default=0.05,
    )
    parser.add_argument(
        "--hard-increment",
        type=float,
        default=0.10,
    )
    parser.add_argument(
        "--output-dir",
        default=(
            "outputs/local/"
            "xente_static_adaptive_policy"
        ),
    )
    return parser.parse_args()


def aggregate(runs: pd.DataFrame) -> pd.DataFrame:
    keys = [
        "fraudster_mode",
        "policy",
        "capacity_ratio",
    ]
    metrics = [
        "successful_fraud_value",
        "fraud_intercept_rate",
        "fraud_intercepted",
        "legitimate_review_count",
        "backlog_end",
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
            row[f"{metric}_p05"] = (
                float(values.quantile(0.05))
                if len(values)
                else None
            )
            row[f"{metric}_p95"] = (
                float(values.quantile(0.95))
                if len(values)
                else None
            )
        rows.append(row)
    return pd.DataFrame(rows)


def main() -> None:
    args = parse_args()
    if args.seeds < 1:
        raise ValueError("--seeds must be >= 1")

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

    generator = (
        XenteFraudTemplateGenerator
        .from_validation_scores(validation)
    )

    review_threshold = threshold_for_target_rate(
        validation,
        args.target_review_rate,
    )
    reference_alerts = validation.loc[
        validation["risk_probability"]
        >= review_threshold
    ]
    reference_rate = mean_arrival_rate_per_hour(
        reference_alerts
    )
    if reference_rate <= 0:
        raise ValueError(
            "Reference alert-arrival rate must be positive"
        )

    rows = []
    capacity_ratios = [
        float(value)
        for value in args.capacity_ratios.split(",")
    ]

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
                    service_rate = (
                        reference_rate
                        * capacity_ratio
                    )

                    if fraudster_mode == "adaptive":
                        fraudster = AdaptiveFraudster(
                            generator.strategies,
                            learning_rate=(
                                args.learning_rate
                            ),
                            epsilon=args.epsilon,
                            seed=seed,
                        )
                    else:
                        fraudster = (
                            StaticMixtureFraudster(
                                generator.strategy_weights,
                                seed=seed,
                            )
                        )

                    if policy_name == "fixed":
                        policy = FixedThresholdPolicy(
                            review_threshold=(
                                review_threshold
                            ),
                            block_threshold=(
                                args.block_threshold
                            ),
                        )
                    else:
                        policy = CapacityAwarePolicy(
                            base_review_threshold=(
                                review_threshold
                            ),
                            block_threshold=(
                                args.block_threshold
                            ),
                            soft_backlog_hours=(
                                args.soft_backlog_hours
                            ),
                            hard_backlog_hours=(
                                args.hard_backlog_hours
                            ),
                            soft_increment=(
                                args.soft_increment
                            ),
                            hard_increment=(
                                args.hard_increment
                            ),
                        )

                    summary, _, _ = (
                        simulate_adaptive_policy_system(
                            test,
                            policy,
                            fraudster,
                            generator,
                            service_rate,
                            discipline=(
                                args.discipline
                            ),
                            seed=seed + 100_000,
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
                            "review_threshold": (
                                review_threshold
                            ),
                            "reference_service_rate": (
                                reference_rate
                            ),
                            "learning_rate": (
                                args.learning_rate
                            ),
                            "epsilon": args.epsilon,
                        }
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
    generator.summary().to_csv(
        output_dir / "template_summary.csv",
        index=False,
    )

    print("Template regimes")
    print(
        generator.summary().to_string(
            index=False
        )
    )
    print("\nExperiment summary")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
