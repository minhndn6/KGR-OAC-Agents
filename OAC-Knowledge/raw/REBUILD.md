# REBUILD — tái dựng OAC-Knowledge từ raw (reproducible)

Pipeline Python (deterministic) sinh các catalog YAML từ raw JSON. Chạy với `PYTHONUTF8=1 PYTHONIOENCODING=utf-8`.

## Vị trí (hiện tại)
- **Staging đang hoạt động**: `C:\Project\KGR-OAC-Agents\Dashboard-builder\_oac_extract\` (chứa scripts + raw JSON + digest). Scripts có `STG=...\_oac_extract`, `OUT=...\OAC-Knowledge`.
- **Bản backup**: `C:\Project\KGR-OAC-Agents\OAC-Knowledge\raw\` (raw JSON + bản copy các .py). ⚠️ P2 còn lại: relocate staging về đây + sửa path để self-contained (xem OAC-Orchestrator/ORCHESTRATION_DESIGN §6).

## Thứ tự chạy (từ thư mục staging)
```
python build_catalogs.py     # 5 catalog: workbook/dataset/dataflow/physical/lineage
python field_dict_build.py    # field_dictionary.yaml (resolver: công thức→gốc, no số)
python p2_grain_compose.py    # grain + db-dataset composition
python capability_build.py    # capability_map.yaml + fields/*.md
python ../OAC-Knowledge/skill/kgr-oac-lineage/scripts/validate_kb.py   # phải 0 ERROR
python qa_tests.py            # 23/23 PASS
```

## Re-extract raw từ OAC (khi cấu trúc đổi — freshness probe báo stale)
Theo `OAC-Knowledge/external/oac_rest_api_notes.md`: login OAC (chrome-dashboard) → fetch projects/json (4 wb) + homepage enumerate + 40 dataflow def + datasets?datasetID=all → lưu vào staging raw → chạy pipeline trên.

## Nguồn raw cần có (trong staging)
`raw/dataflows_all.json`, `raw/datasets_all.json`, `raw/catalog_enumeration.json`, `digest/*.json`, `dataflows_steps.json`, `dataflows_digest.json`, `physical_mapping.json`, `closure_datasets.json`, `dbdataset_flowsql.json`.
