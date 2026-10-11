# THỨ TỰ ĐỌC REPO — đọc ít nhưng đúng thứ tự

Mục tiêu của file này là giúp bạn **không bị loạn** khi repo có nhiều file do các vòng làm việc trước tạo ra.

## Nếu chỉ có 10–15 phút

Chỉ đọc 4 file:

1. [[Current Direction - 2026-10-11]]
2. [[Research Design v1.0 - Policy Experimentation]]
3. [[Conceptual Model v1.0 - Adaptive Policy ABM]]
4. [[GVHD Brief - Current Direction 2026-10-11]]

Đọc xong 4 file này phải tự trả lời được:

- Tôi nghiên cứu vấn đề gì?
- Vì sao dùng ABM?
- Data nào dùng?
- Fraudster thích nghi ở đâu?
- Policy nào được thử?
- Sản phẩm cuối là gì?

## Khi đã hiểu hướng, đọc methodology

Theo thứ tự:

1. [[Two-Scenario Data Strategy v0.1]]
2. [[Parameter Registry v0.2]]
3. [[Adaptive Fraudster Design v0.1]]
4. [[Queue and Analyst Service Design v0.1]]
5. [[Operational Parameter Grounding v0.1]]
6. [[Validation Plan v0.1]]

Mục tiêu là hiểu:
- cái gì lấy được từ data;
- cái gì phải lấy từ literature;
- cái gì chỉ là assumption;
- cái gì chính là biến policy để thử nghiệm.

## Sau đó mới đọc những gì đã làm thật trên Xente

Theo thứ tự:

1. [[Xente Empirical Profile]]
2. [[Xente Baseline Risk Model Feasibility]]
3. [[Xente Queue Pilot v0.1]]
4. [[Xente Robustness Pack v0.1]]
5. [[Xente Alert-rate and Starvation Sensitivity v0.1]]
6. [[Xente Variable Team Capacity Sensitivity v0.1]]

Đây là **pilot/groundwork cho Xente scenario**, không phải full result của adaptive-ABM hiện tại.

## Đọc code theo pipeline

```text
profile_xente.py
    ↓
build_xente_features.py
    ↓
train_xente_baseline.py
    ↓
simulate_alert_queue.py
    ↓
adaptive_fraudster.py
    ↓
run_adaptive_vs_static.py
```

Mỗi file chỉ cần trả lời bốn câu:
- Input là gì?
- Nó xử lý gì?
- Output là gì?
- Assumption quan trọng nhất là gì?

Không cần thuộc từng dòng code.

## File KHÔNG nên đọc đầu tiên

Các file sau phản ánh hướng cũ Xente-only và đã bị superseded về framing:

- [[Research Design v0.2]]
- [[Candidate Core Specification v0.3]]
- [[Core Experiment Grid v0.1]]
- [[Conceptual Model v0.2]]
- [[GVHD Update - Xente Queue Milestone]]
- [[Methodology Skeleton v0.1]]
- [[Results and Discussion Outline v0.1]]

Chúng vẫn hữu ích để truy lịch sử hoặc lấy lại mechanism, nhưng **không dùng để học hướng hiện tại**.

## File lịch sử

- [[Legacy Project Audit - FinRisk]]
- [[Legacy Migration Map]]
- [[Prototype-to-Thesis Gap]]

Chỉ đọc khi muốn biết dự án đi từ prototype cũ tới KLTN hiện tại như thế nào.
