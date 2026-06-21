# LIVE QUERY RECIPES — lấy SỐ tươi (không bao giờ cache số)

> Nguyên tắc: data LIVE, mọi giá trị có thể đổi mỗi lần refresh. File này dạy **cách lấy số ngay lúc cần**, và các **bất biến quan hệ** (durable) để self-check — KHÔNG ghi giá trị tuyệt đối.

## Cách lấy số cho BẤT KỲ field nào (3 đường, ưu tiên trên xuống)
1. **executePreview trên dataflow output** (chính xác nhất, đúng logic đang chạy): mở OAC (login minhndn@bizin.vn) → same-origin fetch:
   - `GET /ui/dv/ui/api/v1/dataflows?dataFlowID=<producer flow id>` → lấy `definition`.
   - `POST /ui/dv/ui/api/v1/dataflows/executePreview?stepID=<OutputDataset step>` body `{steps,links,stepId,DSSDependencies}` (header `x-csrf-token` từ `GET sessioninfo`) → `flowData` (≤30 dòng) + `flowSQL`.
   - Producer flow + output step: tra `field_dictionary.yaml > datasets.<ds>.live_query_recipe`.
   - ⚠️ Preview cắt ~31 cột & ≤30 dòng → để lấy TỔNG/aggregate theo grain mong muốn thì chạy logical SQL (đường 2) hoặc đọc dataset đã materialize.
2. **OAC logical SQL / nsaw-oac-poc** (`oac_run_logical_sql`, có thể hết token) — query subject area/dataset.
3. **nsaw-analytics MCP** (`get_pl_report`, `get_sfc_report`, `execute_dynamic_query`, `get_data_dictionary`) — báo cáo dựng sẵn; ⚠️ backend này dựa NSAW có thể lệch logic OAC (xem precedence: OAC chuẩn).

→ Khi OAC-knowledge được agent khác gọi và cần số hiện trạng: **tự chạy đường 1** (read-only), trả số kèm "tính đến thời điểm query".

## Recipe theo metric trụ (chỉ trỏ nguồn + công thức, KHÔNG số)
| Metric | Dataset (authoritative) | Cột/where | Công thức (xem field_dictionary) |
|---|---|---|---|
| Doanh thu thực tế | `(KGR) DTF_CALC_INVOICE_MEMO_#` | sum("Doanh thu thực tế") | UNION(INVOICE_LINES_F.BASE_REVENUE, CREDIT_LINES_F.BASE_REVENUE) − doanh thu ngành khác; filter ISPOSTING='T', ACCTTYPE IN('Income','OthCurrLiab'), subsidiary whitelist, Vụ việc≠'HTL' |
| Doanh số thực tế | nt | sum("Doanh số thực tế") | Doanh thu thực tế − "TAX AMT" + "Thuế ngành khác" |
| Giá vốn (COGS) | nt | sum("Giá Vốn") | CASE 3-tier: GVMT (GIA_VON_MUC_TIEU_CT) → GVTK (GIA_VON_TON_KHO) → fallback; free-gift/Discount=0 |
| LN gộp (a4) | `TD_Metrics_Wide`/`TD_Report_Long` (Metric a4) | melt Actual_Amount | a4 = Doanh thu (DT_TĐ) − a3_Giá Vốn |
| **LN gộp kinh doanh (a9)** | `TD_Report_Long` (Metric a9) báo cáo BC | melt Actual_Amount | a9 = a4 − a5_CP CKKM − a6 − a7 − a8 |
| SFC ước tính vs thực tế | **`(KGR) DTF_CALC_MIS`** (báo cáo BC03 — authoritative) | — | xem field_dictionary; DB01 dùng `KGR_DS_SFC_vs_MEMO_v*` (dashboard, ưu tiên thấp hơn) |
| AOP (kế hoạch) | `(KGR) AOP Dataset` → AOP_LINE_CF | LOAI_BAO_CAO=1 (DS), =2 (%) | xem dataflow GRAIN_ACTUAL_AOP / TD_Metrics |

## Bất biến quan hệ (durable — dùng self-check thay vì nhớ số)
- `a4 = a2(Doanh thu) − a3(Giá vốn)`; `a9 = a4 − a5 − a6 − a7 − a8` (P&L cộng dồn theo chỉ tiêu).
- `Doanh số thực tế = Doanh thu thực tế − TAX AMT + Thuế ngành khác` (chênh nhau phần thuế).
- Revenue = invoice ∪ credit-memo (credit tự âm); chỉ ACCTTYPE Income('OthCurrLiab'); loại line ISPOSTING≠'T', loại "Vụ việc"='HTL' (hàng trưng bày), chỉ subsidiary trong whitelist "Tên Đơn vị".
- Xanh/Đỏ: phân loại theo `CSEG_SCV_NHOMXANHDO` (date-range hiệu lực); kết quả luôn Xanh hoặc Đỏ.
- a10 (CP xúc tiến bán hàng) hiện là **SỐ CỨNG** trong dataflow (`247258890.47`) — ⚠️ không phải nguồn động; xem governance_flag trong field_dictionary; cần xác nhận owner.
- Smoke-test khi nghi ngờ: chạy executePreview output step → kiểm các quan hệ trên có giữ không; nếu lệch → có thể logic đổi → cập nhật KB.

## Freshness check (cấu trúc KB có còn khớp OAC không?)
`extracted_live` (2026-06-20) = ngày FETCH raw, KHÔNG phải ngày rebuild. Để phát hiện KB lỗi thời về **cấu trúc** (dataflow bị sửa sau ngày trích):
- Fetch `GET /ui/dv/ui/api/v1/homepage?...&includeCategory=dataflows&includeCategory=datasources` → so `lastModifiedTime` từng dataflow/dataset với `extracted_live`. Cái nào mới hơn → **dataflow đã đổi → cần re-extract** (chạy lại pipeline `raw/*.py`).
- `dataset_catalog.yaml.<ds>.data_last_modified` đã lưu sẵn → so với live để biết dataset nào vừa refresh.
- Số liệu thì LUÔN live (mục trên), không phụ thuộc freshness của KB cấu trúc.

## Precedence khi số/công thức mâu thuẫn
OAC live > NSAW_Claude. Trong OAC: báo cáo (BC01, BC03-04-05) > dashboard (DB01, DB02). Vd revenue: OAC dùng `BASE_REVENUE` + `ACCTTYPE IN('Income','OthCurrLiab')` — KHÁC NSAW_Claude (`BASE_CREDITAMOUNT−BASE_DEBITAMOUNT`, chỉ 'Income') → **theo OAC**.
