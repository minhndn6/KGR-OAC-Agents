# (BASELINE — không skill) Review 6 lỗi canvas executive

**1. Pie 12 nhóm (❌):** Cleveland & McGill (1984) — não đánh giá góc kém hơn chiều dài bar; từ lát thứ 4 không xếp hạng được; không so được với AOP. Fix: horizontal bar sort desc hoặc treemap.

**2. Dual-axis "tương quan" (❌ nghiêm trọng nhất):** kiểm soát scale 2 trục độc lập → giao nhau ở đâu tùy ý → correlation ảo; CEO kết luận nhân quả sai; Tufte "chartjunk correlation". Fix: tách 2 viz; muốn tương quan thật → scatter kèm r².

**3. 9 KPI tile (⚠):** Stephen Few tối đa 5-6 KPI executive; 9 tile mắt không biết nhìn đâu; cần cắt + nhóm lại.

**4. Stacked 8 lớp (❌):** chỉ đọc được lớp đáy + tổng; 8 lớp × 12 tháng = 96 đoạn màu "wall of color". Fix: gom còn 3-4 nhóm hoặc small multiples / line đa đường.

**5. Trục Y từ 300 tỷ (❌ misleading tài chính):** chênh 18% trông như 4×; dẫn phân bổ ngân sách sai. Fix: baseline 0 + delta label trên bar.

**6. Title = tên cột (❌):** data label không phải insight; Knaflic (Storytelling with Data) — title executive = câu khẳng định insight dẫn action. Vd: "3 nhóm SP đầu chiếm 68% doanh thu — nơi cần tập trung nguồn lực."

**Verdict: ❌ REWORK** — 4 lỗi misleading (1/2/4/5) sẽ dẫn quyết định sai nếu ship cho C-level.
