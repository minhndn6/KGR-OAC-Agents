# (BASELINE — không skill) Tư vấn CEO/CFO Monday Morning Dashboard — Kangaroo

Nguyên tắc: 10 phút = 3 câu hỏi (tuần rồi tốt/xấu vs plan? cái gì đang hỏng? tháng/năm về đích không?). Mọi thứ phải trả lời 1 trong 3.

**5 canvas:** Overview (6 KPI cards + trend 8 tuần + smart alerts + 2 bảng breakdown) · Ngành hàng (bar ngang actual vs plan sort theo hụt, scatter growth×GP% size=SL, bảng hàng tặng, trend GP% ròng 13 tuần) · Kênh/Chuỗi (heatmap ngành×chuỗi %vs plan, bảng chuỗi + cảnh báo hụt 3 tuần liên tiếp) · GP & Hàng tặng (waterfall GP gross→CK→tặng→ròng, bar % tặng vs ngưỡng, scatter tặng×GP%) · Plan vs Actual (variance waterfall 13 tuần, EOM forecast range, 3 gauge attainment, bảng top contributor).

**KPI cards (6):** DT W-1 vs plan · SL W-1 (trừ tặng) · GP% · GP% ròng · DT MTD %KH tháng · DT YTD %AOP. Màu: xanh vượt/vàng ±5%/đỏ hụt >5%.

**Trend 8 tuần:** cột DT thực (xanh dương Kangaroo) + đường đứt plan; tuần mới nhất highlight.

**Smart Alerts:** tối đa 5, đỏ (GP%<19% hoặc hụt >15% 2 tuần liên tiếp) → vàng → xanh.

**Quy tắc kỹ thuật:** tách "sản lượng thương mại" (trừ tặng) vs tổng xuất kho; kỳ mặc định W-1, hỗ trợ MTD/QTD/YTD; dữ liệu sẵn sàng trước 7AM thứ Hai, thiếu thì hiện "dữ liệu tới W-2" thay vì số 0; làm tròn tỷ 1 số lẻ.

**KHÔNG đưa vào:** chi tiết hóa đơn/SKU; YoY trên Overview; pie chart; >3 màu; filter phức tạp trên Overview.

**Phương án triển khai:** A=Oracle Analytics Cloud (nếu dùng Oracle ERP/DW) · B=Power BI Premium · C=Looker Studio. 

Chờ phê duyệt. Cần xác nhận: tool BI đang dùng, nguồn dữ liệu, ngưỡng cảnh báo GP%/hàng tặng.
