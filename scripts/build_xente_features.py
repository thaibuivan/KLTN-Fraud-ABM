"""Build leakage-safe Xente transaction features.

Raw Xente competition files must remain local/private.

Usage:
    python scripts/build_xente_features.py \
        --input data/raw/xente/training.csv \
        --output data/interim/xente_features.csv
"""

from __future__ import annotations

import argparse
from collections import defaultdict, deque
from pathlib import Path

import numpy as np
import pandas as pd


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    required = [
        "TransactionId", "CustomerId", "Amount", "Value", "TransactionStartTime",
        "ProductCategory", "ChannelId", "ProviderId", "ProductId",
        "PricingStrategy", "FraudResult"
    ]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    data = df.copy()
    data["TransactionStartTime"] = pd.to_datetime(
        data["TransactionStartTime"], utc=True, errors="raise"
    )
    data = data.sort_values(
        ["TransactionStartTime", "TransactionId"]
    ).reset_index(drop=True)

    states: dict[str, dict] = {}
    rows: list[dict] = []

    for row in data.itertuples(index=False):
        cid = str(row.CustomerId)
        now = row.TransactionStartTime
        value = float(row.Value)

        state = states.get(cid)
        if state is None:
            state = {
                "recent": deque(),
                "count": 0,
                "sum_value": 0.0,
                "sumsq_value": 0.0,
                "last_time": None,
                "product_category_counts": defaultdict(int),
                "channel_counts": defaultdict(int),
            }
            states[cid] = state

        while state["recent"] and (
            now - state["recent"][0][0]
        ).total_seconds() > 7 * 86400:
            state["recent"].popleft()

        recent = list(state["recent"])
        threshold_1h = now - pd.Timedelta(hours=1)
        threshold_24h = now - pd.Timedelta(hours=24)

        tx_count_1h = sum(ts >= threshold_1h for ts, _ in recent)
        tx_count_24h = sum(ts >= threshold_24h for ts, _ in recent)
        tx_count_7d = len(recent)

        prior_count = int(state["count"])
        if prior_count:
            prior_mean = state["sum_value"] / prior_count
            variance = max(
                state["sumsq_value"] / prior_count - prior_mean**2, 0.0
            )
            prior_std = float(np.sqrt(variance))
            value_ratio = value / prior_mean if prior_mean > 0 else np.nan
            prior_product_share = (
                state["product_category_counts"][str(row.ProductCategory)]
                / prior_count
            )
            prior_channel_share = (
                state["channel_counts"][str(row.ChannelId)] / prior_count
            )
        else:
            prior_mean = np.nan
            prior_std = np.nan
            value_ratio = np.nan
            prior_product_share = 0.0
            prior_channel_share = 0.0

        if state["last_time"] is None:
            gap_minutes = np.nan
        else:
            gap_minutes = (now - state["last_time"]).total_seconds() / 60.0

        rows.append(
            {
                "prior_tx_count": prior_count,
                "prior_value_mean": prior_mean,
                "prior_value_std": prior_std,
                "gap_minutes": gap_minutes,
                "tx_count_1h": tx_count_1h,
                "tx_count_24h": tx_count_24h,
                "tx_count_7d": tx_count_7d,
                "value_ratio_prior_mean": value_ratio,
                "prior_product_share": prior_product_share,
                "prior_channel_share": prior_channel_share,
            }
        )

        state["recent"].append((now, value))
        state["count"] += 1
        state["sum_value"] += value
        state["sumsq_value"] += value * value
        state["last_time"] = now
        state["product_category_counts"][str(row.ProductCategory)] += 1
        state["channel_counts"][str(row.ChannelId)] += 1

    features = pd.DataFrame(rows)
    out = pd.concat([data, features], axis=1)

    out["log_value"] = np.log1p(out["Value"].clip(lower=0))
    out["is_credit"] = (out["Amount"] < 0).astype(int)
    out["hour"] = out["TransactionStartTime"].dt.hour
    out["weekday"] = out["TransactionStartTime"].dt.dayofweek

    out["log_prior_tx_count"] = np.log1p(out["prior_tx_count"])
    out["log_prior_value_mean"] = np.log1p(
        out["prior_value_mean"].clip(lower=0)
    )
    out["log_prior_value_std"] = np.log1p(
        out["prior_value_std"].clip(lower=0)
    )
    out["log_gap_minutes"] = np.log1p(
        out["gap_minutes"].clip(lower=0)
    )
    out["log_tx_count_1h"] = np.log1p(out["tx_count_1h"])
    out["log_tx_count_24h"] = np.log1p(out["tx_count_24h"])
    out["log_tx_count_7d"] = np.log1p(out["tx_count_7d"])
    out["value_ratio_clip"] = out["value_ratio_prior_mean"].clip(upper=20)

    return out


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument(
        "--output", default="data/interim/xente_features.csv"
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(input_path)
    out = build_features(df)
    out.to_csv(output_path, index=False)

    print(f"Wrote {output_path}")
    print(f"rows={len(out):,}, columns={out.shape[1]}")


if __name__ == "__main__":
    main()
