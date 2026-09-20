"""Simulate a persistent fraud-alert queue on scored Xente holdout data.

This script intentionally avoids bank-specific analyst cases/day assumptions.
Instead it uses a relative pooled-capacity ratio:

    capacity_ratio = service_rate / mean_alert_arrival_rate

Example:
    python scripts/simulate_alert_queue.py \
      --validation-scores outputs/local/xente_baseline/validation_scores.csv \
      --test-scores outputs/local/xente_baseline/test_scores.csv \
      --target-alert-rate 0.01 \
      --capacity-ratios 0.75,1.0,1.25 \
      --output-dir outputs/local/queue

Raw/scored row-level outputs remain local/gitignored.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd


def threshold_for_target_rate(
    validation: pd.DataFrame, target_rate: float
) -> float:
    """Freeze a threshold chosen only on validation data."""
    if not 0 < target_rate < 1:
        raise ValueError("target_rate must be between 0 and 1")

    p = validation["risk_probability"].to_numpy(dtype=float)
    k = max(1, int(np.ceil(len(p) * target_rate)))
    return float(np.partition(p, len(p) - k)[len(p) - k])


def choose_item(
    queue: list[dict], discipline: str
) -> dict:
    if discipline == "fifo":
        return queue.pop(0)

    if discipline == "risk_priority":
        idx = max(
            range(len(queue)),
            key=lambda i: (
                queue[i]["risk_probability"],
                -queue[i]["arrival"].value,
            ),
        )
        return queue.pop(idx)

    raise ValueError(f"Unknown discipline: {discipline}")


def simulate(
    test: pd.DataFrame,
    threshold: float,
    capacity_ratio: float,
    discipline: str,
) -> tuple[dict, pd.DataFrame]:
    """Replay alerts through a single pooled service process.

    The service rate is an abstract pooled-team capacity, not a claim about
    one human analyst's speed.
    """
    if capacity_ratio <= 0:
        raise ValueError("capacity_ratio must be positive")

    alerts = (
        test[test["risk_probability"] >= threshold]
        .copy()
        .sort_values(["TransactionStartTime", "TransactionId"])
    )

    if alerts.empty:
        raise ValueError("No alerts were generated at this threshold")

    horizon_start = alerts["TransactionStartTime"].min()
    horizon_end = test["TransactionStartTime"].max()
    horizon_hours = max(
        (horizon_end - horizon_start).total_seconds() / 3600.0,
        1e-9,
    )

    mean_alert_arrival_rate = len(alerts) / horizon_hours
    pooled_service_rate = max(
        mean_alert_arrival_rate * capacity_ratio,
        1e-9,
    )
    service_hours_per_alert = 1.0 / pooled_service_rate

    arrivals: list[dict] = []
    for row in alerts.itertuples(index=False):
        arrivals.append(
            {
                "TransactionId": row.TransactionId,
                "CustomerId": row.CustomerId,
                "arrival": row.TransactionStartTime,
                "Value": float(row.Value),
                "FraudResult": int(row.FraudResult),
                "risk_probability": float(row.risk_probability),
                "seen_in_train_customer": int(
                    row.seen_in_train_customer
                ),
            }
        )

    queue: list[dict] = []
    i = 0
    server_available = horizon_start
    records: list[dict] = []

    while i < len(arrivals) or queue:
        if not queue:
            if i >= len(arrivals):
                break

            if server_available < arrivals[i]["arrival"]:
                server_available = arrivals[i]["arrival"]

            while (
                i < len(arrivals)
                and arrivals[i]["arrival"] <= server_available
            ):
                queue.append(arrivals[i])
                i += 1
        else:
            while (
                i < len(arrivals)
                and arrivals[i]["arrival"] <= server_available
            ):
                queue.append(arrivals[i])
                i += 1

        item = choose_item(queue, discipline)
        service_start = max(server_available, item["arrival"])

        # If alerts arrived before this actual service start, they are eligible
        # for non-preemptive risk-priority selection.
        while (
            i < len(arrivals)
            and arrivals[i]["arrival"] <= service_start
        ):
            queue.append(arrivals[i])
            i += 1

            if discipline == "risk_priority":
                queue.append(item)
                item = choose_item(queue, discipline)
                service_start = max(server_available, item["arrival"])

        service_end = service_start + pd.Timedelta(
            hours=service_hours_per_alert
        )
        waiting_minutes = (
            service_start - item["arrival"]
        ).total_seconds() / 60.0

        records.append(
            {
                **item,
                "service_start": service_start,
                "service_end": service_end,
                "waiting_minutes": waiting_minutes,
                "reviewed_within_horizon": int(
                    service_start <= horizon_end
                ),
                "backlog_after_start": len(queue),
            }
        )
        server_available = service_end

    reviewed = pd.DataFrame(records)
    within = reviewed["reviewed_within_horizon"].eq(1)
    fraud = reviewed["FraudResult"].eq(1)
    all_test_fraud = int(test["FraudResult"].sum())

    summary = {
        "discipline": discipline,
        "threshold": threshold,
        "realized_test_alert_rate": len(alerts) / len(test),
        "alerts": int(len(alerts)),
        "fraud_alerts": int(fraud.sum()),
        "capacity_ratio_to_mean_alert_arrival": capacity_ratio,
        "mean_alert_arrival_rate_per_hour": mean_alert_arrival_rate,
        "pooled_service_rate_per_hour": pooled_service_rate,
        "implied_service_interval_minutes": 60.0 / pooled_service_rate,
        "reviewed_within_horizon": int(within.sum()),
        "backlog_end": int((~within).sum()),
        "mean_wait_minutes": float(
            reviewed["waiting_minutes"].mean()
        ),
        "p95_wait_minutes": float(
            reviewed["waiting_minutes"].quantile(0.95)
        ),
        "max_wait_minutes": float(
            reviewed["waiting_minutes"].max()
        ),
        "fraud_reviewed_within_horizon": int(
            (within & fraud).sum()
        ),
        "fraud_capture_within_horizon": (
            float((within & fraud).sum() / all_test_fraud)
            if all_test_fraud
            else None
        ),
        "false_positive_reviewed_within_horizon": int(
            (within & ~fraud).sum()
        ),
    }
    return summary, reviewed


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--validation-scores", required=True)
    parser.add_argument("--test-scores", required=True)
    parser.add_argument(
        "--target-alert-rate", type=float, default=0.01
    )
    parser.add_argument(
        "--capacity-ratios", default="0.75,1.0,1.25"
    )
    parser.add_argument(
        "--output-dir", default="outputs/local/queue"
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

    threshold = threshold_for_target_rate(
        validation, args.target_alert_rate
    )

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    rows: list[dict] = []
    for capacity_ratio in [
        float(value)
        for value in args.capacity_ratios.split(",")
    ]:
        for discipline in ("fifo", "risk_priority"):
            summary, reviewed = simulate(
                test=test,
                threshold=threshold,
                capacity_ratio=capacity_ratio,
                discipline=discipline,
            )
            summary["target_validation_alert_rate"] = (
                args.target_alert_rate
            )
            rows.append(summary)

            reviewed.to_csv(
                output_dir
                / (
                    f"queue_{discipline}_capacity_"
                    f"{capacity_ratio:.2f}.csv"
                ),
                index=False,
            )

    summary_df = pd.DataFrame(rows)
    summary_df.to_csv(
        output_dir / "queue_summary.csv", index=False
    )
    (output_dir / "queue_summary.json").write_text(
        json.dumps(rows, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(summary_df.to_string(index=False))


if __name__ == "__main__":
    main()
