# ORCHESTRATION DESIGN — AI-tổng điều phối 3 (→N) sub-agent KGR OAC

> Trả lời câu hỏi gốc của user: *"kiến trúc 3 project đã hoàn chỉnh để 1 AI-tổng gọi & điều phối chưa?"* → **Gần đủ**: tri thức + skill + boundary đã tốt; còn thiếu (a) contract máy-đọc cho builders, (b) state dùng chung, (c) mô hình đồng thời + lock, (d) gỡ stack cũ (đã làm P0). Doc này định nghĩa (a)–(c).

## 1. Vai trò & ranh giới — 3 AGENT (chi tiết → agent_contracts.yaml)
- **OAC-knowledge** (`kgr-oac-lineage`) = tri thức data + tư vấn nguồn + số live (READ). *nsaw-knowledge = backend SAU nó, không phải agent.*
- **dataflow-builder** = data prep (dataset/dataflow).
- **dashboard-builder** = gồm **PHA design** (skill oac-dashboard-designer: WHAT/WHY, blueprint) + **PHA build** (viz/workbook). *designer KHÔNG phải agent thứ 4 — là pha đầu của dashboard-builder.*
- 1 việc = 1 owner. Ranh giới hay bị vượt: **dashboard-builder KHÔNG tự dựng dataflow** → phải gọi dataflow-builder.

## 2. Luồng điều phối chuẩn — "dựng dashboard cần dataset mới"
```
user → ORCHESTRATOR (tạo blackboard: request, period)
 1. dashboard-builder[PHA design]  → blueprint (viz/KPI)        [reads OAC-knowledge, fan-out OK]  gate: user duyệt
 2. OAC-knowledge       → "metric M × chiều D × grain G có chưa? chưa thì dựng từ đâu"
                          → source_blueprint (bảng/join/filter/grain)                      [read]
 3. dataflow-builder    → dựng dataset theo source_blueprint, Run, cross-check
                          → built_datasets[], reload_hint        [WRITE: lock dataflow]    gate: crosscheck PASS
 4. dashboard-builder[PHA build] → add dataset, build viz, format, verify số (executeOrPoll), save ADD-only
                          → saved_canvas_refs, clevel_verdict     [WRITE: lock workbook]   gate: clevel SHIP
 5. OAC-knowledge (kb-update) → ghi dataset/dataflow mới vào catalog (KNOWLEDGE_INDEX §cập nhật)
```
- Hand-off qua **blackboard** (blackboard_schema.json), KHÔNG qua .md rời.
- **period** orchestrator bơm 1 chỗ → mọi agent dùng (bỏ hardcode 42 rải rác — cleanup khi hiện thực).

## 3. Concurrency (chi tiết → concurrency_model.md)
1-writer-nhiều-reader; profile-per-actor (tạo chrome-lineage); write-lock theo artifact (lock.py); orchestrator sở hữu login/session + freshness gate.

## 4. Freshness coordination
- `kb_freshness` trong blackboard. Trước khi tin NSAW → check stale; trước khi tin 1 dataset OAC → freshness probe (live_query_recipes "Freshness check"). Số LUÔN live.
- Nếu probe thấy dataflow đổi sau ngày trích KB → orchestrator yêu cầu lineage **re-extract** trước khi tư vấn lineage chi tiết.

## 5. Context >1M token — chính sách orchestrator (từ họp AI Tech Lead)
- **Externalize nền**: orchestrator giữ blackboard + con-trỏ, KHÔNG nạp KB; sub-agent đọc lát cắt cần qua script (`trace_field`/`find_source`) → mỗi context nhỏ.
- **Fan-out reads** (sub-agent ngắn trả JSON) thay vì gom hết vào 1 context.
- **Ngưỡng**: compact chat-scratch ~40%; **session mới + handoff (qua blackboard) ở ~60–70% hoặc mỗi gate**. KHÔNG kéo 1 session tới 1M (compaction mất filter/ID).
- Mỗi sub-agent là **1 context fresh** đọc đúng phần của mình → bài toán 1M token gần như không phát sinh.

## 6. Còn thiếu để HIỆN THỰC (phụ thuộc owner / khi dựng orchestrator)
1. Rotate password + tài khoản OAC read-only cho readers (P0 owner).
2. Tạo profile/MCP `chrome-lineage` (concurrency).
3. Nhúng contract front-matter vào SKILL.md của 3 agent (hiện tập trung ở agent_contracts.yaml — chưa sửa xâm lấn skill đang chạy).
4. Bỏ hardcode period 42 khỏi mastery/skill (parameterize qua blackboard).
5. Chốt producer sống + governance (CONFLICTS F2 + governance_register) trước khi cho tự động sửa dataflow.
6. Relocate pipeline `_oac_extract` (Dashboard-builder) → OAC-Knowledge (self-contained; xem OAC-Knowledge/raw/REBUILD.md).
```
