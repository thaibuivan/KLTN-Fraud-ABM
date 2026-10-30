import pandas as pd

from scripts.audit_ieee_donor_regimes import summarize


def data():
    return pd.DataFrame({
        "TransactionID": range(12),
        "TransactionDT": range(12),
        "TransactionAmt": [10, 12, 14, 19, 22, 28, 55, 65, 85, 140, 160, 200],
        "ProductCD": ["C"] * 4 + ["W"] * 8,
        "card1": list(range(12)),
        "addr1": [1] * 12,
        "identity_available": [1]*6 + [0]*6,
        "isFraud": [1]*12,
    })


def test_donor_diagnostics_do_not_change_generator():
    validation = data()
    original = validation.copy(deep=True)
    registry, products, meta = summarize(validation)
    pd.testing.assert_frame_equal(validation, original)
    assert registry.loc[registry.population.eq("validation_fraud_donor"), "observations"].sum() == 12
    sums = products.groupby(["population", "regime"])["proportion_within_regime"].sum()
    assert (sums - 1.0).abs().max() < 1e-12
    assert not registry["identity_available_pct"].isna().any()
    assert meta["test_diagnostic_used_for_calibration"] is False


def test_test_context_held_out_diagnostic_only():
    d = data()
    test = d.copy(deep=True)
    test["TransactionAmt"] += 1000
    a, p, m = summarize(d, test)
    assert a.loc[a.population.eq("heldout_test_fraud_diagnostic_only"), "observations"].sum() == 12
    assert m["validation_fraud_median_reward_scale"] == float(d.TransactionAmt.median())
    assert m["upper_validation_fraud_tercile"] < 1000
    assert set(p.population) == {"validation_fraud_donor", "heldout_test_fraud_diagnostic_only"}
