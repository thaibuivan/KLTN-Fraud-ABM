# CHƯƠNG 2 — TỔNG QUAN NGHIÊN CỨU (BẢN THẢO v1.0)

> 18/10/2026. Đây là tổng quan học thuật định hướng phục vụ khóa luận; **không** phải systematic review với PRISMA hoặc khẳng định đã liệt kê hết công trình liên quan. Đã đối chiếu thông tin xuất bản của các nguồn trọng tâm với trang tạp chí/nhà xuất bản. Cần kiểm tra toàn văn và bổ sung nghiên cứu nếu GVHD yêu cầu.

## 2.1. Từ phát hiện gian lận tới quản lý quyết định gian lận

Một phần lớn bài toán fraud detection được tiếp cận như phân loại nhị phân, dự đoán một giao dịch là gian lận hay hợp lệ dựa trên các đặc trưng giao dịch và lịch sử. Trong bối cảnh dữ liệu mất cân bằng, đánh giá chỉ bằng accuracy có thể gây hiểu nhầm; phân tích nên chú trọng khả năng xếp hạng và phân biệt lớp hiếm, chẳng hạn PR-AUC và ROC-AUC, cùng hiện tượng drift theo thời gian. Tuy vậy, đánh giá classifier không tương đương đánh giá một hệ thống quản lý gian lận đã hoạt động.

Delamaire, Abdou và Pointon (2009) tổng quan các kỹ thuật phát hiện gian lận thẻ và nêu vấn đề khách hàng hợp lệ bị đánh dấu sai. Höppner và cộng sự (2022) đề xuất instance-dependent cost-sensitive learning, bao gồm ma trận chi phí theo từng giao dịch và các mô hình phân loại nhạy với chi phí. Đóng góp của Höppner và cộng sự nhấn mạnh rằng hệ thống không chỉ cần phát hiện nhãn gian lận mà cần lưu tâm quy mô thiệt hại và tác động của quyết định. Tuy nhiên, nghiên cứu đó không trực tiếp cung cấp cơ chế hàng đợi analyst hay động lực học của đối tượng gian lận trước chính sách.

Nanduri và cộng sự (2020) báo cáo hệ thống quản lý gian lận thương mại điện tử của Microsoft kết hợp cập nhật thông tin rủi ro, mô hình học máy và mô hình tối ưu hóa quyết định có xét đến các bên khác trong chuỗi xử lý. Đây là minh chứng quan trọng rằng quyết định fraud management có phạm vi rộng hơn dự đoán điểm rủi ro, và các chính sách phải xét tới những hệ quả tiếp theo của quyết định. Tuy nhiên, cấu trúc triển khai và dữ liệu doanh nghiệp của nghiên cứu đó không thể dùng làm calibration cho hai bộ dữ liệu Xente/IEEE-CIS.

**Hệ quả cho khóa luận:** Chất lượng risk score được xem là thành phần đầu vào, trong khi biến phụ thuộc của thí nghiệm là các thước đo fraud-related outcomes, workload, can thiệp giao dịch hợp lệ và congestion. Monetary net benefit không được đưa thành thước đo kết luận chính nếu chi phí phục vụ, thất thoát/thu hồi và friction không có calibration phù hợp.

## 2.2. Chính sách cảnh báo dưới ràng buộc capacity

Shen và Kurshan (2020) nghiên cứu việc lựa chọn ngưỡng cảnh báo thích nghi trong hệ thống fraud alert của ngân hàng bán lẻ dưới ràng buộc năng lực xử lý. Công trình xây dựng một bài toán quyết định tuần tự và sử dụng Deep Q-Network để nâng cao hiệu quả so với ngưỡng cố định. Về quan hệ với khóa luận, đây là **prior art trực tiếp nhất** của phần policy/capacity: giới hạn analyst và điều chỉnh threshold đã có tiền lệ công bố.

