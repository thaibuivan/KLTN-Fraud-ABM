# CHƯƠNG 1 — MỞ ĐẦU (BẢN THẢO v1.0)

> Ngày soạn: 18/10/2026. Bản nháp học thuật dựa trên phạm vi khóa luận hiện hành; cần chuẩn hóa theo mẫu Khoa Toán kinh tế và phê duyệt của GVHD. Không sử dụng tài liệu nội bộ doanh nghiệp.

## 1.1. Bối cảnh nghiên cứu và tính cấp thiết

Sự phát triển của thương mại điện tử và các hình thức thanh toán số làm tăng nhu cầu xử lý khối lượng lớn giao dịch theo thời gian. Với mỗi giao dịch, tổ chức cung cấp dịch vụ phải cân nhắc giữa việc cho phép giao dịch diễn ra thuận lợi và việc ngăn chặn các hành vi gian lận. Hệ thống phát hiện gian lận thường sử dụng mô hình học máy để ước lượng điểm rủi ro giao dịch, nhưng điểm rủi ro không tự quyết định toàn bộ hiệu quả vận hành. Trong thực tế, tổ chức còn phải phân bổ giao dịch vào các luồng chấp thuận, rà soát thủ công hoặc chặn giao dịch; mỗi lựa chọn tạo ra hậu quả khác nhau về khả năng kiểm soát rủi ro, sự bất tiện cho khách hàng và khối lượng công việc của bộ phận xử lý cảnh báo.

Các nghiên cứu về phát hiện gian lận đã từ lâu nhấn mạnh sự bất cân xứng giữa hậu quả của các loại sai lầm phân loại. Delamaire, Abdou và Pointon (2009) đề cập tới hậu quả khi khách hàng hợp lệ bị phân loại là gian lận. Höppner và cộng sự (2022) phát triển cách tiếp cận phát hiện gian lận nhạy với chi phí theo từng giao dịch, cho thấy tiêu chí đánh giá chỉ dựa trên phân biệt nhãn có thể khác mục tiêu tài chính thực tế. Vì vậy, chất lượng của một mô hình phân loại, chẳng hạn ROC-AUC hay PR-AUC, là điều kiện đầu vào quan trọng nhưng không đủ để đánh giá chính sách xử lý giao dịch.

Giới hạn của năng lực xử lý thủ công làm vấn đề trở nên phức tạp hơn. Nếu một chính sách đặt ngưỡng cảnh báo thấp, hệ thống có thể phát sinh nhiều trường hợp đáng nghi cần xem xét, trong khi tốc độ xử lý của chuyên viên không tăng tương ứng. Alert backlog và thời gian chờ có thể gia tăng. Shen và Kurshan (2020) đã xem xét trực tiếp lựa chọn ngưỡng cảnh báo thích nghi trong hệ thống chống gian lận thanh toán có ràng buộc về năng lực xử lý; nghiên cứu này là tiền lệ quan trọng, vì thế không thể xem ý tưởng “điều chỉnh ngưỡng theo năng lực” là đóng góp mới tuyệt đối của khóa luận.

Một thách thức khác là môi trường gian lận không bất biến. Các quan sát thực tiễn được Nanduri và cộng sự (2020) mô tả trong hệ thống quản lý gian lận thương mại điện tử cho thấy hình thái gian lận thay đổi và các quyết định cần tính đến tương tác với các bên tham gia vào quy trình thanh toán. Khi cơ chế phát hiện hoặc can thiệp thay đổi, một đối tượng đối kháng có khả năng thay đổi lựa chọn giao dịch trong tương lai. Do đó, một policy replay dựa hoàn toàn trên một chuỗi điểm rủi ro cố định có thể bỏ sót phản hồi giữa chính sách và môi trường được kiểm soát.

Trong bối cảnh dữ liệu thực về cách đối tượng gian lận học hỏi, thời gian xử lý thủ công và tỷ lệ thu hồi tổn thất còn khó quan sát, một môi trường mô phỏng minh bạch là công cụ hữu ích để khảo sát *những điều gì có thể xảy ra trong các giả định được xác định rõ*. Mô phỏng không thay thế thực nghiệm triển khai tại ngân hàng, nhưng cho phép so sánh chính sách với cùng lịch giao dịch, cùng điều kiện ràng buộc và các chế độ hành vi có kiểm soát. Trong khóa luận này, mô phỏng được xây dựng theo hướng kết hợp tác tử có hành vi thích nghi với cơ chế xử lý sự kiện và hàng đợi hữu hạn.

