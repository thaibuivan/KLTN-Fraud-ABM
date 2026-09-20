# Xente Baseline Implementation Plan v0.1

## Goal
Biến Xente thành một empirical baseline có thể chạy được, nhưng **không migrate mù quáng code từ repo cũ**.

## Stage A — Local profile ✅
Input:
`data/raw/xente/training.csv`

Run:
```bash
python scripts/profile_xente.py --input data/raw/xente/training.csv
```

Verified:
- 95,662 labelled transactions;
- 193 fraud;
- 3,742 CustomerIds;
- significant entity repetition and later cold-start.

## Stage B — Leakage-safe feature table ✅
Run:
```bash
python scripts/build_xente_features.py \
  --input data/raw/xente/training.csv \
  --output data/interim/xente_features.csv
```

Current past-only customer features include:
- prior transaction count;
- prior Value mean/std;
- gap since previous transaction;
- rolling 1h/24h/7d counts;
- current Value relative to prior customer mean;
- prior product/category share;
- prior channel share.

Important:
- no future label statistics;
- no raw CustomerId as a predictor;
- AccountId/SubscriptionId are not treated as clean nested agents.

## Stage C — Risk engine baseline ✅
Run:
```bash
python scripts/train_xente_baseline.py \
  --input data/interim/xente_features.csv \
  --output-dir outputs/local/xente_baseline
```

Baseline:
- regularized logistic regression;
- chronological 70/15/15;
- validation/test score files saved for policy replay.

## Stage D — Persistent queue / policy replay ✅
Run deterministic:
```bash
python scripts/simulate_alert_queue.py \
  --validation-scores outputs/local/xente_baseline/validation_scores.csv \
  --test-scores outputs/local/xente_baseline/test_scores.csv \
  --target-alert-rate 0.01 \
  --capacity-ratios 0.75,1.0,1.25 \
  --service-cv 0 \
  --seeds 1
```

Run stochastic:
```bash
python scripts/simulate_alert_queue.py \
  --validation-scores outputs/local/xente_baseline/validation_scores.csv \
  --test-scores outputs/local/xente_baseline/test_scores.csv \
  --target-alert-rate 0.01 \
  --capacity-ratios 0.75,1.0,1.25 \
  --service-cv 0.5 \
  --seeds 100
```

Queue:
- persistent backlog;
- FIFO vs risk-priority;
- seen/unseen fraud capture;
- waiting-time distribution;
- relative pooled capacity.

## Stage E — Risk-model robustness ✅
Run:
```bash
python scripts/run_xente_model_robustness.py \
  --input data/interim/xente_features.csv
```

Models:
- full logistic;
- no current Value signal;
- amount-only baseline.

Purpose:
test whether policy conclusions depend on an unusually easy Xente score model.

## Stage F — Temporal robustness ✅
Run:
```bash
python scripts/run_xente_temporal_robustness.py \
  --input data/interim/xente_features.csv
```

Expanding-window diagnostic:
- train 50% → evaluate next 10%;
- ...
- train 90% → evaluate final 10%.

## Stage G — Verification ✅
Run:
```bash
pytest -q
```

Current:
**4 queue verification tests passed.**

## Stage H — Next sensitivity
Next implement:
1. alert-rate sensitivity 0.5% / 1% / 2% / 5%;
2. starvation/service-equity metrics;
3. variable team capacity;
4. practitioner structural validation.

Cost-sensitive monetary analysis comes **after** stronger cost/recovery grounding.

## Definition of done for core MVP

- [x] raw Xente remains outside Git;
- [x] chronological feature pipeline is past-only;
- [x] baseline risk model produces holdout scores;
- [x] persistent queue carries backlog over time;
- [x] FIFO and risk-priority run on the same event stream;
- [x] outputs include alerts, FP, backlog, waiting time and workload;
- [x] comparison reproduced across multiple seeds;
- [x] weaker score-model sensitivity implemented;
- [ ] threshold/alert-rate sensitivity completed;
- [ ] practitioner workflow validation completed or explicitly documented as unavailable.

## What NOT to build yet
- LLM analyst;
- adaptive fraudster cognition;
- full Mesa UI;
- dashboard;
- complex game-theoretic equilibrium;
- second full dataset implementation.
