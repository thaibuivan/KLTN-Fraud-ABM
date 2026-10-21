# Xente Feature-Level Sensitivity v0.1

## Status

**Targeted one-factor-at-a-time sensitivity on the feature-level closed loop.**

Purpose:
- avoid full factorial explosion;
- identify which uncertain assumptions materially change conclusions;
- freeze a central Xente configuration only after checking nearby alternatives.

Each sensitivity setting uses 10 seeds.

## Central configuration

- BLOCK validation rate: 0.10%.
- alpha: 0.15.
- epsilon: 0.10.
- congestion triggers: 24 / 72 backlog-hours.
- Medium capacity for BLOCK / alpha / epsilon checks.
- Low capacity for congestion-trigger checks.

## 1. BLOCK-rate sensitivity

Tested:
- 0.05%;
- 0.10%;
- 0.20%.

### Medium capacity — Fixed policy

| Fraudster | BLOCK rate | Fraud intercept | Exposure at horizon |
|---|---:|---:|---:|
| Static | 0.05% | 75.6% | 3,574,408 |
| Static | 0.10% | 78.4% | 2,004,408 |
| Static | 0.20% | 82.8% | 574,408 |
| Adaptive | 0.05% | 59.2% | 1,157,419 |
| Adaptive | 0.10% | 62.0% | 1,037,419 |
| Adaptive | 0.20% | 63.6% | 797,419 |

Interpretation:
- absolute fraud-control outcomes are sensitive to direct BLOCK aggressiveness;
- therefore BLOCK must remain an explicit policy parameter;
- 0.10% is retained as the central nested threshold, not an empirical optimum.

## 2. Learning-rate sensitivity

Tested alpha:
- 0.05;
- 0.15;
- 0.30.

Adaptive low-value share remains approximately:
- 88.4%;
- 89.6%;
- 90.0%.

Fraud-intercept and exposure metrics change only slightly over this range.

Interpretation:

> the current qualitative adaptive shift is not driven by one narrow alpha value.

Central alpha = 0.15 is retained.

## 3. Exploration sensitivity

Tested epsilon:
- 0.05;
- 0.10;
- 0.20.

Adaptive low-value share under Fixed policy:
- epsilon 0.05: about 93.2%;
- epsilon 0.10: about 89.6%;
- epsilon 0.20: about 84.4%.

At Medium capacity under Fixed policy, fraud exposure rises from about:
- 847k;
- 1.04m;
- 1.32m.

Interpretation:
- epsilon materially affects strategy diversity and value exposure;
- it must be reported as a behavioral sensitivity parameter.

Central epsilon = 0.10 is retained.

## 4. Congestion-trigger sensitivity

Capacity-aware at Low capacity:

Tested soft/hard triggers:
- 12 / 48 h;
- 24 / 72 h;
- 48 / 120 h.

Adaptive results:

| Trigger | Fraud intercept | Exposure | Backlog | Legit intervention |
|---|---:|---:|---:|---:|
| 12/48 | 50.8% | 1,447,419 | 21.8 | 0.75% |
| 24/72 | 53.6% | 1,317,419 | 28.2 | 0.80% |
| 48/120 | 53.2% | 1,347,419 | 37.4 | 0.88% |

Interpretation:
- earlier congestion response clearly lowers backlog/intervention;
- fraud-control effects are not monotone enough to claim an optimum;
- 24/72 is kept as a central stress setting, with 12/48 and 48/120 as robustness bounds.

## Freeze decision

Central Xente parameters for the core run:

```text
BLOCK rate     = 0.10% validation tail
alpha          = 0.15
epsilon        = 0.10
soft trigger   = 24 backlog-hours
hard trigger   = 72 backlog-hours
capacity       = 0.75 / 1.00 / 1.25
queue          = FIFO
dormancy       = off
```

These values are **scenario settings**, not estimated truths.

## Main sensitivity conclusion

The most assumption-sensitive quantities are:
1. value exposure under BLOCK aggressiveness;
2. adaptive strategy composition under epsilon;
3. congestion/backlog under trigger timing.

The qualitative findings that:
- adaptation changes strategy composition;
- analyst capacity matters;
- Capacity-aware changes operational congestion;

remain present across the tested ranges.
