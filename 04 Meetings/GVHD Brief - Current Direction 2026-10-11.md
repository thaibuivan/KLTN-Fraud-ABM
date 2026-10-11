# GVHD Brief — Current Direction — 2026-10-11

## 1. What I am studying

I am using ABM as a **policy experimentation / stress-testing environment** for transaction-fraud management.

The thesis is not primarily about building the highest-AUC classifier.

## 2. Why ABM

The system contains persistent state and feedback:

- customer/fraud transaction history;
- adaptive fraud behavior;
- alert queues;
- limited analyst capacity;
- backlog and waiting time;
- policy decisions that affect future system state.

If the final model collapses to transaction -> score -> threshold -> cost, the ABM label should be reconsidered.

## 3. Proposed model

```text
Customer / Fraudster
        ↓
Transactions
        ↓
Detection System
        ↓
Approve / Step-up / Review / Block
                   ↓
               Alert Queue
                   ↓
                Analyst
                   ↓
                Outcome

Fraudster observes response -> updates strategy -> next transaction
```

## 4. Main research question

> How do alternative transaction-fraud management policies perform under adaptive fraudster behavior and analyst capacity constraints?

## 5. Data

Current core scenarios:
- IEEE-CIS;
- Xente.

They are treated as separate empirical environments, not merged.

## 6. Policies to compare

- Fixed threshold.
- Cost-sensitive.
- Capacity-aware.

## 7. Core experiments

1. Static vs adaptive fraudster.
2. Policy comparison.
3. Analyst-capacity stress test.

## 8. Current methodological concern

The difficult part is not only coding agents. It is identifying mechanisms and classifying parameters correctly:

- empirical parameters;
- literature-informed operational parameters;
- policy variables;
- uncertain behavioral assumptions.

The goal is not to claim one perfectly calibrated parameter vector, but to test whether policy conclusions remain robust over plausible parameter ranges.

## 9. Questions for supervisor

1. Is policy experimentation the right central framing?
2. Is adaptive fraudster best treated as a stress mechanism rather than the main research output?
3. Are IEEE-CIS + Xente sufficient as the core empirical scope?
4. Is customer/fraudster/analyst + persistent queue enough to justify ABM?
5. Is fixed vs cost-sensitive vs capacity-aware a reasonable policy set?
6. Should behavioral parameters be handled mainly by sensitivity analysis rather than aggressive calibration?
