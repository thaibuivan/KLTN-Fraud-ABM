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

Next external check:
- practitioner structural validation;
- GVHD scope/framing validation.

### 2. Input / empirical validation
Verified Xente patterns:
- fraud prevalence;
- Value/Amount distribution;
- transaction timing;
- customer repetition;
- cold-start share;
- product/channel/provider distribution.

Risk-model validation includes:
- chronological 70/15/15 split;
- PR-AUC, ROC-AUC, Brier;
- seen vs unseen-customer performance;
- expanding-window temporal checks;
- weaker/alternate score specifications.

Key finding:
PR-AUC varies substantially across chronological windows, so one final-test score is not treated as stable production performance.

### 3. Code verification
Automated queue tests now check:
- no alert serviced before arrival;
- FIFO/risk-priority use the same total capacity under equal conditions;
- risk-priority ordering does not use `FraudResult`;
- stochastic service is reproducible under the same seed;
- fixed pooled service rate remains fixed across threshold changes.

Local verification:
**5 tests passed.**

Still required if monetary cost engine is added:
- no double counting of FP/FN/loss;
- recovery assumptions isolated from observed labels;
- cost units clearly marked simulated/external.

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
Completed:
- capacity ratio 0.75 / 1.00 / 1.25;
- risk-model structure;
- stochastic service time;
- target alert rate 0.5% / 1% / 2% / 5%.

Important design:
threshold sensitivity holds **absolute pooled service capacity fixed**, anchored to a reference validation alert stream.

This prevents a sensitive policy from receiving artificial extra capacity.

### 6. Structural sensitivity
Completed:
- FIFO vs risk-priority;
- full logistic vs no-current-value vs amount-only score model.

Possible later:
- constant vs variable team capacity;
- risk-priority vs aging/hybrid priority;
- shifted fraud regime.

## Current robustness finding
[[Xente Robustness Pack v0.1]] and [[Xente Alert-rate and Starvation Sensitivity v0.1]] show:
- risk-priority generally increases fraud service under congestion;
- effect persists under stochastic service times;
- effect persists with a materially weaker score model;
- threshold-induced alert growth can create severe backlog under fixed staffing;
- risk-priority can create severe low-priority tail waiting/starvation.

This remains conditional on the Xente environment and tested structures.

## Claim discipline
Do not conclude:
- risk-priority is universally best;
- simulated waiting hours are real-bank SLAs;
- Xente classifier performance transfers to a bank;
- capacity ratios are empirical staffing levels;
- low-priority starvation is operationally acceptable;
- monetary value is identified before cost parameters are grounded.

Allowed claim form:
> Under the Xente event/score streams and evaluated capacity/model structures, alert thresholds and queue disciplines change how scarce review capacity is allocated, generating trade-offs among fraud capture, backlog and waiting-time distribution.

## Not required initially
- full History Matching + ABC;
- bank-specific calibration;
- LLM user study;
- massive experiment grid.

## TODO
- [x] Chốt primary dataset.
- [x] FIFO vs risk-priority.
- [x] Persistent queue.
- [x] Seen vs cold-start.
- [x] Expanding-window temporal robustness.
- [x] Weak/alternate score-model sensitivity.
- [x] Stochastic service time + multiple seeds.
- [x] Threshold/alert-rate sensitivity with fixed staffing.
- [x] Starvation/service-equity diagnostics.
- [ ] Practitioner structural validation.
- [ ] Decide aging/expiry/hybrid mechanism.
- [ ] Freeze final experiment grid.
