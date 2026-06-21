# Trace playbook — lineage_graph + trace_field.py

## trace_field.py
`cd C:\Project\KGR-OAC-Agents\OAC-Knowledge\skill\kgr-oac-lineage\scripts`
`PYTHONUTF8=1 python trace_field.py "<substring>"`
- Khớp node theo substring (case-insensitive) trong workbook columnID / dataset / dataflow / physical.
- In **downstream** (đi về nguồn tới `physical:`) và **upstream** (ai dùng).
- KB root mặc định = 2 cấp trên thư mục scripts; override bằng env `OAC_KB_ROOT`.

## Trace thủ công (khi cần chính xác cột)
Theo `HOW_TO_TRACE_A_FIELD.md`: workbook field.expression → dataset.column → (dataflow step nếu dataflow_output) → input dataset (đệ quy) → physical_table.

## Impact analysis (đổi X thì gãy gì)
Đi NGƯỢC `lineage_graph.yaml` từ `physical:<TBL>` hoặc `dataset:<X>` → gom mọi `dataflow:`/`dataset:` phụ thuộc → tới `workbook:<slug>/<columnID>` → tra columnID trong `workbook_catalog` để biết viz/canvas nào. Hoặc `trace_field.py "<X>"` (phần upstream).

## Lưu ý granularity
- Edge `dataset:<name> → physical:<TBL>` ở mức DATASET (không kèm cột). Khi trace_field khớp `dataset:<name>/<col>`, để thấy bảng vật lý hãy trace thêm node `dataset:<name>` (không cột) hoặc xem `dataset_catalog.<name>.physical_tables`.
- Qua dataflow, edge ở mức dataset (không lần cột-qua-cột trong flow). Logic cột nằm trong `dataflow_catalog.steps[].adds/aggregations`.

## Verify live (khi nghi ngờ)
- Tồn tại bảng/cột: `executePreview` trên InputDataset step (xem api_extraction) → flowSQL.
- Số: `executePreview` trên OutputDataset step, hoặc MCP `nsaw-analytics` (lưu ý backend có thể cũ).