## 1.2. Vấn đề nghiên cứu

Bài toán được xem xét không phải chỉ là “giao dịch nào gian lận?”, mà là “hệ thống nên vận hành và đánh giá các chính sách xử lý cảnh báo như thế nào khi có phản hồi hành vi đối kháng và nguồn lực xử lý bị giới hạn?”. Hai chính sách đối chứng được lựa chọn: **Fixed-threshold**, giữ ngưỡng can thiệp cố định, và **Capacity-aware**, thay đổi ngưỡng đưa vào review theo trạng thái hàng đợi. Đồng thời, môi trường gian lận được biểu diễn theo hai chế độ: **StaticMixture**, có phân phối chiến lược cố định, và **Adaptive**, có cơ chế điều chỉnh giá trị các chiến lược sau những phản hồi của hệ thống.

Khóa luận không tìm một ngưỡng tối ưu có thể chuyển trực tiếp sang thực tế. Mục tiêu là xác định các đánh đổi trong kết quả mô phỏng: thay đổi tỷ lệ gian lận được chặn/được đưa vào review, giá trị giao dịch rủi ro, can thiệp với giao dịch hợp lệ, số lượng cảnh báo, backlog và thời gian chờ; đồng thời xem những đánh đổi đó có thay đổi theo năng lực xử lý và môi trường dữ liệu hay không.

Cần nhấn mạnh một giới hạn nhận diện: “Adaptive fraudster” trong nghiên cứu là **giả định tác tử học hỏi có giới hạn** (bounded adaptation), không phải mô hình được ước lượng trực tiếp về nhận thức của đối tượng gian lận trong thực tế. Tương tự, việc bắt đầu review chưa phải bằng chứng đã ngăn được tổn thất; khóa luận báo cáo riêng chỉ tiêu proxy và các kiểm định giả định về hiệu quả review.

## 1.3. Mục tiêu nghiên cứu

**Mục tiêu tổng quát** là phát triển và đánh giá một môi trường mô phỏng chính sách xử lý gian lận giao dịch, có tác tử gian lận với cơ chế thích nghi, bộ chấm điểm rủi ro đóng băng, cơ chế phân luồng giao dịch, hàng đợi chuyên viên xử lý giới hạn năng lực và hệ thống chỉ số đa mục tiêu. Thông qua hai bộ dữ liệu công khai, nghiên cứu xem xét sự thay đổi hiệu quả tương đối của các chính sách dưới các điều kiện khác nhau.

**Mục tiêu cụ thể** gồm: (i) thiết kế kiến trúc mô phỏng sự kiện theo thời gian và vòng phản hồi của tác tử; (ii) xây dựng đặc điểm thực nghiệm của hai môi trường dữ liệu riêng biệt; (iii) so sánh chính sách và hành vi gian lận với các mức capacity chuẩn hóa; (iv) thực hiện đánh giá lặp lại và phân tích độ nhạy về reward, score, feedback, queue và outcome; (v) tổng hợp các phát hiện thành kết luận có điều kiện, ghi nhận rõ nguồn dữ liệu, bất định và phạm vi suy luận.

## 1.4. Câu hỏi nghiên cứu

- **RQ1 — Behavioral adaptation:** Chế độ gian lận thích nghi làm thay đổi phân bố chiến lược, tỷ lệ can thiệp và các thước đo rủi ro mô phỏng như thế nào so với chế độ StaticMixture, khi giữ nguyên quy tắc mô phỏng?
- **RQ2 — Policy trade-offs:** Chính sách Capacity-aware khác Fixed-threshold như thế nào về workload, backlog, can thiệp giao dịch hợp lệ và thước đo gian lận?
- **RQ3 — Capacity interactions:** Các tác động trên thay đổi ra sao giữa Low, Medium và High capacity?
- **RQ4 — Cross-scenario robustness:** Các kết luận có nhất quán giữa hai môi trường Xente và IEEE-CIS hay phụ thuộc vào đặc điểm giao dịch, chất lượng score và giả định kịch bản?

