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

## Already completed

### Data / EDA
- [x] Xente raw data available in Library
- [x] Xente full EDA notebook
- [x] Xente Data → ABM mapping
- [x] IEEE-CIS raw zip / identity files available in Library
- [x] IEEE-CIS full EDA notebook
- [x] IEEE Data → ABM mapping
- [x] two-scenario complementarity established

### Xente empirical groundwork
- [x] leakage-safe customer-history features
- [x] chronological logistic baseline
- [x] temporal robustness
- [x] degraded score models
- [x] persistent queue
- [x] FIFO vs risk-priority
- [x] threshold/load sensitivity
- [x] stochastic service
- [x] variable team capacity
- [x] starvation/tail waiting analysis

### Shared model design/code
- [x] Research Design v1.1
- [x] Shared Two-Scenario Architecture
- [x] Parameter Registry
- [x] Validation Plan
- [x] Fixed policy code
- [x] Capacity-aware policy code
- [x] Cost-sensitive extension code
- [x] integrated policy + queue engine code
- [x] Xente policy replay runner
- [x] IEEE policy replay runner
- [x] Xente/IEEE scenario adapters
- [x] adaptive fraudster prototype
- [x] static comparator
- [x] experiment grid / cross-scenario plan

## Still required

### Shared engine
- [ ] execute current policy/queue tests end-to-end
- [ ] verify empirical policy replay on Xente
- [ ] freeze action/outcome semantics
- [ ] freeze normalized Low/Medium/High capacity definition
- [ ] integrate adaptive fraudster with shared engine
- [ ] shared seed/convergence runner
- [ ] shared result schema

### Xente final
- [ ] Xente-grounded fraud generator
- [ ] Static full loop
- [ ] Adaptive full loop
- [ ] 12 core configs
- [ ] convergence/sensitivity
- [ ] final figures/tables

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
- [ ] final figures/tables

### Cross-scenario
- [ ] run 24 configurations
- [ ] adaptation penalty
- [ ] capacity-aware gain
- [ ] policy ranking
- [ ] consistent vs environment-dependent conclusions

### Final validation
- [ ] current full test suite
- [ ] adaptive integration tests
- [ ] extreme-condition tests
- [ ] final parameter registry
- [ ] seed convergence report

### Writing
- [ ] Introduction
- [ ] Literature Review
- [ ] Data
- [ ] Methodology
- [ ] Results
- [ ] Discussion
- [ ] Limitations
- [ ] Conclusion
- [ ] Appendices / References

## Immediate next task

**No more EDA.**

1. materialize existing Xente data;
2. regenerate/locate validation + test risk scores;
3. run `run_xente_policy_replay.py`;
4. inspect Fixed vs Capacity-aware results;
5. freeze operational semantics;
6. then integrate Static/Adaptive fraudster.
