"""Run queue sensitivity across validation-selected target alert rates.

Unlike the standard capacity stress test, this experiment holds absolute pooled
service capacity fixed across thresholds. Capacity is anchored to a reference
validation alert stream (default: 1% target alert rate) and then replayed on
all test thresholds. This prevents analyst capacity from increasing simply
because a more sensitive threshold generates more alerts.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from simulate_alert_queue import (
    simulate,
    threshold_for_target_rate,
)


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
        "--alert-rates",
        default="0.005,0.01,0.02,0.05",
    )
    parser.add_argument(
        "--reference-alert-rate",
        type=float,
        default=0.01,
    )
    parser.add_argument(
        "--capacity-ratios",
        default="0.75,1.0,1.25",
    )
    parser.add_argument(
        "--service-cv",
        type=float,
        default=0.0,
    )
    parser.add_argument(
        "--seeds",
        type=int,
        default=1,
    )
    parser.add_argument(
        "--output-dir",
        default=(
            "outputs/local/"
            "alert_rate_sensitivity"
        ),
    )
    return parser.parse_args()


def alert_arrival_rate_per_hour(
    frame: pd.DataFrame,
    threshold: float,
) -> float:
    start = frame[
        "TransactionStartTime"
    ].min()
    end = frame[
        "TransactionStartTime"
    ].max()
    hours = max(
        (end - start).total_seconds()
        / 3600.0,
        1e-9,
    )
    alerts = int(
        (
            frame["risk_probability"]
            >= threshold
        ).sum()
    )
    return alerts / hours


def main() -> None:
    args = parse_args()
    if args.seeds < 1:
        raise ValueError(
            "--seeds must be >= 1"
        )

    validation = pd.read_csv(
        args.validation_scores
    )
    test = pd.read_csv(
        args.test_scores
    )
    validation[
        "TransactionStartTime"
    ] = pd.to_datetime(
        validation[
            "TransactionStartTime"
        ],
        utc=True,
    )
    test[
        "TransactionStartTime"
    ] = pd.to_datetime(
        test["TransactionStartTime"],
        utc=True,
    )

    alert_rates = [
        float(v)
        for v
        in args.alert_rates.split(",")
    ]
    capacity_ratios = [
        float(v)
        for v
        in args.capacity_ratios.split(",")
    ]

    reference_threshold = (
        threshold_for_target_rate(
            validation,
            args.reference_alert_rate,
        )
    )
    reference_arrival_rate = (
        alert_arrival_rate_per_hour(
            validation,
            reference_threshold,
        )
    )

    rows: list[dict] = []
    for target_rate in alert_rates:
        threshold = (
            threshold_for_target_rate(
                validation,
                target_rate,
            )
        )

        for requested_capacity_ratio in (
            capacity_ratios
        ):
            fixed_service_rate = (
                reference_arrival_rate
                * requested_capacity_ratio
            )

            for discipline in (
                "fifo",
                "risk_priority",
            ):
                for seed in range(
                    args.seeds
                ):
                    summary, _ = simulate(
                        test=test,
                        threshold=threshold,
                        capacity_ratio=(
                            requested_capacity_ratio
                        ),
                        discipline=discipline,
                        service_cv=(
                            args.service_cv
                        ),
                        seed=seed,
                        pooled_service_rate_per_hour=(
                            fixed_service_rate
                        ),
                    )
                    summary[
                        "target_validation_alert_rate"
                    ] = target_rate
                    summary[
                        "reference_validation_alert_rate"
                    ] = (
                        args.reference_alert_rate
                    )
                    summary[
                        (
                            "reference_validation_"
                            "alert_arrival_rate_"
                            "per_hour"
                        )
                    ] = (
                        reference_arrival_rate
                    )
                    rows.append(summary)

    runs = pd.DataFrame(rows)

    group_cols = [
        "target_validation_alert_rate",
        "reference_validation_alert_rate",
        "requested_capacity_ratio",
        "discipline",
        "service_cv",
        "threshold",
        "realized_test_alert_rate",
        "alerts",
        "fraud_alerts",
        "pooled_service_rate_per_hour",
        (
            "capacity_ratio_to_"
            "mean_alert_arrival"
        ),
    ]

    metric_cols = [
        "reviewed_within_horizon",
        "backlog_end",
        "fraud_capture_within_horizon",
        "seen_fraud_capture_within_horizon",
        "unseen_fraud_capture_within_horizon",
        "mean_wait_minutes",
        "p95_wait_minutes",
        "p99_wait_minutes",
        "share_wait_over_24h",
        "share_wait_over_48h",
        "share_wait_over_72h",
        "low_priority_p95_wait_minutes",
        "high_priority_p95_wait_minutes",
    ]

    summaries: list[dict] = []
    for keys, group in runs.groupby(
        group_cols,
        dropna=False,
    ):
        row = dict(
            zip(group_cols, keys)
        )
        for metric in metric_cols:
            values = group[
                metric
            ].dropna()
            row[
                f"{metric}_mean"
            ] = (
                float(values.mean())
                if len(values)
                else None
            )
            row[
                f"{metric}_p05"
            ] = (
                float(
                    values.quantile(0.05)
                )
                if len(values)
                else None
            )
            row[
                f"{metric}_p95"
            ] = (
                float(
                    values.quantile(0.95)
                )
                if len(values)
                else None
            )
        summaries.append(row)

    summary = pd.DataFrame(
        summaries
    )

    output_dir = Path(
        args.output_dir
    )
    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )
    runs.to_csv(
        output_dir
        / "alert_rate_runs.csv",
        index=False,
    )
    summary.to_csv(
        output_dir
        / "alert_rate_summary.csv",
        index=False,
    )

    print(
        summary.to_string(index=False)
    )


if __name__ == "__main__":
    main()
