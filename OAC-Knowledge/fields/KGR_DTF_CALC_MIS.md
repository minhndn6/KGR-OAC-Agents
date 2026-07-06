# (KGR) DTF_CALC_MIS

- **type**: dataflow_output
- **grain**: Grain dến invoice line id  ()
- **producer_flow**: (KGR) 5. DTF_CALC_MIS Ver 4
- **used_by_workbooks**: ['(KGR) BRD.BC03-04-05_SFC ước tính_SFC thực tế_ MIS']
- **physical_tables**: []

## Cột
### %GP Ròng
- formula: `IFnull("%LN Gộp",0) - IFnull("CKKM Per",0)`
- physical_roots: ['DW_NS_CUSTOMER_CREDIT_LINES_F.BASE_REVENUE', 'DW_NS_CUSTOMER_CREDIT_LINES_F.QUANTITY', 'DW_NS_CUSTOMER_INVOICE_LINES_F.BASE_REVENUE', 'DW_NS_CUSTOMER_INVOICE_LINES_F.QUANTITY', 'DW_NS_X_CAM_CUSTCREDTRANSACTIONLINEEXTENSION.CSEG_SCV_SC', 'DW_NS_X_CAM_CUSTCREDTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_DISCOUNT_AMOUNT_01', 'DW_NS_X_CAM_CUSTINVCTRANSACTIONLINEEXTENSION.CSEG_SCV_SC', 'DW_NS_X_CAM_CUSTINVCTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_DISCOUNT_AMOUNT_01', 'DW_NS_X_CAM_CUSTOMEREXTENSION.CSEG_SCV_CHAIN', 'DW_NS_X_GIA_VON_MUC_TIEU_CT.CUSTRECORD_SCV_GVMT_LINE_GVMT_SP', 'DW_NS_X_GIA_VON_TON_KHO.CUSTRECORD_SCV_GVTK_UNIT_COST_L', 'DW_NS_X_TRADE_PROMOTION_LINE.CUSTRECORD_SCV_PRO_DIS_LINE_DISCOUNT']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']
- shown_as: ['GPRng_24 @(KGR) BRD.BC03-04-05_SFC ước tính_SFC thực tế_ MIS']

### %GV/DT
- formula: `Case when "Tiền vốn" > 0 then "Tiền vốn"/"Doanh thu xuất bán" Else 0 End`
- physical_roots: ['DW_NS_CUSTOMER_CREDIT_LINES_F.BASE_REVENUE', 'DW_NS_CUSTOMER_CREDIT_LINES_F.QUANTITY', 'DW_NS_CUSTOMER_INVOICE_LINES_F.BASE_REVENUE', 'DW_NS_CUSTOMER_INVOICE_LINES_F.QUANTITY', 'DW_NS_X_CAM_CUSTCREDTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_DISCOUNT_AMOUNT_01', 'DW_NS_X_CAM_CUSTINVCTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_DISCOUNT_AMOUNT_01', 'DW_NS_X_GIA_VON_MUC_TIEU_CT.CUSTRECORD_SCV_GVMT_LINE_GVMT_SP', 'DW_NS_X_GIA_VON_TON_KHO.CUSTRECORD_SCV_GVTK_UNIT_COST_L']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']
- shown_as: ['GVDT_83 @(KGR) BRD.BC03-04-05_SFC ước tính_SFC thực tế_ MIS']

### %LN Gộp
- formula: `"LN Gộp"/"Doanh thu thực tế"`
- physical_roots: ['DW_NS_CUSTOMER_CREDIT_LINES_F.BASE_REVENUE', 'DW_NS_CUSTOMER_CREDIT_LINES_F.QUANTITY', 'DW_NS_CUSTOMER_INVOICE_LINES_F.BASE_REVENUE', 'DW_NS_CUSTOMER_INVOICE_LINES_F.QUANTITY', 'DW_NS_X_CAM_CUSTCREDTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_DISCOUNT_AMOUNT_01', 'DW_NS_X_CAM_CUSTINVCTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_DISCOUNT_AMOUNT_01', 'DW_NS_X_GIA_VON_MUC_TIEU_CT.CUSTRECORD_SCV_GVMT_LINE_GVMT_SP', 'DW_NS_X_GIA_VON_TON_KHO.CUSTRECORD_SCV_GVTK_UNIT_COST_L']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']
- shown_as: ['LNGp_16 @(KGR) BRD.BC03-04-05_SFC ước tính_SFC thực tế_ MIS']

### %TB/DT
- formula: `Case when "Thực bán" > 0 then "Thực bán"/"Doanh thu xuất bán" Else 0 End`
- physical_roots: ['DW_NS_CUSTOMER_CREDIT_LINES_F.BASE_REVENUE', 'DW_NS_CUSTOMER_INVOICE_LINES_F.BASE_REVENUE', 'DW_NS_X_CAM_CUSTCREDTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_DISCOUNT_AMOUNT_01', 'DW_NS_X_CAM_CUSTINVCTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_DISCOUNT_AMOUNT_01']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']
- shown_as: ['TBDT_82 @(KGR) BRD.BC03-04-05_SFC ước tính_SFC thực tế_ MIS']

### ACCTTYPE
- formula: `UNION(...)`
- physical_roots: ['DW_NS_ACCOUNT_D.ACCTTYPE']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']

### CKKM Per
- formula: `CASE
    WHEN "CKKM Per Kênh" IS NOT NULL AND "ID Kênh" IS NOT NULL
       
    THEN "CKKM Per Kênh"

    WHEN "CKKM Per Chuỗi" IS NOT NULL AND "ID Chuỗi" IS NOT NULL
      
    THEN  "CKKM Per Chuỗi"

    ELSE 0
END`
- physical_roots: ['DW_NS_X_CAM_CUSTCREDTRANSACTIONLINEEXTENSION.CSEG_SCV_SC', 'DW_NS_X_CAM_CUSTINVCTRANSACTIONLINEEXTENSION.CSEG_SCV_SC', 'DW_NS_X_CAM_CUSTOMEREXTENSION.CSEG_SCV_CHAIN', 'DW_NS_X_TRADE_PROMOTION_LINE.CUSTRECORD_SCV_PRO_DIS_LINE_DISCOUNT']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']

### CKKM Per Chuỗi
- formula: `sum( ... )`
- aggregation: sum
- physical_roots: ['DW_NS_X_TRADE_PROMOTION_LINE.CUSTRECORD_SCV_PRO_DIS_LINE_DISCOUNT']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']

