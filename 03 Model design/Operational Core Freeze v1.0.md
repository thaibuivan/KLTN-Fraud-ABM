# Operational Core Freeze v1.0

## Purpose

Freeze the shared operational semantics before the final two-scenario experiments so later results are not changed by repeatedly redesigning the queue/policy layer.

## Queue discipline

- Core: **FIFO**.
- Robustness: **risk-priority**.

FIFO isolates the routing-policy effect. Risk-priority is a separate downstream service-allocation mechanism already studied in Xente pilots.

## Capacity normalization

Reference = validation alert-arrival rate under the base 1% review threshold.

- Low = 0.75 × reference service rate
- Medium = 1.00 × reference service rate
- High = 1.25 × reference service rate

These are normalized stress scenarios, not real-bank staffing values.

## Fixed policy

Base review threshold = scenario-specific validation threshold for top **1.0%** review rate.

## Capacity-aware policy

Same semantics in Xente and IEEE-CIS.

Validation-calibrated tiers:
- Base = top 1.00%
- Soft congestion = top 0.75%
- Hard congestion = top 0.50%

Congestion state:

```text
backlog_hours = queue_size / pooled_service_rate_per_hour
```

Central triggers:
- soft = 24 backlog-hours;
- hard = 72 backlog-hours.

Robustness:
- early response = 12 / 48;
- late response = 48 / 120.

## BLOCK

Core baseline:
- direct BLOCK threshold = validation top **0.10%** score tail.

Sensitivity:
- 0.05%;
- 0.10%;
- 0.20%.

This is not an empirical optimum. It is a nested scenario threshold chosen between review routing and extreme-risk intervention.

## Review / outcome semantics

- APPROVE fraud = immediately successful/exposed fraud.
- BLOCK fraud = prevented fraud.
- REVIEW enters the persistent queue.
- Fraud is counted as intercepted if analyst service starts within the observation horizon.
- Fraud still waiting at the horizon is **unresolved fraud exposure**, not automatically counted as realized loss.
- Core analyst review is perfect once service starts.
- Analyst error is robustness only if grounded.

Value metrics:
- successful_fraud_value;
- unresolved_fraud_value;
- fraud_exposure_at_horizon = successful + unresolved;
- prevented_fraud_value.

## Adaptive fraudster baseline

Shared learning form:

```text
V_s(new) = V_s(old) + alpha × (reward - V_s(old))
```

Central behavioral parameters:
- alpha = 0.15;
- epsilon = 0.10;
- dormancy = off in the core experiment.

Sensitivity:
- alpha = 0.05 / 0.15 / 0.30;
- epsilon = 0.05 / 0.10 / 0.20.

Reward uses normalized transaction value:

```text
normalized_value = transaction_value / scenario_reward_scale
```

Scenario reward scale:
- Xente = validation-fraud median Value;
- IEEE-CIS = corresponding pre-test fraud amount scale to be calibrated analogously.

This preserves the learning rule across scenarios without pretending their raw monetary units are directly comparable.

## Static comparator

Static comparator uses a fixed empirical strategy mixture and does not change future strategy probabilities after APPROVE / REVIEW / BLOCK.

This is preferred over one arbitrarily fixed strategy because the empirical fraud environment contains multiple regimes.

## Primary metrics

Fraud:
- fraud_intercept_rate;
- successful_fraud_value;
- unresolved_fraud_value;
- fraud_exposure_at_horizon;
- prevented_fraud_value.

Operations:
- review_count;
- backlog_end;
- mean/P95 waiting time.

Customer/intervention:
- legitimate_review_count;
- legitimate_block_count;
- legitimate_intervention_rate.

Behavior:
- strategy shares over time / by run.

## Cross-scenario rule

Raw risk probabilities may differ between Xente and IEEE-CIS.

Common policy semantics are therefore defined by:
- validation review-rate targets;
- normalized service capacity;
- backlog-hours;
- normalized reward scale;

not by identical raw probability thresholds or identical monetary scales.

## Freeze status

For Xente core:
- policy thresholds: frozen;
- capacity levels: frozen;
- FIFO baseline: frozen;
- alpha / epsilon baseline: frozen;
- congestion triggers: frozen;
- BLOCK baseline: frozen;
- unresolved-review semantics: frozen.

Remaining before full thesis lock:
- feature-level degraded-score robustness;
- IEEE-CIS scenario parameterization using the same shared semantics.
