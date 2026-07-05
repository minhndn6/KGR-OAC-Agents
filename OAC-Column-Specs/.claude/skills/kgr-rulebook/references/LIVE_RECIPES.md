# LIVE_RECIPES — Lấy định nghĩa LIVE từ OAC (read-only) + bẫy đã biết

Instance: `https://oaxinst70021-id3pgnmhxlya-0p-bo.analytics.ocp.oraclecloud.com`. User `minhndn@bizin.vn`.
**Mọi REST gọi qua same-origin browser fetch** (MCP `chrome-lineage` → `evaluate_script` trên trang OAC đang mở). **Bash curl bị proxy chặn (exit 56).**

## Auth
- Mở trang OAC bất kỳ (`/ui/dv/?pageid=home`). Nếu redirect IDCS signin → điền `../.secrets/oac.env` (OAC_USER/OAC_PW) **1 LẦN** → Sign In. Lỗi → DỪNG báo owner (ORA-28000, tài khoản dùng chung).
- Header GET: `{authorization:'session', 'x-requested-with':'XMLHttpRequest'}`, `credentials:'include'`. Không cần CSRF cho GET.

## Endpoint (verified)
1. **Workbook model**: `GET /ui/dv/ui/api/v2/projects/json?path=<encodeURIComponent('/@Catalog/shared/(KGR) .../<NAME>')>`
   → `criteria.columns.children[]` (columnID, columnFormula.expr.expression), `views.children[]` (saw:canvas + saw:pluginView), `layouts.children[]`. ⚠ **double-JSON**: khi lưu chuỗi qua evaluate_script filePath, parse 2 lần (`json.loads` rồi nếu `isinstance(str)` loads tiếp).
2. **Dataflow def (NGUỒN CÔNG THỨC CHỈ TIÊU)**: `GET /ui/dv/ui/api/v1/dataflows?dataFlowID=<encodeURIComponent("'owner'.'NAME'")>`
   → `definition.steps[]`: InputDataset (physical_tables/columns), AddColumns (`columns[{name,expression}]` = công thức), Filter, GroupBy, Join, OutputDataset. Đây là nơi đọc a4/a6/a9/... thật.
3. **Số viz (chỉ khi cần verify, cẩn thận)**: `POST /ui/dv/ui/api/v2/data/executeOrPoll` (đọc số render). Hoặc oac-native logical-SQL — XEM BẪY.

## Lưu file & đọc
- evaluate_script `filePath` lưu giá trị return ra file → parse bằng Python (xử lý double-JSON). Đừng đổ JSON lớn vào context.
- Snapshot lưu `work/snapshots_live/` kèm hiểu ngầm timestamp (mtime).

## ⚠️ BẪY (đã trả giá ở pilot)
- **oac-native logical-SQL auto-aggregate cột đo**: `GROUP BY Metric_Code` hay `MAX(Metric_Code)` đều trả 115×k = code_thật(1..24) × số-dòng(~115). → KHÔNG dùng SQL để suy mã/giá trị đo. Chỉ dùng để liệt kê **giá trị dimension** (vd `GROUP BY Metric_Name` ra tên — OK vì cột text).
- **Dữ liệu lũy-kế-theo-AsOfDate**: SUM across nhiều ngày = cộng chồng → quan hệ derived (a9=a4−a5−...) sẽ "không khớp" giả. Verify số phải cố định 1 AsOfDate.
- **Cột tiếng Việt**: oac-native lỗi encoding (nQSError 22078) với TÊN cột tiếng Việt → tránh; đọc số cột Việt qua executeOrPoll.
- **BOM**: cột `﻿Sort_Order` có ký tự BOM ở đầu — chú ý khi tham chiếu.
- **WAF Akamai**: fetch dồn dập có thể 401 HTML → reload + giãn nhịp.
- **Curl proxy chặn** → chỉ browser same-origin fetch.

## Suy ra: nguồn công thức ĐÚNG
Công thức chỉ tiêu/cột = đọc từ **dataflow def** (#2) + **viz expression** (#1). KHÔNG bao giờ suy công thức từ con số logical-SQL.
