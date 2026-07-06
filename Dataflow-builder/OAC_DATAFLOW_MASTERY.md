# 🛠️ OAC DATA FLOW MASTERY — GOLDEN, tự chứa (Kangaroo / KGR)
> **File DUY NHẤT** cần đọc để tạo & cấu hình Data Flow trên Oracle Analytics Cloud qua Chrome DevTools MCP. Đọc xong là thao tác như người làm 15 năm.
> **TỰ CHỨA — không cần đọc file/memory nào khác.** Mọi knowledge dataflow cũ (OAC_CHROME_MCP_PLAYBOOK §4.16, NAVIGATION_PLAYBOOK §11-12, ERROR_LOG, SFC docs, các memory) đã được migrate vào đây.
> Nguồn: thực nghiệm LIVE trong sandbox `KGR_DF_SANDBOX_EXPLORE` + lịch sử build SFC (v1/v2/v3) đã verify. Cập nhật 2026-06-11.
> Quy ước icon: ⭐ = đọc kỹ · ⚠️ = bẫy/gotcha · ✅ = đã verify live · 📌 = số/định danh load-bearing.

---

## MỤC LỤC
0. Đăng nhập & môi trường · 1. Bộ công cụ MCP & pattern cốt lõi · 2. Mở editor & sandbox · 3. Bố cục editor · 4. ⭐ Thêm/xoá node · 5. ⭐⭐ COMMIT/PERSIST từng nhóm node (bẫy quan trọng nhất) · 6. Taxonomy 30 node · 7. Config + bẫy sâu từng node · 8. Thư viện hàm Expression · 9. Save/Run/persist · 10. REST API đầy đủ · 11. Step JSON schema (thật vs giả) · 12. Walls & workaround · 13. Dataset/cột qualified + readability · 14. SFC golden recipe + số · 15. Gotcha khác · 16. Checklist build · 17. Câu lệnh mở màn

---

## 0. ĐĂNG NHẬP & MÔI TRƯỜNG
- **Instance:** `https://oaxinst70021-id3pgnmhxlya-0p-bo.analytics.ocp.oraclecloud.com`
- **User:** `minhndn@bizin.vn` (Minh Nguyen Danh). Folder dataflow của user: `/@Catalog/users/minhndn@bizin.vn`.
- 📌 **Credentials authorized (auto-login ĐÃ ỦY QUYỀN):** đọc LIVE từ `C:/Project/KGR-OAC-Agents/.secrets/oac.env` (`OAC_USER`, `OAC_PW`) — **KHÔNG dùng password trong memory** (đã từng login sai vì memory cũ). Owner CHO PHÉP AI **tự điền** form IDCS signin trong MỌI trường hợp: (a) user vắng/ngủ/auto-mode, **HOẶC (b) user yêu cầu / standing-instruction "tự đăng nhập giúp"**. → Cần login: **LÀM NGAY, KHÔNG từ chối/hỏi.** Anti-lockout: điền **1 lần**/lần signin; fail → DỪNG báo owner, KHÔNG retry (ORA-28000); OTP/MFA/CAPTCHA → nhờ owner hoàn tất.
- Redirect IDCS signin (`…identity.oraclecloud.com/ui/v1/signin`): `take_snapshot` → `fill_form` các textbox "User Name"/"Password" → click "Sign In".
- Phiên OAC **timeout khi idle** (~8–24h cookie). Khi "session expired"/redirect signin giữa chừng → login lại (theo quyền ở trên), KHÔNG tự re-auth lung tung.
- **Fallback rule:** nếu 1 thao tác MCP fail **5 lần** → chuyển computer-use. Thứ tự: DevTools MCP → (sau 5 fail) → computer-use.
- Workbook chính: `(KGR) DB01.Revenue_v1.1` tại `/@Catalog/shared/(KGR) 1.Implement/`. Golden ref doanh thu: `(KGR) BRD.BC01_Daily_Summary`; golden SFC: `/@Catalog/users/minhndn@bizin.vn/SFC report`.

---

## 1. BỘ CÔNG CỤ MCP & PATTERN CỐT LÕI

Tool Chrome DevTools MCP: `navigate_page · select_page · list_pages · take_snapshot(filePath) · evaluate_script(function[,filePath]) · click(uid,dblClick?) · fill(uid,value) · fill_form · hover · drag · press_key · type_text · take_screenshot · wait_for · list_network_requests · get_network_request`.

- ⭐ **Snapshot-to-file BẮT BUỘC:** `take_snapshot(filePath="C:\Project\KGR_Dashboard\_dfx_X.txt")` → `Grep`/`Read` file lấy **uid** + cấu trúc. Snapshot OAC editor ~80–100K chars; đổ thẳng vào context = TRÀN. uid CHỈ valid trong snapshot mới nhất → re-snapshot sau khi DOM đổi/navigate.
- ⭐ **evaluate_script trả JSON GỌN** — đừng map toàn bộ textContent. Query hẹp: đếm/lọc/lấy vài field.
- ⭐ **KHÔNG dùng `wait_for` để chờ editor dataflow render** — nó trả cả snapshot khổng lồ → tràn context. Thay bằng **async-poll** trong evaluate_script:
```js
async () => { for(let i=0;i<40;i++){ if(document.querySelectorAll('g.joint-cell,.joint-element').length>0 && [...document.querySelectorAll('[role=tree]')].some(t=>/Add Data/.test(t.textContent))) break; await new Promise(r=>setTimeout(r,300)); } return {cells:[...document.querySelectorAll('g.joint-cell,.joint-element')].map(c=>c.textContent.trim().slice(0,25)).filter(Boolean)}; }
```
- **Đọc danh sách node trên canvas:** `[...document.querySelectorAll('g.joint-cell, .joint-element')].map(c=>c.textContent.trim())`.
- **Real CDP click vs synthetic:**
  - `click` tool (real CDP) = ổn định cho: **treeitem step (panel "Data Flow Steps")** sau reload, chip grammar, dropdown Title, suggestion search, treeitem cột.
  - Synthetic `dispatchEvent`/`.click()`: chạy cho menuitem/label/nút thường + tree double-click (đôi khi), NHƯNG **popup canvas dataflow ("+ Add Preparation Step") BỎ QUA synthetic** (isTrusted check).
- **Native setter input thường:** `Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set.call(inp,val)` + dispatch `input` **và `change`+`blur`** (xem §5 — nhiều ô commit lúc blur, chỉ `input` là KHÔNG ăn). Ô search OAC: dùng `fill` tool (cần keystroke thật trigger autocomplete).
- **Expression/contenteditable (Add Columns/Transform):** click vào ô rồi `type_text` (bàn phím thật). KHÔNG dùng execCommand/native-setter cho ô expression (model riêng có thể revert).
- **CodeMirror (nếu editor công thức là CM):** `cm.setValue(...)` không tự fire change → focus → gõ space+Backspace (nudge) → Validate → Apply.
- **Undo bằng script:** `[...document.querySelectorAll('button[aria-label]')].find(x=>/Undo Last Edit/.test(x.getAttribute('aria-label'))).click()`.
- **`drag` tool quirk:** đôi khi lỗi "'left' is already pressed" → kẹt nút chuột → mọi click sau timeout; JS mouseup KHÔNG cứu → `navigate_page(reload)` (mất edit chưa lưu, giữ saved).
- **MCP wedge "browser already running" (cập nhật 2026-06-11, đa session):** project này dùng MCP server riêng **`chrome-dataflow`** (profile `profile-dataflow`, khai trong `.mcp.json`) — LUÔN dùng tools `mcp__chrome-dataflow__*`, KHÔNG dùng server plugin profile-chung (giẫm session khác). Gỡ kẹt AN TOÀN THEO PROFILE: chỉ kill chrome thuộc profile mình (`Get-CimInstance Win32_Process -Filter "Name='chrome.exe'" | ? { $_.CommandLine -match 'profile-dataflow' } | % { Stop-Process -Id $_.ProcessId -Force }`) + xoá lock (`SingletonLock/SingletonCookie/SingletonSocket/DevToolsActivePort`) trong đúng profile → gọi lại tool MCP (tự relaunch); vẫn kẹt → restart MCP server. ⛔ KHÔNG `Stop-Process chrome` toàn cục (giết nhầm cửa sổ session khác). 2 session không sửa cùng 1 flow/workbook. Tránh click in-dialog hyperlink (navigate → wedge).
  - 📌 **Đọc đúng thông báo:** "browser already running" / "chrome đang bị process khác dùng" = **SingletonLock của user-data-dir ĐANG mở**, KHÔNG phải hết cổng. Mở một **profile khác**, hoặc dùng `--isolated`, LUÔN hợp lệ và **KHÔNG cần kill** gì. **TUYỆT ĐỐI KHÔNG kill Chrome global.**
- 📸 **Ưu tiên `take_snapshot` (text a11y) hơn `take_screenshot` (ảnh)** khi chỉ cần verify text/persist — ảnh phình context; screenshot chỉ khi cần soi pixel/màu render.
- **Bash `curl` tới OAC BỊ CHẶN** (proxy allowlist, exit 56 `blocked-by-allowlist`) — KHÔNG phải auth fail. Chỉ **same-origin browser fetch** (từ trang OAC đang mở qua evaluate_script) chạy được REST API.

---

