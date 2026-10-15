"""Profile the Xente Fraud Detection training data without redistributing row-level data.

Usage
-----
python scripts/profile_xente.py --input data/raw/xente/training.csv

The script writes aggregate-only outputs to outputs/local/, which is ignored by Git.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = [
    "TransactionId",
    "AccountId",
    "SubscriptionId",
    "CustomerId",
    "Amount",
    "Value",
    "TransactionStartTime",
    "FraudResult",
]


def quantile_summary(series: pd.Series) -> dict[str, float | int | None]:
    s = pd.to_numeric(series, errors="coerce").dropna()
    if s.empty:
        return {"count": 0}
    q = s.quantile([0, 0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99, 1.0])
    return {
        "count": int(s.size),
        "mean": float(s.mean()),
        "std": float(s.std()),
        "min": float(q.loc[0.0]),
        "p01": float(q.loc[0.01]),
        "p05": float(q.loc[0.05]),
        "p25": float(q.loc[0.25]),
        "median": float(q.loc[0.5]),
        "p75": float(q.loc[0.75]),
        "p95": float(q.loc[0.95]),
        "p99": float(q.loc[0.99]),
        "max": float(q.loc[1.0]),
    }


def entity_summary(df: pd.DataFrame, key: str) -> dict[str, float | int]:
    counts = df.groupby(key, dropna=False).size()
    return {
        "unique_entities": int(counts.size),
        "transactions_per_entity_mean": float(counts.mean()),
        "transactions_per_entity_median": float(counts.median()),
        "transactions_per_entity_p95": float(counts.quantile(0.95)),
        "transactions_per_entity_max": int(counts.max()),
        "share_entities_with_2plus_tx": float((counts >= 2).mean()),
        "share_entities_with_5plus_tx": float((counts >= 5).mean()),
    }


def split_diagnostics(df: pd.DataFrame) -> list[dict[str, float | int]]:
    out: list[dict[str, float | int]] = []
    n = len(df)
    for frac in (0.60, 0.70, 0.75, 0.80):
        cut = max(1, min(n - 1, int(n * frac)))
        left = df.iloc[:cut]
        right = df.iloc[cut:]
        out.append(
            {
                "train_fraction": frac,
                "train_rows": int(len(left)),
                "train_fraud": int(left["FraudResult"].sum()),
                "train_fraud_rate": float(left["FraudResult"].mean()),
                "holdout_rows": int(len(right)),
                "holdout_fraud": int(right["FraudResult"].sum()),
                "holdout_fraud_rate": float(right["FraudResult"].mean()),
                "cut_timestamp": str(right["TransactionStartTime"].iloc[0]),
            }
        )
    return out


def build_profile(df: pd.DataFrame) -> dict:
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df = df.copy()
    df["TransactionStartTime"] = pd.to_datetime(
        df["TransactionStartTime"], utc=True, errors="coerce"
    )
    df["FraudResult"] = pd.to_numeric(df["FraudResult"], errors="raise").astype(int)
    df = df.sort_values(["TransactionStartTime", "TransactionId"]).reset_index(drop=True)

    fraud = df["FraudResult"].eq(1)
    nonfraud = ~fraud

    time_valid = df["TransactionStartTime"].dropna()
    daily = (
        df.dropna(subset=["TransactionStartTime"])
        .assign(date=lambda x: x["TransactionStartTime"].dt.floor("D"))
        .groupby("date")
        .agg(transactions=("TransactionId", "size"), fraud=("FraudResult", "sum"))
        .reset_index()
    )

    profile = {
        "rows": int(len(df)),
        "columns": int(df.shape[1]),
        "column_names": list(df.columns),
        "fraud_count": int(fraud.sum()),
        "nonfraud_count": int(nonfraud.sum()),
        "fraud_rate": float(fraud.mean()) if len(df) else None,
        "time": {
            "start": str(time_valid.min()) if not time_valid.empty else None,
            "end": str(time_valid.max()) if not time_valid.empty else None,
            "days_observed": int(time_valid.dt.floor("D").nunique()) if not time_valid.empty else 0,
        },
        "missing_values": {c: int(df[c].isna().sum()) for c in df.columns},
        "entities": {
            "CustomerId": entity_summary(df, "CustomerId"),
            "AccountId": entity_summary(df, "AccountId"),
            "SubscriptionId": entity_summary(df, "SubscriptionId"),
        },
        "amount_all": quantile_summary(df["Amount"]),
        "amount_fraud": quantile_summary(df.loc[fraud, "Amount"]),
        "amount_nonfraud": quantile_summary(df.loc[nonfraud, "Amount"]),
        "value_all": quantile_summary(df["Value"]),
        "value_fraud": quantile_summary(df.loc[fraud, "Value"]),
        "value_nonfraud": quantile_summary(df.loc[nonfraud, "Value"]),
        "daily_volume": quantile_summary(daily["transactions"]) if not daily.empty else {},
        "daily_fraud": quantile_summary(daily["fraud"]) if not daily.empty else {},
        "chronological_split_diagnostics": split_diagnostics(df),
    }

    for col in ("ProductCategory", "ChannelId", "ProviderId", "ProductId", "PricingStrategy"):
        if col in df.columns:
            vc = df[col].value_counts(dropna=False, normalize=True).head(20)
            profile[f"top_{col}"] = {str(k): float(v) for k, v in vc.items()}

    return profile


def profile_to_markdown(profile: dict) -> str:
    e = profile["entities"]
    lines = [
        "# Xente local profile",
        "",
        "> Aggregate-only local output. Do not commit raw Xente competition data.",
        "",
        "## Core",
        f"- Rows: {profile['rows']:,}",
        f"- Fraud count: {profile['fraud_count']:,}",
        f"- Fraud rate: {profile['fraud_rate']:.6%}",
        f"- Time start: {profile['time']['start']}",
        f"- Time end: {profile['time']['end']}",
        f"- Days observed: {profile['time']['days_observed']}",
        "",
        "## Entity repetition",
    ]
    for key in ("CustomerId", "AccountId", "SubscriptionId"):
        d = e[key]
        lines += [
            f"### {key}",
            f"- Unique: {d['unique_entities']:,}",
            f"- Median transactions/entity: {d['transactions_per_entity_median']:.2f}",
            f"- P95 transactions/entity: {d['transactions_per_entity_p95']:.2f}",
            f"- Share entities with >=2 transactions: {d['share_entities_with_2plus_tx']:.2%}",
            "",
        ]

    lines += [
        "## Chronological split diagnostics",
        "",
        "| Train fraction | Train fraud | Holdout fraud | Holdout rows | Cut timestamp |",
        "|---:|---:|---:|---:|---|",
    ]
    for d in profile["chronological_split_diagnostics"]:
        lines.append(
            f"| {d['train_fraction']:.0%} | {d['train_fraud']} | "
            f"{d['holdout_fraud']} | {d['holdout_rows']:,} | {d['cut_timestamp']} |"
        )
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to Xente training.csv")
    parser.add_argument("--output-dir", default="outputs/local")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_path = Path(args.input)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(input_path)
    profile = build_profile(df)

    json_path = output_dir / "xente_profile.json"
    md_path = output_dir / "xente_profile.md"

    json_path.write_text(json.dumps(profile, indent=2, ensure_ascii=False), encoding="utf-8")
    md_path.write_text(profile_to_markdown(profile), encoding="utf-8")

    print(f"Wrote {json_path}")
    print(f"Wrote {md_path}")
    print(
        f"rows={profile['rows']:,}, fraud={profile['fraud_count']:,}, "
        f"fraud_rate={profile['fraud_rate']:.6%}"
    )


if __name__ == "__main__":
    main()
