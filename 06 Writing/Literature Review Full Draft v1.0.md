# CHƯƠNG TỔNG QUAN NGHIÊN CỨU — BẢN THẢO v1.0 (18/10/2026)

> **Mục đích:** định vị khoảng trống nghiên cứu của KLTN Fraud-ABM mà không tuyên bố những đóng góp đã được công bố là mới tuyệt đối. Đây là narrative literature review có định hướng, không phải systematic review; bổ sung đối chiếu toàn văn/tài liệu định lượng trước bản nộp.

## 2.1. Phát hiện gian lận: từ điểm số dự báo đến quyết định vận hành

Phần lớn pipeline xử lý gian lận giao dịch bắt đầu từ mô hình rủi ro, sau đó chuyển điểm số thành hành động đối với giao dịch hoặc cảnh báo. Tuy nhiên, thứ tự ưu tiên theo AUC/PR-AUC của một detector không tự động cho biết hệ thống vận hành nào giảm thiểu trade-off tổng thể tốt hơn: cảnh báo quá nhiều có thể làm quá tải lực lượng xử lý, trong khi ngưỡng chặt hơn có thể tăng số giao dịch gian lận bỏ qua hoặc thay đổi trải nghiệm khách hàng. Do đó, bài toán nghiên cứu của khóa luận tập trung ở **downstream policy evaluation**, chứ không tìm đóng góp từ thuật toán phân loại mới.

Höppner, Baesens, Verbeke và Verdonck (2022) phát triển khung học có chi phí phụ thuộc từng giao dịch, nhấn mạnh quyết định chống gian lận cần xét đến tổn thất phụ thuộc instance thay vì tối ưu accuracy/AUC đơn lẻ. Bài báo hỗ trợ việc báo song song *fraud count* và *transaction value*, đồng thời giải thích tại sao một policy có tỷ lệ bắt giữ cao hơn chưa chắc tối ưu theo thước đo kinh tế. Tuy nhiên, bài báo không cung cấp bằng chứng để hiệu chuẩn analyst staffing, thời gian chờ hay xác suất recovery trong mô phỏng hiện tại.

**Nguồn:** Höppner et al. (2022), *European Journal of Operational Research*, 297(1), 291–300, https://doi.org/10.1016/j.ejor.2021.05.028.

## 2.2. Điều chỉnh ngưỡng cảnh báo theo năng lực xử lý: prior art trực tiếp

Shen và Kurshan (2020) coi lựa chọn ngưỡng cảnh báo fraud dưới giới hạn analyst/alert-processing bandwidth là một quyết định tuần tự và đề xuất phương pháp Deep Q-Network để điều chỉnh threshold. Đây là công trình *closest conceptual prior art* cho nhánh Capacity-aware của khóa luận. Vì vậy, khóa luận **không** trình bày dynamic/adaptive alert threshold như một phát minh mới; cũng không khẳng định queue + classifier + alert threshold là tổ hợp chưa từng được nghiên cứu.

Khác biệt theo định hướng của luận văn hiện tại là *đối tượng thay đổi chiến lược trong quá trình tương tác với policy*, *persistent review backlog*, thiết kế 2×2×3 trên **hai môi trường dữ liệu giao dịch**, và đánh giá rủi ro từ các giả định cơ chế. Những khác biệt này cần được kiểm chứng bằng việc đọc toàn văn đối chứng nghiên cứu chứ không chỉ dựa vào từ khóa trên abstract. Cụ thể, sau khi đóng băng thiết kế, đặt câu hỏi: giữ cùng review-budget thì kết luận ra sao; thứ hạng policy có đổi khi fraud generator thay đổi hay không.

**Nguồn:** Shen, H., & Kurshan, E. (2020), *Deep Q-Network-based Adaptive Alert Threshold Selection Policy for Payment Fraud Systems in Retail Banking*, ICAIF 2020, https://doi.org/10.1145/3383455.3422563, preprint https://arxiv.org/abs/2010.11062.

