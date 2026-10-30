# IEEE-CIS Baseline + Integrated Policy Replay v0.1

## Status

**Executed empirical Scenario B milestone.**

This note records:
1. the first memory-bounded chronological IEEE-CIS risk baseline;
2. the first Fixed vs Capacity-aware replay through the shared policy/queue engine.

It is still **pre-adaptation** for IEEE-CIS.

## 1. Risk baseline

Entity proxy:
- card1 + addr1.

Temporal split:
- first 70% train;
- next 15% validation;
- final 15% test.

Model:
- streaming SGD log-loss;
- alpha = 1e-3;
- train-only frequency encoding for high-cardinality context;
- train-only sparse one-hot for low-cardinality context;
- past-only entity history.

### Metrics

| Split | Rows | Fraud | Fraud rate | PR-AUC | ROC-AUC | Brier | Mean predicted p |
|---|---:|---:|---:|---:|---:|---:|---:|
| Validation | 88,581 | 3,042 | 3.434% | 0.3644 | 0.8218 | 0.02840 | 0.0653 |
| Test | 88,581 | 3,083 | 3.480% | 0.3840 | 0.8219 | 0.03370 | 0.0946 |

Important contrast with Xente:
- IEEE score ranking is useful but much less separable;
- forward calibration drift is visible;
- therefore this is a genuinely different empirical risk environment rather than a duplicate Xente scenario.

### Validation operating points

| Review rate | Reviewed | Fraud reviewed | Precision | Recall |
|---:|---:|---:|---:|---:|
| 0.5% | 443 | 394 | 88.9% | 13.0% |
| 1.0% | 886 | 663 | 74.8% | 21.8% |
| 2.0% | 1,772 | 890 | 50.2% | 29.3% |
| 5.0% | 4,430 | 1,291 | 29.1% | 42.4% |

### Test operating points

| Review rate | Reviewed | Fraud reviewed | Precision | Recall |
|---:|---:|---:|---:|---:|
| 0.5% | 443 | 401 | 90.5% | 13.0% |
| 1.0% | 886 | 707 | 79.8% | 22.9% |
| 2.0% | 1,772 | 988 | 55.8% | 32.0% |
| 5.0% | 4,430 | 1,321 | 29.8% | 42.8% |

## 2. Why alpha = 1e-3

A first alpha = 1e-5 streaming pilot produced severe score saturation:
- more than 1% of validation probabilities were exactly/near 1;
- validation 1.0%, 0.75% and 0.5% policy thresholds collapsed to the same value.

A regularization screen showed alpha = 1e-3:
- improved PR-AUC and ROC-AUC;
- materially improved Brier score;
- produced a usable non-degenerate validation tail.

This is a model-feasibility choice, not classifier optimization as the thesis contribution.

## 3. Shared policy calibration

Validation-tail thresholds:

- base 1.00%: **0.578884**
- soft 0.75%: **0.732727**
- hard 0.50%: **0.904288**

Reference alert-arrival rate:
- **1.1776 alerts/hour**

Core capacity:
- Low = 0.75 × reference;
- Medium = 1.00 × reference;
- High = 1.25 × reference.

Queue:
- FIFO core baseline.

BLOCK:
- off in this pre-adaptation replay.

## 4. Fixed vs Capacity-aware replay

| Capacity | Policy | Reviews | Backlog | Fraud intercept | Fraud exposure at horizon | Legit intervention | Mean wait | P95 wait |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| Low 0.75 | Fixed | 1,371 | 724 | 13.14% | 437,102 | 0.566% | 172.7 h | 328.4 h |
| Low 0.75 | Capacity-aware | 740 | 93 | 17.22% | 427,876 | 0.151% | 67.8 h | 113.0 h |
| Medium 1.00 | Fixed | 1,371 | 516 | 17.65% | 425,192 | 0.566% | 117.2 h | 230.7 h |
| Medium 1.00 | Capacity-aware | 941 | 86 | 21.25% | 417,789 | 0.254% | 45.5 h | 79.1 h |
| High 1.25 | Fixed | 1,371 | 309 | 22.22% | 412,570 | 0.566% | 66.3 h | 151.5 h |
| High 1.25 | Capacity-aware | 1,089 | 48 | 23.97% | 407,044 | 0.358% | 26.3 h | 46.3 h |

## 5. Interpretation

