# KẾ HOẠCH DATAFLOW — SFC Kế hoạch vs Thực tế theo CHUỖI (T5/2026)

> **Trạng thái:** BẢN KẾ HOẠCH CHỜ DUYỆT — chưa thao tác gì trên OAC (môi trường hiện tại không có browser).
> **Người lập:** Claude Code · 2026-06-11 · Instance: `oaxinst70021` · User OAC: `minhndn@bizin.vn`
> **Nguồn tri thức:** `C:\Project\KGR-OAC-Agents\Dataflow-builder\OAC_DATAFLOW_MASTERY.md` (file golden tự chứa) + bằng chứng build đã verify trên đĩa (`v4_chuoi_validate.json`, `v4v5_verify.json`, `actual_kenh_chuoi.json`, `plan_kenh_chuoi_test.json`).

---

## 0. TÓM TẮT ĐIỀU HÀNH (đọc 30 giây)

**Yêu cầu:** 1 dataset OAC, **mỗi dòng = 1 chuỗi** (BIGC, DMX, Caophong…), có cột **SL kế hoạch SFC** và **SL thực tế bán**, kỳ **tháng 5/2026**, để vẽ chart so sánh.

**Phát hiện quan trọng nhất:** dataset đúng yêu cầu này **ĐÃ TỒN TẠI và ĐÃ VERIFY CHÍNH XÁC** ngày 2026-06-07:

- Dataflow: `KGR_DF_SFC_vs_MEMO_v4_Chuoi` — id `'e659cf70-cfe4-4143-a1b4-6e0088a2a1ad'.'KGR_DF_SFC_vs_MEMO_v4_Chuoi'`
- Dataset output: `'minhndn@bizin.vn'.'KGR_DS_SFC_vs_MEMO_v4_Chuoi'` — 9 dòng (8 chuỗi + 1 bucket "Khác (ngoài chuỗi)"), cột `Chuỗi gộp` / `SL_Ke_Hoach` / `SL_Thuc_Te`, tổng khớp golden (plan 445.043 / actual 713.262).
- Dataflow/dataset tạo qua REST POST nên **độc lập workbook** — không bị mất theo sự cố Escape-save của workbook (ERROR_LOG xác nhận "v3/v4/v5 dataset + dataflow vẫn còn sau mất canvas").

**Khuyến nghị: Phương án A — TÁI SỬ DỤNG v4_Chuoi** (chạy bộ check trinh sát C1–C6 → re-run để refresh số liệu → nghiệm thu), **KHÔNG build mới**. Chỉ rơi xuống Phương án B (build lại bản sao) nếu check phát hiện flow/dataset đã hỏng/mất. Phương án C (nâng cấp actual sang đúng scope SFC) là tùy chọn, phụ thuộc kết quả check C7.

**1 caveat nghiệp vụ phải chốt khi duyệt (mục 8, Q1):** cột "thực tế" lấy từ MEMO# = **tổng SL hóa đơn mọi SKU** (713K toàn quốc), KHÔNG phải "thực tế trong scope kế hoạch SFC" (586K golden). Ở grain chuỗi thì đây vẫn là nguồn khả dụng duy nhất đã verify (nguồn SFC-scope `DTF_CALC_SFC Thực tế` đang thiếu ~2/3 dữ liệu tháng 5 và chưa rõ có cột chuỗi). Nhãn chart phải ghi rõ "SL thực tế (tổng hóa đơn)".

---

## 1. YÊU CẦU & TIÊU CHÍ NGHIỆM THU

