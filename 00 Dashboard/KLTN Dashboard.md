# KLTN Dashboard

## Current thesis direction

**Current framing (2026-10-11):**

> Dùng ABM như một môi trường thử nghiệm/stress-test chính sách quản lý gian lận giao dịch, trong đó fraudster có khả năng thích nghi với phản hồi hệ thống và fraud analyst có năng lực review hữu hạn.

### Main RQ

> **How do alternative transaction-fraud management policies perform under adaptive fraudster behavior and analyst capacity constraints?**

## What is current vs superseded

### Current master documents
- [[Current Direction - 2026-10-11]]
- [[Research Design v1.0 - Policy Experimentation]]
- [[Conceptual Model v1.0 - Adaptive Policy ABM]]
- [[Parameter Registry v0.2]]
- [[Two-Scenario Data Strategy v0.1]]
- [[Adaptive Policy Experiment Plan v0.1]]
- [[GVHD Brief - Current Direction 2026-10-11]]

### Earlier Xente-only direction
The older Xente queue/capacity documents are **not deleted**, because they contain real completed work, code, diagnostics and pilot results.

However, files such as:
- [[Research Design v0.2]]
- [[Candidate Core Specification v0.3]]
- [[Core Experiment Grid v0.1]]
- [[Conceptual Model v0.2]]
- [[GVHD Update - Xente Queue Milestone]]

are **superseded as project framing**.

Use them only to understand the previous Xente-only queue design or to reuse validated mechanisms.

See [[Repo Audit - 2026-10-11]].

## Work already completed

### A. Xente empirical groundwork
- Data audit completed.
- 95,662 labelled Xente transactions profiled.
- 193 fraud cases verified.
- 3,742 CustomerIds verified.
- Customer repetition and cold-start patterns documented.
- Strong Value/context signal documented.
- Leakage-safe past-only customer features implemented.

### B. Risk baseline
- Chronological 70/15/15 split implemented.
- Regularized logistic risk model implemented.
- Temporal instability checked.
- Full / no-current-value / amount-only score structures compared.

### C. Operational queue module
- Persistent event-driven alert queue implemented.
- FIFO and risk-priority implemented.
- Relative/fixed pooled capacity experiments implemented.
- Alert-threshold overload sensitivity implemented.
- Stochastic service-time sensitivity implemented.
- Variable team-capacity sensitivity implemented.
- Starvation/tail-wait diagnostics implemented.
- Queue verification tests implemented.

### D. Current ABM direction
- Current Research Design v1.0 drafted.
- Two-scenario strategy drafted: IEEE-CIS + Xente.
- Adaptive fraudster mechanism specified.
- Static-vs-adaptive smoke-test prototype implemented.
- Parameter Registry v0.2 drafted.
- Current supervisor brief drafted.

## Current conceptual model

```text
Customer --------\
                  \
                   -> Transactions -> Detection System -> APPROVE
Adaptive Fraudster/                           |           -> STEP-UP
                                             |           -> REVIEW -> Alert Queue -> Analyst
                                             |           -> BLOCK
                                             |
                                             +--> system response
                                                    |
                                                    v
                                            fraudster adaptation
```

### Feedback loops

1. **Adversarial loop:** action -> system response -> learning/adaptation -> next action.
2. **Operational loop:** policy -> alerts -> queue/backlog -> review delay/capacity -> system outcomes.

## Current data strategy

### Scenario A
IEEE-CIS — online/card/e-commerce environment.

### Scenario B
Xente — mobile/payment/e-commerce environment.

The two datasets are not merged.

## Current policy families

1. Fixed-threshold policy.
2. Cost-sensitive policy.
3. Capacity-aware policy.

## Core experiments

1. Static vs adaptive fraudster.
2. Policy comparison.
3. Analyst-capacity stress test.

## Parameter philosophy

Do not search for one "true" value for every parameter.

Classify each parameter as:
- empirical;
- literature-informed;
- policy variable;
- uncertain behavioral assumption.

Sensitivity-test uncertain parameters and mechanisms.

## Immediate blockers / open decisions

- GVHD confirmation of the final framing.
- Final decision on exact policy definitions.
- IEEE-CIS detailed audit for the current two-scenario framework.
- Final mapping from dataset variables to ABM states/parameters.
- Public grounding for adaptive-fraudster mechanisms where possible.
- Final decision on how much customer-friction/cost monetization to include.

## Immediate reading order

Open [[READING ORDER]].
