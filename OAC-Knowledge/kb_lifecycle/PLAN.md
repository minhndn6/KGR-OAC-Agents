# KB Lifecycle — Implementation Plan (TDD-first)

> Theo quy trình owner: test-case TRƯỚC → triển khai → test/fix → UAT loop (≥200) → use thật (≥500) → tối ưu.
> Mỗi task: ID · mô tả · **test trước** · acceptance · rủi ro/rollback. Backward-safe: test cũ (validate_kb, qa_*, test_orchestrator) PHẢI xanh sau mỗi task (AC7).
> Thứ tự = rủi ro thấp → cao (reviewer-1 sequencing). Commit sau mỗi task.

## Bố cục mã (chốt)
- Bộ công cụ mới: `OAC-Knowledge/kb_lifecycle/tools/` (tracked): `kgr_runtime.py`, `kb_route.py`, `check_clean.py`, `kb_kinds.py`, `learn2.py` (nâng cấp), `drift.py`.
- Test: `OAC-Knowledge/kb_lifecycle/tests/` chạy `PYTHONUTF8=1 python tests/run_all.py` (deterministic, offline, dùng tmp ngoài — KHÔNG đụng state thật).
- `kinds.yaml`, `scratch_manifest.txt` (data cho cả gitignore lẫn check_clean).
- Bản sao đông cứng `kgr_runtime.py` → 3 repo còn lại ở Phase 1.4.

---

## PHASE 0 — Foundations (BLOCKER, no behavior change)
**P0.1 — Fix split-brain KB root (INV-1).**
- Test trước: `tests/test_kbroot.py` — giả lập chạy từ `~/.claude/skills/...`; assert resolution KHÔNG rơi vào `C:\Project\OAC-Knowledge` lạ; thiếu marker → fail loud.
- Làm: marker `.kb_root` (hoặc anchor theo `knowledge_map`/`kinds.yaml`) ở workspace KB; `kb_root()` ưu tiên `OAC_KB_ROOT` → marker tìm lên cây → **bỏ hardcoded fallback mù** (raise nếu không thấy). Sửa ở `learn.py` + util chung `kb_paths.py`.
- Acceptance: từ mọi cwd & cả bản cài, resolve đúng workspace KB hoặc fail rõ. AC7 xanh.
- Rủi ro: skill đang chạy gọi learn.py → giữ tương thích chữ ký; chỉ đổi resolution.

**P0.2 — Pin determinism (INV-3, V2/V4).**
- Test trước: `tests/test_determinism.py` — assert `.gitattributes` tồn tại + có rule LF cho yaml/md/py/json; assert không còn `*.pyc/__pycache__` tracked.
- Làm: thêm `.gitattributes` (4 repo); `git rm --cached` file `.pyc`; thêm `__pycache__/`,`*.pyc` vào `.gitignore`.
- Acceptance: test xanh; `git status` sạch; rebuild diff chỉ là nội dung thật.

**P0.3 — Centralize EXTRACT_DATE (chuẩn bị D8).**
- Test trước: `tests/test_extractdate.py` — assert chỉ 1 nguồn EXTRACT_DATE; builder đọc từ đó.
- Làm: đưa EXTRACT_DATE về `raw/extract_manifest.json` (hoặc derive từ extract); 3 builder đọc chung. (Không rebuild rủi ro — chỉ refactor hằng số.)
- Acceptance: build vẫn ra cùng bytes (trừ chỗ ngày); test xanh.

## PHASE 1 — Hygiene (INV-4)
**P1.1 — `kgr_runtime.py` (D9/D10).** Test trước: zero-env default đúng (Windows `%LOCALAPPDATA%` fallback khi unset); `KGR_RUNTIME_DIR` override; durable() vs scratch() khác nhau; tmp cùng volume với target. Làm: module path-resolution thuần.
**P1.2 — `blackboard.py` → durable dir (V5).** Test trước: cập nhật `test_orchestrator.py` set env TRƯỚC import (giữ reassignable global); assert BB ghi vào `<WS>\_orchestration\blackboards`, KHÔNG vào repo; recover vẫn chạy. Làm: `BB_DIR` đọc `kgr_runtime.durable_blackboards()` + env; di dời 14 file hiện có.
**P1.3 — `check_clean.py` + scoped manifest (D11).** Test trước: tạo file scratch giả trong tmp-repo → check FAIL; file curated `_INDEX.md` → PASS (không orphan). Làm: script tracked, iterate 4 repo; sửa `.gitignore` scoped; `git rm --cached` 9 scratch (`_PNL_*`,`_DB01_NOTES_DRAFT`,`_build_heatmap.js`,`_combochip.txt`) → chuyển ra `_work`/durable.
**P1.4 — Entrypoint (D12).** Workspace-root `CLAUDE.md` + `kgr` CLI (`where`/`doctor`) + 1 dòng vào mỗi SKILL/CLAUDE.md. Test: `kgr where` in runtime root + cách route.

## PHASE 2 — Write-routing & anti-rot (INV-2)
**P2.1 — banner emission + one-off stamp + hash (D1/D2).** Test trước: file có banner→generated; sửa body→hash mismatch→guard FAIL; curated có banner→FAIL. Làm: stamp script (KHÔNG rebuild rủi ro) + builder emit banner sau này.
**P2.2 — `kb_route.py` (D4).** Test trước: mọi `--type` (≥12) trả target tồn tại; type lạ→exit≠0; `check-path` đúng kind. Làm: classifier JSON.
**P2.3 — validator extension warn→error (D1).** Test trước: file unclassified→WARN(→ERROR). Làm: nối vào `validate_kb.py`, warn-first.

## PHASE 3 — Self-learning hardening (INV-5/INV-6)
**P3.1 — schema record mới (D5).** content_hash/fact_key/supersedes/attested_by/verify_ref/source. Test: migrate 9 record cũ không vỡ.
**P3.2 — `learn2.py`: dedup + contradiction + supersede + typed gate (D5/D6).** Test trước: trùng→reject; mâu thuẫn→cần supersede; promote thiếu evidence đúng-loại→reject; governance không auto.
**P3.3 — `drift.py` upsert+debounce+storm+auto-resolve (D7/D8).** Test trước (fixture, offline): cùng drift_key→upsert; <2 lần→không emit; >K→bulk; rebuild→resolved_stale. Freshness SLA gate FAIL khi quá hạn.

## PHASE 4 — Validation loop (owner-mandated)
**P4.1 — UAT ≥200 (offline, deterministic).** Sinh corpus use-case "AI cần đọc/ghi/route/học tri thức" + sai-cách-phải-bị-chặn. Chạy → sửa → lặp.
**P4.2 — Mở rộng ≥500 use-case thật.** Lát cần OAC live: DỪNG, chuẩn bị bước login, chờ owner. Phần offline tiếp tục.
**P4.3 — Tối ưu tới hội tụ.** Theo kết quả QA/UAT.

## Acceptance tổng (Definition of Done)
DoD1 split-brain hết (INV-1) · DoD2 100% file phân loại được (INV-2) · DoD3 hash/diff ổn định đa máy (INV-3) · DoD4 repo sạch + cleanliness-test cả 4 repo (INV-4) · DoD5 learn: dedup/contradiction/supersede/typed-gate (INV-5) · DoD6 staleness FAIL ồn (INV-6) · DoD7 ≥200 UAT pass · DoD8 test cũ luôn xanh (AC7) · DoD9 entrypoint để AI lạ tự khám phá.
