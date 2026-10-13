# Two-Scenario Data Strategy v0.1

## Status

**Xente và IEEE-CIS đều là core empirical scenarios.**

Khác nhau ở **vai trò**, không phải mức độ quan trọng.

- Xente: customer/history-rich.
- IEEE-CIS: card/device/identity-rich.

Không merge hai dataset thành một population.

## Scenario A — Xente

Dùng để ground:
- customer identity/history;
- real chronology;
- Value/Amount;
- product/provider/channel;
- customer-centric risk features;
- scenario-specific risk model.

Điểm mạnh:
- agent/state dễ diễn giải;
- repeated behavior rõ.

Điểm yếu:
- fraud sample hiếm;
- Value signal rất mạnh;
- device/card context hạn chế.

## Scenario B — IEEE-CIS

Dùng để ground:
- online/card/e-commerce transaction context;
- TransactionAmt / ProductCD;
- card/device/identity heterogeneity;
- address/email relations;
- count/time-delta/match/rich detector features;
- scenario-specific risk model.

Điểm mạnh:
- richer detection context;
- larger/heterogeneous environment;
- distribution shift hữu ích cho robustness.

Điểm yếu:
- many masked features;
- no true CustomerId;
- relative TransactionDT;
- state phải dùng entity proxies.

## Nguyên tắc chung

Giữ giống nhau:
- policy interface;
- queue/analyst mechanism;
- fraudster update rule;
- capacity normalization;
- outcome definitions;
- experiment protocol.

Cho phép khác nhau:
- agent/entity state;
- feature engineering;
- risk model;
- fraud prevalence;
- transaction/context distributions;
- strategy-to-feature mapping.

## Câu hỏi cross-scenario

> Cùng một fraud-management framework có cho qualitative policy conclusions tương tự khi parameterize độc lập trên Xente và IEEE-CIS hay không?

Nếu giống:
- conclusion robust hơn.

Nếu khác:
- policy effect là environment-dependent.

## Thứ tự triển khai

1. hoàn thiện engine trên Xente;
2. freeze common schema/interfaces;
3. build IEEE-CIS adapter;
4. chạy cùng 12 configurations;
5. compare 12 Xente + 12 IEEE.
