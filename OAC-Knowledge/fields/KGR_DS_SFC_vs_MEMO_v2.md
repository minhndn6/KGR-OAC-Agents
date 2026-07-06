# KGR_DS_SFC_vs_MEMO_v2

- **type**: dataflow_output
- **grain**: group: Tên Ngành  ()
- **producer_flow**: KGR_DF_SFC_vs_MEMO_v2
- **used_by_workbooks**: ['(KGR) DB01.Revenue_v1.1']
- **physical_tables**: []

## Cột
### DT_Ke_Hoach
- formula: `sum( ... )`
- aggregation: sum
- physical_roots: ['DW_NS_X_SFC_LINES_CF.Doanh thu (-VAT)']
- filters: ['"PERIODNAME" IN(\'May 2026\')']
- joins: ['fullouterjoin: Tên Ngành = Ngành hàng']

### Doanh thu thực tế Sum
- formula: `sum( ... )`
- aggregation: sum
- physical_roots: ['DW_NS_CUSTOMER_CREDIT_LINES_F.BASE_REVENUE', 'DW_NS_CUSTOMER_CREDIT_LINES_F.CLASS', 'DW_NS_CUSTOMER_INVOICE_LINES_F.BASE_REVENUE', 'DW_NS_CUSTOMER_INVOICE_LINES_F.CLASS', 'DW_NS_X_CAM_CUSTCREDTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_DISCOUNT_AMOUNT_01', 'DW_NS_X_CAM_CUSTINVCTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_DISCOUNT_AMOUNT_01']
- filters: ['"PERIODNAME" IN(\'May 2026\')']
- joins: ['fullouterjoin: Tên Ngành = Ngành hàng']

### Ngành hàng
- formula: `physical DW_NS_X_CAM_CUSTOMRECORD_CSEG_SCV_PRODCATG.Ngành hàng`
- physical_roots: ['DW_NS_X_CAM_CUSTOMRECORD_CSEG_SCV_PRODCATG.Ngành hàng']
- filters: ['"PERIODNAME" IN(\'May 2026\')']
- joins: ['fullouterjoin: Tên Ngành = Ngành hàng']

### QUANTITY Sum
- formula: `sum( ... )`
- aggregation: sum
- physical_roots: ['DW_NS_CUSTOMER_CREDIT_LINES_F.QUANTITY', 'DW_NS_CUSTOMER_INVOICE_LINES_F.QUANTITY']
- filters: ['"PERIODNAME" IN(\'May 2026\')']
- joins: ['fullouterjoin: Tên Ngành = Ngành hàng']

### SL W1
- formula: `sum( ... )`
- aggregation: sum
- physical_roots: ['DW_NS_X_SFC_LINES_CF.SL W1']
- filters: ['"PERIODNAME" IN(\'May 2026\')']
- joins: ['fullouterjoin: Tên Ngành = Ngành hàng']

### SL W2
- formula: `sum( ... )`
- aggregation: sum
- physical_roots: ['DW_NS_X_SFC_LINES_CF.SL W2']
- filters: ['"PERIODNAME" IN(\'May 2026\')']
- joins: ['fullouterjoin: Tên Ngành = Ngành hàng']

### SL W3
- formula: `sum( ... )`
- aggregation: sum
- physical_roots: ['DW_NS_X_SFC_LINES_CF.SL W3']
- filters: ['"PERIODNAME" IN(\'May 2026\')']
- joins: ['fullouterjoin: Tên Ngành = Ngành hàng']

### SL W4
- formula: `sum( ... )`
- aggregation: sum
- physical_roots: ['DW_NS_X_SFC_LINES_CF.SL W4']
- filters: ['"PERIODNAME" IN(\'May 2026\')']
- joins: ['fullouterjoin: Tên Ngành = Ngành hàng']

### SL W5
- formula: `sum( ... )`
- aggregation: sum
- physical_roots: ['DW_NS_X_SFC_LINES_CF.SL W5']
- filters: ['"PERIODNAME" IN(\'May 2026\')']
- joins: ['fullouterjoin: Tên Ngành = Ngành hàng']

### SL_Ke_Hoach
- formula: `"SL W1"+"SL W2"+"SL W3"+"SL W4"+"SL W5"`
- physical_roots: ['DW_NS_X_SFC_LINES_CF.SL W1', 'DW_NS_X_SFC_LINES_CF.SL W2', 'DW_NS_X_SFC_LINES_CF.SL W3', 'DW_NS_X_SFC_LINES_CF.SL W4', 'DW_NS_X_SFC_LINES_CF.SL W5']
- filters: ['"PERIODNAME" IN(\'May 2026\')']
- joins: ['fullouterjoin: Tên Ngành = Ngành hàng']
- shown_as: ['Δ SL (Actual − Plan) @(KGR) DB01.Revenue_v1.1', 'SFC Achievement % @(KGR) DB01.Revenue_v1.1']

### SL_Thuc_Te
- formula: `0 - "QUANTITY Sum"`
- physical_roots: ['DW_NS_CUSTOMER_CREDIT_LINES_F.QUANTITY', 'DW_NS_CUSTOMER_INVOICE_LINES_F.QUANTITY']
- filters: ['"PERIODNAME" IN(\'May 2026\')']
- joins: ['fullouterjoin: Tên Ngành = Ngành hàng']
- shown_as: ['Δ SL (Actual − Plan) @(KGR) DB01.Revenue_v1.1', 'SFC Achievement % @(KGR) DB01.Revenue_v1.1']

### Tên Ngành
- formula: `← (KGR) DTF_CALC_INVOICE_MEMO_#.Tên Ngành`
- physical_roots: ['DW_NS_CLASSIFICATION_D.Tên ngành']
- filters: ['"PERIODNAME" IN(\'May 2026\')']
- joins: ['fullouterjoin: Tên Ngành = Ngành hàng']
