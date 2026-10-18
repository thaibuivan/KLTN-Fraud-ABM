import numpy as np
import pytest
from scipy import sparse

from scripts.ieee_online_scorer import IEEEOnlineRiskScorer
from scripts.train_ieee_streaming_baseline import (
    NUMERIC_FEATURES, FREQUENCY_COLUMNS, C_COLUMNS, D_COLUMNS,
    M_COLUMNS, SELECTED_V, IDENTITY_NUMERIC, IDENTITY_CATEGORICAL,
    LOW_CARD_CATEGORICAL,
)


class IdentityScaler:
    def transform(self, array):
        return array


class EmptyEncoder:
    def transform(self, df):
        return sparse.csr_matrix((len(df), 0))


class CountBasedClassifier:
    def predict_proba(self, matrix):
        prior_count_idx = NUMERIC_FEATURES.index("log_prior_tx_count")
        n = matrix.toarray()[:, prior_count_idx]
        p = np.where(n > 0, 0.75, 0.25)
        return np.column_stack([1-p, p])


def model_bundle():
    return {
        "classifier": CountBasedClassifier(),
        "scaler": IdentityScaler(),
        "encoder": EmptyEncoder(),
        "frequency_maps": {c: {} for c in FREQUENCY_COLUMNS},
    }


def raw_event(identifier=1, time=100):
    cols = (
        C_COLUMNS + D_COLUMNS + M_COLUMNS + SELECTED_V
        + IDENTITY_NUMERIC + IDENTITY_CATEGORICAL + LOW_CARD_CATEGORICAL
    )
    event = {col: np.nan for col in cols}
    event.update({
        "TransactionID": identifier, "TransactionDT": time,
        "TransactionAmt": 30.0, "ProductCD": "W", "card1": 1122,
        "addr1": 87.0, "dist1": np.nan,
        "P_emaildomain": "example.com", "R_emaildomain": "example.com",
        "DeviceInfo": "mobile", "id_31": "browser", "id_33": "screen",
        "identity_available": 1,
    })
    return event


def test_scores_depend_on_past_only_state():
    s = IEEEOnlineRiskScorer(model_bundle())
    assert s.score_and_update(raw_event(1, 100)) == 0.25
    assert s.score_and_update(raw_event(2, 200)) == 0.75
    other = raw_event(3, 300)
    other["card1"] = 9999
    assert s.score_and_update(other) == 0.25


def test_warmup_does_not_predict_or_fit():
    s = IEEEOnlineRiskScorer(model_bundle())
    s.observe_past_only(raw_event(1, 100))
    assert s.score_and_update(raw_event(2, 200)) == 0.75


def test_incomplete_event_fails_closed():
    s = IEEEOnlineRiskScorer(model_bundle())
    with pytest.raises(ValueError, match="Missing event context"):
        s.score_and_update({"TransactionAmt": 100.0})
