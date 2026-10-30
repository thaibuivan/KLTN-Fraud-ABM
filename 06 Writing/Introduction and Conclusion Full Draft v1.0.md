# DỰ THẢO MỞ ĐẦU VÀ KẾT LUẬN — v1.0 (18/10/2026)

**Trạng thái:** Sẵn sàng đưa GVHD góp ý về framing; phần kết luận là **kết luận tạm thời với IEEE pilot 5 seeds**, không được nộp dưới dạng chứng cứ IEEE cuối khi chưa có full canonical convergence.

# CHƯƠNG 1. MỞ ĐẦU

## 1.1. Đặt vấn đề

Giao dịch số tạo ra những luồng thông tin cần được sàng lọc rủi ro trong thời gian và nguồn lực vận hành hữu hạn. Trong nghiên cứu fraud detection, kết quả thường được báo qua phân loại đúng/sai, PR-AUC hoặc ROC-AUC. Song ngân hàng và các đơn vị trung gian thanh toán cần đưa ra hành động: cho phép, chuyển kiểm tra hoặc chặn giao dịch. Mỗi hành động ảnh hưởng khác nhau tới khả năng can thiệp các trường hợp gian lận, trải nghiệm giao dịch hợp lệ và số lượng cảnh báo cần chuyên viên xử lý. Chính vì vậy, cải thiện một thước đo dự báo chưa đủ để kết luận chính sách vận hành tốt hơn.

Năng lực kiểm tra hữu hạn khiến cùng một detector có thể tạo ra những kết quả hệ thống khác nhau dưới các chính sách định tuyến. Shen và Kurshan (2020) xem xét lựa chọn ngưỡng cảnh báo thích nghi trong payment fraud systems dựa trên khả năng xử lý, gợi ý rằng bài toán cần được đặt ở tầng downstream decision policy thay vì chỉ tối ưu fraud score. Đồng thời, kết quả fraud không chỉ là số lượng sự kiện phát hiện: theo khung instance-dependent cost-sensitive của Höppner et al. (2022), giá trị và tổn thất tiềm tàng giữa các giao dịch có thể khác nhau đáng kể.

Một khó khăn khác là các giao dịch nghi ngờ và phản ứng của hệ thống có thể ảnh hưởng đến môi trường rủi ro trong tương lai. Nếu đối tượng gian lận thay đổi cơ cấu hành vi sau khi nhận phản hồi, hiệu quả chính sách đánh giá trên một fraud stream cố định có thể khác với hiệu quả trong một stress scenario có feedback. Tuy nhiên, dữ liệu gian lận công khai chủ yếu ghi nhận giao dịch và nhãn, không trực tiếp quan sát được sự học hỏi, động cơ hay phản hồi của từng fraudster. Do đó, một mô hình mô phỏng cần công khai những cơ chế chỉ là giả định và kiểm tra mức độ nhạy với chúng; không được tuyên bố mô phỏng là một ngân hàng số thực tế.

Trong bối cảnh đó, khóa luận phát triển khung mô phỏng kết hợp thành phần tác tử có lựa chọn chiến lược thích nghi với mô-đun ra quyết định và hàng đợi theo sự kiện. Đóng góp hướng đến **đánh giá tương tác và trade-off theo điều kiện**, không phát minh một detector mới hay chứng minh một loại chiến lược fraudster có tồn tại ngoài thực tế.

## 1.2. Mục tiêu nghiên cứu

Mục tiêu chung là xây dựng và kiểm định một môi trường thí nghiệm có empirical grounding để so sánh chính sách quản lý gian lận giao dịch khi cơ chế sinh giao dịch gian lận có thể phản ứng với quyết định của hệ thống và năng lực chuyên viên xử lý cảnh báo có giới hạn.

Mục tiêu cụ thể:
1. Chuyển đặc điểm transaction/environment từ hai bộ dữ liệu công khai thành cấu phần đầu vào mô phỏng có quy tắc chronological và nguồn gốc tham số minh bạch.
2. Đặc tả vòng tương tác giữa fraudster strategy, frozen detector, policy, persistent alert queue và feedback.
3. Đánh giá hiệu ứng Static/Adaptive, Fixed/Capacity-aware và Low/Medium/High capacity trên các chỉ tiêu gian lận, giao dịch hợp lệ và workload.
4. Xác định những kết quả ổn định và phụ thuộc bối cảnh, thông qua repeated-seed comparisons, alternative reward/feedback/outcome semantics và structural sensitivity.
5. Trình bày giới hạn suy luận, đặc biệt khoảng cách từ mô hình mô phỏng tới loss prevention và bank-specific deployment.

## 1.3. Câu hỏi nghiên cứu

