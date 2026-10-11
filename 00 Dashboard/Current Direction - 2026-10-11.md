# Hướng nghiên cứu hiện tại — 2026-10-11

## Một câu để nhớ

> Dùng **Agent-Based Modelling (ABM) như một phòng thí nghiệm chính sách** để stress-test các chính sách quản lý gian lận giao dịch trong hệ thống có fraudster thích nghi và fraud analyst có năng lực review hữu hạn.

## Vai trò từng phần

- **Mục tiêu:** policy experimentation / stress testing.
- **ABM:** công cụ nghiên cứu.
- **Adaptive fraudster:** cơ chế stress-test.
- **Alert queue + analyst capacity:** ràng buộc vận hành.
- **Risk model:** thành phần cung cấp risk score.
- **Public data:** grounding empirical cho scenario.
- **Sensitivity analysis:** xử lý uncertainty khi parameter không xác định chính xác.

## Câu hỏi nghiên cứu chính

> Các chính sách quản lý gian lận giao dịch khác nhau hoạt động như thế nào khi fraudster có khả năng thích nghi và analyst capacity bị giới hạn?

## Ba câu hỏi phụ

### RQ1 — Adaptation
Fraudster thích nghi làm thay đổi fraud loss và policy effectiveness thế nào so với fraudster tĩnh?

### RQ2 — Policy trade-off
Các policy tạo trade-off thế nào giữa:
- fraud loss;
- false positive;
- customer friction;
- analyst workload;
- backlog / delay?

### RQ3 — Robustness
Analyst capacity và parameter uncertainty làm thay đổi kết luận policy thế nào?

## Kiến trúc khái niệm

```text
Customer --------\
                  \
                   -> Transaction -> Detection -> Policy
Fraudster --------/                             |
   ^                                            |
   |                                            v
   +----------- feedback <--- Approve / Step-up / Review / Block
                                              |
                                              v
                                         Alert Queue
                                              |
                                              v
                                           Analyst
                                              |
                                              v
                                           Outcome
```

Có hai feedback loop:

1. **Adversarial:** system response làm fraudster thay đổi strategy.
2. **Operational:** policy làm thay alert volume, queue, backlog và review delay.

## Dữ liệu

### Scenario A — IEEE-CIS
Online/card/e-commerce.

### Scenario B — Xente
Mobile/payment/e-commerce.

Không ghép hai dataset.

Mỗi scenario có:
- empirical distributions riêng;
- risk model riêng;
- parameter riêng;
- cùng một conceptual framework.

## Policy dự kiến

1. Fixed threshold.
2. Cost-sensitive.
3. Capacity-aware.

## Ba experiment chính

1. Static vs adaptive fraudster.
2. So sánh ba policy.
3. Analyst-capacity stress test.

## Điều đã có

Phần Xente đã có:
- data audit;
- empirical profile;
- leakage-safe features;
- logistic risk baseline;
- persistent queue;
- FIFO vs risk-priority;
- capacity and threshold sensitivity;
- stochastic robustness.

Adaptive fraudster đã có:
- specification;
- code prototype;
- unit test;
- synthetic smoke runner.

## Điều chưa có

- IEEE-CIS audit đầy đủ theo scope mới;
- adaptive fraudster tích hợp vào Xente/IEEE scenario thật;
- final policy definitions;
- full final experiment grid;
- final Results/Discussion.

## Claim boundary

Không claim:
- digital twin;
- production threshold;
- bank staffing recommendation;
- fraudster cognition “thật”;
- universal best policy.

Chỉ kết luận trong phạm vi scenario, assumptions và ranges đã thử.
