# Quy tắc cập nhật OAC_DATAFLOW_MASTERY.md (chống rác knowledge)

File knowledge là tài sản dùng chung ngàn lần — mỗi lần update cẩu thả là mọi phiên sau trả giá. Quy tắc:

## Điều kiện ghi
1. **Chỉ ghi findings ĐÃ VERIFY trong phiên** (tự tay thử ≥1 lần thành công, hoặc lỗi tái hiện được + workaround đã chạy). Phỏng đoán/chưa thử → KHÔNG ghi (có thể note vào báo cáo cho user thay vì vào knowledge).
2. Finding phải **tổng quát hóa được** (lần sau gặp lại sẽ dùng). Chi tiết chỉ đúng cho 1 task cụ thể (vd tên 1 dataset tạm) → không ghi.

## Đặt đúng chỗ — map loại finding → section
| Loại finding | Section đích |
|---|---|
| Login/môi trường/timeout | §0 |
| Pattern MCP mới (selector, poll, setter...) | §1 |
| Cách mở editor/URL/sandbox | §2 |
| Cơ chế thêm/xóa node, undo, reset | §4 |
| Hành vi commit/persist (Apply, blur, mất dữ liệu) | §5 (+ cập nhật cột "Nhóm commit" §6 nếu đổi nhóm) |
| Config/option/bẫy của 1 node cụ thể | §7.x của node đó |
| Hàm Expression mới phát hiện | §8 |
| Save/Run/persist | §9 |
| REST endpoint/header/lỗi mới | §10 |
| Schema step JSON | §11 |
| **Wall mới + workaround** | §12 (thêm dòng vào bảng) |
| Tên cột qualified/dataset/readability | §13 |
| Con số golden/recipe SFC | §14 |
| Gotcha không thuộc nhóm trên | §15 |
| Thay đổi quy trình build chuẩn | §16 |

## Cách ghi (chống trùng, chống phình)
3. **Grep trước khi viết**: tìm trong file xem chủ đề đã có chưa.
   - Đã có và ĐÚNG → không ghi gì (đừng diễn đạt lại).
   - Đã có nhưng SAI/lỗi thời → **SỬA TẠI CHỖ** (supersede), thêm `(cập nhật YYYY-MM-DD)` vào câu sửa. KHÔNG giữ song song bản cũ + mới.
   - Chưa có → thêm vào đúng section, đúng vị trí logic (cạnh nội dung liên quan), KHÔNG mặc định append cuối section.
4. **Giữ văn phong file**: tiếng Việt, gọn, icon `⭐ ⚠️ ✅ 📌`, bảng cho danh sách walls/options, code block cho snippet. 1 finding thường = 1-3 dòng, không viết tiểu luận.
5. **Không phình file**: section nào sau khi thêm vượt quá ~2 màn hình → cô đọng lại nội dung cũ trong section đó (gộp ý trùng) thay vì cứ chồng thêm.
6. Snippet code chỉ đưa vào khi pattern tái dùng được; 1 biến thể nhỏ của snippet đã có → ghi chú khác biệt 1 dòng, không dán lại cả block.

## Changelog
7. Mỗi đợt update: thêm dòng vào mục `## 18. CHANGELOG` ở CUỐI file (tạo mục nếu chưa có):
   `- YYYY-MM-DD: <tóm tắt 1 dòng> (§N[, §M]) [supersedes: <gì> nếu có]`
8. Xóa/sửa nội dung cũ → bắt buộc ghi `supersedes` trong changelog để truy vết.

## Sau khi sửa
9. Đọc lại đoạn vừa sửa (Read đúng range) — xác nhận không vỡ bảng markdown, không lạc section.
10. Báo trong report cuối cho user: danh sách thay đổi KB (section + 1 dòng tóm tắt mỗi thay đổi). Không có finding mới → ghi rõ "không có finding mới" (đó cũng là thông tin).
