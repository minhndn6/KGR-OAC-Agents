# KGR_DS_SFC_vs_MEMO_v3

- **type**: dataflow_output
- **grain**: group: Tên Ngành, Nhóm SP  ()
- **producer_flow**: KGR_DF_SFC_vs_MEMO_v3
- **used_by_workbooks**: ['(KGR) DB01.Revenue_v1.1']
- **physical_tables**: []

## Cột
### DT_Ke_Hoach
- formula: `sum( ... )`
- aggregation: sum
- physical_roots: ['DW_NS_X_SFC_LINES_CF.Doanh thu (-VAT)']
- filters: ['"PERIODNAME" IN(\'May 2026\')']
- joins: ['fullouterjoin: Tên Ngành = Ngành hàng, Nhóm SP = Nhóm sản phẩm']

### Doanh thu thực tế Sum
- formula: `sum( ... )`
- aggregation: sum
- physical_roots: ['DW_NS_CUSTOMER_CREDIT_LINES_F.BASE_REVENUE', 'DW_NS_CUSTOMER_CREDIT_LINES_F.CLASS', 'DW_NS_CUSTOMER_INVOICE_LINES_F.BASE_REVENUE', 'DW_NS_CUSTOMER_INVOICE_LINES_F.CLASS', 'DW_NS_X_CAM_CUSTCREDTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_DISCOUNT_AMOUNT_01', 'DW_NS_X_CAM_CUSTINVCTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_DISCOUNT_AMOUNT_01']
- filters: ['"PERIODNAME" IN(\'May 2026\')']
- joins: ['fullouterjoin: Tên Ngành = Ngành hàng, Nhóm SP = Nhóm sản phẩm']

### Ngành gộp
- formula: `IFNULL("Ngành hàng", "Tên Ngành")`
- physical_roots: ['DW_NS_CLASSIFICATION_D.Tên ngành', 'DW_NS_X_CAM_CUSTOMRECORD_CSEG_SCV_PRODCATG.Ngành hàng']
- filters: ['"PERIODNAME" IN(\'May 2026\')']
- joins: ['fullouterjoin: Tên Ngành = Ngành hàng, Nhóm SP = Nhóm sản phẩm']

### Ngành hàng
- formula: `physical DW_NS_X_CAM_CUSTOMRECORD_CSEG_SCV_PRODCATG.Ngành hàng`
- physical_roots: ['DW_NS_X_CAM_CUSTOMRECORD_CSEG_SCV_PRODCATG.Ngành hàng']
- filters: ['"PERIODNAME" IN(\'May 2026\')']
- joins: ['fullouterjoin: Tên Ngành = Ngành hàng, Nhóm SP = Nhóm sản phẩm']

### Nhóm SP
- formula: `← (KGR) DTF_CALC_INVOICE_MEMO_#.Nhóm SP`
- physical_roots: ['DW_NS_X_CAM_CUSTOMRECORD_CSEG_SCV_PRODGROUP.Nhóm SP']
- filters: ['"PERIODNAME" IN(\'May 2026\')']
- joins: ['fullouterjoin: Tên Ngành = Ngành hàng, Nhóm SP = Nhóm sản phẩm']

### Nhóm SP gộp
- formula: `IFNULL("Nhóm sản phẩm", "Nhóm SP")`
- physical_roots: ['DW_NS_X_CAM_CUSTOMRECORD_CSEG_SCV_PRODGROUP.Nhóm SP', 'DW_NS_X_CAM_CUSTOMRECORD_CSEG_SCV_PRODGROUP.Nhóm sản phẩm']
- filters: ['"PERIODNAME" IN(\'May 2026\')']
- joins: ['fullouterjoin: Tên Ngành = Ngành hàng, Nhóm SP = Nhóm sản phẩm']
- shown_as: ['NhmSPgp @(KGR) DB01.Revenue_v1.1']

### Nhóm sản phẩm
- formula: `physical DW_NS_X_CAM_CUSTOMRECORD_CSEG_SCV_PRODGROUP.Nhóm sản phẩm`
- physical_roots: ['DW_NS_X_CAM_CUSTOMRECORD_CSEG_SCV_PRODGROUP.Nhóm sản phẩm']
- filters: ['"PERIODNAME" IN(\'May 2026\')']
- joins: ['fullouterjoin: Tên Ngành = Ngành hàng, Nhóm SP = Nhóm sản phẩm']

