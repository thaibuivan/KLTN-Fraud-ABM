# Alves et al. 2025 — OpenL2D / FiFAR

## Citation
Alves, J. V. et al. (2025). *A benchmarking framework and dataset for learning to defer in human-AI decision-making*. Scientific Data, 12, 506.

Source:
https://www.nature.com/articles/s41597-025-04664-y

## Why this matters
Đây là nguồn mạnh nhất hiện có trong literature pack cho **human expert capacity constraints** trong fraud-review setting.

Paper tạo:
- 50 synthetic fraud analysts;
- 30K alert-review instances;
- heterogeneous expert decision processes;
- explicit work-capacity constraints;
- validation against high-stakes decision-making literature và một private dataset của real transaction-fraud analysts.

## Capacity mechanism
OpenL2D không giả định một số “cases/day” cố định cho mọi analyst.

Capacity được biểu diễn theo batch/time window:
- `Batch Size`: số case trong window;
- `Deferral Rate`: fraction của batch có thể defer cho expert team;
- `H[b,j]`: số case tối đa expert j có thể xử lý trong batch b.

Hai dạng:
1. **Homogeneous**: mỗi expert cùng capacity.
2. **Variable**: capacity expert j được sample quanh mean
   `mu = Deferral_Rate * Batch_Size / N_experts`,
   với độ biến thiên proportional to `sigma_d * mu`.

### Bài học cho KLTN
Đây hỗ trợ **cơ chế capacity constraint** và **capacity heterogeneity**.

Nó **không cung cấp một con số bank-specific** để ta bê nguyên sang Xente.

Vì vậy core thesis nên:
- dùng pooled/relative capacity trong baseline;
- stress-test capacity thay vì claim exact cases/day;
- chỉ thêm heterogeneous analysts ở structural extension.

## Real analyst validation — giới hạn quan trọng
Paper có private transaction-fraud analyst data, nhưng:
- chỉ một expert prediction per instance;
- missing ground-truth labels;
- không thể dùng để estimate inter/intra-rater agreement đầy đủ;
- không thể dùng để estimate team performance distribution.

Private data chủ yếu giúp kiểm tra **feature/model-score dependence** của real analyst decisions.

### Consequence
Không dùng FiFAR để nói:
- analyst accuracy thực là X%;
- analyst capacity thực là Y cases/day;
- review time thực là Z minutes.

## Strong result relevant to thesis
Paper cho thấy ranking của human-AI assignment methods thay đổi theo:
- expert team available;
- capacity constraints;
- workload distribution.

Đây là precedent rất phù hợp với RQ của KLTN: policy ranking có thể thay đổi dưới operational constraints.

## What to reuse
- capacity matrix concept;
- capacity as scenario variable;
- homogeneous vs variable capacity structural sensitivity;
- robustness across expert availability/workload scenarios.

## What not to reuse
- 50 experts;
- benchmark deferral rate 10/11;
- any FiFAR expert-error parameter as transaction-fraud ground truth.

## Link
- [[Operational Parameter Grounding v0.1]]
- [[Queue and Analyst Service Design v0.1]]
