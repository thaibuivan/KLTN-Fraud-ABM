# Validation Plan v1.0 — Full Xente Adaptive Policy Model

## Model purpose

Model dùng để **compare và stress-test policy dưới stated scenarios/assumptions**.

Không dùng để:
- dự báo chính xác một ngân hàng cụ thể;
- khuyến nghị production threshold;
- khẳng định fraudster cognition thật.

## 1. Conceptual validation

Mỗi component phải có:
- link tới RQ;
- evidence type;
- assumption boundary.

Components:
- customer state → Xente repeated history;
- risk score → empirical model;
- queue/capacity → literature + operational simulation;
- fraudster adaptation → explicit behavioral mechanism + sensitivity;
- policy rules → experimental treatments.

## 2. Input/empirical validation

Đã có trên Xente:
- fraud prevalence;
- Value/Amount distribution;
- timestamp/ordering;
- customer repetition;
- cold-start;
- product/channel/provider distribution;
- chronological risk-model evaluation.

Không coi adaptive parameters là empirical Xente parameters.

## 3. Risk-model validation

Giữ:
- chronological split;
- PR-AUC / ROC-AUC / Brier;
- temporal expanding-window checks;
- seen vs unseen customers;
- weaker score-model specification.

Policy conclusions phải được kiểm tra dưới ít nhất một degraded score model.

## 4. Code verification

Đã có queue tests:
- no service before arrival;
- equal capacity across queue disciplines;
- no use of FraudResult for priority;
- reproducible stochastic service;
- fixed service rate across thresholds;
- reproducible variable capacity.

Cần thêm:
- policy threshold boundary tests;
- capacity-aware threshold reacts monotonically to congestion;
- queue state passed to policy uses only current/past state;
- blocked transaction never enters review queue;
- approved transaction never enters review queue;
- fraudster reward/update uses realized system response;
- identical seed reproduces adaptive path.

## 5. Stochastic uncertainty

Báo cáo:
- mean;
- standard deviation;
- percentile interval hoặc CI phù hợp.

Final N seeds dựa trên convergence của:
- successful fraud value;
- fraud capture;
- backlog;
- P95 waiting time.

## 6. Parameter sensitivity

### Operational
- low / medium / high capacity;
- service-time CV;
- team-capacity CV.

### Fraudster behavior
- learning rate alpha;
- exploration epsilon;
- optional dormancy assumptions.

### Policy
- fixed review threshold;
- block threshold;
- congestion trigger / threshold increment.

## 7. Structural sensitivity

Ít nhất:
- FIFO vs risk-priority;
- static vs adaptive;
- full vs degraded risk score.

Optional:
- alternate adaptation rule nếu thời gian cho phép.

## 8. Pattern/output checks

Model không cần match một ngân hàng thật.

Nhưng phải kiểm tra:
- legitimate replay preserves observed Xente chronology;
- synthetic/counterfactual fraud amount/context nằm trong declared support/ranges;
- fraud prevalence/exposure không tự drift ngoài scenario mà không được giải thích;
- queue/backlog mechanics có expected limiting behavior.

## 9. Extreme-condition tests

Ví dụ:
- infinite/high capacity → backlog gần 0;
- zero/near-zero review capacity → queue tăng;
- threshold cực strict → alert giảm;
- threshold cực sensitive → alert tăng;
- adaptive learning rate 0 → gần static-value-update behavior;
- epsilon 0 → no exploration ngoài tie/initialization rule.

## 10. Claim rule

Mỗi result phải được gắn nhãn:
- empirical observation;
- simulation result;
- sensitivity result;
- assumption-dependent interpretation.

Không biến một simulation finding thành real-bank claim.
