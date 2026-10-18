"""Check exact IEEE online scoring against the frozen empirical baseline.

Run BEFORE adaptive fraud simulations. On an unchanged chronological test stream,
model scores should agree with the saved baseline within the chosen tolerance.
This checks counterfactual streaming feature construction without test-label use.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from scripts.ieee_online_scorer import IEEEOnlineRiskScorer


def audit_equivalence(
    baseline_scores: pd.DataFrame,
    test_context: pd.DataFrame,
    scorer,
    *,
    n_events: int = 200,
    tolerance: float = 1e-6,
) -> dict:
    if n_events < 1 or tolerance < 0:
        raise ValueError("n_events must be positive, tolerance nonnegative")
    for frame, fields in (
        (baseline_scores, {"TransactionID", "risk_probability"}),
        (test_context, {"TransactionID", "TransactionDT"}),
    ):
        missing = fields.difference(frame.columns)
        if missing:
            raise ValueError(f"Missing audit fields: {sorted(missing)}")
    observed = baseline_scores.loc[:, ["TransactionID", "risk_probability"]].copy()
    observed = observed.set_index("TransactionID")
    context = test_context.head(n_events)
    if context["TransactionID"].duplicated().any():
        raise ValueError("Duplicate test TransactionIDs")
    if not pd.to_numeric(context["TransactionDT"]).is_monotonic_increasing:
        raise ValueError("Test context not chronological")
    missing = set(context["TransactionID"]).difference(observed.index)
    if missing:
        raise ValueError(f"Missing frozen reference risk scores: {len(missing)}")
    online = np.array([
        scorer.score_and_update(row)
        for row in context.to_dict(orient="records")
    ], dtype=float)
    target = observed.loc[context["TransactionID"], "risk_probability"].to_numpy(dtype=float)
    delta = np.abs(online - target)
    max_delta = float(np.max(delta))
    return {
        "n_events": int(len(context)),
        "max_abs_difference": max_delta,
        "mean_abs_difference": float(np.mean(delta)),
        "tolerance": float(tolerance),
        "pass": bool(max_delta <= tolerance),
        "first_mismatch": int(np.argmax(delta)),
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--test-scores", required=True)
    p.add_argument("--test-context", required=True)
    p.add_argument("--history-context", required=True)
    p.add_argument("--model-bundle", required=True)
    p.add_argument("--n-events", type=int, default=200)
    p.add_argument("--tolerance", type=float, default=1e-6)
    p.add_argument("--output", required=True)
    a = p.parse_args()
    scorer = IEEEOnlineRiskScorer.from_joblib(a.model_bundle)
    scorer.warm_history(pd.read_csv(a.history_context))
    result = audit_equivalence(
        pd.read_csv(a.test_scores),
        pd.read_csv(a.test_context, low_memory=False),
        scorer, n_events=a.n_events, tolerance=a.tolerance,
    )
    out = Path(a.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    if not result["pass"]:
        raise SystemExit("IEEE online scorer mismatch: investigate before adaptive runs")


if __name__ == "__main__":
    main()
