# Queue and Analyst Service Design v0.1

## Goal
Nâng legacy daily-capacity cut-off thành một **persistent queue** có waiting time/backlog và structural sensitivity.

## 1. Input event stream
Use chronological scored Xente holdout events:
- TransactionId
- CustomerId
- TransactionStartTime
- Value
- FraudResult
- risk_probability
- seen/unseen customer flag

Threshold is selected on validation, then frozen for test replay.

## 2. Alert generation
Baseline:
- choose validation operating point by target alert/review rate;
- freeze score threshold;
- apply to later test stream.

Important:
a fixed threshold can produce a different test alert rate because score distribution drifts over time.

This is an operational result, not a bug.

## 3. Persistent queue
Each alert stores:
- arrival time;
- risk score;
- fraud label only for evaluation;
- service start/end;
- service duration;
- waiting time;
- backlog state.

Backlog carries across time; it is not reset at day boundaries.

## 4. Pooled service capacity

Core v0.1 does not invent analysts/day.

### Experiment A — Capacity stress conditional on one alert policy
Define:

`capacity_ratio = pooled service rate / realized mean alert arrival rate`

Stress:
- 0.75 under-capacity;
- 1.00 matched average capacity;
- 1.25 spare capacity.

Use this when asking:
> For one fixed threshold/event stream, how does more or less service capacity change outcomes?

These are explicit stress scenarios motivated by [[Alves et al 2025 - OpenL2D FiFAR]], not bank calibration.

### Experiment B — Threshold sensitivity with fixed staffing
When comparing different alert thresholds, **absolute service capacity must stay fixed**.

Procedure:
1. choose a reference validation alert rate, currently 1%;
2. derive its validation alert-arrival rate;
3. set pooled service rate as a multiple of that reference;
4. freeze the service rate;
5. replay 0.5%, 1%, 2%, 5% target thresholds.

Reason:
a more sensitive threshold must not automatically receive more analyst capacity.

See [[Xente Alert-rate and Starvation Sensitivity v0.1]].

## 5. Service-time stochasticity
Baseline can be deterministic.

Robustness mode:
- lognormal service time;
- mean fixed by pooled service rate;
- coefficient of variation configurable;
- repeated seeds.

Current pilot:
- service CV = 0.5;
- 100 seeds.

CV is an explicit stress assumption, not empirical review-time calibration.

## 6. Queue disciplines

### FIFO
Serve earliest waiting alert first.

### Risk-priority
Serve highest risk score among waiting alerts first.

Non-preemptive:
a review already in service is not interrupted.

Fraud label is never available to the queue rule.

## 7. Core outcomes

### Capacity / workload
- alerts generated;
- reviewed within horizon;
- backlog at horizon end.

### Fraud
- fraud alerts;
- fraud reviewed within horizon;
- fraud capture within horizon;
- seen vs unseen-customer fraud capture.

### Waiting time
- mean wait;
- P95 wait;
- P99 wait;
- max wait.

### Starvation / service-equity diagnostics
- share waiting >24h;
- share waiting >48h;
- share waiting >72h;
- low-priority quartile P95 wait;
- high-priority quartile P95 wait.

Do not compute final money/net benefit as a primary result yet.

## 8. Why risk-priority creates a trade-off
Risk-priority can:
- improve high-risk/fraud service under congestion;
- increase waiting time for low-score alerts;
- create long-tail starvation;
- leave total service capacity unchanged.

Therefore evaluate:

> **fraud capture + backlog + tail waiting + starvation**

not only average wait or recall.

## 9. Structural interpretation
If queue discipline materially changes fraud capture under identical scores/capacity, this supports the thesis claim that operational policy matters beyond classifier metrics.

If the result survives:
- weaker score models;
- temporal variation;
- service stochasticity;
- threshold/load variation,

then the conclusion is more robust.

## 10. Later extensions
Only after core is stable:
- variable team capacity over time;
- heterogeneous analysts;
- risk-tier-specific review times;
- alert aging/expiry/escalation;
- delayed-review loss mechanism;
- cost-sensitive priority;
- LLM-assisted review.

## 11. Validation checks
Current automated checks:
- no alert serviced before arrival;
- equal total capacity across FIFO/risk-priority;
- risk-priority ordering independent of FraudResult;
- stochastic service reproducible by seed;
- fixed pooled service rate stays fixed across threshold changes.

Local status:
**5 tests passed.**
