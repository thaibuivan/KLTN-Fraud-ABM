# Markov/HMM vs ABM: evidence and experiments to justify ABM — 30 Oct 2026

**Research decision:** Yes, investigate the supervisor's Markov/HMM suggestion as *time-state statistical baselines*. Do **not** replace or artificially embellish the frozen ABM core with Markov merely for complexity. Quantify *incremental model value*.

## A. One clear question
Under finite review capacity, does adding fraudster policy-response feedback change the assessment/ranking/trade-off of Fixed-threshold vs Capacity-aware policies, beyond what simpler data/statistical/DES models imply?

Markov/HMM models the **temporal environment regime**; DES handles **events and queues**; ABM adds **feedback-dependent action selection**. These are complementary, not interchangeable.

## B. Existing ABM results: difference in policy effects (descriptive from cell means)

Effect of policy = Capacity-aware interception proxy minus Fixed interception proxy. The interaction = effect under Adaptive minus effect under Static, in **percentage points**.

| Environment | Capacity | Static policy effect | Adaptive policy effect | Interaction |
|---|---|---:|---:|---:|
| Xente (50-seed reported means) | Low | -1.72 | -3.20 | **-1.48** |
| Xente | Medium | -1.48 | -2.52 | **-1.04** |
| Xente | High | +1.04 | +0.80 | **-0.24** |
| IEEE-CIS (30-seed manuscript means) | Low | +3.08 | +1.04 | **-2.04** |
| IEEE-CIS | Medium | +2.04 | +0.12 | **-1.92** |
| IEEE-CIS | High | +0.66 | +0.00 | **-0.66** |

All six *mean-model interaction estimates* have the same negative sign, despite opposite levels of absolute policy effect between data environments. **This is hypothesis-generating only**: differences taken from rounded cell averages, no seed-level interaction CIs, no independently checked IEEE 30-seed CSV/manifest in this work session, and not causal evidence of real fraudster responses.

The main fraud interception proxy counts direct BLOCK or REVIEW *service started* by finite horizon. It is NOT realized financial loss prevented.

## C. New independently executed empirical time-model benchmark — observed Markov state

Dataset: original public IEEE-CIS labeled `train_transaction.csv`, 590,540 chronological rows; train first 70%, validation next 15%, last 15% **unused**. Time bins are 24h in *relative TransactionDT* (119 full train bins, 31 full validation bins, excluding boundary partial bins).

Observed binary state = daily *fraud-label share* greater than training-day median (threshold approx **3.614%**). Estimate first-order Markov state transition with 0.5 pseudocounts:
`A≈[[0.6311,0.3689],[0.3644,0.6356]]`.
Compare one-step validation state forecasts against an IID Bernoulli high-state prevalence learned on train.

| Validation metric (lower better) | IID Bernoulli | First-order Markov |
|---|---:|---:|
| Binary log loss | **0.69130** | 0.72212 |
| Brier score | **0.24908** | 0.26390 |

**Result:** In this prespecified retrospective 24h binary state setup, Markov does NOT improve held-out prediction. This does not imply that Markov models are universally useless. A critical limitation is that prior-day state is computed using **verified fraud labels**; the exercise is retrospective, and cannot be presented as a deployable live real-time forecast when labels arrive late.

The separately recorded **Poisson–HMM** pilot for 24h fraud counts also failed to demonstrate strong incremental Markov information: validation total log likelihood Poisson -179.031; 2-Poisson IID mixture -153.770; 2-state Poisson–HMM -153.657; negative binomial -141.817 (higher better). Different metrics/tasks from the binary Markov benchmark: **do not put their scores on the same axis**.

Raw transaction files and model bundles stay private; no per-transaction information is committed.

## D. Direct test needed to justify ABM

Design a controlled model ladder, holding policy, score and capacities constant:

- **M0:** DES-only static observed-risk-score replay and FIFO queue.
- **M1:** DES + validation-fraud donor generator with fixed strategy distribution.
- **M2:** M1 + epsilon-greedy strategy updates from policy feedback.
- **Optional M3:** M2 with an empirically supported or explicitly hypothetical nonstationary arrival regime (e.g., NB, HMM only if justified).

The *M1 versus M2* comparison isolates the assumed adaptation mechanism more directly than M0 versus M2, since M0 also removes generation/rescoring.

For each, report policy contrasts and **paired-seed interaction CIs**, fraud BLOCK vs REVIEW start/completion, backlog and review counts, matched-review-budget diagnostics, trajectories `Q(t)`, `T_R(t)`, strategy shares and waiting times. Stress-test reward, alpha/epsilon, REVIEW observability and score degradation.

**Success criterion:** M2 changes a meaningful policy trade-off or ranking, the effect persists under plausible assumption changes, and the extra complexity is justified by its contribution to the research question. Otherwise simplify model claims; do not equate code-level differences with empirical realism.

**Suggestion for advisor report:** show Section B's existing comparison as *first evidence*, Section C's negative Markov finding as *model-selection discipline*, and the M0–M2/trajectory tests as *next decisive scientific validation*.

Primary related papers: Shen & Kurshan (2020), Mayo et al. (2023, 2024), Grimm et al. (2020). Existing source files: `05 Experiments/Xente Feature-Level Core Run v0.2.md`, 22-Oct 38-page manuscript Section 5.3, and `01 Literature/Mayo 2023 Strategic ABM and IEEE HMM Feasibility - 2026-10-28.md`.
