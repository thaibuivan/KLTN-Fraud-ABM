# Data Audit — Xente vs IEEE-CIS

## Goal
Chọn **một primary transaction-fraud dataset** làm empirical grounding chính cho KLTN.

Legacy repo `FinRisk-ABM-Policy-Simulation` đã dùng ULB, BankSim và PaySim để calibrate synthetic assumptions. Trong KLTN, các nguồn đó chỉ nên được xem là **legacy reference evidence**, không mặc định là primary dataset.

---

## Executive decision

**Primary dataset đề xuất: Xente Fraud Detection.**

**Secondary / optional robustness dataset: IEEE-CIS Fraud Detection.**

Lý do chính: mục tiêu KLTN không phải benchmark classifier thuần túy mà là xây dynamic policy simulation/ABM có **persistent customer/account state, transaction history, policy, queue và analyst capacity**. Xente có `CustomerId`, `AccountId`, `SubscriptionId` và `TransactionStartTime` rõ ràng, nên hỗ trợ state/history trực tiếp tốt hơn. IEEE-CIS lớn và giàu feature hơn, nhưng không cung cấp true customer identifier; muốn dựng entity history phải dùng pseudo-entity key từ các trường card/address/email đã anonymized.

---

## 1. Xente Fraud Detection

### Official dataset facts
Theo trang dữ liệu chính thức của Zindi:
- Xente là nền tảng e-commerce/financial-services tại Uganda với hơn 10,000 khách hàng.
- Challenge chứa khoảng 140,000 transactions trong khoảng 15/11/2018–15/03/2019.
- Training period: 15/11/2018–13/02/2019, có `FraudResult`.
- Test period: 13/02/2019–14/03/2019, không có fraud label.
- Raw competition data không được phép redistribute/publicly upload theo rules của Zindi.

Các bản mô tả dataset công khai cho thấy training schema gồm:
- `TransactionId`
- `BatchId`
- `AccountId`
- `SubscriptionId`
- `CustomerId`
- `CurrencyCode`, `CountryCode`
- `ProviderId`, `ProductId`, `ProductCategory`
- `ChannelId`
- `Amount`, `Value`
- `TransactionStartTime`
- `PricingStrategy`
- `FraudResult`

Một phân tích công bố trên bộ training báo cáo 95,662 rows, 193 fraud cases (~0.20%). **Con số này phải được verify lại bằng local profiling sau khi tải dữ liệu**, vì Zindi page không công bố trực tiếp fraud count.

### Strengths for this thesis
1. **True customer/account identifiers**
   - phù hợp để build rolling history theo customer/account;
   - hỗ trợ persistent state mà không cần proxy entity.

2. **Actual transaction timestamp**
   - phù hợp event ordering;
   - có thể replay transaction stream theo thời gian;
   - hỗ trợ rolling features và queue arrival process.

3. **Fraud ground truth trên training period**
   - dùng để train/evaluate risk engine;
   - dùng làm observed outcome trong policy replay.

4. **Manageable size**
   - thuận lợi cho KLTN, repeated experiments và debugging.

5. **Low fraud prevalence**
   - gần với bài toán extreme imbalance hơn IEEE-CIS;
   - hữu ích khi nghiên cứu false positives / analyst workload.

### Limitations
1. Labelled period tương đối ngắn.
2. Fraud positives rất ít (~193 theo published analysis), có thể hạn chế complex risk model.
3. Dữ liệu đến từ một platform/market cụ thể ở Uganda; không đại diện trực tiếp cho ngân hàng Việt Nam.
4. Không có operational analyst logs, review time, cost hay queue data.
5. Raw data **không được commit vào public GitHub repo** vì competition rules.

---

## 2. IEEE-CIS Fraud Detection

### Official dataset facts
Theo Kaggle:
- target: `isFraud`;
- transaction và identity tables join bằng `TransactionID`;
- identity information không tồn tại cho mọi transaction;
- `TransactionDT` là time delta từ một reference point, không phải actual datetime;
- transaction features gồm `TransactionAmt`, `ProductCD`, `card1-card6`, `addr1-2`, email-domain, C/D/M/V groups;
- identity table có `DeviceType`, `DeviceInfo`, `id_12-id_38`;
- dataset distribution/availability chịu competition rules.

