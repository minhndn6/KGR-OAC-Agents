# QA_PROCESS — Vòng QA1 → QA2 trên rule-book (.md) + 3 cột QA mới

> Pha sau khi 6 .md đã đạt cột GỐC. Mục tiêu: 2 vòng QA độc lập (đại diện người confirm KGR), thêm 3 cột QA (KHÔNG đè cột gốc), rồi gộp Excel mới. Đây là việc DÀI/đa-session — đọc file này + STATE.md trước khi làm; checkpoint STATE sau mỗi bước.

## Bất biến (không vi phạm)
1. **KHÔNG sửa/đè 3 cột GỐC** (Cách tính / Loại trừ / Ghi chú gốc) — đã chốt qua cổng reviewer 100%. Mọi chỉnh của QA ghi vào **3 cột MỚI**: `qa1_calc`, `qa1_exclusions`, `qa1_note` (hiển thị: "Cách tính (QA)" / "Loại trừ-Bộ lọc (QA)" / "Ghi chú (QA)").
2. **QA1** = người confirm KGR KHÓ TÍNH, KHÁCH QUAN, KHÔNG xem dataflow/tri thức nội bộ; CHỈ đọc .md. **QA2** = biên tập ngôn từ (không đổi nội dung tính toán/logic).
3. Khi QA cần xác minh lại công thức/ngữ nghĩa (live_check) → gọi sub-agent đọc def trong `work/snapshots_live/` để CHỐT, KHÔNG đoán/không bịa.
4. Nội dung tính toán/logic là của cột gốc (đã verify live). QA1 làm RÕ HƠN/sửa chỗ mơ hồ, KHÔNG bịa logic mới.

## Data model (rulebook JSON)
Thêm `"qa_phase": true`; mỗi row thêm `qa1_calc`, `qa1_exclusions`, `qa1_note`. Cột gốc (`calc`/`exclusions`/`note`) GIỮ NGUYÊN.
Dòng QA1 không có ý kiến → 3 cột QA = `"(Giữ nguyên)"`.

## Quy trình / mỗi file .md (checkpoint STATE sau mỗi bước)
1. **QA1 review** (sub-agent — `scripts/qa1_prompt.md`): đọc DUY NHẤT .md → JSON verdict + vấn đề + đề xuất sửa (+ `live_check` nếu cần). Lưu `work/qa/qa1_<slug>.json`.
2. **Apply QA1** (session): mỗi dòng → nếu "cần sửa": viết `qa1_*` = bản sửa (theo đề xuất QA1; nếu có `live_check` → gọi sub-agent đối chiếu def rồi mới viết); nếu "OK" → `qa1_*` = "(Giữ nguyên)". Set `qa_phase=true`. Lưu JSON. Checkpoint STATE.
3. **QA2 polish** (sub-agent — `scripts/qa2_prompt.md`): đọc cột gốc + qa1_* (qua .md đã render sơ bộ hoặc JSON) → trau chuốt ngôn từ CHỈ trên qa1_* (bỏ từ thừa/mơ hồ/lủng củng; giữ nguyên ý + số + logic). Trả JSON edits → apply vào JSON.
4. **Re-render .md** (`render_md.py` đã hỗ trợ cột QA). Checkpoint STATE (file: qa1✔ apply✔ qa2✔ rendered✔).

## Sau khi CẢ 6 file xong
Gộp Excel mới: `render_excel.py` (đã thêm 3 cột QA) → `work/FINAL/KGR_RuleBook_QA_<date>.xlsx`. Bố cục: cột GỐC giữ nguyên + 3 cột QA + 'KGR xác nhận'.

## DoD / mỗi file
qa1 reviewed + applied (live-check nếu cần) + qa2 polished + re-rendered + STATE cập nhật. Thiếu bước nào → chưa xong file đó.

## Thứ tự 6 file
BC01_Summary_TD · BC01_Summary_Nganh · BC01_HangNgay · BC0345_SFC_UocTinh · BC0345_SFC_ThucTe · BC0345_MIS.
