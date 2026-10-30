# Xente Baseline Risk Model — feasibility screen

## Purpose
Quick feasibility test on the uploaded Xente training data before building the queue/policy simulator.

This is **not** a final thesis result.

## Data split
Chronological 70/15/15:
- Train: 66,963 rows, 104 fraud
- Validation: 14,349 rows, 39 fraud
- Test: 14,350 rows, 50 fraud

## Leakage-safe features
No raw CustomerId/AccountId/SubscriptionId are used as predictors.

Current-transaction context:
- log(Value)
- debit/credit sign
- hour
- weekday
- PricingStrategy
- ProductCategory
- ChannelId
- ProviderId
- ProductId

Past-only customer history:
- prior transaction count
- prior mean/std Value
- gap since previous transaction
- rolling counts over 1h / 24h / 7d
- current Value relative to prior mean
- prior product/category share
- prior channel share

All history features are constructed using transactions **strictly before the current transaction**.

## Model
Regularized logistic regression:
- no class weighting in the baseline;
- one-hot categorical context;
- standardized numeric features.

Reason:
- interpretable;
- suitable for only 193 positive cases;
- probability output is easier to calibrate/use in policy logic than a heavily reweighted classifier.

## Screening performance

| Split | AP / PR-AUC | ROC-AUC | Brier |
|---|---:|---:|---:|
| Validation | **0.561** | **0.971** | **0.00181** |
| Test | **0.893** | **0.9997** | **0.00126** |

### Validation operating points
| Review rate | Reviewed | Fraud caught | Precision | Recall |
|---:|---:|---:|---:|---:|
| 0.5% | 71 | 27 | 38.0% | 69.2% |
| 1% | 143 | 35 | 24.5% | 89.7% |
| 2% | 286 | 37 | 12.9% | 94.9% |
| 5% | 717 | 37 | 5.2% | 94.9% |

### Test operating points
| Review rate | Reviewed | Fraud caught | Precision | Recall |
|---:|---:|---:|---:|---:|
| 0.5% | 71 | 50 | 70.4% | 100% |
| 1% | 143 | 50 | 35.0% | 100% |
| 2% | 287 | 50 | 17.4% | 100% |
| 5% | 717 | 50 | 7.0% | 100% |

## Interpretation
The very strong test ranking should **not** be treated as evidence of production-grade fraud detection.

Likely reasons:
- fraud transactions in Xente are strongly separated by transaction value;
- fraud is concentrated in specific product/provider/channel contexts;
- only 50 fraud cases are in the test period;
- temporal distribution differs across periods.

Therefore:
- use this model as a score generator for policy experiments;
- keep classifier comparison secondary;
- later report confidence intervals and temporal robustness;
- consider a deliberately simpler score model as structural sensitivity if policy conclusions become too dependent on near-perfect ranking.

## Decision
The dataset is feasible for the KLTN baseline.

Next implementation priority:
1. persistent alert queue;
2. pooled analyst service process;
3. FIFO vs risk-priority comparison;
4. policy outcomes under explicit capacity/review-time assumptions.
