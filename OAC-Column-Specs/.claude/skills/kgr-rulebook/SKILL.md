---
name: kgr-rulebook
description: >-
  Dựng & duy trì RULE-BOOK mô tả công thức/cách tính/loại trừ/mapping CẤP-CỘT cho các báo cáo OAC của
  Kangaroo (BC01 Daily Summary; BC03-04-05 SFC ước tính/thực tế/MIS) để phía Kangaroo ĐỌC & CONFIRM, làm
  baseline cho change request. Dùng skill này BẤT KỲ KHI NÀO user muốn: lập/cập nhật bản đặc tả công thức
  từng cột & từng dòng của báo cáo OAC KGR; mô tả "cột/chỉ tiêu này tính thế nào, lấy số nào nhân/trừ số nào,
  loại trừ gì" theo chuẩn tài-chính-confirm-được; tiếp tục công việc rule-book qua nhiều session (đọc STATE.md);
  hoặc gộp kết quả sang Excel bàn giao. Đây là công việc dài, nhiều session — luôn đọc STATE.md trước khi làm tiếp.
---

# KGR Rule-book builder

Tạo tài liệu để **phía tài chính Kangaroo xác nhận** rule/công thức/loại trừ của **mọi cột và mọi dòng** trên các báo cáo OAC release. Sau khi confirm → **baseline**; thay đổi sau này là change request.

## Nguyên tắc CỨNG (không vi phạm)
1. **LIVE là nguồn chân lý.** Công thức lấy từ **định nghĩa dataflow LIVE** + **định nghĩa viz LIVE** (projects/json). KB project chỉ tham khảo. Live đúng → mô tả trung thực, KHÔNG phán xét/không gắn cờ-lỗi.
2. **CẤM suy công thức bằng logical-SQL gộp.** `oac-native` auto-aggregate cột đo (vd Metric_Code thật 1..24 bị SUM ×số-dòng = 115×k) và dữ liệu lũy-kế-theo-ngày cộng chồng → SAI. Logical-SQL CHỈ dùng để liệt kê giá trị dimension (distinct). Verify số (nếu cần) phải cố định 1 AsOfDate.
3. **READ-ONLY trên OAC.** Chỉ GET. Không POST/save. Cấm MCP `nsaw-oac-poc`. Một tài khoản dùng chung → đăng nhập điền-1-lần, lỗi thì dừng (ORA-28000).
4. **Mô tả ở tầng nghiệp vụ** đủ để tài chính tự tái lập 1 dòng số (xem `references/METHOD.md`). Không lộ tên field/bảng kỹ thuật ở cột hướng-người-dùng.
5. **Hygiene:** mọi file làm việc nằm trong `OAC-Column-Specs/work/`. Không ghi rác ra ngoài.

## Phạm vi (2 workbook — chốt qua live)
- **(KGR) BRD.BC01_Daily_Summary v1.1** — `/@Catalog/shared/(KGR) 1.Implement/(KGR) BRD.BC01_Daily_Summaryv1.1`. 3 canvas: BC01_Hàng ngày (4 bảng + filter), BC01_Summary_TĐ (pivot 25 chỉ tiêu), BC01_Summary_Ngành (4 pivot ngành + filter).
- **(KGR) BRD.BC03-04-05_SFC ước tính_SFC thực tế_ MIS** — `/@Catalog/shared/(KGR) Report/...`. 3 canvas: SFC Ước Tính, SFC Thực Tế, MIS (bảng chi tiết lớn).

## Quy trình / báo cáo (7 bước, resume được)
> Đọc `STATE.md` để biết canvas nào đang ở bước nào. Làm dứt điểm 1 canvas rồi cập nhật STATE.

1. **Truy cập live**: dùng MCP `chrome-lineage` (profile riêng, login OAC bền) + `oac-native`. Chi tiết & bẫy: `references/LIVE_RECIPES.md`.
2. **Trích & đóng băng**: GET projects/json (workbook) + GET dataflow def cho các flow nuôi chỉ tiêu → lưu `work/snapshots_live/` (timestamp).
3. **Skeleton (máy, deterministic)**: `scripts/build_skeleton.py <projects.json> <out> "<WB>"` → liệt kê ĐẦY ĐỦ canvas→viz→cột (col_id, display, expression, filter, source). Đảm bảo độ phủ. Cách model OAC map ra sao: `references/OAC_MODEL_PARSING.md`.
4. **Soạn mô tả theo METHOD**: với mỗi cột/chỉ tiêu, viết "Cách tính" CỤ THỂ (số nào×số nào, nguồn+khoá tra+kỳ+fallback) + "Loại trừ" bằng từ vựng KGR. Công thức chỉ tiêu lấy từ **dataflow def live** (không đoán). Chuẩn + ví dụ ĐẠT: `references/METHOD.md`.
5. **Harness máy**: `scripts/rulebook_tests.py --skeleton <s> --rulebook <r> --glossary <g>` → coverage / grounding / no-leak / required / glossary phải ALL PASS.
6. **Cổng review tài chính (sub-agent)**: gọi 1 sub-agent đóng vai chuyên viên tài chính KGR (KHÔNG cho xem dataflow) chấm từng dòng theo rubric (`scripts/reviewer_prompt.md`). Dòng CHƯA ĐẠT → viết lại → review lại tới **100% ĐẠT**.
7. **Giao .md** vào `work/out_md/`, cập nhật `STATE.md`. Sang canvas kế.

