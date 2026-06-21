<!-- INTENDED PATH (Write bị deny-rule chặn dưới .claude\):
     C:\Project\KGR-OAC-Agents\Dataflow-builder\.claude\skills\oac-dataflow-builder-workspace\iteration-1\eval-1-revenue-by-channel-monthly-exclude-freegift\without_skill\outputs\plan.md
     → User copy file này vào đúng chỗ, hoặc cấp quyền Write dưới .claude\ rồi yêu cầu lưu lại. -->

# PLAN — Dataset "Doanh thu thực tế (ex‑VAT) theo Nhóm Kênh × Tháng (Mar/Apr/May 2026), loại hàng tặng"

> **Trạng thái:** DRAFT chờ duyệt — CHƯA build. Môi trường hiện tại KHÔNG có browser → không thao tác OAC; mọi trinh sát nguồn được viết thành **CHECK chạy được** (§4) cho phiên có browser.
> **Ngày lập:** 2026-06-11 · **Người duyệt:** user (đại diện finance)
> **Tài liệu nền:** `C:\Project\KGR-OAC-Agents\Dataflow-builder\OAC_DATAFLOW_MASTERY.md` (golden guide — §10 REST, §11 schema, §13 cột, §16 checklist) · `C:\Project\KGR_Dashboard\v2_dataflow_full.json` (def THẬT để clone) · `MEMO_FILTER_DIAGNOSIS.md` · `ERROR_LOG.md`.

---

## 1. YÊU CẦU & SPEC OUTPUT

**Finance cần:** 1 dataset trên OAC — doanh thu thực tế **ex‑VAT** theo **Nhóm Kênh** × **tháng** (Mar/Apr/May 2026), **loại bỏ hàng tặng (free gift)**, nguồn **dữ liệu hóa đơn**. Grain: **mỗi dòng = 1 nhóm kênh × 1 tháng**.

**Output đề xuất:**

| Thuộc tính | Giá trị |
|---|---|
| Dataflow | `KGR_DF_DT_NhomKenh_Thang_v1` (folder `/@Catalog/users/minhndn@bizin.vn`) |
| Dataset output | `KGR_DS_DT_NhomKenh_Thang_v1` (Dataset Storage) |
| Grain | Nhóm Kênh × PERIODNAME — **không join, không fan-out khả dĩ** (1 nguồn duy nhất) |
| Số dòng kỳ vọng | (4–6 nhóm kênh + có thể 1 bucket "(Chưa gán kênh)") × 3 tháng ≈ **12–21 dòng** |

**Cột output:**

| Cột | Kiểu | Nguồn / công thức |
|---|---|---|
| `PERIODNAME` | attribute | "Mar 2026" / "Apr 2026" / "May 2026" |
| `POSTINGPERIOD` | numeric (aggr **Max**, để sort tháng) | MAX(POSTINGPERIOD) |
| `Nhom_Kenh` | attribute | `IFNULL("Nhóm Kênh",'(Chưa gán kênh)')` |
| `DT_ExVAT` | measure (Sum) | `SUM("Doanh thu thực tế")` sau khi lọc free-gift |

---

## 2. PHÂN TÍCH NGUỒN (từ knowledge đã verify trong repo — chưa re-verify live phiên này)

