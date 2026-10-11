# THỨ TỰ ĐỌC REPO — giai đoạn hoàn thiện KLTN

Không đọc repo theo folder. Đọc theo research pipeline.

## 1. Hiểu KLTN phát triển từ đề án như thế nào

1. [[De an to KLTN - Development Map]]
2. [[Current Direction - 2026-10-11]]
3. [[Research Design v1.1 - Develop from FinRisk Proposal]]

Sau ba file này phải trả lời được:
- KLTN giữ gì từ đề án?
- nâng cấp gì?
- RQ chính là gì?
- Xente dùng ở đâu?
- adaptive fraudster dùng để làm gì?

## 2. Hiểu full model

4. [[Xente Full Model Specification v1.0]]
5. [[Parameter Registry v0.2]]
6. [[Adaptive Fraudster Design v0.1]]
7. [[Queue and Analyst Service Design v0.1]]
8. [[Validation Plan v1.0]]

## 3. Hiểu thí nghiệm cuối

9. [[Final Core Experiment Grid v1.0]]

Core:

```text
Static / Adaptive
×
Fixed / Capacity-aware
×
Low / Medium / High capacity
= 12 configurations
```

## 4. Sau đó mới đọc evidence Xente đã hoàn thành

1. [[Xente Empirical Profile]]
2. [[Xente Baseline Risk Model Feasibility]]
3. [[Xente Queue Pilot v0.1]]
4. [[Xente Robustness Pack v0.1]]
5. [[Xente Alert-rate and Starvation Sensitivity v0.1]]
6. [[Xente Variable Team Capacity Sensitivity v0.1]]

Các file này là empirical/operational groundwork, chưa phải final adaptive-ABM result.

## 5. Code pipeline

```text
profile_xente.py
    ↓
build_xente_features.py
    ↓
train_xente_baseline.py
    ↓
fraud_policies.py
    ↓
simulate_alert_queue.py
    ↓
adaptive_fraudster.py
    ↓
[INTEGRATION ENGINE — next]
```

## File cũ không dùng làm source of truth

- [[Research Design v0.2]]
- [[Research Design v1.0 - Policy Experimentation]]
- [[Candidate Core Specification v0.3]]
- [[Core Experiment Grid v0.1]]
- [[Conceptual Model v0.2]]
- [[Validation Plan v0.1]]
- [[Methodology Skeleton v0.1]]
- [[Results and Discussion Outline v0.1]]

Giữ để truy lịch sử hoặc tái sử dụng nội dung; không dùng để quyết định scope hiện tại.
