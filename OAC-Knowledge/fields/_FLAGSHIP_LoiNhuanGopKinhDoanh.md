# DOSSIER MẪU — "Lợi nhuận gộp kinh doanh" của Tập đoàn (báo cáo Summary)

> Ví dụ end-to-end: từ field hiển thị trên báo cáo → công thức → từng thành tố → bảng vật lý NSAW → filter/loại trừ → ý nghĩa. (Trích live 2026-06-20. SỐ luôn lấy live — xem live_query_recipes.md.)

## 1. Field hiển thị ở đâu
- Workbook **(KGR) BRD.BC01_Daily_Summary** (và DB02.Expense) — viz P&L theo chỉ tiêu.
- Field = dòng **Metric "Lợi nhuận gộp kinh doanh"** trong dataset **`TD_Report_Long`** (long-format: mỗi dòng 1 chỉ tiêu × kỳ), giá trị ở cột `Actual_Amount` (kế hoạch ở `AOP_Amount`).
- Mã chỉ tiêu = **a9**.

## 2. Dataset & dataflow sinh ra
- `TD_Report_Long` (grain: PERIODNAME × Metric_Code) ← **melt** từ `TD_Metrics_Wide` (wide, mỗi chỉ tiêu 1 cột) — producer **`KGR_DF_TD_Metrics_bk`** (⚠ tên "_bk" nhưng là producer ĐANG SỐNG; còn `KGR_DF_TD_Metrics_v1.0` đã ở folder Archived).
- Giá trị a9 = cột `a9` trong `TD_Metrics_Wide`.

## 3. Công thức (bung dần tới gốc)
```
a9 (Lợi nhuận gộp kinh doanh)
 = a4  −  a5_CP CKKM  −  a6  −  a7  −  a8
   │        │            │     │     │
   │        │            │     │     └ a8 = AOP_PER_A8 × DT_TĐ        (CP công tác — ƯỚC TÍNH theo %AOP)
   │        │            │     └────── a7 = AOP_PER_A7 × DT_TĐ        (CP roadshow/hội nghị — ƯỚC TÍNH)
   │        │            └──────────── a6 = AOP_PER_A6 × DT_TĐ        (CP nhân viên bán hàng — ƯỚC TÍNH)
   │        └─ a5_CP CKKM = sum(chi phí CKKM)  ← TRADE_PROMOTION_LINE.CKKM (qua dataset (KGR) CKKM TT)  [THỰC]
   └─ a4 (Lợi nhuận gộp) = DT_TĐ − a3_Giá Vốn
        ├─ DT_TĐ (Doanh thu thực tế) = UNION( INVOICE_LINES_F.BASE_REVENUE , CREDIT_LINES_F.BASE_REVENUE ) − "Doanh thu ngành khác"
        └─ a3_Giá Vốn = sum( CASE 3-tier ):  GVMT (GIA_VON_MUC_TIEU_CT.GVMT_SP) → GVTK (GIA_VON_TON_KHO.UNIT_COST) → fallback ;
                         hàng tặng (ISFREEGIFT='T' & DT=0) = 0 ; ITEMTYPE='Discount' = 0 ; dấu theo TYPE (CustCred = −1)
```

## 4. Bảng vật lý gốc (NSAW DW_*)
- `DW_NS_CUSTOMER_INVOICE_LINES_F` (.BASE_REVENUE, .QUANTITY, .CLASS, .TYPE, .ITEMTYPE) — doanh thu/khối lượng invoice
- `DW_NS_CUSTOMER_CREDIT_LINES_F` (tương tự) — credit memo (trừ ra)
- `DW_NS_X_GIA_VON_MUC_TIEU_CT` (.CUSTRECORD_SCV_GVMT_LINE_GVMT_SP) — giá vốn mục tiêu
- `DW_NS_X_GIA_VON_TON_KHO` (.CUSTRECORD_SCV_GVTK_UNIT_COST_L) — giá vốn tồn kho
- `DW_NS_X_TRADE_PROMOTION_LINE` (.CKKM) — chi phí khuyến mãi (a5)
- `DW_NS_X_AOP_LINE_CF` (Per DS (AOP), Chỉ tiêu (AOP)) — tỷ lệ %AOP cho a6/a7/a8
- (+ extension/segment: ITEMEXTENSION, CUSTINVCTRANSACTIONLINEEXTENSION cho ISFREEGIFT…)

## 5. Filter / loại trừ áp dụng (dọc đường)
- ISPOSTING = 'T' (đã hạch toán); ACCTTYPE IN ('Income','OthCurrLiab'); ISINACTIVE='F'.
- Loại "Vụ việc" = 'HTL' (hàng trưng bày); chỉ subsidiary trong whitelist "Tên Đơn vị" (loại nội bộ SC=14).
- AOP %: CUSTBODY_SCV_AOP_LOAI_BAO_CAO = 2 và Chỉ tiêu (AOP) 1–200.

## 6. Ý nghĩa & CẢNH BÁO (cho người đọc/agent)
- a9 = Lợi nhuận gộp **sau khi trừ** chiết khấu khuyến mãi (thực) + 3 nhóm chi phí bán hàng.
- ⚠️ **a6/a7/a8 là ƯỚC TÍNH theo tỷ lệ AOP × doanh thu, KHÔNG phải chi phí thực** → a9 mang tính kế-hoạch-hóa phần chi phí. Khi báo cáo cho sếp, nêu rõ. Muốn a9 theo chi phí THỰC → phải dựng dataflow mới từ FACT_EXPENSE/JOURNAL (xem source_selection_playbook).
- Authoritative: bản trong **TD_Report_Long (báo cáo BC01)** > mọi bản dashboard nếu lệch.

## 7. Lấy SỐ hiện tại (không cache)
executePreview OutputDataset của `KGR_DF_TD_Metrics_bk` (dataset TD_Report_Long) → lọc Metric a9, kỳ cần; hoặc dùng TD_Metrics_Wide cột `a9`. Xem `live_query_recipes.md`.
