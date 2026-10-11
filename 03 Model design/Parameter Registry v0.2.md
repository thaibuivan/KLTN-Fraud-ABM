# Parameter Registry v0.2

## Nguyên tắc

Mục tiêu không phải tìm một “con số đúng tuyệt đối” cho mọi parameter.

Quan trọng hơn là xác định **parameter thuộc loại evidence nào** và có cần sensitivity-test hay không.

| Parameter | Ý nghĩa | Nguồn ban đầu | Vai trò | Ưu tiên sensitivity |
|---|---|---|---|---|
| fraud prevalence | tỷ lệ fraud | dataset | empirical input | thấp-vừa |
| amount distribution | phân bố giá trị GD | dataset | empirical input | thấp |
| temporal distribution | phân bố theo thời gian | dataset | empirical input | vừa |
| customer transaction frequency | mức độ hoạt động | dataset nếu xác định được | state/input | vừa |
| risk threshold | ngưỡng action | experiment | policy variable | cao |
| queue discipline | FIFO / risk-priority | experiment | policy variable | cao |
| analyst capacity | số case xử lý mỗi period | literature/scenario | operational uncertainty | cao |
| review time | thời gian xử lý case | literature/scenario | operational uncertainty | cao |
| analyst accuracy | độ chính xác review | literature/scenario | operational uncertainty | vừa-cao |
| fraudster learning rate alpha | tốc độ học | explicit assumption | behavioral uncertainty | cao |
| exploration epsilon | xác suất thử strategy khác | explicit assumption | behavioral uncertainty | cao |
| strategy-switch mechanism | rule thích nghi | model design | structural uncertainty | cao |
| block tolerance | số block trước dormancy | explicit assumption | behavioral uncertainty | cao |
| dormancy duration | thời gian ngủ đông | explicit assumption | behavioral uncertainty | vừa |
| review cost | chi phí xử lý | literature/scenario | economic uncertainty | vừa |
| false-positive cost | chi phí can thiệp nhầm | literature/scenario | economic uncertainty | cao |
| friction cost | customer inconvenience / abandonment proxy | literature/scenario | economic uncertainty | cao |

## Bốn nhóm parameter

### 1. Empirical parameter
Estimate trực tiếp nếu dataset hỗ trợ.

Ví dụ:
- fraud prevalence;
- amount distribution;
- observable timing;
- channel/product mix.

### 2. Literature-informed operational parameter
Dùng public literature hoặc plausible range.

Ví dụ:
- analyst capacity;
- review time;
- analyst accuracy.

### 3. Policy parameter
Không cần estimate vì chính nó là biến thí nghiệm.

Ví dụ:
- threshold;
- queue rule;
- capacity-aware decision rule.

### 4. Uncertain behavioral assumption
Không được transaction data identify trực tiếp.

Ví dụ:
- fraudster learning rate;
- exploration;
- switching threshold;
- dormancy.

Các parameter này phải được báo cáo minh bạch và sensitivity-test.

## Quy tắc quan trọng

Nếu data không identify được parameter, **không được tạo false precision**.

Hãy ghi rõ:
- assumption;
- plausible range;
- sensitivity result.
