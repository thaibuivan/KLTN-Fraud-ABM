# FINAL IEEE REPRODUCIBILITY GATE & THESIS ACCEPTANCE CHECKLIST v1.0

**18/10/2026. Status:** **NOT PASSED YET** for IEEE main run. This document separates code tests, independently reported real-data checks, and reproducibility of the exact canonical runner. Source of truth is the latest Git commit plus the artifacts produced privately by the commands below. Never commit competition raw data, user data, model bundle, or organization-internal information.

## A. Evidence tiers

| Evidence | As of 18 Oct | Acceptance |
|---|---|---|
| GitHub CI unit/integration tests | PASSED on 9d5bf32 and preceding commits | Code behavior checks only |
| IEEE streaming SGD baseline | Reported independently reproduced | Store metrics, training command, frozen model checksum |
| IEEE real-data unchanged-score equivalence (88,581 events) | Reported PASS: max abs error 4.3138e-7 at tolerance 1e-6 | Archive audit output, scorer/model SHA and command |
| IEEE 12×5 full-test pilot | **Executed via local mirror**, NOT canonical repo runner | Canonical replay must match within stated tolerances |
| IEEE 12×N final seed run | **PENDING** | 12 cell keys × N seeds with convergence |
| IEEE reward/feedback/outcome sensitivity | One-seed exploratory ablations, outcome accounting code | Multi-seed sensitivity with intervals |
| Xente 12×50 main | Candidate final | Lock code/semantics and verify stored run manifest |
| Cross-scenario conclusions | **PENDING** | Within-scenario effects + intervals, no raw currency pooling |
| Advisor approval/thesis manuscript | **PENDING** | User + GVHD review and final formatting |

## B. Inputs and environment

- Use branch `chatgpt-draft`; record `git rev-parse HEAD` before each execution. Do not silently mix outputs from different commits.
- Python 3.11; install `requirements.txt`. Record `python --version` and `pip freeze`.
- IEEE original Kaggle archive `ieee-fraud-detection.zip`, saved **outside public GitHub**; original labeled `train_transaction.csv` and `train_identity.csv`.
- Reproduce frozen baseline bundle and score files only if missing, using `scripts.train_ieee_streaming_baseline`. Verify validation/test PR-AUC 0.36438685/0.38403028 to documented precision.
- Private context extraction: `scripts.prepare_ieee_closed_loop`. Expected history/donor/test counts: 501,959/3,042/88,581; fraud test slots: 3,083.
- Use train+validation context for warmup, validation frauds as donors. Test labels enter only fixed fraud-attempt slot scheduling and evaluation.

## C. Minimum executable command sequence

Commands assume an already checked-out repo and baseline outputs in `outputs/local/ieee_streaming_baseline`.

```bash
# 1. Confirm source SHA and software versions
git rev-parse HEAD
python --version
python -m pytest -q

# 2. Prepare held-out contexts (only if NOT already generated)
python -m scripts.prepare_ieee_closed_loop \
  --zip /private/ieee-fraud-detection.zip \
  --output-dir outputs/local/ieee_closed_loop

# 3. Audit exact frozen risk probabilities
python -m scripts.audit_ieee_online_equivalence \
  --test-scores outputs/local/ieee_streaming_baseline/test_scores.csv \
  --test-context outputs/local/ieee_closed_loop/test_context.csv \
  --history-context outputs/local/ieee_closed_loop/history_context.csv \
  --model-bundle outputs/local/ieee_streaming_baseline/model_bundle.joblib \
  --n-events 88581 --tolerance 0.000001 \
  --output outputs/local/ieee_closed_loop/score_audit_full.json

# 4. Small deterministic smoke and full 5-seed canonical pilot
python -m scripts.run_ieee_feature_level_static_adaptive \
  --validation-scores outputs/local/ieee_streaming_baseline/validation_scores.csv \
  --validation-donors outputs/local/ieee_closed_loop/validation_fraud_donors.csv \
  --test-context outputs/local/ieee_closed_loop/test_context.csv \
  --history-context outputs/local/ieee_closed_loop/history_context.csv \
  --model-bundle outputs/local/ieee_streaming_baseline/model_bundle.joblib \
  --seeds 1 --max-test-events 2000 --scorer reference \
  --output-dir outputs/local/ieee_closed_loop/canonical_smoke

python -m scripts.run_ieee_feature_level_static_adaptive \
  --validation-scores outputs/local/ieee_streaming_baseline/validation_scores.csv \
  --validation-donors outputs/local/ieee_closed_loop/validation_fraud_donors.csv \
  --test-context outputs/local/ieee_closed_loop/test_context.csv \
  --history-context outputs/local/ieee_closed_loop/history_context.csv \
  --model-bundle outputs/local/ieee_streaming_baseline/model_bundle.joblib \
  --seeds 5 --scorer fast \
  --output-dir outputs/local/ieee_closed_loop/canonical_pilot5

# 5. Summarize and retain output/checksum
python -m scripts.summarize_ieee_closed_loop \
  --runs outputs/local/ieee_closed_loop/canonical_pilot5/ieee_closed_loop_runs.csv \
  --output-dir outputs/local/ieee_closed_loop/canonical_pilot5/analysis
sha256sum outputs/local/ieee_closed_loop/canonical_pilot5/ieee_closed_loop_runs.csv
```

