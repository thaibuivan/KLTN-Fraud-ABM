# Legacy Project Audit - FinRisk

## Repo được audit
`thaibuivan/FinRisk-ABM-Policy-Simulation`

## Những gì đề án cũ đã làm được

### 1. Policy-first framing
Repo cũ đã chuyển trọng tâm từ fraud classification sang transaction-risk decisioning và đánh giá trade-off giữa:
- fraud loss;
- false positives;
- analyst workload/capacity;
- customer-friction proxy;
- simulated net benefit.

### 2. Synthetic simulation pilot
Code legacy đã tạo:
- customer profiles;
- transaction stream;
- fraud labels/strategies;
- behavior features;
- risk scores;
- policy decisions;
- analyst reviews;
- outcome/cost metrics.

### 3. Policy experiments
Đã có các candidate policy:
- balanced threshold;
- sensitive threshold;
- strict threshold;
- capacity-aware;
- cost-sensitive.

### 4. Capacity/cost/scenario experiments
Repo đã chạy scenario theo fraud pressure, analyst capacity và cost assumptions. Đây là phần nên tái sử dụng về **experiment logic**, nhưng không coi các con số legacy là kết luận KLTN.

### 5. Risk-model experiments
Đã có nhiều phiên bản XGBoost và recall-first operating-point analysis. Insight hữu ích: operating point phục vụ recall cao và operating point phục vụ capacity thấp có thể khác nhau.

## Khoảng trống khi nâng thành KLTN

### A. Chưa đủ để mặc định gọi là ABM
Trong code legacy, customer profiles được sinh trước, transactions được tạo theo vòng lặp, rồi policy/analyst review được áp dụng theo procedure. Analyst capacity chủ yếu là giới hạn số case/ngày.

Điều này là một **policy simulation tốt**, nhưng chưa tự động chứng minh có:
- agent scheduling rõ;
- persistent agent states thay đổi qua thời gian;
- queue state động qua nhiều timestep;
- interaction/feedback;
- emergence từ tương tác agent.

### B. Empirical grounding còn yếu
ULB, BankSim và PaySim được dùng để tham khảo high-level patterns cho synthetic generator. Nhiều parameter vận hành vẫn là giả định mô phỏng, ví dụ:
- analyst capacity;
- review time;
- false-positive cost;
- recovery rate;
- một số fraud-strategy probabilities.

KLTN phải phân loại rõ empirical / literature-informed / expert-informed / explicit assumption.

### C. Fraud adaptation chưa được chứng minh
Legacy framing nói về fraud adaptation, nhưng generator chủ yếu lấy strategy từ distribution định trước. Vì vậy core KLTN nên dùng **bounded fraud regimes/scenarios** thay vì claim fraudster cognition.

### D. Analyst mechanism còn đơn giản
Review accuracy/time hiện là xác suất/phân phối đặt trước. Chưa có persistent queue/backlog hoặc analyst heterogeneity được grounding.

### E. LLM/AI explanation chưa đủ evidence
Token-cost feasibility và theoretical framing có ích, nhưng chưa có evidence để đưa LLM thành core contribution.

## Quyết định chuyển tiếp
- Giữ repo cũ làm archive/pilot evidence.
- Không rewrite lịch sử repo cũ để biến nó thành thesis.
- Thiết kế mới nằm trong `KLTN-Fraud-ABM`.
- Chỉ migrate code khi module đó gắn trực tiếp với RQ và parameter provenance mới.

## Reusable assets
- policy comparison logic;
- capacity-aware ranking;
- cost/outcome engine;
- recall-first operating-point analysis;
- plotting/report utilities.

## Rewrite-first assets
- agent/state model;
- scheduler/timestep;
- persistent queue/backlog;
- empirical-data adapter;
- uncertainty runner;
- validation tests.