Published descriptions commonly report:
- 590,540 train transactions;
- 20,663 fraud (~3.5%);
- khoảng six months;
- 394 transaction features plus identity features.

### Strengths
1. Large sample and many fraud positives.
2. Rich transaction/device/identity features.
3. Good benchmark for risk-engine modeling and temporal validation.
4. Suitable for advanced ML comparison if classifier performance becomes important.

### Limitations for this thesis
1. **No documented true customer identifier.**
   - recent research uses pseudo-entity keys such as combinations of `card1`, `card2`, `addr1`, `P_emaildomain`;
   - this creates entity-identification uncertainty and may merge/split real customers.

2. Extensive anonymization/masking.
   - many mechanisms cannot be given clear behavioral meaning.

3. Identity table only covers a subset of transactions.

4. Much heavier compute/data-engineering burden.

5. Fraud rate (~3.5%) is much higher than Xente training and may be less suitable as a baseline for alert-load stress unless treated carefully.

---

## 3. Direct comparison

| Criterion | Xente | IEEE-CIS | KLTN implication |
|---|---|---|---|
| Fraud label | `FraudResult` in train | `isFraud` in train | Both usable |
| Time | Actual `TransactionStartTime` | Relative `TransactionDT` | Xente easier for event replay |
| True customer ID | **Yes: `CustomerId`** | **No explicit true customer ID** | Xente strongly preferred |
| Account-level ID | `AccountId`, `SubscriptionId` | Card/address proxies | Xente preferred |
| Amount | `Amount`, `Value` | `TransactionAmt` | Both usable |
| Product/category/channel | Explicit | Rich but partly masked | Xente more interpretable |
| Train size | ~95.7k reported | ~590.5k | IEEE larger |
| Fraud positives | ~193 reported | ~20.7k reported | IEEE stronger for ML |
| Fraud rate | ~0.20% reported | ~3.5% | Xente gives harsher imbalance |
| Identity/device richness | Limited | Rich identity/device subset | IEEE advantage |
| Missingness | reportedly low in train; verify locally | substantial/sparse in many columns | Xente simpler |
| Mechanism interpretability | Higher | Lower because masking | Xente preferred |
| Compute burden | Low/medium | High | Xente preferred |
| Public redistribution | **No** under Zindi rules | subject to Kaggle competition rules | Raw data stays outside repo |

---

## 4. Decision for thesis architecture

### Primary empirical baseline: Xente
Use Xente as **observed-event baseline**, not merely as calibration input for a synthetic generator.

Recommended baseline pipeline:

```text
Observed Xente transaction stream
        ↓
Chronological feature construction
        ↓
Risk engine trained only on earlier data
        ↓
Policy layer
        ↓
Persistent alert queue
        ↓
Analyst service/capacity
        ↓
Observed fraud label used for outcome evaluation
        ↓
Loss / FP / workload / delay / cost
```

This is preferable to making synthetic transactions the core because it reduces unnecessary generator assumptions.

### Secondary role: IEEE-CIS
Use IEEE-CIS only if time allows for one of these purposes:
- robustness check for risk-engine behavior;
- external benchmark showing that conclusions are not tied to one feature set;
- optional structural sensitivity using pseudo-entity history.

Do **not** make IEEE-CIS a second full ABM unless necessary; that would add large engineering cost without directly strengthening the main RQ.

---

## 5. Entity choice

### Proposed primary stateful entity
**Customer agent/state = `CustomerId`**

Candidate nested/account states:
- `AccountId`
- `SubscriptionId`

Initial thesis implementation should avoid making Customer, Account and Subscription three independent agents unless interactions among them are required by an RQ.

Recommended hierarchy:

```text
Customer state
  ├── one or more AccountId
  └── one or more SubscriptionId
```

Use customer as the persistent entity; account/subscription are attributes/grouping levels first.

---

## 6. What can be estimated directly from Xente

