# Validation Plan v1.0 — Two-Scenario Adaptive Policy Model

## Model purpose

Model dùng để **compare và stress-test policy dưới stated scenarios/assumptions** trên:
- Xente;
- IEEE-CIS.

Không dùng để:
- tái tạo chính xác một ngân hàng;
- khuyến nghị production threshold/staffing;
- khẳng định fraudster cognition thật.

## 1. Conceptual validation

Mỗi component phải có:
- link tới RQ;
- evidence type;
- assumption boundary;
- scenario-specific hay shared.

Shared:
- policy logic;
- queue/analyst mechanism;
- adaptive update rule;
- outcome semantics.

Scenario-specific:
- entity/customer state;
- empirical distributions;
- feature engineering;
- risk model;
- strategy-to-feature mapping.

## 2. Input / empirical validation

### Xente
Kiểm tra:
- fraud prevalence;
- Value/Amount;
- real timestamp;
- CustomerId repetition;
- cold-start;
- product/channel/provider;
- drift.

### IEEE-CIS
Kiểm tra:
- fraud prevalence;
- TransactionAmt/ProductCD;
- card/device/identity coverage;
- relative TransactionDT;
- entity/proxy repetition;
- missingness;
- train-test drift;
- masked-feature limitations.

Không coi adaptive parameters là empirical parameters ở bất kỳ dataset nào.

## 3. Risk-model validation

Cho từng scenario:
- chronological split/validation;
- PR-AUC;
- ROC-AUC;
- Brier/calibration;
- temporal/drift checks;
- stronger/degraded specification.

Policy conclusions phải được stress-test dưới ít nhất một degraded score specification.

## 4. Code verification

Đã/đang có:
- no service before arrival;
- equal capacity under same conditions;
- priority không dùng fraud label;
- reproducible stochastic service/capacity;
- fixed service rate across threshold changes;
- policy threshold boundary;
- capacity-aware congestion response;
- APPROVE/BLOCK không vào review queue;
- REVIEW mới vào queue.

Cần đảm bảo cho hai scenario:
- adapter không đổi label/amount/time meaning;
- IEEE relative time giữ đúng ordering;
- Xente real time không bị reorder;
- common engine cho cùng config semantics;
- fraudster update dùng realized response;
- same seed reproduces adaptive path.

## 5. Stochastic uncertainty

Final N seeds dựa trên convergence của:
- successful fraud exposure;
- fraud capture/intercept;
- backlog;
- P95 wait.

Report:
- mean;
- standard deviation;
- percentile interval hoặc CI phù hợp.

## 6. Parameter sensitivity

Operational:
- Low / Medium / High normalized capacity;
- service-time CV;
- team-capacity CV.

Behavioral:
- alpha;
- epsilon;
- optional dormancy.

Policy:
- review/block thresholds;
- congestion trigger/increment.

Scenario-specific:
- fraud generator support/ranges;
- entity-proxy definition cho IEEE;
- customer/history initialization cho Xente.

## 7. Structural sensitivity

- FIFO vs risk-priority;
- Static vs Adaptive;
- full vs degraded score;
- Xente vs IEEE-CIS.

Optional:
- alternate adaptation rule.

## 8. Pattern/output checks

### Xente
- legitimate replay preserves observed chronology/history;
- generated fraud stays in declared empirical support/ranges.

### IEEE-CIS
- relative ordering preserved;
- identity/device/card perturbations stay within declared support;
- masked features không bị gán semantic giả.

Cả hai:
- queue limiting behavior hợp lý;
- policy effect không do accidental capacity re-scaling;
- fraud regime không drift ngoài scenario nếu không được thiết kế.

## 9. Extreme-condition tests

- very high capacity → backlog gần 0;
- near-zero capacity → queue tăng;
- strict threshold → alerts giảm;
- sensitive threshold → alerts tăng;
- alpha = 0 → không có value learning;
- epsilon = 0 → không exploration ngoài tie/init;
- capacity-aware congestion tăng → review selectivity không giảm.

## 10. Cross-scenario validation

Không yêu cầu raw outcomes giống nhau.

Kiểm tra:
- direction của adaptation effect;
- policy gain;
- ranking;
- interaction với capacity.

Phân loại kết luận:
- robust/consistent;
- environment-dependent;
- uncertain.

## 11. Claim rule

Mỗi result phải ghi rõ:
- empirical observation;
- simulation result;
- sensitivity result;
- assumption-dependent interpretation.

Không biến simulation finding thành real-bank claim.
