# BẢN THẢO CHƯƠNG PHƯƠNG PHÁP v1.1 — 18/10/2026

**Trạng thái:** Bản thảo nghiên cứu để GVHD rà soát. Không đưa bất cứ tài liệu Green SM nội bộ nào vào bản thảo. Các kết quả chưa chạy thực nghiệm phải được ghi rõ.

## 1. Phạm vi và thiết kế nghiên cứu

Khóa luận xây dựng một môi trường thí nghiệm chính sách quản lý gian lận giao dịch theo hướng **hybrid agent-based/discrete-event simulation**. Tác tử gian lận có trạng thái và cơ chế học theo phản hồi; chính sách, chấm điểm rủi ro và hàng đợi chuyên viên là những mô-đun vận hành có tương tác. Mục tiêu là so sánh những trade-off về fraud, can thiệp giao dịch hợp lệ và workload, không tối ưu một classifier mới hoặc dựng digital twin của ngân hàng.

Bốn RQ: (1) tác động của Static so với Adaptive fraudster; (2) Fixed-threshold so với Capacity-aware; (3) tương tác với Low/Medium/High capacity; (4) độ vững giữa Xente và IEEE-CIS. Đặc tả dự kiến theo ODD (Grimm et al., 2020); nguồn bất định tham số/cấu trúc/ngẫu nhiên/quan sát được tách theo McCulloch et al. (2022).

## 2. Hai môi trường thực nghiệm

**Xente**: 95.662 giao dịch có nhãn ở tập huấn luyện, 193 fraud; có CustomerId, timestamp thực, Amount/Value, channel/product/provider. Đặc trưng lịch sử khách hàng được dựng từ quá khứ; không giả định AccountId hoặc SubscriptionId là chủ sở hữu tài khoản phân cấp đúng nghĩa.

**IEEE-CIS**: 590.540 giao dịch có nhãn; 20.663 fraud. Các biến TransactionAmt, ProductCD, card, address/email, device/identity và nhóm C/D/M/V. TransactionDT là relative time. Khóa luận chỉ sử dụng card1+addr1 như entity proxy, **không** gọi là khách hàng có danh tính thật. Masked C/D/M/V chỉ giữ vai trò detection context, không diễn giải thành lựa chọn gian lận có chủ đích.

Hai tập dữ liệu **không trộn**. Mỗi scenario có empirical distributions, history state và frozen risk model riêng; chỉ chia sẻ policy/queue/learning/metric semantics.

## 3. Temporal split và quy tắc phản thực tế

Trên phần dữ liệu có nhãn, chia theo thứ tự thời gian **70% train / 15% validation / 15% test**. Train dùng fit model; validation dùng calibration thresholds và donor fraud samples; test dùng đánh giá. Không lấy các fraud events của test làm mẫu donor cho giả lập.

Trong closed-loop, thời điểm các fraud test events xác định **attempt slots** để giữ lịch thử nghiệm và số lượng attempts đối chiếu. Khi đến một slot, agent chọn strategy, sinh raw fraud event từ pool validation tương ứng, rồi **chấm điểm lại** với state quá khứ đã thay đổi. Các legitimate test events vẫn cần được tái chấm điểm theo chronology tương tự; sử dụng risk score cố định của legitimate events khi history đã thay đổi là phép xấp xỉ chưa đủ chặt cho main experiment.

Giới hạn nhận diện: đây là **stress test conditional on test fraud-attempt timing**, không phải mô hình xác suất xuất hiện fraud toàn diện. Donor regime được suy ra từ nhãn validation; cơ chế sinh không thể chứng minh cognition hoặc kỹ thuật tấn công thật.

Kiểm tra trực tiếp IEEE raw từ archive: 501.959 events trước test để warm-up history; validation fraud donors = 3.042; test = 88.581, trong đó fraud slots = 3.083. Validation fraud amount terciles là **50** và **117**, median **77**, pool sizes **1.052/1.030/960**. Ba nhóm này chỉ là *bounded amount-regime abstraction*.

## 4. Mô hình chấm điểm

