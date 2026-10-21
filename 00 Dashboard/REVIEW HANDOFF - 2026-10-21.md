# KLTN — REVIEW HANDOFF / EVIDENCE LOCK (2026-10-21)

> This is the latest research readiness handoff for the author. **NOT** a statement that the main IEEE repeated-seed experiment is complete, nor a submission approval. Keep Draft PR unmerged pending author's final review.

## Scope — unchanged

Agent-Based Stress Testing of Transaction Fraud-Management Policies under Adaptive Fraudster Behavior and Analyst Capacity Constraints. Two scenarios (Xente/IEEE-CIS), two fraudster modes (Static/Adaptive), two policies (Fixed/Capacity-aware), three capacity ratios (0.75/1/1.25), 24 core configurations. No private organization data included.

## Evidence verified/reported

- Xente: 12 cells × 50 seeds documented in `05 Experiments/Xente Feature-Level Core Run v0.2.md`; degraded-score 12 × 30 plus targeted sensitivity, with strong conditionality of the policy interception effects.
- IEEE: original Kaggle train labeled 590,540; chronology 413,378/88,581/88,581, fraud 14,538/3,042/3,083; categorical/identity availability drift and joint amount/ProductCD donor composition independently checked.
- IEEE canonical frozen streaming-SGD **re-run on October 20** (commit `662e94fada`): validation PR-AUC 0.36438685, test 0.38403028; full 88,581 test-event fast-score equivalence max absolute error 4.3138051e-7 < tolerance 1e-6. Mean risk score 0.0653414 validation versus 0.0946393 test; ECE 10-bin 0.031072 versus 0.059835; validation top 1% score threshold triggers 1.5489% of heldout events. This is model score/alert drift, NOT main adaptive-policy reproducibility.
- IEEE full-test 12×5 *locally mirrored* preliminary pilot is in `05 Experiments/IEEE-CIS Adaptive Full-Test Pilot v0.2.md` — **not the canonical final inference**. Reward ablation seed 0 is exploratory.
- GitHub Actions CI on latest SHA `139909039d` succeeded (software tests only).

## Reproducibility hard gate (OPEN)

1. Canonical 12×5 replay on frozen October-20 bundle, compare all 60 cells with archived mirror pilot.
2. Non-overlapping 12×N batches with adequate MCSE/CI stability, especially value exposure.
3. Multi-seed reward and REVIEW-observation ablations and q-assumption outcomes.
4. Paired policy/adaptation contrasts; normalized two-scenario comparison with uncertainty intervals.
5. QA results, tables, bibliography, university formatting and GVHD approval.

Code exists: `scripts/complete_ieee_experiments.py`, `scripts/summarize_ieee_closed_loop.py`, `scripts/audit_ieee_donor_regimes.py`. Original IEEE competition ZIP is available in the conversation runtime; however the *actual executable repo source snapshot* and *previous private frozen-model/pilot artifact ZIPs* could not be transferred as authorized bytes into this runtime. Therefore **no new canonical closed-loop seed batch was executed here**. Do not fabricate missing numeric outputs or seed uncertainty.

## Written outputs prepared for author

- Integrated 6-chapter Vietnamese manuscript available as conversation DOCX/PDF, updated with October-20 independent canonical baseline and scoring evidence in **Appendix E** (2026-10-21 review build).
- Prior integrated manuscript with charts and source notes remains available; this later build is the preferred review copy.
- Narrative remains explicit: Xente candidate 50-seed, IEEE 5-seed pilot only, no verified bank loss prevention, no bank-specific staffing optimizer or empirically identified fraudster cognition.

**Final reviewer decision to be taken only after hard gate:** approve manuscript, approve conditional pilot-only scope (if university permits) or run canonical full IEEE + seed sensitivity and replace provisional findings.
