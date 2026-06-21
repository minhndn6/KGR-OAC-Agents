# Khuyến nghị Archive Dataflow/Dataset OAC (KGR)

> **Chỉ KHUYẾN NGHỊ — không tự xóa/di chuyển bất cứ gì.** Tài liệu này là deliverable phân tích, dùng để CTO/owner duyệt trước khi thao tác trên catalog OAC thật.

## Phương pháp & nguyên tắc đánh giá

- **Nguồn dữ liệu**: `dataflow_catalog.yaml` (40 dataflow), `dataset_catalog.yaml` (63 dataset), `catalog_enumeration.json` (folder path + lastModifiedTime + 2 object `sequence`). Đã đọc và đối chiếu chéo cả ba, không tin nguyên văn bản tóm tắt.
- **Test quyết định = reachability (khả năng tới đích)**: output dataset của dataflow có thực sự được 1 trong **4 workbook** dùng (trực tiếp hoặc bắc cầu) hay không. `in_closure: true` = có; `in_closure: false` = **ứng viên archive mạnh**.
- 4 workbook trong phạm vi: `(KGR) BRD.BC01_Daily_Summary`, `(KGR) DB01.Revenue_v1.1`, `(KGR) DB02.Expense_v1.1`, `(KGR) BRD.BC03-04-05_SFC ước tính_SFC thực tế_ MIS`.
- **Caveat 1 — hậu tố version KHÔNG phải bằng chứng đúng/sai.** v3 không nhất thiết là bản live; `_bk` không nhất thiết là backup chết; `v1.0` không nhất thiết là bản chuẩn. Chỉ xét bằng chứng reachability + folder + last_modified + thứ tự producer.
- **Caveat 2 — chỉ xét với 4 workbook nêu trên.** Nếu một dataflow có thể nuôi workbook NGOÀI phạm vi này thì hạ xuống REVIEW. Riêng flow sandbox/test thì archive an toàn.
- **Lưu ý đặc biệt về `in_closure` của bản trùng**: hai dataflow trùng output dataset đều bị đánh `in_closure: true` (vì cùng "có thể" sinh ra dataset đang dùng), nhưng **chỉ MỘT là producer live**. Vì vậy có 3 flow `in_closure: true` vẫn nằm trong danh sách ARCHIVE — đó là các bản v1.0 đã bị bản mới đè và đã nằm sẵn trong folder `(KGR) Archived`.

**Tổng quan đếm được**: 40 dataflow → **21 `in_closure: true`, 19 `in_closure: false`**.

---

## Bảng tổng hợp

### Nhóm A — ARCHIVE (độ tin cậy cao)

| Dataflow | Output dataset | in_closure | last_modified | Folder | Verdict | Lý do | Hỏng gì nếu archive |
|---|---|---|---|---|---|---|---|
| `(KGR) 1. DTF_CALC_INVOICE_MEMO_v1.0` | `(KGR) DTF_CALC_INVOICE_MEMO_#` | true* | 2026-06-18 | **(KGR) Archived** | ARCHIVE cao | Bản v1.0 đã ở folder Archived; producer live là bản `#` (mod 06-20). Trùng producer. | Không — bản `#` vẫn sinh output. |
| `(KGR) 5. DTF_CALC_MIS_v1.0` | `(KGR) DTF_CALC_MIS` | true* | 2026-06-18 | **(KGR) Archived** | ARCHIVE cao | Bản v1.0 đã ở folder Archived; producer live là bản `5.` (mod 06-19). Trùng producer. | Không — bản `5.` vẫn sinh output. |
| `KGR_DF_TD_Metrics_v1.0` | `TD_Report_Long`, `TD_Metrics_Wide` | true* | 2026-06-18 | **(KGR) Archived** | ARCHIVE cao | Bản v1.0 đã ở folder Archived; producer live là `_bk` (mod 06-20). Trùng producer. | Không — `_bk` vẫn sinh cả 2 output. |
| `KGR_DF_SANDBOX_EXPLORE` | (không có output) | false | 2026-06-10 | users/minhndn | ARCHIVE cao | Sandbox, 1 step, không sinh dataset nào. | Không gì. |
| `KGR_DF_AOP_v3test` | `KGR_DS_AOP_v3test` | false | 2026-06-11 | users/minhndn | ARCHIVE cao | Flow test ("AOP fix test"); output không tới workbook nào. | Không gì. |
| `DTF_PRODUCT_KPI_PY` | (không có output) | false | 2026-05-24 | @default/minhndn | ARCHIVE cao | 1 step AddColumns, không sinh dataset, không ai dùng. | Không gì. |
| `KGR_DF_ACTUAL_AOP_MONTHLY_v1` | `KGR_DS_ACTUAL_AOP_MONTHLY_v1` | false | 2026-06-11 | users/minhndn | ARCHIVE cao | Output `_v1` không tới workbook, không flow nào dùng. Bản cũ trong loạt MONTHLY. | Không — dataset cô lập. |
| `DF_TD_Report_PNL_v1` | `TD_Report_PNL_v1` | false | 2026-06-17 | users/minhndn | ARCHIVE cao | P&L long-format đời đầu; output không tới workbook, không flow nào dùng. Đã có bản Bridge thay thế. | Không — dataset cô lập. |
| `DF_TD_Report_PNL_v2` | `TD_Report_PNL_v2` | false | 2026-06-17 | users/minhndn | ARCHIVE cao | Bản kế của PNL_v1; output vẫn không tới workbook nào (workbook dùng `TD_Report_PNL_Bridge*`). | Không — dataset cô lập. |
| `KGR_DF_SFC_vs_Actual` | `KGR_DS_SFC_vs_Actual` | false | 2026-06-06 | users/minhndn | ARCHIVE cao | Bản đầu của SFC_vs_Actual; bản `_v2` (in_closure=true) đã thay thế và là input của chuỗi SFC live. | Không — `_v2` mới là bản dùng. |

