"""Prepare leakage-safe local IEEE-CIS context streams for ABM pilot.

Requires original labeled IEEE train_transaction.csv and train_identity.csv.
Use only validation fraud as donor contexts, and ALL train+validation events
only to warm past-only history. Test labels supply attempt slots, not donors.
No raw or restricted data is committed to GitHub.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import zipfile
import shutil
import tempfile

import pandas as pd

from scripts.build_ieee_features import (
    IDENTITY_COLUMNS, TRANSACTION_COLUMNS,
)
from scripts.train_ieee_streaming_baseline import join_identity


def prepare(transaction, identity, out_dir: str | Path, *, chunksize=5000):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    n = sum(1 for _ in transaction) - 1
    transaction.seek(0)
    train_end = int(n * .70)
    validation_end = int(n * .85)
    identity_df = pd.read_csv(identity, usecols=IDENTITY_COLUMNS)
    identity_df["identity_available"] = 1
    history_path = out_dir / "history_context.csv"
    donor_path = out_dir / "validation_fraud_donors.csv"
    test_path = out_dir / "test_context.csv"
    for p in (history_path, donor_path, test_path):
        if p.exists():
            raise FileExistsError(f"Refusing to overwrite {p}")
    start = 0
    counts = {"history": 0, "donors": 0, "test": 0}
    for chunk in pd.read_csv(transaction, usecols=TRANSACTION_COLUMNS, chunksize=chunksize):
        end = start + len(chunk)
        merged = join_identity(chunk, identity_df)
        regions = {
            "history": merged.iloc[:max(0, min(end, validation_end) - start)],
            "validation": merged.iloc[max(0, train_end - start):max(0, min(end, validation_end) - start)],
            "test": merged.iloc[max(0, validation_end - start):],
        }
        hist = regions["history"][[
            "TransactionID", "TransactionDT", "TransactionAmt", "ProductCD",
            "card1", "addr1", "identity_available",
        ]]
        donor = regions["validation"].loc[regions["validation"]["isFraud"].eq(1)]
        test = regions["test"]
        for name, df, path in (("history", hist, history_path),
                               ("donors", donor, donor_path),
                               ("test", test, test_path)):
            if df.empty:
                continue
            df.to_csv(path, mode="a", index=False, header=not path.exists())
            counts[name] += len(df)
        start = end
    if start != n or counts["history"] != validation_end or counts["test"] != n - validation_end:
        raise AssertionError("IEEE chronological split counts failed")
    return counts


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--zip", required=True, help="IEEE competition zip, kept local")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--chunksize", type=int, default=5000)
    a = parser.parse_args()
    with zipfile.ZipFile(a.zip) as z:
        with tempfile.TemporaryDirectory() as tmp:
            for name in ("train_transaction.csv", "train_identity.csv"):
                with z.open(name) as source, (Path(tmp) / name).open("wb") as dest:
                    shutil.copyfileobj(source, dest, length=1024 * 1024)
            with (Path(tmp)/"train_transaction.csv").open("r", encoding="utf-8") as tx, (Path(tmp)/"train_identity.csv").open("r", encoding="utf-8") as identity:
                print(prepare(tx, identity, a.output_dir, chunksize=a.chunksize))


if __name__ == "__main__":
    main()
