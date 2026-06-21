# Nganh_Report_Long_#

- **type**: dataflow_output
- **grain**: group: PERIODNAME, CLASS  (heuristic: GroupBy gần Output nhất — verify qua dataflow_catalog steps)
- **producer_flow**: KGR_DF_Nganh_Metrics_v3
- **used_by_workbooks**: ['(KGR) BRD.BC01_Daily_Summary', '(KGR) DB02.Expense_v1.1']
- **physical_tables**: []

## Cột
### AOP_Amount
- formula: `CASE "Metric_Code" WHEN 1 THEN "AOP_DoanhSo_ng" WHEN 2 THEN "AOP_DT_ng" WHEN 3 THEN "AOP_GiaVon_ng" WHEN 4 THEN ("AOP_DT_ng" - "AOP_GiaVon_ng") WHEN 5 THEN "AOP_CKKM_ng" WHEN 6 THEN "AOP_PER_A6_1" WHEN 7 THEN "AOP_PER_A7_1" WHEN 8 THEN "AOP_PER_A8_1" WHEN 9 THEN (("AOP_DT_ng" - "AOP_GiaVon_ng") - "AOP_CKKM_ng" - "AOP_PER_A6_1" - "AOP_PER_A7_1" - "AOP_PER_A8_1") WHEN 10 THEN ABS("AOP_AMT_A10_ng") W`
- physical_roots: ['DW_NS_CUSTOMER_CREDIT_LINES_F.BASE_REVENUE', 'DW_NS_CUSTOMER_CREDIT_LINES_F.CLASS', 'DW_NS_CUSTOMER_INVOICE_LINES_F.BASE_REVENUE', 'DW_NS_CUSTOMER_INVOICE_LINES_F.CLASS', 'DW_NS_X_AOP_LINE_CF.Chỉ tiêu (AOP)', 'DW_NS_X_AOP_LINE_SF_1.NETAMOUNT', 'DW_NS_X_CAM_CUSTOMRECORD_CSEG_SCV_NHOMXANHDO.ID XD', 'DW_NS_X_CUST_CREDIT_LINES_SUPPLEMENTARY.TAX1AMT', 'DW_NS_X_CUST_INVOICE_LINES_SUPPLEMENTARY_1.TAX1AMT']
- filters: ['"POSTINGPERIOD" between 42 and 42', '"ACCTTYPE" IN(\'Income\')', '"PERIODNAME" IN(\'May 2026\') and "CUSTBODY_SCV_AOP_LOAI_BAO_CAO" between 3 and 3 and "Chỉ tiêu (AOP)" between 1 and 200']
- joins: ['rightouterjoin: PERIODNAME = PERIODNAME, TRANDATE <= AsOfDate, ID CLASS = ID CLASS', 'leftouterjoin: PERIODNAME = PERIODNAME, AsOfDate = AsOfDate', 'leftouterjoin: PERIODNAME = PERIODNAME, ID CLASS = CLASS', 'leftouterjoin: _k = _k']
- shown_as: ['AOP_GiaTri_Nganh @(KGR) BRD.BC01_Daily_Summary', 'Thieu_PerDS_Nganh @(KGR) BRD.BC01_Daily_Summary', 'Thieu_GiaTri_Nganh @(KGR) BRD.BC01_Daily_Summary', 'AOP_PerDS_Nganh @(KGR) BRD.BC01_Daily_Summary', '% lệch KH @(KGR) DB02.Expense_v1.1', 'Tốt/Xấu hơn KH @(KGR) DB02.Expense_v1.1']

### Actual_Amount
- formula: `CASE WHEN "Metric_Code" = 1 THEN "a1_ng"
     WHEN "Metric_Code" = 2 THEN "DT_ng"
     WHEN "Metric_Code" = 3 THEN "a3_ng"
     WHEN "Metric_Code" = 4 THEN "a4"
     WHEN "Metric_Code" = 5 THEN "a5_ng"
     WHEN "Metric_Code" = 6 THEN "a6"
     WHEN "Metric_Code" = 7 THEN "a7"
     WHEN "Metric_Code" = 8 THEN "a8"
     WHEN "Metric_Code" = 9 THEN "a9"
     WHEN "Metric_Code" = 10 THEN "a10"
     W`
