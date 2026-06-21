# Dataflow-builder — quy tắc bắt buộc mỗi session

## Browser (Chrome DevTools MCP) — kỷ luật đa session
- Project này có MCP server RIÊNG: **`chrome-dataflow`** (tools `mcp__chrome-dataflow__*`, profile riêng `profile-dataflow`, login OAC bền). **Mọi thao tác browser dùng server này** — KHÔNG dùng server plugin chrome-devtools mặc định (profile dùng chung, sẽ giẫm session khác).
- ⛔ **TUYỆT ĐỐI KHÔNG kill Chrome toàn cục** (`Stop-Process chrome` / taskkill chrome.exe không lọc): cửa sổ Chrome khác có thể thuộc session khác. Gặp "browser already running" → gỡ kẹt THEO PROFILE của mình: chỉ kill process chrome có CommandLine chứa `profile-dataflow`, xoá lock trong đúng thư mục profile đó.
- 2 session KHÔNG sửa cùng 1 dataflow/workbook (Save đè nhau).

## Kiến thức & skill (master OAC Dataflow)
- Đọc `OAC_DATAFLOW_MASTERY.md` (golden tự chứa) trước mọi việc dataflow; skill `oac-dataflow-builder` tự kích hoạt.
- Mảng dashboard/viz → `C:\Project\KGR-OAC-Agents\Dashboard-builder\` (DESIGN + OAC mastery, skills designer/builder).
- Viết tiếng Việt. Gate duyệt plan trước khi build. ADD-only, sandbox `KGR_DF_SANDBOX_EXPLORE`.
