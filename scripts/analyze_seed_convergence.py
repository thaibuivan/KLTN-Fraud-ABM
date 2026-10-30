"""Summarize Monte Carlo convergence for core simulation runs.

Expected input contains one row per seed/configuration. The default grouping
matches the Xente feature-level runner but can be overridden by editing the
columns in a future scenario-specific wrapper.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


DEFAULT_METRICS = [
    "fraud_intercept_rate",
    "fraud_exposure_at_horizon",
    "backlog_end",
    "legitimate_intervention_rate",
]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--runs", required=True)
    p.add_argument(
        "--output",
        default="outputs/local/seed_convergence.csv",
    )
    p.add_argument(
        "--checkpoints",
        default="10,20,30",
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()
    runs = pd.read_csv(args.runs)

    mode_col = (
        "fraudster_mode"
        if "fraudster_mode" in runs.columns
        else "mode"
    )
    required = {
        mode_col,
        "policy",
        "seed",
    }
    capacity_col = (
        "capacity_ratio"
        if "capacity_ratio" in runs.columns
        else "capacity"
    )
    required.add(capacity_col)
    required.update(DEFAULT_METRICS)

    missing = required.difference(runs.columns)
    if missing:
        raise ValueError(
            f"Missing run columns: {sorted(missing)}"
        )

    checkpoints = [
        int(x)
        for x in args.checkpoints.split(",")
        if x.strip()
    ]

    rows = []
    group_cols = [
        mode_col,
        "policy",
        capacity_col,
    ]

    for key, group in runs.groupby(group_cols):
        group = group.sort_values("seed")
        row = dict(zip(group_cols, key))
        row["n_seeds"] = int(len(group))

        for metric in DEFAULT_METRICS:
            values = group[metric].astype(float)
            mean = float(values.mean())
            sd = float(values.std(ddof=1)) if len(values) > 1 else 0.0
            mcse = (
                sd / np.sqrt(len(values))
                if len(values)
                else np.nan
            )

            row[f"{metric}_mean"] = mean
            row[f"{metric}_sd"] = sd
            row[f"{metric}_mcse"] = mcse
            row[f"{metric}_relative_mcse"] = (
                abs(mcse / mean)
                if mean != 0
                else np.nan
            )

            for n in checkpoints:
                if len(values) >= n:
                    row[f"{metric}_mean_{n}"] = float(
                        values.iloc[:n].mean()
                    )

        rows.append(row)

    out = pd.DataFrame(rows)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(output, index=False)
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()
