import numpy as np
import pandas as pd
from numpy.testing import assert_allclose
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

from scripts.ieee_online_scorer import IEEEOnlineRiskScorer
from scripts.train_ieee_streaming_baseline import (
    EntityHistoryState, NUMERIC_FEATURES, FREQUENCY_COLUMNS,
    LOW_CARD_CATEGORICAL, build_chunk_features, make_entity_proxy,
    make_encoder, make_matrix,
)
from scripts.build_ieee_features import (
    C_COLUMNS, D_COLUMNS, M_COLUMNS, SELECTED_V, IDENTITY_NUMERIC,
    IDENTITY_CATEGORICAL,
)


def synthetic_events():
    n = 16
    events = []
    for i in range(n):
        all_ctx = (
            C_COLUMNS + D_COLUMNS + M_COLUMNS + SELECTED_V
            + IDENTITY_NUMERIC + IDENTITY_CATEGORICAL + LOW_CARD_CATEGORICAL
        )
        event = {x: 0.0 for x in all_ctx}
        event.update({
            "TransactionID": i+1,
            "TransactionDT": 100 + i * 37,
            "TransactionAmt": float((i+1) * 14),
            "ProductCD": "W" if i % 3 == 0 else "C",
            "card1": 100 if i % 2 == 0 else 200,
            "addr1": 55.0,
            "dist1": 1.0,
            "P_emaildomain": "example.com",
            "R_emaildomain": "example.com" if i % 3 else "other.com",
            "identity_available": 1,
            "DeviceType": "mobile" if i % 2 else "desktop",
            "DeviceInfo": "test-device",
            "id_31": "browser",
            "id_33": "screen",
        })
        events.append(event)
    return events


def fitted_synthetic_bundle(events):
    part = pd.DataFrame(events)
    part["entity_proxy"] = make_entity_proxy(part["card1"], part["addr1"])
    maps = {}
    for col in FREQUENCY_COLUMNS:
        counts = part[col].astype("string").fillna("__MISSING__").value_counts(normalize=True)
        maps[col] = counts.to_dict()
    state = EntityHistoryState()
    numeric, categorical = build_chunk_features(part, state, maps)
    scaler = StandardScaler().fit(numeric.to_numpy(dtype=float))
    categories = [
        sorted(set(categorical[col].astype(str)) | {"__MISSING__"})
        for col in LOW_CARD_CATEGORICAL
    ]
    encoder = make_encoder(categories)
    matrix = make_matrix(numeric, categorical, scaler, encoder)
    labels = np.array([0, 1] * (len(events)//2))
    classifier = LogisticRegression(max_iter=1000).fit(matrix, labels)
    bundle = {
        "classifier": classifier,
        "scaler": scaler,
        "encoder": encoder,
        "frequency_maps": maps,
    }
    return bundle, classifier.predict_proba(matrix)[:, 1]


def test_online_exact_equals_offline_full_context():
    events = synthetic_events()
    bundle, expected = fitted_synthetic_bundle(events)
    scorer = IEEEOnlineRiskScorer(bundle)
    actual = [scorer.score_and_update(e) for e in events]
    assert_allclose(actual, expected, atol=1e-10, rtol=1e-10)


def test_chunked_warmup_equal_to_single_event_warmup():
    events = synthetic_events()
    bundle, _ = fitted_synthetic_bundle(events)
    single = IEEEOnlineRiskScorer(bundle)
    batch = IEEEOnlineRiskScorer(bundle)
    for e in events[:11]:
        single.observe_past_only(e)
    batch.warm_history(pd.DataFrame(events[:11]), chunksize=3)
    assert_allclose(
        [single.score_and_update(events[11])],
        [batch.score_and_update(events[11])],
        atol=1e-10, rtol=1e-10,
    )
