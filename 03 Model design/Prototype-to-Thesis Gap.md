# Prototype-to-Thesis Gap

## Gap 1 — Policy simulation → justified ABM/dynamic model
Legacy code là procedural simulation hữu ích, nhưng KLTN cần xác định:
- persistent state;
- state update qua timestep;
- interaction/feedback;
- persistent queue/backlog;
- heterogeneity nào thực sự ảnh hưởng outcome.

Nếu cuối cùng chỉ còn `transaction -> score -> threshold -> cost`, nên gọi đúng là policy simulation/microsimulation.

## Gap 2 — Synthetic assumptions → evidence provenance
Mỗi parameter phải có provenance:
- empirical;
- literature-informed;
- expert-informed;
- explicit assumption.

Không dùng con số legacy chỉ vì nó đã có trong code.

## Gap 3 — Few scenarios → uncertainty-aware experiments
Cần:
- repeated seeds;
- parameter sensitivity;
- structural sensitivity có chọn lọc;
- distribution/interval của outcomes.

## Gap 4 — Static capacity → queue dynamics
Legacy đã có daily capacity/overflow. Thesis cần kiểm tra liệu persistent waiting time/backlog có thay policy conclusions không.

## Gap 5 — Exploratory results → disciplined claims
Không nói "policy X tốt nhất" tuyệt đối.

Nên nói:
> Trong scenarios, parameter ranges và structures đã đánh giá, policy X tạo trade-off Y so với policy Z.

## Thesis-ready baseline checklist
- [ ] Main RQ chốt.
- [ ] Primary dataset chốt.
- [ ] Core states/rules có evidence hoặc explicit assumptions.
- [ ] Queue/backlog chạy đúng.
- [ ] Cost/outcome không double-count.
- [ ] Repeated seeds ổn định.
- [ ] Có 2–3 policies.
- [ ] Có sensitivity plan.
