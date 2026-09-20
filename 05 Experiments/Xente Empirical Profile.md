# Xente Empirical Profile — verified from competition package

## Source
Profiled directly from the uploaded Xente competition package:
- `training.csv`
- `test.csv`
- `Xente_Variable_Definitions.csv`
- `sample_submission.csv`

Raw competition rows are **not** committed to GitHub.

## Training data
- Rows: **95,662**
- Columns: **16**
- Fraud cases: **193**
- Fraud rate: **0.2018%**
- Time range: **2018-11-15 02:18:49 UTC → 2019-02-13 10:01:28 UTC**
- Missing values: **0 in all training columns**
- Unique `CustomerId`: **3,742**
- Unique `AccountId`: **3,633**
- Unique `SubscriptionId`: **3,627**

## Entity repetition

### CustomerId
- Mean transactions/customer: **25.56**
- Median: **7**
- P95: **98**
- Max: **4,091**
- Share customers with >=2 transactions: **80.97%**
- Share customers with >=5 transactions: **63.68%**

This is strong empirical support for customer-level persistent state/history.

### Important correction about AccountId / SubscriptionId
`AccountId` and `SubscriptionId` are **not safe to assume as one-to-one nested customer accounts**.

Observed facts:
- ~70.6% of customers use more than one AccountId.
- Some AccountIds are shared by very many CustomerIds.
- The largest `AccountId` has **30,893 transactions** and is observed across a very large number of customers.
- One AccountId is associated with up to **2,577 CustomerIds**.

Therefore:
> `CustomerId` remains the primary persistent entity. `AccountId` and `SubscriptionId` should initially be treated as transaction-context identifiers/features, not as independent agents or clean nested account states.

## Fraud concentration
- Fraud transactions belong to **54 unique customers**.
- Fraud transactions belong to **52 unique AccountIds**.
- The top 10 fraud customers account for approximately **62.7%** of all fraud cases.

Implication:
- customer heterogeneity matters;
- but fraud labels are concentrated in a small number of entities, so model evaluation must report uncertainty and avoid over-generalization.

## Amount / Value

### Amount definition
Dataset definition:
- positive `Amount` = debit from customer account;
- negative `Amount` = credit into customer account;
- `Value` = absolute value of amount.

### Overall
- Median Amount: **1,000**
- P95 Amount: **14,500**
- P99 Amount: **80,000**
- Negative Amount share: **39.92%**
- Median Value: **1,000**
- P95 Value: **25,000**
- P99 Value: **90,000**

### Fraud
- Median Amount: **600,000**
- P95 Amount: **5,000,000**
- Mean Amount: **1,535,272**
- Median Value: **650,000**
- Only ~**2.6%** of fraud transactions have negative Amount.

### Legitimate
- Median Amount: **1,000**
- P95 Amount: **12,930**
- Mean Amount: **3,628**

Implication:
Xente fraud is strongly associated with high transaction value. This likely makes the risk-model benchmark relatively easy and must be acknowledged when interpreting policy results.

## Category/channel patterns

### ProductCategory
Fraud counts:
- financial_services: **161 / 45,405**
- airtime: **18 / 45,027**
- utility_bill: **12 / 1,920**
- transport: **2 / 25**

### ChannelId
- ChannelId_3: **184 fraud / 56,935**
- ChannelId_2: **5 / 37,141**
- ChannelId_1: **4 / 538**
- ChannelId_5: **0 / 1,048**

### ProviderId
Fraud concentration is also strongly heterogeneous across providers.

Implication:
Risk engine can use product/provider/channel context, but the thesis must avoid confusing dataset-specific fraud signatures with universal fraud mechanisms.

## Chronological split diagnostics

### Candidate 70/15/15
| Split | Rows | Fraud | Fraud rate | Period |
|---|---:|---:|---:|---|
| Train | 66,963 | 104 | 0.1553% | 2018-11-15 → 2019-01-21 |
| Validation | 14,349 | 39 | 0.2718% | 2019-01-21 → 2019-02-01 |
| Test | 14,350 | 50 | 0.3484% | 2019-02-01 → 2019-02-13 |

### Cold-start issue
Relative to the first 70% training period:
- ~**21.8%** of validation transactions belong to customers not seen in training;
- ~**37.1%** of test transactions belong to customers not seen in training;
- **30/39** validation fraud cases come from customers unseen during training;
- **41/50** test fraud cases come from customers unseen during training.

This is a major finding.

Implications:
1. Raw CustomerId must **not** be a model feature.
2. Customer history should be represented through rolling behavioral features.
3. The risk engine needs a cold-start fallback when prior history is absent.
4. Performance should be reported separately for:
   - seen customers;
   - unseen/cold-start customers.

## Split decision
Use **70/15/15 chronological split as the first baseline**, because it leaves:
- 104 fraud cases for training;
- 39 for validation;
- 50 for final testing.

However, because only 193 frauds exist overall:
- do not rely on one metric point estimate;
- add bootstrap confidence intervals and/or rolling-origin checks later.

## Thesis consequence
Xente supports a stateful customer model, but it also creates two important limitations:
1. **strong amount/category signal** may make fraud ranking unusually easy;
2. **many later frauds are cold-start customers**, so customer-history features alone cannot solve the task.

These limitations are useful rather than fatal: they motivate the policy/queue focus and explicit robustness analysis.
