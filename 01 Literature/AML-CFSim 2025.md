# AML-CFSim 2025

## 1. Thông tin tài liệu
- Tên: *AML-CFSim: An agent-based simulation model for anti-money laundering from cyber fraud crimes*
- Năm: 2025
- Chủ đề: Mô phỏng quá trình rửa tiền phát sinh từ cyber fraud bằng ABM.
- Vai trò đối với KLTN: paper nền tảng để học cách xây fraud-related ABM có empirical grounding, validation và policy experimentation.

## 2. Vấn đề nghiên cứu
Paper nghiên cứu quá trình tiền thu được từ cyber fraud được chuyển qua mạng lưới tài khoản và rửa tiền như thế nào, đồng thời đánh giá liệu các chính sách của ngân hàng và cảnh sát có thể làm gián đoạn quá trình này hay không.

Điểm quan trọng:
> Giá trị chính của ABM trong paper nằm ở **policy experimentation**, không phải prediction.

## 3. Tác tử và state
Tác tử chính là **bank-account agents**, không phải mặc định là con người.

Mỗi account có:
- balance;
- active/suspended state;
- behavioral rules;
- interactions với transfer network và supervisory mechanisms.

Bài học:
Agent có thể là một entity có state, rules, persistence và interaction; không cần gắn nhãn “agent” cho mọi module.

## 4. Empirical grounding
Paper dùng real cyber-fraud cases để identify patterns rồi abstract thành mechanisms.

Nguồn parameter gồm:
1. empirical estimation;
2. expert-informed values;
3. theory/regulatory-informed rules;
4. explicit modeling assumptions.

Đây là framework grounding mà KLTN nên giữ.

## 5. Validation
Paper dùng nhiều lớp:
- so sánh với real cases;
- repeated simulation;
- expert validation;
- external cross-validation;
- sensitivity analysis.

Bài học:
Validation không phải “output nhìn hợp lý”.

## 6. Điều áp dụng cho KLTN
- ABM như policy-testing laboratory.
- Behavioral rules phải có grounding.
- Parameter provenance phải minh bạch.
- Unknown parameters nên dùng plausible ranges.
- Chạy multiple seeds.
- Kết luận chỉ trong phạm vi assumptions/scenarios.

## 7. Điều không được copy trực tiếp
- Không bê nguyên account-pool size, transfer tiers, tracing probability, fee hay supervisory policy sang transaction fraud.
- Không mặc định bank account phải là agent trong KLTN.
- Không gọi configuration “optimal” ngoài tập scenarios đã thử.

## 8. Liên kết
- [[Evidence Parameter Matrix]]
- [[Validation Plan v0.1]]
- [[McCulloch 2022]]

Source:
https://www.sciencedirect.com/science/article/pii/S0957417425016161
