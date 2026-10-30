import pandas as pd
import pytest

from scripts.complete_ieee_experiments import seed_batches, validate_rows


def make_complete(n=3):
    rows=[]
    for seed in range(n):
        for mode in ("static", "adaptive"):
            for policy in ("fixed", "capacity_aware"):
                for capacity in (0.75, 1.0, 1.25):
                    rows.append({"seed":seed, "fraudster_mode":mode, "policy":policy,
                                 "capacity_ratio":capacity,"fraud_attempt_slots":3083})
    return pd.DataFrame(rows)


def test_batches_cover_all_seeds_once():
    batches=seed_batches(31, 5)
    ids=[s+i for s,n in batches for i in range(n)]
    assert ids==list(range(31))
    assert batches[-1]==(30,1)
    with pytest.raises(ValueError):
        seed_batches(0,5)


def test_validate_complete_grid():
    validate_rows(make_complete(), {0,1,2})


def test_reject_duplicate_or_missing_cells():
    df=make_complete()
    with pytest.raises(ValueError, match="Duplicate"):
        validate_rows(pd.concat([df,df.iloc[:1]],ignore_index=True),{0,1,2})
    with pytest.raises(ValueError):
        validate_rows(df.iloc[:-1].copy(),{0,1,2})


def test_reject_nonfinal_fraud_attempt_count():
    df=make_complete()
    df.loc[0,"fraud_attempt_slots"]=20
    with pytest.raises(ValueError,match="3,083"):
        validate_rows(df,{0,1,2})
