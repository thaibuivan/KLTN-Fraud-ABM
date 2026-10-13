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

## 8. Adaptive fraudster — FEATURE-LEVEL CLOSED LOOP DONE ON XENTE

Exists:
- Adaptive Fraudster Design v0.1
- adaptive_fraudster.py
- StaticFraudster / StaticMixtureFraudster
- XenteOnlineFeatureBuilder
- XenteFeatureLevelFraudGenerator
- FastXenteLogisticScorer
- PolicyQueueEngine
- run_xente_feature_level_static_adaptive.py

Historical integration notes:
- [[Xente Static-Adaptive Integration Pilot v0.1]]
- [[Xente Feature-Level Adaptive Smoke v0.1]]

Current mechanism:

```text
validation fraud regime
→ Static / Adaptive strategy
→ raw Xente-compatible fraud event
→ online past-only fraudster history
→ risk-model rescoring
→ Fixed / Capacity-aware
→ persistent FIFO queue
→ APPROVE / REVIEW / BLOCK
→ normalized reward
→ next strategy
```

Important upgrade:
- generated fraud no longer inherits a historical risk score;
- generated fraud is rescored from its generated raw context + synthetic past-only history;
- reward is normalized by scenario-level fraud value scale;
- dormancy is off in the core model so fraud-attempt count remains comparable.

## 9. Xente final scenario — MAIN CORE RUN + SENSITIVITY + DEGRADED-SCORE ROBUSTNESS DONE

Completed:
- EDA / Data-to-ABM;
- risk baseline + temporal checks;
- queue/capacity groundwork;
- empirical Fixed vs Capacity-aware replay;
- feature-level Static vs Adaptive closed loop;
- BLOCK / alpha / epsilon / congestion sensitivity;
- 50-seed, 12-configuration main Xente core run;
- 30-seed degraded-score feature-level robustness;
- Monte Carlo convergence analysis;
- operational/adaptive parameter freeze;
- current CI test suite passing.

Key result files:
- [[Xente Feature-Level Core Run v0.2]]
- [[Xente Feature-Level Sensitivity v0.1]]
- [[Xente Feature-Level Degraded-Score Robustness v0.1]]
- [[Operational Core Freeze v1.0]]

Current frozen central Xente settings:
- base review rate = 1.00% validation tail;
- Capacity-aware review tiers = 1.00% / 0.75% / 0.50%;
- BLOCK = top 0.10% validation tail;
- Low / Medium / High capacity = 0.75 / 1.00 / 1.25 × validation reference load;
- FIFO = core queue;
- risk-priority = structural robustness;
- alpha = 0.15;
- epsilon = 0.10;
- congestion triggers = 24 / 72 backlog-hours;
- dormancy = off;
- reward scale = validation-fraud median Value.

50-seed convergence:
- fraud-intercept relative MCSE <= about 1.6%;
- backlog <= about 1.1%;
- legitimate intervention <= about 0.3%;
- value exposure remains noisier, up to about 7.3%, so report intervals.

Current Xente interpretation:
- adaptive behavior strongly changes strategy composition;
- analyst capacity consistently matters;
- Capacity-aware robustly reduces backlog / intervention under scarcity;
- the fraud-control effect of Capacity-aware is conditional and changes with score quality;
- count-based and value-based fraud outcomes can move in opposite directions.

Still needed for Xente before final thesis submission:
1. final publication-quality tables / figures;
2. optional extreme-condition/adaptive integration tests if needed for appendix;
3. final parameter-registry snapshot;
4. incorporate results into Methods / Results / Discussion.

**Do not rerun the main Xente design unless code semantics or frozen parameters change.**

## 10. IEEE-CIS final scenario — NEXT MAJOR IMPLEMENTATION BLOCK

Already done:
- full EDA;
- Data-to-ABM mapping;
- entity-proxy analysis;
- two-scenario role;
- common canonical adapter;
- shared policy/queue architecture.

