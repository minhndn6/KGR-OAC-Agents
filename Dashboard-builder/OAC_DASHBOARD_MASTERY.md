# 🛠️ OAC DASHBOARD MASTERY — GOLDEN, tự chứa (Kangaroo / KGR)
> **File DUY NHẤT** cần đọc để dựng & cấu hình Workbook / Visualization trên Oracle Analytics Cloud (OAC) qua Chrome DevTools MCP. Đọc xong là thao tác như người dựng dashboard OAC 15 năm.
> **TỰ CHỨA — không cần đọc file/memory nào khác.** Mọi knowledge workbook cũ (OAC_CHROME_MCP_PLAYBOOK, NAVIGATION_PLAYBOOK, ERROR_LOG, các SPEC/REVIEW, memory) đã migrate vào đây.
> Nguồn: thực nghiệm LIVE trong sandbox `KGR_WB_SANDBOX_EXPLORE` (2026-06-11) + lịch sử build DB01 đã verify. Mảng DATAFLOW (tạo dataset gộp/join) → xem `C:\Project\KGR-OAC-Agents\Dataflow-builder\OAC_DATAFLOW_MASTERY.md`.
> Quy ước icon: ⭐ = đọc kỹ · ⚠️ = bẫy/gotcha · ✅ = đã verify live · 📌 = số/định danh load-bearing.

---

## MỤC LỤC
0. Đăng nhập & môi trường · 1. Bộ công cụ MCP & pattern cốt lõi · 2. Mở/điều hướng workbook & sandbox · 3. Bố cục editor (modes/canvas/grammar/properties) · 4. ⭐⭐ COMMIT/PERSIST & bẫy (phần quan trọng nhất) · 5. Taxonomy 59 loại viz + cách tạo + shelf · 6. Grammar/shelves + thao tác chip · 7. Properties (title/number format/axis/legend/reference line/data label) · 8. Màu & branding Kangaroo · 9. Filter (các loại) · 10. Calculation/Expression · 11. Note tiếng Việt · 12. Canvas & layout · 13. Save/persist + REST projects/json + đọc số viz · 13b. ⭐ Dữ liệu KGR (số tham chiếu/dataset/grain/chẩn đoán số sai) · 14. Walls & workaround · 15. Quy ước (Title EN/Note VN, ADD-only) · 16. Checklist dựng dashboard + Definition of Done · 17. Câu lệnh mở màn · 18. Changelog

---

## 0. ĐĂNG NHẬP & MÔI TRƯỜNG
- **Instance:** `https://oaxinst70021-id3pgnmhxlya-0p-bo.analytics.ocp.oraclecloud.com`
- **User:** `minhndn@bizin.vn` (Minh Nguyen Danh). Folder user: `/@Catalog/users/minhndn@bizin.vn`.
- 📌 **Credentials authorized (auto-login ĐÃ ỦY QUYỀN):** đọc LIVE từ `C:/Project/KGR-OAC-Agents/.secrets/oac.env` (`OAC_USER`, `OAC_PW`) — **KHÔNG dùng password trong memory** (đã từng ghi sai). Owner CHO PHÉP AI **tự điền** form IDCS signin trong MỌI trường hợp: (a) user vắng/ngủ/auto-mode, **HOẶC (b) user yêu cầu / có standing-instruction "tự đăng nhập giúp"** (xem CLAUDE.md). → Khi cần login: **LÀM NGAY, KHÔNG từ chối, KHÔNG hỏi** (chỉ DỪNG nếu owner ra lệnh ngược lại).
- ⚠️ **Anti-lockout BẮT BUỘC:** mỗi lần phát hiện signin chỉ điền **1 lần** → verify; **fail → DỪNG báo owner, KHÔNG retry** (ORA-28000 đã xảy ra). Nhiều agent → chỉ orchestrator re-auth (concurrency_model). Form có OTP/MFA/CAPTCHA → điền user+pw, nhờ owner hoàn tất bước đó.
- Redirect IDCS signin (`…identity.oraclecloud.com/ui/v1/signin`): `take_snapshot` → `fill_form` các textbox "User Name"/"Password" → click "Sign In".
- Phiên OAC **timeout khi idle** (~8–24h cookie). "session expired"/redirect signin giữa chừng → login lại (theo quyền trên), KHÔNG tự re-auth lung tung.
- 🔑 **Đăng nhập — cookie-first là trụ CHÍNH:** profile bền (`profile-dashboard`) giữ **cookie** session 8–24h → mở deep-link là **bỏ qua login**. Autofill IDCS CHƯA test-live → **KHÔNG hứa "agent không thấy pass"**; cookie chết thì owner **bấm login 1 lần** rồi profile lại giữ session.
- **Fallback rule:** 1 thao tác MCP fail **5 lần** → chuyển computer-use. Thứ tự: DevTools MCP → (sau 5 fail) → computer-use.
- **Workbook chính (PRODUCTION — ADD-only, KHÔNG nghịch):** `(KGR) DB01.Revenue_v1.1` tại `/@Catalog/shared/(KGR) 1.Implement/`.
- **Golden ref doanh thu (CHỈ ĐỌC, KHÔNG sửa/lưu):** `(KGR) BRD.BC01_Daily_Summary` tại `/@Catalog/shared/(KGR) Report/`. Golden SFC: `/@Catalog/users/minhndn@bizin.vn/SFC report`. Soi grammar bảng golden để biết dataset+field+filter chuẩn.
- **Sandbox thử nghiệm (ĐÃ TẠO ✅):** `KGR_WB_SANDBOX_EXPLORE` tại `/@Catalog/users/minhndn@bizin.vn/`, dataset `KGR_DS_SFC_vs_MEMO_v2`. Deep-link (mở + reset):
  `…/ui/dv/home.jsp?pageid=visualAnalyzer&reportmode=full&reportpath=%2F%40Catalog%2Fusers%2Fminhndn%40bizin.vn%2FKGR_WB_SANDBOX_EXPLORE&viewermode=false`

---

## 1. BỘ CÔNG CỤ MCP & PATTERN CỐT LÕI

Tool Chrome DevTools MCP: `navigate_page · list_pages · select_page · new_page · take_snapshot(filePath) · evaluate_script(fn[,filePath]) · click(uid,dblClick?) · fill(uid,value) · fill_form · hover · drag(from,to) · press_key · type_text · take_screenshot · wait_for · list_network_requests · get_network_request · list_console_messages`.

