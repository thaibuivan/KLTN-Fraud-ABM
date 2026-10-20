# IEEE-CIS raw-data validation: amount regimes and chronological drift — 2026-10-18

> **Status:** Independently checked from the original publicly distributed `ieee-fraud-detection.zip` **labeled training** archive in this working session. The table uses the original input CSV rows and an immutable 70/15/15 chronological split. It is descriptive EDA, **not** a completed canonical IEEE simulation, fraudster behavioral validation or formal proof of a policy effect. No organization-internal data used.

## 1. Procedure

- Read `train_transaction.csv` from the original competition zip, preserving source chronological order (`TransactionDT` nondecreasing).
- For efficient independent validation, extract only `TransactionID,isFraud,TransactionDT,TransactionAmt,ProductCD,card1,addr1`; identity presence is checked by membership in the original `train_identity.csv` `TransactionID` keys, rather than interpreting a missing `DeviceType` value as “identity absent”.
- Split index bounds: 413,378 (70%) and 501,959 (85%), computed without sampling or future-value features.
- Fraud-donor amount regimes are defined **only on the validation fraud subset** at its observed tercile cutoffs; test fraud is used only for **post-hoc descriptive drift auditing** and never to set the thresholds/pools.
- Descriptive statistics were computed locally; no individual transactions, customer proxies or device strings were committed to this repository.

## 2. Independently verified numerical profile

| Quantity | Train | Validation | Held-out labeled Test |
|---|---:|---:|---:|
| Number of transactions | 413,378 | 88,581 | 88,581 |
| Fraud transactions | 14,538 | 3,042 | 3,083 |
| Fraud prevalence (%) | 3.5169 | 3.4341 | 3.4804 |
| Identity-row availability (%) | 26.5885 | 17.6720 | 21.0745 |
| Median TransactionAmt | 68.95 | 67.95 | 68.50 |
| Median fraud TransactionAmt | 75.00 | 77.00 | 63.95 |
| Distinct card1+addr1 proxies within split | 34,755 | 14,254 | 14,091 |

The **identity coverage** decline from 26.6% in train to 17.7% in validation is material for interpreting available identity features. This may contribute to score/policy distribution shift but alone does not identify its causal contribution; additional model ablation would be needed.

Among validation fraud transactions:
- Amount tercile boundaries: **50.0** and **117.0**; median = **77.0**.
- Regime donor sizes: **low 1,052**, **middle 1,030**, **high 960**.
- ProductCD overall: W 48.817%, C 37.804%, R 5.260%, H 4.602%, S 3.517%.

## 3. Critical diagnostic: amount regime is NOT a pure amount intervention

| ProductCD share within validation fraud regime | Low amount | Middle amount | High amount |
|---|---:|---:|---:|
| C | 62.2% | 38.3% | 10.5% |
| W | 24.6% | 52.9% | 70.9% |
| H | 4.1% | 4.4% | 5.4% |
| R | 1.2% | 2.2% | 12.9% |
| S | 7.9% | 2.1% | 0.2% |

**Interpretation:** `IEEEFeatureLevelFraudGenerator` samples an entire empirical donor row conditional on amount tercile. It therefore changes a *joint distribution of amount + ProductCD + card/device/identity context* when the fraudster switches strategies. It is scientifically **incorrect** to infer from such a change that the model has isolated a causal “change in amount alone”.

In particular, the exploratory result that IEEE Adaptive favors high-amount regimes may reflect joint context, the frozen detector, and amount-normalized reward together. The opposing low-amount preference in Xente must be framed as a **model/environment-specific emergent pattern**, not demonstrated real fraudster cognition or directly comparable causal amount effect.

**Research recommendation:** retain the validated joint-context generator as core because it preserves realistic donor support; add an optional, *separate* sensitivity that conditions or stratifies by ProductCD where sufficient support exists. Do not rebuild frozen IEEE main scenario to silently force equal ProductCD between regimes.

## 4. Temporal amount shift (post-hoc descriptive only)

