# OAC-Orchestrator — thiết kế AI-tổng điều phối 3 (→ N) sub-agent KGR

> Đây là **gói THIẾT KẾ** (chưa phải implementation) cho AI-tổng tương lai điều phối **3 sub-agent = 3 project**:
> **dashboard-builder** (Dashboard-builder; gồm pha *design* = skill oac-dashboard-designer + pha *build* = oac-dashboard-builder),
> **OAC-knowledge** (`kgr-oac-lineage`, read), **dataflow-builder** (Dataflow-builder).
> *nsaw-knowledge (NSAW_Claude) = backend SAU OAC-knowledge, không phải agent thứ 4.* Tạo sau review 2026-06-20 (P2).

## File
- `ORCHESTRATION_DESIGN.md` — luồng điều phối, trình tự gọi, freshness coordination, chính sách context >1M.
- `agent_contracts.yaml` — contract máy-đọc của từng agent (owns / must_not / inputs / outputs JSON / calls / exclusive_resource / gate).
- `blackboard_schema.json` + `blackboard.template.json` — state object dùng chung do orchestrator sở hữu (thay handoff .md rời).
- `concurrency_model.md` — 1-writer-nhiều-reader, profile-per-actor, write-lock, sở hữu login/session.
- `lock.py` — helper file-lock theo workbook (sẵn để orchestrator gọi).

## Nguyên tắc nền (từ họp review)
1. **Externalize**: tri thức ở file (OAC-Knowledge KB) + script truy hồi → context orchestrator luôn nhỏ; bài toán >1M token gần như không xảy ra.
2. **1-writer-nhiều-reader**: reads (lineage/crosscheck/designer) fan-out; writes (builder/dataflow) serialize + write-lock; mỗi browser-actor 1 profile.
3. **Số luôn LIVE**; cấu trúc/lineage cache trong KB (có freshness gate).
4. **Precedence**: OAC>NSAW (đk freshness); báo cáo BC>dashboard DB.
5. **Session mới + handoff khi qua gate/ngưỡng**, không kéo 1 session tới 1M.

## CHỜ trước khi hiện thực (phụ thuộc owner — xem OAC-Knowledge/CONFLICTS + governance_register)
- Rotate password OAC + tài khoản read-only riêng (cho reader-agents).
- Chốt producer sống (multi-producer) trước khi cho tự động sửa dataflow.
- Tạo profile thứ 3 (chrome-lineage/profile-lineage) cho lineage live-read.
