# OAC-Column-Specs

Project tạo **rule-book công thức cấp-cột** cho báo cáo OAC của Kangaroo (BC01 Daily Summary; BC03-04-05 SFC/MIS) để Kangaroo **confirm** làm **baseline** (đổi sau = change request).

## Tiếp tục công việc (mỗi session)
1. Đọc `STATE.md` (đang ở đâu) + `docs/OBJECTIVE.md` + `docs/PLAN.md`.
2. Theo `CLAUDE.md` → kích hoạt skill `kgr-rulebook` (`.claude/skills/kgr-rulebook/SKILL.md`).
3. Làm dứt điểm 1 canvas theo quy trình 7 bước → cập nhật `STATE.md`.

## Bản đồ nhanh
- `docs/` — OBJECTIVE · PLAN(+tracker) · ARCHITECTURE · CONVENTIONS.
- `.claude/skills/kgr-rulebook/` — skill: SKILL.md, references/ (METHOD, LIVE_RECIPES, OAC_MODEL_PARSING), scripts/.
- `work/` — snapshots_live · skeletons · rulebooks · out_md · FINAL.
- `STATE.md` · `glossary.json`.

## Nguyên tắc 1 dòng
LIVE = đúng & là nguồn chân lý (công thức từ dataflow def, KHÔNG suy bằng SQL-sum); READ-ONLY; mô tả đủ để tài chính tự tái lập 1 dòng số.
