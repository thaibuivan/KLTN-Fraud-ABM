# IEEE-CIS Executable Baseline Design v1.1

## Status

**Executed.** This is the Scenario B executable baseline translated from the completed IEEE EDA. It is not a new EDA pass.

## Why streaming execution

A first full-width batch materialization attempt exceeded the available working-memory envelope. The final executable path therefore preserves the same feature logic but computes it in bounded chunks.

Canonical runner:
- `scripts/train_ieee_streaming_baseline.py`

The older `build_ieee_features.py` remains useful as a readable feature specification / high-memory path, but it is not the preferred execution route for the full 590,540-row dataset.

## Persistent entity proxy

Core proxy:

```text
entity_proxy = card1 + addr1
```

From prior EDA:
- 39,974 unique proxies;
- median 2 transactions/proxy;
- P95 45;
- max 9,928;
- 3,439 fraud proxy entities;
- about 32% cold-start at first observed fraud.

Boundary:

> This is an entity proxy, not a true CustomerId.

## Past-only entity state

Streaming features:
- prior_tx_count;
- prior_amount_mean/std;
- gap_seconds;
- prior same-product share;
- cold_start_entity.

Each row is scored from state **before** the current event updates the proxy state.

## Detection context

Current/interpretable context:
- TransactionAmt;
- ProductCD;
- card1/card4/card6;
- addr1/dist1;
- P/R email;
- identity availability;
- DeviceType / DeviceInfo;
- selected id fields.

Masked detector context:
- C1-C14;
- D1-D15;
- M1-M9;
- selected V fields from prior EDA.

Boundary:
- masked features support risk scoring;
- they are not interpreted as fraudster actions.

## Missingness

Explicit:
- identity_available;
- identity_missing_count;
- detector_missing_count;
- email_both_missing;
- email_match.

## Encoding

Train-only high-cardinality frequency encoding:
- card1;
- entity_proxy;
- DeviceInfo;
- id_31;
- id_33;
- P/R email domains.

Low-cardinality context:
- fixed train-only categorical vocabulary;
- sparse one-hot encoding.

Numeric features:
- train-only StandardScaler fitted incrementally;
- NaNs are mapped to the standardized mean (0) after scaling.

## Temporal design

Use only labelled IEEE training data:

```text
first 70% chronological  -> train
next 15%                -> validation
final 15%               -> test
```

TransactionDT remains relative time.

## Baseline model

Streaming `SGDClassifier(loss="log_loss")`.

Frozen pilot regularization:
- alpha = **1e-3**

Reason:
- the earlier alpha = 1e-5 pilot produced severe 0/1 probability saturation in the validation tail;
- alpha = 1e-3 improved ranking/calibration and produced a usable continuous score tail for policy thresholds.

Classifier novelty is not the contribution.

## Executed metrics

| Split | Rows | Fraud | PR-AUC | ROC-AUC | Brier | Mean predicted p |
|---|---:|---:|---:|---:|---:|---:|
| Validation | 88,581 | 3,042 | 0.3644 | 0.8218 | 0.02840 | 0.0653 |
| Test | 88,581 | 3,083 | 0.3840 | 0.8219 | 0.03370 | 0.0946 |

Test fraud rate is about 3.48%, while mean predicted probability is 9.46%.

Interpretation:
- ranking is materially useful but much weaker than Xente;
- calibration drifts forward in time;
- this is exactly the richer / less separable environment wanted for Scenario B;
- policy thresholds should remain validation-tail calibrated rather than treated as universal probability cutoffs.

## 1% operating point

Validation:
- reviewed 886;
- fraud reviewed 663;
- precision 74.8%;
- recall 21.8%.

Test:
- reviewed 886;
- fraud reviewed 707;
- precision 79.8%;
- recall 22.9%.

## Outputs

- validation_scores.csv;
- test_scores.csv;
- metrics.json;
- model_bundle.joblib.

## Next

1. integrated Fixed vs Capacity-aware replay;
2. IEEE feature-level fraud strategy generator using interpretable context only;
3. reuse Static / Adaptive learning and normalized reward semantics from Xente.
