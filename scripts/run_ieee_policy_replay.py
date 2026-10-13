"""Run the first integrated IEEE-CIS policy-replay experiment.

Expected inputs are scored validation/test CSV files containing:
- TransactionID
- TransactionDT
- TransactionAmt
- isFraud
- risk_probability

The runner converts IEEE's relative TransactionDT to an arbitrary timestamp
origin only to preserve event ordering and inter-arrival intervals. The derived
timestamps have no calendar interpretation.

This is a pre-adaptation pilot, parallel to run_xente_policy_replay.py.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from scripts.fraud_policies import (
    CapacityAwarePolicy,
    FixedThresholdPolicy,
)
from scripts.scenario_adapters import normalize_ieee_scores
from scripts.simulate_alert_queue import threshold_for_target_rate
from scripts.simulate_policy_system import simulate_policy_system


def mean_arrival_rate_per_hour(alerts: pd.DataFrame) -> float:
    if len(alerts) <= 1:
        return 0.0

    start = alerts["TransactionStartTime"].min()
    end = alerts["TransactionStartTime"].max()
    hours = max(
        (end - start).total_seconds() / 3600.0,
        1e-9,
    )
    return len(alerts) / hours


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--validation-scores", required=True)
    parser.add_argument("--test-scores", required=True)
    parser.add_argument(
        "--target-review-rate",
        type=float,
        default=0.01,
    )
    parser.add_argument(
        "--block-threshold",
        type=float,
        default=1.0,
        help=(
            "Default 1.0 keeps BLOCK effectively off in the first "
            "policy-replay pilot."
        ),
    )
    parser.add_argument(
        "--capacity-ratios",
        default="0.75,1.0,1.25",
    )
    parser.add_argument(
        "--discipline",
        default="risk_priority",
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
        "--output",
        default="outputs/local/ieee_policy_replay/summary.csv",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    validation_raw = pd.read_csv(args.validation_scores)
    test_raw = pd.read_csv(args.test_scores)

    validation = normalize_ieee_scores(validation_raw)
    test = normalize_ieee_scores(test_raw)

    review_threshold = threshold_for_target_rate(
        validation,
        args.target_review_rate,
    )

    reference_alerts = validation.loc[
        validation["risk_probability"] >= review_threshold
    ]
    reference_rate = mean_arrival_rate_per_hour(
        reference_alerts
    )
    if reference_rate <= 0:
        raise ValueError(
            "Reference validation alert-arrival rate must be positive"
        )

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
                    "dataset": "IEEE-CIS",
                    "policy": name,
                    "capacity_ratio_to_validation_reference": (
                        capacity_ratio
                    ),
                    "validation_reference_review_rate": (
                        args.target_review_rate
                    ),
                    "review_threshold": review_threshold,
                    "block_threshold": args.block_threshold,
                }
            )
            rows.append(summary)

    out = pd.DataFrame(rows)
    output = Path(args.output)
    output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    out.to_csv(
        output,
        index=False,
    )
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()
