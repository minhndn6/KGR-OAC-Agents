# TD_Report_Long

- **type**: dataflow_output
- **grain**: group: PERIODNAME  ()
- **producer_flow**: KGR_DF_TD_Metrics_bk
- **used_by_workbooks**: ['(KGR) BRD.BC01_Daily_Summary', '(KGR) DB02.Expense_v1.1']
- **physical_tables**: []

## Cột
### AOP_Amount
- formula: `CASE WHEN "Metric_Code" = 10 THEN "AOP_AMT_A10"
     WHEN "Metric_Code" = 12 THEN "AOP_AMT_A12"
     WHEN "Metric_Code" = 18 THEN "AOP_AMT_A18"
     WHEN "Metric_Code" = 19 THEN "AOP_AMT_A19"
     ELSE NULL END`
- physical_roots: ['DW_NS_X_AOP_LINE_CF.Chỉ tiêu (AOP)', 'DW_NS_X_AOP_LINE_SF_1.NETAMOUNT']
- filters: ['(1 = 1)', '"ACCTTYPE" IN(\'Income\')', '"CUSTBODY_SCV_AOP_LOAI_BAO_CAO" between 2 and 2 and "Chỉ tiêu (AOP)" between 1 and 200', '"Chỉ tiêu AOP is NULL" IN(\'NOT NULL\')']
- joins: ['rightouterjoin: PERIODNAME = PERIODNAME, TRANDATE <= AsOfDate', 'leftouterjoin: PERIODNAME = PERIODNAME', 'leftouterjoin: _k = _k', 'leftouterjoin: PERIODNAME = PERIODNAME, Metric_Code = Chỉ tiêu (AOP)']

### AOP_Amount_1
- formula: `{"k": "unknown", "col": "AOP_Amount_1"}`
- filters: ['(1 = 1)', '"ACCTTYPE" IN(\'Income\')', '"CUSTBODY_SCV_AOP_LOAI_BAO_CAO" between 2 and 2 and "Chỉ tiêu (AOP)" between 1 and 200', '"Chỉ tiêu AOP is NULL" IN(\'NOT NULL\')']
- joins: ['rightouterjoin: PERIODNAME = PERIODNAME, TRANDATE <= AsOfDate', 'leftouterjoin: PERIODNAME = PERIODNAME', 'leftouterjoin: _k = _k', 'leftouterjoin: PERIODNAME = PERIODNAME, Metric_Code = Chỉ tiêu (AOP)']
- shown_as: ['AOP_Amount_1 @(KGR) BRD.BC01_Daily_Summary', 'Thieu_PerDS @(KGR) BRD.BC01_Daily_Summary', 'Thieu_GiaTri @(KGR) BRD.BC01_Daily_Summary', 'Pct_AOP @(KGR) DB02.Expense_v1.1', 'AOP_Amount_1 @(KGR) DB02.Expense_v1.1']

### AOP_Amount_2
- formula: `CASE WHEN "Metric_Code"=24 THEN null ELSE "AOP_Amount_1" END`
- filters: ['(1 = 1)', '"ACCTTYPE" IN(\'Income\')', '"CUSTBODY_SCV_AOP_LOAI_BAO_CAO" between 2 and 2 and "Chỉ tiêu (AOP)" between 1 and 200', '"Chỉ tiêu AOP is NULL" IN(\'NOT NULL\')']
- joins: ['rightouterjoin: PERIODNAME = PERIODNAME, TRANDATE <= AsOfDate', 'leftouterjoin: PERIODNAME = PERIODNAME', 'leftouterjoin: _k = _k', 'leftouterjoin: PERIODNAME = PERIODNAME, Metric_Code = Chỉ tiêu (AOP)']