Khóa luận này **không** cạnh tranh với thuật toán Deep Q-Network, cũng không tự nhận đã phát minh adaptive threshold. Sự khác biệt được đề xuất là mục đích thí nghiệm: sử dụng policy đơn giản, minh bạch làm hai đối chứng, sau đó chủ động thay đổi cơ chế hành vi của fraudster và capacity trong mô hình có vòng phản hồi để phân tích mức độ vững của hiệu ứng. Điều này chỉ có giá trị mới về thực nghiệm/phương pháp nếu các sensitivity checks chứng minh tác động không chỉ là hệ quả tất yếu của rule routing.

Ở khía cạnh con người trong vòng ra quyết định, Alves và cộng sự (2025) giới thiệu OpenL2D/FiFAR, một benchmark learning-to-defer có mô hình chuyên gia nhân tạo, giới hạn năng lực và sự khác biệt giữa các expert. Công trình này ủng hộ việc đánh giá các chiến lược phân giao công việc trong điều kiện nhân lực hạn chế. Dữ liệu synthetic expert và sự kiểm tra đối chiếu bằng dữ liệu chuyên viên thực của bài báo **không** cung cấp số giao dịch một chuyên viên ngân hàng trong Xente/IEEE có thể xử lý mỗi giờ, cũng không trực tiếp đo chính xác suất review có thể ngăn một giao dịch gian lận.

Do thiếu tham số năng lực xử lý thực tế, khóa luận chọn phương pháp **normalized capacity stress**: tốc độ phục vụ được biểu diễn theo tỉ số 0,75; 1,00; 1,25 so với lưu lượng cảnh báo cơ sở trên validation. Đây là biến thiết kế thí nghiệm, không phải ước lượng số chuyên viên cần tuyển dụng cho ngân hàng.

Hàng đợi được mô hình hóa với trạng thái bền vững theo thời gian, thứ tự FIFO trong thí nghiệm chính, risk-priority trong kiểm định cấu trúc. Đặt backlog và waiting time bên cạnh tỷ lệ cảnh báo được review là cần thiết: một chính sách giảm lượng cảnh báo gửi tới hàng đợi có thể làm backlog giảm gần như theo cơ học; phần có ý nghĩa nghiên cứu hơn là mức đánh đổi tương ứng về đối tượng gian lận và giao dịch hợp lệ.

## 2.3. Agent-based simulation và mô phỏng dựa trên sự kiện

Trong mô phỏng dựa trên tác tử (agent-based model — ABM), trạng thái và quy tắc ra quyết định của các tác tử được mô tả ở cấp vi mô; động học vĩ mô xuất hiện từ quá trình tương tác giữa tác tử và môi trường. Grimm và cộng sự (2020) cung cấp chuẩn ODD (Overview, Design concepts, Details) để mô tả cấu trúc và cơ chế của ABM theo cách nhất quán, hướng tới minh bạch và tái lập. Chuẩn ODD không thay thế verification/validation, nhưng buộc người nghiên cứu nêu rõ tác tử nào có state, thông tin nào được quan sát, thứ tự event và quy tắc cập nhật.

Ding và cộng sự (2025) phát triển AML-CFSim, một mô hình ABM đối với rửa tiền phát sinh từ cyber fraud và thử nghiệm các biện pháp giám sát của ngân hàng và cơ quan thực thi. Nghiên cứu này cung cấp ví dụ về việc dùng mô phỏng để so sánh tác động chính sách trong môi trường khó triển khai thí nghiệm thực. Tuy nhiên, hệ thống rửa tiền qua mạng tài khoản, quy trình điều tra AML và transaction-fraud alert routing là **những miền vấn đề khác nhau**. Do đó, chỉ nên kế thừa cách đặt vấn đề, nguyên tắc minh bạch giả định và phương pháp validation, không chuyển trực tiếp quy mô mạng hay tham số giám sát.

Với nghiên cứu hiện tại, việc gọi mô hình là ABM cần được trình bày có điều kiện: fraudster là thành phần agent rõ nhất vì có trạng thái giá trị chiến lược và cập nhật sau phản hồi; customer stream trong lõi có thể là observed transaction replay, còn bộ chấm điểm risk, policy và hàng đợi là các mô-đun có logic theo sự kiện. Vì vậy, mô tả kỹ thuật chính xác là **hybrid agent-based behavioral simulation coupled with event-driven policy/queue simulation**. Không cần gán tính tự trị giả tạo cho mọi giao dịch hay mọi analyst để giữ tên ABM.

