# QA_REPORT — toàn diện

PASS=61 FAIL=0 WARN=1  (tổng 62)


## S1
- ✅ `1.1_produced_by_bidirectional`
- ✅ `1.2_df_outputs_exist`
- ✅ `1.3_df_inputs_known`
- ✅ `1.4_used_by_wb_titles`
- ✅ `1.5_closure_reachable`

## S2
- ✅ `2.derive_a9`
- ✅ `2.derive_a4`
- ✅ `2.derive_a20`
- ✅ `2.revenue_roots`
- ✅ `2.cogs_3tier`

## S3
- ✅ `3.trace_match`
- ✅ `3.trace_fd_fallback`
- ✅ `3.trace_nomatch_graceful`
- ✅ `3.find_hub`
- ✅ `3.find_asm`
- ✅ `3.blackboard_roundtrip`
- ✅ `3.lock_contention`

## S4
- ✅ `4.encoding_content_files`

## S5
- ✅ `5.no_cached_money`

## S6
- ✅ `6.contracts_3_agents`
- ✅ `6.contracts_fields`
- ✅ `6.nsaw_backend`
- ✅ `6.bb_template`
- ✅ `6.bb_schema`
- ✅ `6.no_4agent_stray`

## S7
- ✅ `7.physical_count`
- ✅ `7.workbooks_4`
- ✅ `7.lineage_skill_synced`
- ✅ `7.orch_skill_synced`
- ✅ `7.validate_synced`
- ✅ `7.git_OAC-Knowledge_no_secret`
- ✅ `7.git_OAC-Orchestrator_no_secret`
- ✅ `7.git_Dashboard-builder_no_secret`
- ✅ `7.git_Dataflow-builder_no_secret`

## S8
- ✅ `8.validate_kb`
- ✅ `8.qa_tests`

## S9
- ✅ `9.1_typing_closure`
- ⚠️ `9.2_dataflow_output` — 2 no-output (archive cand, OK): ['KGR_DF_SANDBOX_EXPLORE', 'DTF_PRODUCT_KPI_PY']
- ✅ `9.3_physical_complete`
- ✅ `9.4_capability`
- ✅ `9.5_glossary_codes`
- ✅ `9.5b_glossary_src`
- ✅ `9.6_count_consistency`
- ✅ `9.6c_edge_count`
- ✅ `9.6b_counts_regression`
- ✅ `9.7_lineage_terminals`

## S10
- ✅ `10.doc_links_exist`

## S11
- ✅ `11.find_usage`
- ✅ `11.bb_get_missing`
- ✅ `11.lock_status_missing`
- ✅ `11.validate_root_resolve`

## S12
- ✅ `12.precommit_hook`
- ✅ `12.gitignore_rules`
- ✅ `12.secrets_untracked`
- ✅ `12.secret_store_exists`

## S13
- ✅ `13.1_glossary_fd_formula_match`
- ✅ `13.3_type_no_contradiction`
- ✅ `13.5_fd_keys_in_dscat`
- ✅ `13.6_cap_keys_in_dscat`
- ✅ `13.7_archive_doc`
- ✅ `13.8_shown_as_wb_real`
- ✅ `13.9_fd_roots_in_phys`