# Validation Plan v0.1

## Model purpose
Model dùng để **compare/stress-test policy under stated scenarios and uncertainty**, không phải dự báo chính xác hệ thống của một ngân hàng cụ thể.

## Validation layers

### 1. Conceptual / structural validation
Với mỗi agent/state/rule:
- nó cần cho RQ nào?
- evidence từ đâu?
- assumption nào phải ghi rõ?

### 2. Input / pattern validation
Nếu generate/sample transaction behavior, so sánh pattern chính với primary dataset:
- amount;
- timing;
- fraud prevalence;
- entity-level history;
- các pattern khác mà data thực sự hỗ trợ.

### 3. Code verification
Sanity/unit checks:
- queue không service quá capacity;
- backlog carry-over đúng;
- waiting time cập nhật đúng;
- policy decisions đúng rule;
- outcome/cost không double-count;
- seed reproducibility.

### 4. Stochastic uncertainty
Không kết luận từ một run.
- chạy multiple seeds;
- chọn số replications sau pilot stability/convergence check;
- report distributions/intervals.

### 5. Parameter sensitivity
Ưu tiên parameter uncertainty cao trong Evidence Parameter Matrix.

### 6. Structural sensitivity
Chỉ thử mechanisms có khả năng đổi policy conclusion, ví dụ:
- pooled vs heterogeneous analysts;
- FIFO vs risk-priority queue;
- static regime vs regime shift.

## What legacy repo already contributes
Legacy repo đã có scenario comparison và cost sensitivity. KLTN có thể reuse experiment logic, nhưng phải chạy lại trên architecture/data mới.

## Claim discipline
Không suy rộng ngoài:
- model structure;
- parameter ranges;
- scenarios;
- datasets/evidence đã nêu.

## Not required initially
- full History Matching + ABC;
- bank-specific calibration;
- LLM user study;
- massive experiment grid.

## TODO
- [ ] Chốt primary dataset.
- [ ] Chọn empirical validation patterns.
- [ ] Pilot number of seeds.
- [ ] Chọn sensitivity parameters.
- [ ] Chọn 1–2 structural alternatives quan trọng nhất.