\* `in_closure: true` chỉ vì trùng output với bản live; bản thân flow này là bản cũ đã bị đè → vẫn ARCHIVE.

### Nhóm B — REVIEW (cần cân nhắc / hỏi owner)

| Dataflow | Output dataset | in_closure | last_modified | Folder | Verdict | Lý do | Hỏng gì nếu archive |
|---|---|---|---|---|---|---|---|
| `KGR_DF_ACTUAL_AOP_MONTHLY_LK` | `KGR_DS_ACTUAL_AOP_MONTHLY_v2` | false | 2026-06-11 | shared/Data Flow | REVIEW | 1 trong 3 producer của cùng dataset `_v2`; dataset không tới workbook nào. Tên dataset nói "v2" nhưng producer có thể là LK/v3. | Có thể không, nhưng cần xác nhận flow nào đang chạy theo lịch. |
| `KGR_DF_ACTUAL_AOP_MONTHLY_v2` | `KGR_DS_ACTUAL_AOP_MONTHLY_v2` | false | 2026-06-11 | shared/Data Flow | REVIEW | Trùng producer (3 flow) của dataset không reachable; 5 step (clone editor-friendly). | Như trên. |
| `KGR_DF_ACTUAL_AOP_MONTHLY_v3` | `KGR_DS_ACTUAL_AOP_MONTHLY_v2` | false | 2026-06-11 | users/minhndn | REVIEW | Trùng producer (3 flow); ở folder user. | Như trên. |
| `(KGR) DF_ACTUAL_AOP_EXPENSE` | `(KGR) DTF_ACTUAL_AOP_EXPENSE` | false | 2026-06-18 | shared/Data Flow | REVIEW | Output chỉ nuôi loạt MONTHLY/AOP (toàn bộ không reachable) → dead subtree. Nhưng ở folder Data Flow chung, mod gần đây. | Gãy chuỗi MONTHLY (vốn đã không tới workbook). Hỏi owner xác nhận BC02 tháng có còn xài. |
| `(KGR) DF_ACTUAL_AOP_EXPENSE_minh` | `(KGR) DTF_ACTUAL_AOP_EXPENSE` | false | 2026-06-11 | users/minhndn | REVIEW | Trùng producer với bản trên; ở folder user `_minh` (bản cá nhân, cũ hơn). Bản chung mới hơn. | Không — bản chung là live hơn. |
| `(KGR) DF_GRAIN_ACTUAL_AOP` | `(KGR) DTF_GRAIN_ACTUAL_AOP` | false | 2026-06-11 | @default/anhdk (object id DF_BC02_ACTUAL_MONTH) | REVIEW | Output chỉ nuôi `DF_ACTUAL_AOP_EXPENSE*` (dead subtree). Có thể phục vụ "BC Thực tế Tháng". | Gãy chuỗi BC02 tháng nếu chuỗi đó còn dùng. |
| `(KGR) DF_FACT_EXPENSE` | `(KGR) DTF_FACT_EXPENSE` | false | 2026-06-18 | shared/Data Flow | REVIEW | Output chỉ nuôi `DF_ACTUAL_AOP_EXPENSE*` (dead subtree). 25 step, mod gần đây. | Gãy chuỗi expense tháng nếu còn dùng. |
| `(KGR) DF_DAILY_SC_CHAIN` | `(KGR) DTF_DAILY_KENH_CHUOI` | false | 2026-06-10 | @default/minhndn | REVIEW | Output không tới workbook nào, không flow nào dùng. Nhưng tên "lợi nhuận bước 2 theo kênh chuỗi" gợi báo cáo daily đang phát triển. | Có thể không tới workbook nào, nhưng xác nhận đây không phải feed báo cáo daily ngoài phạm vi. |
| `KGR_DF_SFC_Plan_by_Kenh` | `KGR_DS_SFC_Plan_by_Kenh` | false | 2026-06-09 | users/minhndn | REVIEW | Output không tới workbook nào, không flow nào dùng (plan-only theo Kênh). | Có thể dùng cho phân tích SFC ad-hoc; xác nhận. |
| `KGR_DF_Nganh_Cumulative_AsOf` | `KGR_DTF_CHI_PHI_XUC_TIEN` | false | 2026-06-03 | @default/minhndn (id "KGR_DF_Group Rate As-Of_Ngành") | REVIEW | Trùng producer của `KGR_DTF_CHI_PHI_XUC_TIEN` với `Group Rate As-Of`; mới hơn (06-03 vs 05-27). Dataset không reachable. | Không — nếu dùng thì bản này là bản mới hơn. |
| `KGR_DF_Group Rate As-Of` | `KGR_DTF_CHI_PHI_XUC_TIEN` | false | 2026-05-27 | @default/minhndn | REVIEW | Bản cũ hơn của cùng output; cả output không reachable. | Không — bị bản `Cumulative_AsOf` đè. |
| `KGR_DF_Group Rate As-Of_Ngành` | `KGR_DTF_Nganh_Cumulative_AsOf` | false | 2026-06-03 | @default/minhndn (id "...As-Of_Ngành1") | REVIEW | Output không tới workbook, không flow nào dùng. | Có thể cô lập; xác nhận. |

