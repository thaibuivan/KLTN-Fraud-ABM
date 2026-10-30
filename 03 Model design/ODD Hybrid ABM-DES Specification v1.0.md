# ODD v1.0 — Hybrid agent-based / discrete-event transaction-fraud policy simulation

**Date:** 2026-10-18 · **Status:** executable-model documentation / research audit; not empirical validation or approval by GVHD.  
**Scope:** 24 core cells = (Xente, IEEE-CIS) × (static mixture, adaptive fraudster) × (fixed, capacity-aware) × (0.75, 1.00, 1.25 normalized capacity).  
**Reporting framework:** Grimm et al. (2020), *ODD Protocol* (https://doi.org/10.18564/jasss.4259).

## I. Overview

### 1. Purpose and question
Estimate conditional **differences among transaction-fraud management policies** when fraud attempts may alter their amount-regime choices based on modeled policy feedback and analyst service capacity is finite. RQ1: adaptation effect; RQ2: policy trade-off; RQ3: capacity interaction; RQ4: cross-environment robustness. This is NOT a bank-specific digital twin or estimator of observed criminal preferences.

### 2. Entities, state variables, and scales
| Entity / component | Persistent state | Action / purpose | Implementation |
|---|---|---|---|
| Fraudster agent | strategy value estimates, currently selected strategy, epsilon-greedy RNG; counters | choose amount regime; consume modeled APPROVE/REVIEW/BLOCK response; update values | `scripts/adaptive_fraudster.py` |
| Static comparator | frozen validation-derived regime weights, RNG | choose regime without policy-response learning | `StaticMixtureFraudster` |
| Transaction and entity history | Xente synthetic-fraudster past-only velocity; IEEE entity-proxy past-only features | generate/rescore event using history strictly before that event | `xente_online_features.py`, `ieee_online_scorer.py` |
| Detector (module, not necessarily agent) | frozen coefficients/transformers; streaming state for IEEE | compute risk score; does not learn from test labels | `xente_fast_scorer.py`, `ieee_fast_online_scorer.py` |
| Policy (module) | fixed operating points or queue-dependent REVIEW tier | choose APPROVE, REVIEW, BLOCK | `fraud_policies.py` |
| Queue and pooled analyst resource | waiting events, service completion clock, finite service rate | serve FIFO review arrivals; accumulate backlog | `policy_queue_engine.py` |
| Observer/accounting | event/action/review records, horizon | aggregate fraud, intervention, queue outcomes | `policy_queue_engine.py`, `outcome_semantics.py` |

Core analyst capacity is **pooled deterministic service**, not individually autonomous analyst agents. Observed legitimate stream is mainly replayed: Xente legitimate scores are held frozen while IEEE legitimate events are rescored online in the counterfactual stream. Avoid suggesting all legitimate customers are autonomous behavioral agents. Model characterization: **agent-based adversarial behavior embedded in discrete-event policy and queue simulation**.

Time: Xente UTC observed timestamps; IEEE `TransactionDT` is relative seconds, mapped to a synthetic epoch *only for simulation scheduling*. Do not interpret IEEE simulated epoch as an actual calendar date. No geographically explicit space.

### 3. Process overview and schedule
1. On training/validation data, fit independent frozen risk models, define 1.00/0.75/0.50% validation review-tail thresholds and 0.10% BLOCK-tail threshold per scenario. Determine service-rate reference from validation base-alert arrivals.
2. Initialize static/adaptive fraudster, RNG, policy and empty FIFO queue; initialize history per scenario. IEEE warms history on pretest events without test labels. Xente synthetic-fraudster history starts empty.
3. Traverse held-out test-event chronology. Real fraud labels select **fixed attempt time slots**, NOT donor contexts. At an attempt, agent chooses low/middle/high amount regime and the generator samples a coherent validation-fraud row; synthetic identity/time substitution follows scenario specification.
4. Score new event using frozen detector and past-only features. IEEE rescoring also updates legitimate transaction histories; Xente legitimate risk scores remain fixed from baseline (known approximation).
5. Advance queue/service to current time. Policy sees current queue and score, acts APPROVE/REVIEW/BLOCK. REVIEW is enqueued and may start immediately if server idle.
6. Core adaptive agent updates regime value from **immediate policy action feedback**; static agent records but does not learn. The REVIEW observability alternative omits this update on REVIEW; neither variant demonstrates what a real fraudster can see.
7. At horizon, summarize actions, begun review and unresolved alerts. Alternative outcome accounting separates *completed* reviews from merely started reviews.

Xente sorts legitimate events ahead of synthetic attempt slots when timestamps coincide. IEEE sorts by `TransactionDT`, then `TransactionID` for stable ordering. The event order must be documented because it affects past-state and congestion.

## II. Design concepts

### 4. Basic principles and emergence
Adaptation uses a lightweight multi-armed-bandit-like value update, **not a calibrated adversary cognitive model**. Emergent quantities are policy–queue workload, strategy-share shift, reviewed-fraud proxy and customer intervention. Capacity-aware policy creates endogenous routing–backlog feedback; generated fraud affects detector state, policy routing and future feedback.

### 5. Adaptation, objectives, learning and prediction
For chosen strategy s, `V_s <- V_s + alpha*(r-V_s)`; epsilon-greedy chooses a random strategy with probability epsilon and otherwise one maximizing V. Core alpha=0.15 and epsilon=0.10; both are assumed, not identified from data. Reward uses scenario amount / validation-fraud median amount: approve = positive; review = -0.15 scaled; block = -1 scaled. Reward ablation tests unit-per-success instead of value-dependent reward. Fixed policy itself is **not a learning RL policy**.

### 6. Interaction, observation, sensing and stochasticity
Fraudster and policy interact through generated features → detector → decision → immediate assumed feedback. Queue capacity and congestion state are observed by Capacity-aware policy, not by fraudster directly. Randomness: initial strategy selection, epsilon exploration, donor-row resampling and seed. Core queue service duration = 1/service_rate (deterministic). No communication/network among fraudsters in core model.

**Key observability limitation:** `REVIEW` may be an internal bank action; fraudster's immediate awareness is an explicit stress assumption. The available `no_review_observation` ablation **drops** updates on reviews, not a validated delay distribution.

**Key synthetic identity limitation:** all Xente generated frauds currently reuse `SIM_FRAUDSTER` in the feature-level generator, which can create a concentrated synthetic history/velocity signature. Treat as a *structural* feature of the stress environment and test alternate fraudster identity/history patterns before claiming realism.

### 7. Collectives and heterogeneity
Core includes one effective adaptive strategy chooser per run; it is **not a population calibrated to individual criminals**. Coherent fraud donor contexts introduce heterogeneity in amount/product/card/device but do not identify deliberately controlled attributes. IEEE `card1+addr1` is an entity proxy, not a verified bank account or natural person; masked C/D/M/V variables remain detector context and must not receive behavioral interpretations.

## III. Details

### 8. Initialization
Freeze classifier on chronological 70/15/15 labeled split per scenario and calibrate thresholds using validation, NEVER test labels for fitting. Static regime weights from validation frauds; adaptive strategy values initialized equally. Dormancy off in core to preserve test fraud attempt counts. Queue starts empty. Capacity ratios 0.75/1/1.25 relative to each scenario's validation mean base-alert arrival rate.

### 9. Input data
**Xente:** 95,662 labeled train transactions, 193 fraud; true `CustomerId`, `TransactionStartTime`, `Amount`, `Value`, channel/product/provider. Generator draws from validation fraud terciles of `Value`, rescoring synthetic raw contexts using saved logistic model. Legitimate test scores currently fixed despite synthetic history changes.

**IEEE-CIS:** 590,540 labeled historical transactions, relative transaction time, `TransactionAmt`, `ProductCD`, card/address and optional device/identity/masked features. Historical events warm online proxy history; validation donors only; test-fraud timestamps are attempt slots. Generator samples entire coherent validation-fraud context conditioned on validation-fraud amount tercile; generated and legitimate test events are rescored with frozen streaming-SGD risk model. Reference–fast scoring equivalence was documented on unchanged test stream (88,581 events), tolerance 1e-6; re-run canonical runner before final results.

Neither dataset provides actual analyst actions, review resolution time, analyst effectiveness, fraudster learning parameters or observed counterfactual responses.

### 10. Policy, queue and outcome submodels
Let p = risk score, T_B = block threshold, T_R = review threshold. Action = BLOCK if p≥T_B, REVIEW if T_R≤p<T_B, else APPROVE. Capacity-aware uses estimated backlog-hours `Q/mu` to replace T_R with stricter thresholds at 24/72 backlog-hours. FIFO baseline; risk-priority structural sensitivity.

Core **legacy** `fraud_intercept_rate` counts direct BLOCK plus fraud REVIEW whose service *begins* by finite horizon. This is a **service-start interception proxy**, not documented monetary prevention. Record distinct values for directly blocked, approved, review started, review completed and unresolved. `outcome_semantics.py` defines hypothetical completion-only prevention with q∈{0,0.5,1}, giving expected prevented value = blocked value + q×completed-fraud-review value. q is an explicit assumption, not an empirical estimate of recovery; exposed value at horizon ≠ realized loss.

### 11. Parameter provenance
| Type | Parameters | Evidence strength |
|---|---|---|
| Empirical | fraud prevalence, amount donor support, context mix, timestamps, detector score distributions | dataset-specific but temporally limited |
| Empirical + decision rule | validation tail thresholds; reference validation arrival rate | threshold target is an experimental policy choice |
| Literature mechanism / explicit stress | finite capacity, FIFO, normalized ratios, congestion tiers | not bank-staffing calibration |
| Behavioral assumption | strategy choices, value reward, alpha/epsilon, immediate REVIEW feedback | not recoverable from fraud labels |
| Economic/outcome assumption | q review effectiveness, cost of friction/recovery | hypothetical sensitivity only |

### 12. Validation and sensitivity acceptance criteria
- **V1 Code:** 60+ CI tests; correct event ordering, no target leakage, conservation of action counts, deterministic repeat for same seed; document GitHub Actions runs.
- **V2 Empirical:** amount/product/identity donor support; test labels affect only attempt slots; no post-test model calibration.
- **V3 Causality:** matched within-seed policy contrasts; same attempt counts/timing; note adaptive trajectories diverge so seed pairing is not identical realized transactions.
- **V4 Model form:** alpha/epsilon, reward unit/value ablation, immediate/hidden REVIEW, Xente synthetic-identity/history variation, FIFO vs risk-priority; test degraded scores.
- **V5 Operational:** service-start vs completion-q assumptions, queue invariants, extreme capacities; label pending review correctly.
- **V6 Uncertainty:** Monte Carlo SE, paired confidence intervals and convergence for counts, backlog and heavy-tailed value exposure; 5-seed IEEE pilot is *preliminary* only.
- **V7 Cross-scenario:** compare signs and conditional effects, never raw monetary levels or raw score thresholds across Xente and IEEE.

## IV. Limitations and literature
This protocol describes **the current implementation, including its asymmetries**, rather than an idealized feature-complete system. It is suitable for *conditional policy stress testing*, not operational deployment, behavioral identification or universal policy-optimum recommendations. Results may be mechanically influenced by how fraud is generated, how feedback is revealed and what a review is assumed to accomplish.

**Key methodological references:** Grimm et al. (2020), https://doi.org/10.18564/jasss.4259; McCulloch et al. (2022), https://doi.org/10.18564/jasss.4791; Shen & Kurshan (2020), https://doi.org/10.1145/3383455.3422563; Höppner et al. (2022), https://doi.org/10.1016/j.ejor.2021.05.028.

**Next:** canonical IEEE artifact-based run and seed convergence; formal cross-scenario contrasts; advisor review; revise ODD only when code/assumptions actually change.
