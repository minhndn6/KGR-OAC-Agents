# Routing reference — orchestrator O1 (read/advisory)

## Phân loại yêu cầu → route
| Yêu cầu | Route O1 | Có cần GHI (O2)? |
|---|---|---|
| "Field/số này từ đâu / tính sao / impact" | → OAC-knowledge (read) → trả lời | Không |
| "Cần metric M theo D ở grain G — lấy đâu" | → OAC-knowledge (capability/source) | Không (nếu đã có) |
| "Nên show gì cho [sếp] / thiết kế dashboard" | → dashboard-builder[pha design] (blueprint) + OAC-knowledge profile data | Không (design) |
| "Dựng dashboard X cần dữ liệu chưa có" | → design → OAC-knowledge (source_blueprint) → **XUẤT KẾ HOẠCH** (dataflow+viz) | **CÓ → O2/người** |
| "Dựng/đổi dataset/dataflow" | → OAC-knowledge (nguồn) → **XUẤT KẾ HOẠCH** | **CÓ → O2/người** |

## Quy tắc quyết định
- Nếu trả lời được bằng **đọc** (knowledge/design) → làm tới cùng, trả kết quả.
- Nếu cần **ghi** (save viz / build-run dataflow) → **DỪNG ở kế hoạch**: xuất các bước GHI + nguồn + gate, ghi vào blackboard, báo "cần O2/duyệt người". KHÔNG tự gọi pha build.

## Blackboard protocol (single-writer = orchestrator)
- `new` khi nhận yêu cầu phối hợp. `set blueprint/source_blueprint/...` sau mỗi pha. `log` mỗi lần gọi sub-agent.
- Sub-agent trả JSON (consultation_playbook / agent_contracts outputs) → orchestrator merge vào blackboard.
- KHÔNG ghi số tuyệt đối vào blackboard.

## Ví dụ (O1) — "Thêm KPI Lợi nhuận gộp KD theo Chuỗi × tháng lên dashboard"
1. `blackboard.py new "KPI LN gộp KD theo Chuỗi×tháng" "T5-2026"` → bb_id.
2. design: blueprint = combo/bar "a9 theo Chuỗi", note. (gate: user duyệt)
3. OAC-knowledge: a9 (LN gộp KD) có ở `TD_Report_Long`/`TD_Metrics_Wide` (Metric a9); theo Chuỗi? → a9 ở grain kỳ/ngành, **chưa có grain Chuỗi** → cần dataflow mới từ hub `(KGR) DTF_CALC_INVOICE_MEMO_#` (line grain, có Chuỗi) tính a9-components theo Chuỗi. ⚠️ a9 = a4−a5−a6−a7−a8, **a6/a7/a8 ước tính AOP** → disclosure bắt buộc; **KHÔNG SUM ratio**.
4. **Kế hoạch (giao O2/người)**: (a) dataflow-builder dựng dataset `a9 theo Chuỗi×kỳ` từ hub (join key/filter theo source_blueprint) → cross-check; (b) dashboard-builder add dataset + build combo + disclosure note + verify + clevel gate + save ADD-only.
5. Trả user: blueprint + source_blueprint + kế hoạch + cảnh báo. (Không tự ghi.)

## O2 (CHƯA bật) — điều kiện trước khi cho GHI tự động
rotate password + tài khoản read-only; profile chrome-lineage; chốt producer sống + ký GR1–GR7; write-lock (lock.py) + human-approval gate; observability. Xem `../ORCHESTRATION_DESIGN.md` §6.
