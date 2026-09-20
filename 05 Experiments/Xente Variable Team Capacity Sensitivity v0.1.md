# Xente Variable Team Capacity Sensitivity v0.1

## Status
**Preliminary structural sensitivity — not bank staffing calibration.**

This experiment asks:

> If average pooled review capacity is the same, does day-to-day variation in team capacity materially change queue-policy conclusions?

The mechanism is motivated by [[Alves et al 2025 - OpenL2D FiFAR]], which treats expert capacity as a constrained and potentially variable quantity.

No claim is made that the chosen CV values represent a real bank.

---

## 1. Design

### Alert policy
Validation target alert rate:
- **1%**

Threshold is selected on validation and frozen.

### Fixed base capacity
Base pooled service capacity is anchored to the **validation 1% reference alert-arrival rate**.

Requested capacity ratios:
- 0.75
- 1.00
- 1.25

### Variable team capacity
A day-level capacity multiplier is drawn from a lognormal distribution with mean approximately 1.

Scenarios:
- CV = 0.0 → constant capacity
- CV = 0.3 → moderate variability stress
- CV = 0.6 → severe variability stress

The multiplier changes service rate, not alert priority.

### Replications
- 100 random seeds for variable-capacity scenarios.

Service-time CV is kept at 0 in this experiment so that **team-capacity variability is isolated**.

---

## 2. Full logistic model — capacity ratio 1.0

| Team capacity CV | Queue | Mean fraud capture | 5–95% range | Mean backlog | Mean P95 wait |
|---:|---|---:|---:|---:|---:|
| 0.0 | FIFO | 76.0% | 76–76% | 41.0 | 74.2 h |
| 0.0 | Risk-priority | 100.0% | 100–100% | 41.0 | 112.1 h |
| 0.3 | FIFO | 77.3% | 75.9–82.0% | 42.1 | 78.3 h |
| 0.3 | Risk-priority | 99.4% | 96–100% | 42.1 | 118.1 h |
| 0.6 | FIFO | 76.6% | 69.9–86.0% | 47.2 | 92.9 h |
| 0.6 | Risk-priority | 97.8% | 90–100% | 47.2 | 146.3 h |

### Interpretation
Variable capacity increases uncertainty in:
- backlog;
- waiting time;
- fraud capture.

The qualitative queue trade-off remains:
- risk-priority protects fraud service;
- but increases tail waiting time.

Under severe capacity volatility, even the strong Xente score model no longer guarantees 100% fraud review.

---

## 3. Weaker score model — capacity ratio 1.0

Using the **no-current-value** model:

| Team capacity CV | Queue | Mean fraud capture | 5–95% range | Mean backlog | Mean P95 wait |
|---:|---|---:|---:|---:|---:|
| 0.0 | FIFO | 56.0% | 56–56% | 62.0 | 110.9 h |
| 0.0 | Risk-priority | 72.0% | 72–72% | 62.0 | 145.3 h |
| 0.3 | FIFO | 54.6% | 50–56% | 63.0 | 112.9 h |
| 0.3 | Risk-priority | 70.8% | 66–74% | 63.0 | 150.3 h |
| 0.6 | FIFO | 53.3% | 47.9–62% | 67.5 | 127.4 h |
| 0.6 | Risk-priority | 69.0% | 62–76% | 67.5 | 173.8 h |

### Interpretation
The same qualitative mechanism survives when:
- score quality is weaker;
- team capacity fluctuates.

This is stronger evidence that the queue result is not solely caused by near-perfect Xente ranking.

---

## 4. Moderate capacity variability across staffing levels

Team-capacity CV = **0.3**, 100 seeds.

### Full logistic

| Requested capacity ratio | Queue | Mean fraud capture | Mean backlog | Mean P95 wait |
|---:|---|---:|---:|---:|
| 0.75 | FIFO | 68.6% | 71.5 | 171.4 h |
| 0.75 | Risk-priority | 96.8% | 71.5 | 308.2 h |
| 1.00 | FIFO | 77.3% | 42.1 | 78.3 h |
| 1.00 | Risk-priority | 99.4% | 42.1 | 118.1 h |
| 1.25 | FIFO | 82.2% | 32.7 | 52.8 h |
| 1.25 | Risk-priority | 100.0% | 32.7 | 75.1 h |

### No-current-value model

| Requested capacity ratio | Queue | Mean fraud capture | Mean backlog | Mean P95 wait |
|---:|---|---:|---:|---:|
| 0.75 | FIFO | 47.0% | 91.5 | 216.9 h |
| 0.75 | Risk-priority | 63.0% | 91.5 | 309.0 h |
| 1.00 | FIFO | 54.6% | 63.0 | 112.9 h |
| 1.00 | Risk-priority | 70.8% | 63.0 | 150.3 h |
| 1.25 | FIFO | 58.5% | 47.6 | 71.0 h |
| 1.25 | Risk-priority | 74.1% | 47.6 | 99.6 h |

---

## 5. Service-equity interpretation

With capacity CV = 0.3 and requested ratio = 1.0:

### Full logistic
- FIFO low-priority P95 wait ≈ 70.9 h
- Risk-priority low-priority P95 wait ≈ **156.1 h**
- Risk-priority high-priority P95 wait ≈ **24.1 h**

### Weaker model
- FIFO low-priority P95 wait ≈ 96.9 h
- Risk-priority low-priority P95 wait ≈ **189.3 h**
- Risk-priority high-priority P95 wait ≈ **23.7 h**

So variable capacity does not remove the core trade-off:

> prioritization protects high-risk service partly by shifting delay toward lower-priority alerts.

---

## 6. Current conclusion

The queue-priority finding is now robust to three distinct uncertainties:

1. **score-model structure**
2. **per-case service-time randomness**
3. **day-level pooled-team capacity variation**

This does not establish external bank validity.

It does strengthen the narrower simulation claim:

> Under the evaluated Xente event streams, prioritization changes how limited and variable review capacity is allocated, and the resulting fraud-capture benefit is accompanied by a tail-waiting cost.

---

## 7. Parameter-status reminder
- CV = 0.3 and 0.6 are **stress assumptions**.
- They are not estimates from FiFAR or a bank.
- Practitioner feedback may later replace or narrow these ranges.

Links:
- [[Xente Robustness Pack v0.1]]
- [[Xente Alert-rate and Starvation Sensitivity v0.1]]
- [[Operational Parameter Grounding v0.1]]
- [[Validation Plan v0.1]]
