# KLTN Dashboard

## Current thesis direction
Phát triển từ pilot `FinRisk-ABM-Policy-Simulation` thành một **empirically grounded, uncertainty-aware dynamic fraud-policy simulation/ABM**.

## Decisions locked
- **Primary dataset:** Xente Fraud Detection.
- **Primary stateful entity:** `CustomerId`.
- **Baseline data mode:** chronological observed-event replay.
- **Simulation clock:** event-driven.
- **AccountId / SubscriptionId:** context identifiers/features, not separate agents.
- **Baseline risk engine candidate:** regularized logistic regression.
- **Core policy families:** fixed-threshold, capacity-aware, cost-sensitive.
- **IEEE-CIS:** optional external robustness, not second full ABM.

## Current milestone
**Empirical baseline setup + operational-parameter grounding.**

### Priority
1. [[Data Audit]] ✅
2. [[Xente Empirical Profile]] ✅
3. Leakage-safe customer feature builder ✅
4. Logistic baseline feasibility screen ✅
5. [[Evidence Parameter Matrix]] — literature cho analyst/cost/queue parameters.
6. Implement persistent queue/backlog.
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
- Analyst capacity/review-time literature chưa chốt.
- False-positive/friction cost và review-delay mechanism chưa chốt.
- Persistent queue chưa implement.

## Verified Xente facts
- 95,662 labelled transactions; 193 fraud.
- 3,742 CustomerIds; median 7 transactions/customer.
- 70/15/15 chronological split: 104 / 39 / 50 fraud.
- Significant cold-start in later periods.
- AccountId/SubscriptionId are not clean nested customer entities.

## Next coding target
Persistent event-driven alert queue + pooled analyst service, then FIFO vs risk-priority comparison.
