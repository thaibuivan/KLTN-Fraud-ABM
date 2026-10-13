# KLTN Completion Roadmap — 2026-10-13

## Mục tiêu cuối

Hoàn thành một closed-loop fraud-policy simulation / ABM phát triển từ đề án FinRisk, được parameterize trên hai empirical scenarios:

- Xente
- IEEE-CIS

và trả lời:

> Policy nào hoạt động ra sao dưới adaptive fraudster và limited analyst capacity, và conclusion có robust giữa hai environments hay không?

## Workstream A — Shared engine

- [x] Policy interface
- [x] Fixed-threshold policy
- [x] Capacity-aware policy
- [x] Cost-sensitive extension
- [x] Persistent queue engine
- [x] Integrated policy + queue engine
- [x] Static/adaptive fraudster prototype
- [x] Scenario adapters skeleton
- [ ] Full fraudster → policy → queue feedback integration
- [ ] Shared experiment runner
- [ ] Shared result schema
- [ ] Seed/convergence runner

## Workstream B — Xente Scenario A

- [x] EDA
- [x] Data-to-ABM mapping
- [x] Leakage-safe customer history
- [x] Chronological risk baseline
- [x] Temporal robustness
- [x] Queue/capacity pilots
- [x] Threshold sensitivity
- [x] FIFO/risk-priority robustness
- [x] Stochastic capacity/service robustness
- [ ] Run new integrated Fixed vs Capacity-aware replay
- [ ] Freeze Low/Medium/High capacity definitions
- [ ] Build Xente-grounded fraud generator
- [ ] Static fraudster full integration
- [ ] Adaptive fraudster full integration
- [ ] Run 12 core configurations
- [ ] Behavioral sensitivity
- [ ] Final Xente result tables/figures

## Workstream C — IEEE-CIS Scenario B

- [x] EDA
- [x] Data-to-ABM mapping
- [x] Role in two-scenario framework frozen
- [x] Common schema adapter code added
- [x] Pre-adaptation policy replay runner added
- [ ] Re-materialize / re-upload raw IEEE train files if needed
- [ ] Build executable chronological feature pipeline
- [ ] Freeze entity-proxy definition
- [ ] Train/validate IEEE risk model
- [ ] Run integrated policy replay
- [ ] Build IEEE-grounded fraud generator
- [ ] Static fraudster integration
- [ ] Adaptive fraudster integration
- [ ] Run 12 core configurations
- [ ] Behavioral sensitivity
- [ ] Final IEEE result tables/figures

## Workstream D — Cross-scenario experiment

- [x] 24-config core design frozen
- [x] Cross-scenario comparison plan written
- [ ] Align normalized capacity definition
- [ ] Align shared adaptation mechanism
- [ ] Run 12 Xente + 12 IEEE
- [ ] Compute adaptation penalty
- [ ] Compute capacity-aware policy gain
- [ ] Compare policy ranking
- [ ] Classify conclusions: consistent / environment-dependent / uncertain
- [ ] Main cross-scenario figures

## Workstream E — Validation

- [x] Validation Plan v1.0
- [x] Queue tests
- [x] Policy tests
- [x] Scenario-adapter tests
- [x] Integrated policy-system tests added
- [ ] Run full test suite locally
- [ ] Add full adaptive integration tests
- [ ] Extreme-condition tests
- [ ] Seed convergence analysis
- [ ] Cross-scenario robustness report

## Workstream F — Writing

- [x] Research Design v1.1
- [x] Methodology Skeleton v1.0
- [x] Results and Discussion Outline v1.0
- [ ] Introduction
- [ ] Literature Review
- [ ] Data section
- [ ] Full Methodology
- [ ] Results
- [ ] Discussion
- [ ] Limitations
- [ ] Conclusion
- [ ] Appendix: parameter registry
- [ ] Appendix: experiment configuration
- [ ] Appendix: validation/tests

## Critical path

```text
Get Xente score/raw files
        ↓
Run integrated Xente replay
        ↓
Freeze common interfaces + capacity normalization
        ↓
Static fraudster integration
        ↓
Adaptive fraudster integration
        ↓
12 Xente configurations
        ↓
Get IEEE raw files
        ↓
IEEE feature/risk pipeline
        ↓
12 IEEE configurations
        ↓
Cross-scenario comparison
        ↓
Sensitivity / validation
        ↓
Final thesis writing
```

## Current blockers

### Blocker 1 — Xente executable artifacts
Need at least:
- validation_scores.csv
- test_scores.csv

or raw Xente training.csv so they can be regenerated.

### Blocker 2 — IEEE executable raw data
Need:
- train_transaction.csv
- train_identity.csv if used

The EDA notebook exists, but raw IEEE CSVs are not currently available in the connected Library/session.

## Rule

Do not add a new mechanism until it is clear:
1. which RQ it answers;
2. what evidence supports it;
3. whether it belongs in core or robustness.
