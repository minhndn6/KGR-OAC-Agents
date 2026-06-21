# KNOWLEDGE INDEX — KGR OAC Data Lineage

> Đọc `QUICK_REFERENCE.md` trước. Nếu chưa đủ → dùng Topic Map dưới để biết mở file nào, mục nào.

## File summaries
| File | Định dạng | Nội dung | Khi nào đọc |
|---|---|---|---|
| **QUICK_REFERENCE.md** | MD | Tổng quan 4 wb, dataset hub, sơ đồ tầng, quy mô, bẫy | LUÔN đọc đầu tiên |
| **workbook_catalog.yaml** | YAML | 4 wb → canvas → viz (chart type) → field (expression) → dataset.column nguồn; datasource used/unused | Cần biết viz nào dùng gì, hoặc field hiển thị tính từ đâu |
| **dataset_catalog.yaml** | YAML | 63 dataset: type, produced_by, used_by_workbooks/dataflows, columns, physical_tables, description | Cần biết 1 dataset: ai sinh, ai dùng, cột gì, gốc bảng nào |
| **dataflow_catalog.yaml** | YAML | 40 dataflow: steps đầy đủ (Join/Aggregate/AddColumns expression/Filter/Union/Output), input→output, in_closure | Cần biết 1 dataflow biến đổi/ tính toán thế nào |
| **physical_table_catalog.yaml** | YAML | 60 bảng vật lý NSAW: cột đang dùng, dataset/dataflow dùng, có trong NSAW_Claude không | Cần biết field gốc ở bảng/cột NSAW nào (TẦNG NỀN tự chứa) |
| **lineage_graph.yaml** | YAML | Edge list traversable: workbook→dataset→dataflow→dataset→physical | Trace tự động / impact analysis |
| **field_dictionary.yaml** | YAML | ⭐ CẤP CỘT: mỗi field (477) → công thức trực tiếp → bung tới bảng vật lý + filter/join + grain + governance_flag. NO số | "Field này = cái gì trừ cái gì, loại trừ gì, gốc đâu" |
| **fields/*.md** + `_FLAGSHIP_*` | MD | Dossier từng dataset (giải thích mọi cột) + ví dụ mẫu LN gộp KD | Đọc người, theo dataset |
| **business_glossary.yaml** | YAML | ⭐ Ontology nghiệp vụ grounded-in-OAC: a1–a20 P&L, revenue/COGS/GP/CKKM/Xanh-Đỏ/AOP/SFC + dimension; authoritative source + confidence + CRITICAL_INSIGHT | Nghĩa nghiệp vụ + nguồn chuẩn của metric |
| **capability_map.yaml** | YAML | ⭐ metric×dimension×grain → dataset cấp được (by_metric/by_dimension/datasets) | "Cần M theo D lấy đâu" |
| **source_selection_playbook.md** | MD | ⭐ Luật tư vấn "tính/dựng X từ đâu", reuse-vs-build, cạm bẫy "30 năm" | Tư vấn cho dashboard/dataflow-builder |
| **live_query_recipes.md** | MD | Lấy SỐ live + bất biến quan hệ + freshness-check (KHÔNG cache số) | Khi cần số hiện tại |
| **governance_register.md** | MD | ⚠️ GR1–GR7: rủi ro chính trực TC (AOP-estimate, số cứng a10/thuế, whitelist subsidiary, drift NSAW, producer chưa chắc) — cần owner ký | Khi đụng lợi nhuận/CP/audit |
| **OWNER_TODO.md** | MD | Việc chờ owner (rotate password, chốt producer, ký GR) + điều kiện bật O2 | Khi user xử lý phần của mình |
| **fields/_FLAGSHIP_* / _EXAMPLES_extra** | MD | Dossier mẫu end-to-end (LN gộp KD, DB01 Xanh/Đỏ, BC03 SFC) + rule workbook ngoài-4 | Học cách trace/tư vấn |
| **HOW_TO_TRACE_A_FIELD.md** | MD | Quy trình 4 bước trace + ví dụ + quy tắc handoff sang NSAW | Khi cần lần 1 field tới gốc |
| **CONFLICTS_AND_OPEN_QUESTIONS.md** | MD | Mâu thuẫn, giả định, câu hỏi chờ user trả lời | Khi gặp số liệu/nguồn nghi ngờ |
| **archive_recommendations.md** | MD | (RIÊNG) dataflow nên archive + bằng chứng | Khi dọn dataflow rác — KHÔNG phải tri thức lõi |
| **external/README.md** | MD | Hợp đồng cross-KB + quy tắc freshness với NSAW_Claude | Khi cần ngữ nghĩa bảng vật lý / khi mâu thuẫn |
| **CHANGELOG.md** | MD | Nhật ký build/verify | Khi cần lịch sử |
| **skill/kgr-oac-lineage/** | skill | Skill sub-agent + scripts (trace_field.py, validate_kb.py) | Khi project chạy như agent |
| **raw/** | JSON | Dump API gốc (provenance, regenerate được) | Khi cần re-distill, không authoritative |

## Topic Map — "Cần biết… → đọc…"
| Cần biết | File | Khóa/mục |
|---|---|---|
| Viz/field trên dashboard tính từ công thức nào | `workbook_catalog.yaml` | `workbooks.<title>.canvases[].vizzes[].fields[].expression` + `.sources` |
| Canvas nào có những viz gì | `workbook_catalog.yaml` | `workbooks.<title>.canvases[].vizzes[]` |
| Datasource nào của wb KHÔNG được dùng | `workbook_catalog.yaml` | `datasources[].used=false` |
| Dataset X do dataflow nào sinh ra | `dataset_catalog.yaml` | `datasets.<X>.produced_by_dataflows` |
| Dataset X được workbook/dataflow nào dùng | `dataset_catalog.yaml` | `used_by_workbooks` / `used_by_dataflows` |
| Dataset X có cột gì (workbook dùng) | `dataset_catalog.yaml` | `columns_used_by_workbooks` |
| Dataset X gốc bảng vật lý nào | `dataset_catalog.yaml` | `physical_tables` (nếu db_dataset) hoặc lần qua `produced_by_dataflows` |
| Dataflow Y join/aggregate/tính cột thế nào | `dataflow_catalog.yaml` | `dataflows.<Y>.steps[]` |
| Dataflow Y đọc từ bảng vật lý nào | `dataflow_catalog.yaml` | `steps[].physical_tables` (ở step InputDataset) |
| Bảng vật lý T cột nào đang dùng, ai dùng | `physical_table_catalog.yaml` | `physical_tables.<T>.columns_in_use` / `used_by_*` |
| Bảng T có trong NSAW_Claude không | `physical_table_catalog.yaml` | `physical_tables.<T>.nsaw_claude_ref.documented_in_nsaw` |
| Field → tận gốc bảng NSAW | `HOW_TO_TRACE_A_FIELD.md` + `lineage_graph.yaml` | trace_field.py |
| Nếu đổi bảng/dataflow X thì viz nào gãy (impact) | `lineage_graph.yaml` | walk ngược edges |
| Công thức nghiệp vụ canonical (Revenue/COGS/Xanh-Đỏ/AOP/SFC) | `external/README.md` → NSAW_Claude | `NSAW_Claude/data_context/QUICK_REFERENCE.md` (⚠ verify freshness) |
| Dataflow nào nên archive | `archive_recommendations.md` | toàn file |
| Vì sao số/nguồn nghi ngờ | `CONFLICTS_AND_OPEN_QUESTIONS.md` | toàn file |

## Quy trình AI cập nhật knowledge (khi học fact mới)
- Field/viz mới trên workbook → cập nhật `workbook_catalog.yaml` + nếu đổi lineage → `lineage_graph.yaml`.
- Dataset/dataflow mới hoặc đổi logic → `dataset_catalog.yaml` / `dataflow_catalog.yaml` (chạy lại builder `_oac_extract/build_catalogs.py` nếu re-fetch raw).
- Bảng vật lý mới phát hiện → `physical_table_catalog.yaml`.
- Mâu thuẫn/giả định mới → `CONFLICTS_AND_OPEN_QUESTIONS.md` + 1 dòng `CHANGELOG.md`.
- **Nguyên tắc**: mọi fact quan trọng → ≥1 dòng trong `CHANGELOG.md` (kèm ngày verify).
- **Re-extract toàn bộ**: chạy lại pipeline trong `skill/.../references/api_extraction.md` (fetch raw) → `build_catalogs.py` → `validate_kb.py`.
