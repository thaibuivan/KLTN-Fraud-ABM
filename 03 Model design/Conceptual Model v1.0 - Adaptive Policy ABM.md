# Conceptual Model v1.0 — Adaptive Policy ABM

## Model purpose

The model is a **policy experimentation / stress-testing environment**.

It is not designed to reproduce one real bank exactly.

## Core entities and modules

### Customer agent
Persistent state may include:
- transaction history;
- recent frequency/velocity;
- recent amount statistics;
- channel/product history;
- accumulated intervention/friction state if needed by an RQ.

Action:
- generate or replay legitimate transactions.

### Fraudster agent
Persistent state:
- current strategy;
- strategy values/preferences;
- recent success;
- recent system responses;
- repeated-block counter;
- optional dormancy state.

Action:
- choose a strategy and generate a fraud transaction.

Adaptation:
- observe APPROVE / STEP-UP / REVIEW / BLOCK;
- update strategy preference;
- alter future behavior.

### Detection system
A component/module rather than necessarily an agent.

Input:
- transaction features;
- past-only state/features.

Output:
- fraud-risk score;
- rule triggers if rule layer is used.

### Policy layer
Maps current information to an action.

Candidate actions:
- APPROVE;
- STEP-UP;
- REVIEW;
- BLOCK.

Candidate policy families:
1. fixed threshold;
2. cost-sensitive;
3. capacity-aware.

### Alert queue
Persistent state:
- alert arrivals;
- priority;
- waiting time;
- backlog;
- service status.

Candidate queue disciplines:
- FIFO;
- risk-priority;
- later hybrid/aging only if justified.

### Fraud analyst
Core abstraction:
- pooled or agent-level review capacity;
- service process;
- review outcome if analyst decision error is modeled.

Individual analyst heterogeneity is not required for the first implementation.

---

## System flow

```text
LEGITIMATE CUSTOMER
        |
        v
legitimate transaction
        |
        +----------------------+
                               |
                               v
                        DETECTION SYSTEM
                               |
ADAPTIVE FRAUDSTER             |
        |                      |
        v                      |
fraud transaction -------------+
                               |
                               v
                         POLICY LAYER
                               |
              +----------------+----------------+
              |                |                |
           APPROVE          STEP-UP          BLOCK
              |
              +---------- REVIEW
                           |
                           v
                      ALERT QUEUE
                           |
                           v
                    FRAUD ANALYST
                           |
                           v
                        OUTCOME
                           |
                           v
        fraud loss / FP / workload / delay / cost
```

## Adversarial feedback loop

```text
fraudster action
      ↓
system response
      ↓
reward / penalty
      ↓
strategy-value update
      ↓
future strategy choice
```

This feedback loop is what turns adaptive fraudster behavior into a stress mechanism.

## Operational feedback loop

```text
policy threshold / action rule
      ↓
alert arrivals
      ↓
queue / backlog
      ↓
waiting time / service pressure
      ↓
review outcomes and system metrics
```

A capacity-aware policy may additionally observe queue/capacity state before making the next action decision.

## Simulation time

The current preferred design is event-driven or fine-grained chronological processing because transaction ordering and queue waiting matter.

For Xente:
- observed transaction replay can be used for the empirical baseline.

For counterfactual adaptive-fraudster experiments:
- fraud events may be generated/perturbed while maintaining scenario-specific empirical distributions.

For IEEE-CIS:
- exact implementation depends on the final data audit because persistent customer identity is less directly observed.

## State-transition view

At time/event t:

1. Customer/fraudster produces a transaction.
2. Detection system computes risk information.
3. Policy selects an action.
4. REVIEW action adds an alert to the persistent queue.
5. Analyst capacity serves available alerts.
6. Outcomes and metrics are recorded.
7. Customer/queue/fraudster states update.
8. Next event is processed.

## Why this may justify ABM

The ABM label is justified only if the final implementation retains:
- persistent agent state;
- heterogeneous behavior;
- feedback between actions and future behavior;
- interaction through shared operational resources such as the queue.

If adaptive behavior is removed and only a fixed empirical score stream is replayed through a queue, the more conservative label **dynamic/discrete-event policy simulation** remains valid.

## Minimum viable ABM

Do not begin with all complexity.

### MVP 0
Transaction -> risk -> policy -> queue -> analyst -> metrics.

### MVP 1
Add persistent customer state / empirical history.

### MVP 2
Add static fraudster comparator.

### MVP 3
Add adaptive fraudster.

### MVP 4
Compare policy families.

### MVP 5
Sensitivity and robustness.

## Claim boundary

The model may support conditional statements about:
- policy trade-offs;
- congestion;
- adaptation stress;
- robustness.

It must not claim:
- exact fraudster cognition;
- a digital twin;
- production thresholds;
- bank-specific staffing requirements without evidence.
