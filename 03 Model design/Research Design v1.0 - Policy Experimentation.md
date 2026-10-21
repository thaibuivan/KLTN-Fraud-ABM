# Research Design v1.0 — Thử nghiệm chính sách

## Tên đề tài dự kiến

**Mô phỏng dựa trên tác tử để stress-test chính sách quản lý gian lận giao dịch dưới hành vi gian lận thích nghi và giới hạn năng lực phân tích**

Tên tiếng Anh:
**Agent-Based Stress Testing of Transaction Fraud-Management Policies under Adaptive Fraudster Behavior and Analyst Capacity Constraints**

## Vấn đề nghiên cứu

Fraud detection thường được đánh giá bằng AUC, Precision, Recall, F1.

Nhưng khi triển khai thật, risk score phải được chuyển thành hành động:
- approve;
- step-up;
- review;
- block.

Hạ threshold có thể tăng fraud capture nhưng đồng thời:
- tăng alert;
- tăng false positive;
- làm analyst quá tải;
- tăng backlog;
- tăng review delay;
- tăng customer friction.

Ngoài ra fraudster có thể phản ứng lại hệ thống và thay đổi:
- amount;
- timing;
- identity;
- strategy.

Vì vậy đề tài xem fraud management là một **dynamic policy problem**, không chỉ là classification problem.

## Câu hỏi nghiên cứu chính

> Các chính sách quản lý gian lận giao dịch khác nhau hoạt động như thế nào khi fraudster có khả năng thích nghi và analyst capacity bị giới hạn?

## RQ1 — Adaptive fraudster

Hành vi thích nghi làm thay đổi fraud loss và detection outcome thế nào so với fraudster tĩnh?

## RQ2 — Policy trade-off

Các fraud-management policies tạo trade-off thế nào giữa:
- fraud loss;
- detection;
- false positive;
- customer friction;
- analyst workload?

## RQ3 — Operational robustness

Analyst capacity và các parameter/mechanism bất định làm thay đổi policy conclusion thế nào?

## Mục tiêu nghiên cứu

Xây một ABM / dynamic policy-simulation framework có empirical grounding để chạy counterfactual experiments.

## Đóng góp dự kiến

Đề tài **không** nhằm:
- đề xuất classifier mới;
- claim adaptive fraudster là ý tưởng chưa từng có.

Đóng góp hướng tới một closed-loop framework kết hợp:

- persistent customer/fraud state;
- adaptive fraudster;
- risk/detection system;
- alert queue;
- limited analyst capacity;
- alternative fraud-management policies;
- repeated stochastic simulation;
- sensitivity / structural robustness.

## Metrics

### Fraud / detection
- fraud detection rate;
- false negative rate;
- successful fraud value;
- prevented fraud value.

### Customer
- false-positive rate;
- challenge/review rate;
- friction proxy nếu đủ grounding.

### Operations
- queue length;
- backlog;
- waiting time;
- analyst utilization.

### Economics
- fraud loss;
- review cost;
- false-positive / friction cost;
- total cost nếu cost assumptions được công khai rõ.

## Scope hiện tại

Core:
- IEEE-CIS scenario;
- Xente scenario;
- adaptive fraudster;
- alert queue;
- analyst capacity;
- fixed / cost-sensitive / capacity-aware policy;
- sensitivity and robustness.

Nedbank và AMLSim/Libra không phải core dependency ở giai đoạn này.

## Giới hạn

Không claim mô hình đại diện chính xác một ngân hàng hay hệ thống thực tế cụ thể. Kết luận phải mang tính điều kiện theo data, scenario, model structure và parameter range đã thử.