### CKKM Per Kênh
- formula: `sum( ... )`
- aggregation: sum
- physical_roots: ['DW_NS_X_TRADE_PROMOTION_LINE.CUSTRECORD_SCV_PRO_DIS_LINE_DISCOUNT']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']

### CP CKKM
- formula: `"Doanh thu thực tế" * "CKKM Per"`
- physical_roots: ['DW_NS_CUSTOMER_CREDIT_LINES_F.BASE_REVENUE', 'DW_NS_CUSTOMER_INVOICE_LINES_F.BASE_REVENUE', 'DW_NS_X_CAM_CUSTCREDTRANSACTIONLINEEXTENSION.CSEG_SCV_SC', 'DW_NS_X_CAM_CUSTCREDTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_DISCOUNT_AMOUNT_01', 'DW_NS_X_CAM_CUSTINVCTRANSACTIONLINEEXTENSION.CSEG_SCV_SC', 'DW_NS_X_CAM_CUSTINVCTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_DISCOUNT_AMOUNT_01', 'DW_NS_X_CAM_CUSTOMEREXTENSION.CSEG_SCV_CHAIN', 'DW_NS_X_TRADE_PROMOTION_LINE.CUSTRECORD_SCV_PRO_DIS_LINE_DISCOUNT']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']
- shown_as: ['CPCKKM_20 @(KGR) BRD.BC03-04-05_SFC ước tính_SFC thực tế_ MIS']

### CUSTCOL_SCV_DISCOUNT_AMOUNT_01
- formula: `sum( ... )`
- aggregation: sum
- physical_roots: ['DW_NS_X_CAM_CUSTCREDTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_DISCOUNT_AMOUNT_01', 'DW_NS_X_CAM_CUSTINVCTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_DISCOUNT_AMOUNT_01']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']

### Chiết khấu
- formula: `Case When "Transaction Type"  like 'Invoice'then Ifnull("CUSTCOL_SCV_DISCOUNT_AMOUNT_01",0) Else 0 End`
- physical_roots: ['DW_NS_X_CAM_CUSTCREDTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_DISCOUNT_AMOUNT_01', 'DW_NS_X_CAM_CUSTINVCTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_DISCOUNT_AMOUNT_01']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']
- shown_as: ['Chitkhu @(KGR) BRD.BC03-04-05_SFC ước tính_SFC thực tế_ MIS']

### Chiết khấu trả lại
- formula: `Case When "Transaction Type"  like 'Credit Memo' then -Ifnull("CUSTCOL_SCV_DISCOUNT_AMOUNT_01",0) Else 0 End`
- physical_roots: ['DW_NS_X_CAM_CUSTCREDTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_DISCOUNT_AMOUNT_01', 'DW_NS_X_CAM_CUSTINVCTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_DISCOUNT_AMOUNT_01']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']
- shown_as: ['Chitkhutrli @(KGR) BRD.BC03-04-05_SFC ước tính_SFC thực tế_ MIS']

### DS Xanh
- formula: `CASE WHEN "ID XD" = 1 then "Doanh số thực tế" else 0 end`
- physical_roots: ['DW_NS_CUSTOMER_CREDIT_LINES_F.BASE_REVENUE', 'DW_NS_CUSTOMER_INVOICE_LINES_F.BASE_REVENUE', 'DW_NS_X_CAM_CUSTCREDTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_DISCOUNT_AMOUNT_01', 'DW_NS_X_CAM_CUSTINVCTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_DISCOUNT_AMOUNT_01', 'DW_NS_X_CAM_CUSTOMRECORD_CSEG_SCV_NHOMXANHDO.ID XD', 'DW_NS_X_CUST_CREDIT_LINES_SUPPLEMENTARY.TAX1AMT', 'DW_NS_X_CUST_CREDIT_LINES_SUPPLEMENTARY.TAXRATE1', 'DW_NS_X_CUST_INVOICE_LINES_SUPPLEMENTARY_1.TAX1AMT', 'DW_NS_X_CUST_INVOICE_LINES_SUPPLEMENTARY_1.TAXRATE1']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']

### DS Đỏ
- formula: `"Doanh số thực tế" - "DS Xanh"`
- physical_roots: ['DW_NS_CUSTOMER_CREDIT_LINES_F.BASE_REVENUE', 'DW_NS_CUSTOMER_INVOICE_LINES_F.BASE_REVENUE', 'DW_NS_X_CAM_CUSTCREDTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_DISCOUNT_AMOUNT_01', 'DW_NS_X_CAM_CUSTINVCTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_DISCOUNT_AMOUNT_01', 'DW_NS_X_CAM_CUSTOMRECORD_CSEG_SCV_NHOMXANHDO.ID XD', 'DW_NS_X_CUST_CREDIT_LINES_SUPPLEMENTARY.TAX1AMT', 'DW_NS_X_CUST_CREDIT_LINES_SUPPLEMENTARY.TAXRATE1', 'DW_NS_X_CUST_INVOICE_LINES_SUPPLEMENTARY_1.TAX1AMT', 'DW_NS_X_CUST_INVOICE_LINES_SUPPLEMENTARY_1.TAXRATE1']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']

### Diễn giải
- formula: `UNION(...)`
- physical_roots: ['DW_NS_CUSTOMER_CREDIT_F.MEMO', 'DW_NS_CUSTOMER_INVOICE_F.MEMO']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']
- shown_as: ['Dingii @(KGR) BRD.BC03-04-05_SFC ước tính_SFC thực tế_ MIS']

### Doanh số thực tế
- formula: `sum( ... )`
- aggregation: sum
- physical_roots: ['DW_NS_CUSTOMER_CREDIT_LINES_F.BASE_REVENUE', 'DW_NS_CUSTOMER_INVOICE_LINES_F.BASE_REVENUE', 'DW_NS_X_CAM_CUSTCREDTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_DISCOUNT_AMOUNT_01', 'DW_NS_X_CAM_CUSTINVCTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_DISCOUNT_AMOUNT_01', 'DW_NS_X_CUST_CREDIT_LINES_SUPPLEMENTARY.TAX1AMT', 'DW_NS_X_CUST_CREDIT_LINES_SUPPLEMENTARY.TAXRATE1', 'DW_NS_X_CUST_INVOICE_LINES_SUPPLEMENTARY_1.TAX1AMT', 'DW_NS_X_CUST_INVOICE_LINES_SUPPLEMENTARY_1.TAXRATE1']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']
- shown_as: ['Doanhsthct @(KGR) BRD.BC03-04-05_SFC ước tính_SFC thực tế_ MIS']

