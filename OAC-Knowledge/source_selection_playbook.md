# SOURCE SELECTION PLAYBOOK — tư vấn "lấy/dựng data từ đâu" (cho dashboard-builder & dataflow-builder)

> Khi một agent hỏi *"tôi cần metric M theo chiều D ở grain G — có sẵn không? lấy đâu nhanh nhất? chưa có thì dựng từ nguồn nào?"* → theo quy trình này. Luôn tôn trọng precedence: **OAC > NSAW_Claude; báo cáo (BC) > dashboard (DB)**. Số luôn lấy LIVE (xem `live_query_recipes.md`).

## Quy trình 4 bước
1. **Có sẵn không?** Tra `capability_map.yaml` → `by_metric[M]` ∩ `by_dimension[D]`; kiểm `datasets.<ds>.grain` có ≤ G (re-aggregate được lên G không). Nếu có dataset thỏa → **dùng thẳng** (nhanh nhất, đã materialize).
2. **Chọn nguồn authoritative** nếu nhiều nơi có: báo cáo > dashboard; nguồn gần grain mong muốn nhất; tránh bản trùng-producer chưa xác nhận (xem CONFLICTS Q1).
3. **Chưa đủ?** Nếu metric/chiều có nhưng grain chưa đúng → re-aggregate (nếu nguồn mịn hơn) hoặc extend dataflow. Nếu chiều/metric CHƯA có → sang bước 4.
4. **Dựng mới** (gọi dataflow-builder): chỉ ra dataset/bảng khởi đầu + plan join (mục "Khởi từ đâu" dưới) + cạm bẫy.

## Khởi từ đâu để TÍNH X (bản đồ nguồn nhanh)
| Cần | Khởi từ | Vì sao |
|---|---|---|
| Doanh thu / Doanh số / Giá vốn / LN gộp / %GP / Xanh-Đỏ / CKKM / SP mới — ở BẤT KỲ grain (line→ngành/chuỗi/kênh/model/đơn vị/ngày/kỳ) | **`(KGR) DTF_CALC_INVOICE_MEMO_#`** (HUB, grain invoice/credit line) | Đã join sẵn HẦU HẾT segment/extension + tính sẵn DT/DSố/COGS 3-tier/CKKM/Xanh-Đỏ/SP mới. Re-aggregate lên grain nào cũng được — KHÔNG cần dựng lại. |
| P&L chỉ tiêu a1–a20 (LN gộp KD, LN trước/sau thuế…) theo kỳ/ngành | `TD_Metrics_Wide` (wide) / `TD_Report_Long` (long, dùng cho báo cáo) / `Nganh_Report_Long_#` (theo ngành) | Producer `KGR_DF_TD_Metrics_bk`/`KGR_DF_Nganh_Metrics_v3`. ⚠ cost a6–a18 là ƯỚC TÍNH theo AOP (xem dưới). |
| Waterfall P&L (bridge) | `TD_Report_PNL_Bridge` (tập đoàn) / `_Bridge_Nganh` (ngành) | Đã dựng dạng bridge từ Report_Long. |
| Lũy kế ngày vs AOP | `Daily_TD_Report` / `Daily_Nganh_Report` | Join Report_Long + AOP LINE CF + SP mới. |
| AOP (kế hoạch) | `(KGR) AOP Dataset` → `AOP LINE CF` (daily) / `DTF_GRAIN_ACTUAL_AOP` (grain hóa) | LOAI_BAO_CAO=1 doanh số, =2 %. |
| SFC ước tính vs thực tế | **`(KGR) DTF_CALC_MIS`** (báo cáo BC03 — authoritative) | DB01 dùng `KGR_DS_SFC_vs_MEMO_v1..v4` (mỗi bản 1 grain) — ưu tiên thấp hơn. |
| ASM / lịch sử nhiều năm / tỉnh-thành | `DW_X_SALE_HISTORY_Dataset` (hoặc `SALE HIST w INVC` union với invoice) | Hub không có ASM; lịch sử YoY nằm ở SALE_HISTORY. ⚠ SALE_HISTORY chỉ có **doanh thu+quantity**, KHÔNG có COGS/GP/CKKM → "lợi nhuận/biên theo ASM" = **phải BUILD** (join SALE_HISTORY × giá vốn từ hub/CALC_INVOICE_MEMO theo SKU), không có sẵn. |
| Chi phí THỰC (GL) | `(KGR) DTF_FACT_EXPENSE` / `JOURNAL` (ngoài closure) | ⚠ chưa nối vào P&L 4 workbook — xem CONFLICTS Q3. |

