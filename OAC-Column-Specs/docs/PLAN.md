# PLAN — Kế hoạch thực thi (theo phase) + tracker

> Tiến độ chi tiết từng canvas: xem `STATE.md`. File này là kế hoạch khung.

## Phase
- **P0 — Hạ tầng** (xong): chrome-lineage (profile riêng), token refresh, snapshot live, skeleton deterministic, harness máy.
- **P1 — Khung project + skill** (đang): dựng OAC-Column-Specs (docs, skill kgr-rulebook, scripts, STATE), chốt METHOD + reviewer.
- **P2 — Soạn theo từng báo cáo** (giao dần): mỗi canvas chạy 7 bước (SKILL.md) tới 100% ĐẠT → giao .md.
  - Thứ tự đề xuất: BC01_Summary_TĐ (pilot, làm lại đạt bar) → BC01_Summary_Ngành → BC01_Hàng ngày → BC03-04-05 (SFC Ước Tính → SFC Thực Tế → MIS).
- **P3 — Gộp & bàn giao**: hợp nhất out_md → Excel (FINAL), Glossary + cột "KGR xác nhận"; check_clean; trình Kangaroo confirm từng sheet.

## Quy mô (từ skeleton live)
- BC01: 3 canvas / 12 viz / ~95 cột (+ pivot summary: 6 cột giá trị × ~25 dòng chỉ tiêu/pivot).
- BC03-04-05: 3 canvas / 13 viz / ~106 cột (3 bảng chi tiết lớn 35/27/40 cột).

## Cơ chế đảm bảo chất lượng
- Harness máy (coverage/grounding/no-leak/required/glossary) + Reviewer tài chính (rubric, tới 100% ĐẠT).
- Nguồn công thức = dataflow def live (chống sai SQL-sum). Giao dần để Kangaroo phát hiện sớm.

## Rủi ro & đối phó (tóm tắt)
- Khối lượng lớn × độ sâu cao → fan-out Workflow theo viz; tái dùng nguồn (HUB doanh thu/giá vốn dùng chung).
- oac-native auto-agg đánh lừa → cấm SQL-sum suy công thức.
- Phiên dài → STATE.md + snapshots đóng băng để resume.
- Chrome bị kill → profile riêng, không kill toàn cục.
