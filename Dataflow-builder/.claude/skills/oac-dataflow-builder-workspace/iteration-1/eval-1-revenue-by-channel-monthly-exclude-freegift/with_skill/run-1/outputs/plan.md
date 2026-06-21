# 📋 PLAN: KGR_DF_REV_NhomKenh_Thang_v1

> **Trạng thái: CHỜ USER DUYỆT (Phase 3 gate — chưa build).**
> Môi trường phiên này KHÔNG có browser → phần trinh sát nguồn (Phase 1.2) không chạy live được; thay vào đó toàn bộ trinh sát được ghi thành **bộ pre-build checks C1–C7** (mục dưới) sẽ chạy NGAY khi có browser, TRƯỚC khi đụng vào build. Mọi nhận định nguồn bên dưới dựa trên knowledge đã verify trong `OAC_DATAFLOW_MASTERY.md` (§13–§15, cập nhật 2026-06-11).

---

## 1. Yêu cầu đã hiểu

Finance cần 1 dataset: **doanh thu thực tế (ex-VAT) theo Nhóm Kênh × tháng**, 3 kỳ **Mar/Apr/May 2026**, **loại bỏ dòng hàng tặng (free gift)**, nguồn từ **dữ liệu hóa đơn**.

- **Grain:** 1 dòng = 1 Nhóm Kênh × 1 tháng. Kỳ vọng ~N nhóm × 3 tháng (N ≈ 3–8, chốt sau check C1).
- **Measure:** Doanh thu thực tế ex-VAT (VND), **net credit memo** (CustInvc + CustCred cùng cộng — không ABS, không loại credit), **đã loại free gift**.
- **Kỳ/filter:** `"PERIODNAME" IN ('Mar 2026','Apr 2026','May 2026')` — tương ứng 📌 POSTINGPERIOD 39/40/42. ⚠️ Lọc bằng **IN-list trên PERIODNAME**, KHÔNG dùng range POSTINGPERIOD 39–42 (giữa Apr=40 và May=42 có kỳ 41 không thuộc scope).
- **Scope item:** MỌI SKU trên hóa đơn (KHÔNG áp SFC plan-scope — bài học 713K vs 586K knowledge §14 là item-scope; yêu cầu này là doanh thu hóa đơn thuần túy nên dùng full scope).
- **Số expected user cho:** không có → sẽ đối chiếu BC01 Daily Summary + NSAW (mục 7 Verify plan).

---

## 2. ⛔ Xung đột data ĐÃ BIẾT — cần user quyết trước/cùng lúc duyệt plan

**Knowledge §14 (verified live trong phiên SFC trước):** trên `(KGR) DTF_CALC_INVOICE_MEMO_#`, cột **"Nhóm Kênh"/"Tên Kênh" = NULL toàn bộ** (group-by chỉ ra 1 bucket) — tức **grain Kênh user muốn có thể KHÔNG tồn tại trong nguồn hóa đơn**. Đây đúng tình huống skill §4 yêu cầu dừng hỏi user. Dataset này CÓ grain **"Tên Chuỗi"** (BIGC/DMX/MM/...).

**Decision tree (check C1 là gate):**

| Path | Điều kiện | Hành động |
|---|---|---|
| **A (mặc định)** | C1 thấy "Nhóm Kênh" có giá trị thật ở Mar/Apr/May (lần verify trước chỉ soi ngữ cảnh May/SFC — Mar/Apr chưa soi riêng) | Build chuỗi node Path A (mục 5) |
| **B** | "Nhóm Kênh" NULL nhưng C7 tìm được cột khách hàng trong MEMO# + nguồn mapping Khách hàng→Nhóm Kênh (vd dimension Khách hàng/Kênh của DW_SFC) | Build Path B = Path A + enrich join (mục 5b), mapping dedup 1-dòng/khách trước join |
| **C** | NULL và không map được | **DỪNG — không build.** Trình user 2 lựa chọn: (i) đổi dimension sang "Tên Chuỗi" (có sẵn, nhưng đổi grain = lệch LỚN cần user đồng ý); (ii) yêu cầu team data fix upstream load cột Nhóm Kênh vào MEMO# rồi build Path A |

