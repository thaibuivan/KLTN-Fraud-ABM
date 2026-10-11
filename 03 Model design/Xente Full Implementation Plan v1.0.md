# Xente Full Implementation Plan v1.0

## Mục tiêu

Hoàn thành core KLTN trên Xente trước khi mở rộng dataset khác.

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
- service-time stochasticity;
- variable team capacity;
- starvation/tail waiting;
- verification tests.

## Stage 2 — Shared policy layer ✅ code added

Đã thêm:
- `scripts/fraud_policies.py`
- `tests/test_fraud_policies.py`

Policy interface:
- APPROVE
- REVIEW
- BLOCK

Implement:
- FixedThresholdPolicy;
- CapacityAwarePolicy;
- CostSensitivePolicy extension.

## Stage 3 — Integrated policy + queue engine ✅ code added

Đã thêm:
- `scripts/simulate_policy_system.py`
- `tests/test_policy_system.py`
- `scripts/run_xente_policy_replay.py`

Mục tiêu:
- policy quan sát queue state tại đúng thời điểm;
- REVIEW mới vào queue;
- APPROVE/BLOCK không vào queue;
- fixed staffing được giữ khi so policy.

### Việc phải chạy local
Dùng validation/test score files đã sinh từ Xente:

```bash
python scripts/run_xente_policy_replay.py \
  --validation-scores outputs/local/xente_baseline/validation_scores.csv \
  --test-scores outputs/local/xente_baseline/test_scores.csv
```

Đây là **pre-adaptation pilot**, chưa phải final result.

## Stage 4 — Freeze baseline operational choices ⏳

Sau pilot phải chốt:
- baseline queue discipline: FIFO hay risk-priority;
- review target / threshold calibration rule;
- block có bật trong core hay để threshold = 1.0;
- low/medium/high capacity definition.

Nguyên tắc:
- policy comparison không được tự thay staffing;
- capacity levels phải dùng chung reference.

## Stage 5 — Empirical fraud generator ⏳

Mục tiêu:
tạo fraud counterfactual nhưng vẫn bám Xente.

Không sinh toàn bộ world từ đầu.

### Baseline design
Legitimate environment:
- replay observed legitimate Xente events.

Fraud generator:
- sample/perturb từ observed fraud support;
- giữ explicit bounds cho Value/context/timing;
- không tạo mechanism mà Xente không support nếu không gắn assumption label.

Output phải có cùng feature interface để risk engine chấm score.

## Stage 6 — Static fraudster integration ⏳

Static fraudster:
- fixed strategy distribution;
- không update theo response.

Mục tiêu:
- tạo comparator cho RQ1;
- đảm bảo full event loop chạy trước khi thêm adaptation.

## Stage 7 — Adaptive fraudster integration ⏳

Nối:
```text
strategy
→ fraud transaction
→ risk model
→ policy response
→ reward
→ strategy update
```

Parameter:
- learning rate alpha;
- exploration epsilon;
- dormancy rule.

Tất cả là explicit assumptions/sensitivity parameters nếu không có independent empirical evidence.

## Stage 8 — Core 12 configurations ⏳

```text
Static / Adaptive
×
Fixed / Capacity-aware
×
Low / Medium / High capacity
```

Pilot:
- 20–30 seeds.

Final:
- chọn N theo convergence.

## Stage 9 — Robustness ⏳

Chạy riêng:
- FIFO vs risk-priority;
- degraded risk score;
- service randomness;
- team-capacity randomness;
- alpha/epsilon sensitivity;
- optional cost-sensitive.

## Stage 10 — Final outputs ⏳

Xuất reproducible:
- configuration table;
- seed-level results;
- aggregated results;
- main figures;
- robustness appendix;
- final parameter registry snapshot.

## Definition of done

Core KLTN kỹ thuật hoàn thành khi:
- [ ] integrated replay chạy local;
- [ ] static fraudster full loop;
- [ ] adaptive fraudster full loop;
- [ ] 12 configurations chạy;
- [ ] convergence/sensitivity xong;
- [ ] verification tests pass;
- [ ] result artifacts reproducible;
- [ ] Methods và Results map 1-1 với code/experiment.
