# MASTER STATUS — KLTN Fraud ABM — 2026-10-13

> Đây là **source of truth về tiến độ** để tránh làm lại việc đã làm.
> Khi một file cũ mâu thuẫn với file này, ưu tiên file này + Research Design v1.1 + Shared Two-Scenario Architecture v1.0.

## 1. Framing khóa luận — DONE

Đề tài phát triển trực tiếp từ FinRisk proposal.

Main idea:
- không tối ưu classifier đơn thuần;
- dùng dynamic simulation / ABM để stress-test fraud-management policy;
- có persistent analyst queue;
- có Static vs Adaptive fraudster;
- kiểm tra robustness trên **hai empirical scenarios core**:
  - Xente;
  - IEEE-CIS.

Main experiment:
```text
2 datasets
× 2 fraudster modes
× 2 policies
× 3 capacity levels
= 24 core configurations
```

Core policies:
- Fixed-threshold;
- Capacity-aware.

Cost-sensitive:
- extension nếu cost grounding đủ defensible.

## 2. Data availability — DONE

### Xente raw data — AVAILABLE IN LIBRARY
- training.csv
- test.csv
- Xente_Variable_Definitions.csv
- Xente competition zip
- 01_EDA_Xente.ipynb

### IEEE-CIS raw data — AVAILABLE IN LIBRARY
- ieee-fraud-detection.zip
- train_identity.csv
- test_identity.csv
- 02_EDA_IEEE_CIS.ipynb

### Shared data-design artifacts — AVAILABLE
- Parameter_Registry_and_Data_to_ABM_v0.1.xlsx
- Data_to_ABM_Mapping_Xente_IEEE_v0.1.csv

Do **not** ask the user to re-upload these unless materialization actually fails.

## 3. EDA / Data-to-ABM — DONE

### Xente — DONE
Đã phân tích trực tiếp:
- schema / data quality;
- fraud imbalance;
- Value/Amount;
- product/provider/channel;
- chronology;
- CustomerId repetition;
- AccountId/SubscriptionId caveat;
- cold-start;
- train-test drift;
- Data → ABM mapping.

Verified key facts:
- train 95,662 rows;
- 193 fraud;
- 3,742 CustomerIds;
- true timestamp;
- strong Value signal;
- many later frauds are cold-start.

**Do not redo Xente EDA from scratch.**

### IEEE-CIS — DONE
Notebook đã phân tích full raw dataset:
- 590,540 train transactions;
- 20,663 fraud (3.499%);
- 182-day train span;
- transaction + identity structure;
- amount/product/card/address/email;
- C/D/M/V missingness and separation;
- identity coverage;
- device/identity drift;
- repeated card/entity proxies;
- cold-start;
- temporal structure;
- Data → ABM mapping;
- Xente vs IEEE complementarity.

Key modeling boundary:
- no true CustomerId;
- card1 / card1+addr1 are entity proxies;
- masked V/C/D/M features may feed detector but should not be interpreted as explicit fraudster actions.

**Do not redo IEEE EDA from scratch.**

## 4. Xente empirical risk pipeline — DONE

Code:
- profile_xente.py
- build_xente_features.py
- train_xente_baseline.py
- run_xente_temporal_robustness.py
- run_xente_model_robustness.py

Completed:
- chronological 70/15/15 split;
- leakage-safe customer-history features;
- regularized logistic baseline;
- validation/test score analysis;
- seen vs unseen customer checks;
- temporal expanding-window checks;
- full / no-current-value / amount-only robustness.

Baseline was reproduced again on 2026-10-13 from Library raw data:
- validation PR-AUC = 0.560851;
- test PR-AUC = 0.892521.

This matches the earlier stored baseline.

Important result:
- Xente Value is a dominant signal;
- classifier novelty is not thesis contribution;
- policy results must be checked under degraded score quality.

**Do not rebuild a new Xente baseline unless needed for reproducibility or a defined robustness test.**

## 5. Xente queue / capacity experiments — DONE as preliminary groundwork

Code/docs already exist for:
- persistent queue;
- FIFO vs risk-priority;
- relative/fixed capacity;
- threshold/load sensitivity;
- stochastic service time;
- variable team capacity;
- starvation/tail waiting metrics.

Preliminary findings already established:
- capacity scarcity creates backlog/delay;
- queue discipline changes who gets scarce service;
- risk-priority tends to increase fraud review within finite horizon;
- tail waiting/starvation can worsen;
- qualitative effect survives degraded score and stochastic service.

These are **pilot/groundwork results**, not final adaptive-ABM results.

**Do not rerun these experiments merely to rediscover the same qualitative point.**

## 6. Shared policy layer — CODE DONE + XENTE EMPIRICAL PILOT DONE

