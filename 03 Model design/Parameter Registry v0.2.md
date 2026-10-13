# Parameter Registry v0.2 — Two-Scenario Version

## Nguyên tắc

Không tìm một “true parameter vector” cho mọi môi trường.

Mỗi parameter phải có:
- scenario;
- source/evidence type;
- role;
- calibration status;
- sensitivity priority.

## Shared vs scenario-specific

### Scenario-specific empirical parameters
Ước lượng riêng cho Xente và IEEE-CIS:
- fraud prevalence;
- transaction amount distribution;
- temporal/relative-time distribution;
- product/context mix;
- entity/history distributions;
- risk-score distribution/calibration.

### Shared mechanism parameters
Giữ cùng logic để comparison có ý nghĩa:
- fraudster learning rule;
- action space;
- policy functional form;
- queue mechanics;
- metric definitions.

Giá trị cụ thể của policy threshold/capacity có thể normalize theo scenario.

## Registry

| Parameter | Scenario | Nguồn | Loại | Sensitivity |
|---|---|---|---|---|
| fraud prevalence | Xente / IEEE riêng | dataset | empirical | thấp-vừa |
| amount distribution | Xente / IEEE riêng | dataset | empirical | thấp |
| temporal distribution | riêng | dataset | empirical | vừa |
| customer/history frequency | Xente | dataset | empirical | vừa |
| card/device/entity proxy distribution | IEEE | dataset | empirical/proxy | cao |
| risk score / calibration | riêng | trained model | empirical/model | cao |
| review threshold | normalize theo scenario | experiment | policy | cao |
| block threshold | normalize theo scenario | experiment | policy | cao |
| queue discipline | shared experiment | design | structural | cao |
| analyst capacity | normalized load + literature/scenario | operational | uncertain | cao |
| review time | literature/scenario | operational | uncertain | cao |
| analyst accuracy | literature/scenario | operational | uncertain | vừa-cao |
| learning rate alpha | shared rule | assumption | behavioral | cao |
| exploration epsilon | shared rule | assumption | behavioral | cao |
| strategy mapping | scenario-specific | data + design | structural | cao |
| block tolerance | shared/scenario stress | assumption | behavioral | cao |
| dormancy duration | assumption | behavioral | behavioral | vừa |
| review cost | external | literature/scenario | economic | cao |
| false-positive/friction cost | external | literature/scenario | economic | cao |

## Bốn evidence classes

### 1. Empirical
Từ dataset:
- prevalence;
- amount;
- timing;
- context mix;
- history/proxy distributions.

### 2. Literature-informed operational
- analyst capacity/review time;
- analyst accuracy;
- cost ranges nếu dùng.

### 3. Policy variable
- thresholds;
- congestion triggers;
- queue rule.

### 4. Behavioral assumption
- alpha;
- epsilon;
- switching/dormancy.

## Cross-scenario rule

Không ép:
- fraud prevalence bằng nhau;
- amount scale bằng nhau;
- customer/entity state giống nhau.

Chỉ giữ common mechanism khi cần để so policy.

## False precision rule

Nếu parameter không được data identify:
- ghi assumption;
- khai báo range;
- sensitivity-test;
- không mô tả như empirical estimate.
