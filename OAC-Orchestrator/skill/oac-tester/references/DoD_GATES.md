# DoD_GATES — 7 cổng gác của oac-tester (recipe live, KHÔNG số cứng)

> Reviewer read-only. Mọi số lấy **LIVE** qua `oac-native` (⛔ KHÔNG `nsaw-oac-poc`). SQL dưới đây là **mẫu logical-SQL** — thay subject-area/cột theo `artifact_ref`; KHÔNG chép số vào KB. Mỗi cổng phải sinh 1 check `{name,result,evidence,source,expected,actual}`.

## Nguyên tắc chung
- **Thiếu evidence = FAIL** (không có "PASS trần").
- **Golden thiếu kỳ = BLOCKED** (không auto-PASS) — chờ owner cấp golden cho kỳ đó.
- **Lệch giải-thích-được** (item-scope, capture-basis) = PASS + ghi chú; **lệch không giải thích** = FAIL.
- Verdict tổng: dùng `scripts/verdict.py::decide_verdict` (FAIL > BLOCKED > PASS).

---

## Cổng #1 — SỐ-KHỚP-ĐA-NGUỒN (độc-lập-số) — 3 CHẾ ĐỘ
**Mục tiêu:** số viz live được xác nhận bằng ĐƯỜNG/NGUỒN ĐỘC LẬP, KHÔNG tự-xác-nhận trong chính pipeline OAC của artifact.
Số live từ viz (oac-native): `SELECT "<Fact>"."<Measure>" FROM "<SubjectArea>" WHERE "<Time>"."<Period>"='<period>'`.

**(A) CÓ golden owner-attested (mặc định — owner thường cấp):** so live vs golden NGOÀI pipeline OAC — chọn 1 theo cadence owner cấu hình:
`nsaw-analytics get_pl_report/get_sfc_report` · `seadent-docs tra_cuu_so_lieu` · rule-book **OAC-Column-Specs** owner-confirmed.
→ |live − golden| trong ngưỡng → **PASS**; lệch giải-thích-được (item-scope/capture-basis) → **PASS**+ghi chú; lệch không giải thích → **FAIL**.

**(B) KHÔNG có golden → TỰ SUY RA cross-check case-by-case (KHÔNG mặc định BLOCKED):** tester dùng HIỂU-BIẾT-DATA tự sinh ≥1 kiểm-tra-độc-lập PHÙ HỢP artifact/metric — chọn theo ngữ cảnh, ví dụ:
- **Sum-of-parts = total:** tổng theo chiều chi tiết (Ngành/Kênh/Chuỗi) == tổng tổng-hợp.
- **Cross-report reconciliation:** cùng metric ở báo cáo/nguồn KHÁC (BC01 report vs dashboard; DTF vs DW nguồn) có khớp.
- **Lineage-recompute:** qua `kgr-oac-lineage` lấy công thức gốc → tự tính lại từ dataset/field nguồn (oac-native) → so viz.
- **Sanity bậc-độ-lớn & dấu:** đúng bậc/đúng dấu nghiệp vụ (doanh thu ≥0; LN gộp ≤ doanh thu; % trong [0,1]…).
- **Continuity kỳ-liền:** period-over-period không nhảy bất thường không-giải-thích.
- **Alternative-aggregation-path:** tính lại con số bằng đường-tổng-hợp khác.
→ ≥1 cross-check khớp & KHÔNG mâu thuẫn → **PASS** (`source="self-derived cross-check"`, ghi RÕ cách đã dùng + evidence + độ-mạnh); có mâu thuẫn → **FAIL**.

**(C) BLOCKED chỉ khi** thật sự KHÔNG dựng nổi bất kỳ kiểm-tra-độc-lập nào (artifact quá cô lập: thiếu cả lineage lẫn báo cáo đối chiếu) → ghi lý do + đề xuất owner cấp golden. **KHÔNG BLOCKED chỉ vì "thiếu golden" — PHẢI thử (B) trước.**

> Mỗi check ghi rõ **mode (A/B/C)** + cross-check đã dùng. Owner khuyến khích cấp golden (đạt chuẩn cao nhất — mode A), nhưng thiếu golden KHÔNG làm tester bó tay: nó tự đánh giá theo hiểu-biết-data (mode B).

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
