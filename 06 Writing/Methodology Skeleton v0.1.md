# Methodology Skeleton v0.1

## Status
**Writing scaffold — pending final core freeze.**

This note maps the current implementation into a thesis-ready Methodology chapter.

Do not turn this into final prose until:
- GVHD confirms framing;
- practitioner structural validation is completed or documented unavailable;
- [[Candidate Core Specification v0.3]] is frozen.

---

# 2. Data and Methodology

## 2.1 Research design

### Purpose
The study evaluates transaction-fraud management policies as a dynamic operational system rather than evaluating the fraud classifier in isolation.

Core mechanisms:
- transaction arrival;
- fraud risk scoring;
- alert threshold;
- limited review capacity;
- persistent backlog;
- queue priority;
- operational outcomes.

### Research design type
Current preferred wording:
**empirical event-replay policy simulation with stateful/agent-based components**.

Explain that the model is used for:
- counterfactual policy comparison;
- stress testing;
- robustness under parameter/model uncertainty.

Do not claim bank-specific prediction.

---

## 2.2 Data

### 2.2.1 Xente Fraud Detection
Report verified training data:
- 95,662 labelled transactions;
- 193 fraud;
- 0.2018% fraud prevalence;
- 3,742 CustomerIds;
- actual transaction timestamps.

Discuss:
- repeated customer histories;
- fraud concentration;
- strong Value/context signal;
- cold-start customers.

Reference:
- [[Xente Empirical Profile]]
- [[Data Audit]]

### 2.2.2 Chronological split
Baseline:
- 70% train;
- 15% validation;
- 15% final test.

Fraud counts:
- 104;
- 39;
- 50.

Justify chronological rather than random split:
- preserves temporal ordering;
- prevents future information entering past decisions;
- exposes cold-start and temporal drift.

### 2.2.3 Data restrictions
State that raw Xente competition data are stored locally and not redistributed in the public repository.

---

## 2.3 Customer state and feature construction

### Stateful entity
`CustomerId`.

Important:
`AccountId` and `SubscriptionId` are not interpreted as clean nested bank-account agents because local profiling shows shared/many-to-many-like identifier patterns.

### Past-only features
Current:
- prior transaction count;
- rolling transaction counts over 1h/24h/7d;
- prior Value mean/std;
- time since previous transaction;
- Value relative to prior customer mean;
- prior product/category share;
- prior channel share.

Current transaction context:
- Value;
- debit/credit sign;
- hour/weekday;
- product;
- channel;
- provider;
- pricing strategy.

Explicit leakage rule:
for transaction t, customer-history features can only use transactions before t.

Implementation:
`scripts/build_xente_features.py`.

---

## 2.4 Fraud risk engine

### Baseline
Regularized logistic regression.

Why:
- interpretable;
- suitable for sparse positive labels;
- probability-like score;
- keeps thesis focus on policy rather than ML leaderboard performance.

### Evaluation
- PR-AUC;
- ROC-AUC as secondary;
- Brier score;
- recall/precision at fixed alert rates.

### Model-structure robustness
Compare:
- full logistic;
- no-current-value logistic;
- amount-only diagnostic.

Reason:
Xente fraud is strongly separated by current transaction Value, so policy findings must not depend on an unusually easy score stream.

Reference:
- [[Xente Baseline Risk Model Feasibility]]
- [[Xente Robustness Pack v0.1]]

---

## 2.5 Alert policy

The risk engine outputs a score.

A transaction becomes an alert when:
`score >= threshold`.

Threshold is chosen on validation for target alert rates:
- 0.5%;
- 1%;
- 2%.

5% is an extreme stress scenario.

The threshold is then frozen before test replay.

Important:
the realized test alert rate may differ because the score distribution changes over time.

---

## 2.6 Persistent queue model

### Event-driven simulation
Transactions are processed in chronological order.

Alert state:
- arrival time;
- risk score;
- service start;
- service end;
- waiting time;
- backlog state.

Backlog persists over time.

It is not reset daily.

Implementation:
`scripts/simulate_alert_queue.py`.

### Queue disciplines

#### FIFO
Earliest alert first.

#### Risk-priority
Highest model risk score among waiting alerts first.

Non-preemptive:
an alert already in service is not interrupted.

Fraud ground-truth label is never visible to the queue rule.

---

## 2.7 Review capacity

### Why capacity is modeled relatively
No defensible public source identifies a bank-specific Xente-like analyst cases/day value.

Therefore the thesis avoids fake precision.

### Capacity experiment A
For a fixed alert policy:

`capacity_ratio = pooled_service_rate / mean_alert_arrival_rate`

Scenarios:
- 0.75;
- 1.00;
- 1.25.

### Capacity experiment B — fixed staffing across thresholds
To compare thresholds:
- derive service capacity from a reference validation 1% alert stream;
- freeze absolute pooled capacity;
- vary threshold.

This ensures that a more sensitive threshold does not automatically receive more analyst capacity.

Reference:
- [[Operational Parameter Grounding v0.1]]
- [[Queue and Analyst Service Design v0.1]]

---

## 2.8 Operational uncertainty

### Per-case service-time uncertainty
Lognormal service-time variation.

Current stress:
- CV = 0.5;
- 100 seeds.

### Day-level team-capacity uncertainty
Lognormal daily capacity multiplier.

Current stress:
- CV = 0.3;
- CV = 0.6 severe stress;
- 100 seeds.

These CVs are explicit uncertainty scenarios, not empirical bank estimates.

Reference:
- [[Xente Variable Team Capacity Sensitivity v0.1]]
- [[McCulloch 2022]]

---

## 2.9 Outcome metrics

### Fraud
- fraud capture within horizon;
- fraud alerts reviewed;
- seen/unseen customer fraud capture.

### Workload
- alerts generated;
- alerts reviewed;
- ending backlog.

### Delay
- mean wait;
- P95;
- P99;
- max wait.

### Service equity / starvation
- share waiting >24h;
- share >48h;
- share >72h;
- low-priority P95 wait;
- high-priority P95 wait.

### False positives
- legitimate alerts reviewed.

Monetary net benefit is not a primary metric until cost/recovery assumptions are better grounded.

---

## 2.10 Experiment design

Use [[Core Experiment Grid v0.1]].

Main deterministic grid:
- 2 risk models;
- 2 queue rules;
- 3 alert rates;
- 3 capacity levels.

36 core configurations.

Stochastic robustness is intentionally focused rather than fully factorial.

---

## 2.11 Validation and robustness

### Conceptual validation
Literature + practitioner/GVHD review.

### Empirical validation
Xente patterns and chronological score performance.

### Verification
Automated queue tests.

### Temporal robustness
Expanding-window score evaluation.

### Structural sensitivity
- FIFO vs risk-priority;
- full vs weaker risk score;
- constant vs variable team capacity.

### Stochastic robustness
Repeated seeds.

Reference:
- [[Validation Plan v0.1]]

---

## 2.12 Claim limitations

Explicitly state:
- Xente does not represent a Vietnamese bank;
- queue hours are simulated operational time, not bank SLAs;
- capacity ratios are stress parameters, not staffing estimates;
- results compare mechanisms within evaluated scenarios;
- policy conclusions are conditional, not universal recommendations.
