# THESIS LOCK GATES — 18/10/2026

> Live implementation tracker. **Do not call this thesis ready-to-submit while the required empirical validation below is pending.** Earlier MASTER STATUS has useful history but may be stale; cross-check this with the newest run reports and commit SHA on the draft branch.

## A. Confirmed today

- [x] Identified and read 18-Oct 21:29–21:30 failed CI logs. Python test issue: `test_three_way_split_and_validation_only_donors` raised `KeyError: identity_available`; report `1 failed, 50 passed`. Later runs at 21:31 succeeded; latest observed test suite 60 passed.
- [x] IEEE canonical code exists; local real-data pilot report exists at `05 Experiments/IEEE-CIS Adaptive Full-Test Pilot v0.2.md`, **12 core cells × 5 seeds**. This remains exploratory.
- [x] Added canonical runner `--seed-start` support and regression tests for nonoverlapping, deterministic seed-batch execution. Check corresponding GitHub Actions runs before relying on changes.
- [x] Added model ODD documentation (`03 Model design/ODD Hybrid ABM-DES Specification v1.0.md`), Literature Review (`06 Writing/Literature Review Full Draft v1.0.md`) and Results/Discussion (`06 Writing/Results and Discussion Full Draft v1.2.md`).
- [x] Updated IEEE runbook with safe canonical batching, per-cell comparison, duplicate checking and private artifacts policy.
- [x] Refreshed draft PR #1 description to reflect 24-cell research design and current unfinished gates; remains draft. **Do not merge to main without review**.

## B. Required BEFORE calling IEEE main experiments final

- [ ] Materialize/download legally usable **private reproduction ZIPs** into a local authorized machine. Library metadata lists `KLTN_IEEE_PRIVATE_REPRO_ARTIFACTS_2026-10-18.zip` and `KLTN_IEEE_5seed_PILOT_results_2026-10-18.zip`, but this chat's attempts to materialize their bytes failed with unavailable authorized backing path. Existence in Library is not execution evidence in this turn.
- [ ] Load frozen baseline bundle / validation scores; test raw split and context file integrity; repeat independent unchanged-stream online-vs-offline score equivalence.
- [ ] Execute canonical repo runner **seeds 0–4**, compare all 60 cells against existing local mirrored pilot; archive source SHA, CLI, seeds, summary and hashes. If numbers differ, investigate rather than averaging.
- [ ] Run **non-overlapping** seed batches from 5 onward until stable MCSE and paired interval diagnostics. Use `--seed-start` and save each batch in its own folder; combine with duplicate-key rejection.
- [ ] Run `scripts.summarize_ieee_closed_loop` on the final combined table. Inspect count/operation and heavy-tailed exposed value metrics separately.
- [ ] Repeat reward unit/value and REVIEW observability sensitivities across multiple seeds/conditions; document conditional direction and uncertainty.
- [ ] Check score-quality and identity persistence structural alternatives appropriate to IEEE; do not assume masked fields are strategic actions.

## C. Required BEFORE thesis claims/chapters final

- [ ] Verify policy improvement beyond mechanical load shedding or explain explicitly that load shedding is the mechanism; include effective review-budget normalization if feasible.
- [ ] Separate BLOCK, REVIEW started, REVIEW completed and hypothetical prevention q assumptions; never equate service-start proxy with avoided realized loss.
- [ ] Explicitly note Xente generator's single `SIM_FRAUDSTER` identity and contrast with IEEE's entity-proxy contexts; assess plausible structural sensitivity.
- [ ] Produce within-scenario policy contrasts and adaptation contrasts with uncertainty bands; compare **sign / normalized effects** across Xente and IEEE, not raw value units.
- [ ] Complete Introduction, Abstract, Limitations, Conclusion, References/Zotero metadata and figures/tables using verified output; review language and APA/NEU thesis format.
- [ ] Confirm access/permission status for any company-derived information; absent authorization use ONLY open datasets and public literature. No company materials were used in these commits.
- [ ] Arrange GVHD/practitioner critique of realism, outcome semantics and claims; incorporate approved revisions and perform final CI/test artifact checks.
- [ ] Merge draft PR into main only after explicit review and verified final experiment outputs; finalize reproducibility bundle without private raw data.

