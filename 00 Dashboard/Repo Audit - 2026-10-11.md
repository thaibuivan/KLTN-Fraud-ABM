# Repo Audit — 2026-10-11

## Why this audit exists

The branch currently contains **two research phases**:

### Phase A — earlier Xente-only operational policy simulation
Focus:
- chronological Xente replay;
- score threshold;
- persistent queue;
- FIFO vs risk-priority;
- capacity/load uncertainty.

### Phase B — current ABM policy-experimentation direction
Focus:
- policy experimentation as the research objective;
- adaptive fraudster as a stress mechanism;
- analyst queue/capacity as operational feedback;
- IEEE-CIS + Xente as two separate empirical scenarios.

The main risk is not bad code. The risk is **reading a Phase-A design document and mistaking it for the current thesis framing**.

---

## A. KEEP ACTIVE — current source of truth

These should remain at the front of the repo:

- `00 Dashboard/Current Direction - 2026-10-11.md`
- `00 Dashboard/KLTN Dashboard.md`
- `00 Dashboard/READING ORDER.md`
- `03 Model design/Research Design v1.0 - Policy Experimentation.md`
- `03 Model design/Conceptual Model v1.0 - Adaptive Policy ABM.md`
- `03 Model design/Adaptive Fraudster Design v0.1.md`
- `03 Model design/Parameter Registry v0.2.md`
- `03 Model design/Two-Scenario Data Strategy v0.1.md`
- `05 Experiments/Adaptive Policy Experiment Plan v0.1.md`
- `04 Meetings/GVHD Brief - Current Direction 2026-10-11.md`

---

## B. KEEP — strong reusable empirical / methodological assets

### Xente empirical evidence
- `03 Model design/Data Audit.md`
- `05 Experiments/Xente Empirical Profile.md`
- `05 Experiments/Xente Baseline Risk Model Feasibility.md`

Why keep:
these contain verified empirical facts, not only old framing.

### Queue / capacity methodology
- `03 Model design/Queue and Analyst Service Design v0.1.md`
- `03 Model design/Operational Parameter Grounding v0.1.md`
- `01 Literature/Alves et al 2025 - OpenL2D FiFAR.md`
- `01 Literature/Hoppner et al 2022 - Cost-sensitive transfer fraud.md`
- `01 Literature/Real bank AML alert scoring 2025.md`
- `01 Literature/McCulloch 2022.md`
- `01 Literature/AML-CFSim 2025.md`

Why keep:
the current direction still needs queue dynamics, uncertainty, cost-sensitive policy, capacity constraints and validation.

### Xente pilot experiments
- `05 Experiments/Xente Queue Pilot v0.1.md`
- `05 Experiments/Xente Robustness Pack v0.1.md`
- `05 Experiments/Xente Alert-rate and Starvation Sensitivity v0.1.md`
- `05 Experiments/Xente Variable Team Capacity Sensitivity v0.1.md`

Why keep:
these are completed pilot results and provide a strong operational module for the Xente scenario.

Boundary:
they are **not yet the final results of the current adaptive-fraudster thesis design**.

### Code
Keep:
- Xente profiling/feature/risk scripts;
- queue simulator;
- robustness runners;
- adaptive-fraudster prototype;
- tests.

The old queue code is not obsolete. It is a reusable subsystem.

---

## C. MERGE / REWRITE — useful content but duplicate current documents

### `03 Model design/Evidence Parameter Matrix.md`
Useful because it contains detailed Xente-specific evidence status.

Problem:
it overlaps with `Parameter Registry v0.2.md`.

Recommended cleanup:
- keep `Parameter Registry v0.2` as the master general registry;
- later convert Evidence Parameter Matrix into a scenario-specific
  `Xente Parameter Evidence.md`.

### `03 Model design/Validation Plan v0.1.md`
Useful foundation.

Problem:
adaptive-fraudster uncertainty and IEEE-CIS cross-scenario validation are missing.

Recommended:
upgrade to Validation Plan v1.0; do not delete until migration is complete.

### `03 Model design/Xente Baseline Implementation Plan v0.1.md`
Useful and executable.

Problem:
its wording says Xente is the core MVP and second dataset should not be built.

Recommended:
rename/reframe later as:
`Xente Scenario Implementation Plan.md`.

---

## D. SUPERSEDED — should not remain in the active reading path

These reflect the previous scope:

- `03 Model design/Research Design v0.2.md`
- `03 Model design/Candidate Core Specification v0.3.md`
- `03 Model design/Core Experiment Grid v0.1.md`
- `03 Model design/Conceptual Model v0.2.md`
- `04 Meetings/GVHD Update - Xente Queue Milestone.md`
- `06 Writing/Methodology Skeleton v0.1.md`
- `06 Writing/Results and Discussion Outline v0.1.md`

Main conflicts:
- Xente as the only primary empirical core;
- IEEE-CIS treated as optional;
- adaptive fraudster explicitly deferred/non-core;
- old experiment grid centered only on threshold × capacity × queue rule.

Recommendation:
move to an archive folder after supervisor discussion rather than permanently deleting immediately.

---

## E. HISTORICAL — useful only for provenance

- `00 Dashboard/Legacy Project Audit - FinRisk.md`
- `03 Model design/Legacy Migration Map.md`
- `03 Model design/Prototype-to-Thesis Gap.md`

Recommendation:
keep in archive/history, not in normal reading flow.

---

## F. SPECIAL CASE — adaptive smoke-test code

`scripts/run_adaptive_vs_static.py` currently uses synthetic response probabilities.

Keep it because it verifies the learning mechanism.

But label it clearly:
> prototype / smoke test only; not empirical thesis evidence.

It should not be quoted as a result.

---

## Cleanup principle

Do not delete valuable empirical work merely because the framing changed.

Use three layers:

```text
CURRENT DESIGN
    ↓
REUSABLE EVIDENCE / MODULES
    ↓
ARCHIVED PREVIOUS FRAMING
```

This preserves reproducibility without allowing old scope decisions to contaminate the current thesis narrative.

## Recommended next cleanup

After GVHD confirms the current direction:

1. move superseded files into `99 Archive/Previous Xente-only direction/`;
2. move legacy provenance files into `99 Archive/Legacy FinRisk/`;
3. upgrade Validation Plan to v1.0;
4. convert Evidence Parameter Matrix into Xente-specific evidence;
5. reframe Xente Baseline Implementation Plan as Scenario B;
6. create IEEE-CIS data audit / scenario implementation plan;
7. only then merge `chatgpt-draft` into `main`.
