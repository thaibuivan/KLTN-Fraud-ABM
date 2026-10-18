# DỰ THẢO CHƯƠNG KẾT QUẢ VÀ THẢO LUẬN v1.2 — 18/10/2026

> **Tình trạng học thuật:** Bản thảo để tích hợp vào khóa luận và phản biện với GVHD, KHÔNG PHẢI kết luận cuối. Xente: mô hình chính 12 cấu hình × 50 seeds. IEEE-CIS: local empirical full-test pilot 12 cấu hình × **5 seeds**, chưa được canonical repo runner tái chạy và chưa có convergence đầy đủ. Tất cả IEEE findings dưới đây phải được ghi nhãn **pilot / exploratory**; không tự tạo CI/p-value khi chưa có per-seed raw outputs được kiểm tra.

## 4.1. Mục tiêu phân tích và cách đọc chỉ số

Khóa luận không so sánh hai thuật toán phân loại như một competition. Risk model là module đầu vào của một mô phỏng tương tác giữa nguồn giao dịch, cơ chế thích nghi của fraudster, policy và hàng đợi xử lý cảnh báo. Vì mô hình có feedback, một chính sách được đánh giá đồng thời theo (i) đường đi giao dịch gian lận, (ii) can thiệp lên giao dịch hợp lệ, (iii) tải xử lý và backlog, và (iv) độ nhạy với các giả định hành vi/vận hành.

Ba lưu ý khi đọc bảng:
1. **Fraud interception proxy:** trong engine chính, gian lận được tính là intercepted nếu trực tiếp BLOCK hoặc REVIEW *bắt đầu được xử lý* trước khi kết thúc horizon. Chỉ số này KHÔNG đồng nghĩa với prevented transaction loss ngoài đời. Một số thử nghiệm bổ trợ yêu cầu REVIEW hoàn tất trước horizon và thử effectiveness q∈{0,0.5,1} hoàn toàn giả định.
2. **Fraud exposure at horizon** gồm approved-fraud value và unresolved-review fraud value trong semantics engine. Đây không phải chứng cứ của realized bank financial losses hoặc expected recovery.
3. **Xente và IEEE-CIS:** khác thời gian quan sát, tình trạng mất cân bằng, đơn vị amount và feature representation; không đặt giá trị exposure danh nghĩa hai bộ dữ liệu cạnh nhau để xếp hạng.

## 4.2. Các môi trường dữ liệu và hệ thống chấm điểm

### 4.2.1. Xente
Dữ liệu có 95.662 giao dịch có nhãn, trong đó 193 fraud, với timestamp thực và CustomerId. Chronological logistic baseline ghi nhận PR-AUC validation = **0,560851**, test = **0,892521**. Cách biệt lớn giữa hai giai đoạn cảnh báo rõ rệt rằng kết quả phụ thuộc cấu trúc tín hiệu `Value` và thay đổi phân phối; không khẳng định mô hình được calibrated cho mọi hoàn cảnh. Các thử nghiệm degraded-score trong repository là cấu phần quan trọng của robustness, không phải phụ lục tùy chọn.

### 4.2.2. IEEE-CIS
Dữ liệu 590.540 giao dịch có nhãn; split 70/15/15: train 413.378, validation 88.581 (3.042 fraud), test 88.581 (3.083 fraud). Mô hình streaming SGD(log-loss) được kiểm tra độc lập trên dữ liệu gốc với:
- Validation PR-AUC **0,36438685**, ROC-AUC **0,82181085**, Brier **0,02839840**.
- Test PR-AUC **0,38403028**, ROC-AUC **0,82189958**, Brier **0,03369795**.

Kiểm tra điểm số trên 88.581 test events khi giữ nguyên input thu được maximum absolute error của fast scorer so với baseline **4,3138×10⁻⁷** (ngưỡng chấp nhận 10⁻⁶). Việc này xác minh computational equivalence trên **unchanged stream**, không chứng minh các event gian lận giả lập có phân phối thực tế hay chiến lược của fraudster là thật. IEEE `card1+addr1` là proxy thực thể, không phải CustomerId xác thực.

## 4.3. Thiết kế thực nghiệm và độ mạnh bằng chứng

