# LEARNING — cơ chế để AI tích lũy tri thức, thông minh dần qua từng phiên

> Vấn đề: KB tĩnh không tự lớn. Cơ chế này biến mỗi phiên làm việc thành **tri thức tích lũy**: phát hiện mới / bị user sửa / gặp gap → ghi lại → review → đưa vào KB.

> **CƠ CHẾ THẬT = `kb_lifecycle/tools/learn2.py`** (governance: content_hash dedup, fact_key,
> typed promote-gate, supersede có audit, CHẶN số-cứng theo type). `skill/.../scripts/learn.py`
> giờ là **shim DEPRECATED** forward sang learn2 — gọi lệnh nào cũng được, ngữ nghĩa là learn2.

## Vòng học (capture → review → promote)
```
[Trong lúc làm] phát hiện fact mới / user correction / gap / Q&A đáng nhớ / bài học
      │  learn2.py add <type> "<topic>" "<content>" [source] [confidence]
      │  (fact/correction/formula_correction/physical_table + SỐ-CỨNG lớn -> BỊ CHẶN;
      │   lesson/qa/open-question CHO PHÉP số = ví-dụ tái lập)
      ▼
learnings/log.jsonl  (append-only, durable, dedup theo content_hash, KHÔNG lưu số cấu trúc)
      │  learn2.py list pending   → learnings/pending.md (regen: learn.py pending shim)
      ▼
[Định kỳ / cuối phiên] REVIEW pending → cập nhật file KB phù hợp:
   - fact cấu trúc/cột/bảng  → catalog (.yaml) tương ứng
   - ý nghĩa/metric           → business_glossary.yaml
   - mâu thuẫn/giả định       → CONFLICTS_AND_OPEN_QUESTIONS.md
   - rủi ro governance        → governance_register.md
   - bài học vận hành/AI      → CONVENTIONS.md / skill
   + 1 dòng CHANGELOG.md
      │  learn2.py promote <id> '<evidence-json>'   (typed-gate: cần rebuild_sha/live_evidence/attested_by…)
      ▼
KB lớn lên — phiên sau thông minh hơn.
```

## type
- **fact**: dữ kiện cấu trúc mới (cột/bảng/dataflow/grain) phát hiện khi làm.
- **correction**: user/owner sửa → ghi lại để KHÔNG lặp lỗi (vd nghĩa metric, producer sống).
- **gap**: thiếu sót KB phát hiện qua câu hỏi không trả lời được.
- **qa**: cặp hỏi-đáp đáng tái dùng (vào fields/ hoặc glossary).
- **lesson**: bài học kỹ thuật/AI/process (vd reproducibility, encoding).

## Nguyên tắc
- KHÔNG ghi số tuyệt đối vào fact cấu trúc (data live) — ghi *cách tính / quan hệ / bài học*. (learn2 **CHẶN CỨNG** số tuyệt đối lớn cho type fact/correction/formula_correction/physical_table; type lesson/qa/open-question CHO PHÉP số vì đó là ví-dụ tái lập.)
- Mỗi correction từ user = ưu tiên promote ngay (đó là tri thức quý nhất).
- learnings/log.jsonl + pending.md là TRACKED (git) → tích lũy bền qua phiên, qua compaction.
- Khi orchestrator/consultant trả lời sai và được sửa → BẮT BUỘC `learn2.py add correction`.

## Tích hợp
- Skill `kgr-oac-lineage` & `kgr-oac-orchestrator`: khi phát hiện mới / bị sửa / gặp gap → gọi `learn2.py add` (hoặc shim `learn.py add` — cùng ngữ nghĩa). Cuối phiên: `learn2.py list pending` + promote (typed-gate).
- Đây cũng là bước **KB-update** trong orchestrator (sau khi dựng dataset/dataflow mới → ghi learning → promote vào catalog).
