# Real-bank AML alert scoring evidence — 2025

## Source
*Developing a scoring model for managing money laundering transactions using machine learning*  
Journal of Money Laundering Control, 2025.

Source:
https://doi.org/10.1108/JMLC-09-2024-0152

## Why it is useful
Đây là **operational evidence** từ implementation tại một major bank, nhưng domain là AML transaction monitoring, không phải Xente-style transaction fraud.

Paper mô tả:
- large institutions may employ hundreds of alert analysts;
- alerts có thể đi qua Level 1 / Level 2 / Level 3 review;
- low-risk alerts trong pilot dùng **5-minute light-touch review**;
- high-risk alerts có thể auto-escalate;
- sau implementation, một phần low-risk alerts được auto-hibernate;
- 19% alerts hibernated và 18% auto-escalated ở cuối period được báo cáo;
- time-to-SAR giảm 61%.

## What this supports
- review time có thể khác theo risk tier;
- automation/routing thay đổi analyst workload;
- operational delay là meaningful outcome;
- customer/history overrides có thể ảnh hưởng routing.

## What it does NOT support
Không được dùng trực tiếp để nói:
- transaction-fraud analyst review time = 5 minutes;
- Xente analyst capacity = N cases/day;
- AML escalation workflow = fraud-card workflow.

## How to use in KLTN
Use **5 minutes only as an external lower/fast-review anchor** if later testing service-time scenarios.

Core v0.1 nên tránh bank-specific minute assumptions bằng cách parameterize **relative service capacity**.

## Link
- [[Operational Parameter Grounding v0.1]]
- [[Queue and Analyst Service Design v0.1]]