## 2. MỞ EDITOR & SANDBOX
**3 cách mở Data Flow editor:**
1. **Tạo mới:** `navigate_page("…/ui/dv/home.jsp?pageid=visualAnalyzer&reportmode=dataflow")` → OAC bật dialog **"Add Data"** chọn dataset nguồn đầu → double-click 1 dataset → vào editor (1 node Add Data). ⚠️ Trang mở ở **TAB 2** `…/ui/dv/ui/project.jsp?...reportmode=dataflow` → phải `select_page(pageId=2)`.
2. **Mở/Reset flow đã lưu (deep-link):** `…/ui/dv/ui/project.jsp?artifactid=<urlenc "'guid'.'NAME'">&pageid=visualAnalyzer&perflog=true&reportmode=dataflow&reportpath=%2F%40Catalog%2Fusers%2Fminhndn%40bizin.vn`. **Đây cũng là cách RESET sạch** khi canvas rối (xem §4).
3. **Từ Home:** mục **Data Flows** → click tên flow.
- ⚠️ Nút **Create → Data Flow** trên Home: MCP click **KHÔNG mở dialog** (synthetic bị nuốt). Dùng cách 1.
- 📌 **Sandbox thử nghiệm:** `KGR_DF_SANDBOX_EXPLORE` (artifactid guid `ca8113d2-5d01-497a-8411-51810f312ae9`, owner minhndn, /My Folders, nguồn = `(KGR) DTF_CALC_INVOICE_MEMO_#`). Deep-link đầy đủ:
  `…/project.jsp?artifactid=%27ca8113d2-5d01-497a-8411-51810f312ae9%27.%27KGR_DF_SANDBOX_EXPLORE%27&pageid=visualAnalyzer&perflog=true&reportmode=dataflow&reportpath=%2F%40Catalog%2Fusers%2Fminhndn%40bizin.vn`
  Thử node trong đây rồi reload để reset. KHÔNG xoá sandbox; KHÔNG save trạng thái hỏng.

---

## 3. BỐ CỤC EDITOR
```
┌ TOOLBAR: Go back · Undo(Ctrl+Z) · Redo(Ctrl+Y) · [Run Data Flow] · [Save] · [Save menu▾] · ⋮
├ TRÁI "Data Panel" 2 TAB:  • "Data" (cây dataset/cột nguồn)  • "Data Flow Steps" (CÂY 30 STEP — nơi double-click để THÊM node) ⭐
├ GIỮA-TRÊN CANVAS (joint.js): node nối trái→phải; mỗi node có nút "+"; Layout Compact/Expanded; Zoom 25–175%; "Show labels".
├ GIỮA-DƯỚI STEP EDITOR: config node ĐANG CHỌN (đổi theo loại node).
└ ĐÁY "Data Flow Preview Table": grid 30 dòng × N cột, LIVE theo node đang chọn. Toggle: auto-refresh preview · Data&Steps panel · Data preview · Step editor.
```
- Node canvas = `g.joint-cell`/`.joint-element`. Cây step trái = `[role=tree]` chứa text "Add Data". Cây cột nguồn = `[role=tree][aria-label="Data Elements Tree"]`.

---

## 4. ⭐ THÊM / XOÁ NODE QUA MCP (verified 2026-06)

> **WALL cũ chỉ áp dụng cho popup "+ Add Preparation Step" trên node canvas** (popup hover tự biến mất, cần trusted click, không lặp lại). **CÁCH ĐÚNG = double-click treeitem trong panel trái "Data Flow Steps".** Node mới chèn **SAU node đang chọn** và tự được chọn (step editor đổi sang nó). Double-click liên tiếp = chuỗi tuyến tính A→B→C.

### 4.1 THÊM node
- ✅ **Cách A (MCP click — TIN CẬY NHẤT, dùng mặc định):** snapshot → grep uid của `treeitem " <Tên Step>"` → `click(uid, dblClick=true)`.
- **Cách B (script-dispatch — gọn, KHÔNG cần uid, nhưng KÉM TIN CẬY SAU RELOAD):**
```js
const tree=[...document.querySelectorAll('[role=tree]')].find(t=>/Add Data/.test(t.textContent));
const ti=[...tree.querySelectorAll('[role=treeitem]')].find(x=>x.textContent.trim()==='Aggregate'); // đổi tên step
const tgt=ti.querySelector('.oj-treeview-item-text')||ti;
['pointerdown','mousedown','pointerup','mouseup','click','dblclick'].forEach(e=>tgt.dispatchEvent(new MouseEvent(e,{bubbles:true,cancelable:true,view:window})));
```
- ⚠️ **Sau deep-link reload, script-dispatch (cách B) đôi khi KHÔNG add được** (node Add Data chưa "selected" / timing). Khi đó dùng **cách A (MCP click)**. Trước khi add, chọn node nguồn: click vào `g.joint-cell` chứa tên dataset.
- ⚠️ **Canvas repaint TRỄ** → sau khi add phải **async-poll** xác nhận cell xuất hiện (≤2.5s). **ĐỪNG retry mù** khi chưa thấy cell — lệnh "thất bại" có thể render trễ → retry tạo **node trùng** (vd "Add Columns" + "Add Columns 1").
- Poll xác nhận:
```js
async () => { for(let i=0;i<10;i++){ if([...document.querySelectorAll('g.joint-cell,.joint-element')].some(c=>/Aggregate/.test(c.textContent))) break; await new Promise(r=>setTimeout(r,250)); } return {cells:[...document.querySelectorAll('g.joint-cell,.joint-element')].map(c=>c.textContent.trim().slice(0,20)).filter(Boolean)}; }
```

### 4.2 XOÁ / hoàn tác
- **Undo = click nút toolbar (script ở §1).** ⚠️ **1 undo = 1 CALL evaluate RIÊNG** — gọi nhiều undo trong CÙNG 1 call (vòng for) bị React gộp, chỉ ăn 1 lần.
- ⚠️ **Mỗi edit-config là 1 undo riêng:** thêm node + chọn cột + đổi option = 3 undo. Node có column-picker (Bin/Transform/Filter) cần ~2–5 undo.
- ⚠️ **OVER-UNDO XOÁ luôn node Add Data gốc → canvas RỖNG** ("No data added. Click '+'…"). Khi đó **reload deep-link** (§2 cách 2) để về saved gần nhất. KHÔNG save trạng thái rỗng.
- 💡 **Reset sạch tin cậy nhất = reload deep-link**, KHÔNG phải undo.

### 4.3 Multi-input node (Join / Union Rows) — pattern 2 nguồn ✅
1. Chọn node nguồn 1 → double-click **"Join"** (hoặc "Union Rows") → node "pending" (chưa hiện cell vì thiếu input 2).
2. Double-click **"Add Data"** trong cây step → dialog "Add Data" mở → double-click dataset nguồn 2 (chọn row chứa tên dataset).
3. **Join/Union TỰ NỐI** cả 2 nguồn và hiện cell. (Add Data dialog dùng `[role=row]`/`tr`; chọn bằng double-click row chứa tên dataset.)

---

## 5. ⭐⭐ COMMIT / PERSIST — BẪY QUAN TRỌNG NHẤT (verified live)

> OAC chia node thành **2 NHÓM commit khác hẳn nhau.** Hiểu sai = mất công thức / cấu hình mà không báo lỗi.

