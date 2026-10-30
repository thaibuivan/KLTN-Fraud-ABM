# Core Experiment Grid v0.1

## Purpose
Define a **small, defensible experiment grid** for the thesis so the project does not expand into an uncontrolled Cartesian product.

This grid is a candidate freeze pending:
- GVHD feedback;
- practitioner structural validation.

---

## 1. Main experiment factors

### Risk model
Primary:
1. `full_logistic`

Structural robustness:
2. `no_current_value`

`amount_only` is retained as a diagnostic demonstrating Xente's strong Value signal, not as a main thesis model.

### Queue discipline
1. FIFO
2. Risk-priority

### Alert policy
Validation target alert rates:
1. 0.5%
2. 1%
3. 2%

Extreme stress:
- 5% → appendix/stress case, not main comparison.

### Base pooled capacity
Relative to validation 1% reference alert arrival:
1. 0.75
2. 1.00
3. 1.25

When comparing thresholds, absolute pooled service rate is held fixed within each capacity scenario.

---

## 2. Main deterministic grid

```text
2 risk models
× 2 queue rules
× 3 alert rates
× 3 base capacity levels
= 36 core configurations
```

Purpose:
estimate the systematic interaction:

```text
score quality
× threshold/load
× capacity
× queue discipline
→ capture/backlog/waiting distribution
```

No random seeds are required for the deterministic layer.

---

## 3. Stochastic robustness layer

Do **not** run every stochastic assumption over all 36 configurations.

Use a focused design at:
- alert target = 1%;
- capacity ratios = 0.75 / 1.00 / 1.25;
- both queue rules;
- both primary risk models.

### A. Per-case service variation
- service CV = 0.5
- team capacity CV = 0
- 100 seeds

### B. Team-capacity variation
- service CV = 0
- team capacity CV = 0.3
- 100 seeds

### Severe stress appendix
- team capacity CV = 0.6

Reason:
separate stochastic mechanisms rather than mixing them immediately.

---

## 4. Temporal robustness layer
Existing expanding-window model diagnostic:

```text
50% train → next 10%
60% train → next 10%
70% train → next 10%
80% train → next 10%
90% train → final 10%
```

Purpose:
show that score quality is temporally unstable and policy conclusions should not depend on one favorable holdout.

No need to run the full queue grid on every temporal fold unless GVHD asks.

---

## 5. Metrics required in every core policy table

### Detection / outcome
- fraud alerts generated;
- fraud reviewed within horizon;
- fraud capture within horizon;
- seen/unseen fraud capture.

### Workload
- alerts generated;
- reviewed within horizon;
- backlog end.

### Waiting / service equity
- mean wait;
- P95 wait;
- P99 wait;
- share >24h;
- share >48h;
- share >72h;
- low-priority P95 wait;
- high-priority P95 wait.

### Model diagnostics
- realized test alert rate;
- effective capacity ratio;
- score-model identity.

---

## 6. Primary thesis comparisons

### Comparison A — Capacity effect
Hold:
- model;
- threshold;
- queue rule

Vary:
- capacity 0.75 / 1.00 / 1.25

Question:
> How does scarce review capacity change policy outcomes?

### Comparison B — Threshold/load effect
Hold:
- fixed absolute service rate;
- model;
- queue rule

Vary:
- alert target 0.5% / 1% / 2%

Question:
> Does a more sensitive detection policy overload review capacity?

### Comparison C — Queue-priority effect
Hold:
- event stream;
- score;
- threshold;
- capacity

Vary:
- FIFO vs risk-priority

Question:
> Does prioritization change fraud capture/backlog/waiting trade-offs?

### Comparison D — Score-quality robustness
Repeat A–C using `no_current_value`.

Question:
> Do operational conclusions survive when the score model is materially weaker?

---

## 7. What stays out of the core grid
Unless new evidence/feedback requires it:
- LLM analyst;
- fraudster cognition;
- individual analyst accuracy;
- adaptive threshold optimizer;
- monetary net-benefit optimization;
- IEEE-CIS full simulator;
- complex game theory;
- full factorial combinations of every uncertainty.

---

## 8. Candidate stopping rule
Core experimental design is sufficient when:
1. qualitative conclusions are stable across full + weaker score models;
2. stochastic uncertainty is reported with intervals;
3. starvation is visible, not hidden;
4. practitioner says workflow is not materially wrong;
5. GVHD accepts scope/framing.

At that point:
> stop adding mechanisms and write the thesis.
