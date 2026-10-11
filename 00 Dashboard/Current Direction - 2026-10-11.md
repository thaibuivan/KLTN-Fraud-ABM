# Current Direction — 2026-10-11

## One-sentence thesis framing

Use **Agent-Based Modelling (ABM) as a policy laboratory** to stress-test transaction-fraud management policies in a dynamic system where fraudsters can adapt to system feedback and fraud analysts have limited review capacity.

## Current status

This is the **current working direction for supervisor discussion**. It extends, rather than deletes, the earlier Xente queue/capacity work already in this repository.

### Core research logic

- **Research objective:** policy experimentation / stress testing.
- **ABM:** research instrument.
- **Adaptive fraudster:** stress mechanism.
- **Analyst capacity + alert queue:** operational constraint and feedback mechanism.
- **ML risk model:** a component of the detection system, not the thesis end-goal.
- **Empirical grounding:** public fraud datasets + literature + explicit assumptions.

## Main research question

> How do alternative transaction-fraud management policies perform under adaptive fraudster behavior and analyst capacity constraints?

## Sub-questions

1. How does adaptive fraudster behavior change policy effectiveness relative to static fraud behavior?
2. What trade-offs do different policies create among fraud loss, false positives, customer friction and analyst workload?
3. How do analyst capacity and parameter uncertainty affect policy robustness?

## Current conceptual architecture

```text
Customer --------                                     -> Transaction -> Detection System -> APPROVE
Adaptive Fraudster/                         |           -> STEP-UP
                                           |           -> REVIEW -> Alert Queue -> Analyst
                                           |           -> BLOCK
                                           |
                                           +--> response observed by fraudster
                                                  |
                                                  v
                                          strategy adaptation
```

Two dynamic feedback loops matter:

1. **Adversarial loop:** fraudster action -> system response -> adaptation -> next action.
2. **Operational loop:** alert policy -> queue -> backlog/delay -> loss/workload -> policy outcomes.

## Current data direction

### Scenario A — IEEE-CIS
Online / card / e-commerce transaction environment.

### Scenario B — Xente
Mobile/payment/e-commerce environment in Uganda.

Important: the two datasets are **not merged**. Each independently parameterizes the same conceptual framework.

Xente use has been explicitly permitted by Zindi for thesis use with attribution and acknowledgement.

## Current policy families

1. Fixed-threshold policy.
2. Cost-sensitive policy.
3. Capacity-aware policy.

## Main experiments

1. Static vs adaptive fraudster.
2. Fixed vs cost-sensitive vs capacity-aware policy.
3. Analyst-capacity stress test.

## Claim boundary

The model will not be described as a digital twin, a production fraud system, or direct policy advice for a specific bank. Conclusions are conditional on the evaluated scenarios, assumptions and plausible parameter ranges.

## Immediate next milestone

Before full ABM implementation:
1. freeze research design after supervisor feedback;
2. audit IEEE-CIS and Xente for usable state/parameter grounding;
3. complete the parameter registry;
4. implement a minimal end-to-end simulation;
5. add adaptive fraudster only after the baseline pipeline is verified.
