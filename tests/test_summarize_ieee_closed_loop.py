import math

import pandas as pd
import pytest

from scripts.summarize_ieee_closed_loop import METRICS, summarize_runs


def runs():
    rows = []
    for seed in range(5):
        for mode in ("static", "adaptive"):
            for policy in ("fixed", "capacity_aware"):
                for capacity in (0.75, 1.0, 1.25):
                    value = (
                        0.1 * seed + (1 if mode == "adaptive" else 0)
                        + (2 if policy == "capacity_aware" else 0)
                        + capacity
                    )
                    row = {
                        "seed": seed, "capacity_ratio": capacity,
                        "fraudster_mode": mode, "policy": policy,
                    }
                    row.update({metric: value for metric in METRICS})
                    rows.append(row)
    return pd.DataFrame(rows)


def test_seed_matched_contrasts_and_t_intervals():
    a, policy, adaptation = summarize_runs(runs())
    assert len(a) == 12 * len(METRICS)
    assert len(policy) == 6 * len(METRICS)
    assert len(adaptation) == 6 * len(METRICS)
    assert (policy["n"] == 5).all()
    assert (adaptation["n"] == 5).all()
    assert all(math.isclose(v, 2.0) for v in policy["mean"])
    assert all(math.isclose(v, 1.0) for v in adaptation["mean"])
    assert (a["ci95_low"] <= a["mean"]).all()
    assert (a["ci95_high"] >= a["mean"]).all()


def test_reject_duplicate_cell():
    d = runs()
    with pytest.raises(ValueError, match="Duplicate"):
        summarize_runs(pd.concat([d, d.iloc[[0]]]))
