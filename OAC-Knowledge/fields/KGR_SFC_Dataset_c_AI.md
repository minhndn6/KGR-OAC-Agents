# (KGR) SFC Dataset (có AI)

- **type**: db_dataset
- **grain**: dim/lookup  ()
- **producer_flow**: 
- **used_by_workbooks**: ['(KGR) BRD.BC03-04-05_SFC ước tính_SFC thực tế_ MIS']
- **physical_tables**: ['DW_NS_ACCOUNTINGPERIOD_D', 'DW_NS_ITEM_D', 'DW_NS_X_CAM_CUSTOMRECORD_CSEG_SCV_CHAIN', 'DW_NS_X_CAM_CUSTOMRECORD_CSEG_SCV_PRODCATG', 'DW_NS_X_CAM_CUSTOMRECORD_CSEG_SCV_PRODGROUP', 'DW_NS_X_SALE_CHANNEL', 'DW_NS_X_SFC_LINES_CF', 'DW_NS_X_SFC_TRANSACTION_HEADERS_1']

> Join-key & WHERE NỘI BỘ của dataset KHÔNG lộ qua API trên instance này (executePreview đọc cache XSA; endpoint dataset/datasets/metadata trả 500). Cột giữ qualifier bảng vật lý nên biết ĐỦ bảng+cột nguồn; quan hệ join theo chuẩn NetSuite (line→ACCOUNT/ITEM/PERIOD; extension→ID; segment→CSEG_*). Filter NGHIỆP VỤ quan trọng (posting/acct/subsidiary/vụ việc) nằm ở DATAFLOW tiêu thụ — xem field_dictionary cột tương ứng. confidence: join=medium.

## Cột