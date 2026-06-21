# 🎯 DASHBOARD DESIGN MASTERY — GOLDEN, tự chứa (Kangaroo / KGR)
> **File DUY NHẤT** cần đọc để TƯ VẤN & HOẠCH ĐỊNH dashboard như một Data Analyst expert: với dữ liệu hiện có thì NÊN show gì, cho AI xem, góc nhìn/chỉ số phái sinh nào đắt giá, loại biểu đồ nào đúng — kết hợp nhuần nhuyễn với năng lực thật của OAC.
> **Phân vai 3 file golden:** file này = TƯ VẤN/THIẾT KẾ (what/why/which) · `OAC_DASHBOARD_MASTERY.md` = THỰC THI trên OAC (how: click-path, commit/persist, verify) · `C:\Project\KGR-OAC-Agents\Dataflow-builder\OAC_DATAFLOW_MASTERY.md` = CHUẨN BỊ DỮ LIỆU (transform/join/pivot).
> Nguồn chưng cất: Anthropic skills (build-dashboard, data-visualization, create-viz) · Tableau Public most-favorited (Visual Vocabulary — Andy Kriebel, KPI Options — Adam McCann, Chart Catalog — Flerlage) · DataCamp dashboard examples · Stephen Few · thực chiến KGR. Cập nhật 2026-06-11.
> Quy ước icon: ⭐ đọc kỹ · ⚠️ bẫy · ✅ đã verify thực chiến · 📌 load-bearing.

---

## MỤC LỤC
0. Vai trò & ranh giới · 1. Phân loại dashboard (3 loại) · 2. ⭐ Framework tư vấn: AUDIENCE → QUYẾT ĐỊNH → CÂU HỎI → KPI · 3. ⭐ Playbook chỉ số phái sinh (góc nhìn đắt giá) · 4. ⭐⭐ Cây chọn chart → map 59 viz OAC · 5. Composition & layout canvas · 6. Quy trình tư vấn + BLUEPRINT bàn giao · 7. Checklist chất lượng thiết kế · 8. Changelog

---

## 0. VAI TRÒ & RANH GIỚI
- File này phục vụ vai **Data Analyst / Dashboard Designer**: nhận dữ liệu (hoặc mô tả dữ liệu) + bối cảnh người xem → đề xuất dashboard NÊN có gì. Đầu ra chuẩn = **BLUEPRINT** (§6) để người/agent thực thi build.
- KHÔNG chứa click-path OAC (xem OAC_DASHBOARD_MASTERY.md). KHÔNG chứa cách build dataflow (xem OAC_DATAFLOW_MASTERY.md).
- 📌 Nguyên tắc gốc (rút từ Tableau most-favorited): **tính hữu dụng kinh doanh thắng thẩm mỹ** — viz được yêu thích nhất toàn là business dashboard + công cụ chọn chart, không phải viz đẹp về pop culture. Mọi đề xuất phải trả lời được: *"viz này giúp người xem RA QUYẾT ĐỊNH gì?"*

---

## 1. PHÂN LOẠI DASHBOARD — chọn đúng loại trước khi chọn chart
| | **Executive / Strategic** | **Operational** | **Analytical** |
|---|---|---|---|
| Người xem | CEO/CFO/lãnh đạo | Trưởng nhóm vận hành, sales ops | Analyst, manager đào sâu |
| Nhịp xem | Tuần/tháng, 5 giây ra ý chính | Hằng ngày/realtime | Khi cần điều tra |
| Câu hỏi | "Có đạt mục tiêu? Xu hướng? Rủi ro lớn?" | "Hôm nay có gì lệch chuẩn cần can thiệp?" | "VÌ SAO số này lệch? Pattern nào?" |
| Đặc trưng | Ít KPI (3-6), BANs to, vs plan/kỳ trước, RẤT ít filter | Ngưỡng cảnh báo, status màu, danh sách việc, latest-period | Nhiều filter/drill, grain mịn, scatter/heatmap/phân phối |
| Mật độ | 3-5 viz/canvas | 4-7 viz, bảng ưu tiên | Tự do hơn, nhưng mỗi canvas 1 chủ đề |
| Hành động | Quyết định phân bổ/chiến lược | Can thiệp ngay trong ngày | Tìm root cause → đề xuất |
- ⚠️ Lỗi phổ biến nhất: trộn 3 loại vào 1 canvas → ai xem cũng thấy thừa/thiếu. Hỏi rõ audience TRƯỚC (§2), chốt loại, rồi mới thiết kế.
- Tab/canvas order: **overview → detail** (executive canvas đầu, analytical canvas sau, drill từ trên xuống).