### Nhóm C — KEEP

| Dataflow | Output dataset | in_closure | last_modified | Verdict | Lý do |
|---|---|---|---|---|---|
| `(KGR) 1. DTF_CALC_INVOICE_MEMO_#` | `(KGR) DTF_CALC_INVOICE_MEMO_#` | true | 2026-06-20 | KEEP | Producer live nền tảng (BC01/DB01/DB02 + ~18 flow hạ nguồn dùng). |
| `(KGR) 5. DTF_CALC_MIS` | `(KGR) DTF_CALC_MIS` | true | 2026-06-19 | KEEP | Producer live nuôi workbook SFC/MIS (BC03-04-05). |
| `KGR_DF_TD_Metrics_bk` | `TD_Report_Long`, `TD_Metrics_Wide` | true | 2026-06-20 | KEEP | Producer live (mod mới nhất 06-20); nuôi BC01/DB02 + chuỗi Nganh/PNL/Daily. |
| `KGR_DF_Nganh_Metrics_v3` | `Nganh_Report_Long_#`, `SPmoi_ng_v3` | true | 2026-06-10 | KEEP | Producer live của `Nganh_Report_Long_#` (mới nhất + duy nhất sinh `SPmoi_ng_v3`). |
| `DF_Nganh_Report_Long_TD` | `Nganh_Report_Long_TD` | true | 2026-06-18 | KEEP | Nuôi DB02 (P&L ngành). |
| `DF_TD_Report_PNL_Bridge` | `TD_Report_PNL_Bridge` | true | 2026-06-18 | KEEP | Nuôi DB02 (waterfall P&L Tập đoàn). |
| `DF_TD_Report_PNL_Bridge_Nganh` | `TD_Report_PNL_Bridge_Nganh` | true | 2026-06-18 | KEEP | Nuôi DB02 (P&L bridge theo ngành). |
| `Union SALE HIST w INVC` | `SALE HIST w INVC` | true | 2026-06-10 | KEEP | Nuôi DB01.Revenue. |
| `KGR_DF_SFC_vs_Actual_v2` | `KGR_DS_SFC_vs_Actual_v2` | true | 2026-06-09 | KEEP | Nuôi DB01 + là input của `SFC_vs_MEMO_v1`. |
| `KGR_DF_SFC_vs_MEMO_v1` | `KGR_DS_SFC_vs_MEMO_v1` | true | 2026-06-07 | KEEP | Nuôi DB01. |
| `KGR_DF_SFC_vs_MEMO_v2` | `KGR_DS_SFC_vs_MEMO_v2` | true | 2026-06-09 | KEEP | Nuôi DB01. |
| `KGR_DF_SFC_vs_MEMO_v3` | `KGR_DS_SFC_vs_MEMO_v3` | true | 2026-06-07 | KEEP | Nuôi DB01 (grain nhóm SP). |
| `KGR_DF_SFC_vs_MEMO_v4_Chuoi` | `KGR_DS_SFC_vs_MEMO_v4_Chuoi` | true | 2026-06-09 | KEEP | Nuôi DB01 (theo Chuỗi). |
| `KGR_DF_Daily_TD_Report` | `Daily_TD_Report` | true | 2026-06-04 | KEEP | Nuôi BC01 Daily Summary. |
| `KGR_DF_Daily_Nganh_Report_m` | `Daily_Nganh_Report` | true | 2026-06-04 | KEEP | Producer live của `Daily_Nganh_Report` (bản `_m` mới hơn base). |

