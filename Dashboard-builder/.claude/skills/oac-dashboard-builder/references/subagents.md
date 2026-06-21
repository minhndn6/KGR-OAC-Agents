# Subagent — phân vai, prompt template, model & effort

## Nguyên tắc chung (vì sao kiến trúc thế này)
- **Browser là tài nguyên ĐỘC QUYỀN của agent chính.** Chrome DevTools MCP có đúng 1 browser; 2 phiên cùng điều khiển → giẫm state, wedge MCP (phải restart server). Subagent CHỈ làm việc không-browser: đọc file, gọi NSAW MCP, suy luận, viết.
- Subagent cần dữ liệu từ OAC → agent chính fetch trước (executeOrPoll/projects/json/executePreview) rồi dán vào prompt.
- Prompt subagent phải TỰ CHỨA: subagent không thấy hội thoại/plan trừ khi bạn dán vào.
- Đừng spawn khi việc < 1 phút tự làm — orchestration có chi phí.

## 1. plan-reviewer (Phase 2)
- **Mục đích:** bắt lỗi thiết kế TRƯỚC khi user thấy plan + trước khi tốn công build. Lỗi đắt nhất: loại viz sai (2 chart riêng thay vì 1 combo plan-vs-actual), số fan-out đa kỳ (actual nổ 2–5×), plan màu cam thay xám, %GP 0.27 thay 27%, title hardcode số.
- **subagent_type:** `general-purpose` · **model:** `sonnet` · effort thấp (1 lượt, chỉ Read/Grep).
- **Prompt template:**
```
Bạn là reviewer phản biện thiết kế dashboard OAC cho Kangaroo (C-level). KHÔNG browser — chỉ đọc file + suy luận.
Đọc knowledge: C:\Project\KGR-OAC-Agents\Dashboard-builder\OAC_DASHBOARD_MASTERY.md (tập trung §5 taxonomy viz + map use-case, §7 number format, §8 màu, §9 filter grain, §15 quy ước; §13b số tham chiếu + dataset/grain + 5 bậc chẩn đoán số sai).

PLAN cần phản biện:
<dán toàn bộ plan markdown>
DỮ LIỆU TRINH SÁT (agent chính đã fetch):
<dán số executeOrPoll/NSAW/projects-json liên quan>

Kiểm, trả JSON:
1. Decision-value: viz này trả lời câu hỏi điều hành gì? có hàm ý hành động? hay chart-junk/thừa? (≤6 KPI/canvas)
2. Loại viz ĐÚNG cho thông điệp chưa? (plan-vs-actual→Combo 1 viz 2 measure KHÔNG phải 2 chart; cơ cấu+biên→Treemap; gap→Waterfall; mật độ 2 chiều→Grid Heat Map; %đạt→Gauge/Liquid Fill).
3. Shelf mapping đúng? (measure→Values, dim→Category; Treemap size+color; Scatter X/Y/size/color). Grain dataset có hỗ trợ chiều X/color không? (vd MEMO# KHÔNG có Kênh).
4. Số expected có nguồn đối chiếu độc lập? Statistical honesty: baseline 0? ratio vỡ (denominator nhỏ)? AOP grain TĐ(LOAI 5)≠Σngành(LOAI 4)? Xanh/Đỏ denominator? double-count GP? mâu thuẫn viz khác trên cùng workbook?
5. Branding: màu Kangaroo (#44BA46 actual/#636466 plan/#F16522 cost)? Title English? Number format M/%? Note VN?
6. No-hardcode, ADD-only, canvas trống cho viz mới, rủi ro readability (MEMO# intermittent).

Trả: {"issues":[{"severity":"BLOCKER|MAJOR|MINOR","point":"...","fix":"..."}], "ok_points":["..."], "verdict":"APPROVE|REVISE"}
```
- **Xử lý:** BLOCKER/MAJOR xác đáng → sửa plan. Bất đồng → bạn quyết, ghi lý do vào mục "Ý kiến plan-reviewer".

## 2. data-crosscheck (Phase 5) — BLIND
- **Mục đích:** recompute độc lập đối chiếu số viz. **BLIND = không cho xem số bạn đọc từ viz** (anchor bias). Tái dùng tinh thần skill `oac-data-crosscheck`.
- **subagent_type:** `general-purpose` · **model:** `sonnet` · effort TB.
- **Tool:** NSAW MCP (`mcp__nsaw-analytics__get_pl_by_dimension`, `get_sfc_report`, `execute_dynamic_query`, `get_data_dictionary`); `nsaw-oac-poc` (`oac_run_logical_sql`). KHÔNG browser.
- **Canonical facts (đưa vào prompt, đừng để nó re-derive):** May 2026 = posting_period_id **42** (Mar=39,Apr=40). Revenue = `SUM(NVL(BASE_CREDITAMOUNT,0)-NVL(BASE_DEBITAMOUNT,0))` trên DW_NS_CUSTOMER_INVOICE_LINES_F, POSTING='T', TYPE IN(CustInvc,CustCred), Income, **exclude internal customer (Sales Channel ID=14)**. AOP keyed CUSTBODY_SCV_AOP_LOAI_BAO_CAO (Summary=2,3; Daily TĐ=5; Daily Ngành=4; **TĐ≠Σngành by design**). SFC item-level (POSTINGPERIOD+ITEM). Tỷ trọng SP mới = revenue-weighted SUM(DT SP mới)/SUM(DT thực tế) (~40% TĐ).
- **Prompt template:**
```
Bạn là verifier dữ liệu độc lập (Kangaroo). Tính các số sau từ NSAW MCP — KHÔNG hỏi lại, KHÔNG browser.
Canonical: May 2026 = posting_period_id 42. [dán canonical facts liên quan].
Câu hỏi (trả số tuyệt đối):
1. Tổng <measure> theo <dimension> kỳ 42 = ? (liệt kê từng giá trị dimension)
2. <câu hỏi 2...>
Gợi ý tool: get_sfc_report(period=42) cho SFC plan/actual; get_pl_by_dimension(posting_period_id=42, break_by=...) cho revenue/GP; execute_dynamic_query cho tùy biến.
Trả JSON: {"answers":[{"question":1,"values":{...},"total":...,"source":"tool+params"}], "caveats":["..."]}
```
- **Xử lý:** so bảng số 2 bên. Khớp → báo cáo. Lệch → root-cause (713K vs 586K = item-scope không phải bug; ghi "Đã chốt" nếu là design feature). NSAW chết/token hết → fallback executeOrPoll viz + golden report, ghi rõ verify 1 nguồn.