**Câu hỏi gộp cho user (trả lời 1 lần):**
1. Nếu rơi vào Path C, anh/chị chọn (i) Tên Chuỗi hay (ii) chờ fix upstream?
2. Xác nhận "ex-VAT" = cột `"Doanh thu thực tế"` của MEMO# (giả thuyết mặc định, sẽ kiểm bằng C3 trước build — nếu C3 chỉ ra cột khác, dùng cột C3 chốt)?

---

## 3. Nguồn dữ liệu (knowledge-based — chốt lại bằng C1–C7 trước build)

| Nguồn | Vai trò | Cột lấy | Readability / trạng thái |
|---|---|---|---|
| `(KGR) DTF_CALC_INVOICE_MEMO_#` — dataset DB, owner anhdk@bizin.vn, `XSA('anhdk@bizin.vn'.'(KGR) DTF_CALC_INVOICE_MEMO_#')`, cột UNQUALIFIED | Actual hóa đơn (nguồn chính, duy nhất ở Path A) | `"Nhóm Kênh"`, `"PERIODNAME"`, `"POSTINGPERIOD"`, `"Doanh thu thực tế"` (C3 chốt), `"CUSTCOL_SCV_LINE_ISFREEGIFT"` | ⚠️ INTERMITTENT (ORA-00942 transient; ORA-28000 chỉ chặn viz-live, KHÔNG chặn DataFlow Run) → **validate-first C5**, không pre-assume hỏng |
| `(KGR) BRD.BC01_Daily_Summary` | Golden đối chiếu tổng doanh thu tháng | — (đọc số, không join) | Đọc lúc verify |
| (Chỉ Path B) nguồn mapping Khách hàng → Nhóm Kênh — ứng viên: dimension Khách hàng/Kênh trong `(KGR) DW_SFC` | Enrich kênh | TBD ở C7 | TBD ở C7 |

---

## 4. Pre-build checks C1–C7 (thay cho trinh sát live — chạy tuần tự qua `executePreview`/REST metadata, knowledge §10, không side-effect)

| # | Check | Cách chạy | Tiêu chí PASS | FAIL → |
|---|---|---|---|---|
| **C5** (chạy đầu) | Readability MEMO# | executePreview def tối giản: Add Data MEMO# → Filter `"PERIODNAME" IN('May 2026')` → GroupBy đếm | Trả ≥1 row | 0 rows/ORA-00942 → reload dataset 1 lần, thử lại (transient §13); vẫn fail → báo user, KHÔNG lặng lẽ đổi nguồn |
| **C1** ⛔gate | Grain Nhóm Kênh | GroupBy `"Nhóm Kênh"` × `"PERIODNAME"`, SUM rev, cả 3 kỳ | ≥2 giá trị Nhóm Kênh non-NULL ở CẢ 3 kỳ | NULL → C7 (Path B) → hết đường → Path C dừng hỏi user |
| **C2** | Free-gift flag | GroupBy `"CUSTCOL_SCV_LINE_ISFREEGIFT"`: distinct values + COUNT + SUM rev theo value | Biết tập giá trị thật (T/F? 1/0? NULL?) → chốt predicate; ghi nhận **impact** rev của dòng free gift (kỳ vọng ~0; lớn bất thường → ghi báo cáo) | Cột không tồn tại → tra metadata tìm cột free-gift khác; không có → hỏi user |
| **C3** | Cột ex-VAT | SUM(`"Doanh thu thực tế"`) vs SUM(`"Doanh số thực tế"`) May 2026; tính ratio | Ratio ≈ 1.08–1.10 (VAT 8–10%) → cột nhỏ hơn = ex-VAT; cross-check tháng với BC01 | Ratio ≈ 1.0 / khó hiểu → đối chiếu BC01 từng cột; vẫn mơ hồ → hỏi user kèm 2 số |
| **C4** | Dấu doanh thu | Xem dấu SUM ở C3 (invoice-sign: QUANTITY âm — rev có thể cùng quy ước) | Quyết định cần `0 - SUM` hay giữ nguyên | — (luôn có kết luận) |
| **C6** | Đủ 3 kỳ + format PERIODNAME | GroupBy `"PERIODNAME"`,`"POSTINGPERIOD"`: rows + SUM rev mỗi kỳ; confirm format 'Mar 2026'/'Apr 2026' (knowledge mới verify 'May 2026') | Cả 3 kỳ có data, rev mỗi kỳ cùng bậc BC01 (bài học DTF_CALC_SFC May partial ~1/3 — dataset khác nhưng vẫn check completeness) | Kỳ hụt nặng → báo user trước build (lỗi data load, không phải lỗi flow) |
| **C7** (chỉ khi C1 fail) | Đường enrich kênh | `POST /dataset/datasets/metadata` trên MEMO# tìm cột khách hàng (64 cột, knowledge chỉ liệt kê ~12); tìm nguồn mapping KH→Nhóm Kênh (DW_SFC folder Khách hàng/Kênh) | Có key chung cùng kiểu + mapping 1-dòng/KH sau dedup | Không có → Path C |

