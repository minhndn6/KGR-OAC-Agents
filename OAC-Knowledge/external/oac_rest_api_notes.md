# OAC REST API cookbook (read-only) — để RE-EXTRACT kho tri thức

Instance: `https://oaxinst70021-id3pgnmhxlya-0p-bo.analytics.ocp.oraclecloud.com`
User: `minhndn@bizin.vn`. Tất cả qua **same-origin browser fetch** từ trang OAC đang mở (MCP `chrome-dashboard` → `evaluate_script`). Bash curl bị proxy chặn.

## Auth & header
- GET: header `{authorization:'session', 'x-requested-with':'XMLHttpRequest'}`, `credentials:'include'`. KHÔNG cần CSRF.
- POST: thêm `x-csrf-token` = `csrftoken` lấy từ `GET /ui/dv/ui/api/v1/sessioninfo` (field `csrftoken`).
- Chưa login → bị redirect IDCS signin: điền `minhndn@bizin.vn` / mật khẩu, Sign In.

## Endpoint dùng (verified 2026-06-20)
1. **Enumerate dataflow + dataset** (toàn instance):
   `GET /ui/dv/ui/api/v1/homepage?maxRowTiles=5000&includeCategory=dataflows&includeCategory=datasources`
   → `searchResults[].searchQueryResults.childItems[]` mỗi item: `type` (dataflow/sequence/dataset/subjectarea), `name`, `owner`, `lastModifiedTime` (epoch ms), `id`, `dataflowId`, `path`.
2. **Workbook model**: `GET /ui/dv/ui/api/v2/projects/json?path=<urlenc '/@Catalog/shared/(KGR) Report/<NAME>'>`
   → `datasources.children[].subjectArea`, `criteria.columns.children[]` (columnID, columnFormula.expr.expression, columnHeading.caption.text), `views.children[]` (saw:canvas + saw:pluginView pluginType/dataModels/viewCaption), `layouts.children[]` (canvas→view qua content.viewName). ⚠ đôi khi double-JSON → parse 2 lần.
3. **Dataflow def**: `GET /ui/dv/ui/api/v1/dataflows?dataFlowID=<urlenc "'owner_or_guid'.'NAME'">`
   → `definition.steps[]`, `definition.links[]`, `definition.DSSDependencies.{inputDatasets,outputDatasets}[].datasetId`, `last-modified`, `object-path`, `version_no`.
   - Step InputDataset: `datasetId`, `datasetType`, `qualifiedTable`, `columns[].name` = `"DW_NS_TABLE"."col"` ⟵ **NGUỒN VẬT LÝ**.
   - Join: joinType/leftDataset/rightDataset/joinOn[{leftColumn,operator,rightColumn}]. GroupBy: groupByColumns[]/aggrColumns[{newName,aggrtype,column}]. AddColumns: columns[{name,expression}]. Filter: filter[{expression}]. Concatenate(Union): leftDataset/rightDataset/concatenateType. OutputDataset: datasetName/customizedColumns[]/datasetDescription.
4. **Dataset metadata (63 dataset)**: `GET /ui/dv/ui/api/v1/dataset/datasets?datasetID=all`
   → `datasets[]`: `datasetId`, `displayName`, `description`, `datamodelProvider.provider-type` (db/...), `dataLastModified`, `folderPath`, `name`, `namespace`. (Param datasetID bị bỏ qua → trả tất cả.)
5. **executePreview (verify live, read-only)**: `POST /ui/dv/ui/api/v1/dataflows/executePreview?stepID=<id>` body `{steps, links, stepId, DSSDependencies}` (lấy từ def) → `flowData[]` (≤30 dòng), `flowSQL` (lộ bảng vật lý thật → set verified_live).

## Endpoint KHÔNG dùng được trên instance này
- `POST /ui/dv/ui/api/v1/dataset/datasets/metadata` → **500** mọi shape body. Thay bằng cách 3 (InputDataset.columns) + 5 (flowSQL).

## Bẫy
- WAF Akamai `_abck` → fetch nhanh liên tiếp có thể 401 HTML: reload trang + giãn nhịp (~150ms/req).
- chrome-dashboard chỉ ghi file trong workspace root của nó (C:\Project\KGR-OAC-Agents\Dashboard-builder) → lưu raw ở `_oac_extract\` rồi copy sang OAC-Knowledge.
- Gỡ kẹt browser THEO PROFILE `profile-dashboard`; KHÔNG kill Chrome toàn cục.

## Pipeline re-extract (tóm tắt)
1. Login → fetch 4 workbook (projects/json) → digest.
2. homepage → enumerate flow+dataset.
3. Loop GET dataflow def (40) → lưu `dataflows_all.json`.
4. GET dataset/datasets?datasetID=all → `datasets_all.json`.
5. Chạy `C:\Project\KGR-OAC-Agents\Dashboard-builder\_oac_extract\build_catalogs.py` → sinh 5 YAML vào OAC-Knowledge.
6. Chạy `skill/kgr-oac-lineage/scripts/validate_kb.py` → phải PASS.