### AOP_Per
- formula: `"Per DS (AOP)"`
- physical_roots: ['DW_NS_X_AOP_LINE_CF.Per DS (AOP)']
- filters: ['(1 = 1)', '"ACCTTYPE" IN(\'Income\')', '"CUSTBODY_SCV_AOP_LOAI_BAO_CAO" between 2 and 2 and "Chỉ tiêu (AOP)" between 1 and 200', '"Chỉ tiêu AOP is NULL" IN(\'NOT NULL\')']
- joins: ['rightouterjoin: PERIODNAME = PERIODNAME, TRANDATE <= AsOfDate', 'leftouterjoin: PERIODNAME = PERIODNAME', 'leftouterjoin: _k = _k', 'leftouterjoin: PERIODNAME = PERIODNAME, Metric_Code = Chỉ tiêu (AOP)']
- shown_as: ['AOP_Per @(KGR) BRD.BC01_Daily_Summary']

### AOP_Per_24
- formula: `CASE WHEN "Metric_Code"=24 THEN null ELSE "AOP_Per" END`
- physical_roots: ['DW_NS_X_AOP_LINE_CF.Per DS (AOP)']
- filters: ['(1 = 1)', '"ACCTTYPE" IN(\'Income\')', '"CUSTBODY_SCV_AOP_LOAI_BAO_CAO" between 2 and 2 and "Chỉ tiêu (AOP)" between 1 and 200', '"Chỉ tiêu AOP is NULL" IN(\'NOT NULL\')']
- joins: ['rightouterjoin: PERIODNAME = PERIODNAME, TRANDATE <= AsOfDate', 'leftouterjoin: PERIODNAME = PERIODNAME', 'leftouterjoin: _k = _k', 'leftouterjoin: PERIODNAME = PERIODNAME, Metric_Code = Chỉ tiêu (AOP)']

### Actual_Amount
- formula: `CASE WHEN "Metric_Code" = 1 THEN "a1_Doanh số thực tế Sum"
     WHEN "Metric_Code" = 2 THEN "DT_TĐ"
     WHEN "Metric_Code" = 3 THEN "a3_Giá Vốn"
     WHEN "Metric_Code" = 4 THEN "a4"
     WHEN "Metric_Code" = 5 THEN "a5_CP CKKM"
     WHEN "Metric_Code" = 6 THEN "a6"
     WHEN "Metric_Code" = 7 THEN "a7"
     WHEN "Metric_Code" = 8 THEN "a8"
     WHEN "Metric_Code" = 9 THEN "a9"
     WHEN "Metric_`