- **RQ1 — Adaptation:** Khi cơ chế lựa chọn chiến lược gian lận có thể cập nhật từ phản hồi của hệ thống, thành phần fraud attempts và các metrics fraud-management thay đổi thế nào so với static empirical mixture?
- **RQ2 — Policy:** Chính sách Fixed-threshold và Capacity-aware tạo ra các trade-off như thế nào giữa fraud interception proxy, intervention và tắc nghẽn?
- **RQ3 — Capacity:** Sự khác biệt giữa các chính sách phụ thuộc thế nào vào năng lực xử lý Low/Medium/High?
- **RQ4 — Robustness:** Những hiệu ứng và thứ hạng chính sách có ổn định giữa Xente và IEEE-CIS hay chỉ đúng trong từng môi trường thực nghiệm và tập giả định?

RQ được đặt theo dạng khám phá/đối sánh để tránh gán sẵn Capacity-aware là tối ưu. Một phát hiện policy ranking không ổn định cũng có thể có giá trị học thuật.

## 1.4. Đối tượng và phạm vi

**Đối tượng:** Cơ chế chính sách quyết định xử lý cảnh báo và đầu ra hệ thống quản lý rủi ro gian lận giao dịch. Không nghiên cứu nhận dạng cá nhân tội phạm, không dự báo exact cognition, không cung cấp khuyến nghị vận hành cho ngân hàng cụ thể.

**Dữ liệu:** Xente với CustomerId/timestamp/Amount/Value/product/channel; IEEE-CIS với relative time/TransactionAmt/ProductCD/card/address/device/identity context. Hai môi trường độc lập, không ghép bảng và không chuẩn hóa raw amount thành một đơn vị tài chính chung. `card1+addr1` là entity proxy của IEEE, không phải customer identity được xác nhận.

**Mô hình:** Detector riêng cho từng scenario, học trên train và frozen trước test; fraud strategy generator dựa vào validation donor regimes; static/adaptive fraudster; Fixed/Capacity-aware; pooled FIFO analyst queue và deterministic baseline service. Số lần thử fraud cố định theo test-fraud attempt slots — một điều kiện hóa của stress design. Hạn chế: không mô hình hóa arrival intensity của gian lận như một stochastic endogenous process độc lập.

**Thực nghiệm chính:** 2 × 2 × 2 × 3 = 24 core configurations; replication theo seed và phân tích sensitivity không nhân vào core grid.

**Khía cạnh đạo đức và bảo mật:** Sử dụng dữ liệu và bài báo được công khai hợp pháp. Không đưa tài liệu, dữ liệu khách hàng, thresholds, dashboards hoặc facts nội bộ Green SM vào bản nộp/GitHub nếu chưa có phê duyệt của công ty cho mục đích nghiên cứu và công bố. Không cần dữ liệu Green SM để hoàn thành luận văn.

## 1.5. Phương pháp nghiên cứu

Phương pháp chính là mô phỏng có thành phần agent-based cho hành vi đối kháng và discrete-event cho policy/queue, với empirical risk scoring được đóng băng theo chronological splits. Bộ quy trình gồm (1) EDA và time-safe modeling, (2) scenario-specific generated fraud context and online scoring, (3) shared policy and finite service queue, (4) repeated-seed comparisons and uncertainty, (5) conceptual/empirical/output/structural validation.

ODD (Grimm et al., 2020) là tiêu chuẩn mô tả cấu trúc. Khung bất định của McCulloch et al. (2022) định hướng phân biệt tham số ước lượng từ dữ liệu, giả định về hành vi, rủi ro cấu trúc mô hình và biến thiên seed. Model-vs-data validation kiểm tra nhiều patterns thay vì kết luận mô hình đúng nếu chỉ khớp một chỉ số.

## 1.6. Đóng góp kỳ vọng

**Về phương pháp:** Một môi trường policy stress-testing có fraudster feedback, finite queue và frozen empirical risk scoring, đặc tả/reproducibility ở mức có thể kiểm tra.  
**Về thực nghiệm:** Thiết kế đối chứng có hệ thống để phân tích `behavior × policy × capacity` trong hai transaction environments bổ sung nhau.  
**Về đánh giá:** Làm rõ những metric trade-offs và điều kiện làm thay đổi chiều hiệu ứng; báo những giới hạn của giả định review/amount/behavior một cách trung thực.  
**Không claim:** “lần đầu có adaptive threshold”, “mô hình hiểu hành vi kẻ gian lận thật”, “tối ưu số chuyên viên ngân hàng” hoặc “đã lượng hóa tổn thất ngân hàng thực”.

## 1.7. Bố cục khóa luận

Chương 1 trình bày bối cảnh, mục tiêu, phạm vi, RQ. Chương 2 tổng quan literature về fraud decision, human-capacity, ABM và validation. Chương 3 trình bày dữ liệu Xente/IEEE, quy tắc xây features, agent/policy/queue design, thí nghiệm và uncertainty. Chương 4 trình bày empirical baseline, Xente main, IEEE pilot→main khi validated, contrasts/robustness và thảo luận. Chương 5 kết luận, đóng góp và giới hạn.

# CHƯƠNG 5. KẾT LUẬN — BẢN TẠM THỜI CHƯA KHÓA