Xente dùng regularized logistic regression với past-only customer features. IEEE dùng SGDClassifier log-loss, chronological history features, train-only frequency mappings và categorical encodings. Các kết quả baseline đã được repo ghi nhận:
- Xente PR-AUC: validation 0,560851; test 0,892521.
- IEEE PR-AUC: validation 0,3644; test 0,3840; ROC-AUC: 0,8218 và 0,8219.

Những chỉ số này là độ phù hợp của module đầu vào, **không đồng nghĩa với policy hiệu quả**. Trước khi chạy IEEE main experiment, phải làm pass **unchanged held-out online-vs-offline score equivalence**. Phiên bản fast scorer phải khớp online reference và frozen model; CI synthetic equivalence là cần thiết nhưng chưa đủ thay cho kiểm tra bằng real raw test.

## 5. Chính sách và giới hạn analyst

Với p_t là predicted fraud score, T_R ngưỡng review và T_B ngưỡng block:

\[
a_t = \begin{cases}
\mathrm{BLOCK}, & p_t \ge T_B \\
\mathrm{REVIEW}, & T_R \le p_t < T_B \\
\mathrm{APPROVE}, & p_t < T_R .
\end{cases}
\]

Policy Fixed giữ nguyên các ngưỡng. Policy Capacity-aware quan sát Q_t (backlog) và \(\mu_t\) (pooled service rate), với \(H_t=Q_t/\mu_t\) khi \(\mu_t>0\), từ đó đổi ngưỡng REVIEW theo trạng thái tắc nghẽn. Core validation review-rate tails: **1,00%, 0,75%, 0,50%**; BLOCK tail **0,10%**; congestion triggers **24/72 backlog-hours**. Những giá trị này là scenario assumptions phải sensitivity-test, không phải tham số tối ưu thực tế.

Capacity được chuẩn hóa theo validation alert-arrival workload: \(\mu(c)=c\lambda_{\rm val}\), \(c\in\{0.75,1.0,1.25\}\). FIFO làm core queue; risk-priority kiểm tra structural robustness. Shen & Kurshan (2020) đã nghiên cứu adaptive threshold dưới giới hạn xử lý cảnh báo: đóng góp khóa luận không phải đề xuất dynamic threshold lần đầu.

## 6. Tác tử gian lận thích nghi

Agent có strategy value \(V_s\), chọn chiến lược bằng epsilon-greedy và cập nhật theo phần thưởng:

\[
V_s(t+1) = V_s(t) + \alpha [r_t - V_s(t)].
\]

Core \(\alpha=0.15\), \(\epsilon=0.10\); reward scale là median validation-fraud amount riêng từng scenario. Dormancy off để giữ số lượng fraud-attempt slots cố định giữa đối chứng. Static comparator bốc thăm theo empirical validation regime weights, không cập nhật weights sau action.

Trong core, fraudster nhận reward ngay từ quyết định policy APPROVE/REVIEW/BLOCK. Đây là **giả định observability**, đặc biệt vì REVIEW có thể là quyết định nội bộ mà đối tượng gian lận không biết. Nghiên cứu phải thực hiện sensitivity bỏ quan sát trực tiếp REVIEW hoặc mô hình hóa delay. Không diễn giải thay đổi strategy shares là hành vi thực tế đã được chứng minh từ dữ liệu.

## 7. Outcome semantics

Các metrics quan trọng:
- Fraud: direct block count/value, fraud approved count/value, review started/completed, unresolved review và fraud amount exposure at horizon.
- Operations: review count, backlog, mean/P95 waiting time.
- Customer: legitimate review/block/intervention rate.
- Behavior: regime shares và thay đổi shares qua thời gian.

Metric cũ “fraud_intercept_rate” gộp BLOCK với REVIEW bắt đầu trước horizon. Metric này là **interception/review routing proxy**, không đồng nghĩa với prevented monetary loss. Phần bổ sung outcome sensitivity đòi hỏi REVIEW hoàn tất trước horizon mới đủ điều kiện tính prevented conditional on assumed effectiveness q:

