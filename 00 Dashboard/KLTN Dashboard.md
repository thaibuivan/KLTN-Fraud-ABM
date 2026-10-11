# KLTN Dashboard

## Hướng hiện tại

> **Dùng ABM để thử nghiệm chính sách quản lý gian lận giao dịch trong hệ thống có fraudster thích nghi và analyst capacity hữu hạn.**

### Câu hỏi nghiên cứu chính

> Các chính sách quản lý gian lận giao dịch khác nhau hoạt động như thế nào khi fraudster có khả năng thích nghi và năng lực xử lý của fraud analyst bị giới hạn?

## Hãy nhớ 5 khối này

```text
Research Question
      ↓
Real Data
      ↓
Risk + Policy + Queue + Analyst
      ↓
Adaptive Fraudster
      ↓
Policy Experiments + Robustness
```

## File nào là “nguồn sự thật” hiện tại?

- [[Current Direction - 2026-10-11]]
- [[Research Design v1.0 - Policy Experimentation]]
- [[Conceptual Model v1.0 - Adaptive Policy ABM]]
- [[Parameter Registry v0.2]]
- [[Two-Scenario Data Strategy v0.1]]
- [[Adaptive Fraudster Design v0.1]]
- [[Adaptive Policy Experiment Plan v0.1]]
- [[GVHD Brief - Current Direction 2026-10-11]]

Các file v0.1/v0.2/v0.3 cũ không phải hướng hiện tại nếu nội dung mâu thuẫn với các file trên.

## Những gì đã làm thật

### 1. Xente data
- audit dữ liệu;
- profile empirical;
- 95,662 giao dịch có nhãn;
- 193 fraud;
- 3,742 CustomerId;
- phát hiện cold-start và strong Value signal.

### 2. Risk baseline
- chronological 70/15/15;
- leakage-safe customer history;
- logistic baseline;
- temporal robustness;
- full / no-current-value / amount-only comparison.

### 3. Queue / analyst capacity
- persistent alert queue;
- FIFO;
- risk-priority;
- fixed/relative pooled capacity;
- threshold overload;
- stochastic service time;
- variable team capacity;
- starvation / tail-wait diagnostics;
- queue verification tests.

### 4. Hướng ABM mới
- Research Design v1.0;
- two-scenario strategy: IEEE-CIS + Xente;
- adaptive fraudster specification;
- adaptive fraudster smoke-test code;
- Parameter Registry;
- supervisor brief.

## Những gì chưa xong

- IEEE-CIS audit theo scope hiện tại;
- tích hợp adaptive fraudster vào empirical scenario;
- freeze 3 policy definitions;
- full adaptive-vs-static experiment;
- cross-scenario robustness;
- final sensitivity;
- final Results/Discussion.

## Conceptual model

```text
Customer --------\
                  \
                   -> Transaction -> Detection System -> Policy
Fraudster --------/                                  |
   ^                                                  |
   |                                                  v
   +--------- observe response <--- Approve / Step-up / Review / Block
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

## Policy dự kiến

1. Fixed threshold.
2. Cost-sensitive.
3. Capacity-aware.

## Thí nghiệm chính

1. Static vs Adaptive Fraudster.
2. Policy comparison.
3. Analyst-capacity stress test.

## Quy tắc parameter

Mỗi parameter phải thuộc một trong bốn nhóm:

- empirical;
- literature-informed;
- policy variable;
- explicit behavioral assumption.

Không có dữ liệu thì không được giả vờ là đã “estimate”.

## Việc tiếp theo

1. Gặp GVHD và chốt framing.
2. Freeze policy definitions.
3. Audit IEEE-CIS.
4. Tích hợp adaptive fraudster vào một scenario trước.
5. Chạy MVP end-to-end.
6. Sau đó mới mở rộng robustness.
