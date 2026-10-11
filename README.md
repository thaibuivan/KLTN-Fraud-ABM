# KLTN — Thử nghiệm chính sách quản lý gian lận bằng ABM

Kho này phát triển trực tiếp từ đề án **FinRisk Decision Simulation**.

## Một câu để nhớ

> Phát triển framework transaction-risk decisioning của đề án thành một dynamic policy-simulation / ABM có empirical grounding tốt hơn, persistent analyst queue và adaptive fraudster.

## Hướng nghiên cứu hiện tại

- **Mục tiêu:** thử nghiệm / stress-test fraud-management policy.
- **ABM / dynamic simulation:** công cụ nghiên cứu.
- **Adaptive fraudster:** phát triển risky actor của đề án thành cơ chế feedback qua nhiều vòng.
- **Persistent queue + analyst capacity:** phát triển daily overflow thành operational dynamics.
- **Risk model:** thành phần tạo risk score, không phải contribution chính.
- **Xente:** empirical development environment chính.
- **IEEE-CIS:** optional external robustness nếu core Xente hoàn thành.

## Bắt đầu đọc từ đâu?

1. `00 Dashboard/READING ORDER.md`
2. `00 Dashboard/De an to KLTN - Development Map.md`
3. `00 Dashboard/Current Direction - 2026-10-11.md`
4. `03 Model design/Research Design v1.1 - Develop from FinRisk Proposal.md`
5. `03 Model design/Xente Full Model Specification v1.0.md`
6. `05 Experiments/Final Core Experiment Grid v1.0.md`

## Core experiment

```text
Static / Adaptive fraudster
×
Fixed / Capacity-aware policy
×
Low / Medium / High analyst capacity
=
12 configurations
```

Cost-sensitive policy là extension nếu cost assumptions đủ defensible.

FIFO vs risk-priority là structural robustness, không nhân vào toàn bộ core grid.

## Những gì đã làm được

Xente:
- data audit/profile;
- leakage-safe customer-history features;
- chronological logistic risk baseline;
- temporal / score-model robustness;
- persistent alert queue;
- FIFO vs risk-priority;
- fixed-capacity threshold sensitivity;
- stochastic service;
- variable team capacity;
- starvation/tail waiting diagnostics.

Adaptive fraudster:
- conceptual specification;
- heuristic/bandit-style prototype;
- unit tests;
- synthetic smoke runner.

Policy layer:
- shared policy interface;
- fixed-threshold policy;
- capacity-aware policy;
- cost-sensitive extension;
- policy unit tests đã được thêm vào repo.

## Phần còn thiếu để hoàn thành core KLTN

1. tích hợp policy interface vào event-driven Xente simulator;
2. tích hợp static fraudster với empirical fraud generator;
3. nối adaptive feedback vào Xente environment;
4. chạy 12 core configurations;
5. behavioral sensitivity + convergence;
6. final tables/figures;
7. Methods / Results / Discussion.

## Git

- `main`: stable.
- `chatgpt-draft`: active research branch.

## Claim boundary

Không claim:
- digital twin;
- production threshold;
- bank staffing recommendation;
- exact fraudster cognition;
- universal best policy.

Kết luận phải gắn với scenario, assumptions và parameter ranges đã thử.
