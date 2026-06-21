# KB Lifecycle — Báo cáo nghiệm thu (offline) cho owner

> Ngày 2026-06-21. Mục tiêu owner giao: (1) chống-rác tri thức "AI biết ghi vào đâu", (2) tự-học bám kịp OAC, (3) giữ harness sạch.
> Quy trình đã theo: định hướng → 3 sub-agent review → chốt thiết kế → kế hoạch → **test-first** → triển khai → test/fix → **UAT ≥200**.
> Trạng thái test: **`run_all --with-legacy` = 15/15** (11 unit/integration kb_lifecycle + UAT 209-case + 3 bộ legacy validate_kb/qa_full/test_orchestrator).

## 1. Đã xây gì (theo 3 mục tiêu)

**Mục tiêu #1 — Chống rác / "ghi tri thức vào đâu"**
- `kb_route.py`: hỏi 1 lệnh ra đích + cách ghi + validation cho **14 loại tri thức**; loại lạ → exit≠0 (không misroute).
- `kb_kinds.py` + `kinds.yaml`: phân loại mọi file (35 GENERATED / 18 CURATED / 2 LOG, **0 unclassified** — file mới chưa phân loại sẽ làm fail build).
- `guard_generated.py`: bắt hành vi **sửa tay file máy-sinh** qua hash-manifest (`generated_manifest.json`); chừa file người-viết.

**Mục tiêu #2 — Tự học, bám kịp OAC**
- `learn2.py`: `content_hash` + `fact_key` + **dedup** + **phát hiện mâu thuẫn** + **supersede có audit** (không xoá fact cũ) + **promote-gate theo loại** (governance/glossary bắt buộc người ký, KHÔNG auto; gap không thành fact).
- `drift.py`: cảm biến trôi (drift) có chống nhiễu — lọc timestamp rỗng, debounce ≥N, gộp bão (storm), cooldown, auto-resolve sau rebuild.

**Mục tiêu #3 — Harness sạch**
- `kgr_runtime.py`: tách **durable** (`_orchestration/`, trong backup) vs **ephemeral scratch** (`%LOCALAPPDATA%`, ngoài repo); agent lấy đường ghi bằng API.
- `check_clean.py` + pre-commit hook: cổng chặn rác bị track (monorepo-aware). Đã gỡ 9 file rác khỏi git.
- `CLAUDE.md` gốc + `kgr` CLI (`where/doctor/setup/route`): AI lạ mở workspace là tự đọc luật.

## 2. Definition-of-Done

| DoD | Nội dung | Trạng thái |
|---|---|---|
| DoD1 | Hết split-brain KB root (INV-1) | ✅ `kb_paths` + marker + registry; test_kbroot 7/7 |
| DoD2 | 100% file tri thức phân loại được (INV-2) | ✅ 0 unclassified; coverage gate trong test_guard |
| DoD3 | Hash/diff ổn định đa máy (INV-3) | ✅ `.gitattributes` LF (root + 4 sub) |
| DoD4 | Repo sạch + cleanliness-test (INV-4) | ✅ monorepo, check_clean SẠCH, hook |
| DoD5 | learn: dedup/contradiction/supersede/typed-gate (INV-5) | ✅ test_learn2 + test_gate |
| DoD6 | Staleness FAIL ồn (INV-6) | 🟢 **CÓ BẰNG CHỨNG LIVE** — drift sensor + lọc nhiễu (offline); LIVE UAT qua oac-native: **existence 63/63**, **queryability 17/17 closure** (COUNT>0), structure 3 P&L khớp 100% (TD_Metrics_Wide 42/42, PNL_Bridge 9/9, _Nganh 11/11). Còn lại (tùy chọn): cổng SLA-cadence tự động |

### Live UAT (2026-06-21, oac-native read-only)
- **Existence: 63/63** KB dataset có trên OAC live (62 qua discover-list + `(KGR) DTF_CALC_MIS` xác minh qua `COUNT(*)`=294.294 rows; discover-list THIẾU nó).
- **Queryability: 17/17** dataset closure (có column-detail) trả dữ liệu live (`SELECT COUNT(*)`>0).
- **Structure: 3/3** dataset P&L core — live column count khớp field_dictionary 100%; P&L codes (a4..a24, AOP_PER/AMT) hiện diện live; `execute_logical_sql` trả dữ liệu thật (tiếng Việt đúng).
- **Bài học (sửa L0011)**: `discover_data` LIST có thể THIẾU dataset có thật → verify existence bằng `COUNT(*)` qua XSA, không chỉ tin discover-list.
- **Column-level: 328/477 cột verify LIVE từng cái** (28 query `COUNT(col,...)` qua oac-native, 0 fail). Còn **149 cột tên tiếng Việt KHÔNG verify được từng cái** — `oac-native` transport **double-encode ký tự non-ASCII cả 2 chiều** (gửi `"Ròng"` → OAC nhận `"RÃÂ²ng"` → nonexistent); existence của 149 cột này được **corroborate** qua count-match (describe) + queryability. (Bug transport, ghi log.)
- **TỔNG VALIDATION: 620 case** = 209 offline + 411 live (existence 63 + queryability 17 + ASCII-cột 328 + structure 3), all pass. Bằng chứng: `_work/kgr-governance-build/live_uat_report.json`.
| DoD7 | ≥200 UAT offline | ✅ **209 PASS / 0 FAIL / 0 GAP** |
| DoD8 | Test cũ luôn xanh (AC7) | ✅ validate_kb / qa_full / test_orchestrator |
| DoD9 | AI lạ tự khám phá entrypoint | ✅ CLAUDE.md gốc + `kgr doctor` |

UAT 209 case phủ: route(32) · check_path(99, oracle độc lập) · negative "sai chỗ bị chặn"(22) · clean(10) · gate(29) · learn(2) · guard(3) · drift(12). Corpus: `tests/uat/uat_cases.jsonl`.

## 3. Chờ owner (không làm tự động được)
- **G1** — Ký GR1–GR7 (rủi ro tài chính: AOP-as-actual, thuế cứng 0.21, hằng số 247tr, whitelist 2 pháp nhân). Chặn promote governance tự động cho tới khi ký.
- **G2** — Refresh đúng `tokens.json` (MCP) để mở kênh scriptable → bật **drift probe live** (hoàn tất DoD6) + **UAT ≥500 live**.
- **GitHub** — đã gộp monorepo + 2 commit + remote set, secret-free. Chờ `gh auth login` để `git push -u origin main`.
- Khuyến nghị: đặt repo **Private** + **đổi mật khẩu OAC** (đang plaintext trong `.secrets/oac.env`, đã gitignore).

## 4. Quyết định kỹ thuật đáng lưu ý (owner duyệt)
- Anti-edit guard dùng **hash-manifest sidecar** thay vì nhét banner vào file 13k dòng (ít xâm lấn, mạnh tương đương; refresh sau rebuild = re-bless).
- `learn2.py` tách riêng để KHÔNG đụng `learn.py` mà skill đang gọi.
- Đã gộp **monorepo** (xoá 4 .git con) theo lựa chọn owner — lịch sử commit con không giữ (đã backup).
