# OAC_MODEL_PARSING — Cấu trúc projects/json → canvas / viz / cột

`build_skeleton.py` đã tự động hoá phần này; tài liệu để hiểu & sửa khi gặp viz lạ.

## Top keys
`criteria` (data model: cột + filter) · `views` · `layouts` · `datasources` · ...

## Cột (criteria.columns.children[])
Mỗi cột: `{columnID, type:"saw:regularColumn", columnFormula.expr.expression}`. **Expression** = công thức tại tầng workbook (thường là `XSA('owner'.'dataset')."Columns"."col"` passthrough, hoặc CASE/biểu thức). Display name KHÔNG ở đây — xem header override trong view.

## Views (views.children[])
- `saw:canvas`: `{viewName:"canvas!N", rootLayoutName:"layoutX", viewCaption.caption.text = TÊN CANVAS}`.
- `saw:pluginView`: `{viewName:"view!N", pluginType, viewCaption.caption.text = TÊN VIZ, viewConfig, dataModels}`.
  - pluginType: `oracle.bi.tech.table` (bảng), `...pivot` (pivot), `...canvasfilterviz.listbox` (bộ lọc), `chart...`.

## Canvas → viz (qua layouts)
`layouts.children[]` mỗi layout `{name, children[].content.viewName}`. Canvas.rootLayoutName ↔ layout.name → danh sách viewName trên canvas (đúng thứ tự).

## Viz → cột (dataModels.children[0])
- `edges.children[]` theo `axis`: `row` / `column` / `page` / `section`; mỗi axis `edgeLayers.children[].columnID`.
  - Bảng (table): mọi cột hiển thị nằm ở axis `row`.
  - Pivot: axis `row` = chiều dòng (vd Sort_Order + Metric_Name → các dòng chỉ tiêu); measures ở `logicalEdges.measures` / `measuresList.children[].columnID`.
- **Display header** của cột: `viewConfig.settings."viz:grid".columnHeaderProperty_<columnID>.headerText`. Không có → fallback tên cột.
- **Number format**: `viewConfig.settings."viz:chart".bidvtchart_number_format_<columnID>` → `{style:"percent|decimal", maximumFractionDigits}` (biết "%", số lẻ).

## Báo cáo tổng hợp (pivot summary)
Các "dòng chỉ tiêu" = GIÁ TRỊ của cột dimension trên axis row (vd Metric_Name có 25 giá trị) — KHÔNG phải 25 cột. → rule-book mô tả: (A) các cột giá trị (measures); (B) từng dòng chỉ tiêu (công thức lấy từ dataflow def, map theo Metric_Code).

## Bẫy
- double-JSON khi đọc file (parse 2 lần).
- caption viz đôi khi là HTML (`<p>...`) → strip thẻ.
- caption rỗng → OAC auto-ghép tên các cột (bảng chi tiết) — chấp nhận, đặt tên mô tả.
