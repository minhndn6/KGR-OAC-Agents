# CONFLICTS & OPEN QUESTIONS — chờ user trả lời (2026-06-20)

> Gom mọi mâu thuẫn, giả định đã áp, và câu hỏi cần xác nhận trong phiên trích xuất live 2026-06-20. Duyệt 1 lượt khi rảnh. Đánh số để tiện trả lời.

## A. Câu hỏi cần XÁC NHẬN (ảnh hưởng đúng/sai của tri thức)

**Q1 — Multi-producer cho cùng 1 output dataset (in_closure, đang dùng thật).** 3 dataset đang được workbook dùng nhưng có ≥2 dataflow cùng khai là producer → không chắc bản nào THỰC SỰ chạy ghi dữ liệu:
- `Nganh_Report_Long_#` ← `KGR_DF_Nganh_Metrics_v3` / `_v2` / `KGR_DF_Nganh_Metrics` (3 flow). Bản nào là bản đang chạy ghi?
- `Daily_Nganh_Report` ← `KGR_DF_Daily_Nganh_Report_m` / `KGR_DF_Daily_Nganh_Report` (2 flow).
- `KGR_DS_ACTUAL_AOP_MONTHLY_v2` ← `KGR_DF_ACTUAL_AOP_MONTHLY_LK` / `_v3` / `_v2` (3 flow; tên dataset là v2 nhưng có thể LK/v3 mới là bản ghi cuối).
→ **Cần biết flow nào là bản sản xuất** để (a) lineage chỉ đúng 1 nguồn, (b) archive phần còn lại. (Chi tiết: `archive_recommendations.md`.)

**Q2 — `TD_Report_Long` & `TD_Metrics_Wide` nằm trong folder `(KGR) Archived` nhưng VẪN được BC01 + DB02 dùng.** Producer sống là `KGR_DF_TD_Metrics_bk` (sửa 2026-06-20, ở `@default`), còn `KGR_DF_TD_Metrics_v1.0` ở folder Archived. → Dataset “Archived” mà vẫn production: có chủ ý không, hay cần chuyển ra khỏi Archived? Tên `_bk` (backup) gây hiểu nhầm — có nên đổi tên flow sản xuất?

**Q3 — Subtree chi phí/AOP-tháng (in_closure=false) có phục vụ báo cáo NGOÀI 4 workbook không?** Các dataflow `(KGR) DF_FACT_EXPENSE` → `(KGR) DTF_FACT_EXPENSE`, `(KGR) DF_GRAIN_ACTUAL_AOP`, `(KGR) DF_ACTUAL_AOP_EXPENSE`, `KGR_DF_ACTUAL_AOP_MONTHLY_*` không nuôi 4 workbook đang xét, nhưng có 2 *sequence* (`BC Thực tế Tháng`, `Daily & Summary report`) có thể chạy chúng theo lịch cho báo cáo khác. → Có workbook/báo cáo khác ngoài 4 cái này dùng chúng không? (Nếu có, đừng archive.)

**Q4 — NSAW_Claude drift.** 20/60 bảng vật lý đang dùng KHÔNG có trong NSAW_Claude (`documented_in_nsaw=false`), ví dụ: `DW_NS_X_BANG_CP_LUONG`, `DW_NS_X_TY_LE_CP_KHAC`, `DW_NS_X_TY_LE_RSHN`, `DW_NS_X_BUT_TOAN_UT_*`, `DW_NS_X_CAM_CUSTOMRECORD_CSEG_SCV_*` (PRODGROUP/MODEL/SG_PRO/EXP_LIST), `DW_NS_X_CUSTOMRECORD_SCV_EXP_MAPPING`, `DW_NS_X_LIST_SALE_CHANEL_NS`, `DW_APPS_DAY_D`... → NSAW_Claude cần bổ sung; tạm thời ngữ nghĩa các bảng này chỉ suy từ tên cột. (Danh sách đầy đủ: lọc `physical_table_catalog.yaml` theo `documented_in_nsaw: false`.)

## B. Quan sát / giả định đã áp (không chặn, nhưng nên biết)

