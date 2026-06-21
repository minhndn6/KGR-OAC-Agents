# Quy tắc cập nhật DASHBOARD_DESIGN_MASTERY.md (chống rác knowledge)

File knowledge dùng chung ngàn lần — update cẩu thả là mọi phiên sau trả giá.

## Điều kiện ghi
1. **Chỉ ghi bài học ĐÃ KIỂM CHỨNG trong phiên**: user xác nhận đề xuất đúng/sai, persona-critic chỉ ra pattern lặp lại, hoặc thiết kế đã build và được đón nhận/bị chê. Phỏng đoán → KHÔNG ghi.
2. Bài học phải **tổng quát hóa được** (lần tư vấn sau dùng lại). Chi tiết chỉ đúng 1 dashboard cụ thể → không ghi (skill này là master THUẦN, không ôm task).

## Đặt đúng chỗ — map loại bài học → section
| Loại bài học | Section đích |
|---|---|
| Đặc trưng/khác biệt loại dashboard, audience mới | §1 |
| Pattern hỏi-khám-phá, framework audience→KPI | §2 |
| Chỉ số phái sinh mới + quyết định nó phục vụ + route | §3 (thêm dòng bảng) |
| Quan hệ dữ liệu ↔ chart, map viz OAC, anti-pattern mới | §4 |
| Layout/màu/title/tương tác/trung thực thống kê | §5 |
| Quy trình tư vấn, format Blueprint | §6 (+ blueprint-template.md nếu đổi cấu trúc) |
| Tiêu chí chất lượng mới | §7 |
- Thao tác OAC (click-path, persist) → KHÔNG ghi ở đây → OAC_DASHBOARD_MASTERY.md (kb-rules của builder). Transform/dataflow → OAC_DATAFLOW_MASTERY.md.

## Cách ghi
3. **Grep trước khi viết**: có rồi + đúng → thôi; có nhưng sai/lỗi thời → SỬA TẠI CHỖ (supersede, thêm `(cập nhật YYYY-MM-DD)`); chưa có → đúng section, cạnh nội dung liên quan.
4. Giữ văn phong: tiếng Việt, gọn, icon ⭐⚠️✅📌, bảng cho danh mục. 1 bài học = 1-3 dòng.
5. Không phình: section >~2 màn hình → cô đọng nội dung cũ thay vì chồng thêm.

## Changelog & hậu kiểm
6. Mỗi đợt: thêm dòng `## 8. CHANGELOG`: `- YYYY-MM-DD: <1 dòng> (§N) [supersedes: <gì>]`.
7. Đọc lại đoạn vừa sửa (không vỡ bảng). Báo trong report: danh sách KB changes; không có → ghi "không có bài học mới".
