# Methodology Skeleton v1.0

## 1. Research design

Khóa luận phát triển từ FinRisk proposal theo hướng:
- dynamic policy evaluation;
- empirical grounding bằng Xente;
- persistent operational constraints;
- adaptive adversarial feedback.

Main RQ:
> Các chính sách quản lý gian lận giao dịch hoạt động như thế nào khi fraudster thích nghi và analyst capacity bị giới hạn?

## 2. Data

### 2.1 Xente
Mô tả:
- transaction-level public dataset;
- CustomerId;
- TransactionStartTime;
- Value/Amount;
- product/provider/channel context;
- FraudResult.

### 2.2 Data role
Không dùng Xente để identify mọi parameter.

Xente dùng để ground:
- transaction chronology;
- customer history;
- fraud prevalence;
- amount/context distributions;
- risk model.

Không có trực tiếp:
- analyst capacity;
- review time;
- adaptive learning rate;
- policy counterfactual;
- friction cost.

## 3. Empirical preprocessing

### 3.1 Chronological ordering
Không random split làm baseline chính.

### 3.2 Leakage-safe customer state
Past-only:
- prior count;
- prior Value mean/std;
- inter-arrival gap;
- rolling velocity;
- product/channel history.

### 3.3 Cold-start
Unseen/new customer state được xử lý bằng population/default state thay vì future information.

## 4. Risk model

Baseline:
- regularized logistic regression.

Vai trò:
- cung cấp risk_probability cho policy.

Không claim classifier novelty.

Validation:
- chronological 70/15/15;
- PR-AUC;
- ROC-AUC;
- Brier;
- temporal robustness;
- degraded-score sensitivity.

## 5. Agent / system specification

### 5.1 Customer
Persistent state từ transaction history.

### 5.2 Fraudster
Static vs adaptive.

Adaptive state:
- strategy values;
- recent response;
- block/dormancy state.

### 5.3 Detection system
Module tạo risk score.

### 5.4 Policy
Core:
- fixed-threshold;
- capacity-aware.

Optional:
- cost-sensitive.

### 5.5 Alert queue
Persistent queue.

Baseline discipline được freeze trước final experiment.

### 5.6 Analyst
Pooled finite service capacity.

## 6. Event loop

Mỗi event:
1. transaction xuất hiện;
2. state/features được xác định từ current/past information;
3. risk model tạo p_t;
4. policy chọn APPROVE/REVIEW/BLOCK;
5. REVIEW vào queue;
6. analyst service diễn ra theo capacity;
7. outcome được ghi;
8. fraudster nhận feedback nếu event là fraud;
9. state update.

## 7. Policy definitions

### Fixed
```text
p < T_review            → APPROVE
T_review ≤ p < T_block  → REVIEW
p ≥ T_block             → BLOCK
```

### Capacity-aware
Review threshold phụ thuộc congestion state.

Backlog-hours proxy:
```math
B_t = Q_t / \mu_t
```

Khi B_t tăng, policy nâng review threshold theo experimental rule.

## 8. Fraudster adaptation

Value update:
```math
V_s^{t+1}=V_s^t+\alpha(r_t-V_s^t)
```

Strategy choice:
- epsilon-greedy baseline.

Không claim đây là exact fraud cognition.

## 9. Experimental design

Core:
```text
2 fraudster modes
×
2 policies
×
3 capacity levels
= 12 configurations
```

Repeated seeds.

## 10. Outcomes

Fraud:
- successful fraud value;
- prevented/intercepted fraud value;
- fraud intercept/capture.

Customer:
- legitimate review;
- legitimate block;
- intervention rate.

Operations:
- backlog;
- waiting time;
- queue tails;
- service load.

## 11. Validation and uncertainty

- conceptual validation;
- empirical input validation;
- code verification;
- temporal score robustness;
- stochastic replication;
- parameter sensitivity;
- structural sensitivity;
- extreme-condition tests.

## 12. Claim boundaries

Kết luận là conditional simulation findings.

Không suy rộng trực tiếp thành:
- production rule;
- bank staffing;
- universal policy optimum;
- real fraudster cognition.
