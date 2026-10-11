# Results and Discussion Outline v1.0

## 1. Empirical Xente environment

Report:
- data size / fraud rarity;
- customer repetition;
- cold-start;
- Value/context signal;
- temporal drift.

Mục đích:
chứng minh empirical environment được hiểu trước khi simulation.

## 2. Risk-model baseline

Report:
- chronological validation/test;
- PR-AUC / ROC-AUC / Brier;
- temporal robustness;
- full vs degraded score specifications.

Discussion:
- classifier performance không ổn định tuyệt đối;
- Xente Value signal mạnh;
- vì vậy policy conclusions phải stress-test score quality.

## 3. Operational groundwork

Tóm tắt pilot đã có:
- threshold/load;
- capacity;
- FIFO vs risk-priority;
- stochastic service;
- variable capacity;
- starvation.

Key interpretation:
> same score stream + same capacity + different operational mechanism → different system outcome.

Đây là nền cho full model, không phải final adaptive result.

## 4. Integrated policy replay

So:
- Fixed;
- Capacity-aware;
trên cùng historical score stream trước adaptation.

Report:
- review rate;
- backlog;
- waiting time;
- fraud interception;
- legitimate interventions.

Mục đích:
verify policy mechanics trước khi thêm adversary adaptation.

## 5. RQ1 — Static vs Adaptive Fraudster

Giữ policy/capacity cố định.

Report:
- successful fraud value;
- intercepted fraud;
- strategy shares over time;
- risk-score distribution shift;
- alert load shift.

Discussion:
- adaptation có làm historical/static policy evaluation lạc quan không?
- effect phụ thuộc capacity/policy thế nào?

## 6. RQ2 — Fixed vs Capacity-aware

Giữ fraudster mode và capacity cố định.

Report:
- fraud outcome;
- false-positive/intervention;
- queue outcome.

Không ép một single winner.

Dùng trade-off / Pareto interpretation nếu phù hợp.

## 7. RQ3 — Capacity interaction

Low / Medium / High.

Question:
- policy ranking có đổi khi capacity khan hiếm?
- adaptation effect có lớn hơn khi congestion cao?

## 8. Main interaction

Kiểm tra interaction quan trọng:

> Adaptive fraudster × Capacity-aware policy × Low capacity.

Nếu capacity-aware chỉ hữu ích trong overload, đó là conditional policy insight chứ không phải universal optimum.

## 9. Behavioral sensitivity

Alpha / epsilon / dormancy.

Report:
- policy ranking stability;
- outcome ranges;
- parameter regions làm conclusion đổi.

## 10. Structural robustness

- FIFO vs risk-priority;
- degraded score model;
- stochastic service;
- variable team capacity.

## 11. Optional cost-sensitive extension

Chỉ report nếu cost assumptions đủ rõ.

Không dùng một bộ arbitrary cost để tạo headline conclusion.

## 12. Limitations

Ít nhất:
- Xente-specific environment;
- observed labels/history không identify fraud cognition;
- analyst parameters partly scenario/literature-based;
- adaptive generator is counterfactual;
- no claim of real-bank external validity.

## 13. Final discussion

Trả lời trực tiếp main RQ:
- policy performance là dynamic/system-level;
- adaptive behavior và limited review resources có thể thay đổi policy outcome;
- robustness quan trọng hơn một point-estimate optimum.
