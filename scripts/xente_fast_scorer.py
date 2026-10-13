"""Fast exact scorer for the fitted Xente logistic baseline.

The final adaptive simulation needs thousands of sequential single-event scores.
Calling the full sklearn preprocessing pipeline for every generated fraud event is
correct but unnecessarily slow. This class extracts the fitted imputer/scaler,
one-hot categories and logistic coefficients once, then evaluates the same linear
predictor directly.

It is not a new model. Unit tests must verify numerical equivalence to
Pipeline.predict_proba before it is used in final experiments.
"""

from __future__ import annotations

import math

import numpy as np

from scripts.train_xente_baseline import (
    CATEGORICAL_FEATURES,
    NUMERIC_FEATURES,
)


class FastXenteLogisticScorer:
    def __init__(self, fitted_pipeline) -> None:
        preprocessor = fitted_pipeline.named_steps[
            "preprocessor"
        ]
        classifier = fitted_pipeline.named_steps[
            "classifier"
        ]

        if classifier.coef_.shape[0] != 1:
            raise ValueError(
                "Expected a binary logistic classifier"
            )

        numeric_pipeline = (
            preprocessor.named_transformers_[
                "numeric"
            ]
        )
        imputer = numeric_pipeline.named_steps[
            "imputer"
        ]
        scaler = numeric_pipeline.named_steps[
            "scaler"
        ]
        encoder = preprocessor.named_transformers_[
            "categorical"
        ]

        self.intercept = float(
            classifier.intercept_[0]
        )
        coef = classifier.coef_[0]

        numeric_slice = (
            preprocessor.output_indices_[
                "numeric"
            ]
        )
        categorical_slice = (
            preprocessor.output_indices_[
                "categorical"
            ]
        )

        self.numeric_coef = np.asarray(
            coef[numeric_slice],
            dtype=float,
        )
        self.numeric_impute = np.asarray(
            imputer.statistics_,
            dtype=float,
        )
        self.numeric_mean = np.asarray(
            scaler.mean_,
            dtype=float,
        )
        self.numeric_scale = np.asarray(
            scaler.scale_,
            dtype=float,
        )

        categorical_coef = np.asarray(
            coef[categorical_slice],
            dtype=float,
        )
        self.category_coef: dict[
            str, dict[object, float]
        ] = {}

        offset = 0
        for feature_name, categories in zip(
            CATEGORICAL_FEATURES,
            encoder.categories_,
        ):
            width = len(categories)
            weights = categorical_coef[
                offset : offset + width
            ]
            self.category_coef[
                feature_name
            ] = {
                category: float(weight)
                for category, weight in zip(
                    categories,
                    weights,
                )
            }
            offset += width

        if offset != len(categorical_coef):
            raise ValueError(
                "Categorical coefficient layout mismatch"
            )

    @staticmethod
    def _is_missing(value) -> bool:
        try:
            return bool(np.isnan(value))
        except (TypeError, ValueError):
            return value is None

    def decision_function_one(
        self,
        features: dict,
    ) -> float:
        raw_numeric = []
        for i, name in enumerate(
            NUMERIC_FEATURES
        ):
            value = features.get(name)
            if self._is_missing(value):
                value = self.numeric_impute[i]
            raw_numeric.append(float(value))

        numeric = np.asarray(
            raw_numeric,
            dtype=float,
        )
        standardized = (
            numeric - self.numeric_mean
        ) / self.numeric_scale

        logit = (
            self.intercept
            + float(
                np.dot(
                    standardized,
                    self.numeric_coef,
                )
            )
        )

        for name in CATEGORICAL_FEATURES:
            value = features.get(name)
            logit += self.category_coef[
                name
            ].get(value, 0.0)

        return float(logit)

    def predict_proba_one(
        self,
        features: dict,
    ) -> float:
        logit = self.decision_function_one(
            features
        )

        if logit >= 0:
            z = math.exp(-logit)
            return 1.0 / (1.0 + z)

        z = math.exp(logit)
        return z / (1.0 + z)
