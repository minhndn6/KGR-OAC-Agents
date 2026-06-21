# REVIEW THIẾT KẾ CANVAS EXECUTIVE — 6 MỤC (theo DASHBOARD_DESIGN_MASTERY §4/§5/§7)

**1. Pie 12 nhóm** (❌ §4 anti-pattern): pie chỉ khi <6 nhóm — người đọc kém so góc; 12 lát = mớ màu vô nghĩa, không sort tự nhiên. FIX OAC: **Horizontal Bar** sort desc + **Top Bottom N** filter (Top 8-10 + "Khác"); hoặc **Treemap** nếu cần 2 chiều size=DT, màu=YoY%.

**2. Dual-axis "thấy tương quan"** (❌ rất nặng — §4/§5): đổi tỷ lệ trục Y phải làm 2 đường cắt nhau ở bất kỳ đâu → tương quan ẢO. Tương quan thật cần kiểm định, không phải nhìn 2 đường. FIX OAC: (a) muốn 2 xu hướng riêng → **Trellis Rows** 2 panel cùng trục thời gian; (b) muốn đúng câu hỏi → chỉ số phái sinh **Doanh thu/đơn** (My Calculations) → 1 Line; (c) dual-axis chỉ hợp lệ cho plan-vs-actual (**Combo** bar xanh #44BA46 + line xám #636466).

**3. 9 KPI tile** (❌ §5 ≤6 KPI/Stephen Few): 9 tile = không biết nhìn đâu, mờ tín hiệu, chiếm hết chỗ primary chart. FIX: cắt còn 4-5 KPI thật sự gắn quyết định (DT MTD vs Plan%, GP%, YoY%, Achievement%); **Tile**+sparkline hoặc **KPI Tile Plugin** (Base/Target/Previous — mỗi tile tự kể "đạt/chưa"); tile thừa → canvas Operational riêng.

**4. Stacked bar 8 lớp × 12 tháng** (❌ §4): chỉ lớp đáy + tổng so được; 6 lớp giữa baseline trôi nổi → không đọc được. FIX OAC (theo mục đích): (A) xu hướng từng chuỗi → **Trellis Rows/Columns** (small multiples, cùng thang); (B) tỷ trọng dịch chuyển → **100% Stacked Area**; (C) đóng góp tăng trưởng → phái sinh **Contribution-to-growth** (§3) → Bar 1 lớp ± màu.

**5. Bar trục Y từ 300 tỷ** (❌ nặng nhất — §4/§5 trung thực thống kê): bar = so DIỆN TÍCH; baseline 300 tỷ làm 350 vs 700 tỷ trông như 1:7 thay vì 1:2 → executive ước lượng sai chênh lệch nhiều lần. "Nhìn rõ chênh lệch" = sai đề: nếu chênh nhỏ thì vẽ **delta vs trung bình/target** (My Calculations) baseline 0, hoặc Bar + **Reference Line** (Add Statistics) tại target. Bar luôn từ 0.

**6. Title = tên cột** (❌ §5): "Doanh thu by Nhóm SP" = mô tả cơ học, không nói người xem RÚT RA gì. FIX (Title EN insight/câu hỏi + Note VN; số sống trong viz vì title OAC tĩnh):
| Cũ | Mới |
|---|---|
| Doanh thu by Nhóm SP | Top Revenue Groups — Where Is Growth Coming From? |
| Doanh thu và Đơn hàng by Tháng | Monthly Revenue Trend — Are We Tracking to Plan? |
| Doanh thu by Vùng | Regional Revenue — Which Region Is Underperforming? |

## ĐỀ XUẤT BỐ CỤC LẠI (Z-pattern/BANs §5)
[4 KPI tile + sparkline] / [PRIMARY Combo actual-vs-plan 60% | Treemap nhóm SP] / [HBar delta vùng baseline-0] / [Table CF drill cuối]. Trellis 8 chuỗi → canvas Analytical riêng (không để lẫn executive).

**Tóm tắt:** lỗi nặng nhất = #5 (baseline ≠0) và #2 (tương quan giả) — misleading trực tiếp dẫn quyết định sai; #1/#4 = không đọc được; #3/#6 = mờ tín hiệu/mất insight.