## 2.3. Human-in-the-loop và analyst capacity

Alves et al. (2025) giới thiệu OpenL2D và bộ benchmark Financial Fraud Alert Review (FiFAR), nơi chuyên gia có khả năng ra quyết định không đồng nhất và bị giới hạn năng lực xử lý theo batch/time window. Benchmark tạo ra **50 synthetic fraud analysts** và 30 nghìn review instances. Nghiên cứu cho thấy thứ hạng các phương pháp learning-to-defer có thể thay đổi khi cấu hình expert availability và capacity thay đổi.

KLTN mượn **ý tưởng giới hạn nguồn lực và phụ thuộc vào capacity**, không mượn trực tiếp số lượng experts hay năng suất case/hour. Dữ liệu công khai không đủ định danh review-time hay analyst effectiveness của một ngân hàng cụ thể. Vì vậy service rate được biểu diễn bằng ba tỷ lệ chuẩn hóa 0,75/1/1,25 từ validation alert arrival rate. FIFO là lựa chọn cấu trúc cho baseline, không phải quy tắc chính thức của tổ chức trong thực tế.

**Nguồn:** Alves, J. V. et al. (2025), *A benchmarking framework and dataset for learning to defer in human-AI decision-making*, *Scientific Data* 12, 506, https://doi.org/10.1038/s41597-025-04664-y.

Từ lý thuyết hàng đợi, quan hệ Little's law `L=λW` mô tả quan hệ giữa lượng công việc trung bình, arrival rate và thời gian lưu lại hệ thống trong điều kiện thích hợp. Nó hỗ trợ kiểm tra tính hợp lý của accounting, nhưng không thể áp đặt nguyên xi lên mỗi finite-horizon trajectory mất ổn định. Xem Whitt (1991), *A review of L=λW and extensions*, *Queueing Systems* 9:235–268, https://www.columbia.edu/~ww2040/ReviewLlamW91.pdf.

## 2.4. ABM như một phương pháp thử nghiệm chính sách

Ding et al. (2025) giới thiệu AML-CFSim, mô hình agent-based để mô phỏng rửa tiền phát sinh từ cyber fraud và đánh giá các can thiệp giám sát. Bài báo cho thấy ABM phù hợp trong những môi trường khó thử nghiệm chính sách trực tiếp, nhưng khác biệt lĩnh vực giữa AML/luân chuyển tiền và transaction fraud detection/alert handling không cho phép bê nguyên tác tử, mạng luân chuyển tiền, tham số và findings.

Grimm et al. (2020) đề xuất phiên bản cập nhật của ODD protocol — **Overview, Design concepts, Details** — nhằm tăng tính minh bạch, khả năng tái lập và sức thuyết phục cấu trúc của mô hình ABM. Đây là **chuẩn mô tả**, không phải giấy chứng nhận mô hình có external validity. Vì phần fraudster là thành phần có persistent strategy values và học từ feedback còn queue vận hành theo discrete-event logic, KLTN mô tả chi tiết là **hybrid agent-based behavioral and discrete-event operational simulation**. Các risk-score/policy module không cần được gọi là agents; mô hình hiện chưa có nhiều fraudsters tương tác mạng lưới hoặc đội chuyên gia có sở thích, hành vi độc lập.

**Nguồn:** Ding et al. (2025), *Expert Systems with Applications* 285:127995, https://doi.org/10.1016/j.eswa.2025.127995; Grimm et al. (2020), *JASSS* 23(2), 7, https://doi.org/10.18564/jasss.4259. Đặc tả của chính đề tài: `03 Model design/ODD Hybrid ABM-DES Specification v1.0.md`.

## 2.5. Thích nghi đối kháng: phân biệt stress assumptions và bằng chứng hành vi thực

