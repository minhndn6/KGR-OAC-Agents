# OBJECTIVE — Mục tiêu & Phạm vi

## Mục tiêu tối thượng
Bàn giao cho Kangaroo một tài liệu mô tả **rule / công thức tính / loại trừ / mapping của TẤT CẢ các cột và (với báo cáo tổng hợp) tất cả các DÒNG** trên các báo cáo OAC release. Kangaroo **đọc và xác nhận (confirm)** toàn bộ. Sau khi confirm → tài liệu là **baseline (đường gốc)**: mọi thay đổi sau này được xử lý như **change request** đối chiếu baseline.

## "Confirm được" nghĩa là gì
- Người **tài chính Kangaroo** đọc mô tả một cột/dòng là **tự tái lập được một dòng số** (biết lấy số nào, ở đâu, nhân/trừ với cái gì, fallback ra sao), KHÔNG cần hỏi lại, KHÔNG cần đọc code/dataflow.
- Mô tả ở **tầng logic nghiệp vụ** (cách tính, loại trừ, mapping) — KHÔNG phải công thức kỹ thuật trong dataflow. Tên field/bảng hệ thống không xuất hiện ở cột hướng-người-dùng.

## Phạm vi (đã chốt — 2 workbook)
| Workbook | Đường dẫn | Canvas |
|---|---|---|
| (KGR) BRD.BC01_Daily_Summary v1.1 | /@Catalog/shared/(KGR) 1.Implement/...v1.1 | BC01_Hàng ngày · BC01_Summary_TĐ · BC01_Summary_Ngành |
| (KGR) BRD.BC03-04-05_SFC ước tính/thực tế/MIS | /@Catalog/shared/(KGR) Report/... | SFC Ước Tính · SFC Thực Tế · MIS |

Ngoài phạm vi: DB01.Revenue, DB02.Expense (dashboard, không phải báo cáo release).

## Nguyên tắc nền (xem SKILL.md / CLAUDE.md)
- LIVE = nguồn chân lý; công thức từ dataflow def live; KHÔNG suy bằng SQL-sum; READ-ONLY; mô tả confirm-được.

## Không phải mục tiêu (non-goals)
- KHÔNG phán xét/sửa lỗi báo cáo: coi công thức live là đúng, chỉ mô tả trung thực.
- KHÔNG tài liệu hoá công thức nội bộ dataflow cho người dùng (chỉ dùng để hiểu rồi diễn đạt nghiệp vụ).
- KHÔNG ghi ngược tri thức vào kho KB project.
