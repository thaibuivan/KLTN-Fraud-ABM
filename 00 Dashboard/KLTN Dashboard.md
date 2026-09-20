# KLTN Dashboard

## Current thesis direction
Phát triển từ pilot `FinRisk-ABM-Policy-Simulation` thành một **empirically grounded, uncertainty-aware dynamic fraud-policy simulation/ABM**.

## Decisions locked
- **Primary dataset:** Xente Fraud Detection.
- **Primary stateful entity:** `CustomerId`.
- **Baseline data mode:** chronological observed-event replay.
- **Simulation clock:** event-driven.
- **AccountId / SubscriptionId:** nested state/grouping trước.
- **Baseline risk engine candidate:** regularized logistic regression.
- **Core policy families:** fixed-threshold, capacity-aware, cost-sensitive.
- **IEEE-CIS:** optional external robustness, not second full ABM.

## Current milestone
**Empirical baseline setup + operational-parameter grounding.**

### Priority
1. [[Data Audit]] ✅
2. Xente local profiling + chronological split.
3. [[Evidence Parameter Matrix]] — tìm literature cho analyst/cost/queue parameters.
4. Implement leakage-safe customer features.
5. Implement persistent queue/backlog.
6. Fit baseline risk engine.
7. Re-run legacy policy hypotheses.
8. [[Validation Plan v0.1]] + repeated seeds/sensitivity.

## Legacy project
- [[Legacy Project Audit - FinRisk]]
- [[Legacy Migration Map]]
- [[Prototype-to-Thesis Gap]]

> Repo cũ là pilot/legacy. Không copy nguyên assumptions hoặc kết quả sang KLTN; kết luận chính phải được re-test trong design mới.

## Design
- [[Research Design v0.2]]
- [[Conceptual Model v0.2]]
- [[Data Audit]]
- [[Evidence Parameter Matrix]]
- [[Validation Plan v0.1]]

## Current blockers
- Chưa có raw Xente local trong workspace.
- Analyst capacity/review-time literature chưa chốt.
- False-positive/friction cost và review-delay mechanism chưa chốt.

## Next coding target
`scripts/profile_xente.py` → profile schema, label imbalance, entity repetition, time range, amount distribution and leakage-safe split feasibility without committing raw data.