> Lưu ý các `KGR_DF_SFC_vs_MEMO_v1..v4` đều được DB01 dùng đồng thời (mỗi bản một grain: tổng / nhóm SP / chuỗi). Đây KHÔNG phải version chồng nhau — đừng archive theo phản xạ "vX cũ".

---

## Phân tích từng bộ trùng producer (duplicate-producer sets)

**1. `TD_Report_Long` & `TD_Metrics_Wide` ← `KGR_DF_TD_Metrics_bk` vs `KGR_DF_TD_Metrics_v1.0`**
Live = **`_bk`** (mod 2026-06-20, ở folder `@default/minhndn`, mới nhất). Superseded = **`_v1.0`** (mod 06-18, đã nằm trong `(KGR) Archived`). Bất chấp tên "_bk" nghe như backup, đây mới là bản chạy mới nhất; "_v1.0" mới là bản cũ đã được dọn vào Archived. → ARCHIVE `_v1.0`.

**2. `(KGR) DTF_CALC_INVOICE_MEMO_#` ← `(KGR) 1. DTF_CALC_INVOICE_MEMO_#` vs `..._v1.0`**
Live = **bản `#`** (mod 2026-06-20, folder dataset active). Superseded = **`_v1.0`** (mod 06-18, đã trong `(KGR) Archived`). → ARCHIVE `_v1.0`.

**3. `(KGR) DTF_CALC_MIS` ← `(KGR) 5. DTF_CALC_MIS` vs `..._v1.0`**
Live = **bản `5.`** (mod 2026-06-19). Superseded = **`_v1.0`** (mod 06-18, đã trong `(KGR) Archived`). → ARCHIVE `_v1.0`.

**4. `(KGR) DTF_ACTUAL_AOP_EXPENSE` ← `(KGR) DF_ACTUAL_AOP_EXPENSE` vs `..._minh`**
Bản chung (folder shared `Data Flow`, mod 06-18) mới hơn bản `_minh` (folder user, mod 06-11) → nếu giữ thì giữ bản chung, archive bản `_minh`. **Nhưng cả hai đều `in_closure: false`** (output chỉ nuôi loạt MONTHLY/AOP không tới workbook) → cả cụm là dead subtree, để REVIEW chờ owner xác nhận BC02-tháng.

**5. `KGR_DS_ACTUAL_AOP_MONTHLY_v2` ← BA producer: `KGR_DF_ACTUAL_AOP_MONTHLY_LK`, `_v3`, `_v2`**
Cả 3 cùng mod 2026-06-11, cùng sinh ra dataset `_v2`, và dataset đó **không tới workbook nào**. Tên dataset là "v2" nhưng không có bằng chứng rõ ràng producer nào là bản chạy theo lịch (LK = "lũy kế"? v3 = mới nhất theo tên?). → **FLAG cần owner xác nhận** (xem mục dưới). Hai bản `v1`/`v1` chuỗi MONTHLY (`KGR_DF_ACTUAL_AOP_MONTHLY_v1` → dataset `_v1` riêng) đã ARCHIVE cao vì cô lập.

**6. `Nganh_Report_Long_#` ← BA producer: `KGR_DF_Nganh_Metrics_v3`, `_v2`, base `KGR_DF_Nganh_Metrics`**
Live = **`_v3`** (mod 2026-06-10, mới nhất, VÀ là producer duy nhất sinh thêm `SPmoi_ng_v3` mà chuỗi Daily dùng). Superseded = **`_v2`** (05-31) và **base** (05-30). → ARCHIVE `_v2` + base (xem FLAG owner — cả ba `in_closure: true` nên cần xác nhận lịch chạy trước khi dọn).

