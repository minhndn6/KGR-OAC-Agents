# Template PLAN trình user duyệt (Phase 3 gate)

Trình bày GỌN — user cần duyệt được trong 2 phút đọc. Chi tiết kỹ thuật (schema JSON, uid, click-path) KHÔNG đưa vào plan; đó là việc của Phase 4.

```markdown
# 📋 PLAN: <Tên dataflow đề xuất, vd KGR_DF_REV_by_Channel_v1>

## Yêu cầu đã hiểu
<1-3 câu: user muốn dataset gì, grain = 1 dòng là gì, dùng để làm gì>
- Kỳ/filter: <vd PERIODNAME = 'May 2026'>
- Số expected user cho (nếu có): <số / "không có — sẽ đối chiếu X">

## Nguồn dữ liệu (đã trinh sát thật)
| Nguồn | Vai trò | Cột lấy | Readability check |
|---|---|---|---|
| (KGR) DW_SFC | Plan | "Ngành hàng", SL W1..W5, PERIODNAME | ✅ executePreview OK |
| (KGR) DTF_CALC_INVOICE_MEMO_# | Actual | "Tên Ngành", QUANTITY, PERIODNAME | ✅ trả rows / ⚠️ ... |

## Chuỗi node
| # | Node | Config chính |
|---|---|---|
| 1 | Add Data | DW_SFC, N cột |
| 2 | Filter | PERIODNAME IN ('May 2026') |
| 3 | Aggregate | Group by: Ngành hàng; SUM(SL W1..W5); ID→Maximum |
| 4 | Add Columns | SL_Ke_Hoach = SL W1+...+W5 (Apply từng cột) |
| 5 | Join | full outer, "Tên Ngành" = "Ngành hàng" |
| 6 | Save Dataset | KGR_DS_..._v1, Dataset Storage |

## Output
- Dataset: `<tên_vN>` · Grain: <...> · Cột: <danh sách + nghĩa>

## Verify plan (Phase 5 sẽ kiểm thế nào)
| Số cần khớp | Giá trị expected | Nguồn đối chiếu |
|---|---|---|
| Tổng SL_Ke_Hoach | 445,043 | golden / NSAW get_sfc_report p42 |
| Tổng SL_Thuc_Te | 713,262 | executePreview MEMO# raw |
+ Sanity: không fan-out (rows trước/sau join), không null join key, dấu số đúng.

## Rủi ro & phòng ngừa
- <vd: MEMO# readability intermittent → validate-first trước khi build; nếu 0 rows thì fallback X>
- <vd: cột Y 2 nguồn khác kiểu → Cast trước join>

## Phương án thi công
<UI canvas / REST clone-def / hybrid> — vì <lý do: số node, độ phức tạp join, wall đã biết>

## Ý kiến plan-reviewer
<những issue reviewer nêu + đã sửa gì / vì sao bỏ qua issue nào>
```

Sau khi trình: hỏi đúng 1 câu "Duyệt plan này chứ? Có gì cần đổi?" rồi CHỜ. Không build trước khi có đồng ý.
