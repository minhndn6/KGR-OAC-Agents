# 📋 PLAN: KGR_DF_SFC_vs_MEMO_v5_Chuoi — SFC Kế hoạch vs Thực tế theo CHUỖI, May 2026

> **Trạng thái: ⛔ CHỜ USER DUYỆT (Phase 3 gate) — chưa build.**
> Eval mode (không browser): phần trinh sát nguồn được ghi thành **checklist C0–C7 sẽ chạy** ở đầu Phase 4; thông tin nguồn/cột/số expected điền từ knowledge đã verify (`OAC_DATAFLOW_MASTERY.md` §13–§14, bản 2026-06-11).

## Yêu cầu đã hiểu
User cần 1 dataset OAC để vẽ chart so sánh **kế hoạch SFC vs thực tế bán theo TỪNG CHUỖI** (BIGC, DMX, Caophong, …) cho **tháng 5/2026**.
- **Grain: 1 dòng = 1 chuỗi** (+ 1 dòng kỹ thuật `(Ngoài chuỗi)` để đối soát tổng — sẽ loại khỏi viz).
- Cột: `Chuỗi` · `SL_Ke_Hoach` · `SL_Thuc_Te`.
- Kỳ/filter: `PERIODNAME = 'May 2026'` (= POSTINGPERIOD **42**, map 1:1).
- Số expected user cho: **không có** → đối chiếu golden numbers §14 + NSAW MCP (bảng Verify bên dưới).

## ⚠️ Quyết định scope — cần user xác nhận khi duyệt
- **Thực tế = MEMO# mọi SKU** (tổng May 2026 = **713,262**). Đây là nguồn DUY NHẤT hiện khả dụng vừa có grain Chuỗi vừa đủ data May 2026. Nhãn measure phải là **"SL thực tế (hóa đơn, mọi SKU)"** — KHÔNG được gọi "% đạt KH SFC" (scope rộng hơn plan; achievement tổng ~160% sẽ "đẹp" hơn thực chất SFC-scope ~131.7%).
- Alternative SFC-scope (**586,292** — `(KGR) DTF_CALC_SFC Thực tế`) hiện **KHÔNG dùng được**: May 2026 mới load ~1/3 (Water 155K vs golden 459K). Nếu user muốn scope này → phải refresh DTF trước, plan đổi nguồn actual (quay lại gate).

## Nguồn dữ liệu (knowledge-based; xác nhận lại bằng checks Phụ lục A)
| Nguồn | Vai trò | Cột lấy | Readability / check |
|---|---|---|---|
| `(KGR) DW_SFC` (datamodel, nền `(KGR) SFC Dataset (có AI)` owner viethl@bizin.vn) | **Plan** | Cột Chuỗi (folder "Chuỗi" có thật trong ~23 folder; tên qualified chính xác → check **C2**) · `"DW_NS_ACCOUNTINGPERIOD_D"."PERIODNAME"` · `"DW_NS_X_SFC_LINES_CF"."SL W1".."SL W5"` | C2 metadata + C3 executePreview. ⚠️ Plan KHÔNG có cột QTY tháng — monthly = SUM(SL W1..W5) |
| `(KGR) DTF_CALC_INVOICE_MEMO_#` (dataset DB, owner anhdk@bizin.vn, cột unqualified) | **Actual** | `"Tên Chuỗi"` · `"PERIODNAME"` · `"QUANTITY"` (⚠️ ÂM — invoice sign) | C4 **validate-first** (ORA-00942 transient; ORA-28000 chỉ chặn viz live, KHÔNG chặn DataFlow Run) |

Đã biết chắc từ knowledge §14: actual MEMO# **có grain Chuỗi** với values `BIGC / DMX / MM / Caophong / FPT / VHC / Nguyenkim / Thongnhat`; plan DW_SFC có cả Kênh + Chuỗi; **cả 2 phía có bucket "ngoài chuỗi" ~76% tổng** (→ phần chuỗi ~24%).

