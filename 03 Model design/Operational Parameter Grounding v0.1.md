# Operational Parameter Grounding v0.1

## Purpose
Chốt cách dùng literature hiện có cho analyst / queue / cost parameters mà **không biến external evidence thành fake calibration**.

## 1. Analyst capacity

### Evidence
[[Alves et al 2025 - OpenL2D FiFAR]] supports:
- work capacity as an explicit constraint;
- capacity defined per batch/time window;
- homogeneous vs variable expert capacities;
- robustness testing across expert availability/workload.

### What is NOT identified
Không có public evidence đủ mạnh để nói:
- một Xente-like fraud analyst xử lý chính xác N alerts/day;
- capacity của bank Việt Nam là một fixed value.

### Thesis decision
Core baseline dùng **relative pooled team capacity**:

`capacity_ratio = service_rate / mean_alert_arrival_rate`

Stress scenarios:
- 0.75 = under-capacity;
- 1.00 = capacity equal to mean alert arrival;
- 1.25 = above-average capacity.

Các mức này là **explicit stress assumptions**, không phải empirical fraud-operations estimates.

Advantage:
- transparent;
- dimensionless;
- directly tests congestion;
- avoids fake precision.

## 2. Analyst review time

### Evidence
[[Real bank AML alert scoring 2025]] reports a **5-minute light-touch review** for low-risk AML alerts during a bank pilot, while ordinary review was materially longer.

### Boundary
AML alert investigation != Xente transaction-fraud review.

### Thesis decision
Core queue v0.1 does **not** claim real review minutes.

Service interval is implied by capacity ratio and empirical alert arrivals.

Optional later sensitivity:
- fast-review anchor can reference 5 min externally;
- all longer review times must be explicit scenarios / practitioner-informed ranges.

## 3. Analyst heterogeneity / error

### Evidence
[[Alves et al 2025 - OpenL2D FiFAR]]:
- synthetic analysts can be heterogeneous;
- capacity heterogeneity matters;
- real transaction-fraud analyst data validates feature/model-score dependence.

Important limitation:
the private real-analyst dataset cannot identify team performance distribution because of missing labels and single-expert-per-instance observations.

### Thesis decision
Core v0.1:
- pooled analyst service;
- no arbitrary analyst accuracy distribution.

Extension:
- heterogeneous capacity / decision-quality mechanism only after evidence/practitioner input.

## 4. Queue discipline

Evidence supports limited human work capacity, but does not dictate exact queue discipline.

Structural alternatives:
1. FIFO;
2. risk-priority.

These are **model structures**, not calibrated bank facts.

Use structural sensitivity to ask:
> Does policy conclusion change when queue priority rule changes?

## 5. False-positive / friction cost

### Evidence
[[Hoppner et al 2022 - Cost-sensitive transfer fraud]] supports instance-dependent cost-sensitive decisioning.

Additional bank anti-fraud literature reports material operational/customer costs from false positives, but exact values are context-specific.

### Thesis decision
Primary results report decomposed outcomes:
- fraud caught/missed;
- false positives;
- reviewed alerts;
- backlog;
- waiting time.

Net-benefit/cost ranking is secondary sensitivity unless bank-specific costs become available.

## 6. Fraud loss / prevention

Xente gives observed transaction `Value`, which can be used as a **loss exposure proxy**.

What is unknown:
- how much loss a review prevents;
- how prevention probability decays with review delay.

Therefore:
- do not assume 75% recovery from legacy repo;
- initially report fraud Value exposed/caught without monetizing recovery;
- later add bounded recovery/delay scenarios if literature/practitioner evidence is sufficient.

## 7. Parameters now classified

| Parameter | Evidence status | Core treatment |
|---|---|---|
| Alert arrivals | Empirical + policy | derive from Xente score/policy |
| Customer history | Empirical-derived | Xente past-only features |
| Analyst capacity | Mechanism literature; no absolute calibration | relative capacity ratio stress |
| Review time | one external AML lower anchor only | not fixed in core |
| Analyst error | insufficient direct fraud-domain calibration | defer |
| Queue discipline | structural assumption | FIFO vs risk-priority |
| FP cost | literature supports relevance; exact value context-specific | decomposed outcome + later sensitivity |
| Fraud loss | Xente Value proxy | report exposed/caught Value |
| Recovery rate | weak | do not fix yet |
| Delay-loss relationship | weak | no causal claim yet |

## 8. Why this is methodologically safer
This design follows [[McCulloch 2022]]:
- observed parameters from data;
- uncertain parameters as ranges/scenarios;
- uncertain mechanisms as structural alternatives;
- conclusions reported conditionally.

It also follows the original research pack:
> do not self-select a single parameter when evidence is weak; use plausible ranges and sensitivity.