- physical_roots: ['DW_NS_CUSTOMER_CREDIT_LINES_F.BASE_REVENUE', 'DW_NS_CUSTOMER_CREDIT_LINES_F.CLASS', 'DW_NS_CUSTOMER_CREDIT_LINES_F.ITEMTYPE', 'DW_NS_CUSTOMER_CREDIT_LINES_F.QUANTITY', 'DW_NS_CUSTOMER_CREDIT_LINES_F.TRANDATE', 'DW_NS_CUSTOMER_CREDIT_LINES_F.TYPE', 'DW_NS_CUSTOMER_INVOICE_LINES_F.BASE_REVENUE', 'DW_NS_CUSTOMER_INVOICE_LINES_F.CLASS', 'DW_NS_CUSTOMER_INVOICE_LINES_F.ITEMTYPE', 'DW_NS_CUSTOMER_INVOICE_LINES_F.QUANTITY', 'DW_NS_CUSTOMER_INVOICE_LINES_F.TRANDATE', 'DW_NS_CUSTOMER_INVOICE_LINES_F.TYPE', 'DW_NS_X_AOP_LINE_CF.Chỉ tiêu (AOP)', 'DW_NS_X_AOP_LINE_CF.Per DS (AOP)', 'DW_NS_X_AOP_LINE_SF_1.NETAMOUNT', 'DW_NS_X_BANG_CP_LUONG.CUSTRECORD_SCV_TY_LE_PER_LUONG', 'DW_NS_X_CAM_CUSTCREDTRANSACTIONLINEEXTENSION.CSEG_SCV_SC', 'DW_NS_X_CAM_CUSTCREDTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_DISCOUNT_AMOUNT_01', 'DW_NS_X_CAM_CUSTCREDTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_LINE_ISFREEGIFT', 'DW_NS_X_CAM_CUSTINVCTRANSACTIONLINEEXTENSION.CSEG_SCV_SC', 'DW_NS_X_CAM_CUSTINVCTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_DISCOUNT_AMOUNT_01', 'DW_NS_X_CAM_CUSTINVCTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_LINE_ISFREEGIFT', 'DW_NS_X_CAM_CUSTOMEREXTENSION.CSEG_SCV_CHAIN', 'DW_NS_X_CAM_CUSTOMRECORD_CSEG_SCV_NHOMXANHDO.ID XD', 'DW_NS_X_CUST_CREDIT_LINES_SUPPLEMENTARY.TAX1AMT', 'DW_NS_X_CUST_CREDIT_LINES_SUPPLEMENTARY.TAXRATE1', 'DW_NS_X_CUST_INVOICE_LINES_SUPPLEMENTARY_1.TAX1AMT', 'DW_NS_X_CUST_INVOICE_LINES_SUPPLEMENTARY_1.TAXRATE1', 'DW_NS_X_GIA_VON_MUC_TIEU_CT.CUSTRECORD_SCV_GVMT_LINE_GVMT_SP', 'DW_NS_X_GIA_VON_TON_KHO.CUSTRECORD_SCV_GVTK_UNIT_COST_L', 'DW_NS_X_TRADE_PROMOTION_LINE.CUSTRECORD_SCV_PRO_DIS_LINE_DISCOUNT']
- filters: ['(1 = 1)', '"ACCTTYPE" IN(\'Income\')', '"CUSTBODY_SCV_AOP_LOAI_BAO_CAO" between 2 and 2 and "Chỉ tiêu (AOP)" between 1 and 200', '"Chỉ tiêu AOP is NULL" IN(\'NOT NULL\')']
- joins: ['rightouterjoin: PERIODNAME = PERIODNAME, TRANDATE <= AsOfDate', 'leftouterjoin: PERIODNAME = PERIODNAME', 'leftouterjoin: _k = _k', 'leftouterjoin: PERIODNAME = PERIODNAME, Metric_Code = Chỉ tiêu (AOP)']
- shown_as: ['LuyKe_GiaTri @(KGR) BRD.BC01_Daily_Summary', 'Thieu_PerDS @(KGR) BRD.BC01_Daily_Summary', 'Thieu_GiaTri @(KGR) BRD.BC01_Daily_Summary', 'LuyKe_PerDS @(KGR) BRD.BC01_Daily_Summary', 'Signed_Amount @(KGR) DB02.Expense_v1.1', 'CKKM_per_GP @(KGR) DB02.Expense_v1.1']

### AsOfDate
- formula: `← (KGR) DTF_CALC_INVOICE_MEMO_#.TRANDATE`
- physical_roots: ['DW_NS_CUSTOMER_CREDIT_LINES_F.TRANDATE', 'DW_NS_CUSTOMER_INVOICE_LINES_F.TRANDATE']
- filters: ['(1 = 1)', '"ACCTTYPE" IN(\'Income\')', '"CUSTBODY_SCV_AOP_LOAI_BAO_CAO" between 2 and 2 and "Chỉ tiêu (AOP)" between 1 and 200', '"Chỉ tiêu AOP is NULL" IN(\'NOT NULL\')']
- joins: ['rightouterjoin: PERIODNAME = PERIODNAME, TRANDATE <= AsOfDate', 'leftouterjoin: PERIODNAME = PERIODNAME', 'leftouterjoin: _k = _k', 'leftouterjoin: PERIODNAME = PERIODNAME, Metric_Code = Chỉ tiêu (AOP)']
- shown_as: ['AsOfDate_1 @(KGR) BRD.BC01_Daily_Summary', 'AsOfDate_1 @(KGR) DB02.Expense_v1.1']