### QUANTITY Sum
- formula: `sum( ... )`
- aggregation: sum
- physical_roots: ['DW_NS_CUSTOMER_CREDIT_LINES_F.QUANTITY', 'DW_NS_CUSTOMER_INVOICE_LINES_F.QUANTITY']
- filters: ['"PERIODNAME" IN(\'May 2026\')']
- joins: ['fullouterjoin: Tên Ngành = Ngành hàng, Nhóm SP = Nhóm sản phẩm']

### SL W1
- formula: `sum( ... )`
- aggregation: sum
- physical_roots: ['DW_NS_X_SFC_LINES_CF.SL W1']
- filters: ['"PERIODNAME" IN(\'May 2026\')']
- joins: ['fullouterjoin: Tên Ngành = Ngành hàng, Nhóm SP = Nhóm sản phẩm']

### SL W2
- formula: `sum( ... )`
- aggregation: sum
- physical_roots: ['DW_NS_X_SFC_LINES_CF.SL W2']
- filters: ['"PERIODNAME" IN(\'May 2026\')']
- joins: ['fullouterjoin: Tên Ngành = Ngành hàng, Nhóm SP = Nhóm sản phẩm']

### SL W3
- formula: `sum( ... )`
- aggregation: sum
- physical_roots: ['DW_NS_X_SFC_LINES_CF.SL W3']
- filters: ['"PERIODNAME" IN(\'May 2026\')']
- joins: ['fullouterjoin: Tên Ngành = Ngành hàng, Nhóm SP = Nhóm sản phẩm']

### SL W4
- formula: `sum( ... )`
- aggregation: sum
- physical_roots: ['DW_NS_X_SFC_LINES_CF.SL W4']
- filters: ['"PERIODNAME" IN(\'May 2026\')']
- joins: ['fullouterjoin: Tên Ngành = Ngành hàng, Nhóm SP = Nhóm sản phẩm']

### SL W5
- formula: `sum( ... )`
- aggregation: sum
- physical_roots: ['DW_NS_X_SFC_LINES_CF.SL W5']
- filters: ['"PERIODNAME" IN(\'May 2026\')']
- joins: ['fullouterjoin: Tên Ngành = Ngành hàng, Nhóm SP = Nhóm sản phẩm']

### SL_Ke_Hoach
- formula: `"SL W1"+"SL W2"+"SL W3"+"SL W4"+"SL W5"`
- physical_roots: ['DW_NS_X_SFC_LINES_CF.SL W1', 'DW_NS_X_SFC_LINES_CF.SL W2', 'DW_NS_X_SFC_LINES_CF.SL W3', 'DW_NS_X_SFC_LINES_CF.SL W4', 'DW_NS_X_SFC_LINES_CF.SL W5']
- filters: ['"PERIODNAME" IN(\'May 2026\')']
- joins: ['fullouterjoin: Tên Ngành = Ngành hàng, Nhóm SP = Nhóm sản phẩm']
- shown_as: ['SL_Ke_Hoach_2 @(KGR) DB01.Revenue_v1.1']

### SL_Thuc_Te
- formula: `0 - "QUANTITY Sum"`
- physical_roots: ['DW_NS_CUSTOMER_CREDIT_LINES_F.QUANTITY', 'DW_NS_CUSTOMER_INVOICE_LINES_F.QUANTITY']
- filters: ['"PERIODNAME" IN(\'May 2026\')']
- joins: ['fullouterjoin: Tên Ngành = Ngành hàng, Nhóm SP = Nhóm sản phẩm']
- shown_as: ['SL_Thuc_Te_1 @(KGR) DB01.Revenue_v1.1']

### Tên Ngành
- formula: `← (KGR) DTF_CALC_INVOICE_MEMO_#.Tên Ngành`
- physical_roots: ['DW_NS_CLASSIFICATION_D.Tên ngành']
- filters: ['"PERIODNAME" IN(\'May 2026\')']
- joins: ['fullouterjoin: Tên Ngành = Ngành hàng, Nhóm SP = Nhóm sản phẩm']
