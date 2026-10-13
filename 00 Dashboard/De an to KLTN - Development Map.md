# Từ đề án FinRisk đến khóa luận — Bản đồ phát triển

## Một câu để hiểu mối quan hệ

Khóa luận **không đổi đề tài**. Nó phát triển trực tiếp từ đề án:

> từ một framework policy simulation dựa nhiều vào synthetic assumptions sang một closed-loop dynamic/agent-based simulation có empirical grounding trên **hai transaction environments bổ sung cho nhau: Xente và IEEE-CIS**.

## Đề án đã có

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

Đề án đã có:
- risky actor;
- threshold policies;
- capacity-aware idea;
- cost-sensitive idea;
- analyst capacity;
- operational metrics.

## KLTN nâng cấp gì?

### 1. Empirical grounding
Đề án:
- synthetic stream;
- public data chủ yếu tham khảo phân phối.

KLTN:
- Xente và IEEE-CIS là hai empirical scenarios core;
- observed data dùng cho state, chronology/context, risk model và generator support;
- counterfactual components được tách rõ khỏi observed components.

### 2. Risk scoring
Đề án:
- proxy/rule-based score.

KLTN:
- train/validate riêng risk model theo từng scenario.

### 3. Analyst dynamics
Đề án:
- daily capacity/overflow.

KLTN:
- persistent queue;
- backlog;
- waiting time;
- tail delay;
- variable capacity.

### 4. Risky actor
Đề án:
- fixed/predefined strategy chủ yếu ở mức minh họa.

KLTN:
- static comparator;
- adaptive fraudster;
- response → reward → strategy update qua nhiều vòng.

### 5. Policy experiment
Đề án:
- nhiều threshold labels + capacity-aware/cost-sensitive.

KLTN:
- balanced/sensitive/strict được gom thành Fixed-threshold family;
- Capacity-aware là core alternative;
- Cost-sensitive là extension nếu cost grounding đủ tốt.

## Vì sao hai dataset?

### Xente
Cho customer/history state rõ.

### IEEE-CIS
Cho card/device/identity-rich risk environment.

Hai bộ giải quyết hai mặt khác nhau của cùng framework và giúp kiểm tra xem kết luận có phụ thuộc một dataset cụ thể hay không.

## Core experiment toàn thesis

```text
2 datasets
×
2 fraudster modes
×
2 policies
×
3 capacities
=
24 configurations
```

## Chuỗi phát triển

```text
Freeze shared design
        ↓
Implement full Xente scenario
        ↓
Freeze common interfaces
        ↓
Implement IEEE-CIS adapter/risk/state
        ↓
Run 12 Xente + 12 IEEE
        ↓
Cross-scenario comparison
        ↓
Sensitivity / robustness
        ↓
Methods + Results + Discussion
```

## Nguyên tắc chống scope explosion

- Không merge datasets.
- Không bắt hai scenario có cùng state variables.
- Chỉ giữ cùng policy/queue/adaptation protocol.
- Robustness factors khác chạy riêng, không nhân hết vào core grid.
