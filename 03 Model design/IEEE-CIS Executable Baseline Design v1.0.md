# IEEE-CIS Executable Baseline Design v1.0

## Status

Implementation design translated directly from the completed IEEE EDA. This is
not a new EDA pass.

## Persistent entity proxy

Core proxy:

```text
entity_proxy = card1 + addr1
```

Reason from prior EDA:
- 39,974 unique proxies;
- median 2 transactions/proxy;
- P95 45;
- max 9,928;
- 3,439 fraud proxy entities;
- 32% cold-start at first observed fraud.

Boundary:
> This is an entity proxy, not a true CustomerId.

## Past-only entity state

Executable features:
- prior_tx_count;
- prior_amount_mean/std;
- gap_seconds;
- prior same-product share;
- cold_start_entity.

All are calculated before the current event is added to state.

## Current transaction / detection context

Interpretable/current context:
- TransactionAmt;
- ProductCD;
- card1-card6;
- addr1/addr2;
- dist1/dist2;
- P/R email;
- identity availability;
- DeviceType / DeviceInfo;
- selected id fields.

Masked detector context:
- C1-C14;
- D1-D15;
- M1-M9;
- V45, V257, V44, V86, V87, V246, V244, V158, V242, V156,
  V149, V52, V51, V201, V200.

The selected V features come from the prior EDA separation screen.

Boundary:
- masked features may support risk scoring;
- they are not interpreted as fraudster actions.

## Missingness

Explicit features:
- identity_available;
- identity_missing_count;
- detector_missing_count;
- email_both_missing;
- email_match.

This follows the prior EDA finding that identity/missingness is not random with
respect to fraud label and also shifts over time.

## Encoding

High-cardinality fields are frequency-encoded using TRAIN ONLY:
- card1;
- entity_proxy;
- DeviceInfo;
- id_31;
- id_33;
- P/R email domains.

Low-cardinality context is one-hot encoded.

## Temporal design

Use only labelled IEEE training data for thesis evaluation:

```text
first 70% chronological  -> train
next 15%                -> validation
final 15%               -> test
```

TransactionDT remains relative time. No calendar-date interpretation is added.

## Baseline model

Regularized logistic regression.

Purpose:
- interpretable first probability score;
- common risk_probability interface for the shared policy engine;
- classifier novelty is not the thesis contribution.

Outputs:
- validation_scores.csv;
- test_scores.csv;
- metrics.json;
- model_bundle.joblib.

## Next after execution

1. inspect PR-AUC / calibration / temporal behavior;
2. run Fixed vs Capacity-aware policy replay;
3. define IEEE feature-level fraud strategy dimensions only from interpretable
   fields;
4. reuse the same Static / Adaptive learning mechanism and normalized capacity
   semantics as Xente.