---

## 5. Chuỗi node — Path A (mặc định)

| # | Node | Config chính |
|---|---|---|
| 1 | Add Data | MEMO#, 5 cột: Nhóm Kênh, PERIODNAME, POSTINGPERIOD, Doanh thu thực tế (cột C3 chốt), CUSTCOL_SCV_LINE_ISFREEGIFT |
| 2 | Filter | `"PERIODNAME" IN ('Mar 2026','Apr 2026','May 2026')` |
| 3 | Filter (expression) | Loại free gift, NULL-safe: `IFNULL("CUSTCOL_SCV_LINE_ISFREEGIFT",'F') <> 'T'` — literal chốt theo C2 |
| 4 | Aggregate | Group by: `"Nhóm Kênh"`, `"PERIODNAME"`; SUM(`"Doanh thu thực tế"`) → `DT Sum`; `"POSTINGPERIOD"` → **Maximum** (định danh/sort — KHÔNG Sum, §7.5) |
| 5 | Add Columns | `DT_ThucTe_exVAT` = `0 - "DT Sum"` nếu C4 âm, `= "DT Sum"` nếu dương (giữ node để schema ổn định; ⚠️ Apply TỪNG cột — nhóm A §5.1) |
| 6 | Select Columns | Bỏ `DT Sum` thô; giữ Nhóm Kênh, PERIODNAME, POSTINGPERIOD, DT_ThucTe_exVAT |
| 7 | Save Dataset | `KGR_DS_REV_NhomKenh_Thang_v1` · Dataset Storage · Nhóm Kênh/PERIODNAME/POSTINGPERIOD = Attribute; DT_ThucTe_exVAT = Measure/Sum · ⚠️ tên commit khi blur; kiểm tên sau Run (§5.3) |

Ghi chú: KHÔNG join ở Path A → multi-period (3 kỳ) **không có rủi ro fan-out** (fan-out 4× lịch sử là artifact join đa kỳ — §14); KHÔNG filter TYPE (giữ CustCred để net); KHÔNG áp ACCTTYPE trừ khi verify cho thấy lệch do dòng non-Income mang rev (khi đó thêm Filter `"ACCTTYPE"='Income'`, ghi báo cáo như lệch-plan nhỏ).

### 5b. Delta Path B (chỉ khi C1 fail + C7 pass)

