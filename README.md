# KLTN — Thử nghiệm chính sách quản lý gian lận bằng ABM

Kho này phát triển trực tiếp từ đề án **FinRisk Decision Simulation**.

## Một câu để nhớ

> Phát triển framework transaction-risk decisioning của đề án thành một dynamic policy-simulation / ABM có empirical grounding tốt hơn, persistent analyst queue và adaptive fraudster, được kiểm tra trên **hai empirical scenarios bổ sung cho nhau: Xente và IEEE-CIS**.

## Hai scenario core

### Scenario A — Xente
Mạnh ở:
- CustomerId rõ;
- repeated customer history;
- timestamp thực;
- product/provider/channel dễ diễn giải;
- phù hợp xây persistent customer state.

### Scenario B — IEEE-CIS
Mạnh ở:
- dữ liệu transaction lớn và giàu detection context;
- card/device/identity context;
- entity/proxy heterogeneity;
- distribution shift rõ;
- phù hợp stress-test framework trong môi trường online/card/e-commerce khác Xente.

**Không merge hai dataset.** Dùng cùng system architecture nhưng parameterize riêng.

## Vai trò từng phần

- **Mục tiêu:** thử nghiệm / stress-test fraud-management policy.
- **ABM / dynamic simulation:** công cụ nghiên cứu.
- **Adaptive fraudster:** phát triển risky actor của đề án thành cơ chế feedback qua nhiều vòng.
- **Persistent queue + analyst capacity:** phát triển daily overflow thành operational dynamics.
- **Risk model:** scenario-specific component tạo risk score.
- **Xente + IEEE-CIS:** hai empirical environments bổ sung cho nhau.

## Bắt đầu đọc từ đâu?

1. `00 Dashboard/READING ORDER.md`
2. `00 Dashboard/De an to KLTN - Development Map.md`
3. `03 Model design/Research Design v1.1 - Develop from FinRisk Proposal.md`
4. `03 Model design/Shared Two-Scenario Architecture v1.0.md`
5. `03 Model design/Xente Full Model Specification v1.0.md`
6. `03 Model design/IEEE-CIS Full Implementation Plan v1.0.md`
7. `05 Experiments/Final Core Experiment Grid v1.0.md`
8. `05 Experiments/Cross-Scenario Comparison Plan v1.0.md`

## Core experiment toàn thesis

```text
2 datasets
×
2 fraudster modes
×
2 policies
×
3 analyst-capacity levels
=
24 configurations
```

Datasets:
- Xente
- IEEE-CIS

Fraudster:
- Static
- Adaptive

Policies:
- Fixed-threshold
- Capacity-aware

Capacity:
- Low
- Medium
- High

Cost-sensitive là extension nếu cost assumptions đủ defensible.

## Thứ tự implementation

Không build hai simulator riêng song song.

```text
Shared architecture
      ↓
Xente full implementation
      ↓
tách/freeze common interfaces
      ↓
IEEE-CIS adapter + parameterization
      ↓
24 core configurations
      ↓
cross-scenario robustness
```

## Những gì đã có

Xente:
- audit/profile;
- leakage-safe customer-history features;
- chronological risk baseline;
- persistent queue;
- threshold/capacity/priority robustness.

IEEE-CIS:
- EDA/data-to-ABM analysis;
- scenario role đã được xác định;
- cần chuyển từ EDA sang executable feature/risk/adapter pipeline.

Shared:
- fraud-policy interface;
- integrated policy/queue engine;
- adaptive fraudster prototype;
- tests cho queue/policy/adaptation mechanics.

## Claim boundary

Không claim:
- digital twin;
- production threshold;
- bank staffing recommendation;
- exact fraudster cognition;
- universal best policy.

Kết luận phải gắn với scenario, assumptions và parameter ranges đã thử.
