"""Run a first integrated Xente policy-replay experiment.

This runner is intentionally pre-adaptation. It verifies that fixed-threshold and
capacity-aware policies can operate on the same chronological Xente score stream
with fixed analyst service capacity.

It is a bridge to the final static/adaptive fraudster experiment, not a final thesis
result by itself.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from scripts.fraud_policies import CapacityAwarePolicy, FixedThresholdPolicy
from scripts.simulate_alert_queue import threshold_for_target_rate
from scripts.simulate_policy_system import simulate_policy_system


def mean_arrival_rate_per_hour(alerts: pd.DataFrame) -> float:
    if len(alerts) <= 1:
        return 0.0
    start = alerts["TransactionStartTime"].min()
    end = alerts["TransactionStartTime"].max()
    hours = max((end - start).total_seconds() / 3600.0, 1e-9)
    return len(alerts) / hours


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--validation-scores", required=True)
    parser.add_argument("--test-scores", required=True)
    parser.add_argument("--target-review-rate", type=float, default=0.01)
    parser.add_argument(
        "--block-threshold",
        type=float,
        default=1.0,
        help="Default 1.0 keeps BLOCK effectively off in the first replay pilot.",
    )
    parser.add_argument(
        "--capacity-ratios",
        default="0.75,1.0,1.25",
        help="Service capacity relative to validation reference review-arrival rate.",
    )
    parser.add_argument("--discipline", default="risk_priority")
    parser.add_argument("--soft-backlog-hours", type=float, default=24.0)
    parser.add_argument("--hard-backlog-hours", type=float, default=72.0)
    parser.add_argument("--soft-increment", type=float, default=0.05)
    parser.add_argument("--hard-increment", type=float, default=0.10)
    parser.add_argument(
        "--output",
        default="outputs/local/xente_policy_replay/summary.csv",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    validation = pd.read_csv(args.validation_scores)
    test = pd.read_csv(args.test_scores)
    validation["TransactionStartTime"] = pd.to_datetime(
        validation["TransactionStartTime"], utc=True
    )
    test["TransactionStartTime"] = pd.to_datetime(
        test["TransactionStartTime"], utc=True
    )

    review_threshold = threshold_for_target_rate(
        validation,
        args.target_review_rate,
    )

    validation_reference_alerts = validation.loc[
        validation["risk_probability"] >= review_threshold
    ]
    reference_rate = mean_arrival_rate_per_hour(
        validation_reference_alerts
    )
    if reference_rate <= 0:
        raise ValueError("Reference validation alert-arrival rate must be positive")

    rows = []
    for capacity_ratio in [
        float(x) for x in args.capacity_ratios.split(",")
    ]:
        service_rate = reference_rate * capacity_ratio

        policies = {
            "fixed": FixedThresholdPolicy(
                review_threshold=review_threshold,
                block_threshold=args.block_threshold,
            ),
            "capacity_aware": CapacityAwarePolicy(
                base_review_threshold=review_threshold,
                block_threshold=args.block_threshold,
                soft_backlog_hours=args.soft_backlog_hours,
                hard_backlog_hours=args.hard_backlog_hours,
                soft_increment=args.soft_increment,
                hard_increment=args.hard_increment,
            ),
        }

        for name, policy in policies.items():
            summary, _, _ = simulate_policy_system(
                test,
                policy,
                pooled_service_rate_per_hour=service_rate,
                discipline=args.discipline,
            )
            summary.update(
                {
                    "policy": name,
                    "capacity_ratio_to_validation_reference": capacity_ratio,
                    "validation_reference_review_rate": args.target_review_rate,
                    "review_threshold": review_threshold,
                    "block_threshold": args.block_threshold,
                }
            )
            rows.append(summary)

    out = pd.DataFrame(rows)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(output, index=False)
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()
