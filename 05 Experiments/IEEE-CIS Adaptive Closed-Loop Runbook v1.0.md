# IEEE-CIS Adaptive Closed-Loop — Reproduction Runbook v1.0

Date: 2026-10-18. Target branch: chatgpt-draft. **Do not run commands against Green SM data.** These commands use only Kaggle/IEEE-CIS research datasets and model artifacts saved privately.

## 0. Gate 0: inputs and storage

Prerequisites: Python 3.11, requirements installed; archive ieee-fraud-detection.zip available locally. The archive is public competition data but should remain outside this public GitHub repository. Expected original CSVs: train_transaction.csv, train_identity.csv. Do not upload model bundle, score artifacts or raw data to the public repo without checking their applicable license and permissions.

Existing empirical baseline on Oct 15 was executed and reported in the IEEE-CIS Baseline and Policy Replay v0.1 note. If saved local model outputs are no longer available, reproduce with the existing canonical trainer.

## 1. Recreate the baseline (only if artifacts are absent)

Extract the train CSVs into a private temporary directory. Run:

    python -m scripts.train_ieee_streaming_baseline \
      --transaction /private/ieee/train_transaction.csv \
      --identity /private/ieee/train_identity.csv \
      --output-dir outputs/local/ieee_streaming_baseline \
      --alpha 0.001

Save:
- outputs/local/ieee_streaming_baseline/model_bundle.joblib
- outputs/local/ieee_streaming_baseline/validation_scores.csv
- outputs/local/ieee_streaming_baseline/test_scores.csv
- outputs/local/ieee_streaming_baseline/metrics.json

Baseline checks: validation PR-AUC around 0.3644, test around 0.3840; validation/test sizes 88,581 each. If results do not reproduce closely, investigate versions, preprocessing and row-order differences before proceeding.

## 2. Prepare private closed-loop contexts

    python -m scripts.prepare_ieee_closed_loop \
      --zip /private/ieee-fraud-detection.zip \
      --output-dir outputs/local/ieee_closed_loop

Expected exact counts from a direct raw-data preparation completed 18 Oct:
- history_context.csv: 501,959 events;
- validation_fraud_donors.csv: 3,042 fraud events, all from validation;
- test_context.csv: 88,581 events (3,083 fraud attempt slots).

The donor generator uses validation amount terciles 50 and 117, with the fraud median 77 as reward scale. No test fraud context is sampled as a donor.

## 3. Mandatory online equivalence audit

    python -m scripts.audit_ieee_online_equivalence \
      --test-scores outputs/local/ieee_streaming_baseline/test_scores.csv \
      --test-context outputs/local/ieee_closed_loop/test_context.csv \
      --history-context outputs/local/ieee_closed_loop/history_context.csv \
      --model-bundle outputs/local/ieee_streaming_baseline/model_bundle.joblib \
      --n-events 200 --tolerance 0.000001 \
      --output outputs/local/ieee_closed_loop/score_audit.json

The audit must pass against the **same frozen baseline**. Test on larger prefixes after a 200-event pass. CI confirms algorithmic equivalence only on synthetic, fitted test cases. The real-data audit is NOT yet verified. The 200-event audit does not guarantee all remaining events match; investigate systematic and tail differences on a larger sample before reporting.

Fast scorer is an algebraic optimization, also tested for equivalence on synthetic examples. It should be cross-checked on real held-out data before replacing the reference scorer in final 12×N-seed runs.

## 4. Closed-loop smoke

    python -m scripts.run_ieee_feature_level_static_adaptive \
      --validation-scores outputs/local/ieee_streaming_baseline/validation_scores.csv \
      --validation-donors outputs/local/ieee_closed_loop/validation_fraud_donors.csv \
      --test-context outputs/local/ieee_closed_loop/test_context.csv \
      --history-context outputs/local/ieee_closed_loop/history_context.csv \
      --model-bundle outputs/local/ieee_streaming_baseline/model_bundle.joblib \
      --seeds 1 --max-test-events 2000 \
      --scorer reference \
      --output-dir outputs/local/ieee_closed_loop/smoke

All 12 cells should be present (2 behaviors × 2 policies × 3 capacity ratios). Use the same fraud attempt schedule per cell. The 2,000-event smoke is a correctness pilot, NOT final hypothesis testing; the fixed 70/15/15 reference capacity remains calibrated on full validation and pilot-window queue metrics are not externally interpretable.

## 5. Full empirical runs and replication

After the smoke and real-score equivalence audits pass:

    python -m scripts.run_ieee_feature_level_static_adaptive \
      --validation-scores outputs/local/ieee_streaming_baseline/validation_scores.csv \
      --validation-donors outputs/local/ieee_closed_loop/validation_fraud_donors.csv \
      --test-context outputs/local/ieee_closed_loop/test_context.csv \
      --history-context outputs/local/ieee_closed_loop/history_context.csv \
      --model-bundle outputs/local/ieee_streaming_baseline/model_bundle.joblib \
      --seeds 10 --scorer fast \
      --output-dir outputs/local/ieee_closed_loop/pilot10

Estimate memory/runtime from pilot10 and run a convergence check. Increase to 30–50+ seeds where Monte Carlo SE and uncertainty of exposure metrics justify the budget. Do not assume N=50 is sufficient just because Xente used 50. The exact reference scorer can be expensive; the fast scorer must be validated empirically before using it to draw final conclusions.