## 5.1. Tổng kết nghiên cứu trong phạm vi bằng chứng hiện tại

Khóa luận đã hình thành khung mô phỏng quản lý gian lận có fraudster chiến lược, hệ thống chấm điểm rủi ro, policy và hàng đợi cảnh báo persistent. Hai môi trường Xente và IEEE-CIS được parameterize độc lập để kiểm tra liệu kết luận vận hành có phụ thuộc vào dữ liệu và cơ chế sinh fraud hay không. Khác với chỉ tối ưu classifier, mô hình phân tích nhiều chiều: count interception proxy, value exposure at finite horizon, customer intervention và workload/backlog.

**Xente (candidate core 12 × 50 seeds):** adaptive mechanism làm thay đổi phân phối low/middle/high amount regimes; các chỉ số interception count và exposure value không nhất thiết di chuyển cùng chiều; capacity-aware thường giảm backlog dưới scarcity, còn ưu thế về fraud interception có tính điều kiện. Đây là các kết quả trong mô hình Xente-grounded, không phải bằng chứng về chiến lược của fraudster thực tế.

**IEEE (12 × 5 seeds preliminary pilot):** một số hiệu ứng policy/backlog được quan sát trong full-test local pilot, và chiến lược thích nghi có thể chuyển về high-amount regime — ngược chiều Xente. Nhưng vì chỉ 5 seeds và chưa canonical-runner replay từ artifact lưu riêng, **chưa được xem là kết luận cuối cho IEEE hoặc RQ4**.

## 5.2. Hàm ý

Một chính sách giảm backlog có thể làm thay đổi số cảnh báo được tiếp nhận và cấu phần gian lận bị quan sát; vì vậy chọn chính sách chỉ theo fraud-count interception hoặc backlog riêng rẽ có thể gây hiểu sai. Hệ thống đánh giá nên báo song song gian lận ở từng trạng thái APPROVE/REVIEW/BLOCK, legitimacy intervention và service delay. Những hàm ý này chỉ là phương pháp đánh giá trong **môi trường nghiên cứu giả lập**, không phải khuyến nghị áp dụng threshold hay tuyển thêm staffing trong thực tế.

## 5.3. Giới hạn

- Không quan sát được thích nghi chiến lược của fraudster trong datasets; epsilon-greedy/reward/REVIEW feedback là giả định.
- Fraud generator dựa trên validation fraud rows và three amount regimes, có thể thiếu mode chưa thấy; Xente synthetic fraud history tập trung vào một ID, IEEE entity proxy không phải customer thật.
- Outcome metric mặc định tính service start như interception; prevention và recovery không có quan sát gốc. `q` là sensitivity assumption, không phải xác suất ngăn ngừa do ngân hàng cung cấp.
- Frozen risk score quality thay đổi theo thời gian; Xente legitimate risk scores trong loop giữ nguyên là một approximation, trong khi IEEE replay đã dùng updated online scores.
- Relative capacity và backlog thresholds không phản ánh staffing hay SLA của ngân hàng xác định.
- Seed CI đo stochastic variation conditional on model choices; structural/model-discrepancy uncertainty cần các ablations độc lập.
- Hai datasets khác nhau về công nghệ, feature semantics, fraud mix và thời gian; raw monetary exposure không đối chiếu trực tiếp.

## 5.4. Hướng hoàn thiện trước kết luận cuối

1. Reproduce IEEE pilot bằng canonical code trên artifact riêng tư; lưu seed/commit SHA/checksum; không upload data vào public GitHub.
2. Chạy đủ IEEE seeds để so paired contrasts/CI/MCSE, gồm value heavy-tail; phân tích reward/feedback/score/identity structural sensitivity.
3. Đối chiếu outcome giả định service-start với completion-only review q, định nghĩa từng metric.
4. Hoàn thiện Figure/Table/Appendix và Literature References, nhận phản biện GVHD, điều chỉnh diễn giải theo evidence.
5. Sau khi hoàn thành, thay thế các đoạn nói **pilot/chưa đủ** bằng kết quả final được tái lập; không sửa giả thuyết tùy tiện để khớp kết quả.

## Tài liệu tham khảo minh họa
- Shen, H., & Kurshan, E. (2020). https://doi.org/10.1145/3383455.3422563.
- Höppner, S., et al. (2022). https://doi.org/10.1016/j.ejor.2021.05.028.
- Grimm, V., et al. (2020). https://doi.org/10.18564/jasss.4259.
- McCulloch, J., et al. (2022). https://doi.org/10.18564/jasss.4791.
- Alves, J. V., et al. (2025). https://doi.org/10.1038/s41597-025-04664-y.
- Ding, N., et al. (2025). https://doi.org/10.1016/j.eswa.2025.127995.

**Editor check:** đoạn Conclusion hiện là provisional; không đổi thành finalized thesis chapter khi chưa qua các hard gates nêu tại `00 Dashboard/THESIS LOCK GATES - 2026-10-18.md`.
