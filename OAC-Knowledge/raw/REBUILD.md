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
# ── BẮT BUỘC khi RE-EXTRACT (không chỉ rebuild tại chỗ): preserve tri-thức-người ──
python merge_curated_fields.py --prior <field_dictionary CŨ> --fresh <fresh> --out field_dictionary.yaml --preserve-meta --ph-catalog physical_table_catalog.yaml
python merge_curated_fields.py --prior <dataset_catalog CŨ>   --fresh <fresh> --out dataset_catalog.yaml   --ph-catalog physical_table_catalog.yaml
python ../OAC-Knowledge/skill/kgr-oac-lineage/scripts/validate_kb.py   # phải 0 ERROR
python qa_tests.py            # 25/25 PASS
python qa_full.py             # 62/62 (WARN=0)
```

## ⚠️ RE-EXTRACT làm MẤT tri-thức-người → PHẢI merge-preserve + bump fixtures (xem memory `catalog-rebuild-distill-gap`)
Distill fresh KHÔNG tái tạo được: **grain / _meta / internal_joins_filters** (prose người-biên) và **db_dataset `physical_tables`** (endpoint metadata OAC trả **500** trên instance này — giới hạn vĩnh viễn). `merge_curated_fields.py` carry chúng từ catalog đời-trước:
- `--ph-catalog` **BẮT BUỘC**: reconcile physical_tables carried theo PH-catalog fresh, bỏ bảng đã đổi tên/bỏ live (nếu không → validate_kb "unknown table").
- db_dataset mới không-prior → fill note 500-disclosure (không bịa); grain suy theo analog, **owner xác nhận**.
- **Bump count-fixtures** khi ds/df count đổi (refresh hợp lệ): `qa_full.py` (9.6b) · `qa_tests.py` (I3) · `QUICK_REFERENCE.md` (dòng "Quy mô" + lineage edge + ngày verified). Đều có comment "cập nhật khi refresh".
- Lịch sử: ⑥ 2026-07-06 apply (2ded16a+2b2a6cd+d30f5ba): 40/63→36/67 df/ds.

## Re-extract raw từ OAC (khi cấu trúc đổi — freshness probe báo stale)
Theo `OAC-Knowledge/external/oac_rest_api_notes.md`: login OAC (chrome-dashboard) → fetch projects/json (4 wb) + homepage enumerate + 40 dataflow def + datasets?datasetID=all → lưu vào staging raw → chạy pipeline trên.

## Nguồn raw cần có (trong staging)
`raw/dataflows_all.json`, `raw/datasets_all.json`, `raw/catalog_enumeration.json`, `digest/*.json`, `dataflows_steps.json`, `dataflows_digest.json`, `physical_mapping.json`, `closure_datasets.json`, `dbdataset_flowsql.json`.
