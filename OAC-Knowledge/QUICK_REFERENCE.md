# QUICK REFERENCE — KGR OAC Data Lineage (ĐỌC TRƯỚC TIÊN)

> Bộ não tri thức về **tầng dữ liệu OAC của Kangaroo**: từ viz trên dashboard → dataset → dataflow → **bảng vật lý NSAW**. Trích **LIVE 2026-06-20** từ chính OAC (read-only). Khi cần chi tiết hơn → mở `KNOWLEDGE_INDEX.md` để biết đọc file nào.

## File này là gì / KHÔNG là gì
- **LÀ**: tầng ngữ nghĩa + lineage của OAC (workbook, dataset, dataflow) và bảng/cột vật lý NSAW mà chúng thực sự đọc.
- **KHÔNG**: không phải tài liệu nghiệp vụ NSAW gốc. Ngữ nghĩa sâu của bảng vật lý (công thức canonical, data gap) nằm ở `C:\Project\NSAW_Claude\data_context\` — **nhưng kho đó ~1 tháng chưa update, có thể sai**. Quy tắc: **bản trích live ở đây THẮNG khi mâu thuẫn** (xem `external/README.md`).

## 4 workbook & dataset chính
| Workbook | Dùng cho | Dataset nguồn chính |
|---|---|---|
| **(KGR) DB01.Revenue_v1.1** | Doanh thu/LN gộp/Xanh-Đỏ/SFC theo ngành·chuỗi·kênh·ASM | `(KGR) DTF_CALC_INVOICE_MEMO_#` (lõi), `DW_X_SALE_HISTORY_Dataset` (ASM/lịch sử), `Daily_Nganh_Report` (AOP vs actual), `KGR_DS_SFC_vs_MEMO_v1..v4` + `KGR_DS_SFC_vs_Actual_v2`, `SALE HIST w INVC`, `(KGR) DW_NS_CUSTOMER_D` (geo) |
| **(KGR) DB02.Expense_v1.1** | Waterfall P&L Tập đoàn + theo Ngành, cơ cấu chi phí | `TD_Report_PNL_Bridge`, `TD_Report_PNL_Bridge_Nganh`, `TD_Report_Long`, `Nganh_Report_Long_#` / `_TD`, `(KGR) DTF_CALC_INVOICE_MEMO_#` |
| **(KGR) BRD.BC01_Daily_Summary** | Tổng hợp ngày/lũy kế vs AOP | `(KGR) DTF_CALC_INVOICE_MEMO_#`, `Daily_TD_Report`, `Daily_Nganh_Report`, `Nganh_Report_Long_#`, `TD_Report_Long`, `AOP LINE CF` |
| **(KGR) BRD.BC03-04-05_SFC ... MIS** | SFC ước tính vs thực tế, MIS | `(KGR) DTF_CALC_MIS`, `(KGR) SFC Dataset (có AI)` |

## 🔑 Dataset HUB quan trọng nhất
**`(KGR) DTF_CALC_INVOICE_MEMO_#`** (owner anhdk) — fact grain *invoice/credit-memo line*: Doanh thu thực tế, Doanh số, Giá vốn (COGS 3-tier), LN Gộp, %GP, Xanh/Đỏ, CKKM, SP mới. Dùng bởi **3/4 workbook + 18 dataflow**. Nếu sửa nó → ảnh hưởng diện rộng (xem impact qua `lineage_graph.yaml`). Sinh bởi dataflow `(KGR) 1. DTF_CALC_INVOICE_MEMO_#` từ các bảng vật lý: `DW_NS_CUSTOMER_INVOICE_LINES_F`, `DW_NS_CUSTOMER_CREDIT_LINES_F`, `DW_NS_X_GIA_VON_MUC_TIEU_CT`, `DW_NS_X_GIA_VON_TON_KHO`, `DW_NS_X_TRADE_PROMOTION_HEADER/LINE`, `DW_NS_X_BANG_CP_LUONG`, + extensions/segments.