Exists:
- fraud_policies.py
- test_fraud_policies.py

Implemented:
- FixedThresholdPolicy;
- CapacityAwarePolicy;
- CostSensitivePolicy extension;
- APPROVE / REVIEW / BLOCK interface.

Executed on reproduced Xente score stream:
- [[Xente Integrated Policy Replay v0.1]]

Current working operational baseline after the normalized replay:
- validation base review target = 1.00%;
- Capacity-aware tiers = 1.00% / 0.75% / 0.50% validation review-rate thresholds;
- frozen Xente thresholds ≈ 0.014801 / 0.026892 / 0.050961;
- Low / Medium / High capacity = 0.75 / 1.00 / 1.25 × validation base-review workload;
- **FIFO = core queue discipline** to isolate routing-policy effects;
- risk-priority = structural robustness;
- congestion state = backlog-hours.

Operational semantics now frozen in:
- [[Operational Core Freeze v1.0]]

Still not final:
- direct BLOCK threshold for the adaptive full loop;
- sensitivity range for congestion triggers;
- analyst-error extension.

## 7. Integrated policy + queue engine — EMPIRICALLY VERIFIED ON XENTE

Exists:
- simulate_policy_system.py
- test_policy_system.py
- run_xente_policy_replay.py
- run_ieee_policy_replay.py
- scenario_adapters.py
- test_scenario_adapters.py

Xente replay milestone:
- Fixed and Capacity-aware ran on the same empirical score stream;
- policy observed current queue state;
- capacity reference remained frozen;
- policy semantics were upgraded from arbitrary raw-score increments to validation-rate-calibrated tiers;
- FIFO was frozen as the core queue baseline;
- Capacity-aware reduced review demand/backlog under scarce capacity and its advantage diminished at high capacity.

Do not repeat this pilot unless engine semantics change.

## 8. Adaptive fraudster — FIRST CLOSED-LOOP PILOT DONE + FEATURE-LEVEL UPGRADE IN PROGRESS

Exists:
- Adaptive Fraudster Design v0.1
- adaptive_fraudster.py
- StaticFraudster
- StaticMixtureFraudster
- xente_fraud_templates.py
- simulate_adaptive_policy_system.py
- run_xente_static_vs_adaptive_policy.py
- tests for adaptive/static/template mechanisms

Closed-loop pilot:
- [[Xente Static-Adaptive Integration Pilot v0.1]]

Pilot mechanism:
```text
validation fraud template regime
→ Static / Adaptive strategy choice
→ score/value
→ Fixed / Capacity-aware
→ queue
→ response
→ reward
→ next strategy
```

Observed pilot behavior:
- adaptive strategy shifted strongly toward the lower-value/lower-score regime;
- static replay and adaptive replay produced materially different policy outcomes;
- naive congestion-driven threshold raising could create an evasion channel in this pilot.

Important:
- the historical pilot is **not final thesis evidence**;
- the old generator sampled empirical score/value templates and is now treated as a historical integration check;
- reward/congestion parameters are assumption-dependent;
- Xente Value separation is unusually strong.

New refinement already implemented:
- adaptive reward now supports scenario-normalized `reward_scale`;
- `XenteOnlineFeatureBuilder` reproduces the batch past-only feature logic for generated fraud events;
- `XenteFeatureLevelFraudGenerator` resamples raw fraud context from validation fraud regimes;
- generated fraud is **rescored through the saved Xente risk model** instead of inheriting a historical risk score;
- `PolicyQueueEngine` provides a stateful queue/policy engine for adaptive simulation;
- `run_xente_feature_level_static_adaptive.py` runs the new feature-level closed loop.

Verification completed:
- online feature builder matched the batch builder on an empirical Xente subset;
- a 1-seed / 12-configuration smoke run completed successfully;
- the smoke run exposed an important count-vs-value trade-off: adaptation can reduce capture rate while also shifting toward lower-value fraud, so final reporting must include both count-based and value-based outcomes.

Not completed yet:
- multi-seed feature-level experiment;
- sensitivity/convergence;
- final BLOCK calibration.

## 9. Xente final scenario — PARTIAL, NOW IN MODEL-REFINEMENT PHASE

Already done:
- EDA;
- Data-to-ABM;
- risk model;
- queue/capacity groundwork;
- empirical Fixed vs Capacity-aware replay;
- first Static vs Adaptive closed-loop pilot;
- validation-based template generator;
- 30-seed integration pilot.

