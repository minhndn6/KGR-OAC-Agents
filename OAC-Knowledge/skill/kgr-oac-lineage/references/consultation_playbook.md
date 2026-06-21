# Consultation playbook — khi builder-agent gọi OAC-knowledge

Vai: được `dashboard-builder` hoặc `dataflow-builder` (hoặc orchestrator) gọi để tham vấn data. Trả lời gọn, có cấu trúc, kèm độ tin + cảnh báo. Số luôn live (tự query nếu cần).

## Loại câu hỏi & cách trả lời

### 1) "Hiện trạng data: tôi cần metric M theo chiều D ở grain G — có sẵn không?"
1. Tra `capability_map.yaml`: `by_metric[M]` ∩ `by_dimension[D]`; check `datasets.<ds>.grain ≤ G`.
2. Trả về:
   - **Có sẵn**: dataset nào, grain, cột, có materialize không, recipe lấy live. (Nếu nhiều → chọn authoritative theo precedence BC>DB.)
   - **Có nhưng sai grain**: nguồn mịn hơn để re-aggregate, hoặc cần aggregate-step.
   - **Chưa có**: nói rõ thiếu gì, sang câu (2).
3. Nếu cần xác nhận data đã có cho kỳ/chiều cụ thể → TỰ chạy executePreview (read-only) và báo "tính đến thời điểm query".

### 2) "Chưa có — dựng dataflow thế nào / lấy từ đâu nhanh & đúng nhất?" (cho dataflow-builder)
Theo `source_selection_playbook.md`:
- Ưu tiên **reuse/extend** dataset/dataflow gần nhất (thường là hub `(KGR) DTF_CALC_INVOICE_MEMO_#` — đã có hầu hết chiều + DT/COGS/GP/CKKM/Xanh-Đỏ ở line grain → re-aggregate mọi grain).
- Nếu build mới: chỉ ra **bảng vật lý nguồn** (physical_table_catalog), **key join chuẩn NS**, **filter nghiệp vụ bắt buộc** (posting/acct/subsidiary/HTL), **grain đích**, và **cạm bẫy** liên quan (fan-out GVMT, Xanh/Đỏ date-range, AOP-estimate…).
- Trả về 1 "blueprint nguồn": từ bảng X,Y → join trên key → filter → grain → metric.

### 3) "Field/số này từ đâu, tính sao, loại trừ gì?" (cho dashboard-builder / audit)
→ Dùng `field_dictionary.yaml` + `fields/<ds>.md`; trả: công thức bung tới gốc + filter + bảng vật lý + ý nghĩa + cảnh báo (ước tính/số cứng). Mẫu: `fields/_FLAGSHIP_LoiNhuanGopKinhDoanh.md`.

### 4) "Đổi bảng/dataflow X thì ảnh hưởng gì?" (impact)
→ `lineage_graph.yaml` đi ngược tới `workbook:` / `find_source`/`trace_field`. Liệt kê dataset/dataflow/viz bị ảnh hưởng.

## Format trả về (gợi ý)
- **Kết luận** (1–2 câu: có/không, nguồn nào).
- **Chi tiết**: dataset/dataflow/bảng + công thức/filter + grain.
- **Độ tin & cảnh báo**: confidence; precedence đã áp; ước tính/số cứng/multi-producer chưa xác nhận.
- **Lấy số live**: recipe (nếu hỏi số) — kèm "data live, số có thể đổi".
- **Khuyến nghị** (nếu tư vấn build): reuse/extend/build + blueprint nguồn.

## JSON output contract (để orchestrator tiêu thụ máy)
Khi được gọi tự động, ngoài câu trả lời người-đọc, trả kèm 1 block JSON theo loại câu hỏi:

Loại 1 (availability/source):
```json
{"type":"source","available":true,"metric":"revenue","dimensions":["chuoi","model"],
 "source_dataset":"(KGR) DTF_CALC_INVOICE_MEMO_#","grain":"invoice line","reaggregatable":true,
 "authoritative":true,"confidence":"cao","caveats":["KHÔNG SUM ratio; ASM/tỉnh không có ở hub"],
 "live_query_recipe":"executePreview OutputDataset ...","recommendation":"reuse hub, re-aggregate"}
```
Loại 3 (trace field):
```json
{"type":"trace","field":"a9","dataset":"TD_Metrics_Wide","producer_flow":"KGR_DF_TD_Metrics_bk",
 "formula":"a4 - a5_CP CKKM - a6 - a7 - a8","physical_roots":["DW_NS_CUSTOMER_INVOICE_LINES_F.BASE_REVENUE","..."],
 "filters":["ISPOSTING='T'","ACCTTYPE IN('Income','OthCurrLiab')"],"disclosure":"a6/a7/a8 ước tính theo AOP",
 "confidence":"cao"}
```
Loại 4 (impact): `{"type":"impact","changed":"physical:DW_NS_X_GIA_VON_MUC_TIEU_CT","affected_workbooks":[...],"affected_datasets":[...]}`.
Số tuyệt đối KHÔNG nằm trong JSON (lấy live riêng).

## Luôn nhớ
- Không khẳng định con số từ trí nhớ — query live.
- OAC > NSAW_Claude; BC > DB.
- Nếu phát hiện fact mới/đổi → đề xuất cập nhật KB (CHANGELOG + file tương ứng), không tự sửa số.
