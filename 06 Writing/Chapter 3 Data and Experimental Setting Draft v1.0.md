# CHƯƠNG 3 — DỮ LIỆU VÀ THIẾT KẾ THỰC NGHIỆM (BẢN THẢO v1.0)

> Ngày: 18/10/2026. Phân biệt rõ **dữ liệu quan sát**, **tham số suy ra từ dữ liệu**, **giả định mô phỏng** và **kết quả thí nghiệm đã chạy**. Không đưa raw transactions lên public repository.

## 3.1. Mục đích và nguyên tắc chọn dữ liệu

Nghiên cứu sử dụng hai bộ dữ liệu giao dịch có nhãn gian lận công khai: Xente Fraud Detection Challenge (Zindi) và IEEE-CIS Fraud Detection (Kaggle). Hai dữ liệu khác nhau về bối cảnh giao dịch, cấu trúc biến, mức độ mất cân bằng, tính khả dụng của entity history và khả năng phân biệt gian lận của risk score. Vì vậy, thay vì ghép hai nguồn thành một mẫu chung, khóa luận coi mỗi nguồn là một **empirical environment** độc lập để kiểm tra các kết luận chính sách có bền vững khi điều kiện quan sát thay đổi hay không.

Các quan sát từ dữ liệu làm cơ sở cho phân phối thời gian, giá trị giao dịch, bối cảnh product/channel hoặc card/device/identity và risk score. Nhưng hai nguồn **không chứa lịch sử quyết định analyst, bộ chính sách của ngân hàng, chi phí false positive, tỷ lệ ngăn chặn giao dịch sau review hay tham số tâm lý học hỏi của fraudster**. Vì vậy, chỉ các phân phối thực sự quan sát được mới là empirical estimates; các thành phần còn lại phải được ghi là lựa chọn chính sách hoặc explicit stress assumptions.

## 3.2. Môi trường Xente

Xente Fraud Detection Challenge là bộ dữ liệu giao dịch thuộc nền tảng thanh toán/dịch vụ tài chính Xente tại Uganda, công bố qua Zindi. Trong nghiên cứu sử dụng **95.662 giao dịch có nhãn ở tập training.csv** với **193 giao dịch gian lận**, tương ứng khoảng **0,2018%**. Đây là tỉ lệ rất thấp, cho thấy phân loại chịu class imbalance nghiêm trọng.

Các trường dữ liệu phục vụ mô hình hóa gồm:
- `TransactionStartTime`: thời điểm giao dịch để xác lập thứ tự sự kiện và xây dựng các biến lịch sử chỉ dựa vào quá khứ.
- `CustomerId`: định danh lặp lại có thể dùng cho thống kê hành vi trong tập quan sát, không suy diễn cơ cấu pháp lý của khách hàng.
- `Amount` và `Value`: thông tin về giá trị giao dịch, trong đó `Value` có ý nghĩa quan trọng đối với signal của risk model và proxy về giá trị fraud exposure.
- `ProductCategory`, `ChannelId`, `ProviderId`, `ProductId` và `PricingStrategy`: bối cảnh giao dịch, hỗ trợ empirical resampling theo regime.
- `FraudResult`: nhãn quan sát dùng huấn luyện, đánh giá, phân nhóm fraud donor và lập lịch *fixed attempt slots* trong hold-out counterfactual experiment.

EDA trên repo ghi nhận **3.742 CustomerId** trong labeled train; lịch giao dịch quan sát được trải từ tháng 11/2018 đến tháng 2/2019. Các biến `AccountId` và `SubscriptionId` không được mặc định là quan hệ tài khoản sở hữu phân cấp, vì đặc điểm dữ liệu không đủ để chứng minh cách hiểu đó.

**Giới hạn:** số lượng fraud có nhãn nhỏ, phân phối `Value` tạo tín hiệu phân loại mạnh và nhiều trường hợp fraud về sau là cold-start. Một kết luận chính sách chỉ dựa trên Xente có nguy cơ phụ thuộc vào mức dễ tách fraud bằng Value; đây là lý do cần thí nghiệm degraded-score và môi trường đối chứng IEEE-CIS.

