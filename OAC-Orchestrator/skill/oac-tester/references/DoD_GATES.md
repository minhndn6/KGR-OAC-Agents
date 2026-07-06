# DoD_GATES — 7 cổng gác của oac-tester (recipe live, KHÔNG số cứng)

> Reviewer read-only. Mọi số lấy **LIVE** qua `oac-native` (⛔ KHÔNG `nsaw-oac-poc`). SQL dưới đây là **mẫu logical-SQL** — thay subject-area/cột theo `artifact_ref`; KHÔNG chép số vào KB. Mỗi cổng phải sinh 1 check `{name,result,evidence,source,expected,actual}`.

## Nguyên tắc chung
- **Thiếu evidence = FAIL** (không có "PASS trần").
- **Golden thiếu kỳ = BLOCKED** (không auto-PASS) — chờ owner cấp golden cho kỳ đó.
- **Lệch giải-thích-được** (item-scope, capture-basis) = PASS + ghi chú; **lệch không giải thích** = FAIL.
- Verdict tổng: dùng `scripts/verdict.py::decide_verdict` (FAIL > BLOCKED > PASS).

---

## Cổng #1 — SỐ-KHỚP-ĐA-NGUỒN (golden owner-attested)
**Mục tiêu:** số viz live == golden NGOÀI pipeline OAC (không tự-xác-nhận trong OAC).
1. Số live từ viz (oac-native):
   ```sql
   SELECT "<Fact>"."<Measure>"
   FROM   "<SubjectArea>"
   WHERE  "<Time>"."<Period>" = '<period>'
   ```
2. Golden ngoài pipeline (CHỌN 1, theo cadence owner cấu hình):
   - `nsaw-analytics get_pl_report` / `get_sfc_report` (period=`<period>`), hoặc
   - `seadent-docs tra_cuu_so_lieu` (owner-attested), hoặc
   - rule-book **OAC-Column-Specs** owner-confirmed cho cột đó.
3. So sánh: |live − golden| trong ngưỡng?  →  **PASS**. Golden **thiếu kỳ** → **BLOCKED**. Lệch không giải thích → **FAIL**.
> Nếu golden CHƯA tồn-tại-vật-lý toàn dự án → hạ cổng về "cross-check nội-OAC đa-điểm (BC01 report vs dashboard) + DISCLOSURE lệch", **KHÔNG** tuyên "độc lập".
> **BLOCKER cấu hình (đợi owner):** golden BC01/SFC owner-attested SỐNG Ở ĐÂU (path/kênh/cadence). Ghi vào blackboard field `blockers`, KHÔNG chặn sprint.

## Cổng #2 — FAN-OUT (nhân bản dòng)
**Mục tiêu:** phát hiện fan-out chi phí/doanh thu (lỗi lngopkd) do join đa kỳ.
```sql
SELECT COUNT(*)                                   AS rows_raw,
       COUNT(DISTINCT "<Txn>"||'-'||"<Line>")     AS rows_distinct
FROM   "<SubjectArea>" WHERE "<Time>"."<Period>" = '<period>'
```
`rows_raw > rows_distinct` (theo TRANSACTION+LINE ID) ⇒ fan-out ⇒ **FAIL** (evidence = 2 số). Bằng nhau ⇒ PASS.

## Cổng #3 — SCOPE/FILTER (exclude kênh nội bộ)
**Mục tiêu:** loại đúng kênh nội bộ mà KHÔNG hardcode id.
1. DERIVE id LIVE từ dimension (không hardcode "=14"):
   ```sql
   SELECT "<Chan>"."Id", "<Chan>"."Name" FROM "<SubjectArea>"
   WHERE  "<Chan>"."Name" IN ('<Kênh nội bộ>')
   ```
2. Kiểm số viz đã exclude đúng id đó. Filter thiếu/sai hoặc phát hiện hardcode id trong artifact ⇒ **FAIL**.

## Cổng #4 — BRANDING
Checklist (đọc `projects/json`): title **English + mode=Custom** (persist), màu **#44BA46/#F16522/#636466**, number format **M/%**, note **VN** (nếu yêu cầu). Bất kỳ mục sai/mất ⇒ **FAIL**. Evidence = trích thuộc tính từ projects/json.

## Cổng #5 — PERSIST (không tin toast)
```
GET .../projects/json   (SAU reload deep-link)
```
Kiểm: canvas/viz tồn tại, title Custom còn, màu còn, **last-modified mới hơn ts build**. `task_type=EDIT`: thêm kiểm KHÔNG regression viz khác trên cùng workbook. Mất sau reload ⇒ **FAIL**.

## Cổng #6 — LINEAGE-ĐÚNG-NGUỒN
Gọi **kgr-oac-lineage**: "field X của viz lấy từ dataset/dataflow nào?". Xác nhận KHÔNG nhầm **AOP-flat** cho **actual**, KHÔNG lấy _bk/_v cũ (xét in_closure + producer thực, tên vN không cho biết bản đúng). Sai nguồn ⇒ **FAIL**. Evidence = chuỗi lineage.

## Cổng #7 — DISCLOSURE a6-a21 / AOP
Nếu artifact chạm **a9↓ / CP lương a6 / gate a21** (chi phí dưới mức gộp = ƯỚC TÍNH AOP; a10 & thuế 0.21 là số cứng) ⇒ PHẢI có cảnh báo AOP-estimate theo `business_glossary` **MANDATORY_DISCLOSURE**. Thiếu ⇒ **FAIL**. Không chạm các mục này ⇒ PASS (n/a, evidence = "không chạm a6-a21").