Đây là các câu hỏi đánh giá kết quả thí nghiệm; nghiên cứu **không mặc định trước** rằng Adaptive làm tăng mọi chỉ tiêu rủi ro hay Capacity-aware có ưu thế trên mọi thước đo.

## 1.5. Đối tượng, phạm vi và dữ liệu

Đối tượng nghiên cứu là **cơ chế quyết định và vận hành chính sách quản lý giao dịch nghi gian lận** trong môi trường mô phỏng, bao gồm điểm rủi ro, phân luồng quyết định, tác tử có phản hồi và hàng đợi xử lý giới hạn năng lực. Khóa luận không đánh giá hiệu quả của tổ chức tài chính hay hệ thống công nghệ cụ thể.

Hai môi trường thực nghiệm có nguồn dữ liệu riêng biệt:

1. **Xente Fraud Detection Challenge** trên nền tảng Zindi, sử dụng phần tập train có nhãn gồm 95.662 giao dịch với 193 trường hợp fraud; có thông tin CustomerId, thời gian, Value/Amount, product, channel/provider. Các con số là kiểm kê của dữ liệu dùng trong repo nghiên cứu, không phải số liệu toàn bộ giao dịch của doanh nghiệp Xente.
2. **IEEE-CIS Fraud Detection** trên Kaggle, sử dụng 590.540 giao dịch huấn luyện có nhãn với 20.663 trường hợp fraud; TransactionDT là thời gian tương đối, dữ liệu identity chỉ xuất hiện ở một phần giao dịch, card1+addr1 được dùng như *entity proxy*, không phải danh tính khách hàng được xác minh.

Hai tập dữ liệu không được gộp; mỗi môi trường có mô hình rủi ro, tập đặc trưng và các phân phối giao dịch riêng, trong khi quy tắc thí nghiệm, chính sách vận hành và chỉ số được chuẩn hóa về ý nghĩa. Dữ liệu có nhãn được chia theo thứ tự thời gian thành train/validation/test, lần lượt 70%/15%/15%.

Thiết kế thực nghiệm lõi gồm **2 môi trường × 2 chế độ tác tử × 2 chính sách × 3 mức năng lực = 24 cấu hình**. Các biến thể khác, như FIFO so với risk-priority, reward hay review-prevention, chỉ đóng vai trò kiểm định độ nhạy.

## 1.6. Phương pháp nghiên cứu

Nghiên cứu kết hợp phân tích dữ liệu quan sát, mô hình phát hiện gian lận có giám sát, mô phỏng dựa trên tác tử và mô phỏng vận hành hàng đợi theo sự kiện. Điểm rủi ro được ước lượng từ bộ huấn luyện và được khóa trong thí nghiệm; các ngưỡng chính sách chọn trên validation. Khi phát sinh fraud event phản thực tế, giao dịch được tạo từ donor fraud trong validation theo những kịch bản hạn chế rồi chấm điểm lại dựa trên trạng thái lịch sử quá khứ của mô hình.

Tác tử gian lận có thể giữ phân phối chiến lược cố định hoặc cập nhật giá trị chiến lược qua phần thưởng bằng quy tắc incremental learning với epsilon-greedy. Policy route giao dịch thành APPROVE/REVIEW/BLOCK. REVIEW tạo yêu cầu phục vụ trong hàng đợi có giới hạn capacity; quyết định sau có thể chịu ảnh hưởng của backlog. Các kết quả được tổng hợp theo seed và đối chiếu trong cùng môi trường qua policy/adaptation contrasts.

Độ tin cậy được đánh giá nhiều lớp: kiểm tra phần mềm, đối chiếu score online–offline, chống rò rỉ thông tin tương lai, kiểm tra phân phối sự kiện sinh, thực nghiệm lặp lại, độ nhạy tham số và độ nhạy cấu trúc. Việc báo cáo mô hình dự kiến tuân theo ODD protocol của Grimm và cộng sự (2020); phân loại bất định tham khảo McCulloch và cộng sự (2022), còn validation của mô phỏng tham khảo Sargent (2013).

## 1.7. Đóng góp dự kiến và giới hạn