- physical_roots: ['DW_NS_CUSTOMER_CREDIT_LINES_F.BASE_REVENUE', 'DW_NS_CUSTOMER_CREDIT_LINES_F.CLASS', 'DW_NS_CUSTOMER_CREDIT_LINES_F.ITEMTYPE', 'DW_NS_CUSTOMER_CREDIT_LINES_F.QUANTITY', 'DW_NS_CUSTOMER_CREDIT_LINES_F.TRANDATE', 'DW_NS_CUSTOMER_CREDIT_LINES_F.TYPE', 'DW_NS_CUSTOMER_INVOICE_LINES_F.BASE_REVENUE', 'DW_NS_CUSTOMER_INVOICE_LINES_F.CLASS', 'DW_NS_CUSTOMER_INVOICE_LINES_F.ITEMTYPE', 'DW_NS_CUSTOMER_INVOICE_LINES_F.QUANTITY', 'DW_NS_CUSTOMER_INVOICE_LINES_F.TRANDATE', 'DW_NS_CUSTOMER_INVOICE_LINES_F.TYPE', 'DW_NS_X_AOP_LINE_CF.Chỉ tiêu (AOP)', 'DW_NS_X_AOP_LINE_CF.Per DS (AOP)', 'DW_NS_X_AOP_LINE_SF_1.NETAMOUNT', 'DW_NS_X_CAM_CUSTCREDTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_LINE_ISFREEGIFT', 'DW_NS_X_CAM_CUSTINVCTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_LINE_ISFREEGIFT', 'DW_NS_X_CAM_CUSTOMRECORD_CSEG_SCV_NHOMXANHDO.ID XD', 'DW_NS_X_CUST_CREDIT_LINES_SUPPLEMENTARY.TAX1AMT', 'DW_NS_X_CUST_INVOICE_LINES_SUPPLEMENTARY_1.TAX1AMT', 'DW_NS_X_GIA_VON_MUC_TIEU_CT.CUSTRECORD_SCV_GVMT_LINE_GVMT_SP', 'DW_NS_X_GIA_VON_TON_KHO.CUSTRECORD_SCV_GVTK_UNIT_COST_L', 'DW_NS_X_TRADE_PROMOTION_LINE.CKKM']
- filters: ['"POSTINGPERIOD" between 42 and 42', '"ACCTTYPE" IN(\'Income\')', '"PERIODNAME" IN(\'May 2026\') and "CUSTBODY_SCV_AOP_LOAI_BAO_CAO" between 3 and 3 and "Chỉ tiêu (AOP)" between 1 and 200']
- joins: ['rightouterjoin: PERIODNAME = PERIODNAME, TRANDATE <= AsOfDate, ID CLASS = ID CLASS', 'leftouterjoin: PERIODNAME = PERIODNAME, AsOfDate = AsOfDate', 'leftouterjoin: PERIODNAME = PERIODNAME, ID CLASS = CLASS', 'leftouterjoin: _k = _k']
- shown_as: ['Thieu_PerDS_Nganh @(KGR) BRD.BC01_Daily_Summary', 'Thieu_GiaTri_Nganh @(KGR) BRD.BC01_Daily_Summary', 'LuyKe_PerDS_Nganh @(KGR) BRD.BC01_Daily_Summary', 'LuyKe_GiaTri_Nganh @(KGR) BRD.BC01_Daily_Summary', '% lệch KH @(KGR) DB02.Expense_v1.1', 'Tốt/Xấu hơn KH @(KGR) DB02.Expense_v1.1']

### AsOfDate
- formula: `← (KGR) DTF_CALC_INVOICE_MEMO_#.TRANDATE`
- physical_roots: ['DW_NS_CUSTOMER_CREDIT_LINES_F.TRANDATE', 'DW_NS_CUSTOMER_INVOICE_LINES_F.TRANDATE']
- filters: ['"POSTINGPERIOD" between 42 and 42', '"ACCTTYPE" IN(\'Income\')', '"PERIODNAME" IN(\'May 2026\') and "CUSTBODY_SCV_AOP_LOAI_BAO_CAO" between 3 and 3 and "Chỉ tiêu (AOP)" between 1 and 200']
- joins: ['rightouterjoin: PERIODNAME = PERIODNAME, TRANDATE <= AsOfDate, ID CLASS = ID CLASS', 'leftouterjoin: PERIODNAME = PERIODNAME, AsOfDate = AsOfDate', 'leftouterjoin: PERIODNAME = PERIODNAME, ID CLASS = CLASS', 'leftouterjoin: _k = _k']
- shown_as: ['AsOfDate_7 @(KGR) BRD.BC01_Daily_Summary', 'AsOfDate_2 @(KGR) DB02.Expense_v1.1']

