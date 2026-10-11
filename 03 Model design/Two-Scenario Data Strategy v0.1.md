# Two-Scenario Data Strategy v0.1 — trạng thái sau khi thu gọn scope

## Status

**Xente là core development environment. IEEE-CIS là optional external robustness.**

File này không còn có nghĩa hai dataset bắt buộc phải hoàn thành ngang nhau.

## Vì sao thu gọn?

KLTN đang phát triển trực tiếp từ đề án FinRisk.

Để hoàn thành contribution chính, cần trước hết đóng vòng đầy đủ:

```text
Xente transaction state
→ risk
→ policy
→ queue/analyst
→ outcome
→ adaptive fraudster feedback
```

Nếu chia effort sang hai dataset trước khi vòng này hoàn chỉnh, scope tăng mạnh nhưng RQ chính chưa được trả lời.

## Scenario A — Xente (CORE)

Vai trò:
- empirical transaction chronology;
- repeated CustomerId;
- customer-history state;
- risk-model training/evaluation;
- queue/policy replay;
- empirical grounding cho counterfactual fraud generation.

## Scenario B — IEEE-CIS (OPTIONAL)

Vai trò nếu thời gian cho phép:
- online/card/e-commerce-like robustness environment;
- kiểm tra qualitative policy conclusions có phụ thuộc mạnh vào Xente hay không.

Giới hạn:
- many anonymized features;
- TransactionDT là relative time;
- true persistent customer identity kém rõ hơn Xente.

## Câu hỏi cross-scenario nếu triển khai

> Khi cùng một policy framework được parameterize độc lập ở Xente và IEEE-CIS, qualitative policy conclusions có giữ được không?

Không yêu cầu:
- merge datasets;
- transfer cùng một classifier;
- hoàn thành IEEE để core thesis hợp lệ.

## Quyết định thực thi

Thứ tự:
1. full Xente model;
2. final Xente experiment;
3. Xente sensitivity;
4. final writing draft;
5. chỉ sau đó mới quyết định IEEE-CIS replication.
