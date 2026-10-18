# KLTN research implementation checkpoint — 2026-10-18

> Supplements the older `MASTER STATUS - 2026-10-13.md`. This is a **code/preparation milestone**, NOT a completed IEEE-CIS adaptive experiment. No Green SM internal evidence was used.

## 1. Thesis protocol: unchanged

**Working title:** Agent-Based Stress Testing of Transaction Fraud-Management Policies under Adaptive Fraudster Behavior and Analyst Capacity Constraints.

Core experiment stays: Xente / IEEE-CIS × Static / Adaptive × Fixed-threshold / Capacity-aware × Low / Medium / High normalized analyst capacity = **24 configurations**.

Xente has a candidate main closed-loop 12-config × 50-seed run, degraded-score and targeted sensitivity. IEEE-CIS has a trained baseline and 6 pre-adaptation policy replays. The IEEE adaptive full experiment **remains pending**.

## 2. IEEE-CIS empirical donor audit (directly read from public original Kaggle training zip)

Labeled training rows: 590,540. Chronological split 70% / 15% / 15%.

- Validation: 88,581 rows, including 3,042 fraud.
- Test: 88,581 rows, including 3,083 fraud.
- Validation-fraud TransactionAmt empirical tercile boundaries: **50.0** and **117.0**.
- Validation-fraud median TransactionAmt: **77.0**, candidate scenario-specific normalization scale.
- Generator donor pool sizes: low = **1,052**, middle = **1,030**, high = **960**.
- ProductCD among validation fraud: W ≈ 48.82%, C ≈ 37.80%, remaining products ≈ 13.38%.
- Card1+addr1 combinations among validation fraud: 810 distinct pairs. These are **entity proxies**, not true customers.

This is distributional support for a **bounded amount-regime stress mechanism**. It does not identify strategic choice, opponent learning, or real-world behavior of fraudsters.

## 3. Code added in this checkpoint

- `scripts/ieee_feature_level_fraud.py`: resample full coherent validation-fraud rows by three empirical amount regimes, preserving matched product/card/device/identity and masked C/D/M/V detector context. Synthetic transaction ID and relative event time are replaced. Never sample test fraud as a donor.
- `scripts/ieee_online_scorer.py`: exact per-event feature construction via the **existing** IEEE baseline `build_chunk_features` and `make_matrix`, with past-only entity history and frozen model bundle. Supports warming history before the test period.
- `scripts/prepare_ieee_closed_loop.py`: local-only streaming extraction of pre-test history, validation fraud donors, and held-out test contexts using chronological 70/15/15 source order. Do not commit prepared raw CSVs.
- `scripts/outcome_semantics.py`: hypothetical outcome-accounting sensitivity where review is eligible for prevention only on **service completion** before the horizon and a review success probability is explicitly assumed; unresolved review is exposure at horizon, **not realized bank loss**.
- Dedicated `tests/` for each new component.

Unit tests and CI test software behavior; they **do not validate** empirical realism, the fraudster learning rule, or counterfactual outcome semantics.

## 4. Research boundaries to retain

1. The generator's amount terciles are an **explicit model abstraction**, not a claim that fraudsters naturally have exactly three strategies.
2. Fraud donor sampling resamples coherent observed contexts; masked fields are never interpreted as deliberate fraudster actions.
3. Since test-event histories change under synthetic fraud, **re-score both legitimate and fraud test events chronologically** in a proper full closed loop; don't mix counterfactual fraud scores with incompatible frozen legitimate scores without describing that approximation.
4. The original scorer's past-only warmup must include train and validation events (without learning from post-test labels); then replay the counterfactual test stream.
5. Immediate `REVIEW` feedback to fraudster is an **observability assumption**; analyze instant vs delayed/no-feedback variants before interpreting learning as behavioral realism.
6. The old main intercept metric counts **service start** as interception. It must not be called actual loss prevention; report direct blocking separately and conduct a review-completion / effectiveness sensitivity.
7. Parameter alpha/epsilon, review recovery rate, and analyst service assumptions remain assumptions, not empirically calibrated quantities.

## 5. Next hard gates (not yet complete)

- [ ] Produce local context CSVs using `prepare_ieee_closed_loop.py`; check split identity and missingness.
- [ ] Obtain/reproduce the saved `model_bundle.joblib` and validation/test scores **locally**, never add raw transactions or model secrets to public GitHub.
- [ ] Compare unchanged original IEEE test probabilities from online replay with the canonical saved baseline predictions; investigate differences before adaptation.
- [ ] Integrate `IEEEFeatureLevelFraudGenerator`, `IEEEOnlineRiskScorer`, StaticMixture/AdaptiveFraudster, shared policy and persistent queue in an executable **small closed-loop pilot**.
- [ ] Confirm deterministic replay at same seed and matched fraud-attempt slots across policies.
- [ ] Complete IEEE 12 core configurations with replication/convergence, plus adaptive and outcome-semantics robustness.
- [ ] Generate cross-scenario comparative tables with paired differences, confidence intervals, sensitivity and caveats.
- [ ] Finalize ODD, Parameter Registry, peer/GVHD review and full thesis chapters.
- [ ] Leave draft PR unmerged pending review.

## 6. Local preparation command

```bash
python -m scripts.prepare_ieee_closed_loop \
  --zip /private/local/ieee-fraud-detection.zip \
  --output-dir outputs/local/ieee_closed_loop
```

**Do not interpret the existence of this command as having run the full IEEE adaptive ABM.**

## 7. Green SM information handling

No internal Green SM document or fact was read, uploaded, committed or cited in this milestone. Follow the user's pending authorization check with management before any external academic use; public data and peer-reviewed literature remain sufficient to continue the thesis.


---

## Addendum — 18 Oct, later execution checkpoint (supersedes older pending flags above)

**New actual empirical progress:**
- IEEE canonical streaming-SGD baseline independently reproduced from original raw archive, matching reported validation/test PR-AUC and ROC-AUC to displayed precision. Artifacts remained private in working environment.
- Prepared all IEEE test contexts from original labeled training archive; history 501,959, validation donors 3,042, test 88,581 (3,083 fraud attempt slots).
- Audited fast per-event IEEE scorer against frozen baseline probabilities for ALL 88,581 unchanged test events: maximum absolute difference **4.314e-7**, below **1e-6** threshold.
- Built repo IEEE Static/Adaptive closed-loop runner, reward ablation controls, score equivalence audit, summarization utility, tests, and full Vietnamese Methodology Draft v1.1.
- Local empirical **full-test 12 configurations × 5 seeds** pilot run (60 cells), documented in **05 Experiments/IEEE-CIS Adaptive Full-Test Pilot v0.2.md**. This is PRELIMINARY and locally mirrored to repo logic: canonical repo runner cross-check is still pending.
- Reward/value ablation and REVIEW observability ablation executed for one full-test seed as exploratory sensitivity.
- **60 unit/integration tests passed** on GitHub Actions at latest verified head before the pilot note commit. New documentation commit may trigger CI again.

**Current critical path:** (1) canonical runner replay with saved bundle and compared outputs; (2) expand seed count and convergence/sensitivity for IEEE; (3) Xente–IEEE paired/normalized cross-scenario comparison; (4) final literature/parameter provenance and academic writing; (5) GVHD approval; (6) merge draft PR when reviewed.

**Do not** label IEEE main experiment fully completed or the thesis finished yet.
