# KLTN — Thử nghiệm chính sách quản lý gian lận bằng ABM

Đây là kho làm việc cho khóa luận về **thử nghiệm chính sách quản lý gian lận giao dịch bằng mô phỏng dựa trên tác tử (Agent-Based Modelling — ABM)**.

## Hướng nghiên cứu hiện tại

> Dùng ABM như một “phòng thí nghiệm chính sách” để stress-test các chính sách quản lý gian lận trong một hệ thống động, nơi fraudster có thể thích nghi với phản hồi của hệ thống và fraud analyst có năng lực review hữu hạn.

Cách hiểu ngắn gọn:

- **Mục tiêu nghiên cứu:** thử nghiệm / stress-test chính sách.
- **ABM:** công cụ nghiên cứu.
- **Adaptive fraudster:** cơ chế tạo áp lực đối kháng lên policy.
- **Alert queue + analyst capacity:** ràng buộc vận hành.
- **Risk model / ML:** một thành phần của hệ thống, không phải mục tiêu cuối.
- **Dữ liệu:** dùng để grounding các phân bố, state và risk score; không giả vờ tái tạo chính xác một ngân hàng thật.

## Bắt đầu đọc từ đâu?

Đọc theo thứ tự:

1. `00 Dashboard/READING ORDER.md`
2. `00 Dashboard/Current Direction - 2026-10-11.md`
3. `03 Model design/Research Design v1.0 - Policy Experimentation.md`
4. `03 Model design/Conceptual Model v1.0 - Adaptive Policy ABM.md`
5. `04 Meetings/GVHD Brief - Current Direction 2026-10-11.md`

Sau đó mới đọc các file parameter, data, experiment và code.

## Hai môi trường dữ liệu dự kiến

### Scenario A — IEEE-CIS
Đại diện cho môi trường online/card/e-commerce.

### Scenario B — Xente
Đại diện cho môi trường mobile/payment/e-commerce tại Uganda.

**Không ghép hai dataset thành một dataset lớn.** Mỗi dataset parameterize một scenario riêng của cùng framework.

## Những gì đã làm được từ hướng Xente trước đây

Phần này **không bỏ đi**, vì đã có nhiều kết quả và code thật:

- audit và profile Xente;
- leakage-safe customer-history features;
- chronological logistic risk baseline;
- persistent alert queue;
- FIFO vs risk-priority;
- capacity stress;
- threshold/load sensitivity;
- stochastic service-time robustness;
- variable team-capacity sensitivity;
- unit tests cho queue.

Các file cũ nói “Xente là core duy nhất”, “IEEE chỉ optional” hay “adaptive fraudster không phải core” đã **hết vai trò định hướng**, nhưng vẫn được giữ để truy vết và tái sử dụng mechanism.

## Code chính hiện có

### Xente / queue
- `scripts/profile_xente.py`
- `scripts/build_xente_features.py`
- `scripts/train_xente_baseline.py`
- `scripts/simulate_alert_queue.py`
- các script sensitivity / robustness.

### Adaptive fraudster
- `scripts/adaptive_fraudster.py`
- `scripts/run_adaptive_vs_static.py`
- `tests/test_adaptive_fraudster.py`

Lưu ý: adaptive runner hiện mới là **smoke test**, chưa phải kết quả khóa luận.

## Quy tắc Git

- `main`: bản ổn định đã chấp nhận.
- `chatgpt-draft`: branch đang làm việc / review trước khi merge.

## Bảo mật và dữ liệu

Không commit:
- raw Xente / IEEE-CIS;
- dữ liệu nội bộ công ty;
- threshold/rule proprietary;
- API key, token, mật khẩu;
- dữ liệu người dùng nhạy cảm.

## Giới hạn claim

Không claim:
- digital twin của ngân hàng;
- fraudster trong model suy nghĩ giống fraudster thật;
- một policy tối ưu phổ quát;
- ngưỡng/staffing production cho một tổ chức cụ thể.

Kết luận phải luôn gắn với scenario, assumption và parameter range đã thử.