### 2.1 Nguồn chọn: `(KGR) DTF_CALC_INVOICE_MEMO_#` ("MEMO#")
- `datasetId = XSA('anhdk@bizin.vn'.'(KGR) DTF_CALC_INVOICE_MEMO_#')`, type `dataset` (DB), **64 cột, tên cột UNQUALIFIED** (`"PERIODNAME"`, `"Doanh thu thực tế"`, …) — xác nhận trong `v2_dataflow_full.json` + MASTERY §13.
- Là **fact hóa đơn line-grain chính của DB01** (Invoice + Credit Memo) — đúng yêu cầu "lấy từ dữ liệu hóa đơn". Là dataset duy nhất đã biết có **đủ cùng lúc**: doanh thu ex‑VAT + cờ free-gift + Nhóm Kênh + PERIODNAME.
- Cột liên quan: `PERIODNAME`, `POSTINGPERIOD`, `TYPE` (CustInvc/CustCred), `QUANTITY` (CustInvc ÂM), `"Doanh thu thực tế"`, `"Doanh số thực tế"`, `"Nhóm Kênh"`, `"Tên Kênh"`, `"ID Nhóm kênh"`, `"CUSTCOL_SCV_LINE_ISFREEGIFT"`, `ACCTTYPE`, `TRANDATE`, `"Đơn Giá (-VAT)"/"(+VAT)"`.
- Alternative bị loại: `(KGR) DW_INVOICE` (chưa rõ cột — giữ làm fallback CHECK-B3); `DTF_DAILY_KENH_CHUOI`/DAILY_KÊNH (pre-aggregated, **không lọc được free-gift ở line level**); `(KGR) DTF_CALC_SFC Thực tế` (chỉ quantity theo ngành/SP, không có doanh thu theo kênh).

### 2.2 Measure ex‑VAT = `"Doanh thu thực tế"`
- `DATA_JOIN_DESIGN.md` (dòng 88, 185) ghi rõ DB01 `"Doanh thu thực tế"` = **ex‑VAT**; `"Doanh số thực tế"` là measure khác (May 2026: Doanh số ≈ 351.3B vs Doanh thu ≈ 326.7B — tỷ lệ ~1.075 gợi ý chênh VAT) → **CHECK-H** xác nhận lại quan hệ trước khi chốt.
- Quy ước dấu: `QUANTITY` âm cho CustInvc, nhưng các viz DB01 SUM `"Doanh thu thực tế"` ra số DƯƠNG → cột doanh thu nhiều khả năng mang dấu "đúng chiều" (invoice dương, credit âm) ⇒ **plain SUM tự net credit memo** — **CHECK-E** xác nhận (đừng suy từ QUANTITY).

### 2.3 ⚠️ RỦI RO #1 — grain Nhóm Kênh trên MEMO# có BẰNG CHỨNG MÂU THUẪN
- **Bằng chứng CÓ:** DB01 Canvas CHANNEL (filter **Mar 2026**) có loạt viz hoạt động trên MEMO#: H-Bar "Revenue by Channel Group" (Nhóm Kênh: Delta/GT/General/MT), treemap "Doanh thu thực tế by Nhóm Kênh", table 5 dòng… (INVENTORY.md Canvas 4).
- **Bằng chứng KHÔNG:** 2026-06-07, đọc MEMO# qua **dataflow** (filter **May 2026**), group by `"Nhóm Kênh"`/`"Tên Kênh"` → **toàn NULL, 1 bucket = 713,262** (ERROR_LOG session 11; `actual_kenh_chuoi.json`; MASTERY §14).
- Giả thuyết hợp nhất: cột kênh (và có thể cả cờ free-gift — đều là field enrichment) bị NULL ở các dòng load sau khi bảng nền `OAX$DW.DW_NS_X_CUST_INVOICE_LINES_SUPPLEMENTARY` biến mất (~2026-06-05, làm upstream flow `(KGR) 1. DTF_CALC_INVOICE_MEMO_#` của anhdk FAIL — memory `project_dtf_invoice_memo_not_dataflow_readable`). Mar OK / May NULL khớp giả thuyết này. **→ CHECK-B là GATE GO/NO-GO của cả plan.**

### 2.4 ⚠️ RỦI RO #2 — cờ free-gift `CUSTCOL_SCV_LINE_ISFREEGIFT` chỉ thấy giá trị `F` / trống
- Đo live May 2026 (SFC_HANDOFF §16): Water care F=328K, **trống=171K** (đơn vị: quantity) — **chưa từng quan sát thấy 'T'**. Trống có thể = enrichment thiếu (cùng gốc §2.3), không chắc = "không phải hàng tặng", càng không chắc = hàng tặng.
- ⇒ Quy tắc loại trừ đề xuất: **chỉ loại dòng flag = 'T'** (`IFNULL(flag,'F') <> 'T'`), GIỮ F và trống. Nếu CHECK-C cho thấy không tồn tại 'T' ở cả 3 tháng → dừng, hỏi finance định nghĩa "hàng tặng" (vd dòng đơn giá ex‑VAT = 0, hoặc CKKM 100%).

