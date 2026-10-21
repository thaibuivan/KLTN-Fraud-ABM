> **HISTORICAL INTEGRATION PILOT — superseded for the core model by the feature-level rescored Xente mechanism.**\n> Keep this file as evidence that the first closed-loop feedback architecture worked. Do not use its score-template / raw-threshold-increment settings as the final core specification.\n\n# Xente Static–Adaptive Integration Pilot v0.1

## Status

**Executed closed-loop integration pilot — NOT final thesis result.**

This is the first run where:
- empirical Xente score/value templates;
- Static vs Adaptive fraudster behavior;
- Fixed vs Capacity-aware policy;
- persistent analyst queue;
- feedback from policy response;

operate in one loop.

## Purpose

The goal is not to estimate a real fraudster strategy.

The goal is to verify whether the thesis mechanism can produce the feedback channel:

```text
fraud strategy
→ score/value regime
→ policy response
→ queue pressure
→ reward
→ next strategy
```

## Empirical fraud-template design

To avoid using test fraud outcomes to define strategies, the pilot uses **validation fraud observations only**.

Validation frauds:
- 39 total.

They are divided by observed `Value` terciles into three stress regimes:

| Strategy regime | n | Median Value | Median risk score |
|---|---:|---:|---:|
| low_value | 14 | 100,000 | 0.0392 |
| medium_value | 13 | 500,000 | 0.1962 |
| high_value | 12 | 2,450,000 | 0.7074 |

Important boundary:

> The labels low/medium/high value are simulation regimes built from observed fraud templates. They are not claims that Xente identifies real fraudster cognition or explicit strategy switching.

## Static comparator

Static behavior is **not one arbitrarily fixed strategy**.

It draws from the empirical validation strategy mixture with fixed probabilities and does not react to APPROVE/REVIEW/BLOCK.

This isolates feedback adaptation more cleanly.

## Adaptive mechanism

Baseline pilot:
- epsilon-greedy;
- learning rate = 0.15;
- epsilon = 0.10;
- APPROVE reward = transaction Value;
- REVIEW reward = -0.15 × Value;
- BLOCK reward = -1.0 × Value.

Direct block is effectively disabled in this pilot because `block_threshold=1.0`.

These behavioral parameters are assumptions and must be sensitivity-tested.

## Operational settings

Same as integrated policy replay:
- validation review target = 1%;
- frozen review threshold ≈ 0.014801;
- Low / Medium / High capacity = 0.75 / 1.00 / 1.25 × validation reference service rate;
- queue discipline = risk-priority;
- Capacity-aware congestion triggers = 24h / 72h backlog-hours;
- threshold increments = +0.05 / +0.10.

## 30-seed pilot results

### Successful approved fraud value

| Fraudster | Policy | Capacity | Mean successful fraud value | SD |
|---|---|---:|---:|---:|
| Static | Fixed | 0.75 | 107,205 | 73,885 |
| Static | Fixed | 1.00 | 107,205 | 73,885 |
| Static | Fixed | 1.25 | 107,205 | 73,885 |
| Adaptive | Fixed | 0.75 | 264,948 | 97,976 |
| Adaptive | Fixed | 1.00 | 264,948 | 97,976 |
| Adaptive | Fixed | 1.25 | 264,948 | 97,976 |
| Static | Capacity-aware | 0.75 | 1,012,205 | 258,261 |
| Static | Capacity-aware | 1.00 | 867,205 | 250,375 |
| Static | Capacity-aware | 1.25 | 675,538 | 231,342 |
| Adaptive | Capacity-aware | 0.75 | 1,995,015 | 241,446 |
| Adaptive | Capacity-aware | 1.00 | 1,356,632 | 211,436 |
| Adaptive | Capacity-aware | 1.25 | 1,138,315 | 205,094 |

### Strategy composition

Static mixture remains near:
- low-value ≈ 34.4%;
- medium-value ≈ 33.5%;
- high-value ≈ 32.1%.

Adaptive behavior shifts strongly toward:
- low-value ≈ 89%;
- medium/high ≈ 5–6% each.

## What the pilot demonstrates

### 1. The feedback mechanism is operational

Adaptive behavior does not stay at the historical mixture.

Under this reward structure and these empirical template pools, it learns to favor the lower-value/lower-score regime.

### 2. Static policy evaluation can become optimistic

Under Fixed policy:
- Static mean successful fraud value ≈ 107k;
- Adaptive ≈ 265k.

This is an **adaptation penalty** in the pilot.

### 3. Naive capacity-aware threshold raising can create an evasion channel

Capacity-aware policy reduces workload by raising the review threshold under congestion.

But that also makes low-score fraud templates easier to approve.

The adaptive fraudster then concentrates on the low-value regime.

At Low capacity:
- Static Capacity-aware mean successful fraud value ≈ 1.01m;
- Adaptive Capacity-aware ≈ 2.00m.

This is exactly the type of adversarial-policy interaction the thesis intends to stress-test.

## Very important limitation

Do **not** treat these numbers as final thesis findings.

The magnitude is highly assumption-dependent because:
1. only 39 validation frauds define the template pools;
2. strategy is currently represented only by empirical Value/score regimes;
3. risk score is sampled jointly with Value rather than recomputed from a fully perturbed feature vector;
4. reward parameters are assumptions;
5. capacity-aware threshold increments are assumptions;
6. Xente has unusually strong Value/fraud separation.

Therefore the defensible conclusion at this stage is only:

> The closed-loop architecture works and shows that an adaptive adversary can exploit policy-induced changes in decision thresholds in a way that static replay cannot reveal.

## Design consequence

The next task is **not** to declare Capacity-aware inferior.

The next tasks are:
1. sensitivity-test the adaptation parameters;
2. sensitivity-test congestion thresholds/increments;
3. improve the Xente fraud generator from score/value-template replay toward feature-level empirical perturbation;
4. then freeze the final Xente mechanism before running the 12 core Xente configurations.

## Current status

Milestone achieved:

```text
Empirical Xente environment
+ policy
+ queue
+ Static/Adaptive fraudster
+ feedback
= first closed-loop pilot ✅
```
