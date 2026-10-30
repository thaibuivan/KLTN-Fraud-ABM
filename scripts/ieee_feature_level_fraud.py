"""Validation-grounded IEEE-CIS fraud events for an adaptive-policy pilot.

Only three observable *amount regimes* are offered as strategy actions.
Masked C/D/M/V columns and identity fields are copied together from one
validation donor transaction and are NOT interpreted as controllable actions.
This is a bounded synthetic scenario, not evidence of fraudster cognition.
"""

from __future__ import annotations

from dataclasses import dataclass
import random

import numpy as np
import pandas as pd

STRATEGIES = ("low_amount", "middle_amount", "high_amount")
REQUIRED = {
    "TransactionID", "TransactionDT", "TransactionAmt", "ProductCD",
    "card1", "addr1", "isFraud",
}


@dataclass
class IEEEFeatureLevelFraudGenerator:
    pools: dict[str, pd.DataFrame]
    strategy_weights: dict[str, float]
    lower_cut: float
    upper_cut: float
    reward_scale: float

    @classmethod
    def from_validation_raw(cls, validation: pd.DataFrame):
        """Fit donor pools on validation fraud ONLY, never on test outcomes."""
        missing = REQUIRED.difference(validation.columns)
        if missing:
            raise ValueError(f"Missing IEEE columns: {sorted(missing)}")
        fraud = validation.loc[validation["isFraud"].eq(1)].copy()
        amounts = pd.to_numeric(fraud["TransactionAmt"], errors="coerce")
        fraud = fraud.loc[amounts.notna() & amounts.ge(0)].copy()
        if len(fraud) < 9:
            raise ValueError("At least nine validation fraud donors are required")
        lower, upper = fraud["TransactionAmt"].quantile([1 / 3, 2 / 3])
        if not np.isfinite(lower) or not np.isfinite(upper) or lower >= upper:
            raise ValueError("Fraud amount terciles are degenerate; revise regimes")
        fraud["strategy"] = pd.cut(
            fraud["TransactionAmt"],
            bins=[-np.inf, lower, upper, np.inf],
            labels=list(STRATEGIES),
            include_lowest=True,
        ).astype(str)
        pools = {
            name: fraud.loc[fraud["strategy"].eq(name)].drop(
                columns="strategy"
            ).reset_index(drop=True)
            for name in STRATEGIES
        }
        if any(pool.empty for pool in pools.values()):
            raise ValueError("Every fraud amount regime needs validation support")
        shares = fraud["strategy"].value_counts(normalize=True)
        reward_scale = float(fraud["TransactionAmt"].median())
        return cls(
            pools=pools,
            strategy_weights={name: float(shares.get(name, 0.0)) for name in STRATEGIES},
            lower_cut=float(lower),
            upper_cut=float(upper),
            reward_scale=reward_scale if reward_scale > 0 else 1.0,
        )

    @property
    def strategies(self) -> tuple[str, ...]:
        return STRATEGIES

    def sample_raw(
        self,
        strategy: str,
        rng: random.Random,
        timestamp_seconds: int,
        attempt_index: int,
    ) -> dict:
        """Resample a coherent donor row; only ID and relative time change.

        The donor's card/device/identity and masked detector context are kept
        together. Negative synthetic IDs avoid collisions with Kaggle IDs.
        """
        if strategy not in self.pools:
            raise ValueError(f"Unknown strategy: {strategy}")
        if attempt_index < 0 or int(timestamp_seconds) < 0:
            raise ValueError("Attempt index and relative time must be non-negative")
        pool = self.pools[strategy]
        row = pool.iloc[rng.randrange(len(pool))].to_dict()
        row.update({
            "TransactionID": -1 - int(attempt_index),
            "TransactionDT": int(timestamp_seconds),
            "isFraud": 1,
            "strategy": strategy,
        })
        return row
