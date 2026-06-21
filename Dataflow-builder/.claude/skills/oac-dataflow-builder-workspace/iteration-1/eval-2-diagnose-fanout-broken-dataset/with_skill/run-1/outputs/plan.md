# 📋 CHẨN ĐOÁN + PLAN: Thay thế KGR_DS_SFC_vs_Actual_v2 (Canvas 14 sai số)

> Phiên eval KHÔNG có browser → toàn bộ chẩn đoán dựa trên knowledge file `C:\Project\KGR-OAC-Agents\Dataflow-builder\OAC_DATAFLOW_MASTERY.md` (golden, cập nhật 2026-06-11); mọi bước cần OAC thật được ghi thành **danh sách check sẽ chạy** (mục E). Theo Phase 3 gate của skill: turn này kết thúc bằng bản plan — **chưa build gì** cho tới khi user duyệt.

---

## A. Yêu cầu đã hiểu

Canvas 14 "SFC Plan vs Actual" (workbook `(KGR) DB01.Revenue_v1.1`) đang hiển thị số sai từ dataset `KGR_DS_SFC_vs_Actual_v2`:

| Số trên Canvas 14 | Đang hiện | Đúng phải là (golden May 2026, period 42) | Lệch |
|---|---|---|---|
| Actual QTY | **2.44M** | **713,262** (−SUM(QUANTITY) trên MEMO#, mọi SKU) | ~3.4× phồng |
| Plan QTY | **40K** | **445,043** (SUM(SL W1..W5) trên DW_SFC) | còn ~9% |

User cần: (1) chẩn đoán nguyên nhân, (2) plan dataflow thay thế để duyệt.
- Kỳ/filter: PERIODNAME = 'May 2026' (POSTINGPERIOD 42).
- Số expected: plan 445,043 · actual 713,262 (golden đã verify trong knowledge §14).

---

## B. CHẨN ĐOÁN ROOT-CAUSE

### B1. Kết luận nhanh
`KGR_DS_SFC_vs_Actual_v2` **hỏng từ thiết kế dataflow, không phải lỗi data nguồn và không sửa được ở tầng viz**. Ba lỗi chồng nhau:

### B2. Ba root-cause (theo knowledge §14-§15 + lịch sử build đã verify)

**RC1 — Actual phồng ~3.4× do FAN-OUT đa kỳ (join trước khi lọc 1 kỳ, trước khi aggregate).**
DS_v2 được dựng theo "Path B" join item-level giữa plan và actual, **đa kỳ (period 41→61 forward), KHÔNG có filter single-period trước join**. Mỗi dòng actual (item × kỳ) khớp nhiều dòng plan (item × tuần/kỳ) → dòng actual bị nhân bản; SUM trên grain đã nhân bản → 713K phồng thành 2.44M (đo lịch sử: fan-out ~4.17×, riêng Water ~1.55M; hệ số trên canvas thay đổi theo filter của viz). Knowledge §14 đã đóng đinh: *"Single-period filter (PERIODNAME='May 2026') TRIỆT fan-out"* — DS_v2 thiếu đúng điều này.

**RC2 — Plan mất ~91% do INNER JOIN item-level + viz vá bằng MAX.**
- Inner join item-level làm **rớt toàn bộ SKU có plan nhưng chưa bán** (bài học v1 đã verify: plan từ DS_v2 chỉ còn ~198K = 44% golden).
- Trên Canvas 14, Plan bị đặt **aggregation = MAX** (một cách "vá dedup" fan-out ở tầng viz) → thay vì cộng SL W1..W5 theo nhóm, MAX chỉ lấy 1 giá trị lớn nhất → sập xuống 40K, vô nghĩa. Knowledge §15 ghi nhận đúng tổ hợp này: *"Canvas 14 BROKEN (fan-out DS_v2 + Plan=MAX → 2.44M/40K/61%)"*.

**RC3 — Anti-pattern gốc: join ở grain item×kỳ rồi mới aggregate.**
Thứ tự đúng (đã verify EXACT ở `KGR_DF_SFC_vs_MEMO_v2`): **Filter 1 kỳ → Aggregate TỪNG nhánh về grain báo cáo → rồi mới Join (full outer)**. DS_v2 làm ngược → viz không thể gỡ: SUM thì phồng (RC1), MAX/AVG thì sai nghĩa (RC2). → Bắt buộc sửa ở tầng dataflow.

### B3. Vì sao KHÔNG phải các nguyên nhân khác (đã loại trừ)
- **Không phải data nguồn sai:** cùng nguồn (DW_SFC + MEMO#), recipe MEMO_v2 ra EXACT 445,043 / 713,262.
- **Không phải dấu/sign bug:** QUANTITY âm đã xử lý chuẩn bằng `0 - "QUANTITY Sum"` trong recipe đúng; sign bug cho số âm/đảo chiều chứ không phồng 3.4×.
- **Không phải scope 713K-vs-586K:** lệch scope chỉ giải thích ~18% (586,292 vs 713,262), không giải thích 2.44M.
- **Không phải blend ở viz:** Canvas 14 đọc 1 dataset (DS_v2); lỗi cartesian blend (plan nổ ~1.55M) là bệnh khác, đã ghi nhận riêng §14.

---

## C. PHƯƠNG ÁN THAY THẾ

### C0. Khuyến nghị tổng: **Phương án A trước, B chỉ khi cần grain khác**

**Phương án A (khuyến nghị — KHÔNG cần build dataflow mới):** dùng lại dataset đã build & verify EXACT:
- `KGR_DS_SFC_vs_MEMO_v2` — grain **Tên Ngành**, plan 445,043 / actual 713,262 (canonical, §14).
- `KGR_DS_SFC_vs_MEMO_v3` — grain **Ngành + Nhóm SP** (join 2 điều kiện, cột coalesce "Nhóm SP gộp") nếu Canvas 14 cần drill-down.
Việc còn lại là **sửa viz Canvas 14**: trỏ sang dataset trên, đặt aggregation **SUM** (bỏ MAX), nhãn actual ghi rõ scope "Tổng SL hóa đơn (mọi SKU)". ADD-only: không xóa DS_v2, chỉ ngừng dùng.

**Phương án B (chỉ khi user xác nhận cần dataset tên `..._SFC_vs_Actual_*` riêng hoặc grain khác v2/v3):** build dataflow mới `KGR_DF_SFC_vs_Actual_v3` theo plan dưới đây — bản chất là clone recipe đã verify của MEMO_v2, đổi tên output.

### C1. Plan chi tiết Phương án B — `KGR_DF_SFC_vs_Actual_v3`

#### Nguồn dữ liệu (sẽ trinh sát lại khi có browser — xem mục E)
| Nguồn | Vai trò | Cột lấy | Readability check |
|---|---|---|---|
| `(KGR) DW_SFC` (datamodel) | Plan | "Ngành hàng", ("Nhóm sản phẩm" nếu grain mịn), PERIODNAME, SL W1..SL W5, "Doanh thu (-VAT)" | ⏳ sẽ executePreview (mục E#4) |
| `(KGR) DTF_CALC_INVOICE_MEMO_#` (dataset, owner anhdk) | Actual | "Tên Ngành", ("Nhóm SP"), PERIODNAME, QUANTITY, "Doanh thu thực tế" | ⏳ INTERMITTENT — validate-first (mục E#3) |

#### Chuỗi node
| # | Node | Config chính |
|---|---|---|
| 1 | Add Data (PLAN) | DW_SFC — cột như bảng nguồn |
| 2 | Filter | `"PERIODNAME" IN ('May 2026')` ← **chốt triệt fan-out** |
| 3 | Aggregate | Group by: Ngành hàng (+Nhóm sản phẩm nếu grain mịn); SUM(SL W1..W5), SUM(Doanh thu (-VAT)→DT_Ke_Hoach). Không giữ cột ID; nếu buộc giữ ID → Maximum |
| 4 | Add Columns | `SL_Ke_Hoach = "SL W1"+"SL W2"+"SL W3"+"SL W4"+"SL W5"` (Apply từng cột) |
| 5 | Add Data (ACTUAL) | MEMO# — cột như bảng nguồn |
| 6 | Filter | `"PERIODNAME" IN ('May 2026')` |
| 7 | Aggregate | Group by: Tên Ngành (+Nhóm SP); SUM(QUANTITY→QUANTITY Sum), SUM(Doanh thu thực tế→DT_Thuc_Te) |
| 8 | Add Columns | `SL_Thuc_Te = 0 - "QUANTITY Sum"` (QUANTITY mang dấu ÂM — net credit, KHÔNG ABS) |
| 9 | Join | **full outer** (All+All), `"Ngành hàng" = "Tên Ngành"` (+`"Nhóm sản phẩm" = "Nhóm SP"` nếu grain mịn) — giữ nhóm chỉ-plan & chỉ-actual |
| 10 | Add Columns | `Nganh_gop = IFNULL("Ngành hàng","Tên Ngành")` (+ "Nhóm SP gộp" nếu grain mịn); `Ty_le_dat = SL_Thuc_Te / SL_Ke_Hoach` |
| 11 | Save Dataset | `KGR_DS_SFC_vs_Actual_v3`, Dataset Storage; tên commit bằng blur; kiểm tên cột sau Run |

#### Output
- Dataset: `KGR_DS_SFC_vs_Actual_v3` · Grain: 1 dòng = 1 Ngành hàng (hoặc Ngành × Nhóm SP) cho May 2026 · Cột: Nganh_gop, SL_Ke_Hoach, SL_Thuc_Te, DT_Ke_Hoach, DT_Thuc_Te, Ty_le_dat.
- ADD-only: không đụng `KGR_DS_SFC_vs_Actual_v2` cũ và mọi flow/dataset đang có.

#### Phương án thi công
**REST clone-def** (knowledge §10-§11): GET def thật của `KGR_DF_SFC_vs_MEMO_v2` (hoặc v3 nếu grain mịn) → JSON.parse → mutate tên output/cột → POST `dataflows?folderPath&dataFlowName` → Run từ **Home → Actions → Run** (editor hay hang với def REST-built). Lý do: flow >6 node, schema thật có sẵn để clone, đường này đã verify bypass canvas wall.

---

## D. VERIFY PLAN (Phase 5 sẽ kiểm thế nào)

| Số cần khớp | Expected | Nguồn đối chiếu |
|---|---|---|
| Tổng SL_Ke_Hoach | **445,043** (Water 313,894 · Home 124,655 · Cold & Hygen 6,494) | golden §14 + NSAW `get_sfc_report(period=42)` (verifier BLIND) |
| Tổng SL_Thuc_Te | **713,262** (Water 498,204 · Home 199,062 · Cold 11,741 · Khác 3,759 · Sanitary 496) | executePreview MEMO# raw + NSAW (BLIND) |
| Số dòng output | = số Ngành (~5–6 dòng; grain mịn = số cặp Ngành×Nhóm) | đếm rows — **fan-out check** |

Sanity bổ sung: không dòng trùng key join; không NULL ở Nganh_gop; SL_Thuc_Te dương (dấu đã đảo); tỷ lệ đạt tổng ~160% (713K/445K). Lệch số → tối đa 3 vòng sửa rồi dừng báo user kèm phân tích. *Lưu ý eval: không spawn được verifier subagent → khi chạy thật sẽ spawn BLIND theo references/subagents.md; plan này định nghĩa sẵn câu hỏi cho nó (2 dòng đầu bảng).*

---

## E. DANH SÁCH CHECK THỰC TẾ SẼ CHẠY (khi có browser — phiên này không chạy được)

1. **Xác nhận chẩn đoán trên def thật:** login (§0) → `GET /ui/dv/ui/api/v1/dataflows?dataFlowID=<DS_v2 flow>` → kiểm: có Filter single-period không (kỳ vọng: KHÔNG), joinType (kỳ vọng: innerjoin), join ở grain item × multi-period (41–61).
2. **Audit Canvas 14:** `GET /ui/dv/ui/api/v2/projects/json?path=<DB01>` → xác nhận viz đang trỏ DS_v2 và Plan aggregation = MAX; ghi lại grain viz cần (Ngành hay Nhóm SP) để chốt A-v2 / A-v3 / B.
3. **Readability MEMO# (validate-first, intermittent):** `executePreview` trên MEMO# filter May 2026 → phải trả rows; tổng −SUM(QUANTITY) = 713,262. 0 rows → reload dataset / cân nhắc fallback (rủi ro R2).
4. **DW_SFC May:** executePreview SUM(SL W1..W5) filter 'May 2026' = 445,043 (nguồn rev mới 342.8B — xác nhận golden chưa dịch).
5. **Dataset có sẵn còn đúng:** mở `KGR_DS_SFC_vs_MEMO_v2` (+v3) → vẫn 445,043 / 713,262.
6. **NSAW BLIND verify:** spawn verifier với `get_sfc_report(period=42)` — không đưa số builder.
7. (Nếu user muốn scope SFC 586K) check trạng thái refresh `(KGR) DTF_CALC_SFC Thực tế` — May đang PARTIAL (~1/3).
8. **Sau build (nếu B):** Run từ Home→Actions→Run → verify dataset + cột + bảng số mục D; Save workbook nhớ **click OK** dialog "Share Related Items" (Escape = HỦY save).

---

## F. RỦI RO & PHÒNG NGỪA

- **R1 — Sửa dataset mà quên sửa viz:** Plan=MAX nằm Ở VIZ Canvas 14; chỉ thay dataset vẫn ra số sai → bước bắt buộc: đặt lại aggregation SUM khi rewire (mục C0/E#2).
- **R2 — MEMO# readability intermittent (ORA-00942 transient):** validate-first (E#3); fail → reload dataset rồi thử lại; fallback `(KGR) DTF_CALC_SFC Thực tế` **chỉ sau khi refresh** (May partial ~1/3) và chấp nhận đổi scope sang 586,292.
- **R3 — Scope nhãn số actual:** 713,262 = MỌI SKU (MEMO#) ≠ 586,292 (scope item SFC plan). Dùng MEMO# thì nhãn phải là "Tổng SL hóa đơn (mọi SKU)", KHÔNG ghi "% đạt KH SFC". ❓ *Câu hỏi mở cho user khi duyệt: chọn scope 713K (khuyến nghị — nguồn sạch, đã verify) hay 586K (phải chờ refresh DTF_CALC_SFC)?*
- **R4 — Tên dataset/cột ở Save step có thể không persist** → kiểm sau Run, rename tầng dataset nếu cần (§5.3).
- **R5 — ORA-28000 (account anhdk khóa) trong preview viz:** false alarm với DataFlow Run — ignore, proceed (§13).
- **R6 — Editor Run hang với def REST-built** → luôn Run từ Home→Actions→Run (§9/§12).

---

## G. Ý KIẾN PLAN-REVIEWER (eval không spawn subagent → tự đóng vai reviewer, kết quả ghi tại đây)

Reviewer chạy checklist 6 mục theo `references/subagents.md`:

| # | Severity | Issue | Xử lý |
|---|---|---|---|
| 1 | MAJOR | Build `_vs_Actual_v3` trùng chức năng `KGR_DS_SFC_vs_MEMO_v2` đã verify EXACT — tốn công + artifact thừa | **ĐÃ SỬA:** Phương án A (reuse) đặt làm khuyến nghị chính; B chỉ kích hoạt khi user xác nhận cần tên/grain riêng (C0) |
| 2 | MAJOR | Plan ban đầu chỉ sửa dataflow, bỏ sót lỗi viz-level Plan=MAX → thay dataset xong Canvas 14 vẫn sai | **ĐÃ SỬA:** thêm R1 + bước E#2 + yêu cầu đặt SUM khi rewire |
| 3 | MINOR | Nhãn actual 713K dễ bị đọc nhầm thành "% đạt KH SFC" (scope mọi-SKU vs SFC-scope 586K) | **ĐÃ SỬA:** R3 + câu hỏi mở cho user ở gate |
| 4 | MINOR | Nếu Canvas 14 cần grain Nhóm SP, plan B phải clone từ def v3 (join 2 điều kiện + IFNULL 2 cột), không phải v2 | **ĐÃ SỬA:** ghi chú grain mịn xuyên suốt C1; E#2 chốt grain trước khi build |
| 5 | — | OK: filter single-period TRƯỚC aggregate/join cả 2 nhánh (triệt fan-out); full outer giữ nhóm chỉ-plan/chỉ-actual; không cột ID trong aggregate (nếu có → Maximum); dấu QUANTITY xử lý `0 − SUM` không ABS; verify 2 nguồn độc lập (golden + NSAW blind) + fan-out row-count check; naming `_v3` ADD-only | — |

**Verdict: APPROVE (sau 4 sửa trên, đã phản ánh vào các mục C/E/F của plan).**

---

## ⛔ ĐIỂM DỪNG (Phase 3 gate)

Theo skill: **không build khi chưa có duyệt**; phiên headless/eval không hỏi được user → turn kết thúc bằng chính bản plan này. Khi duyệt, user cần chốt 3 điều:
1. **Phương án A hay B?** (A = rewire Canvas 14 sang MEMO_v2/v3, không build mới — khuyến nghị; B = build `KGR_DF_SFC_vs_Actual_v3`).
2. **Grain Canvas 14:** Ngành (v2) hay Ngành × Nhóm SP (v3)?
3. **Scope actual:** 713,262 (MEMO#, mọi SKU — khuyến nghị) hay 586,292 (SFC-scope, chờ refresh DTF_CALC_SFC)?