Core fraudster trong KLTN chọn một trong ba **amount regimes** low/middle/high bằng epsilon-greedy, cập nhật giá trị chiến lược sau modeled APPROVE/REVIEW/BLOCK. Đây là sự trừu tượng hóa có chủ đích: cả Xente và IEEE-CIS đều có observed fraud labels và feature contexts, **không** chứa quan sát trực tiếp về objective, exploration rate, bộ nhớ, strategic learning hay khả năng biết một alert nội bộ của fraudster. Không suy diễn rằng kẻ gian lận ngoài đời học epsilon-greedy hoặc theo đúng ba nhóm amount.

Xente và IEEE dùng validation-fraud donor pools theo tercile, nhưng sinh phản thực tế thông qua loop và frozen detector khác nhau. Mô hình vì vậy kiểm định *policy robustness conditional on adaptive strategy-choice rules*, không suy ra causal impact của sự học hỏi tội phạm trong thế giới thật. Thực nghiệm phải bao gồm reward unit/value ablation, alpha/epsilon sensitivity và review-observability alternatives, cũng như structural tests về persistence của synthetic identities.

## 2.6. Calibration, validation, uncertainty và mô hình hóa theo patterns

McCulloch et al. (2022) phân biệt parameter uncertainty, model discrepancy, observation uncertainty và stochastic uncertainty khi calibration ABMs; thảo luận History Matching và Approximate Bayesian Computation. KLTN hiện **không thực hiện** HM/ABC, nhưng ứng dụng nguyên tắc phân loại provenance: thống kê amount/prevalence từ dữ liệu; review targets là policy choices; capacity là stress ratios; alpha/epsilon/review effectiveness là assumptions. Việc lặp seeds và báo MCSE chỉ xử lý stochastic uncertainty sau khi giữ các giả định còn lại cố định, không thể đồng nhất với bất định toàn bộ hệ thống thực.

Grimm et al. (2005) nêu phương pháp *pattern-oriented modeling*, khuyến nghị dùng nhiều patterns để hỗ trợ phát triển/đánh giá cấu trúc agent models. Với dự án này, generator nên được kiểm tra theo amount, product, entity repeat/cold-start, temporal pattern, missingness, score và queue dynamics. Match một marginal distribution đơn lẻ không chứng minh adaptive mechanism đúng về mặt hành vi. Nhánh IEEE cần đặc biệt lưu ý `card1+addr1` chỉ là proxy, C/D/M/V masked fields không được gán ngụ ý strategic intent.

**Nguồn:** McCulloch et al. (2022), *JASSS* 25(2),1, https://doi.org/10.18564/jasss.4791; Grimm et al. (2005), *Science* 310(5750):987–991, https://doi.org/10.1126/science.1116681.

## 2.7. Tổng hợp khoảng trống và giá trị bổ sung của khóa luận

| Nhánh nghiên cứu | Điều đã được nghiên cứu | Điều KLTN bổ sung trong phạm vi triển khai | Ranh giới claim |
|---|---|---|---|
| Fraud detection / cost learning | Detector, loss-aware prediction, instance costs (Höppner) | Evaluates policy + finite queue, count/value/operational outcomes | không bảo đảm cost optimality |
| Capacity-aware alert selection | Dynamic thresholds under finite workload (Shen & Kurshan) | explicitly controlled adversarial regime feedback, capacity-policy contrasts | không claim threshold mới |
| Human-AI defer | Analyst heterogeneity/capacity constraints (Alves) | pooled FIFO stress with two empirical input environments | không hiệu chuẩn cases/hour |
| Fraud-adjacent ABM | AML policy-testing agents (Ding) | transaction-fraud + policy queue + adaptive-regime loop | không đồng nhất AML vs fraud |
| ABM reporting/validation | ODD, UQ, pattern-oriented modeling | assumption registry, outcome semantics, targeted ablations | vẫn cần external/practitioner validation |