| Dataset evidence | Model state / parameter | Estimation |
|---|---|---|
| `CustomerId` | Customer identity/state | Direct |
| `AccountId` | Account grouping | Direct |
| `SubscriptionId` | Subscription grouping | Direct |
| `TransactionStartTime` | Arrival time / temporal ordering | Direct |
| `Amount`, `Value` | Transaction amount distribution / potential loss proxy | Empirical distribution |
| `ProductCategory` | Product/category heterogeneity | Empirical frequencies |
| `ChannelId` | Channel heterogeneity | Empirical frequencies |
| `ProviderId`, `ProductId` | Provider/product pattern | Empirical frequencies |
| `PricingStrategy` | Pricing context | Empirical frequencies |
| `FraudResult` | Ground-truth fraud outcome | Direct |
| Customer transaction history | frequency/velocity/rolling amount | Derived chronologically |
| Fraud prevalence | baseline fraud regime | Estimate from labelled train |
| Inter-arrival times | transaction arrival process | Derived by customer/global stream |

---

## 7. What Xente cannot identify

These **must not be presented as empirically estimated from Xente**:
- analyst capacity;
- analyst review-time distribution;
- analyst accuracy/error;
- queue discipline;
- cost per analyst minute;
- false-positive/customer-friction cost;
- fraud recovery rate;
- effect of delayed review on recoverable fraud loss;
- sophisticated fraudster adaptation.

These require literature-informed ranges, expert input, or explicit assumptions + sensitivity analysis.

---

## 8. Baseline experiment split

Avoid random train/test split for the core model.

Recommended:
1. sort training data by `TransactionStartTime`;
2. use early period for risk-engine training;
3. use later labelled period for policy replay/validation;
4. construct rolling features using **past transactions only**;
5. never use future information to build customer history.

Exact cut points should be chosen after local profiling to preserve enough fraud events in train/validation/test.

Because fraud positives are sparse, cut points must be checked against event counts rather than fixed blindly at 70/15/15.

---

## 9. Scenario strategy after empirical baseline

Start from observed Xente baseline, then apply bounded stress scenarios:

- higher fraud arrival/intensity;
- altered amount mix;
- higher/lower transaction volume;
- analyst capacity reduction;
- review-time increase;
- cost ranges;
- selected fraud-pattern shifts supported by data/literature.

Clearly label these as **counterfactual stress scenarios**, not observed Xente facts.

---

## 10. Data governance

### Public GitHub repo
Do **not** commit:
- Xente `training.csv`;
- Xente `test.csv`;
- derived row-level copies that recreate competition data.

Commit only:
- code;
- schemas;
- aggregate profiling tables that do not redistribute raw competition data;
- documentation;
- reproducible instructions.

Suggested local path:

```text
data/raw/xente/
```

and keep `data/raw/` in `.gitignore`.

---

## 11. Sources

### Xente
- Zindi competition data page: https://zindi.world/competitions/xente-fraud-detection-challenge/data
- Zindi competition rules/data restrictions: https://zindi.africa/competitions/xente-fraud-detection-challenge/hackathons
- Published schema/class-count cross-check (must still verify locally): https://rsisinternational.org/journals/ijrsi/articles/a-comparative-analysis-of-machine-learning-algorithms-on-card-based-financial-fraud-detection-with-infusion-of-sigmoid-and-isotonic-functions/

### IEEE-CIS
- Kaggle official data page: https://www.kaggle.com/competitions/ieee-fraud-detection/data
- Recent study explicitly noting lack of true customer identifier and use of pseudo-entity key: https://www.mdpi.com/2076-3417/16/12/5809

---

## Final decision

**Primary dataset: Xente Fraud Detection.**

Rationale:
> Xente sacrifices sample size and number of fraud positives, but its explicit customer/account identifiers and actual transaction timestamp provide a substantially cleaner empirical basis for a stateful dynamic policy simulation/ABM. IEEE-CIS is stronger as a classifier benchmark, but weaker for this thesis's core need: interpretable persistent entities and transaction histories.

## Immediate next steps
- [ ] Download Xente data locally after accepting Zindi terms.
- [ ] Run local schema + label + entity + temporal profiling.
- [ ] Choose chronological split based on fraud counts.
- [ ] Build leakage-safe rolling customer features.
- [ ] Fit a simple baseline risk engine.
- [ ] Implement persistent alert queue.
- [ ] Re-run legacy policy ideas on the new empirical baseline.