### Doanh thu SP mới
- formula: `Case when "Quy hoạch SP" = 'SP mới' then "Doanh thu thực tế" else 0 end`
- physical_roots: ['DW_NS_CUSTOMER_CREDIT_LINES_F.BASE_REVENUE', 'DW_NS_CUSTOMER_INVOICE_LINES_F.BASE_REVENUE', 'DW_NS_X_CAM_CUSTCREDTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_DISCOUNT_AMOUNT_01', 'DW_NS_X_CAM_CUSTINVCTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_DISCOUNT_AMOUNT_01', 'DW_NS_X_CAM_CUSTOMLIST_SCV_QUY_HOACH_SP.Quy hoạch SP']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']

### Doanh thu thực tế
- formula: `sum( ... )`
- aggregation: sum
- physical_roots: ['DW_NS_CUSTOMER_CREDIT_LINES_F.BASE_REVENUE', 'DW_NS_CUSTOMER_INVOICE_LINES_F.BASE_REVENUE', 'DW_NS_X_CAM_CUSTCREDTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_DISCOUNT_AMOUNT_01', 'DW_NS_X_CAM_CUSTINVCTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_DISCOUNT_AMOUNT_01']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']
- shown_as: ['Doanhthuthct @(KGR) BRD.BC03-04-05_SFC ước tính_SFC thực tế_ MIS']

### Doanh thu trả lại
- formula: `Case When "Transaction Type"  like 'Credit Memo' then -("Doanh thu thực tế" + IFNULL("CUSTCOL_SCV_DISCOUNT_AMOUNT_01",0)) Else 0 End`
- physical_roots: ['DW_NS_CUSTOMER_CREDIT_LINES_F.BASE_REVENUE', 'DW_NS_CUSTOMER_INVOICE_LINES_F.BASE_REVENUE', 'DW_NS_X_CAM_CUSTCREDTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_DISCOUNT_AMOUNT_01', 'DW_NS_X_CAM_CUSTINVCTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_DISCOUNT_AMOUNT_01']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']
- shown_as: ['Doanhthutrli @(KGR) BRD.BC03-04-05_SFC ước tính_SFC thực tế_ MIS']

### Doanh thu xuất bán
- formula: `Case When "Transaction Type"  like 'Invoice' then "Doanh thu thực tế" + IFNULL("CUSTCOL_SCV_DISCOUNT_AMOUNT_01",0) Else 0 End`
- physical_roots: ['DW_NS_CUSTOMER_CREDIT_LINES_F.BASE_REVENUE', 'DW_NS_CUSTOMER_INVOICE_LINES_F.BASE_REVENUE', 'DW_NS_X_CAM_CUSTCREDTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_DISCOUNT_AMOUNT_01', 'DW_NS_X_CAM_CUSTINVCTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_DISCOUNT_AMOUNT_01']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']
- shown_as: ['Doanhthuxutbn @(KGR) BRD.BC03-04-05_SFC ước tính_SFC thực tế_ MIS']

### Giá Vốn
- formula: `sum( ... )`
- aggregation: sum
- physical_roots: ['DW_NS_CUSTOMER_CREDIT_LINES_F.BASE_REVENUE', 'DW_NS_CUSTOMER_CREDIT_LINES_F.QUANTITY', 'DW_NS_CUSTOMER_INVOICE_LINES_F.BASE_REVENUE', 'DW_NS_CUSTOMER_INVOICE_LINES_F.QUANTITY', 'DW_NS_X_CAM_CUSTCREDTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_DISCOUNT_AMOUNT_01', 'DW_NS_X_CAM_CUSTINVCTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_DISCOUNT_AMOUNT_01', 'DW_NS_X_GIA_VON_MUC_TIEU_CT.CUSTRECORD_SCV_GVMT_LINE_GVMT_SP', 'DW_NS_X_GIA_VON_TON_KHO.CUSTRECORD_SCV_GVTK_UNIT_COST_L']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']
- shown_as: ['GiVn_8 @(KGR) BRD.BC03-04-05_SFC ước tính_SFC thực tế_ MIS']

### Giá bán TB
- formula: `Case When "Transaction Type"  like 'Invoice' then -("Doanh thu thực tế" + IFNULL("CUSTCOL_SCV_DISCOUNT_AMOUNT_01",0))/"QUANTITY" Else 0 End`
- physical_roots: ['DW_NS_CUSTOMER_CREDIT_LINES_F.BASE_REVENUE', 'DW_NS_CUSTOMER_CREDIT_LINES_F.QUANTITY', 'DW_NS_CUSTOMER_INVOICE_LINES_F.BASE_REVENUE', 'DW_NS_CUSTOMER_INVOICE_LINES_F.QUANTITY', 'DW_NS_X_CAM_CUSTCREDTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_DISCOUNT_AMOUNT_01', 'DW_NS_X_CAM_CUSTINVCTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_DISCOUNT_AMOUNT_01']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']
- shown_as: ['GibnTB @(KGR) BRD.BC03-04-05_SFC ước tính_SFC thực tế_ MIS']

### Giá trả lại TB
- formula: `Case When "Transaction Type"  like 'Credit Memo' then -("Doanh thu thực tế" + IFNULL("CUSTCOL_SCV_DISCOUNT_AMOUNT_01",0))/"QUANTITY" Else 0 End`
- physical_roots: ['DW_NS_CUSTOMER_CREDIT_LINES_F.BASE_REVENUE', 'DW_NS_CUSTOMER_CREDIT_LINES_F.QUANTITY', 'DW_NS_CUSTOMER_INVOICE_LINES_F.BASE_REVENUE', 'DW_NS_CUSTOMER_INVOICE_LINES_F.QUANTITY', 'DW_NS_X_CAM_CUSTCREDTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_DISCOUNT_AMOUNT_01', 'DW_NS_X_CAM_CUSTINVCTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_DISCOUNT_AMOUNT_01']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']
- shown_as: ['GitrliTB @(KGR) BRD.BC03-04-05_SFC ước tính_SFC thực tế_ MIS']

### ID Chuỗi
- formula: `UNION(...)`
- physical_roots: ['DW_NS_X_CAM_CUSTOMEREXTENSION.CSEG_SCV_CHAIN']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']

### ID Kênh
- formula: `UNION(...)`
- physical_roots: ['DW_NS_X_CAM_CUSTCREDTRANSACTIONLINEEXTENSION.CSEG_SCV_SC', 'DW_NS_X_CAM_CUSTINVCTRANSACTIONLINEEXTENSION.CSEG_SCV_SC']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']

