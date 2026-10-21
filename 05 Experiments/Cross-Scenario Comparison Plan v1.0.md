# Cross-Scenario Comparison Plan v1.0

## Core design toàn khóa luận

```text
2 datasets
×
2 fraudster modes
×
2 policies
×
3 capacity levels
=
24 configurations
```

Datasets:
- Xente
- IEEE-CIS

Fraudster:
- Static
- Adaptive

Policy:
- Fixed-threshold
- Capacity-aware

Capacity:
- Low
- Medium
- High

## Không hiểu 24 configuration là 24 model

Chỉ có:
- một shared system architecture;
- hai scenario adapters/parameterizations;
- cùng experiment protocol.

## Cross-scenario outcomes

### 1. Adaptation penalty

Trong mỗi dataset/policy/capacity:

```text
Adaptive - Static
```

đối với:
- successful fraud exposure;
- fraud capture;
- alert load;
- backlog;
- P95 waiting.

### 2. Capacity-aware policy gain

Trong mỗi dataset/fraudster/capacity:

```text
Capacity-aware - Fixed
```

### 3. Capacity interaction

Kiểm tra policy gain ở:
- Low;
- Medium;
- High.

### 4. Cross-scenario consistency

Phân loại conclusion:

- **Consistent:** cùng direction/ranking ở cả hai.
- **Environment-dependent:** direction/ranking khác nhau.
- **Weak/uncertain:** interval overlap lớn hoặc seed variability cao.

## Reporting

Bảng chính:

| Dataset | Fraudster | Capacity | Fixed | Capacity-aware | Relative effect |
|---|---|---|---:|---:|---:|

Figure chính có thể dùng:
- policy effect plot theo capacity, facet theo dataset;
- adaptation penalty plot;
- backlog/waiting trade-off plot.

## Không nên làm

Không:
- pool raw datasets;
- train một classifier chung chỉ để ép symmetry;
- đồng nhất fraud prevalence;
- gọi IEEE entity proxy là true customer;
- so raw monetary exposure trực tiếp mà không ghi rõ scale khác nhau.

## Robustness ngoài 24 core configurations

Chạy riêng:
- FIFO vs risk-priority;
- degraded score quality;
- stochastic service;
- variable team capacity;
- alpha/epsilon sensitivity;
- optional cost-sensitive policy.

Cost-sensitive nếu thêm vào cả hai dataset:

```text
2 × 2 × 3 × 3 = 36 configurations
```

nhưng đây là extension, không phải core requirement.
