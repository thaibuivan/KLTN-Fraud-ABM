# Results and Discussion Outline v1.0

## 1. Empirical environments

### 1.1 Xente
Report:
- fraud rarity;
- customer repetition;
- cold-start;
- Value/context signal;
- temporal drift.

### 1.2 IEEE-CIS
Report:
- fraud prevalence;
- transaction amount/product;
- card/device/identity coverage;
- entity/proxy repetition;
- missingness/drift;
- feature interpretability limits.

### 1.3 Vì sao hai dataset bổ sung nhau
Xente:
- customer/history-rich.

IEEE-CIS:
- identity/device-risk-context-rich.

## 2. Scenario-specific risk models

Mỗi dataset:
- chronological validation;
- PR-AUC / ROC-AUC / calibration;
- drift;
- degraded-score robustness.

Không so classifier như một competition.

## 3. Operational groundwork

Tóm tắt Xente pilot đã có:
- threshold/load;
- capacity;
- FIFO vs risk-priority;
- service/capacity stochasticity;
- starvation.

Mục đích:
justify persistent operational layer.

## 4. Integrated pre-adaptation replay

Trong từng scenario:
- Fixed;
- Capacity-aware;
- same normalized capacity protocol.

Mục đích:
verify policy mechanics trước adaptive loop.

## 5. RQ1 — Static vs Adaptive

Cho Xente và IEEE:
- successful fraud exposure;
- capture/interception;
- strategy shares;
- score distribution shift;
- alert/load shift.

Sau đó so adaptation penalty giữa scenarios.

## 6. RQ2 — Fixed vs Capacity-aware

Trong mỗi scenario:
- fraud outcome;
- intervention;
- backlog/wait.

Sau đó so policy gain giữa scenarios.

## 7. RQ3 — Capacity interaction

Low / Medium / High.

Question:
- policy ranking đổi không?
- adaptive penalty tăng khi congestion tăng không?

## 8. RQ4 — Cross-scenario robustness

Phân loại:
- consistent;
- environment-dependent;
- weak/uncertain.

Không yêu cầu cùng một winner trong cả hai datasets.

## 9. Main interaction discussion

```text
Dataset × Fraudster mode × Policy × Capacity
```

Tập trung vào effect contrasts, không cần biến thesis thành bài factorial statistics thuần túy.

## 10. Behavioral sensitivity

- alpha;
- epsilon;
- dormancy nếu giữ.

## 11. Structural robustness

- FIFO vs risk-priority;
- degraded score;
- stochastic service;
- variable capacity.

## 12. Optional cost-sensitive extension

Chỉ report nếu cost assumptions đủ defensible.

## 13. Limitations

- Xente-specific amount signal;
- IEEE masked features / entity proxy;
- no observed fraud cognition in either dataset;
- analyst parameters external/scenario-based;
- counterfactual generator assumptions;
- no real-bank external validity claim.

## 14. Final discussion

Trả lời:
1. adaptation làm policy evaluation thay đổi ra sao?
2. capacity-aware có ích trong điều kiện nào?
3. analyst scarcity thay đổi ranking ra sao?
4. effect nào robust giữa Xente và IEEE, effect nào environment-dependent?