### 5.1 NHÓM A — node EXPRESSION cần **Apply** tường minh: **Add Columns**, **Transform Column**
- Mỗi cột = **Name** + **Expression** + bấm **Apply** (TỪNG cột).
- ⚠️⚠️ **CHƯA Apply mà chuyển sang cột/tab khác (hoặc rời node) → cột đang soạn MẤT CẢ TÊN LẪN CÔNG THỨC.** ✅ Đã verify: set Name="TC1", Expr="100", KHÔNG Apply, bấm "Column" tạo cột 2, quay lại → tab vẫn "New Column1", Name về mặc định, Expression RỖNG.
- ✅ Sau **Apply**: tab đổi tên thành tên cột, cột xuất hiện trong preview, **giữ nguyên khi chuyển tab qua lại**.
- **Validate** = chỉ kiểm cú pháp (báo lỗi nếu sai), **KHÔNG commit**. Apply mới commit.
- ⚠️ **Tab label STALE** — đừng tin label tab để verify; verify qua **preview** (cột mới xuất hiện) hoặc Name field sau Apply.
- ⚠️ **Name field commit khi BLUR:** nếu set Name bằng native-setter, phải dispatch `change`+`blur` (hoặc dùng `fill` tool / type + **Tab**) TRƯỚC khi Apply (ERROR_LOG cũ #1: "type name + Tab rồi Apply").
- ⚠️ **Sửa công thức của cột Add Columns ĐÃ CÓ SẴN (flow đã lưu) thường KHÔNG persist qua Save** → **THÊM CỘT MỚI** thay vì sửa cột cũ (ERROR_LOG cũ #13). Apply TỪNG cột, KHÔNG batch.
- **Formula syntax:** dùng autocomplete chọn token cột; KHÔNG gõ `"Tên cột"` literal (bị coi string → lỗi). Trong context dataset/workbook calc, ref đầy đủ: `XSA('minhndn@bizin.vn'.'__DATASET__')."Columns"."COL"`. Trong dataflow AddColumns, cột nguồn tham chiếu bằng tên hiển thị qua autocomplete; `IFNULL`/`+`/`-`… hợp lệ.

### 5.2 NHÓM B — node LƯỚI **auto-apply LIVE** (KHÔNG có nút Apply): **Add Data, Join, Union Rows, Filter, Aggregate, Save Dataset, Select Columns, Rename Columns, Merge Columns, Split Columns, Bin, Group, Cumulative Value**
- ✅ Không có nút Apply/Validate. Đổi dropdown / tick / thêm dòng → **preview cập nhật NGAY**.
- ⚠️ **Ô TEXT commit khi BLUR/change, KHÔNG phải lúc gõ.** ✅ Verify trên **Rename Columns**: native-set ô rename + chỉ dispatch `input` → preview KHÔNG đổi; sau khi dispatch `change`+`blur` → preview hiện tên mới. → **Luôn dùng `fill` tool** (nó fire change) hoặc **dispatch `change`+`blur`** (hoặc type + **Tab**) cho mọi ô text: rename, Dataset name (Save Dataset), New column name (Merge/Bin), Custom delimiter, Step Description.
- ⚠️ **Dropdown commit ngay khi chọn option** (Function, Join Keep-rows, Operator, Delimiter, Bin Method) — không cần Apply.
- ⚠️ **Aggregate "Add Group" tạo 1 ROW TRỐNG phantom** (✅ verify 16→17 groups, 1 empty). Click ô trống → popup cây cột để chọn dim. Bấm "Add Group" nhiều lần mà chưa điền = nhiều row trống phải xoá (hover row → nút Remove chỉ hiện khi hover).
- ⚠️ **Add Data "Add Selected" trên flow ĐÃ LƯU** có thể KHÔNG propagate cột xuống downstream → chọn cột trên **fresh load**, hoặc Join dataset đã có cột, hoặc build qua REST.

### 5.3 Persist tổng
- **Save NGAY sau mỗi cụm step** (chống timeout/redirect → mất). Reload = discard mọi edit chưa lưu.
- **Tên dataset/measure đặt trong Save step đôi khi KHÔNG persist** → dataset ra default names (vd `QUANTITY Sum`, `Quantity Maximum Maximum Sum`). Kiểm tên cột sau Run; rename ở tầng dataset/workbook nếu cần.

---

## 6. TAXONOMY 30 STEP (đúng thứ tự cây "Data Flow Steps")
| # | Step | Nhóm commit | Mục đích | ≥2 input |
|---|---|---|---|---|
| 1 | **Add Data** | B | Thêm dataset nguồn | — |
| 2 | **Join** | B | Nối 2 nguồn theo điều kiện cột | ✅ |
| 3 | **Union Rows** | B | Append dòng từ 2+ nguồn cùng cấu trúc | ✅ |
| 4 | **Filter** | B | Lọc dòng (List/Range/Expression) | — |
| 5 | **Aggregate** | B | Group-by + Sum/Avg/Min/Max/Count/CountDistinct | — |
| 6 | **Save Dataset** | B | Output: ghi dataset/DB (bắt buộc để Run) | — |
| 7 | **Add Columns** | **A (Apply)** | Tạo cột mới bằng Expression | — |
| 8 | **Select Columns** | B | Giữ/bỏ cột + sắp xếp thứ tự | — |
| 9 | **Rename Columns** | B (blur) | Đổi tên cột | — |
| 10 | **Transform Column** | **A (Apply)** | Sửa 1 cột tại chỗ bằng Expression | — |
| 11 | **Merge Columns** | B | Ghép ≥2 cột text + Delimiter | — |
| 12 | **Split Columns** | B | Tách 1 cột thành ≤4 cột | — |
| 13 | **Bin** | B | Chia cột SỐ thành khoảng | — |
| 14 | **Group** | B | Gom GIÁ TRỊ cột thành bucket có tên | — |
| 15 | **Branch** | B | Tách flow thành 2 nhánh output (tự tạo 2 "Save Data") | — |
| 16 | **Cumulative Value** | B | Running/window aggregate (Sort By + Restart) | — |
| 17 | **Time Series Forecast** | B | Dự báo chuỗi thời gian | — |
| 18 | **Analyze Sentiment** | B | Cảm xúc cột text → điểm/nhãn | — |
| 19 | **Similarity Analysis** | B | Tìm bản ghi tương đồng | — |
| 20 | **Graph Analytics** | B | Thuật toán đồ thị | — |
| 21 | **Database Analytics** | B | Hàm analytics chạy trong DB | — |
| 22 | **Train Numeric Prediction** | B | Train model hồi quy | — |
| 23 | **Train Multi-Classifier** | B | Train phân loại đa lớp | — |
| 24 | **Train Clustering** | B | Train gom cụm | — |
| 25 | **Train Binary Classifier** | B | Train phân loại nhị phân | — |
| 26 | **AutoML** | B | Tự chọn & train model | — |
| 27 | **Apply Model** | B | Áp model đã train chấm điểm | cần model đăng ký |
| 28 | **Apply AI Model** | B | Áp AI/LLM model đã đăng ký | cần model |
| 29 | **Apply Custom Script** | B | Chạy script Python/R đã đăng ký | cần script |
| (AI) | **AI Functions** (trong Add Columns) | A | `AI Generate`, `AI Filter` = sinh/lọc cột bằng LLM | — |
> ⚠️ **Apply Model / Apply AI Model / Apply Custom Script**: double-click KHÔNG tạo node nếu CHƯA có model/script đăng ký (im lặng). Cần register artifact trước.

---

## 7. CONFIG + BẪY SÂU TỪNG NODE (verified live; 12 node trong ảnh ưu tiên)

### 7.1 Add Data (InputDataset)
- Step editor: ô **Dataset** (readonly) + nút **Replace** + **Description** + checkbox **"Prompt to select Dataset when run"**.
- **Chọn cột:** ô **Search** + cây **"Data Elements Tree"** (multiselect) → tick cột → nút **"Add Selected"**. Bảng phải = cột đã chọn ("Selections (N)"), có Move up/down/Remove. Mặc định tạo mới = chọn HẾT cột.
- ⚠️ Synthetic/ctrl-click cây cột KHÔNG ăn → MCP click thật từng leaf (~2 call/cột). Click TABLE node = expand.
- ⚠️ Add Selected trên flow ĐÃ LƯU không propagate downstream (§5.2).

### 7.2 Join ✅ (xem §4.3 cách tạo 2 nguồn)
- **Keep rows** — 2 dropdown: **Input 1** & **Input 2**, mỗi cái `All rows`/`Matching rows`. Tổ hợp = loại join:
  - Matching + Matching = **Inner** · All + Matching = **Left outer** (giữ hết Input 1) · Matching + All = **Right outer** · All + All = **Full outer**.
- **Match columns** = bảng "Joins table": mỗi dòng `[Input 1 column ▾]  [Operator]  [Input 2 column ▾]`. OAC tự match cột trùng tên. **"Add join"** thêm điều kiện; **"Delete join"** xoá.
- **Operator** (nút haspopup): Equals · Not equal · Greater than · Less than · Greater than or equal · Less than or equal → **hỗ trợ non-equi/range join**.
- ⚠️ Cột match phải CÙNG KIỂU (cast nếu cần). Đổi dropdown auto-apply live.

### 7.3 Union Rows ✅ (xem §4.3)
- Map cột giữa các input + chọn giữ all/matching columns. 2 nguồn cần cấu trúc cột tương thích. Khi nguồn 2 chưa hợp lệ, dialog Add Data có thể hiện "No data to display" → chọn dataset cùng schema.

### 7.4 Filter
- Nút **"Add Filter"** → column picker (mọi cột) → chọn cột:
  - **dimension** → filter **List** (popup "<col> List"): **Limit Values** · Search · **Add (N)** · **Clear**. dblclick giá trị để chọn.
  - **số** → Range; **ngày** → date range.
- Nút **"Filter Bar Menu"** (▾): Limit Values By (Default/Auto/None) · Show All/Hide All · Clear All Filter Selections · Remove All Filters · **Create Expression Filter** (lọc bằng biểu thức boolean, vd `"PERIODNAME" IN('May 2026')`) · **Auto-Apply Filters** (On/Off).
- ⚠️ Đóng popup giá trị = **Escape** (giữ lựa chọn, KHÔNG hủy). Auto-Apply On → áp live.

### 7.5 Aggregate
- OAC **tự phân loại**: cột SỐ → **bảng "Aggregate"** (mặc định **Sum** — kể cả ID, SAI), cột text/dim → panel **"Group by"**.
- Bảng Aggregate mỗi dòng: `[cột nguồn]  [Function ▾]  [New column name]`. **Function = Sum · Average · Minimum · Maximum · Count · Count Distinct** (KHÔNG có "Group By"!). Nút **"Add Aggregate"** thêm measure.
- Panel **"Group by"**: nút **"Add Group"** → ⚠️ tạo **row trống phantom** → click ô trống → popup cây cột chọn dim. Nhiều lần Add Group = nhiều row trống (hover→Remove). Quy trình đúng: remove dim khỏi bảng Aggregate (hover→trash) → set Function measure → Add Group từng dim.
- 📌 **Cột định danh (ID) phải đặt Maximum, KHÔNG Sum** — Sum làm sai join/dedup (ERROR_LOG #7).
- ✅ Auto-apply live (không Apply).

### 7.6 Save Dataset (OutputDataset) — node OUTPUT
- **Dataset** (tên, ⚠️ commit khi blur) + **Browse** (chọn folder) · **Dataset Location** (vd /My Folders) · **Dataset Table** (tên bảng khi lưu DB) · **Description**.
- **Save data to ▾**: **Dataset Storage** (cache nội bộ OAC, mặc định) · **Database Connection** (ghi ngược DB ngoài).
- Checkbox **"Prompt to specify Dataset"** (When Run).
- **Bảng Columns**: mỗi cột `[Name] [Treat As ▾ = Attribute/Measure] [Default Aggregation ▾ = Sum/Avg/Min/Max/Count/Count Distinct/None] [Description]`.
- ⚠️ Tên dataset/cột đặt ở đây đôi khi không persist (§5.3) → kiểm sau Run.

### 7.7 Add Columns — NHÓM A (xem §5.1 quy tắc Apply)
- Nhiều cột = **tablist dọc** (mỗi cột 1 tab "New Column1"…); nút **"Column"** thêm tab.
- Mỗi cột: **Name text input** + **Expression** (contenteditable) + **Validate** + **Apply**. Bên phải = cây hàm (§8).
- ⚠️⚠️ Apply TỪNG cột; chưa Apply mà chuyển tab → MẤT (§5.1).
- ⚠️⚠️⚠️ **BẪY NULL-PROPAGATION (verified 2026-06-11, bug thật trong `(KGR) DF_ACTUAL_AOP_EXPENSE`).** Trong SQL/OAC, **bất kỳ phép `+`/`-`/`*` nào có MỘT toán hạng NULL → CẢ biểu thức = NULL**. Nếu bọc **một** `IFNULL(toàn-biểu-thức, 0)` quanh chuỗi nhiều cột (vd `IFNULL("LN Gộp" - "a5" - "a6" - "a7" - "a8", 0)`), thì ở mọi dòng có **bất kỳ** cột nào NULL → cả dòng → NULL → IFNULL biến thành **0** = **XÓA SẠCH đóng góp của dòng đó** (không phải +0 vô hại — nó nuốt mất các giá trị âm/dương lớn). Cực kỳ hay xảy ra **sau outer-join** (cột bên không-khớp = NULL ở ~nửa số dòng). Triệu chứng: cộng thêm 1 cột nhỏ (mà cột đó sparse/NULL) làm tổng **nhảy/đổi dấu vô lý**; hoặc tổng nhỏ hơn nhiều lần kỳ vọng (vd LNG KD chỉ còn ~8% giá trị đúng vì hàng trăm dòng doanh-thu-thuần có chi phí=NULL bị về 0). **CHẨN ĐOÁN:** executePreview thêm nhánh `AddColumns(diag = CASE WHEN "col" IS NULL THEN 1 ELSE 0 END, k=1) → GroupBy(k) SUM` để đếm NULL từng cột + so SUM(công-thức-cũ) vs SUM(công-thức-guarded). **SỬA = bọc `IFNULL(...,0)` quanh TỪNG cột:** `IFNULL("LN Gộp",0) - IFNULL("a5",0) - IFNULL("a6",0) - …`. Lỗi lan theo chuỗi (LNG KD→XTBH→NV→QLVH→LNTT) nên phải sửa MỌI node, không chỉ node phát hiện.

### 7.8 Transform Column — NHÓM A
- Link **"Select Column"** → chọn 1 cột → **Expression + Validate + Apply + cây hàm** (y Add Columns) nhưng **sửa cột TẠI CHỖ** + ô **Name** (output). Quy tắc Apply giống §5.1.

### 7.9 Select Columns — NHÓM B
- Shuttle: **Add all / Add selected / Remove all / Remove selected** + **Move up / Move down / Move menu** (sắp thứ tự) + Search + "Select All Rows". Auto-apply live.

### 7.10 Rename Columns — NHÓM B (blur)
- Mỗi cột 1 ô input "Rename <col>" = tên hiện tại → gõ tên mới. ✅ **Commit khi BLUR** (input-only không ăn — §5.2). Dùng `fill` tool / dispatch change+blur / type+Tab.

### 7.11 Merge Columns — NHÓM B
- **New column name** (blur) + `[Col A] With [Col B]` (link chọn cột) + nút **"Add Columns"** (ghép thêm) + **Delimiter ▾**: Space ( ) · Comma (,) · Dot (.) · Dash (-) · **Custom**.

### 7.12 Split Columns — NHÓM B
- Link **"Select Column"** + combobox **method** (Delimiter / theo vị trí) + combobox **delimiter char** (Space/Comma/Dot/Dash/Custom) + **spinbutton số cột** (tối đa 4).

### 7.13 Bin — NHÓM B (chỉ cột SỐ)
- Link **"Select Column"** (picker CHỈ liệt kê cột số) → **New element name** · **Number of bins** (spinbutton, mặc định 4) · **Method ▾** = **Manual · Equal Width · Equal Height** · view Histogram/List.

### 7.14 Group — NHÓM B (gom giá trị)
- Nút **"Group"** thêm nhóm · ô **Name** (tên nhóm) · checkbox **"Include Others"** · có chart preview. (Khác Aggregate "Group by" — đây gom VALUE thành bucket categorical mới.)

### 7.15 Branch — NHÓM B
- Double-click → **tự tạo 2 nhánh, mỗi nhánh 1 node "Save Data"** ("Save Data" + "Save Data 1"). Sinh 2 dataset output từ cùng phần prep.

### 7.16 Cumulative Value — NHÓM B
- **Bảng Aggregate**: `[Select column] [Function ▾] [Rows = cửa sổ N] [New column name]`. + **Sort By table** (thứ tự tính) + **"Restart for each"** (mốc reset/partition).

### 7.17 Time Series Forecast (đại diện ML) — NHÓM B
- **Target** (measure) · **Time** (cột thời gian) · **Periods** (số kỳ, mặc định 14) · **Model Type ▾** (mặc định "Seasonal Arima") · mức tin cậy (95%/80%). Output: cột **PredictedValue** + **PredictionLevel**.
- Train*/AutoML: chọn Target/positive-class + thuật toán + train/test split → sinh model artifact; **Apply Model** dùng model đó chấm điểm.

### 7.18 ⭐ PATTERN: pivot kỳ→cột tháng + clone def NGUỒN (verified 2026-06-11, build KGR_DF_ACTUAL_AOP_MONTHLY_v1)
> Bài toán hay gặp: nguồn ở grain (kỳ × entity), cần output 1 dòng/entity với cột theo tháng (T1..T12). OAC KHÔNG có node Pivot → pivot thủ công bằng **AddColumns CASE + GroupBy SUM**.
- **Pivot 1 measure theo kỳ:** AddColumns tạo cột mỗi tháng: `IFNULL(CASE WHEN "Posting_Period"=<mã kỳ> THEN "LNG KD" ELSE 0 END, 0)` (mã POSTINGPERIOD của tháng đó, tra live — vd một tháng đầu năm). Tháng không có data → expression literal `"0"`. Rồi GroupBy(entity) **SUM** các cột này → mỗi tháng gom về 1 dòng/entity. ✅ CASE so sánh **string** (`='39'`) chạy; bọc IFNULL chống NULL.
- ✅ **Tên cột TIẾNG VIỆT có dấu cách CHẠY trong expression** (bọc nháy kép): `"Doanh số thực tế"/"Doanh số (AOP) TĐ"`, `"DS T3"+"DS T4"`. Lỗi "ra 0" trước đó là do preview chập chờn (§10), KHÔNG phải tên cột.
- **Cột kế hoạch/coarse-grain (AOP cấp TĐ/Ngành/Kênh/Chuỗi) lặp per-row → GroupBy đặt `max` (KHÔNG sum)** để gắn 1 giá trị/entity, chống phồng. (Chính source flow cũng dùng `max` cho 8 cột AOP.) Ở viz cũng phải MAX/AVG, đừng SUM.
- **Lũy kế cộng vài tháng:** sau GroupBy (đã 1 dòng/entity), AddColumns: `IFNULL("Doanh số T3"+"Doanh số T4"+"Doanh số T5",0)`. KHÔNG cần self-join khi grain đã là entity. (Nếu giữ grain kỳ thì mới cần self-join entity→broadcast.)
- ⭐⭐ **CLONE DEF của FLOW TẠO RA NGUỒN của bạn.** Nếu nguồn là 1 dataset do dataflow khác sinh (vd `(KGR) DTF_X` ← `(KGR) DF_X`), GET def `DF_X` (`/dataflows?dataFlowID=`) để học **tên cột chính xác, cú pháp CASE/IFNULL, sum-vs-max thật, công thức nghiệp vụ** (vd LNG KD = LN Gộp − a5 − a6…; LNTT = LN QLVH − CP Dự phòng). Đây là template tin cậy nhất, đúng nguyên tắc "clone def thật" §11.
- ⚠️ **Verify trên DATASET OUTPUT, không trên preview** (preview cắt cột + chập chờn §10): sau Run, executePreview group-by-[] trên output dataset → đối chiếu tổng bảo toàn (vd ΣT3+T4+T5+T6 = Σnguồn). Pivot/reshape đúng ⟺ tổng được bảo toàn.

---

## 8. THƯ VIỆN HÀM cho Expression (Add Columns / Transform Column) — 8 nhóm ✅
- **AI Functions:** `AI Generate`, `AI Filter`.
- **Operators:** `+ - * / ||` `( )` `> < = >= <= <>` `,` `AND OR NOT` `Between` `In` `Is Null` `Like`.
- **Aggregate:** `NTile`, `Percentile`, `Rank`.
- **String:** `ASCII, Bit_Length, Char, Char_Length, Concat, Insert, Left, Length, Locate, Lower, Octet_Length, Position, Repeat, Replace, Right, Space, Substring, TrimBoth, TrimLeading, TrimTrailing, Upper`.
- **Math:** `Abs, Acos, Asin, Atan, Atan2, Ceiling, Cos, Cot, Degrees, Exp, Floor, Log, Log10, Mod, Pi, Power, Radians, Rand, RandFromSeed, Round, Sign, Sin, Sqrt, Tan, Truncate`.
- **Calendar/Date:** `Current_Date, Current_Time, Current_TimeStamp, Day_of_Quarter, DayName, DayOfMonth, DayOfWeek, DayOfYear, Hour, Minute, Month, Month_Of_Quarter, MonthName, Now, Quarter_Of_Year, Second, TimestampAdd, TimestampDiff, Week_Of_Quarter, Week_Of_Year, Year`.
- **Conversion:** `Attribute`, `Cast`, `IfNull`.
- **Expressions:** `Case (Switch)`, `Case (If)`.
> Coalesce sau join: `IFNULL("Nhóm sản phẩm","Nhóm SP")`. Cột định danh: `Cast`/giữ numeric để match join đúng kiểu.

---

## 9. SAVE / RUN / PERSIST
- **Save:** nút **"Save"** (aria-label "Save", KHÔNG phải "Save menu"). Lần đầu → dialog **"Save Data Flow As"**: ô tên `(e.g) My Data Flow` + Description + cây Location (My Folders/Shared) + **OK**. Toast "The Data Flow was successfully saved."
- **Run:** nút **"Run Data Flow"** (cần node **Save Dataset** output). ~10–60s; dataset xuất hiện ở Home (search/Data).
- ⚠️ **Editor "Run Data Flow"/"Save & Run" có thể HANG với flow dựng bằng REST API** → Run từ **Home → hover card → Actions ▾ → "Run"** (def đã lưu, server-side).
- **Workbook ở shared folder** Save → dialog "Share Related Items" → **click OK** (KHÔNG Escape — Escape HỦY cả save). Verify persist: GET `/ui/dv/ui/api/v2/projects/json?path=<enc>` (canvas count + last-modified).
- **Reload Data:** dataflow re-run thêm cột → workbook KHÔNG thấy qua Refresh/Replace/reopen → catalog → **phải-chuột dataset tile → "Reload Data"** → reopen workbook.

---

## 10. REST API DATAFLOW — BUILD/SỬA KHÔNG QUA CANVAS (verified)
> Same-origin `fetch` từ trang OAC đang mở (qua evaluate_script). Header POST/PUT: `x-csrf-token` (lấy từ XHR trước), `authorization:session`, `x-requested-with:XMLHttpRequest`, `credentials:'include'`. GET không cần CSRF. (Bash curl bị proxy chặn — chỉ browser fetch chạy.)

- **GET (đọc def để clone/verify):** `GET /ui/dv/ui/api/v1/dataflows?dataFlowID=<urlenc "'guid'.'NAME'">`.
  - ⚠️ Body trả về có thể là **JSON-encoded STRING** → `JSON.parse` 1–2 lần rồi lấy `.definition`.
  - Top-level keys: `dataReplicator, crconnectionDependencies, datagen-name, namespace, definition, datagen-type, display-name, alias-id, object-path, owner, created-date, last-modified, effective-permissions, dataflow-name, acl, id, success, requestStatus`.
  - `definition` keys: `steps, links, description, version_no, DSSDependencies, runFromCache, settings` (vd `version_no:"2.6"`, `settings:{autoLayout:true,zoomPercent:100}`).
- **executePreview (validate số, KHÔNG side-effect):** `POST /ui/dv/ui/api/v1/dataflows/executePreview?stepID=<id>` body = **definition PHẲNG** `{steps, links, stepId:"<output step id>", DSSDependencies}` (lấy def rồi `Object.assign(def,{stepId})`). Trả `flowData` (≤30 dòng) + `flowSQL`.
  - ⚠️ **executePreview ĐỌC QUA FLOW (từ nguồn) thì ổn, nhưng ĐỌC DATASET ĐÃ MATERIALIZE (InputDataset trỏ `XSA('owner'.'DS')` rồi preview) hay trả `flowDataStatusCode:1` + rỗng** (verified 2026-06-11, đọc DTF/KGR_DS_... đều rỗng dù dataset có data). Để verify SỐ trên dataset đã ghi: dùng **oac-native MCP `execute_logical_sql`** (`SELECT SUM(XSA('guid'.'DS')."Columns"."Col")…`) — cột KHÔNG DẤU query sạch; cột có dấu (ố/ũ…) bị mã hoá lỗi qua MCP → chỉ COUNT cột ASCII (Sub_Id) hoặc đặt alias. ⚠️ MCP có thể disconnect giữa task → mất kênh đọc materialized; khi đó verify bằng executePreview-qua-flow (logic) + Run "complete" + customizedColumns, hoặc mở dataset trong DV UI.
  - Body thiếu stepId → `22123 member missing (stepId)` (nghĩa là MỘT STEP thiếu `stepId`, KHÔNG phải preview target). Body nested `{definition,stepId}` → `46043 Invalid input Json`. `flowDataStatusCode:1` + chỉ "SET VARIABLE…" = 0 rows.
  - ⚠️ Preview = **30 group BẤT KỲ (chưa sort)** → muốn top-N thật phải thêm Filter sau GroupBy rồi sort client.
  - ⚠️⚠️ **executePreview GIỚI HẠN ~31 CỘT — cắt bớt cột PASSTHROUGH (không tham chiếu) (verified 2026-06-11).** Flow nhiều cột (vd 51 cột) preview chỉ trả ~28-31 cột: cột do AddColumns TẠO RA + cột được tham chiếu trong expression được giữ; cột passthrough từ InputDataset không dùng (vd DS Tn, AOP) bị RỚT khỏi preview. **ĐÂY LÀ ARTIFACT PREVIEW, KHÔNG phải lỗi def** — Run thật materialize ĐỦ mọi cột. Test passthrough bằng flow nhỏ (<31 cột) để xác nhận, rồi cứ POST-create + Run; verify trên DATASET OUTPUT (không phải preview).
  - ⚠️⚠️ **executePreview ĐỌC NGUỒN CHẬP CHỜN khi cache nguồn đang rebuild / cold sau re-login (verified 2026-06-11).** Cùng 1 truy vấn, các lần gọi cách nhau vài giây trả tổng KHÁC nhau (lúc đủ mọi kỳ, lúc chỉ 1 kỳ, lúc 0) — trong CÙNG 1 probe thì self-consistent. **Đừng tin 1 read; chạy lại 2-3 lần, lấy bản đầy đủ nhất.** RUN (materialized pathway) thì ỔN ĐỊNH (output đúng dù preview chập chờn) — verify trên output dataset, retry read nếu cold.
  - ⚠️ **WAF Akamai (`_abck` cookie) chặn fetch nhanh liên tiếp → HTTP 401 "Authorization Required" (HTML, không phải JSON).** Không phải lỗi token/auth. Cách gỡ: reload trang (`navigate_page` home) để browser giải challenge + refresh `_abck`, rồi giãn nhịp fetch. Token `x-csrf-token` thường KHÔNG đổi qua re-login cùng JSESSIONID.
- **POST (TẠO MỚI — CREATE = POST, KHÔNG phải PUT):** `POST /ui/dv/ui/api/v1/dataflows?folderPath=<urlenc /@Catalog/users/EMAIL>&dataFlowName=<urlenc NAME>` body = DataGenAttributes `{"datagen-name":NAME,"display-name":NAME,"dataflow-name":NAME,"datagen-type":"DATAFLOW","definition":<def>}` → `{dataflowId:"'<server-guid>'.'NAME'", success:true, requestStatus:201}`.
  - ⚠️ `custom-attrs` PHẢI là STRING (object → 400 "Cannot deserialize String from Object") → **BỎ HẲN custom-attrs**. Chỉ gửi ~13 field DataGenAttributes; field lạ (`dataReplicator/namespace/id/created-date/success`…) → 400 "Unrecognized field" (clone từ GET phải XOÁ chúng).
  - ⚠️⚠️ **CLONE DEF → OutputDataset KẾ THỪA `datasetName` của flow nguồn (verified 2026-06-11, KGR_DF_..._v3).** Clone def v2 để dựng v3 nhưng QUÊN đổi `OutputDataset.datasetName` → v3 vẫn ghi vào dataset **"KGR_DS_..._v2"**, KHÔNG tạo dataset "v3". Hậu quả: (a) tìm "dataset v3" mãi không thấy (nó đổ vào v2); (b) nếu dataset đích đã tồn tại + `outputType:"Create"` → finalize có thể no-op/xung đột → Run "complete" nhưng không ra dataset mới (red herring tốn cả buổi). **LUÔN đổi `OutputDataset.datasetName` (+ `datasetDescription`) sau clone**, và verify bằng GET def trước khi Run. Nếu CHỦ ĐỊNH refresh dataset cũ thì giữ nguyên tên (Run đè data, đúng nếu cùng owner).
- **PUT (CẬP NHẬT flow đã có):** `PUT /ui/dv/ui/api/v1/dataflows?dataFlowID=<id>&folderPath=<urlenc path>&propagatePermissions=false&skipAutoML=false` body `{"definition":<def>}` → `success:true`. PUT với id tự-mint → `success:false, "DataGenerator not found"` (PUT chỉ update). folderPath = đúng thư mục flow (user folder `/@Catalog/users/EMAIL`, hoặc shared `/shared/...` lấy từ `object-path` của GET).
  - ⚠️⚠️⚠️ **ĐỪNG PUT flow do NGƯỜI KHÁC sở hữu (verified 2026-06-11, bug thật `(KGR) DF_ACTUAL_AOP_EXPENSE` của anhdk).** Khi user X PUT flow owner Y, OAC **đóng dấu lại `srcexpression` `__CLIENT_FLOW_DATASET__` owner Y→X trên MỌI cột** (kể cả cột không sửa; `expression` giữ nguyên). executePreview vẫn ĐÚNG SỐ (compute OK), nhưng **Run thật FAIL ở "Bulk Finalize": `[nQSError:46236] Dataset Service error during Bulk Finalize - Request failed`** (KHÔNG có ORA/constraint → KHÔNG phải lỗi dữ liệu, là lỗi finalize do owner-mismatch). PUT lại bản gốc cũng vô ích (vẫn bị đóng dấu X). **CÁCH SỬA: để CHÍNH CHỦ (owner Y) mở flow → Save (đóng dấu về Y, nhất quán) → Run** ⇒ finalize OK. Muốn sửa flow người khác: đưa họ công thức before/after để họ tự áp + Save + Run; KHÔNG tự PUT. Finalize fail = rollback (bảng output giữ nguyên data cũ, không hỏng).
- **RUN:** `POST /ui/dv/ui/api/v1/dataflows/run?dataFlowID=<urlenc id>` body `{}` → `{success:true, jobKey, instanceKey, adhocJobId}`. ✅ **POST /run qua same-origin fetch CHẠY TỐT (verified 2026-06-11)** khi có dataflowId thật (từ response POST-create hoặc Home search) — bỏ ghi chú cũ "classifier chặn /run" (đó là ngữ cảnh bash curl). Async ~10–60s; poll dataset xuất hiện qua Home search `includeCategory=datasources` (`jobs/<key>`=404, không có job-status dễ). Hoặc Home → hover card → Actions → "Run" (UI).
  - ⚠️⚠️ **Def REST-built nếu THIẾU metadata editor sẽ MỞ ĐƯỢC editor nhưng CANVAS TRỐNG (0 node) + Run UI báo "invalid Data Flow" — xem §11.5 để dựng def MỞ/SỬA/RUN được trong editor.** POST /run vẫn chạy đúng số trên def thiếu-metadata (engine không cần metadata), nhưng người dùng KHÔNG mở/sửa/Run-UI được → luôn dựng def đầy đủ metadata (§11.5).
- **Tìm tên qualified cột:** `POST /ui/dv/ui/api/v1/dataset/datasets/metadata` body `{"subjectArea":["XSA('owner'.'name')"],"fetchAcl":"false"}` → `datasetsMetadata[sa].outputColumns.columnMetadataArray[]` (`displayName,name,sourceexpr,datatype`) + `presentation.folders[].columns[]` map display→physical table + `inputTables[]`. `POST /modelmetadata/columninfo/columns` → resolved `formula`.
- **Audit workbook:** GET `/ui/dv/ui/api/v2/projects/json?path=<urlenc>` (model 600KB+, JSON thường). POST projects/json = "Logic Error" → phải GET.

---

## 11. STEP JSON SCHEMA — ⚠️ THẬT vs GIẢ (clone def thật, ĐỪNG hand-build)

> Trên đĩa có 2 kiểu file: **`v2_dataflow_full.json` / `v3_final_def.json` = SCHEMA THẬT** (GET từ OAC). **`OAC_V3_DATAFLOW_DEFINITION.json` = PSEUDO-SCHEMA SAI** (hand-drafted). Luôn **GET def flow thật → JSON.parse → mutate in-place**, đừng hand-build từ pseudo.

| | THẬT (dùng cái này) | GIẢ (gây lỗi 22123) |
|---|---|---|
| key step | `stepId` | `id` |
| link | `{id, startNode, endNode}` | `{sourceID, targetID}` |
| Filter | `filter:[{expression, srcexpression, type:"complexFilter"}]` | `filterCondition:{type:"BinaryExpression"…}` |
| InputDataset cột | `{newName, name:"\"PHYS_TABLE\".\"col\""}` + `datasetId:"XSA('owner'.'name')"` | `datasetName` + `{name,datatype,columnDataType}` |

**Schema thật (rút gọn từ v2/v3):**
- **InputDataset:** `{stepId, type:"InputDataset", datasetId:"XSA('owner'.'name')", datasetRef:"ds_N", qualifiedTable:"XSA(ds_N)", datasetType:"datamodel|dataset", inputType:"all", parameters:[], promptForInputSource:[], columns:[{newName, name:"\"PHYS_TABLE\".\"col\""}]}`. ⚠️ `name` = PLAIN qualified physical ref, KHÔNG phải expression (cột dẫn xuất tính ở AddColumns).
- **Filter:** `{stepId, type:"Filter", filter:[{expression:"\"PERIODNAME\" IN('May 2026')", srcexpression:"…", type:"complexFilter"}], shouldUpgradeVersion:false}`.
- **GroupBy:** `{stepId, type:"GroupBy", groupByColumns:["displayName"], aggrColumns:[{newName, aggrtype:"sum|max", column, datatype:"numeric", columnDataType:"number"}], hashCount:2}`.
- **AddColumns:** `{stepId, type:"AddColumns", columns:[{name, expression, datatype:"number", columnDataType:"number"}]}` (cần CẢ name+expression). VD thật: `SL_Ke_Hoach` = `"SL W1"+"SL W2"+"SL W3"+"SL W4"+"SL W5"`; `SL_Thuc_Te` = `0 - "QUANTITY Sum"`.
- **Join:** `{stepId, type:"Join", joinType:"fullouterjoin|innerjoin|leftouterjoin|rightouterjoin", leftDataset:<stepId>, rightDataset:<stepId>, joinCondition:"and", joinOn:[{id, leftColumn, rightColumn, operator:"="}]}`. VD 2 điều kiện: `[{leftColumn:"Ngành hàng",rightColumn:"Tên Ngành",operator:"="},{leftColumn:"Nhóm sản phẩm",rightColumn:"Nhóm SP",operator:"="}]`.
- **OutputDataset:** `{stepId, type:"OutputDataset", datasetRef:"ds_2", datasetName, datasetDescription:"", outputType:"Create", customizedColumns:[{colName, DBColName:"", aggrRule:"none|sum", dataType:"varchar|numeric"}], saveType:"obi", connectionRef:"", tableName:"", connectionDisplayName:""}`.
- **links:** `[{id, startNode:<stepId>, endNode:<stepId>}]`.
- **DSSDependencies:** `{inputDatasets:[{datasetRef, datasetId:"'owner'.'name'"}], outputDatasets:[{datasetRef, datasetId:"'minhndn@bizin.vn'.'OUTPUT_NAME'"}]}`.
- **Union:** `{type:"Union", …}`.
- ⚠️ **stepId KHÔNG trùng SQL reserved word** — `stepId:"IN"` → `27002 Near <IN>: Syntax error`. Dùng `SRC/GB/IN2/InputDataset_0/Filter_0/GroupBy_P/Join_0/OutputDataset_0`.

### 11.5 ⭐⭐ DEF MỞ/SỬA/RUN ĐƯỢC TRONG EDITOR — metadata BẮT BUỘC (verified 2026-06-11, build KGR_DF_ACTUAL_AOP_MONTHLY_v2)
> Def REST tối-giản (đủ field cho ENGINE) thì POST /run ra số ĐÚNG, NHƯNG mở editor ra **canvas TRỐNG (0 node)** và Run-UI báo **"invalid Data Flow"**. Console lỗi: `obitech-dataprep/steppluginhandler/ERROR: l.aggrule is not a function` tại `generateOutputDataframe` → editor cần field metadata mà def tối-giản thiếu. Muốn người dùng MỞ/SỬA/RUN-UI được, def phải **clone đúng schema flow tạo-bằng-UI** (GET def flow nguồn làm khuôn). Phải có:
> 1. **MỖI step:** `description`, `stepDisplayName`, `stepDescription:""`, `_label`, `shortDesc` (ngoài `stepId`,`type`). Thiếu → node không vẽ/nhãn.
> 2. **MỖI cột AddColumns:** ngoài `name`,`expression`,`datatype` phải có **`aggrule`** (`"sum"`/`"none"`) + **`srcexpression`** = expression nhưng MỖI ref `"col"` thay bằng `XSA('<flow-owner>'.'__CLIENT_FLOW_DATASET__')."Columns"."col"`. **THIẾU `aggrule` = CRASH `aggrule is not a function` → canvas trống.** Sinh srcexpression bằng regex: `expr.replace(/"([^"]+)"/g, (m,c)=>`+"`XSA('owner'.'__CLIENT_FLOW_DATASET__').\"Columns\".\"${c}\"`"+`)` (literal `'39'` nháy đơn KHÔNG bị thay).
> 3. **`settings:{autoLayout:true, zoomPercent:100}`** → editor tự xếp node, KHỎI cần toạ độ.
> 4. **InputDataset đọc-all kiểu UI:** BỎ mảng `columns` (đọc hết), `qualifiedTable:"XSA(ds_N).\"Columns\""` (có `.\"Columns\"`), + `datasetDisplayName`,`datasetDescription`,`datasetType:"db"`. (Cột chọn-lọc → để GroupBy/SelectColumns chiếu; tránh InputDataset.columns trong def editor.)
> 5. **OutputDataset:** thêm `parameters:[]`,`promptForOutputDataset:[]`; `customizedColumns` mỗi cột `{colName, DBColName:"", aggrRule:"none|sum|max|avg", dataType:"varchar|numeric"}`; Dataset Storage = `saveType:"obi"`, `connectionRef:""`,`tableName:""`,`connectionDisplayName:""`.
> - ⚠️ **Sau khi mở def REST trong editor, lần Run-UI ĐẦU báo "invalid Data Flow" do model còn STALE → bấm SAVE (editor re-serialize thành model native) → Run-UI lại = CHẠY** (toast "Data Flow '…' complete."). Save không hiện "Share dialog" nếu flow ở /@Catalog/users (chỉ shared mới hỏi).
> - 💡 Cách an toàn nhất: GET def 1 flow mà flow đó TẠO RA dataset nguồn của bạn (vd `(KGR) DF_X` tạo `(KGR) DTF_X`) — nó có sẵn mọi field editor + công thức nghiệp vụ thật (LNG KD = LN Gộp − a5..a8; LNTT = LN QLVH − CP dự phòng…). Clone, mutate, POST.
> - ⚠️⚠️ **ĐỪNG PUT-đè def đầy-metadata lên flow CŨ (def tối-giản) mà dataset đã được tạo bởi def cũ — nút Run-UI sẽ HỎNG VĨNH VIỄN "invalid Data Flow" (verified 2026-06-11).** PUT làm flow MỞ/SỬA được + POST /run + Actions→Run vẫn chạy, NHƯNG editor mất liên kết "flow này sở hữu dataset X" (dataset do def cũ đăng ký) → Save+Run-UI bao nhiêu lần vẫn invalid. **CÁCH ĐÚNG: ngay từ đầu POST-create flow MỚI với def đầy-metadata (§11.5) → dataset do chính def này tạo → editor sở hữu đúng → Run-UI + RE-RUN đều OK (đã verify re-run khi dataset đã tồn tại vẫn chạy).** Nếu lỡ build flow bằng def tối-giản rồi: ĐỪNG PUT-patch — tạo flow MỚI (clone editor-friendly) output ra dataset tên MỚI, bỏ flow cũ.

---

## 12. WALLS & WORKAROUND
| Wall | Workaround |
|---|---|
| Popup "+ Add Preparation Step" canvas tự biến mất / cần trusted click | Double-click treeitem panel "Data Flow Steps" (§4) HOẶC REST |
| Script-dispatch add node fail sau reload | MCP `click(uid,dblClick=true)`; chọn node nguồn trước |
| Aggregate source-column picker (readonly + jQuery autocomplete) | Add Group → click ô trống → cây cột popup; hoặc user tay |
| Add Data "Add Selected" trên DF đã lưu không propagate | Add trên fresh load; hoặc REST |
| Editor "Run"/"Save & Run" HANG với def REST-built | Home → Actions → Run (server-side) |
| Create→Data Flow trên Home không mở dialog | navigate URL `reportmode=dataflow` |
| `wait_for` editor dataflow → tràn context | evaluate async-poll (§1) |
| Undo loop trong 1 call bị gộp | 1 undo = 1 call |
| Over-undo xoá Add Data → canvas rỗng | reload deep-link |
| Retry add mù khi repaint trễ → node trùng | poll trước khi retry |
| Mid-flow redirect → about:blank mất state | Save sau MỖI step |
| Hover Actions menu không hiện (dispatched mouseover) | URL navigation / click tile name |
| Right-click context menu blocked | Delete qua Save menu / dùng _v2 naming |
| MCP wedge "browser already running" | Restart chrome-devtools MCP server |
| Add Dataset output vào workbook (OJ trusted-click) | ~2 phút manual; multi-select không bền qua đổi search (add từng cái); profiling 30–60s đừng tưởng hang |

---

## 13. DATASET / CỘT QUALIFIED + READABILITY

**PLAN — `(KGR) DW_SFC`** (datamodel, nền `(KGR) SFC Dataset (có AI)` owner **viethl@bizin.vn**; ~23 folder: Header SF/CF, Line SF/CF, Pro, Model, Chuỗi, Nhóm sản phẩm, Nhóm xanh đỏ, Ngành hàng, Item, Khách hàng, Kênh, …):
- Ngành: `"DW_NS_X_CAM_CUSTOMRECORD_CSEG_SCV_PRODCATG"."Ngành hàng"` (Water care / Home care / Cold & Hygen care)
- Nhóm SP: `"DW_NS_X_CAM_CUSTOMRECORD_CSEG_SCV_PRODGROUP"."Nhóm sản phẩm"`
- Plan REV tháng ex-VAT: `"DW_NS_X_SFC_LINES_CF"."Doanh thu (-VAT)"` (= `CUSTCOL_SCV_SFC_TRANS_DT_NO_VAT`)
- Plan QTY: **KHÔNG có cột tháng** — chỉ weekly `SL W1..SL W5` (`DW_NS_X_SFC_LINES_CF`); monthly = **SUM(SL W1..W5)**
- Period: `"DW_NS_ACCOUNTINGPERIOD_D"."PERIODNAME"` / `"POSTINGPERIOD"`; Model: `CSEG_SCV_MODEL`; Item internal ID: `ID` (numeric, NetSuite)

**ACTUAL — `(KGR) DTF_CALC_INVOICE_MEMO_#`** (dataset DB, owner **anhdk@bizin.vn**, datasetId `XSA('anhdk@bizin.vn'.'(KGR) DTF_CALC_INVOICE_MEMO_#')`; cột **UNQUALIFIED**, 64 cột):
- Ngành: `"Tên Ngành"` · Nhóm SP: `"Nhóm SP"` · Model: `"Model name"`
- QTY: `"QUANTITY"` (**ÂM** — invoice sign: CustInvc âm, CustCred dương) · REV: `"Doanh thu thực tế"` / `"Doanh số thực tế"` (VND)
- Item: `"ITEM"` (= DW_SFC Item.ID) · `"ID CLASS"` (= CSEG_SCV_PRODCATG) · `"PERIODNAME"` · `"POSTINGPERIOD"` · `"TYPE"` (CustInvc/CustCred) · `"ACCTTYPE"` · free-gift `"CUSTCOL_SCV_LINE_ISFREEGIFT"`

**ID types:** DW_SFC = numeric codes (`CSEG_SCV_PRODCATG` 1-5, `CSEG_SCV_MODEL`, `Item.ID`); MEMO# = `ITEM`(=Item.ID), `ID CLASS`(=CSEG_SCV_PRODCATG) numeric + label text. Match join đúng kiểu (cast nếu lệch). **Cột ID khi Aggregate đặt Maximum, KHÔNG Sum.**

**Readability (INTERMITTENT — đừng pre-assume hỏng):**
- MEMO# từng fail `ORA-00942 ...KGR__DTF_CALC_INVOICE_MEMO_#... does not exist` (dataflow đọc qua OAX_USER cache) NHƯNG sau đó READ FINE → lỗi 0-rows/ORA-00942 là **TRANSIENT** (gated trên cache tồn tại). **ALWAYS validate-first qua executePreview**: trả rows → proceed; 0 rows → reload dataset hoặc fallback `(KGR) DTF_CALC_SFC Thực tế`.
- **ORA-28000 (account anhdk khoá):** chặn **VIZ WORKBOOK query live** trên dataset anhdk, **NHƯNG KHÔNG chặn DataFlow Run** (Run dùng materialized pathway). Thấy ORA-28000 trong preview viz → ignore, proceed Save+Run. Fix tận gốc: DBA `ALTER USER anhdk ACCOUNT UNLOCK`; mẹo: reload dataset 1 lần lúc account khoẻ để có cache.

---

## 14. SFC GOLDEN RECIPE + CÔNG THỨC VERIFY (kỳ chuẩn = May 2026; kỳ đổi → LẤY LIVE lại)

📌 **CÁCH LẤY SỐ VERIFY = CÔNG THỨC + NGUỒN + "LẤY LIVE" (owner cấm lưu số tuyệt đối — số kỳ cũ đóng-băng gây "wall ảo verify kỳ mới bằng số kỳ cũ"). Chạy công thức trên kỳ đang xét; đừng chép số.**
- **Plan QTY (by Ngành):** `SUM(SL W1..SL W5) GROUP BY Ngành hàng` trên `DW_SFC` lọc `PERIODNAME=<kỳ>` (Water / Home / Cold & Hygen); tổng = cộng 3 ngành. get_sfc_report(period=<p>) làm golden.
- **Plan REV ex-VAT (by Ngành):** `SUM("Doanh thu (-VAT)") GROUP BY Ngành hàng` cùng filter 1 kỳ. ⚠️ **Nếu ra bội số ~4× kỳ vọng = còn fan-out** (chưa lọc 1 kỳ / cộng nhầm cột tuần) — chẩn đoán, đừng gán số.
- **Actual QTY (MEMO# scope):** `SL_Thuc_Te = 0 − SUM("QUANTITY") GROUP BY Tên Ngành` trên `(KGR) DTF_CALC_INVOICE_MEMO_#` lọc 1 kỳ (QUANTITY âm — invoice sign; **đã net credit, KHÔNG ABS**). Achievement = actual/plan (LẤY LIVE).
- **Actual QTY (golden SFC scope):** `get_sfc_report(period=<p>)` — item-scope hẹp hơn MEMO# (xem gotcha dưới).

⭐ **KEY (THIẾT KẾ — giữ):** **Single-period filter (PERIODNAME=1 kỳ) TRIỆT fan-out.** Plan qty = plain `SUM(SL W1..SL W5)` by Ngành trên DW_SFC lọc 1 kỳ = golden CHÍNH XÁC. **KHÔNG cần MAX-then-SUM dedup** (fan-out ~4× là multi-period artifact, KHÔNG phải within-period).

⭐ **MEMO# vs golden SFC = ITEM-SCOPE, KHÔNG phải filter bug (THIẾT KẾ — giữ mô tả, bỏ số):** MEMO# actual = **MỌI SKU**; golden = chỉ item trong SFC plan scope (`qty_count_flag=1`: ITEMTYPE='Service' OR item ∈ SFC forecast, + ACCTTYPE='Income' + POSTING='T' + exclude SC=14). Home gap lớn nhất. **KHÔNG có MEMO# column filter nào khớp golden scope.** Actual đúng trên MEMO# = **−SUM(QUANTITY)** (đã net credit, KHÔNG ABS). Nếu dùng MEMO# phải nhãn "Tổng SL hóa đơn (mọi SKU)", KHÔNG gọi "% đạt KH SFC".

**Recipe v2 (✅ DONE/RUN/VERIFIED EXACT, grain = Tên Ngành) — clone từ `v2_dataflow_full.json`:**
```
PLAN:   DW_SFC (Ngành hàng, PERIODNAME, SL W1..W5, DT_KH="Doanh thu (-VAT)")
        → Filter PERIODNAME IN('May 2026')
        → GroupBy(Ngành hàng) SUM(SL W1..W5), SUM(DT_KH→DT_Ke_Hoach)
        → AddColumns SL_Ke_Hoach = "SL W1"+"SL W2"+"SL W3"+"SL W4"+"SL W5"
ACTUAL: MEMO# (Tên Ngành, PERIODNAME, QUANTITY, Doanh thu thực tế)
        → Filter PERIODNAME IN('May 2026')
        → GroupBy(Tên Ngành) SUM(QUANTITY→QUANTITY Sum), SUM(Doanh thu thực tế)
        → AddColumns SL_Thuc_Te = 0 - "QUANTITY Sum"
JOIN:   fullouterjoin, joinOn Tên Ngành = Ngành hàng
OUTPUT: KGR_DS_SFC_vs_MEMO_v2
```
**v3 (thêm Nhóm SP grain, `v3_final_def.json`):** GroupBy thêm `Nhóm sản phẩm`(plan)/`Nhóm SP`(actual); Join 2 điều kiện (Ngành + Nhóm SP); AddColumns `IFNULL("Nhóm sản phẩm","Nhóm SP")` → "Nhóm SP gộp". Output `KGR_DS_SFC_vs_MEMO_v3`.

**Lịch sử flow (độ tin — mô tả THIẾT KẾ, số LẤY LIVE):**
- ✅ **KGR_DF_SFC_vs_MEMO_v2** = canonical (plan by Ngành + actual −SUM(QUANTITY); single-period). Verify số theo công thức §14 trên kỳ đang xét.
- ⚠️ KGR_DF_SFC_vs_Actual/_v2 (plan từ DS_v2 inner-join multi-period) → **fan-out ~4× (multi-period artifact)**, undercount. KHÔNG dùng chart.
- ⚠️ KGR_DF_SFC_vs_MEMO_v1: actual side đúng (MEMO# scope), plan từ DS_v2 bị inner-join drop unsold-planned (thiếu ~nửa) → **chỉ tin actual side.**
- v3 (Nhóm SP), v4_Chuoi (coalesce "Chuỗi gộp"), Plan_by_Kenh (plan-only): built via POST.
- ⚠️ `(KGR) DTF_CALC_SFC Thực tế`: May 2026 PARTIAL (chỉ ~1/3 sản lượng so golden); Mar/Apr complete; cần REFRESH trước plan-vs-actual. Cột: qty=`Số lượng`(dương,SUM), `Tên ngành`, `Nhóm SP`, `PERIODNAME`.
- ⚠️ Single combo overlay Plan+Actual **blend bất khả** (cross-dataset blend = cartesian fan-out, plan nổ theo bội) → pre-join bằng dataflow (recipe trên) HOẶC 2 viz riêng.
- **DATA: SFC actual (MEMO#) KHÔNG có grain Kênh** ("Nhóm Kênh"/"Tên Kênh" NULL → 1 bucket). CÓ grain **Chuỗi** ("Tên Chuỗi": BIGC/DMX/MM/Caophong/FPT/VHC/Nguyenkim/Thongnhat). Plan DW_SFC có cả Kênh (8 kênh) + Chuỗi. → Plan-vs-Actual theo Kênh KHÔNG làm được (actual N/A); theo Chuỗi combo đầy đủ (2 bucket "ngoài chuỗi" chiếm phần lớn doanh thu — loại khỏi viz).
- **Màu Kangaroo:** actual `#44BA46` (green bars) / plan `#636466` (gray line). Set workbook-wide qua viz Menu→Color→Manage Assignments (mỗi measure×dataset là entry riêng cùng tên → set HẾT).

---

## 15. GOTCHA KHÁC
- 📌 **Posting period:** PERIODNAME ↔ POSTINGPERIOD 1:1 (mã kỳ = số tháng kế toán, tra LIVE cho kỳ đang xét — đừng nhớ mã cứng, kỳ đổi là lỗi thời).
- **IDCLASS=Sum → join sai** → cột định danh dùng **Maximum**.
- **Add Columns Tab-blur** + **thêm cột mới thay vì sửa cột cũ** khi flow đã lưu (§5.1).
- **Formula:** đừng gõ `"COL"` literal (string) → autocomplete chọn token / XSA đầy đủ.
- **Undo 1/call; over-undo rỗng canvas → reload** (§4.2).
- **Save sau mỗi cụm; reload = discard unsaved.**
- **Tên dataset/cột Save step đôi khi không persist** → kiểm sau Run.
- **BẪY THIẾT KẾ canvas SFC (bài học, KHÔNG snapshot số):** combo SFC plan-vs-actual DÙNG dataset pre-join single-period (KGR_DS_SFC_vs_MEMO_v2) + plan=SUM(cột tuần); nếu lấy từ DS_v2 multi-period + Plan=MAX thì **fan-out** (actual nổ theo bội, plan hụt, achievement sai) — đối chiếu 2 canvas mâu thuẫn thì canvas fan-out là canvas SAI. Verify số LIVE theo §14, đừng tin số canvas cũ.
- **NSAW/OAC API token** hết hạn ~19 ngày: OAC → Profile → Access Tokens → Refresh → Download → ghi đè `tokens.json`.

---

## 16. CHECKLIST BUILD 1 DATAFLOW
1. **Add Data** nguồn 1 → chọn đúng cột (Add Selected; trên fresh load).
2. (Join) **Add Data** nguồn 2 → **Join** tự nối → set Keep rows (loại join) + Match columns (cột cùng kiểu + operator).
3. **Filter** 1 kỳ (PERIODNAME='May 2026') để triệt fan-out.
4. **Aggregate**: Group by dims; measures Sum (ID → Max); Function commit ngay.
5. (Tuỳ) **Add Columns**: Name + Expression + **Apply TỪNG cột** (chưa Apply mà chuyển = mất); coalesce `IFNULL`.
6. **Save Dataset**: tên (blur để commit) + Treat As/Default Aggregation + Save to Dataset Storage.
7. **Save** flow → **Run** (Home→Actions→Run nếu editor hang).
8. **VERIFY số** qua executePreview hoặc mở dataset — so golden theo CÔNG THỨC §14 trên kỳ đang xét (plan = SUM(SL W1..W5) by Ngành; actual = −SUM(QUANTITY)); LẤY LIVE, đừng chép số kỳ cũ. Đừng tin toast một mình.

---

## 17. CÂU LỆNH MỞ MÀN (phiên sau)
> "Đọc `C:\Project\KGR-OAC-Agents\Dataflow-builder\OAC_DATAFLOW_MASTERY.md` (file golden TỰ CHỨA về Data Flow OAC qua Chrome DevTools MCP — không cần file khác). Mở sandbox `KGR_DF_SANDBOX_EXPLORE` (deep-link §2) hoặc tạo flow mới. Rồi [việc cần làm]. Nếu user vắng mặt, login bằng credentials §0."

---

## 18. CHANGELOG
> Changelog đã tách → OAC_DATAFLOW_MASTERY.CHANGELOG.md (không nạp mỗi phiên)
