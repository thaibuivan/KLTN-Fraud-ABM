# Research Design v1.0 — Policy Experimentation

## Working title

**Agent-Based Stress Testing of Transaction Fraud-Management Policies under Adaptive Fraudster Behavior and Analyst Capacity Constraints**

Vietnamese working title:

**Mô phỏng dựa trên tác tử để thử nghiệm chính sách quản lý gian lận giao dịch dưới hành vi gian lận thích nghi và giới hạn năng lực phân tích**

## Research problem

Fraud-detection research is often evaluated with predictive metrics such as AUC, precision, recall and F1. In deployment, however, a risk score must be converted into actions such as approve, step-up authentication, review or block.

Lower thresholds may improve fraud capture but also increase alerts, false positives, analyst workload, queue length and review delay. At the same time, fraudsters may react to system feedback and alter transaction amount, timing, identity or strategy.

The thesis therefore studies fraud management as a **dynamic policy problem**, not only a classification problem.

## Main research question

> How do alternative transaction-fraud management policies perform under adaptive fraudster behavior and analyst capacity constraints?

## RQ1 — Adaptation

How does adaptive fraudster behavior affect fraud loss and detection outcomes relative to static fraud behavior?

## RQ2 — Policy trade-offs

What trade-offs do alternative fraud-management policies create among fraud loss, detection performance, false positives, customer friction and analyst workload?

## RQ3 — Operational robustness

How do analyst capacity and uncertain behavioral/operational parameters affect the robustness of policy conclusions?

## Research objective

Build an empirically grounded ABM / dynamic policy-simulation framework for controlled counterfactual experiments.

## Contribution target

The intended contribution is **not** a new classifier or a claim that adaptive fraudsters have never been studied before.

The contribution target is a closed-loop experimental framework combining:

- heterogeneous/persistent transaction actors;
- adaptive fraudster behavior;
- a fraud-risk/detection system;
- an alert queue;
- limited analyst capacity;
- alternative fraud-management policies;
- repeated stochastic simulation and sensitivity analysis.

## Expected metrics

### Fraud / detection
- fraud detection rate;
- false negative rate;
- successful fraud value;
- prevented fraud value.

### Customer impact
- false-positive rate;
- challenge/review rate;
- optional friction/abandonment proxy.

### Operations
- queue length;
- backlog;
- review waiting time;
- analyst utilization.

### Economics
- fraud loss;
- review cost;
- false-positive/friction cost;
- total cost when cost assumptions are explicitly declared.

## Scope discipline

Core implementation should remain small enough to verify and defend. IEEE-CIS and Xente are the two current empirical scenarios. Nedbank and AMLSim/Libra are treated as possible future extensions unless the supervisor explicitly requests a broader scope.
