# KB Lifecycle — STATUS (loop memory; đọc file này khi tiếp tục)

> "Trí nhớ" của vòng lặp tự động. Mỗi lần thức dậy: đọc file này + PLAN.md → tiếp tục task `NEXT`.
> Spec: `DESIGN_v1_FINAL.md` · Kế hoạch: `PLAN.md`. Quy trình: design→review→chốt→plan→test-first→impl→test→UAT.
> Regression gate sau mỗi task: `PYTHONUTF8=1 python kb_lifecycle/tests/run_all.py --with-legacy` PHẢI xanh.

## Trạng thái: PHASE 0–4(offline) ✅ · **LIVE UAT đang chạy** (oac-native sống)
### LIVE UAT (2026-06-21) — XONG. Bằng chứng: C:\Project\_work\kgr-governance-build\live_uat_report.json
- existence **63/63** live (62 qua discover-list + `DTF_CALC_MIS` qua COUNT=294.294; discover-list THIẾU nó → đã SỬA L0011).
- queryability **17/17** dataset closure (COUNT>0). structure **3/3** P&L core khớp 100% (TD_Metrics_Wide 42/42, PNL_Bridge 9/9, _Nganh 11/11).
- **DoD6 → 🟢 có bằng chứng live.** Bài học (ghi log): discover-list có thể THIẾU → verify existence bằng `COUNT(*)` qua XSA.
- column-level: **328/477 cột verify live từng cái** (0 fail); **149 cột tiếng Việt KHÔNG verify được** (oac-native transport double-encode non-ASCII — bug, ghi log) → corroborate qua count-match+queryability.
- **TỔNG VALIDATION = 620 case** (209 offline + 411 live), all pass. KHÔNG dùng nsaw-oac-poc.

## (cũ) PHASE 0–4 offline · UAT 209 PASS
Cập nhật: 2026-06-21. **run_all --with-legacy = 15/15 ✅** · UAT 209/0 FAIL/0 GAP · REPORT.md xong.
Phần còn lại đều cần owner: G1 ký GR · G2 token (drift live + UAT ≥500) · `gh auth login` để push GitHub.
(File Phase 4 — run_uat.py/uat_cases.jsonl/REPORT.md — đang UNCOMMITTED; sẽ commit+push 1 lần khi owner auth.)

