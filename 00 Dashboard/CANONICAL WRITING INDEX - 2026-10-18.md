# CANONICAL WRITING INDEX — KLTN Fraud ABM — 18/10/2026

> **Purpose:** Multiple draft-writing tracks contributed notes to `chatgpt-draft` on 18 Oct. This index removes ambiguity without deleting alternative drafts. **None of these drafts is a final approved thesis.** The independent IEEE repeated-seed experiment remains unfinished.

## 1. Preferred manuscript source by chapter

| Intended chapter | Preferred current source | Required work before thesis lock |
|---|---|---|
| 1. Introduction | `06 Writing/Introduction and Conclusion Full Draft v1.0.md` (Introduction section) | Integrate research problem, clear prior-art distinction, approved thesis title and university format |
| 2. Literature Review | `06 Writing/Literature Review Full Draft v1.0.md` | Full-text verification of closest work; consistent APA bibliography; avoid overstating uniqueness |
| 3. Data & Experimental Setting | `06 Writing/Chapter 3 Data and Experimental Setting Draft v1.0.md` | Final data statistics/plots, license statement, baseline provenance, exact anti-leakage checks |
| 4. Methodology / ODD | `06 Writing/Methodology Full Draft v1.1.md` + `03 Model design/ODD Hybrid ABM-DES Specification v1.0.md` | Reconcile exact canonical runner and outcome semantics, finalize parameter registry/ODD |
| 5. Results & Discussion | `06 Writing/Results and Discussion Full Draft v1.2.md` | **IEEE 5-seed content currently PILOT**; canonical main repeated-seed replacement, CI/MCSE, figures |
| 6. Conclusions, limitations | `06 Writing/Introduction and Conclusion Full Draft v1.0.md` (Conclusion section) | Recheck every claim against final verified results; advisor sign-off |

## 2. Alternate sources (retain as working notes, NOT independent final chapters)

- `06 Writing/Chapter 1 Introduction Draft v1.0.md`: expanded motivation and scope, reviewed sources; cross-check phrasing when consolidating preferred Introduction.
- `06 Writing/Chapter 2 Literature Review Draft v1.0.md`: supplementary narrative synthesis and detailed sources; only merge material after citation verification.
- `06 Writing/Chapter 5 Results and Discussion Working Draft v1.0.md`: table-rich alternate notes with explicit IEEE pilot warning; do not combine pilot means and final run means inadvertently.
- `06 Writing/Methodology Skeleton v0.1.md`, `06 Writing/Methodology Skeleton v1.0.md` and historical outlines: legacy structure/reference only.

**Do not mechanically concatenate** all drafts into one thesis: they contain overlapping prose and possibly different section numbering. For example, the older Results full draft currently uses internal section numbers 4.x; rename systematically when setting the final chapter scheme. Remove repeated text, normalize citations and check every table/equation reference.

## 3. Latest research/coding status: evidence types

- **Verified GitHub CI:** last checks observed at commit `32db7979` were PASS; code tests are NOT behavioral validity or bank-loss calibration.
- **Xente empirical candidate:** closed-loop 12 cells × 50 seeds, plus degraded-score 12 × 30 and targeted sensitivity; from recorded run reports.
- **IEEE empirical baseline:** original streaming SGD and 88,581 unchanged-test score audit documented as reproduced using local raw data.
- **IEEE preliminary full-test:** 12 cells × 5 seeds from locally mirrored execution; **canonical repo runner comparison still mandatory**.
- **Missing final:** canonical IEEE 12×5 equivalence → independent seed batches to converged N → paired cross-scenario outputs → robustness/validation appendix → final manuscript review.
- **Ethics/security:** do not quote or upload Green SM internal information absent organizational permission.

## 4. Reference execution documents

- `00 Dashboard/THESIS LOCK GATES - 2026-10-18.md`: latest implementation/academic checklist.
- `05 Experiments/IEEE-CIS Adaptive Closed-Loop Runbook v1.0.md`: executable reproducibility commands.
- `05 Experiments/Final IEEE Reproducibility and Thesis Acceptance Gates v1.0.md`: acceptance requirements and command sequence.
- `05 Experiments/IEEE-CIS Adaptive Full-Test Pilot v0.2.md`: **provisional** 5-seed report.
- `03 Model design/Operational Core Freeze v1.0.md`: baseline policy/queue/learning semantics.
- `03 Model design/Research Design v1.1 - Develop from FinRisk Proposal.md`: research questions and scope.

## 5. Publication-quality completion criteria

1. Single manuscript with consistent chapter numbering, notation, Vietnamese/English terms and figure/table styles.
2. Final N-seed IEEE runner outputs linked to source SHA and command, with per-seed uncertainty.
3. Xente/IEEE comparisons within scenario, with effect signs/intervals but no raw cross-currency amount ranking.
4. Explicit distinction between BLOCK, REVIEW started, REVIEW completed, unresolved, and hypothetical prevention under q.
5. Research contribution framed as *conditional trade-off/robustness evaluation*, not a first-ever adaptive threshold or digital twin.
6. Bibliography verified from original publishers; dataset usage/ethics documented.
7. GVHD approves final content, then user decides when to merge draft PR to main.

**Draft PR #1 remains unmerged deliberately.**
