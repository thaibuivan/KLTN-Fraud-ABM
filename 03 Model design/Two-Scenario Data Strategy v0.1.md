# Two-Scenario Data Strategy v0.1

## Principle

Use one conceptual ABM framework but parameterize separate empirical environments.

Do **not** merge IEEE-CIS and Xente into a single synthetic "bank".

## Scenario A — IEEE-CIS Fraud Detection

Role:
- online/card/e-commerce empirical environment;
- transaction amount and temporal patterns;
- fraud labels;
- card/device/identity-related observable features;
- training a scenario-specific risk model.

Important limitation:
- many variables are anonymized;
- TransactionDT is relative time, not a real timestamp;
- direct behavioral interpretation of hidden variables must be avoided.

## Scenario B — Xente Fraud Detection

Role:
- mobile/payment/e-commerce empirical environment;
- amount/value distribution;
- product/category/channel/provider information;
- fraud labels;
- scenario-specific risk model.

Permission status:
Zindi has explicitly confirmed thesis use is permitted with attribution and acknowledgement.

## Cross-scenario question

The study does not require a single classifier to transfer directly between the datasets.

Instead:

> Does the same policy-experimentation framework produce qualitatively robust conclusions when independently parameterized in two distinct transaction environments?

## What the datasets can support

Potentially empirical:
- fraud prevalence;
- amount distributions;
- observable temporal/channel patterns;
- scenario-specific predictive risk model performance.

Not directly identified:
- analyst capacity;
- analyst review time;
- analyst accuracy;
- customer friction cost;
- fraudster learning rate;
- strategy-switch cognition.

These require literature, plausible ranges or explicit assumptions.

## Deferred data sources

Nedbank and AMLSim/Libra are not core dependencies in the current scope. They may be considered later as external/future scenarios after the two core environments are complete.
