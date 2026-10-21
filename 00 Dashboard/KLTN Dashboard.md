# KLTN Dashboard

## Hướng hiện tại

> **KLTN phát triển trực tiếp từ đề án FinRisk và kiểm tra cùng một policy-testing framework trên hai empirical environments bổ sung cho nhau: Xente và IEEE-CIS.**

## Câu hỏi nghiên cứu chính

> Các chính sách quản lý gian lận giao dịch hoạt động như thế nào khi fraudster thích nghi với phản hồi của hệ thống và analyst capacity bị giới hạn, và các kết luận này có robust giữa hai transaction environments khác nhau hay không?

## Bản đồ nghiên cứu

```text
Đề án FinRisk
      ↓
Shared ABM / policy framework
      ↓
 ┌───────────────┬────────────────┐
 ↓               ↓
Xente          IEEE-CIS
Customer-      Card/device/
history rich   identity-context rich
 ↓               ↓
scenario-specific risk/state
 └───────┬───────┘
         ↓
Static / Adaptive
× Fixed / Capacity-aware
× Low / Medium / High capacity
         ↓
Cross-scenario comparison
```

## Source of truth

- [[De an to KLTN - Development Map]]
- [[Research Design v1.1 - Develop from FinRisk Proposal]]
- [[Shared Two-Scenario Architecture v1.0]]
- [[Xente Full Model Specification v1.0]]
- [[Xente Full Implementation Plan v1.0]]
- [[IEEE-CIS Full Implementation Plan v1.0]]
- [[Parameter Registry v0.2]]
- [[Adaptive Fraudster Design v0.1]]
- [[Validation Plan v1.0]]
- [[Final Core Experiment Grid v1.0]]
- [[Cross-Scenario Comparison Plan v1.0]]

## Trạng thái

### Xente
Đã làm sâu:
- empirical profile;
- customer-history features;
- risk baseline;
- queue/capacity experiments;
- robustness.

### IEEE-CIS
Đã có:
- EDA;
- data-to-ABM mapping;
- role definition: identity/device-rich scenario.

Còn thiếu:
- executable chronological feature pipeline;
- scenario-specific risk pipeline;
- common-schema adapter;
- full policy/adaptation runs.

### Shared engine
Đã có:
- fixed/capacity-aware policy code;
- integrated policy + persistent queue simulator;
- adaptive fraudster prototype;
- verification tests.

## Core experiment

```text
2 Dataset
× 2 Fraudster mode
× 2 Policy
× 3 Capacity
= 24 configurations
```

## Việc tiếp theo

1. hoàn thiện Xente integrated policy replay;
2. freeze shared interfaces;
3. nối Static rồi Adaptive fraudster trên Xente;
4. build IEEE-CIS feature/risk/adapter pipeline;
5. nối cùng Static/Adaptive mechanism vào IEEE;
6. chạy 12 Xente + 12 IEEE;
7. cross-scenario comparison;
8. sensitivity/convergence;
9. final writing.
