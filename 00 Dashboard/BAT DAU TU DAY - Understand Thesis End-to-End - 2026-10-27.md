# BẮT ĐẦU TỪ ĐÂY — HIỂU TOÀN BỘ KHÓA LUẬN FRAUD-ABM

**Bản học hiểu và bàn giao nghiên cứu — 27/10/2026**  
**Nguồn code:** [GitHub KLTN-Fraud-ABM](https://github.com/thaibuivan/KLTN-Fraud-ABM/tree/chatgpt-draft). Commit HEAD đã xác minh khi lập guide: `317d4b684d`.  
**Bản thảo nghiên cứu để đọc:** `KLTN_ABM_BAN_CUOI_DE_REVIEW_2026-10-22.docx/pdf` (38 trang, được bàn giao trong cuộc trò chuyện, *không nằm trong repo*).  
**Mục đích:** Giúp tác giả *thực sự giải thích được* từng lựa chọn, phép tính, luồng code, thí nghiệm, bằng chứng và giới hạn khi làm việc với GVHD/hội đồng. Đây là tài liệu định hướng/giảng giải, không thay thế các bảng dữ liệu thí nghiệm theo seed.

---

## A. Bức tranh 90 giây: bạn đang nghiên cứu cái gì?

**Tóm tắt 1 câu:** Dùng mô phỏng gồm tác tử gian lận có thể học từ phản hồi và một hệ thống xử lý cảnh báo có năng lực hữu hạn để **stress-test** hiệu quả tương đối của hai chính sách quản lý giao dịch gian lận, dưới ba mức năng lực và hai môi trường dữ liệu.

### Xuất phát điểm và sự phát triển

Đề án trước có sơ đồ: `risk score → policy → capacity → outcome`. Khóa luận bổ sung:
1. **Feedback/closed-loop:** fraudster thay đổi lựa chọn trong những giao dịch tiếp theo dựa trên quyết định hệ thống.
2. **Persistent queue:** REVIEW có thể chờ từ sự kiện này sang sự kiện sau, không giả định mọi alert được xử lý tức thời.
3. **Empirical grounding:** riêng Xente và IEEE-CIS có dữ liệu, feature/history, mô hình risk và kịch bản đầu vào khác nhau.
4. **Experimental uncertainty:** lặp lại seeds và kiểm tra độ nhạy để không gán một kết quả tình cờ thành quy luật.

**Không làm:** thuật toán ML mới tối ưu nhất, dự đoán hành vi tội phạm thật, mô phỏng toàn bộ ngân hàng (digital twin), tìm staffing hay threshold tối ưu để triển khai thật.

### Bốn câu hỏi nghiên cứu — phải thuộc

| RQ | Điều cần biết | Phép so sánh |
|---|---|---|
| RQ1 — Adaptation | Fraudster có cập nhật chiến lược làm thay đổi outcome không? | Adaptive − Static (giữ policy và capacity) |
| RQ2 — Policy | Capacity-aware đánh đổi fraud/intervention/backlog thế nào so với Fixed? | Capacity-aware − Fixed (giữ fraudster/capacity) |
| RQ3 — Capacity | Những hiệu ứng đó có thay đổi khi nguồn lực nhiều/ít? | Low vs Medium vs High; interaction |
| RQ4 — Cross-scenario | Kết luận nào bền vững giữa hai môi trường? | So *hướng và hiệu ứng chuẩn hóa*, không gộp tiền thô |

## B. Bản đồ luồng nghiên cứu xuyên suốt

```text
TÀI LIỆU HỌC THUẬT + BÀI TOÁN QUẢN LÝ GIAN LẬN
      |
      v
4 RQs, giả thuyết định hướng, claim boundaries
      |
      v
DỮ LIỆU XENTE ------------------------ DỮ LIỆU IEEE-CIS
CustomerId, real timestamps           TransactionDT (relative), card/device
Value, product/channel                TransactionAmt, ProductCD, entity proxy
      |                                      |
      v                                      v
Chronological 70/15/15 split  (RIÊNG TỪNG DATASET)
      |                                      |
      +--> TRAIN: fit score model + encoders/features
      +--> VALIDATION: risk thresholds, base alert rate,
      |                fraud donor/context pools, reward scale
      +--> HELD-OUT TEST: event timeline; labels dùng để
                       xác định fraud-attempt slots và để đo outcome
      |
      v
       SCENARIO-SPECIFIC EVENT/SCORING PIPELINE
       observed legitimate events + generated fraud contexts
       chronological history --> frozen model --> risk score p
      |
      v
FRAUDSTER DECISION: STATIC MIXTURE / ADAPTIVE (epsilon-greedy)
       |        chọn amount regime trong validation fraud donor pools
       v
POLICY: FIXED / CAPACITY-AWARE  <-- queue length / service capacity
       |        risk score -> APPROVE / REVIEW / BLOCK
       v
REVIEW QUEUE: FIFO, finite service capacity (Low/Medium/High)
       |        service_start, service_end, backlog/waiting
       v
MODEL OUTCOME LEDGER + FEEDBACK  ------> fraudster strategy updates
       |
       v
24 CELLS × nhiều seeds, matched contrasts, sensitivity
       |
       v
XENTE vs IEEE: policy gain, adaptation, capacity, robustness
       |
       v
THESIS: Data - Method - Results - Discussion - Limitations
```

**Điều quan trọng:** Vòng mô phỏng chạy theo giao dịch/sự kiện, không phải “huấn luyện lại classifier mỗi khi fraudster thay đổi”. Classifier **frozen**, nhưng đặc trưng/history và các risk scores của giao dịch phản thực tế có thể thay đổi theo quá trình mô phỏng.

## C. Hai bộ dữ liệu: khác nhau ở đâu, tại sao cần cả hai?

| Nội dung | Xente | IEEE-CIS |
|---|---|---|
| Labeled dataset | 95.662 dòng; 193 fraud | 590.540 dòng; 20.663 fraud |
| Đặc điểm quan trọng | CustomerId và timestamp thực; Value và product/channel | TransactionAmt, ProductCD, card, address, identity/device, relative TransactionDT |
| Lịch sử | CustomerId + các đặc trưng past-only | `card1+addr1` chỉ là *entity proxy* và các đặc trưng past-only |
| Risk baseline | Logistic regression | SGDClassifier log-loss (streaming) |
| PR-AUC validation / test đã ghi | 0,560851 / 0,892521 | 0,364387 / 0,384030 |
| Giá trị tiền | Xente Value | IEEE TransactionAmt — không mặc nhiên cùng đơn vị |
| Closed loop | Fraud counterfactual rescored, legitimate observed scores frozen | Generated fraud và legitimate test events rescored online |

**IEEE labeled holdout ≠ official unlabeled competition test:** 70%/15%/15% là chia từ 590.540 giao dịch có nhãn của `train_transaction.csv`. Test ở đây là 15% cuối của labeled training set, 88.581 giao dịch (3.083 fraud slots). Không dùng nhãn Kaggle official test chưa biết.

**Leakage logic:** train fit mô hình, validation chọn threshold/donor, test giữ cho counterfactual schedule/outcome. Tuy nhiên, *test labels được dùng để ấn định các vị trí giả lập fraud attempt*; do đó kết luận có điều kiện trên lịch xuất hiện attempt đã biết, không phải dự báo được lịch tấn công thật.

**IEEE temporal drift đã quan sát:** validation mean risk score khoảng 0,06534 và test khoảng 0,09464; threshold chọn cho 1% validation alerts tạo khoảng 1,5489% alerts trên test. Vì vậy queue có thể chịu tải khác mức tham chiếu dù policy threshold vẫn đóng băng.

**IEEE donor caveat:** 3 nhóm low/middle/high được phân theo validation fraud `TransactionAmt` terciles (50 và 117). Generator lấy **toàn bộ hàng donor** trong nhóm; đổi strategy cũng làm đổi phân phối ProductCD/card/device context. Đây không phải can thiệp nhân quả tách riêng `TransactionAmt`. Ví dụ `ProductCD=C` chiếm khoảng 62,2% ở nhóm low và 10,5% ở high.

## D. Mô hình: hiểu bằng 1 giao dịch mô phỏng

Giả sử có một transaction xảy ra ở thời điểm t. Đây là ví dụ khái niệm, **không dùng các con số score dưới đây làm threshold thật**:

1. **Nguồn event:** nếu là legitimate → lấy event đang quan sát; nếu là fraud attempt → agent chọn strategy (low/middle/high) rồi lấy donor validation phù hợp, tạo một giao dịch phản thực tế.
2. **History:** hệ thống tạo biến quá khứ (velocity/frequency/delta time); không dùng sự kiện tương lai.
3. **Risk model:** mô hình đã huấn luyện tạo `p_t` (risk score) từ event hiện tại và history.
4. **Policy:** so `p_t` với threshold; BLOCK ưu tiên ở mức nguy cơ cao; REVIEW đi hàng đợi; APPROVE đi tiếp.
5. **Queue:** nếu REVIEW, sự kiện vào hàng FIFO; analyst pooled capacity quyết định thời điểm bắt đầu/hoàn tất review. Nếu chậm, backlog tăng.
6. **Feedback:** trong chế độ Adaptive chính, agent nhận phản hồi tương ứng với action ngay lúc policy decision rồi cập nhật chiến lược. Đây là **giả định observability**: real fraudster có thể không biết alert REVIEW nội bộ.
7. **Next event:** cập nhật history, queue và state agent; xử lý sự kiện tiếp theo. Hiệu ứng tích lũy có thể không tuyến tính.

### Bốn đối tượng bạn phải phân biệt

- **Fraudster agent:** có trạng thái và ra quyết định theo chiến lược; phần ABM rõ nhất.
- **Risk engine:** module dự đoán điểm gian lận; không phải tác tử học theo mỗi test event.
- **Policy:** quy tắc APPROVE/REVIEW/BLOCK; Capacity-aware quan sát trạng thái congestion.
- **Queue + pooled analyst service:** logic discrete-event, sức phục vụ hữu hạn; không nên gọi đây là đội nhân viên thật với năng suất đã được đo.

Vì thế mô tả chặt chẽ: **hybrid agent-based adversarial behavior + event-driven fraud-policy/queue simulation**.

### Fraudster static và adaptive

StaticMixture chọn strategy từ một phân phối xác định bằng validation fraud, **không học từ feedback**.

Adaptive sử dụng `epsilon-greedy`: với xác suất `epsilon`, thử strategy ngẫu nhiên; còn lại ưu tiên strategy có giá trị ước lượng lớn. Sau kết quả mô hình:
`V_s(t+1) = V_s(t) + alpha [r_t - V_s(t)]`

Baseline `alpha=0.15`, `epsilon=0.10` là **giả định nghiên cứu**, không được ước lượng từ tâm lý đối tượng gian lận. Reward theo giá trị giao dịch đã chuẩn hóa bởi median fraud validation trong mỗi dataset (Xente median Value 400.000; IEEE median amount 77). Reward cho APPROVE dương, REVIEW/BLOCK âm tương ứng theo rule; giá trị reward và selection có thể tạo preference mạnh, nên cần kiểm định reward ablation.

### Fixed và Capacity-aware

- **Fixed:** giữ ngưỡng REVIEW đã hiệu chỉnh trên validation cho tail 1%, ngưỡng BLOCK riêng cho tail 0,1%.
- **Capacity-aware:** khi `backlog_hours = queue_size / service_rate` chạm 24 và 72 h (baseline), chuyển sang các ngưỡng REVIEW có review rate mục tiêu 0,75% và 0,5% trên validation; BLOCK rule không tự đổi.
- **Capacity Low/Medium/High:** tốc độ phục vụ = 0,75 / 1,0 / 1,25 × validation baseline alert arrival rate. **Không phải số nhân viên thật**.

**Hệ quả cơ học:** ngưỡng review tăng khi tắc nghẽn → ít alerts vào queue → backlog có thể giảm. Đóng góp nghiên cứu không chỉ là chỉ ra backlog giảm, mà là đo **đánh đổi với fraud-related outcomes và can thiệp lên giao dịch hợp lệ**.

## E. Cách các thực nghiệm được cấu trúc

Tổng lõi = 2 datasets × 2 fraudster modes × 2 policies × 3 capacities = **24 cells**: mỗi dataset có **12 cells**. Chạy lại dưới nhiều random seeds để lấy phân phối kết quả theo cơ chế sampling và learning.

- **Xente:** tài liệu core ghi 12 cells × 50 seeds; degraded-score 12 × 30 seeds; cùng các sensitivity về alpha, epsilon, BLOCK, congestion.
- **IEEE:** bản thảo cuối 22/10 **báo** canonical 12 cells × 30 seeds = 360 rows run-level; con số này được dùng trong Chương 5. **Lưu ý provenance:** run-level CSV/manifest từ đợt 30 seeds không có trong public GitHub, và khi đối chiếu hướng dẫn ngày 27/10, chưa độc lập mở lại các bytes đó. Kết quả bảng Word là nguồn báo cáo của phiên mô phỏng, không thể thay thế file output có checksum.
- **Static vs Adaptive**, **Fixed vs Capacity-aware** được so **trong cùng scenario**; điều kiện/seed được ghép khi tính contrasts. Phải dùng CI/MCSE để tránh đọc sai một hiệu số do stochasticity.

### Công thức cần nắm

**Policy effect** tại (scenario, fraudster, capacity):  
`Delta_policy = E[Y | Capacity-aware] - E[Y | Fixed]`

**Adaptation effect** tại (scenario, policy, capacity):  
`Delta_adapt = E[Y | Adaptive] - E[Y | Static]`

**Policy × adaptation interaction:**  
`[Y_Adaptive,CapacityAware - Y_Adaptive,Fixed] - [Y_Static,CapacityAware - Y_Static,Fixed]`

**Uncertainty:** báo mean, standard deviation, `MCSE=SD/sqrt(N)`, CI95% t trên paired seed-differences khi phù hợp. Đây là **Monte Carlo uncertainty conditional on model**; nó không giải quyết toàn bộ bất định cấu trúc hoặc sự khác biệt với thế giới thật.

### Metrics — cực kỳ quan trọng khi bảo vệ

- `fraud_intercept_rate` **legacy proxy** = fraud được direct BLOCK **hoặc** REVIEW mà analyst **bắt đầu** phục vụ trước cuối horizon. **Không phải tỷ lệ tiền gian lận thực sự tránh được**.
- `review_count`: số giao dịch policy route vào REVIEW; không đồng nghĩa với số đã hoàn tất.
- `backlog_end`: pending chưa bắt đầu service theo accounting của engine.
- `legitimate_intervention_rate`: legitimate REVIEW hoặc BLOCK / tổng legitimate quan sát trong mô phỏng.
- `fraud_exposure_at_horizon`: amount proxy theo semantics đã xác định, không gọi realized bank losses.
- q-sensitivity có thể tính hypothetical prevention với q ∈ {0,0.5,1} chỉ dành cho fraud REVIEW đã **hoàn tất** trong horizon, cộng với direct BLOCK theo giả định; q **không phải recovery rate ước lượng từ ngân hàng**.

## F. Kết quả nên hiểu theo RQs

### RQ1 — adaptation thay đổi chiến lược

Xente core ghi Adaptive tăng low-value share khoảng **36,8% → 88,7%**, interception theo số lượng thường giảm khoảng **14–17 điểm phần trăm** so với Static, nhưng total fraud amount exposure có thể giảm do amount composition thấp hơn.

Bản Word IEEE 30 seeds báo Adaptive tập trung vào **high-amount** (Static khoảng **31,65%**, Adaptive khoảng **92,52%**) thay vì low như Xente. **Không kết luận kẻ gian lận thật tại hai miền này thích low/high.** Đây là kết quả tương tác reward + donor-context distribution + frozen score/policy.

### RQ2 — Capacity-aware vs Fixed

- Xente Low: theo bảng báo cáo, effect interception proxy **Static ~−1,72 điểm %; Adaptive ~−3,20 điểm %** khi dùng Capacity-aware.
- IEEE Low: trong bản Word 30 seeds, effect interception proxy **Static ~+3,08 điểm %; Adaptive ~+1,04 điểm %**, kèm t-interval theo paired seeds trong bảng Chương 5.
- Cả hai môi trường có bằng chứng mô phỏng Capacity-aware làm giảm congestion/backlog dưới scarcity.

**Thông điệp cốt lõi:** chính sách responsive với congestion có thể giảm backlog, nhưng hiệu quả fraud theo proxy **không có hướng ưu thế phổ quát giữa Xente và IEEE**. Kết luận phải gắn với metric, detector quality, reward assumption, capacity và từng scenario.

### RQ3 — capacity

Nếu tăng service rate, backlog thường giảm và nhiều review có thể bắt đầu trước finite horizon hơn. Đây phần nào là hệ quả cấu trúc. Câu hỏi có giá trị là *policy gain* thay đổi bao nhiêu, dấu có đổi hay có thể hòa bằng khi capacity đủ lớn.

### RQ4 — cross-scenario

Không so raw tiền Uganda/Xente với amount IEEE; không coi cùng raw score threshold có cùng ý nghĩa. Nên so chiều của contrast, độ lớn tương đối trong từng dataset, uncertainty và mức nhạy với assumptions. Cross-environment khác dấu là **environment-dependent finding**, không phải thất bại của khóa luận.

## G. Những giới hạn bạn phải nói rõ với GVHD

1. Không đo được cách fraudster thực tế học hỏi; epsilon-greedy là stress mechanism.
2. Fraud-attempt times cố định theo heldout labels; không sinh độc lập tần suất fraud.
3. Xente observed legitimate risk scores frozen, IEEE legítimate scores rescored online; có khác biệt cấu trúc đáng kể giữa hai scenarios.
4. Xente generated fraud dùng một synthetic-fraudster identity; có thể khiến online history/velocity có cấu trúc đặc thù.
5. IEEE amount-regime donor là cả bundle amount+context, không phải tác động nhân quả riêng của amount.
6. REVIEW có thể là alert nội bộ, fraudster trong thực tế không nhìn thấy; immediate REVIEW feedback là assumption.
7. Không có observed analyst error/service-time, true loss/recovery hay bank staffing; outcomes là proxies.
8. Không thể suy kết quả chắc chắn trong thực tế chỉ từ CI qua random seeds; còn parameter/model discrepancy.

**Chú ý về validation:** CI/test code xanh kiểm tra *phần mềm thực hiện đúng quy tắc lập trình*, không chứng minh *quy tắc phản ánh đúng ngân hàng thực*. Đó là hai câu khác nhau.

## H. Bản đồ file chính xác: đọc cái nào, theo thứ tự nào?

> Chỉ cần 12 mục cốt lõi. Các tài liệu v0.x lịch sử chủ yếu để kiểm tra quyết định thiết kế, không phải bắt buộc đọc toàn bộ.

| Bước | File trong repo | Đọc để trả lời |
|---|---|---|
| 1 | `03 Model design/Research Design v1.1 - Develop from FinRisk Proposal.md` | Vì sao có RQ1–RQ4, contribution là gì? |
| 2 | `03 Model design/ODD Hybrid ABM-DES Specification v1.0.md` | Có những agent/modules/states nào, schedule ra sao? |
| 3 | `03 Model design/Operational Core Freeze v1.0.md` | Các policy/capacity/queue/reward assumptions cụ thể? |
| 4 | `scripts/build_xente_features.py` và `scripts/build_ieee_features.py` | History/data-to-features làm gì và chống leakage ra sao? |
| 5 | `scripts/train_xente_baseline.py` và `scripts/train_ieee_streaming_baseline.py` | Frozen detectors học từ dữ liệu nào? |
| 6 | `scripts/adaptive_fraudster.py` | Static/Adaptive khác nhau ở đâu? Epsilon-greedy cập nhật thế nào? |
| 7 | `scripts/fraud_policies.py` | Hệ thống quyết định APPROVE/REVIEW/BLOCK như thế nào? |
| 8 | `scripts/policy_queue_engine.py` và `scripts/outcome_semantics.py` | Queue và metrics được tính chính xác như thế nào? |
| 9 | `scripts/run_xente_feature_level_static_adaptive.py` | Trình tự một thí nghiệm Xente? |
| 10 | `scripts/run_ieee_feature_level_static_adaptive.py` | IEEE khác Xente thế nào ở data/history/rescoring? |
| 11 | `05 Experiments/Xente Feature-Level Core Run v0.2.md` và bản Word Chương 5 | Kết quả chính và trade-off? |
| 12 | `scripts/summarize_ieee_closed_loop.py` và `05 Experiments/Cross-Scenario Comparison Plan v1.0.md` | Paired contrasts, confidence intervals, cross-scenario conclusions? |

Mở source từng file tại: [GitHub branch chatgpt-draft](https://github.com/thaibuivan/KLTN-Fraud-ABM/tree/chatgpt-draft); tra cứu tên file từ ô tìm kiếm trong repository. Để chuẩn bị manuscript, đọc tiếp `06 Writing/Methodology Full Draft v1.1.md` và bản DOCX cuối (không đọc bản Results GitHub v1.2 cũ như final data).

## I. Lộ trình 5 buổi để tự tin trình bày khóa luận

**Buổi 1 — Vì sao làm?**  
Đọc Chương 1–2 trong Word, tài liệu Research Design v1.1. Tự nói trong 2 phút “đề tài, research gap, 4 RQs, phạm vi đóng góp”; so với Shen & Kurshan (2020), không claim sáng chế dynamic threshold.

**Buổi 2 — Dữ liệu đi vào mô hình như thế nào?**  
Đọc Chương 3 + module build/train. Tự vẽ train/validation/test, giải thích tại sao test labels dùng tạo fixed attempt slots không phải input vào scorer, vai trò donor validation và temporal drift.

**Buổi 3 — Mô hình chạy một giao dịch ra sao?**  
Đọc Chương 4 + four source files: `adaptive_fraudster`, `fraud_policies`, `policy_queue_engine`, `outcome_semantics`. Diễn giải cả đường APPROVE, REVIEW, BLOCK và feedback sau đó. Phải phân biệt service-start và service-completed.

**Buổi 4 — Thực nghiệm, thống kê và kết quả.**  
Đọc Chương 5, bảng 24 configurations, hai runners, summarizer. Tự tính một policy contrast Fixed vs Capacity-aware và lý giải trường hợp backlog giảm mà intercept có thể xấu đi. Phân biệt mean across seeds và CI over paired differences.

**Buổi 5 — Tự phản biện.**  
Đọc Limitations, ODD, parameter registry. Tự trả lời 12 câu ở phần J; chỗ nào chưa tự tin thì quay lại đúng module tương ứng, không cần đọc lại từ đầu.

## J. 12 câu phản biện phải trả lời trôi chảy

1. Tại sao gọi là ABM trong khi queue là discrete-event? **Vì hành vi đối kháng có agent state và feedback; mô hình được mô tả chính xác là hybrid ABM–DES.**
2. Vì sao dùng cả hai datasets? **Để test robustness theo empirical environments khác nhau, không nhằm pool dữ liệu.**
3. Tại sao cần risk classifier nếu đề tài không tập trung ML? **Policy cần score đầu vào; dùng frozen detector để cô lập các hiệu ứng downstream.**
4. Vì sao Static là đối chứng hợp lý? **Cùng donor regimes/timing; chỉ không cập nhật strategy values theo feedback.**
5. Alpha/epsilon đến từ đâu? **Assumptions cần sensitivity, không ước lượng hành vi thật.**
6. Tại sao 3 amount regimes? **Cách trừu tượng hóa có empirical donor support trên validation, không nhận diện kỹ thuật tấn công.**
7. Capacity-aware giảm backlog có hiển nhiên không? **Có một phần do load shedding; phải báo trade-off và so review budget.**
8. Có phải 30/50 seeds cho CI95% nghĩa là mô phỏng đúng thực tế? **Không: chỉ lượng hóa Monte Carlo uncertainty dưới mô hình.**
9. Vì sao nghiên cứu dùng test fraud labels? **Để cố định attempt slots trong stress scenario và tính outcome; không dùng để train detector hay chọn donor.**
10. Fraud interception là tiền đã ngăn được? **Không, REVIEW-start chỉ là một proxy; phải tách BLOCK, completed REVIEW, pending và q assumptions.**
11. Vì sao hai datasets cho dấu policy effect khác nhau? **Do detector, fraud context, score drift, reward/donor regimes và policy/queue tương tác; chưa chứng minh nguyên nhân nhân quả riêng.**
12. Đóng góp lớn nhất? **Chỉ ra các trade-offs/điều kiện robustness của chính sách trong hệ thống có feedback đối kháng và capacity constraints, kèm minh bạch assumptions.**

## K. Kiểm tra nguyên bản kết quả — việc quan trọng trước khi chốt hẳn

Có ba cấp bằng chứng; cần xem đúng loại:
1. **Bản thảo Word/PDF:** văn bản chính đã biên tập; bảng/nhận xét.
2. **GitHub scripts/CI:** code và verification tự động; version SHA, tests.
3. **Private run artifacts:** `ieee_closed_loop_runs.csv` (30×12), `cells.csv`, `policy_contrasts.csv`, `adaptation_contrasts.csv`, `manifest.json`, baseline SHA256; Xente run-level (50×12), sensitivity raw outputs. **Đây là vật chứng tái lập quan trọng nhất khi cần kiểm tra số liệu.**

Tại thời điểm lập guide ngày 27/10, GitHub branch mới nhất được xem là `317d4b684d`, CI của commit đó thành công. **Repo public chưa chứa bảng kết quả IEEE 30-seed hoặc Xente 50-seed theo từng seed.** Tài liệu trên GitHub vẫn có nhiều report cũ ghi pilot như trạng thái lúc viết. Bản Word 22/10 báo kết quả 30-seed và bản QA nêu không mở lại từng tệp run-level trong lượt biên tập cuối. Do đó **đừng nói cả bộ đã được một bên độc lập nghiệm thu raw artifact** trước khi kiểm tra những tệp này.

Nếu được yêu cầu tái lập, `scripts/complete_ieee_experiments.py` mô tả cách tái huấn luyện baseline, chuẩn bị context, audit score, chia batch seeds và tổng hợp. Cần Python 3.11, public Kaggle ZIP và đủ compute; không đưa raw competition data, model bundles hoặc thông tin nội bộ công ty vào GitHub public. Reference ODD/Methods cần được đối chiếu nếu source code mới thay đổi.

---

## L. Cách dùng tài liệu này khi làm việc với ChatGPT

Bạn có thể học tuần tự theo format vấn đáp, ví dụ:
- “Giảng cho tôi **Buổi 1** như người mới, sau mỗi phần hỏi 2 câu để kiểm tra.”
- “Chạy mô phỏng **một fraud transaction giả định** bằng các bước và công thức, chỉ rõ nơi phát sinh backlog.”
- “Đọc `scripts/policy_queue_engine.py` và giải thích theo thứ tự execution, liên hệ Chương 4.”
- “Đóng vai GVHD phản biện mạnh Chương 5, hỏi 10 câu khó và nhận xét câu trả lời của tôi.”
- “Lập danh sách từng bảng trong Word phải truy xuất từ CSV nào để audit reproducibility.”

**Nguyên tắc:** khi học một kết quả, luôn tìm lại được chuỗi `câu hỏi → biến đầu vào → code/module → run-level output → thống kê → cách diễn giải → claim boundary`. Nếu không truy ngược được một mắt xích, cần đánh dấu đó là phần chưa thực sự nắm chắc.