### DT_grain
- formula: `"DT_TĐ"`
- physical_roots: ['DW_NS_CUSTOMER_CREDIT_LINES_F.BASE_REVENUE', 'DW_NS_CUSTOMER_CREDIT_LINES_F.CLASS', 'DW_NS_CUSTOMER_INVOICE_LINES_F.BASE_REVENUE', 'DW_NS_CUSTOMER_INVOICE_LINES_F.CLASS']
- filters: ['"POSTINGPERIOD" between 42 and 42', '"ACCTTYPE" IN(\'Income\')', '"PERIODNAME" IN(\'May 2026\') and "CUSTBODY_SCV_AOP_LOAI_BAO_CAO" between 3 and 3 and "Chỉ tiêu (AOP)" between 1 and 200']
- joins: ['rightouterjoin: PERIODNAME = PERIODNAME, TRANDATE <= AsOfDate, ID CLASS = ID CLASS', 'leftouterjoin: PERIODNAME = PERIODNAME, AsOfDate = AsOfDate', 'leftouterjoin: PERIODNAME = PERIODNAME, ID CLASS = CLASS', 'leftouterjoin: _k = _k']

### ID CLASS
- formula: `← (KGR) DTF_CALC_INVOICE_MEMO_#.ID CLASS`
- physical_roots: ['DW_NS_CUSTOMER_CREDIT_LINES_F.CLASS', 'DW_NS_CUSTOMER_INVOICE_LINES_F.CLASS']
- filters: ['"POSTINGPERIOD" between 42 and 42', '"ACCTTYPE" IN(\'Income\')', '"PERIODNAME" IN(\'May 2026\') and "CUSTBODY_SCV_AOP_LOAI_BAO_CAO" between 3 and 3 and "Chỉ tiêu (AOP)" between 1 and 200']
- joins: ['rightouterjoin: PERIODNAME = PERIODNAME, TRANDATE <= AsOfDate, ID CLASS = ID CLASS', 'leftouterjoin: PERIODNAME = PERIODNAME, AsOfDate = AsOfDate', 'leftouterjoin: PERIODNAME = PERIODNAME, ID CLASS = CLASS', 'leftouterjoin: _k = _k']
- shown_as: ['IDCLASS @(KGR) BRD.BC01_Daily_Summary', 'AOP_GiaTri_Nganh @(KGR) BRD.BC01_Daily_Summary', 'Thieu_PerDS_Nganh @(KGR) BRD.BC01_Daily_Summary', 'Thieu_GiaTri_Nganh @(KGR) BRD.BC01_Daily_Summary', 'LuyKe_PerDS_Nganh @(KGR) BRD.BC01_Daily_Summary', 'LuyKe_GiaTri_Nganh @(KGR) BRD.BC01_Daily_Summary']

### Metric_Code
- formula: `physical Metric_Dim.Metric_Code`
- filters: ['"POSTINGPERIOD" between 42 and 42', '"ACCTTYPE" IN(\'Income\')', '"PERIODNAME" IN(\'May 2026\') and "CUSTBODY_SCV_AOP_LOAI_BAO_CAO" between 3 and 3 and "Chỉ tiêu (AOP)" between 1 and 200']
- joins: ['rightouterjoin: PERIODNAME = PERIODNAME, TRANDATE <= AsOfDate, ID CLASS = ID CLASS', 'leftouterjoin: PERIODNAME = PERIODNAME, AsOfDate = AsOfDate', 'leftouterjoin: PERIODNAME = PERIODNAME, ID CLASS = CLASS', 'leftouterjoin: _k = _k']
- shown_as: ['AOP_GiaTri_Nganh @(KGR) BRD.BC01_Daily_Summary', 'Thieu_PerDS_Nganh @(KGR) BRD.BC01_Daily_Summary', 'Thieu_GiaTri_Nganh @(KGR) BRD.BC01_Daily_Summary', 'LuyKe_PerDS_Nganh @(KGR) BRD.BC01_Daily_Summary', 'LuyKe_GiaTri_Nganh @(KGR) BRD.BC01_Daily_Summary', 'AOP_PerDS_Nganh @(KGR) BRD.BC01_Daily_Summary']