## Chuỗi node
| # | Node | Config chính |
|---|---|---|
| 1 | Add Data (P) | DW_SFC: cột Chuỗi (C2), PERIODNAME, SL W1..W5 |
| 2 | Filter (P) | `"PERIODNAME" IN ('May 2026')` — **single-period TRƯỚC aggregate/join để triệt fan-out** |
| 3 | Aggregate (P) | Group by: Chuỗi; SUM(SL W1..W5). Không có cột ID trong flow → không dính bẫy ID→Sum |
| 4 | Add Columns (P) | `SL_Ke_Hoach = "SL W1"+"SL W2"+"SL W3"+"SL W4"+"SL W5"` · `Chuoi_KH = IFNULL(<Chuỗi>, '(Ngoài chuỗi)')` ← coalesce **TRƯỚC join** (fix BLOCKER reviewer). Apply TỪNG cột |
| 5 | Add Data (A) | MEMO#: "Tên Chuỗi", PERIODNAME, QUANTITY |
| 6 | Filter (A) | `"PERIODNAME" IN ('May 2026')` |
| 7 | Aggregate (A) | Group by: Tên Chuỗi; SUM(QUANTITY) → `QUANTITY Sum` |
| 8 | Add Columns (A) | `SL_Thuc_Te = 0 - "QUANTITY Sum"` (lật dấu, **net credit — KHÔNG ABS**) · `Chuoi_TT = IFNULL("Tên Chuỗi",'(Ngoài chuỗi)')` |
| 9 | Join | **Full outer** (All+All), `Chuoi_KH = Chuoi_TT` — giữ chuỗi chỉ-có-plan lẫn chỉ-có-actual; key không bao giờ NULL nhờ bước 4/8 |
| 10 | Add Columns | `Chuỗi = IFNULL(Chuoi_KH, Chuoi_TT)` · (tuỳ chọn) coalesce 2 measure NULL→0 |
| 11 | Select Columns | Chuỗi, SL_Ke_Hoach, SL_Thuc_Te |
| 12 | Save Dataset | `KGR_DS_SFC_vs_MEMO_v5_Chuoi`, Dataset Storage; Treat As: Chuỗi=Attribute, 2 SL=Measure/Sum |

## Output
- Dataset: **`KGR_DS_SFC_vs_MEMO_v5_Chuoi`** · Grain: 1 dòng/chuỗi (~9–10 dòng = 8 chuỗi + `(Ngoài chuỗi)` ± dòng lệch-tên nếu C5 phát hiện).
- Cột: `Chuỗi` (text) · `SL_Ke_Hoach` (số, KH SFC tháng = SUM W1..W5) · `SL_Thuc_Te` (số, SL hóa đơn mọi SKU, đã net credit).
- Chart đề xuất: bar đôi theo chuỗi, filter loại `(Ngoài chuỗi)`; màu Kangaroo actual `#44BA46` / plan `#636466`.

## Verify plan (Phase 5 sẽ kiểm thế nào)
| Số cần khớp | Giá trị expected | Nguồn đối chiếu |
|---|---|---|
| Tổng `SL_Ke_Hoach` (mọi dòng, kể cả Ngoài chuỗi) | **445,043** | Golden §14 / NSAW `get_sfc_report(period=42)` |
| Tổng `SL_Thuc_Te` (mọi dòng) | **713,262** | Golden §14 / executePreview MEMO# raw |
| Tổng 8 chuỗi (loại Ngoài chuỗi) | ~24% mỗi phía (band: plan ≈ 105–110K, actual ≈ 165–175K) | §14 "cả 2 bucket ngoài chuỗi ~76%" — band sanity, không phải số cứng |
| Per-chain (BIGC, DMX, MM, Caophong, FPT, VHC, Nguyenkim, Thongnhat) | **TBD — điền từ C3/C4** trước khi build | Blind verify: NSAW `execute_dynamic_query` theo chuỗi, posting period 42 |

Sanity checks: rows sau join ≤ rows(P)+rows(A) (không fan-out) · key Chuỗi duy nhất, không dòng trùng · không NULL key (đã coalesce) · `SL_Thuc_Te > 0` mọi dòng (dấu đã lật đúng) · đếm dòng "một phía NULL nhưng có tên chuỗi" = 0 sau khi map tên (C5).
Verifier **BLIND** (Phase 5): chỉ đưa câu hỏi "tổng plan/actual theo từng chuỗi p42 = ?", KHÔNG đưa số builder tính được.

## Rủi ro & phòng ngừa
1. **NULL-key join (BLOCKER — reviewer bắt được):** NULL = NULL không match trong full outer → bucket "(Ngoài chuỗi)" tách thành 2 dòng (plan-only + actual-only). **Đã fix trong design:** coalesce `IFNULL(..., '(Ngoài chuỗi)')` ở node 4/8 TRƯỚC join. ⚠️ Empty-string `''` không bị IFNULL bắt → C3/C4 kiểm distinct values; nếu có `''` thì dùng `CASE`.
2. **Lệch chính tả tên chuỗi 2 nguồn** (vd "BIGC" vs "BigC") → full outer sẽ âm thầm tách dòng. C5 so distinct 2 phía; nếu lệch → thêm node Group/Transform map về chuẩn MEMO#.
3. **MEMO# readability INTERMITTENT** → C4 validate-first qua executePreview; 0 rows/ORA-00942 → reload dataset rồi thử lại; vẫn fail → **DỪNG báo user** (KHÔNG fallback sang DTF_CALC_SFC vì May partial).
4. **`KGR_DF_SFC_vs_MEMO_v4_Chuoi` đã tồn tại** (built 2026-06-07 via POST, CHƯA verify số) → C1 đọc def trước: nếu đúng design + số verify → **REUSE** (Run + verify, khỏi build trùng artifact); nếu sai/thiếu → build v5, **ADD-only**, không sửa/xóa v4.
5. **Tên dataset/cột ở Save step đôi khi không persist** (§5.3) → kiểm tên cột sau Run, rename tầng dataset nếu cần.
6. Nếu C2 phát hiện cột **chain-ID numeric tồn tại ở CẢ 2 nguồn** → đổi join key sang ID (bền hơn text); đây là lệch nhỏ, không cần re-gate.
7. Plan-side: nếu C3 cho thấy dim Chuỗi KHÔNG nối được tới SFC_LINES (tổng ≠ 445,043 hoặc toàn NULL) → mâu thuẫn data-vs-yêu cầu → **dừng, hỏi user** (theo SKILL §4).