### 2.5 Các fact nguồn khác đã verify
- **PERIODNAME ↔ POSTINGPERIOD 1:1**; May 2026 = 42 (verify live). Mar/Apr có ghi chép MÂU THUẪN (Mar=39 vs Mar=40) → **KHÔNG hardcode số kỳ; filter bằng PERIODNAME** + CHECK-D map lại.
- **Readability INTERMITTENT:** MEMO# từng `ORA-00942` khi đọc qua dataflow (cache OAX_USER chưa có) rồi lại đọc tốt → luật **validate-first qua executePreview**, không pre-assume (MASTERY §13).
- **ORA-28000 (account anhdk khóa):** chặn viz query live, **KHÔNG chặn DataFlow Run** → nếu gặp ở preview viz thì bỏ qua, vẫn Save+Run được.
- **Scope caveat:** MEMO# bao gồm khách nội bộ (không loại SC=14) và không giới hạn ACCTTYPE='Income' → tổng sẽ cao hơn NSAW external ~2.5% (342.8B vs 351.3B "Doanh số", p42). Cần finance chốt định nghĩa (§9-Q3).
- **Freshness:** upstream flow của MEMO# từng FAIL từ ~2026-06-05; tiền lệ `DTF_CALC_SFC Thực tế` May chỉ load ~1/3 → bắt buộc CHECK-F (độ phủ TRANDATE + đối chiếu tổng) trước khi tin số May.

---

## 3. QUYẾT ĐỊNH THIẾT KẾ (đề xuất — duyệt từng dòng)

| # | Quyết định | Lý do |
|---|---|---|
| D1 | Nguồn duy nhất MEMO#, **không join** | Đủ cột; 1 nguồn ⇒ loại trừ fan-out by construction (bài học DS_v2 4.17×, blend cartesian) |
| D2 | Measure `SUM("Doanh thu thực tế")` (plain SUM, net credit) | Cột ex‑VAT chuẩn DB01; net CustCred đúng nghiệp vụ "doanh thu thực tế"; KHÔNG dùng ABS |
| D3 | Giữ cả `CustInvc` + `CustCred` (không filter TYPE) | Doanh thu tháng phải trừ hàng trả lại; CHECK-E xác nhận dấu |
| D4 | Filter `"PERIODNAME" IN ('Mar 2026','Apr 2026','May 2026')` | PERIODNAME↔period 1:1; tránh bẫy Mar=39/40 |
| D5 | Free-gift: loại `flag='T'`, giữ `F`/NULL | §2.4; tránh loại nhầm 171K+ dòng enrichment-thiếu |
| D6 | NULL kênh → bucket `"(Chưa gán kênh)"` (IFNULL **sau** GroupBy, pattern v3 đã verify) | Tổng theo tháng vẫn khớp 100% baseline; finance nhìn thấy phần chưa gán thay vì mất số âm thầm |
| D7 | Dùng **Nhóm Kênh** (MT/GT/General/Delta…), không phải Tên Kênh | Đúng chữ yêu cầu "Nhóm Kênh"; Tên Kênh (14 giá trị) là grain mịn hơn — để v2 nếu cần |
| D8 | Build qua **REST API** (clone def v2) — canvas chỉ là fallback | Canvas add-step là wall đã biết; REST recipe verified (MASTERY §10/§11) |
| D9 | Đặt thêm `MAX(POSTINGPERIOD)` | Sort tháng đúng thứ tự trong viz; cột định danh dùng Max, KHÔNG Sum |

---

## 4. RECON CHECKS — chạy ở phiên CÓ browser, TRƯỚC khi build

