# KGR-OAC-Agents — Quy tắc workspace (đọc TRƯỚC khi làm bất cứ gì)

> File này là điểm-vào chung cho MỌI AI/người làm trong `C:\Project\KGR-OAC-Agents\` (4 repo: OAC-Knowledge,
> OAC-Orchestrator, Dashboard-builder, Dataflow-builder). Cơ chế chi tiết: `OAC-Knowledge/kb_lifecycle/`.
> Kiểm tra nhanh sức khỏe: `python OAC-Knowledge/kb_lifecycle/tools/kgr.py doctor`.

## 1. KHÔNG ghi rác vào repo (hygiene — INV-4)
- **TUYỆT ĐỐI KHÔNG** tạo file scratch/handoff/state trong cây 4 repo (vd `_PNL_*.md`, dump, screenshot, blackboard).
- Lấy đường ghi hợp lệ bằng API, đừng tự đoán:
  - Scratch tạm (xóa được): `kgr_runtime.scratch("ten.ext")` → `%LOCALAPPDATA%\kgr-oac\runtime\…` (ngoài repo, ngoài backup).
  - State bền (resume/blackboard/lock): `kgr_runtime.blackboards_dir()/locks_dir()` → `<workspace>\_orchestration\…` (ngoài repo NHƯNG trong backup).
  - `from kb_lifecycle.tools import kgr_runtime` hoặc chạy `python OAC-Knowledge/kb_lifecycle/tools/kgr.py where`.
- Cleanliness gate: `python OAC-Knowledge/kb_lifecycle/tools/check_clean.py` (FAIL nếu lỡ track scratch).

## 2. Ghi TRI THỨC mới vào đâu? Hỏi router, đừng đoán (anti-rot — INV-2)
- `python OAC-Knowledge/kb_lifecycle/tools/kb_route.py classify --type <loại>` → trả đích + cách ghi + validation bắt buộc.
- Quy tắc cứng: file có banner `# GENERATED …` là SINH RA — **đừng sửa tay** (sửa nguồn rồi rebuild theo `raw/REBUILD.md`).
  File CURATED (glossary, governance…) sửa trực tiếp + validate. Học/phát hiện → `learn.py add` (append-only) rồi review/promote.

## 3. KB root là DUY NHẤT (chống split-brain — INV-1)
- Mọi script resolve KB qua `kb_paths.resolve_kb_root()` (env `OAC_KB_ROOT` → marker `.kgr_kb_root` → registry). KHÔNG hardcode.
- Bản skill cài ở `~/.claude/skills`: chạy `kgr.py setup` một lần để ghi registry trỏ workspace KB.

## 4. An toàn
- OAC/NSAW: **CHỈ ĐỌC** (không sửa/xóa). Một tài khoản OAC dùng chung → KHÔNG tự re-login loạn (rủi ro khóa ORA-28000).
- ⛔ **CẤM dùng MCP `nsaw-oac-poc`** (mọi `mcp__nsaw-oac-poc__*`) — deprecated, owner cấm. Đọc OAC live → dùng **`oac-native`** (`oracle_analytics-execute_logical_sql` / `-discover_data` / `-describe_data`).
- Browser: mỗi actor một profile riêng; KHÔNG kill Chrome toàn cục.
- Số liệu: KHÔNG lưu số tuyệt đối vào KB (lấy live khi cần). Trên workbook production: ADD-only.

## 5. Bất biến (INV) & quy trình
INV-1 KB root duy nhất · INV-2 mọi file tri thức phân loại được · INV-3 pin LF (`.gitattributes`) trước khi tin hash/diff ·
INV-4 durable backed-up / scratch ngoài repo · INV-5 đổi fact = supersede có audit · INV-6 staleness phải FAIL ồn.
Dev theo TDD; sau mỗi thay đổi: `python OAC-Knowledge/kb_lifecycle/tests/run_all.py --with-legacy` phải xanh.
