# CHƯƠNG 5 — KẾT QUẢ THỰC NGHIỆM VÀ THẢO LUẬN (BẢN THẢO LÀM VIỆC v1.0)

> **Tình trạng:** Xente là candidate main 50-seed; IEEE hiện chỉ là empirical **5-seed pilot** và chưa có nghiệm thu reproducing bằng canonical repo runner. Nội dung chương này phục vụ tiếp tục viết luận văn, **không được nộp như final inference** trước IEEE repeated-seed/convergence và validation. Đọc cùng `Methodology Full Draft v1.1`.

## 5.1. Mở đầu chương

Chương này đánh giá tác động của hành vi gian lận giả định, chính sách điều chỉnh ngưỡng và nguồn lực chuyên viên đối với đầu ra của một hệ thống quản lý cảnh báo được mô phỏng. Phân tích được tiến hành trên hai môi trường độc lập Xente và IEEE-CIS theo cùng thiết kế nhân tố: StaticMixture/Adaptive, Fixed-threshold/Capacity-aware, Low/Medium/High normalized capacity. Các chỉ số được xét đồng thời gồm tỷ lệ *model-defined fraud intercepted* (BLOCK hoặc REVIEW bắt đầu phục vụ trước horizon), giá trị fraud exposure tại horizon theo quy ước mô hình, tỷ lệ can thiệp giao dịch hợp lệ và mức backlog.

Việc dùng nhiều đầu ra là cần thiết vì một thay đổi policy có thể làm giảm queue nhưng đồng thời tăng/giảm khả năng review các trường hợp gian lận. Tương tự, chuyển phân bố fraud attempts sang giá trị nhỏ hơn có thể làm fraud-count interception xấu đi nhưng amount exposure giảm. Không kết luận chính sách “tốt nhất” từ một chỉ số riêng lẻ.

## 5.2. Khả năng phân biệt gian lận của mô-đun chấm điểm

**Xente.** Mô hình logistic baseline với đặc trưng past-only có PR-AUC khoảng 0,560851 trên validation và 0,892521 trên test, trong bối cảnh fraud prevalence rất thấp. Độ khác biệt lớn giữa validation và test cần được hiểu trong bối cảnh phân bố gian lận theo thời gian và tín hiệu Value mạnh; việc cải thiện PR-AUC trên test không tự chứng minh mô hình ổn định trong môi trường khác.

**IEEE-CIS.** SGDClassifier log-loss với chronological entity history được tái lập trên dữ liệu labeled. Validation PR-AUC 0,36438685; test 0,38403028; ROC-AUC xấp xỉ 0,8218/0,8219. Brier score validation 0,02839840, test 0,03369795; mean score/test calibration đã có dấu hiệu thay đổi. Do khác biệt fraud prevalence và feature space, không so trực tiếp PR-AUC giữa hai tập như một thước đo duy nhất về chất lượng policy.

Kết quả đầu vào chứng minh khả thi cho việc kiểm tra chính sách dưới hai distributional environments, **không** chứng minh risk models có khả năng phòng ngừa gian lận thực tế.

## 5.3. Xente — Thực nghiệm chính 12 cấu hình × 50 seeds

Bảng 5.1 tổng hợp các chỉ số trung bình được ghi trong `Xente Feature-Level Core Run v0.2`:

| Fraudster | Policy | Capacity | Interception proxy (%) | Exposure at horizon (Xente Value units) | Backlog cuối | Can thiệp hợp lệ (%) |
|---|---|---:|---:|---:|---:|---:|
| Static | Fixed | Low | 75.84 | 2,679,456 | 47.12 | 0.965 |
| Static | Capacity-aware | Low | 74.12 | 2,648,056 | 28.20 | 0.822 |
| Static | Fixed | Medium | 79.56 | 2,143,456 | 30.72 | 0.965 |
| Static | Capacity-aware | Medium | 78.08 | 2,160,056 | 23.36 | 0.911 |
| Static | Fixed | High | 81.44 | 1,840,456 | 24.14 | 0.965 |
| Static | Capacity-aware | High | 82.48 | 1,458,056 | 19.36 | 0.934 |
| Adaptive | Fixed | Low | 59.64 | 1,215,327 | 52.86 | 0.965 |
| Adaptive | Capacity-aware | Low | 56.44 | 1,250,347 | 28.00 | 0.805 |
| Adaptive | Fixed | Medium | 64.40 | 964,327 | 32.68 | 0.965 |
| Adaptive | Capacity-aware | Medium | 61.88 | 1,002,347 | 24.12 | 0.902 |
| Adaptive | Fixed | High | 66.04 | 861,327 | 25.78 | 0.965 |
| Adaptive | Capacity-aware | High | 66.84 | 714,347 | 19.96 | 0.932 |

