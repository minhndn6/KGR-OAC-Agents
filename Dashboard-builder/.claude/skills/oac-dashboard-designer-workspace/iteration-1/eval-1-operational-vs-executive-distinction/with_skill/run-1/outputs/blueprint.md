# BLUEPRINT: Sales Ops Daily Monitor — Theo dõi đơn hàng hằng ngày theo kênh & chuỗi

## 1. Bối cảnh
- **Audience:** Team Sales Operations · **Loại: OPERATIONAL** · **Nhịp:** hằng ngày sáng 8-9h + giữa chiều · Desktop.
- **Khác executive:** executive xem tuần/tháng hỏi "đạt plan không?" (BAN to, trend, ít filter); operational xem NGÀY hỏi "hôm nay lệch chuẩn gì cần can thiệp NGAY?" (ngưỡng cảnh báo đỏ/cam, danh sách chuỗi/kênh cụ thể, hành động gắn vào viz). Nhịp hành động: executive phân bổ tháng/quý, ops can thiệp trong ngày.
- **4 quyết định hằng ngày:** kênh chậm run-rate → ưu tiên gọi hôm nay · chuỗi hụt nhịp tháng → leo thang/chương trình bù · đơn hủy đột biến → điều tra · tổng đơn đủ nhịp target tháng → push thêm?

## 2. Dữ liệu (theo mô tả — verify khi build)
Order (1 dòng=1 đơn: ngày, kênh, chuỗi, trạng thái, giá trị) — ⚠️ check % đơn chưa gắn chuỗi, trạng thái hủy realtime hay lag. Plan (kênh × tháng) — ⚠️ check plan có grain chuỗi không (quyết định route Pace% chuỗi: calc vs dataflow phân bổ).

## 3. Ba canvas (mỗi canvas 1 câu hỏi)
### Canvas 1: "Hôm nay đang ở đâu so với nhịp tháng?"
4 BAN: Orders Today (xanh ≥ run-rate/cam <) · Projected Month-End Orders (run-rate EOM) · Cancellations Today (cam >5%/đỏ >10% — ngưỡng cần chốt) · MTD Pace % (xanh ≥100%/đỏ <85%). + **Horizontal Bar + Reference Line** "Orders by Channel vs Daily Target" (kênh dưới vạch = hụt → ưu tiên gọi, sort theo gap) + **Line 30 ngày** vs run-rate.

### Canvas 2: "Đơn hủy — bao nhiêu, kênh nào, xu hướng?"
BAN hủy + tỷ lệ hủy (⚠️ mẫu số nhỏ sáng sớm → ẩn trước 9h) · **Horizontal Bar** hủy theo kênh (phân biệt tuyệt-đối-cao vs tỷ-lệ-cao) · **Line** trend tỷ lệ hủy 30 ngày (đột biến vs leo dần) · **Table hành động** đơn hủy hôm nay sort giá trị + Use as Filter.

### Canvas 3: "Chuỗi nào hụt nhịp tháng — leo thang ngay?"
**Horizontal Bar + ref 100%** "Chain MTD Pace vs Run-Rate" (đỏ <85% lên đầu = danh sách ưu tiên can thiệp) · **Grid Heat Map** chuỗi × tuần (hụt đều structural vs hụt 1 tuần event) · **Stacked Bar** chuỗi × kênh (đổi cơ cấu kênh?) · **Table** Target/Actual/Gap/Pace% + CF, Use as Filter sang Canvas 2.

## 4. Metric (chốt trước build): Đơn hôm nay (status IN Confirmed/Delivered) · Tỷ lệ hủy ngày · Run-rate EOM = (Σ MTD/ngày qua)×ngày tháng · MTD Pace % = actual/(target×ngày qua/tổng ngày) · Gap MTD. Route: calc; Pace% chuỗi cần dataflow nếu plan không có grain chuỗi.

## 5. ⭐ Phái sinh đề xuất thêm: **Ngưỡng "điểm không thể phục hồi"** (hụt không thể bù dù push max → leo thang manager) · **Chuỗi hụt 2 tuần liên tiếp** (pattern ≠ nhiễu) · Tỷ lệ hủy theo giờ trong ngày · Contribution top-5 chuỗi vào gap tổng.

## 6. Caveats & 4 open questions: plan có grain chuỗi? · "hủy" tính lúc nào (lag)? · ngưỡng cảnh báo ops hiện dùng? · cần mobile?

## 7. Thứ tự: verify grain → (dataflow phân bổ nếu cần) → Canvas 1 → 3 → 2 → drill liên canvas. DoD: BAN khớp số ops, ngưỡng màu đúng + cấu hình được (không hardcode), title EN/note VN, persist.

Duyệt blueprint này chứ?