Một mô phỏng replay tĩnh có thể dùng để đánh giá hậu quả điều chỉnh routing với score stream cố định, nhưng khó đại diện phản hồi từ việc fraudster thay đổi đặc trưng giao dịch trong tương lai. Trong closed-loop, agent chọn regime, sinh giao dịch có bộ đặc trưng phù hợp, bộ phát hiện chấm điểm lại và policy/queue cập nhật. Chu trình này tạo khả năng khảo sát cơ chế ảnh hưởng hai chiều mà một thiết kế replay tĩnh không nắm bắt trọn vẹn.

## 2.4. Fraudster adaptation như giả định stress-test

Sự biến đổi của phương thức gian lận và sự thay đổi của môi trường đã được nêu trong các nghiên cứu thực tế về fraud management, trong đó Nanduri và cộng sự (2020) mô tả việc cập nhật tri thức và quyết định nhằm ứng phó những pattern mới. Tuy vậy, quan sát môi trường thay đổi **không** cho phép nhận dạng trực tiếp một thuật toán ra quyết định của fraudster. Các bộ dữ liệu cạnh tranh có nhãn giao dịch thường không ghi lại toàn bộ hành động, kỳ vọng, phản hồi quan sát được hoặc mục tiêu của đối tượng thực hiện gian lận.

Khóa luận sử dụng tác tử thích nghi **có giới hạn**: trong mỗi sự kiện gian lận, tác tử chọn một trong các regime có căn cứ phân bố amount/value trên validation. Tác tử quan sát phản hồi được mô hình quy định và cập nhật ước lượng giá trị chiến lược theo:

`V_s(t+1) = V_s(t) + α[r_t - V_s(t)]`

Với xác suất `ε`, tác tử chọn một regime mang tính khám phá; còn lại ưu tiên regime có giá trị ước lượng cao hơn. Trong thí nghiệm chính, `α=0.15`, `ε=0.10`, nhưng hai con số là **explicit behavioral assumptions**. Reward được chuẩn hóa theo median amount/value của fraud donor trong từng scenario, không thể giải thích là hàm hữu dụng thực tế đã đo được.

Đối chứng StaticMixture chọn regime theo trọng số cố định suy ra từ validation; do đó khác biệt về kết quả giữa Static và Adaptive cho biết **hệ quả trong mô hình của cơ chế thay đổi phân phối chiến lược**, không chứng minh fraudster thực học theo epsilon-greedy.

Ba điểm cần đặc biệt kiểm định: (i) phân bố amount/value và reward có thể làm ưu tiên các regime khác nhau ngay cả khi cùng learning rule; (ii) một quyết định REVIEW có thể không được đối tượng biết ở thời điểm policy route giao dịch; (iii) sự thay đổi generated fraud history phải tác động đến score của các sự kiện tiếp theo, tránh sử dụng điểm rủi ro cố định không tương thích với lịch sử mô phỏng đã thay đổi.

## 2.5. Verification, validation và uncertainty quantification

Sargent (2013) phân biệt kiểm tra cấu trúc khái niệm, xác minh implementation, tính hợp lệ vận hành và dữ liệu đầu vào trong mô hình mô phỏng. Điều này có ý nghĩa trực tiếp: GitHub Actions chạy thành công chứng tỏ những thuộc tính phần mềm được test hoạt động như mong đợi, nhưng **không chứng minh** các giả định học hỏi, khả năng ngăn tổn thất hay cơ chế hàng đợi phản ánh đúng ngân hàng cụ thể.

Grimm và cộng sự (2005) đề xuất *pattern-oriented modeling* đối với các hệ thống ABM: đánh giá mô hình qua nhiều patterns thay vì chỉ so khớp một thống kê tổng hợp. Áp dụng phù hợp trong nghiên cứu này là so sánh generated donors/counterfactuals với nhiều đặc điểm từ dữ liệu đầu vào, gồm phân phối amount, product, biến lịch sử, missingness hoặc entity context, đồng thời tách rõ các patterns không thể quan sát. Việc khớp empirical marginal distributions cũng không tự xác định được learning rule thật của fraudster.

