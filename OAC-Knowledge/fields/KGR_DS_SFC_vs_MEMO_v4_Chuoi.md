# KGR_DS_SFC_vs_MEMO_v4_Chuoi

- **type**: dataflow_output
- **grain**: group: Tên Chuỗi  (heuristic: GroupBy gần Output nhất — verify qua dataflow_catalog steps)
- **producer_flow**: KGR_DF_SFC_vs_MEMO_v4_Chuoi
- **used_by_workbooks**: ['(KGR) DB01.Revenue_v1.1']
- **physical_tables**: []

## Cột
### Chuỗi
- formula: `physical DW_NS_X_CAM_CUSTOMRECORD_CSEG_SCV_CHAIN.Chuỗi`
- physical_roots: ['DW_NS_X_CAM_CUSTOMRECORD_CSEG_SCV_CHAIN.Chuỗi']
- filters: ['"PERIODNAME" IN(\'May 2026\')']
- joins: ['fullouterjoin: Tên Chuỗi = Chuỗi']

### Chuỗi gộp
- formula: `IFNULL(IFNULL("Chuỗi", "Tên Chuỗi"), 'Khác (ngoài chuỗi)')`
- physical_roots: ['DW_NS_X_CAM_CUSTOMRECORD_CSEG_SCV_CHAIN.Chuỗi', 'DW_NS_X_CAM_CUSTOMRECORD_CSEG_SCV_CHAIN.Tên Chuỗi']
- filters: ['"PERIODNAME" IN(\'May 2026\')']
- joins: ['fullouterjoin: Tên Chuỗi = Chuỗi']
- shown_as: ['Chuigp @(KGR) DB01.Revenue_v1.1']

### DT_Ke_Hoach
- formula: `sum( ... )`
- aggregation: sum
- physical_roots: ['DW_NS_X_SFC_LINES_CF.Doanh thu (-VAT)']
- filters: ['"PERIODNAME" IN(\'May 2026\')']
- joins: ['fullouterjoin: Tên Chuỗi = Chuỗi']

### Doanh thu thực tế Sum
- formula: `sum( ... )`
- aggregation: sum
- physical_roots: ['DW_NS_CUSTOMER_CREDIT_LINES_F.BASE_REVENUE', 'DW_NS_CUSTOMER_CREDIT_LINES_F.CLASS', 'DW_NS_CUSTOMER_INVOICE_LINES_F.BASE_REVENUE', 'DW_NS_CUSTOMER_INVOICE_LINES_F.CLASS']
- filters: ['"PERIODNAME" IN(\'May 2026\')']
- joins: ['fullouterjoin: Tên Chuỗi = Chuỗi']

### QUANTITY Sum
- formula: `sum( ... )`
- aggregation: sum
- physical_roots: ['DW_NS_CUSTOMER_CREDIT_LINES_F.QUANTITY', 'DW_NS_CUSTOMER_INVOICE_LINES_F.QUANTITY']
- filters: ['"PERIODNAME" IN(\'May 2026\')']
- joins: ['fullouterjoin: Tên Chuỗi = Chuỗi']

### SL_Ke_Hoach
- formula: `"SL W1"+"SL W2"+"SL W3"+"SL W4"+"SL W5"`
- physical_roots: ['DW_NS_X_SFC_LINES_CF.SL W1', 'DW_NS_X_SFC_LINES_CF.SL W2', 'DW_NS_X_SFC_LINES_CF.SL W3', 'DW_NS_X_SFC_LINES_CF.SL W4', 'DW_NS_X_SFC_LINES_CF.SL W5']
- filters: ['"PERIODNAME" IN(\'May 2026\')']
- joins: ['fullouterjoin: Tên Chuỗi = Chuỗi']
- shown_as: ['SL_Ke_Hoach_5 @(KGR) DB01.Revenue_v1.1']

### SL_Thuc_Te
- formula: `0 - "QUANTITY Sum"`
- physical_roots: ['DW_NS_CUSTOMER_CREDIT_LINES_F.QUANTITY', 'DW_NS_CUSTOMER_INVOICE_LINES_F.QUANTITY']
- filters: ['"PERIODNAME" IN(\'May 2026\')']
- joins: ['fullouterjoin: Tên Chuỗi = Chuỗi']
- shown_as: ['SL_Thuc_Te_4 @(KGR) DB01.Revenue_v1.1']

### Tên Chuỗi
- formula: `← (KGR) DTF_CALC_INVOICE_MEMO_#.Tên Chuỗi`
- physical_roots: ['DW_NS_X_CAM_CUSTOMRECORD_CSEG_SCV_CHAIN.Tên Chuỗi']
- filters: ['"PERIODNAME" IN(\'May 2026\')']
- joins: ['fullouterjoin: Tên Chuỗi = Chuỗi']
