# Data Audit

## Goal
Chọn **một primary transaction-fraud dataset** làm empirical grounding chính cho KLTN.

Legacy repo đã dùng ULB, BankSim và PaySim để calibrate synthetic assumptions. Trong KLTN, các nguồn này chỉ nên được xem là **legacy reference evidence**, không mặc định là primary dataset.

## Candidate primary datasets
- Xente
- IEEE-CIS

## Audit criteria

| Criterion | Xente | IEEE-CIS | Why it matters |
|---|---|---|---|
| Fraud label | TBD | TBD | empirical fraud outcomes |
| Transaction time/order | TBD | TBD | dynamic state |
| Customer/account identifier or proxy | TBD | TBD | persistent history |
| Transaction amount | TBD | TBD | loss/amount distribution |
| Repeated observations per entity | TBD | TBD | heterogeneity/history |
| Time horizon | TBD | TBD | temporal/regime analysis |
| Missingness/anonymization | TBD | TBD | mechanism limitations |
| Licence/reproducibility | TBD | TBD | thesis reproducibility |
| Computational size | TBD | TBD | feasibility |

## Mandatory mapping after audit

| Dataset variable/pattern | Model state/parameter | Estimation approach | Limitation |
|---|---|---|---|
| TBD | TBD | TBD | TBD |

## Decision rule
Chọn dataset dựa trên mức độ hỗ trợ **state và mechanisms trong Conceptual Model v0.2**, không chỉ vì benchmark classifier tốt.

## Legacy warning
Không merge ULB + BankSim + PaySim + primary dataset thành một "real bank" dataset. Nếu dùng cross-dataset patterns, phải gắn nhãn external evidence / scenario assumption.

## Decision
**Primary dataset: TBD**
