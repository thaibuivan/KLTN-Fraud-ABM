# Kế hoạch thí nghiệm Adaptive Policy v0.1

## Experiment 1 — Static vs Adaptive Fraudster

Giữ cố định:
- policy;
- transaction environment;
- analyst capacity.

So sánh:
- static fraudster;
- adaptive fraudster.

Outcome chính:
- successful fraud value;
- fraud detection rate;
- time to detection;
- alert volume;
- queue/backlog;
- policy cost nếu đủ grounding.

Lưu ý:
“adaptive gây loss cao hơn” là hypothesis, không phải kết quả bắt buộc.

## Experiment 2 — Policy Comparison

Fraudster:
- adaptive.

So sánh:
1. fixed threshold;
2. cost-sensitive;
3. capacity-aware.

Đánh giá trade-off:
- fraud loss;
- false positives;
- customer friction proxy;
- review volume;
- backlog;
- waiting time;
- total cost nếu cost coefficients được khai báo rõ.

## Experiment 3 — Analyst Capacity Stress Test

Thay đổi analyst capacity:
- low;
- medium;
- high;
hoặc một range có grounding/sensitivity rationale.

Đo:
- queue length;
- waiting time;
- utilization;
- fraud loss;
- policy ranking.

Câu hỏi:
> Policy ranking có đổi khi review capacity khan hiếm không?

## Replication

Mỗi configuration chạy nhiều random seeds.

Report:
- mean;
- standard deviation;
- confidence interval khi phù hợp.

## Robustness

1. stochastic replication;
2. parameter sensitivity;
3. structural sensitivity của adaptation mechanism;
4. cross-scenario replication trên IEEE-CIS và Xente.

## Thứ tự implementation

1. verified static baseline;
2. static fraudster;
3. adaptive mechanism;
4. static-vs-adaptive;
5. policy comparison;
6. capacity stress;
7. sensitivity.
