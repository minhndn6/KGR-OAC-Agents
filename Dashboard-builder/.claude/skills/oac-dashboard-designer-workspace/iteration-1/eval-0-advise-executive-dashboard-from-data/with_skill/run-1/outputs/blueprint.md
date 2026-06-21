# BLUEPRINT: Weekly Revenue & Margin Pulse — CEO/CFO Monday Dashboard

## 1. Bối cảnh
- **Audience:** CEO + CFO · **Loại:** Executive / Strategic · **Nhịp xem:** Mỗi sáng thứ Hai, ~10 phút · **Màn hình:** Desktop (possibly present mode)
- **Quyết định phục vụ (4):** (1) Đúng track kế hoạch không — can thiệp kênh/ngành nào? (2) Biên GP bị bào mòn không, ở chuỗi/ngành nào? (3) Hàng tặng ăn vào doanh thu thực bao nhiêu? (4) Kênh/chuỗi nào kéo tổng lên/xuống — phân bổ nguồn lực tuần tới?

## 2. Dữ liệu (theo mô tả — checks cần chạy)
| Nguồn | Grain | Dims | Measures | Chất lượng (checks) |
|---|---|---|---|---|
| HĐ bán hàng theo dòng | 1 dòng = 1 line item | Ngành, Nhóm SP, Chuỗi, Kỳ, Cờ tặng | SL, DT, GP%, %GP ròng | ⚠️ % dòng thiếu Chuỗi/Ngành · duplicate ID · cờ tặng binary? · Kỳ là date hay string |
| Kế hoạch SL + DT | 1 dòng = tuần × Ngành × Kênh × Chuỗi | Ngành, Kênh, Chuỗi, Tuần | SL KH, DT KH | ⚠️ **grain Kênh có trong actual không** (nếu không → plan-vs-actual theo Kênh BẤT KHẢ — cần dataflow mapping Chuỗi→Kênh hoặc bỏ chiều Kênh); plan có GP% không |

## 3. Thiết kế 4 canvas (mỗi canvas 1 câu hỏi)

### Canvas 1: "Tuần này có đang đi đúng kế hoạch không?"
- 4 BAN (KPI Tile Plugin Base/Target/Previous): Revenue vs Weekly Plan · Volume vs Weekly Plan · Weekly Achievement % · YTD Achievement % — xanh #44BA46 đạt / cam #F16522 dưới plan.
- **Combo Bar+Line** "Actual vs Plan — Last 8 Weeks": Bar=DT actual (xanh), Line=DT plan (xám #636466), Category=Tuần.
- **Horizontal Bar** "Revenue Gap by Industry — This Week": Variance (actual−plan), âm=cam dương=xanh, sort theo gap.
- Bố cục: [4 BAN] / [Combo 60% | Gap bar 40%].

### Canvas 2: "Biên lợi nhuận đang khỏe không — bào mòn ở đâu?"
- 2 BAN: Gross Margin % · Net Margin % (khoảng cách = deduction spread).
- **Waterfall** "What Is Eating Into Gross Margin?": GP% → −CKKM% → −CK% → Net GP% (xanh GP, cam khấu trừ).
- **Grid Heat Map** "Margin Map: Industry × Chain": Y=Ngành, X=Chuỗi, Color=GP% (thang 1 hướng, cap ±3σ).
- **Horizontal Bar + Top-Bottom N** "Net Margin — Top & Bottom Product Groups".

### Canvas 3: "Hàng tặng chiếm bao nhiêu, ăn vào kết quả thực?"
- BAN: Gift Revenue Share (cam nếu >ngưỡng ~10%) · Net Commercial Revenue.
- **100% Stacked Bar** "Gift vs Commercial Mix Trend — 8 Weeks".
- **Treemap** "Where Are Gift Products Concentrated?": size=DT tặng, color=% tặng/DT ngành.
- **Pivot** "Margin: Gift vs Commercial by Industry" + CF đỏ nếu GP% tặng < 0.

### Canvas 4: "Kênh/chuỗi nào kéo tổng — phân bổ nguồn lực thế nào?"
- **Combo** "Chain Performance: Revenue & Achievement": Bar=DT (Y1), Line=Achievement% (Y2) + ref line 100%.
- **Stacked Bar** "Revenue Composition by Chain" (màu theo Ngành — rủi ro tập trung).
- **Scatter** "Chain Quadrant: Achievement vs Margin": X=Achievement%, Y=GP%, Size=DT, 4 quadrant.
- **Table** "Chain Detail Drill — Top 15" + CF.

## 4. Metric & định nghĩa (chốt trước build) — trích
| Metric | Công thức | Số expected | Route |
|---|---|---|---|
| DT Actual tuần | Σ DT theo tuần (chốt gồm/loại tặng) | khớp báo cáo tuần thủ công | calc |
| Achievement % | DT actual/DT plan | tính tay 1 ngành mẫu | calc |
| GP% tuần | Σ(DT×GP%)/ΣDT weighted | khớp báo cáo lãi gộp | calc |
| % DT hàng tặng | Σ DT[cờ=1]/Σ DT | = DT tổng − DT thuần | calc |

## 5. ⭐ Chỉ số phái sinh ĐỀ XUẤT THÊM (6)
| Chỉ số | Vì sao đắt giá | Route |
|---|---|---|
| Run-rate EOM Forecast vs Plan | biết tháng đóng ở bao nhiêu % plan NGAY trong tuần, không đợi cuối tháng | calc |
| Contribution-to-Growth theo Ngành | tổng tăng 10% do đâu — ngành lớn che ngành nhỏ tăng nhanh | dataflow + Waterfall |
| ASP (giá bán bình quân) | DT tăng nhờ giá hay nhờ lượng | calc |
| % DT Top-3 Chuỗi | rủi ro tập trung | calc + Top-N |
| GP% Mix shift kỳ này vs trước | GP% tăng vì mix dịch hay thật sự cải thiện giá | dataflow + Waterfall |
| Gift Unit Share | tặng hàng giá trị thấp hay cao giá (ăn GP nặng) | calc |

## 6. Caveats & open questions (6 câu, gom 1 lần)
Grain mismatch actual/plan (Kênh!) · Kỳ date vs string · DT gross vs net · plan có GP%? · ngưỡng cảnh báo GP% · workbook mới hay DB01?

## 7. Thứ tự build + DoD
Chốt 6 câu hỏi → Dataflow A (join actual+plan, Achievement/Variance) → Dataflow B (map Chuỗi→Kênh nếu cần) → Canvas 1 → 4 → 2 → 3 → filter/màu/title/note. DoD: số khớp expected, Waterfall balance, title EN insight + note VN, màu ngữ nghĩa, persist verified.

Duyệt blueprint này chứ? Có gì cần đổi?