*Lưu ý bảng:* “Exposure at horizon” là amount proxy trong điều kiện mô phỏng; không phải tổn thất tài chính thực. Các trung bình theo 50 seeds không phải confidence intervals. Số liệu phải được xuất lại từ canonical run-level CSV trước bản cuối.

### 5.3.1. RQ1 — Phản ứng của fraudster thích nghi

Trung bình, regime low-value xuất hiện khoảng **36,8%** trong StaticMixture và **88,7%** trong Adaptive. Với cùng loại policy/capacity, tỉ lệ interception proxy của Adaptive thấp hơn Static khoảng **14–17 điểm phần trăm**. Đây là phản ứng của learning mechanism với regime pools và quy tắc reward, không cho phép kết luận trực tiếp về nhận thức của fraudsters trên Xente.

Một kết quả đáng lưu ý là amount exposure của Adaptive trong bảng thấp hơn Static, mặc dù interception theo số lượng giảm. Hai kết quả không mâu thuẫn về toán học: thành phần giao dịch được lựa chọn có giá trị khác nhau. Vì vậy, phải tách metric *số lượng fraud được can thiệp* và *tổng Value trong các sự kiện chưa được ngăn theo quy ước mô phỏng*.

### 5.3.2. RQ2 — Đánh đổi của chính sách Capacity-aware

So với Fixed, Capacity-aware làm giảm backlog ở cả ba mức capacity và cả hai chế độ Static/Adaptive; mức giảm lớn nhất xuất hiện trong điều kiện Low capacity. Ví dụ, Adaptive-Low giảm từ **52,86** xuống **28,00** cases backlog, trong khi interception proxy giảm từ **59,64%** xuống **56,44%**. Đây là minh họa rõ cho trade-off giữa giảm tắc nghẽn và năng lực phát hiện trong phạm vi một thiết kế queue/policy xác định.

Ở điều kiện Static-High, Capacity-aware có thể tăng nhẹ interception (81,44% → 82,48%); trong Adaptive-Low lại giảm. Vì vậy, mô hình **không hỗ trợ** tuyên bố Capacity-aware luôn tốt hơn về fraud interception. Khi viết kết luận cuối, dùng paired confidence intervals và xem xét sự khác biệt có phân biệt được khỏi stochastic variation hay không.

### 5.3.3. RQ3 — Tác động của capacity

Tăng capacity từ Low lên High nhìn chung giảm backlog và nâng interception proxy, phù hợp với việc nhiều alert được phục vụ trong observation horizon. Tuy nhiên, đây một phần là hệ quả trực tiếp của cách định nghĩa finite service capacity, nên ý nghĩa nghiên cứu nằm ở *độ lớn và sự biến đổi policy effects*, thay vì chỉ phát biểu “capacity càng lớn càng ít tồn đọng”.

### 5.3.4. Monte Carlo uncertainty

Trong báo cáo Xente core, relative MCSE tối đa khoảng **1,6%** cho interception, **1,1%** backlog, **0,3%** legitimate intervention và **7,3%** amount exposure. Sự bất định lớn hơn của amount exposure yêu cầu trình bày intervals và/hoặc distributional plots; không chỉ đưa trung bình.

## 5.4. Xente — Các kiểm định độ nhạy và điểm yếu cần diễn giải