**Cuối cùng** (khi mọi canvas ĐẠT): gộp tất cả `out_md/` → 1 file Excel bàn giao (`work/FINAL/`), mỗi báo cáo 1 sheet + sheet Glossary, có cột "KGR xác nhận".

## Định dạng output (.md trong khi làm; Excel ở cuối)
Mỗi báo cáo: Glossary dùng chung + (báo cáo tổng hợp) 2 khối **A. Các cột giá trị** / **B. Các dòng chỉ tiêu**. Cột: `Cột/Chỉ tiêu · Cách tính · Loại trừ/Bộ lọc · Ghi chú · KGR xác nhận`. KHÔNG cột trạng thái/ý-nghĩa/nguồn/bằng-chứng. Render: `scripts/render_md.py`.

## Điều phối agent
- Author per-canvas (có thể fan-out Workflow nếu nhiều viz).
- Reviewer tài chính **độc lập** (người chấm ≠ người viết).
- Trace nguồn dataflow sâu → có thể hỏi skill `kgr-oac-lineage` (kho OAC-Knowledge).

## Pha QA bổ sung (sau khi 6 .md đạt cột gốc) — xem `../../docs/QA_PROCESS.md`
2 vòng QA độc lập đại diện người confirm KGR, THÊM 3 cột QA (`qa1_calc`/`qa1_exclusions`/`qa1_note`), **KHÔNG đè cột gốc**:
- **QA1** (`scripts/qa1_prompt.md`): chuyên viên KGR khó tính, CHỈ đọc .md → flag chỗ không-confirm-được / term-sai / mâu-thuẫn / khó-tái-lập + đề xuất sửa. Apply: `scripts/qa_apply.py --mode qa1`. Có `live_check` → gọi sub-agent đối chiếu def trong work/snapshots_live rồi mới chốt (không đoán).
- **QA2** (`scripts/qa2_prompt.md`): biên tập ngôn từ, CHỈ trau chuốt 3 cột QA (giữ nguyên ý/số/logic). Apply: `qa_apply.py --mode qa2`.
- Render `render_md.py`/`render_excel.py` tự hiện 3 cột QA khi `qa_phase=true`. **DoD/file QA**: qa1 + apply (+live_check) + qa2 + re-render + cập nhật STATE.

## Tài liệu kèm
- `references/METHOD.md` — chuẩn mô tả logic + ví dụ ĐẠT + rubric reviewer (ĐỌC TRƯỚC khi soạn).
- `references/LIVE_RECIPES.md` — endpoint live + auth + bẫy (auto-agg, lũy kế, BOM, double-JSON, proxy).
- `references/OAC_MODEL_PARSING.md` — cấu trúc projects/json → canvas/viz/edge/measures.
- `scripts/` — build_skeleton, render_md, rulebook_tests (harness), reviewer_prompt.

## Definition of Done & CHỐNG DRIFT (BẮT BUỘC — bảo đảm nhất quán qua phiên dài/compaction)
> Chất lượng KHÔNG được dựa vào trí nhớ hội thoại (sẽ mất khi compact). Nó dựa vào FILE DURABLE + 2 CỔNG KHÁCH QUAN dưới đây. Một context "mới tinh" đọc các file này vẫn cho ra kết quả y hệt.

**DoD — 1 canvas chỉ được đánh `delivered` khi đủ CẢ 3:**
1. Harness máy (`scripts/rulebook_tests.py`) **ALL PASS** (coverage/grounding/no-leak/required/glossary).
2. Cổng **reviewer tài chính** (spawn theo `scripts/reviewer_prompt.md`, gồm 2 mẫu mồi hiệu chỉnh) đạt **100% ĐẠT** — chưa đạt thì sửa & review lại.
3. Cập nhật `STATE.md` ngay (trạng thái + ngày + ghi chú).
→ Thiếu bất kỳ điều nào: **KHÔNG giao**. Hai cổng này TỪ CHỐI bản dưới chuẩn dù người soạn có "quên" — đây là thứ bảo đảm nhất quán, không phải trí nhớ.

**Quy tắc chống drift (mỗi canvas, mỗi session):**
- ĐỌC LẠI `references/METHOD.md` TRƯỚC khi soạn — đừng soạn theo trí nhớ.
- Công thức lấy từ **snapshot def đã đóng băng** (`work/snapshots_live/`) — KHÔNG suy từ SQL-sum; thiếu def thì fetch live (LIVE_RECIPES) rồi đóng băng.
- **Facts trong `STATE.md` là chuẩn** (map công thức đã chốt, scope...) — dùng lại, đừng tự tính lại khác đi.
- KHÔNG hạ bar, KHÔNG bỏ cổng reviewer, KHÔNG đoán (thiếu bằng chứng → fetch def, không bịa).
- Làm DỨT ĐIỂM 1 canvas rồi cập nhật STATE; không mở nhiều canvas dở.

**Sau COMPACTION / session mới:** chỉ cần đọc `CLAUDE.md → STATE.md → SKILL.md → references/METHOD.md` là khôi phục đủ chuẩn; tiếp canvas kế. Không cần lịch sử chat.