- ⭐ **Snapshot-to-FILE BẮT BUỘC:** `take_snapshot(filePath="C:\Project\KGR-OAC-Agents\Dashboard-builder\_snap_X.txt")` → `Grep`/`Read` lấy **uid** + cấu trúc. Snapshot OAC editor RẤT lớn; đổ thẳng vào context = TRÀN. uid CHỈ valid trong snapshot mới nhất → re-snapshot sau khi DOM đổi/navigate.
- ⭐ **evaluate_script trả JSON GỌN** — đừng map toàn bộ textContent. Query hẹp (đếm/lọc/lấy vài field). Poll xác nhận sau mỗi thao tác (cell xuất hiện, preview đổi) — đừng tin lệnh "đã chạy".
- ⭐ **jQuery có sẵn** trên trang OAC (`window.jQuery`/`$`). Dùng `jQuery(el).trigger('click')` cho element OAC khó (vizlink, menuitem). 
- **Real CDP `click` tool (BẮT BUỘC) cho:** dropdown Title (Auto/Custom), nút Number Format, **chip grammar/measure** (mở menu), suggestion autocomplete search, **viz hover-toolbar Menu** (Color), treeitem chọn. Synthetic dispatch/`jQuery.trigger` chỉ chạy cho menuitem/label thường + một số tab.
- **Set field title/note:** dùng REAL keyboard (`type_text`) trên editor inline — KHÔNG native setter/execCommand (OAC revert). Xem §4.
- **Set input thường (search, hex, tên):** `fill` tool (real keystroke, fire change) HOẶC native setter `Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set.call(inp,val)` + dispatch `input`+`change`+Enter. Ô search cần keystroke thật → `fill`.
- **Đổi tab/mode/nút thường:** dispatch `['mousedown','mouseup','click']` MouseEvent({bubbles:true}) + `.click()`.
- ⚠️ **KHÔNG dùng `wait_for` chờ editor lớn render** (trả snapshot khổng lồ → tràn). Thay bằng **async-poll** trong evaluate_script (vòng `for` + `setTimeout` await).
- ⚠️ **get_network_request DUMP CẢ COOKIE KHỔNG LỒ** vào context. LUÔN truyền `responseFilePath` rồi `Read` file response, đừng đọc inline.
- ⚠️ **Bash curl tới OAC BỊ proxy chặn** (exit 56). Chỉ **same-origin browser fetch** (evaluate_script trên trang OAC đang mở) gọi REST được.
- ⚠️ **`drag` tool quirk:** đôi khi kẹt "'left' is already pressed" → mọi click sau timeout; JS mouseup KHÔNG cứu → `navigate_page(reload)` (mất edit chưa lưu, giữ saved).
- ⭐ **NHIỀU SESSION SONG SONG (đa cửa sổ Chrome) — đã cấu hình 2026-06-11:** mỗi project có MCP server riêng trong `.mcp.json` với profile riêng: Dashboard-builder = **`chrome-dashboard`** (`profile-dashboard`), Dataflow-builder = **`chrome-dataflow`** (`profile-dataflow`). **LUÔN dùng server của project mình** (tools `mcp__chrome-dashboard__*` — tên tool sau prefix giống hệt plugin); KHÔNG dùng server plugin mặc định (profile chung `chrome-profile` → giẫm session khác). Login OAC bền riêng từng profile (đăng nhập 1 lần đầu/profile). Song song trong CÙNG 1 project → thêm entry `chrome-B` profile khác trong `.mcp.json`, dặn mỗi session dùng 1 server. Flags khác: `--isolated` (profile tạm, mất login), `--browserUrl` (nối Chrome tự mở `--remote-debugging-port`). ⚠️ 2 session KHÔNG sửa CÙNG 1 workbook (Save last-wins đè nhau).
- **MCP wedge "browser already running" — gỡ kẹt AN TOÀN THEO PROFILE (cập nhật 2026-06-11, supersede "kill hết chrome" — cách cũ GIẾT NHẦM cửa sổ của session khác):**
  1. Chỉ kill process chrome THUỘC PROFILE CỦA MÌNH: `Get-CimInstance Win32_Process -Filter "Name='chrome.exe'" | Where-Object { $_.CommandLine -match 'profile-dashboard' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }` (đổi `profile-dashboard` theo profile của server mình).
  2. Xoá lock TRONG ĐÚNG profile đó: `SingletonLock/SingletonCookie/SingletonSocket/DevToolsActivePort` trong `~\.cache\chrome-devtools-mcp\<profile-của-mình>`.
  3. Gọi lại tool MCP (navigate_page) → server tự relaunch browser sạch (✅ verified). Vẫn kẹt → restart MCP server. Sau relaunch: navigate deep-link, kiểm login (session OAC thường còn sống).
  - ⛔ TUYỆT ĐỐI KHÔNG `Stop-Process chrome` toàn cục — cửa sổ khác thuộc session/người khác.
  - 📌 **Đọc đúng thông báo:** "browser already running" / "chrome đang bị process khác dùng" = **SingletonLock của user-data-dir ĐANG mở**, KHÔNG phải hết cổng. Mở một **profile khác**, hoặc dùng `--isolated`, LUÔN hợp lệ và **KHÔNG cần kill** gì. **TUYỆT ĐỐI KHÔNG kill Chrome global.**
- 📸 **Ưu tiên `take_snapshot` (text a11y) hơn `take_screenshot` (ảnh)** khi chỉ cần verify text/persist — ảnh phình context; screenshot chỉ khi cần soi pixel/màu render.

---

## 2. MỞ / ĐIỀU HƯỚNG WORKBOOK & SANDBOX

**Mở workbook có sẵn:** `navigate_page(URL reportpath)`. Pattern: `…/ui/dv/home.jsp?pageid=visualAnalyzer&reportmode=full&reportpath=<ENC>&viewermode=false`. Encode: space=`%20`, `/`=`%2F`, `@`=`%40`, `(`/`)` giữ nguyên. Nếu "Failed to Load" → path sai → vào `…/home.jsp?pageid=home` → snapshot → đọc thumbnail image URL (chứa path đúng) → ghép lại reportpath.
- URL DB01: `…?pageid=visualAnalyzer&reportmode=full&reportpath=%2F%40Catalog%2Fshared%2F(KGR)%201.Implement%2F(KGR)%20DB01.Revenue_v1.1&viewermode=false`

**✅ Tạo workbook MỚI (verified 2026-06-11):** `navigate_page("…/ui/dv/home.jsp?pageid=visualAnalyzer&reportmode=full")` (KHÔNG reportpath) → mở **Canvas 1** + dialog **"Add Data"** (KHÔNG mở tab 2 như dataflow). 
  - Chọn dataset nguồn: `fill` ô search "Type to refine the results press Enter to search" → Enter → poll kết quả → **double-click row tên dataset** (`click(uid_tên, dblClick=true)`; hoặc tick checkbox "Select Row" → nút "Add to Workbook"). Dataset vào → data panel hiện cột.
  - ⚠️ Nút **Create → Workbook** trên Home: MCP click có thể không mở dialog (synthetic nuốt) — dùng URL navigation như trên.

**✅ Sandbox (verified):** dùng `KGR_WB_SANDBOX_EXPLORE` (deep-link §0). Thử thao tác lạ ở đây, reload deep-link để reset. KHÔNG nghịch DB01 production.

**Lần Save đầu của workbook mới:** nút Save → dialog **"Save Workbook"** (Name + Description + Location, mặc định My Folders + nút "Save"). `fill` Name → click Save. (Lưu /users → KHÔNG hỏi share; lưu shared → dialog "Share Related Items", click OK — §13.)

---

## 3. BỐ CỤC EDITOR (verified 2026-06-11)
```
┌ TOOLBAR trên: Undo · Redo · [Save] (aria-label "Save menu", cái haspopup≠true) · [Save menu▾] · Add Note · ⋮ Workbook menu (Themes/Properties)
├ 3 MODE (radio, label.oj-button-label): • Data (chuẩn bị dataset/blend) • Visualize (dựng viz — mặc định) • Present (trình bày/preview)
├ TRÁI "Data Panel" (tab "Visualizations"/"Data"): ô "Search input field" (combobox autocomplete) + cây dataset→cột (treeitem level=2) + "Key Metrics" + "My Calculations" + "Value Labels". Nút "Menu" data-panel.
├ GIỮA-DƯỚI TABS CANVAS: [role=tab].bitech-rui-tab-item ("Canvas 1"...) + nút "Create Canvas".
├ GIỮA CANVAS: vùng thả viz. Mỗi viz = khối có hover-toolbar (Maximize Visualization · Menu ⋮) + title (RTE khi Custom). Filter Bar trên cùng canvas ("Add Filter" + "Filter Bar Menu").
└ PHẢI "Grammar/Properties Panel" (2 tab chính): • "Grammar" (shelves: kéo field) • "Properties" (sub-tab General/Edge Labels/Axis/Values/Filters/Advanced). Trên cùng panel: "Select Visualization Type" (đổi loại chart).
```
- Mode switch: tìm `label.oj-button-label` text `Data|Visualize|Present` → click label + set radio con checked + dispatch change.
- ⭐ **Viz mới phải dựng trên CANVAS TRỐNG** — double-click field trên canvas đã có viz sẽ MERGE vào viz đang chọn (verified). Muốn viz mới riêng → tạo canvas mới (trống) rồi thả field.

---

## 4. ⭐⭐ COMMIT / PERSIST — BẪY QUAN TRỌNG NHẤT (verified live 2026-06-11)

> Hiểu sai = mất title/note/cấu hình mà không báo lỗi, hoặc save HỦY.

