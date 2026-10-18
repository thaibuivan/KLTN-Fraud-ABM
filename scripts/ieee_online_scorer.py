"""Exact per-event IEEE baseline rescoring with past-only entity state.

Unlike score-template replay, generated fraud is passed through the frozen
IEEE-CIS preprocessing and classifier. This module uses the SAME feature
builder and model matrix construction as the empirical streaming baseline.

Important: for a fully consistent counterfactual test stream, ALL events
(including legitimate events) must be processed in chronological order with
one scorer/state for each simulation run. Before test events, warm the state
with all earlier observed events (without fitting the model on them).
"""

from __future__ import annotations

from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from scripts.train_ieee_streaming_baseline import (
    EntityHistoryState,
    build_chunk_features,
    make_entity_proxy,
    make_matrix,
)


class IEEEOnlineRiskScorer:
    def __init__(self, model_bundle: dict):
        required = {"classifier", "scaler", "encoder", "frequency_maps"}
        if not required.issubset(model_bundle):
            raise ValueError(f"Missing bundle components: {sorted(required - set(model_bundle))}")
        self.classifier = model_bundle["classifier"]
        self.scaler = model_bundle["scaler"]
        self.encoder = model_bundle["encoder"]
        self.frequency_maps = model_bundle["frequency_maps"]
        self.state = EntityHistoryState()

    @classmethod
    def from_joblib(cls, path: str | Path):
        return cls(joblib.load(path))

    @staticmethod
    def _as_part(event: dict) -> pd.DataFrame:
        """Build one raw, identity-joined event; fail if context is missing."""
        part = pd.DataFrame([event])
        required = {"card1", "addr1", "ProductCD", "TransactionAmt", "TransactionDT", "identity_available"}
        missing = required.difference(part.columns)
        if missing:
            raise ValueError(f"Missing event context: {sorted(missing)}")
        part["entity_proxy"] = make_entity_proxy(part["card1"], part["addr1"])
        return part

    def score_and_update(self, event: dict) -> float:
        """Score event, then commit its features to past-only entity history."""
        part = self._as_part(event)
        numeric, categorical = build_chunk_features(
            part, self.state, self.frequency_maps
        )
        matrix = make_matrix(numeric, categorical, self.scaler, self.encoder)
        p = float(self.classifier.predict_proba(matrix)[0, 1])
        if not np.isfinite(p) or not 0 <= p <= 1:
            raise ValueError("Risk model returned invalid probability")
        return p

    def observe_past_only(self, event: dict) -> None:
        """Warm history without predicting or updating the learned model."""
        part = self._as_part(event)
        self.state.features_then_update(
            entities=part["entity_proxy"].astype(str).to_numpy(),
            amounts=part["TransactionAmt"].to_numpy(dtype=float),
            times=part["TransactionDT"].to_numpy(dtype=np.int64),
            products=part["ProductCD"].astype(str).to_numpy(),
        )