> **Cách chạy chung:** mở trang OAC bất kỳ (đã login) → `evaluate_script` same-origin fetch
> `POST /ui/dv/ui/api/v1/dataflows/executePreview?stepID=<stepId>` — header `x-csrf-token` (lấy từ XHR trước đó), `authorization: session`, `x-requested-with: XMLHttpRequest`, `credentials:'include'`.
> Body = **definition PHẲNG** `{steps, links, stepId, DSSDependencies}` (thiếu `stepId` → lỗi 22123; nested → 46043). Preview trả ≤30 dòng — các check dưới đều group nhỏ (<30) nên đủ. **Không side-effect** — an toàn chạy trước duyệt build.
> Template def dùng chung (mutate `groupByColumns`/`filter` cho từng check):

```js
// CHECK template — đổi GB.groupByColumns + FILTER.expression theo từng check
const SRC = {stepId:"SRC", type:"InputDataset",
  datasetId:"XSA('anhdk@bizin.vn'.'(KGR) DTF_CALC_INVOICE_MEMO_#')",
  datasetRef:"ds_1", qualifiedTable:"XSA(ds_1)", datasetType:"dataset",
  inputType:"all", parameters:[], promptForInputSource:[],
  columns:[
    {newName:"PERIODNAME",  name:"\"PERIODNAME\""},
    {newName:"POSTINGPERIOD", name:"\"POSTINGPERIOD\""},
    {newName:"Nhóm Kênh",   name:"\"Nhóm Kênh\""},
    {newName:"Tên Kênh",    name:"\"Tên Kênh\""},
    {newName:"ID Nhóm kênh", name:"\"ID Nhóm kênh\""},
    {newName:"TYPE",        name:"\"TYPE\""},
    {newName:"FREEGIFT",    name:"\"CUSTCOL_SCV_LINE_ISFREEGIFT\""},
    {newName:"ACCTTYPE",    name:"\"ACCTTYPE\""},
    {newName:"TRANDATE",    name:"\"TRANDATE\""},
    {newName:"DT",          name:"\"Doanh thu thực tế\""},
    {newName:"DS",          name:"\"Doanh số thực tế\""}]};
const FIL = {stepId:"FIL", type:"Filter", shouldUpgradeVersion:false,
  filter:[{expression:"\"PERIODNAME\" IN('Mar 2026','Apr 2026','May 2026')",
           srcexpression:"\"PERIODNAME\" IN('Mar 2026','Apr 2026','May 2026')",
           type:"complexFilter"}]};
const GB  = {stepId:"GB", type:"GroupBy", hashCount:2,
  groupByColumns:["PERIODNAME","Nhóm Kênh"],            // ← đổi theo check
  aggrColumns:[{newName:"DT_Sum", aggrtype:"sum", column:"DT",  datatype:"numeric", columnDataType:"number"},
               {newName:"PP_Max", aggrtype:"max", column:"POSTINGPERIOD", datatype:"numeric", columnDataType:"number"}]};
const def = {steps:[SRC,FIL,GB],
  links:[{id:"l1",startNode:"SRC",endNode:"FIL"},{id:"l2",startNode:"FIL",endNode:"GB"}],
  stepId:"GB", version_no:"2.6",
  DSSDependencies:{inputDatasets:[{datasetRef:"ds_1",
    datasetId:"'anhdk@bizin.vn'.'(KGR) DTF_CALC_INVOICE_MEMO_#'"}], outputDatasets:[]},
  settings:{autoLayout:true, zoomPercent:100}};
// fetch(...executePreview?stepID=GB, {method:'POST', body: JSON.stringify(def), headers:{...}})
// → đọc flowData; ghi kết quả GỌN ra file, KHÔNG dump cả response vào context
```

⚠️ Nếu tên cột trong `SRC.columns` sai (`"Nhóm Kênh"`, `"ID Nhóm kênh"`, `"TRANDATE"`, `"Doanh số thực tế"` là suy đoán có-căn-cứ nhưng chưa GET-verify) → chạy **CHECK-0** trước để lấy tên hiển thị chính xác rồi sửa template.