### 4.1 TITLE viz Auto→Custom (PERSIST qua reload ✅✅)
1. Chọn viz (click leaf chứa text title: dispatch mousedown/up/click).
2. Grammar/Properties panel → tab **"Properties"** → sub-tab **General** → button **"Title Auto"** (snapshot grep `button "Title Auto"`).
3. ⚠️⚠️ **MCP-click THẬT (real CDP)** button đó → dropdown **Auto/Custom/None**. (Mở bằng script/jQuery thì menu hiện + click Custom có vẻ OK NHƯNG **KHÔNG persist** → revert Auto sau navigate.)
4. Click option **"Custom"** (jQuery/script OK *sau khi* đã real-open dropdown) → button đổi "Title Custom".
5. ⚠️ Title KHÔNG ở panel — nó thành **Rich Text Editor (CKEditor) INLINE TRÊN CANVAS** (snapshot grep `textbox "Rich Text Editor`), auto-focus, **pre-fill text auto** (vd "SL_Thuc_Te by Tên Ngành").
6. **dblClick RTE (uid)** → `press_key("Control+a")` → `type_text("<English Title>")` (REAL keyboard) → `press_key("Escape")`.
7. **Save** → reload deep-link → đọc lại title (✅ persist). Verify mode = "Title Custom".
- ⚠️ Select-viz và set-title là **2 thao tác riêng** (panel re-render async). Title đã-Custom-sẵn → set field thẳng (bỏ B3-4).
- ⚠️ **Title = TEXT TĨNH**, KHÔNG nhúng số/kỳ động. Số động → KPI Tile; kỳ → filter chip.
- **Phân biệt title vs non-title** (giữ VN, scope chỉ viz-title EN): `breadcrumb`/`bi_breadcrumbs_*`=drill; `bitech_legend_customSectionTitle`=legend; `bitech-shared-tile-*-label`=nhãn KPI tile; `dropTarget_token*`=chip; `[object SVGAnimatedString]`=axis SVG. Title thật = dropdown "Title Auto/Custom/None" panel General.

### 4.2 NOTE (annotation) tiếng Việt — TẠO MỚI chạy, SỬA text = WALL
- Tạo: nút toolbar **"Add Note"** → menu (Show Notes / **Add Note**) → click menuitem "Add Note" (script dispatch OK) → editor là **CKEditor** (`.ck-editor__editable`; ⚠️ doc cũ ghi TinyMCE = LỖI THỜI), auto-focus → **`type_text` nội dung VN** (dấu tiếng Việt OK) → **Escape** commit → toolbar đổi "Hide Notes". Save persist.
- ⚠️ **SỬA text note cũ qua DOM = WALL** (OAC giữ model riêng, DOM mutation revert kể cả real keyboard — verified lại 2026-06-17). ⭐ **CÁCH ĐÚNG để sửa/đặt-lại/xoá note (nhất là HÀNG LOẠT): sửa trong MODEL rồi POST projects/json (§13)** — `model.annotations.children[]` chứa text+vị trí; round-trip tin cậy, tránh cả wall này lẫn wall drag. (Cách cũ xoá+tạo-mới qua DOM vẫn được cho 1-2 note: right-click note → "Delete"; tạo mới spawn giữa canvas.)
- ⚠️ Note ra **GIỮA canvas**, không tự gắn viz → `drag(note_uid, chart_container_uid)` để neo; nhiều note CHỒNG nhau → **prefix nội dung note bằng TÊN CHART** để map đúng dù chồng. Toggle "Hide/Show Notes". Note = OVERLAY (đè chart khi Show).

### 4.3 SAVE & các thao tác mất-việc
- ⭐ **Save NGAY sau mỗi cụm thay đổi** (chống timeout/redirect → mất). Reload = discard mọi edit CHƯA lưu.
- **Save workbook shared folder** → dialog **"Share Related Items"** → ⚠️⚠️ **click "OK" (KHÔNG Escape — Escape HỦY cả lần Save**, đã từng mất nhiều canvas chưa-lưu vì lỗi này). OK = chỉ lưu workbook (không share gì nếu không tick item). Workbook /users → KHÔNG có dialog này. Verify persist: GET projects/json (§13).
- ⚠️ **Reorder CHIP trong shelf = WALL** (HTML5 DnD, `drag` no-op) → nhờ user kéo tay; hoặc delete+add (add luôn vào CUỐI → tile-slot đầu có thể mislabel).
- ⚠️ **Reorder/resize ô viz trong Auto-layout = WALL** → chỉ delete+create; reorder nhờ user.
- ⚠️ **Dialog stacking**: click Done/menu khi đang có dialog khác → stack nhiều dialog. Dọn = click Cancel/Done/Close lặp + Escape; verify `[role=dialog]:visible`=0.

---

## 5. TAXONOMY 59 LOẠI VIZ + SHELF (picker "Select Visualization Type", verified 2026-06-11)

**Tạo viz:** double-click field data-panel (1 dim → Auto Table; +1 measure → Auto Bar; 1 dim+2 measure → Auto **Scatter**). Hoặc kéo field → canvas/shelf. Hoặc nút Add Visualization. ⭐ Trên canvas trống mới được viz mới (canvas đông = merge).

**Đổi loại:** mở picker = click `*[class*=bi_viewselectorwidget_rootcontainer]` (dispatch mousedown/up/click) → 59 vizlink `.bi_vsd_vizlink` → click = `jQuery(link).trigger('click')` + `link.click()`.

**Chọn đúng dataset khi field trùng tên:** `fill(combobox "Search input field", 'tên field')` → autocomplete liệt kê field KÈM dataset → `click(uid_suggestion, dblClick=true)` đúng dòng đúng dataset. Field đầu = tạo viz; field sau = thêm vào viz đang chọn.

**59 loại (đầy đủ):** Auto · Bar · Stacked Bar · 100% Stacked Bar · Range Bar · Horizontal Bar/Stacked/100% Stacked/Range · **Combo** · Overlay Chart · Butterfly · **Waterfall** · Boxplot · Horizontal Boxplot · Gantt · Line · Area · Stacked Area · 100% Area · Range Area · Radar Line/Area/Bar · **Scatter** · Category · Stacked Category · Pie · Donut · Sunburst · **Treemap** · Pivot · Table · Correlation Matrix · **Grid Heat Map** · Picto · Network · Circular Network · **Sankey** · Tree Diagram · Chord Diagram · Parallel Coordinates · Dashboard Filters · Button Bar · Spacer · **Tile** · Map · **Gauge** · Language Narrative · Tag Cloud · List · Timeline · Legend · iFrame · Text Box · Image · **Funnel Plugin** · **KPI Tile Plugin** · **Liquid Fill Plugin** · **NineboxViz Plugin**.

⭐ **SHELF TAXONOMY (role=application aria-label):**
| Loại | Shelf nhận field (ngoài Trellis Cols/Rows · Tooltip · Filters) |
|---|---|
| **Bar / Stacked Bar** | Values(Y-Axis) · Category(X-Axis) · Color · Size(Width) · Detail |
| **Line** | như Bar + Shape |
| **Combo** ⭐ | Values(Y-Axis)[cả N measure] · Category(X-Axis) · Color · Size(Width) · Shape · Detail |
| **Waterfall** | Values(Y-Axis) · Category(X-Axis) · Color · Size(Width) · Detail (cầu nối tăng/giảm) |
| **Scatter** | Values(Y-Axis) · **Values(X-Axis)** · Category(Points) · Color · Size · Shape (4-layer) |
| **Butterfly** | Values(X-Axis) · Category(Y-Axis) · Color · Size (đối xứng 2 phía) |
| **Boxplot** | Values(Y-Axis) · Category(X-Axis) · Color · Detail(Box) |
| **Treemap** ⭐ | **Values(Box Size)** · **Category(Boxes)** · **Color** (size+color, vd size=Rev color=GP%) |
| **Pie / Donut / Sunburst** | **Values(Slice)** · Category · Color (Sunburst = phân cấp) |
| **Grid Heat Map** ⭐ | **Category(Y-Axis)** · **Category(X-Axis)** · **Color** · Values (heatmap 2 chiều thật) |
| **Pivot** | **Columns · Rows · Values** · Color · Size · Shape (cross-tab) |
| **Table** | cột (Grid) |
| **Tile (KPI)** ⭐ | **Values** · Category(Chart) (sparkline/segment) |
| **Gauge** ⭐ | **Values(Gauge) · Values(Target) · Values(Start) · Values(End)** (%đạt vs mục tiêu) |
| **Radar Line/Area/Bar** | Values(Radius) · Category(Angle) · Color · Size(Width) |
| **Sankey** ⭐ | **Category[nhiều dim = stage luồng]** · Color(Link) · Size(Link) |
| **Map** | Category(Location) · Color · Size · Shape |
| **Funnel / Liquid Fill Plugin** | Values · Category · Color (phễu / bình nước %) |
| **KPI Tile Plugin** | **Base · State · Target · Previous · Custom Currency** |
| **NineboxViz Plugin** | ma trận 9 ô (tăng trưởng × biên) |