## 3.3. Môi trường IEEE-CIS

IEEE-CIS Fraud Detection là bộ dữ liệu giao dịch online trên Kaggle. Trong khóa luận, phần có nhãn được sử dụng là **590.540 dòng của `train_transaction.csv`**, trong đó có **20.663 giao dịch `isFraud=1`**, tỉ lệ khoảng **3,499%**. Dữ liệu identity được nối với transaction theo `TransactionID`; không phải giao dịch nào cũng có identity.

Các nhóm biến chính:
- `TransactionAmt`: giá trị giao dịch trong biểu diễn của dataset, không đồng nhất đơn vị với `Value` của Xente.
- `TransactionDT`: **độ lệch thời gian so với một mốc tham chiếu không công bố**, không phải ngày giờ thực; chỉ dùng làm trục thời gian tương đối.
- `ProductCD`, `card1`–`card6`, `addr1`–`addr2`, email-domain: thông tin bối cảnh giao dịch có thể hỗ trợ detector.
- `DeviceType`, `DeviceInfo`, một số trường `id_*`: thông tin identity/device nếu có; missingness được giữ như đặc tính quan sát.
- `C/D/M/V`: nhóm biến ẩn/được mã hóa, chỉ dùng làm detection context, **không** diễn giải thành thủ thuật hay hành động do fraudster trực tiếp chọn.

Vì không có CustomerId đáng tin như Xente, nghiên cứu sử dụng `card1+addr1` như **proxy gom nhóm sự kiện** để xây lịch sử giao dịch quá khứ. Cùng một proxy không chứng minh cùng một cá nhân; do đó phần luận văn phải dùng từ “entity proxy”, không viết “lịch sử khách hàng thật” trong IEEE.

Số liệu từ quá trình chuẩn bị chronology đã ghi nhận:
- Train: **413.378** sự kiện; validation: **88.581**; test: **88.581**.
- Phần trước test dùng warmup feature history: **501.959** sự kiện.
- Fraud donor validation: **3.042** giao dịch có nhãn fraud.
- Test fraud attempt slots: **3.083** vị trí; test legitimate events vẫn thuộc cùng observed context stream.
- IEEE validation fraud `TransactionAmt` terciles: mốc **50** và **117**; median **77**; các pool donor có **1.052 / 1.030 / 960** dòng.

**Quan trọng:** Tập `test` trong các con số 88.581 ở đây là **15% cuối của official labeled training file** được giữ làm hold-out. Không phải official unlabeled Kaggle `test_transaction.csv`. Cách phân chia này cho phép đánh giá trong khóa luận mà không phụ thuộc vào nhãn ẩn của leaderboard.

## 3.4. Temporal split và nguyên tắc chống rò rỉ

Cả hai empirical environments được chia theo thứ tự thời gian tăng dần thành train 70%, validation 15%, test 15%. Không chọn ngẫu nhiên các dòng trên toàn bộ chronology vì tương quan thời gian và history-dependent features có thể gây optimistic evaluation.

Các quy tắc cụ thể:
1. Risk model được fit trên train. Các frequency encodings/categories được suy ra từ train, tránh dùng thống kê của hold-out để huấn luyện bộ biến đổi.
2. Review thresholds, BLOCK threshold và các mức policy operating point được chọn theo phân phối score của validation; áp dụng không đổi trên test, ngoại trừ policy Capacity-aware chuyển *giữa các threshold tiers đã cố định* dựa trên trạng thái queue.
3. Trong IEEE, online feature state được warm từ toàn bộ **train + validation observed events** ở chế độ past-only. Khi chạy counterfactual test, history tiếp tục cập nhật tuần tự trên các giao dịch mới, không dùng nhãn fraud tương lai để xây detector features.
4. Generated fraud context được lấy từ **validation-fraud donor pool**. **Không dùng raw test fraud rows để chọn donor hay fit risk model**.
5. Trong core counterfactual comparison, `isFraud`/`FraudResult` của test **được sử dụng để xác định các thời điểm fraud attempts** và đánh giá output. Đây là thiết kế kịch bản có điều kiện theo lịch fraud attempt quan sát, **không phải một đánh giá dự đoán hoàn toàn độc lập của quá trình sinh gian lận**. Cần nêu rõ để tránh tuyên bố không hề có sử dụng test labels trong experiment design.
6. Generated fraud event phải được risk model chấm điểm lại từ đặc trưng và history tại thời điểm event. Legitimate event cũng cần được score lại trong đầy đủ IEEE counterfactual replay khi thay đổi fraud history có thể ảnh hưởng tới entity state.