| ID | Check | Cách đo | Tiêu chí GO | Hành động nếu FAIL |
|---|---|---|---|---|
| **CHECK-0** | Schema MEMO# chính xác (64 cột) | `POST /ui/dv/ui/api/v1/dataset/datasets/metadata` body `{"subjectArea":["XSA('anhdk@bizin.vn'.'(KGR) DTF_CALC_INVOICE_MEMO_#')"],"fetchAcl":"false"}` → `columnMetadataArray[].displayName/datatype` | Có đủ: Nhóm Kênh, cờ free-gift, Doanh thu thực tế, PERIODNAME, TRANDATE | Sửa tên cột template; nếu thiếu cờ free-gift → §9-Q2 |
| **CHECK-A** | Readability (validate-first) | Template trên, `groupByColumns:["PERIODNAME"]` | 3 dòng, DT_Sum > 0 cả 3 tháng | `flowDataStatusCode:1`/0 rows = cache ORA-00942 → catalog → Reload Data MEMO# → retry; vẫn fail → dừng, báo data team |
| **CHECK-B** ⭐GATE | Độ phủ Nhóm Kênh per tháng | `groupByColumns:["PERIODNAME","Nhóm Kênh"]` → share DT của dòng kênh NULL theo tháng | NULL-share < **2%** doanh thu ở CẢ 3 tháng | B1: group `["PERIODNAME","ID Nhóm kênh"]` — nếu ID còn số → thêm bước map ID→tên (Group step hoặc join dim AOP_UPDATE/DW_NS_X_SALE_CHANNEL); B2: nhờ anhdk/data team fix upstream supplementary + re-run rồi đo lại; B3: thăm dò `(KGR) DW_INVOICE` (CHECK-0 trên dataset đó); B4 (chót): grain Mar-only + caveat. **Báo user trước khi chọn B1–B4** |
| **CHECK-C** | Phân bố cờ free-gift | `groupByColumns:["PERIODNAME","FREEGIFT"]` (thêm aggr `count` nếu cần) | Tồn tại giá trị 'T'; share NULL-flag nhỏ hoặc giải thích được | Không có 'T' cả 3 tháng → **DỪNG**, hỏi finance định nghĩa hàng tặng (đơn giá 0? CKKM 100%?) — §9-Q2 |
| **CHECK-D** | Literal PERIODNAME + map kỳ | `groupByColumns:["PERIODNAME"]` aggr max/min POSTINGPERIOD, filter `"POSTINGPERIOD" BETWEEN 38 AND 43` | 3 literal đúng 'Mar 2026'/'Apr 2026'/'May 2026'; mỗi tháng 1 kỳ duy nhất | Sửa literal filter theo thực tế; ghi map Mar/Apr vào ERROR_LOG (giải mâu thuẫn 39/40) |
| **CHECK-E** | Dấu & net credit memo | `groupByColumns:["PERIODNAME","TYPE"]` SUM(DT) | CustInvc > 0, CustCred < 0 (hoặc ngược dấu nhất quán) ⇒ plain SUM = net | Nếu CustCred cùng dấu dương → đổi D2 thành `SUM(CASE TYPE...)` qua AddColumns trước GroupBy |
| **CHECK-F** | Freshness + baseline tổng | (i) `groupByColumns:["PERIODNAME"]` aggr `max TRANDATE`; (ii) SUM(DT) per tháng KHÔNG lọc free-gift | (i) max TRANDATE ≥ cuối tháng (31/3, 30/4, 31/5); (ii) May ≈ 326–351B (ref DB01/NSAW 342.8B ±5%), Mar ≈ 287B ±5% | Tháng nào hụt phủ → yêu cầu refresh/upstream re-run trước khi build; ghi baseline 3 số làm acceptance §7 |
| **CHECK-G** | Scope: ACCTTYPE + kênh nội bộ | `groupByColumns:["ACCTTYPE"]`; và đọc danh sách giá trị Nhóm Kênh/Tên Kênh từ CHECK-B | Doanh thu nằm ≥99% ở Income; không có bucket kênh nội bộ bất thường | Nếu non-Income/SC nội bộ đáng kể → đề xuất filter bổ sung, hỏi finance §9-Q3 |
| **CHECK-H** | Xác nhận "Doanh thu thực tế" = ex‑VAT | So `SUM(DT)` vs `SUM(DS)` per tháng (tỷ lệ ≈ 1+VAT ~8–10%?); nếu chưa thuyết phục: so dòng mẫu `DT ≈ -QUANTITY × "Đơn Giá (-VAT)"` | DS/DT ≈ 1.08–1.10 ổn định, hoặc khớp đơn giá -VAT | Nếu DT KHÔNG phải ex‑VAT → đổi measure (vd `-QUANTITY × Đơn Giá (-VAT)` qua AddColumns) + báo user |
| **CHECK-I** | Cú pháp filter free-gift trong dataflow | executePreview với 2 filter entry (xem §5) — so tổng vs CHECK-F(ii) | Chênh lệch = đúng doanh thu dòng 'T' của CHECK-C | `IFNULL` không hợp lệ trong complexFilter → dùng dạng `("X" IS NULL OR "X" <> 'T')`; vẫn fail → chuyển logic vào AddColumns CASE + filter cột mới |

