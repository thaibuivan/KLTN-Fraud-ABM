# Practitioner Validation Questions v0.1

## Purpose
Dùng practitioner để **validate workflow/mechanism và plausible ranges**, không hỏi bí mật nội bộ hay threshold sản xuất.

Mục tiêu là kiểm tra:
- model có sai nghiệp vụ ở đâu;
- queue priority nào hợp lý;
- parameter nào có thể đặt low/medium/high range;
- KPI nào thực sự có ý nghĩa.

Không yêu cầu:
- exact bank threshold;
- số lượng fraud thật;
- confidential model features;
- staffing/headcount cụ thể nếu nhạy cảm.

---

## 1. Workflow validation

### Q1
Ở mức khái quát, flow này có hợp lý không?

```text
transaction
→ risk score
→ policy/action
→ alert queue
→ analyst review
→ decision/outcome
```

**Model decision affected:** conceptual structure.

### Q2
Có bước quan trọng nào bị thiếu giữa alert và analyst decision không?
Ví dụ:
- automated step-up;
- customer contact;
- secondary system check;
- case consolidation;
- escalation.

**Model decision affected:** whether queue is too simple.

---

## 2. Queue priority

### Q3
Khi alert volume vượt capacity, team thường ưu tiên theo yếu tố nào ở mức khái quát?
- risk score;
- transaction amount/exposure;
- customer segment;
- alert age/SLA;
- fraud type;
- combination/hybrid rule.

**Model decision affected:** FIFO vs risk-priority vs hybrid/aging.

### Q4
Pure FIFO có bao giờ là approximation hợp lý không, hay thực tế luôn có priority?

### Q5
Nếu một alert score thấp chờ quá lâu, có:
- aging priority;
- expiry;
- auto-close;
- escalation;
- SLA trigger?

**Model decision affected:** starvation/expiry mechanism.

---

## 3. Review time and capacity

### Q6
Có thể chia review thành các mức như:
- fast/light-touch;
- standard;
- complex/escalated
không?

Nếu có, practitioner chỉ cần cho **broad plausible range**, không cần số nội bộ chính xác.

**Model decision affected:** service-time distribution.

### Q7
Capacity thực tế thường ổn định hay thay đổi đáng kể theo:
- ngày/ca;
- incident;
- campaign;
- staffing;
- system outage?

**Model decision affected:** constant vs variable team capacity.

### Q8
Khi overload xảy ra, team thường:
- tăng staffing;
- tăng threshold;
- auto-clear low-risk alerts;
- prioritize high-risk;
- accept backlog;
- combination?

**Model decision affected:** policy adaptation scenarios.

---

## 4. Analyst heterogeneity

### Q9
Sự khác nhau giữa analyst có đủ lớn để cần mô hình riêng từng analyst không?

Hay pooled-team abstraction là đủ cho câu hỏi policy-level?

**Model decision affected:** whether heterogeneous analyst agents are justified.

### Q10
Nếu heterogeneity quan trọng, dimension nào quan trọng nhất?
- speed;
- experience;
- fraud-type expertise;
- decision quality;
- escalation tendency.

Không hỏi accuracy cá nhân cụ thể.

---

## 5. False positive / customer friction

### Q11
False positive trong workflow này thường gây friction theo hình thức nào?
- transaction hold/block;
- step-up authentication;
- customer contact;
- card/account restriction;
- manual delay.

**Model decision affected:** friction proxy.

### Q12
KPI nào team thực sự quan tâm hơn:
- false-positive count/rate;
- customer contact rate;
- blocked legitimate value;
- complaint/churn;
- review workload?

**Model decision affected:** thesis output metrics.

---

## 6. Delay and fraud loss

### Q13
Review delay có làm giảm khả năng ngăn/recover loss không?

Nếu có, practitioner có thể mô tả:
- mechanism;
- order-of-magnitude time windows;
- fraud types where delay matters.

Không cần exact recovery percentage.

**Model decision affected:** whether delay → loss mechanism is defensible.

### Q14
Transaction amount có phải proxy hợp lý cho loss exposure không, hay cần cap/adjustment?

---

## 7. Policy evaluation

### Q15
Nếu so hai fraud policies, những KPI nào practitioner muốn nhìn cùng nhau?
Candidate:
- fraud captured/missed;
- false positives;
- alert volume;
- backlog;
- mean/P95 turnaround time;
- analyst workload;
- exposed value;
- operational cost.

### Q16
Có KPI nào trong danh sách trên dễ gây hiểu nhầm nếu không có dữ liệu bank-specific?

---

## 8. Plausible scenarios

### Q17
Ba trạng thái stress nào hợp lý nhất để mô phỏng mà không tiết lộ data nội bộ?
Ví dụ:
- fraud pressure tăng;
- alert volume tăng;
- analyst capacity giảm;
- service time tăng;
- risk-model degradation.

### Q18
Các capacity scenario dạng **under-capacity / matched / spare-capacity** có hợp lý hơn việc giả định một con số alerts/day tuyệt đối không?

---

## 9. Questions to avoid
Không hỏi:
- production threshold;
- exact fraud rate;
- exact loss;
- customer PII;
- proprietary feature list;
- confidential headcount;
- confidential model performance.

## 10. How to record answers
Mỗi answer ghi theo format:

```text
Question:
Practitioner answer:
Mechanism supported?
Parameter/range suggested?
Confidentiality restriction?
Model change:
Evidence type: expert-informed
```

Mọi value practitioner cung cấp phải được label **expert-informed**, không biến thành universal empirical truth.

Links:
- [[Operational Parameter Grounding v0.1]]
- [[Queue and Analyst Service Design v0.1]]
- [[Evidence Parameter Matrix]]
