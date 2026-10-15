# GVHD Update - Xente Queue Milestone

## 1. Thesis direction in one sentence
Khóa luận dùng empirical Xente transaction stream + risk scoring + persistent analyst queue để stress-test fraud-management policies dưới capacity constraints và uncertainty, thay vì chỉ tối ưu classifier accuracy.

## 2. What has been completed

### Data
- Xente: 95,662 labelled transactions.
- 193 fraud cases.
- 3,742 CustomerIds.
- Chronological 70/15/15 baseline.
- Leakage-safe customer-history features.

### Risk engine
Regularized logistic regression baseline.

Important finding:
Xente has very strong transaction-Value/context signal, so high classifier performance is **not** treated as the contribution.

### Operational model
Implemented persistent event-driven alert queue:
- FIFO;
- risk-priority;
- backlog;
- waiting time;
- fixed/relative capacity;
- stochastic service times.

### Robustness
Checked:
- seen vs cold-start customers;
- expanding temporal windows;
- full vs degraded vs amount-only score models;
- stochastic service time over 100 seeds;
- alert-rate overload;
- starvation/tail waiting.

### Verification
Queue code currently has automated tests for:
- no service before alert arrival;
- same capacity across queue rules;
- priority independent of fraud ground truth;
- seed reproducibility;
- fixed service rate across threshold changes.

---

## 3. Current empirical/simulation insight

With fixed service capacity:

```text
lower threshold
→ more alerts
→ overload/backlog
→ longer waiting time
```

Risk-priority:
- tends to protect high-risk/fraud review under overload;
- but pushes lower-priority alerts to much longer waits.

This qualitative result persists with a weaker score model.

Therefore the emerging research contribution is:

> operational decision mechanisms can change system outcomes even when the underlying classifier/event stream is held fixed.

---

## 4. Important methodological caution
The thesis does **not** claim:
- simulated queue hours are real-bank SLAs;
- Xente represents a Vietnamese bank;
- risk-priority is universally best;
- exact analyst capacity has been empirically calibrated.

Analyst capacity is currently represented as relative/stress conditions because public sources do not provide defensible bank-specific values.

---

## 5. Literature grounding
Current core:
- [[AML-CFSim 2025]] — ABM policy experimentation and validation.
- [[McCulloch 2022]] — uncertainty/ranges/sensitivity.
- [[Alves et al 2025 - OpenL2D FiFAR]] — expert capacity constraints.
- [[Hoppner et al 2022 - Cost-sensitive transfer fraud]] — cost-sensitive fraud decisions.
- [[Real bank AML alert scoring 2025]] — external operational review/routing evidence.

---

## 6. Five decisions to ask GVHD

### Decision 1 — Framing
Is it acceptable to frame the thesis as:
**dynamic policy simulation / ABM for fraud policy stress-testing under uncertainty**, rather than a bank-specific digital twin?

### Decision 2 — Contribution
Is this contribution sufficiently focused?

> Evaluate how threshold, queue priority and analyst capacity interact to change fraud capture, backlog and waiting-time trade-offs.

### Decision 3 — ABM label
Does the current state/history + persistent queue + interaction structure justify ABM framing, or should the thesis use the more conservative term **dynamic/discrete-event policy simulation**?

### Decision 4 — Cost engine
Should monetary net benefit be:
- a core outcome; or
- secondary sensitivity because bank-specific FP/recovery costs are unavailable?

Recommended current position: secondary sensitivity.

### Decision 5 — Scope
Is FIFO vs risk-priority + capacity/threshold uncertainty enough for the core KLTN, with analyst heterogeneity/LLM deferred?

Recommended current position: yes; keep core narrow and validated.

---

## 7. Next before writing full Methodology
1. practitioner structural validation;
2. decide queue aging/expiry/hybrid priority;
3. freeze core mechanisms;
4. freeze final experiment grid;
5. then write Methodology against the frozen implementation.

Links:
- [[Xente Robustness Pack v0.1]]
- [[Xente Alert-rate and Starvation Sensitivity v0.1]]
- [[Validation Plan v0.1]]
- [[Practitioner Validation Questions v0.1]]