\[
E[\mathrm{prevented\ fraud\ value}\mid q]
= V_{\rm direct\,BLOCK} + q V_{\rm completed\,fraud\,REVIEW},
\quad q \in \{0,0.5,1\}.
\]

Q hoàn toàn giả định, **không** phải empirically estimated fraud recovery. Unresolved review không được tự động gọi là realized loss.

## 8. Experimental design, uncertainty và validation

Full core = **2 datasets × 2 fraudster modes × 2 policies × 3 capacity levels = 24 cells**. Xente đã có 12 cells × 50 seeds và targeted sensitivity, degraded-score 30 seeds. IEEE cần chạy 12 cells với seed convergence rồi mới phân tích cross-scenario.

Đánh giá adaptation penalty, policy gain, interactions theo capacity và ranking consistency bằng contrasts trong cùng dataset; báo seed variability và uncertainty intervals. Do đầu vào hai môi trường khác đơn vị/tỉ lệ gian lận, không so trực tiếp raw monetary amounts hoặc raw probability thresholds giữa hai datasets.

Validation gồm:
1. **Conceptual/structural:** agents, feedback, queue và RQs được nối logic, ODD minh bạch.
2. **Empirical:** source split, observed patterns, donor support, missingness, drift, no future leakage.
3. **Code/score:** CI tests, score-equivalence trên frozen IEEE model, reproducibility và invariants.
4. **Stochastic:** repeated seeds, convergence của count-based, value-based và operational metrics.
5. **Parameter & structural:** alpha/epsilon, feedback timing, q, threshold tiers, capacity, queue discipline, degraded risk scoring.
6. **Claim boundary:** không digital twin, không real-bank optimum, không xác định cognition đối kháng, không staffing recommendation.

Lưu ý causal design: sử dụng cùng random seed là công cụ giảm variance nếu tạo tương quan thích hợp, nhưng trong feedback system khi policy đổi chiến lược thì hai trajectories không bắt buộc giống hệt nhau. Cần giải thích đúng pair-by-seed comparisons.

## 9. Trạng thái thực nghiệm và ghi chú cho GVHD

**Đã chạy:** Xente closed-loop main/sensitivity, IEEE empirical baseline và pre-adaptation policy replay.

**Đã viết và CI xác nhận mã:** IEEE donor generator, online scorer, fast scalar scorer, history warmup, context splitter, outcome accounting, IEEE integrated runner và các bài unit/integration tests.

**Chưa được khẳng định hoàn thành:** online-vs-frozen-baseline audit bằng artifact IEEE, pilot closed-loop trên frozen real model, 12-cell IEEE repeated-seed run, final across-environment comparisons và hoàn chỉnh từng chương văn bản.

**Không dùng Green SM internal documents, code hoặc facts**, trừ khi quyền công bố / sử dụng học thuật được xác nhận chính thức.

## Tài liệu phương pháp chọn lọc

1. Grimm, V., et al. (2020). The ODD Protocol for Describing Agent-Based and Other Simulation Models: A Second Update to Improve Clarity, Replication, and Structural Realism. JASSS 23(2), 7. DOI: 10.18564/jasss.4259.
2. McCulloch, J., et al. (2022). Calibrating Agent-Based Models Using Uncertainty Quantification Methods. JASSS 25(2), 1. DOI: 10.18564/jasss.4791.
3. Shen, H., & Kurshan, E. (2020). Deep Q-Network-based Adaptive Alert Threshold Selection Policy for Payment Fraud Systems in Retail Banking. ICAIF 2020. DOI: 10.1145/3383455.3422563.
4. Ding et al. (2025). AML-CFSim: An agent-based simulation model for anti-money laundering from cyber fraud crimes. Expert Systems with Applications. DOI: 10.1016/j.eswa.2025.127995.
5. Höppner, S., et al. (2022). Instance-dependent cost-sensitive learning for detecting transfer fraud. European Journal of Operational Research. DOI: 10.1016/j.ejor.2021.05.028.

**Trước khi nộp:** rà bibliographic details theo bản xuất bản, viết lại hoàn chỉnh văn phong và dẫn nguồn cụ thể cho bảng/biểu đồ, xác minh mọi metric với output được lưu.
