# Template BLUEPRINT — artifact bàn giao (trình user duyệt ở Phase 4)

Trình GỌN — user duyệt được trong 3 phút. Blueprint phải đủ để oac-dashboard-builder thi công KHÔNG hỏi lại.

```markdown
# 📐 BLUEPRINT: <tên dashboard đề xuất>

## 1. Bối cảnh
- **Audience:** <ai xem, vai trò> · **Loại:** Executive/Operational/Analytical · **Nhịp xem:** <tuần/ngày/họp tháng> · **Màn hình:** <desktop/trình chiếu/mobile>
- **Quyết định phục vụ:** <liệt kê 2-4 quyết định định kỳ dashboard này giúp ra>

## 2. Dữ liệu (đã profile thật / theo mô tả)
| Nguồn | Grain | Dims chính | Measures chính | Kỳ có data | Chất lượng |
|---|---|---|---|---|---|
| <dataset> | <1 dòng = gì> | <dims + cardinality> | <measures + dấu/đơn vị> | <kỳ> | <✅/⚠️ null X%, trùng ID...> |

## 3. Thiết kế canvas (mỗi canvas 1 câu hỏi)
### Canvas 1: "<câu hỏi điều hành>"
| # | Viz | Loại OAC | Shelf mapping | Filter | Màu | Title (EN) | Format | Note VN (ý) |
|---|---|---|---|---|---|---|---|---|
| 1 | <tên> | <viz OAC §4> | <measure/dim → shelf nào> | <kỳ/scope> | <hex + nghĩa> | <insight-title> | <M/%/units DP0> | <1 câu> |
(lặp cho từng canvas, thứ tự overview → detail)

## 4. Metric & định nghĩa (chốt trước khi build)
| Metric | Định nghĩa/công thức | Grain | Nguồn | Số expected (verify) | Route |
|---|---|---|---|---|---|
| <tên> | <công thức đã chốt> | <grain> | <dataset/NSAW> | <số + nguồn đối chiếu> | sẵn có / My Calculations / **dataflow** |

## 5. ⭐ Chỉ số phái sinh ĐỀ XUẤT THÊM (chưa được yêu cầu)
| Chỉ số | Vì sao đắt giá (quyết định phục vụ) | Cách tính | Route |
|---|---|---|---|

## 6. Caveats & open questions
- Data quality: <vd X% bản ghi thiếu chuỗi → lát cắt chuỗi kèm caveat>
- Giả định: <những gì tự quyết, user có thể chỉnh>
- Hỏi user (gom 1 lần): <định nghĩa cần chốt / lựa chọn cần quyết>

## 7. Thứ tự build + DoD
1. <dataflow trước nếu có route dataflow> → 2. <canvas ưu tiên>...
DoD: viz đúng loại + số khớp expected (bảng §4) + title EN/note VN + màu/format đúng + persist verified.
```

Sau khi trình: hỏi đúng 1 câu "Duyệt blueprint này chứ? Có gì cần đổi?" rồi CHỜ. Không build trước khi có đồng ý.