## Phương án thi công
**REST clone-def** (knowledge §10–§11): GET def `KGR_DF_SFC_vs_MEMO_v2` (schema THẬT đã verify, đừng hand-build) → mutate in-place (đổi cột chain, thêm AddColumns coalesce, đổi `joinOn`, đổi output name) → **POST** `/dataflows?folderPath=…&dataFlowName=KGR_DF_SFC_vs_MEMO_v5_Chuoi` → Run qua **Home → Actions → Run** (editor Run hay HANG với flow REST-built).
Lý do: 12 node + 2 nguồn vượt ngưỡng UI thoải mái (~6 node); các wall UI đã biết (Add Selected không propagate trên flow đã lưu, Aggregate picker, popup canvas); REST đã verified end-to-end cho chính họ flow SFC_vs_MEMO này. stepId tránh SQL reserved word (`GB_P`, `IN2`… không dùng `IN`).

## Ý kiến plan-reviewer
*(Eval mode không spawn subagent → tự đóng vai reviewer theo template `references/subagents.md` §1, checklist 6 mục, phản biện trên draft v0 của plan này.)*

```json
{
  "issues": [
    {"severity": "BLOCKER", "point": "Draft v0 join thẳng cột chuỗi raw 2 phía: bucket 'ngoài chuỗi' NULL cả 2 bên, NULL=NULL không match trong full outer → tách 2 dòng, grain '1 dòng = 1 chuỗi' vỡ và tổng đối soát theo dòng sai", "fix": "Coalesce IFNULL(...,'(Ngoài chuỗi)') ở node Add Columns TRƯỚC join (node 4/8)"},
    {"severity": "MAJOR", "point": "Join bằng TEXT tên chuỗi giữa 2 nguồn khác owner mà chưa có check normalization (case/spelling) — full outer lệch tên sẽ âm thầm tách dòng thay vì báo lỗi", "fix": "Thêm check C5 (so distinct 2 phía) + node mapping nếu lệch; ưu tiên chain-ID numeric nếu C2 tìm thấy ở cả 2 nguồn"},
    {"severity": "MAJOR", "point": "v4_Chuoi cùng mục đích đã tồn tại — build v5 mù là tạo artifact trùng, vi phạm tinh thần ADD-only-có-kỷ-luật", "fix": "Thêm C1: GET def v4_Chuoi, verify-reuse trước; chỉ build v5 khi v4 sai design/sai số"},
    {"severity": "MINOR", "point": "Verify plan thiếu số expected per-chain (chỉ có 2 tổng golden)", "fix": "Chấp nhận trong eval (không browser); C3/C4 điền per-chain TRƯỚC build + blind verify NSAW p42 ở Phase 5"},
    {"severity": "MINOR", "point": "IFNULL không bắt empty-string '' nếu 'ngoài chuỗi' lưu '' thay vì NULL", "fix": "C3/C4 kiểm distinct; chuyển CASE WHEN nếu gặp ''"}
  ],
  "ok_points": [
    "Filter single-period 'May 2026' TRƯỚC GroupBy/Join — đúng bài học triệt fan-out §14",
    "Full outer join đúng nghĩa plan-vs-actual (giữ chuỗi chỉ-plan / chỉ-actual)",
    "SL_Thuc_Te = 0−SUM(QUANTITY), net credit, không ABS — đúng §13/§14",
    "Không có cột ID trong flow → không dính bẫy ID→Sum; SL W1..W5 và QUANTITY đều Sum đúng",
    "Naming _vN, ADD-only, output Dataset Storage; verify plan có 2 nguồn đối chiếu độc lập (golden + NSAW)",
    "REST clone-def từ def thật v2 — tránh pseudo-schema và walls UI đã biết"
  ],
  "verdict": "REVISE → các fix BLOCKER/MAJOR đã đưa vào bản plan này → APPROVE"
}
```

