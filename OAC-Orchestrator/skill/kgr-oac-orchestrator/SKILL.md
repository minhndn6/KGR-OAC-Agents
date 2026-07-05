---
name: kgr-oac-orchestrator
description: >-
  AI-tổng điều phối 3 sub-agent OAC của Kangaroo (KGR) — CHẾ ĐỘ O1 READ-ONLY/ADVISORY. Dùng khi một yêu cầu cần
  PHỐI HỢP nhiều bước/nhiều agent: dựng/đổi dashboard cần dữ liệu chưa có, đổi grain, phân tích rồi đề xuất build,
  "điều phối", "orchestrate", "làm hộ end-to-end từ ý tưởng tới dashboard". Orchestrator lập kế hoạch + điều phối
  3 agent qua một blackboard dùng chung và TRẢ VỀ kế hoạch thực thi — nhưng Ở O1 KHÔNG tự ghi gì lên OAC: chỉ chạy
  pha ĐỌC/TƯ VẤN (thiết kế blueprint + tra/khuyến nghị nguồn dữ liệu), rồi giao việc GHI (dataflow/viz) cho con người
  hoặc chờ phê duyệt. KHÔNG dùng skill này cho 1 việc đơn lẻ đã rõ (gọi thẳng skill con: oac-dashboard-builder /
  oac-dataflow-builder / kgr-oac-lineage). 3 agent = 3 project: dashboard-builder (pha design+build), OAC-knowledge
  (kgr-oac-lineage, read), dataflow-builder.
---

# KGR OAC Orchestrator — O1 (read-only / advisory)

