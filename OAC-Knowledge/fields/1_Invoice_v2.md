# 1. Invoice_v2

- **type**: db_dataset
- **grain**: line-level  ()
- **producer_flow**: 
- **used_by_workbooks**: None
- **physical_tables**: ['DW_NS_CUSTOMER_INVOICE_LINES_F', 'DW_NS_ACCOUNT_D', 'DW_NS_ACCOUNTINGPERIOD_D', 'DW_NS_X_CAM_CUSTINVCTRANSACTIONLINEEXTENSION', 'DW_NS_X_SALE_CHANNEL', 'DW_NS_SUBSIDIARY_D', 'DW_NS_CLASSIFICATION_D', 'DW_NS_X_CAM_CUSTOMRECORD_CSEG_SCV_CHAIN', 'DW_NS_X_LIST_SALE_CHANEL_NS', 'DW_NS_X_CAM_CUSTOMRECORD_CSEG_SCV_MODEL', 'DW_NS_X_CAM_CUSTOMRECORD_CSEG_SCV_NHOMXANHDO', 'DW_NS_X_CAM_CUSTOMLIST_SCV_QUY_HOACH_SP', 'DW_NS_X_CAM_EMPLOYEEEXTENSION', 'DW_NS_LOCATION_D', 'DW_NS_X_CAM_CUSTOMLIST_SCV_SALES_CATEGORY', 'DW_NS_X_CAM_CUSTOMRECORD_CSEG_SCV_SG_PRO', 'DW_NS_X_CAM_CUSTOMRECORD_CSEG_SCV_PRODGROUP', 'DW_NS_ITEM_D', 'DW_NS_X_CAM_CUSTOMEREXTENSION', 'DW_NS_X_CUST_INVOICE_LINES_SUPPLEMENTARY_1', 'DW_NS_X_CUSTOMER_EXTENSION_AUGMENTATION', 'DW_NS_LOCATION_CF_DH', 'DW_NS_X_CAM_CUSTINVCTRANSACTIONSEXTENSION', 'DW_NS_X_CAM_ITEMEXTENSION', 'DW_NS_X_CAM_CUSTOMRECORD_SCV_TINH', 'DW_NS_CUSTOMER_D', 'DW_NS_CUSTOMER_INVOICE_F', 'DW_NS_X_CAM_CUSTOMLIST_SCV_PRODUCT_SOURCE']

> Join-key & WHERE NỘI BỘ của dataset KHÔNG lộ qua API trên instance này (executePreview đọc cache XSA; endpoint dataset/datasets/metadata trả 500). Cột giữ qualifier bảng vật lý nên biết ĐỦ bảng+cột nguồn; quan hệ join theo chuẩn NetSuite (line→ACCOUNT/ITEM/PERIOD; extension→ID; segment→CSEG_*). Filter NGHIỆP VỤ quan trọng (posting/acct/subsidiary/vụ việc) nằm ở DATAFLOW tiêu thụ — xem field_dictionary cột tương ứng. confidence: join=medium.

## Cột