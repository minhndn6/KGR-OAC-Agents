# Cross-KB contract — OAC-Knowledge ↔ NSAW_Claude (quy tắc freshness)

## Thứ tự ưu tiên khi MÂU THUẪN (precedence — CÓ ĐIỀU KIỆN, không tuyệt đối)
1. **OAC live > NSAW_Claude** — *với điều kiện* dataset OAC còn TƯƠI (kiểm `data_last_modified` / freshness probe). Nếu dataset OAC nghi cũ/chưa refresh kỳ hiện tại → verify live trước khi tin.
2. Trong OAC: **báo cáo BC (BC01, BC03-04-05) > dashboard DB (DB01, DB02)** — *trừ khi* nguồn BC là **multi-producer/Archived chưa xác nhận** (xem CONFLICTS F2) hoặc đã quá hạn refresh → khi đó KHÔNG mặc định tin BC, phải verify live producer trước.
3. Hai báo cáo mâu thuẫn nhau, hoặc nguồn "thắng" lại là bản chưa xác nhận → **flag owner**, không tự quyết.
4. **Quy tắc an toàn:** precedence chỉ chọn *nguồn nào để tin*, KHÔNG thay cho việc kiểm freshness. Số luôn lấy LIVE.
Các drift đã phân xử: `CONFLICTS_AND_OPEN_QUESTIONS.md` §D; nghi vấn producer/clause: §F; rủi ro governance: `governance_register.md`.

## Hai kho, hai vai trò
| Kho | Sở hữu | Độ tươi |
|---|---|---|
| **OAC-Knowledge** (kho này) | Mọi thứ TỪ biên InputDataset trở LÊN: workbook, dataset, dataflow, **và snapshot bảng/cột vật lý đang được dùng** | **TƯƠI** — trích live 2026-06-20 từ OAC |
| **NSAW_Claude** (`C:\Project\NSAW_Claude\data_context\`) | Ngữ nghĩa nghiệp vụ tầng vật lý: ý nghĩa cột, công thức canonical (Revenue/COGS/Xanh-Đỏ/AOP/SFC), data gap, sentinel | ⚠️ **CÓ THỂ CŨ** — ~1 tháng chưa update (≈2026-05) |

## Quy tắc vàng (vì NSAW_Claude có thể sai)
1. **OAC-Knowledge tự chứa tầng vật lý cho phần đang dùng.** `physical_table_catalog.yaml` liệt kê tên bảng `DW_NS_*` thật + đúng cột mỗi dataflow lấy, trích từ chính def dataflow (`InputDataset.columns` dạng `"TABLE"."col"`), đã xác minh resolve sống bằng `executePreview` flowSQL. → KHÔNG cần NSAW_Claude để biết field gốc ở bảng/cột nào.
2. **NSAW_Claude chỉ là tầng LÀM GIÀU ngữ nghĩa.** Dùng để hiểu *ý nghĩa* cột và *công thức nghiệp vụ chuẩn*. Mỗi entry bảng ở `physical_table_catalog.yaml` có `nsaw_claude_ref.documented_in_nsaw` cho biết NSAW_Claude có tài liệu bảng đó không.
3. **Mâu thuẫn → bản LIVE của OAC-Knowledge THẮNG.** Nếu NSAW_Claude nói cột/bảng khác với những gì thấy live ở đây (đổi tên, bỏ cột, công thức khác), tin bản live; ghi lệch vào `CONFLICTS_AND_OPEN_QUESTIONS.md` (#NSAW-drift).
4. **20/60 bảng vật lý ở đây CHƯA có trong NSAW_Claude** (`documented_in_nsaw=false`) — bằng chứng NSAW_Claude thiếu. Với các bảng này, chỉ có thông tin live ở đây; ngữ nghĩa sâu phải hỏi owner/tự suy từ tên cột.

## Token & cách resolve
- Trong lineage, bảng vật lý là node `physical:<DW_TABLE>` (tự chứa trong kho này) — KHÔNG phụ thuộc token ngoài.
- Để lấy ngữ nghĩa: mở `C:\Project\NSAW_Claude\data_context\TABLE_CATALOG.yaml` tìm theo tên bảng (`nsaw_claude_ref.table`); công thức nghiệp vụ ở `NSAW_Claude/data_context/QUICK_REFERENCE.md`. **Luôn kèm tâm thế: có thể đã cũ, verify trước khi tin.**

## Mốc đồng bộ
- OAC-Knowledge trích: **2026-06-20**.
- Đối chiếu với NSAW_Claude tại mốc CHANGELOG gần nhất của kho đó (~2026-05). Khi NSAW_Claude được update lại, nên review các mục `#NSAW-drift` trong CONFLICTS.

## Các file/tool khác trong `external/`
- `oac_rest_api_notes.md` — cookbook endpoint OAC + cách enumerate + bẫy (để re-extract sau này).
