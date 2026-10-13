# Operational Core Freeze v1.0

## Purpose
Freeze the shared operational semantics before adaptive-fraudster integration so later results are not changed by repeatedly redesigning the queue/policy layer.

## Queue discipline
- Core: FIFO.
- Robustness: risk-priority.

FIFO isolates the routing-policy effect. Risk-priority is a separate downstream service-allocation mechanism already studied in Xente pilots.

## Capacity normalization
Reference = validation alert-arrival rate under the base 1% review threshold.
- Low = 0.75 × reference service rate
- Medium = 1.00 × reference service rate
- High = 1.25 × reference service rate

These are normalized stress scenarios, not real-bank staffing values.

## Fixed policy
Base review threshold = scenario-specific validation threshold for top 1.0% review rate.

## Capacity-aware policy
Same semantics in Xente and IEEE-CIS.
Validation-calibrated tiers:
- Base = top 1.00%
- Soft congestion = top 0.75%
- Hard congestion = top 0.50%

Congestion state: backlog_hours = queue_size / pooled_service_rate_per_hour.
Core pilot triggers: soft = 24 backlog-hours; hard = 72 backlog-hours.
Trigger values remain sensitivity parameters.

## BLOCK
Pre-adaptation replay: block effectively off to isolate review routing.
Adaptive final loop: BLOCK must be explicitly calibrated before the final 24-config run because fraudster feedback requires a response stronger than REVIEW.

## Review semantics
- REVIEW enters persistent queue.
- Fraud is intercepted if analyst service starts within the observation horizon.
- Fraud still waiting at the horizon is unresolved fraud exposure.
- Analyst review is perfect in the core baseline.
- Analyst error is robustness/sensitivity only if grounded.

## Primary metrics
Fraud: fraud_intercept_rate, prevented_fraud_value, successful_fraud_value, unresolved_fraud_value, fraud_exposure_at_horizon.
Operations: review_count, backlog_end, mean/P95 waiting time.
Customer/intervention: legitimate_review_count, legitimate_block_count, legitimate_intervention_rate.

## Cross-scenario rule
Raw risk probabilities may differ between Xente and IEEE-CIS. Common policy semantics are therefore defined by validation review-rate targets, normalized service capacity and backlog-hours, not identical raw probability thresholds.