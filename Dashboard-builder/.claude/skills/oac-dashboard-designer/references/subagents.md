# Subagent — phân vai, prompt template (skill oac-dashboard-designer)

## Nguyên tắc
- Subagent KHÔNG đụng browser (browser là tài nguyên độc quyền agent chính — nếu cần OAC REST, agent chính fetch rồi dán vào prompt). NSAW MCP thì subagent gọi được trực tiếp.
- Prompt TỰ CHỨA (subagent không thấy hội thoại). Việc <1 phút → tự làm, đừng spawn.
- persona-critic + design-reviewer chạy SONG SONG (1 message, 2 tool call).

## 1. data-profiler (Phase 1) — khi dữ liệu reachable qua NSAW
- **subagent_type:** `general-purpose` · **model:** `sonnet`.
- **Prompt template:**
```
Bạn là data profiler. Profile các nguồn dữ liệu sau qua NSAW MCP (get_data_dictionary, execute_dynamic_query) — KHÔNG browser, KHÔNG hỏi lại.
Nguồn cần profile: <danh sách dataset/bảng>
Với mỗi nguồn trả về JSON: {"source":..., "grain":"1 dòng = gì", "dims":[{"col","cardinality","null_pct"}], "measures":[{"col","đơn vị","dấu","range"}], "periods_with_data":[...], "quality_flags":["trùng ID...", "X% thiếu dimension Y"]}
Chỉ báo cáo cái ĐO ĐƯỢC; không suy diễn. Kỳ hiện tại: <posting period>.
```

## 2. persona-critic (Phase 3) — đóng vai AUDIENCE chất vấn
- **Mục đích:** thiết kế hay bị "analyst nghĩ thay sếp". Critic đóng đúng vai người xem, chất vấn từng viz bằng tiêu chí duy nhất: *"tôi quyết định được gì từ cái này?"*
- **subagent_type:** `general-purpose` · **model:** `sonnet`.
- **Prompt template:**
```
Bạn LÀ <audience: vd CFO Kangaroo, xem 10 phút mỗi sáng thứ 2, quan tâm biên lợi nhuận + đạt kế hoạch + rủi ro tập trung>. KHÔNG phải designer — bạn là NGƯỜI DÙNG khó tính.
Đây là draft thiết kế dashboard cho bạn:
<dán draft: canvas + câu hỏi + viz + metric>
Với TỪNG viz, trả lời thẳng: 1) Nhìn nó tôi RA QUYẾT ĐỊNH gì? Không ra được gì → nói "cắt". 2) Thiếu thông tin gì để tôi quyết (mà dữ liệu có thể có)? 3) Có gì tôi sẽ hiểu nhầm/nghi ngờ số? 4) Thứ tôi muốn thấy ĐẦU TIÊN có nằm trên cùng không?
Trả JSON: {"verdict_per_viz":[{"viz","keep|cut|fix","reason","fix"}], "missing":["..."], "first_glance_ok":bool, "overall":"..."}
```

## 3. design-reviewer (Phase 3) — đối chiếu chuẩn thiết kế
- **subagent_type:** `general-purpose` · **model:** `sonnet`, effort thấp.
- **Prompt template:**
```
Bạn là reviewer thiết kế dashboard. KHÔNG browser. Đọc C:\Project\KGR-OAC-Agents\Dashboard-builder\DASHBOARD_DESIGN_MASTERY.md (§1 loại dashboard, §4 cây chọn chart + anti-patterns, §5 layout, §7 checklist).
Draft cần review:
<dán draft>
Dữ liệu đã profile: <dán profile — để kiểm khả thi grain>
Kiểm: 1) Chart đúng quan hệ dữ liệu theo §4? Viz OAC được chọn có thật + khả thi theo grain? 2) Anti-pattern (pie>6, dual-axis, stacked nhiều lớp, chart lạ cho executive)? 3) Layout §5 (BANs, ≤6 KPI, đa dạng viz, filter, nhãn kỳ)? 4) Trung thực thống kê (baseline 0, ratio mẫu số, cherry-pick, grain so sánh)? 5) Metric có định nghĩa + số expected + nguồn verify? 6) Checklist §7 mục nào fail?
Trả JSON: {"issues":[{"severity":"BLOCKER|MAJOR|MINOR","point","fix"}], "ok_points":[], "verdict":"APPROVE|REVISE"}
```

## Xử lý kết quả
- BLOCKER/MAJOR xác đáng → sửa draft. persona-critic nói "cắt" mà bạn muốn giữ → phải ghi được lý do quyết-định-phục-vụ vào Blueprint, không ghi được = cắt thật.
- Bất đồng giữa 2 reviewer → bạn quyết, ghi lý do vào mục Caveats/Giả định của Blueprint.
