# Final Core Experiment Grid v1.0

## Mục tiêu

Giữ experiment grid đủ nhỏ để trả lời RQ rõ ràng và tránh factorial explosion.

## Core factors

### Factor A — Fraudster mode
2 mức:
- Static
- Adaptive

### Factor B — Policy
2 mức:
- Fixed-threshold
- Capacity-aware

### Factor C — Analyst capacity
3 mức:
- Low
- Medium
- High

Tổng:

```text
2 × 2 × 3 = 12 configurations
```

## 12 configurations

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

## Comparisons chính

### RQ1 — Effect of adaptation
Giữ policy và capacity cố định:

```text
Static vs Adaptive
```

### RQ2 — Effect of policy
Giữ fraudster mode và capacity cố định:

```text
Fixed vs Capacity-aware
```

### RQ3 — Effect of scarce review resources
Giữ fraudster mode và policy cố định:

```text
Low → Medium → High capacity
```

### Interaction quan trọng
Kiểm tra:

> lợi ích của capacity-aware policy có lớn hơn khi fraudster adaptive và capacity thấp hay không?

Đây là interaction trung tâm của thesis.

## Seeds

Pilot:
- 20–30 seeds.

Final:
- chọn N dựa trên convergence / Monte Carlo error của các metrics chính;
- không chọn N chỉ vì một con số tròn.

## Core outcomes

Fraud:
- successful fraud value;
- prevented fraud value;
- fraud capture.

Operations:
- alert/review count;
- backlog;
- mean/P95 wait;
- analyst load/utilization proxy.

Customer:
- legitimate review;
- legitimate block;
- intervention rate.

## Robustness không nhân vào full grid

Chạy riêng:
1. FIFO vs risk-priority.
2. Full vs degraded score model.
3. Service-time stochasticity.
4. Variable team capacity.
5. Learning-rate sensitivity.
6. Exploration sensitivity.
7. Optional cost-sensitive policy.

## Cost-sensitive extension

Nếu cost grounding đủ tốt:

```text
Fixed
vs
Capacity-aware
vs
Cost-sensitive
```

khi đó grid mở rộng thành:

```text
2 × 3 × 3 = 18 configurations
```

Nhưng 18-config grid không phải điều kiện để core thesis hoàn thành.

## Dataset scope

Core final experiment:
- Xente.

Optional replication:
- IEEE-CIS sau khi Xente full model và final results đã ổn định.
