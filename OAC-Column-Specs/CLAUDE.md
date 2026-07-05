# OAC-Column-Specs — Rule-book công thức cấp-cột cho báo cáo KGR (ĐỌC TRƯỚC KHI LÀM)

> Project chuyên trách: tạo tài liệu mô tả **rule/công thức/loại trừ/mapping của MỌI cột & MỌI dòng** trên các
> báo cáo OAC release của Kangaroo, để **phía Kangaroo confirm** làm **baseline** (đổi sau = change request).
> Đây là việc DÀI, NHIỀU SESSION → **luôn đọc `STATE.md` trước**, làm dứt điểm 1 canvas rồi cập nhật STATE.

## Bắt đầu mỗi session
1. Đọc `STATE.md` (tiến độ từng canvas) + `docs/OBJECTIVE.md` (mục tiêu/scope) + `docs/PLAN.md`.
2. Kích hoạt skill **`kgr-rulebook`** (`.claude/skills/kgr-rulebook/SKILL.md`) — chứa quy trình 7 bước + nguyên tắc + scripts.
3. Trước khi soạn mô tả: đọc `.claude/skills/kgr-rulebook/references/METHOD.md` (chuẩn viết "Cách tính").

> ⚠️ **Chống compaction / phiên dài:** TUYỆT ĐỐI không dựa vào lịch sử hội thoại để giữ chuẩn — nó sẽ mất khi compact. Mọi chuẩn + dữ liệu + tiến độ đã nằm trong các file durable trên. Chất lượng được bảo đảm bởi **Definition of Done** trong SKILL.md: 1 canvas chỉ giao khi **harness ALL PASS + cổng reviewer tài chính 100% ĐẠT + cập nhật STATE**. Hai cổng này từ chối bản dưới chuẩn ngay cả khi context đã mất — đó là cơ chế giữ nhất quán.

## Nguyên tắc CỨNG (chi tiết trong SKILL.md)
- **LIVE = nguồn chân lý**; công thức lấy từ **dataflow def live** + viz def live. Live đúng → mô tả trung thực, KHÔNG gắn cờ-lỗi.
- **CẤM suy công thức bằng logical-SQL gộp** (oac-native auto-aggregate/lũy kế đánh lừa). Logical-SQL chỉ để liệt kê giá trị dimension.
- **READ-ONLY** trên OAC; cấm MCP `nsaw-oac-poc`; đăng nhập điền-1-lần (ORA-28000).
- Mô tả **đủ để tài chính tự tái lập 1 dòng số**; không lộ tên field kỹ thuật ở cột hướng-người-dùng.
- **Hygiene:** mọi file làm việc ở `work/`. Trước khi báo xong: `python ../OAC-Knowledge/kb_lifecycle/tools/check_clean.py --strict`.

## Cấu trúc project
- `docs/` — OBJECTIVE, PLAN (+tracker), ARCHITECTURE, CONVENTIONS.
- `.claude/skills/kgr-rulebook/` — skill (SKILL.md + references/ + scripts/).
- `work/` — snapshots_live/ (def đóng băng) · skeletons/ · rulebooks/ (JSON nội bộ) · out_md/ (.md giao dần) · FINAL/ (Excel).
- `STATE.md` — sổ tiến độ đa-session. `glossary.json` — thuật ngữ dùng chung.

## Liên hệ workspace
- Browser đọc live: MCP `chrome-lineage` (profile `profile-lineage`, KHÔNG kill Chrome toàn cục — chỉ theo profile của mình).
- Số/lineage sâu: skill `kgr-oac-lineage` (kho `../OAC-Knowledge`). Credentials OAC: `../.secrets/oac.env` (uỷ quyền điền-1-lần).
- Con trỏ resume liên-session: `C:\Project\_kgr-state\orchestration\rulebook_bc_RESUME.md` (đã dời NGOÀI cây; tra bằng `kgr_runtime.orch_dir()`).
