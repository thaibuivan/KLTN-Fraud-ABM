"""Aggregate IEEE closed-loop runs and calculate seed-matched contrasts.

No assumption of policy universality: effect direction can vary by
capacity, behavior, score quality and model assumptions. Do not report a
single-run CI, and never compare Xente vs IEEE in raw monetary units.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import t as student_t


METRICS = (
    "fraud_intercept_rate", "fraud_exposure_at_horizon", "backlog_end",
    "legitimate_intervention_rate", "mean_wait_minutes",
    "assumed_q_0p5_exposure_value", "strategy_share_low_amount",
)
KEY = ("seed", "capacity_ratio")


def confidence_stats(values: pd.Series) -> dict:
    values = pd.to_numeric(values, errors="coerce").dropna().astype(float)
    n = len(values)
    if n == 0:
        return {"n": 0, "mean": np.nan, "sd": np.nan,
                "mcse": np.nan, "ci95_low": np.nan, "ci95_high": np.nan}
    mean = float(values.mean())
    if n == 1:
        return {"n": n, "mean": mean, "sd": np.nan,
                "mcse": np.nan, "ci95_low": np.nan, "ci95_high": np.nan}
    sd = float(values.std(ddof=1))
    se = sd / np.sqrt(n)
    cutoff = float(student_t.ppf(0.975, df=n-1))
    return {"n": n, "mean": mean, "sd": sd, "mcse": se,
            "ci95_low": mean-cutoff*se, "ci95_high": mean+cutoff*se}


def summarize_runs(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    required = {"seed", "capacity_ratio", "policy", "fraudster_mode", *METRICS}
    absent = required.difference(df.columns)
    if absent:
        raise ValueError(f"Missing run columns: {sorted(absent)}")
    identity = ["seed", "capacity_ratio", "fraudster_mode", "policy"]
    if df.duplicated(identity).any():
        raise ValueError("Duplicate seed/capacity/mode/policy cells")
    full_rows = []
    for (mode, policy, capacity), cell in df.groupby(
        ["fraudster_mode", "policy", "capacity_ratio"], sort=True
    ):
        for metric in METRICS:
            full_rows.append({
                "fraudster_mode": mode, "policy": policy,
                "capacity_ratio": capacity, "metric": metric,
                **confidence_stats(cell[metric]),
            })
    main = pd.DataFrame(full_rows)
    policy = _contrasts(
        df, treatment="capacity_aware", control="fixed",
        comparison_field="policy",
        within_fields=("fraudster_mode", "capacity_ratio"),
    )
    adaptive = _contrasts(
        df, treatment="adaptive", control="static",
        comparison_field="fraudster_mode",
        within_fields=("policy", "capacity_ratio"),
    )
    return main, policy, adaptive


def _contrasts(df, *, treatment, control, comparison_field, within_fields):
    diffs = []
    for keys, sub in df.groupby(list(within_fields), sort=True):
        if not isinstance(keys, tuple):
            keys = (keys,)
        a = sub.loc[sub[comparison_field].eq(treatment)]
        b = sub.loc[sub[comparison_field].eq(control)]
        joined = a.merge(
            b, on=["seed", *within_fields],
            how="inner", suffixes=("_treatment", "_control"),
            validate="one_to_one"
        )
        for metric in METRICS:
            v = joined[f"{metric}_treatment"] - joined[f"{metric}_control"]
            diffs.append({
                **dict(zip(within_fields, keys)),
                "comparison": f"{treatment} - {control}",
                "metric": metric,
                "paired_by_seed": True,
                **confidence_stats(v),
            })
    return pd.DataFrame(diffs)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--runs", required=True)
    p.add_argument("--output-dir", required=True)
    args = p.parse_args()
    data = pd.read_csv(args.runs)
    tables = summarize_runs(data)
    folder = Path(args.output_dir)
    folder.mkdir(parents=True, exist_ok=True)
    for name, frame in zip(
        ("cells.csv", "policy_contrasts.csv", "adaptation_contrasts.csv"),
        tables
    ):
        frame.to_csv(folder / name, index=False)
    print("Wrote cell summaries and paired seed contrasts to", folder)


if __name__ == "__main__":
    main()