**Research gap có thể bảo vệ:** Tài liệu gần nhất giải quyết những thành phần quan trọng **riêng rẽ**; đề tài phát triển một hệ thống mô phỏng minh bạch để kiểm tra **mối tương tác** giữa hành vi đối kháng có feedback, chính sách kiểm soát và năng lực phân tích trong hai môi trường transaction data, với báo cáo độ vững và giới hạn validity. Đây là *integration-and-evaluation contribution* (đóng góp thiết kế/thực nghiệm), không là chứng minh không công trình nào trên thế giới từng làm điều tương tự.

## 2.8. Chuyển hóa thành research hypotheses / testable statements

- **H1 (behavior/metric composition):** một lựa chọn chiến lược có feedback làm thay đổi regime shares và/hoặc kết quả fraud so với mixture không học, nhưng hướng effect có thể khác giữa scenarios.
- **H2 (routing/congestion):** Capacity-aware giảm alert load/backlog trong các trạng thái quá tải, đổi lại capture có thể tăng/giảm theo detector/strategy distribution.
- **H3 (capacity):** normalized capacity là moderator quan trọng của workload và effectiveness proxy; effect được báo kèm giới hạn staffing extrapolation.
- **H4 (robustness):** kết luận từ một empirical environment hoặc một learning/review assumption không nhất thiết bảo toàn ở environment khác. Null/heterogeneous effects đều là kết quả có giá trị.

Các giả thuyết không được điều chỉnh hậu nghiệm để chỉ hợp với kết quả đẹp. Mọi quyết định cập nhật mechanism sau pilot cần ghi trong model-version history và thực nghiệm xác nhận độc lập.

## References (bản xác minh DOI, hoàn thiện APA ở khâu biên tập)
1. Shen, H., & Kurshan, E. (2020). *Deep Q-Network-based Adaptive Alert Threshold Selection Policy for Payment Fraud Systems in Retail Banking*. Proceedings of the First ACM International Conference on AI in Finance. https://doi.org/10.1145/3383455.3422563.
2. Höppner, S., Baesens, B., Verbeke, W., & Verdonck, T. (2022). *Instance-dependent cost-sensitive learning for detecting transfer fraud*. European Journal of Operational Research, 297(1), 291–300. https://doi.org/10.1016/j.ejor.2021.05.028.
3. Alves, J. V., et al. (2025). *A benchmarking framework and dataset for learning to defer in human-AI decision-making*. Scientific Data, 12, 506. https://doi.org/10.1038/s41597-025-04664-y.
4. Ding, N., Fan, Z., Zhai, Y., Wang, Y., & Zhang, E. (2025). *AML-CFSim: An agent-based simulation model for anti-money laundering from cyber fraud crimes*. Expert Systems with Applications, 285, 127995. https://doi.org/10.1016/j.eswa.2025.127995.
5. Grimm, V., et al. (2020). *The ODD Protocol for Describing Agent-Based and Other Simulation Models: A Second Update to Improve Clarity, Replication, and Structural Realism*. JASSS, 23(2), 7. https://doi.org/10.18564/jasss.4259.
6. McCulloch, J., et al. (2022). *Calibrating Agent-Based Models Using Uncertainty Quantification Methods*. JASSS, 25(2), 1. https://doi.org/10.18564/jasss.4791.
7. Grimm, V., et al. (2005). *Pattern-oriented modeling of agent-based complex systems: Lessons from ecology*. Science, 310(5750), 987–991. https://doi.org/10.1126/science.1116681.
8. Whitt, W. (1991). *A review of L=λW and extensions*. Queueing Systems, 9, 235–268. https://www.columbia.edu/~ww2040/ReviewLlamW91.pdf.

**Editorial note:** Trước nộp GVHD, cần đối chiếu PDF toàn văn của các nghiên cứu sát nhất, nhập DOI/metadata vào Zotero và trích dẫn đúng format khoa/NEU. Không bổ sung thông tin Green SM nội bộ khi chưa được cấp quyền.
