# IEEE-CIS Adaptive Full-Test Pilot v0.2 — 5 seeds (18/10/2026)

> **Research status:** empirical pilot, not final thesis inference. Full raw data/model bundles were processed privately, NOT committed. No internal Green SM materials used.

## Reproduction and validation milestones

Original IEEE labeled training set: 590,540 transactions. Chronological split: train 413,378 / validation 88,581 / test 88,581. Validation fraud donors: 3,042; test fraud-attempt slots: 3,083.

A local independent reconstruction of the repository's SGD log-loss training pipeline reproduced its metrics:
- Validation: PR-AUC **0.36438685**, ROC-AUC **0.82181085**, Brier **0.02839840**.
- Test: PR-AUC **0.38403028**, ROC-AUC **0.82189958**, Brier **0.03369795**.

Full **88,581-event** unchanged-stream audit of the fast online scorer against saved test baseline predictions: max absolute error **4.3138e-7**, mean **1.8729e-8**, meeting tolerance 1e-6. The 300-event reference online scorer also passed with max difference about 6.07e-9. These are real-data equivalence checks, not validation of adversarial cognition.

IEEE fraud generator draws coherent transactions from **validation-fraud amount regimes**: terciles at 50 and 117, with sizes 1,052 / 1,030 / 960. Test fraud observations supply only fixed attempt timestamps, never donors.

## Full-test 12-cell × 5-seed pilot: mean results

| Mode | Policy | Capacity | Fraud interception proxy | End backlog |
|---|---|---|---:|---:|
| Static | Fixed | Low | 14.99% | 478.2 |
| Static | Capacity-aware | Low | 18.19% | 63.6 |
| Adaptive | Fixed | Low | 9.63% | 166.8 |
| Adaptive | Capacity-aware | Low | 10.38% | 21.2 |
| Static | Fixed | Medium | 18.76% | 268.0 |
| Static | Capacity-aware | Medium | 20.82% | 37.4 |
| Adaptive | Fixed | Medium | 11.49% | 17.8 |
| Adaptive | Capacity-aware | Medium | 11.57% | 14.0 |
| Static | Fixed | High | 21.91% | 98.2 |
| Static | Capacity-aware | High | 22.67% | 35.0 |
| Adaptive | Fixed | High | 11.73% | 3.2 |
| Adaptive | Capacity-aware | High | 11.73% | 3.2 |

Under Low capacity, the within-seed contrast Capacity-aware minus Fixed for Static was +3.20 percentage points interception, -414.6 backlog. For Adaptive the same comparison gave +0.75pp interception, -145.6 backlog.

Mean high-amount strategy share: **Static 31.66%**, **Adaptive 92.84%** across 5 seeds; opposite the *low-amount regime shift* previously found in Xente. This is a difference in **model dynamics under two empirical scenarios**, not evidence that real adversaries necessarily learn opposite strategies.

## Targeted behavioral validity checks — seed 0 only

- Adaptive Fixed Low, value-scaled reward: high-amount share **93.29%**, interception **9.67%**.
- Changing reward to unit-per-success proxy: high-amount share **83.49%**, interception **10.70%**.
- Removing immediate REVIEW feedback left seed-0 outcomes unchanged. This is one scenario/run, not a general theorem about REVIEW observability.

## Claim rules

1. A fraud counted as intercepted in the original metric can be a BLOCK **or a REVIEW whose service starts within the horizon**; do not call this verified loss prevention.
2. The scenario's q=0/0.5/1 review-completion sensitivity is an explicit assumption, not a calibrated recovery probability.
3. Five seeds establish feasibility and preliminary patterns, **not** final convergence, parameter uncertainty or external validity.
4. Outputs were generated via a **local execution mirroring the repo's shared policy/queue/adaptation mechanisms**, with verified frozen model metrics and score equivalence. Before final submission, re-run the **canonical repository runner** using the saved private model bundle and compare outputs.
5. Cross-scenario raw monetary quantities must never be compared as if directly commensurate.
6. An account/card/entity proxy is not a known physical person; missing identity and masked C/D/M/V features remain detector context.
7. No internal Green SM documents, thresholds, customer records or implementation details were used.

## Immediate next gates

- Reproduce this pilot with the canonical GitHub runner and archive its command, commit SHA, seeds, config and output checksum.
- Increase repetitions until MCSE/interval stability, especially heavy-tailed exposure.
- Replicate reward and REVIEW observability ablations across more seeds and other parameter values.
- Use paired, within-scenario contrasts for Xente vs IEEE; characterize consistent/environment-dependent/uncertain signs.
- Generate final thesis figures, discussion and parameter/uncertainty appendices.

Code: scripts/run_ieee_feature_level_static_adaptive.py, scripts/ieee_fast_online_scorer.py, scripts/summarize_ieee_closed_loop.py. CI (latest Oct 18): **60 tests passed**.
