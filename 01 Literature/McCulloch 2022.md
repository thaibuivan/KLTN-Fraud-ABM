# McCulloch 2022

## 1. Thông tin tài liệu
- Tên: *Calibrating Agent-Based Models using Uncertainty Quantification Methods*
- Năm: 2022
- Vai trò: nền phương pháp cho calibration, parameter uncertainty, model discrepancy và stochasticity.

## 2. Bốn nguồn uncertainty

### Parameter uncertainty
Không biết exact value của parameter.

### Model discrepancy
Model luôn đơn giản hóa/thiếu mechanisms của thế giới thật.

### Observation uncertainty
Observed data có thể thiếu, biased hoặc đo lường không hoàn hảo.

### Stochastic uncertainty
Cùng parameter set nhưng random seed khác nhau có thể cho output khác.

## 3. History Matching và ABC
History Matching loại vùng parameter rõ ràng implausible.

ABC phân tích sâu vùng còn plausible và cho posterior distribution thay vì chỉ một best-fit value.

KLTN **không cần** full HM + ABC ngay.

## 4. Bài học áp dụng
- Có data → estimate/calibrate từ real data.
- Không có exact value → literature + plausible range.
- Stochasticity → multiple seeds.
- Uncertain mechanisms → structural sensitivity/competing structures.
- Quan tâm policy ranking có robust trong plausible region hay không.

## 5. Điều không được suy diễn
- Calibration không biến simulation thành bank truth.
- Match empirical pattern không chứng minh mọi behavioral assumption đúng.
- Sensitivity analysis không tự chứng minh external validity.

## 6. Áp dụng hiện tại
Xente ground:
- customer state/history;
- transaction timing;
- amount/category/channel patterns;
- fraud base rate.

Literature/scenario ground:
- analyst capacity;
- review-time;
- queue discipline;
- cost assumptions;
- fraud regime stress.

## 7. Liên kết
- [[Evidence Parameter Matrix]]
- [[Validation Plan v0.1]]
- [[Operational Parameter Grounding v0.1]]

Source:
https://www.jasss.org/25/2/1.html
