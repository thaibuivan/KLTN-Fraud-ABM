from __future__ import annotations

from collections import defaultdict, deque

import numpy as np
import pandas as pd


class XenteOnlineFeatureBuilder:
    """Build the same past-only Xente features one event at a time.

    The class is used only for counterfactual fraud events in the adaptive
    experiment. Legitimate holdout events may continue to use their empirical
    precomputed risk scores.
    """

    def __init__(self) -> None:
        self.states: dict[str, dict] = {}

    def transform_and_update(self, event: dict) -> dict:
        cid = str(event["CustomerId"])
        now = pd.to_datetime(
            event["TransactionStartTime"],
            utc=True,
        )
        value = float(event["Value"])

        state = self.states.get(cid)
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
            self.states[cid] = state

        while state["recent"] and (
            now - state["recent"][0][0]
        ).total_seconds() > 7 * 86400:
            state["recent"].popleft()

        recent = list(state["recent"])
        threshold_1h = now - pd.Timedelta(hours=1)
        threshold_24h = now - pd.Timedelta(hours=24)

        tx_count_1h = sum(
            ts >= threshold_1h
            for ts, _ in recent
        )
        tx_count_24h = sum(
            ts >= threshold_24h
            for ts, _ in recent
        )
        tx_count_7d = len(recent)

        prior_count = int(state["count"])
        if prior_count:
            prior_mean = (
                state["sum_value"] / prior_count
            )
            variance = max(
                state["sumsq_value"] / prior_count
                - prior_mean**2,
                0.0,
            )
            prior_std = float(np.sqrt(variance))
            value_ratio = (
                value / prior_mean
                if prior_mean > 0
                else np.nan
            )
            prior_product_share = (
                state["product_category_counts"][
                    str(event["ProductCategory"])
                ]
                / prior_count
            )
            prior_channel_share = (
                state["channel_counts"][
                    str(event["ChannelId"])
                ]
                / prior_count
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
            gap_minutes = (
                now - state["last_time"]
            ).total_seconds() / 60.0

        features = dict(event)
        features["TransactionStartTime"] = now
        features.update(
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
                "log_value": np.log1p(max(value, 0.0)),
                "is_credit": int(
                    float(event["Amount"]) < 0
                ),
                "hour": now.hour,
                "weekday": now.dayofweek,
                "log_prior_tx_count": np.log1p(
                    prior_count
                ),
                "log_prior_value_mean": (
                    np.log1p(prior_mean)
                    if pd.notna(prior_mean)
                    and prior_mean >= 0
                    else np.nan
                ),
                "log_prior_value_std": (
                    np.log1p(prior_std)
                    if pd.notna(prior_std)
                    and prior_std >= 0
                    else np.nan
                ),
                "log_gap_minutes": (
                    np.log1p(gap_minutes)
                    if pd.notna(gap_minutes)
                    and gap_minutes >= 0
                    else np.nan
                ),
                "log_tx_count_1h": np.log1p(
                    tx_count_1h
                ),
                "log_tx_count_24h": np.log1p(
                    tx_count_24h
                ),
                "log_tx_count_7d": np.log1p(
                    tx_count_7d
                ),
                "value_ratio_clip": (
                    min(value_ratio, 20.0)
                    if pd.notna(value_ratio)
                    else np.nan
                ),
            }
        )

        state["recent"].append((now, value))
        state["count"] += 1
        state["sum_value"] += value
        state["sumsq_value"] += value * value
        state["last_time"] = now
        state["product_category_counts"][
            str(event["ProductCategory"])
        ] += 1
        state["channel_counts"][
            str(event["ChannelId"])
        ] += 1

        return features
