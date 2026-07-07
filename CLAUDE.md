# KGR-OAC-Agents — Quy tắc workspace (đọc TRƯỚC khi làm bất cứ gì)

> File này là điểm-vào chung cho MỌI AI/người làm trong `C:\Project\KGR-OAC-Agents\` (4 repo: OAC-Knowledge,
> OAC-Orchestrator, Dashboard-builder, Dataflow-builder). Cơ chế chi tiết: `OAC-Knowledge/kb_lifecycle/`.
> Kiểm tra nhanh sức khỏe: `python OAC-Knowledge/kb_lifecycle/tools/kgr.py doctor`.

## 0. Định tuyến & write-authority (main = orchestrator, KHÔNG tự ghi OAC) — [ĐANG SIẾT THÀNH CƠ-CHẾ]
- **Yêu cầu GHI OAC (dựng/sửa dataflow/workbook)** → main **KHÔNG tự thực thi bằng browser/REST**; PHẢI giao `oac-dashboard-builder`/`oac-dashboard-designer`/`oac-dataflow-builder` (hoặc orchestrator). Main chỉ **điều-phối + gate + tổng-kết**.
- **Ngữ nghĩa CỨNG (khử nhập-nhằng — sau sự cố 2026-07-07 main tự lái browser sửa production):**
  - Owner nói **"tự làm 100%" / "cứ làm đi"** trên việc GHI = **"điều-phối / giao builder tới 100%"** — TUYỆT ĐỐI KHÔNG = "main tự lái browser ghi production".
  - Owner **cấp token/csrf = DUYỆT bước GHI**, KHÔNG = cho phép main tự-đóng-vai-builder. Token phải đi vào **builder**, không cư-trú/không dùng ở main.
  - Lệnh mơ hồ ("cứ làm đi") trên việc GHI → **PHẢI reflect-back 1 câu** ("tôi sẽ giao builder X chạy…") TRƯỚC khi hành động.
- **Luật fallback khi đường-giao bị chặn** (vd token-gate chặn): thứ tự ĐÚNG = (a) sửa cách giao → (b) leo-thang hỏi owner → (c) **DỪNG báo cáo**. **CẤM self-execute** cái ý-định vừa bị chặn (đây chính là ngòi nổ sự cố 07-07).
- **Read vs Execute — lằn ranh CỨNG:** main được ĐỌC (oac-native read, snapshot/screenshot). Ngay khi cần **thao-tác-đổi-trạng-thái** (click editor, POST save, Run dataflow, fill form OAC) = **ĐÃ sang việc GHI → DỪNG, giao builder**. Không "đọc-dần trượt thành sửa".
- (Cơ chế ép cứng đang triển khai: capability-removal ở `.claude/settings.json` [gỡ browser-write khỏi main] + builder out-of-process + artifact-gate. Chi tiết + root-cause: `_kgr-state/work/_review/INCIDENT_REPORT_2026-07-07.md`. Nhãn [MỀM] cũ đã gỡ.)

## 1. KHÔNG ghi rác vào cây project — MỌI scratch/state ra NGOÀI (hygiene — INV-4)
> Vì sao: file tạm nằm trong cây → agent (Read/Glob/Explore) crawl vào đọc → **đốt token**. Nên scratch/state
> nằm ở `C:\Project\_kgr-state\` (sibling, ngoài crawl NHƯNG trong backup) hoặc `%LOCALAPPDATA%` (xóa được).
- **TUYỆT ĐỐI KHÔNG** tạo file scratch/handoff/state trong cây project (vd `_PNL_*.md`, dump, screenshot, blackboard, `_work/`, `_orchestration/`).
- Lấy đường ghi hợp lệ bằng API, đừng tự đoán (`python OAC-Knowledge/kb_lifecycle/tools/kgr.py where`):

  | Loại | Gọi API | Vị trí (NGOÀI cây) | Backup |
  |---|---|---|---|
  | Scratch "giữ lại được" (thay `<repo>/_work/`) | `kgr_runtime.work_dir("<repo>")` | `C:\Project\_kgr-state\work\<repo>\` | ✅ |
  | State bền (resume/blackboard/lock) | `kgr_runtime.blackboards_dir()/locks_dir()` | `C:\Project\_kgr-state\orchestration\…` | ✅ |
  | Scratch tạm (xóa được) | `kgr_runtime.scratch("ten.ext")` | `%LOCALAPPDATA%\kgr-oac\runtime\…` | ❌ |

  `from kb_lifecycle.tools import kgr_runtime` (hoặc thêm `OAC-Knowledge/kb_lifecycle/tools` vào `sys.path`).
  *(Ngoại lệ: `OAC-Knowledge/_work/staging/` giữ trong cây làm input pipeline rebuild — gitignored + đã chặn crawl.)*
- **ĐÃ TỰ ĐỘNG ÉP (không còn dựa trí nhớ):**
  1. **PreToolUse guard** (`.claude/hooks/guard_write.py`) — DENY ngay khi Write/Edit vào file GENERATED hoặc path scratch trong cây; gợi ý `work_dir()`/`scratch()`.
  2. **Stop gate** (`.claude/hooks/gate_clean.py`) — chặn kết thúc session nếu còn scratch trong cây.
  3. **Git pre-commit** (`.githooks/pre-commit`, bật bằng `kgr.py setup`) — chặn commit nếu tree bẨN.
  4. **deny-Read** (`.claude/settings.json`) — agent không crawl được `_work/`/state → đỡ token.
  5. **Retention:** `python OAC-Knowledge/kb_lifecycle/tools/kgr.py gc --apply` — dọn tmp/dump cũ, archive blackboard >30 ngày.
- Tự kiểm khi cần: `python OAC-Knowledge/kb_lifecycle/tools/check_clean.py --strict` (0 = sạch). `kgr.py doctor` báo `physical_scratch`.

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