Still needed:
1. build executable chronological IEEE feature pipeline from the completed EDA;
2. freeze entity proxy used for persistent state;
3. train/validate IEEE scenario-specific risk model;
4. generate validation/test risk_probability outputs;
5. run Fixed vs Capacity-aware empirical replay;
6. build IEEE feature-level fraud strategy generator;
7. reuse Static / Adaptive learning mechanism with IEEE-normalized reward scale;
8. run 12 IEEE core configurations;
9. seed convergence + targeted sensitivity;
10. final IEEE tables/figures.

## 11. Cross-scenario design — DESIGN DONE, RESULTS WAITING FOR IEEE

Design exists:
- Shared Two-Scenario Architecture v1.0
- Final Core Experiment Grid v1.0
- Cross-Scenario Comparison Plan v1.0

After IEEE is complete, compare:
- adaptation penalty;
- Capacity-aware policy gain;
- policy ranking;
- congestion sensitivity;
- count/value trade-offs.

Classify each conclusion:
- consistent;
- environment-dependent;
- uncertain.

## 12. Validation — CURRENT CODE TEST SUITE PASSING

Done:
- validation framework designed;
- Xente temporal robustness;
- Xente score structural sensitivity;
- queue verification;
- policy tests;
- integrated policy-system tests;
- scenario-adapter tests;
- online-feature equivalence test;
- fast-scorer equivalence tests;
- adaptive/static/template tests;
- degraded model fast-scorer tests;
- GitHub Actions CI configured.

Latest verified CI result:
- **37 tests passed** before the later degraded-scorer test additions;
- subsequent CI runs after the scorer/model-variant changes are also succeeding.

Still needed by final thesis:
- explicit cross-scenario validation summary;
- final extreme-condition test summary if included in appendix;
- final seed-convergence report for IEEE.

## 13. Literature / parameter grounding — PARTIAL but sufficient for implementation

Existing notes:
- AML-CFSim 2025;
- McCulloch 2022;
- Alves et al. 2025;
- Höppner et al. 2022;
- real-bank AML alert scoring 2025;
- Operational Parameter Grounding v0.1;
- Parameter Registry v0.2.

Before final writing:
- update Parameter Registry with the actual frozen values/ranges used;
- distinguish empirical / policy / operational / behavioral assumptions;
- attach final citations to the parameters discussed in text.

## 14. Writing — OUTLINE DONE, FINAL PROSE NOT DONE

Already exists:
- Research Design v1.1;
- Methodology Skeleton v1.0;
- Results and Discussion Outline v1.0;
- GVHD brief materials.

Still needed:
- Introduction;
- Literature Review;
- Data;
- full Methodology;
- Xente Results;
- IEEE Results;
- Cross-scenario Discussion;
- Limitations;
- Conclusion;
- appendices;
- references.

Xente result prose can now be drafted, but final thesis Results should wait until IEEE is also completed so the cross-scenario narrative stays coherent.

## 15. Things explicitly NOT to redo

1. Do not redo Xente EDA.
2. Do not redo IEEE-CIS EDA.
3. Do not re-decide whether Xente + IEEE are core: both are core.
4. Do not redesign the conceptual model again.
5. Do not rebuild Xente customer-history features from scratch.
6. Do not rerun FIFO vs risk-priority just to prove queue priority matters.
7. Do not rerun the old score/value-template adaptive pilot.
8. Do not rerun Xente main 12 configurations unless semantics/parameters change.
9. Do not add Deep RL to the core.
10. Do not add more policy families before the two core scenarios are complete.
11. Do not merge Xente and IEEE.

## 16. Critical path from NOW

```text
A. Build executable IEEE-CIS chronological feature/state pipeline
        ↓
B. Train + validate IEEE risk model
        ↓
C. Run IEEE empirical policy replay
        ↓
D. Build IEEE feature-level Static / Adaptive closed loop
        ↓
E. Run 12 IEEE configurations + convergence/sensitivity
        ↓
F. Cross-scenario comparison with Xente
        ↓
G. Final parameter registry + validation appendix
        ↓
H. Write final KLTN
```

## 17. Immediate next task

**Do not do more Xente redesign.**

Next technical task:

> Convert the completed IEEE-CIS EDA/Data-to-ABM decisions into an executable chronological feature pipeline, freeze the persistent entity proxy, and train the first IEEE scenario-specific risk baseline that outputs validation/test risk probabilities for the shared policy engine.