## ⚠️ Guardrail RE-AGGREGATE từ hub (đừng tư vấn sai)
Hub `(KGR) DTF_CALC_INVOICE_MEMO_#` ở grain line — re-aggregate lên grain thô hơn CHỈ đúng cho **measure cộng được** (Doanh thu, Doanh số, Giá vốn, LN gộp, QUANTITY, DS Xanh/Đỏ, CKKM tiền).
- ❌ **KHÔNG SUM trực tiếp các TỶ LỆ/RATIO** (%GP, %GP Ròng, %LN Gộp, %CKKM, tỷ trọng SP mới, tỷ lệ Xanh/Đỏ) → phải **tính lại từ tử/mẫu** sau khi aggregate (vd %GP = ΣLN gộp / ΣDoanh thu).
- ❌ **KHÔNG SUM cột đã max/đơn-giá** (GVMT/GVTK unit cost, AOP %) — chúng là per-item/per-kỳ.
- ❌ Chiều hub KHÔNG có: **ASM, tỉnh/thành** (ASM→`DW_X_SALE_HISTORY_Dataset`; tỉnh→`(KGR) DW_NS_CUSTOMER_D` geo). Đừng hứa "hub mọi chiều".
- P&L a1–a20 đã tính sẵn ở `TD_Metrics_Wide`/`Report_Long` — dùng bản đó, đừng tự dựng lại từ hub.

## Cạm bẫy & nguyên tắc "30 năm" (PHẢI biết khi tư vấn/dựng)
1. **Lợi nhuận dưới mức gộp là ƯỚC TÍNH, không phải chi phí thực.** a6/a7/a8/a15/a16/a17 = %AOP × Doanh thu; a10/a12/a18 = AOP_AMT × ngày/30; a21 thuế = ×0.21 cứng. → Khi build dashboard "lợi nhuận", ghi rõ "ước tính theo AOP". Muốn lợi nhuận theo chi phí THỰC → phải dựng mới từ FACT_EXPENSE/JOURNAL.
2. **Số cứng**: a10 (CP xúc tiến) = 247,258,890.47 nhúng trong dataflow; thuế 0.21. → cảnh báo stale; đừng coi là nguồn động.
3. **Revenue filters bắt buộc** (OAC): ISPOSTING='T', ACCTTYPE IN('Income','OthCurrLiab'), subsidiary trong whitelist 'Tên Đơn vị', loại 'Vụ việc'='HTL' (hàng trưng bày). OAC dùng `BASE_REVENUE` (KHÔNG phải BASE_CR−DB như NSAW_Claude).
4. **COGS fan-out**: GVMT/GVTK join theo item×kỳ×subsidiary có thể nhân dòng → hub đã xử lý bằng GroupBy max. Nếu tự join GVMT ở line, dùng scalar/max, đừng LEFT JOIN thô.
5. **Xanh/Đỏ**: theo CSEG_SCV_NHOMXANHDO với date-range hiệu lực; mặc định Đỏ nếu không match.
6. **Nội bộ**: loại khách/đơn vị nội bộ (SC=14) — trong OAC thực hiện qua subsidiary whitelist.
7. **Multi-producer chưa xác nhận**: `Nganh_Report_Long_#`, `Daily_Nganh_Report`, `KGR_DS_ACTUAL_AOP_MONTHLY_v2` có ≥2 dataflow cùng sinh — xác nhận bản live (CONFLICTS Q1) trước khi phụ thuộc/extend.
8. **Tên version KHÔNG cho biết bản đúng** — xét in_closure + producer thực tế.
9. **Join-key nội bộ db-dataset không lộ qua API** → nếu dựng thẳng từ bảng vật lý, dùng key chuẩn NetSuite (line→ACCOUNT/ITEM/POSTINGPERIOD; extension→ID; segment→CSEG_*; dim→ID).
10. **Số luôn LIVE** — không cache; trả số kèm thời điểm query.

## Reuse vs Build (khuyến nghị cho dataflow-builder)
- **Reuse trước**: nếu metric+chiều đã có trong hub/Report_Long → re-aggregate, KHÔNG dựng mới.
- **Extend**: cần thêm 1 chiều mà hub đã join sẵn bảng đó → thêm cột/extend dataflow hub thay vì flow mới.
- **Build mới**: chỉ khi cần grain mịn hơn nguồn hiện có, hoặc metric/chiều CHƯA tồn tại (vd chi phí thực theo P&L) → khởi từ bảng vật lý trong `physical_table_catalog.yaml` + plan join chuẩn NS + áp filter nghiệp vụ ở mục (3).
- Khi đề xuất build, luôn kèm: bảng nguồn, key join, filter bắt buộc, grain đích, và cảnh báo cạm bẫy liên quan.
