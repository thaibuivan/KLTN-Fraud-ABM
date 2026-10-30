# Thiết kế Adaptive Fraudster v0.1

## Mục đích

Adaptive fraudster là **cơ chế stress-test policy**, không phải mục tiêu cuối cùng của đề tài.

Fraudster quan sát phản hồi của hệ thống rồi điều chỉnh strategy theo thời gian.

## State

Có thể gồm:
- current strategy;
- strategy value estimates;
- recent success rate;
- số lần block liên tiếp;
- lịch sử phản hồi gần đây;
- dormancy counter nếu dùng.

## Action

Prototype ban đầu chỉ cần một số strategy trừu tượng:

- low-amount / threshold-avoidance;
- high-amount;
- timing shift;
- identity/card switching.

Chỉ thêm strategy đặc thù khi có public evidence hoặc ghi rõ là assumption.

## Observation

System response:
- APPROVE;
- CHALLENGE / STEP-UP;
- REVIEW;
- BLOCK.

## Reward

Một dạng đơn giản, dễ giải thích:

```text
APPROVE fraud  -> reward dương, có thể tỷ lệ theo amount
CHALLENGE      -> penalty
REVIEW         -> penalty nhỏ/vừa
BLOCK          -> penalty lớn
```

## Learning rule

Bản đầu nên dùng cơ chế dễ kiểm soát:

```math
V_s^{new} = V_s^{old} + \alpha(r_t - V_s^{old})
```

Trong đó:
- `V_s`: giá trị ước lượng của strategy s;
- `r_t`: reward vừa quan sát;
- `alpha`: learning rate.

Strategy selection có thể dùng epsilon-greedy.

Không cần Deep RL trong MVP.

## Dormancy

Nếu bị block liên tiếp vượt ngưỡng, fraudster có thể inactive vài bước rồi quay lại.

Đây là behavioral assumption nếu không có independent evidence.

## Parameter nào không được giả vờ là empirical?

Các parameter sau thường không được IEEE-CIS/Xente xác định trực tiếp:

- learning rate;
- exploration rate;
- consecutive-block tolerance;
- dormancy duration;
- strategy-switch rule.

Do đó phải:
- ghi rõ là assumption;
- chọn plausible ranges;
- sensitivity-test.

## Static comparator

Static fraudster:
- dùng fixed strategy;
- không update strategy value.

Experiment 1 so sánh static vs adaptive dưới cùng các điều kiện khác.