The median fraud TransactionAmt declines from validation **77.0** to held-out test **63.95**, despite modest change in overall fraud prevalence. A two-sample descriptive KS distance between the observed validation- and test-fraud amount distributions was approximately **0.07619**. The formal i.i.d. KS p-value must **not** be interpreted as a definitive temporal hypothesis test: records may share entities and both time window and fraud selection processes vary.

This pattern is another reason to preserve chronological hold-out and separately investigate score/policy robustness.

## 5. Code and provenance

New repository command:

```bash
python -m scripts.audit_ieee_donor_regimes \
  --validation-donors outputs/local/ieee_closed_loop/validation_fraud_donors.csv \
  --test-context outputs/local/ieee_closed_loop/test_context.csv \
  --output-dir outputs/local/ieee_closed_loop/regime_audit
```

It saves only aggregated `regime_registry.csv`, `regime_product_mix.csv`, and `regime_audit_metadata.json`; the original local data remains private. Unit tests ensure held-out test data does not change validation cuts or reward scale.

**Acceptance caveat:** This independent audit corroborates the report's split/tercile counts but does **not** replace canonical IEEE risk-bundle or full 12×N simulation reproducibility. The latter remains outstanding as of this note.

## 6. Manuscript use

Add the split/identity table to Data chapter; the ProductCD-by-regime matrix to data-to-ABM/generator validation appendix; explain the observed-context-bundle interpretation in Methodology. Mention the conditional-covariate dependence when discussing IEEE/Xente strategy contrasts and the limits of counterfactual identification.

Source: IEEE-CIS Fraud Detection Kaggle labeled training files, original public archive in user-authorized research workspace. Aggregates were directly recomputed on 2026-10-18.


## 7. Independent numerical re-audit — 20/10/2026

The original `ieee-fraud-detection.zip` was read directly with a memory-bounded pandas chunked pipeline and the train/validation/holdout index boundaries held fixed at 413,378 and 501,959; this newly executed check reproduced the split/count/coverage numbers reported above.

Additional regime-specific diagnostics (validation fraud ONLY):

| Regime | Donors | Median TransactionAmt | Identity-row availability | Distinct card1+addr1 proxies |
|---|---:|---:|---:|---:|
| Low | 1,052 | 29.818 | 73.574% | 276 |
| Middle | 1,030 | 78.571 | 45.534% | 356 |
| High | 960 | 250.000 | 28.646% | 451 |

The stark differences in identity coverage provide **strong evidence of context-mixture confounding** in the amount-conditioned donor resampling mechanism. A high-amount regime is not just a larger TransactionAmt; it also has a lower share of matched identity records, different ProductCD composition, and a broader collection of card/address proxies.

A descriptive ProductCD × amount-regime contingency calculation over the 3,042 validation fraud donors gave chi-square ≈ **832.32** and Cramér's V ≈ **0.370**. The low-minus-high ProductCD=C proportion gap is approximately **51.65 percentage points**; an IID-within-regime nonparametric bootstrap over 1,200 draws gave an *illustrative*, **not cluster-robust**, percentile interval [48.03, 54.87] pp. These formal IID results must NOT be interpreted as a valid population-level significance test: fraud records can share entity proxies and chronology.

A separate descriptive validation→holdout test comparison found the median fraud amount changing from **77.00** to **63.95** (difference = −13.05 in IEEE amount units); the IID row-bootstrap illustrative interval for the median difference was [−18.80, −6.30]. KS distance ≈ **0.07619**, likewise a descriptive divergence statistic rather than rigorous i.i.d. significance evidence. Holdout fraud labels were used **only after model/strategy definition**, to assess change; they did not affect donor pools.

**New thesis implication:** In Results and Discussion, rename these regimes *amount-conditioned empirical context bundles*. A strategy share shift cannot causally be attributed to amount alone, and reward ablation alone is insufficient to establish behavioral validity if ProductCD, identity and proxy composition co-vary. Optionally run matched-ProductCD donor sensitivity **with declared support restrictions**, without changing main frozen 24-cell protocol post hoc.

**Execution provenance:** Independently calculated 20 Oct 2026 on the authorized Kaggle raw ZIP using a chunked, read-only local audit. The numerical output and an executable analysis script are retained in the working conversation artifacts. This addendum does **not** claim that the canonical IEEE adaptive experiment was run.