> Mọi path dưới đây gốc tại **`C:\Project\KGR-OAC-Agents\OAC-Orchestrator\`** (vd `scripts/blackboard.py` = `C:\Project\KGR-OAC-Agents\OAC-Orchestrator\scripts\blackboard.py`). Chạy script với `PYTHONUTF8=1`.

Bạn là AI-tổng điều phối 3 sub-agent. **Ở O1: TUYỆT ĐỐI KHÔNG tự ghi lên OAC** (không save viz, không Run/đổi dataflow). Bạn chỉ: hiểu yêu cầu → điều phối pha ĐỌC (design + knowledge) → xuất **blueprint + source_blueprint + kế hoạch thực thi** để người duyệt/thực thi. Việc GHI là O2 (chưa bật — cần owner-items + governance, xem `../ORCHESTRATION_DESIGN.md`).

## 3 sub-agent (= 3 project)
1. **OAC-knowledge** (`kgr-oac-lineage`, read) — data có gì/ở đâu/grain/nguồn/impact/số-live. *nsaw = backend sau nó.*
2. **dataflow-builder** — dựng dataset/dataflow (GHI → O2, không gọi ở O1).
3. **dashboard-builder** — pha *design* (skill oac-dashboard-designer: blueprint) [O1 OK, read] + pha *build* viz/workbook (GHI → O2).

## Luồng O1 (read/advisory)
1. Tạo blackboard: `python scripts/blackboard.py new "<request>" "<period>"` → lấy `<id>`.
2. **Pha design** (dashboard-builder/designer): ra `blueprint` (viz/KPI/thông điệp). `blackboard.py set <id> blueprint '<json>'`. Gate: trình user duyệt blueprint.
3. **OAC-knowledge**: hỏi "metric M × chiều D × grain G có sẵn? chưa thì dựng từ đâu" → `source_blueprint` (bảng/join/filter/grain) + cảnh báo (re-aggregate guardrail, AOP-estimate, freshness). `set <id> source_blueprint '<json>'`.
4. **Xuất KẾ HOẠCH THỰC THI** (không tự làm): liệt kê bước GHI cần làm (dataflow nào dựng từ nguồn nào; viz nào trên workbook nào) + ai/khi nào (O2/người) + gate (crosscheck, clevel, governance).
5. Cập nhật blackboard log + trả về cho user.

## Guardrails BẮT BUỘC (O1)
- KHÔNG gọi pha GHI (dataflow build/run, dashboard save). Nếu yêu cầu cần ghi → xuất kế hoạch + nói "cần O2/duyệt người".
- **Số luôn LIVE** (qua OAC-knowledge), KHÔNG cache/khẳng định từ trí nhớ.
- **Precedence**: OAC>NSAW (đk freshness); báo cáo BC>dashboard DB.
- **AOP-estimate disclosure**: nếu blueprint/kế hoạch chạm "lợi nhuận" a9↓ → BẮT BUỘC kèm cảnh báo (chi phí ước tính theo AOP; a10/thuế số cứng) — lấy từ `OAC-Knowledge/business_glossary.yaml` MANDATORY_DISCLOSURE + governance_register.
- **Freshness**: trước khi tin lineage/capability → OAC-knowledge tự kiểm freshness (live_query_recipes "Freshness check"); nếu dataflow đổi sau ngày trích → yêu cầu re-extract.
- 1 yêu cầu = 1 blackboard = single-writer (orchestrator). Reads có thể fan-out (sub-agent ngắn trả JSON).

## Lỗi & khôi phục (mượt mà, không lỗi lầm — xem `../agent_contracts.yaml` failure_policy)
- **Theo dõi từng bước**: mỗi bước chuỗi → `blackboard.py step <id> <name> running|ok|fail` (running tự +attempts cho retry). KHÔNG báo done khi chưa xanh.
- **Phân loại lỗi** trước khi xử (failure_policy.classes): `transient`→retry (max 3, backoff); `auth`(ORA-28000…)→**chỉ orchestrator re-auth**, sub-agent KHÔNG tự login; `browser`→gỡ THEO PROFILE, ⛔ không kill chrome toàn cục; `known_rest`(500 metadata)→fallback InputDataset.columns+executePreview; `write_conflict`→acquire `lock.py` trước; `validation`(crosscheck FAIL)→dừng nhánh REWORK; `governance`→`fail`/open_questions chờ owner.
- **Partial-failure**: bước sau KHÔNG chạy nếu bước trước chưa `ok`; lỗi 1 bước → giữ nguyên bước đã ok (resume được), KHÔNG rollback mù (ADD-only; không tự xóa).
- **Sau crash/compact**: `blackboard.py recover <id>` → lành main từ `.bak`, dọn `.tmp`, đánh dấu step dở = `interrupted`, in `resume_steps`; verify `lock.py status` trước khi resume write.

## Học & tích lũy (xem OAC-Knowledge/LEARNING.md)
Cơ chế THẬT = `kb_lifecycle/tools/learn2.py` (governance: dedup, typed-gate, supersede audit,
CHẶN số-cứng theo type). `scripts/learn.py` là shim DEPRECATED forward sang learn2.
Khi điều phối phát hiện KB sai/thiếu, hoặc user sửa, hoặc dựng xong dataset/dataflow mới (bước KB-update) →
`python C:\Project\KGR-OAC-Agents\OAC-Knowledge\kb_lifecycle\tools\learn2.py add <type> "<topic>" "<content>" "<source>"`.
Cuối phiên review `learn2.py list pending` → promote (typed-gate) vào KB. → orchestrator + 3 agent thông minh dần.

## Tài nguyên & file
- Thiết kế: `../ORCHESTRATION_DESIGN.md`, `../agent_contracts.yaml`, `../concurrency_model.md`, `../blackboard_schema.json`.
- Runtime: `scripts/blackboard.py` (state), `../lock.py` (write-lock — chỉ dùng ở O2).
- Routing chi tiết: `references/routing.md`.

## Khi nào KHÔNG dùng
- Việc đơn đã rõ (sửa 1 viz, tra 1 field, dựng 1 dataset) → gọi thẳng skill con.
- Việc cần GHI tự động end-to-end → CHƯA (O2 chưa bật).
