# Xente Feature-Level Degraded-Score Robustness v0.1

## Status

**Executed structural robustness check on the feature-level closed loop.**

The same Static / Adaptive × Fixed / Capacity-aware × Low / Medium / High design was rerun with the deliberately weaker **no-current-value** Xente risk model.

This model removes the strongest current-transaction Value signals:
- `log_value`;
- `value_ratio_clip`.

Earlier empirical screening showed approximately:
- validation PR-AUC ≈ 0.205;
- test PR-AUC ≈ 0.389.

So this is a materially weaker score environment than the full Xente baseline.

## Recalibrated policy thresholds

Because policy semantics are defined by validation review-rate targets, thresholds were recalibrated on the degraded score distribution:

| Role | Threshold |
|---|---:|
| BLOCK top 0.10% | 0.130978 |
| Base review top 1.00% | 0.021552 |
| Soft review top 0.75% | 0.033446 |
| Hard review top 0.50% | 0.050234 |

Validation reference alert arrival rate:
- about **0.5449 alerts/hour**.

The policy meaning is therefore preserved without forcing raw score thresholds from the full model onto a weaker model.

## Experiment

- 30 seeds;
- 12 Xente core configurations;
- feature-level fraud generation;
- online synthetic fraudster history;
- generated fraud rescored by the degraded logistic model;
- FIFO queue;
- alpha = 0.15;
- epsilon = 0.10;
- BLOCK = top 0.10%;
- congestion triggers = 24 / 72 backlog-hours.

## Mean results

| Fraudster | Policy | Capacity | Fraud intercept | Exposure at horizon | Backlog | Legit intervention |
|---|---|---:|---:|---:|---:|---:|
| Static | Fixed | 0.75 | 87.60% | 5,251,653 | 50.10 | 1.18% |
| Static | Fixed | 1.00 | 87.60% | 5,251,653 | 37.10 | 1.18% |
| Static | Fixed | 1.25 | 90.00% | 3,233,252 | 30.03 | 1.18% |
| Static | Capacity-aware | 0.75 | 87.00% | 5,181,720 | 28.17 | 1.02% |
| Static | Capacity-aware | 1.00 | 89.00% | 3,761,686 | 26.00 | 1.11% |
| Static | Capacity-aware | 1.25 | 89.87% | 3,104,986 | 22.90 | 1.13% |
| Adaptive | Fixed | 0.75 | 67.27% | 2,999,096 | 59.27 | 1.18% |
| Adaptive | Fixed | 1.00 | 67.73% | 2,884,096 | 45.87 | 1.18% |
| Adaptive | Fixed | 1.25 | 72.80% | 2,448,096 | 37.20 | 1.18% |
| Adaptive | Capacity-aware | 0.75 | 68.93% | 3,176,779 | 34.00 | 1.01% |
| Adaptive | Capacity-aware | 1.00 | 73.33% | 2,770,779 | 32.20 | 1.10% |
| Adaptive | Capacity-aware | 1.25 | 77.47% | 2,405,096 | 28.40 | 1.13% |

## Adaptive strategy composition

Under the degraded model, Adaptive still concentrates on the low-value regime:

- Fixed: low-value share ≈ **82.1%**.
- Capacity-aware: low-value share ≈ **81.2%**.

This is lower than the roughly 88–89% low-value share under the full Xente score model, but the adaptive shift remains strong.

Therefore the adaptation effect is not only an artifact of copying or exploiting the full-model current Value score.

## Robust finding 1 — operational effect survives weaker scores

Capacity-aware continues to reduce backlog substantially.

Examples:

### Static
- Low: 50.1 → 28.2.
- Medium: 37.1 → 26.0.
- High: 30.0 → 22.9.

### Adaptive
- Low: 59.3 → 34.0.
- Medium: 45.9 → 32.2.
- High: 37.2 → 28.4.

So the main operational claim is robust:

> congestion-responsive routing changes workload/backlog even when score quality is materially weaker.

## Robust finding 2 — fraud-control policy effect is score-dependent

Under the full score model, the fraud-interception effect of Capacity-aware was small and often crossed zero.

Under the degraded model, Capacity-aware improves Adaptive fraud interception by about:
- +1.7 percentage points at Low capacity;
- +5.6 points at Medium;
- +4.7 points at High.

For Static behavior the effect remains close to neutral.

This is an important thesis result:

> the operational benefit of Capacity-aware is stable, but its fraud-control benefit depends on the quality/structure of the underlying risk score.

That is exactly why the thesis should evaluate the whole policy system rather than declare one routing policy universally optimal.

## Claim boundary

This robustness run does not establish a production policy recommendation.

It supports:
1. adaptive behavior still changes strategy composition under weaker scoring;
2. analyst capacity still matters;
3. Capacity-aware still reduces congestion;
4. the fraud-control ranking of policies can change with score quality.

## Consequence

The Xente main mechanism now has:
- feature-level generation and rescoring;
- 50-seed main run;
- targeted behavioral/policy sensitivity;
- degraded-score structural robustness.

The next major implementation task is the IEEE-CIS executable scenario pipeline.
