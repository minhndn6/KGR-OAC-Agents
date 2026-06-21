# IMPROVEMENTS — tổng hợp từ 100+ use-case (gap + partial)

PASS 106/120. Dưới đây là điểm cần cải thiện (GAP) + cần lưu ý (PARTIAL).

## GAP (KB chưa trả lời được)
- (không có GAP)

## PARTIAL (trả lời được nhưng cần build/lưu ý)
- 🟡 [source] Cần cogs theo asm — lấy đâu? — metric+chiều có riêng, chưa cùng dataset → có thể build từ hub
- 🟡 [build] Build dashboard: sfc theo model ở grain tháng — dựng từ đâu? — metric+chiều có riêng, chưa cùng dataset → có thể build từ hub

## Khuyến nghị cải thiện (rút ra)
- Mọi 'cần M theo D' chưa cùng dataset → là cơ hội DỰNG dataflow mới từ hub (orchestrator O1 lập kế hoạch).
- Chiều chưa index trong capability_map (nếu có) → bổ sung index hoặc ghi rõ 'build từ hub'.
- Metric thiếu hẳn (GAP source) → cân nhắc bổ sung vào glossary/capability hoặc nói rõ 'chưa build trong OAC'.
- PARTIAL nhiều ở 1 chiều → ưu tiên dựng sẵn dataset chiều đó nếu hỏi thường xuyên.