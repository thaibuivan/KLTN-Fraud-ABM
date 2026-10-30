# Xente Baseline Implementation Plan v0.1

## Goal
Biến Xente thành một empirical baseline có thể chạy được, nhưng **không migrate mù quáng code từ repo cũ**.

## Stage A — Local profile ✅
```bash
python scripts/profile_xente.py --input data/raw/xente/training.csv
```

Verified:
- 95,662 labelled transactions;
- 193 fraud;
- 3,742 CustomerIds;
- significant entity repetition and later cold-start.

## Stage B — Leakage-safe feature table ✅
```bash
python scripts/build_xente_features.py \
  --input data/raw/xente/training.csv \
  --output data/interim/xente_features.csv
```

Past-only features:
- prior transaction count;
- prior Value mean/std;
- gap since previous transaction;
- rolling 1h/24h/7d counts;
- current Value relative to prior customer mean;
- prior product/category share;
- prior channel share.

Rules:
- no future label statistics;
- no raw CustomerId as predictor;
- AccountId/SubscriptionId are not clean nested agents.

## Stage C — Risk engine baseline ✅
```bash
python scripts/train_xente_baseline.py \
  --input data/interim/xente_features.csv \
  --output-dir outputs/local/xente_baseline
```

Baseline:
- regularized logistic regression;
- chronological 70/15/15;
- validation/test scores saved for policy replay.

## Stage D — Persistent queue / policy replay ✅

Deterministic capacity stress:
```bash
python scripts/simulate_alert_queue.py \
  --validation-scores outputs/local/xente_baseline/validation_scores.csv \
  --test-scores outputs/local/xente_baseline/test_scores.csv \
  --target-alert-rate 0.01 \
  --capacity-ratios 0.75,1.0,1.25 \
  --service-cv 0 \
  --seeds 1
```

Stochastic service:
```bash
python scripts/simulate_alert_queue.py \
  --validation-scores outputs/local/xente_baseline/validation_scores.csv \
  --test-scores outputs/local/xente_baseline/test_scores.csv \
  --target-alert-rate 0.01 \
  --capacity-ratios 0.75,1.0,1.25 \
  --service-cv 0.5 \
  --seeds 100
```

## Stage E — Risk-model robustness ✅
```bash
python scripts/run_xente_model_robustness.py \
  --input data/interim/xente_features.csv
```

Models:
- full logistic;
- no current Value;
- amount-only.

## Stage F — Temporal robustness ✅
```bash
python scripts/run_xente_temporal_robustness.py \
  --input data/interim/xente_features.csv
```

Expanding-window evaluation from 50%→60% through 90%→100%.

## Stage G — Fixed-capacity alert-rate sensitivity ✅
Use score files from the chosen model:

```bash
python scripts/run_alert_rate_sensitivity.py \
  --validation-scores outputs/local/xente_baseline/validation_scores.csv \
  --test-scores outputs/local/xente_baseline/test_scores.csv \
  --alert-rates 0.005,0.01,0.02,0.05 \
  --reference-alert-rate 0.01 \
  --capacity-ratios 0.75,1.0,1.25
```

Important:
absolute pooled service capacity is anchored to the reference validation load and held fixed across thresholds.

Outputs include:
- backlog;
- fraud capture;
- mean/P95/P99 wait;
- >24/48/72h wait shares;
- low/high-priority tail wait.

## Stage H — Verification ✅
```bash
pytest -q
```

Current:
**5 queue verification tests passed.**

## Stage I — Structural validation
Prepared:
- [[Practitioner Validation Questions v0.1]]
- [[GVHD Update - Xente Queue Milestone]]

Next:
1. collect practitioner feedback;
2. collect GVHD scope feedback;
3. decide aging/expiry/hybrid priority;
4. freeze final experiment grid.

## Definition of done for core MVP

- [x] raw Xente outside Git;
- [x] past-only chronological features;
- [x] holdout risk scores;
- [x] persistent backlog;
- [x] FIFO/risk-priority on same event stream;
- [x] alerts/FP/backlog/wait/workload outputs;
- [x] multiple seeds;
- [x] weaker score-model sensitivity;
- [x] fixed-capacity threshold sensitivity;
- [x] starvation diagnostics;
- [x] verification tests;
- [ ] practitioner workflow validation completed or documented unavailable;
- [ ] final core mechanism frozen.

## What NOT to build yet
- LLM analyst;
- adaptive fraudster cognition;
- full Mesa UI;
- dashboard;
- complex game-theoretic equilibrium;
- second full dataset implementation.
