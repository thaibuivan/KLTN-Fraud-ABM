# Xente Baseline Implementation Plan v0.1

## Goal
Biến quyết định dataset thành một baseline có thể chạy được, nhưng **không migrate mù quáng code từ repo cũ**.

## Stage A — Local profile
Input:
`data/raw/xente/training.csv`

Run:
```bash
python scripts/profile_xente.py --input data/raw/xente/training.csv
```

Outputs (ignored by Git):
- `outputs/local/xente_profile.json`
- `outputs/local/xente_profile.md`

Use profile to check:
- fraud count/rate;
- time range;
- repeated customers/accounts;
- amount distribution;
- missingness;
- fraud counts under candidate chronological splits.

## Stage B — Leakage-safe feature table
Build chronological features using only prior information for each transaction.

Initial features:
- hour / weekday;
- customer transaction count in rolling windows;
- rolling amount mean/median/sum;
- gap from previous transaction;
- current amount relative to customer history;
- product/category/channel frequencies from past data only;
- account/subscription activity counts.

Do not use future label statistics or whole-dataset target encoding.

## Stage C — Risk engine baseline
Start with regularized logistic regression.

Why:
- interpretable;
- small fraud-positive count;
- easy probability output;
- helps keep thesis focus on policy rather than classifier competition.

Evaluation:
- PR-AUC;
- ROC-AUC as secondary;
- recall at selected alert/review rates;
- calibration curve/Brier score if feasible;
- chronological holdout only.

Optional robustness:
- XGBoost/LightGBM after baseline is stable.

## Stage D — Observed-event policy replay
Process holdout transactions by `TransactionStartTime`.

Each event:
1. update/read customer history using past-only state;
2. score transaction;
3. apply policy;
4. if alert, insert into persistent queue;
5. analyst service completes alerts according to capacity/service-time assumptions;
6. compute outcome using observed `FraudResult` plus explicit prevention/recovery assumptions.

## Stage E — Persistent queue
Minimum queue state:
- alert id;
- transaction id;
- arrival time;
- priority;
- service start;
- service end;
- waiting time;
- queue length at arrival.

Baseline disciplines:
1. FIFO;
2. risk-priority.

Cost-sensitive priority comes after cost assumptions are grounded.

## Stage F — Re-test legacy hypotheses
Re-test, do not copy:
- lower threshold increases recall but workload/FP;
- low capacity changes policy ranking;
- capacity-aware priority helps under congestion;
- cost assumptions can change preferred policy.

## Stage G — Uncertainty
Only after baseline works:
- repeated seeds for stochastic service-time/review components;
- analyst capacity range;
- review-time range;
- cost range;
- fraud-pressure stress scenarios;
- queue discipline structural sensitivity.

## Definition of done for MVP
MVP is complete when:
- [ ] raw Xente remains outside Git;
- [ ] chronological feature pipeline passes leakage checks;
- [ ] baseline risk model produces scores on holdout;
- [ ] persistent queue carries backlog over time;
- [ ] at least two policies run on exactly the same event stream;
- [ ] output includes fraud loss proxy, FP, alerts, backlog, waiting time and workload;
- [ ] one policy comparison is reproduced over multiple seeds/parameter values.

## What NOT to build yet
- LLM analyst;
- adaptive fraudster cognition;
- full Mesa multi-agent UI;
- dashboard;
- complex game-theoretic equilibrium;
- second full dataset implementation.
