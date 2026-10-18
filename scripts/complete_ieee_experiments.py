"""Run the frozen IEEE-CIS 12-cell experiment reproducibly in private storage.

This script *does not run in GitHub CI*. It requires local public-competition
raw data, Python packages and compute. By default it only prints the plan.
Pass --execute on an authorized machine to actually train/replay 12×N cells.

Experiment results are NOT proof of real fraudster behavior or bank losses.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from zipfile import ZipFile

import pandas as pd


EXPECTED_MODES = {"static", "adaptive"}
EXPECTED_POLICIES = {"fixed", "capacity_aware"}
EXPECTED_CAPACITIES = {0.75, 1.0, 1.25}
RUN_FILENAME = "ieee_closed_loop_runs.csv"


def seed_batches(total: int, batch_size: int) -> list[tuple[int, int]]:
    if total < 1 or batch_size < 1:
        raise ValueError("total and batch_size must be positive")
    return [(start, min(batch_size, total-start)) for start in range(0, total, batch_size)]


def validate_rows(frame: pd.DataFrame, expected_seeds: set[int]) -> None:
    keys = ["seed", "fraudster_mode", "policy", "capacity_ratio"]
    required = set(keys) | {"fraud_attempt_slots"}
    absent = required.difference(frame.columns)
    if absent:
        raise ValueError(f"Missing run fields: {sorted(absent)}")
    if frame.duplicated(keys).any():
        raise ValueError("Duplicate factors/seed combination")
    if set(frame["seed"].astype(int)) != expected_seeds:
        raise ValueError(f"Incorrect seeds: {sorted(set(frame.seed))} vs {sorted(expected_seeds)}")
    if len(frame) != 12 * len(expected_seeds):
        raise ValueError(f"Expected {12 * len(expected_seeds)} cells, found {len(frame)}")
    if set(frame["fraudster_mode"]) != EXPECTED_MODES:
        raise ValueError("Fraudster factors must be static and adaptive")
    if set(frame["policy"]) != EXPECTED_POLICIES:
        raise ValueError("Policy factors must be fixed and capacity_aware")
    if set(frame["capacity_ratio"].astype(float)) != EXPECTED_CAPACITIES:
        raise ValueError("Capacity factors must be 0.75, 1, 1.25")
    if not frame["fraud_attempt_slots"].eq(3083).all():
        raise ValueError("Full-test fraud attempt slots must equal 3,083 per cell")
    for seed in expected_seeds:
        chunk=frame.loc[frame.seed.eq(seed)]
        if len(chunk)!=12:
            raise ValueError(f"Seed {seed} lacks 12 complete factor cells")


def digest(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        while data := f.read(2**20):
            h.update(data)
    return h.hexdigest()


def invoke(args: list[str]) -> None:
    print("+", " ".join(map(str,args)), flush=True)
    subprocess.run(args, check=True)


def source_revision() -> str | None:
    try:
        return subprocess.check_output(
            ["git","rev-parse","HEAD"], text=True, stderr=subprocess.DEVNULL
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def execute(args) -> None:
    source=Path(args.zip).expanduser().resolve()
    if not source.exists():
        raise FileNotFoundError(f"Public IEEE-CIS ZIP not found: {source}")
    root=Path(args.output_dir).expanduser().resolve()
    if "outputs/local" not in root.as_posix():
        print("PRIVACY WARNING: keep output folder outside tracked/public Git files.")
    root.mkdir(parents=True,exist_ok=True)
    base=root/"baseline"
    context=root/"context"
    runs=root/"runs"
    model=base/"model_bundle.joblib"
    scores=[base/"validation_scores.csv",base/"test_scores.csv",base/"metrics.json"]
    if not (model.exists() and all(p.exists() for p in scores)):
        if base.exists() and any(base.iterdir()):
            raise RuntimeError("Partially populated baseline directory: investigate; refusing to overwrite")
        base.mkdir(parents=True,exist_ok=True)
        with ZipFile(source) as z, tempfile.TemporaryDirectory(prefix="ieee-training-") as d:
            folder=Path(d)
            for name in ("train_transaction.csv","train_identity.csv"):
                with z.open(name) as inp,(folder/name).open("wb") as out:
                    shutil.copyfileobj(inp,out,length=2**20)
            invoke([sys.executable,"-m","scripts.train_ieee_streaming_baseline",
                    "--transaction",str(folder/"train_transaction.csv"),
                    "--identity",str(folder/"train_identity.csv"),
                    "--alpha","0.001","--output-dir",str(base)])
    if not (model.exists() and all(p.exists() for p in scores)):
        raise AssertionError("Missing saved canonical baseline artifacts")
    hist=context/"history_context.csv"
    donors=context/"validation_fraud_donors.csv"
    test=context/"test_context.csv"
    if not all(p.exists() for p in (hist,donors,test)):
        if context.exists() and any(context.iterdir()):
            raise RuntimeError("Partial IEEE contexts: investigate; refusing to overwrite")
        invoke([sys.executable,"-m","scripts.prepare_ieee_closed_loop",
                "--zip",str(source),"--output-dir",str(context)])
    audit=context/"audit_full.json"
    if not audit.exists():
        invoke([sys.executable,"-m","scripts.audit_ieee_online_equivalence",
                "--test-scores",str(base/"test_scores.csv"),
                "--test-context",str(test),"--history-context",str(hist),
                "--model-bundle",str(model),"--n-events",str(args.audit_events),
                "--tolerance","1e-6","--output",str(audit)])
    audit_payload=json.loads(audit.read_text(encoding="utf-8"))
    if not audit_payload.get("pass"):
        raise RuntimeError("Frozen IEEE heldout score audit failed; do not run adaptive experiment")
    if audit_payload.get("n_events",0) < args.audit_events:
        raise RuntimeError("Score audit covers fewer events than requested")
    # Descriptive donor audit is not calibration from test data.
    registry=context/"regime_audit"/"regime_registry.csv"
    if not registry.exists():
        invoke([sys.executable,"-m","scripts.audit_ieee_donor_regimes",
                "--validation-donors",str(donors),"--test-context",str(test),
                "--output-dir",str(context/"regime_audit")])
    runs.mkdir(parents=True,exist_ok=True)
    batches=[]
    for start,count in seed_batches(args.target_seeds,args.batch_seeds):
        folder=runs/f"seeds_{start:03d}_{start+count-1:03d}"
        path=folder/RUN_FILENAME
        if not path.exists():
            if folder.exists() and any(folder.iterdir()):
                raise RuntimeError(f"Partial run folder {folder}; do not silently overwrite")
            invoke([sys.executable,"-m","scripts.run_ieee_feature_level_static_adaptive",
                    "--validation-scores",str(base/"validation_scores.csv"),
                    "--validation-donors",str(donors),
                    "--test-context",str(test),"--history-context",str(hist),
                    "--model-bundle",str(model),"--seeds",str(count),
                    "--seed-start",str(start),"--scorer","fast",
                    "--output-dir",str(folder)])
        frame=pd.read_csv(path)
        validate_rows(frame,set(range(start,start+count)))
        batches.append(frame)
    full=pd.concat(batches,ignore_index=True)
    validate_rows(full,set(range(args.target_seeds)))
    full=full.sort_values(["seed","fraudster_mode","policy","capacity_ratio"]).reset_index(drop=True)
    combined=root/"ieee_final_run_level.csv"
    if combined.exists():
        earlier=pd.read_csv(combined)
        # Abort rather than overwrite if results differ from already archived file.
        pd.testing.assert_frame_equal(
            earlier.reset_index(drop=True),full,check_dtype=False,rtol=1e-10,atol=1e-12
        )
    else:
        full.to_csv(combined,index=False)
    invoke([sys.executable,"-m","scripts.summarize_ieee_closed_loop",
            "--runs",str(combined),"--output-dir",str(root/"analysis")])
    metadata={
        "result_status":"canonical_runner_completed_pending_sensitivity_and_advisor_review",
        "git_commit_sha":source_revision(),
        "python_version":sys.version,
        "original_zip_sha256":digest(source),
        "model_sha256":digest(model),
        "combined_run_sha256":digest(combined),
        "audit_report":audit_payload,
        "seeds":args.target_seeds,
        "grid":"12 cells per seed",
        "fraud_slots_per_full_test_cell":3083,
        "do_not_claim":"real bank losses or observed real fraudster learning",
    }
    (root/"manifest.json").write_text(
        json.dumps(metadata,indent=2,ensure_ascii=False),encoding="utf-8"
    )
    print("Canonical IEEE batch run completed. Check pilot equivalence, sensitivity and intervals before thesis claims.")


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--zip",required=True,help="Original public Kaggle competition ZIP, stored privately")
    p.add_argument("--output-dir",default="outputs/local/ieee_final")
    p.add_argument("--target-seeds",type=int,default=30)
    p.add_argument("--batch-seeds",type=int,default=5)
    p.add_argument("--audit-events",type=int,default=88581)
    p.add_argument("--execute",action="store_true",help="Explicit opt-in to train and run full experiment")
    args=p.parse_args()
    if args.audit_events<1 or args.audit_events>88581:
        p.error("--audit-events must be within held-out 1..88581")
    batches=seed_batches(args.target_seeds,args.batch_seeds)
    print(f"IEEE plan: {len(batches)} batches, 12×{args.target_seeds}={12*args.target_seeds} cells, audit {args.audit_events} heldout events")
    if not args.execute:
        print("DRY RUN ONLY. Pass --execute to train/pilot/run using your local private artifacts.")
        for s,n in batches:print(f"  seeds {s}..{s+n-1}")
        return
    execute(args)


if __name__=="__main__":
    main()
