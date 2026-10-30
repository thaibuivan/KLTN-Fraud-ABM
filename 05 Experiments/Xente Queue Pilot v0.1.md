# Xente Queue Pilot v0.1

## Status
**Preliminary structural experiment — not final thesis result.**

Goal:
Test whether persistent backlog + queue discipline can change operational outcomes even when the risk scores and alert threshold are held fixed.

## Setup

### Data
Chronological Xente split:
- train 70%;
- validation 15%;
- test 15%.

Risk engine:
- regularized logistic regression;
- leakage-safe rolling features;
- threshold chosen **only on validation**.

### Threshold
Target validation alert rate: **1%**.

Frozen validation threshold:
- risk probability ≈ **0.014801**.

When applied to test, realized alert rate became **1.31%**:
- 188 alerts;
- 50 fraud alerts.

This difference is useful evidence of temporal score/alert-rate drift.

### Capacity
Pooled capacity is not a claimed bank cases/day figure.

`capacity_ratio = service_rate / mean alert arrival rate`

Scenarios:
- 0.75
- 1.00
- 1.25

### Queue disciplines
1. FIFO
2. Risk-priority

Fraud label is **never** used for priority; risk-priority uses model score only.

---

## Results

| Capacity ratio | Discipline | Reviewed within horizon | Backlog end | Mean wait | P95 wait | Fraud reviewed | Fraud capture |
|---:|---|---:|---:|---:|---:|---:|---:|
| 0.75 | FIFO | 142 | 46 | 40.1 h | 91.6 h | 38 | 76% |
| 0.75 | Risk-priority | 142 | 46 | 40.1 h | 131.9 h | 50 | 100% |
| 1.00 | FIFO | 155 | 33 | 18.7 h | 51.2 h | 41 | 82% |
| 1.00 | Risk-priority | 155 | 33 | 18.7 h | 68.9 h | 50 | 100% |
| 1.25 | FIFO | 163 | 25 | 11.8 h | 35.2 h | 45 | 90% |
| 1.25 | Risk-priority | 163 | 25 | 11.8 h | 50.6 h | 50 | 100% |

## Interpretation

### 1. Capacity matters
Higher capacity:
- reduces backlog;
- reduces average/tail waiting time;
- improves how much fraud is reviewed before the observed horizon ends.

This re-tests the legacy hypothesis using an empirical Xente score stream.

### 2. Queue discipline matters even with identical model scores
Risk-priority serves high-score alerts sooner.

In this pilot it increases fraud capture within horizon substantially relative to FIFO.

### 3. Risk-priority has a fairness/service-tail cost
Total service capacity and total backlog are unchanged relative to FIFO under the same capacity ratio.

However, risk-priority produces worse P95/max waiting time for lower-priority alerts.

So:
> optimizing fraud capture can worsen service equity / tail delay.

This is exactly the type of system-level trade-off that pure classifier metrics do not show.

## Important limitation
The result is unusually strong because:
- Xente fraud is highly separable by Value/context;
- test contains only 50 frauds;
- the logistic model ranks these test frauds extremely well;
- capacity ratios are explicit stress assumptions, not bank calibration.

Therefore the statement is **not**:
> risk-priority is the best policy.

The defensible statement is:
> under this Xente score stream and the evaluated capacity scenarios, risk-priority changes which alerts receive scarce service first and can materially increase fraud review within the observation horizon, while increasing tail waiting time for lower-priority alerts.

## Robustness already screened
The same qualitative pattern was screened at validation target alert rates:
- 0.5%;
- 1%;
- 2%.

Risk-priority generally improves fraud capture under congestion, but the magnitude depends on threshold and capacity.

## Next experiment
1. bootstrap / rolling temporal robustness;
2. seen vs cold-start customer outcomes;
3. more conservative risk-score model / degraded-score structural sensitivity;
4. cost-sensitive priority only after cost assumptions are bounded;
5. optional stochastic capacity/service-time scenarios.
