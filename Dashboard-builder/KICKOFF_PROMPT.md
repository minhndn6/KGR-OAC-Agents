# PROMPT KHỞI ĐỘNG — Trở thành MASTER OAC DASHBOARD (Workbook/Visualization)

> Dán toàn bộ khối dưới đây vào một session Claude Code MỚI, mở tại thư mục `C:\Project\KGR-OAC-Agents\Dashboard-builder`.
> (Mục tiêu: lặp lại đúng quy trình đã biến một session trước thành Master Dataflow, nhưng cho mảng DASHBOARD/WORKBOOK.)

---

Nhiệm vụ tối thượng của bạn trong session này: **trở thành MASTER OAC Dashboard (Workbook / Visualization) builder cho Kangaroo (KGR)** — thông thuộc MỌI loại biểu đồ, mọi cấu hình, mọi ngóc ngách của workbook editor trên Oracle Analytics Cloud, thành thạo như người dựng dashboard OAC 15 năm. Làm y hệt cơ chế mà một session trước đã dùng để trở thành **Master Dataflow** (kết quả của nó: `C:\Project\KGR-OAC-Agents\Dataflow-builder\OAC_DATAFLOW_MASTERY.md` + skill `oac-dataflow-builder`).

**Hai sản phẩm cuối bắt buộc:**
1. **File golden TỰ CHỨA** `C:\Project\KGR-OAC-Agents\Dashboard-builder\OAC_DASHBOARD_MASTERY.md` — đọc 1 file này là dựng được mọi dashboard, không cần file nào khác.
2. **Skill** `oac-dashboard-builder` (đặt ở `C:\Project\KGR-OAC-Agents\Dashboard-builder\.claude\skills\oac-dashboard-builder\`) — để các session Claude sau tự động dựng/sửa/review dashboard như master.

Tôi (người dùng) là đầu mối finance/data Kangaroo, nói tiếng Việt, dùng Windows + PowerShell. **Viết mọi tài liệu & giao tiếp bằng tiếng Việt.** ĐỪNG hỏi xin phép vụn vặt — tự chủ làm, chỉ hỏi khi thực sự là quyết định của tôi (xem "Khi nào hỏi" cuối prompt).

---

## A. ĐỌC THAM CHIẾU TRƯỚC (đừng làm lại từ số 0)

**A1. Khuôn mẫu CHẤT LƯỢNG + ĐỊNH DẠNG (đọc để biết "đích đến trông như thế nào"):**
- `C:\Project\KGR-OAC-Agents\Dataflow-builder\OAC_DATAFLOW_MASTERY.md` — file golden mảng dataflow. Học CÁCH NÓ ĐƯỢC VIẾT: tự chứa, tiếng Việt, icon (⭐ đọc kỹ · ⚠️ bẫy · ✅ đã verify live · 📌 số load-bearing), mục lục, mỗi loại node 1 mục + config + **bẫy commit/persist** + walls + REST + checklist + changelog. File golden dashboard của bạn phải đạt CÙNG đẳng cấp cho mảng workbook.
- `C:\Project\KGR-OAC-Agents\Dataflow-builder\.claude\skills\oac-dataflow-builder\SKILL.md` + thư mục `references/` — khuôn mẫu CẤU TRÚC SKILL (6 phase: ANALYZE → PLAN → GATE trình duyệt → BUILD → VERIFY bằng số → REPORT + tự cập nhật knowledge; kiến trúc multi-agent; quy tắc cập nhật knowledge; Definition of Done). Skill dashboard của bạn nên theo khung tương tự, chỉnh cho hợp workbook.

**A2. Kiến thức WORKBOOK CŨ đang nằm rải rác — phải MINE HẾT rồi migrate vào file golden mới (đừng bỏ sót, nhưng PHẢI verify-live lại vì có thể lỗi thời):**
- `C:\Project\KGR_Dashboard\OAC_CHROME_MCP_PLAYBOOK.md` — §0 login, §2 bộ công cụ Chrome DevTools MCP, §3 patterns (snapshot→file→grep uid; evaluate trả JSON gọn; real-click vs synthetic; set title CKEditor; note TinyMCE), §4 NAVIGATION click-path đã verify (đổi mode Data/Visualize/Present, đổi canvas, **tạo viz + chọn field đúng dataset**, đổi loại chart, sửa Title→Custom, number format M/%, filter canvas/viz, thao tác chip measure, **add Note tiếng Việt**, xoá viz/note, rename canvas, **SAVE workbook**, add dataset, blend data diagram), §5 quy ước (Title tiếng Anh / Note tiếng Việt; **màu Kangaroo** xanh #44BA46 / cam #F16522 / xám #636466 / xanh đậm #008242 / xám nhạt #E6E7E8; ADD-only; save thường xuyên).
- `C:\Project\KGR_Dashboard\NAVIGATION_PLAYBOOK.md` — mode switch, rename canvas, save, **add note flow tối ưu**, reload data, My Calculations.
- `C:\Project\KGR_Dashboard\ERROR_LOG.md` — các WALL workbook đã biết: **#A note text không sửa được qua script** (xoá+tạo mới), **#B reorder chip trong shelf là wall** (nhờ user kéo tay), **#C set Title bằng setter trên Auto-title KHÔNG persist** (phải MCP-click dropdown → Custom → real keyboard), Save "Share Related Items" **bấm OK KHÔNG Escape**, verify persist qua `GET projects/json`, viz Top-N/Exclude filter, set màu series qua Menu→Color→Manage Assignments (workbook-level), combo bar+line, đọc số viz qua XHR `executeOrPoll`.
- `C:\Project\KGR_Dashboard\OAC_CHART_TYPES.md`, `UX_LAYOUT_RECOMMENDATIONS.md`, `_SPEC_titles_formats.md`, `_SPEC_notes.md`, `C-LEVEL_DATA_STORY.md`, `PROPOSED_CHARTS.md`, `_REVIEW_DB01_2026-06-09.md`.
- **Skill workbook đã có** (đọc để biết click-path + vai trò, rồi nâng cấp/tổng hợp): `oac-implementor` (sửa viz tận tay), `oac-manager` (điều phối + gate), `oac-clevel-reviewer` (review góc C-level), `oac-data-crosscheck` (đối chiếu số qua NSAW MCP). Tìm trong registry skill của máy / `.claude/skills`.
- **Memory** ở `C:\Users\ADMIN\.claude\projects\C--Project-KGR-Dashboard\memory\` (đọc `MEMORY.md` + các file): title cần real keyboard, **viz mới phải dựng trên canvas trống** (double-click trên canvas đông sẽ merge vào viz chính), save OK-not-Escape, DB01 hiện 10 canvas, màu Kangaroo, các canvas SFC.

**A3. Môi trường & login:** OAC instance `https://oaxinst70021-id3pgnmhxlya-0p-bo.analytics.ocp.oraclecloud.com`. Thông tin đăng nhập + cách xử lý redirect IDCS xem `OAC_DATAFLOW_MASTERY.md §0` (TIN file này, ĐỪNG tin password trong memory cũ — đã có vụ memory ghi sai password). Nếu phiên hết hạn và tôi đang hiện diện → nhờ tôi login tay.

---

## B. QUY TRÌNH HỌC (làm tuần tự, mỗi phase xong mới sang phase sau)

### Phase 1 — HỌC QUA ĐỌC
Đọc hết A1+A2+A3. Rút ra: workbook editor có những vùng nào (modes, canvas, grammar/shelves, properties, filters, calculations, data panel), loại viz nào, gotcha nào đã ghi. Lập danh sách "cần verify-live + cần khám phá sâu".

### Phase 2 — HỌC QUA LÀM (thực nghiệm LIVE, quan trọng nhất)
Công cụ ưu tiên: **Chrome DevTools MCP** (`mcp__plugin_chrome-devtools-mcp_chrome-devtools__*`). Sau **5 lần** thất bại cùng 1 thao tác → chuyển **computer-use**. Pattern bắt buộc: `take_snapshot(filePath=...)` ra file rồi Grep/Read lấy uid (đừng đổ snapshot vào context); `evaluate_script` trả JSON GỌN (đừng map toàn bộ textContent); poll xác nhận sau mỗi thao tác.

**⚠️ Guardrail bắt buộc:**
- **Tạo 1 WORKBOOK SANDBOX riêng** để thử (ví dụ `KGR_WB_SANDBOX_EXPLORE`) — KHÔNG nghịch trên workbook production `(KGR) DB01.Revenue_v1.1`. Nếu cần data thật để dựng viz, add 1 dataset có sẵn vào sandbox.
- **ADD-only / KHÔNG xoá** bất kỳ artifact production nào. Chỉ thử trong sandbox.
- **Save thường xuyên** (chống timeout). Reload = mất edit chưa lưu.

**Khám phá CHO HẾT, mỗi thứ tự tay làm + ghi lại config + bẫy:**
1. **Mode**: Data / Visualize / Present — chuyển qua lại, khác nhau gì.
2. **Canvas**: tạo / rename / reorder / xoá canvas; layout Auto vs Freeform; di chuyển/resize ô viz (cái nào là wall).
3. **Tạo viz**: mọi cách (double-click field, kéo field vào canvas, nút Add Visualization). **Quy tắc "viz mới trên canvas trống"** — verify.
4. **MỌI LOẠI VIZ** (tự liệt kê từ picker "Select Visualization Type" và làm thử từng cái): Bar/Stacked Bar/Horizontal Bar, Line, **Combo (bar+line)**, Area, Pie/Donut, Table, Pivot Table, **KPI/Tile**, Treemap, Scatter, Bubble, Map, Gauge, Heatmap, Waterfall, Funnel, List/Text box, v.v. Với mỗi loại: cách tạo, shelf nào nhận field gì, config riêng.
5. **Grammar panel / shelves**: Category (X) / Values (Y) / Color / Size / Trellis (rows/cols) / Tooltip / … — add/swap/remove pill; **thao tác chip measure** (Aggregate Sum/Avg/Min/Max/…, Sort, Number Format, Y2 axis, Bar/Line cho combo, Create Filter, Delete); **reorder chip trong shelf** (xác nhận còn là wall không).
6. **Properties (General/Values/Axis/Legend/…)**: **Title Auto/Custom/None** (verify cơ chế: setter revert hay không, có cần real keyboard); **Number Format** (Million/Percent/Decimal/Abbreviate/currency); data labels; axis min/max/title; legend vị trí; **reference line**; conditional format.
7. **Màu**: set màu 1 series (Menu→Color→Manage Assignments, workbook-level) + bảng màu Kangaroo; theme.
8. **Filter**: filter bar canvas-level vs filter của viz (shelf Filters); loại filter (List / Range / Date / **Top-Bottom-N** / **Expression filter**); cách chọn giá trị; áp nhiều viz.
9. **Calculation**: My Calculations / calculated column; cú pháp biểu thức; chèn token cột (đừng gõ literal "Tên cột").
10. **Note/annotation tiếng Việt**: tạo / sửa (wall?) / xoá / di chuyển / neo vào viz / hide-show.
11. **Data panel**: add dataset vào workbook; **blend / Data Diagram** (định nghĩa match); reload data; nhiều dataset.
12. **Save & persist**: nút Save, dialog "Share Related Items" (**OK không Escape**); verify persist qua REST `GET /ui/dv/ui/api/v2/projects/json?path=<enc>` (đếm canvas, last-modified, map canvas→viz); Present mode.
13. **Mô hình REST của workbook** (nếu khám phá được): `projects/json` đọc model; thử xem có PUT/save model được không; XHR data-query `…/data/executeOrPoll` để đọc SỐ THẬT của viz (đối chiếu khi verify). (Lưu ý: dựng viz qua REST thường khó hơn dataflow — ưu tiên UI; nhưng REST rất hữu ích để ĐỌC/AUDIT model + số.)

**Tinh thần "deep practice" (điều tôi coi trọng nhất):** với mỗi thao tác, tìm cho ra **hành vi commit/persist & bẫy** bằng thử-sai THẬT, không tin chay tài liệu cũ (nó có thể lỗi thời). Ví dụ kiểu bẫy: cái gì set bằng script bị REVERT (title Auto, note text), cái gì cần REAL keyboard, cái gì merge nhầm khi double-click trên canvas đông, reorder gì là wall, Save kiểu nào mất việc (Escape), số trên viz lấy ở đâu. Ghi rõ "✅ verify ngày…" cho thứ đã tự kiểm.

### Phase 3 — VIẾT FILE GOLDEN TỰ CHỨA
Tổng hợp tất cả vào `C:\Project\KGR-OAC-Agents\Dashboard-builder\OAC_DASHBOARD_MASTERY.md`: **tự chứa tuyệt đối** (migrate hết kiến thức workbook từ A2 vào, KHÔNG để cross-ref tới file cũ), tiếng Việt, icon, mục lục. Cấu trúc gợi ý: §0 login/môi trường · §1 bộ công cụ MCP & pattern · §2 mở/điều hướng workbook & sandbox · §3 bố cục editor (modes/canvas/grammar/properties/filters/data) · §4 ⭐⭐ COMMIT/PERSIST & bẫy (title/chip/note/filter/màu/layout/save — phần quan trọng nhất) · §5 taxonomy MỌI loại viz + cách tạo + config riêng · §6 grammar/shelves + thao tác chip · §7 properties (title/number format/axis/legend/reference line/data label) · §8 màu & branding Kangaroo · §9 filter (các loại) · §10 calculation/expression · §11 note tiếng Việt · §12 canvas & layout · §13 save/persist + REST projects/json + đọc số viz · §14 walls & workaround · §15 quy ước (Title EN/Note VN, ADD-only) · §16 checklist dựng 1 dashboard + Definition of Done · §17 câu lệnh mở màn · §18 changelog. Thêm memory pointer + 1 dòng index trong `MEMORY.md`.

### Phase 4 — DỰNG SKILL (dùng skill-creator)
Gọi skill `skill-creator` để tạo `oac-dashboard-builder` tại `C:\Project\KGR-OAC-Agents\Dashboard-builder\.claude\skills\`. Skill phải operationalize file golden thành quy trình: **ANALYZE** (hiểu yêu cầu dashboard: thông điệp, đối tượng C-level, viz nào, số nào) → **PLAN** (chọn loại viz, shelf, filter, layout, số kỳ vọng) → **GATE trình tôi duyệt** → **BUILD** (Chrome MCP, kỷ luật: viz mới trên canvas trống, title real keyboard, save OK-not-Escape, ADD-only) → **VERIFY bằng số** (đối chiếu số trên viz với nguồn qua NSAW MCP / executeOrPoll / golden report — KHÔNG để dashboard hiển thị số sai) → **REPORT + tự cập nhật knowledge**. **Cân nhắc multi-agent**: agent chính độc quyền browser; subagent phụ trợ KHÔNG đụng browser (plan-reviewer; **data-crosscheck** đối chiếu số qua NSAW — tái dùng tinh thần skill `oac-data-crosscheck`; **C-level reviewer** review "dashboard có giúp ra quyết định không, có chart-junk / số gây hiểu nhầm không" — tái dùng `oac-clevel-reviewer`). Tự cân nhắc model/effort cho từng subagent. Chạy **eval** (dry-run plan-only như session dataflow đã làm: test prompt → agent đọc knowledge + ra PLAN dashboard chi tiết, KHÔNG đụng OAC thật) + iterate. Cuối cùng tối ưu description để skill trigger đúng.

### Phase 5 — THỰC CHIẾN
Dùng chính skill vừa tạo để làm THẬT ≥1 yêu cầu dashboard nhỏ trên sandbox (hoặc 1 canvas mới trên DB01 nếu tôi đồng ý), end-to-end: plan → tôi duyệt → build → verify số → báo cáo. Gặp wall thì tra/ghi; phát hiện/gotcha mới → tự cập nhật vào file golden (đúng section, supersede thay vì trùng, có changelog). Definition of Done của 1 dashboard: viz đúng loại + số khớp nguồn (có bảng đối chiếu) + persist verified qua projects/json + branding/format đúng + **mở lại reload thấy còn nguyên**.

---

## C. NGUYÊN TẮC CHUNG
- Công cụ: Chrome DevTools MCP → (sau 5 lần fail) → computer-use. Snapshot ra file rồi grep; evaluate trả JSON gọn.
- **KHÔNG xoá/ghi đè artifact production**; thử trong workbook sandbox; ADD-only khi đụng DB01.
- Title tiếng Anh, Note tiếng Việt, axis/legend giữ tên gốc; màu Kangaroo chuẩn.
- Verify bằng SỐ, đừng tin toast; persist verify qua `projects/json`.
- Tự cập nhật knowledge có kỷ luật: đúng section, grep trước khi viết, supersede nội dung sai thay vì append trùng, mỗi đợt thêm dòng changelog.
- **Khi nào hỏi tôi (ngoài gate duyệt plan):** thiếu quyền/credentials; yêu cầu mâu thuẫn với data thật; 2 nguồn số khác nhau không tự quyết được; sắp làm việc phá hủy (xoá/ghi đè). Còn lại tự xử + báo cáo sau.

Bắt đầu từ Phase 1. Khi cần tôi (login, duyệt plan, chốt lựa chọn) thì hỏi gọn 1 lần kèm phương án đề xuất.