**7. `Daily_Nganh_Report` ← `KGR_DF_Daily_Nganh_Report_m` vs base `KGR_DF_Daily_Nganh_Report`**
Live = **`_m`** (mod 2026-06-04, mới hơn). Superseded = **base** (06-03). → KEEP `_m`, ARCHIVE base (cần owner xác nhận vì cả hai in_closure=true).

**8. `KGR_DTF_CHI_PHI_XUC_TIEN` ← `KGR_DF_Nganh_Cumulative_AsOf` vs `KGR_DF_Group Rate As-Of`**
Bản `Cumulative_AsOf` mới hơn (06-03 vs 05-27). Cả hai output không reachable → cụm REVIEW; nếu giữ thì giữ bản mới, archive `Group Rate As-Of`. Ghi chú: trong enumeration, object id của `Nganh_Cumulative_AsOf` lại là "KGR_DF_Group Rate As-Of_Ngành" và id của `Group Rate As-Of_Ngành` là "...As-Of_Ngành1" — tên hiển thị và id bị lệch, **dễ nhầm khi thao tác** → kiểm tra kỹ object id trước khi di chuyển.

---

## Ghi chú về 2 object kiểu `sequence` (orchestration)

`catalog_enumeration.json` liệt kê 2 object **type = "sequence"**, KHÔNG phải dataflow transform:

- **`BC Thực tế Tháng`** — folder `/@Catalog/shared/(KGR) 1.Implement`, mod 2026-06-17, owner anhdk.
- **`Daily & Summary report`** — folder `/@Catalog/shared/(KGR) 1.Implement`, mod 2026-06-17, owner minhndn.

Đây là **chuỗi điều phối chạy các dataflow theo lịch** (orchestration sequence), không sinh dataset trực tiếp. → **KEEP cả hai.** Quan trọng: chúng chính là nơi xác định flow nào còn "chạy thật theo lịch". Trước khi archive bất kỳ flow `in_closure: true` trùng nào (set #5, #6, #7), **nên mở 2 sequence này để xem flow nào thực sự được gọi** — đó là bằng chứng cuối cùng về bản live.

---

## Danh sách "cần CTO/owner xác nhận" (ambiguous)

1. **Loạt `KGR_DS_ACTUAL_AOP_MONTHLY_v2` (3 producer: LK / v2 / v3)** + toàn bộ subtree nuôi nó (`DF_ACTUAL_AOP_EXPENSE`, `_minh`, `DF_FACT_EXPENSE`, `DF_GRAIN_ACTUAL_AOP`): tất cả `in_closure: false`. Cần xác nhận báo cáo "BC Thực tế Tháng" (BC02 tháng) có còn dùng dataset này không, và producer nào đang chạy theo lịch. Nếu BC02-tháng đã ngừng → archive cả cụm; nếu còn → giữ đúng 1 producer.
2. **Loạt `Nganh_Report_Long_#` (3 producer: Metrics / v2 / v3)**: cả ba `in_closure: true` (cùng sinh dataset đang dùng), nên không thể archive theo reachability đơn thuần. Đề xuất giữ `_v3`, archive `_v2` + base — nhưng **phải xác nhận qua sequence `BC Thực tế Tháng`/`Daily & Summary report`** rằng chỉ `_v3` được gọi.
3. **`Daily_Nganh_Report` (base vs `_m`)**: cả hai in_closure=true. Đề xuất giữ `_m`, archive base — xác nhận sequence gọi bản nào.
4. **Subtree expense tháng** (`DF_ACTUAL_AOP_EXPENSE` / `_minh` / `DF_FACT_EXPENSE` / `DF_GRAIN_ACTUAL_AOP` / `DF_DAILY_SC_CHAIN`): output không tới 4 workbook nhưng mô tả gợi ý báo cáo chi phí/daily đang phát triển hoặc ngoài phạm vi. Hạ REVIEW; xác nhận trước khi dọn.

---

> **Nhắc lại: tài liệu này chỉ KHUYẾN NGHỊ — không tự xóa hay di chuyển bất kỳ dataflow/dataset nào. Mọi thao tác archive thực tế cần owner/CTO duyệt và nên đối chiếu với 2 sequence orchestration để xác nhận bản đang chạy theo lịch.**