**O1 — Field `owner` (enumeration) ≠ owner trong `id`.** VD dataset `TD_Report_Long`/`Daily_Nganh_Report` enumeration ghi owner `anhdk` nhưng id là `'minhndn@bizin.vn'.'...'`. → Đã dùng **owner trong id (XSA)** làm chuẩn (đó là cái workbook tham chiếu). 

**O2 — Workbook đính nhiều datasource KHÔNG dùng.** DB01: 10/20 datasource không có cột nào tham chiếu (vd `(KGR) AOP Dataset`, `1. Invoice_v2`, `(KGR) DTF_DAILY_TAP_DOAN`, `Daily_TD_Report`, `(KGR) SFC Dataset (có AI)`, `(KGR) DTF_DAILY_KENH_CHUOI`, `AOP LINE CF`, `(KGR) DTF_CALC_SFC Thực tế`, `KGR_DS_SFC_Plan_by_Kenh`, `(KGR) DTF_ACTUAL_AOP_EXPENSE`). DB02: 4/11; BC01: 2/8. → Có thể gỡ khỏi workbook cho gọn (xem `workbook_catalog.yaml` `datasources[].used=false`). KHÔNG tự gỡ.

**O3 — `SFC_vs_MEMO_v1..v4_Chuoi` là 4 GRAIN khác nhau, không phải version chồng.** DB01 dùng cả 4 (v1: theo item; v2: SL plan vs actual; v3: nhóm SP gộp; v4: theo Chuỗi). → Đã coi là 4 dataset hợp lệ, KHÔNG đề xuất dedupe.

**O4 — `(KGR) DW_NS_CUSTOMER_D` (geo) DB01 đọc thẳng, không qua dataflow.** Nguồn vật lý suy từ expression workbook: `DW_NS_CUSTOMER_D` + file upload `oac_vn63_geo_bridge_with_ten_moi` (bridge tỉnh/thành 63→34 tỉnh mới). → physical_tables cho dataset này có thể chưa đầy đủ cột (chỉ những cột workbook dùng).

**O5 — `Metric_Dim` là dataset dim (file/nhập tay), không phải bảng DW.** Đã tách khỏi `physical_table_catalog`; nguồn của nó ghi ở `dataset_catalog` mục `file_or_other_sources`.

**O6 — Một số bảng có alias `_1` (vd `DW_NS_X_AOP_HEADER_CF_1`, `_SF_1`).** Đó là cùng bảng được add 2 lần trong dataset-builder (OAC tự thêm hậu tố). `base_table` đã ghi trong `physical_table_catalog`. → Coi như cùng bảng gốc.

## C. Giới hạn phương pháp (method notes)
- **M1 — Endpoint `POST /ui/dv/ui/api/v1/dataset/datasets/metadata` trả 500** trên instance này (mọi shape body). → Lineage vật lý lấy từ `InputDataset.columns` trong dataflow def (đã verify bằng `executePreview` flowSQL: `DW_NS_CUSTOMER_INVOICE_LINES_F` resolve sống). Hệ quả: dataset db **không được dataflow nào đọc** thì thiếu nguồn vật lý (chỉ O4 rơi vào trường hợp này, đã xử lý qua expression workbook).
- **M2 — `verified_live=true`** mới chỉ probe 2 bảng (`DW_NS_CUSTOMER_INVOICE_LINES_F`, `DW_NS_ACCOUNT_D`). 58 bảng còn lại = `via_dataflow_def` (trích từ def đọc hôm nay; chưa probe SELECT riêng). Đủ tin cho tên bảng/cột; nếu cần chắc 100% từng bảng → probe thêm.
- **M3 — KHÔNG lưu số (nguyên tắc)**: data live → KB chỉ lưu *cách tính* + *cách lấy số live* + *bất biến quan hệ*. Verify công thức bằng `executePreview` (đã xác nhận resolve sống) + kiểm các bất biến trong `live_query_recipes.md` (vd a4=a2−a3; a9=a4−a5−a6−a7−a8). KHÔNG ghi giá trị tuyệt đối.

