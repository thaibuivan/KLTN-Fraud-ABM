# Chiến lược dữ liệu hai scenario v0.1

## Nguyên tắc

Dùng **một conceptual framework chung**, nhưng parameterize các empirical environment riêng.

Không merge IEEE-CIS và Xente thành một “ngân hàng tổng hợp”.

## Scenario A — IEEE-CIS Fraud Detection

Vai trò:
- online/card/e-commerce environment;
- transaction amount / timing;
- fraud labels;
- card/device/identity context;
- train scenario-specific risk model.

Giới hạn:
- nhiều feature bị anonymized;
- TransactionDT là relative time;
- không có true customer identifier rõ ràng;
- không được diễn giải hidden variables như hành vi thật nếu không có evidence.

## Scenario B — Xente Fraud Detection

Vai trò:
- mobile/payment/e-commerce environment;
- Amount/Value;
- product/category/channel/provider;
- fraud labels;
- customer repetition;
- scenario-specific risk model.

Permission:
Zindi đã xác nhận cho phép dùng cho thesis với attribution và acknowledgement.

## Câu hỏi cross-scenario

Không yêu cầu một classifier duy nhất transfer trực tiếp giữa hai dataset.

Câu hỏi đúng hơn là:

> Khi cùng một policy-experimentation framework được parameterize độc lập trên hai môi trường khác nhau, các kết luận system-level có còn tương tự/robust không?

## Dataset ground được gì?

Có thể empirical:
- fraud prevalence;
- amount distribution;
- observable temporal/channel patterns;
- scenario-specific risk score;
- một số customer/history state nếu identifier cho phép.

Không được data identify trực tiếp:
- analyst capacity;
- analyst review time;
- analyst accuracy;
- false-positive/friction cost;
- fraudster learning rate;
- fraudster cognition/strategy-switch rule.

Những phần này phải dựa vào literature, plausible ranges hoặc explicit assumptions.

## Dataset khác

Nedbank và AMLSim/Libra hiện không phải core dependency.

Chỉ mở rộng sau khi hai scenario chính đã hoàn thành và scope cho phép.