```
Add Data (mapping KH→Nhóm Kênh)
  → Aggregate dedup: Group by KH-key; "Nhóm Kênh" → Maximum   (ép 1-dòng/KH, triệt fan-out)
  → Join: MEMO# side = All rows, mapping side = Matching rows (left outer); key KH cùng kiểu (Cast nếu lệch)
  → Add Columns: "Nhóm Kênh gộp" = IFNULL(<Nhóm Kênh mapping>, 'Chưa phân kênh')
  → tiếp node 4–7 như Path A, group theo "Nhóm Kênh gộp"
```
Sanity bắt buộc Path B: **COUNT rows trước join = sau join** (mapping đã dedup → phải bằng); tổng DT trước/sau join bằng nhau tuyệt đối.

---

## 6. Output

- **Dataflow:** `KGR_DF_REV_NhomKenh_Thang_v1` · **Dataset:** `KGR_DS_REV_NhomKenh_Thang_v1` (ADD-only, không đụng artifact có sẵn)
- **Grain:** 1 dòng = Nhóm Kênh × tháng, key duy nhất (Nhóm Kênh, PERIODNAME), ~N×3 dòng
- **Cột:** `Nhóm Kênh` (text) · `PERIODNAME` (text) · `POSTINGPERIOD` (số, sort 39/40/42) · `DT_ThucTe_exVAT` (VND, dương, ex-VAT, net credit memo, đã loại free gift)

---

## 7. Verify plan (Phase 5 sẽ kiểm thế nào)

Chưa có số expected (không chạy được executePreview phiên này) → ghi rõ nguồn đối chiếu theo đúng thứ tự skill:

| Số cần khớp | Giá trị expected | Nguồn đối chiếu |
|---|---|---|
| Tổng DT ex-VAT từng tháng (mọi nhóm kênh) | Lấy lúc verify | (2) NSAW MCP: `execute_dynamic_query` / `get_pl_report` theo posting period 39/40/42 → (3) golden `BC01_Daily_Summary` |
| DT theo Nhóm Kênh từng tháng | Lấy lúc verify | NSAW `get_pl_by_dimension` (dimension kênh) nếu hỗ trợ; không thì execute_dynamic_query |
| Delta free-gift (tổng trước − sau filter) | = số đo ở C2 | (4) executePreview trên raw MEMO# |
| Sanity bậc độ lớn | Trăm tỷ VND/tháng (plan REV May ≈213B làm mốc bậc) | §14 — ra **nghìn tỷ** → nghi fan-out/cộng nhầm cột (bài học ≈919B = 4×); ra **âm** → thiếu negation C4 |

**Sanity tự chạy:** (a) key (Nhóm Kênh, PERIODNAME) không trùng dòng; (b) không NULL ở cột group (Path A) / bucket 'Chưa phân kênh' báo cáo riêng (Path B); (c) dấu dương toàn bộ; (d) đủ đúng 3 kỳ; (e) Path B: rows & tổng DT trước/sau join bằng nhau. Verify **BLIND** (recompute NSAW TRƯỚC, mở số dataset so SAU — eval không spawn subagent thì agent chính tự làm theo thứ tự đó). **Tối đa 3 vòng sửa**; vẫn lệch không giải thích được → dừng, báo user kèm số 2 bên + giả thuyết + đã thử gì.

---

## 8. Rủi ro & phòng ngừa

- **"Nhóm Kênh" NULL trong MEMO# (rủi ro số 1, có tiền lệ verified)** → C1 gate cứng; decision tree mục 2; không build mù ra dataset 1-bucket.
- **MEMO# readability intermittent** (ORA-00942 transient; ORA-28000 chỉ chặn viz, không chặn Run) → C5 validate-first; fail thì reload dataset, không vội đổi nguồn.
- **Nhầm cột ex-VAT vs inc-VAT** → C3 ratio + BC01 trước build; user confirm câu hỏi 2.
- **Dấu âm invoice-sign** → C4; dùng `0 − SUM`, **KHÔNG ABS** (ABS cộng dương credit memo → phóng đại doanh thu).
- **Giá trị flag free-gift không như đoán** → C2 chốt literal; predicate NULL-safe bằng IFNULL.
- **Path B fan-out qua join mapping** → dedup Maximum 1-dòng/KH + sanity rows-equal.
- **Tên dataset/cột Save step không persist** (§5.3) → kiểm sau Run, rename tầng dataset nếu cần.
- **Kỳ nào đó load thiếu kiểu DTF_CALC_SFC May partial** → C6 đối chiếu bậc số từng kỳ với BC01 trước build; hụt → báo user.
- **Kỳ 41 lọt filter** → phòng bằng IN-list PERIODNAME (không range).

