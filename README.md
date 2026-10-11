# KLTN — Fraud Policy Experimentation with ABM

Research workspace for an undergraduate thesis on **transaction-fraud policy experimentation under adaptive fraudster behavior and limited analyst capacity**.

## Current thesis framing

> Use Agent-Based Modelling (ABM) as a policy laboratory to stress-test alternative fraud-management policies in a dynamic environment where fraudsters can adapt to system feedback and fraud analysts have limited review capacity.

The current project logic is:

- **Research objective:** policy experimentation / stress testing.
- **ABM:** research instrument.
- **Adaptive fraudster:** stress mechanism.
- **Alert queue + analyst capacity:** operational constraint and feedback mechanism.
- **Risk model:** one component of the detection system, not the thesis contribution.
- **Empirical grounding:** public fraud data + literature + explicit assumptions.

## Start here

Read in this order:

1. `00 Dashboard/READING ORDER.md`
2. `00 Dashboard/Current Direction - 2026-10-11.md`
3. `03 Model design/Research Design v1.0 - Policy Experimentation.md`
4. `03 Model design/Conceptual Model v1.0 - Adaptive Policy ABM.md`
5. `03 Model design/Parameter Registry v0.2.md`
6. `03 Model design/Two-Scenario Data Strategy v0.1.md`
7. `05 Experiments/Adaptive Policy Experiment Plan v0.1.md`

For supervisor discussion:
- `04 Meetings/GVHD Brief - Current Direction 2026-10-11.md`

## Empirical scenarios

### Scenario A — IEEE-CIS
Online/card/e-commerce fraud environment.

### Scenario B — Xente
Mobile/payment/e-commerce fraud environment.

The datasets are **not merged**. Each independently parameterizes the same conceptual framework.

## Work already completed before the current framing

The repository contains a substantial Xente queue/capacity pilot from the earlier, narrower direction:

- Xente data audit and empirical profiling;
- leakage-safe customer-history features;
- chronological logistic risk baseline;
- persistent alert queue;
- FIFO vs risk-priority;
- fixed/relative pooled capacity experiments;
- threshold/load sensitivity;
- stochastic service-time robustness;
- variable team-capacity sensitivity;
- automated queue verification tests.

These results are **not discarded**. They are treated as:
1. empirical groundwork for the Xente scenario;
2. a validated operational queue module;
3. pilot evidence that policy/capacity mechanisms affect system outcomes.

However, older files that state "Xente only", "IEEE optional", or "do not model adaptive fraudster" are **superseded as project framing** and should not be read as the current research design.

See:
- `00 Dashboard/Repo Audit - 2026-10-11.md`

## Current prototype code

### Xente empirical / queue modules
- `scripts/profile_xente.py`
- `scripts/build_xente_features.py`
- `scripts/train_xente_baseline.py`
- `scripts/simulate_alert_queue.py`
- robustness/sensitivity runners

### Adaptive fraudster prototype
- `scripts/adaptive_fraudster.py`
- `scripts/run_adaptive_vs_static.py`
- `tests/test_adaptive_fraudster.py`

The adaptive runner is currently a **synthetic smoke test**, not a thesis result.

## Git workflow

- `main`: accepted/stable version.
- `chatgpt-draft`: active working branch for review before merge.

## Data and security

Do not commit:
- raw Xente / IEEE-CIS competition data;
- row-level restricted data;
- employer/internal data;
- proprietary thresholds/rules;
- API keys, passwords, tokens or secrets.

## Claim boundary

The project does not claim:
- a digital twin of a bank;
- a production-ready fraud system;
- a universal optimal policy;
- exact real-world fraudster cognition;
- direct policy advice for a specific financial institution.

Conclusions must remain conditional on the evaluated scenarios, assumptions and parameter ranges.