Các kiểm tra score equivalence trên cùng chuỗi dữ liệu chưa thay đổi là một điều kiện nghiệm thu kỹ thuật; sự khớp này không chứng minh hành vi fraud được generate là thực tế.

## 3.5. Chấm điểm rủi ro và sự khác biệt giữa hai môi trường

Risk engine của Xente là logistic regression với regularization và customer-history features; risk engine của IEEE là streaming SGDClassifier với log-loss, train-only encodings và chronological history. Khóa luận không nhắm chứng minh các classifier này tối ưu về dự đoán.

Các kết quả đã ghi nhận:

| Chỉ tiêu | Xente validation | Xente test | IEEE validation | IEEE test |
|---|---:|---:|---:|---:|
| PR-AUC | **0,560851** | **0,892521** | **0,36438685** | **0,38403028** |
| ROC-AUC | — | — | **0,82181085** | **0,82189958** |
| Brier score | — | — | **0,02839840** | **0,03369795** |

Dấu “—” biểu thị chưa dùng con số trong bảng nguồn hiện tại, không phải metric bằng 0. Kết quả giữa các datasets không thể dùng làm ranking thuần túy về mức “tốt hơn” của classifier vì fraud prevalence, không gian đặc trưng, nhiệm vụ và nền dữ liệu khác nhau; PR-AUC đặc biệt phụ thuộc tỷ lệ fraud. Trong mỗi dataset, cần phân tích score drift và độ nhạy policy trong các nhóm chất lượng score tương ứng.

IEEE fast online scorer được báo cáo đã so khớp với frozen original predictions trên **88.581 events** ở dòng test không thay đổi, max absolute difference **4,3138 × 10^-7**, đạt ngưỡng tolerance 10^-6. Đây là một đối chiếu thực nghiệm được ghi nhận trong run report; cần lưu lại artifact/command/hash và kiểm tra bằng runner canonical trước khi đóng dấu final reproducibility.

## 3.6. Thiết lập cơ chế mô phỏng và biến thực nghiệm

**Independent factors:** environment `{Xente,IEEE}`, fraudster mode `{StaticMixture,Adaptive}`, policy `{Fixed,Capacity-aware}`, normalized capacity `{0.75,1.00,1.25}`.

**Policy/operational semantics dùng chung:**
- Base review threshold từ validation score tail top 1,00%; congestion soft/hard chuyển sang 0,75% và 0,50% review tails.
- Direct BLOCK threshold top 0,10% validation tail trong core đã đóng băng; sensitivity 0,05%/0,20% nếu chạy.
- Queue discipline: FIFO baseline; risk-priority là structural sensitivity.
- Relative capacity: tốc độ phục vụ = tỉ số năng lực × validation base alert arrival rate.
- Congestion indicator: `backlog_hours = queue_size / pooled_service_rate_per_hour`, triggers baseline 24/72 h; đây là rule/assumption, không đo đạc từ tổ chức cụ thể.
- Adaptive rule: incremental value update `α=0.15`; exploration `ε=0.10`; dormancy off để giữ số attempt slots có thể đối chiếu.
- Reward normalized bởi median fraud validation amount/value **riêng từng scenario**; không so sánh reward tiền tuyệt đối giữa Xente và IEEE.

**Outcome groups:** (i) direct BLOCK; (ii) fraud approved; (iii) REVIEW entered, service started/completed; (iv) unresolved review at horizon; (v) legitimate REVIEW/BLOCK; (vi) total alert load, waiting times/backlog; (vii) strategy shares. Mọi thước đo “fraud prevented” từ review phải gắn giả định về service completion và effectiveness `q`.

## 3.7. Khung so sánh phản thực tế và độ bất định

