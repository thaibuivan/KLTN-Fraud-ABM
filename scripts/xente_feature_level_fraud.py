from __future__ import annotations

from dataclasses import dataclass
import random

import numpy as np
import pandas as pd


STRATEGIES = (
    "low_value",
    "medium_value",
    "high_value",
)

CONTEXT_COLUMNS = [
    "Amount",
    "Value",
    "ProductCategory",
    "ChannelId",
    "ProviderId",
    "ProductId",
    "PricingStrategy",
]


@dataclass
class XenteFeatureLevelFraudGenerator:
    """Resample raw validation fraud context by empirical value regime.

    The generator does not reuse historical risk scores. Generated events are
    rescored by the saved Xente baseline model after online past-only features
    are constructed.
    """

    pools: dict[str, pd.DataFrame]
    strategy_weights: dict[str, float]
    lower_cut: float
    upper_cut: float
    reward_scale: float

    @classmethod
    def from_validation_raw(
        cls,
        validation: pd.DataFrame,
    ):
        required = set(CONTEXT_COLUMNS) | {
            "FraudResult",
        }
        missing = required.difference(
            validation.columns
        )
        if missing:
            raise ValueError(
                f"Missing validation columns: {sorted(missing)}"
            )

        fraud = validation.loc[
            validation["FraudResult"].eq(1)
        ].copy()

        if len(fraud) < 6:
            raise ValueError(
                "Need at least 6 fraud rows"
            )

        lower_cut, upper_cut = fraud[
            "Value"
        ].quantile(
            [1.0 / 3.0, 2.0 / 3.0]
        ).tolist()

        fraud["strategy"] = pd.cut(
            fraud["Value"],
            bins=[
                -np.inf,
                lower_cut,
                upper_cut,
                np.inf,
            ],
            labels=list(STRATEGIES),
            include_lowest=True,
        ).astype(str)

        pools = {
            name: group[
                CONTEXT_COLUMNS
            ].reset_index(drop=True)
            for name, group in fraud.groupby(
                "strategy"
            )
        }

        weights = (
            fraud["strategy"]
            .value_counts(normalize=True)
            .reindex(STRATEGIES)
            .fillna(0.0)
            .to_dict()
        )

        reward_scale = float(
            fraud["Value"].median()
        )
        if reward_scale <= 0:
            reward_scale = 1.0

        return cls(
            pools=pools,
            strategy_weights=weights,
            lower_cut=float(lower_cut),
            upper_cut=float(upper_cut),
            reward_scale=reward_scale,
        )

    @property
    def strategies(self) -> tuple[str, ...]:
        return STRATEGIES

    def sample_raw(
        self,
        strategy: str,
        rng: random.Random,
        timestamp,
        attempt_index: int,
    ) -> dict:
        if strategy not in self.pools:
            raise ValueError(
                f"Unknown strategy: {strategy}"
            )

        pool = self.pools[strategy]
        row = pool.iloc[
            rng.randrange(len(pool))
        ]

        return {
            "TransactionId": (
                f"SIM_FRAUD_{attempt_index:05d}"
            ),
            "CustomerId": "SIM_FRAUDSTER",
            "TransactionStartTime": timestamp,
            "Amount": float(row["Amount"]),
            "Value": float(row["Value"]),
            "ProductCategory": row[
                "ProductCategory"
            ],
            "ChannelId": row["ChannelId"],
            "ProviderId": row["ProviderId"],
            "ProductId": row["ProductId"],
            "PricingStrategy": row[
                "PricingStrategy"
            ],
            "FraudResult": 1,
            "strategy": strategy,
        }
