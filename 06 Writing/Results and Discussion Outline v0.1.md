# Results and Discussion Outline v0.1

## Status
**Writing scaffold based on current experiments.**

The final chapter should tell one coherent story:

> classifier performance alone does not determine operational fraud outcomes when review capacity is limited.

---

# 3. Results and Discussion

## 3.1 Xente empirical environment

### Table
Dataset profile:
- transactions;
- fraud count/rate;
- customers;
- time range;
- customer repetition.

### Figure candidate
Fraud vs legitimate `Value` distribution on log scale.

### Discussion
Emphasize:
- severe class imbalance;
- strong Value signal;
- cold-start issue;
- why classifier results require caution.

Source:
[[Xente Empirical Profile]]

---

## 3.2 Risk-score baseline and temporal instability

### Table
Validation/test:
- PR-AUC;
- ROC-AUC;
- Brier.

### Table
Expanding-window PR-AUC.

### Key discussion
Final test is unusually easy relative to some earlier windows.

Therefore:
> do not make risk-model accuracy the thesis contribution.

Source:
[[Xente Baseline Risk Model Feasibility]]
[[Xente Robustness Pack v0.1]]

---

## 3.3 Baseline effect of review capacity

Hold:
- threshold;
- risk model;
- queue rule.

Compare:
- capacity 0.75;
- 1.00;
- 1.25.

### Figure candidate
Capacity ratio vs:
- fraud capture;
- backlog;
- P95 wait.

### Main point
Capacity scarcity changes operational outcomes even when the score model is unchanged.

---

## 3.4 Queue discipline: FIFO vs risk-priority

### Table
For each capacity:
- fraud capture;
- backlog;
- P95/P99 wait;
- low/high-priority P95.

### Main point
Risk-priority does not create capacity.

It changes **who receives service first**.

Expected synthesis:
- higher fraud capture under congestion;
- same total service resource;
- worse lower-priority tail waiting.

Source:
[[Xente Queue Pilot v0.1]]

---

## 3.5 Alert sensitivity under fixed staffing

This is a central result.

### Figure candidate
Target alert rate vs ending backlog.

Separate lines:
- FIFO;
- risk-priority.

### Figure candidate
Target alert rate vs fraud capture.

### Figure candidate
Target alert rate vs low-priority P95 waiting time.

### Main point
A lower threshold may increase fraud candidates but can overwhelm a fixed review team.

This converts a statistical threshold choice into an operational capacity problem.

Source:
[[Xente Alert-rate and Starvation Sensitivity v0.1]]

---

## 3.6 Does the conclusion depend on an unusually strong risk model?

Compare:
- full logistic;
- no-current-value model.

### Main table
At selected threshold/capacity:
- FIFO fraud capture;
- risk-priority fraud capture;
- backlog;
- P95 wait.

### Main point
Prioritization benefit remains with weaker score quality, but its magnitude falls.

This is a stronger and more defensible result than the near-perfect full-model case.

---

## 3.7 Cold-start customers

Report:
- seen vs unseen fraud counts;
- subgroup score metrics;
- queue capture.

### Main point
Many later frauds come from previously unseen customers.

Customer history alone is insufficient; current transaction context remains important.

---

## 3.8 Stochastic service-time robustness

### Table
Mean + 5–95% range across 100 seeds.

Metrics:
- fraud capture;
- backlog;
- P95 wait.

### Main point
The queue-policy trade-off persists under random service duration.

---

## 3.9 Variable team-capacity robustness

### Table
CV 0 / 0.3 / 0.6:
- fraud capture;
- backlog;
- P95 wait.

### Main point
Capacity volatility widens operational uncertainty but does not reverse the current qualitative queue trade-off.

Source:
[[Xente Variable Team Capacity Sensitivity v0.1]]

---

## 3.10 Synthesis of policy trade-offs

Recommended synthesis matrix:

| Mechanism | Helps | Costs / risks |
|---|---|---|
| Lower threshold | more fraud candidates | alert overload |
| More capacity | lower backlog/delay | operational resource |
| Risk-priority | protects high-risk service | starvation/tail delay |
| Stronger score | better prioritization | model/regime dependence |

Do not name an overall “best policy”.

Instead discuss where conclusions change.

---

## 3.11 Robustness and limitations

Discuss explicitly:
- only 193 total frauds;
- Xente Value signal;
- short labelled horizon;
- non-bank-specific operational parameters;
- no direct analyst logs;
- no empirically identified delay→recovery function;
- simulation horizon censoring;
- public-data external validity.

Connect to:
[[McCulloch 2022]]
[[Validation Plan v0.1]]

---

## Candidate final takeaway
A defensible final message is:

> Fraud-policy performance is jointly determined by score quality, alert generation and review-capacity allocation. Under limited capacity, a statistically more sensitive policy can create operational overload, while risk-based prioritization can preserve fraud review at the cost of greater delay for lower-priority alerts. These trade-offs persist across several Xente-based robustness checks but remain conditional on the evaluated data, model structures and capacity scenarios.
