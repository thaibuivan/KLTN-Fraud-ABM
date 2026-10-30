# Legacy Migration Map

| Legacy component | KLTN decision | Status |
|---|---|---|
| Transaction-risk decisioning framing | Giữ và viết lại theo thesis scope | Keep |
| Policy comparison | Giữ candidate policies, re-test | Conditional keep |
| Analyst capacity / overflow | Nâng thành persistent queue/backlog | Upgrade |
| Cost engine | Giữ cấu trúc, thay assumptions bằng parameter registry + sensitivity | Upgrade |
| Synthetic customer generator | Chỉ dùng như scenario/pilot support | Support only |
| Fraud strategy probabilities | Chuyển thành bounded regimes/ranges | Rewrite |
| XGBoost experiments | Có thể làm risk-engine baseline/reference | Conditional reuse |
| Recall-first analysis | Giữ như operating-point insight | Keep |
| Analyst accuracy/review time | Tìm literature/ranges + sensitivity | Re-ground |
| AI explanation / LLM | Không đưa vào core | Defer |
| Static dashboard | Tái sử dụng sau core experiments | Defer |
| Game Theory / Mechanism Design | Chỉ giữ nếu operationalized trong policy/payoff | Narrow |

## Code migration rule
Không copy toàn bộ `scripts/`. Chỉ migrate module khi:
1. nó trả lời một RQ cụ thể;
2. input/output được định nghĩa lại;
3. parameter có provenance;
4. có test hoặc sanity check.

## Candidate modules to reuse later
- policy comparison logic;
- cost/outcome calculation;
- capacity-aware ranking;
- recall-first operating-point analysis;
- reporting/plot utilities.

## Rewrite first
- agent/state model;
- timestep/scheduler;
- persistent queue;
- empirical-data adapter;
- uncertainty experiment runner;
- validation checks.
