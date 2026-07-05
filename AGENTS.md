# AGENTS.md — luật tối thiểu cho MỌI AI agent trong KGR-OAC-Agents

> Bản rút gọn cho tool đọc `AGENTS.md`. Luật đầy đủ: **`CLAUDE.md`** (cùng thư mục). Cơ chế: `OAC-Knowledge/kb_lifecycle/`.

## 1. KHÔNG ghi scratch/state vào cây project — ghi RA NGOÀI
File tạm nằm trong cây → agent crawl vào đọc → **đốt token**. Lấy đường ghi bằng API (`python OAC-Knowledge/kb_lifecycle/tools/kgr.py where`), đừng hardcode:

| Loại | API | Vị trí (NGOÀI cây) |
|---|---|---|
| Scratch "giữ lại được" (thay `_work/`) | `kgr_runtime.work_dir("<repo>")` | `C:\Project\_kgr-state\work\<repo>\` (in-backup) |
| State bền (resume/blackboard/lock) | `kgr_runtime.blackboards_dir()/locks_dir()` | `C:\Project\_kgr-state\orchestration\` (in-backup) |
| Scratch tạm (xóa được) | `kgr_runtime.scratch("ten")` | `%LOCALAPPDATA%\kgr-oac\runtime\` (ngoài backup) |

**TUYỆT ĐỐI KHÔNG** tạo `_work/`, `_orchestration/`, `_PNL_*.md`, dump/screenshot trong cây. File có banner `# GENERATED` (hoặc trong `generated_manifest.json`) → **đừng sửa tay** (sửa nguồn `raw/` rồi rebuild). *(Ngoại lệ: `OAC-Knowledge/_work/staging/` là input pipeline, giữ trong cây.)*

**Đã tự động ép** (Claude Code): PreToolUse guard DENY ghi-sai · Stop gate chặn kết thúc khi còn rác · git pre-commit chặn commit bẨN · deny-Read chặn crawl. Tool khác: tự chạy `check_clean.py --strict` + tôn trọng luật trên. Dọn định kỳ: `kgr.py gc --apply`.

## 2. An toàn (tóm tắt — xem CLAUDE.md §4)
- OAC/NSAW **CHỈ ĐỌC**; ⛔ CẤM MCP `nsaw-oac-poc` (dùng `oac-native`); đăng nhập điền-1-lần (ORA-28000); mỗi actor 1 profile Chrome, KHÔNG kill Chrome toàn cục.
- Sau thay đổi code: `python OAC-Knowledge/kb_lifecycle/tests/run_all.py --with-legacy` phải xanh (TDD).
