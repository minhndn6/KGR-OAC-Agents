# GOVERNANCE REGISTER — rủi ro chính trực tài chính/dữ liệu (cần OWNER ký xác nhận)

> Gom các điểm "đúng kỹ thuật theo OAC live nhưng tiềm ẩn rủi ro nghiệp vụ/quản trị". Mỗi mục cần owner xác nhận có chủ đích hay cần sửa. KB chỉ ghi nhận + cảnh báo, KHÔNG tự sửa logic OAC.

| ID | Vấn đề | Sự thật (OAC live) | Rủi ro | Đề xuất | Owner ký |
|---|---|---|---|---|---|
| GR1 | **Chi phí dưới mức gộp là ƯỚC TÍNH theo AOP** | a6/a7/a8/a15/a16/a17 = %AOP×Doanh thu; a10/a12/a18 = AOP_AMT×ngày/30 | "Lợi nhuận" (a9/a11/a13/a20) là plan-vs-actual lai → không phải lợi nhuận thực (GAAP) | Gắn nhãn "(mô hình AOP)"; muốn lợi nhuận THỰC → dựng từ FACT_EXPENSE/JOURNAL | ☐ |
| GR2 | **a10 (CP xúc tiến) = SỐ CỨNG** | `AOP_AMT_A10 = 247.258.890,47` nhúng trong KGR_DF_Nganh_Metrics_v3/TD_Metrics_bk | Lỗi thời ngầm; không theo kỳ/đơn vị | Thay bằng nguồn động (bảng AOP) hoặc tham số hóa | ☐ |
| GR3 | **Thuế TNDN = ×0,21 cứng** | a21 = a20 × 0.21 | Thuế suất thay đổi → sai âm thầm | Tham số hóa thuế suất | ☐ |
| GR4 | **Doanh thu Tập đoàn lọc bằng whitelist 2 pháp nhân CỨNG** | `"Tên Đơn vị" IN('CTCP LD Kangaroo Quốc tế','Chi nhánh HCM')` | Thêm pháp nhân mới → bị rớt khỏi doanh thu âm thầm (rủi ro hợp nhất) | Chuyển sang loại trừ theo cờ nội bộ động, hoặc duyệt định kỳ danh sách | ☐ |
| GR5 | **Mệnh đề `"Kênh nội bộ" IN('T')` lặp + nghĩa chưa rõ** | Filter_0 có 2 lần (idempotent, KHÔNG đổi số); Filter_1 có 1 lần; nghĩa 'T'=gồm hay loại nội bộ? | Dấu vết copy-paste; nghĩa mơ hồ | Dọn mệnh đề lặp + xác nhận nghĩa (xem CONFLICTS F1) | ☐ |
| GR6 | **Revenue OAC ≠ định nghĩa NSAW_Claude** | OAC: `BASE_REVENUE` (UNION invoice+credit), ACCTTYPE IN('Income','OthCurrLiab'); NSAW: BASE_CR−DB, chỉ 'Income' | Cross-check theo NSAW sẽ "báo sai" dù OAC đúng | Theo OAC (đã chốt); cập nhật NSAW_Claude | ☐ |
| GR7 | **Producer SỐNG cho 3 dataset multi-producer chưa chắc** | xem CONFLICTS F2 | Lineage/extend có thể trỏ nhầm bản | Owner xem lịch sử Run trên UI để chốt | ☐ |

**Quy tắc cho consultant:** khi ai hỏi "lợi nhuận" (a9 trở xuống), BẮT BUỘC kèm câu: *"⚠️ Các dòng chi phí dưới lợi nhuận gộp là ƯỚC TÍNH theo AOP (không phải chi phí thực); a10 & thuế là số cứng — xem governance_register."*
