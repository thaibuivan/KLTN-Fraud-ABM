# AUDIT REPO — file nào còn tác dụng?

## Vì sao repo trông rất nhiều file?

Repo hiện chứa hai giai đoạn nghiên cứu:

### Giai đoạn A — Xente-only operational simulation
Trọng tâm:
- Xente chronological replay;
- risk threshold;
- persistent queue;
- FIFO vs risk-priority;
- analyst capacity;
- robustness.

### Giai đoạn B — hướng hiện tại
Trọng tâm:
- ABM để thử nghiệm policy;
- adaptive fraudster là stress mechanism;
- queue/capacity là operational feedback;
- IEEE-CIS + Xente là hai scenario riêng.

Nguy cơ lớn nhất là đọc nhầm file giai đoạn A và tưởng đó vẫn là research design hiện tại.

## Nhóm 1 — PHẢI GIỮ, đang dùng hiện tại

- `Current Direction - 2026-10-11.md`
- `Research Design v1.0 - Policy Experimentation.md`
- `Conceptual Model v1.0 - Adaptive Policy ABM.md`
- `Adaptive Fraudster Design v0.1.md`
- `Parameter Registry v0.2.md`
- `Two-Scenario Data Strategy v0.1.md`
- `Adaptive Policy Experiment Plan v0.1.md`
- `GVHD Brief - Current Direction 2026-10-11.md`

## Nhóm 2 — PHẢI GIỮ vì có evidence / code thật

### Data và Xente
- `Data Audit.md`
- `Xente Empirical Profile.md`
- `Xente Baseline Risk Model Feasibility.md`

### Queue / capacity / parameter grounding
- `Queue and Analyst Service Design v0.1.md`
- `Operational Parameter Grounding v0.1.md`
- literature notes về uncertainty, capacity và cost-sensitive decision.

### Xente pilot experiments
- `Xente Queue Pilot v0.1.md`
- `Xente Robustness Pack v0.1.md`
- `Xente Alert-rate and Starvation Sensitivity v0.1.md`
- `Xente Variable Team Capacity Sensitivity v0.1.md`

Đây không phải “rác từ hướng cũ”. Chúng là phần empirical/operational groundwork có thể tái sử dụng.

## Nhóm 3 — GIỮ TẠM, sau này gộp/viết lại

### Evidence Parameter Matrix
Có giá trị nhưng trùng một phần với Parameter Registry.

Sau này nên đổi thành:
**Xente Parameter Evidence**.

### Validation Plan v0.1
Nền validation tốt nhưng thiếu adaptive fraudster + IEEE-CIS.

Sau này nâng thành v1.0.

### Xente Baseline Implementation Plan
Có tác dụng như implementation plan cho Xente scenario, nhưng wording cũ đang coi Xente là toàn bộ core.

Sau này đổi tên/viết lại thành:
**Xente Scenario Implementation Plan**.

## Nhóm 4 — HẾT VAI TRÒ ĐỊNH HƯỚNG

- `Research Design v0.2.md`
- `Candidate Core Specification v0.3.md`
- `Core Experiment Grid v0.1.md`
- `Conceptual Model v0.2.md`
- `GVHD Update - Xente Queue Milestone.md`
- `Methodology Skeleton v0.1.md`
- `Results and Discussion Outline v0.1.md`

Không phải các file này “sai”. Chúng chỉ thuộc phiên bản scope cũ.

Sau khi GVHD xác nhận hướng mới, nên chuyển chúng vào:

`99 Archive/Previous Xente-only direction/`

## Nhóm 5 — CHỈ ĐỂ TRUY LỊCH SỬ

- `Legacy Project Audit - FinRisk.md`
- `Legacy Migration Map.md`
- `Prototype-to-Thesis Gap.md`

Sau này nên chuyển sang:

`99 Archive/Legacy FinRisk/`

## Code nào vẫn cần?

Giữ toàn bộ code Xente/queue vì nó là subsystem có giá trị.

Giữ adaptive fraudster code vì đây là prototype cho hướng mới.

Đặc biệt:
`run_adaptive_vs_static.py` hiện chỉ là **smoke test synthetic**, không được dùng làm empirical result.

## Kết luận

Repo nên được hiểu theo ba tầng:

```text
CURRENT DESIGN
    ↓
REUSABLE EVIDENCE / MODULES
    ↓
ARCHIVED PREVIOUS FRAMING
```

Sau khi gặp GVHD và chốt scope, mới nên move file cũ vào Archive. Chưa cần xóa vĩnh viễn.