## D. Current interpretation

**What is defensible:** Xente has a 50-seed full-grid simulated result; IEEE has a separate 5-seed full-test exploratory pilot, a documented equivalence audit and working code. CI confirms test behavior, not external behavioral validity. Differences between the two environments are scientifically relevant **within the stated simulation assumptions**.

**What is not yet defensible:** “IEEE main fully converged”, “24 configurations completed at final inferential quality”, “fraudster cognition reconstructed”, “capacity-aware universally optimal”, “fraud value successfully prevented in a real bank”, or “thesis ready for submission”.

Next owner action: run canonical IEEE artifact-based seeds 0–4 on authorized local environment, compare against the private pilot ZIP, and advance seed batches. Next writing action: refine introduction and research-gap text after GVHD feedback.


---

## E. Implementation and independent data validation addendum — 18/10/2026 (later work)

**New verified additions:**

- [x] Independently parsed the original labeled IEEE-CIS public zip (590,540 chronological transactions), verifying train/validation/test = **413,378 / 88,581 / 88,581**, fraud = **14,538 / 3,042 / 3,083**, and identity-row availability = **26.5885% / 17.6720% / 21.0745%**.
- [x] Audited validation-fraud donor terciles = **50 / 117** and pool sizes **1,052 / 1,030 / 960**; validation fraud median = **77**. Empirical ProductCD composition differs materially across regimes (C: low **62.2%** vs high **10.5%**; W: low **24.6%** vs high **70.9%**). These are **joint donor-context changes**, not causal evidence about fraudster choosing only TransactionAmt.
- [x] Added `scripts/audit_ieee_donor_regimes.py`, tests, and `05 Experiments/IEEE-CIS Raw Validation and Donor Regime Audit v1.0.md`. Test fraud may be used only for held-out **post-hoc diagnostics**, not calibration or donor construction.
- [x] Added a resumable, privacy-preserving **canonical IEEE batch runner** at `scripts/complete_ieee_experiments.py` with `--seed-start` batches, mandatory scorer audit, 12-cell completeness checks, fail-closed behavior on partial outputs and private experiment manifest.
- [x] Produced an integrated Vietnamese six-chapter Word/PDF **working manuscript** with empirical split tables, Xente 50-seed candidate summaries, **IEEE five-seed clearly marked PILOT**, sensitivity/limitation discussion, citations and appendices. Files were generated in the conversation's working container, not committed to public GitHub as binary artifacts.
- [x] Generated aggregate IEEE/data and provisional policy-contrast figures, packaged **without raw transaction IDs**; charts use observed split data or recorded run-summary means, NOT reconstructed seed-level intervals.

**Hard gate still OPEN:** Private IEEE frozen bundle and prior five-seed pilot ZIPs were listed in Library but could not be exported through the authorized materialization path in this session. Therefore the canonical 12×5 replay **was not rerun**, the final 12×N batch **was not executed**, and final IEEE confidence intervals/cross-scenario inference cannot be responsibly reported as complete. The new automated runner enables these steps when inputs are available on an authorized local machine:

```bash
python -m scripts.complete_ieee_experiments \\
  --zip /private/ieee-fraud-detection.zip \\
  --output-dir outputs/local/ieee_final \\
  --target-seeds 30 --batch-seeds 5 --execute
```

The wrapper rebuilds missing frozen model outputs from the original competition zip and runs the real-data full scorer audit **before** simulation; it can be resumed without silently overwriting prior batch results. Running it can take substantial time/memory; use authorized private storage, keep raw data out of public GitHub.

**Not a completed thesis until:** canonical IEEE output + convergence + multi-seed reward/feedback/outcome sensitivity + seed-level cross-scenario contrasts and intervals + figure/table consistency + references + GVHD approval. Preserve draft PR until reviewed.