Shared core: 2 dataset × 2 fraudster mode × 2 policy × 3 capacity ratio = **24 cấu hình**. Frozen routing semantics: validation review-rate tail 1,00%/0,75%/0,50%, direct BLOCK 0,10%, FIFO, congestion triggers 24/72 backlog-hours, capacity ratio 0,75/1,00/1,25, alpha=0,15, epsilon=0,10, dormancy off. Threshold và capacity là **policy/stress choices**, không phải thực nghiệm đo được staffing thực tế.

- **Xente:** 600 full-run observations (12 × 50), kèm targeted sensitivity và 30-seed degraded-score pack. Số seed hỗ trợ count/operational outcomes; value exposure có heavy-tail nên cần báo CI/MCSE.
- **IEEE:** 60 observations (12 × 5) từ **local mirrored execution** trên full held-out test. Cần canonical rerun, replicate nhiều seed, ablations và paired confidence intervals trước khi kết luận chính thức.

## 4.4. Kết quả mô phỏng Xente — 50 seeds

| Fraudster | Policy | Capacity | Fraud interception proxy | Backlog cuối kỳ | Legitimate intervention |
|---|---|---|---:|---:|---:|
| Static | Fixed | Low | 75,84% | 47,12 | 0,965% |
| Static | Capacity-aware | Low | 74,12% | 28,20 | 0,822% |
| Adaptive | Fixed | Low | 59,64% | 52,86 | 0,965% |
| Adaptive | Capacity-aware | Low | 56,44% | 28,00 | 0,805% |
| Static | Fixed | Medium | 79,56% | 30,72 | 0,965% |
| Static | Capacity-aware | Medium | 78,08% | 23,36 | 0,911% |
| Adaptive | Fixed | Medium | 64,40% | 32,68 | 0,965% |
| Adaptive | Capacity-aware | Medium | 61,88% | 24,12 | 0,902% |
| Static | Fixed | High | 81,44% | 24,14 | 0,965% |
| Static | Capacity-aware | High | 82,48% | 19,36 | 0,934% |
| Adaptive | Fixed | High | 66,04% | 25,78 | 0,965% |
| Adaptive | Capacity-aware | High | 66,84% | 19,96 | 0,932% |

**RQ1 (adaptation).** Trong model, Adaptive giảm proxy fraud interception khoảng 14–17 điểm phần trăm so với Static, nhưng làm tăng tỷ trọng chiến lược low-value (Static ~36,8%, Adaptive ~88,7%). Do amount composition giảm, amount exposure có thể thấp hơn dù số lượng fraud bị phát hiện giảm. Vì vậy, “Adaptive nguy hiểm hơn” không được suy ra từ một chỉ số đơn lẻ: *count vs value exposure* có trade-off.

**RQ2 (policy).** Capacity-aware thường giảm backlog và legitimate intervention dưới scarcity. Ví dụ Low/Adaptive: backlog 52,86 → 28,00 và legitimate intervention 0,965% → 0,805%, nhưng interception 59,64% → 56,44%. Đây là bằng chứng quan trọng cho trade-off: giảm hàng chờ không đồng nghĩa với nâng mọi chỉ số gian lận. Lợi ích operational có thể là hệ quả trực tiếp của việc nâng ngưỡng khi quá tải; do đó cần so sánh bổ sung tại cùng effective review budget hoặc định nghĩa rõ **load reduction chính là cơ chế policy**.

**RQ3 (capacity).** Từ Low lên High, tất cả nhánh đều tăng proxy interception và giảm backlog. Cần đánh giá liệu chênh lệch là hiệu ứng model assumption hay còn bền vững khi thay service-time structure; không được suy ra số lượng nhân sự cần tuyển tại ngân hàng.

**Uncertainty.** Báo cáo Xente ghi max relative MCSE khoảng 1,6% cho interception, 1,1% backlog và 7,3% value exposure. Đánh giá value-based có thể cần thêm seed, bootstrapping hoặc phương pháp phù hợp heavy-tail trước khi chốt.

## 4.5. Kết quả IEEE-CIS — full-test 5-seed pilot, CHƯA PHẢI kết quả cuối