**Thứ tự chạy:** 0 → A → B (gate) → C (gate) → D → E → F → G → H → I. Tổng ~10–15 call executePreview, không ghi gì lên server. Kết quả từng check ghi vào `RUN_LOG.md` / file json trong workspace (pattern snapshot-to-file, giữ context gọn).

---

## 5. THIẾT KẾ DATAFLOW (build sau khi §4 GO + user duyệt)

```
(KGR) DTF_CALC_INVOICE_MEMO_#  [InputDataset_0  — cột: PERIODNAME, POSTINGPERIOD, Nhóm Kênh,
                                CUSTCOL_SCV_LINE_ISFREEGIFT, Doanh thu thực tế]
   → Filter_0   :  "PERIODNAME" IN ('Mar 2026','Apr 2026','May 2026')
                   AND ("CUSTCOL_SCV_LINE_ISFREEGIFT" IS NULL OR "CUSTCOL_SCV_LINE_ISFREEGIFT" <> 'T')
   → GroupBy_0  :  group [PERIODNAME, Nhóm Kênh]
                   aggr  SUM("Doanh thu thực tế") → DT_ExVAT
                         MAX("POSTINGPERIOD")     → POSTINGPERIOD
   → AddColumns_0: Nhom_Kenh = IFNULL("Nhóm Kênh", '(Chưa gán kênh)')   ← pattern coalesce v3 đã verify
   → OutputDataset_0: KGR_DS_DT_NhomKenh_Thang_v1  (Dataset Storage)
```

**Định nghĩa JSON (clone-mutate từ def THẬT của v2 — KHÔNG hand-build):**

