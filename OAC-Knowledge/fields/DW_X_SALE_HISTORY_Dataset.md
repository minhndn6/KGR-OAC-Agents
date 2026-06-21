# DW_X_SALE_HISTORY_Dataset

- **type**: db_dataset
- **grain**: dim/lookup  ()
- **producer_flow**: 
- **used_by_workbooks**: ['(KGR) DB01.Revenue_v1.1', '(KGR) DB02.Expense_v1.1']
- **physical_tables**: ['DW_X_SALE_HISTORY']

> Join-key & WHERE NỘI BỘ của dataset KHÔNG lộ qua API trên instance này (executePreview đọc cache XSA; endpoint dataset/datasets/metadata trả 500). Cột giữ qualifier bảng vật lý nên biết ĐỦ bảng+cột nguồn; quan hệ join theo chuẩn NetSuite (line→ACCOUNT/ITEM/PERIOD; extension→ID; segment→CSEG_*). Filter NGHIỆP VỤ quan trọng (posting/acct/subsidiary/vụ việc) nằm ở DATAFLOW tiêu thụ — xem field_dictionary cột tương ứng. confidence: join=medium.

## Cột