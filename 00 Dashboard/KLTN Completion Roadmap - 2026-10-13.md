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
- [ ] materialize raw IEEE transaction/identity data from existing Library zip
- [ ] implement chronological split
- [ ] freeze entity proxy from prior EDA
- [ ] build leakage-safe entity/history features
- [ ] build missingness/context features
- [ ] train interpretable baseline risk model
- [ ] validate PR-AUC / ROC-AUC / calibration / temporal drift
- [ ] save validation/test risk scores + model
- [ ] canonical adapter verification

### IEEE policy / adaptive layer
- [ ] Fixed vs Capacity-aware empirical replay
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

1. use the existing IEEE-CIS raw data already in Library;
2. turn the completed IEEE EDA into an executable chronological feature/state builder;
3. train the first IEEE risk baseline and output validation/test risk scores;
4. feed those scores into the shared policy engine;
5. then build the IEEE Static/Adaptive closed loop.
