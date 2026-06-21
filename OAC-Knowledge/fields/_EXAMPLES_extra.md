# Dossier mẫu bổ sung (DB01 Revenue, BC03 SFC) + quy tắc workbook ngoài-4

## VD2 — "Tỷ lệ Xanh/Đỏ" theo Kênh (DB01.Revenue, canvas CHANNEL)
- Viz "Channel Mix — Green vs Red %" (`oracle.bi.tech.chart.horizontalstackbar100`) trên **DB01.Revenue**.
- Field hiển thị: `Green` (columnID) = `CASE WHEN round(DS Xanh*100 / Doanh số thực tế,0) > 100 THEN 100 ELSE round(...) END`; phần Đỏ = 100 − Green.
- Nguồn: **`(KGR) DTF_CALC_INVOICE_MEMO_#`** (hub) → cột `DS Xanh`, `Doanh số thực tế`, `Nhóm xanh đỏ`.
- Bung tới gốc: `DS Xanh` = doanh số dòng có `CSEG_SCV_NHOMXANHDO`=Xanh (date-range hiệu lực) từ `DW_NS_X_CAM_CUSTOMRECORD_CSEG_SCV_NHOMXANHDO` + revenue `DW_NS_CUSTOMER_INVOICE_LINES_F`/`CREDIT_LINES_F`. Chiều Kênh = `DW_NS_X_SALE_CHANNEL`/`DW_NS_X_LIST_SALE_CHANEL_NS`.
- ⚠️ Xanh/Đỏ luôn 1 trong 2 (mặc định Đỏ nếu không match). `Green` là **TỶ LỆ** → đừng SUM khi re-aggregate (tính lại ΣDS Xanh/ΣDoanh số).
- Lấy số: executePreview hub OutputDataset, group theo Kênh. (xem live_query_recipes)

## VD3 — "SFC ước tính vs thực tế" (BC03-04-05 SFC/MIS)
- Workbook **BC03-04-05_SFC_MIS** — combo SL Kế hoạch vs SL Thực tế.
- Nguồn authoritative (báo cáo): **`(KGR) DTF_CALC_MIS`** + **`(KGR) SFC Dataset (có AI)`** (db, nối `DW_NS_X_SFC_*`). DB01 dùng `KGR_DS_SFC_vs_MEMO_v1..v4` (dashboard, ưu tiên thấp hơn — mỗi bản 1 grain).
- SL_Ke_Hoach (forecast) ← SFC tables; SL_Thuc_Te (actual) ← invoice (giống revenue actual). Variance = (TT−FC)/FC.
- ⚠️ SFC Dataset là db_dataset **ít tài liệu nhất** (producer/grain trống, join nội bộ không lộ qua API) dù được chọn authoritative → confidence **vừa**; verify live khi cần số.

## Quy tắc khi hỏi về workbook/field NGOÀI 4 workbook đã trích
KB này chỉ phủ 4 workbook: DB01.Revenue, DB02.Expense, BC01_Daily_Summary, BC03-04-05_SFC_MIS.
- Nếu user hỏi workbook/canvas/field **không có trong workbook_catalog** → NÓI RÕ "ngoài phạm vi KB hiện tại", KHÔNG bịa.
- Cách xử lý: (1) enumerate live `GET projects/json?path=<wb>` để lấy datasources+criteria của workbook đó; (2) map dataset→dataflow→physical bằng dataflow_catalog/physical_table_catalog đã có (đa số dataset dùng chung); (3) nếu cần đầy đủ → đề xuất chạy lại pipeline thêm workbook đó vào closure.