---

## 9. Phương án thi công

**REST clone-def** (§10–§11) — vì: (a) C1–C6 chạy bằng executePreview với def JSON, def pass được **tái dùng nguyên vẹn** cho `POST /dataflows` → không re-work, số preview = số build; (b) né trọn bộ bẫy commit canvas §5; (c) Run qua **Home → Actions → Run** (editor Run hay hang với def REST-built). Def clone từ `v2_dataflow_full.json` (schema THẬT, không hand-build từ pseudo; stepId tránh SQL reserved word). Fallback: UI canvas (7 node, 1 nguồn — trong tầm) nếu REST gặp wall mới; thao tác lạ thử trước trong sandbox `KGR_DF_SANDBOX_EXPLORE`. Kỷ luật: ADD-only, `_v1`, save theo cụm, poll xác nhận.

---

## 10. Ý kiến plan-reviewer

*(Ràng buộc eval: không spawn subagent → tự đóng vai plan-reviewer theo checklist 6 mục trong `references/subagents.md`, review bản nháp v0 rồi sửa.)*

**Verdict: REVISE → APPROVED sau sửa.** Issues đã bắt:

| Severity | Issue (bản nháp v0) | Đã sửa |
|---|---|---|
| **BLOCKER** | v0 mặc định MEMO# có "Nhóm Kênh" dùng được — mâu thuẫn knowledge §14 (NULL, verified); build theo v0 ra dataset 1-bucket vô dụng | Mục 2: C1 gate cứng + decision tree A/B/C + 2 câu hỏi gộp; Path C dừng đúng skill §4 |
| **MAJOR** | Chưa chốt cột ex-VAT ("Doanh thu thực tế" vs "Doanh số thực tế") | C3 ratio + cross BC01 + câu hỏi user #2; không build khi chưa chốt |
| **MAJOR** | v0 bỏ qua dấu invoice-sign cho revenue (chỉ QUANTITY được verify âm) | C4 + AddColumns negation có điều kiện; cấm ABS, giữ net-credit |
| **MAJOR** | Path B v0 join mapping thô = đúng pattern fan-out 4× lịch sử | Dedup Maximum 1-dòng/KH trước join + sanity rows-equal + left outer với bucket 'Chưa phân kênh' |
| **MINOR** | Filter range POSTINGPERIOD 39–42 dính kỳ 41 ngoài scope | IN-list PERIODNAME; POSTINGPERIOD chỉ làm sort key (Maximum) |
| **MINOR** | Predicate free-gift đoán 'T' cứng, không NULL-safe | C2 chốt giá trị thật + IFNULL wrap |
| **MINOR** | Format 'Mar 2026'/'Apr 2026' là suy đoán (mới verify 'May 2026') | Gộp vào C6 |
| **MINOR** | Thiếu sort key tháng | Thêm POSTINGPERIOD (Maximum) vào Aggregate + output |

**OK-points:** Path A single-source aggregate không có rủi ro fan-out dù multi-period; naming `_vN` + ADD-only đúng chuẩn; không cột ID nào bị Sum; thang verify 4 bậc đúng thứ tự skill; REST clone-def là đường proven (v2 build).

---

**Duyệt plan này chứ? Có gì cần đổi?** *(Kèm 2 câu hỏi mục 2 — trả lời gộp 1 lần. Sau duyệt: tự chủ build đến hết Phase 6, chỉ quay lại gate nếu rơi Path C hoặc lệch LỚN.)*
