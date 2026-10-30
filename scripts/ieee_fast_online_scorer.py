"""Accelerated IEEE streaming scorer for repeated ABM simulations.

Algebraically matches the frozen SGD log-loss scorer's StandardScaler,
sparse OneHotEncoder and existing past-only entity features. This fast path
MUST pass test equivalence and real held-out online-vs-offline audit before
being used for the full IEEE simulation grid.

This module changes computational implementation only, NOT the fitted model.
"""

from __future__ import annotations

import math

import numpy as np
import pandas as pd

from scripts.ieee_online_scorer import IEEEOnlineRiskScorer
from scripts.train_ieee_streaming_baseline import (
    NUMERIC_FEATURES, LOW_CARD_CATEGORICAL, FREQUENCY_COLUMNS,
    C_COLUMNS, D_COLUMNS, M_COLUMNS, SELECTED_V,
    IDENTITY_NUMERIC, IDENTITY_CATEGORICAL,
)


def is_missing(value) -> bool:
    return value is None or bool(pd.isna(value))


def numeric(value) -> float:
    if is_missing(value):
        return float("nan")
    return float(value)


def categorical_key(value) -> str:
    return "__MISSING__" if is_missing(value) else str(value)


def integer_key(value, missing_marker: str) -> str:
    if is_missing(value):
        return missing_marker
    return str(int(np.round(float(value))))


class FastIEEEOnlineRiskScorer(IEEEOnlineRiskScorer):
    """Fast scalar scoring with exact original feature definitions."""

    def __init__(self, bundle: dict):
        super().__init__(bundle)
        coef = np.asarray(self.classifier.coef_, dtype=float)
        if coef.ndim != 2 or coef.shape[0] != 1:
            raise ValueError("Expected binary linear IEEE classifier")
        self.intercept = float(self.classifier.intercept_[0])
        self.numeric_coef = coef[0, :len(NUMERIC_FEATURES)]
        self.means = np.asarray(self.scaler.mean_, dtype=float)
        self.scales = np.asarray(self.scaler.scale_, dtype=float)
        if len(self.means) != len(NUMERIC_FEATURES):
            raise ValueError("Fitted scaler feature count mismatch")
        offset = len(NUMERIC_FEATURES)
        self.categorical_coef = {}
        for name, choices in zip(LOW_CARD_CATEGORICAL, self.encoder.categories_):
            end = offset + len(choices)
            self.categorical_coef[name] = {
                str(category): float(weight)
                for category, weight in zip(choices, coef[0, offset:end])
            }
            offset = end
        if offset != coef.shape[1]:
            raise ValueError("Fitted classifier/encoder columns are incompatible")
        self.required_context = set(
            C_COLUMNS + D_COLUMNS + M_COLUMNS + SELECTED_V
            + IDENTITY_NUMERIC + IDENTITY_CATEGORICAL
            + LOW_CARD_CATEGORICAL
            + ["ProductCD", "TransactionAmt", "TransactionDT",
               "card1", "addr1", "dist1", "P_emaildomain",
               "R_emaildomain", "identity_available"]
        )

    def score_and_update(self, event: dict) -> float:
        missing_cols = self.required_context.difference(event)
        if missing_cols:
            raise ValueError(f"Missing IEEE event context: {sorted(missing_cols)}")

        t = int(event["TransactionDT"])
        amount = numeric(event["TransactionAmt"])
        if not math.isfinite(amount) or amount < 0:
            raise ValueError("IEEE TransactionAmt must be finite and nonnegative")
        entity = (
            integer_key(event["card1"], "__MISSING_CARD1__") + "|"
            + integer_key(event["addr1"], "__MISSING_ADDR1__")
        )
        product = categorical_key(event["ProductCD"])
        state = self.state
        count = state.count[entity]
        prior_mean = float("nan")
        prior_std = float("nan")
        gap = float("nan")
        share = 0.0
        ratio = float("nan")
        if count:
            mean64 = state.sum_amount[entity] / count
            variance = max(state.sumsq_amount[entity] / count - mean64 * mean64, 0.0)
            prior_mean = float(np.float32(mean64))
            prior_std = float(np.float32(math.sqrt(variance)))
            share = state.product_count[entity].get(product, 0) / count
            if entity in state.last_time:
                gap = float(np.float32(t - state.last_time[entity]))
            if prior_mean != 0 and math.isfinite(prior_mean):
                ratio = min(amount / prior_mean, 20.0)
        email_p, email_r = event["P_emaildomain"], event["R_emaildomain"]
        e_missing = is_missing(email_p) and is_missing(email_r)
        e_match = (
            not is_missing(email_p) and not is_missing(email_r)
            and str(email_p) == str(email_r)
        )
        vals = {
            "log_transaction_amt": math.log1p(amount),
            "day_index": float(t // 86400),
            "hour_proxy": (t % 86400) / 3600.0,
            "addr1": numeric(event["addr1"]),
            "dist1": numeric(event["dist1"]),
            "identity_available": numeric(event["identity_available"]),
            "identity_missing_count": float(sum(
                is_missing(event[col])
                for col in IDENTITY_NUMERIC + IDENTITY_CATEGORICAL
            )),
            "detector_missing_count": float(sum(
                is_missing(event[col])
                for col in C_COLUMNS + D_COLUMNS + M_COLUMNS + SELECTED_V
            )),
            "email_both_missing": float(e_missing),
            "email_match": float(e_match),
            "log_prior_tx_count": math.log1p(float(np.float32(count))),
            "log_prior_amount_mean": math.log1p(max(prior_mean, 0)) if math.isfinite(prior_mean) else float("nan"),
            "log_prior_amount_std": math.log1p(max(prior_std, 0)) if math.isfinite(prior_std) else float("nan"),
            "log_gap_seconds": math.log1p(max(gap, 0)) if math.isfinite(gap) else float("nan"),
            "amount_ratio_clip": ratio,
            "prior_product_share": share,
            "cold_start_entity": float(count == 0),
        }
        for column in C_COLUMNS + D_COLUMNS + SELECTED_V + IDENTITY_NUMERIC:
            vals[column] = numeric(event[column])
        for col in FREQUENCY_COLUMNS:
            value = entity if col == "entity_proxy" else event[col]
            vals["freq_" + col] = self.frequency_maps[col].get(categorical_key(value), 0.0)

        numeric_vector = np.array([vals[k] for k in NUMERIC_FEATURES], dtype=float)
        with np.errstate(divide="ignore", invalid="ignore"):
            standardized = (numeric_vector - self.means) / self.scales
        standardized = np.nan_to_num(standardized, nan=0.0, posinf=0.0, neginf=0.0).astype(np.float32)
        logit = self.intercept + float(np.dot(standardized, self.numeric_coef))
        for col in LOW_CARD_CATEGORICAL:
            logit += self.categorical_coef[col].get(categorical_key(event[col]), 0.0)
        if logit >= 0:
            z = math.exp(-logit)
            prob = 1.0 / (1.0 + z)
        else:
            z = math.exp(logit)
            prob = z / (1.0 + z)
        # Never consume future information. The current transaction is only
        # added to history AFTER its own features have been evaluated.
        state.count[entity] = count + 1
        state.sum_amount[entity] += amount
        state.sumsq_amount[entity] += amount * amount
        state.last_time[entity] = t
        state.product_count[entity][product] += 1
        return prob
