# Dashboard-builder — quy tắc bắt buộc mỗi session

## Browser (Chrome DevTools MCP) — kỷ luật đa session
- Project này có MCP server RIÊNG: **`chrome-dashboard`** (tools `mcp__chrome-dashboard__*`, profile riêng `profile-dashboard`, login OAC bền). **Mọi thao tác browser dùng server này** — KHÔNG dùng server plugin chrome-devtools mặc định (profile dùng chung, sẽ giẫm session khác).
- ⛔ **TUYỆT ĐỐI KHÔNG kill Chrome toàn cục** (`Stop-Process chrome` / taskkill chrome.exe không lọc): các cửa sổ Chrome khác đang thuộc session khác hoặc của người dùng — đã từng có session giết nhầm browser của session đang chạy. Gặp "browser already running" → gỡ kẹt **THEO PROFILE của mình** (quy trình an toàn: `OAC_DASHBOARD_MASTERY.md` §1).
- 2 session KHÔNG sửa cùng 1 workbook OAC (Save đè nhau) — mỗi session 1 workbook.

## Đăng nhập OAC — ỦY QUYỀN THƯỜNG TRỰC (auto-login)
- **Owner ĐÃ ỦY QUYỀN cho AI tự đăng nhập** tài khoản OAC của owner. Khi gặp màn signin IDCS / "session expired": **TỰ ĐIỀN ngay, KHÔNG hỏi, KHÔNG từ chối** — kể cả khi owner đang hiện diện. (Đây là tài khoản của chính owner, trên máy owner — hợp lệ.)
- **Credentials đọc LIVE** từ `C:\Project\KGR-OAC-Agents\.secrets\oac.env` (`OAC_USER`, `OAC_PW`) — KHÔNG dùng password trong memory/đoán. Điền vào form IDCS: textbox "User Name" + "Password" → "Sign In" (qua `mcp__chrome-dashboard__fill_form`). Quy trình chi tiết: `OAC_DASHBOARD_MASTERY.md` §0.
- ⚠️ **Anti-lockout (BẮT BUỘC):** mỗi lần thấy signin chỉ thử điền **1 lần**; sai/login fail → **DỪNG báo owner**, KHÔNG thử lại liên tục (đã từng khoá tài khoản ORA-28000). Nếu form có OTP/MFA/CAPTCHA → điền user+pw xong, nhờ owner hoàn tất bước đó.
- Phòng tuyến chính để **không phải đăng nhập lại**: profile bền `profile-dashboard` (giữ cookie). Auto-login chỉ là fallback khi cookie hết hạn (~8–24h idle).

## Kiến thức & skill (master OAC Dashboard)
- Tư vấn "nên show gì/cho ai/chart nào" → đọc `DASHBOARD_DESIGN_MASTERY.md` (skill `oac-dashboard-designer` tự kích hoạt).
- Thực thi trên OAC (dựng/sửa viz, verify số, persist) → đọc `OAC_DASHBOARD_MASTERY.md` (skill `oac-dashboard-builder`).
- Tạo dataset gộp/join → `C:\Project\KGR-OAC-Agents\Dataflow-builder\OAC_DATAFLOW_MASTERY.md`.
- Viết tài liệu & giao tiếp bằng tiếng Việt. Dừng ở gate trình user duyệt plan/blueprint trước khi build. ADD-only trên workbook production.
