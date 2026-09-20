# Validation Plan v0.1

## Model purpose
Model dùng để **compare/stress-test policy under stated scenarios and uncertainty**, không phải dự báo chính xác hệ thống của một ngân hàng cụ thể.

## Validation layers

### 1. Conceptual / structural validation
Với mỗi agent/state/rule:
- nó cần cho RQ nào?
- evidence từ đâu?
- assumption nào phải ghi rõ?

Current focus:
- customer state is justified by Xente repetition/history;
- analyst capacity mechanism is literature-supported;
- exact analyst speed/cost is not directly identified;
- queue discipline is a structural assumption.

### 2. Input / empirical validation
Current verified Xente patterns:
- fraud prevalence;
- Value/Amount distribution;
- transaction timing;
- customer repetition;
- cold-start share;
- product/channel/provider distribution.

Risk-model validation:
- chronological split only;
- report PR-AUC, calibration/Brier, operating points;
- report seen vs unseen-customer performance later;
- add temporal/rolling robustness.

### 3. Code verification
Mandatory checks:
- no alert serviced before arrival;
- threshold selected on validation, never test;
- fraud label never used for priority;
- queue does not reset at day boundary;
- backlog carry-over is correct;
- service capacity is not exceeded;
- FIFO/risk-priority use identical alert stream/capacity;
- cost calculations do not double-count when cost engine is added.

### 4. Stochastic uncertainty
Current queue v0.1 is deterministic conditional on scores/capacity.

Stochasticity will enter only when adding:
- variable analyst/service capacity;
- stochastic review time;
- optional analyst error;
- fraud-regime perturbation.

Then:
- run multiple seeds;
- report mean/CI/distribution;
- choose number of replications after convergence/stability check.

### 5. Parameter sensitivity
Prioritize high-uncertainty parameters:
- capacity ratio;
- review-time/service-rate distribution;
- FP/customer-friction cost;
- recovery/prevention rate if introduced;
- threshold/alert rate.

### 6. Structural sensitivity
Current first structural test:
- **FIFO vs risk-priority queue**.

Later candidates:
- pooled vs heterogeneous analyst capacity;
- logistic vs stronger/degraded risk-score model;
- static vs shifted fraud regime.

## Current pilot finding
[[Xente Queue Pilot v0.1]] shows queue discipline changes fraud capture under identical score/capacity conditions, while risk-priority worsens tail waiting time for lower-priority alerts.

This is a structural result that must be tested for robustness before becoming a thesis conclusion.

## Claim discipline
Do not conclude:
- risk-priority is universally best;
- observed queue wait is real-bank waiting time;
- Xente classifier performance transfers to a bank;
- capacity ratios are empirical cases/day.

Allowed claim form:
> Under the Xente score stream and evaluated capacity scenarios, queue discipline changes the allocation of scarce review capacity and therefore the trade-off between fraud capture and waiting-time distribution.

## Not required initially
- full History Matching + ABC;
- bank-specific calibration;
- LLM user study;
- massive experiment grid.

## TODO
- [x] Chốt primary dataset.
- [x] Chọn first structural alternative: FIFO vs risk-priority.
- [x] Implement first persistent queue pilot.
- [ ] Seen vs cold-start evaluation.
- [ ] Bootstrap/rolling temporal robustness.
- [ ] Add variable capacity/service-time and multiple seeds.
- [ ] Decide whether cost-sensitive priority is thesis-core or secondary sensitivity.
