# OWNER TODO — việc chỉ owner làm được (AI không tự làm)

> Gom các việc cần bạn/owner xử lý. AI đã làm hết phần an toàn (P0+P1+P2 thiết kế+O1). Dưới đây KHÔNG chặn O1 read-only; nhưng **chặn O2 (ghi tự động)**.

## A. Bảo mật (làm sớm)
- [ ] **Rotate mật khẩu OAC** (`minhndn@bizin.vn`) — đã từng lộ plaintext nhiều nơi (đã redact khỏi file active + các project cũ đã archive, nhưng `.secrets/oac.env` + bản cũ vẫn còn giá trị). Đổi trên OAC/IDCS rồi cập nhật `C:\Project\KGR-OAC-Agents\.secrets\oac.env`.
- [ ] (Khuyến nghị) Tạo **tài khoản OAC read-only** riêng cho reader-agents (lineage/crosscheck) — tránh lockout + least-privilege.

## B. Chốt dữ liệu (xem CONFLICTS_AND_OPEN_QUESTIONS.md §F + governance_register.md)
- [ ] **F1** — Mệnh đề `"Kênh nội bộ" IN('T')` lặp trong dataflow revenue: xác nhận nghĩa ('T' = gồm hay loại nội bộ?) + dọn mệnh đề trùng (idempotent, không sai số nhưng nên sạch).
- [ ] **F2** — Chốt **producer SỐNG** (xem Run-history trên OAC UI): đề xuất `Nganh_Report_Long_#`→v3, `Daily_Nganh_Report`→_m, `ACTUAL_AOP_MONTHLY_v2`→(mơ hồ).
- [ ] **GR1–GR7** (governance_register): ký xác nhận hoặc yêu cầu sửa — AOP-estimate, số cứng a10/thuế 0.21, whitelist 2 subsidiary, drift NSAW.

## C. Điều kiện bật O2 (orchestrator GHI tự động) — sau A,B
- [ ] Tạo profile/MCP `chrome-lineage` (concurrency: mỗi browser-actor 1 profile).
- [ ] Bổ sung contract: error/retry/partial-failure + ai sở hữu KB-update (xem agent_contracts.yaml).
- [ ] Blackboard: single-writer + recovery khi orchestrator chết; lock fencing token (lock.py).
- [ ] **Human-approval gate** cho mọi ghi chạm P&L; cưỡng chế disclosure AOP qua orchestrator.
- [ ] Observability: consultation_log + blackboard log.

## D. Hygiene còn lại (không gấp)
- [ ] Relocate pipeline `C:\Project\KGR-OAC-Agents\Dashboard-builder\_oac_extract` → OAC-Knowledge self-contained (sửa STG path) — hiện vẫn chạy được từ chỗ cũ; backup đã ở OAC-Knowledge/raw. Xem `raw/REBUILD.md`.
- [ ] Bỏ hardcode period (vd 42) khỏi mastery/skill → bơm qua blackboard.
- [ ] Cập nhật NSAW_Claude theo các drift đã ghi (D1–D4) khi rảnh.

## Đã xong (tham khảo)
KB lineage+consultant (4 wb→63 ds→40 df→60 bảng), skill kgr-oac-lineage, archive_recommendations, P0 (secrets/git/AOP/precedence/allowlist/archive legacy), P1 (grain/no-TODO/guardrail/customer/AsOfDate/JSON contract/examples/encoding-test), P2 thiết kế orchestrator (OAC-Orchestrator/), O1 orchestrator read-only (skill kgr-oac-orchestrator + blackboard). git: OAC-Knowledge, OAC-Orchestrator, Dashboard-builder, Dataflow-builder.
