# Research Design v1.1 — Phát triển trực tiếp từ đề án FinRisk

## Tên đề tài làm việc

**Mô phỏng dựa trên tác tử để stress-test chính sách quản lý gian lận giao dịch dưới hành vi gian lận thích nghi và giới hạn năng lực phân tích**

Tên tiếng Anh:

**Agent-Based Stress Testing of Transaction Fraud-Management Policies under Adaptive Fraudster Behavior and Analyst Capacity Constraints**

## Logic phát triển từ đề án

Đề án trước đã có:

```text
risk score → policy → analyst capacity → system outcome
```

KLTN nâng bốn điểm:
1. empirical grounding trên hai environments;
2. persistent operational dynamics;
3. adaptive fraudster;
4. systematic cross-scenario uncertainty/robustness.

## Main RQ

> Các fraud-management policies hoạt động như thế nào khi fraudster có khả năng thích nghi với phản hồi của hệ thống và năng lực review của analyst bị giới hạn, và các kết luận này có robust giữa các transaction environments khác nhau hay không?

## Sub-RQ

### RQ1 — Adaptation
Static vs Adaptive ảnh hưởng:
- successful fraud exposure;
- fraud capture;
- alert volume;
- queue pressure;
như thế nào?

### RQ2 — Policy
Fixed-threshold vs Capacity-aware tạo trade-off thế nào giữa:
- fraud outcome;
- false positive/intervention;
- review volume;
- backlog;
- waiting time?

### RQ3 — Capacity
Policy ranking thay đổi ra sao ở Low / Medium / High capacity?

### RQ4 — Cross-scenario robustness
Các effect/ranking trên có nhất quán giữa:
- Xente;
- IEEE-CIS;
hay phụ thuộc environment?

## Empirical strategy

### Scenario A — Xente
Customer/history-rich environment:
- CustomerId;
- timestamp thực;
- repeated history;
- product/provider/channel context.

### Scenario B — IEEE-CIS
Identity/device-rich e-commerce environment:
- transaction amount/product;
- card/device/identity/address/email context;
- count/time-delta/match/rich detector features;
- relative transaction time.

Không merge datasets.

Mỗi scenario có:
- state representation riêng;
- risk model riêng;
- empirical parameterization riêng;
- cùng policy/queue/adaptation framework.

## Core policies

### 1. Fixed-threshold
Baseline policy family.

### 2. Capacity-aware
Policy quan sát congestion/capacity state.

### 3. Cost-sensitive — extension
Chỉ đưa vào main analysis nếu cost assumptions đủ defensible.

## Core experiment

```text
Dataset: Xente / IEEE-CIS
× Fraudster: Static / Adaptive
× Policy: Fixed / Capacity-aware
× Capacity: Low / Medium / High
= 24 configurations
```

## Robustness chạy riêng

- FIFO vs risk-priority;
- degraded score model;
- stochastic service;
- variable capacity;
- alpha/epsilon sensitivity;
- cost-sensitive extension.

## Contribution dự kiến

> Một closed-loop fraud-management policy-testing framework phát triển từ FinRisk proposal, được parameterize độc lập trên hai empirical transaction environments bổ sung cho nhau và dùng để đánh giá adaptation × policy × capacity interactions.

Không claim:
- new classifier;
- exact fraud cognition;
- digital twin;
- universal optimum.