### ID Model
- formula: `UNION(...)`
- physical_roots: ['DW_NS_X_CAM_ITEMEXTENSION.CSEG_SCV_MODEL']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']

### ID XD
- formula: `UNION(...)`
- physical_roots: ['DW_NS_X_CAM_CUSTOMRECORD_CSEG_SCV_NHOMXANHDO.ID XD']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']

### ITEM
- formula: `UNION(...)`
- physical_roots: ['DW_NS_CUSTOMER_CREDIT_LINES_F.ITEM', 'DW_NS_CUSTOMER_INVOICE_LINES_F.ITEM']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']

### Item Name
- formula: `UNION(...)`
- physical_roots: ['DW_NS_ITEM_D.Item Name']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']
- shown_as: ['ItemName @(KGR) BRD.BC03-04-05_SFC ước tính_SFC thực tế_ MIS']

### KH ký gửi
- formula: `UNION(...)`
- physical_roots: ['DW_NS_X_CUSTOMER_EXTENSION_AUGMENTATION.CUSTENTITY_SCV_KH_KY_GUI']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']
- shown_as: ['KHkgi @(KGR) BRD.BC03-04-05_SFC ước tính_SFC thực tế_ MIS']

### LINE ID
- formula: `UNION(...)`
- physical_roots: ['DW_NS_CUSTOMER_CREDIT_LINES_F.ID', 'DW_NS_CUSTOMER_INVOICE_LINES_F.ID']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']

### LN Gộp
- formula: `"Doanh thu thực tế"  - "Giá Vốn"`
- physical_roots: ['DW_NS_CUSTOMER_CREDIT_LINES_F.BASE_REVENUE', 'DW_NS_CUSTOMER_CREDIT_LINES_F.QUANTITY', 'DW_NS_CUSTOMER_INVOICE_LINES_F.BASE_REVENUE', 'DW_NS_CUSTOMER_INVOICE_LINES_F.QUANTITY', 'DW_NS_X_CAM_CUSTCREDTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_DISCOUNT_AMOUNT_01', 'DW_NS_X_CAM_CUSTINVCTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_DISCOUNT_AMOUNT_01', 'DW_NS_X_GIA_VON_MUC_TIEU_CT.CUSTRECORD_SCV_GVMT_LINE_GVMT_SP', 'DW_NS_X_GIA_VON_TON_KHO.CUSTRECORD_SCV_GVTK_UNIT_COST_L']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']
- shown_as: ['LNGp_12 @(KGR) BRD.BC03-04-05_SFC ước tính_SFC thực tế_ MIS']

### Là hàng tặng
- formula: `UNION(...)`
- physical_roots: ['DW_NS_X_CAM_CUSTCREDTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_LINE_ISFREEGIFT', 'DW_NS_X_CAM_CUSTINVCTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_LINE_ISFREEGIFT']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']

### Lãi
- formula: `Ifnull("Thực bán",0) - (Ifnull("Tiền vốn",0) - Ifnull("Tiền vốn tl",0))`
- physical_roots: ['DW_NS_CUSTOMER_CREDIT_LINES_F.BASE_REVENUE', 'DW_NS_CUSTOMER_CREDIT_LINES_F.QUANTITY', 'DW_NS_CUSTOMER_INVOICE_LINES_F.BASE_REVENUE', 'DW_NS_CUSTOMER_INVOICE_LINES_F.QUANTITY', 'DW_NS_X_CAM_CUSTCREDTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_DISCOUNT_AMOUNT_01', 'DW_NS_X_CAM_CUSTINVCTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_DISCOUNT_AMOUNT_01', 'DW_NS_X_GIA_VON_MUC_TIEU_CT.CUSTRECORD_SCV_GVMT_LINE_GVMT_SP', 'DW_NS_X_GIA_VON_TON_KHO.CUSTRECORD_SCV_GVTK_UNIT_COST_L']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']
- shown_as: ['Li @(KGR) BRD.BC03-04-05_SFC ước tính_SFC thực tế_ MIS']

### Model name
- formula: `UNION(...)`
- physical_roots: ['DW_NS_X_CAM_CUSTOMRECORD_CSEG_SCV_MODEL.NAME']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']
- shown_as: ['Modelname_71 @(KGR) BRD.BC03-04-05_SFC ước tính_SFC thực tế_ MIS']

### Month_No
- formula: `UNION(...)`
- physical_roots: ['DW_NS_ACCOUNTINGPERIOD_D.Month_No']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']

### Mã CKKM
- formula: `UNION(...)`
- physical_roots: ['DW_NS_X_CAM_CUSTCREDTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_TRANS_MA_CKKM', 'DW_NS_X_CAM_CUSTINVCTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_TRANS_MA_CKKM']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']
- shown_as: ['MCKKM @(KGR) BRD.BC03-04-05_SFC ước tính_SFC thực tế_ MIS']

### Mã KH
- formula: `UNION(...)`
- physical_roots: ['DW_NS_X_CAM_CUSTOMEREXTENSION.CUSTENTITY_SCV_ENTITY_CODE']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']
- shown_as: ['MKH_47 @(KGR) BRD.BC03-04-05_SFC ước tính_SFC thực tế_ MIS']

### Mã Kho
- formula: `UNION(...)`
- physical_roots: ['DW_NS_LOCATION_CF_DH.PARENT_NAME']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']

### Mã NVBH
- formula: `UNION(...)`
- physical_roots: ['DW_NS_X_CAM_EMPLOYEEEXTENSION.CUSTENTITY_SCV_EMP_ASM_CODE']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']
- shown_as: ['MNVBH_29 @(KGR) BRD.BC03-04-05_SFC ước tính_SFC thực tế_ MIS']

### Mã hàng
- formula: `UNION(...)`
- physical_roots: ['DW_NS_ITEM_D.UPCCODE']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']
- shown_as: ['Mhng @(KGR) BRD.BC03-04-05_SFC ước tính_SFC thực tế_ MIS']

### Mã tỉnh
- formula: `CASE WHEN POSITION('_' IN "Địa chỉ") > 0 THEN       CASE WHEN POSITION('_' IN "Địa chỉ") = 1 THEN ''      ELSE SUBSTRING("Địa chỉ",1, POSITION('_' IN "Địa chỉ")-1) END   ELSE "Địa chỉ" END`
- physical_roots: ['DW_NS_X_CAM_CUSTOMRECORD_SCV_TINH.NAME']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']

