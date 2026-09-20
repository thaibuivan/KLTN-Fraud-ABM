# Validation Plan v0.1

## Model purpose
Model dùng để **compare/stress-test policy under stated scenarios and uncertainty**, không phải dự báo chính xác hệ thống của một ngân hàng cụ thể.

## Validation layers

### 1. Conceptual / structural validation
Với mỗi agent/state/rule:
- nó cần cho RQ nào?
- evidence từ đâu?
- assumption nào phải ghi rõ?

Current:
- customer state is justified by Xente repetition/history;
- analyst capacity mechanism is literature-supported;
- exact analyst speed/cost is not directly identified;
- queue discipline is a structural assumption.

### 2. Input / empirical validation
Verified Xente patterns:
- fraud prevalence;
- Value/Amount distribution;
- transaction timing;
- customer repetition;
- cold-start share;
- product/channel/provider distribution.

Risk-model validation now includes:
- chronological 70/15/15 split;
- PR-AUC, ROC-AUC, Brier;
- seen vs unseen-customer performance;
- expanding-window temporal checks;
- deliberately weaker/alternate score specifications.

Key finding:
PR-AUC varies substantially across chronological windows, so one final-test score is not treated as stable production performance.

### 3. Code verification
Implemented tests now check:
- no alert serviced before arrival;
- FIFO/risk-priority use the same total capacity under equal conditions;
- risk-priority ordering does not use `FraudResult`;
- stochastic service is reproducible under the same seed.

Local verification:
**4 tests passed.**

Still required when cost engine is added:
- no double counting of FP/FN/loss;
- threshold always selected on validation;
- raw fraud labels never enter queue priority.

### 4. Stochastic uncertainty
Implemented:
- lognormal service-time variation;
- coefficient of variation parameter;
- repeated random seeds;
- mean + 5th/95th percentile reporting.

Current pilot:
- service CV = 0.5;
- 100 seeds;
- CV is an explicit stress assumption, not empirical review-time calibration.

Future stochastic components only if justified:
- variable team capacity;
- analyst decision error;
- fraud-regime perturbation.

### 5. Parameter sensitivity
Current:
- capacity ratio 0.75 / 1.00 / 1.25;
- score model structure;
- stochastic service time.

Next:
- alert/review rate 0.5% / 1% / 2% / 5%;
- service-equity/starvation metric;
- optional wider service-variation range.

Later, if cost engine enters core:
- FP/customer-friction cost;
- recovery/prevention rate.

### 6. Structural sensitivity
Completed:
- FIFO vs risk-priority queue;
- full logistic vs no-current-value vs amount-only score model.

Planned:
- pooled constant mean capacity vs variable team capacity;
- optional shifted fraud regime.

## Current robustness finding
[[Xente Robustness Pack v0.1]] shows:
- risk-priority generally increases fraud review within the finite observation horizon under congestion;
- the qualitative result survives stochastic service times;
- it also survives a materially weaker score model;
- but risk-priority worsens tail waiting time for lower-priority alerts.

This is stronger than the first pilot but remains conditional on the Xente environment and tested structures.

## Claim discipline
Do not conclude:
- risk-priority is universally best;
- observed queue wait is real-bank waiting time;
- Xente classifier performance transfers to a bank;
- capacity ratios are empirical staffing levels;
- monetary value is identified before cost parameters are grounded.

Allowed claim form:
> Under the Xente event/score streams and evaluated capacity/model structures, queue discipline changes how scarce review capacity is allocated and therefore changes the trade-off between fraud capture and waiting-time distribution.

## Not required initially
- full History Matching + ABC;
- bank-specific calibration;
- LLM user study;
- massive experiment grid.

## TODO
- [x] Chốt primary dataset.
- [x] FIFO vs risk-priority structural test.
- [x] Persistent queue.
- [x] Seen vs cold-start evaluation.
- [x] Expanding-window temporal robustness.
- [x] Weak/alternate score-model sensitivity.
- [x] Stochastic service time + multiple seeds.
- [ ] Threshold/alert-rate sensitivity.
- [ ] Starvation/service-equity metrics.
- [ ] Variable team-capacity structure.
- [ ] Practitioner structural validation.
