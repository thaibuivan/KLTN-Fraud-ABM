# Methodology Skeleton v1.0

## 1. Research design

Khóa luận phát triển từ FinRisk proposal theo hướng:
- dynamic policy evaluation;
- two-scenario empirical grounding;
- persistent operational constraints;
- adaptive adversarial feedback.

Main RQ:
> Các fraud-management policies hoạt động như thế nào khi fraudster thích nghi và analyst capacity bị giới hạn, và các kết luận có robust giữa hai transaction environments hay không?

## 2. Data strategy

### 2.1 Scenario A — Xente
Customer/history-rich:
- CustomerId;
- TransactionStartTime;
- Value/Amount;
- Product/Provider/Channel;
- FraudResult.

### 2.2 Scenario B — IEEE-CIS
Identity/device-rich:
- transaction amount/product;
- card context;
- address/email relations;
- device/identity features;
- count/time-delta/match/rich detector features;
- isFraud;
- relative TransactionDT.

### 2.3 Không merge datasets
Mỗi scenario có:
- state representation riêng;
- risk model riêng;
- empirical parameters riêng;
- cùng shared system architecture.

## 3. Scenario-specific state construction

### Xente
Past-only customer history:
- prior count;
- Value mean/std;
- inter-arrival;
- rolling velocity;
- product/channel history;
- cold-start handling.

### IEEE-CIS
Entity/proxy state:
- card/device/identity/address/email context;
- chronological proxy history;
- missing/unknown identity handling.

Không gọi entity proxy là true customer.

## 4. Risk models

Train riêng cho từng scenario.

Yêu cầu chung:
- chronological validation;
- probability/risk score output;
- PR-AUC / ROC-AUC / calibration;
- drift diagnostics;
- degraded-score robustness.

Classifier novelty không phải contribution.

## 5. Shared system specification

- Fraudster: Static / Adaptive.
- Detection: scenario-specific risk module.
- Policy: Fixed / Capacity-aware.
- Queue: persistent.
- Analyst: pooled finite capacity.
- Outcome module: shared semantics.

## 6. Shared event loop

1. event xuất hiện;
2. scenario-specific state/features được cập nhật bằng current/past information;
3. risk model tạo p_t;
4. policy chọn APPROVE/REVIEW/BLOCK;
5. REVIEW vào queue;
6. analyst service;
7. outcome;
8. fraudster feedback nếu là fraud event;
9. state update.

## 7. Policies

### Fixed
```text
p < T_review            → APPROVE
T_review ≤ p < T_block  → REVIEW
p ≥ T_block             → BLOCK
```

### Capacity-aware
Dùng congestion state, ví dụ backlog-hours:

```math
B_t = Q_t / \mu_t
```

để điều chỉnh review threshold.

## 8. Fraudster adaptation

```math
V_s^{t+1}=V_s^t+\alpha(r_t-V_s^t)
```

Strategy choice:
- epsilon-greedy baseline.

Giữ learning rule giống nhau giữa hai scenarios; strategy-to-feature mapping có thể khác.

## 9. Experimental design

```text
2 datasets
× 2 fraudster modes
× 2 policies
× 3 capacity levels
= 24 configurations
```

Repeated seeds.

## 10. Cross-scenario comparison

Không so raw scale máy móc.

So:
- adaptation penalty;
- policy gain;
- policy ranking;
- congestion response;
- relative effects.

## 11. Outcomes

Fraud:
- successful/prevented exposure;
- capture/intercept rate.

Customer/intervention:
- legitimate review/block;
- intervention rate.

Operations:
- backlog;
- waiting-time distribution;
- load/utilization proxy.

## 12. Validation and uncertainty

- conceptual validation;
- input/empirical validation;
- code verification;
- temporal/drift checks;
- stochastic replication;
- parameter sensitivity;
- structural sensitivity;
- cross-scenario robustness;
- extreme-condition tests.

## 13. Claim boundaries

Kết luận là conditional simulation findings theo từng scenario và across-scenario comparison.

Không suy rộng thành universal production rules.