Xử lý: cả 5 issue đều xác đáng — BLOCKER + 2 MAJOR đã sửa thẳng vào chuỗi node/checks; 2 MINOR ghi thành check C3/C4/C5 và rủi ro #1. Không bỏ qua issue nào.

---

## Phụ lục A — Trinh sát nguồn: checks C0–C7 (sẽ chạy ngay đầu Phase 4, khi có browser)
> Eval không có browser nên chưa chạy được; mỗi check ghi rõ lệnh + expected + hành động khi lệch. Tất cả qua same-origin fetch/evaluate_script (Bash curl bị proxy chặn — §1).

| # | Check | Cách chạy | Expected (từ knowledge) | Nếu lệch |
|---|---|---|---|---|
| C0 | Login + mở OAC | Deep-link §2; nếu redirect IDCS → login theo §0 (user vắng mặt mới tự gõ) | Vào Home OK | Dừng, báo user |
| C1 | v4_Chuoi tồn tại? def đúng? | `GET /ui/dv/ui/api/v1/dataflows?dataFlowID=<urlenc 'guid'.'KGR_DF_SFC_vs_MEMO_v4_Chuoi'>` (tìm guid qua Home search); JSON.parse 1–2 lần lấy `.definition` | Flow tồn tại (built 2026-06-07), có coalesce "Chuỗi gộp" | Def đúng design → REUSE (nhảy sang Run+Verify). Def sai/thiếu → build v5 |
| C2 | Tên qualified cột Chuỗi phía plan + tìm chain-ID | `POST /ui/dv/ui/api/v1/dataset/datasets/metadata` body `{"subjectArea":[<datasetId plan-side copy từ def v2>],"fetchAcl":"false"}` → tìm folder "Chuỗi" trong `presentation.folders` | Có cột dạng `"DW_NS_…CHUOI…"."Tên Chuỗi"` (varchar); có/không chain-ID numeric | Không có cột Chuỗi → mâu thuẫn yêu cầu-vs-data → dừng hỏi user (rủi ro #7) |
| C3 | Số plan theo chuỗi | `executePreview` (POST `…/dataflows/executePreview?stepID=GB_P`, def PHẲNG `{steps,links,stepId:"GB_P",DSSDependencies}`): InputDataset(DW_SFC: Chuỗi, PERIODNAME, SL W1..W5) → Filter May 2026 → GroupBy(Chuỗi) SUM | ~9 rows; tổng SUM(W1..W5) = **445,043**; phần chuỗi ~24% | Tổng ≠ 445,043 → soát filter/cột trước khi build (đừng build trên nền sai) |
| C4 | Readability MEMO# + số actual theo chuỗi (validate-first §13) | `executePreview`: InputDataset(MEMO#: Tên Chuỗi, PERIODNAME, QUANTITY) → Filter May 2026 → GroupBy(Tên Chuỗi) SUM(QUANTITY) | 8 chuỗi + bucket ngoài chuỗi; tổng = **−713,262**; xác nhận NULL hay `''` | 0 rows/ORA-00942 → reload dataset, retry; vẫn fail → dừng báo user |
| C5 | Normalization tên chuỗi | So distinct values C3 vs C4 (case-sensitive) | Trùng khớp 8 tên | Lệch → thêm node map (Group/Transform) về chuẩn MEMO# |
| C6 | Va chạm tên output | Home search `KGR_DS_SFC_vs_MEMO_v5_Chuoi` (datasets + dataflows) | Chưa tồn tại | Đã tồn tại → tăng version, không ghi đè (ADD-only) |
| C7 | Số đối chiếu độc lập cho Phase 5 | NSAW MCP: `execute_dynamic_query` SL theo chuỗi, posting period 42 (+ `get_sfc_report(period=42)` cho tổng) — dành cho **blind verifier**, không chạy trước lúc build để giữ blind | Per-chain bổ sung vào bảng Verify | NSAW token hết hạn (~19 ngày) → refresh token §15, hoặc verify 1 nguồn + ghi rõ trong báo cáo |

## Phụ lục B — Câu hỏi chốt khi duyệt
1. **Duyệt plan này chứ? Có gì cần đổi?**
2. Chốt scope thực tế = **MEMO# mọi SKU (713,262)** với nhãn "SL hóa đơn (mọi SKU)" — OK? (SFC-scope cần refresh DTF trước, sẽ re-plan.)
3. Giữ dòng `(Ngoài chuỗi)` trong dataset để đối soát tổng (viz sẽ ẩn) — OK?
4. Nếu C1 cho thấy **v4_Chuoi đúng design + số verify khớp** → REUSE v4 thay vì build v5 — đồng ý?

*Theo SKILL.md Phase 3: phiên eval/headless không hỏi được user → turn kết thúc tại đây, bản plan này là deliverable. Sau khi user duyệt: tự chủ hoàn toàn Phase 4→6 (build REST, Run, verify blind, báo cáo + cập nhật knowledge).*
