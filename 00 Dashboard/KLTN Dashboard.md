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
- **Capacity representation:** relative/fixed pooled capacity experiments, not invented analysts/day.
- **IEEE-CIS:** optional external robustness, not second full ABM.

## Current milestone
**Freeze core MVP after robustness + structural validation.**

### Completed
1. [[Data Audit]] ✅
2. [[Xente Empirical Profile]] ✅
3. Leakage-safe customer features ✅
4. Logistic baseline feasibility ✅
5. Literature grounding for analyst/capacity/cost ✅
6. Persistent queue simulator ✅
7. [[Xente Queue Pilot v0.1]] ✅
8. Seen vs cold-start analysis ✅
9. Expanding-window temporal robustness ✅
10. Risk-model structural sensitivity ✅
11. Stochastic service-time robustness over 100 seeds ✅
12. Fixed-capacity alert-threshold sensitivity ✅
13. Starvation/service-equity diagnostics ✅
14. Queue verification tests: **5 passed** ✅
15. Practitioner validation question guide drafted ✅
16. GVHD milestone update drafted ✅

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

## Experiments
- [[Xente Baseline Risk Model Feasibility]]
- [[Xente Queue Pilot v0.1]]
- [[Xente Robustness Pack v0.1]]
- [[Xente Alert-rate and Starvation Sensitivity v0.1]]

## Current robust insight
Across tested Xente score streams:
- scarce service capacity creates backlog/delay;
- threshold changes can create overload under fixed staffing;
- risk-priority reallocates scarce service toward high-risk alerts;
- fraud capture within a finite horizon generally increases relative to FIFO;
- tail waiting/starvation for lower-priority alerts worsens;
- the qualitative result persists after removing current-Value features;
- the result persists under stochastic service times.

This is a **conditional simulation result**, not a universal policy recommendation.

## Important caution
Xente has unusually strong transaction-Value/context signal.

The amount-only baseline is nearly as strong as the full logistic model on the final test period.

Therefore:
- classifier novelty is not the contribution;
- policy conclusions must be reported across time/model structures;
- final-test PR-AUC is not treated as stable production performance.

## Current blockers
- practitioner validation has been drafted but not yet conducted;
- transaction-fraud review-time range remains weakly grounded;
- recovery/delay-to-loss mechanism is not identified;
- false-positive/customer-friction monetary value is context-specific;
- alert aging/expiry rule is not yet justified.

## Next priorities
1. Conduct practitioner structural validation using [[Practitioner Validation Questions v0.1]].
2. Ask GVHD the five decisions in [[GVHD Update - Xente Queue Milestone]].
3. Based on feedback, decide whether to add:
   - hybrid aging priority;
   - variable team capacity;
   - cost-sensitive monetary layer.
4. Freeze core mechanisms and final experiment grid.
5. Then write Methodology from the frozen implementation.

## Rule
Không làm LLM, fraudster cognition hoặc dashboard trước khi core mechanism được freeze.
