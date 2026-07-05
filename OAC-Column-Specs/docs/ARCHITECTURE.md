# ARCHITECTURE — Rule-book pipeline (đa-session, có kiểm chứng)

## Luồng dữ liệu / báo cáo
```
OAC LIVE
  ├─(chrome-lineage GET projects/json)──► snapshots_live/<wb>_projects.json   (định nghĩa viz/cột)
  └─(chrome-lineage GET dataflows?dataFlowID)► snapshots_live/df_<flow>.json   (công thức chỉ tiêu)
        │
        ▼  build_skeleton.py (DETERMINISTIC, không AI)
   skeletons/<wb>_skeleton.json   = canvas → viz → cột (col_id, display, expr, filter, source)  ◄─ độ phủ
        │
        ▼  AUTHOR (theo METHOD: số nào×số nào + nguồn+khoá+kỳ+fallback; công thức chỉ tiêu ĐỌC TỪ df def)
   rulebooks/<canvas>.json   = {rows:[{block, name, calc, exclusions, note, evidence}]}
        │
        ├─► rulebook_tests.py (HARNESS máy): coverage / grounding / no-leak / required / glossary  → ALL PASS
        └─► REVIEWER tài chính (sub-agent, KHÔNG xem df): rubric 5 ý → dòng CHƯA ĐẠT thì sửa, lặp tới 100% ĐẠT
        │
        ▼  render_md.py
   out_md/<canvas>.md   (giao dần cho Kangaroo)
        │
        ▼  (khi mọi canvas ĐẠT) render_excel.py
   FINAL/KGR_RuleBook.xlsx   (1 sheet/báo cáo + Glossary + cột "KGR xác nhận")
```

## Hai tầng kiểm chứng (chống bịa & đảm bảo confirm-được)
- **Harness máy** (khách quan, nhanh): độ phủ đủ cột; mọi dòng có "calc"; không lộ field-gốc; đủ trường; glossary đủ.
- **Reviewer tài chính** (sub-agent đóng vai KGR, độc lập với người viết, KHÔNG được xem dataflow): chấm độ RÕ theo rubric — "tài chính có tự tái lập 1 dòng số không?". Dòng CHƯA ĐẠT → viết lại. Đây là cổng chất lượng then chốt.
- **Nguồn công thức = dataflow def live** (không phải SQL-sum) → chống sai do auto-aggregate/lũy kế.

## Điều phối agent
- **Author**: 1 agent/canvas (fan-out Workflow khi 1 canvas nhiều viz).
- **Reviewer**: agent độc lập, vai tài chính KGR; 2 mẫu mồi (1 ĐẠT/1 CHƯA ĐẠT) để hiệu chỉnh chấm.
- **Lineage trace**: hỏi skill `kgr-oac-lineage` khi cần truy nguồn bảng vật lý sâu.

## Resume đa-session
- `STATE.md` = trạng thái từng canvas (extracted/authored/harness/reviewed/delivered) + snapshot nào đã đóng băng.
- Session mới: đọc STATE → tiếp canvas dang dở. Snapshots_live giữ lại để khỏi fetch lại (re-fetch chỉ khi nghi đổi).

## Quyết định thiết kế (đã rút ra từ pilot)
- oac-native logical-SQL **không** đáng tin để verify số đo (auto-SUM, lũy kế) → công thức lấy từ df def.
- Reviewer đối kháng từng báo "lỗi" giả (a9 lệch, X/Đ "dead-code") do tạo tác SQL → bài học: verify theo def, không SQL ngây thơ.
- Output .md trong khi làm (nhanh, dễ sửa, dễ review); Excel chỉ ở bước cuối.
