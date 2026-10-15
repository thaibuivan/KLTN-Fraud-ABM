import numpy as np

from scripts.train_ieee_streaming_baseline import EntityHistoryState


def test_ieee_entity_history_is_past_only():
    state = EntityHistoryState()

    (
        prior_count,
        prior_mean,
        prior_std,
        gap,
        product_share,
    ) = state.features_then_update(
        entities=["A", "A", "A"],
        amounts=np.array([10.0, 20.0, 30.0]),
        times=np.array([100, 160, 220]),
        products=np.array(["W", "W", "C"]),
    )

    assert prior_count.tolist() == [0.0, 1.0, 2.0]
    assert np.isnan(prior_mean[0])
    assert prior_mean[1] == 10.0
    assert prior_mean[2] == 15.0
    assert np.isnan(gap[0])
    assert gap[1] == 60.0
    assert gap[2] == 60.0
    assert product_share[0] == 0.0
    assert product_share[1] == 1.0
    assert product_share[2] == 0.0