**Operational note:** Do not rerun the context preparer into a nonempty destination: the script intentionally refuses to overwrite existing output files. Back up/move previous contexts or skip step 2. An `--n-events 88581` audit can be computationally costly; run a 200-event prefix first if resource constraints require it, then full audit before claiming passed.

## D. Mandatory automatic checks on canonical pilot

1. Exactly **12 unique factor cells** per seed: two fraudster modes × two policies × three capacities. With N=5, total rows must equal 60 and unique keys (`seed`, `fraudster_mode`, `policy`, `capacity_ratio`) must be valid.
2. For each event, unique TransactionId and exactly one action among APPROVE, REVIEW, BLOCK.
3. Fraud attempts must equal **3,083 per full-test cell**; any truncation via `--max-test-events` makes that run smoke-only.
4. `risk_probability` finite, within [0,1]; no test fraud raw event reused as donor.
5. All generated score/context features use current/past-only history; no future/test label as input.
6. Policy threshold and service-rate calibration frozen by validation; BLOCK dominates REVIEW.
7. No raw Xente–IEEE monetary comparison. Outcome values obey accounting identity and q=0/0.5/1 sensitivity definitions.
8. Exact same seed/code/data/artifact/config rerun should reproduce file content or well-explained floating-point-tolerant metrics. Store hashes and package versions.
9. Compare **all** pilot cells against mirrored `IEEE-CIS Adaptive Full-Test Pilot v0.2`; define numeric tolerance before assessing. Differences require root-cause analysis and re-issuance of pilot results.
10. Repo GitHub CI success alone does not pass any real-data hypothesis-testing gate.

## E. Scale to IEEE final 12×N

After canonical pilot equivalence, benchmark runtime and memory for N=10. Increase to N=30 or 50+ only when needed by MCSE and confidence interval stability, focusing on exposure heavy tails and close policy contrasts. Save per-seed `ieee_closed_loop_runs.csv`, exact CLI, score/model checksum, `cells.csv`, `policy_contrasts.csv`, `adaptation_contrasts.csv` and any plotting inputs.

**Statistical acceptance:**
- All primary count/intervention/backlog means carry CI or appropriate MCSE.
- Close contrasts must be labeled uncertain if intervals cross zero.
- Value exposure needs tail diagnostics and uncertainty interval.
- Sufficient seeds are determined empirically; Xente's N=50 is not proof of IEEE convergence.
- Nonlinear/adaptive trajectories can diverge across policies, so pair-by-seed does not guarantee variance reduction.
- Same-budget diagnostic report: effective reviews per fraud intercepted, legitimate interventions, and total review volume together; do not claim policy intelligence merely because fewer alerts were routed.

## F. Robustness prior to thesis lock

- IEEE reward/value vs unit-response reward: ≥ several seeds, matched by experimental design, report share and outcomes.
- REVIEW observability: baseline `policy_action` vs `no_review_observation`; this omits reward update on REVIEW and is NOT a physically calibrated review delay.
- Outcome: report direct BLOCK, REVIEW started, REVIEW completed and assumed effectiveness `q=0/0.5/1`; realized bank loss is **not estimated**.
- Alpha/epsilon variation and fraud amount strategy donor-pattern diagnostics.
- At least one structural check of queue discipline or detector quality when feasible.
- Test negative/extreme cases (zero/near-zero service; high capacity; no adaptation).
- Cross-scenario effect sizes and signs in normalized, within-scenario units; separate robust/environment-dependent/uncertain categories.

## G. Academic manuscript and sign-off

- [x] Research design frozen: 24 configurations and 4 RQs.
- [x] Xente main core and robustness documented.
- [x] IEEE baseline, generator, scorer and runner code added.
- [x] Chapter 1 Introduction draft v1.0.
- [x] Chapter 2 Literature Review draft v1.0.
- [x] Chapter 3 Data/Experimental Setting draft v1.0.
- [x] Methodology Full Draft v1.1 (previously existed).
- [x] Results/Discussion working draft, Xente candidate and IEEE pilot clearly labeled.
- [ ] Canonical IEEE 12×5 mirror reproducibility gate.
- [ ] IEEE full 12×N seed convergence and sensitivity.
- [ ] Cross-scenario final effect tables, figures and policy comparisons.
- [ ] Completed ODD/Parameter Registry checked against **latest** code.
- [ ] Full thesis editing, references, equations/figure consistency, final conclusion without overclaims.
- [ ] GVHD review, defense preparation and approved submission version.
- [ ] Merge draft PR only after user review and appropriate checks.

**Stop rule:** No claim of completed final results until the corresponding row has an artifact/run manifest and a checkable acceptance outcome. No corporate Green SM evidence without explicit organizational authorization.
