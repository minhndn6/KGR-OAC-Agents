# HOW TO TRACE A FIELD — từ viz trên dashboard về tận bảng NSAW

Quy trình chuẩn để trả lời: *"Số/field này lấy từ đâu, tính thế nào, gốc bảng nào?"*

## 4 bước
1. **Tìm field trong workbook** → `workbook_catalog.yaml`, mục `workbooks.<title>.canvases[].vizzes[].fields[]`.
   - Mỗi field có `expression` (công thức OAC) và `sources: ["<dataset>.<column>", ...]`.
   - Hoặc nhanh hơn: `python skill/kgr-oac-lineage/scripts/trace_field.py "<tên field>"`.
2. **Mở dataset nguồn** → `dataset_catalog.yaml`, mục `datasets.<dataset>`.
   - Xem `type`:
     - `dataflow_output` → đi bước 3 (lần vào dataflow).
     - `db_dataset` → field tới thẳng bảng vật lý: xem `physical_tables` → **DỪNG ở bước 4**.
3. **Mở dataflow sinh ra dataset** → `dataset_catalog.<dataset>.produced_by_dataflows` → `dataflow_catalog.yaml`, mục `dataflows.<flow>.steps[]`.
   - Tìm step tạo ra cột đó: `AddColumns` (có `expression`), `GroupBy` (aggregation), `Join`, `Filter`.
   - Lấy `input_datasets` của flow → mỗi input lại quay về **bước 2** (đệ quy) cho tới khi gặp `db_dataset`.
4. **Chạm bảng vật lý** → `physical_table_catalog.yaml`, mục `physical_tables.<DW_NS_*>`.
   - Có `columns_in_use`, `verified_live`, và `nsaw_claude_ref.documented_in_nsaw`.
   - **HANDOFF**: cần ngữ nghĩa nghiệp vụ sâu (ý nghĩa cột, công thức canonical, data gap) → mở `C:\Project\NSAW_Claude\data_context\TABLE_CATALOG.yaml` / `QUICK_REFERENCE.md` **NHƯNG** coi đó là tham khảo có-thể-cũ; số/cấu trúc live ở đây thắng (xem `external/README.md`).

## Ví dụ: "Doanh thu" trên DB01 Overview
1. `workbook_catalog.yaml` → DB01 → canvas "Overview" → viz "Revenue & Profit Overview" → field `Revenue` → expression `XSA('anhdk...'.'(KGR) DTF_CALC_INVOICE_MEMO_#')."Columns"."Doanh thu thực tế"` → source `(KGR) DTF_CALC_INVOICE_MEMO_#.Doanh thu thực tế`.
2. `dataset_catalog.yaml` → `(KGR) DTF_CALC_INVOICE_MEMO_#` → type `dataflow_output`, produced_by `(KGR) 1. DTF_CALC_INVOICE_MEMO_#`.
3. `dataflow_catalog.yaml` → `(KGR) 1. DTF_CALC_INVOICE_MEMO_#` → step AddColumns "Doanh thu thực tế" (công thức), InputDataset `1. Invoice_v2` (datasetType db) → physical_tables `DW_NS_CUSTOMER_INVOICE_LINES_F` + `DW_NS_ACCOUNT_D`.
4. `physical_table_catalog.yaml` → `DW_NS_CUSTOMER_INVOICE_LINES_F` (verified_live=true) → cột `BASE_REVENUE/BASE_CREDITAMOUNT/...`. Ngữ nghĩa Revenue canonical (BASE_CR−DB, ACCTTYPE='Income', loại SC=14) → tham khảo NSAW_Claude (verify).

## Impact analysis (chiều ngược)
"Nếu đổi bảng/dataflow X thì viz nào gãy?" → trong `lineage_graph.yaml` đi NGƯỢC edges từ `physical:X` hoặc `dataset:X` lên tới các node `workbook:<slug>/<columnID>`. Hoặc `trace_field.py "X"` (in cả phần upstream consumers).

## Quy tắc handoff sang NSAW_Claude (quan trọng)
- Chạm `physical:DW_NS_*` là **biên** của kho này. Tên bảng + cột đang-dùng là **tươi** (đọc hôm nay).
- Ngữ nghĩa sâu (ý nghĩa business của cột, công thức P&L canonical, sentinel/null, data gap) → NSAW_Claude, nhưng **kho đó ~1 tháng chưa update**. Nếu NSAW_Claude mô tả cột/bảng khác với những gì thấy live ở đây → **tin bản live**, ghi lệch vào `CONFLICTS_AND_OPEN_QUESTIONS.md`.