---

## 2. ⭐ FRAMEWORK TƯ VẤN: AUDIENCE → QUYẾT ĐỊNH → CÂU HỎI → KPI → VIZ
> Đi đủ 5 bước, KHÔNG nhảy thẳng từ "có dữ liệu" sang "vẽ chart". Dashboard tồn tại để phục vụ quyết định, không phải để "xem cho biết".

1. **AUDIENCE** — Ai xem? Vai trò gì? Nhịp xem? Trình độ đọc số? Xem trên màn hình gì (desktop/trình chiếu/mobile)? → chốt LOẠI dashboard (§1).
2. **QUYẾT ĐỊNH** — Người đó phải ra quyết định gì định kỳ? (phân bổ ngân sách, can thiệp kênh yếu, duyệt khuyến mãi, điều chỉnh forecast, nhân sự…). Mỗi quyết định = 1 cụm thông tin cần.
3. **CÂU HỎI ĐIỀU HÀNH** — Để quyết định đó cần trả lời câu hỏi nào? 📌 **Mỗi canvas = đúng 1 câu hỏi** ("Chúng ta có đạt kế hoạch không, lệch ở đâu?", "Biên lợi nhuận bị bào mòn bởi gì?", "Doanh thu phụ thuộc bao nhiêu vào nhóm khách lớn?").
4. **KPI/METRIC** — Chỉ số nào trả lời câu hỏi? Mỗi metric phải chốt: **định nghĩa/công thức · grain · kỳ · nguồn · số expected để verify**. Ưu tiên cặp lagging (kết quả) + leading (cảnh báo sớm). Cân nhắc chỉ số PHÁI SINH (§3) — thường đắt giá hơn chỉ số thô.
5. **VIZ** — chọn theo quan hệ dữ liệu (§4), bố trí theo §5.

**Câu hỏi khám phá chuẩn khi yêu cầu mơ hồ** (gom hỏi 1 lần, kèm phương án đề xuất): mục đích (executive overview / monitoring / deep-dive)? · ai xem + nhịp? · 3 con số quan trọng nhất với họ? · cần cắt theo chiều nào (filter/slice)? · nguồn dữ liệu + nhịp cập nhật? · có kế hoạch/chuẩn để so không (plan/AOP/target/kỳ trước)?
- ⚠️ **Profile dữ liệu THẬT trước khi hứa** (qua NSAW/executePreview/metadata — đừng đoán): grain có hỗ trợ chiều muốn cắt không (✅ bài học KGR: actual không có grain Kênh → plan-vs-actual theo Kênh bất khả); kỳ nào có data đủ; cột nào null nhiều; dimension nào bẩn (trùng ID, chưa gắn nhóm) → caveat hoặc đề xuất làm sạch.

---

## 3. ⭐ PLAYBOOK CHỈ SỐ PHÁI SINH — góc nhìn đắt giá từ dữ liệu sẵn có
> Giá trị tư vấn lớn nhất: chỉ ra chiều thông tin chủ dữ liệu CHƯA NGHĨ ĐẾN. Mỗi chỉ số dưới đây gắn 1 quyết định. **Route hiện thực hoá:** nhẹ (ratio/hiệu/%) = **My Calculations** trong workbook; nặng (pivot kỳ, join nhiều nguồn, pre-aggregate, cột mới materialized) = **dataflow** (OAC_DATAFLOW_MASTERY.md).

