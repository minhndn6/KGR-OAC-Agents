# CONVENTIONS — Định dạng, đặt tên, hygiene

## Cột chuẩn của rule-book (mỗi báo cáo)
`Cột / Chỉ tiêu` · `Cách tính (logic nghiệp vụ)` · `Loại trừ / Bộ lọc` · `Ghi chú` · `KGR xác nhận`
- KHÔNG có cột: trạng thái, ý nghĩa (gộp vào cách tính), nguồn-mô-tả, bằng-chứng-kỹ-thuật, yêu-cầu-thay-đổi.
- Báo cáo tổng hợp (pivot): 2 khối **A. Các cột giá trị** (áp cho mọi dòng) + **B. Các dòng chỉ tiêu** (mỗi dòng 1 công thức).
- Sheet đầu: **Glossary** thuật ngữ dùng chung (confirm 1 lần).

## Chuẩn viết "Cách tính" / "Loại trừ"
Theo `.claude/skills/kgr-rulebook/references/METHOD.md` (5 ý bắt buộc + bổ sung). Tiêu chí ĐẠT = tài chính tự tái lập 1 dòng số. Từ vựng loại-trừ dùng giá trị thật KGR ("VU1", "HCM", "hàng thanh lý (HTL)", "khách ký gửi", "kênh nội bộ"). Viết tắt không chắc → giữ nguyên, không tự giải nghĩa.

## Đặt tên file
- snapshot: `snapshots_live/<wb-slug>_projects.json`, `snapshots_live/df_<flow>.json`.
- skeleton: `skeletons/<wb-slug>_skeleton.json`.
- rulebook JSON (nội bộ): `rulebooks/<canvas-slug>.json`.
- output: `out_md/<canvas-slug>.md` (bản giao); `.draft.md` = bản nháp chưa đạt bar.
- final: `FINAL/KGR_RuleBook_<ngày>.xlsx`.

## Output language
Tiếng Việt, đối tượng đọc = tài chính Kangaroo. Số tuyệt đối KHÔNG ghi vào tài liệu (đổi theo ngày/refresh); chỉ mô tả cách tính.

## Hygiene
- Mọi file làm việc trong `OAC-Column-Specs/work/`. Snapshot lớn = regenerable (có thể gitignore).
- Trước khi báo xong: `python ../OAC-Knowledge/kb_lifecycle/tools/check_clean.py --strict`.
- READ-ONLY OAC; không POST/save; không kill Chrome toàn cục (chỉ theo profile-lineage).
