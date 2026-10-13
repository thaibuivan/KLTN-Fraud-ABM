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

Important result:
- Xente Value is a dominant signal;
- classifier novelty is not thesis contribution;
- policy results must be checked under degraded score quality.

**Do not rebuild a new Xente baseline unless needed for reproducibility or an explicit robustness test.**

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
Rerun only if:
- producing final reproducible appendix;
- changing shared engine semantics;
- running a predefined robustness check.

## 6. Shared policy layer — CODE DONE, empirical verification PENDING

Exists:
- fraud_policies.py
- test_fraud_policies.py

Implemented:
- FixedThresholdPolicy;
- CapacityAwarePolicy;
- CostSensitivePolicy extension;
- APPROVE / REVIEW / BLOCK interface.

Status:
- code exists;
- do not redesign policy API again;
- still need to run/verify against empirical score streams and freeze final parameterization.

## 7. Integrated policy + queue engine — CODE DONE, empirical run PENDING

Exists:
- simulate_policy_system.py
- test_policy_system.py
- run_xente_policy_replay.py
- run_ieee_policy_replay.py
- scenario_adapters.py
- test_scenario_adapters.py

Status:
- common event schema exists;
- Xente/IEEE adapter logic exists;
- Fixed vs Capacity-aware replay runners exist;
- these new components have **not yet been documented as empirically executed end-to-end** on current raw/score artifacts.

Next action:
- materialize existing Library data;
- regenerate scores if needed;
- run integrated replay;
- verify outputs;
- freeze common semantics.

## 8. Adaptive fraudster — DESIGN + PROTOTYPE DONE, FULL INTEGRATION NOT DONE

Exists:
- Adaptive Fraudster Design v0.1
- adaptive_fraudster.py
- run_adaptive_vs_static.py
- test_adaptive_fraudster.py

Prototype supports:
- strategy state;
- epsilon-greedy choice;
- value update;
- block-triggered dormancy;
- Static comparator.

Important:
- current runner is synthetic smoke test;
- not an empirical thesis result.

Still needed:
```text
strategy
→ scenario-specific fraud transaction
→ risk model
→ real policy response
→ queue/analyst outcome
→ reward
→ strategy update
```

## 9. Xente final scenario — PARTIAL

Already done:
- EDA;
- Data-to-ABM;
- risk model;
- queue/capacity groundwork;
- policy/queue shared code.

Still needed:
1. run integrated Fixed vs Capacity-aware replay;
2. freeze Low/Medium/High normalized capacity;
3. freeze block/review semantics;
4. build Xente-grounded fraud generator;
5. integrate Static fraudster;
6. integrate Adaptive fraudster;
7. run 12 core configurations;
8. seed convergence;
9. alpha/epsilon sensitivity;
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
- scenario-adapter tests written.

PENDING:
- run current full test suite;
- adaptive full-loop tests;
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

Already established:
- empirical vs literature-informed vs policy vs behavioral-assumption parameters.

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

Do not write final Results before final simulations are run.

## 15. Things explicitly NOT to redo

1. Do not redo Xente EDA.
2. Do not redo IEEE-CIS EDA.
3. Do not re-decide whether Xente + IEEE are core: they are both core.
4. Do not redesign the whole conceptual model again.
5. Do not rebuild Xente customer-history features from scratch.
6. Do not rerun FIFO vs risk-priority just to prove queue priority matters again.
7. Do not search for a new main dataset unless supervisor changes scope.
8. Do not add Deep RL unless the current heuristic adaptation is demonstrably insufficient.
9. Do not add more policy families before Fixed + Capacity-aware are completed.
10. Do not merge Xente and IEEE into one dataset.

## 16. Critical path from NOW

```text
A. EXECUTE shared policy engine on existing Xente artifacts
        ↓
B. Freeze operational semantics/capacity normalization
        ↓
C. Build full Static → Adaptive Xente loop
        ↓
D. Run 12 Xente configurations
        ↓
E. Convert IEEE EDA into executable feature/risk pipeline
        ↓
F. Run same Static → Adaptive architecture on IEEE
        ↓
G. Run 12 IEEE configurations
        ↓
H. Cross-scenario comparison
        ↓
I. Sensitivity + convergence + final validation
        ↓
J. Write final thesis
```

## 17. Immediate next task

**Do not do more EDA.**

Next technical task:
> Materialize existing Xente raw data from Library, reproduce/obtain risk scores, then execute and verify the new integrated Fixed vs Capacity-aware policy replay using the shared policy/queue engine.

After that, freeze the shared interface before building the adaptive full loop.
