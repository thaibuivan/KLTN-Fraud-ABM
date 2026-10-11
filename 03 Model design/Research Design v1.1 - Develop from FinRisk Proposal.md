# Research Design v1.1 — Phát triển trực tiếp từ đề án FinRisk

## Tên đề tài làm việc

**Mô phỏng dựa trên tác tử để stress-test chính sách quản lý gian lận giao dịch dưới hành vi gian lận thích nghi và giới hạn năng lực phân tích**

Tên tiếng Anh:

**Agent-Based Stress Testing of Transaction Fraud-Management Policies under Adaptive Fraudster Behavior and Analyst Capacity Constraints**

## Logic phát triển từ đề án

Đề án trước đã xây framework transaction-risk decisioning:

```text
risk score → policy → analyst capacity → system outcome
```

KLTN giữ nguyên câu hỏi nền đó nhưng nâng bốn điểm:
1. empirical grounding;
2. persistent operational dynamics;
3. adaptive fraudster;
4. systematic uncertainty/robustness analysis.

## Vấn đề nghiên cứu

Fraud classifier chỉ tạo risk score. Tổ chức vẫn phải quyết định:
- approve;
- review;
- block;
- và phân bổ review capacity hữu hạn.

Một threshold nhạy hơn có thể tăng candidate fraud coverage nhưng đồng thời làm:
- alert volume tăng;
- false positive tăng;
- queue quá tải;
- waiting time tăng;
- lower-priority cases bị starvation.

Ngoài ra, risky actor có thể phản ứng lại policy, làm transaction distribution và score distribution thay đổi theo thời gian.

Vì vậy đây là bài toán **dynamic policy evaluation**, không chỉ classification.

## Câu hỏi nghiên cứu chính

> Các chính sách quản lý gian lận giao dịch hoạt động như thế nào khi fraudster có khả năng thích nghi với phản hồi của hệ thống và năng lực review của analyst bị giới hạn?

## Câu hỏi phụ

### RQ1 — Adaptation
So với fraudster tĩnh, adaptive fraudster làm thay đổi:
- successful fraud exposure;
- fraud capture;
- alert volume;
- queue pressure;
như thế nào?

### RQ2 — Policy
Fixed-threshold và capacity-aware policy tạo trade-off thế nào giữa:
- fraud capture/loss exposure;
- false positive;
- review volume;
- backlog;
- waiting time?

Cost-sensitive policy được thêm nếu cost assumptions đủ defensible.

### RQ3 — Capacity / robustness
Policy ranking có thay đổi khi:
- analyst capacity thấp/trung bình/cao;
- score quality yếu đi;
- service/capacity biến động;
- behavioral assumptions thay đổi?

## Mục tiêu nghiên cứu

Xây một closed-loop simulation framework có empirical grounding, cho phép:

```text
transaction
→ risk
→ policy
→ queue/analyst
→ outcome
→ fraudster feedback
→ future transaction behavior
```

## Empirical strategy

### Core
**Xente** là development environment chính vì hiện đã có:
- empirical profile;
- repeated CustomerId;
- real transaction timestamp;
- leakage-safe customer-history features;
- trained risk baseline;
- queue/capacity experiments.

### Optional external robustness
**IEEE-CIS** được giữ như scenario mở rộng nếu core model hoàn thành sớm.

Không cần IEEE-CIS để claim core KLTN hoàn thành.

## Core policy families

### 1. Fixed-threshold
Policy baseline. Balanced/sensitive/strict trong đề án cũ được hiểu là các operating points khác nhau của cùng family này.

### 2. Capacity-aware
Policy được phép quan sát queue/capacity state và thay đổi routing/review threshold theo congestion.

### 3. Cost-sensitive — extension
Policy chọn action theo expected cost/loss.

Chỉ đưa vào main results nếu:
- cost parameters được phân loại rõ;
- uncertainty ranges được khai báo;
- conclusion không phụ thuộc vào một bộ cost tùy ý.

## Core experiment

```text
Fraudster mode: Static / Adaptive
×
Policy: Fixed / Capacity-aware
×
Capacity: Low / Medium / High
= 12 configurations
```

Mỗi configuration chạy nhiều seeds khi stochastic/adaptation được bật.

## Robustness riêng

Không đưa mọi yếu tố vào full factorial.

Chạy riêng:
- FIFO vs risk-priority;
- full vs degraded risk score;
- service-time variation;
- team-capacity variation;
- fraudster learning-rate / exploration sensitivity;
- cost-sensitive extension.

## Contribution dự kiến

Không claim:
- classifier mới;
- adaptive fraudster mới hoàn toàn;
- digital twin;
- universal best policy.

Contribution hướng tới:

> Một framework phát triển từ FinRisk proposal, trong đó empirical transaction state, risk scoring, persistent analyst queue và adaptive fraudster được đóng vòng để stress-test fraud-management policy dưới resource constraints.

## Sản phẩm cuối

1. Xente-grounded simulation environment;
2. policy interface;
3. persistent queue/analyst module;
4. static + adaptive fraudster;
5. core factorial experiment;
6. sensitivity/robustness package;
7. Methods / Results / Discussion có claim boundary rõ.
