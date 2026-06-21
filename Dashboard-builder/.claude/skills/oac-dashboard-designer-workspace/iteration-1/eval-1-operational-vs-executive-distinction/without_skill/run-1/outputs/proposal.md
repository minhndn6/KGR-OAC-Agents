# (BASELINE — không skill) Tư vấn Sales Ops Daily Dashboard

**3 canvas:** Đơn hôm nay ("bán được gì, ở đâu?") · Đơn hủy ("vấn đề gì xử lý ngay?") · Run-rate chuỗi ("chuỗi nào lỡ tháng nếu không can thiệp?").

**Canvas 1:** 4 KPI theo giờ (tổng đơn vs hôm qua, doanh số, backlog intraday, hủy vs TB 7 ngày) · bar ngang kép mỗi kênh (hôm nay vs TB 7 ngày) · bảng top 5 SP bán chạy · đường tích lũy đơn theo giờ (hôm nay vs hôm qua — phát hiện chậm nhịp trước 12h).

**Canvas 2:** logic cảnh báo (hủy >3% banner đỏ; kênh hủy tăng >20% vs TB7 cam; "hết hàng" >30% → Supply Chain) · bảng hủy theo kênh + mũi tên · bar lý do hủy (hết hàng→SC, giá→Sales, lỗi thông tin→CS) · line 14 ngày + ngưỡng 3% · thời gian hủy TB sau đặt (lỗi hệ thống).

**Canvas 3:** Pace % = actual lũy kế ÷ (target × ngày qua/tổng ngày); ngưỡng ≥90 xanh / 80-90 cam / <80 đỏ (họp ASM hôm nay) · pace bar theo chuỗi sort thấp→cao, vạch 100% · EOM forecast = actual ÷ pace% · 2 bảng drill: chuỗi hụt (gap) + chuỗi vượt (học playbook).

**Checks dữ liệu:** độ trễ cập nhật; cancel_reason null <5%; channel_code đủ 5 kênh; store_code join được target; target nhập trước ngày 1.

**Triển khai 3 pha:** P1 Canvas 1+3 KPI · P2 Canvas 2 (chuẩn hóa cancel_reason) · P3 alert email/Zalo pace <80% lúc 9h.

Chờ duyệt trước khi thực thi.
