"""Run the integrated pre-adaptation Xente policy replay.

This verifies Fixed vs scenario-normalized Capacity-aware routing on the same
chronological Xente score stream and the same absolute pooled service capacity.

This is still a pre-adaptation pilot, not a final thesis result.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from scripts.fraud_policies import (
    FixedThresholdPolicy,
    TieredCapacityAwarePolicy,
)
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

    parser.add_argument("--base-review-rate", type=float, default=0.01)
    parser.add_argument("--soft-review-rate", type=float, default=0.0075)
    parser.add_argument("--hard-review-rate", type=float, default=0.005)

    parser.add_argument(
        "--block-threshold",
        type=float,
        default=1.0,
        help=(
            "Default 1.0 keeps BLOCK effectively off in the pre-adaptation "
            "replay so the capacity-routing mechanism can be isolated."
        ),
    )
    parser.add_argument(
        "--capacity-ratios",
        default="0.75,1.0,1.25",
        help=(
            "Pooled service capacity relative to the validation base-review "
            "alert-arrival rate."
        ),
    )
    parser.add_argument(
        "--discipline",
        default="fifo",
        help=(
            "FIFO is the core baseline to isolate routing-policy effects; "
            "risk_priority is retained for structural robustness."
        ),
    )
    parser.add_argument("--soft-backlog-hours", type=float, default=24.0)
    parser.add_argument("--hard-backlog-hours", type=float, default=72.0)
    parser.add_argument(
        "--output",
        default="outputs/local/xente_policy_replay/summary.csv",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if not (
        0 < args.hard_review_rate
        <= args.soft_review_rate
        <= args.base_review_rate
        < 1
    ):
        raise ValueError(
            "Review rates must satisfy "
            "0 < hard <= soft <= base < 1"
        )

    validation = pd.read_csv(args.validation_scores)
    test = pd.read_csv(args.test_scores)
    validation["TransactionStartTime"] = pd.to_datetime(
        validation["TransactionStartTime"], utc=True
    )
    test["TransactionStartTime"] = pd.to_datetime(
        test["TransactionStartTime"], utc=True
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
                review_threshold=base_threshold,
                block_threshold=args.block_threshold,
            ),
            "capacity_aware": TieredCapacityAwarePolicy(
                base_review_threshold=base_threshold,
                soft_review_threshold=soft_threshold,
                hard_review_threshold=hard_threshold,
                block_threshold=args.block_threshold,
                soft_backlog_hours=args.soft_backlog_hours,
                hard_backlog_hours=args.hard_backlog_hours,
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
                    "dataset": "Xente",
                    "policy": name,
                    "capacity_ratio_to_validation_reference": capacity_ratio,
                    "base_review_rate": args.base_review_rate,
                    "soft_review_rate": args.soft_review_rate,
                    "hard_review_rate": args.hard_review_rate,
                    "base_review_threshold": base_threshold,
                    "soft_review_threshold": soft_threshold,
                    "hard_review_threshold": hard_threshold,
                    "block_threshold": args.block_threshold,
                    "soft_backlog_hours": args.soft_backlog_hours,
                    "hard_backlog_hours": args.hard_backlog_hours,
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
