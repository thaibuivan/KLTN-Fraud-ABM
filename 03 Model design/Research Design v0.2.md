---
status: draft
version: v0.2
legacy_basis: FinRisk-ABM-Policy-Simulation
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

Câu hỏi này cố ý chưa khóa cứng nhãn ABM trước khi conceptual model chứng minh đủ persistent state, interaction và feedback.

## 4. Sub-RQs

### RQ1 — Policy trade-offs
Các policy khác nhau tạo trade-off như thế nào giữa fraud loss, false positives/customer friction và analyst workload?

### RQ2 — Capacity and queue dynamics
Analyst capacity, queue/backlog và review delay thay đổi policy effectiveness như thế nào?

### RQ3 — Robustness under uncertainty
Policy conclusions có ổn định khi fraud regime, cost assumptions, uncertain parameters và một số structural assumptions quan trọng thay đổi không?

## 5. Objectives
1. Chọn một primary transaction-fraud dataset làm empirical grounding.
2. Định nghĩa state, rules và parameter provenance.
3. Xây dynamic baseline gồm transaction/customer state, risk engine, policy layer, persistent alert queue và analyst capacity.
4. So sánh ít nhất 2–3 policy dưới cùng environment.
5. Đánh giá bằng system metrics, không chỉ predictive metrics.
6. Kiểm tra robustness qua repeated seeds, parameter sensitivity và structural sensitivity có chọn lọc.

## 6. Expected contribution

### Methodological
Đặt risk model vào một dynamic operational environment có capacity constraints và explicit uncertainty.

### Analytical
Làm rõ khi nào policy ranking thay đổi do capacity, risk regime hoặc cost assumptions.

### Reproducibility
Tách empirical inputs, literature-informed ranges và explicit assumptions.

## 7. Scope

### Core
- transaction fraud;
- policy experimentation;
- queue/backlog;
- analyst capacity;
- loss / FP / workload / delay / cost metrics;
- uncertainty and sensitivity.

### Extension only
- adaptive fraudster cognition;
- LLM analyst/advisor;
- sophisticated game-theoretic equilibrium;
- bank-specific digital twin.

## 8. Claim boundary
Không claim:
- mô phỏng chính xác một ngân hàng cụ thể;
- policy tối ưu phổ quát;
- fraud actor thật suy nghĩ như model;
- simulated cost là chi phí tài chính thật nếu không có evidence.

Kết luận nên có dạng:
> Policy A tạo trade-off tốt hơn policy B trong các scenario/ranges đã đánh giá, nhưng ranking có thể thay đổi khi điều kiện X thay đổi.

## 9. Legacy findings dùng như pilot hypotheses
Các insight từ repo cũ chỉ dùng để thiết kế experiment mới:
- capacity thấp có thể làm overflow tăng và đổi policy ranking;
- threshold nhạy hơn có thể tăng recall nhưng tăng workload/FP;
- recall-first và capacity-aware ranking phục vụ mục tiêu vận hành khác nhau;
- simulated utility nhạy với cost assumptions.

Các insight này phải được re-test trong KLTN.

## 10. Immediate decisions
- [ ] Primary dataset.
- [ ] Customer hay Account là stateful entity chính.
- [ ] Queue persistence và service discipline.
- [ ] Risk-engine baseline.
- [ ] Main policy set.
- [ ] Analyst/cost parameter ranges.
- [ ] ABM hay dynamic policy simulation là framing chính xác hơn.
