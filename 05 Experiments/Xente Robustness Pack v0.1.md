# Xente Robustness Pack v0.1

## Status
**Preliminary robustness package — not final thesis result.**

This note extends [[Xente Queue Pilot v0.1]] in four directions:
1. seen vs cold-start customers;
2. temporal stability;
3. risk-model structural sensitivity;
4. stochastic service-time robustness.

---

## 1. Seen vs cold-start customer robustness

Chronological 70/15/15 split.

### Full logistic model

| Split | Subgroup | Rows | Fraud | PR-AUC |
|---|---|---:|---:|---:|
| Validation | Seen customers | 11,224 | 9 | 0.464 |
| Validation | Unseen customers | 3,125 | 30 | 0.631 |
| Test | Seen customers | 9,019 | 9 | 0.906 |
| Test | Unseen customers | 5,331 | 41 | 0.903 |

### Interpretation
The model does **not** collapse on unseen customers.

However, this should not be read as proof that customer history generalizes extremely well. Most predictive strength is coming from current transaction Value/context, and Xente fraud is unusually separable on those signals.

In the deterministic capacity-ratio = 1.0 queue:
- Seen fraud: FIFO 9/9, risk-priority 9/9.
- Unseen fraud: FIFO 32/41 (78.0%), risk-priority 41/41 (100%).

So the operational difference is concentrated in cold-start/unseen fraud alerts under congestion.

---

## 2. Temporal robustness

The full logistic model was retrained on expanding historical prefixes and evaluated on the immediately following 10% chronological block.

| Training prefix | Eval fraud | PR-AUC | ROC-AUC | Unseen txn share |
|---:|---:|---:|---:|---:|
| 50% | 15 | 0.585 | 0.999 | 20.0% |
| 60% | 13 | 0.501 | 0.999 | 22.9% |
| 70% | 23 | 0.363 | 0.952 | 20.8% |
| 80% | 41 | 0.842 | 0.999 | 19.1% |
| 90% | 25 | 0.879 | 1.000 | 22.3% |

### Interpretation
PR-AUC varies substantially over time: approximately **0.36 to 0.88**.

This matters because the final 15% test period happens to be relatively easy for the score model.

Therefore:
> the high final-test PR-AUC should not be treated as stable fraud-detection performance.

For the thesis, policy experiments need robustness to score quality / temporal regime, not only one favorable test period.

---

## 3. Risk-model structural sensitivity

Three deliberately different score generators were tested.

### Models
1. **full_logistic**
   - current Value;
   - product/provider/channel context;
   - temporal features;
   - leakage-safe customer history.

2. **no_current_value**
   - removes `log_value` and `value_ratio_clip`;
   - keeps context and past-only history.

3. **amount_only**
   - only current log(Value) + debit/credit sign.

### Risk-model metrics

| Model | Validation PR-AUC | Test PR-AUC |
|---|---:|---:|
| full_logistic | 0.561 | 0.893 |
| no_current_value | 0.205 | 0.389 |
| amount_only | 0.531 | 0.913 |

### Key finding
The amount-only model performs almost as well as, or on the final test slightly better than, the full model.

This confirms that **current transaction Value is a dominant Xente signal**.

Consequences:
- classifier novelty should not be the thesis contribution;
- do not interpret near-perfect test ranking as a general fraud fact;
- queue/policy conclusions must be checked under weaker/degraded score quality.

---

## 4. Queue robustness across score models

Validation target alert rate: 1%.

### Capacity ratio = 1.0, deterministic service

| Risk model | Queue | Fraud capture within horizon | P95 wait |
|---|---|---:|---:|
| full_logistic | FIFO | 82% | 51.2 h |
| full_logistic | Risk-priority | 100% | 68.9 h |
| no_current_value | FIFO | 62% | 57.8 h |
| no_current_value | Risk-priority | 76% | 87.7 h |
| amount_only | FIFO | 82% | 50.1 h |
| amount_only | Risk-priority | 100% | 58.8 h |

### Interpretation
The risk-priority advantage becomes smaller when the score model is degraded, but the qualitative trade-off remains:
- more fraud receives service before the horizon;
- lower-priority alerts experience worse tail waiting time.

This is important because it shows the first queue result is **not only an artifact of the full logistic specification**.

---

## 5. Stochastic service-time robustness

Service times were made stochastic with:
- lognormal distribution;
- same mean implied by the relative capacity ratio;
- coefficient of variation = **0.5**;
- **100 random seeds**.

The CV value is an explicit stress assumption, not an empirically calibrated analyst-review distribution.

### Full logistic — capacity ratio 1.0

| Queue | Mean fraud capture | 5–95% range | Mean P95 wait |
|---|---:|---:|---:|
| FIFO | 81.5% | 77.9–82.0% | 52.6 h |
| Risk-priority | 99.98% | 100–100%* | 71.3 h |

*Discrete finite-fraud counts make the empirical quantiles collapse near 100%.

Cold-start fraud:
- FIFO mean capture ≈ **77.4%**
- Risk-priority mean capture ≈ **99.98%**

### Degraded model — no current Value — capacity ratio 1.0

| Queue | Mean fraud capture | 5–95% range | Mean P95 wait |
|---|---:|---:|---:|
| FIFO | 60.4% | 56–68% | 58.3 h |
| Risk-priority | 75.4% | 74–76% | 84.8 h |

### Interpretation
The queue-priority result survives random service-time variation and a materially weaker score model.

But the trade-off becomes clearer:
> risk-priority improves fraud capture under scarce service capacity while increasing tail waiting time.

---

## 6. What is robust so far?

### Supported by current experiments
Under the Xente event stream and evaluated capacity conditions:
1. capacity scarcity creates backlog/delay;
2. queue discipline changes which alerts receive scarce service first;
3. risk-priority tends to increase fraud review before the finite horizon;
4. the improvement persists under stochastic service time;
5. the improvement persists under a weaker score model;
6. risk-priority worsens tail waiting time for lower-priority alerts.

### NOT supported yet
Do **not** conclude:
- risk-priority is universally optimal;
- these waiting times are realistic bank waiting times;
- the 0.75/1.00/1.25 capacity ratios are empirical bank staffing levels;
- Xente score quality generalizes to Vietnamese banks;
- monetary net benefit favors risk-priority.

---

## 7. Why this improves the thesis contribution

The legacy project already showed threshold/capacity trade-offs using synthetic data.

The new KLTN baseline now shows, on an empirical Xente transaction stream:

```text
same events
+ same score model
+ same total service capacity
+ different queue rule
        ↓
different fraud-capture / waiting-time outcomes
```

And this qualitative relationship remains after:
- weakening the risk model;
- adding service stochasticity.

This is a stronger basis for the claim that **operational decision mechanisms matter beyond classifier metrics**.

---

## 8. Verification
Queue unit tests now check:
- no service before alert arrival;
- FIFO/risk-priority have the same total service capacity under equal conditions;
- risk-priority ordering does not use `FraudResult`;
- stochastic service is reproducible under the same random seed.

Current local verification result:
**4 tests passed.**

---

## 9. Next experiment
Priority order:
1. threshold/alert-rate robustness: 0.5%, 1%, 2%, 5%;
2. time-window / horizon sensitivity;
3. explicit starvation/service-equity metric;
4. pooled vs variable capacity structural sensitivity;
5. only then cost-sensitive priority and monetary sensitivity.

Linked notes:
- [[Xente Queue Pilot v0.1]]
- [[Validation Plan v0.1]]
- [[Operational Parameter Grounding v0.1]]
- [[Alves et al 2025 - OpenL2D FiFAR]]
- [[McCulloch 2022]]