McCulloch và cộng sự (2022) xem calibration trong bối cảnh uncertainty quantification, gồm bất định tham số, cấu trúc/sai khác mô hình, quan sát và ngẫu nhiên. Bài báo thảo luận History Matching và Approximate Bayesian Computation, song khóa luận không cần khẳng định đã thực hiện các phương pháp này nếu chưa có điều kiện dữ liệu và ngân sách tính toán. Về mặt khả thi, nghiên cứu có thể giải quyết:
- **Bất định ngẫu nhiên:** chạy nhiều random seeds; báo trung bình, độ lệch chuẩn, MCSE và confidence intervals, đặc biệt với metric value có đuôi phân phối dày.
- **Bất định tham số:** thay `alpha`, `epsilon`, reward scaling, threshold, congestion triggers, service capacity và giả định effectiveness `q`.
- **Bất định cấu trúc:** FIFO/risk-priority, feedback observability, cách tính interception/review completion và chất lượng score khi bị suy giảm.
- **Bất định quan sát:** thiếu dữ liệu về analyst decisions, customer friction, post-transaction outcomes và true customer identity trong IEEE.

Với kết quả tài chính, việc `REVIEW` bắt đầu trước horizon không thể được mô tả là loss prevented. Theo lớp outcome sensitivity hiện có, chỉ khi service hoàn thành trước horizon mới được xem là eligible for assumed prevention; `q∈{0,0.5,1}` là ba trường hợp giả định để kiểm tra tính vững, không phải tỷ lệ thu hồi thực tế.

## 2.6. Tổng hợp khoảng trống và định vị đóng góp

| Nhánh nghiên cứu | Đã giải quyết | Những câu hỏi khóa luận cần kiểm tra thêm |
|---|---|---|
| Fraud classification và cost-sensitive learning | Điểm rủi ro, chi phí sai lầm theo từng giao dịch (Höppner et al., 2022) | Tác động của score tới review backlog/decision policy khi có feedback |
| Adaptive threshold/alert policy | Chính sách điều chỉnh ngưỡng với giới hạn analyst (Shen & Kurshan, 2020) | Độ vững của policy gain dưới regime giả định có thích nghi và khác biệt giữa môi trường dữ liệu |
| Fraud operations triển khai | Dynamics và hệ thống đa quyết định thực tế (Nanduri et al., 2020) | Môi trường mô phỏng minh bạch có thể tái lập và đánh giá assumption sensitivity bằng public datasets |
| Agent-based policy simulation | ABM để thử nghiệm biện pháp AML (Ding et al., 2025) | Cơ chế transaction fraud routing và review queue, không sao chép quy trình AML |
| Capacity-constrained human decisions | Giới hạn/heterogeneity của expert và learning-to-defer (Alves et al., 2025) | Tương tác congestion–fraud adaptation–false interventions trong queue event-driven |
| Simulation methodology | ODD (Grimm et al., 2020), validation (Sargent, 2013), uncertainty (McCulloch et al., 2022) | Báo cáo cơ chế, độ vững và claim boundaries trong thí nghiệm cụ thể |

**Khoảng trống nghiên cứu được đề xuất (cần duy trì cách viết thận trọng):** Trong phạm vi các tài liệu đã rà soát, ít công trình khảo sát một cách có hệ thống **tương tác giữa tác tử đối kháng có cơ chế học hỏi, routing policy và analyst-capacity queue**, đồng thời kiểm tra khác biệt policy effects giữa **hai empirical transaction-fraud environments** dưới chung một thiết kế. Đây là khoảng trống phục vụ câu hỏi của khóa luận, **không phải tuyên bố đã chứng minh tính độc nhất tuyệt đối** so với mọi công trình trên thế giới.

Điều làm nghiên cứu có ý nghĩa không chỉ là Adaptive khác Static hoặc Capacity-aware giảm backlog. Câu hỏi sâu hơn là liệu hiệu quả policy trên fraud outcome có đổi chiều, suy giảm hoặc phụ thuộc vào reward, score quality và nguồn lực review; các kết luận đó còn vững đến đâu khi thay các giả định đã công bố.

