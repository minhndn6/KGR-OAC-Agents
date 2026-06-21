# LEARNING — cơ chế để AI tích lũy tri thức, thông minh dần qua từng phiên

> Vấn đề: KB tĩnh không tự lớn. Cơ chế này biến mỗi phiên làm việc thành **tri thức tích lũy**: phát hiện mới / bị user sửa / gặp gap → ghi lại → review → đưa vào KB.

## Vòng học (capture → review → promote)
```
[Trong lúc làm] phát hiện fact mới / user correction / gap / Q&A đáng nhớ / bài học
      │  learn.py add <type> "<topic>" "<content>" [source] [confidence]
      ▼
learnings/log.jsonl  (append-only, durable, KHÔNG lưu số)
      │  learn.py pending  → learnings/pending.md
      ▼
[Định kỳ / cuối phiên] REVIEW pending → cập nhật file KB phù hợp:
   - fact cấu trúc/cột/bảng  → catalog (.yaml) tương ứng
   - ý nghĩa/metric           → business_glossary.yaml
   - mâu thuẫn/giả định       → CONFLICTS_AND_OPEN_QUESTIONS.md
   - rủi ro governance        → governance_register.md
   - bài học vận hành/AI      → CONVENTIONS.md / skill
   + 1 dòng CHANGELOG.md
      │  learn.py promote <id> "<đã đưa vào file X>"
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
- KHÔNG ghi số tuyệt đối (data live) — ghi *cách tính / quan hệ / bài học*. (learn.py cảnh báo nếu phát hiện số.)
- Mỗi correction từ user = ưu tiên promote ngay (đó là tri thức quý nhất).
- learnings/log.jsonl + pending.md là TRACKED (git) → tích lũy bền qua phiên, qua compaction.
- Khi orchestrator/consultant trả lời sai và được sửa → BẮT BUỘC `learn.py add correction`.

## Tích hợp
- Skill `kgr-oac-lineage` & `kgr-oac-orchestrator`: khi phát hiện mới / bị sửa / gặp gap → gọi `learn.py add`. Cuối phiên: `learn.py pending` + promote.
- Đây cũng là bước **KB-update** trong orchestrator (sau khi dựng dataset/dataflow mới → ghi learning → promote vào catalog).
