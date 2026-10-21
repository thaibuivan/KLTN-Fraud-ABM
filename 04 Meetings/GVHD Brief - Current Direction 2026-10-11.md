# Brief gặp GVHD — Hướng hiện tại — 2026-10-11

## 1. Em đang nghiên cứu gì?

Em dùng ABM như một **môi trường thử nghiệm/stress-test chính sách quản lý gian lận giao dịch**.

Em không tập trung vào việc xây classifier có AUC cao nhất.

## 2. Vì sao dùng ABM?

Hệ thống có:
- customer/fraud state tồn tại qua thời gian;
- adaptive fraud behavior;
- alert queue;
- limited analyst capacity;
- backlog / waiting time;
- feedback từ system response sang hành vi tương lai.

Nếu model cuối cùng chỉ còn transaction -> score -> threshold -> cost thì em sẽ cân nhắc gọi là dynamic/discrete-event policy simulation thay vì ép ABM.

## 3. Mô hình dự kiến

```text
Customer / Fraudster
        ↓
Transactions
        ↓
Detection System
        ↓
Approve / Step-up / Review / Block
                   ↓
               Alert Queue
                   ↓
                Analyst
                   ↓
                Outcome

Fraudster quan sát phản hồi -> update strategy -> transaction tiếp theo
```

## 4. Main RQ

> Các chính sách quản lý gian lận giao dịch khác nhau hoạt động như thế nào khi fraudster có khả năng thích nghi và analyst capacity bị giới hạn?

## 5. Data

Hai scenario core:
- IEEE-CIS;
- Xente.

Không merge hai dataset.

## 6. Policy dự kiến

- Fixed threshold.
- Cost-sensitive.
- Capacity-aware.

## 7. Experiment dự kiến

1. Static vs adaptive fraudster.
2. Policy comparison.
3. Analyst-capacity stress test.

## 8. Điểm khó methodology

Khó không chỉ ở code agent.

Khó nhất là:
- chọn đúng mechanism;
- biết parameter nào empirical;
- parameter nào literature-informed;
- parameter nào policy variable;
- parameter nào chỉ là behavioral assumption.

Mục tiêu không phải tìm một “true parameter vector”, mà xem policy conclusion có robust trong plausible ranges hay không.

## 9. Những gì em đã làm thật

Trên Xente:
- data audit / empirical profile;
- leakage-safe features;
- logistic risk baseline;
- persistent queue;
- FIFO vs risk-priority;
- capacity stress;
- threshold/load sensitivity;
- stochastic/variable capacity robustness.

Adaptive fraudster:
- đã có conceptual design;
- đã có smoke-test code;
- chưa tích hợp full empirical ABM.

## 10. Các câu cần hỏi cô

1. Policy experimentation có đúng là central framing không?
2. Adaptive fraudster nên được xem là stress mechanism thay vì main output có đúng không?
3. IEEE-CIS + Xente có đủ làm core scope không?
4. Cấu trúc customer/fraudster/analyst + queue có đủ justify ABM không?
5. Fixed / cost-sensitive / capacity-aware có phải policy set phù hợp không?
6. Behavioral parameters nên xử lý chủ yếu bằng sensitivity thay vì cố calibration có hợp lý không?