## 2.7. Khung khái niệm tổng hợp

```text
Empirical scenario (Xente / IEEE-CIS)
      |                         Fraudster agent
      |                         static/adaptive strategy
      |                                  |
      v                                  v
Transaction history ----------> Generated/observed transaction
                                           |
                                           v
                            Frozen risk model, rescored online
                                           |
                         +-----------------+------------------+
                         |                                    |
               Fixed-threshold                         Capacity-aware
                         |                          observes queue/capacity
                         +-----------------+------------------+
                                           |
                                   APPROVE/REVIEW/BLOCK
                                           |
                                     Persistent FIFO queue
                                           |
                                  Finite pooled review service
                                           |
                 Operational/fraud/legitimate-intervention metrics
                                           |
                                Assumed feedback to fraudster
```

Cấu trúc logic của các câu hỏi nghiên cứu xuất phát từ tương tác bốn chiều: **fraudster regime × decision policy × reviewer capacity × empirical scenario**. Sự phát sinh output phản thực tế phải tuân theo chronology và thông tin có sẵn tại thời điểm đó; mọi mức tham số không nhận diện được từ dữ liệu phải công bố là assumption/scenario variable.

## Danh mục nguồn học thuật cho chương này

1. Delamaire, L., Abdou, H., & Pointon, J. (2009). Credit card fraud and detection techniques: A review. *Banks and Bank Systems*, 4(2), 57–68. https://researchportal.northumbria.ac.uk/en/publications/credit-card-fraud-and-detection-techniques-a-review/
2. Höppner, S., Baesens, B., Verbeke, W., & Verdonck, T. (2022). Instance-dependent cost-sensitive learning for detecting transfer fraud. *European Journal of Operational Research*, 297(1), 291–300. https://doi.org/10.1016/j.ejor.2021.05.028
3. Shen, H., & Kurshan, E. (2020). Deep Q-Network-based Adaptive Alert Threshold Selection Policy for Payment Fraud Systems in Retail Banking. *ACM International Conference on AI in Finance*. https://doi.org/10.1145/3383455.3422563
4. Nanduri, J., Jia, Y., Oka, A., Beaver, J., & Liu, Y.-W. (2020). Microsoft Uses Machine Learning and Optimization to Reduce E-Commerce Fraud. *INFORMS Journal on Applied Analytics*, 50(1), 64–79. https://doi.org/10.1287/inte.2019.1017
5. Alves, J. V., et al. (2025). A benchmarking framework and dataset for learning to defer in human-AI decision-making. *Scientific Data*, 12, 506. https://doi.org/10.1038/s41597-025-04664-y
6. Ding, N., Fan, Z., Zhai, Y., Wang, Y., & Zhang, E. (2025). AML-CFSim: An agent-based simulation model for anti-money laundering from cyber fraud crimes. *Expert Systems with Applications*, 285, 127995. https://doi.org/10.1016/j.eswa.2025.127995
7. Grimm, V., et al. (2005). Pattern-oriented modeling of agent-based complex systems: Lessons from ecology. *Science*, 310(5750), 987–991. https://doi.org/10.1126/science.1116681
8. Grimm, V., et al. (2020). The ODD Protocol for Describing Agent-Based and Other Simulation Models. *Journal of Artificial Societies and Social Simulation*, 23(2), 7. https://doi.org/10.18564/jasss.4259
9. McCulloch, J., et al. (2022). Calibrating Agent-Based Models Using Uncertainty Quantification Methods. *Journal of Artificial Societies and Social Simulation*, 25(2), 1. https://doi.org/10.18564/jasss.4791
10. Sargent, R. G. (2013). Verification and validation of simulation models. *Journal of Simulation*, 7(1), 12–24. https://doi.org/10.1057/jos.2012.20

> **Nghiệm thu Literature Review:** trước bản nộp GVHD, kiểm tra từng claim với bài gốc; bổ sung 2–4 công trình chuyên về adversarial fraud, queue/staffing và multi-objective simulation nếu tìm được source primary mạnh. Không sử dụng báo cáo nội bộ của bất cứ công ty nào khi chưa có quyền.
