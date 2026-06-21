# Template PLAN trình user duyệt (Phase 3 gate)

Trình GỌN — user duyệt được trong 2 phút đọc. Chi tiết kỹ thuật (uid, click-path, selector) KHÔNG đưa vào plan; đó là Phase 4.

```markdown
# 📋 PLAN: <Tên dashboard/canvas/viz, vd "Canvas CHAIN — SFC Plan vs Actual by Chuỗi">

## Thông điệp & yêu cầu đã hiểu
<1-3 câu: viz này cho C-level thấy gì, trả lời câu hỏi điều hành gì, hàm ý hành động gì>
- Canvas đích: <canvas mới TRỐNG / canvas có sẵn tên...> · Kỳ/filter: <vd May 2026 / All-Time>
- Số expected user cho (nếu có): <số / "không có — sẽ đối chiếu X">

## Nguồn dữ liệu (đã trinh sát thật)
| Dataset | Vai trò | Cột/measure dùng | Grain hỗ trợ chiều? | Readability |
|---|---|---|---|---|
| (KGR) DTF_CALC_INVOICE_MEMO_# | actual | "Doanh số thực tế", "Tên Ngành", "Tên Chuỗi" | ✅ có Chuỗi, ❌ không Kênh | ✅/⚠️ intermittent |
| KGR_DS_SFC_vs_MEMO_v2 | SFC plan+actual | SL_Thuc_Te, SL_Ke_Hoach | Ngành | ✅ |

## Viz đề xuất
| # | Viz | Loại | Shelf mapping | Màu | Title (EN) | Format | Note VN |
|---|---|---|---|---|---|---|---|
| 1 | Plan vs Actual | **Combo** | Cat(X)=Tên Ngành; Values(Y)=SL_Thuc_Te[Bar], SL_Ke_Hoach[Line] | actual #44BA46, plan #636466 | "SFC Plan vs Actual Quantity by Industry (May 2026)" | units, DP0, no-M | "...vượt KH..." |
| 2 | Cơ cấu + biên | Treemap | Boxes=Nhóm SP; Box Size=Revenue; Color=%GP Ròng | scale red→green | "..." | M / % | "..." |

## Verify plan (Phase 5 sẽ kiểm thế nào)
| Số cần khớp | Giá trị expected | Nguồn đối chiếu |
|---|---|---|
| Tổng SL_Ke_Hoach | 445,043 (Water 313,894/Home 124,655/Cold 6,494) | NSAW get_sfc_report p42 / golden |
| Tổng SL_Thuc_Te | 713,262 | executeOrPoll viz / NSAW |
+ Sanity: không mâu thuẫn viz khác, baseline 0, ratio không vỡ, dấu số đúng, persist projects/json.

## Rủi ro & phòng ngừa
- <vd: MEMO# readability intermittent → validate-first; Chuỗi có bucket "Khác" ~24-76% → Exclude tại viz level>
- <vd: title Auto-VN → đổi Custom English + verify persist; plan màu mặc định cam → set xám>

## Branding/format checklist
- Title English Custom · Number format <M/units/%> · Màu Kangaroo · Note VN · No-hardcode · ADD-only.

## Ý kiến plan-reviewer
<issue reviewer nêu + đã sửa gì / vì sao bỏ qua>
```

Sau khi trình: hỏi đúng 1 câu "Duyệt plan này chứ? Có gì cần đổi?" rồi CHỜ. Không build trước khi có đồng ý.
