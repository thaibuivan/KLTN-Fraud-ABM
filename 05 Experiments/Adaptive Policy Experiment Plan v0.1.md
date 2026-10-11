# Adaptive Policy Experiment Plan v0.1

## Experiment 1 — Static vs Adaptive Fraudster

Hold the policy, transaction environment and analyst capacity fixed.

Compare:
- static fraudster;
- adaptive fraudster.

Primary outcomes:
- successful fraud value;
- fraud detection rate;
- time to detection;
- alert volume;
- queue/backlog;
- policy-specific cost.

Important: "adaptive causes more loss" is a hypothesis, not a guaranteed result.

## Experiment 2 — Policy Comparison

Fraudster: adaptive.

Compare:
1. fixed-threshold;
2. cost-sensitive;
3. capacity-aware.

Evaluate trade-offs among:
- fraud loss;
- false positives;
- customer friction proxy;
- review volume;
- backlog;
- waiting time;
- total cost if cost coefficients are declared.

## Experiment 3 — Analyst Capacity Stress Test

Vary analyst capacity over low / medium / high or a calibrated range.

Measure:
- queue length;
- waiting time;
- utilization;
- fraud loss;
- policy ranking.

Research question:
Does the ranking of policies change when review capacity becomes scarce?

## Replication

Each configuration must be run over multiple random seeds.

Report:
- mean;
- standard deviation;
- confidence intervals where useful.

## Robustness layers

1. stochastic replication;
2. parameter sensitivity;
3. structural sensitivity for the adaptation mechanism;
4. cross-scenario replication in IEEE-CIS and Xente environments.

## Minimum viable sequence

1. verified static baseline;
2. static fraudster experiment;
3. adaptive mechanism;
4. static-vs-adaptive comparison;
5. policy comparison;
6. capacity stress test;
7. sensitivity analysis.
