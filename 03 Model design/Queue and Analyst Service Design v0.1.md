# Queue and Analyst Service Design v0.1

## Goal
Nâng legacy daily-capacity cut-off thành một **persistent queue** có waiting time/backlog và có thể kiểm tra structural sensitivity.

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
fixed threshold may generate a different test alert rate because the score distribution can drift over time.

This itself is an operational result, not a bug.

## 3. Persistent queue
Each alert stores:
- arrival time;
- risk score;
- fraud label only for evaluation (not visible to policy);
- service start/end;
- waiting time;
- backlog state.

Backlog carries across time; it is not reset at day boundaries.

## 4. Pooled service capacity
Core v0.1 does not invent analysts/day.

Define:

`capacity_ratio = pooled service rate / mean alert arrival rate`

Stress:
- 0.75 under-capacity;
- 1.00 matched average capacity;
- 1.25 spare capacity.

These are explicit stress scenarios, motivated by [[Alves et al 2025 - OpenL2D FiFAR]] capacity-constraint methodology, not direct bank calibration.

## 5. Queue disciplines

### FIFO
Serve earliest waiting alert first.

### Risk-priority
Serve highest risk score among waiting alerts first.

Non-preemptive:
a review already in service is not interrupted.

## 6. Core outcomes
Report:
- alerts generated;
- fraud alerts among candidates;
- reviewed within observed horizon;
- backlog at horizon end;
- mean waiting time;
- P95 waiting time;
- max waiting time;
- fraud reviewed within horizon;
- fraud capture within horizon;
- false positives reviewed within horizon.

Do not compute final money/net benefit yet.

## 7. Why risk-priority can create a trade-off
Risk-priority can improve high-risk/fraud service under congestion, but may:
- increase waiting time for low-score alerts;
- create long-tail starvation;
- leave the same total backlog as FIFO under equal service capacity.

Therefore evaluate **fraud capture + tail waiting time**, not only average wait.

## 8. Structural interpretation
If queue discipline materially changes fraud capture under identical scores/capacity, this supports the thesis claim that operational policy matters beyond classifier metrics.

## 9. Later extensions
Only after core is stable:
- heterogeneous analysts;
- stochastic service times;
- risk-tier-specific review times;
- alert expiry/escalation;
- delayed-review loss mechanism;
- cost-sensitive priority;
- LLM-assisted review.

## 10. Validation checks
- no alert serviced before arrival;
- service never exceeds pooled capacity;
- backlog carries across events;
- same alert stream for FIFO/risk-priority;
- fraud label never used for priority;
- risk-priority only uses model score;
- threshold chosen on validation, not test.
