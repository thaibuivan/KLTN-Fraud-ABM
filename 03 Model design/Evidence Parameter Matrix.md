# Evidence Parameter Matrix

## Evidence labels
- **Empirical**: estimate trực tiếp từ primary dataset.
- **Literature-informed**: range/mechanism từ nghiên cứu liên quan.
- **Expert-informed**: expert input nếu có.
- **Theory-informed**: rule có theoretical support.
- **Explicit assumption**: lựa chọn mô hình hóa phải kiểm tra sensitivity.
- **Legacy assumption**: giá trị có trong đề án cũ nhưng chưa được tái-ground cho KLTN.

| Parameter / mechanism | Module | Candidate source | Evidence type | Value/range | Uncertainty | Status |
|---|---|---|---|---|---|---|
| Fraud prevalence | Fraud regime | Primary dataset | Empirical | TBD | TBD | Data audit |
| Amount distribution | Transaction | Primary dataset | Empirical | TBD | TBD | Data audit |
| Temporal pattern | Transaction | Primary dataset | Empirical | TBD | TBD | Data audit |
| Customer/account history | Customer/Account | Primary dataset | Empirical | TBD | TBD | Data audit |
| Risk threshold | Policy | Experiment design | Explicit assumption | TBD range | High | Open |
| Analyst capacity | Queue/Analyst | Literature / expert | Literature/Expert | TBD | High | Need source |
| Review-time distribution | Queue/Analyst | Literature / expert | Literature/Expert | TBD | High | Need source |
| Analyst error | Analyst | Literature / assumption | Mixed | TBD | High | Optional |
| False-positive/friction cost | Cost engine | Literature / scenario | Mixed | TBD | High | Define proxy |
| Fraud loss | Cost engine | Amount + scenario | Empirical/Scenario | TBD | Medium | Data audit |
| Queue discipline | Queue | Literature/design | Assumption/Literature | TBD | High | Open |
| Review-delay effect | Outcome | Literature/design | Mixed | TBD | High | Open |
| Fraud regime shift | Scenario | Data/literature/scenario | Mixed | TBD | High | Open |

## Legacy values that must NOT be copied automatically
Repo cũ used values such as:
- daily analyst capacities;
- analyst review-time assumptions;
- fraud recovery rate;
- false-positive costs;
- fraud strategy probabilities.

These are useful for pilot replication but remain **legacy assumptions** until re-grounded.

## Rule
Không điền một con số chỉ vì "đã chạy được" trong code cũ. Mỗi value phải có provenance hoặc được ghi explicit assumption và sensitivity-tested.
