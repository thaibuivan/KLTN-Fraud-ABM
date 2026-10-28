# Mayo et al. (2023), HMM và kiểm tra khả thi trên IEEE-CIS — 28/10/2026

**Trạng thái:** Literature review + empirical **feasibility pilot**. **KHÔNG thay đổi thiết kế lõi 24 configurations, không tuyên bố HMM đã chạy trong closed-loop policy experiment.**

## I. Bài báo gốc

Mayo, Katherine; Fozdar, Shaily; Wellman, Michael P. (2023), *Flagging Payments for Fraud Detection: A Strategic Agent-Based Model* (MuFin, 7 trang). Bản gốc: https://kmayo.com/files/papers/mufin23_fraud.pdf.

**Không dùng Hidden Markov Model.** Tác giả xây credit-network ABM và empirical game-theoretic analysis (EGTA) để nghiên cứu cân bằng giữa lựa chọn flagging của ngân hàng và fraudster chọn **payment frequency × amount**.

- Banks strong/weak có giả định độ chính xác detector gamma 0.75–0.90 / 0.50–0.65, và đánh đổi fraud-loss, false-positive fee/inconvenience, detector costs.
- Fraudster có 2 frequency levels × 4 value patterns = 8 strategies; banks có 3 amount thresholds × 4 suspicion matrices = 12 strategies.
- Simulated network: 200 customers, 4 banks, 1 fraudster, 4,320 steps; 9 cost configurations, EGTA equilibria; trong game fraudster thường chọn [high frequency, high value].
- “Payment queue” trong bài là **arrival scheduling queue**, không phải human-analyst REVIEW backlog trong thesis hiện tại.
- Không được sao chép giả định gamma, cost, credit-network, hoặc claim về Nash equilibrium sang thesis khi không có matching implementation/empirical data.

**Điểm bổ trợ trực tiếp:** Current ABM chỉ thay đổi validation-donor amount regimes low/mid/high, trong khi fraud attempt timestamps được gắn vào fixed held-out fraud slots. Paper cho thấy **fraud attempt frequency** cũng là một phương diện quan trọng để stress-test policy; đồng thời strategic flagging và false-positive effects nên được thảo luận riêng khỏi accuracy của detector.

Nghiên cứu nối tiếp trực tiếp: Mayo, Grabill & Wellman (2024), *Fraud Risk Mitigation in Real-Time Payments: A Strategic Agent-Based Analysis*, IJCAI, DOI: 10.24963/ijcai.2024/18.

## II. HMM ứng dụng vào thesis ở đâu?

**Ưu tiên nếu dùng:** latent **attack-intensity** regime (low vs high) để kiểm tra burstiness/fraud-attempt timing trong *structural sensitivity* của queue/capacity/policy. **Không thay** epsilon-greedy agent. Conditional Poisson–HMM:

```text
hidden Z_t  --Markov transitions--> Z_(t+1)
    |
    v
observed/simulated fraud-labeled event count N_t | Z_t=s, exposure_t
                         |
                         v
event attempts -> existing Static/Adaptive fraudster strategy -> donor generator
               -> frozen detector -> Fixed/Capacity-aware -> existing analyst FIFO queue
```

`N_t | Z_t=s,E_t ~ Poisson(E_t * rho_s)`. Training using labeled **train** and validation for score selection only. Latent state is an *environment factor*, not identified criminal intent. Live filtered state cannot access future labels or immediate fraud truth.

Alternative (lower priority): HMM normal customer-spending profile, ideally Xente with CustomerId. Literature: Srivastava et al. (2008), DOI: 10.1109/TDSC.2007.70228; multi-perspective HMM features, DOI: 10.1016/j.future.2019.08.029. This would be detector/score-quality sensitivity, **not** central ABM contribution. Poisson hidden regimes: Avanzi et al. (2021), DOI: 10.1016/j.ejor.2020.07.022.

**DO NOT** try to infer authentic fraudster psychological hidden states directly from dataset: Xente has only 193 labeled fraud in full train; IEEE lacks a trustworthy fraudster identity. Aggregating many unrelated fraud attempts does not create observed strategic individual trajectories.

## III. Pilot định lượng thực thi thật — IEEE-CIS original labeled data

Python research pilot sử dụng raw `train_transaction.csv` từ public Kaggle archive, chronological 70/15/15. Fit only full 24h **relative-time** bins in train: **119**, evaluate 31 full validation bins, bỏ partial boundary bins, **không dùng test labels**. Count là số **labeled fraud transactions**, không phải tất cả intended fraud attempts được quan sát đầy đủ; exposure là total observed transaction volume mỗi bin.

Model comparisons được fit train, chấm điểm **one-step predictive likelihood** trên validation:

| Model | Validation total log-likelihood | Mean log-likelihood / bin |
|---|---:|---:|
| IID Poisson constant rate | **-179.031** | -5.775 |
| IID mixture of two Poisson rates | **-153.770** | -4.960 |
| **2-state Poisson–HMM** | **-153.657** | -4.957 |
| IID Negative Binomial (NB2) | **-141.817** | -4.575 |

**Finding:** HMM cải thiện Poisson cố định nhưng **chỉ hơn non-Markov 2-component mixture 0.113 total log-likelihood / 31 validation bins**, và **kém NB2 11.840**. Data chưa ủng hộ kết luận *Markov persistence* thực sự thêm predictive information đáng kể. Train fraud-rate lag-1 autocorrelation ~0.451; validation ~-0.080, cho thấy tín hiệu có thể không ổn định. Estimated rates HMM khoảng 2.577% / 4.321%, transition A [[0.643,0.357],[0.229,0.771]]. **Đây là statistical latent states, không phải fraudster regimes đã được nhận diện.**

**Giới hạn:** chỉ 119/31 bins; chưa làm được sensitivity ở 6h (execution timeout), không có full uncertainty hoặc ABM stress output; NB2 đếm số vụ theo exposure, không mô phỏng từng strategic action. Pilot dựa trên conditional known transaction volume trong validation, không dự báo future volume. Các dữ liệu Kaggle raw/transaction-level không được commit.

## IV. Quyết định phương pháp

**NO-GO tích hợp HMM vào mô hình chính ở thời điểm này.** Lý do: hiện còn công việc khóa reproducibility/robustness của 24 core cells; pilot 24h chưa chứng minh thành phần Markov tốt hơn đối chứng đơn giản, đặc biệt NB2. HMM có thể được đưa vào **Limitations/Future Work** hoặc chạy structural sensitivity sau này nếu có bằng chứng across time resolutions/holdouts. Nếu chỉ cần stress-test burstiness và overdispersion, thử **NB arrival process** như benchmark trước HMM.

Nếu GVHD muốn extension, protocol:
1. Fit/validate multiple time bins **chọn trước**, compare Poisson, NB, iid mixture, HMM; kiểm tra state/transition stability.
2. Stress case timing-only (giữ N attempts/seed, thay spacing theo inferred latent intensity) và count-plus-timing (N stochastic) **tách rời**.
3. Giữ cùng arrival stream/seed across Fixed vs Capacity-aware để matched comparisons; không đổi core frozen scorer/queue/thresh/agent learning.
4. Run repeated seeds, CI for paired policy contrasts/backlog/intercept proxy, guard against realized-loss claim.
5. Chỉ nâng extension lên results nếu nó trả lời câu hỏi về policy robustness có ý nghĩa, không chỉ cải thiện likelihood tại train.

**Không claim:** thuật toán trong Mayo là HMM; hiện tại thesis đã fit HMM trong ABM; latent HMM states = observed fraudster intent; fraud REVIEW-start proxy = loss prevented.
