"""Xente-grounded fraud template regimes for adaptive stress testing.

This module does NOT claim that real fraudsters consciously choose these named
regimes. It uses observed pre-test fraud score/value pairs as empirical templates
and groups them into value regimes so the adaptive mechanism has interpretable
scenario-specific actions.

The recommended pilot source is the chronological validation score file, so test
fraud outcomes are not used to define strategy templates.
"""

from __future__ import annotations

from dataclasses import dataclass
import random

import numpy as np
import pandas as pd


STRATEGIES = ("low_value", "medium_value", "high_value")


@dataclass
class XenteFraudTemplateGenerator:
    pools: dict[str, pd.DataFrame]
    strategy_weights: dict[str, float]
    lower_cut: float
    upper_cut: float

    @classmethod
    def from_validation_scores(
        cls,
        scores: pd.DataFrame,
    ) -> "XenteFraudTemplateGenerator":
        required = {"Value", "FraudResult", "risk_probability"}
        missing = required.difference(scores.columns)
        if missing:
            raise ValueError(
                f"Missing score columns: {sorted(missing)}"
            )

        fraud = scores.loc[
            scores["FraudResult"].eq(1),
            ["Value", "risk_probability"],
        ].copy()

        if len(fraud) < 6:
            raise ValueError(
                "Need at least 6 fraud observations to build template regimes"
            )

        lower_cut, upper_cut = fraud["Value"].quantile(
            [1 / 3, 2 / 3]
        ).tolist()

        fraud["strategy"] = pd.cut(
            fraud["Value"],
            bins=[-np.inf, lower_cut, upper_cut, np.inf],
            labels=list(STRATEGIES),
            include_lowest=True,
        ).astype(str)

        pools = {
            name: group[["Value", "risk_probability"]]
            .reset_index(drop=True)
            for name, group in fraud.groupby("strategy")
        }

        missing_pools = [
            name for name in STRATEGIES
            if name not in pools or pools[name].empty
        ]
        if missing_pools:
            raise ValueError(
                f"Empty strategy pools: {missing_pools}"
            )

        weights = (
            fraud["strategy"]
            .value_counts(normalize=True)
            .reindex(STRATEGIES)
            .fillna(0.0)
            .to_dict()
        )

        return cls(
            pools=pools,
            strategy_weights=weights,
            lower_cut=float(lower_cut),
            upper_cut=float(upper_cut),
        )

    @property
    def strategies(self) -> tuple[str, ...]:
        return STRATEGIES

    def sample(
        self,
        strategy: str,
        rng: random.Random,
    ) -> dict:
        if strategy not in self.pools:
            raise ValueError(f"Unknown strategy: {strategy}")

        pool = self.pools[strategy]
        row = pool.iloc[rng.randrange(len(pool))]
        return {
            "Value": float(row["Value"]),
            "risk_probability": float(row["risk_probability"]),
        }

    def summary(self) -> pd.DataFrame:
        rows = []
        for strategy in STRATEGIES:
            pool = self.pools[strategy]
            rows.append(
                {
                    "strategy": strategy,
                    "n": int(len(pool)),
                    "weight": float(self.strategy_weights[strategy]),
                    "median_value": float(pool["Value"].median()),
                    "median_score": float(
                        pool["risk_probability"].median()
                    ),
                }
            )
        return pd.DataFrame(rows)
