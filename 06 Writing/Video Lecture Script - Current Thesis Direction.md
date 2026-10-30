# Video Lecture Script — Current Thesis Direction

## Opening

This thesis does not ask only whether a fraud classifier predicts well. It asks which fraud-management policy still performs well when fraudsters can react to system feedback and analysts have limited review capacity.

ABM is the research instrument. Policy experimentation is the research objective. Adaptive fraudster behavior is a stress mechanism.

## Research problem

A risk score does not directly tell an organization what action to take. Lower thresholds can increase detection but also increase alerts, false positives, queue length and analyst delay.

A dynamic model is needed to study these system-level trade-offs.

## Why ABM

Customer, fraudster and analyst entities have persistent states. Alerts enter a queue. Review capacity is limited. Fraudsters may react to challenge/block feedback and change strategy.

These mechanisms create feedback over time.

## Data

Two separate empirical environments are proposed:

- IEEE-CIS for online/card/e-commerce transactions;
- Xente for mobile/payment/e-commerce transactions.

The datasets are not merged.

## Policies

The first policy family is fixed-threshold.

The second is cost-sensitive.

The third is capacity-aware, where decisions respond to queue and available analyst capacity.

## Experiments

Experiment 1 compares static and adaptive fraudsters.

Experiment 2 compares the three policy families.

Experiment 3 stress-tests analyst capacity.

## Parameterization

Some parameters can be estimated from data. Others come from literature. Policy parameters are intentionally manipulated. Behavioral parameters such as learning rate are uncertain assumptions and must be sensitivity-tested.

## Final product

The final product is an experimental simulation framework plus quantitative evidence about policy trade-offs, not a production fraud detector and not a digital twin of a specific organization.
