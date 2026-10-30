---
status: draft
version: v0.2
legacy_basis: FinRisk-ABM-Policy-Simulation
primary_dataset: Xente Fraud Detection
---

# Research Design v0.2

## 1. Positioning
KLTN phát triển từ pilot `FinRisk-ABM-Policy-Simulation`, nơi đã cho thấy một điểm quan trọng: **cùng một risk score có thể tạo outcome khác khi policy, analyst capacity và cost assumptions thay đổi**.

KLTN không chỉ lặp lại policy comparison. Bước phát triển mới là xây một **empirically grounded, uncertainty-aware dynamic simulation/ABM** để kiểm tra robustness của policy conclusions.

## 2. Research problem
Predictive metrics không đủ để đánh giá fraud-management policy. Operational effectiveness còn phụ thuộc vào:
- transaction/customer state;
- risk scoring;
- decision policy;
- alert arrival;
- analyst capacity;
- queue/backlog;
- review delay;
- false positives/customer friction;
- fraud loss;
- operational cost;
- parameter/model uncertainty.

## 3. Main Research Question
> **How do alternative transaction-fraud management policies perform under operational capacity constraints and uncertainty when evaluated in a dynamic agent-based/policy-simulation environment?**

Câu hỏi này cố ý chưa khóa cứng nhãn ABM trước khi implementation chứng minh đủ persistent state, interaction và feedback.

## 4. Sub-RQs

### RQ1 — Policy trade-offs
Các policy khác nhau tạo trade-off như thế nào giữa fraud loss, false positives/customer friction và analyst workload?

### RQ2 — Capacity and queue dynamics
Analyst capacity, queue/backlog và review delay thay đổi policy effectiveness như thế nào?

### RQ3 — Robustness under uncertainty
Policy conclusions có ổn định khi fraud regime, cost assumptions, uncertain parameters và một số structural assumptions quan trọng thay đổi không?

## 5. Empirical strategy

### Primary dataset
**Xente Fraud Detection.**

Reason:
- explicit `CustomerId`, `AccountId`, `SubscriptionId`;
- actual `TransactionStartTime`;
- observed fraud label in training period;
- manageable size for repeated experiments.

### Baseline data strategy
Không dùng synthetic generator làm core baseline.

Baseline sẽ **replay observed Xente transaction events chronologically**, sau đó đưa chúng qua:
1. leakage-safe rolling customer features;
2. risk engine;
3. policy;
4. persistent alert queue;
5. analyst service;
6. outcome/cost engine.

Synthetic/counterfactual perturbation chỉ xuất hiện ở stress scenarios và phải được gắn nhãn rõ.

### Primary stateful entity
**Customer = `CustomerId`.**

`AccountId` và `SubscriptionId` ban đầu là nested grouping/state, chưa tách thành independent agents.

## 6. Objectives
1. Profile Xente và xây chronological empirical baseline.
2. Định nghĩa state, rules và parameter provenance.
3. Xây dynamic baseline gồm customer state, risk engine, policy layer, persistent alert queue và analyst capacity.
4. So sánh 2–3 policy dưới cùng environment.
5. Đánh giá bằng system metrics, không chỉ predictive metrics.
6. Kiểm tra robustness qua repeated seeds, parameter sensitivity và structural sensitivity có chọn lọc.

## 7. Expected contribution

### Methodological
Đặt risk model vào một dynamic operational environment có capacity constraints và explicit uncertainty.

### Analytical
Làm rõ khi nào policy ranking thay đổi do capacity, risk regime hoặc cost assumptions.

### Reproducibility
Tách empirical inputs, literature-informed ranges và explicit assumptions.

## 8. Scope

### Core
- Xente-based transaction fraud baseline;
- policy experimentation;
- queue/backlog;
- analyst capacity;
- loss / FP / workload / delay / cost metrics;
- uncertainty and sensitivity.

### Extension only
- IEEE-CIS external robustness;
- adaptive fraudster cognition;
- LLM analyst/advisor;
- sophisticated game-theoretic equilibrium;
- bank-specific digital twin.

## 9. Claim boundary
Không claim:
- mô phỏng chính xác một ngân hàng cụ thể;
- Xente đại diện cho ngân hàng Việt Nam;
- policy tối ưu phổ quát;
- fraud actor thật suy nghĩ như model;
- simulated cost là chi phí tài chính thật nếu không có evidence.

Kết luận nên có dạng:
> Policy A tạo trade-off tốt hơn policy B trong các scenario/ranges đã đánh giá, nhưng ranking có thể thay đổi khi điều kiện X thay đổi.

## 10. Legacy findings dùng như pilot hypotheses
Các insight từ repo cũ chỉ dùng để thiết kế experiment mới:
- capacity thấp có thể làm overflow tăng và đổi policy ranking;
- threshold nhạy hơn có thể tăng recall nhưng tăng workload/FP;
- recall-first và capacity-aware ranking phục vụ mục tiêu vận hành khác nhau;
- simulated utility nhạy với cost assumptions.

Các insight này phải được re-test trong KLTN.

## 11. Decisions

- [x] Primary dataset: **Xente Fraud Detection**.
- [x] Primary stateful entity: **CustomerId**.
- [x] Account/Subscription: nested grouping/state trước, không tách agent ngay.
- [x] Baseline data mode: **observed-event replay**, không synthetic core.
- [ ] Queue discipline và review-delay mechanism.
- [ ] Risk-engine baseline.
- [ ] Main policy set.
- [ ] Analyst/cost parameter ranges.
- [ ] Final framing: ABM hay dynamic policy simulation sau khi implementation tối thiểu hoàn tất.
