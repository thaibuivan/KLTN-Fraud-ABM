import pandas as pd

from scripts.run_ieee_feature_level_static_adaptive import run_experiments


class TinyScorer:
    def __init__(self):
        self.history = []

    def score_and_update(self, event):
        self.history.append((event["TransactionID"], event["TransactionDT"]))
        return min(0.99999, max(0., float(event["TransactionAmt"]) / 205))


def validation():
    n = 300
    return pd.DataFrame({
        "TransactionID": list(range(n)),
        "TransactionDT": [i * 3600 for i in range(n)],
        "TransactionAmt": [float(i + 1) for i in range(n)],
        "isFraud": [0] * n,
        "risk_probability": [(i + 1) / n for i in range(n)],
    })


def donor_rows():
    amounts = [10, 15, 20, 30, 35, 40, 70, 80, 90, 130, 160, 200]
    n = len(amounts)
    return pd.DataFrame({
        "TransactionID": list(range(400, 400 + n)),
        "TransactionDT": list(range(400, 400 + n)),
        "TransactionAmt": amounts,
        "ProductCD": ["W", "C"] * 6,
        "card1": list(range(300, 300 + n)),
        "addr1": [100] * n,
        "isFraud": [1] * n,
    })


def test_full_grid_is_reproducible_without_changing_fraud_attempts():
    test = donor_rows().iloc[:9].copy()
    test["TransactionID"] = list(range(500, 509))
    test["TransactionDT"] = [1_100_000 + i * 3600 for i in range(9)]
    test["isFraud"] = [0, 1, 0, 1, 0, 0, 1, 0, 0]
    params = {
        "validation_scores": validation(),
        "validation_donors": donor_rows(),
        "test_context": test,
        "scorer_factory": TinyScorer,
        "seeds": 1,
    }
    out_a = run_experiments(**params)
    out_b = run_experiments(**params)
    pd.testing.assert_frame_equal(out_a, out_b)
    assert len(out_a) == 12
    assert set(out_a["fraudster_mode"]) == {"static", "adaptive"}
    assert set(out_a["policy"]) == {"fixed", "capacity_aware"}
    assert set(out_a["capacity_ratio"]) == {0.75, 1.0, 1.25}
    assert (out_a["fraud_attempt_slots"] == 3).all()
    strategy_cols = [c for c in out_a if c.startswith("strategy_share_")]
    assert ((out_a[strategy_cols].sum(axis=1) - 1).abs() < 1e-10).all()
    assert (out_a["total_attempted_fraud_value"] > 0).all() if "total_attempted_fraud_value" in out_a else True


def test_review_feedback_observability_is_explicit():
    test = donor_rows().iloc[:6].copy()
    test["TransactionID"] = list(range(600, 606))
    test["TransactionDT"] = [1_100_000 + i * 3600 for i in range(6)]
    test["isFraud"] = [1, 1, 0, 1, 0, 1]
    out = run_experiments(
        validation(), donor_rows(), test, TinyScorer,
        seeds=1, capacity_ratios=(1.0,),
        review_feedback="no_review_observation", max_test_events=5,
    )
    assert len(out) == 4
    assert (out["fraud_attempt_slots"] == 3).all()
    assert set(out["review_feedback_assumption"]) == {"no_review_observation"}
    for q in ("0p0", "0p5", "1p0"):
        assert f"assumed_q_{q}_prevented_value" in out.columns


def test_unit_reward_ablation_runs_and_labels_assumption():
    test = donor_rows().iloc[:6].copy()
    test["TransactionID"] = list(range(800, 806))
    test["TransactionDT"] = [1_400_000 + i * 3600 for i in range(6)]
    test["isFraud"] = [1, 1, 0, 1, 0, 1]
    out = run_experiments(
        validation(), donor_rows(), test, TinyScorer,
        seeds=1, capacity_ratios=(1.0,),
        reward_amount_mode="unit",
    )
    assert len(out) == 4
    assert set(out["reward_amount_mode"]) == {"unit"}
    assert (out["fraud_attempt_slots"] == 4).all()