### Temporal alert-rate drift is operationally visible

The base threshold is chosen to create 1% validation review load, but the test score distribution generates **1,371 reviews**, about 1.55% of the test stream.

So a fixed score threshold does not preserve review volume under forward distribution shift.

### Capacity-aware routing has a strong congestion effect

Across all three capacity levels, Capacity-aware:
- reduces review volume;
- sharply reduces backlog and waiting time;
- reduces legitimate intervention;
- increases fraud interception within the finite observation horizon.

This happens because it prevents lower-ranked alerts from consuming scarce queue capacity when congestion is high.

### Do not overclaim

This is not evidence that Capacity-aware is universally superior.

The result is conditional on:
- the IEEE baseline score;
- validation-tail policy calibration;
- FIFO;
- the chosen 24/72 backlog-hour congestion triggers;
- no direct BLOCK;
- finite-horizon review semantics.

The final claim must be evaluated again after Static/Adaptive fraudster feedback is added.

## 6. Cross-scenario significance so far

Pre-adaptation Xente and IEEE now both show:

> congestion-aware routing can reduce operational overload under scarce analyst capacity.

But IEEE is meaningfully different:
- score separation is weaker;
- probability calibration drifts more;
- fixed-threshold alert rate changes substantially forward in time;
- the relative operational gain from Capacity-aware is large.

This is the first concrete evidence that the two core datasets are complementary rather than redundant.

## Next milestone

Build the IEEE feature-level fraud strategy generator using only interpretable empirical dimensions supported by EDA:
- TransactionAmt;
- ProductCD;
- card/entity context;
- device/identity availability/context;
- relative timing if used.

Masked C/D/M/V fields may be preserved as detector context but must not be named as explicit fraudster actions.

Then connect:
Static / Adaptive fraudster → feature-level IEEE event → risk rescoring → policy → queue → feedback.


## Independent October 20 canonical frozen-baseline replication and temporal score drift

A **new actual re-execution** using the exact `scripts/train_ieee_streaming_baseline.py` code from the public `chatgpt-draft` source snapshot (Git SHA `d7c398577378007842452970e68fd39ae28bff72`) and the original IEEE competition ZIP reproduced:
- Validation PR-AUC = **0.3643868532231502**, ROC-AUC = **0.8218108469909943**, Brier = **0.02839840203523636**.
- Held-out test PR-AUC = **0.38403028294875263**, ROC-AUC = **0.8218995788366048**, Brier = **0.0336979478597641**.
- Saved frozen model bundle SHA256 = `3783dc167d06a335853bac3037cd6b511b8c42a59afda3826c42e64fc383b520`. Original competition ZIP SHA256 = `4cc646da09d0a9b265983ffed775b1f9ee15af5266586df610e04d6adae0b829`.
- Original non-fast online scorer reference check on 200 unchanged holdout events: **PASS**, maximum absolute difference **6.073×10⁻⁹**.
- **Full 88,581 event** held-out, unchanged-stream fast online scorer vs frozen saved baseline: **PASS**, maximum absolute difference **4.3138051×10⁻⁷**; mean absolute difference **1.8728532×10⁻⁸**, threshold `1e-6`. Fast-score full audit completed in approximately 11 seconds after history warmup. This checks numerical equivalence, NOT synthetic fraud realism.

Additional independently computed score drift (validation-score bin definitions frozen from validation):

| Metric | Validation | Holdout test |
|---|---:|---:|
| Mean frozen risk probability | 0.0653414 | 0.0946393 |
| Observed fraud prevalence | 0.0343415 | 0.0348043 |
| 10-bin expected calibration error (ECE; validation bins) | 0.031072 | 0.059835 |
| Alert fraction at a threshold chosen for top 1% validation | 1.0002% | 1.5489% |
| Alert fraction at a threshold chosen for top 0.5% validation | 0.5001% | 0.6615% |

This is a **measurable temporal scoring/alert-load shift**. ECE depends on the binning convention and is only a diagnostic, not a universal calibration property. The 1% operating-point comparison uses `np.quantile` on serialized validation scores, hence may differ by a very small numerical amount from a threshold computed before score CSV rounding.

The new actual baseline/audit was completed independently of the October 18 local mirrored pilot. The fact that canonical scoring reproduces does **not** by itself complete canonical 12×N adaptive-policy experiments; those are tracked separately.
