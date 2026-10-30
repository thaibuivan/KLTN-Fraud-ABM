# THỨ TỰ ĐỌC REPO — giai đoạn hoàn thiện KLTN

Không đọc repo theo folder. Đọc theo research pipeline.

## 1. Hiểu KLTN phát triển từ đề án

1. [[De an to KLTN - Development Map]]
2. [[Research Design v1.1 - Develop from FinRisk Proposal]]
3. [[Shared Two-Scenario Architecture v1.0]]

Sau đó phải trả lời được:
- KLTN giữ gì từ đề án?
- nâng cấp gì?
- vì sao cần cả Xente và IEEE-CIS?
- phần nào dùng chung, phần nào scenario-specific?

## 2. Hiểu hai scenario

### Xente
4. [[Xente Full Model Specification v1.0]]
5. [[Xente Full Implementation Plan v1.0]]
6. [[Xente Empirical Profile]]

### IEEE-CIS
7. [[IEEE-CIS Full Implementation Plan v1.0]]
8. đọc notebook EDA IEEE-CIS trong Library / working files khi cần đối chiếu chi tiết.

## 3. Hiểu mechanism chung

9. [[Parameter Registry v0.2]]
10. [[Adaptive Fraudster Design v0.1]]
11. [[Queue and Analyst Service Design v0.1]]
12. [[Validation Plan v1.0]]

## 4. Hiểu experiment cuối

13. [[Final Core Experiment Grid v1.0]]
14. [[Cross-Scenario Comparison Plan v1.0]]

Core:

```text
Xente / IEEE-CIS
× Static / Adaptive
× Fixed / Capacity-aware
× Low / Medium / High capacity
= 24 configurations
```

## 5. Xente groundwork đã hoàn thành

Đọc sau khi hiểu model:
- [[Xente Queue Pilot v0.1]]
- [[Xente Robustness Pack v0.1]]
- [[Xente Alert-rate and Starvation Sensitivity v0.1]]
- [[Xente Variable Team Capacity Sensitivity v0.1]]

## 6. Code pipeline

```text
Scenario-specific preprocessing
        ↓
Scenario-specific risk score
        ↓
common policy interface
        ↓
common policy/queue engine
        ↓
static/adaptive fraudster
        ↓
scenario runner
        ↓
cross-scenario aggregator
```

## File cũ không dùng làm source of truth

- [[Research Design v0.2]]
- [[Research Design v1.0 - Policy Experimentation]]
- [[Candidate Core Specification v0.3]]
- [[Core Experiment Grid v0.1]]
- [[Conceptual Model v0.2]]
- [[Validation Plan v0.1]]
- [[Methodology Skeleton v0.1]]
- [[Results and Discussion Outline v0.1]]
