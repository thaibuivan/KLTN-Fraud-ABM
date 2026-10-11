# KLTN Dashboard

## Hướng hiện tại

> **KLTN phát triển trực tiếp từ đề án FinRisk: giữ bài toán transaction-risk decisioning nhưng nâng synthetic framework thành Xente-grounded dynamic policy simulation có persistent queue và adaptive fraudster.**

## Câu hỏi nghiên cứu chính

> Các chính sách quản lý gian lận giao dịch hoạt động như thế nào khi fraudster thích nghi với phản hồi của hệ thống và analyst capacity bị giới hạn?

## Hãy nhớ chuỗi này

```text
Đề án FinRisk
      ↓
Xente empirical grounding
      ↓
Risk + Policy + Persistent Queue + Analyst
      ↓
Static / Adaptive Fraudster
      ↓
Core policy experiments
      ↓
Sensitivity / robustness
      ↓
KLTN Results
```

## Source of truth hiện tại

- [[De an to KLTN - Development Map]]
- [[Current Direction - 2026-10-11]]
- [[Research Design v1.1 - Develop from FinRisk Proposal]]
- [[Xente Full Model Specification v1.0]]
- [[Parameter Registry v0.2]]
- [[Adaptive Fraudster Design v0.1]]
- [[Validation Plan v1.0]]
- [[Final Core Experiment Grid v1.0]]

## Những gì đã làm thật

### Xente empirical layer
- 95,662 labelled transactions;
- 193 fraud;
- 3,742 CustomerIds;
- chronological state/features;
- logistic risk baseline;
- temporal / structural score checks.

### Operational layer
- persistent alert queue;
- FIFO / risk-priority;
- fixed/relative pooled capacity;
- threshold overload;
- service-time stochasticity;
- variable team capacity;
- starvation/tail waiting.

### Adaptive layer
- fraudster state/update prototype;
- static comparator;
- dormancy mechanism;
- synthetic smoke experiment.

### Policy layer
Đã thêm interface chung:
- Fixed-threshold;
- Capacity-aware;
- Cost-sensitive extension.

## Scope core

### Data
- **Xente: core**
- IEEE-CIS: optional external robustness.

### Policy
- Fixed-threshold: core.
- Capacity-aware: core.
- Cost-sensitive: extension nếu cost grounding đủ tốt.

### Core experiment

```text
2 Fraudster modes
×
2 Policies
×
3 Capacity levels
=
12 configurations
```

## Việc tiếp theo

1. tích hợp policy layer vào Xente event-driven simulator;
2. freeze baseline queue discipline;
3. xây empirical fraud transaction generator;
4. nối Static Fraudster;
5. nối Adaptive Fraudster;
6. chạy end-to-end pilot;
7. chạy 12 core configurations;
8. sensitivity / convergence;
9. final writing.
