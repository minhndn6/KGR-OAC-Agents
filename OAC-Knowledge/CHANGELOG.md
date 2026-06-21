# CHANGELOG — OAC-Knowledge

Format: `- YYYY-MM-DD: [tag] mô tả`. Tag: [wb] [ds] [df] [phys] [lineage] [method] [archive] [skill].

- 2026-06-20: [method] Khởi tạo kho. Trích LIVE từ OAC (read-only) qua chrome-dashboard same-origin fetch. Endpoint dùng: `GET projects/json` (workbook model), `GET homepage?includeCategory=dataflows,datasources` (enumerate), `GET dataflows?dataFlowID=` (def), `GET dataset/datasets?datasetID=all` (63 dataset metadata), `executePreview` (verify live). Endpoint `dataset/datasets/metadata` 500 → bỏ.
- 2026-06-20: [wb] Trích 4 workbook (DB01.Revenue, DB02.Expense, BC01_Daily_Summary, BC03-04-05_SFC_MIS): datasource, 6/n canvas, viz (chart type), 76+ criteria column với expression + dataset.column nguồn. → `workbook_catalog.yaml`.
- 2026-06-20: [df] Trích 40 dataflow (def đầy đủ: steps Join/Aggregate/AddColumns expression/Filter/Union/Output, input→output, version 2.6). → `dataflow_catalog.yaml`. (+2 object `sequence` orchestration ghi nhận riêng.)
- 2026-06-20: [ds] Lập catalog 63 dataset: type (dataflow_output/db_dataset/file), produced_by, used_by_workbooks/dataflows, columns, description, physical_tables. → `dataset_catalog.yaml`. Closure = 30 dataset.
- 2026-06-20: [phys] Trích 60 bảng vật lý NSAW từ `InputDataset.columns` của dataflow (dạng `"TABLE"."col"`) + cột đang dùng + ai dùng. Đối chiếu NSAW_Claude: 40 có / 20 thiếu. → `physical_table_catalog.yaml`.
- 2026-06-20: [phys] verified_live=true cho `DW_NS_CUSTOMER_INVOICE_LINES_F` + `DW_NS_ACCOUNT_D` qua executePreview flowSQL. 58 bảng khác = via_dataflow_def.
- 2026-06-20: [lineage] Dựng `lineage_graph.yaml` (655 edges: workbook→dataset→dataflow→dataset→physical) + terminal physical nodes.
- 2026-06-20: [method] validate_kb.py PASS: 0 ERROR / 0 WARN (514 workbook refs, 139 dataflow refs, 1310 edge endpoints đều resolve).
- 2026-06-20: [archive] `archive_recommendations.md` (deliverable RIÊNG): 10 ARCHIVE / 12 REVIEW / 15 KEEP. Quy tắc: reachability (in_closure) + duplicate-producer, KHÔNG xét tên version. Chỉ khuyến nghị.
- 2026-06-20: [skill] Tạo skill `kgr-oac-lineage` + scripts (trace_field.py, validate_kb.py, decode_double_json.py).
- 2026-06-20: [method] Mốc đồng bộ NSAW_Claude ~2026-05 (có thể cũ). Quy tắc: bản live OAC-Knowledge thắng khi mâu thuẫn. Open questions → CONFLICTS_AND_OPEN_QUESTIONS.md.
- 2026-06-21: [lineage] Recount: `lineage_graph.yaml` hiện **1070 edges / 2140 endpoints** (mở rộng từ 655/1310 ghi nhận 2026-06-20); cập nhật QUICK_REFERENCE. `qa_full` S9.6c nay kiểm số edges trong doc khớp file (chống drift).
- 2026-06-21: [qa] Vá lỗ hổng từ review QA độc lập: (1) `trace_field.py` hiện disclosure GR1/GR3 + non_physical_roots cho field P&L ước tính (trước chỉ a10 có cờ); (2) `qa_full` S2 SKIP tường minh khi thiếu raw extract thay vì FAIL khó hiểu; (3) `qa_full` S13.9 kiểm field_dictionary.physical_roots ⊆ physical_table_catalog; (4) `lock.py` ghi atomic O_EXCL + không steal âm thầm lock hỏng; (5) `blackboard.py` enforce retry max_attempts=3 (escalate khi cạn).

