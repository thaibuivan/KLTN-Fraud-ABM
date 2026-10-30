# Xente Full Model Specification v1.0

## Mục tiêu

Đây là specification cho **full Xente model** dùng làm core của KLTN.

Nó nối các phần đã có:
- Xente empirical replay;
- leakage-safe customer state;
- risk model;
- persistent queue;
- analyst capacity;
- adaptive fraudster;
- fraud-management policy.

## 1. Time/event structure

Mô hình xử lý event theo chronological order.

Mỗi transaction event có tối thiểu:
- TransactionId;
- CustomerId;
- timestamp;
- Value;
- context features;
- risk score;
- ground-truth label đối với observed Xente replay.

## 2. Legitimate customer state

Baseline state lấy từ past-only history:
- prior transaction count;
- prior Value mean/std;
- time since previous transaction;
- rolling 1h/24h/7d count;
- prior product/category share;
- prior channel share.

Không dùng future information.

## 3. Fraudster state

Static fraudster:
- fixed strategy distribution;
- không update sau system response.

Adaptive fraudster:
- current strategy;
- strategy value estimates;
- recent responses;
- consecutive block count;
- optional dormancy state.

Strategy set chỉ giữ những dimension có thể defend bằng public data / explicit assumption.

MVP ưu tiên:
- amount regime;
- timing/velocity regime;
- context selection nếu Xente support đủ.

## 4. Detection system

Input:
- current transaction features;
- past-only customer state.

Output:
- risk probability p_t.

Baseline:
- regularized logistic regression.

Robustness:
- no-current-value;
- amount-only;
- optional stronger model nếu cần, nhưng classifier novelty không phải contribution.

## 5. Policy interface

Mọi policy phải trả về một action chung:

```text
APPROVE
REVIEW
BLOCK
```

STEP-UP chưa đưa vào core để tránh thêm mechanism/cost chưa được ground.

Policy nhận:
- risk_probability;
- transaction_value;
- queue state;
- service/capacity state;
- policy parameters.

## 6. Fixed-threshold policy

Hai threshold:

```text
p < T_review            → APPROVE
T_review ≤ p < T_block  → REVIEW
p ≥ T_block             → BLOCK
```

Balanced/sensitive/strict từ đề án cũ trở thành các giá trị khác nhau của T_review/T_block.

## 7. Capacity-aware policy

Policy quan sát congestion.

MVP dùng backlog-hours proxy:

```math
B_t = Q_t / \mu_t
```

trong đó:
- Q_t: số alert đang chờ;
- mu_t: service rate mỗi giờ.

Khi B_t tăng:
- review threshold tăng;
- policy chỉ route các case rủi ro cao hơn vào review.

Đây là **experimental policy mechanism**, không claim là bank rule thực.

## 8. Cost-sensitive policy

Không phải core bắt buộc.

Nếu dùng:
- expected fraud loss;
- review cost;
- false-positive/friction cost;
- analyst review accuracy;
đều phải nằm trong Parameter Registry và sensitivity-test.

## 9. Queue

Core baseline:
- persistent queue;
- risk-priority hoặc FIFO được freeze trước final experiment.

Structural robustness:
- đổi sang discipline còn lại.

Metrics:
- queue length;
- backlog end;
- mean/P95/P99 wait;
- >24/48/72h shares;
- low/high-priority tail wait.

## 10. Analyst

MVP:
- pooled team capacity;
- deterministic service để debug;
- stochastic service/capacity trong robustness.

Không cần từng analyst agent riêng nếu không phục vụ RQ.

## 11. Outcome semantics

### APPROVE
- legitimate: no intervention;
- fraud: successful fraud exposure/value.

### BLOCK
- fraud: prevented exposure;
- legitimate: false-positive block / friction event.

### REVIEW
- alert vào queue;
- nếu review bắt đầu trong horizon: fraud được tính là captured trong baseline;
- nếu chưa được review: unresolved within horizon.

Analyst error chỉ thêm như sensitivity nếu có grounding.

## 12. Feedback sang fraudster

Fraudster quan sát system response:
- APPROVE;
- REVIEW;
- BLOCK.

Reward/update:
- APPROVE fraud: positive reward theo amount/exposure;
- REVIEW: penalty;
- BLOCK: larger penalty.

Learning-rate và exploration là explicit behavioral assumptions.

## 13. Core metrics

Fraud:
- successful fraud value;
- prevented fraud value;
- fraud capture within horizon.

Customer:
- legitimate review count;
- legitimate block count;
- intervention rate.

Operations:
- alerts;
- backlog;
- waiting-time distribution;
- analyst utilization proxy.

Không gộp thành TotalCost trong core nếu cost assumptions chưa đủ mạnh.

## 14. Definition of done

Full Xente model được coi là hoàn thành khi:
- [ ] policy interface chung chạy được;
- [ ] fixed-threshold chạy end-to-end;
- [ ] capacity-aware chạy end-to-end;
- [ ] queue state được policy quan sát đúng thời điểm;
- [ ] static fraudster tích hợp;
- [ ] adaptive fraudster tích hợp;
- [ ] feedback update được test;
- [ ] core 12 configurations chạy được;
- [ ] multiple seeds;
- [ ] sensitivity cho behavioral parameters;
- [ ] verification tests pass;
- [ ] final tables/figures reproducible.