**Map loại → use case C-level (Big4 Kangaroo):** Plan-vs-Actual → **Combo** (bar actual xanh + line plan xám) / Butterfly · AOP→Actual gap → **Waterfall** (xanh tăng, cam giảm) · cơ cấu+biên → **Treemap** (size=Rev, color=GP%) / Sunburst · mật độ Ngành×Kênh → **Grid Heat Map** · Rev↔GP%↔size → **Scatter** 4-layer · nhiều chỉ số chuẩn hóa → **Radar** · luồng Kênh→Chuỗi→Ngành → **Sankey**/Chord · phễu/xếp hạng → **Funnel** · %đạt nổi bật → **Liquid Fill/Gauge** · định vị danh mục → **Ninebox** · KPI chính → **Tile**+sparkline / KPI Tile Plugin.

---

## 6. GRAMMAR / SHELVES + THAO TÁC CHIP

- **Shelf = `[role=application]`** với aria-label = tên shelf. Pill measure/dim = `generic` con, description = `dataset > column`.
- **Thêm field:** kéo TỪ data-panel → shelf (ADD) HOẶC double-click (vào viz đang chọn). Kéo CHIP nội bộ grammar→shelf khác = SWAP/COPY.
- ⭐ **Chip menu (REAL click vào chip → menu):** options tuỳ loại: **Area/Bar/Scatter** (đổi series combo) · **Y2 Axis** (trục phụ) · **Sort By** · **Aggregate (Default)** (submenu Sum/Average/Minimum/Maximum/Count/Count Distinct) · **Create Filter** (⚠️ = CANVAS-level!) · **Number Format** (một số viz) · **Delete**. Synthetic KHÔNG mở menu chip → BẮT BUỘC `click` tool.
- ⭐ **COMBO plan-vs-actual:** thả 2 measure vào Values(Y-Axis) (mặc định cả 2 = Line) → click chip measure ACTUAL → "Bar" (thành cột xanh); measure PLAN giữ Line (xám). Footer "N Lines"→"N Series". Y2 Axis nếu thang đo lệch.
- **Aggregate cột:** chip → Aggregate (Default) → chọn. ⚠️ Cột định danh (ID) đặt **Maximum**, KHÔNG Sum (Sum làm sai).
- ⚠️ **Reorder chip = WALL** (§4.3).

---

## 7. PROPERTIES (sub-tab: General · Edge Labels · Axis · Values · Filters · Advanced)

- **General:** Title (Auto/Custom/None — §4.1) · Title Tooltip · Treat Nulls as (Gap/Zero) · **Legend Position** (Auto/Top/Bottom/Left/Right) · Legend Max Size · **Legend Title** (Auto/Custom/None) · Legend Title Font.
- **Edge Labels = DATA LABELS:** bật/tắt nhãn giá trị trên cột/điểm, vị trí, font.
- **Axis:** min/max (scale), axis title, tick. ⚠️ **Baseline trục = 0** (zero-baseline) để không gây hiểu nhầm.
- ⭐ **Values (per-MEASURE):** mỗi measure có **Number Format** (Auto/Number/Currency/Percent) · Tooltip Number Format · **Aggregation Method** · **Y2 Axis**.
  - **Number Format** → chọn **Number** → lộ: **Thousand Separator** (1,234) · **Decimal Places** (0) · **Abbreviate (1000=1K)** = **Off/K/M/B** · **Negative Values** (-123).
  - 📌 **MONEY** = Number, Decimal=0, **Abbreviate=M** (triệu). **KHÔNG abbreviate cho QUANTITY/Volume** (đơn vị, không phải VND). **RATIO** = Number Format **Percent**, Decimal=0 (%GP Ròng phải "27%" KHÔNG "0.27"). Per-viz, per-measure (không có workbook default).
  - Mở các button dropdown bằng MCP-click như Title.
- **Reference / Trend line:** viz hover-Menu → **"Add Statistics"** → Reference Line / Trend Line / Cluster / Outlier... (vd vẽ vạch AOP/mục tiêu).
- **Conditional Formatting:** nút **"Conditional Formatting"** (toolbar viz) → rule (Color Scale / Threshold). Bảng %GP: 3 steps red `#F16522`(<0) / amber(0–0.2) / green `#44BA46`(≥0.2). Bold header/cột key.
- ⚠️ Number Format per-column TRONG BẢNG: chỉ set được ở Data Element (dataset-wide) — không có ở pill menu/Properties bảng. Cần user duyệt nếu đụng dataset chung.

---

## 8. MÀU & BRANDING KANGAROO

📌 **Palette Kangaroo (hex CHÍNH XÁC):**
- **Green `#44BA46`** = actual revenue / positive / margin / hàng Xanh.
- **Orange `#F16522`** = cost / gap / alert / AOP / khuyến mãi CKKM / hàng Đỏ.
- **Gray `#636466`** = plan (SFC/AOP) / neutral baseline.
- **Dark green `#008242`** · **Light gray `#E6E7E8`** (sequential ramps) · **White `#FFFFFF`** bg.
- ⚠️ Sai cũ: `#44B446`. Semantics PHẢI giữ: orange=cost/gap, green=margin/revenue, gray=plan.

⭐ **Set màu SERIES (workbook-level, verified 2026-06-11):**
1. Hover viz → viz hover-toolbar (cạnh nút "Maximize Visualization") nút **"Menu"** → **MCP-click** (real CDP) → menu (Sort By/Use as Filter/Add Statistics/Conditional Formatting/**Color**/Edit/Export/Delete Visualization/Select All).
2. Hover+click **"Color"** → submenu **"Manage Assignments..."** (+ "Reset Visualization Colors").
3. ⚠️ Submenu Color → "Manage Assignments..." **dễ tự đóng**: hover "Color" + click "Manage Assignments..." nên làm **TRONG CÙNG 1 evaluate pass** + dispatch event KÈM toạ độ (`clientX/Y` từ getBoundingClientRect) — gọi tách lẻ thì submenu sập trước khi click.
4. Dialog **"Manage Color Assignments"**: link palette "Default ( Redwood )" + grid **"Series ( Measures )"** (mỗi series = 1 row generic, vd `SL_Thuc_Te`) + nút "Reset Series Colors" + **"Done"**.
5. **Click ROW series** (không phải text) → mở **color picker inline**: 12 swatch palette + ô **textbox hex** (aria-label = tên series, value `#xxxxxx`) + nút **"OK"**.
6. ⚠️⚠️ **PHẢI: `fill(hex_textbox, "#44BA46")` (real keystroke) → click nút "OK" THẬT.** Set hex bằng native-setter/Enter mà KHÔNG bấm "OK" thì **KHÔNG commit** (render giữ màu cũ — đây là bẫy: đọc lại value ô input thấy đúng hex nhưng series KHÔNG đổi màu → false-positive). Verify bằng **screenshot/render**, KHÔNG bằng giá trị input. (verified 2026-06-11; supersede ghi chú cũ "set hex + Done")
7. Lặp B5-6 cho từng series (uid grid đổi sau mỗi OK → re-snapshot). Xong tất cả → **"Done"** đóng dialog.
- ⭐ **Workbook-level**: set 1 series áp MỌI viz dùng series đó. NHƯNG mỗi (measure × dataset) = **entry RIÊNG cùng tên** → set HẾT. Kangaroo: actual=#44BA46, plan=#636466.
- ⚠️ Khi measure dùng làm **Color gradient** (stepped) → swatch hiện "Stepped Color" + "Number of steps"; đó là gradient, khác màu series rời rạc.
- **Theme:** Workbook ⋮ (top-right) → Properties/Themes (workbook-wide).