### Mã Đơn Vị
- formula: `UNION(...)`
- physical_roots: ['DW_NS_SUBSIDIARY_D.Mã Đơn Vị']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']

### Ngày CT
- formula: `UNION(...)`
- physical_roots: ['DW_NS_CUSTOMER_CREDIT_LINES_F.TRANDATE', 'DW_NS_CUSTOMER_INVOICE_LINES_F.TRANDATE']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']
- shown_as: ['NgyCT @(KGR) BRD.BC03-04-05_SFC ước tính_SFC thực tế_ MIS']

### Ngày bắt đầu
- formula: `UNION(...)`
- physical_roots: ['DW_NS_CUSTOMER_CREDIT_LINES_F.CREATEDDATE', 'DW_NS_CUSTOMER_INVOICE_LINES_F.CREATEDDATE']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']
- shown_as: ['Ngybtu @(KGR) BRD.BC03-04-05_SFC ước tính_SFC thực tế_ MIS']

### Ngày kết thúc
- formula: `UNION(...)`
- physical_roots: ['DW_NS_CUSTOMER_CREDIT_LINES_F.CLOSEDATE', 'DW_NS_CUSTOMER_INVOICE_LINES_F.CLOSEDATE']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']
- shown_as: ['Ngyktthc @(KGR) BRD.BC03-04-05_SFC ước tính_SFC thực tế_ MIS']

### Nhóm Kênh
- formula: `UNION(...)`
- physical_roots: ['DW_NS_X_LIST_SALE_CHANEL_NS.Nhóm Kênh']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']

### Nhóm SP
- formula: `UNION(...)`
- physical_roots: ['DW_NS_X_CAM_CUSTOMRECORD_CSEG_SCV_PRODGROUP.Nhóm SP']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']
- shown_as: ['NhmSP_65 @(KGR) BRD.BC03-04-05_SFC ước tính_SFC thực tế_ MIS']

### Nhóm xanh đỏ
- formula: `UNION(...)`
- physical_roots: ['DW_NS_X_CAM_CUSTOMRECORD_CSEG_SCV_NHOMXANHDO.Nhóm xanh đỏ']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']
- shown_as: ['Nhmxanh_59 @(KGR) BRD.BC03-04-05_SFC ước tính_SFC thực tế_ MIS']

### PERIODNAME
- formula: `UNION(...)`
- physical_roots: ['DW_NS_ACCOUNTINGPERIOD_D.PERIODNAME']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']
- shown_as: ['PERIODNAME_35 @(KGR) BRD.BC03-04-05_SFC ước tính_SFC thực tế_ MIS']

### POSTINGPERIOD
- formula: `UNION(...)`
- physical_roots: ['DW_NS_CUSTOMER_CREDIT_LINES_F.POSTINGPERIOD', 'DW_NS_CUSTOMER_INVOICE_LINES_F.POSTINGPERIOD']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']
- shown_as: ['POSTINGPERIOD @(KGR) BRD.BC03-04-05_SFC ước tính_SFC thực tế_ MIS']

### Phân nhóm SP
- formula: `UNION(...)`
- physical_roots: ['DW_NS_X_CAM_CUSTOMLIST_SCV_PRODUCT_SOURCE.Phân nhóm SP']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']
- shown_as: ['PhnnhmSP @(KGR) BRD.BC03-04-05_SFC ước tính_SFC thực tế_ MIS']

### QUANTITY
- formula: `sum( ... )`
- aggregation: sum
- physical_roots: ['DW_NS_CUSTOMER_CREDIT_LINES_F.QUANTITY', 'DW_NS_CUSTOMER_INVOICE_LINES_F.QUANTITY']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']
- shown_as: ['SỐ LƯỢNG @(KGR) BRD.BC03-04-05_SFC ước tính_SFC thực tế_ MIS']

### Quy hoạch SP
- formula: `UNION(...)`
- physical_roots: ['DW_NS_X_CAM_CUSTOMLIST_SCV_QUY_HOACH_SP.Quy hoạch SP']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']
- shown_as: ['QuyhochSP @(KGR) BRD.BC03-04-05_SFC ước tính_SFC thực tế_ MIS']

### SL trả lại
- formula: `Case When "Transaction Type"  like 'Credit Memo' then "QUANTITY" Else 0 End`
- physical_roots: ['DW_NS_CUSTOMER_CREDIT_LINES_F.QUANTITY', 'DW_NS_CUSTOMER_INVOICE_LINES_F.QUANTITY']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']
- shown_as: ['SLtrli @(KGR) BRD.BC03-04-05_SFC ước tính_SFC thực tế_ MIS']

### SL xuất bán
- formula: `Case When "Transaction Type"  like 'Invoice' then - "QUANTITY" Else 0 End`
- physical_roots: ['DW_NS_CUSTOMER_CREDIT_LINES_F.QUANTITY', 'DW_NS_CUSTOMER_INVOICE_LINES_F.QUANTITY']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']
- shown_as: ['SLxutbn @(KGR) BRD.BC03-04-05_SFC ước tính_SFC thực tế_ MIS']

### Sales Category
- formula: `UNION(...)`
- physical_roots: ['DW_NS_X_CAM_CUSTOMLIST_SCV_SALES_CATEGORY.Sales Category']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']
- shown_as: ['SalesCategory @(KGR) BRD.BC03-04-05_SFC ước tính_SFC thực tế_ MIS']

### Số CT FAST
- formula: `UNION(...)`
- physical_roots: ['DW_NS_X_CAM_CUSTCREDTRANSACTIONSEXTENSION.CUSTBODY_SCV_TRANS_SCT_FAST', 'DW_NS_X_CAM_CUSTINVCTRANSACTIONSEXTENSION.CUSTBODY_SCV_TRANS_SCT_FAST']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']
- shown_as: ['SCTFAST @(KGR) BRD.BC03-04-05_SFC ước tính_SFC thực tế_ MIS']

### T1_GVMT
- formula: `sum( ... )`
- aggregation: sum
- physical_roots: ['DW_NS_CUSTOMER_CREDIT_LINES_F.QUANTITY', 'DW_NS_CUSTOMER_INVOICE_LINES_F.QUANTITY', 'DW_NS_X_GIA_VON_MUC_TIEU_CT.CUSTRECORD_SCV_GVMT_LINE_GVMT_SP']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']
- shown_as: ['T1_GVMT @(KGR) BRD.BC03-04-05_SFC ước tính_SFC thực tế_ MIS']

