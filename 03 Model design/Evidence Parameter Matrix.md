# Evidence Parameter Matrix

## Evidence labels
- **Empirical**: estimate trực tiếp từ primary dataset.
- **Literature-informed**: range/mechanism từ nghiên cứu liên quan.
- **Expert-informed**: expert input nếu có.
- **Theory-informed**: rule có theoretical support.
- **Explicit assumption**: lựa chọn mô hình hóa phải kiểm tra sensitivity.
- **Legacy assumption**: giá trị có trong đề án cũ nhưng chưa được tái-ground cho KLTN.

## Primary empirical source
**Xente Fraud Detection** — xem [[Data Audit]].

| Parameter / mechanism | Module | Source | Evidence type | Value/range | Uncertainty | Status |
|---|---|---|---|---|---|---|
| Fraud prevalence | Fraud regime | Xente labelled train | Empirical | Local profiling required; published analysis ~0.20% | Sampling/time variation | Ready to estimate |
| Amount distribution | Transaction | Xente `Amount`, `Value` | Empirical | Local quantiles/distribution | Low/medium | Ready to estimate |
| Transaction timing | Transaction | Xente `TransactionStartTime` | Empirical | Hour/day/inter-arrival distributions | Medium | Ready to estimate |
| Customer identity | Customer state | Xente `CustomerId` | Empirical | Direct identifier | Low | **Chosen** |
| Account grouping | Customer state | Xente `AccountId` | Empirical | Direct grouping | Low | Use as nested state |
| Subscription grouping | Customer state | Xente `SubscriptionId` | Empirical | Direct grouping | Low | Use as nested state |
| Transaction frequency / velocity | Customer state | chronological Xente history | Empirical-derived | Rolling windows TBD | Medium | Ready to derive |
| Product/category mix | Transaction | `ProductCategory`, `ProductId` | Empirical | Local frequencies | Medium | Ready to estimate |
| Channel mix | Transaction | `ChannelId` | Empirical | Local frequencies | Medium | Ready to estimate |
| Baseline risk-engine coefficients | Risk engine | Xente early-period train | Empirical model | Fit locally | Model uncertainty | Planned |
| Risk threshold | Policy | Experiment design | Explicit assumption / operating point | Range from validation | High | Planned |
| Alert arrival | Queue | policy applied to observed Xente stream | Empirical + policy | Derived | Policy-dependent | Planned |
| Queue discipline | Queue | Design/literature | Assumption/Literature | FIFO vs risk-priority | High | Structural sensitivity |
| Analyst capacity | Queue/Analyst | Literature / expert | Literature/Expert | TBD range | High | **Need source** |
| Review-time distribution | Queue/Analyst | Literature / expert | Literature/Expert | TBD range | High | **Need source** |
| Analyst error | Analyst | Literature / assumption | Mixed | TBD | High | Optional |
| False-positive/friction cost | Cost engine | Literature / scenario | Mixed | TBD range | High | **Need source/proxy** |
| Fraud loss proxy | Cost engine | Xente amount + assumption | Empirical/Scenario | Amount-based baseline | Medium/high | Define carefully |
| Fraud recovery rate | Outcome | Literature / scenario | Mixed | TBD | High | **Need source** |
| Review-delay effect | Outcome | Literature/design | Mixed | TBD | High | **Need source** |
| Fraud-regime shift | Stress scenario | Empirical baseline + bounded perturbation | Mixed | TBD | High | Planned |

## Legacy values that must NOT be copied automatically
Repo cũ used values such as:
- daily analyst capacities;
- analyst review-time assumptions;
- fraud recovery rate;
- false-positive costs;
- fraud strategy probabilities.

These remain **legacy assumptions** until re-grounded.

## Rule
Không điền một con số chỉ vì "đã chạy được" trong code cũ. Mỗi value phải có provenance hoặc được ghi explicit assumption và sensitivity-tested.

## Next evidence search
Ưu tiên literature cho:
1. analyst review time;
2. analyst capacity / alert workload;
3. effect of backlog/delay;
4. false-positive/customer-friction proxy;
5. fraud recovery/prevention assumption.
