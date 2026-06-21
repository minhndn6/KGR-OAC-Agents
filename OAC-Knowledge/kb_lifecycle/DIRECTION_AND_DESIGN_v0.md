# KB Lifecycle — Direction & Design v0 (for adversarial review)

> Mục đích tài liệu: chốt ĐỊNH HƯỚNG + THIẾT KẾ cho 3 cơ chế owner giao, rồi giao sub-agent mổ xẻ.
> Đây là **v0 — bản để bị phản bác**. Reviewer phải tấn công, không xác nhận.
> Ngày: 2026-06-21 · Phạm vi: 4 repo dưới `C:\Project\KGR-OAC-Agents\` (+ scratch ngoài `C:\Project\_work\`).
> Ràng buộc owner: KHÔNG xóa/sửa OAC & NSAW. Được sửa thoải mái repo hiện hành (đã backup).

---

## 0. Vấn đề (từ owner, nguyên văn rút gọn)

1. **Chống rác / "AI nào dùng cũng biết ghi tri thức mới vào đâu"** — không chồng chéo, không rác, không sai cấu trúc. Hệ phải sống "mãi mãi".
2. **Tự học** — AI bám kịp OAC khi OAC & data thay đổi không ngừng. Đây là phần *cốt lõi*, không phải phụ.
3. **Giữ harness sạch** — AI khác dùng hệ KHÔNG được ghi vào thư mục project; scratch/state phải nằm chỗ khác.

## 1. Chẩn đoán hiện trạng (từ review độc lập trước đó — bằng chứng file:line)

- KB là **catalog SINH RA** từ pipeline `raw/` (`build_catalogs.py`, `field_dict_build.py`, `resolver.py`...). ⇒ **Bẫy cấu trúc #1**: nếu AI sửa tay `dataset_catalog.yaml`, lần rebuild kế tiếp **xoá sạch**. Hiện KHÔNG có gì cảnh báo "file này sinh ra, đừng sửa tay".
- `learn.py promote` (`skill/kgr-oac-lineage/scripts/learn.py:42-50`) chỉ **lật cờ status**, không kiểm: KB đã sửa chưa, có trùng/mâu thuẫn không, schema có hợp lệ không. ⇒ **rác/ảo có thể vào KB**.
- `LEARNING.md:36`: `correction` → "promote ngay" — không qua chốt thứ hai.
- `validate_kb.py` / `qa_*.py` **không đọc** `learnings/log.jsonl` ⇒ learning bẩn không bị bắt.
- Rebuild **không tái lập từ repo**: input `raw/*.json` + `_work/` gitignored; staging path `Dashboard-builder/_oac_extract` không tồn tại; `EXTRACT_DATE` hardcode (`build_catalogs.py:12`).
- **Hygiene rò**: `.gitignore` chặn `_*.json` mà KHÔNG chặn `_*.md` ⇒ 7 file `_PNL_*.md` đang tracked trong `Dashboard-builder/`. `lock.py`/`blackboard.py` ghi state **vào trong repo** (`_orchestration/locks`, `OAC-Orchestrator/blackboards`).
- `blackboard_schema.json` là tài liệu, KHÔNG validate khi ghi (`blackboard.py:84-92` set dotted-key tuỳ ý).

⇒ Cả 3 vấn đề owner nêu đều có gốc kỹ thuật rõ ràng, **chữa được bằng "biến quy ước thành cưỡng chế"**.

## 2. Nguyên tắc thiết kế (kim chỉ nam)

- **P1 — Enforcement > Convention.** Mọi bất biến phải có code/test/hook ép, không dựa trí nhớ agent.
- **P2 — Single source of truth, machine-readable.** Một manifest máy-đọc trả lời "cái gì ở đâu, sửa thế nào".
- **P3 — Generated ≠ Curated ≠ Log.** Phân loại rõ; mỗi loại có MỘT đường ghi hợp lệ.
- **P4 — Self-healing & idempotent.** Chạy lại an toàn; rác bị từ chối tại cổng, không phải dọn sau.
- **P5 — Repo sạch theo mặc định.** Scratch/state ra ngoài repo *bằng API*, không bằng nhắc nhở.
- **P6 — Giữ bất biến cũ:** không lưu số tuyệt đối; OAC-live precedence; ADD-only production; rebuild deterministic.
- **P7 — Backward-safe.** Không phá skill/script đang chạy; thay đổi xâm lấn tối thiểu, có migration.

## 3. Kiến trúc giải pháp — 5 thành phần

### A. Knowledge Map — manifest máy-đọc (`OAC-Knowledge/knowledge_map.yaml`)
Khai báo MỌI artifact tri thức:
```yaml
artifacts:
  - id: dataset_catalog
    path: dataset_catalog.yaml
    kind: GENERATED            # GENERATED|CURATED|LOG|DOC|RUNTIME
    write_via: rebuild         # rebuild|learn.py|direct-edit|tool-only|NEVER
    built_from: [raw/datasets_all.json, raw/build_catalogs.py]
    owner_role: kgr-oac-lineage
    schema: schemas/dataset_catalog.schema.json   # optional
  - id: business_glossary
    path: business_glossary.yaml
    kind: CURATED
    write_via: direct-edit
    schema: schemas/glossary.schema.json
  - id: learnings_log
    path: learnings/log.jsonl
    kind: LOG
    write_via: learn.py        # append-only, không sửa tay
```
→ Là **chân lý** cho "cái gì ở đâu / sửa kiểu gì". Mọi tool & test đọc từ đây.

### B. Write-Router — `kb_route.py` ("ghi tri thức mới vào đâu?")
CLI + thư viện. Input = *loại tri thức*; output = đích + phương pháp + validation bắt buộc.
```
python kb_route.py classify --type new_dataset
→ {target: "raw/ + rebuild", method: "edit source extract rồi REBUILD.md", forbidden: "sửa tay dataset_catalog.yaml",
   validate: ["validate_kb.py","qa_full.py"], note: "GENERATED — hand-edit sẽ bị guard chặn"}
python kb_route.py classify --type correction --about field_formula
→ {target: "learn.py add (LOG) → review → sửa raw/ → rebuild", ...}
```
Các `type` tối thiểu: `new_dataset, new_dataflow, new_field, formula_correction, gap, convention, glossary_term, governance_item, drift, physical_table`.
→ Bất kỳ AI nào (kể cả AI lạ) chỉ cần gọi 1 lệnh là biết chỗ ghi đúng — hết "đoán".

### C. Enforcement layer (code + hook + test)
1. **Generated-guard** (`guard_generated.py` + git pre-commit): nếu file `kind:GENERATED` đổi mà `built_from` không đổi ⇒ **FAIL** ("bạn sửa tay file sinh ra"). Mỗi file GENERATED gắn banner header + hash nguồn.
2. **Schema-validate**: file `CURATED`/`LOG` validate theo `schema` khi commit (và trong `validate_kb`).
3. **Learn-gate** (nâng cấp `learn.py`): `add` từ chối trùng (content-hash) & cảnh báo số tuyệt đối (đã có) nay **chặn cứng**; `promote` đòi (i) tham chiếu commit/diff đã sửa KB, (ii) check mâu thuẫn với fact cùng key (phải `supersede` tường minh kèm lý do), (iii) với claim kiểm-live-được: 1 `verify_ref`.
4. **Cleanliness-test**: FAIL nếu có file tracked khớp mẫu scratch (`_PNL_*`, `*.network-response`, `blackboards/*`, `_snap_*`...). Sửa luôn rò `_*.md`.

### D. Self-learning loop (cốt lõi — máy trạng thái cưỡng chế)
```
observe → record(LOG, structured, append-only) → validate+route(B,C) →
incorporate(qua đường hợp lệ: rebuild hoặc direct-edit) → verify → mark incorporated
```
- **Drift sensors** (engine "bám kịp OAC"): khi có OAC live → các probe phát hiện lệch:
  - `freshness`: dataflow đổi sau `EXTRACT_DATE` → emit learning `drift:reextract`.
  - `existence`: dataset/bảng trong KB còn tồn tại trên OAC?
  - `formula_spotcheck`: công thức KB còn khớp def live? (mẫu nhỏ, xoay vòng).
  - Probe **không cần** chạy đêm nay; thiết kế interface + chạy offline bằng fixture trước.
- Learning về *cấu trúc* (dataset/dataflow mới) → **bắt buộc** đi qua re-extract + rebuild (deterministic), KHÔNG patch tay YAML. Log ghi rebuild nào đã hấp thụ.
- Tách `confidence`: low/medium KHÔNG được tiêu thụ như fact chính cho tới khi verify.

### E. Workspace hygiene — `runtime_paths` (API, không phải nhắc nhở)
- Module nhỏ `kgr_runtime.py` (đặt ở OAC-Knowledge, các repo khác import qua path hoặc bản sao mỏng): trả về **runtime root NGOÀI repo**:
  - env `KGR_RUNTIME_DIR` ưu tiên; mặc định Windows `%LOCALAPPDATA%\kgr-oac\runtime\`; có phân vùng con `locks/`, `blackboards/`, `scratch/<session>/`, `extracts/`.
- **Di dời state ra ngoài repo**: `lock.py` (`KGR_LOCK_DIR` đã có — đổi default sang runtime root) và `blackboard.py` (`BB_DIR` → runtime root). Repo không còn chứa state chạy.
- **Quy tắc 1 dòng cho mọi agent** (đưa vào mỗi CLAUDE.md/SKILL.md): *"Mọi output không-phải-tri-thức ghi qua `kgr_runtime.scratch()`; KHÔNG ghi vào cây repo."*
- Belt-and-suspenders: vá `.gitignore` (`_*.md`, `blackboards/`, runtime), gỡ track `_PNL_*.md` (giữ bản ngoài).

## 4. Tiêu chí nghiệm thu (đo được)

- AC1: Gọi `kb_route.py classify --type X` cho mọi `type` → trả đích hợp lệ tồn tại trong `knowledge_map.yaml`. (≥10 type)
- AC2: Sửa tay 1 file GENERATED → guard/test FAIL với thông báo rõ.
- AC3: `learn.py add` trùng nội dung → bị từ chối; `promote` thiếu `verify_ref`/diff-ref → bị từ chối; 2 learning mâu thuẫn → bắt buộc `supersede`.
- AC4: Bất kỳ file scratch nào lọt vào tracked → cleanliness-test FAIL.
- AC5: `lock.py`/`blackboard.py` mặc định KHÔNG tạo file nào trong cây repo (ghi ra runtime root).
- AC6: `knowledge_map.yaml` phủ 100% file `.yaml/.md` tri thức hiện có (không sót, không thừa).
- AC7: Bộ test cũ (validate_kb, qa_*, test_orchestrator) vẫn PASS (không regress).
- AC8 (UAT): ≥200 use-case "AI cần ghi/đọc tri thức" định tuyến đúng & bị chặn khi sai.

## 5. Câu hỏi mở cho reviewer (HÃY TẤN CÔNG)

- Q1: Knowledge Map có phải over-engineering không? Có cách nhẹ hơn (ví dụ chỉ header banner + naming convention) đạt cùng mục tiêu chống-rác không?
- Q2: Generated-guard dựa "built_from đổi" có chắc bắt được mọi hand-edit? Bypass nào? (vd sửa cả nguồn lẫn output cho khớp)
- Q3: Cross-repo: 4 git repo riêng, `kgr_runtime.py` để đâu cho 3 repo còn lại dùng mà không tạo coupling rác? Copy? Submodule? Junction? Env-only?
- Q4: Self-learning có tạo *noise rác mới* không (drift sensor báo động giả tràn log)? Cơ chế chống bão learning?
- Q5: Promote-gate đòi `verify_ref` — với fact KHÔNG kiểm-live-được (vd quy ước nghiệp vụ) thì gate là gì để không thành cửa chết?
- Q6: Di dời blackboard/lock ra runtime root có phá recovery/test hiện tại không? Migration an toàn?
- Q7: Có nên dùng SQLite/DuckDB cho LOG + index thay vì jsonl + YAML monolith để chống rác ở 10×? Đánh đổi?
- Q8: Đâu là thứ tự triển khai rủi-ro-thấp-nhất để không vỡ skill đang chạy?
- Q9: "AI lạ" (không thuộc 4 skill) làm sao biết tới `kb_route.py`? Điểm vào (entrypoint) nên là gì (README? skill front-matter? một lệnh `kgr doctor`)?
- Q10: Bất biến nào còn THIẾU mà đề xuất này chưa phủ?

## 6. Phi-mục-tiêu (đêm nay)
- KHÔNG bật O2 (auto-write OAC). KHÔNG đụng logic OAC/NSAW.
- KHÔNG chạy probe live (chỉ thiết kế interface + test bằng fixture) cho tới khi owner login.
- KHÔNG refactor lớn skill builder; chỉ thêm hook/quy tắc tối thiểu.
