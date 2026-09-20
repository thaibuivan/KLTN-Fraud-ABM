"""Simulate a persistent fraud-alert queue on scored Xente holdout data.

This script avoids bank-specific analyst cases/day assumptions. Capacity is
represented as a relative pooled-capacity ratio:

    capacity_ratio = service_rate / mean_alert_arrival_rate

Deterministic service is the default. Optional lognormal service-time noise can
be added with --service-cv and repeated seeds for stochastic robustness.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd


def threshold_for_target_rate(validation: pd.DataFrame, target_rate: float) -> float:
    """Freeze a score threshold chosen only on validation data."""
    if not 0 < target_rate < 1:
        raise ValueError("target_rate must be between 0 and 1")
    p = validation["risk_probability"].to_numpy(dtype=float)
    k = max(1, int(np.ceil(len(p) * target_rate)))
    return float(np.partition(p, len(p) - k)[len(p) - k])


def choose_item(queue: list[dict], discipline: str) -> dict:
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


def lognormal_draw_parameters(mean_value: float, cv: float) -> tuple[float, float]:
    """Return lognormal (mu, sigma) for requested arithmetic mean and CV."""
    if cv < 0:
        raise ValueError("service_cv must be >= 0")
    if cv == 0:
        return float(np.log(mean_value)), 0.0
    sigma2 = np.log1p(cv * cv)
    sigma = float(np.sqrt(sigma2))
    mu = float(np.log(mean_value) - 0.5 * sigma2)
    return mu, sigma


def simulate(
    test: pd.DataFrame,
    threshold: float,
    capacity_ratio: float,
    discipline: str,
    *,
    service_cv: float = 0.0,
    seed: int = 0,
    pooled_service_rate_per_hour: float | None = None,
) -> tuple[dict, pd.DataFrame]:
    """Replay alerts through a single pooled service process.

    The pooled service rate is an abstract team capacity. It is not a claim
    about one human analyst's review speed.
    """
    if capacity_ratio <= 0:
        raise ValueError("capacity_ratio must be positive")

    required = {
        "TransactionId",
        "CustomerId",
        "TransactionStartTime",
        "Value",
        "FraudResult",
        "risk_probability",
        "seen_in_train_customer",
    }
    missing = sorted(required.difference(test.columns))
    if missing:
        raise ValueError(f"Missing score columns: {missing}")

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
    if pooled_service_rate_per_hour is None:
        pooled_service_rate = max(
            mean_alert_arrival_rate * capacity_ratio,
            1e-9,
        )
        capacity_mode = "relative_to_realized_test_alerts"
    else:
        if pooled_service_rate_per_hour <= 0:
            raise ValueError(
                "pooled_service_rate_per_hour must be positive"
            )
        pooled_service_rate = float(
            pooled_service_rate_per_hour
        )
        capacity_mode = "fixed_external_service_rate"

    effective_capacity_ratio = (
        pooled_service_rate / mean_alert_arrival_rate
    )
    mean_service_hours = 1.0 / pooled_service_rate

    rng = np.random.default_rng(seed)
    mu, sigma = lognormal_draw_parameters(mean_service_hours, service_cv)

    def draw_service_hours() -> float:
        if service_cv == 0:
            return mean_service_hours
        return float(rng.lognormal(mu, sigma))

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
                "seen_in_train_customer": int(row.seen_in_train_customer),
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

        while i < len(arrivals) and arrivals[i]["arrival"] <= server_available:
            queue.append(arrivals[i])
            i += 1

        if not queue:
            server_available = arrivals[i]["arrival"]
            continue

        item = choose_item(queue, discipline)
        service_start = max(server_available, item["arrival"])
        service_hours = draw_service_hours()
        service_end = service_start + pd.Timedelta(hours=service_hours)
        waiting_minutes = (service_start - item["arrival"]).total_seconds() / 60.0

        records.append(
            {
                **item,
                "service_start": service_start,
                "service_end": service_end,
                "service_minutes": service_hours * 60.0,
                "waiting_minutes": waiting_minutes,
                "reviewed_within_horizon": int(service_start <= horizon_end),
                "backlog_after_start": len(queue),
            }
        )
        server_available = service_end

    reviewed = pd.DataFrame(records)
    within = reviewed["reviewed_within_horizon"].eq(1)
    fraud = reviewed["FraudResult"].eq(1)
    all_test_fraud = int(test["FraudResult"].sum())

    seen_fraud_total = int(
        ((test["FraudResult"] == 1) & (test["seen_in_train_customer"] == 1)).sum()
    )
    unseen_fraud_total = int(
        ((test["FraudResult"] == 1) & (test["seen_in_train_customer"] == 0)).sum()
    )
    seen_reviewed_fraud = int(
        (within & fraud & reviewed["seen_in_train_customer"].eq(1)).sum()
    )
    unseen_reviewed_fraud = int(
        (within & fraud & reviewed["seen_in_train_customer"].eq(0)).sum()
    )

    score_q25 = float(reviewed["risk_probability"].quantile(0.25))
    score_q75 = float(reviewed["risk_probability"].quantile(0.75))
    low_priority = reviewed["risk_probability"] <= score_q25
    high_priority = reviewed["risk_probability"] >= score_q75

    summary = {
        "discipline": discipline,
        "seed": seed,
        "service_cv": service_cv,
        "threshold": threshold,
        "realized_test_alert_rate": len(alerts) / len(test),
        "alerts": int(len(alerts)),
        "fraud_alerts": int(fraud.sum()),
        "requested_capacity_ratio": capacity_ratio,
        "capacity_mode": capacity_mode,
        "capacity_ratio_to_mean_alert_arrival": (
            effective_capacity_ratio
        ),
        "mean_alert_arrival_rate_per_hour": mean_alert_arrival_rate,
        "pooled_service_rate_per_hour": pooled_service_rate,
        "mean_service_interval_minutes": 60.0 / pooled_service_rate,
        "reviewed_within_horizon": int(within.sum()),
        "backlog_end": int((~within).sum()),
        "mean_wait_minutes": float(reviewed["waiting_minutes"].mean()),
        "p95_wait_minutes": float(reviewed["waiting_minutes"].quantile(0.95)),
        "max_wait_minutes": float(reviewed["waiting_minutes"].max()),
        "p99_wait_minutes": float(reviewed["waiting_minutes"].quantile(0.99)),
        "share_wait_over_24h": float(
            (reviewed["waiting_minutes"] > 24 * 60).mean()
        ),
        "share_wait_over_48h": float(
            (reviewed["waiting_minutes"] > 48 * 60).mean()
        ),
        "share_wait_over_72h": float(
            (reviewed["waiting_minutes"] > 72 * 60).mean()
        ),
        "low_priority_p95_wait_minutes": float(
            reviewed.loc[low_priority, "waiting_minutes"].quantile(0.95)
        ),
        "high_priority_p95_wait_minutes": float(
            reviewed.loc[high_priority, "waiting_minutes"].quantile(0.95)
        ),
        "fraud_reviewed_within_horizon": int((within & fraud).sum()),
        "fraud_capture_within_horizon": (
            float((within & fraud).sum() / all_test_fraud) if all_test_fraud else None
        ),
        "seen_fraud_capture_within_horizon": (
            seen_reviewed_fraud / seen_fraud_total if seen_fraud_total else None
        ),
        "unseen_fraud_capture_within_horizon": (
            unseen_reviewed_fraud / unseen_fraud_total if unseen_fraud_total else None
        ),
        "false_positive_reviewed_within_horizon": int((within & ~fraud).sum()),
    }
    return summary, reviewed


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--validation-scores", required=True)
    parser.add_argument("--test-scores", required=True)
    parser.add_argument("--target-alert-rate", type=float, default=0.01)
    parser.add_argument("--capacity-ratios", default="0.75,1.0,1.25")
    parser.add_argument(
        "--service-cv",
        type=float,
        default=0.0,
        help="Coefficient of variation for lognormal service times. 0 = deterministic.",
    )
    parser.add_argument(
        "--seeds",
        type=int,
        default=1,
        help="Number of seeds. Use >1 only when service_cv > 0.",
    )
    parser.add_argument("--output-dir", default="outputs/local/queue")
    return parser.parse_args()


def aggregate_runs(runs: pd.DataFrame) -> pd.DataFrame:
    keys = [
        "discipline",
        "capacity_ratio_to_mean_alert_arrival",
        "service_cv",
        "threshold",
        "realized_test_alert_rate",
        "alerts",
        "fraud_alerts",
    ]
    rows: list[dict] = []
    for group_key, group in runs.groupby(keys, dropna=False):
        row = dict(zip(keys, group_key))
        for metric in [
            "reviewed_within_horizon",
            "backlog_end",
            "mean_wait_minutes",
            "p95_wait_minutes",
            "p99_wait_minutes",
            "share_wait_over_24h",
            "share_wait_over_48h",
            "share_wait_over_72h",
            "low_priority_p95_wait_minutes",
            "high_priority_p95_wait_minutes",
            "fraud_capture_within_horizon",
            "seen_fraud_capture_within_horizon",
            "unseen_fraud_capture_within_horizon",
        ]:
            s = group[metric].dropna()
            row[f"{metric}_mean"] = float(s.mean()) if len(s) else None
            row[f"{metric}_p05"] = float(s.quantile(0.05)) if len(s) else None
            row[f"{metric}_p95"] = float(s.quantile(0.95)) if len(s) else None
        rows.append(row)
    return pd.DataFrame(rows)


def main() -> None:
    args = parse_args()
    if args.seeds < 1:
        raise ValueError("--seeds must be >= 1")
    if args.service_cv == 0 and args.seeds > 1:
        print("Warning: deterministic service; repeated seeds will be identical.")

    validation = pd.read_csv(args.validation_scores)
    test = pd.read_csv(args.test_scores)
    validation["TransactionStartTime"] = pd.to_datetime(
        validation["TransactionStartTime"], utc=True
    )
    test["TransactionStartTime"] = pd.to_datetime(
        test["TransactionStartTime"], utc=True
    )

    threshold = threshold_for_target_rate(validation, args.target_alert_rate)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    run_rows: list[dict] = []
    first_detail_written: set[tuple[float, str]] = set()

    for capacity_ratio in [float(v) for v in args.capacity_ratios.split(",")]:
        for discipline in ("fifo", "risk_priority"):
            for seed in range(args.seeds):
                summary, reviewed = simulate(
                    test=test,
                    threshold=threshold,
                    capacity_ratio=capacity_ratio,
                    discipline=discipline,
                    service_cv=args.service_cv,
                    seed=seed,
                )
                summary["target_validation_alert_rate"] = args.target_alert_rate
                run_rows.append(summary)

                key = (capacity_ratio, discipline)
                if key not in first_detail_written:
                    reviewed.to_csv(
                        output_dir
                        / f"queue_{discipline}_capacity_{capacity_ratio:.2f}_seed_{seed}.csv",
                        index=False,
                    )
                    first_detail_written.add(key)

    runs = pd.DataFrame(run_rows)
    summary = aggregate_runs(runs)

    runs.to_csv(output_dir / "queue_runs.csv", index=False)
    summary.to_csv(output_dir / "queue_summary.csv", index=False)
    (output_dir / "queue_summary.json").write_text(
        json.dumps(summary.to_dict(orient="records"), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
