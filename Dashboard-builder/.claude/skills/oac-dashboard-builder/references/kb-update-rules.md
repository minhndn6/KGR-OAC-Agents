# Quy tắc cập nhật OAC_DASHBOARD_MASTERY.md (chống rác knowledge)

File knowledge là tài sản dùng chung ngàn lần — mỗi lần update cẩu thả là mọi phiên sau trả giá.

## Điều kiện ghi
1. **Chỉ ghi findings ĐÃ VERIFY trong phiên** (tự tay thử ≥1 lần thành công, hoặc lỗi tái hiện + workaround đã chạy). Phỏng đoán/chưa thử → KHÔNG ghi (note vào báo cáo user thay vì knowledge).
2. Finding phải **tổng quát hóa được** (lần sau gặp lại sẽ dùng). Chi tiết chỉ đúng 1 task cụ thể (tên 1 viz tạm) → không ghi.

## Đặt đúng chỗ — map loại finding → section
| Loại finding | Section đích |
|---|---|
| Login/môi trường/timeout | §0 |
| Pattern MCP mới (selector, poll, setter) | §1 |
| Cách mở/điều hướng workbook/sandbox | §2 |
| Bố cục editor (mode/canvas/panel) | §3 |
| **Commit/persist (title/note/save/reorder) — bẫy** | §4 |
| Loại viz mới / cách tạo / shelf | §5 |
| Grammar/chip/combo series | §6 |
| Properties (title/number format/axis/legend/reference line/CF) | §7 |
| Màu/branding | §8 |
| Filter (loại/scope) | §9 |
| Calculation/expression | §10 |
| Note VN | §11 |
| Canvas/layout | §12 |
| Save/persist/REST projects-json/đọc số viz | §13 |
| **Wall mới + workaround** | §14 (thêm dòng bảng) |
| Quy ước (title/note/màu/format/ADD-only) | §15 |
| Quy trình build/DoD | §16 |
| Số tham chiếu/grain dataset/readability/chẩn đoán số sai | §13b |

## Cách ghi (chống trùng, chống phình)
3. **Grep trước khi viết**: tìm chủ đề đã có chưa.
   - Đã có + ĐÚNG → không ghi (đừng diễn đạt lại).
   - Đã có nhưng SAI/lỗi thời → **SỬA TẠI CHỖ** (supersede) + thêm `(cập nhật YYYY-MM-DD)`. KHÔNG giữ song song cũ+mới. (Vd doc cũ "note=TinyMCE" đã supersede thành CKEditor.)
   - Chưa có → thêm vào đúng section, đúng vị trí logic (cạnh nội dung liên quan), KHÔNG mặc định append cuối.
4. **Giữ văn phong file**: tiếng Việt, gọn, icon `⭐ ⚠️ ✅ 📌`, bảng cho walls/options, code/selector cho snippet. 1 finding = 1-3 dòng, không tiểu luận.
5. **Không phình**: section vượt ~2 màn hình → cô đọng nội dung cũ (gộp ý trùng) thay vì chồng thêm.
6. Snippet/selector chỉ đưa vào khi tái dùng được; biến thể nhỏ → ghi 1 dòng khác biệt, không dán lại cả block.

## Changelog
7. Mỗi đợt update: thêm dòng vào `## 18. CHANGELOG`:
   `- YYYY-MM-DD: <tóm tắt 1 dòng> (§N[, §M]) [supersedes: <gì>]`
8. Xóa/sửa nội dung cũ → bắt buộc ghi `supersedes` để truy vết.

## Sau khi sửa
9. Đọc lại đoạn vừa sửa (Read đúng range) — không vỡ bảng markdown, không lạc section.
10. Báo trong report cuối: danh sách thay đổi KB (section + 1 dòng/thay đổi). Không có finding mới → ghi rõ "không có finding mới" (cũng là thông tin).
