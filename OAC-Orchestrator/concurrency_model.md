# Concurrency model — chạy N agent an toàn trên 1 OAC instance

> Hệ hiện tại engineered cho **1 người tuần tự**. Chạy 3 agent song song sẽ vỡ vài bất biến. Đây là mô hình để orchestrator an toàn.

## Nguyên tắc: 1-WRITER, NHIỀU-READER
- **Reads fan-out** (song song OK): `kgr-oac-lineage` (lineage/live-read), dashboard-builder[pha design] (đọc OAC-knowledge ra blueprint), cross-check. Mỗi reader là context ngắn, trả JSON.
- **Writes serialize** (tuần tự, độc quyền theo artifact): `oac-dashboard-builder` (save workbook), `oac-dataflow-builder` (save/run dataflow). KHÔNG bao giờ 2 writer cùng 1 workbook/dataflow.

## Profile-per-actor (BẮT BUỘC khi song song)
Đã có 3 profile cho 3 actor (chrome-lineage ĐÃ tạo tại ROOT `./.mcp.json` — hết cảnh lineage dùng chung `profile-dashboard`):
| Agent | MCP server | profile |
|---|---|---|
| oac-dashboard-builder | chrome-dashboard | profile-dashboard |
| oac-dataflow-builder | chrome-dataflow | profile-dataflow |
| kgr-oac-lineage (live-read) | **chrome-lineage (ĐÃ tạo tại ROOT `./.mcp.json`)** | **profile-lineage (ĐÃ tạo)** |
| (mỗi slot song song thêm → 1 profile riêng) | | |
→ Mỗi profile = 1 cookie/CSRF/_abck riêng → hết đụng "browser already running" + hết rotate token lẫn nhau.

## Write-lock (biến quy ước thành cưỡng chế)
- Save workbook OAC = REST `POST projects/json overwrite:true` → **last-writer-wins ÂM THẦM**. 2 agent đụng DB02 → 1 bản mất, `success:true`.
- Cơ chế: trước mọi write, agent phải **acquire lock theo artifact** (workbook path / dataflow id) qua `lock.py`. Orchestrator giữ sổ lock. Reads không cần lock.
- Lock dir: `C:\Project\KGR-OAC-Agents\_orchestration\locks\<slug>.lock` (chứa holder + ts). Stale lock (quá TTL) → orchestrator giải phóng.

## Login/session — orchestrator sở hữu
- 1 tài khoản OAC + 1 login gate "user present → hỏi" → **không có trọng tài** khi 3 agent cùng cần re-auth → rủi ro **khoá tài khoản** (ORA-28000 đã từng xảy ra).
- Orchestrator là **chủ duy nhất** của re-auth + health-check session; sub-agent xin "session khoẻ", KHÔNG tự re-login.
- **Khuyến nghị mạnh**: tài khoản OAC **read-only riêng** cho reader-agents (lineage/crosscheck) + tài khoản write riêng cho builder → lockout writer không làm chết reader; least-privilege.

## Khôi phục sau lỗi/crash (durable state — xem `agent_contracts.yaml` failure_policy + `scripts/blackboard.py`)
- **Ghi state atomic**: `blackboard.py` ghi qua `tmp → os.replace` + giữ `.bak` last-known-good → crash giữa lúc ghi KHÔNG để lại state nửa vời; `_read` tự lành main hỏng từ `.bak`.
- **Step-state để resume**: mỗi bước có `{state, attempts, last_error}`. `running` lúc crash → `recover` đổi thành `interrupted` (chạy lại được); `ok` thì bỏ qua → resume sạch, không làm trùng (ADD-only đối chiếu `saved_canvas_refs`).
- **Quy trình sau gián đoạn**: `blackboard.py recover <id>` (in `resume_steps` + issues) → `lock.py status <artifact>` xác nhận không còn writer sống (steal nếu quá TTL) → tiếp tục từ bước dở.
- **Không vòng lặp vô hạn**: retry chỉ cho `transient`, tối đa 3; hết retry → `fail`/escalate `open_questions` (đã từng kẹt 529 Overloaded — bounded retry chặn việc đó).

## Khi nào song song / khi nào tuần tự (quyết nhanh)
- Song song: nhiều lineage trace / audit nhiều canvas / cross-check mù / designer.
- Tuần tự: mọi thao tác chạm browser-write hoặc Save cùng artifact.
- Build cross-agent (dashboard cần dataset mới): tuần tự theo chuỗi designer→lineage→dataflow→dashboard (xem ORCHESTRATION_DESIGN), với lineage có thể fan-out trong từng bước.