| Nhóm | Chỉ số | Cách tính | Quyết định phục vụ | Route |
|---|---|---|---|---|
| **So với chuẩn** | Achievement % · Variance vs plan (tuyệt đối + %) · Run-rate forecast EOM vs target · YTD vs full-year | actual/plan · actual−plan · (actual/ngày đã qua)×ngày tháng | Có cần can thiệp để đạt mục tiêu? | Calc (plan+actual đã cùng grain) / dataflow nếu phải join plan |
| **Tăng trưởng** | YoY/MoM % · Contribution-to-growth (nhóm nào đóng góp bao nhiêu điểm % tăng trưởng tổng) | (kỳ này−kỳ trước)/kỳ trước · Δnhóm/tổng kỳ trước | Đà tăng thật hay nhờ 1 nhóm? | Dataflow (pivot kỳ→cột) rồi calc |
| **Cơ cấu & dịch chuyển** | Mix % · **Mix shift** (điểm % thay đổi tỷ trọng giữa 2 kỳ) | nhóm/tổng · mix kỳ này − mix kỳ trước | Cơ cấu đang dịch về đâu — chủ động hay bị động? | Calc / dataflow |
| **Tập trung & rủi ro** | Top-N concentration % · Pareto 80/20 (bao nhiêu % khách/SKU tạo 80% doanh thu) | Σtop-N/tổng · đường lũy kế | Phụ thuộc khách/chuỗi/SKU lớn tới đâu? | Viz (Top-N filter + bảng Pareto) / dataflow rank |
| **Hiệu quả & biên** | GP% · Net margin % · **Bridge bào mòn** (Gross → −khuyến mãi/chiết khấu → Net) · Chi phí khuyến mãi/doanh thu | từng tầng /doanh thu thuần | Đòn bẩy lợi nhuận nằm ở đâu? Khuyến mãi ăn bao nhiêu lãi? | Calc + Waterfall |
| **Per-unit** | Giá bán bình quân · Doanh thu/khách · Doanh thu/đơn · SL/điểm bán | doanh thu/số lượng·khách·đơn | Tăng nhờ giá hay nhờ lượng? | Calc |
| **Chất lượng tăng trưởng** | % doanh thu SP mới · % khách quay lại · Tần suất mua | DT SP mới/DT tổng (revenue-weighted) | Tăng trưởng có bền không? | Calc / dataflow cohort |
| **Data quality flag** | % bản ghi thiếu dimension (vd chưa gắn chuỗi/nhóm) · Số ID trùng | count thiếu/tổng | Tin được lát cắt này tới đâu? (show như caveat/KPI phụ) | Calc |
- ⚠️ **Ratio luôn kèm cảnh giác mẫu số**: mẫu nhỏ/0 → ratio "vỡ" (297%, 0 chia) → cap thang màu, lọc dòng mẫu-rỗng, hoặc ẩn nhóm quá nhỏ.
- ⚠️ **Chốt ĐỊNH NGHĨA với chủ dữ liệu trước khi build** (vd "% SP mới" theo doanh thu hay theo số SKU? doanh thu gross hay net? — các định nghĩa khác nhau cho số khác hẳn nhau). Ghi định nghĩa đã chốt vào Blueprint.
- 💡 Mẫu câu tư vấn: "Dữ liệu anh/chị có [X theo grain Y] — ngoài việc xem X thô, ta có thể trả lời thêm: [3-5 chỉ số phái sinh + quyết định nó phục vụ]. Tôi đề xuất ưu tiên [2 cái] vì gắn trực tiếp watch-item hiện tại."

---

## 4. ⭐⭐ CÂY QUYẾT ĐỊNH CHỌN CHART → MAP 59 VIZ OAC
> Chuẩn quốc tế (Visual Vocabulary) + năng lực THẬT của OAC. Cột "OAC" = viz có thật trong picker; shelf/bẫy thao tác chi tiết xem OAC_DASHBOARD_MASTERY.md §5-§7.