| # | Yêu cầu | Diễn giải kỹ thuật |
|---|---|---|
| R1 | Mỗi dòng = 1 chuỗi | Grain = `Chuỗi gộp` (coalesce tên chuỗi 2 nguồn). 8 chuỗi định danh: BIGC, DMX, MM, Caophong, FPT, VHC, Nguyenkim, Thongnhat + 1 bucket "Khác (ngoài chuỗi)" |
| R2 | Cột SL kế hoạch | `SL_Ke_Hoach` = SUM(SL W1..SL W5) từ `(KGR) DW_SFC` (DW_SFC KHÔNG có cột qty tháng — chỉ weekly) |
| R3 | Cột SL thực tế | `SL_Thuc_Te` = `0 − SUM(QUANTITY)` từ `(KGR) DTF_CALC_INVOICE_MEMO_#` (QUANTITY lưu ÂM; công thức này đã net credit memo, không dùng ABS) |
| R4 | Tháng 5/2026 | Filter `PERIODNAME IN ('May 2026')` cả 2 nhánh (= POSTINGPERIOD 42; ánh xạ 1:1 đã verify). **Filter 1 kỳ duy nhất là chốt chặn fan-out** — đã chứng minh triệt tiêu fan-out 4× của DW_SFC |
| R5 | Vẽ được chart so sánh | Plan + Actual phải nằm CÙNG dataset (pre-join bằng dataflow). Blend 2 dataset trong viz đã chứng minh BẤT KHẢ (cartesian fan-out) |