| Fraudster | Policy | Capacity | Fraud interception proxy | Backlog cuối kỳ |
|---|---|---|---:|---:|
| Static | Fixed | Low | 14,99% | 478,2 |
| Static | Capacity-aware | Low | 18,19% | 63,6 |
| Adaptive | Fixed | Low | 9,63% | 166,8 |
| Adaptive | Capacity-aware | Low | 10,38% | 21,2 |
| Static | Fixed | Medium | 18,76% | 268,0 |
| Static | Capacity-aware | Medium | 20,82% | 37,4 |
| Adaptive | Fixed | Medium | 11,49% | 17,8 |
| Adaptive | Capacity-aware | Medium | 11,57% | 14,0 |
| Static | Fixed | High | 21,91% | 98,2 |
| Static | Capacity-aware | High | 22,67% | 35,0 |
| Adaptive | Fixed | High | 11,73% | 3,2 |
| Adaptive | Capacity-aware | High | 11,73% | 3,2 |

**RQ1 (pilot).** Adaptive chuyển mạnh sang high-amount regime: share trung bình 92,84% so với Static 31,66%. Khác hướng với Xente. Cơ chế có thể xuất phát từ reward amount-weighted, detector discrimination, validation donors và policy response, nhưng bảng pilot **không thể tự nhận diện nguyên nhân nhân quả**. Đặc biệt, một seed đơn khi thay reward sang unit-per-success giảm high-amount share từ 93,29% xuống 83,49%, cho thấy reward functional form là giả định có khả năng ảnh hưởng tới kết luận; cần nhiều seed/nhánh hơn.

**RQ2 (pilot).** Low/Static, Capacity-aware giảm backlog 478,2 → 63,6 trong khi interception proxy tăng 14,99% → 18,19%. Low/Adaptive, backlog giảm 166,8 → 21,2, interception tăng từ 9,63% → 10,38%. Khác biệt interception là pilot contrast, không gắn dấu hiệu thống kê cho đến khi có paired intervals.

**RQ3 (pilot).** Nhìn chung giảm backlog khi capacity cao hơn. Một số Adaptive/High cells đạt backlog trung bình 3,2 và proxy interception ngang nhau giữa hai policies; khi không quá tải, Capacity-aware có thể ít tác động. Không được suy rộng ra vận hành ngân hàng thực.

**RQ4 (pilot cross-scenario).** Tỷ trọng strategy thích nghi thay đổi **ngược chiều** giữa hai môi trường theo mô hình hiện tại: low-amount Xente vs high-amount IEEE. Dữ liệu không chứa observations về cách fraudster học khi nhận REVIEW/BLOCK, vì vậy đây là **scenario-dependent model behavior** chứ không phải chứng cứ sinh thái học hoặc tâm lý tội phạm. Cùng nhau, hai môi trường chứng minh cần thận trọng khi diễn giải chính sách theo một dataset.

## 4.6. Bài học về validity, ablation và hàm ý phương pháp

### 4.6.1. Outcome definition là một phần của kết luận
Legacy interception proxy = BLOCK + REVIEW whose service starts in horizon. Độ nhạy q tính hoàn tất review và giả định review effectiveness; với `q=0`, chỉ BLOCK trực tiếp mới đủ điều kiện prevented, với `q=1`, fraud review hoàn tất được gán hiệu quả 100% *trong giả định*. Cần tránh dùng “prevented loss” không định nghĩa rõ. Pending review ở horizon vẫn là unresolved exposure chứ không tự động hiện thực tổn thất.

### 4.6.2. Review feedback có khả năng không quan sát được
Core cập nhật ngay khi policy chọn REVIEW. IEEE one-seed pilot ablation bỏ quan sát REVIEW không đổi chỉ số; một seed không đủ để khẳng định feedback không quan trọng. Cần nhiều seed, thay điều kiện congested và kiểm tra share/CI. Không mô tả `no_review_observation` là a realistic delayed feedback model.

### 4.6.3. Cấu trúc generator và vấn đề đối chứng
Xente generator dùng synthetic `CustomerId=SIM_FRAUDSTER` cho tất cả generated frauds, tạo shared history có thể ảnh hưởng velocity score. IEEE có proxy-specific contexts. Phải thảo luận asymmetry này trong validity; đề xuất structural ablation thay identity persistence và kiểm tra liệu low/high regime switching có còn ổn định.

