# Höppner et al. 2022 — Cost-sensitive transfer fraud

## Citation
Höppner, S., Baesens, B., Verbeke, W., & Verdonck, T. (2022). *Instance-dependent cost-sensitive learning for detecting transfer fraud*. European Journal of Operational Research, 297(1), 291–300.

Source:
https://doi.org/10.1016/j.ejor.2021.05.028

## Core idea
Fraud detection is not only a statistical classification problem.

Business objective is closer to:
> minimizing **financial loss**, where misclassification cost can differ across transactions.

Paper develops:
- instance-dependent cost matrix;
- instance-dependent decision threshold;
- cost-sensitive logistic regression;
- cost-sensitive gradient boosting.

## Application to KLTN
Supports:
- cost-sensitive policy as a legitimate policy family;
- transaction amount as one component of loss exposure;
- evaluating policy by business/operational outcomes instead of AUC only.

## Important boundary
Paper does **not** ground:
- queue/backlog;
- analyst review time;
- analyst capacity;
- customer churn after false positives.

So it should support the **cost engine/policy layer**, not operational queue parameters.

## Thesis use
Primary results should still report decomposed metrics:
- fraud caught/missed;
- false positives;
- alerts reviewed;
- backlog/waiting time.

A cost-sensitive/net-benefit metric should be a **secondary sensitivity analysis** unless bank-specific costs become available.

## Link
- [[Evidence Parameter Matrix]]
- [[Operational Parameter Grounding v0.1]]
