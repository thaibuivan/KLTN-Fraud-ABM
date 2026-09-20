# KLTN Dashboard

## Current thesis direction
Phát triển từ pilot `FinRisk-ABM-Policy-Simulation` thành một **empirically grounded, uncertainty-aware dynamic fraud-policy simulation/ABM**.

## Decisions locked
- **Primary dataset:** Xente Fraud Detection.
- **Primary stateful entity:** `CustomerId`.
- **Baseline data mode:** chronological observed-event replay.
- **Simulation clock:** event-driven.
- **AccountId / SubscriptionId:** context identifiers/features, not separate agents.
- **Baseline risk engine:** regularized logistic regression first.
- **Core operational mechanism:** persistent alert queue.
- **First structural comparison:** FIFO vs risk-priority.
- **Capacity representation:** relative pooled capacity ratio, not invented cases/day.
- **IEEE-CIS:** optional external robustness, not second full ABM.

## Current milestone
**Queue/policy robustness after empirical baseline.**

### Completed
1. [[Data Audit]] ✅
2. [[Xente Empirical Profile]] ✅
3. Leakage-safe customer features ✅
4. Logistic baseline feasibility ✅
5. Literature grounding for analyst/capacity/cost ✅
6. Persistent queue simulator ✅
7. [[Xente Queue Pilot v0.1]] ✅

## Literature
- [[AML-CFSim 2025]]
- [[McCulloch 2022]]
- [[Alves et al 2025 - OpenL2D FiFAR]]
- [[Hoppner et al 2022 - Cost-sensitive transfer fraud]]
- [[Real bank AML alert scoring 2025]]

## Design
- [[Research Design v0.2]]
- [[Conceptual Model v0.2]]
- [[Data Audit]]
- [[Evidence Parameter Matrix]]
- [[Operational Parameter Grounding v0.1]]
- [[Queue and Analyst Service Design v0.1]]
- [[Validation Plan v0.1]]

## Key current insight
At identical model scores and pooled service capacity:
- risk-priority can materially increase fraud review within the observation horizon;
- but it increases tail waiting time for lower-priority alerts;
- total capacity/backlog does not disappear merely by changing priority.

This is a **pilot result**, not yet a final thesis conclusion.

## Current blockers
- transaction-fraud review-time range is still weakly grounded;
- recovery/delay-to-loss mechanism is not identified;
- false-positive/customer-friction monetary value is context-specific;
- risk model is unusually strong on Xente and needs robustness checks.

## Next priorities
1. Seen vs cold-start customer performance.
2. Rolling/temporal robustness and bootstrap intervals.
3. Risk-score degradation / alternate model structural sensitivity.
4. Variable capacity/service-time with multiple seeds.
5. Only then add cost-sensitive priority/net-benefit sensitivity.

## Rule
Không làm LLM, fraudster cognition hoặc dashboard trước khi robustness của core queue/policy model đủ rõ.