Đóng góp kỳ vọng của khóa luận là: (1) một khung mô phỏng có vòng phản hồi giữa hành vi đối kháng giả định và quản lý cảnh báo; (2) so sánh những đánh đổi về fraud, can thiệp hợp lệ và vận hành có giới hạn nguồn lực; (3) đối chứng trên hai môi trường dữ liệu và nghiên cứu các điều kiện khiến hiệu quả tương đối của chính sách thay đổi; (4) quy trình công bố giả định, kiểm định độ nhạy và giới hạn suy luận.

Đóng góp trên được định vị **khác** những công trình đã có về adaptive alert threshold (Shen & Kurshan, 2020), cost-sensitive detection (Höppner et al., 2022) hoặc hệ thống fraud-management thích nghi được triển khai trong thực tế (Nanduri et al., 2020). Vì vậy, không được tuyên bố nghiên cứu là đầu tiên phát minh dynamic threshold, phát hiện hành vi fraudster thực, hoặc tìm được chính sách tối ưu của một ngân hàng.

Những giới hạn chính gồm: bộ dữ liệu competition không phản ánh đầy đủ vòng đời điều tra/thu hồi; cơ chế epsilon-greedy và mức capacity là giả định kịch bản; ngưỡng review không phải khuyến nghị vận hành thực; chỉ tiêu fraud interception khi bắt đầu review là proxy của mô phỏng và không được đánh đồng với mức tổn thất được ngăn chặn trong thực tế.

## 1.8. Kết cấu khóa luận dự kiến

Sau chương Mở đầu, Chương 2 tổng quan lý thuyết và nghiên cứu liên quan. Chương 3 trình bày dữ liệu và thiết kế thực nghiệm. Chương 4 giới thiệu mô hình mô phỏng, các chính sách, tiêu chí đánh giá và phương pháp validation. Chương 5 báo cáo kết quả Xente, IEEE-CIS, so sánh giữa hai môi trường và các kiểm định độ vững. Chương 6 thảo luận ý nghĩa, giới hạn, kết luận và hướng nghiên cứu tiếp theo. Bố cục có thể điều chỉnh theo quy định của Khoa/GVHD.

## Tài liệu sử dụng cho bản thảo

- Delamaire, L., Abdou, H., & Pointon, J. (2009). *Credit card fraud and detection techniques: A review*. Banks and Bank Systems, 4(2), 57–68. https://researchportal.northumbria.ac.uk/en/publications/credit-card-fraud-and-detection-techniques-a-review/
- Höppner, S., Baesens, B., Verbeke, W., & Verdonck, T. (2022). *Instance-dependent cost-sensitive learning for detecting transfer fraud*. European Journal of Operational Research, 297(1), 291–300. https://doi.org/10.1016/j.ejor.2021.05.028
- Shen, H., & Kurshan, E. (2020). *Deep Q-Network-based Adaptive Alert Threshold Selection Policy for Payment Fraud Systems in Retail Banking*. ICAIF. https://doi.org/10.1145/3383455.3422563
- Nanduri, J., Jia, Y., Oka, A., Beaver, J., & Liu, Y.-W. (2020). *Microsoft Uses Machine Learning and Optimization to Reduce E-Commerce Fraud*. INFORMS Journal on Applied Analytics, 50(1), 64–79. https://doi.org/10.1287/inte.2019.1017
- Grimm, V., et al. (2020). *The ODD Protocol for Describing Agent-Based and Other Simulation Models*. JASSS, 23(2), 7. https://doi.org/10.18564/jasss.4259
- McCulloch, J., et al. (2022). *Calibrating Agent-Based Models Using Uncertainty Quantification Methods*. JASSS, 25(2), 1. https://doi.org/10.18564/jasss.4791
- Sargent, R. G. (2013). *Verification and validation of simulation models*. Journal of Simulation, 7, 12–24. https://doi.org/10.1057/jos.2012.20
- Xente Fraud Detection Challenge. Zindi. https://zindi.world/competitions/xente-fraud-detection-challenge/data
- IEEE-CIS Fraud Detection. Kaggle. https://www.kaggle.com/competitions/ieee-fraud-detection/data

> **Biên tập trước nộp:** Thống nhất cách Việt hóa thuật ngữ, định dạng APA/đánh số chương theo trường, thay trích dẫn URL bằng hệ thống Zotero/LaTeX nếu dùng; chưa thêm số liệu ngoài những con số kiểm tra trong repo; không dùng kết quả pilot để viết như kết luận cuối.