Một kiểm định dùng risk model không có tín hiệu current-Value quan trọng đã giảm PR-AUC (validation khoảng 0,205; test khoảng 0,389) và chạy lại **12 cấu hình × 30 seeds**. Tác tử Adaptive vẫn ưu tiên low-value, xấp xỉ **81–82%** thay vì **88–89%** ở full-score. Capacity-aware vẫn giảm backlog, nhưng policy effect lên interception thay đổi đáng kể: trong môi trường degraded-score ở chế độ Adaptive, báo cáo ghi mức tăng interception theo Capacity-aware khoảng **+1,7 / +5,6 / +4,7 điểm phần trăm** ở Low/Medium/High.

Điều này làm nổi bật **sự phụ thuộc của kết luận fraud-related policy effects vào chất lượng và cấu trúc risk score**, dù lợi ích giảm congestion có thể duy trì.

Các kiểm định còn lại cho thấy: thay BLOCK threshold làm thay đổi nhiều exposure; thay exploration `epsilon` làm thay đổi mức đa dạng chiến lược; thay congestion triggers thay đổi backlog và can thiệp hợp lệ. Vì vậy các giá trị trung tâm đóng băng không phải “đúng” hoặc “tối ưu” theo dữ liệu ngân hàng. Chúng chỉ là lựa chọn kịch bản đã được kiểm tra trong một số lân cận.

## 5.5. IEEE-CIS — Kết quả pilot 12 cấu hình × 5 seeds

**Cảnh báo phân loại bằng chứng:** Bảng sau là *pilot*, chưa phải IEEE final main experiment. Đã có tái lập baseline và score equivalence trên 88.581 event test được ghi nhận; tuy nhiên full pilot hiện được tạo bằng local execution mirroring repo logic. Việc tái chạy qua đúng canonical runner và tăng seeds là **hard gate**.

| Fraudster | Policy | Capacity | Interception proxy (%) | Backlog cuối |
|---|---|---:|---:|---:|
| Static | Fixed | Low | 14.99 | 478.2 |
| Static | Capacity-aware | Low | 18.19 | 63.6 |
| Adaptive | Fixed | Low | 9.63 | 166.8 |
| Adaptive | Capacity-aware | Low | 10.38 | 21.2 |
| Static | Fixed | Medium | 18.76 | 268.0 |
| Static | Capacity-aware | Medium | 20.82 | 37.4 |
| Adaptive | Fixed | Medium | 11.49 | 17.8 |
| Adaptive | Capacity-aware | Medium | 11.57 | 14.0 |
| Static | Fixed | High | 21.91 | 98.2 |
| Static | Capacity-aware | High | 22.67 | 35.0 |
| Adaptive | Fixed | High | 11.73 | 3.2 |
| Adaptive | Capacity-aware | High | 11.73 | 3.2 |

Trong pilot IEEE, high-amount strategy share trung bình khoảng **31,66%** đối với Static và **92,84%** đối với Adaptive. Hướng chọn strategy này ngược với kết quả low-value dominance trong Xente. Có thể cả reward-by-amount, score/regime distributions và phản hồi policy góp phần giải thích; chưa thể biết phần nào là cơ chế bền vững nếu chỉ qua 5 seeds.

Dữ liệu pilot cũng cho thấy Capacity-aware giảm backlog đặc biệt mạnh ở Low capacity. Nhưng trong IEEE pilot, việc Adaptive có high-amount share lớn lại đi kèm backlog thấp hơn Static ở một số điều kiện, nên không thể diễn giải “Adaptive luôn tạo áp lực vận hành lớn hơn”. Hai biến cần được so sánh tách rời với amount/value exposure, review routing và BLOCK counts.

**Một seed ablation chưa đủ để kết luận**: trong seed 0, đổi reward thành unit-per-success proxy làm high-amount share giảm từ khoảng 93,29% xuống 83,49%; no-review-observation trong thử nghiệm đó không làm đổi các output đã ghi. Đây là bằng chứng gợi ý cần nghiên cứu reward sensitivity, không phải chứng minh robustness.

## 5.6. RQ4 — Đối chiếu Xente và IEEE-CIS (nhận định sơ bộ)

Hiện có một đối chiếu **mang tính giả thuyết/định hướng**:

