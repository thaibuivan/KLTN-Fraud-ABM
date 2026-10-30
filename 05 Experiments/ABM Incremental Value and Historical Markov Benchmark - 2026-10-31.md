# ABM incremental value: stress-test versus empirical Markov baseline (31 Oct 2026)

> **Status: NEW INDEPENDENT FROZEN-SCORE BENCHMARK, NOT THE CANONICAL ONLINE IEEE-CIS SIMULATION.** Data: public IEEE-CIS labeled training file 590,540 rows, chronological 70/15/15; frozen independent LightGBM (PR-AUC validation 0.4467, holdout 0.4232). Heldout 88,581 events including 3,083 fraud attempt slots. Validation 3,042 fraud donor contexts. Each reported configuration = 120 paired simulation seeds. The detector and donor scores are frozen across the run (unlike canonical scorer). Under no circumstances pool this analysis with the manuscript's 30-seed canonical results.

## Research question

Does fraudster policy-response learning add essential value to capacity-constrained fraud policy evaluation beyond an observable transaction stream, a fixed donor mixture, and a **Markov temporal mixture estimated only from historical train data**?

## Evidence A — observed fraud regime temporal dependence

Amount groups low/middle/high defined using TRAIN fraud terciles 48.693 and 117. A first-order Markov model trained on historical fraud-labeled records predicts the next observed fraud amount category better than an IID amount-mixture baseline.

| Model | Negative log likelihood per validation fraud record | Per heldout fraud record |
|---|---:|---:|
| IID | 1.0977 | 1.0979 |
| Markov 1 | **1.0097** | **0.9977** |
| Markov 2 (exploratory) | 0.9995 | 0.9906 |

Test Markov-1 score improvement about +0.1002 log units per fraud event; 95% bootstrap-by-relative-day interval [+0.0866,+0.1136]. **Critical caveat:** advantage disappears when previous fraud-labeled record is >=5 minutes earlier (test mean score gain -0.0186) or ProductCD differs (-0.1445). Mostly **transaction clustering/product mix**, not evidence of a real identified fraudster's strategic learning. This retrospectively requires previous fraud labels, which are not necessarily known live.

## Evidence B — head-to-head model ladder at 65% normalized analyst capacity

Effect = Capacity-aware interception proxy minus Fixed interception proxy, percentage points. REVIEW START is a proxy, NOT prevented loss.

| Model | Fixed fraud interception | Capacity-aware | Policy effect |
|---|---:|---:|---:|
| M0 DES observed score replay | 16.02% | 16.54% | +0.519 pp |
| M1 Static mixture from validation | 16.53% | 17.04% | +0.506 pp |
| M1m Markov mixture from historical TRAIN | 16.71% | 17.25% | +0.539 pp |
| M2 Adaptive epsilon-greedy ABM | 13.96% | 13.76% | **-0.201 pp** |
| Static oracle after seeing Adaptive shares | 13.91% | 13.71% | -0.200 pp |

M2 minus train-Markov interaction = **-0.740 pp**, paired seed t CI95% **[-0.781,-0.698] pp**. This is conditional simulation evidence of policy ranking sensitivity to scenario behavior, not a bank-level causal policy effect.

## Critical falsification results (do NOT omit from advisor report)

1. The post-hoc oracle static baseline reproduces the M2 policy effect near-exactly. Therefore the policy reversal **does not uniquely demonstrate a need for feedback-learning agent**.
2. Exploratory static high-amount shares 0/25/50/75/100% produce policy effects at 65% capacity **+0.709/+0.613/+0.322/-0.041/-0.189 pp**. Static scenario stress can recover the sign reversal.
3. Adaptive informed by the actual policy decision rather than a fixed-policy shadow feedback changes policy effect at 65% capacity by only **-0.0065 pp** (paired seed CI95% [-0.0097,-0.0033]). This is small in operational magnitude even if statistically distinguishable within the simulation.
4. The Adaptive high-amount share is **~92%**, against ~**28.7%** observed in the labeled IEEE holdout. This is a bounded stress scenario **not an empirically validated behavioral forecast**.
5. At high normalized capacity the policy effects approach zero; do not highlight a selected severe-capacity cell as universal.

## Correctness audit and replication

- An independently implemented Python FIFO simulator matched the Numba fast simulator on **24 cases using 12,000 chronological events and 407 fraud slots**; a prefix-normalization mismatch was fixed in the reference test only, because the full-run kernel uses the 3,083-event full-test denominator by design.
- Actual main 120-seed run-level dataset has paired cell results for six capacities (0.35/0.5/0.65/0.75/1.0/1.25), two policies and eight modes. A separate 120-seed static stress grid checks five ex ante category mix values *but was explored after seeing earlier ABM results*, therefore exploratory, not pre-registered.
- Original IEEE raw archive ZIP SHA-256: `4cc646da09d0a9b265983ffed775b1f9ee15af5266586df610e04d6adae0b829`. Fast frozen-score run CSV SHA-256: `d20c969bf21d00d4fc1935faad91d204d69934dc12001a9dd7de8f723019ef98`. Full code, simulated CSV and metadata preserved in conversation artifact, not raw data repository.

## Scientific verdict

**GO as a transparent conditional ABM–DES stress-test feasibility prototype. NOT YET GO for claiming agent-based feedback is uniquely necessary or empirically realistic.** Further evidence requires approved historical review action/feedback logs, persistent entity identities, an independently observed policy intervention or a redesigned empirically grounded problem. Run canonical online-scorer model with the same train-Markov and realistic non-agent stress baselines before final academic inference.

Validation guidance: Grimm et al. (2020) ODD; Collins et al. (2024) JASSS validation; *How to keep it adequate* (2022), https://doi.org/10.1016/j.envsoft.2022.105559.
