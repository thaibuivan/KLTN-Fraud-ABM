# Xente Feature-Level Core Run v0.2 — 50 seeds

## Status

**Candidate final Xente core run for the main mechanism.**

This run upgrades the earlier score/value-template pilot to a feature-level counterfactual loop:

```text
validation fraud context
→ Static / Adaptive strategy
→ raw Xente-compatible fraud event
→ online past-only fraudster history
→ saved Xente logistic risk model
→ Fixed / Capacity-aware policy
→ FIFO queue / analyst capacity
→ APPROVE / REVIEW / BLOCK feedback
→ next strategy
```

The run covers the full Xente core grid:

```text
2 fraudster modes
× 2 policies
× 3 capacity levels
= 12 configurations
```

with **50 random seeds per configuration**.

## Frozen baseline parameters used here

- Base review rate: top 1.00% of validation scores.
- Soft congestion review rate: top 0.75%.
- Hard congestion review rate: top 0.50%.
- Direct BLOCK rate: top 0.10%.
- Capacity: 0.75 / 1.00 / 1.25 × validation base-review arrival rate.
- Queue discipline: FIFO.
- Adaptive learning rate: alpha = 0.15.
- Exploration: epsilon = 0.10.
- Congestion triggers: 24 / 72 backlog-hours.
- Dormancy: off in the core experiment.
- Reward scale: validation-fraud median Value = 400,000.

These are research scenario settings, not empirical bank rules.

## Mean results over 50 seeds

| Fraudster | Policy | Capacity | Fraud intercept | Fraud exposure at horizon | Backlog | Legit intervention |
|---|---|---:|---:|---:|---:|---:|
| Static | Fixed | 0.75 | 75.84% | 2,679,456 | 47.12 | 0.965% |
| Static | Fixed | 1.00 | 79.56% | 2,143,456 | 30.72 | 0.965% |
| Static | Fixed | 1.25 | 81.44% | 1,840,456 | 24.14 | 0.965% |
| Static | Capacity-aware | 0.75 | 74.12% | 2,648,056 | 28.20 | 0.822% |
| Static | Capacity-aware | 1.00 | 78.08% | 2,160,056 | 23.36 | 0.911% |
| Static | Capacity-aware | 1.25 | 82.48% | 1,458,056 | 19.36 | 0.934% |
| Adaptive | Fixed | 0.75 | 59.64% | 1,215,327 | 52.86 | 0.965% |
| Adaptive | Fixed | 1.00 | 64.40% | 964,327 | 32.68 | 0.965% |
| Adaptive | Fixed | 1.25 | 66.04% | 861,327 | 25.78 | 0.965% |
| Adaptive | Capacity-aware | 0.75 | 56.44% | 1,250,347 | 28.00 | 0.805% |
| Adaptive | Capacity-aware | 1.00 | 61.88% | 1,002,347 | 24.12 | 0.902% |
| Adaptive | Capacity-aware | 1.25 | 66.84% | 714,347 | 19.96 | 0.932% |

## Strategy shift

Static fraudster keeps the validation-derived mixture.

Mean low-value share:
- Static: about **36.8%**.
- Adaptive: about **88.7%**.

So the adaptive mechanism consistently shifts toward the lower-value/lower-score regime.

This is not a claim about real Xente fraudster cognition. It is the response of the specified learning rule to the empirical strategy pools and policy feedback.

## RQ1 — Static vs Adaptive

Across policy/capacity settings, Adaptive has a lower fraud-intercept rate than Static by roughly **14–17 percentage points**.

However, Adaptive also has lower total fraud exposure value because it concentrates on lower-value strategies.

Therefore:

> adaptation cannot be evaluated using fraud-count metrics alone.

The model generates a genuine metric conflict:
- fewer adaptive attempts are intercepted;
- but the adaptive attempts are also smaller in value.

Final reporting must keep both count-based and value-based outcomes.

## RQ2 — Fixed vs Capacity-aware

The most stable effect is operational.

Capacity-aware reduces backlog relative to Fixed by approximately:
- Static: 18.9 / 7.4 / 4.8 cases at Low / Medium / High capacity.
- Adaptive: 24.9 / 8.6 / 5.8 cases.

It also reduces legitimate intervention, especially under Low capacity.

The fraud-interception effect is much less certain. Paired seed contrasts often cross zero:
- Static Low: about -1.7 percentage points.
- Static High: about +1.0 percentage point.
- Adaptive Low: about -3.2 percentage points.
- Adaptive High: about +0.8 percentage point.

Therefore the current evidence supports:

> Capacity-aware routing robustly changes workload/congestion, but its fraud-control benefit is conditional rather than universally positive.

## RQ3 — Capacity

Increasing normalized analyst capacity consistently:
- reduces backlog;
- raises fraud interception;
- reduces unresolved exposure at the finite horizon.

This pattern appears under both fraudster modes and both policies.

## Monte Carlo convergence

At 50 seeds, maximum relative MCSE across the 12 configurations is approximately:

- fraud intercept rate: **1.6%**;
- backlog: **1.1%**;
- legitimate intervention rate: **0.3%**;
- fraud exposure at horizon: **7.3%**.

Decision:

> 50 seeds are sufficient for the main count/operational outcomes. Value exposure remains heavier-tailed, so final reporting must include uncertainty intervals rather than only the mean.

## Claim boundary

This run does **not** show:
- a real-bank optimal policy;
- true fraudster preferences;
- realistic bank staffing values;
- universal superiority of Capacity-aware.

It supports a conditional system-level claim:

> Under the Xente-grounded feature-level simulation, adaptive behavior changes both the composition and detectability of fraud attempts, while capacity-aware routing reliably reduces operational congestion but can trade off fraud interception depending on capacity and adversarial behavior.

## Remaining Xente robustness before final thesis lock

1. Degraded-score robustness on the feature-level loop.
2. Latest full test suite must pass.
3. Report the targeted alpha / epsilon / BLOCK / congestion sensitivity.
