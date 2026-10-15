# Xente Integrated Policy Replay v0.1

## Status
**Executed empirical pre-adaptation pilot.**

This milestone uses the existing Xente raw data, the existing leakage-safe feature/risk pipeline, and the new shared policy + persistent queue engine. It is not the final adaptive-ABM result.

## Reproducibility check
| Split | Rows | Fraud | PR-AUC | ROC-AUC | Brier |
|---|---:|---:|---:|---:|---:|
| Validation | 14,349 | 39 | 0.560851 | 0.970573 | 0.001810 |
| Test | 14,350 | 50 | 0.892521 | 0.999664 | 0.001258 |

These reproduce the earlier Xente baseline, so the integrated work is still anchored to the same empirical score model.

## Core policy calibration
Base review target on validation: 1.00%, threshold = 0.014801.

Capacity-aware thresholds are validation-rate calibrated rather than raw probability increments:
- Base 1.00% -> 0.014801
- Soft 0.75% -> 0.026892
- Hard 0.50% -> 0.050961

This is the preferred cross-scenario specification because Xente and IEEE-CIS risk models can have different raw score scales.

Congestion state: backlog_hours = queue_size / pooled_service_rate_per_hour.
Pilot triggers: soft = 24h; hard = 72h. These are experimental stress parameters, not bank SLAs.

## Operational baseline
- Core queue discipline: FIFO.
- Structural robustness: risk-priority.
- Capacity normalization: validation base-review alert-arrival rate.
- Low / Medium / High = 0.75 / 1.00 / 1.25.
- BLOCK effectively off in this pre-adaptation pilot to isolate review routing.

## Results — FIFO baseline
| Capacity | Policy | Reviews | Backlog | Fraud intercept | Unresolved fraud | Fraud exposure at horizon | Legit intervention | Mean wait | P95 wait |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Low 0.75 | Fixed | 188 | 71 | 70% | 15 | 44,120,000 | 0.965% | 56.4 h | 78.8 h |
| Low 0.75 | Capacity-aware | 153 | 36 | 76% | 12 | 23,920,000 | 0.720% | 32.3 h | 58.8 h |
| Medium 1.00 | Fixed | 188 | 40 | 76% | 12 | 23,920,000 | 0.965% | 21.8 h | 44.2 h |
| Medium 1.00 | Capacity-aware | 174 | 31 | 80% | 10 | 17,960,000 | 0.867% | 18.6 h | 41.8 h |
| High 1.25 | Fixed | 188 | 32 | 82% | 9 | 15,000,000 | 0.965% | 12.6 h | 33.2 h |
| High 1.25 | Capacity-aware | 182 | 26 | 82% | 9 | 15,000,000 | 0.923% | 12.3 h | 33.1 h |

## Interpretation
Under this Xente score stream, capacity-aware routing reduces review load and backlog. The effect is largest under Low/Medium capacity. Under FIFO, removing some lower-priority review demand also allows more fraud alerts to receive analyst service before the finite horizon. At High capacity the two policies largely converge.

The defensible claim is conditional: in this Xente pre-adaptation replay, congestion-responsive review routing improves the fraud-interception/backlog/intervention trade-off under scarce capacity, while the advantage diminishes as capacity increases.

## Important limitation
Xente remains unusually easy for the score model because transaction Value is a dominant signal. Final policy conclusions must be repeated under degraded score quality.

## Decisions frozen from this pilot
- FIFO = core queue baseline.
- Risk-priority = structural robustness.
- Capacity = 0.75 / 1.00 / 1.25 of validation base-review arrival rate.
- Capacity-aware = validation-review-rate tiers, not absolute score increments.
- Backlog-hours = core congestion state.
- Pre-adaptation BLOCK = off.

## Still pending before final Xente experiment
1. Xente-grounded fraud template/generator.
2. Static fraudster full loop.
3. Adaptive fraudster full loop.
4. Explicit BLOCK calibration for adaptive feedback.
5. 12 final Xente configurations.
6. Degraded-score + alpha/epsilon sensitivity.