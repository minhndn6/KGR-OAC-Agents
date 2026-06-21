# KGR_DS_SFC_vs_Actual_v2

- **type**: dataflow_output
- **grain**: group: POSTINGPERIOD, ID, CSEG_SCV_PRODCATG, CSEG_SCV_PRODGROUP, CSEG_SCV_MODEL, CSEG_SCV_CHAIN, CSEG_SCV_NHOMXANHDO  (heuristic: GroupBy gần Output nhất — verify qua dataflow_catalog steps)
- **producer_flow**: KGR_DF_SFC_vs_Actual_v2
- **used_by_workbooks**: ['(KGR) DB01.Revenue_v1.1']
- **physical_tables**: []

## Cột
### CKKM Maximum
- formula: `max( ... )`
- aggregation: max
- physical_roots: ['DW_NS_X_SFC_LINES_CF.CKKM']
- joins: ['fullouterjoin: POSTINGPERIOD = POSTINGPERIOD, ID = ITEM']

### CSEG_SCV_CHAIN
- formula: `physical DW_NS_X_SFC_LINES_CF.CSEG_SCV_CHAIN`
- physical_roots: ['DW_NS_X_SFC_LINES_CF.CSEG_SCV_CHAIN']
- joins: ['fullouterjoin: POSTINGPERIOD = POSTINGPERIOD, ID = ITEM']

### CSEG_SCV_MODEL
- formula: `physical DW_NS_X_SFC_LINES_CF.CSEG_SCV_MODEL`
- physical_roots: ['DW_NS_X_SFC_LINES_CF.CSEG_SCV_MODEL']
- joins: ['fullouterjoin: POSTINGPERIOD = POSTINGPERIOD, ID = ITEM']

### CSEG_SCV_NHOMXANHDO
- formula: `physical DW_NS_X_SFC_LINES_CF.CSEG_SCV_NHOMXANHDO`
- physical_roots: ['DW_NS_X_SFC_LINES_CF.CSEG_SCV_NHOMXANHDO']
- joins: ['fullouterjoin: POSTINGPERIOD = POSTINGPERIOD, ID = ITEM']

### CSEG_SCV_PRODCATG
- formula: `physical DW_NS_X_SFC_LINES_CF.CSEG_SCV_PRODCATG`
- physical_roots: ['DW_NS_X_SFC_LINES_CF.CSEG_SCV_PRODCATG']
- joins: ['fullouterjoin: POSTINGPERIOD = POSTINGPERIOD, ID = ITEM']

### CSEG_SCV_PRODGROUP
- formula: `physical DW_NS_X_SFC_LINES_CF.CSEG_SCV_PRODGROUP`
- physical_roots: ['DW_NS_X_SFC_LINES_CF.CSEG_SCV_PRODGROUP']
- joins: ['fullouterjoin: POSTINGPERIOD = POSTINGPERIOD, ID = ITEM']

### Doanh số thực tế Sum
- formula: `sum( ... )`
- aggregation: sum
- physical_roots: ['DW_NS_CUSTOMER_CREDIT_LINES_F.BASE_REVENUE', 'DW_NS_CUSTOMER_CREDIT_LINES_F.CLASS', 'DW_NS_CUSTOMER_INVOICE_LINES_F.BASE_REVENUE', 'DW_NS_CUSTOMER_INVOICE_LINES_F.CLASS', 'DW_NS_X_CUST_CREDIT_LINES_SUPPLEMENTARY.TAX1AMT', 'DW_NS_X_CUST_INVOICE_LINES_SUPPLEMENTARY_1.TAX1AMT']
- joins: ['fullouterjoin: POSTINGPERIOD = POSTINGPERIOD, ID = ITEM']
- shown_as: ['Actual Revenue @(KGR) DB01.Revenue_v1.1']

### Doanh thu (-VAT) Maximum
- formula: `max( ... )`
- aggregation: max
- physical_roots: ['DW_NS_X_SFC_LINES_CF.Doanh thu (-VAT)']
- joins: ['fullouterjoin: POSTINGPERIOD = POSTINGPERIOD, ID = ITEM']

### GP ròng Maximum
- formula: `max( ... )`
- aggregation: max
- physical_roots: ['DW_NS_X_SFC_LINES_CF.GP ròng']
- joins: ['fullouterjoin: POSTINGPERIOD = POSTINGPERIOD, ID = ITEM']

### Giá Vốn Maximum
- formula: `max( ... )`
- aggregation: max
- physical_roots: ['DW_NS_X_SFC_LINES_CF.Giá Vốn']
- joins: ['fullouterjoin: POSTINGPERIOD = POSTINGPERIOD, ID = ITEM']

### ID
- formula: `physical DW_NS_ITEM_D.ID`
- physical_roots: ['DW_NS_ITEM_D.ID']
- joins: ['fullouterjoin: POSTINGPERIOD = POSTINGPERIOD, ID = ITEM']