### Chỉ tiêu (AOP)
- formula: `physical DW_NS_X_AOP_LINE_CF.Chỉ tiêu (AOP)`
- physical_roots: ['DW_NS_X_AOP_LINE_CF.Chỉ tiêu (AOP)']
- filters: ['(1 = 1)', '"ACCTTYPE" IN(\'Income\')', '"CUSTBODY_SCV_AOP_LOAI_BAO_CAO" between 2 and 2 and "Chỉ tiêu (AOP)" between 1 and 200', '"Chỉ tiêu AOP is NULL" IN(\'NOT NULL\')']
- joins: ['rightouterjoin: PERIODNAME = PERIODNAME, TRANDATE <= AsOfDate', 'leftouterjoin: PERIODNAME = PERIODNAME', 'leftouterjoin: _k = _k', 'leftouterjoin: PERIODNAME = PERIODNAME, Metric_Code = Chỉ tiêu (AOP)']

### DT_grain
- formula: `"DT_TĐ"`
- physical_roots: ['DW_NS_CUSTOMER_CREDIT_LINES_F.BASE_REVENUE', 'DW_NS_CUSTOMER_CREDIT_LINES_F.CLASS', 'DW_NS_CUSTOMER_INVOICE_LINES_F.BASE_REVENUE', 'DW_NS_CUSTOMER_INVOICE_LINES_F.CLASS', 'DW_NS_X_CAM_CUSTCREDTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_DISCOUNT_AMOUNT_01', 'DW_NS_X_CAM_CUSTINVCTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_DISCOUNT_AMOUNT_01']
- filters: ['(1 = 1)', '"ACCTTYPE" IN(\'Income\')', '"CUSTBODY_SCV_AOP_LOAI_BAO_CAO" between 2 and 2 and "Chỉ tiêu (AOP)" between 1 and 200', '"Chỉ tiêu AOP is NULL" IN(\'NOT NULL\')']
- joins: ['rightouterjoin: PERIODNAME = PERIODNAME, TRANDATE <= AsOfDate', 'leftouterjoin: PERIODNAME = PERIODNAME', 'leftouterjoin: _k = _k', 'leftouterjoin: PERIODNAME = PERIODNAME, Metric_Code = Chỉ tiêu (AOP)']
- shown_as: ['LuyKe_PerDS @(KGR) BRD.BC01_Daily_Summary']

### Metric_Code
- formula: `physical Metric_Dim.Metric_Code`
- filters: ['(1 = 1)', '"ACCTTYPE" IN(\'Income\')', '"CUSTBODY_SCV_AOP_LOAI_BAO_CAO" between 2 and 2 and "Chỉ tiêu (AOP)" between 1 and 200', '"Chỉ tiêu AOP is NULL" IN(\'NOT NULL\')']
- joins: ['rightouterjoin: PERIODNAME = PERIODNAME, TRANDATE <= AsOfDate', 'leftouterjoin: PERIODNAME = PERIODNAME', 'leftouterjoin: _k = _k', 'leftouterjoin: PERIODNAME = PERIODNAME, Metric_Code = Chỉ tiêu (AOP)']
- shown_as: ['LuyKe_GiaTri @(KGR) BRD.BC01_Daily_Summary', 'Thieu_DoanhSo @(KGR) BRD.BC01_Daily_Summary', 'Thieu_PerDS @(KGR) BRD.BC01_Daily_Summary', 'Thieu_GiaTri @(KGR) BRD.BC01_Daily_Summary', 'LuyKe_PerDS @(KGR) BRD.BC01_Daily_Summary']