1. Trong cả hai environments đã quan sát được, mức capacity và chính sách phân luồng ảnh hưởng mạnh đến backlog.
2. Hành vi Adaptive thay đổi strategy mix đáng kể trong cả hai; nhưng **chiều thay đổi amount regime khác nhau**: Xente ưu tiên low-value, IEEE pilot ưu tiên high-value.
3. Sự khác nhau về fraud prevalence, quan hệ score–amount và feature context có thể khiến policy performance không chuyển giao nguyên xi giữa datasets.
4. Không gộp observations hay so tiền thô qua Xente/IEEE. Với IEEE mới có 5 seeds, mọi phát biểu “consistent/environment-dependent” phải là **provisional** cho tới khi chạy lại canonical, có intervals và sensitivity.

Lưu ý đặc biệt: dùng chung learning rule, reward normalization và policy semantics không có nghĩa hai empirical environments tương đương thống kê. Khác biệt giữa hai miền dữ liệu chính là đối tượng của robustness test.

## 5.7. Rủi ro nội tại và đề xuất kiểm định trước khi chốt kết luận

- **Interception ≠ prevention:** main metric ghi fraud được BLOCK hoặc REVIEW bắt đầu trước horizon. Cần xuất bảng tách trực tiếp block, service start, service completion, unresolved và q-sensitivity.
- **Immediate REVIEW observability:** nếu REVIEW chỉ là xử lý nội bộ, feedback ngay là một giả định mạnh. Phải chạy nhiều seeds của biến thể `no_review_observation` và nếu khả thi mô hình delayed-feedback.
- **Reward-induced strategy shift:** kiểm định value-scaled vs unit reward ở cùng môi trường, alpha/epsilon và matched seeds.
- **Policy mechanical effect:** theo dõi review budget, interception per review, legitimate intervention và backlog đồng thời. Giảm alert routing có thể làm backlog giảm ngay cả khi policy không “thông minh” hơn.
- **Horizon dependence:** kết quả với REVIEW còn pending phải nhạy với observation horizon và service-completion assumptions; không biến pending thành realized loss.
- **Code/empirical equivalence:** canonical runner phải tái lập pilot, lưu SHA256 of result artifacts và version/seed information.

## 5.8. Kết luận tạm của chương

Các kết quả Xente 50-seed cho thấy một hệ thống policy không thể được đánh giá tách khỏi cơ chế tạo fraud attempts và trạng thái nguồn lực. Adaptive thay đổi mức độ can thiệp theo số lượng và composition, trong khi Capacity-aware làm thay đổi rõ tải công việc nhưng hiệu quả fraud-related phụ thuộc điều kiện. IEEE 5-seed pilot đưa ra một dấu hiệu đáng chú ý về sự khác biệt giữa environments, nhưng chưa đủ để nâng thành kết luận khoa học chính thức.

**Để hoàn tất chương 5**, thay các số liệu IEEE pilot bằng output canonical repeated-seed, thêm t-intervals/MCSE và plots; bổ sung outcome q-sensitivity/reward-feedback ablations có intervals; chốt bảng cross-scenario effect-by-capacity và kiểm tra lại toàn bộ con số với artifact lưu vết.

## Nguồn kết quả nội bộ của repository (không phải chứng cứ hoạt động ngân hàng)

- `05 Experiments/Xente Feature-Level Core Run v0.2.md`.
- `05 Experiments/Xente Feature-Level Degraded-Score Robustness v0.1.md`.
- `05 Experiments/Xente Feature-Level Sensitivity v0.1.md`.
- `05 Experiments/IEEE-CIS Adaptive Full-Test Pilot v0.2.md`.
- `05 Experiments/IEEE-CIS Baseline and Policy Replay v0.1.md`.
- `06 Writing/Methodology Full Draft v1.1.md`.

> **Thận trọng phương pháp:** Bản này dùng các số trung bình từ các báo cáo đã lưu trong repo; tôi chưa độc lập tái thực thi toàn bộ IEEE chính thức ở lần biên tập này. Những chữ “candidate”, “pilot” và “conditional” phải được giữ trong mọi bản trình bày trước khi nghiệm thu cổng dữ liệu/runner/seeds.
