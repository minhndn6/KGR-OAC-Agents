# STATE — Sổ tiến độ (đa-session). Cập nhật sau mỗi canvas.

## ▶ RESUME PROTOCOL (đọc ĐẦU TIÊN mỗi session / sau compaction)
1. Đọc file này (STATE) → biết canvas nào đang dở / kế tiếp + các facts đã chốt.
2. Đọc `CLAUDE.md` + skill `.claude/skills/kgr-rulebook/SKILL.md` + `references/METHOD.md` (đừng làm theo trí nhớ hội thoại).
3. Làm canvas kế theo 7 bước SKILL → harness PASS → reviewer 100% ĐẠT (DoD) → giao .md → quay lại cập nhật STATE.
> **Câu kickoff dán mỗi session:** "Đọc OAC-Column-Specs/STATE.md + CLAUDE.md + skill kgr-rulebook, làm canvas kế tiếp theo đúng quy trình (METHOD + harness + cổng reviewer 100% ĐẠT) rồi cập nhật STATE."
> Nhất quán được bảo đảm bởi 2 CỔNG (harness máy + reviewer tài chính theo rubric cố định), KHÔNG bởi trí nhớ.

## ▶▶ PHA QA (QA1→QA2) — ĐANG CHẠY (xem `docs/QA_PROCESS.md`)
Mục tiêu: thêm **3 cột QA** (qa1_calc/qa1_exclusions/qa1_note) vào mỗi .md (KHÔNG đè cột gốc) → gộp Excel mới. Mỗi file: **qa1 review → apply (+live_check nếu cần) → qa2 polish → re-render**. Sau cả 6: `render_excel.py` → `work/FINAL/KGR_RuleBook_QA_<date>.xlsx` (cột gốc + 3 cột QA + KGR xác nhận).
| File (work/rulebooks/*.json + out_md/*.md) | qa1 | apply | qa2 | rendered |
|---|---|---|---|---|
| BC01_Summary_TD | ✅(6OK/27sửa) | qa_apply✔ | ✅(27) | ✅ | XONG hết 4 bước |
| BC01_Summary_Nganh | ✅(8OK/25sửa) | qa_apply✔ | ✅(25) | ✅ | XONG 4 bước; verify OK (QA1 thực 8OK/25, block summary ghi nhầm) |
| BC01_HangNgay | ✅(12OK/43sửa) | qa_apply✔ | ✅(43) | ✅ | XONG 4 bước; LN còn phải thực hiện rõ theo 3 nhóm bảng; khớp section chính xác |
| BC0345_SFC_UocTinh | ✅(29OK/5sửa) | qa_apply✔ | ✅(5) | ✅ | XONG 4 bước; đính chính mẫu Giá SFC, xoá LIVE_CHECK |
| BC0345_SFC_ThucTe | ✅(21OK/7sửa) | qa_apply✔ | ✅(7) | ✅ | XONG 4 bước; đính chính Giá Vốn lớp-3 không ×|SL| |
| BC0345_MIS | ✅(34OK/8sửa) | qa_apply✔ | ✅(8) | ✅ | XONG 4 bước; fix double-count lớp-3, guard theo mẫu |
> QA1 JSON: work/qa/qa1_*.json. Def đã đóng băng cho RESOLVE: df_tdmetrics, df_nganh_metrics, df_daily_td, df_daily_nganh, df_sc_chain_asof, df_mis, **df_hub_invoice_memo** (giá vốn 3 lớp/CKKM/doanh thu gốc). Bước RESOLVE: agent đọc QA1 JSON + def → ghi qa1_* (cần-sửa: sửa def-grounded; OK: "(Giữ nguyên)").
> Kickoff QA (dán mỗi session): "Đọc OAC-Column-Specs/docs/QA_PROCESS.md + STATE.md, chạy QA1→QA2 cho file .md kế chưa xong (theo bảng trên) rồi cập nhật bảng + STATE; xong cả 6 → render_excel ra KGR_RuleBook_QA_<ngày>.xlsx." QA JSON lưu ở work/qa/.

### ✅ PHA QA HOÀN TẤT (2026-07-01)
Cả 6 file đã chạy đủ **QA1 → RESOLVE(def-grounded) → apply → QA2 → re-render**. 227 dòng (115 có nội dung QA def-grounded, 112 "(Giữ nguyên)"); 0 LIVE_CHECK treo; đủ 3 trường QA mọi dòng. .md QA ở `work/out_md/` (8 cột). Excel QA: **`work/FINAL/KGR_RuleBook_QA_20260701.xlsx`** (7 sheet, mỗi báo cáo 4 cột gốc GIỮ NGUYÊN + 3 cột QA + cột KGR xác nhận). check_clean --strict: SẠCH.
- Đính chính THẬT trong cột QA (không đụng cột gốc): Giá vốn/Tiền vốn **lớp-3 = 50% Doanh thu của dòng, KHÔNG ×|SL|** (Summary_TĐ, MIS, SFC Thực Tế); guard %TB/DT & %GV/DT theo MẪU SỐ=0→0; mẫu số cột "%/DS" = Doanh thu thuần (nhãn "DS" cần KGR xác nhận tên cột); "LN còn phải thực hiện" mốc khác theo bảng (Chuỗi/Kênh=LN gộp KD · Tập đoàn=LN sau thuế · Ngành=Lợi nhuận gộp); gỡ mã kỹ thuật → tên nghiệp vụ.
- QA JSON: work/qa/qa1_*_resolved.json (RESOLVE) + qa2_*.json (trau chuốt).


> Quy ước trạng thái mỗi canvas: `extracted` (đã đóng băng def) → `skeleton` → `authored` (.md draft) →
> `harness` (ALL PASS) → `reviewed` (100% ĐẠT) → `delivered` (.md vào out_md/, đã trình).

Cập-nhật-lần-cuối: khung project vừa dựng (P1).

## Snapshots live đã đóng băng (work/snapshots_live/)
- `bc01_projects.json` (BC01 v1.1, 2026) ✔
- `bc0345_projects.json` (BC03-04-05) ✔
- `df_tdmetrics_live.json` (KGR_DF_TD_Metrics_bk — flow chỉ tiêu P&L BC01) ✔
- CẦN bổ sung khi làm: df HUB `(KGR) 1. DTF_CALC_INVOICE_MEMO_V2` (doanh thu/giá vốn/CKKM/Xanh-Đỏ); df SFC/MIS cho BC03-04-05.

## BC01 — (KGR) BRD.BC01_Daily_Summary v1.1
| Canvas | Viz chính | Trạng thái | Ghi chú |
|---|---|---|---|
| BC01_Summary_TĐ | view!9 pivot "SUMMARY TẬP ĐOÀN" (8 cột + 25 chỉ tiêu) | **delivered ✔** | `out_md/BC01_Summary_TD.md` — 33/33 ĐẠT qua 3 vòng review tài chính; harness PASS; check_clean sạch. SẢN PHẨM MẪU CHUẨN (author: work/author_view9.py). |
| BC01_Summary_Ngành | view!20-23 (4 pivot ngành) + filter | **delivered ✔** | `out_md/BC01_Summary_Nganh.md` — 33/33 ĐẠT (2 vòng review); 1 bảng logic phủ cả 4 pivot qua skeleton_refs; per-ngành: a6-a17/adp = %AOP×DT_ngành, a10/12/18/19 = giá trị TĐ × (DS-KH ngành÷DS-KH TĐ). author: work/author_nganh.py |
| BC01_Hàng ngày | view!2/8/26/27 (4 bảng) + filter | **delivered ✔** | `out_md/BC01_HangNgay.md` — 55 cột (4 bảng, có section), 57/57 ĐẠT (2 vòng); nguồn Daily_Chuoi/Kenh (DF_DAILY_SC_CHAIN_ASOF), Daily_TD, Daily_Nganh. Lưu ý live: "LN còn phải thực hiện" bảng TĐ dùng LN sau thuế, bảng Ngành dùng LN gộp. |

## BC03-04-05 — SFC ước tính/thực tế/MIS
| Canvas | Viz chính | Trạng thái | Ghi chú |
|---|---|---|---|
| SFC Ước Tính | view!157 (35 cột) + 2 chart | **delivered ✔** | `out_md/BC0345_SFC_UocTinh.md` — 37 cột, 28/28 ĐẠT; nguồn = dataset DỰ BÁO SFC (db, NGOÀI luồng OAC) → cột số-gốc ghi rõ "nguồn SFC"; 3 cột dẫn xuất (Giá SFC=DS÷SL; DS SFC=tổng 5 tuần; VAT suy ra) có công thức. |
| SFC Thực Tế | view!159 (27 cột) | **delivered ✔** | `out_md/BC0345_SFC_ThucTe.md` — 27/27 ĐẠT; nguồn (KGR) DTF_CALC_MIS; scope RIÊNG (đã hạch toán, tài khoản Income+VAT, loại dòng Discount, loại kênh nội bộ mã 14 — KHÔNG whitelist BC01). |
| MIS | view!136 (40 cột) + 2 chart | **delivered ✔** | `out_md/BC0345_MIS.md` — 42/42 ĐẠT; nguồn (KGR) DTF_CALC_MIS (scope riêng như SFC Thực Tế). Soft-note KGR xác nhận khi ký: (1) 'Tiền vốn lớp-3' = 50% ĐƠN GIÁ doanh thu (DT÷|SL|) × |SL| (không double-count); (2) %TB/DT & %GV/DT: mẫu số=0 → =0. |

## Đã chốt (live, dùng lại)
- Map chỉ tiêu BC01 SUMMARY (code 1..24,101 → tên → công thức): trong `df_tdmetrics_live.json`. a4=DT−GV; a6/7/8/15/16/17=(%AOP)×DT; a10/12/18=Số ngày×(định mức tháng/30); adp(101)=1.5%×DT; a9=LNgộp−CKKM−a6−a7−a8; a14("CP quản lý vận hành")=a15+a16+a17+adp+a18; a20("Lợi nhuận quản lý vận hành")=a13−a14+a19; a21("CP dự phòng hoạt động năm trước")=21%×a20; a22("LN trước thuế")=a20−a21; a23("LN sau thuế")=(a22>0?×0.8:a22); a24=DS Xanh/DS Đỏ, hiển thị %Xanh=Xanh/(Xanh+Đỏ)×100.
- Whitelist doanh thu/giá vốn (HUB): chỉ 2 pháp nhân "CTCP LD Kangaroo Quốc tế" (VU1) + "Chi nhánh HCM"; đã hạch toán; loại HTL (hàng thanh lý) + khách ký gửi + kênh nội bộ. Giá vốn 3 lớp GVMT(MSP+tháng)→GVTK(item+pháp nhân+kỳ)→50% doanh thu; credit memo dấu âm; free-gift(DT=0)/Discount → 0.

## ✅ HOÀN TẤT (2026-07-01)
Cả 6 canvas đã GIAO (work/out_md/) + gộp **`work/FINAL/KGR_RuleBook_BaoCao_20260701.xlsx`** (7 sheet: Glossary + 6 báo cáo; 227 dòng; có cột 'KGR xác nhận'). MỌI canvas qua harness máy + cổng reviewer tài chính **100% ĐẠT**. `check_clean --strict`: SẠCH.
- Điểm KGR cần lưu ý khi ký baseline: **`work/FINAL/HANDOFF_notes.md`**.
- Việc còn lại (sau khi KGR đọc): trình confirm từng sheet; đính chính của KGR → cập nhật `work/rulebooks/*.json` rồi re-render `render_excel.py`.