⭐⭐ **Tô màu TỪNG CỘT / 1 DATA POINT (right-click bar → Color → Data Point) — verified 2026-06-18, P&L waterfall:**
- **Khi nào dùng:** muốn mỗi cột 1 màu theo ý nghĩa (vd waterfall: doanh thu/lợi nhuận XANH, chi phí CAM). **Range Bar (manual waterfall) KHÔNG nhận Color dimension** (đưa bất kỳ trường nào vào shelf Color → vỡ chart, rớt hết bar chỉ còn 1) và **Conditional Formatting KHÔNG tô được thân Range Bar** → **per-data-point là cách DUY NHẤT** tô màu theo chiều cho Range Bar.
- **Thao tác (UI người dùng):** **right-click ngay trên THANH (bar)** cần tô → menu chuột phải → **Color** → submenu: **"Series (<measures>) ..."** (cả series, 1 màu nền) · **"Data Point (<tên cột>) ..."** (CHỈ cột đó) · "Manage Assignments..." · "Reset Visualization Colors" · "Stretch Palette". Chọn **"Data Point (<tên>) ..."** → dialog color picker (12 swatch sẵn gồm `#44ba46`/`#f16522`/`#636466` + ô **hex textbox** + **OK**) → set màu → OK.
- **Chiến lược ÍT THAO TÁC:** set **Series = màu nền** (vd xanh) cho cả 14 cột trước, rồi **override từng Data Point** sang màu kia (vd cam) cho nhóm thiểu số. **Per-data-point override THẮNG màu series** (set series sau cũng không xoá override đã đặt).
- **Automation (Chrome MCP):** bars render là **`<polygon>`** trong `[aria-label*="Data Visualization: Chart"]` (fill là **hex** `#88A03E`/`#F16522` HOẶC **rgba** `rgba(68,186,70,1)` sau khi set series → match cả 2 dạng; cột floating có 3 lớp: nền `#5A5A5A` + trắng `#FFFFFF` + **front màu** → lọc lấy polygon w≈70-85, fill KHÁC transparent/white/gray). `cx` của polygon (getBoundingClientRect) trái→phải = thứ tự category.
  1. `dispatchEvent` **contextmenu** (button:2, kèm `clientX/clientY` = tâm polygon) lên đúng polygon → menu render **ASYNC** (await ~300ms).
  2. hover menuitem **"Color"** (mouseover) → await ~150ms → JS-click **"Data Point (...)"** (JS-click trên item **Color-submenu** ĂN; khác menuitem cấp-1 phải MCP-click theo uid).
  3. picker render (await ~300ms) → set hex bằng **native-setter** `input.value` + click swatch khớp hex + **click "OK" THẬT** (không OK = không commit, y như series).
