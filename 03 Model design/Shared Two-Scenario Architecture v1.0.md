# Shared Two-Scenario Architecture v1.0

## Mục tiêu

Khóa luận dùng **hai empirical scenarios bổ sung cho nhau** nhưng không merge dữ liệu:

- **Scenario A — Xente:** customer/history-rich payment environment.
- **Scenario B — IEEE-CIS:** card/device/identity-rich e-commerce environment.

Hai scenario dùng chung **system architecture**, nhưng state representation, risk model và empirical parameters được xây riêng.

## Shared architecture

```text
Scenario-specific transaction/entity state
                ↓
         Risk / Detection
                ↓
             Policy
      ┌─────────┼─────────┐
   APPROVE    REVIEW      BLOCK
                ↓
          Persistent Queue
                ↓
             Analyst
                ↓
             Outcome
                ↓
   Fraudster feedback / adaptation
```

## Phần PHẢI giống nhau giữa hai scenario

Để so sánh policy có ý nghĩa, giữ chung:

1. action space: APPROVE / REVIEW / BLOCK;
2. policy interface;
3. fixed-threshold policy logic;
4. capacity-aware policy logic;
5. queue/analyst mechanism;
6. fraudster learning/update rule;
7. Low / Medium / High capacity definition theo normalized load;
8. outcome definitions;
9. seed/replication protocol;
10. reporting metrics.

## Phần ĐƯỢC phép khác nhau

### Xente
State thiên về:
- CustomerId repeated history;
- Value/Amount;
- timestamp thực;
- Product/Provider/Channel;
- customer velocity/history.

### IEEE-CIS
State thiên về:
- TransactionAmt;
- ProductCD;
- card context;
- device / identity context;
- address/email relation;
- count/time-delta/match features;
- entity proxies thay vì true CustomerId.

Risk model phải train riêng cho từng scenario.

Fraud prevalence và empirical distributions **không ép bằng nhau**.

## Quy tắc so sánh

Không so raw outcome trực tiếp nếu scale/base rate khác nhau mà không chuẩn hóa.

Ưu tiên so:
- direction của policy effect;
- relative improvement;
- policy ranking;
- interaction với capacity;
- adaptation penalty;
- congestion response.

Ví dụ:

```text
Adaptive penalty
= outcome_adaptive - outcome_static
```

hoặc:

```text
Policy gain
= outcome_capacity-aware - outcome_fixed
```

theo metric phù hợp.

## Cross-scenario research question

> Khi cùng một fraud-management policy framework được parameterize độc lập trên Xente và IEEE-CIS, các kết luận về adaptation, analyst capacity và policy trade-off có giữ được về mặt định tính hay không?

## Ý nghĩa của hai scenario

Xente giúp kiểm tra framework trong môi trường:
- entity/customer state dễ diễn giải;
- timeline thực;
- repeated behavior rõ.

IEEE-CIS giúp kiểm tra framework trong môi trường:
- transaction risk context giàu hơn;
- card/device/identity heterogeneity cao;
- nhiều feature detection nhưng interpretability thấp hơn.

Nếu kết luận giống nhau:
- tăng bằng chứng robustness.

Nếu kết luận khác:
- đó là evidence rằng policy performance phụ thuộc transaction environment.

Cả hai trường hợp đều là kết quả nghiên cứu có giá trị.
