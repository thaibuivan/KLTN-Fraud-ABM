import io

import numpy as np
import pandas as pd

from scripts.build_ieee_features import TRANSACTION_COLUMNS, IDENTITY_COLUMNS
from scripts.prepare_ieee_closed_loop import prepare


def test_three_way_split_and_validation_only_donors(tmp_path):
    n = 20
    tx = pd.DataFrame({c: [np.nan] * n for c in TRANSACTION_COLUMNS})
    tx["TransactionID"] = list(range(1, n + 1))
    tx["TransactionDT"] = list(range(1, n + 1))
    tx["TransactionAmt"] = [float(i) for i in range(1, n + 1)]
    tx["ProductCD"] = ["W"] * n
    tx["card1"] = [101] * n
    tx["addr1"] = [100] * n
    tx["isFraud"] = [0] * 14 + [1, 0, 0] + [1, 0, 0]
    identity = pd.DataFrame({c: [np.nan] * n for c in IDENTITY_COLUMNS})
    identity["TransactionID"] = list(range(1, n + 1))
    stats = prepare(io.StringIO(tx.to_csv(index=False)),
                    io.StringIO(identity.to_csv(index=False)),
                    tmp_path, chunksize=4)
    assert stats == {"history": 17, "donors": 1, "test": 3}
    donors = pd.read_csv(tmp_path / "validation_fraud_donors.csv")
    test = pd.read_csv(tmp_path / "test_context.csv")
    assert donors["TransactionID"].tolist() == [15]
    assert test["TransactionID"].tolist() == [18, 19, 20]
    assert pd.read_csv(tmp_path / "history_context.csv").shape[0] == 17
