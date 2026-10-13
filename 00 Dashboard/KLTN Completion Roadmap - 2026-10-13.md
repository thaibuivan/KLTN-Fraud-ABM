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

### Data / EDA
- [x] Xente raw data available
- [x] Xente full EDA + Data → ABM
- [x] IEEE-CIS raw data available
- [x] IEEE-CIS full EDA + Data → ABM
- [x] two-scenario complementarity frozen

### Xente empirical groundwork
- [x] leakage-safe customer-history features
- [x] chronological logistic baseline
- [x] baseline reproduced from Library raw data
- [x] temporal robustness
- [x] degraded score models
- [x] persistent queue
- [x] FIFO vs risk-priority
- [x] threshold/load sensitivity
- [x] stochastic service
- [x] variable team capacity
- [x] starvation/tail waiting

### Shared model / Xente integration
- [x] Fixed policy code
- [x] Capacity-aware policy code
- [x] Cost-sensitive extension code
- [x] integrated policy + queue engine
- [x] empirical Fixed vs Capacity-aware Xente replay
- [x] Low/Medium/High capacity normalized to validation workload
- [x] adaptive fraudster prototype
- [x] StaticMixture comparator
- [x] Xente validation-based fraud-template generator
- [x] shared adaptive-policy simulation engine
- [x] first 30-seed Static vs Adaptive Xente closed-loop pilot

## Still required

### Xente final mechanism
- [x] feature-level counterfactual fraud generator from validation fraud regimes
- [x] online past-only feature builder for generated fraud
- [x] rescore generated fraud through saved Xente logistic model
- [x] scenario-normalized fraudster reward scale added
- [x] FIFO core / risk-priority robustness frozen
- [x] tiered Capacity-aware policy semantics frozen
- [x] unresolved-review exposure semantics defined
- [x] 1-seed / 12-config feature-level smoke run completed
- [ ] freeze BLOCK calibration after sensitivity
- [ ] learning-rate sensitivity
- [ ] epsilon sensitivity
- [ ] capacity-aware congestion-trigger sensitivity
- [ ] degraded-score sensitivity on the new closed loop
- [ ] run latest full test suite
- [ ] freeze final Xente mechanism

### Xente final results
- [ ] 12 core Xente configurations
- [ ] convergence / Monte Carlo error
- [ ] robustness pack on frozen model
- [ ] final Xente tables/figures

### IEEE final
- [ ] executable chronological feature pipeline
- [ ] freeze entity proxy
- [ ] scenario-specific risk model
- [ ] empirical policy replay
- [ ] IEEE-grounded fraud generator / strategy mapping
- [ ] Static full loop
- [ ] Adaptive full loop
- [ ] 12 core configs
- [ ] convergence/sensitivity
- [ ] final IEEE tables/figures

### Cross-scenario
- [ ] adaptation penalty
- [ ] capacity-aware gain
- [ ] policy ranking
- [ ] consistent vs environment-dependent conclusions
- [ ] final cross-scenario figures

### Final validation
- [ ] adaptive integration tests
- [ ] extreme-condition tests
- [ ] final parameter registry
- [ ] seed convergence report
- [ ] cross-scenario validation summary

### Writing
- [ ] Introduction
- [ ] Literature Review
- [ ] Data
- [ ] full Methodology
- [ ] Results
- [ ] Discussion
- [ ] Limitations
- [ ] Conclusion
- [ ] Appendices / References

## Immediate next task

1. run a structured feature-level sensitivity pilot for BLOCK rate, alpha, epsilon and congestion triggers;
2. run/verify the latest test suite and add missing adaptive integration tests;
3. freeze the Xente closed-loop parameters;
4. run the 12 final Xente configurations with convergence-based seeds;
5. then move to the executable IEEE-CIS feature/risk pipeline.
