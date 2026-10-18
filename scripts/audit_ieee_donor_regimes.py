"""Post-freeze IEEE fraud-donor regime diagnostic.

A regime is an observational *bundle* of amount, ProductCD, card/device and
identity context, not a controlled intervention on amount alone.

Use validation-fraud donors for descriptive regime statistics. Optional
held-out labelled test rows are used only in a post-hoc distributional audit,
NEVER to update generator pools, thresholds, or risk models.

No transaction-level outputs are written by this command.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from scripts.ieee_feature_level_fraud import IEEEFeatureLevelFraudGenerator, STRATEGIES


def summarize(validation: pd.DataFrame, test: pd.DataFrame | None = None):
    generator = IEEEFeatureLevelFraudGenerator.from_validation_raw(validation)
    registry = []
    composition = []
    for regime in STRATEGIES:
        pool = generator.pools[regime]
        amounts = pd.to_numeric(pool["TransactionAmt"], errors="coerce")
        registry.append({
            "population": "validation_fraud_donor",
            "regime": regime,
            "observations": int(len(pool)),
            "share_of_validation_frauds": float(generator.strategy_weights[regime]),
            "median_amount": float(amounts.median()),
            "p10_amount": float(amounts.quantile(0.10)),
            "p90_amount": float(amounts.quantile(0.90)),
            "identity_available_pct": (
                float(100 * pd.to_numeric(pool["identity_available"], errors="coerce").fillna(0).gt(0).mean())
                if "identity_available" in pool else None
            ),
            "unique_card1_addr1_proxies": int(pool[["card1", "addr1"]].drop_duplicates().shape[0]),
        })
        mix = pool["ProductCD"].fillna("<missing>").astype(str).value_counts(normalize=True)
        for product, fraction in mix.items():
            composition.append({
                "population": "validation_fraud_donor",
                "regime": regime,
                "ProductCD": str(product),
                "proportion_within_regime": float(fraction),
            })
    if test is not None:
        if "isFraud" not in test or "TransactionAmt" not in test or "ProductCD" not in test:
            raise ValueError("Optional test data require isFraud, TransactionAmt, ProductCD")
        fraud = test.loc[test["isFraud"].eq(1)].copy()
        fraud["regime"] = pd.cut(
            pd.to_numeric(fraud["TransactionAmt"], errors="coerce"),
            [-np.inf, generator.lower_cut, generator.upper_cut, np.inf],
            labels=STRATEGIES,
            include_lowest=True,
        )
        for regime in STRATEGIES:
            pool = fraud.loc[fraud["regime"].eq(regime)]
            mix = pool["ProductCD"].fillna("<missing>").astype(str).value_counts(normalize=True)
            for product, fraction in mix.items():
                composition.append({
                    "population": "heldout_test_fraud_diagnostic_only",
                    "regime": regime,
                    "ProductCD": str(product),
                    "proportion_within_regime": float(fraction),
                })
            registry.append({
                "population": "heldout_test_fraud_diagnostic_only",
                "regime": regime,
                "observations": int(len(pool)),
                "share_of_validation_frauds": None,
                "median_amount": float(pd.to_numeric(pool["TransactionAmt"], errors="coerce").median()) if len(pool) else None,
                "p10_amount": None, "p90_amount": None,
                "identity_available_pct": None,
                "unique_card1_addr1_proxies": int(pool[["card1", "addr1"]].drop_duplicates().shape[0]) if set(["card1", "addr1"]).issubset(pool.columns) else None,
            })
    metadata = {
        "validation_fraud_only_for_generation": True,
        "lower_validation_fraud_tercile": generator.lower_cut,
        "upper_validation_fraud_tercile": generator.upper_cut,
        "validation_fraud_median_reward_scale": generator.reward_scale,
        "regimes": list(STRATEGIES),
        "interpretation": (
            "Fraud strategies are empirical conditional context bundles, NOT "
            "identifiable causal choices of amount alone. ProductCD/device/"
            "identity distributions may differ by regime."
        ),
        "test_diagnostic_used_for_calibration": False,
    }
    return pd.DataFrame(registry), pd.DataFrame(composition), metadata


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--validation-donors", required=True)
    parser.add_argument("--test-context", default=None)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    val = pd.read_csv(args.validation_donors, low_memory=False)
    tst = pd.read_csv(args.test_context, low_memory=False) if args.test_context else None
    registry, composition, metadata = summarize(val, tst)
    dest = Path(args.output_dir)
    dest.mkdir(parents=True, exist_ok=True)
    registry.to_csv(dest / "regime_registry.csv", index=False)
    composition.to_csv(dest / "regime_product_mix.csv", index=False)
    (dest / "regime_audit_metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    print(f"IEEE-CIS donor audit: {len(registry)} rows, outputs in {dest}")
    print("Warning: changes in amount-regime preference also change the mixture of other donor features.")


if __name__ == "__main__":
    main()