### T2_GVTK
- formula: `sum( ... )`
- aggregation: sum
- physical_roots: ['DW_NS_CUSTOMER_CREDIT_LINES_F.QUANTITY', 'DW_NS_CUSTOMER_INVOICE_LINES_F.QUANTITY', 'DW_NS_X_GIA_VON_MUC_TIEU_CT.CUSTRECORD_SCV_GVMT_LINE_GVMT_SP', 'DW_NS_X_GIA_VON_TON_KHO.CUSTRECORD_SCV_GVTK_UNIT_COST_L']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']
- shown_as: ['T2_GVTK @(KGR) BRD.BC03-04-05_SFC ước tính_SFC thực tế_ MIS']

### T3_FB50
- formula: `sum( ... )`
- aggregation: sum
- physical_roots: ['DW_NS_CUSTOMER_CREDIT_LINES_F.BASE_REVENUE', 'DW_NS_CUSTOMER_INVOICE_LINES_F.BASE_REVENUE', 'DW_NS_X_CAM_CUSTCREDTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_DISCOUNT_AMOUNT_01', 'DW_NS_X_CAM_CUSTINVCTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_DISCOUNT_AMOUNT_01', 'DW_NS_X_GIA_VON_MUC_TIEU_CT.CUSTRECORD_SCV_GVMT_LINE_GVMT_SP', 'DW_NS_X_GIA_VON_TON_KHO.CUSTRECORD_SCV_GVTK_UNIT_COST_L']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']
- shown_as: ['T3_FB50 @(KGR) BRD.BC03-04-05_SFC ước tính_SFC thực tế_ MIS']

### TAX AMT
- formula: `sum( ... )`
- aggregation: sum
- physical_roots: ['DW_NS_X_CAM_CUSTCREDTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_DISCOUNT_AMOUNT_01', 'DW_NS_X_CAM_CUSTINVCTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_DISCOUNT_AMOUNT_01', 'DW_NS_X_CUST_CREDIT_LINES_SUPPLEMENTARY.TAX1AMT', 'DW_NS_X_CUST_CREDIT_LINES_SUPPLEMENTARY.TAXRATE1', 'DW_NS_X_CUST_INVOICE_LINES_SUPPLEMENTARY_1.TAX1AMT', 'DW_NS_X_CUST_INVOICE_LINES_SUPPLEMENTARY_1.TAXRATE1']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']
- shown_as: ['GIÁ VAT @(KGR) BRD.BC03-04-05_SFC ước tính_SFC thực tế_ MIS']

### TAX RATE
- formula: `avg( ... )`
- aggregation: avg
- physical_roots: ['DW_NS_X_CUST_CREDIT_LINES_SUPPLEMENTARY.TAXRATE1', 'DW_NS_X_CUST_INVOICE_LINES_SUPPLEMENTARY_1.TAXRATE1']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']
- shown_as: ['TAXRATE @(KGR) BRD.BC03-04-05_SFC ước tính_SFC thực tế_ MIS']

### TK đối ứng
- formula: `UNION(...)`
- physical_roots: ['DW_NS_ACCOUNT_D.ACCTNUMBER']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']
- shown_as: ['TKing @(KGR) BRD.BC03-04-05_SFC ước tính_SFC thực tế_ MIS']

### TKĐƯ
- formula: `{"k": "unknown", "col": "TKĐƯ"}`
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']

### TYPE
- formula: `UNION(...)`
- physical_roots: ['DW_NS_CUSTOMER_CREDIT_LINES_F.TYPE', 'DW_NS_CUSTOMER_INVOICE_LINES_F.TYPE']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']

### Thuế
- formula: `Case When "Transaction Type"  like 'Invoice' then - "TAX AMT" Else 0 End`
- physical_roots: ['DW_NS_X_CAM_CUSTCREDTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_DISCOUNT_AMOUNT_01', 'DW_NS_X_CAM_CUSTINVCTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_DISCOUNT_AMOUNT_01', 'DW_NS_X_CUST_CREDIT_LINES_SUPPLEMENTARY.TAX1AMT', 'DW_NS_X_CUST_CREDIT_LINES_SUPPLEMENTARY.TAXRATE1', 'DW_NS_X_CUST_INVOICE_LINES_SUPPLEMENTARY_1.TAX1AMT', 'DW_NS_X_CUST_INVOICE_LINES_SUPPLEMENTARY_1.TAXRATE1']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']
- shown_as: ['Thu @(KGR) BRD.BC03-04-05_SFC ước tính_SFC thực tế_ MIS']

### Thuế trả lại
- formula: `Case When "Transaction Type"  like 'Credit Memo' then "TAX AMT" Else 0 End`
- physical_roots: ['DW_NS_X_CAM_CUSTCREDTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_DISCOUNT_AMOUNT_01', 'DW_NS_X_CAM_CUSTINVCTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_DISCOUNT_AMOUNT_01', 'DW_NS_X_CUST_CREDIT_LINES_SUPPLEMENTARY.TAX1AMT', 'DW_NS_X_CUST_CREDIT_LINES_SUPPLEMENTARY.TAXRATE1', 'DW_NS_X_CUST_INVOICE_LINES_SUPPLEMENTARY_1.TAX1AMT', 'DW_NS_X_CUST_INVOICE_LINES_SUPPLEMENTARY_1.TAXRATE1']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']
- shown_as: ['Thutrli @(KGR) BRD.BC03-04-05_SFC ước tính_SFC thực tế_ MIS']

### Thực bán
- formula: `(Ifnull("Doanh thu xuất bán",0) - Ifnull("Chiết khấu",0))-(Ifnull("Doanh thu trả lại",0) - Ifnull("Chiết khấu trả lại",0))`
- physical_roots: ['DW_NS_CUSTOMER_CREDIT_LINES_F.BASE_REVENUE', 'DW_NS_CUSTOMER_INVOICE_LINES_F.BASE_REVENUE', 'DW_NS_X_CAM_CUSTCREDTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_DISCOUNT_AMOUNT_01', 'DW_NS_X_CAM_CUSTINVCTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_DISCOUNT_AMOUNT_01']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']
- shown_as: ['Thcbn @(KGR) BRD.BC03-04-05_SFC ước tính_SFC thực tế_ MIS']