## 3. clevel-reviewer (Phase 6 — GATE) — tái dùng `oac-clevel-reviewer`
- **Mục đích:** verdict ship/rework góc CEO/CFO. **Đây là GATE agent chính KHÔNG tự cấp được.**
- **subagent_type:** `general-purpose` · **model:** `sonnet` (hoặc `opus` cho phase lớn) · effort TB.
- **Prompt template:**
```
Bạn review dashboard Kangaroo như CEO/CFO: "có giúp tôi ra quyết định + tin được không?", KHÔNG phải "đẹp không". KHÔNG browser — dựa số agent chính cung cấp + knowledge.
Đọc: C:\Project\KGR-OAC-Agents\Dashboard-builder\OAC_DASHBOARD_MASTERY.md (§5 viz, §8 màu, §15 quy ước, §13b số tham chiếu + chẩn đoán số sai).
Deliverable + số đã đọc/cross-check:
<dán viz/canvas + số executeOrPoll + kết quả data-crosscheck>
Đánh giá mỗi viz: 1) Decision-value (≤6 KPI/canvas, mỗi viz hàm ý 1 hành động); 2) Trust/no-contradiction (số reconcile cross-check, kỳ 42, không 2 viz cãi nhau); 3) Statistical honesty (truncated axis, ratio-as-absolute, AOP grain TĐ≠Σngành, Xanh/Đỏ denom, %vs-absolute, cherry-pick time, double-count GP); 4) No-hardcode; 5) Branding (#44BA46/#F16522/#636466, M/%, English title, semantics orange=cost/green=margin/gray=plan); 6) Spec fidelity (comment finance được thoả).
Trả mỗi viz: viz/title → ✅/⚠/❌ → lý do → fix bắt buộc. Rồi PHASE VERDICT: ✅SHIP | ⚠SHIP-with-bugs (list defect) | ❌REWORK (list ordered). 1 dòng: canvas này cho C-level quyết định gì.
```
- **Xử lý:** ❌REWORK → loop về Phase 4 sửa đúng list, re-gate. KHÔNG advance phase tới khi ✅.

## 4. kb-updater (Phase 6 — tùy chọn)
- **Mặc định agent chính TỰ update** (có context findings đầy đủ). Spawn khi ≥3 findings lớn / viết lại cả section.
- **subagent_type:** `general-purpose` · **model:** `sonnet`.
- **Prompt:** "Cập nhật C:\Project\KGR-OAC-Agents\Dashboard-builder\OAC_DASHBOARD_MASTERY.md theo C:\Project\KGR-OAC-Agents\Dashboard-builder\.claude\skills\oac-dashboard-builder\references\kb-update-rules.md (đọc trước). FINDINGS verified: <liệt kê nội dung+bằng chứng+ngày>. Edit đúng section, supersede thay vì trùng, cập nhật changelog. Trả danh sách edit (section, trước/sau 1 dòng)."

## 4b. design-advisor (Phase 1 — khi yêu cầu MƠ HỒ, chưa có Blueprint)
- **Mục đích:** lượt tư vấn nhanh trong-builder khi user chưa rõ nên show gì (tư vấn đầy đủ → skill oac-dashboard-designer riêng).
- **subagent_type:** `general-purpose` · **model:** `sonnet`. KHÔNG browser.
- **Prompt template:**
```
Bạn là dashboard design advisor. KHÔNG browser. Đọc C:\Project\KGR-OAC-Agents\Dashboard-builder\DASHBOARD_DESIGN_MASTERY.md (§2 framework audience→KPI, §3 chỉ số phái sinh, §4 cây chọn chart map viz OAC, §5 layout).
Yêu cầu user (mơ hồ): <dán>
Dữ liệu available (agent chính cung cấp): <dán profile/catalog>
Trả về JSON gọn: {"dashboard_type":"executive|operational|analytical", "canvas_questions":["câu hỏi điều hành mỗi canvas"], "vizzes":[{"question","oac_viz","shelf_mapping","metric","derived?","route"}], "derived_suggestions":[{"metric","decision","route"}], "open_questions_for_user":["..."]}
```
- **Xử lý:** dùng output dựng plan Phase 2; open_questions gom hỏi user 1 lần ở gate.

## 5. Có dùng Workflow (fan-out lớn) không?
Mặc định KHÔNG — browser là nút cổ chai, fan-out không tăng tốc build. Cân nhắc khi: **review/audit ≥5 canvas/viz có sẵn** (agent chính fetch projects/json + executeOrPoll hết → fan-out phân tích decision-value/số song song), hoặc user yêu cầu rõ.
