# IEEE-CIS Full Implementation Plan v1.0

## Vai trò trong khóa luận

IEEE-CIS là **Scenario B core**, không phải dataset phụ.

Tuy nhiên thứ tự triển khai là:
1. hoàn thiện shared engine trên Xente;
2. tái sử dụng engine;
3. viết IEEE adapter / state builder;
4. parameterize và chạy cùng experiment grid.

Điều này tránh viết hai simulator riêng.

## Stage A — Data audit / EDA ✅ về mặt phân tích

EDA hiện có đã xác định:
- transaction + identity structure;
- TransactionAmt / ProductCD;
- card context;
- device / identity context;
- address/email relations;
- count/time-delta/match/rich detection features;
- relative TransactionDT;
- fraud label isFraud;
- entity/proxy repetition;
- train-test distribution shift.

Lưu ý:
- không có true CustomerId như Xente;
- nhiều feature bị mask;
- TransactionDT là relative time.

## Stage B — Scenario-specific entity representation ⏳

Không ép IEEE thành customer-centric.

MVP entity state có thể dùng:
- card-based proxy;
- card + address/email/device combinations nếu leakage audit cho phép;
- history/count features được build theo chronological order.

Mỗi proxy phải được ghi rõ là **entity proxy**, không gọi là customer thật.

## Stage C — Leakage-safe feature table ⏳

Mục tiêu:
- chronological features;
- no future information;
- no target-derived history;
- unknown/missing identity handling.

Ưu tiên feature groups:
- TransactionAmt;
- ProductCD;
- card1-card6;
- DeviceType / DeviceInfo;
- id_*;
- address/email context;
- count/time-delta/match groups;
- entity-history features nếu build được.

## Stage D — Risk model ⏳

Train scenario-specific risk model.

Không cần cùng model class tuyệt đối với Xente nếu feature complexity khác, nhưng nên có:
- interpretable baseline;
- stronger model nếu cần;
- chronological validation;
- PR-AUC / ROC-AUC / calibration;
- temporal/drift diagnostics.

Risk score cuối phải map về cùng interface:

```text
risk_probability ∈ [0,1]
```

## Stage E — Policy replay ⏳

Dùng shared:
- fraud_policies.py;
- simulate_policy_system.py;
- queue/analyst mechanism.

Chỉ cần viết IEEE score/event adapter sang common schema:

```text
TransactionId
EventTime
TransactionValue
FraudLabel
risk_probability
scenario/entity metadata
```

EventTime có thể dùng relative TransactionDT.

## Stage F — Static fraudster environment ⏳

Fraud generator/perturbation phải bám IEEE empirical support.

Candidate adaptive dimensions:
- amount regime;
- timing regime;
- card/device/identity context perturbation chỉ khi defend được;
- không diễn giải masked V/C/D/M features thành human-readable fraud strategy nếu semantic không biết.

## Stage G — Adaptive fraudster ⏳

Giữ **cùng learning rule** với Xente.

Khác biệt nằm ở:
- strategy-to-feature mapping;
- empirical support;
- state representation.

Điều này cho phép so adaptation effect giữa hai environments.

## Stage H — 12 scenario-specific configurations ⏳

Cho IEEE:

```text
Static / Adaptive
×
Fixed / Capacity-aware
×
Low / Medium / High capacity
= 12 configurations
```

Sau đó ghép với 12 Xente configurations thành 24 core configurations toàn thesis.

## Stage I — Cross-scenario comparison ⏳

So:
- adaptation penalty;
- capacity-aware gain;
- policy ranking;
- congestion sensitivity;
- customer/intervention proxy phù hợp scenario.

Không ép raw fraud amount/loss scale hai dataset phải giống nhau.

## Definition of done

IEEE scenario hoàn thành khi:
- [ ] entity/proxy definition frozen;
- [ ] chronological feature/risk pipeline chạy;
- [ ] shared policy/queue engine chạy;
- [ ] static/adaptive fraudster mapping chạy;
- [ ] 12 configurations chạy;
- [ ] seed convergence xong;
- [ ] cross-scenario comparison table/figures sinh được.
