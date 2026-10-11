# Từ đề án FinRisk đến khóa luận — Bản đồ phát triển

## Một câu để hiểu mối quan hệ

Khóa luận **không đổi sang một đề tài khác**. Nó phát triển trực tiếp từ đề án:

> từ một framework mô phỏng policy dựa nhiều vào synthetic assumptions sang một dynamic policy-simulation / ABM có empirical grounding tốt hơn, persistent operational state và adaptive fraudster.

## Những gì đề án đã có

Đề án đã đặt bài toán ở cấp **transaction-risk decisioning**, không chỉ fraud classification.

Luồng cũ:

```text
Synthetic customer / transaction
        ↓
Proxy risk score
        ↓
Policy
        ↓
Approve / Review / Escalate / Block
        ↓
Daily analyst capacity
        ↓
Precision / Recall / Overflow / Net benefit
```

Các policy đã xuất hiện:
- balanced threshold;
- sensitive threshold;
- strict threshold;
- capacity-aware;
- cost-sensitive.

Risky actor cũng đã tồn tại ở mức conceptual với các strategy như high-amount, burst/velocity và normal-like behavior.

## Những hạn chế của đề án mà KLTN sẽ phát triển

### 1. Dữ liệu
Đề án:
- tự sinh transaction stream synthetic;
- public datasets chủ yếu dùng làm tham chiếu phân phối.

KLTN:
- Xente là empirical development environment chính;
- observed transaction stream được replay theo thời gian;
- customer state và risk score được xây từ public transaction data;
- chỉ mô phỏng/counterfactual những thành phần lịch sử không thể trực tiếp cung cấp.

### 2. Risk score
Đề án:
- proxy/rule-based score.

KLTN:
- leakage-safe features;
- chronological train/validation/test;
- trained risk model;
- temporal and structural robustness.

### 3. Analyst capacity
Đề án:
- capacity theo ngày;
- vượt capacity tạo overflow.

KLTN:
- persistent queue;
- backlog tồn tại qua thời gian;
- waiting time;
- starvation/tail delay;
- variable service/capacity stress.

### 4. Risky actor
Đề án:
- strategy chủ yếu được chỉ định trước;
- strategic reaction mới ở mức minh họa.

KLTN:
- static comparator;
- adaptive fraudster có state;
- quan sát APPROVE/REVIEW/BLOCK;
- cập nhật strategy value;
- feedback qua nhiều vòng.

### 5. Policy experiment
Đề án:
- nhiều policy nhưng định nghĩa còn lẫn giữa threshold level và policy family.

KLTN:
- gom balanced/sensitive/strict thành **Fixed-threshold policy** với threshold là policy parameter;
- **Capacity-aware policy** là core alternative;
- **Cost-sensitive policy** là extension/core tùy khả năng ground cost assumptions.

## Scope core hiện tại

### Empirical environment
**Xente là development environment chính.**

IEEE-CIS:
- không bỏ;
- để làm external/cross-scenario robustness nếu thời gian và scope cho phép;
- không phải dependency để hoàn thành core KLTN.

### Core experiment tối giản

```text
2 fraudster modes
×
2 core policies
×
3 analyst-capacity levels
=
12 configurations
```

Fraudster:
- Static
- Adaptive

Policy:
- Fixed threshold
- Capacity-aware

Capacity:
- Low
- Medium
- High

Cost-sensitive:
- chạy như extension nếu cost parameters đủ defensible.

Queue discipline:
- giữ một discipline làm baseline;
- FIFO vs risk-priority dùng structural robustness, không nhân vào toàn bộ factorial grid.

## Chuỗi phát triển từ giờ

```text
Freeze research design
        ↓
Freeze policy interface
        ↓
Integrated Xente policy engine
        ↓
Static fraudster empirical generator
        ↓
Adaptive fraudster feedback
        ↓
12 core configurations
        ↓
Sensitivity / robustness
        ↓
Optional IEEE-CIS replication
        ↓
Methods + Results + Discussion
```

## Nguyên tắc chống mở rộng scope

Mỗi cơ chế mới phải trả lời được:
1. nó phục vụ RQ nào?
2. data/literature/assumption nào support nó?
3. nếu bỏ nó, kết luận chính có thay đổi không?

Nếu không trả lời được, chưa thêm vào core model.
