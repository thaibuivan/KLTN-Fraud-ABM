# Xente Integrated Policy Replay v0.1

## Status

**Executed empirical pre-adaptation pilot.**

Mục tiêu:
- verify shared `FixedThresholdPolicy` và `CapacityAwarePolicy`;
- chạy trên cùng chronological Xente score stream;
- dùng cùng frozen analyst-capacity reference;
- chưa có Static/Adaptive fraudster feedback loop.

## Reproducibility check

Xente chronological logistic baseline đã được tái tạo từ raw `training.csv`.

| Split | Rows | Fraud | PR-AUC | ROC-AUC | Brier |
|---|---:|---:|---:|---:|---:|
| Validation | 14,349 | 39 | 0.560851 | 0.970573 | 0.001810 |
| Test | 14,350 | 50 | 0.892521 | 0.999664 | 0.001258 |

Các số này khớp với baseline đã ghi trước đó, nên pipeline mới không làm thay đổi empirical score baseline.

## Policy calibration

Validation target review rate:
- **1%**

Frozen review threshold:
- **0.014801**

Validation reference alert-arrival rate:
- **0.5440 alerts/hour**

Capacity được freeze theo validation reference:

```text
Low    = 0.75 × validation reference service load
Medium = 1.00 × validation reference service load
High   = 1.25 × validation reference service load
```

Queue discipline trong pilot:
- **risk-priority**

Block threshold:
- **1.0**, tức direct BLOCK gần như tắt trong pilot này.

Capacity-aware mechanism:
- soft congestion = 24 backlog-hours;
- hard congestion = 72 backlog-hours;
- review-threshold increments = +0.05 / +0.10.

Các congestion parameters này là experimental policy parameters, chưa phải empirical bank rules.

## Results

| Policy | Capacity | Review | Reviewed in horizon | Backlog end | Fraud intercepted | Fraud intercept rate | Legit review | Mean wait (h) | P95 wait (h) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Fixed | 0.75 | 188 | 117 | 71 | 49 | 98% | 138 | 30.55 | 142.26 |
| Capacity-aware | 0.75 | 133 | 116 | 17 | 48 | 96% | 83 | 19.63 | 87.68 |
| Fixed | 1.00 | 188 | 148 | 40 | 50 | 100% | 138 | 19.63 | 105.96 |
| Capacity-aware | 1.00 | 157 | 140 | 17 | 50 | 100% | 107 | 14.68 | 63.67 |
| Fixed | 1.25 | 188 | 156 | 32 | 50 | 100% | 138 | 10.59 | 44.30 |
| Capacity-aware | 1.25 | 171 | 155 | 16 | 50 | 100% | 121 | 10.05 | 40.62 |

## Interpretation

### 1. Shared policy engine chạy được trên empirical Xente score stream

Đây là milestone mới so với queue-only pilot:
- policy nhìn current queue state;
- policy có thể thay đổi alert inflow;
- REVIEW mới vào persistent queue;
- Fixed và Capacity-aware dùng cùng frozen service-capacity reference.

### 2. Capacity-aware giảm overload rõ nhất ở low/medium capacity

Low capacity:
- review: 188 → 133;
- backlog: 71 → 17;
- legitimate review: 138 → 83;
- P95 wait: 142.26h → 87.68h;
- fraud interception: 98% → 96%.

Medium:
- backlog: 40 → 17;
- P95 wait: 105.96h → 63.67h;
- fraud interception giữ 100%.

Đây là đúng loại trade-off cần nghiên cứu:
> giảm workload/friction nhưng có thể đánh đổi một phần fraud interception khi capacity rất thấp.

### 3. Không dùng pilot này để claim monetary superiority

`successful_fraud_value = 0` trong pilot vì với Xente score stream hiện tại không có observed fraud nào bị APPROVE ở các cấu hình này.

Fraud chưa được review trước horizon được ghi là unresolved review, không được tự động coi là successful fraud loss.

Do đó:
- hiện ưu tiên fraud interception, backlog, waiting và legitimate intervention;
- monetary loss comparison phải chờ full fraud-generator/adaptive environment + outcome semantics được freeze.

### 4. Xente vẫn là môi trường score rất dễ

50 test fraud được rank rất cao.
Kết quả phải tiếp tục được stress-test bằng degraded score model trong robustness, như groundwork trước đã chỉ ra.

## Decision from this pilot

### Freeze tạm thời cho bước integration tiếp theo
- validation-based threshold calibration;
- capacity frozen từ validation reference;
- Low/Medium/High = 0.75 / 1.00 / 1.25;
- risk-priority làm baseline queue discipline;
- FIFO giữ làm structural robustness;
- Fixed và Capacity-aware là hai core policy families.

### Chưa freeze
- direct BLOCK threshold;
- final fraud-loss semantics cho unresolved review;
- adaptive reward scale.

Các điểm chưa freeze phải được giải quyết khi nối full Static/Adaptive fraudster loop.

## Next milestone

Không EDA lại.

Tiếp theo:
1. thiết kế Xente-grounded fraud strategy/generator;
2. nối Static Fraudster vào empirical environment;
3. nối Adaptive Fraudster;
4. chạy end-to-end pilot trước khi chạy 12 Xente core configurations.