**Tiêu chí nghiệm thu (acceptance):**
1. Dataset trả đúng **9 dòng** (hoặc 8 nếu user chốt loại bucket "Khác" ngay trong dataflow — xem Q2).
2. Tổng `SL_Ke_Hoach` (kể cả Khác) = **445.043** (golden plan, đã đối chiếu NSAW `forecast_qty` p42 EXACT).
3. Tổng `SL_Thuc_Te` (kể cả Khác) = **713.262** (golden MEMO#-scope; chấp nhận xê dịch nhỏ nếu MEMO# nhận thêm bút toán muộn sau 2026-06-07 — ghi nhận chênh lệch nếu có).
4. Spot-check theo chuỗi khớp bảng tham chiếu mục 2.
5. Không dòng nào bị nhân bản (fan-out): số dòng = số giá trị distinct của `Chuỗi gộp`.

---

## 2. BẢNG SỐ THAM CHIẾU ĐÃ VERIFY (2026-06-07, executePreview + đọc dataset materialized)

| Chuỗi gộp | SL_Ke_Hoach | SL_Thuc_Te | Ghi chú |
|---|---:|---:|---|
| DMX | 72.230 | 157.407 | chuỗi lớn nhất, vượt KH ~218% |
| Caophong | 11.170 | 6.606 | |
| BIGC | 6.047 | 2.027 | |
| FPT | 4.440 | 597 | |
| MM | 3.403 | 4.204 | |
| VHC | 2.569 | 2.004 | |
| Nguyenkim | 2.545 | 338 | |
| Thongnhat | (NULL) | 350 | có bán, KHÔNG có kế hoạch SFC T5 → xem Q3 (coalesce 0?) |
| Khác (ngoài chuỗi) | 342.639 | 539.729 | ~77% plan / ~76% actual — ngoài chuỗi; thường loại khỏi viz |
| **TỔNG** | **445.043** | **713.262** | khớp golden Canvas 24 |

Cột thực có trong dataset v4 hiện hữu (đọc từ `v4_chuoi_validate.json`):
`Tên Chuỗi · QUANTITY Sum · Doanh thu thực tế Sum · SL_Thuc_Te · Chuỗi · SL W1..SL W5 · DT_Ke_Hoach · SL_Ke_Hoach · Chuỗi gộp`
→ Cột thừa trung gian (SL W1..W5, QUANTITY Sum) vẫn nằm trong dataset; không hại cho chart nhưng kém gọn — xem Q4.

---

## 3. PHÂN TÍCH NGUỒN DỮ LIỆU

### 3.1 Nhánh KẾ HOẠCH — `(KGR) DW_SFC` ✅ (chốt)
- Datamodel star-schema ~23 folder, nền `(KGR) SFC Dataset (có AI)` (owner viethl@bizin.vn).
- Cột chuỗi (display): **`Chuỗi`** — đã chứng minh tồn tại & ra đúng 8 dòng plan (file `plan_kenh_chuoi_test.json`: 7 chuỗi định danh + 1 dòng NULL/ngoài chuỗi = 342.639). Tên physical qualified xác nhận ở check C1 (đọc từ def v4 thật, dự kiến dạng `"DW_NS_X_CAM_CUSTOMRECORD_CSEG_SCV_CHAIN"."..."`).
- Qty kế hoạch: **chỉ có weekly** `"DW_NS_X_SFC_LINES_CF"."SL W1".."SL W5"` → tháng = tổng 5 tuần.
- Kỳ: `"DW_NS_ACCOUNTINGPERIOD_D"."PERIODNAME"` ('May 2026' = POSTINGPERIOD 42).
- ⚠️ Fan-out ~4× ở grain dòng nếu lấy nhiều kỳ → **bắt buộc Filter 1 kỳ TRƯỚC GroupBy** (đã verify: filter 1 kỳ + plain SUM = golden EXACT, không cần dedup MAX-then-SUM).

### 3.2 Nhánh THỰC TẾ — `(KGR) DTF_CALC_INVOICE_MEMO_#` ✅ (chốt, kèm caveat scope)
- Dataset DB 64 cột, owner anhdk@bizin.vn, `XSA('anhdk@bizin.vn'.'(KGR) DTF_CALC_INVOICE_MEMO_#')`, cột KHÔNG qualified.
- Cột chuỗi: **`Tên Chuỗi`** — đã chứng minh có grain chuỗi thật (file `actual_kenh_chuoi.json`: 9 nhóm, 8 chuỗi định danh + NULL 539.729). Lưu ý: **`Nhóm Kênh`/`Tên Kênh` toàn NULL** → grain kênh KHÔNG làm được, grain chuỗi LÀM ĐƯỢC.
- Qty: `QUANTITY` (ÂM với CustInvc, DƯƠNG với CustCred) → `SL_Thuc_Te = 0 − SUM(QUANTITY)` (tự net credit ~5K).
- ⚠️ **Caveat scope:** 713.262 = mọi SKU có hóa đơn; golden SFC-scope chỉ 586.292 (khác biệt = item ngoài quy hoạch SFC, tập trung Home care). KHÔNG có filter cột nào trên MEMO# tái tạo được 586K (đã chẩn đoán cạn kiệt, RESOLVED). → Nhãn phải là "SL thực tế (tổng SL hóa đơn)", không gọi "% đạt KH SFC" tuyệt đối.
- ⚠️ Readability INTERMITTENT: từng dính `ORA-00942` transient và `ORA-28000` (account anhdk khóa — chỉ chặn viz live query, KHÔNG chặn DataFlow Run). → nguyên tắc **validate-first** bằng executePreview (check C3), không pre-assume hỏng.

### 3.3 Nguồn bị LOẠI / để dành
| Nguồn | Lý do loại |
|---|---|
| `(KGR) DTF_CALC_SFC Thực tế` | Actual T5/2026 PARTIAL ~1/3 (Water 155K vs golden 459K); Mar/Apr đủ, May chưa refresh. Chưa rõ có cột chuỗi. → Để dành làm **Phương án C** nếu check C7 cho thấy đã refresh + có chuỗi (khi đó actual đúng SFC-scope 586K) |
| `KGR_DS_SFC_vs_Actual_v2` | Fan-out ~4.17× (multi-period inner join) — cấm dùng cho chart |
| `KGR_DS_SFC_vs_MEMO_v1` | Plan side under-count 44% (inner join rớt SKU có KH nhưng chưa bán) — chỉ actual side tin được |
| Blend 2 dataset trong viz | Cartesian fan-out — bất khả, phải pre-join bằng dataflow |

---

## 4. THIẾT KẾ DATAFLOW

### 4.1 PHƯƠNG ÁN A (KHUYẾN NGHỊ) — Tái sử dụng `KGR_DF_SFC_vs_MEMO_v4_Chuoi`
Không build gì mới. Trình tự sau khi duyệt:
1. Chạy bộ check C1–C6 (mục 5).
2. **Re-run** dataflow (Home → hover card → Actions → Run; server-side, ~10–20s) để materialize lại với dữ liệu MEMO#/DW_SFC mới nhất (lần run trước chốt 2026-06-07; T5 đã đóng nên plan không đổi, actual có thể nhích nhẹ do bút toán muộn).
3. Nghiệm thu theo mục 1 (executePreview hoặc mở dataset, KHÔNG tin toast).
4. (Nếu user duyệt Q4) thêm bước Select/Rename qua PUT định nghĩa để gọn cột — nhưng mặc định GIỮ NGUYÊN để không rủi ro (rename ở Save step từng KHÔNG persist).

**Ưu:** 0 build mới, số đã từng verify EXACT, ít rủi ro nhất. **Nhược:** mang theo cột trung gian thừa; tên dataset hậu tố "_v4" hơi kỹ thuật.

### 4.2 PHƯƠNG ÁN B (DỰ PHÒNG) — Build bản mới `KGR_DF_SFC_Chuoi_T5_v1` (chỉ khi C1/C2 fail)
Kiến trúc 2 nhánh + full outer join (logic giống hệt v4 đã verify, thêm coalesce-0 và Select Columns cho gọn):

```
NHÁNH PLAN (DW_SFC):
  [P1] Add Data (KGR) DW_SFC — chọn cột: Chuỗi, PERIODNAME, SL W1..SL W5
  [P2] Filter: "PERIODNAME" IN ('May 2026')          ← chốt chặn fan-out, TRƯỚC GroupBy
  [P3] Aggregate: Group by (Chuỗi); SUM từng SL W1..W5
  [P4] Add Columns: SL_Ke_Hoach = "SL W1"+"SL W2"+"SL W3"+"SL W4"+"SL W5"   (Apply TỪNG cột!)

NHÁNH ACTUAL (MEMO#):
  [A1] Add Data (KGR) DTF_CALC_INVOICE_MEMO_# — chọn cột: Tên Chuỗi, PERIODNAME, QUANTITY
  [A2] Filter: "PERIODNAME" IN ('May 2026')
  [A3] Aggregate: Group by (Tên Chuỗi); SUM(QUANTITY) → "QUANTITY Sum"
  [A4] Add Columns: SL_Thuc_Te = 0 - "QUANTITY Sum"

GHÉP:
  [J1] Join FULL OUTER (Keep rows: All + All); joinOn: Chuỗi = Tên Chuỗi (cùng kiểu text)
  [J2] Add Columns: Chuoi_Gop = IFNULL(IFNULL("Chuỗi","Tên Chuỗi"), 'Khác (ngoài chuỗi)')
        SL_KH_0 = IFNULL("SL_Ke_Hoach", 0)        ← xử lý Thongnhat plan NULL (nếu duyệt Q3)
        SL_TT_0 = IFNULL("SL_Thuc_Te", 0)
  [J3] Select Columns: giữ Chuoi_Gop, SL_KH_0, SL_TT_0 (bỏ cột trung gian)
  [S1] Save Dataset: KGR_DS_SFC_Chuoi_T5_v1 — Treat As: Chuoi_Gop=Attribute; SL_*=Measure/Sum
```

**Đường thi công:** ưu tiên **REST API** (đường tin cậy nhất, né toàn bộ wall canvas):
- GET def của v4 thật (`GET /ui/dv/ui/api/v1/dataflows?dataFlowID=<urlenc id v4>`; body là JSON-encoded STRING → JSON.parse → `.definition`) → **mutate in-place** (KHÔNG hand-build từ pseudo-schema — `OAC_V3_DATAFLOW_DEFINITION.json` là schema GIẢ, cấm dùng).
- `executePreview` từng nhánh + node output để validate số TRƯỚC khi tạo (body PHẲNG `{steps, links, stepId, DSSDependencies}`; stepId không trùng SQL reserved word).
- **CREATE = POST** `/ui/dv/ui/api/v1/dataflows?folderPath=%2F%40Catalog%2Fusers%2Fminhndn%40bizin.vn&dataFlowName=...` body DataGenAttributes (datagen-name/display-name/dataflow-name/datagen-type:"DATAFLOW"/definition; BỎ custom-attrs và field lạ). PUT chỉ để update flow đã có.
- Run từ Home → Actions → Run (editor Run/Save&Run HANG với def REST-built).
- Mọi call là same-origin fetch từ trang OAC qua evaluate_script (Bash curl bị proxy chặn — exit 56).

### 4.3 PHƯƠNG ÁN C (TÙY CHỌN NÂNG CẤP) — Actual đúng SFC-scope
Chỉ khả thi nếu check C7 cho thấy `(KGR) DTF_CALC_SFC Thực tế` (a) đã refresh đủ T5 (Water ≈459K) VÀ (b) có cột chuỗi. Khi đó thay nhánh ACTUAL bằng nguồn này → `SL_Thuc_Te` đúng scope kế hoạch SFC (tổng ≈586.292), achievement mang nghĩa "% đạt KH SFC" thật. Nếu C7 fail (khả năng cao) → giữ Phương án A + nhãn caveat.

---

## 5. TRINH SÁT NGUỒN — BỘ CHECK SẼ CHẠY (khi có browser, trước khi đụng vào bất kỳ thứ gì)

> Quy ước: tất cả check là **read-only** (GET / executePreview — không side-effect). Chạy bằng same-origin `fetch` qua `evaluate_script` trên trang OAC đã đăng nhập; header POST cần `x-csrf-token` + `authorization: session` + `x-requested-with: XMLHttpRequest`, `credentials:'include'`. Kết quả ghi ra file rồi Grep/Read (không đổ thẳng vào context).

| # | Check | Lệnh cụ thể | Kỳ vọng (PASS) | Nếu FAIL |
|---|---|---|---|---|
| **C1** | Dataflow v4 còn sống + đọc def thật | `GET /ui/dv/ui/api/v1/dataflows?dataFlowID=` + urlenc `'e659cf70-cfe4-4143-a1b4-6e0088a2a1ad'.'KGR_DF_SFC_vs_MEMO_v4_Chuoi'` → JSON.parse → `.definition` | `success:true`; def có 2 InputDataset (DW_SFC + MEMO#), Filter 'May 2026' cả 2 nhánh, Join fullouterjoin, AddColumns `Chuỗi gộp`; ghi lại tên physical của cột `Chuỗi` plan | → Phương án B (clone def từ `v2_dataflow_full.json`/`v3_final_def.json` làm khung) |
| **C2** | Dataset v4 còn trong catalog | Homepage search API `includeCategory=datasources`, query "KGR_DS_SFC_vs_MEMO_v4_Chuoi" (pattern y hệt `v4v5_verify.json`) | thấy id `'minhndn@bizin.vn'.'KGR_DS_SFC_vs_MEMO_v4_Chuoi'` | → re-run dataflow (nếu C1 còn) hoặc Phương án B |
| **C3** | MEMO# readable (validate-first, lỗi transient) | `executePreview` mini-def: InputDataset MEMO# → Filter May 2026 → GroupBy(Tên Chuỗi) SUM(QUANTITY), `stepID` = node GroupBy | ≥8 rows, không ORA-00942; ORA-28000 trong viz-context thì BỎ QUA (không chặn DataFlow Run) | retry 1 lần sau reload dataset; vẫn fail → DBA unlock anhdk / hoãn nhánh actual |
| **C4** | Số liệu v4 hiện tại (trước re-run) | `executePreview` trên def lấy từ C1, `stepId` = OutputDataset node | 9 rows; tổng plan 445.043; actual ≈713.262 | nếu cấu trúc sai (≠9 rows, fan-out) → Phương án B |
| **C5** | Plan tổng còn khớp golden | executePreview nhánh plan: DW_SFC → Filter May 2026 → GroupBy(Chuỗi) SUM(SL W1..W5) | 8 nhóm; tổng = 445.043 EXACT (T5 đã khóa kế hoạch — không được lệch) | điều tra DW_SFC bị sửa/refresh; DỪNG chờ user |
| **C6** | Khớp tên chuỗi 2 nguồn (join key) | từ C4/C5: so distinct `Chuỗi` (plan) vs `Tên Chuỗi` (actual) | 7 chuỗi khớp 1-1; Thongnhat chỉ có actual; NULL 2 bên gộp "Khác (ngoài chuỗi)" | tên mới lệch chính tả → thêm Group/CASE map tên trước Join |
| **C7** | (cho P.án C) DTF_CALC_SFC Thực tế đã refresh + có chuỗi? | metadata API `POST /dataset/datasets/metadata`; executePreview Filter May 2026 → GroupBy(Tên ngành) SUM(Số lượng) | refresh OK nếu Water ≈459K (hiện 155K = chưa); có cột chuỗi trong columnMetadataArray | giữ Phương án A + caveat nhãn |
| **C8** | (hậu-run) Tên cột output persist | sau Run: metadata API đọc outputColumns | có `SL_Ke_Hoach`, `SL_Thuc_Te`, `Chuỗi gộp` (rename Save-step từng không persist) | rename tầng dataset/workbook calc |
| **C9** | (giai đoạn chart) viz Chuỗi trên canvas CHAIN | `GET /ui/dv/ui/api/v2/projects/json?path=<enc DB01>` | viz SFC-theo-Chuỗi đang sống trên canvas CHAIN (line plan đang CAM, cần `#636466`) | rebuild viz từ dataset này; màu Kangaroo: actual `#44BA46` / plan `#636466` |

**Thứ tự:** C1 → C2 → C3 → C4/C5 → C6 → C7 → quyết A/B/C → thi công → C8 → C9.

---

## 6. TRÌNH TỰ THI CÔNG SAU KHI USER DUYỆT

1. Đăng nhập OAC (user vắng mặt: credentials đã ủy quyền trong MASTERY §0; user hiện diện → nhờ user login).
2. Chạy C1–C7, ghi kết quả ra file `_recon_chuoi_*.json`.
3. Theo nhánh: **A:** Home → card v4_Chuoi → Actions → **Run** → ~10–20s → C8. **B:** GET def → mutate → executePreview validate → POST create → Actions→Run → C8.
4. Nghiệm thu số (mục 1) bằng executePreview/mở dataset — **không tin toast**.
5. Bàn giao: id dataset + bảng số per-chuỗi + caveat scope cho bước chart.
6. (Bước chart, ngoài scope): Add Data dataset vào DB01 nếu thiếu; Save ở shared folder → dialog "Share Related Items" → **bấm OK, TUYỆT ĐỐI KHÔNG Escape** (Escape hủy cả save — đã mất canvas 3 lần); verify qua `GET projects/json`.

---

## 7. RỦI RO & GIẢM THIỂU

| Rủi ro | Mức | Giảm thiểu |
|---|---|---|
| MEMO# transient ORA-00942 / ORA-28000 (account anhdk) | TB | Validate-first (C3); ORA-28000 không chặn DataFlow Run; tệ nhất nhờ DBA unlock |
| Actual nhích so 713.262 (bút toán muộn) | Thấp | Re-run rồi chốt số mới; ghi chênh lệch vào nghiệm thu |
| Rename Save-step không persist → cột tên default | TB | C8 kiểm sau Run; fallback rename tầng workbook |
| Editor canvas walls | Cao nếu đi canvas | Đi đường REST (đã verify); canvas chỉ để xem |
| Escape trên Share dialog hủy save workbook | Cao (mất 3 lần) | Chỉ bấm OK + verify projects/json |
| Hiểu nhầm "% đạt KH" do scope MEMO# | Cao (nghiệp vụ) | Nhãn "SL thực tế (tổng hóa đơn)"; chốt Q1 |
| Fan-out nếu sửa filter thành nhiều kỳ | Cao | Ghi vào Description flow: "FILTER 1 KỲ DUY NHẤT" |

---

## 8. CÂU HỎI CHỜ USER QUYẾT

- **Q1 (quan trọng nhất):** Chấp nhận actual = MEMO# tổng SL hóa đơn mọi SKU (713K) với nhãn caveat? Hay chờ refresh `DTF_CALC_SFC Thực tế` để có actual đúng scope SFC (586K)?
- **Q2:** Bucket "Khác (ngoài chuỗi)" (~76–77%): GIỮ trong dataset rồi exclude ở viz (khuyến nghị — giữ khả năng đối soát tổng), hay LOẠI hẳn trong dataflow?
- **Q3:** Thongnhat có actual (350) nhưng KH NULL: coalesce → 0 hay để NULL?
- **Q4:** Có tidy cột (bỏ SL W1..W5, QUANTITY Sum) không? Mặc định GIỮ NGUYÊN v4 (ít rủi ro nhất).
- **Q5:** Giữ tên `KGR_DS_SFC_vs_MEMO_v4_Chuoi` (tái sử dụng) hay tên thân thiện hơn (→ phải build mới, Phương án B)?

---

*Hết kế hoạch. Chưa thực thi gì trên OAC — chờ duyệt.*
