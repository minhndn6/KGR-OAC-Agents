# BCDC Adjustment — Hồ sơ bàn giao toàn tập

> **Mục đích file này:** bàn giao TOÀN BỘ hiểu biết về tính năng "điều chỉnh BCDC" (số điều chỉnh nhập từ
> NetSuite → lan lên báo cáo OAC) cho một phiên Claude khác **chạy trên môi trường khác** (container Linux
> cloud, đọc tri thức từ GitHub repo chứ không phải ổ đĩa local Windows).
>
> **Nguyên tắc viết:** thà thừa còn hơn thiếu. Mọi con số, tên object, endpoint, và mọi cái bẫy đã trả giá
> đều được ghi lại. Chỗ nào tôi KHÔNG chắc thì có nhãn `⚠️ CHƯA CHẮC` — đừng coi là sự thật.
>
> **Cập nhật lần cuối:** 2026-08-01, sau khi sửa lỗi NULL-propagation của waterfall.
>
> **Bối cảnh phiên viết ra file này:** Claude Code trên Windows (`C:\Project\KGR-OAC-Agents\`), có MCP
> `oac-native` + 5 profile Chrome đã đăng nhập OAC, đóng vai **orchestrator** điều phối sub-agent.
>
> **🔒 Quy ước số liệu (CLAUDE.md §4):** file này **cố ý KHÔNG ghi số tuyệt đối** (doanh thu, lợi nhuận,
> số tiền điều chỉnh, tỷ trọng kênh). Cần con số thì **lấy live từ OAC**. Lý do: repo có thể ở chế độ
> công khai, và số liệu tài chính không thuộc về tài liệu kỹ thuật.

---

## MỤC LỤC

0. [Tóm tắt 60 giây](#0-tóm-tắt-60-giây)
1. [Bối cảnh nghiệp vụ — vì sao có task này](#1-bối-cảnh-nghiệp-vụ--vì-sao-có-task-này)
2. [Yêu cầu gốc của owner (R0–R5) và các quyết định chốt](#2-yêu-cầu-gốc-của-owner-r0r5-và-các-quyết-định-chốt)
3. [Kiến trúc chốt: hệ cột song song `_DC`](#3-kiến-trúc-chốt-hệ-cột-song-song-_dc)
4. [Bản đồ luồng dữ liệu — flow nào, làm gì, ghi ra dataset nào](#4-bản-đồ-luồng-dữ-liệu--flow-nào-làm-gì-ghi-ra-dataset-nào)
5. [Ngữ nghĩa số học — allowlist, bậc thang, phân bổ](#5-ngữ-nghĩa-số-học--allowlist-bậc-thang-phân-bổ)
6. [Chuỗi waterfall P&L — mã chỉ tiêu và công thức](#6-chuỗi-waterfall-pl--mã-chỉ-tiêu-và-công-thức)
7. [Danh sách object đã sửa](#7-danh-sách-object-đã-sửa)
8. [16 cái bẫy OAC đã trả giá — đọc kỹ phần này nhất](#8-16-cái-bẫy-oac-đã-trả-giá--đọc-kỹ-phần-này-nhất)
9. [Các lỗi đã mắc trong quá trình làm và bài học](#9-các-lỗi-đã-mắc-trong-quá-trình-làm-và-bài-học)
10. [Phương pháp triển khai — cái gì đã giúp kịp go-live](#10-phương-pháp-triển-khai--cái-gì-đã-giúp-kịp-go-live)
11. [Runbook kỹ thuật — REST endpoint, chạy, rollback](#11-runbook-kỹ-thuật--rest-endpoint-chạy-rollback)
12. [Trạng thái hiện tại và việc còn treo](#12-trạng-thái-hiện-tại-và-việc-còn-treo)
13. [Ghi chú riêng cho phiên chạy trên container Linux](#13-ghi-chú-riêng-cho-phiên-chạy-trên-container-linux)

---

## 0. Tóm tắt 60 giây

Tài chính Kangaroo nhập **số điều chỉnh** vào NetSuite (chỉ tiêu nào, bao nhiêu tiền, hiệu lực từ ngày nào).
Số đó chảy về OAC và phải **tự động lan lên** báo cáo tổng hợp hằng ngày (BC01) và dashboard DB01/DB02,
đi **xuyên qua** các công thức lợi nhuận (tức là tính lại cả chuỗi, không phải cộng phẳng vào dòng cuối).

Giải pháp đã chốt và **đã go-live 2026-07-30**: **hệ cột song song hậu tố `_DC`**. Cột cũ giữ nguyên vĩnh
viễn (= bản "trước điều chỉnh"), mọi giá trị đã-điều-chỉnh nằm ở cột mới `*_DC`. Nhờ vậy các nhánh khác
(BC02 báo cáo thực tế, MIS, DB01, nhánh M8 của anh Đ.K.) **cách ly by-construction** — không cần hàng rào
logic nào cả.

14+ object đã sửa. Nghiệm thu: 19 chứng từ nguồn tái lập chính xác, tập đoàn 8/8 khớp, Σ4 ngành = tập đoàn,
quét cạn hàng trăm nghìn ô chỉ đổi đúng tại 2 ngày hiệu lực.

---

## 1. Bối cảnh nghiệp vụ — vì sao có task này

### 1.1 Vấn đề

Báo cáo P&L hằng ngày của KGR có một số dòng chi phí là **ước tính**, không phải số thực tế:

- **CP chiết khấu khuyến mại (CKKM)** — ước tính theo tỷ lệ, nhưng thực tế lệch rất xa (owner nêu ví dụ:
  số thực tế lớn hơn số ước tính nhiều lần).
- **CP lương / nhân viên kinh doanh** — tính theo rate.
- Nhiều dòng khác tính theo `%AOP × doanh thu` hoặc `tiền AOP pro-rata`.

Hệ quả: lợi nhuận trên báo cáo hằng ngày lệch xa thực tế, C-level ra quyết định trên số sai.

### 1.2 Cách nghiệp vụ muốn xử lý

Kế toán/tài chính, sau khi biết số thật (hoặc số sát hơn), sẽ **nhập một bút toán điều chỉnh** trên NetSuite
qua một màn hình riêng: chọn **chỉ tiêu**, nhập **số tiền**, chọn **kỳ/ngày hiệu lực**, và (với CKKM) chọn
**ngành hàng**. Số này phải tự động chảy về OAC và hiện lên báo cáo.

### 1.3 Bối cảnh hệ thống (rất quan trọng để hiểu vì sao thiết kế như thế)

- Báo cáo BC01 là **as-of lũy kế**: mỗi `AsOfDate` là một ảnh chụp lũy kế từ đầu kỳ tới ngày đó. Bảng
  `TD_Report_Long` có ~31 dòng cho mỗi chỉ tiêu trong một tháng (một dòng/ngày), mỗi dòng là **số lũy kế**
  chứ KHÔNG phải số phát sinh trong ngày. → **Cộng dồn qua các AsOfDate là vô nghĩa** (bẫy #12).
- Waterfall lợi nhuận trên BC01 là **dòng nướng sẵn** trong dataset long-format (`TD_Report_Long`,
  `Nganh_Report_Long_#`), KHÔNG phải công thức tính trong workbook. → Muốn delta cascade thì **phải rót
  delta TRONG dataflow**, trước bước tạo các dòng subtotal.
- Có **hai trục phân tích vuông góc nhau**: ngành hàng (CLASS) và kênh/chuỗi. Cùng một delta xuất hiện ở cả
  hai view là ĐÚNG, không được cộng hai lần.
- Một số chỉ tiêu **không đi qua hub** (11/25): a6 rate lương; a7/a8/a15/a16/a17 = `%AOP × DT`;
  a10/a12/a18 = tiền AOP pro-rata; a21 = cổng 21%; adp = 1,5% × DT.

---

## 2. Yêu cầu gốc của owner (R0–R5) và các quyết định chốt

### 2.1 Quy tắc gốc

| Mã | Nội dung |
|---|---|
| **R0** | Delta là **phẳng**: +X thì mọi as-of date từ ngày hiệu lực trở đi đều nhận đủ +X. KHÔNG pro-rata theo ngày, KHÔNG ramp. |
| **R1** | Chi phí bị **trừ** trong công thức → nhập +X làm **giảm** lợi nhuận. |
| **R2** | **ADD-only, revertible.** Không xoá/ghi đè cột cũ. Phải rollback được. |
| **R3** | **Kiểm-0 tuyệt đối**: khi bảng điều chỉnh rỗng, MỌI ô phải khớp bản gốc từng đồng. |
| **R4** | Tỷ lệ phân bổ tính **LIVE** từ dữ liệu, KHÔNG hard-code. |
| **R5** | CKKM nhập **theo từng ngành** (4 giá trị CLASS) rồi roll-up lên tập đoàn. Các chi phí khác nhập **một lần ở cấp tập đoàn** rồi bổ xuống ngành. |

### 2.2 Nhóm A / nhóm B

- **Nhóm A** (CKKM, CP nhân viên KD, Roadshow, Công tác): phải xuống tới **daily theo kênh/chuỗi**, rải theo
  rổ **"Cách-1"** = GT-Water ∪ Delta ∪ chuỗi DMX. *(Lưu ý: DMX nằm TRONG kênh KA — đây là chủ ý thiết kế,
  không phải lỗi.)*
- **Nhóm B** (CP nhân viên BO, Vận chuyển, Bảo hành, Tài chính, Khác, Dự phòng tồn kho): dừng ở
  **Summary + Ngành**, không xuống daily kênh/chuỗi.

### 2.3 Các quyết định owner đã chốt (không được tự ý đổi)

1. **M8 (báo cáo thực tế) đứng riêng** — delta chỉ chạm tầng ước tính.
2. **Chỉ sửa bản POC** của BC01 daily v2; **BC01 v1.1 = GOLDEN** để kiểm-0. (Tương lai POC sẽ thành bản thật.)
3. **BC02 cách ly tuyệt đối** — báo cáo thực tế không được thay đổi.
4. Rổ Cách-1 **giữ nguyên gồm DMX**.
5. Base giữ rule cũ; **delta bổ theo tỷ lệ doanh thu** (quyết định ban đầu — xem 2.4 để biết phần đã sửa).
6. Mã **103 (dự phòng tồn kho) LOẠI khỏi allowlist** — giữ công thức 1,5% × DT.
7. **Backup rồi sửa thẳng vào bản gốc**; clone chỉ để rollback.

### 2.4 Sửa quy tắc phân bổ (owner yêu cầu SAU khi đã build xong vòng 1)

Owner phát hiện quy tắc "bổ tất cả theo doanh thu" là **hiểu sai từ đầu**, và có một **lỗi có sẵn từ
version gốc**:

- **CP nhân viên KD**: khi bổ xuống ngành đang **dùng chung tỷ lệ của tập đoàn** → SAI ngay từ bản gốc,
  phải dùng tỷ lệ riêng của từng ngành.
- **3 nhóm chi phí (XT bán hàng, Nhân viên BO, Thu nhập khác / chi phí khác)**: bổ xuống ngành theo
  **tỷ lệ AOP**, không phải theo doanh thu.
- Các chỉ tiêu còn lại: **vẫn theo doanh thu**.
- **Nguyên tắc bao trùm**: *"mỗi chỉ tiêu giữ đúng rule riêng của nó"*, không áp một rule chung cho tất cả.

### 2.5 Quyết định về mẫu số âm

Ban đầu tôi đề xuất chặn trường hợp mẫu số âm (một ngành có CKKM ra **âm** vì số điều chỉnh lớn hơn số
thực tế của ngành đó). Owner **bác**:

> *"công thức không nhất quán ấy. Tôi nghĩ bạn cứ để công thức nó tuyến tính thôi, âm thì bổ âm, miễn sao
> tổng bổ vào các ngành đúng là được."*

→ **Bài học nghiệp vụ:** owner ưu tiên **tính nhất quán của công thức** hơn là làm đẹp một ô. Số âm là số
thật, cứ để nó âm.

---

## 3. Kiến trúc chốt: hệ cột song song `_DC`

### 3.1 Ý tưởng

Thay vì thêm **dòng** điều chỉnh vào dữ liệu (phương án đầu tiên, đã bị bỏ), ta thêm **cột**:

```
Cột cũ:   a5, a6, a9, a20, a22, a23, Actual_Amount, ...     ← BẤT BIẾN VĨNH VIỄN
Cột mới:  a5_DC, a6_DC, a9_DC, a20_DC, a22_DC, a23_DC, Actual_Amount_DC, ...   ← đã điều chỉnh
```

### 3.2 Vì sao phương án cột thắng phương án dòng

| Rủi ro của phương án DÒNG | Phương án CỘT xử lý thế nào |
|---|---|
| `Cnt_combo` (đếm tổ hợp kỳ×sub×class) bị lệch vì có dòng mới | Không có dòng mới → không lệch |
| Viz bị NULL ở các chiều mà dòng mới không có giá trị | Không phát sinh |
| Phải dựng hàng rào (fence) chặn dòng điều chỉnh rò sang BC02 | Không cần hàng rào — BC02 đọc cột cũ, by-construction là cách ly |
| `GRAIN_1407` dùng input-list tĩnh sẽ không thấy dòng mới | Cột mới cũng không bị input-list tĩnh nhìn thấy → an toàn |

**Đây là quyết định kiến trúc quan trọng nhất của cả dự án.** Nó biến 4 rủi ro thành 0 việc phải làm.

### 3.3 Hệ quả đẹp

- **BC01 v1.1 (không rebind) trở thành bản "trước điều chỉnh" sống mãi** — dùng để đối chiếu bất cứ lúc nào.
- **Rebind viz = công tắc go-live.** Xây xong hết rồi mà chưa rebind thì báo cáo chưa đổi gì. Bật khi owner
  duyệt số.

### 3.4 Bất biến nghiệm thu (I1–I7)

Viết ra **TRƯỚC khi code** trong `VISION_ENDSTATE.md`. Đây là hợp đồng nghiệm thu:

| Mã | Bất biến |
|---|---|
| **I1** | Cột cũ bất biến vĩnh viễn |
| **I2** | Kiểm-0: bảng điều chỉnh rỗng ⇒ `*_DC` == cột cũ từng đồng |
| **I3** | Hiệu số = đúng bằng số điều chỉnh, **bất biến dưới mọi filter** |
| **I4** | As-of phẳng (bậc thang tại ngày hiệu lực) |
| **I5** | Bảo toàn: Σ4 ngành = tập đoàn |
| **I6** | Cách ly: DB01 / BC02 / MIS / M8 không đổi một đồng |
| **I7** | Cascade số học chính xác qua toàn chuỗi waterfall |

---

## 4. Bản đồ luồng dữ liệu — flow nào, làm gì, ghi ra dataset nào

### 4.1 Sơ đồ tổng

```
NetSuite (màn hình nhập điều chỉnh)
   │
   ├─→ DW_NS_X_DIEUCHINH_BC_SUMMARY_HEADER  (bảng ADW)
   └─→ DW_NS_X_DIEUCHINH_BC_SUMMARY_LINES   (bảng ADW)
            │
            └─→ [dataset owner tự tạo] KGR_DIEUCHINH_BC_SUMMARY
                 (đã join sẵn Header + Lines + Augmentation; có Class, StartDate, EndDate)
                      │
                      ▼
            ┌────────────────────────────────┐
            │ N0: KGR_DF_BCDC_ADJUST  (MỚI)  │  chuẩn hoá về long format
            └────────────────────────────────┘
                      │  DS_ADJUST (chuẩn hoá)
        ┌─────────────┼──────────────────────────────┐
        ▼             ▼                              ▼
  ┌───────────┐  ┌──────────────────┐        ┌──────────────────┐
  │ HUB _ĐC   │  │ KGR_DF_TD_       │        │ KGR_DF_Nganh_    │
  │ (CKKM_DC) │  │ Metrics_bk       │        │ Metrics_v3       │
  └───────────┘  └──────────────────┘        └──────────────────┘
        │               │ TD_Report_Long            │ Nganh_Report_Long_#
        │               ▼                            ▼
        │        DF_TD_Report_PNL_Bridge     DF_TD_Report_PNL_Bridge_Nganh
        │               ▼                            ▼
        │        KGR_DF_Daily_TD_Report      KGR_DF_Daily_Nganh_Report_m
        │               └──────────┬─────────────────┘
        ▼                          ▼
   ZZ_SANDBOX_..._BC01_{TD,KENH,CHUOI}_CLASS_v2  →  ..._v3
                                   │
                                   ▼
                   Workbook BC01 POC (rebind 24 cột / 10 viz)
                   Workbook DB02.Expense_v1.1 (rebind 9 cột / 10 viz)
```

### 4.2 Chi tiết từng flow

#### `KGR_DF_BCDC_ADJUST` — **flow MỚI, tầng N0**
- **Namespace:** `'minhndn@bizin.vn'`
- **Việc:** đọc `KGR_DIEUCHINH_BC_SUMMARY`, chuẩn hoá thành long format: một dòng = (kỳ, chỉ tiêu, ngành, số tiền, ngày hiệu lực).
- **Quy mô:** 21 → 25 step.
- **Ngữ nghĩa quan trọng:** kỳ lấy từ `POSTINGPERIOD`. `Eff_Date` = `StartDate`.
- **Output:** dataset điều chỉnh chuẩn hoá (DS_ADJUST).

#### Hub `'anhdk@bizin.vn'.'(KGR) 1. DTF_CALC_INVOICE_MEMO_#_ĐC'`
- **Việc:** hub trung tâm tính toán ở cấp dòng hoá đơn. Ta thêm cột **`CP_CKKM_DC`**.
- **Quy mô:** 76 → 88 step.
- **⚠️ Cực kỳ lưu ý:** đây là flow **của người khác** (anh Đ.K.). Nó đã có sẵn cột `DT_Adjust_Line` /
  `GV_Adjust_Line` phục vụ nhánh M8 — **KHÔNG được đụng vào**.
- **⚠️ Rủi ro có sẵn:** hub dùng chế độ ghi `Create` + `conn` ⇒ **mỗi lần Run là DROP/CREATE bảng, mất 3–4 phút**.
  Trong khoảng đó bảng không tồn tại. Đây là rủi ro có TRƯỚC dự án này.
- Hai viz trên DB02 Overview đọc **THẲNG** hub → CKKM rót ở tầng Metrics sẽ KHÔNG chạm chúng. Đó là lý do
  CKKM phải rót ở hub chứ không chỉ ở Metrics.

#### `KGR_DF_TD_Metrics_bk` → dataset `TD_Report_Long`
- **Việc:** tính toàn bộ 25 chỉ tiêu P&L **cấp tập đoàn**, dạng long-format (một dòng = một chỉ tiêu × một AsOfDate).
- **Quy mô:** 50 → 63 step.
- Thêm `a5_DC..a24_DC` + `Actual_Amount_DC`; waterfall và cổng thuế **được tính lại** trong hệ `_DC`.
- **⚠️ Tên có hậu tố `_bk` nhưng đây LÀ FLOW PRODUCTION.** Đừng nhầm là backup.

#### `KGR_DF_Nganh_Metrics_v3` → dataset `Nganh_Report_Long_#`
- Y hệt trên nhưng **cấp ngành** (theo `ID CLASS`). 49 → 62 step.
- **⚠️** `Nganh_Report_Long_#` **KHÔNG có trong search_catalog** — phải query thẳng bằng tên.

#### `DF_TD_Report_PNL_Bridge` và `DF_TD_Report_PNL_Bridge_Nganh`
- **Việc:** cầu nối, cõng các cột `_DC` sang tầng daily. Chỉ pass-through + đổi hình dạng.

#### `KGR_DF_Daily_TD_Report` và `KGR_DF_Daily_Nganh_Report_m`
- **Việc:** dựng bảng daily cho canvas Summary (tập đoàn / ngành).

#### `ZZ_SANDBOX_20260727__KGR_DF_BC01_{TD,KENH,CHUOI}_CLASS_v2` và `_v3` (6 flow)
- **Việc:** sidecar dựng dòng theo ngành cho canvas daily kênh/chuỗi.
  - `TD_CLASS_v2` = tái tổng hợp từ Daily_TD/Nganh_Report.
  - `KENH_CLASS_v2` / `CHUOI_CLASS_v2` = dựng thẳng từ dòng hub (as-of + rate + dedup + universe có `ID CLASS`).
  - `_v3` = chỉ thay AOP theo class (×1.08).
- **⚠️ Tiền tố `ZZ_SANDBOX_20260727__` gây hiểu nhầm — đây là flow ĐANG DÙNG THẬT** cho POC.
- `KENH/CHUOI_CLASS_*` **KHÔNG phụ thuộc** vào 2 flow Metrics (chúng đọc hub + DS_ADJUST) → khi chỉ sửa
  Metrics thì **không cần chạy lại** chúng.

#### Sequence `Daily & Summary report_v1.1`
- 11 → 18 mục. Item đầu = hub `_ĐC`, item cuối = `DTF_CALC_MIS Ver 5` (MIS **không** ăn hub).
- **KHÔNG có schedule tự động** chạy sequence này — owner chạy tay. *(Thông tin "job 2h/lần" trong tài liệu
  cũ đã lỗi thời.)*

### 4.3 Workbook đã rebind (= công tắc go-live)

| Workbook | Số viz | Số cột đổi sang `_DC` |
|---|---|---|
| BC01 POC (daily v2) | 10 | 24 |
| `DB02.Expense_v1.1` | 10 | 9 |
| DB01 | 0 | 0 (không có viz nào cần đổi) |

---

## 5. Ngữ nghĩa số học — allowlist, bậc thang, phân bổ

### 5.1 Allowlist chỉ tiêu nhận điều chỉnh

```
{5, 6, 7, 8, 10, 12, 15, 16, 17, 18}
```

Mã **103 (dự phòng tồn kho) bị LOẠI** — giữ nguyên công thức 1,5% × doanh thu theo yêu cầu owner.

### 5.2 Bậc thang tại `Eff_Date` (KHÔNG pro-rata)

```
AsOfDate  <  Eff_Date  →  delta = 0
AsOfDate  >=  Eff_Date  →  delta = 100% số điều chỉnh
```

Delta hành xử như một **bút toán ghi vào ngày `Eff_Date`**. Vì `TD_Report_Long` là as-of lũy kế, delta xuất
hiện nguyên vẹn ở mọi ngày từ `Eff_Date` trở đi.

**Hệ quả khi kiểm tra:** nếu bạn cộng `Actual_Amount_DC` qua nhiều AsOfDate thì delta sẽ bị nhân lên bằng
số ngày hiệu lực. Ví dụ tháng 7 có delta hiệu lực từ 29/07 → cộng cả tháng sẽ ra **3× delta** (29, 30, 31).
Đó KHÔNG phải lỗi — đó là do bạn cộng sai chiều.

### 5.3 Quy tắc phân bổ xuống ngành (bản CUỐI, sau sửa mục 2.4)

| Chỉ tiêu | Cách bổ xuống ngành |
|---|---|
| CKKM | **Nhập trực tiếp theo từng ngành** (4 CLASS), không cần bổ |
| CP nhân viên KD | Theo **tỷ lệ riêng của từng ngành** *(sửa lỗi có sẵn: bản gốc dùng chung tỷ lệ tập đoàn)* |
| XT bán hàng, Nhân viên BO, Thu nhập khác / chi phí khác | Theo **tỷ lệ AOP** |
| Các chỉ tiêu còn lại | Theo **tỷ lệ doanh thu** |

Lớp rác `class = 5` và `−99999` **KHÔNG nhận delta**.

### 5.4 Rải xuống kênh/chuỗi (chỉ nhóm A)

Rổ **"Cách-1"** = GT-Water ∪ Delta ∪ chuỗi DMX.
- DMX ⊂ kênh KA, và một mình DMX chiếm **phần lớn** doanh thu.
- Nếu né KA hoàn toàn thì nền rải còn quá nhỏ → không đủ. Vì thế owner chốt **giữ DMX trong rổ**.
  *(Tỷ trọng cụ thể lấy live khi cần — không ghi số vào tài liệu.)*

### 5.5 Hai trục vuông góc — cảnh báo chống cộng đôi

Ngành ⟂ kênh. **Cùng một delta xuất hiện ở cả view ngành lẫn view kênh là ĐÚNG.** Tuyệt đối không cộng
hai view lại với nhau.

Khi tính delta cho cấp ngành, phải cẩn thận: `aX_TĐ` **đã ngậm delta rồi** → phải trừ ra trước khi allocate,
nếu không sẽ cộng đôi.

---

## 6. Chuỗi waterfall P&L — mã chỉ tiêu và công thức

⚠️ Phần này ghi theo hiểu biết tích luỹ; tên chính xác nên verify lại trên dataset.

```
a4  = Lợi nhuận gộp
a5  = CP chiết khấu khuyến mại (CKKM)
a6  = CP lương / nhân viên kinh doanh          (theo rate, không qua hub)
a7  = CP roadshow hội nghị                     (= %AOP × doanh thu)
a8  = CP công tác tiếp khách                   (= %AOP × doanh thu)
a9  = Lợi nhuận gộp Kinh doanh  = a4 − a5 − a6 − a7 − a8
a10 = CP xúc tiến bán hàng                     (tiền AOP pro-rata)
a11 = Lợi nhuận xúc tiến bán hàng
a12 = CP nhân viên BO                          (tiền AOP pro-rata)
a13 = Lợi nhuận nhân viên
a14 = CP quản lý vận hành (tổng của a15..a19)
a15..a19 = vận chuyển / bảo hành / tài chính / khác ...   (%AOP × DT hoặc AOP pro-rata)
a20 = Lợi nhuận quản lý vận hành
a21 = CP dự phòng hoạt động năm trước = CASE WHEN a20 < 0 THEN 0 ELSE a20 * 0.21
a22 = Lợi nhuận trước thuế (LNTT)
a23 = Lợi nhuận sau thuế (LNST) = CASE WHEN a22 > 0 THEN a22 * 0.8 ELSE a22
a24 = Tỷ lệ Xanh/Đỏ                            ← KHÔNG đụng vào
adp = CP dự phòng (trả hàng, thanh lý, huỷ)    = 1,5% × doanh thu
```

### 6.1 ⚠️ Đính chính quan trọng về a21 và thuế

Tôi đã **hiểu sai** và bị owner sửa: `a21` **KHÔNG phải cổng thuế**. Nó là **khoản dự phòng thật** bằng 21%
của lợi nhuận quản lý vận hành (khi dương). Trên báo cáo nó có nhãn **"CP dự phòng (trả hàng, thanh lý, huỷ)"**.

**Thuế thu nhập doanh nghiệp nằm ẩn ở bước LNTT → LNST**: `LNST = 0,8 × LNTT` khi dương (tức thuế 20%),
còn âm thì đi thẳng không kẹp 0. Thuế **không có dòng riêng** trên báo cáo này.

### 6.2 Σ ngành vs tập đoàn vỡ ở dòng #22 trở xuống — by design

Thuế/dự phòng được tính **độc lập cho từng class**, nên `Σ4 ngành ≠ tập đoàn` ở dòng #22 và thuế
(đã đo được một khoản lệch đáng kể ở tháng 6). Đây là **hiện trạng có sẵn**, không phải lỗi của dự án này. Khi đối soát, chỉ so
**từ dòng #21 trở lên**.

---

## 7. Danh sách object đã sửa

| # | Object | Loại | Thay đổi |
|---|---|---|---|
| 1 | `KGR_DF_BCDC_ADJUST` | dataflow (MỚI) | 21 → 25 step |
| 2 | `(KGR) 1. DTF_CALC_INVOICE_MEMO_#_ĐC` | dataflow (của anhdk) | 76 → 88 step, thêm `CP_CKKM_DC` |
| 3 | `KGR_DF_TD_Metrics_bk` | dataflow | 50 → 63 step |
| 4 | `KGR_DF_Nganh_Metrics_v3` | dataflow | 49 → 62 step |
| 5 | `DF_TD_Report_PNL_Bridge` | dataflow | cõng cột `_DC` |
| 6 | `DF_TD_Report_PNL_Bridge_Nganh` | dataflow | cõng cột `_DC` |
| 7 | `KGR_DF_Daily_TD_Report` | dataflow | cõng cột `_DC` |
| 8 | `KGR_DF_Daily_Nganh_Report_m` | dataflow | cõng cột `_DC` |
| 9–14 | `ZZ_SANDBOX_20260727__KGR_DF_BC01_{TD,KENH,CHUOI}_CLASS_{v2,v3}` | dataflow ×6 | sidecar ngành |
| 15 | `Daily & Summary report_v1.1` | sequence | 11 → 18 mục |
| 16 | BC01 POC | workbook | rebind 24 cột / 10 viz |
| 17 | `DB02.Expense_v1.1` | workbook | rebind 9 cột / 10 viz |

**Backup:** `/users/minhndn/BCDC_BACKUP_20260729` (5 object) + toàn bộ file `defs/*__PRE_*.json` ở
`C:\Project\_kgr-state\work\OAC-Orchestrator\defs\` *(ngoài repo — phiên khác KHÔNG đọc được, phải GET lại
định nghĩa từ OAC nếu cần rollback).*

---

## 8. 16 cái bẫy OAC đã trả giá — đọc kỹ phần này nhất

> Đây là phần **giá trị nhất** của tài liệu. Mỗi mục là một lần mất từ vài giờ tới cả ngày.

### 8.1 — Không thêm được step `Branch` MỚI vào flow đã có nhiều diamond
Hub đã có 3 diamond. Thêm `Branch` thứ 4 → **Run fail CÂM giữa pipeline**, log chỉ nói
`"An error occurred, which could not be interpreted"` + `nQSError 43241`.
**Cách sửa:** mắc vào `Branch` CÓ SẴN.
**Cách tìm ra:** 8 thí nghiệm A/B trên output POC riêng. Giả thuyết ban đầu của tôi (trùng cột `CKKM_PER`)
đã bị POC **bác bỏ** (79 cột, 0 trùng) — may mà tôi thử thay vì tin.

### 8.2 — OAC CHẠY ĐƯỢC `CASE` nhiều `WHEN`
Có 12 `WHEN` đang chạy production. Tin đồn "chỉ hỗ trợ 1 WHEN" là **SAI**.

### 8.3 — `SUM(ABS(a − b))` thoái hoá thành `ABS(SUM − SUM)` → **test giả**
OBIS viết lại số học trên measure. `SUM(a*b)` → `SUM(a)*SUM(b)`; `SUM(CASE WHEN ... NULL ...)` được lượng
giá **SAU** khi tổng hợp.
**Cách đúng:** `GROUP BY <grain đầy đủ> HAVING ABS(SUM(x_DC) − SUM(x)) > θ`, θ = 0,01 (cột dẫn xuất có
epsilon float64 ≤ 5e-5 đồng).
**Control test đúng trên long-format = nhân đôi CÙNG một cột**, không so hai cột khác nhau (vì NULL-propagation
sẽ làm phép so im lặng trả về "không lệch").

### 8.4 — Spine `DIM_TIME` phải nằm SAU một bước distinct
Nếu không → Run chết `nQSError 43241` sau ~4 phút.

### 8.5 — `completed: true` xuất hiện NGAY CẢ KHI job đang chạy
Chỉ tin khi `status` ≠ `running`/`reserved` **VÀ** có `executionFinished`.

### 8.6 — Nhiều agent dùng chung tab browser + biến `window.*` = **GHI LẠC OBJECT**
Đã xảy ra thật: payload của hub bị ghi nhầm vào flow Bridge.
**Luật bắt buộc:** tab riêng cho mỗi agent · `select_page` trước mỗi lệnh · biến có tiền tố riêng · script
tự chứa · assert `outputDatasets.datasetName` · so sha256 trước khi PUT.

### 8.7 — `PUT` trả **200** kèm `retryRequestAfterSessionRestore` / `"CSRF mismatch"` = **KHÔNG ghi gì**
Key csrf là `csrftoken`. **Luôn read-back** sau mọi PUT. Đừng tin HTTP 200.

### 8.8 — Kênh đọc dự phòng khi `oac-native` chết: `POST /ui/dv/ui/api/v1/sqlquery/execute`
Dùng cookie session + csrf. Đơn giản hơn `executeOrPoll`.
**⚠️ Ô NULL bị LOẠI khỏi mảng row** làm lệch vị trí phần tử → phải `assert row.length === aColumnTypes.length`.

### 8.9 — `VALIDATION_DATAFLOW_MULTIPLE_SEQUENCE`: OAC validate theo **tiền tố `stepId`**, KHÔNG theo `type`
Đọc được từ chính `report.js` của tenant: validator kiểm `stepId.startsWith("Join")` /
`startsWith("Concatenate")`. Các step tôi đặt tên `BCDC_LJ1` / `BCDC_LJ2` **vô hình** với validator → OAC
báo *"more than one executable flow sequence"* và **chặn Run trong editor**.
**→ Luật: đặt `stepId` BẮT ĐẦU bằng đúng tên type** (`Join…`, `Concatenate…`, `Branch…`).
9 flow bị dính. Bản vá đã dry-run chứng minh (300/300 fail → 0/300) nhưng **owner cho dừng, chưa áp dụng**.

### 8.10 — Thứ tự trong mảng `links[]` quyết định Input 1 / Input 2 trên UI
Triệu chứng: node join báo *"columns used in the join condition could not be resolved"*, và UI hiển thị
Input 1/2 **đảo nhau**.
Giả thuyết đầu của tôi (`inputDatasetOrder`) **SAI** — field đó không tồn tại trong schema này.
**Nguyên nhân thật:** thứ tự hai phần tử link trong `links[]`.
Đã sửa `SP_JMM` và `BC_J1` trong `KENH_CLASS_v2` + `CHUOI_CLASS_v2`.

### 8.11 — NULL lan truyền trong guard `CASE`
Biểu thức:
```sql
CASE WHEN IFNULL("a7_TĐ_DC" - "a7_TĐ", 0) = 0 THEN "a7" ELSE ... END
```
sập về nhánh "không có delta" vì `a7_TĐ` là NULL → phép trừ ra NULL → `IFNULL(NULL,0)=0` → luôn chọn nhánh sai.
**Sửa:** bọc `IFNULL(...,0)` quanh **CẢ HAI toán hạng**, không chỉ quanh kết quả.

### 8.12 — 🔴 Thiếu `GROUP BY AsOfDate` → OAC trả **tổng toàn cục lặp trên mọi dòng**
Số ra **trông hợp lý** nên rất dễ tin. Đây là bẫy đã làm **hỏng một bảng số tôi đã đưa cho owner**: tôi báo
một giá trị cho `a7` tại 29/07 trong khi thực tế ô đó **NULL** — con số đó là lũy kế cuối tháng 6 bị dán
nhãn tháng 7.
**Luật: mọi truy vấn kiểm chứng PHẢI có `GROUP BY` tường minh gồm cả `AsOfDate`/`PERIODNAME`.**
**Luật 2: khi kiểm NULL thì KHÔNG được bọc `IFNULL` trong câu truy vấn** (sẽ mất dấu NULL).

### 8.13 — Ghi workbook: path phải có tiền tố `@Catalog` + body phải có `overwrite: true`
- `?path=/shared/…` (thiếu `@Catalog`) → trả `success:true` + `lastModified` mới **nhưng KHÔNG ghi gì** — no-op im lặng.
  Phân biệt: **no-op** có `featurePermission: null`; **ghi thật** có `featurePermission:{…iPermissionLevel:2}`
  + `reportPath: "@Catalog/shared/…"`.
- Thiếu `overwrite: true` → `success:false` + `errorCode: OBI-01402`.
- `path` nằm ở **query string**, không phải body.
- Key datasources là **`transientOptionalDatasourcesOnSave`**, không phải `datasources`.
- **CỐ Ý BỎ `previousPath`** khi clone — nếu set, OAC có thể hiểu là MOVE và **dời mất workbook production**.

### 8.14 — Object mồi nhử (decoy) cùng tên ở thư mục khác
Một agent QA báo *"0/17 workbook dùng `_DC`"* → hoảng. Thực ra nó đã soi nhầm: một POC cùng tên ở My Folders
(bind `CLASS_v1`) và một `DB02.Expense_v1.1` **trùng tên** ở `/shared/(KGR) 1.Implement/`.
Kiểm live: POC có 30 tham chiếu `_DC`, DB02 có 11.
**Luật: định danh object bằng ĐƯỜNG DẪN ĐẦY ĐỦ + thời điểm sửa, không bằng tên.**

### 8.15 — Phải sửa cả `expression` LẪN `srcexpression`
Mỗi biểu thức trong definition dataflow tồn tại ở hai trường. Sửa thiếu một cái → UI và engine bất đồng bộ,
hỏng im lặng.

### 8.16 — Chế độ ghi của step "Save Data": `Create` / `Append` / `Replace`
- Một lần cấu hình nhầm `Append` → Run **nhân đôi toàn bộ dữ liệu** (số dòng gấp đúng 2 lần).
- Tôi hướng dẫn dùng `Replace`; agent **phản biện đúng** và dùng `Create` (không flow nào trong project dùng
  `Replace`; bản backup không đụng tới cũng dùng `Create`).
- **🔴 Nguy hiểm nhất:** flow backup `_minh_bk` vẫn **trỏ vào dataset PRODUCTION** với mode `Create` — chỉ
  cần chạy một lần là **xoá bảng production**. Đã repoint sang `ZZ_BK_MINH_OUT` trước khi chạy.
  **→ Luật: trước khi Run BẤT KỲ flow backup nào, kiểm `outputDatasets.datasetName` trỏ đi đâu.**

### 8.17 (bổ sung) — Các bẫy nhỏ khác
- Dataflow thêm cột → dataset embed **không tự thấy** (`nQSError 22078`). "Reload Data" bị từ chối với
  flow-generated dataset. Phải mở **Prepare editor → tab bảng fact → Edit Definition → OK → Save**.
- MCP `/api/mcp` thiếu `charset=UTF-8` → OAC (Java) mặc định ISO-8859-1 → **mangle tên cột tiếng Việt**
  (query rỗng âm thầm).
- `<saw:filter>` trong `executeOrPoll` bị **BỎ QUA IM LẶNG** → phải dùng `FILTER(... USING ...)`.
- Blend giữa dataset lưu bằng con trỏ `conformsToColumn` trên **từng cột** (gieo theo TÊN CỘT) →
  **đổi tên cột = blend chết im lặng**, số phồng thành tổng-không-lọc. Không nằm trong workbook JSON nên
  backup workbook **không cứu được**.
- `Metric_Code` trong `TD_Report_Long` bị SUM (code hiển thị = code thật × số ngày) → **khoá theo `Metric_Name`**.
- Lọc phải dùng cột **ATTRIBUTE**, không dùng measure.
- DV cấm calc tham chiếu calc → phải inline hết.
- `@parameter("tên")(0)` — thiếu default `(0)` sẽ báo "syntax error" giả và rớt cột.

---

## 9. Các lỗi đã mắc trong quá trình làm và bài học

> Ghi thẳng, kể cả những lỗi làm mất mặt. Đây là phần hữu ích nhất cho phiên sau.

### 9.1 Chiến lược đầu tiên bị owner bác: *"chưa đủ sâu"*
Tôi trình chiến lược v1 có câu *"tôi cần đọc definition mới xác nhận được"*. Owner bác thẳng:
> *"Nhận định này của bạn nghĩa là bạn chưa check đúng gốc rễ. Tôi cần bạn đánh giá sâu nhất có thể, lường
> trước mọi vấn đề rồi mới ra được chiến lược đúng. Không phải vội đâu, bạn cứ làm cho kĩ đi nhé."*

**Bài học:** với owner này, **"tôi đoán" là không chấp nhận được**. Phải fetch definition thật (đã fetch 24
definition), chạy các đợt phân tích sâu, rồi mới đề xuất. Chiến lược v2 được duyệt.

### 9.2 Tin vào giả thuyết của chính mình thay vì thử nghiệm
- Hub Run fail 3 lần → tôi khẳng định do trùng cột `CKKM_PER`. **POC bác bỏ** (79 cột, 0 trùng).
- Node join lỗi → tôi khẳng định do `inputDatasetOrder`. **Field đó không tồn tại.**
- a7 delta = 0 → tôi khẳng định do thiếu cột. **Thực ra là NULL-propagation.**
- Run hay fail → tôi khẳng định *"chạy đơn thì được, chạy trong sequence thì fail"*. **Lịch sử Run bác bỏ**:
  fail 46% bất kể cách gọi.

**Bài học:** mọi giả thuyết phải có **thí nghiệm A/B** trước khi tuyên bố. Tỷ lệ tôi đoán đúng ở dự án này
thấp đến mức đáng báo động.

### 9.3 🔴 Đưa cho owner một bảng số SAI
Bảng 25 chỉ tiêu tháng 7 tôi gửi owner có một giá trị cho `a7`. Thực tế ô đó **NULL** — con số đó là lũy kế
cuối tháng 6 bị truy vấn thiếu `GROUP BY` dán nhầm nhãn.
Điều tệ nhất: **bẫy này chính tôi đã ghi vào danh sách cảnh báo từ trước** mà vẫn để lọt.

**Bài học:** danh sách cảnh báo vô dụng nếu không có **quy trình bắt buộc** áp nó vào mọi truy vấn. Từ đó
mọi brief giao cho sub-agent đều có mục "BẪY BẮT BUỘC" liệt kê cụ thể, không để agent tự nhớ.

### 9.4 Tin kết luận PASS của sub-agent
Một agent báo *"0/17 workbook dùng `_DC`"* — sai vì soi nhầm object mồi nhử. Nếu tin thì đã rollback nhầm
cả dự án.

**Bài học:** kết luận của sub-agent là **giả thuyết**, không phải sự thật. Kết luận gây sốc phải verify độc lập.

### 9.5 Hiểu sai nghiệp vụ và bị owner sửa
Tôi gọi `a21` là "cổng thuế". Owner sửa: đó là **dự phòng thật**, thuế nằm ẩn ở LNTT→LNST.

**Bài học:** đừng suy diễn ngữ nghĩa nghiệp vụ từ hình dạng công thức. Hỏi.

### 9.6 Đề xuất "làm đẹp số" bị bác
Tôi đề xuất chặn mẫu số âm cho Sanitary. Owner bác vì làm công thức mất nhất quán.

**Bài học:** ưu tiên **nhất quán** và **trung thực với số liệu** hơn là né một ô xấu.

### 9.7 Sự cố hạ tầng đã gặp (để phiên sau biết mà phòng)
- Mất điện máy giữa lúc PUT → phải verify xem đã commit gì chưa (may là chưa).
- Lỗi API 500/529 lặp lại; session OAC hết hạn giữa chừng; MCP `oac-native` mất token.
- Chạm **giới hạn chi tiêu tháng** của tài khoản → sub-agent bị giết giữa chừng.
  **→ Luật: agent phải ghi tiến độ ra file sau MỖI bước** để nối tiếp được thay vì làm lại từ đầu.
- Classifier chặn một số thao tác (Agent/Write/ScheduleWakeup) → cần đường vòng.

---

## 10. Phương pháp triển khai — cái gì đã giúp kịp go-live

### 10.1 Hình dung kết quả cuối TRƯỚC khi thiết kế
Owner yêu cầu thẳng:
> *"trước khi làm bạn phải suy nghĩ và hình dung được kết quả cuối cùng của bạn sẽ là như thế nào"*

→ Sinh ra `VISION_ENDSTATE.md`: mô tả trạng thái đích + **7 bất biến I1–I7** làm hợp đồng nghiệm thu, viết
**trước** khi code một dòng. Mọi tranh cãi sau đó đều quy chiếu về file này. **Đây là việc có ROI cao nhất
của cả dự án.**

### 10.2 Vai trò orchestrator — không tự nhúng tay
Owner yêu cầu rõ:
> *"tôi vẫn cần nhiều sub-agents, không muốn bạn tự tay kiểm vì như thế bạn sẽ bị tràn context, không minh
> mẫn, bạn cứ gọi sub-agents đi, bạn điều phối là được"*

**Cách làm hiệu quả:**
- Main giữ context sạch: chỉ nhận **kết luận + bằng chứng**, không nhận file dump.
- Mỗi brief giao sub-agent gồm 6 phần cố định: **Mục tiêu · Quy trình · Verify (liệt kê từng mục) · Bẫy bắt
  buộc · Định dạng báo cáo · Ủy quyền**.
- Mục "**Bẫy bắt buộc**" là quan trọng nhất — chép các bẫy ở §8 liên quan vào từng brief. Không để agent tự nhớ.
- Chọn model theo độ rủi ro: việc cơ học → model gọn; việc đụng công thức P&L production → model mạnh.
  Một lần sửa sai công thức đắt hơn nhiều lần chênh lệch token.

### 10.3 Gate theo pha
`plan → design → task chi tiết → test case → GATE → build → test kỹ → QA độc lập → GATE`

Không nhảy pha. Mỗi gate owner duyệt.

### 10.4 QA kiểu "golden-first" (rút ra từ lần kiểm điểm trước)
5 luật bắt buộc:
1. **Đối chiếu golden trước** — diff từng ô với bản golden, không tự dựng mốc nội bộ rồi tự khen.
2. **Quét cạn, không lấy mẫu.** (Đã quét 101.950 / 113.511 / 176.142 ô qua các vòng.)
3. **Render tươi rồi mới báo** — tránh cache cũ.
4. **Lệch thì báo TRƯỚC**, đừng chờ đủ đẹp mới báo.
5. **3 bằng chứng** cho mỗi kết luận.

### 10.5 Control test — chứng minh phép so không thoái hoá
Mọi phép so "không lệch" đều **vô giá trị** nếu phép so bị hỏng. Vì thế mỗi lần kiểm phải kèm một **control
test** cố ý tạo lệch (nhân đôi cùng một cột) để chứng minh phép so **có khả năng** phát hiện lệch.
Đây là thứ đã cứu tôi khỏi vài lần "PASS giả".

### 10.6 Chụp PRE/POST cho mọi object trước khi sửa
Trước mỗi PUT: `GET` định nghĩa → lưu `<tên>__PRE_<việc>.json`. Sau PUT: `GET` lại → **diff phải bằng 0**
so với bản dựng offline. Rollback = PUT lại phần `definition` của file PRE.
**Đã diễn tập rollback hai chiều** để chứng minh nó thật sự chạy — không chỉ nói suông.

### 10.7 Tự-diff trước khi PUT
Trước khi ghi, agent phải tự chứng minh: *"đúng N giá trị đổi, 0 thay đổi ngoài trường dự kiến, số step /
`stepId` / `links` y nguyên"*. Với lần sửa IFNULL còn thêm một bước hay: **gỡ hết `IFNULL(x,0)` ra thì POST
phải ≡ PRE** — chứng minh chỉ bọc chứ không viết lại logic.

### 10.8 Thí nghiệm A/B để tìm nguyên nhân gốc
Khi hub fail câm: dựng POC output riêng, chạy **8 biến thể A/B**, cô lập được nguyên nhân (`Branch` mới).
Không đoán — thử.

### 10.9 Đọc mã nguồn của chính tenant khi tài liệu không có
Lỗi *"more than one executable flow sequence"* không có tài liệu nào giải thích. Tôi **đọc `report.js` của
tenant** và tìm ra validator kiểm `stepId.startsWith(...)`. Cách này cũng dùng để crack hợp đồng save
workbook (đọc `_handleSaveReport` trong `report_base.js`).
**→ Khi API im lặng, đọc bundle JS của OAC.**

### 10.10 Test theo yêu cầu owner (tiết kiệm mà vẫn đủ)
> *"mỗi tháng bạn lấy khoảng 3 ngày thôi, trong đó có ít nhất 1 ngày chủ nhật. Tập trung tháng 5, tháng 7."*
> *"nhớ kiểm cả khi áp filter Ngành Hàng hoặc As of Date nữa nhé"*

Các lỗi owner **cho phép bỏ qua** khi filter ngành: báo cáo cấp tập đoàn vẫn hiện số; lọc 1 ngành thì 3
ngành còn lại báo "no data".

---

## 11. Runbook kỹ thuật — REST endpoint, chạy, rollback

### 11.1 Dataflow

```
# ĐỌC định nghĩa
GET  /ui/dv/ui/api/v1/dataflows?dataFlowID=<encodeURIComponent("'ns'.'tên'")>

# GHI định nghĩa  — body là {definition} TRẦN, không bọc envelope (bọc → 500)
PUT  /ui/dv/ui/api/v1/dataflows?dataFlowID=<enc>
     body: {"definition": { ... }}
     header: x-csrf-token, x-bitech-clientbin
     folderPath RỖNG, skipAutoML=false

# CHẠY
POST /ui/dv/ui/api/v1/dataflows/run?dataFlowID=<enc>
     body: {}
     (ID ở query-string, KHÔNG base64)

# TRẠNG THÁI JOB
GET  /dataload/jobs/dataflow?limit=50        → key "jobs"
GET  /dataload/job/<runId>/log
GET  /dataload/job/<runId>/task/<taskId>/log  ← log THẬT ở đây
```

### 11.2 Sequence
```
GET /ui/dv/ui/api/v1/sequences     (trả kèm definition)
PUT /ui/dv/ui/api/v1/sequences
```

### 11.3 Workbook
```
GET  /ui/dv/ui/api/v2/items?&searchAttribute=replication%3Dfalse&path=<enc>&projectType=auto&{}
     → representation.json là CHUỖI JSON (phải JSON.parse lần nữa)

POST /ui/dv/ui/api/v2/projects/json?path=<enc ĐƯỜNG DẪN ĐÍCH, PHẢI có /@Catalog/...>
     body: {name, tags:[''], description, overwrite: true,
            reportSaveInfo:{lastModifiedUserName, lastModifiedTimestamp},
            json: <chuỗi JSON workbook>,
            transientOptionalDatasourcesOnSave: JSON.stringify(datasources)}
```

### 11.4 Lấy csrf token (không cần owner dán tay)
```
GET /ui/dv/ui/api/v1/sessioninfo/ext?stateId=193   → field `csrftoken`
```
Chạy trong trang OAC đã đăng nhập là lấy được.

### 11.5 Kênh đọc số liệu (theo thứ tự ưu tiên)
1. **MCP `oac-native`** — `oracle_analytics-execute_logical_sql` / `-describe_data` / `-search_catalog`.
2. `POST /ui/dv/ui/api/v1/sqlquery/execute` (cookie + csrf) — ⚠️ ô NULL bị loại khỏi mảng row.
3. `POST /api/mcp` (JSON-RPC nội bộ, chạy bằng cookie phiên) — cần header `Mcp-Session-Id` từ `initialize`.
4. `executeOrPoll` — ⚠️ `<saw:filter>` bị bỏ qua im lặng, phải dùng `FILTER(... USING ...)`.

**⛔ CẤM tuyệt đối MCP `nsaw-oac-poc`** (deprecated, owner cấm).

### 11.6 Thứ tự chạy lại sau khi sửa 2 flow Metrics
```
KGR_DF_TD_Metrics_bk
  → KGR_DF_Nganh_Metrics_v3
    → DF_TD_Report_PNL_Bridge
      → DF_TD_Report_PNL_Bridge_Nganh
        → KGR_DF_Daily_TD_Report
          → KGR_DF_Daily_Nganh_Report_m
            → ZZ_SANDBOX_20260727__KGR_DF_BC01_TD_CLASS_v2
              → ZZ_SANDBOX_20260727__KGR_DF_BC01_TD_CLASS_v3
```
**Chạy tuần tự, không song song.** `KENH/CHUOI_CLASS_*` không phụ thuộc Metrics → không cần chạy.

### 11.7 Rollback
`PUT` lại phần `definition` của file `<tên>__PRE_*.json`, rồi chạy lại flow. Đã diễn tập hai chiều.

---

## 12. Trạng thái hiện tại và việc còn treo

### 12.1 Đã xong và đã verify
- Tính năng điều chỉnh **go-live 2026-07-30**.
- 19 chứng từ nguồn tái lập chính xác; tập đoàn 8/8 khớp; Σ4 ngành = tập đoàn.
- Bậc thang chính xác tại `Eff_Date`; quét cạn chỉ đổi đúng tại 31/05 và 29/07.
- Cách ly BC02 / DB01 / MIS / M8 đã xác nhận.
- **2026-08-01: sửa NULL-propagation của waterfall** — bọc `IFNULL(...,0)` cho 38 vị trí mỗi flow, trên cả
  `TD_Metrics_bk` và `Nganh_Metrics_v3`, cả hệ cột cũ lẫn `_DC`. Lý do: tháng 7 có `a7`/`a8` NULL (owner cho
  biết 2 chi phí này đã gộp vào "chi phí khác") làm **toàn bộ waterfall lợi nhuận tháng 7 trống**. Sau sửa:
  tháng 7 có số ở 31/31 ngày và cả 4 ngành; tháng 3/5/6 khớp từng đồng (300/300 ô, 0 lệch).

### 12.2 Owner đã quyết "để nguyên"
- **Tháng 4**: có 8 dòng chi phí trống (không chỉ 2) → sau khi bọc IFNULL, lợi nhuận tháng 4 hiện số tính
  như thể 8 dòng đó = 0, **có thể lạc quan hơn thực tế**. Owner: *"tháng 4 thì số lung tung lắm, cũng kệ đi."*
- **`ID CLASS = 6`** chỉ xuất hiện 29–31/07: **là ngành mới**, tháng 7 chưa cần. Owner: *"Cứ kệ nó thế thôi."*

### 12.3 Còn treo — cần xử lý ở phiên sau

| # | Việc | Trạng thái |
|---|---|---|
| 1 | **Khoản điều chỉnh cho "CP roadshow hội nghị" tháng 7** | Mâu thuẫn chưa giải: nếu chỉ tiêu này đã bị bỏ/gộp vào "chi phí khác" thì khoản điều chỉnh đang nhập vào **dòng không còn tồn tại**. Owner đã ghi nhận, tạm chưa xử lý |
| 2 | **Đổi tên `stepId` cho 9 flow** (bẫy §8.9) | Đã dry-run chứng minh (300/300 fail → 0/300) nhưng **owner cho dừng**, chưa áp dụng |
| 3 | **Canvas liệt kê delta** (bảng các khoản điều chỉnh, lọc theo ngành/ngày) | Owner để **ưu tiên thấp nhất**, đã hoãn |
| 4 | **`%GP Ròng` trên DB01** | Owner chọn phương án **chỉ ghi chú (disclosure)**, việc sửa ratio-of-sums hoãn sang sprint sau. Lưu ý Notes mặc định ẩn |
| 5 | **Run fail ngẫu nhiên ~25–46%** (`errorCode 9999`, *"An error occurred, which could not be interpreted"*) | **CHƯA GIẢI ĐƯỢC.** Đã loại trừ: dựng lại object mới vẫn fail cùng tỷ lệ; sửa `stepId`/metadata không hết. **Khuyến nghị: mở Oracle Service Request** kèm job ID tái lập được |
| 6 | **Chụp G0 baseline mới** | Apr/Jun trôi do restate thượng nguồn 23→30/07, **KHÔNG do BCDC** (đã chứng minh 3 lớp) |
| 7 | `LN_GOP_KD_DC` lệch 0,01đ ở 1 ô | Do lưu 2 chữ số thập phân — thuần thẩm mỹ |

### 12.4 Rủi ro tồn tại cần biết
- Hub dùng `Create` + `conn` ⇒ mỗi Run **DROP/CREATE bảng 3–4 phút** — cửa sổ bảng không tồn tại.
- Blend lưu bằng `conformsToColumn` theo **tên cột** → đổi tên cột làm blend **chết im lặng**, và backup
  workbook **không cứu được**.
- `KGR_DIEUCHINH_BC_SUMMARY` là dataset **owner tự tạo** — nếu owner sửa cấu trúc, N0 có thể vỡ.

---

## 13. Ghi chú riêng cho phiên chạy trên container Linux

Phiên nhận bàn giao chạy trong **container Linux ephemeral trên cloud**, không phải máy Windows. Những điều
chỉnh cần thiết:

### 13.1 Cái gì KHÔNG dùng được
- ❌ **MCP `chrome-lineage[1-5]`** — cấu hình trỏ đường dẫn Windows, và không có Chrome ở
  `/opt/google/chrome/chrome`. Dùng **Playwright trực tiếp** qua Bash.
- ❌ **MCP `oac-native`** — token nằm ở `C:\Project\OAC-MCP\tokens.json` trên máy owner. Container không có.
  → **Thay bằng `page.evaluate(fetch(...))`** trong trang OAC đã nạp cookie: mọi endpoint ở §11 đều gọi được
  theo cách này vì cookie phiên đã đủ auth.
- ❌ **Mọi đường dẫn `C:\Project\_kgr-state\...`** — các file `defs/*.json`, `VISION_ENDSTATE.md`,
  `TEST_SUITE.md`, `ROLLBACK_PLAN.md` **nằm NGOÀI repo** nên KHÔNG có trên GitHub. Nếu cần rollback,
  phải `GET` lại định nghĩa từ OAC.
- ❌ **Tool `Write`/`Edit`** có thể bị hook chặn (hook gọi bằng đường dẫn Windows `\`). Ghi file bằng
  bash heredoc: `cat > file <<'EOF'`.

### 13.2 Cái gì DÙNG ĐƯỢC nguyên vẹn
- ✅ **Toàn bộ §11 (REST endpoint)** — độc lập môi trường, chỉ cần cookie phiên hợp lệ.
- ✅ **Toàn bộ §8 (các bẫy)** — đặc tính của OAC, không phải của máy.
- ✅ **Toàn bộ §5, §6 (ngữ nghĩa số học)**.
- ✅ **Toàn bộ §10 (phương pháp)**.

### 13.3 Ràng buộc cookie (rất quan trọng)
Cookie OAC **hết hạn ~1 tiếng và xoay vòng sau mỗi lần dùng**.
→ **Phải nạp cookie tươi RỒI làm trọn thao tác trong CÙNG MỘT lần chạy script.** Nạp ở script A rồi mở lại
ở script B sẽ bị đá về màn hình đăng nhập.
→ Với các việc dài (Run dataflow 3–4 phút), thiết kế script **một mạch**: nạp cookie → làm hết → báo cáo.

### 13.4 Quy tắc write-authority vẫn áp dụng
Theo `CLAUDE.md §0`: mặc định **KHÔNG tự lái browser ghi production**. Chỉ ghi khi owner ra tín hiệu override
rõ ràng — cụm khoá **`#GHI-THẲNG`** trong đúng lệnh đó. Lệnh mơ hồ ("cứ làm đi") **không tính**.
Ghi thì bắt buộc: **backup trước → verify sau → báo cáo**.
Object test đặt tiền tố **`ZZ_SANDBOX_CLAUDE_TEST_*`**.

### 13.5 Bảo mật cookie
Cookie phiên OAC là **credential sống** — ai có là dùng được OAC dưới danh nghĩa owner tới khi hết hạn.
Lưu ở scratchpad quyền 600, **ngoài cây repo**, và **tuyệt đối không commit**.

---

## PHỤ LỤC A — Bảng tra nhanh "đừng làm điều này"

| Đừng | Vì |
|---|---|
| Đừng tin `success: true` / HTTP 200 | Có ít nhất 3 dạng no-op im lặng (§8.7, §8.13) |
| Đừng tin `completed: true` | Xuất hiện cả khi đang chạy (§8.5) |
| Đừng dùng `SUM(ABS(a−b))` để kiểm lệch | Thoái hoá thành test giả (§8.3) |
| Đừng truy vấn thiếu `GROUP BY AsOfDate` | Trả tổng toàn cục, số trông đúng mà sai (§8.12) |
| Đừng bọc `IFNULL` khi đang đi tìm NULL | Mất dấu cái mình cần tìm (§8.12) |
| Đừng định danh object bằng tên | Có object mồi nhử trùng tên (§8.14) |
| Đừng thêm step `Branch` mới vào flow nhiều diamond | Fail câm (§8.1) |
| Đừng đặt `stepId` không bắt đầu bằng tên type | Validator OAC không thấy → chặn Run (§8.9) |
| Đừng Run flow backup mà chưa kiểm output trỏ đâu | Có thể xoá bảng production (§8.16) |
| Đừng đổi tên cột dataset | Blend chết im lặng, backup workbook không cứu được |
| Đừng sửa `expression` mà quên `srcexpression` | Hỏng im lặng (§8.15) |
| Đừng cộng dồn as-of qua nhiều ngày | Lũy kế × số ngày (§5.2) |
| Đừng cộng view ngành với view kênh | Hai trục vuông góc (§5.5) |
| Đừng dùng MCP `nsaw-oac-poc` | Owner cấm |
| Đừng tin kết luận sub-agent mà không verify | Đã có tiền lệ báo động giả (§9.4) |

## PHỤ LỤC B — Câu chốt về phương pháp

Ba thứ tạo khác biệt lớn nhất ở dự án này:

1. **Viết `VISION_ENDSTATE` + bất biến TRƯỚC khi code.** Mọi tranh cãi sau đó chỉ mất 1 phút vì có chỗ quy chiếu.
2. **Control test trong mọi phép kiểm.** "Không lệch" là vô nghĩa nếu chưa chứng minh phép so **có thể** phát
   hiện lệch.
3. **Chép danh sách bẫy vào từng brief giao việc.** Trí nhớ không chống được bẫy; quy trình thì có.

Và một điều về thái độ: ở dự án này **tỷ lệ giả thuyết của tôi đúng thấp một cách đáng báo động** (§9.2).
Cái cứu được kết quả không phải là đoán giỏi, mà là **chịu khó thí nghiệm và chịu khó nhận sai sớm**.
