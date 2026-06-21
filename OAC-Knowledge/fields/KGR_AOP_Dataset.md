# (KGR) AOP Dataset

- **type**: db_dataset
- **grain**: dim/lookup  ()
- **producer_flow**: 
- **used_by_workbooks**: None
- **physical_tables**: ['DW_NS_ACCOUNTINGPERIOD_D', 'DW_NS_CLASSIFICATION_D', 'DW_NS_SUBSIDIARY_D', 'DW_NS_X_AOP_HEADER_CF_1', 'DW_NS_X_AOP_HEADER_SF_1', 'DW_NS_X_AOP_LINE_CF', 'DW_NS_X_AOP_LINE_SF_1', 'DW_NS_X_CAM_CUSTOMRECORD_CSEG_SCV_CHAIN', 'DW_NS_X_CAM_CUSTOMRECORD_CSEG_SCV_PRODCATG', 'DW_NS_X_LIST_SALE_CHANEL_NS', 'DW_NS_X_SALE_CHANNEL']

> Join-key & WHERE NỘI BỘ của dataset KHÔNG lộ qua API trên instance này (executePreview đọc cache XSA; endpoint dataset/datasets/metadata trả 500). Cột giữ qualifier bảng vật lý nên biết ĐỦ bảng+cột nguồn; quan hệ join theo chuẩn NetSuite (line→ACCOUNT/ITEM/PERIOD; extension→ID; segment→CSEG_*). Filter NGHIỆP VỤ quan trọng (posting/acct/subsidiary/vụ việc) nằm ở DATAFLOW tiêu thụ — xem field_dictionary cột tương ứng. confidence: join=medium.

## Cột