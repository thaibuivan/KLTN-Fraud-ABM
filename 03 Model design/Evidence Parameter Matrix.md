# Evidence Parameter Matrix

## Evidence labels
- **Empirical**: estimate trực tiếp từ primary dataset.
- **Literature-informed**: range/mechanism từ nghiên cứu liên quan.
- **Expert-informed**: expert input nếu có.
- **Theory-informed**: rule có theoretical support.
- **Explicit assumption**: lựa chọn mô hình hóa phải kiểm tra sensitivity.
- **Legacy assumption**: giá trị có trong đề án cũ nhưng chưa được tái-ground cho KLTN.

## Primary empirical source
**Xente Fraud Detection** — xem [[Data Audit]] và [[Xente Empirical Profile]].

| Parameter / mechanism | Module | Source | Evidence type | Value/range | Uncertainty | Status |
|---|---|---|---|---|---|---|
| Fraud prevalence | Fraud regime | Xente labelled train | Empirical | 193 / 95,662 = 0.2018% overall | Temporal variation | **Verified** |
| Amount / Value distribution | Transaction | Xente | Empirical | See Xente profile | Medium due strong tail | **Verified** |
| Transaction timing | Transaction | Xente `TransactionStartTime` | Empirical | 2018-11-15 → 2019-02-13 labelled | Medium | **Verified** |
| Customer identity | Customer state | Xente `CustomerId` | Empirical | 3,742 unique; median 7 tx/customer | Low | **Chosen** |
| AccountId / SubscriptionId | Transaction context | Xente | Empirical | not clean nested ownership | Medium | **Verified limitation** |
| Transaction frequency / velocity | Customer state | chronological Xente history | Empirical-derived | rolling past-only windows | Medium | **Implemented** |
| Product/category/channel mix | Transaction | Xente | Empirical | observed frequencies | Medium | **Verified** |
| Baseline risk score | Risk engine | Xente chronological train | Empirical model | logistic baseline | Model uncertainty | **Feasibility tested** |
| Risk threshold | Policy | validation operating point | Empirical + policy choice | derived on validation, frozen on test | Temporal drift | **Implemented in plan** |
| Alert arrivals | Queue | Xente score + policy | Empirical + policy | derived from frozen threshold | Policy-dependent | **Ready** |
| Analyst/team capacity mechanism | Queue | Alves et al. 2025 / FiFAR | Literature-informed mechanism | capacity per batch/time window | High externally | **Grounded mechanism** |
| Absolute analyst cases/day | Queue/Analyst | no bank-specific public source | Unknown | **do not fix as empirical** | High | **Use relative stress** |
| Relative pooled capacity | Queue | FiFAR-inspired + explicit stress | Literature + explicit assumption | capacity ratio 0.75 / 1.00 / 1.25 | High | **Core v0.1** |
| Review-time lower anchor | Analyst | real-bank AML scoring study 2025 | External operational evidence | 5-min light-touch low-risk review | High transfer uncertainty | **Anchor only** |
| Standard transaction-fraud review time | Analyst | insufficient direct evidence | Unknown | TBD / scenario only | High | **Do not calibrate yet** |
| Analyst capacity heterogeneity | Analyst | Alves et al. 2025 | Literature-informed mechanism | homogeneous vs variable | High | Extension |
| Analyst decision error | Analyst | FiFAR / high-stakes literature | Mixed; not direct real fraud calibration | no fixed probability | High | Defer from core |
| Queue discipline | Queue | model design | Structural assumption | FIFO vs risk-priority | High | **Structural sensitivity** |
| False-positive operational cost | Cost engine | Höppner 2022 + antifraud literature | Literature supports relevance | exact value context-specific | High | **Report decomposed first** |
| Customer-friction cost | Cost engine | antifraud literature | External | no Xente-specific value | High | Sensitivity only |
| Fraud loss exposure | Cost engine | Xente `Value` | Empirical proxy | transaction Value | Medium | **Usable proxy** |
| Fraud recovery/prevention rate | Outcome | no Xente observation | Assumption/literature TBD | no fixed 75% legacy value | High | **Do not fix yet** |
| Review-delay effect on loss | Outcome | operational logic; insufficient direct estimate | Structural/unknown | no causal coefficient yet | High | **Do not monetize yet** |
| Fraud-regime shift | Stress scenario | Xente baseline + bounded perturbation | Mixed | TBD bounded scenarios | High | Planned |

## Literature decisions

### OpenL2D / FiFAR
Use for:
- capacity constraint representation;
- expert availability/workload robustness;
- homogeneous vs variable capacity.

Do **not** use for:
- a real fraud analyst cases/day number;
- real analyst accuracy distribution;
- real review-time distribution.

### Höppner et al. 2022
Use for:
- instance-dependent cost-sensitive decision framing;
- supporting amount-dependent loss exposure.

Do not use for queue/capacity.

### Real-bank AML alert scoring study
Use for:
- evidence that review time/routing materially affects workload;
- 5-minute light-touch review as an external lower/fast-review anchor only.

Do not transfer directly as transaction-fraud calibration.

## Core v0.1 rule
Until stronger practitioner/bank-specific evidence exists:
1. report **fraud caught/missed, FP, workload, backlog, waiting time** separately;
2. model capacity using **relative stress ratios**;
3. keep monetary net benefit as secondary sensitivity;
4. do not invent analyst accuracy/recovery parameters.

## Legacy values that must NOT be copied automatically
Repo cũ used:
- daily analyst capacities;
- 6/9 minute review times;
- 75% fraud recovery;
- fixed false-positive costs;
- fraud strategy probabilities.

These remain **legacy assumptions**, not thesis calibration.

## Next evidence need
Highest-value missing evidence:
1. practitioner validation of workflow and priority rules;
2. plausible transaction-fraud review-time range;
3. whether delayed review affects recoverability in the intended operational setting;
4. acceptable customer-friction proxy.
