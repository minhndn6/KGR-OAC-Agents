# Chẩn đoán & Kế hoạch dataflow thay thế — KGR_DS_SFC_vs_Actual_v2 (Canvas 14 "SFC Plan vs Actual")

> **Trạng thái:** Bản chẩn đoán + kế hoạch trình duyệt. Môi trường phiên này KHÔNG có browser nên không thao tác OAC thật — mọi kết luận dựa trên bằng chứng đã verify live các phiên trước (2026-06-07 → 2026-06-09); phần cần xác nhận lại được liệt kê thành **checklist sẽ chạy** ở §6.
>
> Workbook: `(KGR) DB01.Revenue_v1.1` · Canvas 14 · Dataset lỗi: `KGR_DS_SFC_vs_Actual_v2` (từ dataflow `KGR_DF_SFC_vs_Actual_v2`) · Kỳ chuẩn đối chiếu: **May 2026 = POSTINGPERIOD 42**

---

## 1. Triệu chứng (đã verify live)

| Chỉ số trên Canvas 14 | Đang hiển thị | Số đúng (golden) | Sai lệch |
|---|---|---|---|
| Actual Qty (SUM "Actual Qty") | **2,444,247 (~2.44M)** | **713,262** (MEMO#, May 2026) | **×3.4 quá cao** (×4.17 nếu so chuẩn SFC-scope 586K) |
| Plan Qty | **~40K** (agg = Maximum) | **445,043** | **~9%** số đúng |
| Achievement % | 61.11% | ~160% (713K/445K) | sai hoàn toàn, mâu thuẫn Canvas 24 |

Số golden đã được xác nhận 2 nguồn độc lập: NSAW `get_sfc_report` period 42 (forecast_qty = 445,043 EXACT) và dataset `KGR_DS_SFC_vs_MEMO_v2` (đã build + verify EXACT 2026-06-07): plan Water 313,894 / Home 124,655 / Cold & Hygen 6,494; actual Water 498,204 / Home 199,062 / Cold 11,741 / Khác 3,759 / Sanitary 496.

---

## 2. Chẩn đoán nguyên nhân gốc

`KGR_DS_SFC_vs_Actual_v2` hỏng vì **3 lỗi cấu trúc chồng nhau** trong dataflow nguồn — không lỗi nào sửa được ở tầng chart:

### 2.1 Fan-out do JOIN ở grain dòng (actual ×3.4–4.17, KHÔNG đồng đều)
- Dataflow join **plan (DW_SFC) ↔ actual (DTF_CALC_INVOICE_MEMO_#) ở mức item/dòng** (`ID` = `ITEM` + `POSTINGPERIOD`) **trước khi** aggregate. Cột `POSTINGPERIOD_1` tồn tại trong dataset là bằng chứng trực tiếp của join 2 phía.
- DW_SFC có **nhiều dòng trùng cho mỗi (model, period)** (broadcast ~4 bản trong kỳ + nhiều kỳ forward) → mỗi dòng actual bị nhân bản theo số dòng plan khớp key.
- Fan-out **không đồng đều** (ngành ~2.6x, tổng ~4x) → không chia hệ số phẳng, không aggregation nào trên chart (SUM quá cao, MAX quá thấp) cho ra số đúng. **Không tồn tại fix tại viz.**

### 2.2 Nhiễm đa kỳ (multi-period contamination)
- Dataset hiện chứa **horizon dự báo ~20 kỳ (POSTINGPERIOD ~41→61)** + bucket (No Value), không phải 1 kỳ.
- Canvas 14 đang filter **POSTINGPERIOD ≥ 42** (vì range `[42,42]` trả "No Data Found" — quirk float/zero-width của OAC) → gom luôn các kỳ forward 43–61. SUM plan toàn dataset: riêng Water đã ~1.55M.
- Chart-side khắc phục bằng Maximum thì chỉ trả về **1 giá trị item lớn nhất ≈ 40K** → chính là con số plan 40K đang thấy.

### 2.3 Plan thiếu dòng cấu trúc (inner-join drop) — chặn cả phương án "dedup rồi dùng tiếp"
- Đã thử nghiệm thật (dataflow `KGR_DF_SFC_vs_MEMO_v1`): dedup chuẩn MAX-per-(Ngành, Nhóm SP, Model) → SUM chỉ ra **198,024 = 44% golden 445,043**.
- Nguyên nhân: join của DS_v2 hành xử như **inner join** — SKU **có kế hoạch nhưng chưa bán** bị rớt khỏi dataset, mất luôn plan qty. Đã test cả 2 cột kỳ (`POSTINGPERIOD` vs `POSTINGPERIOD_1`) — kết quả như nhau → không filter/agg nào trên DS_v2 chạm được 445K.

**Kết luận:** DS_v2 sai từ thiết kế dataflow (join trước aggregate + nguồn plan bị lọc theo hóa đơn). Phải **thay dataflow**, không vá chart.

---

## 3. Nguyên tắc thiết kế thay thế (rút từ thực nghiệm đã verify)

1. **Aggregate TRƯỚC, join SAU** — hai nhánh tự gom về cùng grain hiển thị (Ngành [+ Nhóm SP]) rồi mới join → fan-out bất khả thi về mặt toán học.
2. **Plan lấy từ master kế hoạch `(KGR) DW_SFC`**, không lấy từ blend đã dính hóa đơn → SKU planned-but-unsold được giữ. Lưu ý: DW_SFC **không có cột qty tháng** — plan qty = `SL W1 + SL W2 + SL W3 + SL W4 + SL W5` (bảng `DW_NS_X_SFC_LINES_CF`); doanh thu plan = `Doanh thu (-VAT)`.
3. **Lọc 1 kỳ duy nhất ngay đầu nhánh** (`PERIODNAME = 'May 2026'`): đã chứng minh single-period filter **tự triệt tiêu fan-out 4x** của DW_SFC — SUM(SL W1..W5) theo Ngành = golden CHÍNH XÁC, không cần MAX-then-SUM.
4. **Actual lấy từ `(KGR) DTF_CALC_INVOICE_MEMO_#`**: `SL_Thuc_Te = −SUM(QUANTITY)` (QUANTITY âm; công thức này đã tự net credit memo CustCred). KHÔNG dùng `(KGR) DTF_CALC_SFC Thực tế` cho May — kỳ May chỉ load ~1/3 (Water 155K vs 459K), chưa refresh.
5. **FULL OUTER JOIN** trên khóa grain → giữ cả ngành chỉ-có-plan lẫn chỉ-có-actual (Khác, Sanitary không có plan SFC).

**Mẫu đã chạy đúng:** chính là `KGR_DF_SFC_vs_MEMO_v2` — build qua REST API, RUN, verify **EXACT** plan 445,043 / actual 713,262 (2026-06-07). Canvas 24 đang dùng dataset này và đang đúng (445,043 / 713,262 / ~160%).

---

## 4. Kế hoạch đề xuất (trình anh/chị duyệt)

### Phương án A — KHUYẾN NGHỊ: tái sử dụng `KGR_DS_SFC_vs_MEMO_v2`, sửa Canvas 14, khai tử DS_v2 trên dashboard
Không build dataflow mới khi đã có dataset verify EXACT cùng đúng mục đích.

1. Xác nhận `KGR_DS_SFC_vs_MEMO_v2` còn tồn tại + số còn đúng (checklist §6, mục 1–3).
2. **Canvas 14:** gỡ các viz đang trỏ `KGR_DS_SFC_vs_Actual_v2`, dựng lại theo đúng pattern Canvas 24 (đang đúng):
   - Bar/combo `SL_Ke_Hoach` vs `SL_Thuc_Te` theo `Tên Ngành` (màu Kangaroo: actual `#44BA46`, plan `#636466`).
   - KPI tile Achievement % = SUM(SL_Thuc_Te)/SUM(SL_Ke_Hoach) ≈ 160%.
   - Doanh thu plan kèm caveat hiện hữu (zero_price_pct 76.28%, reliable=false — caveat này ĐÚNG, giữ nguyên).
3. Gỡ `KGR_DS_SFC_vs_Actual_v2` khỏi Data panel của workbook (hoặc tối thiểu: không viz nào còn tham chiếu) để không ai tái sử dụng nhầm.
4. Đề xuất thêm (cần duyệt riêng): rename/move dataflow + dataset DS_v2 thành `_DEPRECATED_...` trong catalog.

- **Ưu:** zero rủi ro số liệu (dataset đã verify EXACT), nhanh nhất, Canvas 14 hết mâu thuẫn với Canvas 24.
- **Nhược:** grain chỉ tới `Tên Ngành` — Canvas 14 sẽ không drill xuống Nhóm SP/Model từ dataset này.

### Phương án B — nếu Canvas 14 cần drill-down Nhóm SP: build `KGR_DF_SFC_vs_MEMO_v3` (mở rộng grain)
Dataflow mới, cùng nguyên tắc §3, thêm Nhóm SP vào grain:

    NHÁNH PLAN:
      Add Data (KGR) DW_SFC
        cột: Ngành hàng, Nhóm sản phẩm, PERIODNAME, SL W1..SL W5, Doanh thu (-VAT)
      → Filter  PERIODNAME = 'May 2026'
      → AddColumns  Plan_Qty = "SL W1"+"SL W2"+"SL W3"+"SL W4"+"SL W5"
      → GroupBy (Ngành hàng, Nhóm sản phẩm)  SUM(Plan_Qty), SUM(Doanh thu (-VAT))

    NHÁNH ACTUAL:
      Add Data (KGR) DTF_CALC_INVOICE_MEMO_#
        cột: Tên Ngành, Nhóm SP, PERIODNAME, QUANTITY, Doanh số thực tế
      → Filter  PERIODNAME = 'May 2026'
      → GroupBy (Tên Ngành, Nhóm SP)  SUM(QUANTITY), SUM(Doanh số thực tế)
      → AddColumns  SL_Thuc_Te = -1 * QUANTITY_sum

    JOIN: FULL OUTER  ON  Ngành hàng = Tên Ngành  AND  Nhóm sản phẩm = Nhóm SP
      → OutputDataset  KGR_DS_SFC_vs_MEMO_v3

- **Gate bắt buộc trước khi save:** tổng theo Ngành của preview phải = golden từng ngành (445,043 / 713,262). Nếu lệch → khả năng taxonomy `Nhóm sản phẩm` (DW_SFC) ≠ `Nhóm SP` (MEMO#) không map 1:1 (độ tin cột DW_SFC ~80%, chưa enumerate) → dừng, báo lại, fallback Phương án A.
- **Cách build:** qua **OAC internal REST API** (canvas add-step bị wall với automation): clone definition flow chạy được (GET `/ui/dv/ui/api/v1/dataflows?dataFlowID=...`) → mutate steps → validate bằng `executePreview` → **POST** tạo mới (`/dataflows?folderPath=...&dataFlowName=...`, body DataGenAttributes; PUT chỉ để update) → Run qua catalog card Actions→Run (Save&Run trong editor sẽ hang với def build bằng API). Cheatsheet đầy đủ: `C:\Project\KGR_Dashboard\ERROR_LOG.md` mục "WORKAROUND VERIFIED"; schema cột: `DW_SFC_COLUMNS.txt`.

### Hạng mục dùng chung cho cả 2 phương án
- **Tham số kỳ:** filter 'May 2026' đang hardcode. Đề xuất biến thể multi-period-safe (đưa `PERIODNAME` vào GroupBy 2 nhánh + thêm vào khóa join, bỏ Filter) để sang June 2026 (period 43) không phải sửa flow — nhưng **chỉ triển khai sau khi gate single-period pass**, vì biến thể này chưa từng verify. Nếu chưa duyệt thì giữ single-period, mỗi tháng sửa 1 giá trị filter.
- **Lưu workbook:** dialog "Share Related Items" phải bấm **OK** (Escape = CANCEL save — đã mất canvas 3 lần vì bug này); sau save verify bằng GET `projects/json` (đếm canvas + last-modified).

---

## 5. Quyết định cần anh/chị duyệt

| # | Câu hỏi | Khuyến nghị |
|---|---|---|
| 1 | Phương án A (tái dùng MEMO_v2) hay B (build v3 grain Nhóm SP)? | **A trước**; B chỉ khi Canvas 14 bắt buộc drill-down |
| 2 | Định nghĩa "Actual" = 713,262 (MEMO#, **mọi SKU** có hóa đơn) — chấp nhận làm chuẩn dashboard? Chuẩn SFC-scope nghiêm ngặt là 586,292 (loại SKU ngoài plan: bảo dưỡng, phụ kiện; rule `qty_count_flag` trong `sfc_actual.sql`). Hai số chênh +22%, dồn ở Home care. | Dùng 713K cho nhất quán với Canvas 24, **nhãn rõ "Tổng SL hóa đơn (mọi SKU)"**; muốn đúng 586K phải refresh `DTF_CALC_SFC Thực tế` (kỳ May đang load ~1/3) hoặc thêm cờ SFC-scope vào flow — việc riêng, cần duyệt riêng |
| 3 | Được phép GỠ viz hỏng trên Canvas 14 (vượt guardrail ADD-only trước đây)? | Có — Canvas 14 đang hiển thị số sai cho executive |
| 4 | Deprecate/rename `KGR_DF/DS_SFC_vs_Actual_v2` trong catalog? | Nên, tránh tái sử dụng nhầm |
| 5 | Kỳ báo cáo: giữ May 2026 hay chuyển/thêm June 2026 (period 43)? | Verify May trước (có golden); June là bước mở rộng sau |

---

## 6. Checklist kiểm chứng thực tế SẼ CHẠY (khi có browser/REST trở lại)

**Bước 0 — môi trường:** mở OAC theo `OAC_CHROME_MCP_PLAYBOOK.md`; mọi snapshot ghi ra file rồi Grep/Read (không dump textContent); lấy `x-csrf-token` từ XHR bất kỳ cho các call REST.

**Khối 1 — xác nhận chẩn đoán (read-only):**
1. `GET /ui/dv/ui/api/v1/dataflows?dataFlowID=<id KGR_DF_SFC_vs_Actual_v2>` → đọc definition: xác nhận join type + vị trí join trước aggregate + nguồn 2 nhánh (chốt root-cause §2.1, §2.3 bằng văn bản định nghĩa thay vì suy luận từ dữ liệu).
2. `executePreview` trên DS_v2 (hoặc viz tạm): đếm distinct POSTINGPERIOD (kỳ vọng ~41–61) và tỷ lệ fan-out theo ngành (kỳ vọng 2.6–4.2x) — xác nhận §2.2 còn nguyên hiện trạng (dataset có thể đã bị rebuild lần nữa).
3. Mở Canvas 14, chụp filter hiện tại (kỳ vọng POSTINGPERIOD ≥ 42) + agg của pill Plan (kỳ vọng Maximum) — khớp triệu chứng 2.44M / 40K.

**Khối 2 — xác nhận giải pháp còn đúng:**
4. Search catalog: `KGR_DS_SFC_vs_MEMO_v2` còn tồn tại; xem last-run của `KGR_DF_SFC_vs_MEMO_v2`.
5. `executePreview` (hoặc bảng tạm trên canvas nháp): tổng theo Ngành = **445,043 plan / 713,262 actual** — nếu lệch, dữ liệu nguồn đã thay đổi → re-run dataflow rồi đo lại.
6. Validate-first nguồn MEMO#: `executePreview` đọc `DTF_CALC_INVOICE_MEMO_#` (lỗi ORA-00942 từng INTERMITTENT — không giả định, phải thử).
7. Cross-check độc lập nếu NSAW MCP có token: `get_sfc_report` period 42 → forecast_qty phải = 445,043.

**Khối 3 — thi công sau khi được duyệt:**
8. (Phương án A) Sửa Canvas 14: gỡ viz DS_v2, dựng bar + KPI từ MEMO_v2 (pattern Canvas 24, màu #44BA46/#636466, viz mới dựng trên canvas trống rồi move nếu cần — double-click trên canvas đông sẽ merge nhầm vào viz chính).
9. (Phương án B, nếu duyệt) Build v3 qua REST theo §4B; **gate preview = golden từng ngành trước khi POST/save**; Run qua Actions→Run; poll dataset xuất hiện.
10. Save workbook → bấm **OK** ở "Share Related Items" → verify persist: GET projects/json đếm canvas + last-modified; reload đọc lại số trên Canvas 14.
11. Hậu kiểm chéo: Canvas 14 vs Canvas 24 phải trùng số (445,043 / 713,262 / ~160%); chạy lại NSAW cross-check nếu có.

---

## 7. Rủi ro & lưu ý

| Rủi ro | Mức | Giảm thiểu |
|---|---|---|
| Dataset MEMO_v2/nguồn đã thay đổi sau 2026-06-07 (DS_v2 từng bị rebuild âm thầm) | TB | Khối 2 checklist chạy TRƯỚC khi sửa canvas |
| Taxonomy Nhóm SP không khớp 2 nguồn (Phương án B) | TB | Gate tổng-theo-Ngành; fallback A |
| MEMO# chứa khách nội bộ (SC=14 chưa loại; doanh thu +2.5% vs NSAW 342.8B) | Thấp (qty), TB (revenue) | Chỉ dùng qty cho achievement; revenue actual ghi chú nguồn |
| Escape-save làm mất canvas | Cao nếu quên | Luôn OK + verify GET projects/json (đã mất canvas 3 lần) |
| `DTF_CALC_SFC Thực tế` bị dùng nhầm cho May | TB | Ghi rõ: cấm dùng tới khi refresh đủ tháng |
| Hardcode kỳ 'May 2026' gây lỗi âm thầm sang tháng sau | TB | Hạng mục multi-period-safe §4 (cần duyệt) |

## 8. Tiêu chí nghiệm thu (acceptance)

1. Canvas 14: Plan = **445,043**, Actual = **713,262**, Achievement ≈ **160%** — trùng Canvas 24 và NSAW.
2. Không viz nào trong workbook còn tham chiếu `KGR_DS_SFC_vs_Actual_v2`.
3. Số persist sau reload + last-modified cập nhật (verify qua GET projects/json).
4. Nhãn actual ghi rõ "Tổng SL hóa đơn (mọi SKU)" nếu giữ chuẩn 713K.

---

*Nguồn bằng chứng: memory project_ds_sfc_v2_actual_fanout / project_kgr_df_sfc_vs_memo_v1 / project_kgr_df_sfc_vs_memo_v2 / project_sfc_actual_vs_golden_gap / project_dtf_calc_sfc_may_partial / project_db01_live_10_canvases; file `C:\Project\KGR_Dashboard\SFC_CHART_RESULT.md`, `ERROR_LOG.md` ("WORKAROUND VERIFIED"), `DW_SFC_COLUMNS.txt`, `MEMO_FILTER_DIAGNOSIS.md`, `C:\Project\NSAW_Claude\queries\sfc_actual.sql`.*
