# Xente Alert-rate and Starvation Sensitivity v0.1

## Status
**Preliminary policy-load sensitivity — not a final bank-operational claim.**

This experiment asks:

> What happens when the alert threshold changes while the analyst team's absolute pooled service capacity stays fixed?

This is different from the earlier capacity-ratio experiment, which scaled service capacity relative to each realized alert stream.

---

## 1. Design correction

For threshold comparison, analyst capacity must **not** automatically increase when a more sensitive threshold produces more alerts.

Therefore the sensitivity runner now:

1. selects a **reference validation alert rate = 1%**;
2. estimates the corresponding validation alert-arrival rate;
3. defines pooled service capacity as a multiple of that fixed reference rate;
4. freezes that absolute service rate;
5. changes only the alert threshold on the test stream.

This allows threshold-induced overload to appear naturally.

### Why this matters
If service capacity were re-scaled separately for every threshold, a 5% alert policy would unrealistically receive roughly five times the analyst capacity of a 1% alert policy.

That would hide the operational consequence the thesis is trying to study.

---

## 2. Full logistic score model

Results below use **requested capacity ratio = 1.0 relative to the validation 1% reference load**.

Because test alert volume drifts relative to validation, the realized effective load/capacity ratio changes.

| Validation target alert rate | Test alerts | Effective capacity ratio on test | Backlog end | FIFO fraud capture | Risk-priority fraud capture |
|---:|---:|---:|---:|---:|---:|
| 0.5% | 106 | 1.46 | 11 | 92% | 100% |
| 1% | 188 | 0.82 | 41 | 76% | 100% |
| 2% | 357 | 0.43 | 202 | 58% | 100% |
| 5% | 824 | 0.19 | 669 | 34% | 100% |

### Interpretation
A fixed team that is comfortably above capacity under a strict threshold can become heavily overloaded when the threshold becomes more sensitive.

The test stream also produces more alerts than implied by the same validation target:
- validation target 1%;
- realized test alert rate ≈ 1.31%.

So even an unchanged policy + unchanged staffing can move from approximately matched capacity to overload because the score/alert distribution shifts over time.

---

## 3. Waiting-time / starvation trade-off

At the same requested capacity ratio = 1.0:

| Alert target | FIFO P95 wait | Risk-priority P95 wait |
|---:|---:|---:|
| 0.5% | ~30.0 h | ~40.5 h |
| 1% | ~74.2 h | ~112.1 h |
| 2% | ~356.2 h | ~512.4 h |
| 5% | ~1,175 h | ~1,337 h |

These are **simulation queue times**, not claimed real-bank review times.

The extreme 2%/5% values are intentional overload stress results: service capacity is anchored to the 1% validation reference while alert arrivals become much larger.

### Priority-specific starvation
At the 5% alert target under risk-priority:
- low-priority alert P95 waiting time ≈ **1,438 h**;
- high-priority alert P95 waiting time ≈ **151 h**.

This shows the mechanism clearly:

> risk-priority can preserve high-risk/fraud service under severe overload by pushing low-priority alerts deep into the queue.

Therefore fraud capture alone is not sufficient to evaluate a queue policy.

---

## 4. Degraded risk model check

To avoid a conclusion driven only by Xente's very strong Value signal, the same fixed-capacity experiment was repeated using the **no-current-value** score model.

Requested capacity ratio = 1.0:

| Alert target | Test alerts | Effective capacity ratio | FIFO fraud capture | Risk-priority fraud capture |
|---:|---:|---:|---:|---:|
| 0.5% | 108 | 1.43 | 50% | 54% |
| 1% | 208 | 0.74 | 56% | 72% |
| 2% | 396 | 0.39 | 56% | 76% |
| 5% | 866 | 0.18 | 34% | 76% |

### Interpretation
With a materially weaker score model:
- risk-priority still improves fraud service under overload;
- the improvement is no longer near-perfect;
- score quality strongly limits how much prioritization can help.

This is a more realistic robustness result than the near-100% capture seen with the full Xente score model.

---

## 5. Current system-level lesson

The experiments now separate three levers:

```text
risk-model quality
        ×
alert threshold / alert volume
        ×
fixed service capacity
        ×
queue priority rule
        ↓
fraud capture + backlog + waiting-time distribution
```

This supports the thesis framing more strongly than a classifier-only analysis.

A policy that improves recall by lowering the threshold can:
- increase candidate fraud coverage;
- but overload a fixed review team;
- increase backlog;
- increase delay;
- create severe starvation for low-priority alerts.

---

## 6. What can be claimed

### Supported conditionally
Under the Xente score/event stream:
- alert-rate drift can change effective capacity pressure even when staffing is fixed;
- lower thresholds can cause nonlinear backlog growth;
- risk-priority can protect fraud review under overload;
- risk-priority can substantially worsen lower-priority waiting time;
- these qualitative effects persist with a weaker score model.

### Not supported
Do not claim:
- the simulated hours are real bank SLA estimates;
- 1% is the correct alert rate for a bank;
- risk-priority is universally optimal;
- low-priority alerts can safely wait indefinitely;
- a 5% alert rate is operationally realistic.

---

## 7. New evaluation requirement
From now on every queue-policy table should include at least:
- fraud capture;
- backlog end;
- mean/P95 wait;
- share waiting > 24h / 48h / 72h;
- low-priority P95 wait;
- high-priority P95 wait.

This prevents a policy from appearing attractive only because it maximizes fraud capture while hiding starvation.

---

## 8. Next step
Before monetary net-benefit:
1. practitioner validation of priority/workflow;
2. variable team capacity as a structural sensitivity;
3. decide whether alert expiry/SLA should exist;
4. define one service-equity metric for final thesis tables.

Links:
- [[Xente Robustness Pack v0.1]]
- [[Queue and Analyst Service Design v0.1]]
- [[Operational Parameter Grounding v0.1]]
- [[Validation Plan v0.1]]