## v3 — consultant brain (2026-06-20, cùng ngày)
- 2026-06-20: [method] Nguyên tắc #1: KHÔNG lưu số (data live). Đã gỡ giá trị tuyệt đối khỏi CONFLICTS. Precedence cứng: OAC>NSAW; báo cáo BC>dashboard DB.
- 2026-06-20: [field] Column resolver (resolver.py): bung mọi field tới gốc qua step DAG + cross-dataflow → field_dictionary.yaml (477 cột, 98% tới bảng vật lý; kèm filters/joins/grain). Fix: cross-df khi InputDataset columns rỗng; ref bare-identifier.
- 2026-06-20: [field] Phát hiện: a6/a7/a8/a15/a16/a17 = %AOP×Doanh thu; a10/a12/a18 = AOP_AMT×ngày/30; a21 thuế ×0.21 → chi phí dưới mức gộp là ƯỚC TÍNH theo AOP, không phải thực. a10 số cứng 247258890.47. (governance_flag)
- 2026-06-20: [field] P&L grounded-in-OAC: a4=DT−a3; a9(LN gộp KD)=a4−a5−a6−a7−a8. Dossier mẫu fields/_FLAGSHIP_LoiNhuanGopKinhDoanh.md.
- 2026-06-20: [method] Drift phân xử (OAC thắng): Revenue=BASE_REVENUE (≠NSAW BASE_CR−DB); ACCTTYPE IN('Income','OthCurrLiab'); loại nội bộ qua subsidiary whitelist. SFC: BC dùng DTF_CALC_MIS > DB dùng SFC_vs_MEMO. → CONFLICTS §D.
- 2026-06-20: [method] flowSQL db-dataset: executePreview đọc cache XSA → KHÔNG lộ join-key/WHERE nội bộ (endpoint metadata 500). Cột vẫn giữ qualifier bảng vật lý. Filter nghiệp vụ nằm ở dataflow (resolver bắt được).
- 2026-06-20: [ds] Thêm grain mỗi dataset (description-stated ưu tiên, else heuristic GroupBy).
- 2026-06-20: [skill] business_glossary.yaml (ontology+precedence+CRITICAL_INSIGHT), capability_map.yaml (metric×dim×grain→nguồn), source_selection_playbook.md (luật+cạm bẫy), live_query_recipes.md (lấy số live+bất biến), fields/*.md (30 dossier). Skill nâng thành consultant + consultation_playbook + find_source.py.
- 2026-06-20: [method] validate_kb.py mở rộng (h: field bottom-out, i: capability resolve, j: no-cached-number) → PASS 0 ERROR/0 WARN.
- 2026-06-20: [qa] Bộ QA khó tính (raw/qa_tests.py, 23 offline + live H1 + script D2/E3 + K1). Bắt & FIX 4 lỗi thật: (1) lineage_graph không đi xuyên (node dataset:<name>/<col> đứt khỏi dataset:<name>) → thêm bridge edge; (2) Metric_Dim lọt physical_roots → lọc DW-only (non_physical_roots); (3) DB01 digest trích bằng regex CŨ làm rớt cột table-qualified (ASM/NET_AMOUNT) → re-trích DB01 chuẩn; (4) external/README thiếu precedence BC>DB → bổ sung. Kết quả: 27/27 PASS.

## Review đầu não + P0/P1 (2026-06-20)
- 2026-06-20: [review] Họp 7 vai (CTO/Dev Lead/DevOps/AI Tech Lead/Data Architect/BA/CFO) đọc thật 3+1 project. Chốt làm P0+P1.
- 2026-06-20: [P0][sec] Mật khẩu OAC redact khỏi 5 file active → con trỏ C:\Project\KGR-OAC-Agents\.secrets\oac.env (gitignored). ⚠️ User cần ROTATE password. git init + .gitignore + pre-commit (validate_kb+qa_tests). Gỡ allowlist chrome-devtools (mâu thuẫn CLAUDE.md). Archive (reversible+manifest): KGR_Dashboard + 4 global skill cũ (oac-implementor/manager/clevel/crosscheck).
- 2026-06-20: [P0][gov] governance_register.md (GR1–GR7); hard-wall AOP (a9/a20 relabel '(mô hình AOP)' + disclosure_required + MANDATORY_DISCLOSURE); precedence ĐỔI sang CÓ ĐIỀU KIỆN (freshness/health), không tuyệt đối.
- 2026-06-20: [P1] field_dictionary bỏ TODO (meaning→glossary); grain thật + loại rác; validator [k] cấm TODO + đếm grain; guardrail re-aggregate (no SUM ratio); customer/ký-gửi dim + AsOfDate/kỳ semantics; JSON output contract; freshness-check recipe; requirements.txt; 2 dossier mẫu + fallback workbook ngoài-4. validate 0 ERROR; qa 23/23.
- 2026-06-20: [open] Còn cho user: rotate password; chốt CONFLICTS F1 (nghĩa 'Kênh nội bộ') + F2 (producer sống) + GR1–GR7. P2 (orchestrator: state object, contract 4 agent, relocate _oac_extract, 1-writer/profile-per-actor) chờ khi dựng orchestrator.
