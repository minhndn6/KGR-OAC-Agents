# CONVENTIONS — phân vùng kiến trúc & chống rác file tạm (toàn bộ project KGR OAC)

> Mục tiêu: file TẠM/scratch phát sinh khi làm việc KHÔNG được rơi vào thư mục gốc project (gây rác + lẫn vào git).

## Quy tắc vùng (zoning)
> **MỌI scratch/state ra NGOÀI cây project** (agent crawl vào cây = đốt token). Lấy path qua `kgr_runtime`, đừng hardcode.
> Đã tự động ép: PreToolUse guard + Stop gate + git pre-commit + deny-Read (xem CLAUDE.md §1). `kgr.py where` để tra.

| Loại | Nơi ĐÚNG | API | Git |
|---|---|---|---|
| **Authoritative** (tri thức/spec/skill/code chính) | gốc project (`*.yaml`, `*.md`, `skill/`, `pipeline/`) | — | TRACKED |
| **Temp/scratch "giữ lại được"** (snapshot, dump, ảnh, model tạm) — thay `<repo>/_work/` | **`C:\Project\_kgr-state\work\<repo>\`** (NGOÀI cây, in-backup) | `kgr_runtime.work_dir("<repo>")` | ngoài repo |
| **Scratch tạm** (xóa được: network-response, extract) | **`%LOCALAPPDATA%\kgr-oac\runtime\`** (ngoài backup) | `kgr_runtime.scratch("ten")` | ngoài repo |
| **State bền** (resume/blackboard/lock/build_state) | **`C:\Project\_kgr-state\orchestration\`** (NGOÀI cây, in-backup) | `kgr_runtime.blackboards_dir()/locks_dir()` | ngoài repo |
| **Staging pipeline** (raw JSON dump input để re-distill) — NGOẠI LỆ giữ trong cây | **`OAC-Knowledge/_work/staging/`** (gitignored + deny-Read) | `OAC_STAGING` env | gitignored |
| **Provenance tối thiểu** (raw cần để rebuild) | `OAC-Knowledge/raw/` (json gitignored, .py tracked) | — | mixed |
| **Secrets** | `C:\Project\KGR-OAC-Agents\.secrets\` | `OAC_ENV_FILE` | gitignored |
| **Archive (reversible)** | `C:\Project\_kgr-state\archived\` (blackboard cũ do `kgr.py gc`) | — | ngoài repo |
| **Learning log** (tích lũy tri thức) | `OAC-Knowledge/learnings/` | `learn.py` | TRACKED (xem LEARNING.md) |

## Luật
1. **KHÔNG ghi file tạm/handoff ra gốc project HAY gốc workspace `C:\Project\`.** Tạm trong 1 repo → `<repo>/_work/`; tài liệu liên-project (brief/review/prompt) → `C:\Project\_work\review\`. (Ngoại lệ duy nhất ở gốc workspace: `CONVENTIONS.md` — file authoritative.)
2. Tên file tạm nên có tiền tố `_` hoặc nằm trong `_work/` để dễ nhận.
3. Pipeline OAC-Knowledge đọc staging qua biến `OAC_STAGING` hoặc mặc định `OAC-Knowledge/_work/staging/` (script tự resolve; xem raw/REBUILD.md).
4. File MCP `chrome-dashboard` chỉ ghi được trong workspace root của nó → nếu phải tạm ở Dashboard-builder thì để `Dashboard-builder/_work/` rồi copy sang `OAC-Knowledge/_work/staging/`.
5. Định kỳ: `_work/`, `_archived/` có thể xóa an toàn (regenerable / reversible). KHÔNG xóa `raw/`, `.secrets/`, `learnings/`.

## Portability — tự-định-vị & biến môi trường (để "bê sang máy khác")
Mọi script runtime **tự-định-vị từ `__file__`** (không hardcode `C:\Project`). Workspace = thư mục cha chứa các repo. Override khi cần (vd máy khác, NSAW để ngoài bundle):

| Biến | Ý nghĩa | Mặc định (tự suy ra) |
|---|---|---|
| `KGR_ROOT` | Thư mục workspace (chứa 4 repo) | cha của `OAC-Knowledge` |
| `OAC_KB_ROOT` | Gốc repo OAC-Knowledge | tự suy từ vị trí script |
| `OAC_STAGING` | Thư mục staging pipeline | `OAC-Knowledge/_work/staging` |
| `NSAW_CLAUDE_ROOT` | `NSAW_Claude/data_context` (kho ngoài, optional) | `<WS>/NSAW_Claude/...` rồi `<WS>/../NSAW_Claude/...` |
| `NSAW_CLAUDE_TC` | File TABLE_CATALOG.yaml của NSAW | suy từ NSAW_CLAUDE_ROOT |
| `KGR_STATE_ROOT` | Gốc state bền NGOÀI cây (sibling) | `<WS>/../_kgr-state` (= `C:\Project\_kgr-state`) |
| `KGR_ORCH_DIR` | Thư mục orchestration (blackboards/locks) | `<KGR_STATE_ROOT>/orchestration` |
| `KGR_WORK_DIR` | Gốc scratch "giữ lại được" | `<KGR_STATE_ROOT>/work` |
| `KGR_LOCK_DIR` | Thư mục write-lock orchestrator | `<KGR_STATE_ROOT>/orchestration/locks` |
| `OAC_ENV_FILE` | File secrets oac.env | `<WS>/.secrets/oac.env` rồi `<WS>/../.secrets/...` |

**Trên máy mới**: set `OAC_KB_ROOT` (cho skill cài ở `~/.claude` tìm được KB) là đủ cho phần lớn; phần còn lại tự suy ra. Skill/MCP ở `~/.claude` là theo-user, KHÔNG nằm trong bundle → cần cài lại (xem script setup khi move xong).

## .gitignore chuẩn (mọi repo)
```
_work/
_archived/
.secrets/
__pycache__/
*.pyc
*.png
*.network-response
```
OAC-Knowledge thêm: `raw/*.json`, `raw/projects/`, `raw/digest/`.
