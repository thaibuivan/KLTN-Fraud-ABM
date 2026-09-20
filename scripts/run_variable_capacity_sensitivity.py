"""Run variable pooled-team capacity sensitivity.

This experiment holds the base pooled service rate fixed relative to a
reference validation alert stream, then adds day-level lognormal variation in
team capacity. It isolates staffing/capacity volatility from threshold changes.

Example:
    python scripts/run_variable_capacity_sensitivity.py \
      --validation-scores outputs/local/xente_baseline/validation_scores.csv \
      --test-scores outputs/local/xente_baseline/test_scores.csv \
      --target-alert-rate 0.01 \
      --reference-alert-rate 0.01 \
      --requested-capacity-ratio 1.0 \
      --team-capacity-cvs 0,0.3,0.6 \
      --seeds 100
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from simulate_alert_queue import (
    simulate,
    threshold_for_target_rate,
)


def alert_arrival_rate_per_hour(
    frame: pd.DataFrame,
    threshold: float,
) -> float:
    start = frame["TransactionStartTime"].min()
    end = frame["TransactionStartTime"].max()
    hours = max(
        (end - start).total_seconds() / 3600.0,
        1e-9,
    )
    alerts = int(
        (
            frame["risk_probability"]
            >= threshold
        ).sum()
    )
    return alerts / hours


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
        "--target-alert-rate",
        type=float,
        default=0.01,
    )
    parser.add_argument(
        "--reference-alert-rate",
        type=float,
        default=0.01,
    )
    parser.add_argument(
        "--requested-capacity-ratio",
        type=float,
        default=1.0,
    )
    parser.add_argument(
        "--team-capacity-cvs",
        default="0,0.3,0.6",
    )
    parser.add_argument(
        "--service-cv",
        type=float,
        default=0.0,
    )
    parser.add_argument(
        "--seeds",
        type=int,
        default=100,
    )
    parser.add_argument(
        "--output-dir",
        default=(
            "outputs/local/"
            "variable_capacity_sensitivity"
        ),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
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

    target_threshold = (
        threshold_for_target_rate(
            validation,
            args.target_alert_rate,
        )
    )
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
    fixed_service_rate = (
        reference_arrival_rate
        * args.requested_capacity_ratio
    )

    rows: list[dict] = []
    for team_cv in [
        float(v)
        for v
        in args.team_capacity_cvs.split(",")
    ]:
        seeds = (
            [0]
            if team_cv == 0
            and args.service_cv == 0
            else range(args.seeds)
        )
        for discipline in (
            "fifo",
            "risk_priority",
        ):
            for seed in seeds:
                summary, _ = simulate(
                    test=test,
                    threshold=target_threshold,
                    capacity_ratio=(
                        args.requested_capacity_ratio
                    ),
                    discipline=discipline,
                    service_cv=args.service_cv,
                    team_capacity_cv=team_cv,
                    seed=seed,
                    pooled_service_rate_per_hour=(
                        fixed_service_rate
                    ),
                )
                summary[
                    "target_validation_alert_rate"
                ] = args.target_alert_rate
                summary[
                    "reference_validation_alert_rate"
                ] = args.reference_alert_rate
                rows.append(summary)

    runs = pd.DataFrame(rows)

    metrics = [
        "fraud_capture_within_horizon",
        "seen_fraud_capture_within_horizon",
        "unseen_fraud_capture_within_horizon",
        "backlog_end",
        "p95_wait_minutes",
        "p99_wait_minutes",
        "low_priority_p95_wait_minutes",
        "high_priority_p95_wait_minutes",
        "share_wait_over_24h",
        "share_wait_over_48h",
        "share_wait_over_72h",
    ]

    summary_rows: list[dict] = []
    for (
        team_cv,
        discipline,
    ), group in runs.groupby(
        [
            "team_capacity_cv",
            "discipline",
        ]
    ):
        row = {
            "team_capacity_cv": team_cv,
            "discipline": discipline,
            "runs": int(len(group)),
            "requested_capacity_ratio": (
                args.requested_capacity_ratio
            ),
            "fixed_service_rate_per_hour": (
                fixed_service_rate
            ),
        }
        for metric in metrics:
            values = group[
                metric
            ].dropna()
            row[
                f"{metric}_mean"
            ] = float(values.mean())
            row[
                f"{metric}_p05"
            ] = float(
                values.quantile(0.05)
            )
            row[
                f"{metric}_p95"
            ] = float(
                values.quantile(0.95)
            )
        summary_rows.append(row)

    summary = pd.DataFrame(
        summary_rows
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
        / "variable_capacity_runs.csv",
        index=False,
    )
    summary.to_csv(
        output_dir
        / "variable_capacity_summary.csv",
        index=False,
    )

    print(
        summary.to_string(index=False)
    )


if __name__ == "__main__":
    main()
