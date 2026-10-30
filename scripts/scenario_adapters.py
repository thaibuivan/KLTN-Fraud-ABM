"""Scenario adapters for the shared fraud-policy simulation engine.

The shared simulator currently consumes the following canonical columns:

- TransactionId
- TransactionStartTime
- Value
- FraudResult
- risk_probability

Xente already maps naturally to this schema. IEEE-CIS uses TransactionID,
TransactionDT, TransactionAmt and isFraud, so it is normalized here without
pretending that TransactionDT is a calendar timestamp.

These adapters are research plumbing, not behavioral assumptions.
"""

from __future__ import annotations

import pandas as pd


CANONICAL_COLUMNS = [
    "TransactionId",
    "TransactionStartTime",
    "Value",
    "FraudResult",
    "risk_probability",
]


def _validate_probability(df: pd.DataFrame) -> None:
    if not df["risk_probability"].between(0.0, 1.0).all():
        raise ValueError("risk_probability must be in [0, 1]")


def normalize_xente_scores(df: pd.DataFrame) -> pd.DataFrame:
    required = {
        "TransactionId",
        "TransactionStartTime",
        "Value",
        "FraudResult",
        "risk_probability",
    }
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(
            f"Missing Xente score columns: {sorted(missing)}"
        )

    out = df.copy()
    out["TransactionStartTime"] = pd.to_datetime(
        out["TransactionStartTime"],
        utc=True,
    )
    out["Value"] = out["Value"].astype(float)
    out["FraudResult"] = out["FraudResult"].astype(int)
    out["risk_probability"] = out["risk_probability"].astype(float)
    _validate_probability(out)

    if (out["Value"] < 0).any():
        raise ValueError("Xente Value must be non-negative")

    return out


def normalize_ieee_scores(
    df: pd.DataFrame,
    *,
    relative_time_origin: str = "1970-01-01T00:00:00Z",
) -> pd.DataFrame:
    """Map IEEE-CIS scored events to the canonical simulation schema.

    TransactionDT is interpreted only as a relative number of seconds from an
    arbitrary origin. The resulting Timestamp preserves order and intervals but
    MUST NOT be interpreted as a real calendar date/time.
    """
    required = {
        "TransactionID",
        "TransactionDT",
        "TransactionAmt",
        "isFraud",
        "risk_probability",
    }
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(
            f"Missing IEEE-CIS score columns: {sorted(missing)}"
        )

    out = df.copy()
    origin = pd.Timestamp(relative_time_origin)

    transaction_dt = pd.to_numeric(
        out["TransactionDT"],
        errors="raise",
    )
    out["TransactionStartTime"] = (
        origin + pd.to_timedelta(transaction_dt, unit="s")
    )
    out["TransactionId"] = out["TransactionID"]
    out["Value"] = pd.to_numeric(
        out["TransactionAmt"],
        errors="raise",
    ).astype(float)
    out["FraudResult"] = pd.to_numeric(
        out["isFraud"],
        errors="raise",
    ).astype(int)
    out["risk_probability"] = pd.to_numeric(
        out["risk_probability"],
        errors="raise",
    ).astype(float)

    if (out["Value"] < 0).any():
        raise ValueError("IEEE TransactionAmt must be non-negative")
    if not out["FraudResult"].isin([0, 1]).all():
        raise ValueError("IEEE isFraud must be binary")
    _validate_probability(out)

    # Preserve useful scenario metadata when present. These columns are not
    # required by the shared simulator, but downstream analysis may use them.
    preferred_metadata = [
        "ProductCD",
        "card1",
        "card2",
        "card3",
        "card4",
        "card5",
        "card6",
        "DeviceType",
        "DeviceInfo",
    ]
    metadata = [c for c in preferred_metadata if c in out.columns]

    return out[CANONICAL_COLUMNS + metadata].copy()


def validate_canonical_scores(df: pd.DataFrame) -> None:
    missing = set(CANONICAL_COLUMNS).difference(df.columns)
    if missing:
        raise ValueError(
            f"Missing canonical score columns: {sorted(missing)}"
        )

    parsed_time = pd.to_datetime(
        df["TransactionStartTime"],
        utc=True,
        errors="raise",
    )
    if parsed_time.isna().any():
        raise ValueError("TransactionStartTime contains invalid values")

    if (pd.to_numeric(df["Value"], errors="raise") < 0).any():
        raise ValueError("Value must be non-negative")

    labels = pd.to_numeric(
        df["FraudResult"],
        errors="raise",
    )
    if not labels.isin([0, 1]).all():
        raise ValueError("FraudResult must be binary")

    probabilities = pd.to_numeric(
        df["risk_probability"],
        errors="raise",
    )
    if not probabilities.between(0.0, 1.0).all():
        raise ValueError("risk_probability must be in [0, 1]")
