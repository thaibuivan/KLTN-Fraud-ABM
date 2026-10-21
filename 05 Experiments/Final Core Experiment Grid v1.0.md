# Final Core Experiment Grid v1.0

## Core design toàn khóa luận

Bốn factors:

### A — Dataset
- Xente
- IEEE-CIS

### B — Fraudster mode
- Static
- Adaptive

### C — Policy
- Fixed-threshold
- Capacity-aware

### D — Analyst capacity
- Low
- Medium
- High

Tổng:

```text
2 × 2 × 2 × 3 = 24 configurations
```

## 12 configurations lặp lại trên mỗi dataset

| # | Fraudster | Policy | Capacity |
|---:|---|---|---|
| 1 | Static | Fixed | Low |
| 2 | Static | Fixed | Medium |
| 3 | Static | Fixed | High |
| 4 | Static | Capacity-aware | Low |
| 5 | Static | Capacity-aware | Medium |
| 6 | Static | Capacity-aware | High |
| 7 | Adaptive | Fixed | Low |
| 8 | Adaptive | Fixed | Medium |
| 9 | Adaptive | Fixed | High |
| 10 | Adaptive | Capacity-aware | Low |
| 11 | Adaptive | Capacity-aware | Medium |
| 12 | Adaptive | Capacity-aware | High |

Chạy bảng này một lần cho Xente và một lần cho IEEE-CIS.

## Comparisons chính

### RQ1 — Adaptation
Static vs Adaptive trong cùng:
- dataset;
- policy;
- capacity.

### RQ2 — Policy
Fixed vs Capacity-aware trong cùng:
- dataset;
- fraudster mode;
- capacity.

### RQ3 — Capacity
Low → Medium → High trong cùng:
- dataset;
- fraudster mode;
- policy.

### RQ4 — Cross-scenario robustness
So effect/ranking giữa Xente và IEEE-CIS.

## Interaction trung tâm

```text
Dataset
× Adaptation
× Policy
× Capacity
```

Không nhất thiết fit một statistical interaction model phức tạp; có thể phân tích effect contrasts + uncertainty intervals.

## Seeds

Pilot:
- 20–30 seeds.

Final:
- chọn N theo convergence / Monte Carlo error.

## Core outcomes

Fraud:
- successful fraud exposure/value;
- prevented/intercepted fraud;
- fraud capture/intercept rate.

Operations:
- alert/review count;
- backlog;
- mean/P95 wait;
- utilization/load proxy.

Customer/intervention:
- legitimate review;
- legitimate block;
- intervention rate.

## Robustness không nhân vào 24 core configs

Chạy riêng:
1. FIFO vs risk-priority.
2. Full vs degraded score model.
3. Service-time stochasticity.
4. Variable team capacity.
5. Learning-rate sensitivity.
6. Exploration sensitivity.
7. Optional cost-sensitive policy.

## Cost-sensitive extension

Nếu đủ grounding:

```text
2 datasets × 2 fraudster × 3 policies × 3 capacity
= 36 configurations
```

Nhưng 36-config grid không phải core requirement.