### ID CLASS
- formula: `← (KGR) DTF_CALC_INVOICE_MEMO_#.ID CLASS`
- physical_roots: ['DW_NS_CUSTOMER_CREDIT_LINES_F.CLASS', 'DW_NS_CUSTOMER_INVOICE_LINES_F.CLASS']
- joins: ['fullouterjoin: POSTINGPERIOD = POSTINGPERIOD, ID = ITEM']

### ITEM
- formula: `← (KGR) DTF_CALC_INVOICE_MEMO_#.ITEM`
- physical_roots: ['DW_NS_CUSTOMER_CREDIT_LINES_F.ITEM', 'DW_NS_CUSTOMER_INVOICE_LINES_F.ITEM']
- joins: ['fullouterjoin: POSTINGPERIOD = POSTINGPERIOD, ID = ITEM']

### LN Gộp Sum
- formula: `sum( ... )`
- aggregation: sum
- physical_roots: ['DW_NS_CUSTOMER_CREDIT_LINES_F.BASE_REVENUE', 'DW_NS_CUSTOMER_CREDIT_LINES_F.CLASS', 'DW_NS_CUSTOMER_CREDIT_LINES_F.ITEMTYPE', 'DW_NS_CUSTOMER_CREDIT_LINES_F.QUANTITY', 'DW_NS_CUSTOMER_CREDIT_LINES_F.TYPE', 'DW_NS_CUSTOMER_INVOICE_LINES_F.BASE_REVENUE', 'DW_NS_CUSTOMER_INVOICE_LINES_F.CLASS', 'DW_NS_CUSTOMER_INVOICE_LINES_F.ITEMTYPE', 'DW_NS_CUSTOMER_INVOICE_LINES_F.QUANTITY', 'DW_NS_CUSTOMER_INVOICE_LINES_F.TYPE', 'DW_NS_X_CAM_CUSTCREDTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_LINE_ISFREEGIFT', 'DW_NS_X_CAM_CUSTINVCTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_LINE_ISFREEGIFT', 'DW_NS_X_GIA_VON_MUC_TIEU_CT.CUSTRECORD_SCV_GVMT_LINE_GVMT_SP', 'DW_NS_X_GIA_VON_TON_KHO.CUSTRECORD_SCV_GVTK_UNIT_COST_L']
- joins: ['fullouterjoin: POSTINGPERIOD = POSTINGPERIOD, ID = ITEM']

### Lãi Gộp Maximum
- formula: `max( ... )`
- aggregation: max
- physical_roots: ['DW_NS_X_SFC_LINES_CF.Lãi Gộp']
- joins: ['fullouterjoin: POSTINGPERIOD = POSTINGPERIOD, ID = ITEM']

### Model name
- formula: `← (KGR) DTF_CALC_INVOICE_MEMO_#.Model name`
- physical_roots: ['DW_NS_X_CAM_CUSTOMRECORD_CSEG_SCV_MODEL.NAME']
- joins: ['fullouterjoin: POSTINGPERIOD = POSTINGPERIOD, ID = ITEM']

### Nhóm SP
- formula: `← (KGR) DTF_CALC_INVOICE_MEMO_#.Nhóm SP`
- physical_roots: ['DW_NS_X_CAM_CUSTOMRECORD_CSEG_SCV_PRODGROUP.Nhóm SP']
- joins: ['fullouterjoin: POSTINGPERIOD = POSTINGPERIOD, ID = ITEM']

### POSTINGPERIOD
- formula: `physical DW_NS_ACCOUNTINGPERIOD_D.ID`
- physical_roots: ['DW_NS_ACCOUNTINGPERIOD_D.ID']
- joins: ['fullouterjoin: POSTINGPERIOD = POSTINGPERIOD, ID = ITEM']

### POSTINGPERIOD_1
- formula: `{"k": "unknown", "col": "POSTINGPERIOD_1"}`
- joins: ['fullouterjoin: POSTINGPERIOD = POSTINGPERIOD, ID = ITEM']

### QUANTITY Sum
- formula: `sum( ... )`
- aggregation: sum
- physical_roots: ['DW_NS_CUSTOMER_CREDIT_LINES_F.QUANTITY', 'DW_NS_CUSTOMER_INVOICE_LINES_F.QUANTITY']
- joins: ['fullouterjoin: POSTINGPERIOD = POSTINGPERIOD, ID = ITEM']
- shown_as: ['Actual Qty @(KGR) DB01.Revenue_v1.1', 'Achievement % @(KGR) DB01.Revenue_v1.1']

### Quantity Maximum
- formula: `max( ... )`
- aggregation: max
- physical_roots: ['DW_NS_X_SFC_LINES_CF.Quantity']
- joins: ['fullouterjoin: POSTINGPERIOD = POSTINGPERIOD, ID = ITEM']
- shown_as: ['Achievement % @(KGR) DB01.Revenue_v1.1']

### Tên Ngành
- formula: `← (KGR) DTF_CALC_INVOICE_MEMO_#.Tên Ngành`
- physical_roots: ['DW_NS_CLASSIFICATION_D.Tên ngành']
- joins: ['fullouterjoin: POSTINGPERIOD = POSTINGPERIOD, ID = ITEM']
