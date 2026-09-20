# KLTN Dashboard

## Current thesis direction
Phát triển từ pilot `FinRisk-ABM-Policy-Simulation` thành một **empirically grounded, uncertainty-aware dynamic fraud-policy simulation/ABM**.

## Current milestone
**Legacy-to-thesis migration + research specification trước khi code lại.**

### Priority
1. Chốt [[Research Design v0.2]] với GVHD.
2. Audit và chọn primary dataset.
3. Hoàn thiện Evidence–Parameter Matrix.
4. Chốt [[Conceptual Model v0.2]] và kiểm tra có đủ lý do giữ ABM framing.
5. Thiết kế queue/backlog + validation/experiment plan.
6. Sau đó mới migrate code cần thiết từ legacy repo.

## Legacy project
- [[Legacy Project Audit - FinRisk]]
- [[Legacy Migration Map]]
- [[Prototype-to-Thesis Gap]]

> Repo cũ là pilot/legacy. Không copy nguyên assumptions hoặc kết quả sang KLTN; kết luận chính phải được re-test trong design mới.

## Design
- [[Research Design v0.2]]
- [[Conceptual Model v0.2]]

## Key unresolved decisions
- Primary dataset.
- Customer hay Account là stateful entity chính.
- Queue discipline và review-delay mechanism.
- Risk-engine baseline.
- Policy set chính.
- Analyst parameter grounding.
- ABM hay dynamic policy simulation là framing chính xác hơn sau khi specification hoàn tất.
