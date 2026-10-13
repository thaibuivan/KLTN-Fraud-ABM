# Xente Full Implementation Plan v1.0 — Scenario A

## Vai trò

Xente là **Scenario A core** và là nơi phát triển/freeze shared engine trước.

Hoàn thiện Xente trước về thứ tự coding **không có nghĩa IEEE-CIS là phụ**. Sau khi common interfaces ổn định, chúng được tái sử dụng cho Scenario B.

## Stage 0 — Empirical baseline ✅

Đã có:
- Xente profile/audit;
- past-only customer features;
- chronological split;
- logistic risk model;
- risk-model robustness;
- temporal robustness.

## Stage 1 — Operational queue baseline ✅

Đã có:
- persistent queue;
- FIFO / risk-priority;
- fixed-capacity threshold sensitivity;
- stochastic service;
- variable team capacity;
- starvation/tail waiting;
- verification tests.

## Stage 2 — Shared policy layer ✅

Đã thêm:
- `scripts/fraud_policies.py`
- `tests/test_fraud_policies.py`

Core:
- FixedThresholdPolicy;
- CapacityAwarePolicy.

Extension:
- CostSensitivePolicy.

## Stage 3 — Integrated policy + queue engine ✅ code added

Đã thêm:
- `scripts/simulate_policy_system.py`
- `tests/test_policy_system.py`
- `scripts/run_xente_policy_replay.py`

Còn phải chạy/verify trên local Xente score files.

## Stage 4 — Freeze operational baseline ⏳

Chốt:
- baseline queue discipline;
- review threshold calibration;
- block action treatment;
- Low / Medium / High normalized capacity.

## Stage 5 — Xente-grounded fraud generator ⏳

Legitimate environment:
- replay observed legitimate events.

Fraud counterfactual:
- sample/perturb từ empirical fraud support;
- explicit bounds;
- no unsupported mechanism without assumption label.

## Stage 6 — Static fraudster ⏳

Fixed strategy distribution.

## Stage 7 — Adaptive fraudster ⏳

```text
strategy → fraud event → risk → policy → response → reward → update
```

## Stage 8 — 12 Xente core configurations ⏳

```text
Static / Adaptive
× Fixed / Capacity-aware
× Low / Medium / High
= 12
```

## Stage 9 — Xente sensitivity ⏳

Chạy riêng:
- FIFO/risk-priority;
- degraded score;
- service/capacity stochasticity;
- alpha/epsilon;
- optional cost-sensitive.

## Stage 10 — Freeze common interfaces for IEEE-CIS ⏳

Sau khi Xente chạy ổn:
- common event schema;
- policy API;
- queue API;
- fraudster API;
- metric schema;
- experiment configuration schema.

Đây là hand-off sang [[IEEE-CIS Full Implementation Plan v1.0]].

## Definition of done cho Scenario A

- [ ] integrated replay verified;
- [ ] static full loop;
- [ ] adaptive full loop;
- [ ] 12 configs;
- [ ] sensitivity/convergence;
- [ ] common interfaces frozen;
- [ ] result artifacts reproducible.