### Tiền vốn
- formula: `Case When "Transaction Type"  like 'Invoice' then "Giá Vốn" Else 0 End`
- physical_roots: ['DW_NS_CUSTOMER_CREDIT_LINES_F.BASE_REVENUE', 'DW_NS_CUSTOMER_CREDIT_LINES_F.QUANTITY', 'DW_NS_CUSTOMER_INVOICE_LINES_F.BASE_REVENUE', 'DW_NS_CUSTOMER_INVOICE_LINES_F.QUANTITY', 'DW_NS_X_CAM_CUSTCREDTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_DISCOUNT_AMOUNT_01', 'DW_NS_X_CAM_CUSTINVCTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_DISCOUNT_AMOUNT_01', 'DW_NS_X_GIA_VON_MUC_TIEU_CT.CUSTRECORD_SCV_GVMT_LINE_GVMT_SP', 'DW_NS_X_GIA_VON_TON_KHO.CUSTRECORD_SCV_GVTK_UNIT_COST_L']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']
- shown_as: ['Tinvn @(KGR) BRD.BC03-04-05_SFC ước tính_SFC thực tế_ MIS']

### Tiền vốn thực tế
- formula: `Ifnull("Tiền vốn",0) - Ifnull("Tiền vốn tl",0)`
- physical_roots: ['DW_NS_CUSTOMER_CREDIT_LINES_F.BASE_REVENUE', 'DW_NS_CUSTOMER_CREDIT_LINES_F.QUANTITY', 'DW_NS_CUSTOMER_INVOICE_LINES_F.BASE_REVENUE', 'DW_NS_CUSTOMER_INVOICE_LINES_F.QUANTITY', 'DW_NS_X_CAM_CUSTCREDTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_DISCOUNT_AMOUNT_01', 'DW_NS_X_CAM_CUSTINVCTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_DISCOUNT_AMOUNT_01', 'DW_NS_X_GIA_VON_MUC_TIEU_CT.CUSTRECORD_SCV_GVMT_LINE_GVMT_SP', 'DW_NS_X_GIA_VON_TON_KHO.CUSTRECORD_SCV_GVTK_UNIT_COST_L']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']
- shown_as: ['Tinvnthct @(KGR) BRD.BC03-04-05_SFC ước tính_SFC thực tế_ MIS']

### Tiền vốn tl
- formula: `Case When "Transaction Type"  like 'Credit Memo' then "Giá Vốn" Else 0 End`
- physical_roots: ['DW_NS_CUSTOMER_CREDIT_LINES_F.BASE_REVENUE', 'DW_NS_CUSTOMER_CREDIT_LINES_F.QUANTITY', 'DW_NS_CUSTOMER_INVOICE_LINES_F.BASE_REVENUE', 'DW_NS_CUSTOMER_INVOICE_LINES_F.QUANTITY', 'DW_NS_X_CAM_CUSTCREDTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_DISCOUNT_AMOUNT_01', 'DW_NS_X_CAM_CUSTINVCTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_DISCOUNT_AMOUNT_01', 'DW_NS_X_GIA_VON_MUC_TIEU_CT.CUSTRECORD_SCV_GVMT_LINE_GVMT_SP', 'DW_NS_X_GIA_VON_TON_KHO.CUSTRECORD_SCV_GVTK_UNIT_COST_L']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']
- shown_as: ['Tinvntl @(KGR) BRD.BC03-04-05_SFC ước tính_SFC thực tế_ MIS']

### Transaction ID
- formula: `UNION(...)`
- physical_roots: ['DW_NS_CUSTOMER_CREDIT_LINES_F.TRANSACTION', 'DW_NS_CUSTOMER_INVOICE_LINES_F.TRANSACTION']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']
- shown_as: ['TransactionID @(KGR) BRD.BC03-04-05_SFC ước tính_SFC thực tế_ MIS']

### Transaction Type
- formula: `UNION(...)`
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']
- shown_as: ['TransactionType @(KGR) BRD.BC03-04-05_SFC ước tính_SFC thực tế_ MIS']

### Tên CKKM
- formula: `UNION(...)`
- physical_roots: ['DW_NS_X_CAM_CUSTCREDTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_TRANS_TEN_CKKM', 'DW_NS_X_CAM_CUSTINVCTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_TRANS_TEN_CKKM']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']
- shown_as: ['TnCKKM @(KGR) BRD.BC03-04-05_SFC ước tính_SFC thực tế_ MIS']

### Tên Chuỗi
- formula: `UNION(...)`
- physical_roots: ['DW_NS_X_CAM_CUSTOMRECORD_CSEG_SCV_CHAIN.Tên Chuỗi']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']
- shown_as: ['TnChui_9 @(KGR) BRD.BC03-04-05_SFC ước tính_SFC thực tế_ MIS']

### Tên KH
- formula: `UNION(...)`
- physical_roots: ['DW_NS_X_CAM_CUSTOMEREXTENSION.CUSTENTITY_SCV_LEGAL_NAME']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']

### Tên Khách Hàng
- formula: `UNION(...)`
- physical_roots: ['DW_NS_CUSTOMER_D.COMPANYNAME']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']
- shown_as: ['TnKhchHng @(KGR) BRD.BC03-04-05_SFC ước tính_SFC thực tế_ MIS']

### Tên Kênh
- formula: `UNION(...)`
- physical_roots: ['DW_NS_X_SALE_CHANNEL.Tên Kênh']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']
- shown_as: ['TnKnh_53 @(KGR) BRD.BC03-04-05_SFC ước tính_SFC thực tế_ MIS']

### Tên Ngành
- formula: `UNION(...)`
- physical_roots: ['DW_NS_CLASSIFICATION_D.Tên ngành']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']
- shown_as: ['TnNgnh @(KGR) BRD.BC03-04-05_SFC ước tính_SFC thực tế_ MIS']

### Tên kho
- formula: `UNION(...)`
- physical_roots: ['DW_NS_LOCATION_D.Location Name']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']
- shown_as: ['Tnkho @(KGR) BRD.BC03-04-05_SFC ước tính_SFC thực tế_ MIS']

### Tên Đơn vị
- formula: `UNION(...)`
- physical_roots: ['DW_NS_SUBSIDIARY_D.Tên Đơn vị']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']
- shown_as: ['Tnnv_41 @(KGR) BRD.BC03-04-05_SFC ước tính_SFC thực tế_ MIS']

### Tỷ trọng SP mới
- formula: `"Doanh thu SP mới"/"Doanh thu thực tế"`
- physical_roots: ['DW_NS_CUSTOMER_CREDIT_LINES_F.BASE_REVENUE', 'DW_NS_CUSTOMER_INVOICE_LINES_F.BASE_REVENUE', 'DW_NS_X_CAM_CUSTCREDTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_DISCOUNT_AMOUNT_01', 'DW_NS_X_CAM_CUSTINVCTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_DISCOUNT_AMOUNT_01', 'DW_NS_X_CAM_CUSTOMLIST_SCV_QUY_HOACH_SP.Quy hoạch SP']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']

