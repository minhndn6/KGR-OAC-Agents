# Dataflow-builder — quy tắc bắt buộc mỗi session

## Browser (Chrome DevTools MCP) — kỷ luật đa session
- Project này có MCP server RIÊNG: **`chrome-dataflow`** (tools `mcp__chrome-dataflow__*`, profile riêng `profile-dataflow`, login OAC bền). **Mọi thao tác browser dùng server này** — KHÔNG dùng server plugin chrome-devtools mặc định (profile dùng chung, sẽ giẫm session khác).
- ⛔ **TUYỆT ĐỐI KHÔNG kill Chrome toàn cục** (`Stop-Process chrome` / taskkill chrome.exe không lọc): cửa sổ Chrome khác có thể thuộc session khác. Gặp "browser already running" → gỡ kẹt THEO PROFILE của mình: chỉ kill process chrome có CommandLine chứa `profile-dataflow`, xoá lock trong đúng thư mục profile đó.
- 2 session KHÔNG sửa cùng 1 dataflow/workbook (Save đè nhau).

## Kiến thức & skill (master OAC Dataflow)
- Đọc `OAC_DATAFLOW_MASTERY.md` (golden tự chứa) trước mọi việc dataflow; skill `oac-dataflow-builder` tự kích hoạt.
- Mảng dashboard/viz → `C:\Project\KGR-OAC-Agents\Dashboard-builder\` (DESIGN + OAC mastery, skills designer/builder).
- Viết tiếng Việt. Gate duyệt plan trước khi build. ADD-only, sandbox `KGR_DF_SANDBOX_EXPLORE`.
- ⛔ **KHÔNG Run/Save dataflow tên `*_bk*` / `*backup*` / `Copy of *`** (vd `(KGR) DF_DAILY_SC_CHAIN_ASOF_bk0307`, `KGR_DF_TD_Metrics_bk`, `KGR_DF_Nganh_Metrics_v3_bk_*`): các backup này ghi **CHUNG output dataset với production** (Daily_Chuoi_Report / Daily_Kenh_Report / TD_Report_Long / Nganh_Report_Long_# …) nhưng chứa **logic CŨ** → chạy nhầm = ĐÈ số production sai âm thầm. Chỉ thao tác dataflow production hiện hành; backup = read-only tham khảo.

## Hygiene — KHÔNG ghi rác file (INV-4)
- File tạm/scratch (dump def `.json`, `*.network-response`, snapshot, ảnh) → ghi RA NGOÀI cây: `kgr_runtime.work_dir("Dataflow-builder")` (giữ lại được) hoặc `kgr_runtime.scratch("ten")` (xóa được). **KHÔNG tạo `_work/` trong repo** — PreToolUse guard sẽ DENY.
- MCP `chrome-dataflow` ghi ở workspace-root của nó → **chuyển ngay ra `kgr_runtime.work_dir("Dataflow-builder")`**; cần cho pipeline rebuild → copy sang `OAC-Knowledge/_work/staging/` (ngoại lệ input, giữ trong cây).
- Đã tự động ép (guard + Stop gate + deny-Read; xem CLAUDE.md gốc §1). Tự kiểm khi cần: `python OAC-Knowledge/kb_lifecycle/tools/check_clean.py --strict`. Tra đích: `kgr.py where`.
