# KLTN Completion Roadmap — 2026-10-13

> Detailed source of truth: [[MASTER STATUS - 2026-10-13]]

## Core thesis

```text
Xente + IEEE-CIS
× Static / Adaptive
× Fixed / Capacity-aware
× Low / Medium / High analyst capacity
= 24 core configurations
```

## Completed

### Shared design
- [x] Proposal → KLTN continuity
- [x] two-scenario architecture
- [x] Fixed / Capacity-aware policy interface
- [x] persistent queue / analyst engine
- [x] normalized capacity semantics
- [x] normalized adaptive-reward semantics
- [x] 24-config final experiment design
- [x] validation framework
- [x] GitHub CI

### Xente data / empirical groundwork
- [x] raw data available
- [x] EDA + Data → ABM
- [x] leakage-safe customer history
- [x] chronological logistic baseline
- [x] temporal robustness
- [x] full / degraded / amount-only score checks
- [x] queue / capacity / priority groundwork

### Xente final closed loop
- [x] feature-level fraud generator
- [x] online past-only synthetic fraudster state
- [x] generated-fraud risk rescoring
- [x] StaticMixture comparator
- [x] Adaptive epsilon-greedy mechanism
- [x] normalized reward scale
- [x] BLOCK / alpha / epsilon / congestion sensitivity
- [x] frozen central Xente parameters
- [x] 50-seed × 12-config main Xente core run
- [x] convergence analysis
- [x] degraded-score feature-level robustness
- [x] current test suite passing

## Current work — IEEE-CIS

### IEEE executable data/risk layer
- [x] materialize raw IEEE transaction/identity data from existing Library zip
- [x] implement chronological split
- [x] freeze entity proxy from prior EDA: card1 + addr1
- [x] build leakage-safe entity/history features
- [x] build missingness/context features
- [x] train scalable streaming baseline risk model
- [x] validate PR-AUC / ROC-AUC / calibration / forward drift
- [x] save validation/test risk scores + model bundle
- [x] canonical adapter interface already available

### IEEE policy / adaptive layer
- [x] Fixed vs Capacity-aware empirical replay
- [ ] IEEE feature-level fraud strategy mapping
- [ ] Static comparator
- [ ] Adaptive closed loop
- [ ] 12 IEEE core configs
- [ ] convergence / sensitivity
- [ ] final IEEE figures/tables

## Cross-scenario
- [ ] adaptation penalty Xente vs IEEE
- [ ] Capacity-aware gain Xente vs IEEE
- [ ] policy ranking comparison
- [ ] capacity interaction comparison
- [ ] consistent / environment-dependent / uncertain classification
- [ ] cross-scenario figures

## Final validation / documentation
- [ ] final Parameter Registry snapshot
- [ ] final cross-scenario validation summary
- [ ] final experiment configuration appendix
- [ ] final convergence appendix

## Writing
- [ ] Introduction
- [ ] Literature Review
- [ ] Data
- [ ] Methodology
- [ ] Xente Results
- [ ] IEEE Results
- [ ] Cross-scenario Discussion
- [ ] Limitations
- [ ] Conclusion
- [ ] Appendices / References

## Immediate next task

1. build IEEE feature-level fraud strategy mapping from interpretable fields;
2. rescore generated fraud through the frozen IEEE baseline;
3. connect StaticMixture / Adaptive fraudster to the shared policy + FIFO queue engine;
4. run the first IEEE closed-loop pilot;
5. then freeze parameters and run the 12 IEEE core configurations.