### Metric_Name
- formula: `physical Metric_Dim.Metric_Name`
- filters: ['"POSTINGPERIOD" between 42 and 42', '"ACCTTYPE" IN(\'Income\')', '"PERIODNAME" IN(\'May 2026\') and "CUSTBODY_SCV_AOP_LOAI_BAO_CAO" between 3 and 3 and "Chỉ tiêu (AOP)" between 1 and 200']
- joins: ['rightouterjoin: PERIODNAME = PERIODNAME, TRANDATE <= AsOfDate, ID CLASS = ID CLASS', 'leftouterjoin: PERIODNAME = PERIODNAME, AsOfDate = AsOfDate', 'leftouterjoin: PERIODNAME = PERIODNAME, ID CLASS = CLASS', 'leftouterjoin: _k = _k']
- shown_as: ['AOP_GiaTri_Nganh @(KGR) BRD.BC01_Daily_Summary', 'Thieu_PerDS_Nganh @(KGR) BRD.BC01_Daily_Summary', 'Thieu_GiaTri_Nganh @(KGR) BRD.BC01_Daily_Summary', 'LuyKe_PerDS_Nganh @(KGR) BRD.BC01_Daily_Summary', 'LuyKe_GiaTri_Nganh @(KGR) BRD.BC01_Daily_Summary', 'AOP_PerDS_Nganh @(KGR) BRD.BC01_Daily_Summary']

### PERIODNAME
- formula: `← (KGR) DTF_CALC_INVOICE_MEMO_#.PERIODNAME`
- physical_roots: ['DW_NS_ACCOUNTINGPERIOD_D.PERIODNAME']
- filters: ['"POSTINGPERIOD" between 42 and 42', '"ACCTTYPE" IN(\'Income\')', '"PERIODNAME" IN(\'May 2026\') and "CUSTBODY_SCV_AOP_LOAI_BAO_CAO" between 3 and 3 and "Chỉ tiêu (AOP)" between 1 and 200']
- joins: ['rightouterjoin: PERIODNAME = PERIODNAME, TRANDATE <= AsOfDate, ID CLASS = ID CLASS', 'leftouterjoin: PERIODNAME = PERIODNAME, AsOfDate = AsOfDate', 'leftouterjoin: PERIODNAME = PERIODNAME, ID CLASS = CLASS', 'leftouterjoin: _k = _k']

### Type
- formula: `physical Metric_Dim.Type`
- filters: ['"POSTINGPERIOD" between 42 and 42', '"ACCTTYPE" IN(\'Income\')', '"PERIODNAME" IN(\'May 2026\') and "CUSTBODY_SCV_AOP_LOAI_BAO_CAO" between 3 and 3 and "Chỉ tiêu (AOP)" between 1 and 200']
- joins: ['rightouterjoin: PERIODNAME = PERIODNAME, TRANDATE <= AsOfDate, ID CLASS = ID CLASS', 'leftouterjoin: PERIODNAME = PERIODNAME, AsOfDate = AsOfDate', 'leftouterjoin: PERIODNAME = PERIODNAME, ID CLASS = CLASS', 'leftouterjoin: _k = _k']

### ﻿Sort_Order
- formula: `physical Metric_Dim.﻿Sort_Order`
- filters: ['"POSTINGPERIOD" between 42 and 42', '"ACCTTYPE" IN(\'Income\')', '"PERIODNAME" IN(\'May 2026\') and "CUSTBODY_SCV_AOP_LOAI_BAO_CAO" between 3 and 3 and "Chỉ tiêu (AOP)" between 1 and 200']
- joins: ['rightouterjoin: PERIODNAME = PERIODNAME, TRANDATE <= AsOfDate, ID CLASS = ID CLASS', 'leftouterjoin: PERIODNAME = PERIODNAME, AsOfDate = AsOfDate', 'leftouterjoin: PERIODNAME = PERIODNAME, ID CLASS = CLASS', 'leftouterjoin: _k = _k']
- shown_as: ['\ufeffSort_Order @(KGR) BRD.BC01_Daily_Summary']