## D. Drift đã PHÂN XỬ theo precedence (OAC thắng) — ghi để biết NSAW_Claude lệch
- **D1 Revenue**: OAC dùng `BASE_REVENUE` (UNION invoice+credit) ≠ NSAW_Claude `BASE_CREDITAMOUNT−BASE_DEBITAMOUNT`. → **theo OAC**.
- **D2 ACCTTYPE**: OAC lọc `IN('Income','OthCurrLiab')` ≠ NSAW chỉ `'Income'`. → **theo OAC**.
- **D3 Loại nội bộ**: OAC qua **whitelist subsidiary "Tên Đơn vị"** + loại `Vụ việc='HTL'` ≠ NSAW exclude SC=14 bằng customer extension. → **theo OAC** (kết quả tương đương nhưng cơ chế khác).
- **D4 SFC**: báo cáo BC03 dùng `(KGR) DTF_CALC_MIS` (authoritative) ≠ DB01 dùng `KGR_DS_SFC_vs_MEMO_v*`. → **theo báo cáo (BC)**.

## F. Điều tra 2026-06-20 (đề xuất — CHỜ OWNER CHỐT)

**F1 — Mệnh đề "Kênh nội bộ" trùng (Filter trong `(KGR) 1. DTF_CALC_INVOICE_MEMO_#`)**
- Sự thật: `Filter_0` = `... "Tên Đơn vị" IN('CTCP LD Kangaroo Quốc tế','Chi nhánh HCM') and "Kênh nội bộ" IN('T') and "Kênh nội bộ" IN('T')`; `Filter_1` chỉ có 1 lần.
- Kết luận kỹ thuật: lặp `A and A` là **idempotent → KHÔNG ảnh hưởng con số**; chỉ là dấu vết copy-paste, và **không nhất quán** giữa 2 filter gần-giống (1 nhánh lặp, 1 nhánh không).
- ❓ CẦN OWNER: ngữ nghĩa `"Kênh nội bộ" IN('T')` — 'T' nghĩa là GỒM hay LOẠI kênh nội bộ? (Việc loại nội bộ đang chủ yếu qua whitelist 2 pháp nhân.) Nên dọn mệnh đề lặp + làm rõ nghĩa.

**F2 — Producer SỐNG cho dataset multi-producer (bằng chứng offline; API KHÔNG lộ run-history → dùng last-modified + #steps + folder, không chắc 100%)**
| Output dataset | Đề xuất bản SỐNG | Bằng chứng | Độ tin | Bản nên ARCHIVE |
|---|---|---|---|---|
| `Nganh_Report_Long_#` | `KGR_DF_Nganh_Metrics_v3` | mới nhất (06-10), 39 steps (vs 37) | cao | `_v2`, base |
| `Daily_Nganh_Report` | `KGR_DF_Daily_Nganh_Report_m` | mới hơn (06-04 vs 06-03) | cao | base |
| `KGR_DS_ACTUAL_AOP_MONTHLY_v2` | **mơ hồ** (nghi `_LK` hoặc `_v3`) | flow tên "v2" chỉ 5 steps (mỏng); v3=21, LK=20 steps dày hơn; dataset ngoài closure 4 wb | thấp | cần owner |
- Giới hạn: last-modified là *thời điểm sửa*, không phải *thời điểm chạy ghi*; OAC API không expose run-history. Muốn chắc 100% → owner xem lịch sử Run trên UI.

## E. Governance findings (số cứng / ước tính — cần owner xác nhận)
- **E1**: a10 (CP xúc tiến bán hàng) = **SỐ CỨNG `247258890.47`** nhúng trong `KGR_DF_Nganh_Metrics_v3`/`KGR_DF_TD_Metrics_bk`. Stale-prone. Có nên thay bằng nguồn động?
- **E2**: a21 (thuế TNDN) = **`a20 × 0.21` cứng**. Thuế suất nên tham số hóa?
- **E3**: các dòng chi phí a6/a7/a8/a15/a16/a17 = **%AOP × Doanh thu**; a10/a12/a18 = **AOP_AMT × ngày/30** → "lợi nhuận" dưới mức gộp là **ƯỚC TÍNH theo AOP, không phải chi phí thực**. Xác nhận đây là chủ đích (P&L kế-hoạch-hóa) hay cần nối chi phí thực (FACT_EXPENSE/JOURNAL)?