| Quan hệ dữ liệu cần thể hiện | Chart chuẩn | **Viz OAC** + lưu ý OAC |
|---|---|---|
| Xu hướng theo thời gian | Line | **Line** (Category=cột thời gian). Line được phép baseline ≠0 khi dao động là trọng tâm |
| Xu hướng + cơ cấu theo thời gian | Stacked Area / 100% Area | **Stacked Area** · **100% Area** (focus tỷ trọng) |
| So sánh giữa các nhóm | Bar | **Bar**; nhóm nhiều/tên dài → **Horizontal Bar**. ⚠️ baseline 0 BẮT BUỘC; sort theo giá trị (không alphabet) |
| Xếp hạng (top/bottom) | Horizontal bar + top-N | **Horizontal Bar** + filter **Top Bottom N** (viz-level) |
| **Plan vs Actual** ⭐ | Combo bar+line | **Combo**: actual=Bar (xanh #44BA46), plan=Line (xám #636466), 1 viz 2 measure — KHÔNG tách 2 chart. Y2 Axis nếu lệch thang. **Butterfly** nếu so 2 phía đối xứng |
| Vs target 1 KPI đơn | Bullet/Gauge | **Gauge** (Values/Target/Start/End) · **Liquid Fill Plugin** (% đạt nổi bật) · OAC không có bullet chuẩn → Bar + Reference Line (Add Statistics) |
| Cơ cấu phần-tổng (1 thời điểm) | Stacked bar / Treemap | **Stacked Bar**; 2 chiều size+màu (vd size=DT, màu=GP%) → **Treemap**. ⚠️ **Pie/Donut chỉ khi <6 nhóm** và so thô — người đọc kém so góc; Donut tối đa cho 1 KPI |
| Cơ cấu phân cấp | Treemap/Sunburst | **Treemap** (2 cấp) · **Sunburst** (nhiều cấp) |
| Phân phối giá trị | Histogram / Boxplot | OAC KHÔNG có histogram trực tiếp → route: **Bin** (dataflow) + Bar, hoặc **Boxplot**/Horizontal Boxplot (so nhóm) |
| Tương quan 2 biến (+2 chiều phụ) | Scatter/Bubble | **Scatter** 4 lớp: X · Y · Size · Color (vd X=%Xanh, Y=%GP, size=DT, màu=Ngành) |
| Ma trận mật độ 2 chiều | Heatmap | **Grid Heat Map** (Category Y × Category X × Color). ⚠️ thang màu 1 hướng; cap khi ratio vỡ |
| Tương quan nhiều biến | Correlation matrix | **Correlation Matrix** |
| Bóc tách gap / cầu nối | Waterfall | **Waterfall** (bridge AOP→Actual, Gross→−CKKM→Net). ⚠️ bước giảm = giá trị ÂM; tổng phải balance — lệch thì thêm cột "Khác/Điều chỉnh", KHÔNG giấu |
| Luồng phân bổ qua nhiều tầng | Sankey | **Sankey** (Category = nhiều dim làm stage) · **Chord** (quan hệ vòng) |
| Phễu chuyển đổi | Funnel | **Funnel Plugin** |
| KPI headline | BAN/KPI card | **Tile** (+sparkline qua Category Chart) · **KPI Tile Plugin** (Base/Target/Previous — có sẵn so-với-target) |
| Nhiều nhóm cùng 1 khung so sánh | Small multiples | ⭐ OAC làm small-multiples bằng shelf **Trellis Columns/Rows** (không phải viz riêng) — thay cho stacked nhiều lớp khó đọc |
| Địa lý | Choropleth/bubble map | **Map** (Category=Location) |
| Định vị danh mục 2 chiều | 9-box | **NineboxViz Plugin** (tăng trưởng × biên) |
| Bảng tra chi tiết | Table | **Table**/**Pivot** + Conditional Formatting (thang màu ratio) — đặt CUỐI canvas làm drill-down |
| Chú giải tự động bằng lời | Narrative | **Language Narrative** |
| Nhiều chỉ số chuẩn hoá so le | Radar | **Radar Line/Area/Bar** — dùng tiết chế (khó đọc với người lạ) |

**⚠️ KHI NÀO KHÔNG (anti-patterns):**
- **Pie/Donut >6 nhóm** → Bar/Treemap. **3D** → không bao giờ (OAC không có — tốt). 
- **Dual-axis (Y2)**: chỉ khi 2 measure thật sự liên quan và nhãn 2 trục rõ — dễ ám thị tương quan giả.
- **Stacked bar nhiều lớp**: lớp giữa không so được → Trellis hoặc grouped bar.
- **Chart kiểu lạ (Radar/Chord/Parallel/Picto/Network)** với audience executive: chỉ dùng khi đã thử chart cơ bản mà không truyền tải được — mới lạ ≠ rõ hơn.
- ⚠️ **Khả thi theo GRAIN trước khi hứa chart**: chiều X/Color/Trellis phải tồn tại trong grain dataset (profile thật §2). Không có grain → đề xuất route dataflow hoặc đổi chiều.

---

## 5. COMPOSITION & LAYOUT CANVAS
**Khung đọc Z-pattern + BANs** (trái-trên → phải, chéo xuống):
```
┌──────────────────────────────────────────────┐
│ Tiêu đề canvas (= câu hỏi điều hành) [Filter]│
├─────────┬─────────┬─────────┬────────────────┤
│ KPI/BAN │ KPI/BAN │ KPI/BAN │ KPI/BAN (3-5)  │ ← số tổng to, vs plan/kỳ trước
├─────────┴─────────┴┬────────┴────────────────┤
│  PRIMARY chart     │  Secondary chart        │ ← trả lời trực tiếp câu hỏi canvas
│  (to nhất, trái)   │  (góc nhìn bổ trợ)      │
├────────────────────┴─────────────────────────┤
│  Bảng chi tiết / drill (cuối, cuộn được)     │
└──────────────────────────────────────────────┘
```
- 📌 **≤6 KPI có nghĩa/canvas** (Stephen Few — quá tải nhận thức) · executive canvas 3-5 viz · **đa dạng loại viz** trong 1 canvas (1 combo + 1 treemap/heatmap + 1 KPI + 1 bảng — đừng 5 bar giống nhau).
- **Filter**: bộ lọc global nhất quán vị trí (đầu canvas); kỳ mặc định = kỳ HOÀN CHỈNH gần nhất; canvas all-history phải gắn nhãn kỳ rõ ("All-Time…") để không lẫn với canvas 1-kỳ. Executive ít filter; analytical nhiều filter + drill (Use as Filter).
- **Màu = ngữ nghĩa cố định, không trang trí**: KGR — xanh `#44BA46`=actual/tốt/margin · cam `#F16522`=chi phí/cảnh báo/gap · xám `#636466`=plan/trung tính (chi tiết thao tác + palette đầy đủ: OAC mastery §8). 1 màu NHẤN cho insight chính, xám hoá phần ngữ cảnh. Colorblind-safe: không dùng đỏ/xanh-lá làm tín hiệu DUY NHẤT — kèm nhãn/vị trí/icon.
- **Title nói INSIGHT hoặc CÂU HỎI, không nói tên cột** ("Promotion Is Eating 1/3 of Gross Margin" > "CKKM by Month"). ⚠️ Ràng buộc OAC: title TĨNH không nhúng số động → title nêu thông điệp/đối tượng + kỳ; SỐ sống trong viz/KPI tile; diễn giải chi tiết → Note tiếng Việt (quy ước Title EN/Note VN — OAC mastery §15).
- **Trung thực thống kê**: bar baseline 0 · thang nhất quán giữa các panel so sánh · không cherry-pick khung thời gian · ratio kèm bối cảnh mẫu số · grain so sánh phải cùng nghĩa (vd tổng công ty ≠ Σ ngành nếu kế hoạch lập khác tầng — nêu rõ thay vì ép khớp) · annotation/note cho điểm bất thường.
- **Mỗi viz 1 note VN** giải thích: thấy gì → hàm ý → điểm đắt giá → liên kết viz lân cận (2-4 câu).
- Trình chiếu/họp → kiểm tra Present mode; mobile → bố cục dọc, chữ to.

---

## 6. QUY TRÌNH TƯ VẤN + BLUEPRINT (artifact bàn giao)
**5 bước:** (1) **DISCOVER** — profile dữ liệu thật (grain/dims/measures/kỳ/chất lượng; NSAW MCP hoặc OAC REST; chưa kết nối được → hỏi schema + xin mẫu). (2) **AUDIENCE & DECISIONS** (§2 — hỏi gọn 1 lần nếu thiếu). (3) **DESIGN** — câu hỏi/canvas → metric (kể cả phái sinh §3 + route) → chart (§4) → layout (§5). (4) **BLUEPRINT + GATE** — trình bản thiết kế, CHỜ DUYỆT; sau duyệt bàn giao: cần dataset mới → oac-dataflow-builder; build viz → oac-dashboard-builder. (5) **LEARN** — bài học mới (pattern tư vấn, phản hồi user, anti-pattern mới) ghi vào file này đúng section + changelog.

**BLUEPRINT** (template đầy đủ: `references/blueprint-template.md` của skill oac-dashboard-designer) — lõi gồm:
1. Bối cảnh: audience, loại dashboard, nhịp xem, quyết định phục vụ.
2. Bảng canvas: mỗi canvas = câu hỏi điều hành + danh sách viz (loại OAC + shelf mapping + filter + màu + format + note VN).
3. Bảng metric: định nghĩa đã chốt + grain + nguồn + **số expected để verify** + route (sẵn có / My Calculations / dataflow).
4. Chỉ số phái sinh ĐỀ XUẤT THÊM (chưa được yêu cầu) + quyết định nó phục vụ — phần "tư vấn đắt giá".
5. Data quality caveats + open questions cho chủ dữ liệu.
6. Thứ tự build ưu tiên + Definition of Done.

---

## 7. CHECKLIST CHẤT LƯỢNG THIẾT KẾ (tự kiểm trước khi trình Blueprint)
- [ ] Mỗi canvas đúng 1 câu hỏi điều hành; mỗi viz trả lời được "giúp ra quyết định gì?" — viz không qua được = cắt (chart-junk).
- [ ] Đúng LOẠI dashboard cho audience (§1); bố cục Z-pattern/BANs; ≤6 KPI/canvas; đa dạng loại viz.
- [ ] Chart đúng quan hệ dữ liệu (§4) + KHẢ THI theo grain đã profile; không dính anti-pattern.
- [ ] Metric định nghĩa chốt + số expected + nguồn verify độc lập; ratio an toàn mẫu số.
- [ ] Có ≥1 chỉ số phái sinh đắt giá được đề xuất chủ động (§3) kèm route hiện thực.
- [ ] Trung thực thống kê (§5); màu đúng ngữ nghĩa; Title EN nói insight, Note VN.
- [ ] Data quality caveats nêu rõ; open questions gom 1 lần.
- [ ] Blueprint đủ để builder thi công KHÔNG cần hỏi lại.

---

## 8. CHANGELOG
- 2026-06-11: Tạo file golden từ chưng cất 3 Anthropic skills (build-dashboard/data-visualization/create-viz — lấy tầng tư duy chọn chart + design principles, bỏ tầng code Chart.js/Python) + Tableau Public most-favorited (Visual Vocabulary/KPI Options/Chart Catalog; bài học "hữu dụng thắng thẩm mỹ") + DataCamp dashboard examples (Z-pattern, BANs, 3 loại dashboard, giảm tải nhận thức) + chuẩn Few + bài học thực chiến KGR (grain-trước-chart, ratio vỡ, plan-vs-actual 1 combo). Map cây chọn chart sang 59 viz OAC thật (Trellis = small multiples; Bin+Bar = histogram; Gauge/LiquidFill = vs-target).
