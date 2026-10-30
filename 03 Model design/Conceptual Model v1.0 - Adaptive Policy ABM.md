# Conceptual Model v1.0 — ABM thử nghiệm policy với fraudster thích nghi

## Mục đích của mô hình

Mô hình được dùng như một **môi trường thử nghiệm / stress-test chính sách**.

Nó không nhằm tái tạo chính xác một ngân hàng cụ thể.

## Các thành phần chính

### Customer agent

State có thể gồm:
- lịch sử giao dịch;
- transaction frequency / velocity;
- thống kê amount gần đây;
- product/channel history;
- accumulated friction nếu thật sự cần cho RQ.

Action:
- sinh hoặc replay giao dịch hợp lệ.

### Fraudster agent

State:
- strategy hiện tại;
- strategy value / preference;
- recent success rate;
- recent system responses;
- consecutive-block counter;
- dormancy state nếu dùng.

Action:
- chọn strategy;
- tạo fraud transaction.

Adaptation:
- quan sát APPROVE / STEP-UP / REVIEW / BLOCK;
- cập nhật preference;
- thay đổi hành vi tương lai.

### Detection system

Đây có thể là module thay vì agent.

Input:
- transaction features;
- past-only state/features.

Output:
- fraud-risk score;
- rule trigger nếu có rule layer.

### Policy layer

Biến risk/state thành action.

Candidate actions:
- APPROVE;
- STEP-UP;
- REVIEW;
- BLOCK.

Candidate policies:
1. fixed threshold;
2. cost-sensitive;
3. capacity-aware.

### Alert queue

State:
- alert arrival;
- priority;
- waiting time;
- backlog;
- service status.

Queue rule:
- FIFO;
- risk-priority;
- hybrid/aging chỉ thêm khi có lý do rõ.

### Fraud analyst

Baseline:
- pooled review capacity;
- service process;
- review outcome nếu sau này model analyst error.

Không cần bắt đầu bằng từng analyst riêng biệt.

## Luồng hệ thống

```text
LEGITIMATE CUSTOMER
        |
        v
legitimate transaction
        |
        +----------------------+
                               |
                               v
                        DETECTION SYSTEM
                               |
ADAPTIVE FRAUDSTER             |
        |                      |
        v                      |
fraud transaction -------------+
                               |
                               v
                         POLICY LAYER
                               |
              +----------------+----------------+
              |                |                |
           APPROVE          STEP-UP          BLOCK
              |
              +---------- REVIEW
                           |
                           v
                      ALERT QUEUE
                           |
                           v
                    FRAUD ANALYST
                           |
                           v
                        OUTCOME
                           |
                           v
        fraud loss / FP / workload / delay / cost
```

## Feedback loop 1 — adversarial

```text
fraudster action
      ↓
system response
      ↓
reward / penalty
      ↓
strategy update
      ↓
future strategy choice
```

Đây là cơ chế khiến fraudster trở thành adaptive stress mechanism.

## Feedback loop 2 — operational

```text
policy threshold / action rule
      ↓
alert arrivals
      ↓
queue / backlog
      ↓
waiting time / service pressure
      ↓
review outcome và system metrics
```

Capacity-aware policy có thể quan sát queue/capacity state trước khi quyết định.

## Thời gian mô phỏng

Ưu tiên event-driven / chronological processing vì transaction order và queue waiting quan trọng.

### Với Xente
Có thể dùng observed transaction replay làm empirical baseline.

### Với adaptive counterfactual
Fraud events có thể được generated/perturbed nhưng vẫn phải bám scenario-specific distributions.

### Với IEEE-CIS
Cách dựng persistent entity phụ thuộc final data audit vì customer identity kém trực tiếp hơn Xente.

## Một event diễn ra như thế nào?

1. Customer hoặc fraudster tạo transaction.
2. Detection system tạo risk information.
3. Policy chọn action.
4. REVIEW tạo alert trong queue.
5. Analyst capacity xử lý alert.
6. Outcome được ghi nhận.
7. Queue/customer/fraudster state được update.
8. Chuyển sang event tiếp theo.

## Khi nào thật sự gọi là ABM?

ABM framing hợp lý nếu implementation giữ được:
- persistent agent state;
- behavioral heterogeneity;
- feedback từ action sang future behavior;
- interaction qua shared resource như queue.

Nếu bỏ adaptive behavior và chỉ replay score stream cố định qua queue, tên **dynamic/discrete-event policy simulation** có thể chính xác hơn.

## Minimum viable model

### MVP 0
Transaction -> risk -> policy -> queue -> analyst -> metrics.

### MVP 1
Thêm persistent customer state.

### MVP 2
Thêm static fraudster.

### MVP 3
Thêm adaptive fraudster.

### MVP 4
So sánh policy.

### MVP 5
Sensitivity + robustness.

## Giới hạn claim

Chỉ được claim có điều kiện về:
- policy trade-off;
- congestion;
- adaptation stress;
- robustness.

Không claim:
- exact fraudster cognition;
- digital twin;
- production threshold;
- bank-specific staffing.
