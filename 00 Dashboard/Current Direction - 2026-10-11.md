# Hướng nghiên cứu hiện tại — 2026-10-11

## Một câu để nhớ

> Phát triển trực tiếp từ đề án FinRisk: dùng ABM/dynamic simulation như một phòng thí nghiệm policy, nhưng empirical-ground tốt hơn bằng Xente, mô hình hóa persistent analyst queue và nâng risky actor thành adaptive fraudster có feedback qua nhiều vòng.

## KLTN giữ gì từ đề án?

Giữ:
- transaction-risk decisioning ở cấp policy;
- risk scoring;
- analyst capacity;
- fraud loss / false positive / workload trade-off;
- capacity-aware và cost-sensitive ideas;
- risky actor / strategic interaction.

## KLTN phát triển gì?

1. Synthetic transaction framework → Xente empirical replay + grounded counterfactuals.
2. Proxy risk score → trained/validated risk score.
3. Daily overflow → persistent queue/backlog/waiting time.
4. Fixed risky strategy → static vs adaptive fraudster.
5. Scenario comparison → systematic factorial experiment + sensitivity.

## Main RQ

> Các chính sách quản lý gian lận giao dịch hoạt động như thế nào khi fraudster thích nghi với phản hồi của hệ thống và analyst capacity bị giới hạn?

## Core model

```text
Customer / Fraudster
        ↓
Transaction
        ↓
Detection / Risk score
        ↓
Policy
   ┌────┼────┐
Approve Review Block
          ↓
      Alert Queue
          ↓
       Analyst
          ↓
        Outcome
          ↓
Fraudster feedback / future behavior
```

## Core empirical environment

### Xente — CORE
Dùng để:
- empirical customer/history state;
- chronology;
- risk model;
- queue/policy replay;
- grounding fraud generator.

### IEEE-CIS — OPTIONAL
Chỉ dùng làm external/cross-scenario robustness nếu core Xente hoàn thành.

## Core policies

1. Fixed-threshold.
2. Capacity-aware.

Cost-sensitive:
- giữ như extension;
- đưa vào main results nếu cost parameters đủ defensible.

## Core experiment

```text
Static / Adaptive fraudster
×
Fixed / Capacity-aware
×
Low / Medium / High capacity
=
12 configurations
```

## Robustness riêng

- FIFO vs risk-priority;
- full vs degraded score model;
- stochastic service;
- variable team capacity;
- fraudster learning/exploration sensitivity;
- optional cost-sensitive policy.

## Đã hoàn thành

Xente:
- audit/profile;
- past-only features;
- logistic baseline;
- temporal robustness;
- persistent queue;
- threshold/load sensitivity;
- queue-priority experiments;
- stochastic/variable capacity robustness.

Adaptive:
- design;
- code prototype;
- static comparator;
- unit tests;
- synthetic smoke runner.

Policy:
- shared action/context interface;
- Fixed-threshold policy;
- Capacity-aware policy;
- Cost-sensitive extension;
- policy tests added.

## Chưa hoàn thành

- integrated Xente policy engine;
- empirical fraud transaction generator;
- static fraudster integration;
- adaptive fraudster integration;
- core 12-run families across seeds;
- behavioral sensitivity;
- final Methods/Results/Discussion.

## Claim boundary

Không claim:
- digital twin;
- production bank rules;
- exact analyst staffing;
- exact fraudster cognition;
- universal best policy.