### Đã xong
- [x] Định hướng + Design v0 → 3 sub-agent adversarial review → chốt `DESIGN_v1_FINAL.md` (D1–D12, INV-1..6).
- [x] `PLAN.md` (Phase 0→4, TDD-first), test runner `tests/run_all.py`.
- [x] **P0.1 split-brain KB root** — `kb_paths.py` + marker `.kgr_kb_root` + registry; sửa `learn.py` (bỏ fallback mù) + sync `~/.claude`. `test_kbroot` 7/7. Cả 2 bản resolve đúng workspace KB.
- [x] **P0.2 determinism** — `.gitattributes` (LF) 4 repo; untrack `.pyc`; gitignore `__pycache__`. `test_determinism` 16/16.
- [x] **P1.1 kgr_runtime** — `tools/kgr_runtime.py`: tách DURABLE (`_orchestration`, in-backup) vs EPHEMERAL (`%LOCALAPPDATA%/kgr-oac/runtime`), env-contract + zero-env default, `scratch()/atomic_write()`, self-locating workspace. `test_runtime` 16/16.
- [x] **P1.2 blackboard relocation** — BB_DIR → `<WS>/_orchestration/blackboards`; di dời 16 file. `test_hygiene`.
- [x] **P1.3 check_clean** — `tools/check_clean.py` + `clean_rules.json` (scoped, KHÔNG blanket `_*.md`); chạy 4 repo. Đã `git rm --cached` 9 file scratch ở Dashboard-builder + gitignore scoped → 4 repo SẠCH. `test_clean` (unit + regression).
- [x] **P1.4 entrypoint** — workspace `CLAUDE.md` (parent chung, AI auto-đọc) + `tools/kgr.py` CLI (`where`/`doctor`/`setup`/`route`). `kgr doctor` = STATUS OK. `test_entrypoint` 14/14.
- [x] **P2.2 kb_route** — `tools/kb_route.py` classifier 14 type (owner goal #1): `classify`/`check-path`/exit≠0 type lạ; `kgr route` ủy quyền. `test_route` 33/33.
- [x] **P2.1/2.3 classify + anti-edit guard** — `kinds.yaml` + `tools/kb_kinds.py` (35 GENERATED / 18 CURATED / 2 LOG, **0 unclassified**) + `tools/guard_generated.py` (hash-manifest `generated_manifest.json`; bắt hand-edit GENERATED, chừa CURATED). `kb_route.check_path` → kb_kinds. `test_guard` 14/14. **QĐ kỹ thuật (owner review)**: dùng HASH-MANIFEST sidecar thay vì stamp banner vào file lớn (tránh churn 13k-dòng field_dictionary; refresh sau rebuild = re-bless; mạnh tương đương hash-in-banner).

### Đã xong PHASE 3 (một phần)
- [x] **P3.1 schema+migrate** — `tools/learn2.py` (riêng, KHÔNG đụng learn.py skill): `content_hash`+`fact_key`+`supersedes`/`superseded_by`. Migrate 10 record log THẬT (backup scratch `learn-migrate/`). `test_learn2`.
- [x] **P3.2 dedup+contradiction+supersede** — add dedup theo content_hash (rejected_dup); `find_contradictions` (cùng fact_key khác nội dung); `supersede` (append+lật trạng thái, audit, KHÔNG xóa; chặn chéo fact_key). `test_learn2` 16/16.
- [x] **P3.3 typed promote-gate** — `learn2.promote(id, evidence)` theo D6, KHỚP `kb_route` gate + consistency-check (mọi type kb_route có quyết định). governance KHÔNG auto/second-agent; gap KHÔNG promote; contradiction chặn tới khi supersede. `test_gate` 31/31.
- [x] **P3.4 drift store** — `tools/drift.py`: lọc ts hợp lệ (bỏ đúng 99 connector), drift_key+upsert, debounce ≥N, cooldown/suppress, storm-breaker (>K→bulk), auto-resolve. State durable. `test_drift` 15/15. Fixture xác nhận KB 0-drift sau 2026-06-21.

### NEXT (theo thứ tự)
1. **PHASE 4 — UAT ≥200 (offline, deterministic)**. Tạo `tests/uat/uat_cases.jsonl` + `tests/uat/run_uat.py` (run_all đã tự-discover). Mỗi case = {situation, action(route/check-path/promote/clean/drift), input, expected}. Phủ:
   - route: 14 type → kind/write_via đúng; type lạ → reject.
   - check-path: ~55 file KB thật + synthetic → kind đúng (oracle ĐỘC LẬP, không vòng tròn).
   - **negative "sai chỗ bị chặn"** (nhiều): hand-edit GENERATED→guard MODIFIED; scratch vào repo→check_clean DIRTY; promote thiếu evidence→reject; promote gap→reject; governance auto→reject; dup add→rejected_dup; supersede chéo→block.
   - learn gate per type (valid/invalid). drift scenarios.
   Mục tiêu ≥200 case PASS, GAP=0. Rồi mở rộng ≥500 (phần cần live → chờ owner G2).
2. (Sau UAT) Tổng kết DoD1–DoD9, viết REPORT cho owner.

### Ràng buộc (đừng vi phạm)
- KHÔNG đụng/đăng nhập OAC/NSAW (chỉ đọc). KHÔNG O2. Live-probe chỉ interface+fixture tới khi owner login.
- Backward-safe: run_all --with-legacy xanh sau mỗi task. Scratch tôi: `C:\Project\_work\kgr-governance-build`. **Đã chuyển MONOREPO + commit (owner duyệt đẩy GitHub)**; loop tự-động cứ để file mới uncommitted — commit/push làm ở phiên tương tác.

### GitHub & monorepo (2026-06-21)
- **ĐÃ GỘP MONOREPO**: xóa 4 .git con → 1 git repo ở workspace root. 2 commit (baf14da init, 447e0e6 utf-8). 201 file tracked, **secret-free** (verify HEAD). Remote `origin=https://github.com/minhndn6/KGR-OAC-Agents.git`.
- **CHƯA push** — chờ owner `gh auth login` (gh chưa cài). Sau auth: `git push -u origin main`.
- Tooling thành monorepo-aware: `check_clean.repos_to_scan/scan_all` (quét root repo), `qa_full` S12 hook-check (root .git/hooks), pre-commit hook gốc chạy check_clean.
- Secrets: `.secrets/` gitignored; đã redact "Hanoi@20"→"Hanoi@**" trong log L0005. Khuyến nghị owner ĐỔI mật khẩu OAC + đặt repo Private.

### Gate cần owner
- **G1** ký GR1–GR7 (rủi ro tài chính: AOP-as-actual, thuế cứng 0.21, hằng số 247tr, whitelist 2 pháp nhân) → chặn promote governance auto. CHƯA.
- **G2** ⚠️ token MCP VẪN hết hạn (owner refresh chưa tới `tokens.json` MCP đọc). Kênh browser OK cho live read. UAT live/≥500 + drift probe thật chờ cái này.
- **G3** runtime root default `%LOCALAPPDATA%\kgr-oac` — owner xác nhận? · **G4** xóa scratch khỏi git history? (monorepo init mới nên history đã sạch — G4 gần như moot).
- **G5** ✅ XONG: giữ 5 `_PNL_*` + `_DB01_*`/`_build_heatmap`/`_combochip` untracked; `_PNL_BUILD_STATE.md` đã DỜI → `_orchestration/build_state/dashboard_PNL_BUILD_STATE.md` (durable).

### Live capture & design refinements (2026-06-21, owner đã login OAC)
- Kênh đọc live = browser same-origin fetch GET (read-only). MCP tokens.json HẾT HẠN (~33 ngày) → refresh nếu cần kênh scriptable.
- Fixture: `C:\Project\_work\kgr-governance-build\oac_freshness_2026-06-21.json` (203 asset). **KB ĐỒNG BỘ: 0 dataflow/dataset đổi sau extract 2026-06-20.**
- REFINEMENT D7/D8: 99/203 datasource thiếu `lastModifiedTime` → drift-sensor PHẢI lọc ts hợp lệ (L0010 pending).

### Log mốc
- 2026-06-21: design→review→chốt→plan. Phase 0 done. P1.2 blackboard relocation. run_all 6/6.
- 2026-06-21: owner login OAC → chụp freshness fixture read-only; KB 0-drift; dogfood learn.py L0010 (validate P0.1).
- 2026-06-21: P1.1 kgr_runtime (16/16) + P1.3 check_clean (untrack 9 scratch, 4 repo sạch). run_all 8/8.
- 2026-06-21: P1.4 entrypoint (workspace CLAUDE.md + kgr CLI, doctor=OK, 14/14) + P2.2 kb_route (14 type, 33/33). **run_all 10/10**. PHASE 1 hoàn tất.
- 2026-06-21: P2.1/2.3 classify (kinds.yaml + kb_kinds, 0 unclassified) + anti-edit guard (guard_generated hash-manifest 35 file, test_guard 14/14) + kb_route check_path→kb_kinds. **run_all 11/11**. PHASE 2 hoàn tất.
- 2026-06-21: P3.1+3.2 learn2 (content_hash/fact_key/dedup/contradiction/supersede, test 16/16) + migrate log thật (10 record, backup scratch). **run_all 12/12**.
- 2026-06-21: P3.3 typed promote-gate (test_gate 31/31) + P3.4 drift store (test_drift 15/15, lọc 99 no-ts, debounce/storm/auto-resolve). **run_all 14/14**. PHASE 3 hoàn tất.
- 2026-06-21: GỘP MONOREPO (xóa 4 .git con, init root) + 2 commit, remote GitHub set, secret-free. G5 xong (dời BUILD_STATE). Tooling monorepo-aware. run_all 14/14. Chờ owner gh auth để push.
- 2026-06-21: PHASE 4 UAT — `tests/uat/run_uat.py` + corpus 209 case (route/check_path/negative/gate/guard/drift), oracle độc lập. **209 PASS / 0 FAIL / 0 GAP**. run_all 15/15. REPORT.md (DoD1–9). **LOOP DỪNG**, báo cáo owner.
- 2026-06-21: ✅ ĐÃ PUSH GitHub (origin/main=2621c05, 4 commit, 205 file, **secret-free verified**). Auth qua Git Credential Manager (creds cached). Lần sau push trực tiếp được. Chờ owner: G1 ký GR · G2 token (UAT≥500 live + drift live) · đặt repo Private + đổi mật khẩu OAC.
