# BÀN GIAO — Rule-book công thức báo cáo KGR (BC01 + BC03-04-05)

**File chính:** `KGR_RuleBook_BaoCao_20260701.xlsx` (cùng thư mục) — 7 sheet: Sheet 0 Glossary (xác nhận 1 lần) + 6 sheet báo cáo. Mỗi sheet có cột **"KGR xác nhận" (Y/N)**.

## Phạm vi đã phủ
2 workbook · 6 canvas/báo cáo · **227 dòng tài liệu** (cột + dòng chỉ tiêu). 100% qua cổng review-tài-chính (sub-agent đóng vai KGR, rubric 5 ý) + harness máy.
- BC01: Summary Tập đoàn (8 cột × 25 chỉ tiêu) · Summary Ngành (4 pivot, phủ chung) · Hàng ngày (4 bảng, 55 cột).
- BC03-04-05: SFC Ước Tính (37) · SFC Thực Tế (27) · MIS (42).

## ĐIỂM KGR CẦN LƯU Ý KHI XÁC NHẬN (quan trọng)
1. **Chi phí dưới "Lợi nhuận gộp" phần lớn là ƯỚC TÍNH theo kế hoạch AOP** (tỷ lệ % × doanh thu, hoặc phân bổ theo ngày), KHÔNG phải chi phí thực phát sinh. (CP nhân viên KD/BO, roadshow, công tác, vận chuyển, bảo hành, tài chính, khác, xúc tiến, dự phòng.)
2. **"Lợi nhuận sau thuế"** = nếu LN trước thuế > 0 thì giữ **80%** (quy ước cố định) — KHÔNG phải thuế suất TNDN thực.
3. **"CP dự phòng hoạt động năm trước"** = **21% × Lợi nhuận quản lý vận hành kỳ hiện tại** (tên dòng dễ hiểu nhầm — đã ghi chú).
4. **"Tỷ lệ Xanh/Đỏ"** hiển thị = **% doanh số Xanh** = DS Xanh ÷ (DS Xanh + DS Đỏ) × 100.
5. **Báo cáo theo NGÀNH**: chi phí ước tính phân bổ về ngành theo **tỷ trọng doanh thu thực tế** (CP nhân viên KD/roadshow/công tác/vận chuyển/bảo hành/tài chính/dự phòng) hoặc **tỷ trọng doanh số KẾ HOẠCH AOP** (CP xúc tiến/nhân viên BO/khác/thu nhập khác).
6. **Phân loại NGÀNH = capture-basis**: lấy theo phân loại ngành (CLASS) ghi trên dòng hóa đơn tại thời điểm phát sinh.
7. **Phạm vi loại trừ KHÁC NHAU giữa các báo cáo** (đã mô tả trung thực theo từng nguồn live):
   - BC01 (doanh thu/giá vốn): chỉ 2 pháp nhân **Kangaroo Quốc tế (VU1) + Chi nhánh HCM**; loại **hàng thanh lý (HTL)** + **khách ký gửi** + **kênh nội bộ**.
   - SFC Thực Tế & MIS (nguồn DTF_CALC_MIS): chỉ giao dịch **đã hạch toán**; tài khoản doanh thu + thuế GTGT; loại **dòng chiết khấu**; loại **kênh nội bộ (mã 14)** — KHÔNG dùng whitelist VU1/HCM/HTL như BC01.
8. **SFC Ước Tính** = số **DỰ BÁO** từ hệ SFC (ngoài luồng OAC). Các cột số dự báo gốc (sản lượng, đơn giá, giá vốn, DS theo tuần...) → KGR xác nhận **ý nghĩa + nguồn là hệ SFC**; cách dự báo do hệ SFC tính. Các cột dẫn xuất (Giá SFC = DS÷SL; DS SFC = tổng 5 tuần; VAT suy ra) có công thức rõ.
9. **"LN còn phải thực hiện"** ở BC01 Hàng ngày: bảng **Tập đoàn** dùng mốc **LN sau thuế**; bảng **Ngành** dùng mốc **Lợi nhuận gộp** (hai mốc khác nhau — theo đúng báo cáo live).
10. **MIS — 2 điểm nên xác nhận**: (a) "Tiền vốn" lớp-3 = 50% **đơn giá** doanh thu (DT÷|SL|) × |SL| (không double-count); (b) %TB/DT & %GV/DT: mẫu số = 0 → kết quả = 0.

## Nguyên tắc tài liệu
- Mô tả ở **tầng nghiệp vụ** (đủ để tài chính tự tái lập 1 dòng số), không dùng tên field/bảng kỹ thuật.
- Số liệu lấy từ **định nghĩa LIVE** (dataflow def + viz def) tại 2026-06/07; tài liệu mô tả **cách tính**, không chốt con số tuyệt đối (số đổi theo ngày/refresh).
- Sau khi KGR xác nhận → đây là **baseline**; thay đổi sau này = change request đối chiếu baseline.