### Unit Cost
- formula: `sum( ... )`
- aggregation: sum
- physical_roots: ['DW_NS_CUSTOMER_CREDIT_LINES_F.BASE_REVENUE', 'DW_NS_CUSTOMER_CREDIT_LINES_F.QUANTITY', 'DW_NS_CUSTOMER_INVOICE_LINES_F.BASE_REVENUE', 'DW_NS_CUSTOMER_INVOICE_LINES_F.QUANTITY', 'DW_NS_X_CAM_CUSTCREDTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_DISCOUNT_AMOUNT_01', 'DW_NS_X_CAM_CUSTINVCTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_DISCOUNT_AMOUNT_01', 'DW_NS_X_GIA_VON_MUC_TIEU_CT.CUSTRECORD_SCV_GVMT_LINE_GVMT_SP', 'DW_NS_X_GIA_VON_TON_KHO.CUSTRECORD_SCV_GVTK_UNIT_COST_L']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']
- shown_as: ['UnitCost @(KGR) BRD.BC03-04-05_SFC ước tính_SFC thực tế_ MIS']

### Vụ việc
- formula: `UNION(...)`
- physical_roots: ['DW_NS_X_CAM_CUSTOMRECORD_CSEG_SCV_SG_PRO.Vụ việc']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']
- shown_as: ['Vvic @(KGR) BRD.BC03-04-05_SFC ước tính_SFC thực tế_ MIS']

### Đvt
- formula: `UNION(...)`
- physical_roots: ['DW_NS_ITEM_D.WEIGHTUNITS']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']
- shown_as: ['vt @(KGR) BRD.BC03-04-05_SFC ước tính_SFC thực tế_ MIS']

### Đơn Giá (-VAT)
- formula: `"Doanh thu thực tế"/"QUANTITY"`
- physical_roots: ['DW_NS_CUSTOMER_CREDIT_LINES_F.BASE_REVENUE', 'DW_NS_CUSTOMER_CREDIT_LINES_F.QUANTITY', 'DW_NS_CUSTOMER_INVOICE_LINES_F.BASE_REVENUE', 'DW_NS_CUSTOMER_INVOICE_LINES_F.QUANTITY', 'DW_NS_X_CAM_CUSTCREDTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_DISCOUNT_AMOUNT_01', 'DW_NS_X_CAM_CUSTINVCTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_DISCOUNT_AMOUNT_01']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']
- shown_as: ['ĐƠN GIÁ (-VAT) @(KGR) BRD.BC03-04-05_SFC ước tính_SFC thực tế_ MIS']

### Đơn giá (+VAT)
- formula: `"Doanh số thực tế"/"QUANTITY"`
- physical_roots: ['DW_NS_CUSTOMER_CREDIT_LINES_F.BASE_REVENUE', 'DW_NS_CUSTOMER_CREDIT_LINES_F.QUANTITY', 'DW_NS_CUSTOMER_INVOICE_LINES_F.BASE_REVENUE', 'DW_NS_CUSTOMER_INVOICE_LINES_F.QUANTITY', 'DW_NS_X_CAM_CUSTCREDTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_DISCOUNT_AMOUNT_01', 'DW_NS_X_CAM_CUSTINVCTRANSACTIONLINEEXTENSION.CUSTCOL_SCV_DISCOUNT_AMOUNT_01', 'DW_NS_X_CUST_CREDIT_LINES_SUPPLEMENTARY.TAX1AMT', 'DW_NS_X_CUST_CREDIT_LINES_SUPPLEMENTARY.TAXRATE1', 'DW_NS_X_CUST_INVOICE_LINES_SUPPLEMENTARY_1.TAX1AMT', 'DW_NS_X_CUST_INVOICE_LINES_SUPPLEMENTARY_1.TAXRATE1']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']
- shown_as: ['ĐƠN GIÁ (+VAT) @(KGR) BRD.BC03-04-05_SFC ước tính_SFC thực tế_ MIS']

### Đơn vị
- formula: `UNION(...)`
- physical_roots: ['DW_NS_CUSTOMER_CREDIT_LINES_F.SUBSIDIARY', 'DW_NS_CUSTOMER_INVOICE_LINES_F.SUBSIDIARY']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']

### Địa chỉ
- formula: `UNION(...)`
- physical_roots: ['DW_NS_X_CAM_CUSTOMRECORD_SCV_TINH.NAME']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']

### Địa chỉ KH
- formula: `CASE WHEN POSITION('_' IN "Địa chỉ") > 0 THEN  SUBSTRING("Địa chỉ", POSITION('_' IN "Địa chỉ")+1, LENGTH("Địa chỉ")) ELSE '' END`
- physical_roots: ['DW_NS_X_CAM_CUSTOMRECORD_SCV_TINH.NAME']
- filters: ['"ISINACTIVE" IN(\'F\')', '"Check ID = 0" IN(\'T\')', '("Is Công ty con Chi nhánh Invoice" IS NULL or "Is Công ty con Chi nhánh Invoice" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\') and "ISPOSTING" IN(\'T\')', '"Is Công ty con Chi nhánh Memo" IN(\'F\') and ("Is Công ty con Chi nhánh Memo" IS NULL or "Is Công ty con Chi nhánh Memo" NOT IN(\'T\'))', '"ISPOSTING" IN(\'T\') and "ACCTTYPE" IN(\'Income\', \'OthCurrLiab\')', '"ACCTTYPE" IN(\'Income\') and ("ITEMTYPE" IS NULL or "ITEMTYPE" NOT IN(\'Discount\'))']
- joins: ['leftouterjoin: ID = ID, TRANSACTION = TRANSACTION', 'leftouterjoin: TRANSACTION = TRANSACTION', 'rightouterjoin: GVMT_LINE_MSP = ITEM, Month Key = Month Key', 'leftouterjoin: ITEM = GVTK_ITEM_CODE_L, POSTINGPERIOD - 1 = GVTK_PERIOD_L, SUBSIDIARY = GVTK_SUBSIDIARY_L', 'leftouterjoin: ID Chuỗi = ID Chuỗi, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD', 'leftouterjoin: ID Kênh = ID Kênh, ID Model = ID Model, POSTINGPERIOD = CUSTRECORD_SCV_PRO_DIS_PERIOD']
- shown_as: ['achKH @(KGR) BRD.BC03-04-05_SFC ước tính_SFC thực tế_ MIS']