## Sơ đồ tầng (lineage layer cake)
```
Viz (chart trên canvas)                      → workbook_catalog.yaml
  └─ criteria column (sourceexpr)            → workbook_catalog.yaml (fields[].expression)
       └─ OAC dataset . column               → dataset_catalog.yaml
            ├─ [type=dataflow_output] dataflow steps (Join/Aggregate/AddColumns/Filter/Union)
            │                                  → dataflow_catalog.yaml
            │     └─ upstream dataset(s) … (đệ quy)
            └─ [type=db_dataset] đọc thẳng    → physical:DW_NS_*  (bảng vật lý NSAW)
                                               → physical_table_catalog.yaml  ⟵ TẦNG NỀN TỰ CHỨA
```
Trace tự động: `skill/kgr-oac-lineage/scripts/trace_field.py "<tên field/dataset>"`.

## Quy mô (verified 2026-06-20, validate PASS 0 lỗi)
- **4** workbook · **63** dataset · **40** dataflow (+2 sequence) · **60** bảng vật lý NSAW · **1070** lineage edges.
- Closure (nuôi 4 workbook): **30** dataset, **21** dataflow.
- **20/60** bảng vật lý CHƯA có trong NSAW_Claude → NSAW_Claude thiếu/cũ (xem CONFLICTS §NSAW-gaps).

## Bẫy & lưu ý nhanh
- **NSAW_Claude có thể sai** (1 tháng chưa update) → ưu tiên bản live ở đây; chỉ lấy NSAW_Claude làm gợi ý ngữ nghĩa.
- **Tên có v1/v2/v3/_bk KHÔNG nói lên bản nào đúng/đang chạy.** VD `KGR_DF_TD_Metrics_bk` (tên "backup") lại là producer ĐANG SỐNG của `TD_Report_Long`. Luôn xét `in_closure` + producer thực tế, không xét tên.
- **`SFC_vs_MEMO_v1..v4` là 4 GRAIN khác nhau** (đều DB01 dùng), KHÔNG phải version chồng nhau.
- Workbook đính nhiều **datasource KHÔNG dùng** (DB01: 10/20 không dùng) — xem workbook_catalog `datasources[].used`.
- Endpoint `dataset/datasets/metadata` của OAC này **500** → lineage vật lý lấy từ `InputDataset.columns` trong dataflow def (đã verify bằng `executePreview` flowSQL).

## Nguyên tắc số liệu (QUAN TRỌNG)
**KHÔNG lưu/khẳng định con số** — data LIVE, số đổi mỗi refresh. Cần số → lấy LIVE (`live_query_recipes.md`). KB chỉ giữ *cách tính + bất biến quan hệ*. Precedence khi mâu thuẫn: **OAC > NSAW_Claude; báo cáo BC > dashboard DB**.

## Khi nào đọc gì
- "Field này = cái gì trừ cái gì, loại trừ gì, gốc bảng nào?" → `field_dictionary.yaml` + `fields/<ds>.md` (mẫu `fields/_FLAGSHIP_*`); quy trình `HOW_TO_TRACE_A_FIELD.md` / `scripts/trace_field.py`
- "Nghĩa nghiệp vụ / công thức chuẩn của metric (a1–a20, revenue, COGS, GP, CKKM, Xanh-Đỏ, AOP, SFC)?" → `business_glossary.yaml`
- "Cần metric M theo chiều D ở grain G — lấy đâu / dựng từ đâu?" → `capability_map.yaml` + `source_selection_playbook.md` / `scripts/find_source.py`
- "Số hiện tại là bao nhiêu / data đã có chưa?" → tự chạy LIVE (`live_query_recipes.md`), KHÔNG đoán
- "Dataset X có gì, ai sinh, ai dùng, grain?" → `dataset_catalog.yaml`; "Dataflow Y biến đổi sao?" → `dataflow_catalog.yaml`; "Field gốc bảng NSAW?" → `physical_table_catalog.yaml`
- "Đổi X thì viz nào gãy?" → `lineage_graph.yaml` / trace_field.py
- "Nên archive dataflow nào?" → `archive_recommendations.md` (riêng); "Mâu thuẫn/câu hỏi chờ?" → `CONFLICTS_AND_OPEN_QUESTIONS.md`; bản đồ đầy đủ → `KNOWLEDGE_INDEX.md`
