# Three foundations of KLTN-Fraud-ABM — research reassessment (28/10/2026)

**Context:** Advisor has reviewed the research direction only, not the actual experiment results. Do not infer rejection of the thesis.

## 1. Real-world research object

The target is **transaction fraud-alert management** under finite review capacity, not an identified bank or criminal. The observation unit is a labeled transaction. Xente provides a CustomerId and actual timestamps; IEEE has relative TransactionDT and card/address context only. The **model entities** comprise an effective adaptive fraudster strategy chooser, a frozen risk engine, Fixed/Capacity-aware policy and persistent pooled analyst queue.

Thus the model's correct label is a **hybrid ABM–DES policy stress-test**, NOT an empirical behavioral twin. Its primary inferential target is the difference between simulated policy outcomes across conditions.

## 2. Data observability

| Component | Status |
|---|---|
| Amount, category, timestamp, fraud label | Observed (competition data) |
| Xente customer history | Derived from provided CustomerId; not external verified natural person |
| IEEE identity | card1+addr1 proxy, NOT true customer ID |
| Fraudster learning, epsilon, alpha, reward, REVIEW observability | Explicit unobserved behavioral assumptions |
| Analyst real-world service/accuracy/recovery | Unavailable; only normalized capacity/scenario outcome bounds |
| Heldout fraud attempt timing | Uses labeled test fraud slots to **condition** counterfactual events; not a separate arrival prediction |

Xente labeled data: 95,662 transactions, 193 fraud. IEEE labeled data: 590,540 transactions, 20,663 fraud. Data supports empirical **input/environment patterns**, not a directly fitted cognitive fraudster agent. IEEE 30-seed results are reported in the 22-Oct manuscript, but run-level CSV/checksum still require independent audit.

## 3. ABM necessity versus simpler models

The simplest competing model is **policy replay + discrete-event FIFO queue** on a fixed observed risk-score stream. It already predicts workload/backlog mechanically; dynamic policy's queue reduction by alert shedding is not sufficient novelty.

**Essential incremental mechanism:** policy outcomes change subsequent fraudster strategy selection, which changes sampled fraud contexts/online scores and subsequent queue states. This assumed feedback mechanism must be tested by ablation.

Proposed nested model comparison:
- **M0:** historical score/policy/queue replay (DES only).
- **M1:** StaticMixture generator + same policy/queue.
- **M2:** Adaptive generator with assumed feedback + same policy/queue.

Quantify policy effect within each model and a difference-in-differences across M2 vs M1, with paired seed CIs and matched review-budget diagnostic. Include no-review-observation and alternative reward assumptions. Report that M2−M1 is a **within-model sensitivity**, not a causal real-bank impact.

Illustration from Xente 50-seed report, low capacity means: policy interception effect -1.72 percentage points (Static), -3.20 (Adaptive); interaction -1.48 pp. Policy backlog effect -18.92 cases (Static) and -24.86 (Adaptive); interaction -5.94 cases. These are descriptive differences from means, **not significance claims** without raw per-seed intervals.

## 4. HMM position

Mayo et al. (2023) varied payment attempt **frequency and value**; current ABM changes amount/context regime but uses fixed attempt slots. Model could test alternative temporal arrival processes. Existing IEEE 24h Poisson–HMM pilot did not show predictive improvement over a simple two-Poisson mixture and lost to Negative Binomial; no justification to make HMM mandatory in core.

## 5. Decision

**Keep the current direction provisionally, strengthen Chapter 3 and validity tests, do not rebuild thesis.** Change topic only if advisor requires observed real-person behavior in agents (beyond mechanism stress-testing), or if rigorous M0/M1/M2 and empirical-pattern tests fail to demonstrate research value for the accepted thesis objective.

**Immediate writing tasks:** (1) explicitly define target system, observation unit, model agents, claims; (2) evidence matrix empirical/derived/literature/assumed; (3) ABM vs DES/Markov justification tied to falsifiable comparison; (4) verification, pattern validity, robustness, cross-scenario uncertainty; (5) lock original IEEE 30-seed run CSV and checksum.

### Primary academic sources
- Grimm et al. (2020), ODD: https://www.jasss.org/23/2/7.html
- Sargent (2013), verification and validation: https://doi.org/10.1057/jos.2012.20
- Wellman (2016), putting agents in ABM: https://doi.org/10.1007/s10458-016-9336-6
- Mayo et al. (2023): https://kmayo.com/files/papers/mufin23_fraud.pdf
- Mayo et al. (2024): https://doi.org/10.24963/ijcai.2024/18
- Shen & Kurshan (2020): https://arxiv.org/abs/2010.11062
- Dervovic et al. (2021): https://doi.org/10.24963/ijcai.2021/579
- Dal Pozzolo et al. (2018): https://pubmed.ncbi.nlm.nih.gov/28920909/
- ABM context-adequate validation (2022): https://doi.org/10.1016/j.envsoft.2022.105559