### Metric_Name
- formula: `physical Metric_Dim.Metric_Name`
- filters: ['(1 = 1)', '"ACCTTYPE" IN(\'Income\')', '"CUSTBODY_SCV_AOP_LOAI_BAO_CAO" between 2 and 2 and "Chỉ tiêu (AOP)" between 1 and 200', '"Chỉ tiêu AOP is NULL" IN(\'NOT NULL\')']
- joins: ['rightouterjoin: PERIODNAME = PERIODNAME, TRANDATE <= AsOfDate', 'leftouterjoin: PERIODNAME = PERIODNAME', 'leftouterjoin: _k = _k', 'leftouterjoin: PERIODNAME = PERIODNAME, Metric_Code = Chỉ tiêu (AOP)']
- shown_as: ['Metric_Name @(KGR) BRD.BC01_Daily_Summary', 'LuyKe_GiaTri @(KGR) BRD.BC01_Daily_Summary', 'Thieu_PerDS @(KGR) BRD.BC01_Daily_Summary', 'Thieu_GiaTri @(KGR) BRD.BC01_Daily_Summary', 'LuyKe_PerDS @(KGR) BRD.BC01_Daily_Summary', 'Signed_Amount @(KGR) DB02.Expense_v1.1']

### PERIODNAME
- formula: `← (KGR) DTF_CALC_INVOICE_MEMO_#.PERIODNAME`
- physical_roots: ['DW_NS_ACCOUNTINGPERIOD_D.PERIODNAME']
- filters: ['(1 = 1)', '"ACCTTYPE" IN(\'Income\')', '"CUSTBODY_SCV_AOP_LOAI_BAO_CAO" between 2 and 2 and "Chỉ tiêu (AOP)" between 1 and 200', '"Chỉ tiêu AOP is NULL" IN(\'NOT NULL\')']
- joins: ['rightouterjoin: PERIODNAME = PERIODNAME, TRANDATE <= AsOfDate', 'leftouterjoin: PERIODNAME = PERIODNAME', 'leftouterjoin: _k = _k', 'leftouterjoin: PERIODNAME = PERIODNAME, Metric_Code = Chỉ tiêu (AOP)']

### PERIODNAME_1
- formula: `{"k": "unknown", "col": "PERIODNAME_1"}`
- filters: ['(1 = 1)', '"ACCTTYPE" IN(\'Income\')', '"CUSTBODY_SCV_AOP_LOAI_BAO_CAO" between 2 and 2 and "Chỉ tiêu (AOP)" between 1 and 200', '"Chỉ tiêu AOP is NULL" IN(\'NOT NULL\')']
- joins: ['rightouterjoin: PERIODNAME = PERIODNAME, TRANDATE <= AsOfDate', 'leftouterjoin: PERIODNAME = PERIODNAME', 'leftouterjoin: _k = _k', 'leftouterjoin: PERIODNAME = PERIODNAME, Metric_Code = Chỉ tiêu (AOP)']

### Type
- formula: `physical Metric_Dim.Type`
- filters: ['(1 = 1)', '"ACCTTYPE" IN(\'Income\')', '"CUSTBODY_SCV_AOP_LOAI_BAO_CAO" between 2 and 2 and "Chỉ tiêu (AOP)" between 1 and 200', '"Chỉ tiêu AOP is NULL" IN(\'NOT NULL\')']
- joins: ['rightouterjoin: PERIODNAME = PERIODNAME, TRANDATE <= AsOfDate', 'leftouterjoin: PERIODNAME = PERIODNAME', 'leftouterjoin: _k = _k', 'leftouterjoin: PERIODNAME = PERIODNAME, Metric_Code = Chỉ tiêu (AOP)']

### ﻿Sort_Order
- formula: `physical Metric_Dim.﻿Sort_Order`
- filters: ['(1 = 1)', '"ACCTTYPE" IN(\'Income\')', '"CUSTBODY_SCV_AOP_LOAI_BAO_CAO" between 2 and 2 and "Chỉ tiêu (AOP)" between 1 and 200', '"Chỉ tiêu AOP is NULL" IN(\'NOT NULL\')']
- joins: ['rightouterjoin: PERIODNAME = PERIODNAME, TRANDATE <= AsOfDate', 'leftouterjoin: PERIODNAME = PERIODNAME', 'leftouterjoin: _k = _k', 'leftouterjoin: PERIODNAME = PERIODNAME, Metric_Code = Chỉ tiêu (AOP)']
- shown_as: ['\ufeffSort_Order @(KGR) BRD.BC01_Daily_Summary']