- ⚠️⚠️ **BẪY "selection sticky":** menu **"Data Point (X)"** phản ánh điểm ĐANG CHỌN, KHÔNG chắc là cột vừa right-click (đôi khi giữ điểm cũ). → **LUÔN verify** chuỗi `Data Point (<tên>)` khớp tên cột mong muốn TRƯỚC khi đổi màu; lệch → `document.body.click()` bỏ chọn + thử lại (left-click chọn rồi right-click; retry 2-3 lần). Verify màu cuối bằng **screenshot/đọc fill polygon**, KHÔNG bằng input.
- ✅ Kết quả verified: waterfall P&L 14 cột — series nền xanh `#44ba46`, override 7 cột chi phí sang cam `#f16522`; mỗi data-point override persisted qua Save + reload.
- ⭐⭐ **Data-point color override = WORKBOOK-LEVEL, key theo (CỘT × GIÁ TRỊ) — KHÔNG phải chỉ GIÁ TRỊ (SỬA LẠI 2026-06-18 #2, supersede ghi chú "tự ăn màu" trước):** override lưu ở `reportConfig.settings["oracle.bi.tech.colorSchemeService"].settings.colorDomains`, key = chuỗi `["obitech.colorcategory.value","datapointSchemes","<columnID>"]` → `colorMap{<value>:<hex>}`. **Key theo COLUMN ID** (vd scheme `"Bridge_Label"` cho bản Tập đoàn) — viz dùng **columnID KHÁC** (vd bản ngành tạo cột mới `"Bridge_Label_1"`) **KHÔNG ăn màu** dù value trùng chuỗi. Màu nền (series) cho Range Bar = key đo `["cum_after_3","cum_before_2"]` trong scheme `categoricalSchemes,"[]"`. ⇒ **Clone waterfall sang viz mới (columnID mới) PHẢI thêm scheme mới**: (a) `categoricalSchemes."[]".colorMap["<cum_after_X>","<cum_before_Y>"]="#44ba46"` (xanh nền 14 cột); (b) `datapointSchemes."<Bridge_Label_X>".colorMap` = 7 nhãn chi phí→`#f16522` (clone từ scheme gốc). **NHƯNG nếu nhiều viz DÙNG CHUNG 1 columnID** (vd clone canvas bằng model-save reuse `Bridge_Label_1`) thì share scheme → set 1 lần, các clone ăn màu free. (Verified khi dựng Range Bar ngành: bars hiện màu OLIVE mặc định, KHÔNG xanh/cam, tới khi thêm scheme cho `Bridge_Label_1`.)

---

## 9. FILTER (verified 2026-06-11)

- **Canvas-level (mọi viz trên canvas):** nút **"Add Filter"** (toolbar Filter Bar) → column picker (cây dataset) → click cột → chip **"<col> Filter. N selected values."** trên filter bar.
- **Mở chip** (jQuery click / `[aria-label^="<col> Filter"]`) → popup:
  - **dim string** → tab **List** / **Top Bottom N** + **Exclude** + Limit Values + Disable Filter + Nulls. List = shuttle: **dblclick** Available→Selections (hoặc "Add (N)"); bỏ = dblclick Selections; "Clear". Áp **live**. Đóng = **Escape** (GIỮ lựa chọn, không hủy).
  - **số** → Range; **ngày** → Date range.
- **Top-N viz-level:** category pill → "Create Filter" → tab **"Top Bottom N"** → Method=Top, Count, **By = Select Measure**. **Exclude 1 giá trị:** tick **"Exclude"** → click value (vào Exclusions) — dùng bỏ "Khác"/"~No Value~".
- ⚠️ **"Create Filter" từ chip menu = CANVAS-LEVEL** (mọi viz)! Muốn filter **CHỈ 1 viz** → KÉO cột data-panel vào shelf **"Filters"** của viz (mọi viz đều có). ⚠️ Kéo cột thứ 2 vào Filters có thể ĐÈ filter cũ → drop vùng trống, verify kỹ.
- **Filter Bar Menu** (▾): Limit Values By · Show/Hide All · Clear All · Remove All · **Create Expression Filter** (boolean, vd `"PERIODNAME" IN('May 2026')`) · Auto-Apply Filters.
- ⚠️ **Blend nhiều dataset/nhiều trục thời gian → DÙNG column filter (dataset-scoped), TRÁNH expression filter** (áp global → dataset thiếu cột bị NULL sạch → viz 0 rows).
- **Exclude "Khác"/"~No Value~"**: tại VIZ level (filter category→Exclude→click Khác), **KHÔNG canvas-level** (rơi total KPI).

---

## 10. CALCULATION / EXPRESSION (workbook)

- Data panel → right-click **"My Calculations"** (dispatch contextmenu button:2 OK) → **Create Calculation...** · Create Time Series Calculation... · Create Group Calculation... · Create/Rename/Delete Folder.
- Dialog **"New Calculation"**: **Name + Description + expression editor (contenteditable) + Save/Cancel**, cây hàm 7 nhóm: **Operators · Aggregate · String · Math · Conversion · Expressions · Analytics**.
- ⚠️ **Chèn cột bằng autocomplete token** (gõ phần đầu tên → dropdown → click token); **ĐỪNG gõ literal `"Tên cột"`** → coi là string → syntax error. Ref đầy đủ: `XSA('minhndn@bizin.vn'.'__DATASET__')."Columns"."COL"`.
- Calc lưu trong **workbook** (My Calculations) — khác calculated-column ở tầng dataset/dataflow.
- ⚠️ My Calculations tree expand qua MCP đôi khi không ổn định → nếu cần đọc/sửa calc có sẵn, nhờ user double-click mở, agent đọc/sửa trong dialog.
- ⭐ **Set expression qua CodeMirror:** dialog "New Calculation" có Name textbox (set bằng `fill` real-keyboard) + editor CodeMirror (set bằng `document.querySelector('.CodeMirror').CodeMirror.setValue(expr)` — ăn ngay, ref cột full `XSA('owner'.'ds')."Columns"."col"` resolve đúng) + Validate + Save. (verified 2026-06-18 #2)
- ⚠️⚠️ **FILTER cross-group ratio HỎNG khi viz GROUP theo dim đó (verified 2026-06-18 #2, TD_Report_Long):** calc `Actual / FILTER(Actual USING Metric_Name='Doanh thu')` đặt làm measure trong viz **Category=Metric_Name** → trả NULL cho MỌI dòng trừ 'Doanh thu' (=1). Lý do: OAC scope FILTER theo group hiện tại; dòng Metric≠'Doanh thu' thì USING Metric='Doanh thu' rỗng → null → x/null=null. **FIX KHÔNG cần dataflow:** (a) tỷ lệ dùng làm **KPI TILE / scalar** (KHÔNG group theo Metric_Name) → cả tử & mẫu FILTER tính ở report-level → ra đúng scalar (vd biên ròng = FILTER(AA Metric='LN sau thuế')/FILTER(AA Metric='Doanh thu') = 9.9% ✓); (b) viz "biên % theo bậc" = **N calc scalar riêng** (Bien_LN_gop, Bien_LN_truocthue…) plot multi-measure (KHÔNG dùng 1 calc + Category=Metric_Name); (c) per-row ratio cùng dòng (vd Actual/AOP_Amount_1) thì OK vì không cross-group. Chỉ khi cần ratio cho NHIỀU dòng trong 1 viz grouped (vd cơ cấu 12 chi phí theo %DT) mới cần **dataflow thêm cột Pct_of_Revenue thật** (broadcast Doanh thu/AsOfDate) — hoặc hiển thị tuyệt đối M.

---

## 11. NOTE TIẾNG VIỆT (chi tiết — xem cơ chế ở §4.2)

- **Quy ước nội dung note** (mỗi viz 1 ô): (1) viz cho thấy gì → (2) hàm ý kinh doanh → (3) điểm đắt giá → (4) liên kết viz lân cận. 2–4 câu, tiếng Việt, ghi kỳ dạng "Tháng 5/2026" (chữ, KHÔNG nhúng mã POSTINGPERIOD cứng — kỳ đổi là lỗi thời). Prefix tên chart để map khi nhiều note.
- **Flow 4 call:** MCP-click "Add Note" toolbar → script-click menuitem "Add Note" → `type_text` VN → `press_key Escape`. Save persist.
- Định vị: `drag(note StaticText uid, chart container uid)`. Toggle "Hide/Show Notes".

---

## 12. CANVAS & LAYOUT

- **Tạo canvas:** nút **"Create Canvas"** → tab "Canvas N" mới, TRỐNG (dựng viz mới sạch ở đây).
- **Rename canvas:** double-click tab → inline input → native setter + input/change → Enter / click `span.bi-va-icon-check_16`.
- **Đổi canvas:** click `[role=tab].bitech-rui-tab-item` text = tên (dispatch mousedown/up/click + .click()).
- **Reorder/xoá canvas:** tab context menu (right-click tab).
- **Layout Auto vs Freeform:** Auto = lưới tự xếp (reorder/resize ô = WALL); Freeform = đặt tự do. Mỗi ô viz có Width/Height/X/Y (Properties → khi chọn viz).
- **Bố cục C-level:** cap **~6 KPI/canvas** (Stephen Few); tab order overview→detail; **đa dạng loại chart** mỗi canvas (1 combo + 1 treemap/heatmap + 1 scatter/radar + 1 KPI + 1 bảng — đừng 5 bar giống nhau); baseline trục=0; ratio tách absolute.

---

## 13. SAVE / PERSIST + REST projects/json + ĐỌC SỐ VIZ

- **Save:** click button aria-label="Save menu" (cái `aria-haspopup`≠'true') → toast "The workbook was successfully saved" + "Last Saved H:MM". Shared folder → dialog "Share Related Items" → **OK (KHÔNG Escape)** (§4.3).
- ⭐ **Verify persist / AUDIT model — GET projects/json:** `GET /ui/dv/ui/api/v2/projects/json?path=<urlenc>` headers `{authorization:'session', x-requested-with:'XMLHttpRequest'}` credentials:'include'.
  - ⚠️ **Encoding KHÔNG nhất quán giữa workbook** (verified 2026-06-17): có workbook trả **double-encoded** (chuỗi `"{\"criteria...}"` → `JSON.parse` 2 lần), có workbook trả **plain object** (parse 1 lần). → parse PHÒNG THỦ: `let m=JSON.parse(txt); if(typeof m==='string') m=JSON.parse(m);`.
  - Cấu trúc: top keys `criteria, layouts, views, datasources, reportConfig, parameters, eventWiring, **annotations**, snapshots, stories`. `views.children[]` (flat) — **canvas** = node có `viewName:"canvas!N"` + `rootLayoutName` + KHÔNG `pluginType` (tên = `viewCaption.caption.text`); **viz** = node có `pluginType` + `viewCaption`. **Vị trí viz**: `layouts.children[]` (1 layout/canvas, khớp `rootLayoutName`); leaf có `content.viewName` + `left`/`top` (PX). `datasources` regex `XSA\('owner'\.'(name)'\)`.
  - Verify: đếm canvas/annotation, search text, last-modified mới hơn. ĐỪNG tin toast một mình.
- ⭐⭐ **SAVE workbook qua REST = POST projects/json (verified 2026-06-17, round-trip OK)** — sửa/audit model bằng code, KHÔNG cần thao tác UI:
  - `POST /ui/dv/ui/api/v2/projects/json?path=<urlenc>` headers `{authorization:'session', x-requested-with:'XMLHttpRequest', 'x-csrf-token':<token>, 'content-type':'application/json; charset=UTF-8'}` credentials:'include'.
  - Body wrapper: `{"name":"<tên wb>","tags":[""],"description":"","reportSaveInfo":{"lastModifiedTimestamp":<ts>,"lastModifiedUserName":"<tên>"},"json":"<MODEL stringified>","overwrite":true}`. `json` = model JSON.stringify (chuỗi). Response `{success:true, lastModified:{timestamp}}`. (Supersede ghi chú cũ "POST=Logic Error" — đó là POST THIẾU body.)
  - `lastModifiedTimestamp`: lấy từ `GET /ui/dv/ui/api/v2/items?path=<enc>&projectType=auto&{}` → field `lastUpdatedTime`. `x-csrf-token`: lấy từ header 1 XHR trước (capture qua list/get_network_request POST save), thường bền trong phiên. `overwrite:true` ghi đè.
  - **Pattern an toàn**: GET model (parse phòng thủ) → mutate in-place → POST. **TEST trên SANDBOX trước khi đụng production** (đã verify round-trip annotation trên KGR_WB_SANDBOX_EXPLORE). Dry-run khớp/đếm trước khi POST. Backup model (lưu GET ra file) trước.
- ⭐⭐ **NOTE/ANNOTATION nằm trong model → SỬA TEXT + VỊ TRÍ qua model-save (verified 2026-06-17) — TRÁNH cả wall sửa-text-DOM lẫn wall drag:**
  - `model.annotations.children[]`: mỗi note `{id, scopeRef:"canvas!N", type:"text", note:"<p>HTML</p>", isHidden, top:"<N>%", left:"<N>%", width, height, showConnectorLine, dataReferences:null}`. `scopeRef` = canvas chứa note; `top`/`left` = % canvas; `showConnectorLine:false` để bỏ đường nối thừa.
  - **Sửa hàng loạt**: GET model → với mỗi annotation, match (theo `scopeRef` + text cũ chứa substring unique, hoặc theo `id`) → set `.note` (HTML mới) và/hoặc `.top/.left` (%) → POST. **Xoá note** = bỏ khỏi children. Khớp 1-1 (dry-run đếm) tránh va chạm substring.
  - ⚠️ Sửa text note tại chỗ qua DOM (mở editor + gõ) VẪN REVERT (wall #A còn đúng — OAC dựng lại từ model); **model-save là cách đúng để sửa note**. Đặt note đúng-chart pixel-perfect vẫn nên kéo tay (note đặt ban đầu bằng mắt; px→% không có công thức sạch) — model-save để de-stack + đưa về đúng vùng, user nudge tinh.
- ⭐ **Đọc SỐ THẬT của viz (cho VERIFY):** `list_network_requests({resourceTypes:["xhr","fetch"]})` → tìm POST **`/ui/dv/ui/api/v2/data/executeOrPoll`** mới nhất của viz/canvas → `get_network_request(reqid, responseFilePath=<file>)` → **Read FILE** (đừng inline — dump cookie).
  - Request body = `saw:report` XML (criteria + columns formula `XSA(...)."Columns"."col"` + dataModel edges). Header có `x-csrf-token` (lấy nếu cần POST tự craft).
  - Response (✅ verified 2026-06-11): `report.views[viewKey][dmKey].edges[]` — edge category có `ed[0].s[]` = giá trị dim (`a`=label, `s`=index); edge measure `ed[0].s[]` = tên measure. **`data[]` = mảng per-CATEGORY (đúng thứ tự edge category); mỗi phần tử = mảng per-measure `{id, r:"<số THẬT>"}`** (`r`=giá trị, rỗng `""`=null). `keys`=[colID...]. Tổng = cộng `r` qua category. (vd combo SFC: data[i]=Water → mỗi measure có `r="<số THẬT>"` cho SL_Thuc_Te / SL_Ke_Hoach — đọc live, KHÔNG chép số kỳ cũ.) Chính xác hơn đọc SVG.
- **Reload Data (workbook nhận cột mới của dataset do dataflow re-run):** workbook KHÔNG thấy qua Refresh/Replace/reopen → catalog → phải-chuột tile dataset → **"Reload Data"** → reopen workbook.
- **Add Dataset vào workbook:** Data mode → "Add Dataset" → dialog → double-click dataset (profiling 30–60s, đừng tưởng hang; multi-select KHÔNG bền qua đổi search → add từng cái). Save ngay.
- **Blend (Data Diagram):** Data mode → tab "Data Diagram" → badge số trên connector = số cặp match → double-click badge → dialog "Blend Data" (NAME↔Tên Chuỗi...) Add/Delete Match/OK.

---

## 13b. ⭐ DỮ LIỆU KGR — SỐ THAM CHIẾU · DATASET/GRAIN · CHẨN ĐOÁN SỐ SAI (tự chứa)

> Kiến thức môi trường để VERIFY viz (KHÔNG phải task của dashboard cụ thể nào). Kỳ chuẩn hiện dùng = **May 2026** (POSTINGPERIOD tra động, vd Mar/Apr/May là 3 kỳ liền); khi kỳ đổi thì **mọi số phải LẤY LIVE lại**, KHÔNG tái dùng số kỳ cũ. Khi user giao 1 dashboard cụ thể, đọc state thật qua projects/json (§13) + số live qua executeOrPoll/NSAW — đừng giả định, đừng "verify kỳ mới bằng số kỳ cũ".

**📌 SỐ THAM CHIẾU = CÔNG THỨC + NGUỒN + "LẤY LIVE" (owner cấm lưu số tuyệt đối vào KB — số kỳ cũ đóng-băng gây wall ảo). Khi verify: chạy công thức trên kỳ đang xét, đừng chép số dưới đây (đã bỏ số).**
- **Doanh số thực tế (kỳ):** `SUM("Doanh số thực tế")` trên `(KGR) DTF_CALC_INVOICE_MEMO_#` lọc `PERIODNAME=<kỳ>`; đối chiếu NSAW `SUM(BASE_CR−BASE_DB)` (crosscheck agent, exclude SC=14). ⚠️ Scope MEMO# rộng hơn NSAW (chênh vài % do def) — LẤY LIVE cả hai rồi so, đừng gán số cứng. **Quy đổi** = doanh số × hệ số quy đổi (tra live).
- **Theo ngành (mix %):** `SUM("Doanh số thực tế") GROUP BY "Tên Ngành"` (Water/Home/Cold & Hygen) → tự tính tỷ trọng; LẤY LIVE (mix đổi theo kỳ).
- **Green/Đỏ (Xanh/Đỏ) %:** `SUM("DS Xanh")/SUM("Doanh số thực tế")` vs phần Đỏ. **%GP Ròng** = cột `"%GP Ròng"` (đã = %LN Gộp − CKKM Per). Watch-item cấu trúc: **gross > net vì CKKM bào mòn ~1/3 lãi gộp** (mô tả THIẾT KẾ — giữ; con số % LẤY LIVE). **SP mới %** = `SUM("Doanh thu SP mới")/SUM("Doanh thu thực tế")`.
- **Branch (Đơn vị) %:** `SUM("Doanh số thực tế") GROUP BY CASE Tên Đơn vị LIKE '%HCM%' THEN HCM ELSE VU1` → tỷ trọng VU1/HCM; LẤY LIVE.
- **SFC Plan (sản lượng, DW_SFC, single-period):** `Plan QTY = SUM(SL W1..SL W5) GROUP BY Ngành hàng` trên `DW_SFC` lọc `PERIODNAME=<kỳ>` (Water/Home/Cold); tổng plan qty = tổng 3 ngành. Plan REV ex-VAT = `SUM("Doanh thu (-VAT)")` cùng filter. **get_sfc_report(period=<p>)** cho golden. (số LẤY LIVE.)
- **SFC Actual (MEMO# scope):** `SL_Thuc_Te = 0 − SUM("QUANTITY")` (QUANTITY âm — invoice sign; đã net credit, KHÔNG ABS) trên `(KGR) DTF_CALC_INVOICE_MEMO_#` lọc 1 kỳ, GROUP BY Ngành. Achievement = actual/plan (LẤY LIVE).
- ⭐ **GOTCHA THIẾT KẾ (giữ — KHÔNG phải số):** Actual MEMO# = **MỌI SKU** (item-scope rộng); golden `get_sfc_report` = **chỉ item trong SFC plan scope** (`qty_count_flag=1`). Chênh **item-scope, KHÔNG phải bug** — KHÔNG có MEMO# column-filter nào khớp golden scope; đừng "sửa". Nếu dùng MEMO# → nhãn "Tổng SL hóa đơn (mọi SKU)", đừng gọi "% đạt KH SFC".
- ⚠️ **SFC DOANH THU KHÔNG TIN** (phần lớn dòng giá=0) → chỉ dùng SẢN LƯỢNG cho SFC.

**📌 DATASET & GRAIN (cột để thả shelf):**
- **`(KGR) DTF_CALC_INVOICE_MEMO_#`** (actual, May 2026; owner **anhdk@bizin.vn**; cột UNQUALIFIED, ~64 cột): dims `"Tên Ngành"` · `"Nhóm SP"` · `"Model name"` · `"Tên Chuỗi"` (BIGC/DMX/MM/Caophong/FPT/VHC/Nguyenkim/Thongnhat). measures `"QUANTITY"` (**ÂM** — invoice sign; actual qty = −SUM) · `"Doanh thu thực tế"`/`"Doanh số thực tế"` (VND) · `"GP %"` · `"%GP Ròng"` (decimal → format Percent!). keys `"ITEM"`,`"ID CLASS"`,`"PERIODNAME"`,`"POSTINGPERIOD"`,`"TYPE"`(CustInvc/CustCred),`"CUSTCOL_SCV_LINE_ISFREEGIFT"`. Canvas dùng: Overview/PROD/CHAIN/CHANNEL/BRANCH.
  - ⚠️ **MEMO# KHÔNG có grain KÊNH** ("Nhóm Kênh"/"Tên Kênh" NULL → 1 bucket) → Plan-vs-Actual theo Kênh KHÔNG làm được (actual N/A). CÓ grain Chuỗi (~24–76% doanh thu chưa gắn chuỗi → bucket "Khác", Exclude khỏi viz).
  - ⚠️ Readability **INTERMITTENT** (ORA-00942 / ORA-28000 anhdk khoá là TRANSIENT) → validate-first; ORA-28000 chặn viz query live dataset mới-add (§14).
- **`KGR_DS_SFC_vs_MEMO_v2`** (đã gộp sẵn, owner minhndn, **đọc ổn định**; grain Tên Ngành): `Tên Ngành`/`Ngành hàng`, `SL_Thuc_Te` (actual qty, dương), `SL_Ke_Hoach` (plan qty), `DT_Ke_Hoach`, `SL W1..W5`, `QUANTITY Sum`, `Doanh thu thực tế Sum`. = dataset chuẩn cho **combo SFC plan-vs-actual** (sandbox + có thể add vào DB01). (v3 thêm grain Nhóm SP.)
- **`DW_SFC`** (datamodel, owner **viethl@bizin.vn**, cột QUALIFIED): Ngành `"DW_NS_X_CAM_CUSTOMRECORD_CSEG_SCV_PRODCATG"."Ngành hàng"`; Nhóm SP `"DW_NS_X_CAM_CUSTOMRECORD_CSEG_SCV_PRODGROUP"."Nhóm sản phẩm"`; Plan qty = SUM(`SL W1..W5`) (KHÔNG có cột tháng); Kênh `"DW_NS_X_SALE_CHANNEL"."Kênh"` (8 kênh — tổng plan qty theo Kênh = tổng theo Ngành, LẤY LIVE); Period `"DW_NS_ACCOUNTINGPERIOD_D"."PERIODNAME"`.
- **ASM/CUSTOMER** → `DW_X_SALE_HISTORY` (all-history, TRANSACTION_DATE — KHÔNG filter PERIODNAME, tag "All-Time"). **AOP** → `Daily_*_Report` + `DW_AOP`/`AOP_UPDATE`.
- **NSAW cross-check (crosscheck agent):** Revenue = `SUM(NVL(BASE_CREDITAMOUNT,0)−NVL(BASE_DEBITAMOUNT,0))` trên DW_NS_CUSTOMER_INVOICE_LINES_F, POSTING='T', TYPE IN(CustInvc,CustCred), Income, **exclude internal SC ID=14**. AOP keyed CUSTBODY_SCV_AOP_LOAI_BAO_CAO (Summary=2,3; Daily TĐ=5; Daily Ngành=4; ⚠️ **TĐ(LOAI 5) ≠ Σngành(LOAI 4)** by design, đừng coi là bug).

**📌 BẪY SỐ TRÊN VIZ & CÁCH CHẨN ĐOÁN (master diagnostics — khi 1 viz hiện số sai):**
> Số trên viz lệch nguồn thường KHÔNG do build sai thao tác mà do 5 lớp nghĩa-dữ liệu. Đọc số THẬT qua executeOrPoll (§13), đối chiếu nguồn (NSAW/golden/số tham chiếu trên), rồi truy theo bậc thang:
1. **Fan-out (số nổ 2–5×, thường ở measure actual khi blend/join nhiều kỳ):** thiếu **filter single-period** trước aggregate/join → SUM cộng nhiều kỳ; HOẶC join many-to-many. Triệu chứng: tổng = bội số ~N kỳ của giá trị đúng. Sửa: filter 1 kỳ trước, hoặc dùng dataset đã pre-join 1 grain. (Đếm rows trước/sau join để xác nhận.)
2. **Aggregate sai function (số quá nhỏ/quá to ở measure kế hoạch/lặp):** cột kế hoạch/coarse-grain lặp per-row → để **Sum** thì phồng, để **Max/Avg** thì hụt. Cột nên Sum (sản lượng tổng) bị set Max/Avg → ~1/N giá trị đúng. Cột định danh (ID) phải Max. Kiểm chip → Aggregate (Default).
3. **Sai scope/filter dataset:** viz lấy từ dataset/kỳ khác (all-history vs 1 kỳ), hoặc filter canvas-level rơi mất rows. Xác nhận subjectArea + filter trong request executeOrPoll.
4. **Ratio "vỡ" / decimal chưa format:** %  hiện `0.27` (chưa Percent) hoặc `297%` (denominator nhỏ/blank). Sửa Number Format Percent + lọc blank-denominator (§7).
5. **Tỷ lệ kéo theo:** Achievement/% = tử/mẫu — nếu tử bị fan-out + mẫu bị Max thì % sai kép; sửa 2 measure gốc thì % tự đúng.
- ⚠️ **2 viz mâu thuẫn nhau trên cùng workbook = dashboard KHÔNG ship được** → truy viz nào sai theo 5 bậc trên, đối chiếu nguồn, KHÔNG đoán.
- ⭐ **Sửa viz số sai = ưu tiên ADD-only**: dựng viz/canvas MỚI đúng rồi để/ẩn cái cũ, hơn là sửa in-place (viz cũ có thể share dataset/blend với viz khác — sửa dễ vỡ lan). Verify lại bằng số sau sửa.

---

## 14. WALLS & WORKAROUND
| Wall | Workaround |
|---|---|
| Sửa text NOTE cũ (annotation) — script revert | Xoá (right-click→Delete) + tạo note mới (§4.2) |
| Set Title Auto bằng setter/script-open dropdown → revert | MCP-click dropdown THẬT → Custom → RTE canvas real keyboard (§4.1) |
| Reorder CHIP trong shelf | Nhờ user kéo tay; hoặc delete+add (add vào cuối) |
| Reorder/resize ô viz Auto-layout | delete+create; reorder nhờ user |
| Escape trên "Share Related Items" → HỦY save | Click OK (§4.3) |
| Number format per-column trong bảng | set ở Data Element (dataset-wide), cần user duyệt |
| My Calculations tree expand không ổn định | nhờ user mở calc, agent đọc/sửa trong dialog |
| Create→Workbook trên Home không mở dialog | navigate URL `reportmode=full` (§2) |
| Aggregate source-column picker (dataflow) | xem OAC_DATAFLOW_MASTERY.md |
| Add Data "Add Selected" trên dataflow đã lưu | xem OAC_DATAFLOW_MASTERY.md |
| ORA-28000 (anhdk khoá) chặn VIZ query dataset mới-add | reload dataset 1 lần lúc account khoẻ để có cache; KHÔNG burn retry (không transient) — shelve+note |
| MEMO# readability ORA-00942 | INTERMITTENT — validate-first executePreview; KHÔNG pre-assume hỏng |
| get_network_request dump cookie khổng lồ | luôn responseFilePath rồi Read file |
| wait_for editor lớn → tràn | evaluate async-poll (§1) |
| MCP wedge "browser already running" | restart chrome-devtools MCP server |
| drag tool kẹt "left already pressed" | navigate_page reload |

---

## 15. QUY ƯỚC CHUNG
- **Title TIẾNG ANH** (Title Case + em-dash subtitle: `Main Title — Qualifier (Period, Unit)`). **Note TIẾNG VIỆT.** Axis/legend/data-element giữ tên gốc VN.
- Period default = **May 2026** trừ ASM/CUSTOMER (all-history → tag **"All-Time (2024–2026 YTD)"**), Flow = All-Time.
- **Number format**: MONEY = M (DP0, Abbreviate M); QUANTITY/volume = units (KHÔNG M); RATIO = Percent (DP0).
- **Màu Kangaroo** chuẩn (§8); semantics orange=cost, green=margin, gray=plan.
- **ADD-only** trên production (DB01): thêm viz mới bên cạnh, KHÔNG xoá viz user; tên/canvas mới. Thử trong sandbox.
- **Verify bằng SỐ**, đừng tin toast; persist verify qua projects/json. Soi golden BC01/SFC report để lấy đúng dataset+field (nhiều field trùng tên).
- **No HARDCODE số trong title/note** — số động ở KPI tile, kỳ ở filter chip (title đổi kỳ là lỗi thời ngay).
- Save sau mỗi cụm; snapshot ra file rồi grep; evaluate JSON gọn; uid theo snapshot mới nhất.

---

## 16. CHECKLIST DỰNG 1 DASHBOARD + DEFINITION OF DONE

**Build:**
1. Mở workbook (DB01 production deep-link, hoặc sandbox). Đăng nhập nếu cần (§0).
2. **Tạo canvas mới TRỐNG** cho viz mới (chống merge). Add dataset đúng nguồn nếu chưa có.
3. Thả field → chọn **loại viz** đúng use case (§5 map). Đặt field vào shelf đúng (§5 taxonomy).
4. **Combo plan-vs-actual:** 2 measure Values(Y) → actual chip → Bar (xanh), plan giữ Line (xám); Y2 nếu lệch thang.
5. **Title** Auto→Custom English (§4.1) + **VERIFY persist** sau reload. **Number format** M/% (§7). **Màu** series Kangaroo (§8).
6. **Filter** kỳ/scope (§9); Exclude "Khác"/"~No Value~" tại VIZ level.
7. **Note VN** (§4.2/§11) giải thích viz + hàm ý.
8. **Save** (OK không Escape nếu shared) → **verify persist** GET projects/json (§13).
9. **VERIFY SỐ**: đọc số viz qua executeOrPoll → đối chiếu golden/NSAW (§13). Đừng tin toast/SVG.

**Definition of DONE 1 viz/canvas:**
- [ ] Viz đúng LOẠI cho thông điệp + shelf đúng + giúp ra 1 quyết định C-level.
- [ ] **Số khớp nguồn** (bảng đối chiếu executeOrPoll vs golden/NSAW) HOẶC chênh lệch được giải thích.
- [ ] Title English (Custom, persist verified) · Number format M/% · Màu Kangaroo · Note VN.
- [ ] KHÔNG hardcode số · KHÔNG mâu thuẫn viz khác · baseline 0 · ratio không "vỡ".
- [ ] Save persisted (projects/json: canvas/viz có, last-modified mới) — **mở lại reload thấy còn nguyên**.

---

## 17. CÂU LỆNH MỞ MÀN (phiên sau)
> "Đọc `C:\Project\KGR-OAC-Agents\Dashboard-builder\OAC_DASHBOARD_MASTERY.md` (file golden TỰ CHỨA về Workbook/Visualization OAC qua Chrome DevTools MCP — không cần file khác). Mở sandbox `KGR_WB_SANDBOX_EXPLORE` (deep-link §0) hoặc workbook DB01. Rồi [việc cần làm]. Nếu user vắng mặt, login bằng credentials §0. (Tạo dataset gộp/join → dùng OAC_DATAFLOW_MASTERY.md.)"

---

## 18. CHANGELOG
> Changelog đã tách → OAC_DASHBOARD_MASTERY.CHANGELOG.md (không nạp mỗi phiên)
