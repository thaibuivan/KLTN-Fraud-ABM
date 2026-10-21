# Hướng nghiên cứu hiện tại

## Một câu để nhớ

> Phát triển trực tiếp từ đề án FinRisk thành một closed-loop ABM/dynamic policy laboratory có persistent queue và adaptive fraudster, rồi kiểm tra cùng framework trên **hai empirical scenarios bổ sung cho nhau: Xente và IEEE-CIS**.

## KLTN giữ gì từ đề án?

Giữ:
- transaction-risk decisioning ở cấp policy;
- risk scoring;
- analyst capacity;
- fraud loss / false positive / workload trade-off;
- capacity-aware và cost-sensitive ideas;
- risky actor / strategic interaction.

## KLTN phát triển gì?

1. Synthetic-only framework → empirical grounding trên Xente và IEEE-CIS.
2. Proxy risk score → scenario-specific trained/validated risk models.
3. Daily overflow → persistent queue/backlog/waiting time.
4. Fixed risky strategy → static vs adaptive fraudster.
5. Scenario comparison → controlled factorial experiment + cross-scenario robustness.

## Hai empirical scenarios core

### Scenario A — Xente
Mạnh ở:
- CustomerId;
- repeated history;
- timestamp thực;
- customer-centric state.

### Scenario B — IEEE-CIS
Mạnh ở:
- card/device/identity context;
- richer transaction-risk features;
- entity/proxy heterogeneity;
- online/card/e-commerce environment khác Xente.

Không merge data.

## Main RQ

> Các fraud-management policies hoạt động như thế nào khi fraudster thích nghi và analyst capacity bị giới hạn, và policy conclusions có robust giữa Xente và IEEE-CIS hay không?

## Shared model

```text
Scenario state
    ↓
Transaction
    ↓
Risk score
    ↓
Policy
 ┌──┼──┐
Approve Review Block
        ↓
      Queue
        ↓
     Analyst
        ↓
     Outcome
        ↓
Fraudster feedback
```

## Core experiment

```text
2 datasets
× 2 fraudster modes
× 2 policies
× 3 capacity levels
= 24 configurations
```

Core policies:
1. Fixed-threshold.
2. Capacity-aware.

Cost-sensitive:
- extension nếu grounding cost đủ mạnh.

## Implementation order

1. develop/freeze engine trên Xente;
2. tách common interfaces;
3. parameterize IEEE-CIS bằng adapter riêng;
4. chạy cùng protocol;
5. compare cross-scenario.

## Claim boundary

Không claim:
- digital twin;
- production bank rules;
- exact analyst staffing;
- exact fraudster cognition;
- universal best policy.