Phân tích trong từng scenario dựa trên hiệu số paired theo seed:
- **Policy effect** = Capacity-aware − Fixed, giữ fraudster mode và capacity.
- **Adaptation effect** = Adaptive − StaticMixture, giữ policy và capacity.
- **Capacity interaction**: so sánh thay đổi các hiệu số trên giữa các mức Low, Medium, High.

Khi báo cáo hiệu ứng, cần nêu chiều tốt/xấu riêng từng thước đo: giảm backlog thường tốt về congestion nhưng có thể song hành với tăng exposure hoặc giảm số lượng review; tăng tỷ lệ fraud intercepted proxy không tự suy ra giảm thiệt hại thực.

Với các kết quả từ nhiều seeds, báo trung bình, SD, Monte Carlo SE và khoảng tin cậy phù hợp. Chênh lệch theo cặp chỉ có giá trị giảm biến thiên nếu cách dùng RNG và việc matching seed tạo tương quan thích hợp; adaptive feedback có thể khiến các trajectories rẽ nhánh nên không thể ngầm định đồng nhất ở mọi event.

**Không so sánh** raw `Value` của Xente với `TransactionAmt` của IEEE; thay bằng hiệu ứng tương đối, tỷ lệ, dấu, hướng và bất định trong từng environment. Nếu muốn tổng hợp thống kê giữa hai scenarios, phải phát biểu rõ đơn vị/normalization, không pooled fraud base rates.

## 3.8. Tình trạng bằng chứng và khả năng tái lập

**Xente:** đã có 12 cấu hình × 50 seeds chính, 30-seed degraded-score và các sensitivity targeted. **IEEE:** baseline/score-equivalence đã báo cáo kiểm tra trên dữ liệu thực; có **pilot 12 cấu hình × 5 seeds**; các kết quả pilot được tạo từ local implementation mô phỏng logic shared engine nhưng **chưa được nghiệm thu bằng canonical repository runner** và chưa đủ seed convergence cho kết luận cuối.

Trước khi viết kết quả chính thức, phải tạo run manifest gồm Git commit SHA, Python/dependency versions, đường dẫn/sha256 artifact private, frozen parameters, seeds, CLI commands, cell count, comparison against pilot và acceptance checks. Raw transaction files và model bundles không được commit công khai.

## 3.9. Đạo đức và giới hạn dữ liệu

Nguồn dữ liệu là bộ dữ liệu cuộc thi có điều kiện sử dụng riêng; việc sử dụng, trích dẫn và công bố artefact phải tuân theo điều khoản tương ứng. Nghiên cứu không sử dụng hoặc công bố dữ liệu doanh nghiệp nội bộ, thông tin cá nhân có thể định danh hay kết quả thực nghiệm từ môi trường Green SM. Nếu có chuyên gia thực tế đóng góp sau này, cần quy định phạm vi cho phép sử dụng, bảo mật và ghi nhận evidence type phù hợp.

## Nguồn dữ liệu và kết quả gốc

- [Xente Fraud Detection Challenge — Zindi](https://zindi.world/competitions/xente-fraud-detection-challenge/data).
- [IEEE-CIS Fraud Detection — Kaggle](https://www.kaggle.com/competitions/ieee-fraud-detection/data).
- `03 Model design/Data Audit.md`; `05 Experiments/Xente Empirical Profile.md`; `05 Experiments/Xente Feature-Level Core Run v0.2.md`.
- `05 Experiments/IEEE-CIS Baseline and Policy Replay v0.1.md`; `05 Experiments/IEEE-CIS Adaptive Full-Test Pilot v0.2.md`.
- `scripts/train_ieee_streaming_baseline.py`; `scripts/prepare_ieee_closed_loop.py`; `scripts/run_ieee_feature_level_static_adaptive.py`; `scripts/audit_ieee_online_equivalence.py`.

> **Biên tập trước nộp:** cập nhật bảng thống kê các tập train/validation/test và tỉ lệ fraud của Xente theo log canonical; thêm bảng missingness/channels và histograms trực tiếp từ script có seed/commit; kiểm tra legal usage terms của datasets; đừng đưa IEEE pilot thành result cuối.
