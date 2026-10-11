# READING ORDER — Nắm toàn bộ KLTN từ branch chatgpt-draft

## Mục tiêu

Đọc theo thứ tự này để hiểu **mình đang làm gì bây giờ**, sau đó mới quay lại các kết quả Xente cũ để biết **mình đã làm được gì trước đó**.

---

## Track A — Nắm đề tài trong 20–30 phút

### 1. [[Current Direction - 2026-10-11]]
Đọc đầu tiên.

Sau file này phải trả lời được:
- mục tiêu nghiên cứu là gì;
- ABM đóng vai trò gì;
- adaptive fraudster đóng vai trò gì;
- analyst capacity đóng vai trò gì;
- data nào đang dùng.

### 2. [[Research Design v1.0 - Policy Experimentation]]
Đọc để hiểu:
- research problem;
- main RQ;
- 3 sub-RQ;
- contribution;
- scope và claim boundary.

### 3. [[Conceptual Model v1.0 - Adaptive Policy ABM]]
Đọc để hình dung model chạy như thế nào:
- state;
- action;
- feedback;
- queue;
- analyst;
- adaptation.

### 4. [[GVHD Brief - Current Direction 2026-10-11]]
Đọc cuối Track A.

Nếu hiểu được file này, bạn đã đủ để giải thích đề tài cho GVHD trong vài phút.

---

## Track B — Hiểu methodology

### 5. [[Two-Scenario Data Strategy v0.1]]
Hiểu tại sao:
- IEEE-CIS và Xente là hai scenario riêng;
- không merge hai dataset;
- dataset ground được gì và không ground được gì.

### 6. [[Parameter Registry v0.2]]
Đây là file quan trọng nhất trước khi code sâu.

Phân biệt:
- empirical parameters;
- literature-informed parameters;
- policy variables;
- uncertain behavioral assumptions.

### 7. [[Adaptive Fraudster Design v0.1]]
Hiểu:
- adaptive state;
- reward;
- learning rule;
- dormancy;
- static comparator.

### 8. [[Queue and Analyst Service Design v0.1]]
Đây là một trong những phần mạnh nhất từ hướng cũ và vẫn dùng được.

Hiểu:
- persistent queue;
- FIFO vs risk-priority;
- pooled capacity;
- waiting time/backlog;
- starvation.

### 9. [[Operational Parameter Grounding v0.1]]
Đọc để hiểu tại sao không được tự bịa:
- analyst cases/day;
- review time;
- analyst accuracy;
- recovery rate.

### 10. [[Validation Plan v0.1]]
Đọc để hiểu:
- verification;
- input validation;
- stochastic uncertainty;
- parameter sensitivity;
- structural sensitivity.

Lưu ý: file này được viết trước adaptive-fraudster direction nên cần được mở rộng sau, nhưng nền validation vẫn hữu ích.

---

## Track C — Hiểu những gì đã thật sự làm bằng Xente

### 11. [[Xente Empirical Profile]]
Đây là evidence thực nghiệm quan trọng nhất đã hoàn thành.

### 12. [[Xente Baseline Risk Model Feasibility]]
Hiểu risk score baseline và hạn chế mạnh của Xente:
- Value signal rất mạnh;
- classifier không phải contribution.

### 13. [[Xente Queue Pilot v0.1]]
Thí nghiệm đầu tiên chứng minh queue policy có thể thay đổi outcome khi score/capacity giữ nguyên.

### 14. [[Xente Robustness Pack v0.1]]
Hiểu:
- temporal instability;
- weaker score model;
- cold-start;
- stochastic service robustness.

### 15. [[Xente Alert-rate and Starvation Sensitivity v0.1]]
Hiểu:
- threshold thấp hơn có thể tạo overload;
- risk-priority có trade-off starvation.

### 16. [[Xente Variable Team Capacity Sensitivity v0.1]]
Hiểu tác động của capacity variability.

Các file 11–16 là **pilot/empirical groundwork cho Xente scenario**, không phải full result của hướng adaptive-ABM hiện tại.

---

## Track D — Code

Đọc code theo thứ tự:

1. `scripts/profile_xente.py`
2. `scripts/build_xente_features.py`
3. `scripts/train_xente_baseline.py`
4. `scripts/simulate_alert_queue.py`
5. `scripts/adaptive_fraudster.py`
6. `scripts/run_adaptive_vs_static.py`
7. `tests/test_alert_queue.py`
8. `tests/test_adaptive_fraudster.py`

Sau đó mới đọc các robustness runners.

---

## Files không nên dùng để học current direction

Các file dưới đây là **superseded framing**:

- [[Research Design v0.2]]
- [[Candidate Core Specification v0.3]]
- [[Core Experiment Grid v0.1]]
- [[Conceptual Model v0.2]]
- [[GVHD Update - Xente Queue Milestone]]
- [[Methodology Skeleton v0.1]]
- [[Results and Discussion Outline v0.1]]

Chúng không sai hoàn toàn, nhưng mô tả hướng **Xente-only queue/capacity** trước khi adaptive-fraudster + two-scenario framing được chốt.

Đọc chúng chỉ khi cần truy lịch sử quyết định hoặc tái sử dụng một mechanism.

---

## Files lịch sử / archive

- [[Legacy Project Audit - FinRisk]]
- [[Legacy Migration Map]]
- [[Prototype-to-Thesis Gap]]

Chúng giúp hiểu dự án đi từ prototype cũ tới KLTN như thế nào, nhưng không cần đọc trước buổi gặp GVHD.

---

## Nếu chỉ có 10 phút

Đọc đúng 4 file:

1. [[Current Direction - 2026-10-11]]
2. [[Research Design v1.0 - Policy Experimentation]]
3. [[Conceptual Model v1.0 - Adaptive Policy ABM]]
4. [[GVHD Brief - Current Direction 2026-10-11]]