1. GET `/ui/dv/ui/api/v1/dataflows?dataFlowID=` `'e6cc022c-f1d3-4bfd-899a-f508414e85d5'.'KGR_DF_SFC_vs_MEMO_v2'` → `JSON.parse` (1–2 lần) → lấy `definition`.
2. Mutate in-place:
   - **Bỏ** toàn bộ nhánh plan (InputDataset_0/Filter_0/GroupBy_P/AddColumns_P) + `Join_0` + links liên quan; giữ nhánh actual làm khung.
   - `InputDataset_1` (giữ nguyên datasetId/datasetRef/datasetType của MEMO#): `columns` = 5 cột ở trên — `{newName:"Nhóm Kênh", name:"\"Nhóm Kênh\""}` v.v. (tên unqualified, theo CHECK-0).
   - `Filter_1.filter` = **2 entry** complexFilter (AND ngầm):
     `{"expression":"\"PERIODNAME\" IN('Mar 2026','Apr 2026','May 2026')", "srcexpression":"…same…", "type":"complexFilter"}` và
     `{"expression":"(\"CUSTCOL_SCV_LINE_ISFREEGIFT\" IS NULL OR \"CUSTCOL_SCV_LINE_ISFREEGIFT\" <> 'T')", …}` (đã validate ở CHECK-I; xoá `filterControlCollections` clone thừa).
   - `GroupBy_A`: `groupByColumns:["PERIODNAME","Nhóm Kênh"]`; `aggrColumns:[{newName:"DT_ExVAT",aggrtype:"sum",column:"Doanh thu thực tế",…},{newName:"POSTINGPERIOD",aggrtype:"max",column:"POSTINGPERIOD",…}]`.
   - `AddColumns_A.columns` = `[{name:"Nhom_Kenh", expression:"IFNULL(\"Nhóm Kênh\",'(Chưa gán kênh)')", datatype:"varchar", columnDataType:"string"}]` (kiểu text — khác mẫu number của v2).
   - `OutputDataset_0`: `datasetName:"KGR_DS_DT_NhomKenh_Thang_v1"`; `customizedColumns`: PERIODNAME/Nhom_Kenh (`aggrRule:"none"`, varchar), DT_ExVAT (`aggrRule:"sum"`, numeric), POSTINGPERIOD (`aggrRule:"none"`, numeric).
   - `DSSDependencies`: inputDatasets chỉ còn MEMO#; `outputDatasets[0].datasetId = "'minhndn@bizin.vn'.'KGR_DS_DT_NhomKenh_Thang_v1'"`.
   - `stepId` mới không trùng SQL reserved word (giữ `InputDataset_1/Filter_1/GroupBy_A/AddColumns_A/OutputDataset_0`).

---

## 6. TRÌNH TỰ BUILD (phiên có browser; đường chính = REST, MASTERY §10)

1. **Login** OAC (nếu user vắng mặt: dùng credentials đã authorize, MASTERY §0).
2. Chạy **toàn bộ §4** → dán bảng kết quả check cho user/finance chốt D1–D9 + Q1–Q5 (§9). **Không build khi CHECK-B/C đỏ.**
3. **executePreview** def cuối (§5) tại `stepID=GroupBy_A` rồi `stepID=AddColumns_A` → đối chiếu tổng per tháng với baseline CHECK-F(ii) − doanh thu free-gift (CHECK-C). ≤30 dòng nên preview thấy ĐỦ mọi dòng output.
4. **POST tạo flow:** `POST /ui/dv/ui/api/v1/dataflows?folderPath=%2F%40Catalog%2Fusers%2Fminhndn%40bizin.vn&dataFlowName=KGR_DF_DT_NhomKenh_Thang_v1`, body `{"datagen-name":…,"display-name":…,"dataflow-name":…,"datagen-type":"DATAFLOW","definition":<def>}` — **bỏ custom-attrs** và mọi field lạ (400 nếu sót). Kỳ vọng `success:true, requestStatus:201`.
5. **Run:** Home → hover card flow → Actions → **Run** (KHÔNG dùng nút Run trong editor với def REST-built — hang đã biết). Poll dataset xuất hiện qua Home search `includeCategory=datasources` (~10–60s).
6. **Verify (§7)** — trước khi báo DONE.
7. Bàn giao: share dataset cho finance / add vào workbook nếu được yêu cầu (lưu ý dialog "Share Related Items" khi Save workbook: **click OK, KHÔNG Escape** — Escape HỦY save).
8. Fallback nếu REST POST bị chặn: build tay trên canvas theo MASTERY §16 (Add Data → Filter → Aggregate → Add Columns (Apply TỪNG cột!) → Save Dataset → Save → Run), các bẫy commit nhóm A/B theo §5 của guide.

---

## 7. ACCEPTANCE CRITERIA (verify bằng số, không tin toast)

1. Dataset `KGR_DS_DT_NhomKenh_Thang_v1` tồn tại, mở được; đúng 4 cột spec §1.
2. **Grain đúng:** số dòng = số cặp (Nhóm Kênh × tháng) distinct; đúng 3 giá trị PERIODNAME; không dòng trùng cặp.
3. **Tổng khớp:** per tháng, `Σ DT_ExVAT` (kể cả bucket "(Chưa gán kênh)") = baseline CHECK-F(ii) **trừ đúng** doanh thu dòng 'T' (CHECK-C). Sai số = 0 (cùng nguồn, cùng filter).
4. **Sanity:** May tổng (chưa trừ gift) ≈ 326–351B vùng tham chiếu; MT là nhóm kênh lớn nhất (~65% ref `_SPEC_notes.md`); không có giá trị kênh lạ ngoài danh sách CHECK-B.
5. Cross-check độc lập (nếu NSAW MCP token còn hạn): `get_pl_by_dimension`/`get_uc1_revenue_variance` theo kênh p40–42 — lệch ≤ ~2.5% (khác scope nội bộ đã biết, §2.5) và ghi chú lệch vào bàn giao.
6. Flow re-run được (Actions → Run lần 2 không lỗi) — vì finance sẽ cần refresh.

---

## 8. RỦI RO & GIẢM THIỂU (tóm tắt)

| Rủi ro | Mức | Giảm thiểu |
|---|---|---|
| Nhóm Kênh NULL ở Apr/May (enrichment gãy) | **CAO — gate** | CHECK-B + fallback B1–B4; không build mù |
| Không có dòng flag 'T' → không định nghĩa được hàng tặng | **CAO — gate** | CHECK-C; dừng hỏi finance, không tự chế định nghĩa |
| MEMO# không đọc được qua dataflow (ORA-00942 cache, intermittent) | TB | CHECK-A validate-first; Reload Data; không retry mù |
| Dữ liệu May/Apr thiếu (tiền lệ DTF May ~1/3) | TB | CHECK-F (max TRANDATE + tổng vs ref) |
| ORA-28000 account anhdk khóa | THẤP | Không chặn dataflow Run; bỏ qua ở viz preview |
| Filter syntax (IS NULL trong complexFilter) | THẤP | CHECK-I trước; fallback AddColumns CASE |
| Đặt tên dataset/cột ở Save step không persist | THẤP | Kiểm tên sau Run, rename tầng dataset nếu lệch |
| Lệch định nghĩa vs NSAW (~+2.5% nội bộ) | THẤP (kỳ vọng) | Ghi rõ caveat trong bàn giao; finance chốt Q3 |

---

## 9. CÂU HỎI CHỜ FINANCE/USER CHỐT (trả lời được trước build càng tốt)

1. **Q1 — Bucket "(Chưa gán kênh)":** giữ thành 1 dòng riêng mỗi tháng (đề xuất — tổng khớp 100%) hay loại khỏi dataset?
2. **Q2 — Định nghĩa hàng tặng:** chỉ `ISFREEGIFT='T'`? Nếu cờ không dùng được (CHECK-C đỏ): dòng đơn giá ex‑VAT = 0 có được coi là hàng tặng không?
3. **Q3 — Scope doanh thu:** lấy theo chuẩn DB01/MEMO# (gồm khách nội bộ, mọi ACCTTYPE — như dashboard hiện tại) hay theo chuẩn NSAW external (loại SC=14, chỉ Income — sẽ KHÔNG khớp DB01 ~2.5%)?
4. **Q4 — Credit memo:** net vào doanh thu tháng (đề xuất, D3) hay chỉ tính CustInvc gross?
5. **Q5 — Tên dataset/nơi đặt:** `KGR_DS_DT_NhomKenh_Thang_v1` tại `/users/minhndn@bizin.vn` OK? Cần share cho ai bên finance?

---

## 10. NGOÀI PHẠM VI / GHI CHÚ VẬN HÀNH

- Dataset là **snapshot 3 tháng cố định**; muốn rolling/tháng mới → sửa filter PERIODNAME + Run lại (hoặc v2 dùng range POSTINGPERIOD sau khi CHECK-D chốt map).
- Refresh phụ thuộc upstream `(KGR) 1. DTF_CALC_INVOICE_MEMO_#` (owner anhdk) chạy thành công — hiện nghi gãy vì thiếu `DW_NS_X_CUST_INVOICE_LINES_SUPPLEMENTARY`; cần data team xác nhận trước khi cam kết lịch refresh với finance.
- Không đụng workbook DB01 trong scope này (chỉ tạo flow + dataset mới, ADD-only, không sửa/xóa artifact có sẵn).
- Mọi số trong plan lấy từ đo đạc các phiên 2026-06-03 → 06-09 — **phải re-verify bằng §4 trước khi build** (dữ liệu nguồn đã thay đổi ít nhất 1 lần: 326–337B → 342.8B).