Still needed before final 12 Xente configs:
1. sensitivity-test / freeze BLOCK review-rate calibration;
2. run multi-seed feature-level Static vs Adaptive pilot;
3. sensitivity-test learning rate / epsilon;
4. sensitivity-test capacity-aware congestion triggers;
5. test at least one degraded-score specification on the frozen mechanism;
6. run full current test suite + adaptive integration tests;
7. freeze final Xente mechanism and parameter registry;
8. run 12 Xente core configurations with convergence-based seeds;
9. final Xente tables/figures.

## 10. IEEE-CIS final scenario — PARTIAL

Already done:
- full EDA;
- Data-to-ABM mapping;
- entity-proxy analysis;
- scenario role;
- common adapter code;
- policy replay runner skeleton.

Still needed:
1. turn notebook analysis into executable chronological feature pipeline;
2. freeze entity proxy definition;
3. train/validate IEEE scenario-specific risk model;
4. generate risk_probability outputs;
5. run integrated Fixed vs Capacity-aware replay;
6. define IEEE-grounded fraud strategy mapping;
7. integrate Static fraudster;
8. integrate Adaptive fraudster;
9. run 12 core configurations;
10. seed convergence/sensitivity;
11. final IEEE tables/figures.

## 11. Cross-scenario design — DESIGN DONE, RESULTS NOT RUN

Design exists:
- Shared Two-Scenario Architecture v1.0
- Final Core Experiment Grid v1.0
- Cross-Scenario Comparison Plan v1.0

Compare:
- adaptation penalty;
- capacity-aware policy gain;
- policy ranking;
- congestion sensitivity.

Still needed:
- execute 12 Xente + 12 IEEE;
- aggregate seed-level uncertainty;
- classify conclusions:
  - consistent;
  - environment-dependent;
  - uncertain.

## 12. Validation — PARTIAL

DONE:
- validation framework designed;
- Xente temporal robustness;
- Xente score structural sensitivity;
- queue unit tests documented as passed in earlier groundwork;
- policy tests written;
- integrated-system tests written;
- scenario-adapter tests written;
- static-mixture/template tests written.

PENDING:
- run the current full test suite from the latest branch;
- adaptive full-loop verification tests;
- extreme-condition tests;
- final seed convergence;
- cross-scenario validation summary.

## 13. Literature / parameter grounding — PARTIAL but sufficient to continue implementation

Existing notes:
- AML-CFSim 2025;
- McCulloch 2022;
- Alves et al. 2025;
- Höppner et al. 2022;
- real-bank AML alert scoring 2025;
- Operational Parameter Grounding v0.1;
- Parameter Registry v0.2.

Still needed before final writing:
- freeze exact ranges actually used;
- cite final sources for those ranges;
- record every final simulation parameter in a final registry snapshot.

## 14. Writing — OUTLINE DONE, thesis text NOT DONE

Already exists:
- Research Design v1.1;
- Methodology Skeleton v1.0;
- Results and Discussion Outline v1.0;
- GVHD brief materials.

Still needed:
- Introduction;
- Literature Review;
- Data section;
- full Methodology;
- Results;
- Discussion;
- Limitations;
- Conclusion;
- appendices;
- references.

Do not write final Results before final simulations are frozen.

## 15. Things explicitly NOT to redo

1. Do not redo Xente EDA.
2. Do not redo IEEE-CIS EDA.
3. Do not re-decide whether Xente + IEEE are core: they are both core.
4. Do not redesign the whole conceptual model again.
5. Do not rebuild Xente customer-history features from scratch.
6. Do not rerun FIFO vs risk-priority just to prove queue priority matters again.
7. Do not rerun the integrated Fixed vs Capacity-aware Xente pilot unless semantics change.
8. Do not search for a new main dataset unless supervisor changes scope.
9. Do not add Deep RL unless the current heuristic adaptation is demonstrably insufficient.
10. Do not add more policy families before Fixed + Capacity-aware are completed.
11. Do not merge Xente and IEEE into one dataset.

## 16. Critical path from NOW

```text
A. Refine/freeze Xente closed-loop mechanism
        ↓
B. Run sensitivity on adaptation + capacity-aware parameters
        ↓
C. Run 12 final Xente configurations
        ↓
D. Convert IEEE EDA into executable feature/risk pipeline
        ↓
E. Run same Static → Adaptive architecture on IEEE
        ↓
F. Run 12 IEEE configurations
        ↓
G. Cross-scenario comparison
        ↓
H. Final validation + convergence
        ↓
I. Write final thesis
```

## 17. Immediate next task

**No more EDA and no more score/value-template redesign.**

The feature-level counterfactual + rescoring path now exists and passed a smoke check.

Next technical task:
> Run a small, structured sensitivity pack on the feature-level Xente closed loop (BLOCK calibration, alpha, epsilon, congestion triggers), verify the latest test suite, then freeze the Xente mechanism and execute the final 12 Xente configurations with enough seeds for convergence.
