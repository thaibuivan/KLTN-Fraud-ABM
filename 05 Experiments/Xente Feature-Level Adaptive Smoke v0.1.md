# Xente Feature-Level Adaptive Smoke v0.1

## Status

**Feature-level closed-loop smoke test — executed, not a final thesis result.**

This milestone upgrades the historical Xente adaptive pilot in one important way:

```text
OLD:
strategy → historical Value/risk-score template → policy

NEW:
strategy
→ raw validation-fraud context template
→ online past-only synthetic-fraudster history
→ saved Xente risk model rescoring
→ policy
→ queue / analyst
→ response
→ strategy update
```

The risk score of a generated fraud transaction is therefore no longer copied from a historical fraud row.

## Empirical source boundary

Fraud strategy regimes are still deliberately conservative:
- low_value;
- medium_value;
- high_value.

They are built only from **chronological validation fraud observations**, not from test fraud outcomes.

The regimes are stress actions, not claims that Xente directly identifies real fraudster intent.

Observed legitimate test transactions remain empirical replay.

Observed test fraud timestamps are used only as fraud-attempt opportunity slots.

## Feature-level generator

Raw fields resampled from validation fraud rows:
- Amount;
- Value;
- ProductCategory;
- ChannelId;
- ProviderId;
- ProductId;
- PricingStrategy.

Generated fraud then receives past-only synthetic-fraudster history features through `XenteOnlineFeatureBuilder`.

The saved Xente logistic baseline then recomputes:
- `risk_probability`.

## Verification

The online feature builder was checked against the existing batch `build_xente_features.py` logic on empirical Xente rows.

Result:
> the checked past-only feature columns matched, so generated fraud events use the same state definition as the original Xente risk pipeline.

A dedicated unit test was also added:
- `tests/test_xente_online_features.py`.

## Core normalized policy settings used in the smoke

Validation-calibrated thresholds:

| Role | Validation rate | Xente threshold |
|---|---:|---:|
| BLOCK pilot | top 0.10% | 0.614774 |
| Review base | top 1.00% | 0.014801 |
| Review soft congestion | top 0.75% | 0.026892 |
| Review hard congestion | top 0.50% | 0.050961 |

Operational settings:
- FIFO core queue;
- Low / Medium / High capacity = 0.75 / 1.00 / 1.25 of the validation base-review arrival rate;
- congestion state = backlog-hours;
- soft / hard congestion triggers = 24 / 72 hours.

BLOCK top-0.10% is still a sensitivity parameter and is **not frozen as the final value yet**.

## Reward normalization

The adaptive fraudster now supports:

```text
normalized_amount = transaction_value / reward_scale
```

For the feature-level Xente pilot:
- `reward_scale` = validation-fraud median Value = **400,000**.

This avoids letting Xente's raw currency scale define the learning dynamics and gives a path to comparable adaptation logic in IEEE-CIS.

Dormancy is disabled in the core smoke because dormancy changes the number of fraud attempts. It remains a robustness mechanism.

## One-seed 12-configuration smoke

This run is only an execution check, not inferential evidence.

### Static fraudster

| Policy | Capacity | Fraud intercept | Fraud exposure at horizon | Backlog |
|---|---:|---:|---:|---:|
| Fixed | 0.75 | 80% | 2,431,505 | 41 |
| Fixed | 1.00 | 82% | 1,631,505 | 29 |
| Fixed | 1.25 | 84% | 831,505 | 23 |
| Capacity-aware | 0.75 | 80% | 2,431,505 | 27 |
| Capacity-aware | 1.00 | 82% | 1,631,505 | 21 |
| Capacity-aware | 1.25 | 88% | 681,505 | 18 |

### Adaptive fraudster

| Policy | Capacity | Fraud intercept | Fraud exposure at horizon | Backlog |
|---|---:|---:|---:|---:|
| Fixed | 0.75 | 68% | 1,014,520 | 58 |
| Fixed | 1.00 | 72% | 864,520 | 32 |
| Fixed | 1.25 | 74% | 764,520 | 25 |
| Capacity-aware | 0.75 | 64% | 1,064,520 | 29 |
| Capacity-aware | 1.00 | 64% | 1,064,520 | 24 |
| Capacity-aware | 1.25 | 72% | 714,520 | 20 |

Adaptive strategy composition in this single seed:
- low_value: 46 / 50;
- medium_value: 3 / 50;
- high_value: 1 / 50.

## Important methodological insight

The smoke reveals why final reporting cannot use fraud-capture rate alone.

Here, adaptive behavior shifts heavily toward lower-value fraud:
- capture/interception rate can fall;
- but total value exposure can also be lower than under a static higher-value mixture.

Therefore the final thesis must report both:

1. **count-based outcomes**
   - fraud intercept rate;
   - number of successful/unresolved frauds;

2. **value-based outcomes**
   - successful fraud value;
   - unresolved fraud value;
   - fraud exposure at horizon.

This is a substantive design improvement over the earlier score-template pilot.

## What this smoke does NOT prove

It does not prove:
- adaptive fraudsters really choose low-value strategies at this rate;
- top 0.10% is the correct BLOCK rule;
- Capacity-aware is better/worse overall;
- the one-seed rankings are stable;
- Xente results transfer to IEEE-CIS.

## Next milestone

Before final 12-config Xente results:

1. run a small BLOCK-rate sensitivity;
2. run alpha / epsilon sensitivity;
3. run congestion-trigger sensitivity;
4. verify full latest tests;
5. choose/freeze the final Xente parameter set;
6. run enough seeds for convergence;
7. repeat a defined degraded-score robustness check.