### 4.6.4. Bất định và độ vững
McCulloch et al. (2022) lưu ý parameter, structural/model discrepancy, observation và stochastic uncertainties. Ở khóa luận này: parameters alpha/epsilon/congestion/q; model discrepancy gồm reward design/identity/observability/queue rule; observation uncertainty gồm fraud labels, proxy/missingness; stochastic uncertainty từ donor sampling và epsilon exploration. Monte Carlo CI **chỉ mô tả seed uncertainty conditional on giả định đã cố định**, không phải interval cho toàn bộ uncertainty ngoài đời.

## 4.7. Liên hệ nghiên cứu trước và đóng góp

Shen & Kurshan (2020) nghiên cứu điều chỉnh alert thresholds theo năng lực xử lý; do đó năng lực capacity-aware threshold không phải đề xuất hoàn toàn chưa từng có. Đóng góp dự kiến của khóa luận là *khung thử nghiệm tương tác endogenously generated/adaptive fraud attempts – frozen empirical detector – operational policy – finite analyst queue*, sự khác biệt conditional giữa hai empirical environments và minh bạch về assumptions. Đây là mô tả đóng góp **trong phạm vi implementation hiện tại**, không phải khẳng định độc nhất tuyệt đối sau systematic review.

Höppner et al. (2022) nhấn mạnh bài toán tổn thất phụ thuộc transaction; khóa luận minh họa vì sao count interception và value exposure có thể cho diễn giải khác nhau. Grimm et al. (2020) định hướng đặc tả ODD; McCulloch et al. (2022) định hướng phân lớp bất định. Các tài liệu này hỗ trợ framework chứ không hiệu chuẩn được learning rate hoặc analyst service throughput.

## 4.8. Kết luận tạm thời

**Từ Xente 50-seed core:** (i) adaptation làm thay đổi thành phần các fraud attempts và hiệu quả đếm được; (ii) policy capacity-aware giảm backlog/intervention trong nhiều điều kiện nhưng không luôn tăng interception; (iii) analyst capacity là một nhân tố điều tiết thiết yếu.  
**Từ IEEE 5-seed pilot:** mô hình có khả năng tái tạo một môi trường dữ liệu khác với dấu hiệu strategy response khác Xente, nhấn mạnh environment dependence, nhưng **chưa thể đưa ra kết luận cuối về IEEE/cross-scenario**.

**Điều kiện khóa chương:** (A) canonical IEEE runner reproduces 5-seed outputs; (B) tăng N và paired 95% CI/MCSE, riêng heavy-tail; (C) review reward/feedback/identity/score ablations; (D) xác nhận outcome semantics và các bảng dựa trên output có thể kiểm tra; (E) bổ sung bảng/biểu đồ sau thẩm định của GVHD.

## Nguồn trong dự án và học thuật
- `05 Experiments/Xente Feature-Level Core Run v0.2.md`; `05 Experiments/Xente Feature-Level Sensitivity v0.1.md`.
- `05 Experiments/IEEE-CIS Adaptive Full-Test Pilot v0.2.md`; `05 Experiments/IEEE-CIS Baseline and Policy Replay v0.1.md`.
- `03 Model design/ODD Hybrid ABM-DES Specification v1.0.md`; `03 Model design/Validation Plan v1.0.md`.
- Shen, H., & Kurshan, E. (2020). *Deep Q-Network-based Adaptive Alert Threshold Selection Policy for Payment Fraud Systems in Retail Banking*. https://doi.org/10.1145/3383455.3422563
- Grimm, V., et al. (2020). *The ODD Protocol...* https://doi.org/10.18564/jasss.4259
- McCulloch, J., et al. (2022). *Calibrating Agent-Based Models Using Uncertainty Quantification Methods*. https://doi.org/10.18564/jasss.4791
- Höppner, S., et al. (2022). *Instance-dependent cost-sensitive learning for detecting transfer fraud*. https://doi.org/10.1016/j.ejor.2021.05.028
