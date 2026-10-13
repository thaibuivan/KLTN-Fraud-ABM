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

Current working operational baseline:
- validation review target = 1%;
- frozen Xente review threshold ≈ 0.014801;
- Low / Medium / High capacity = 0.75 / 1.00 / 1.25 × validation reference workload;
- risk-priority = baseline queue discipline;
- FIFO = structural robustness.

Still not final:
- direct BLOCK threshold;
- unresolved-review fraud-loss semantics;
- final capacity-aware congestion parameters.

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
- Capacity-aware reduced alert volume/backlog/waiting in the pilot, with a small fraud-interception trade-off at the lowest capacity.

Do not repeat this pilot unless engine semantics change.

## 8. Adaptive fraudster — FIRST CLOSED-LOOP XENTE PILOT DONE

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
- this is **not final thesis evidence**;
- current generator samples empirical score/value templates;
- reward/congestion parameters are assumption-dependent;
- Xente Value separation is unusually strong.

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
1. freeze block/review/outcome semantics;
2. improve fraud generator beyond score/value-template replay, preferably feature-level amount perturbation with risk rescoring;
3. sensitivity-test learning rate / epsilon;
4. sensitivity-test capacity-aware congestion thresholds/increments;
5. confirm final Static comparator definition;
6. run full current test suite;
7. freeze Xente mechanism;
8. run 12 Xente core configurations;
9. seed convergence;
10. final Xente tables/figures.

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

**No more EDA and no more queue-only pilots.**

Next technical task:
> Upgrade the Xente fraud generator from score/value-template replay to a feature-level counterfactual mechanism (starting with empirically grounded amount regimes), rescore through the existing risk model, then sensitivity-test the adaptive and capacity-aware parameters before freezing the 12-config Xente experiment.