Additional stress run (different REVIEW observability assumption):

    python -m scripts.run_ieee_feature_level_static_adaptive \
      --validation-scores outputs/local/ieee_streaming_baseline/validation_scores.csv \
      --validation-donors outputs/local/ieee_closed_loop/validation_fraud_donors.csv \
      --test-context outputs/local/ieee_closed_loop/test_context.csv \
      --history-context outputs/local/ieee_closed_loop/history_context.csv \
      --model-bundle outputs/local/ieee_streaming_baseline/model_bundle.joblib \
      --seeds 10 --scorer fast \
      --review-feedback no_review_observation \
      --output-dir outputs/local/ieee_closed_loop/no_review_feedback

The no-review-observation variant **omits learning updates on REVIEW**; it does not model a realistic delayed feedback distribution. Report this narrow assumption explicitly.

## 6. Aggregate policy/adaptation contrasts

    python -m scripts.summarize_ieee_closed_loop \
      --runs outputs/local/ieee_closed_loop/pilot10/ieee_closed_loop_runs.csv \
      --output-dir outputs/local/ieee_closed_loop/pilot10/analysis

Three tables: cells.csv (means, SD, MCSE, t-95% intervals), policy_contrasts.csv (Capacity-aware minus Fixed within seed/mode/capacity), adaptation_contrasts.csv (Adaptive minus Static within seed/policy/capacity). N=1 has no valid uncertainty interval. Value outcomes require careful tail diagnostics.

For sensitivity to review prevention, the runner stores assumed q=0/0.5/1 accounting columns; these are NOT bank-estimated recovery rates.

## 7. Checks before writing IEEE results

- Same risk model and preprocessing frozen across policy/behavior cells.
- No test labels used for fraud-donor generation, classifier training or threshold calibration.
- Legitimate events re-scored under altered counterfactual history.
- Exact attempt slot counts preserved across all conditions.
- Independent re-initialization of agent state, queue, model history per run.
- Counterfactual grouping supports only within-scenario claims.
- Frauds REVIEWed before horizon are not conflated with real prevented financial loss.
- Run results and figures include seed uncertainty and parameter sources.
- Never merge Xente/IEEE monetary amounts; normalize contrasts and report cross-scenario limitations.

## 8. Current status

**Completed:** code added, CI integration tests, reference-vs-offline synthetic equivalence, preparer executed on the real IEEE raw archive, real data split counts verified.

**Still required:** actual frozen model bundle/score artifact must be loaded or retrained in the execution environment; real held-out score audit; full IEEE adaptive closed-loop smoke; full 12×N-seed output; cross-scenario analysis; final paper/appendices. Do not claim these are done based on passing pytest alone.


## 9. Independent seed batches / resumable replication — added 18 Oct

The canonical runner now accepts **`--seed-start`** (absolute initial seed ID) and **`--seeds`** (batch size); the run output has the absolute `seed` column. This permits continuation of a 5-seed pilot without recomputing seed IDs 0–4.

Example *once private data/model artifacts have been made available in the local authorized environment*:

```bash
python -m scripts.run_ieee_feature_level_static_adaptive \
  --validation-scores outputs/local/ieee_streaming_baseline/validation_scores.csv \
  --validation-donors outputs/local/ieee_closed_loop/validation_fraud_donors.csv \
  --test-context outputs/local/ieee_closed_loop/test_context.csv \
  --history-context outputs/local/ieee_closed_loop/history_context.csv \
  --model-bundle outputs/local/ieee_streaming_baseline/model_bundle.joblib \
  --seed-start 5 --seeds 5 --scorer fast \
  --output-dir outputs/local/ieee_closed_loop/seeds_05_09
```

Continue for non-overlapping `--seed-start 10 --seeds 5`, etc., until Monte Carlo convergence. **Do not assume the mirrored 0–4 pilot corresponds exactly to the canonical runner:** first run canonical `--seed-start 0 --seeds 5` independently, compare outputs to archived mirrored pilot by key, then decide whether to reuse/combine. For exact comparison use `seed, fraudster_mode, policy, capacity_ratio`; compare core metrics with declared numerical tolerance and flag discrepancies, never silently concatenate conflicting runs.

Combination check (illustrative; execute locally where CSVs exist):

```python
import pathlib, pandas as pd
files = sorted(pathlib.Path("outputs/local/ieee_closed_loop").glob("seeds_*/ieee_closed_loop_runs.csv"))
rows = pd.concat((pd.read_csv(f) for f in files), ignore_index=True)
keys = ["seed", "fraudster_mode", "policy", "capacity_ratio"]
assert not rows.duplicated(keys).any(), "Overlapping or duplicated seed-condition cells"
assert set(rows["capacity_ratio"]) == {0.75, 1.0, 1.25}
assert rows.groupby("seed").size().eq(12).all(), "A seed is missing core cells"
rows.to_csv("outputs/local/ieee_closed_loop/combined_runs.csv", index=False)
```

Run summary on `combined_runs.csv`, not pilot-only and never with duplicate seeds. Archive: checked-out commit SHA, command, sanitized package versions, SHA256 of input artifacts (not raw files), seed start/end, final CSV SHA256, dates, and any deviations from baseline. Never commit raw IEEE/Xente rows, fitted model bundle, or unapproved company content into public GitHub.

**Validation of new interface:** `tests/test_ieee_closed_loop_runner.py` tests reproducible non-overlapping batches and invalid negative seeds. GitHub CI is software verification, not empirical validity.

**Open blocker as of 18 Oct:** The ChatGPT Project Library currently exposes the archived private reproduction ZIPs in metadata, but byte materialization in this execution environment was denied. Therefore the archived 5-seed pilot could be read from its documentation but the canonical full-data rerun was **not executed in this turn**. Do not state otherwise.
