# Subagent — phân vai, prompt template, model & effort

## Nguyên tắc chung (vì sao kiến trúc thế này)
- **Browser là tài nguyên độc quyền của agent chính.** Chrome DevTools MCP có đúng 1 browser; 2 phiên cùng điều khiển → giẫm state, wedge MCP (phải restart server). Subagent vì thế CHỈ làm việc không-browser: đọc file, gọi NSAW MCP, suy luận, viết.
- Subagent cần dữ liệu từ OAC → agent chính fetch trước (REST/executePreview) rồi dán vào prompt.
- Prompt cho subagent phải TỰ CHỨA: subagent không thấy hội thoại, không thấy plan trừ khi bạn dán vào.
- Đừng spawn khi việc < 1 phút tự làm — orchestration có chi phí.

## 1. plan-reviewer (Phase 2)
- **Mục đích:** bắt lỗi thiết kế TRƯỚC khi user thấy plan và trước khi tốn công build. Các lỗi đắt nhất lịch sử dự án đều là lỗi thiết kế: fan-out đa kỳ 4×, inner-join làm plan mất 56%, aggregate Sum trên cột ID.
- **subagent_type:** `general-purpose` · **model:** `sonnet` · effort thấp (1 lượt, không cần tool ngoài Read/Grep).
- **Prompt template:**

```
Bạn là reviewer phản biện thiết kế OAC dataflow. KHÔNG có browser — chỉ đọc file và suy luận.

Đọc knowledge: C:\Project\KGR-OAC-Agents\Dataflow-builder\OAC_DATAFLOW_MASTERY.md (tập trung §5 commit, §7 node config, §13 cột/dataset, §14 golden numbers + bài học fan-out).

PLAN cần phản biện:
<dán toàn bộ plan markdown>

DỮ LIỆU TRINH SÁT (agent chính đã fetch):
<dán kết quả executePreview/metadata liên quan>

Kiểm các lỗi kinh điển, trả về JSON:
1. Fan-out: có filter single-period trước join/aggregate chưa? Join key có grain duy nhất 2 bên không?
2. Join: kiểu join đúng nghĩa nghiệp vụ chưa (full outer cho plan-vs-actual để giữ SKU chỉ-plan/chỉ-actual)? Key cùng kiểu dữ liệu?
3. Aggregate: cột ID/định danh có bị để Sum không (phải Maximum)? Measure nào nên Sum/Max?
4. Cột: tên qualified đúng theo §13? Dấu số (QUANTITY âm)? Cột tháng vs tuần (SL W1..W5)?
5. Verify plan: số expected có nguồn đối chiếu độc lập chưa? Sanity checks đủ chưa?
6. Naming _vN, ADD-only, rủi ro readability.

Trả về: {"issues":[{"severity":"BLOCKER|MAJOR|MINOR","point":"...","fix":"..."}], "ok_points":["..."], "verdict":"APPROVE|REVISE"}
```

- **Xử lý kết quả:** BLOCKER/MAJOR xác đáng → sửa plan. Bất đồng → bạn quyết, ghi lý do vào mục "Ý kiến plan-reviewer" của plan.

## 2. verifier (Phase 5) — BLIND
- **Mục đích:** recompute độc lập để đối chiếu số. **BLIND = không cho xem số builder đã tính** — biết trước đáp án sẽ sinh xu hướng xác nhận (anchor bias), mất giá trị kiểm chứng.
- **subagent_type:** `general-purpose` · **model:** inherit hoặc `sonnet` · effort trung bình.
- **Tool nó dùng:** NSAW MCP (`mcp__nsaw-analytics__get_sfc_report`, `execute_dynamic_query`, `get_pl_by_dimension`...). KHÔNG browser.
- **Prompt template:**

```
Bạn là verifier dữ liệu độc lập. Tính các con số sau từ nguồn NSAW MCP — KHÔNG hỏi lại, KHÔNG có browser.

Câu hỏi (trả số tuyệt đối):
1. Tổng <measure> theo <dimension> kỳ <PERIODNAME/posting period> = ? (liệt kê từng giá trị dimension)
2. <câu hỏi 2...>

Gợi ý tool: get_sfc_report(period=42) cho plan/actual SFC; execute_dynamic_query cho truy vấn tùy biến. May 2026 = posting period 42.

Trả về JSON: {"answers":[{"question":1,"values":{"Water care":...,"Home care":...},"total":...,"source":"tool+params đã dùng"}], "caveats":["..."]}
```

- **Xử lý kết quả:** so bảng số 2 bên. Khớp → ghi vào báo cáo. Lệch → root-cause (xem §14 knowledge: lệch kiểu 713K-vs-586K có thể là scope khác nhau chứ không phải build sai — phải GIẢI THÍCH được, không lờ đi).
- NSAW MCP chết/token hết hạn → fallback: tự đối chiếu bằng executePreview trên raw + golden report; ghi rõ trong báo cáo là verify 1 nguồn.

## 3. kb-updater (Phase 6 — tùy chọn)
- **Mặc định: agent chính TỰ update** (bạn có context findings đầy đủ, edit vài chỗ là xong). Chỉ spawn khi ≥3 findings lớn hoặc cần viết lại cả section.
- **subagent_type:** `general-purpose` · **model:** `sonnet` (cần đọc hiểu cấu trúc file; haiku dễ đặt sai chỗ).
- **Prompt template:**

```
Cập nhật knowledge file C:\Project\KGR-OAC-Agents\Dataflow-builder\OAC_DATAFLOW_MASTERY.md theo đúng quy tắc trong C:\Project\KGR-OAC-Agents\Dataflow-builder\.claude\skills\oac-dataflow-builder\references\kb-update-rules.md (đọc file đó trước).

FINDINGS đã verify cần ghi (mỗi cái: nội dung + bằng chứng + ngày):
<liệt kê findings>

Yêu cầu: edit đúng section, supersede nội dung sai thay vì append trùng, cập nhật changelog. Trả về danh sách edit đã làm (section, trước/sau 1 dòng).
```

## 4. Có dùng Workflow (fan-out lớn) không?
Mặc định KHÔNG — browser là nút cổ chai duy nhất, fan-out không tăng tốc build. Chỉ cân nhắc Workflow khi: audit ≥5 dataflow có sẵn (đọc def qua REST — agent chính fetch hết def trước rồi fan-out phân tích), hoặc user yêu cầu rõ.
