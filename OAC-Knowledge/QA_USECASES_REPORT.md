# QA_USECASES_REPORT — 100+ ca dùng theo góc nhìn leaders

Tổng 120 ca · PASS=106 · PARTIAL=14 · GAP=0


## trace
- ✅ [Finance Analyst] 'Doanh thu thực tế' tính từ đâu, gốc bảng NSAW nào? → (KGR) DTF_CALC_INVOICE_MEMO_#.Doanh thu thực tế
- ✅ [Finance Analyst] 'Giá Vốn' tính từ đâu, gốc bảng NSAW nào? → (KGR) DTF_CALC_INVOICE_MEMO_#.Giá Vốn
- ✅ [Finance Analyst] 'LN Gộp' tính từ đâu, gốc bảng NSAW nào? → (KGR) DTF_CALC_INVOICE_MEMO_#.%LN Gộp
- ✅ [Finance Analyst] '%GP Ròng' tính từ đâu, gốc bảng NSAW nào? → (KGR) DTF_CALC_INVOICE_MEMO_#.%GP Ròng
- ✅ [Finance Analyst] 'DS Xanh' tính từ đâu, gốc bảng NSAW nào? → (KGR) DTF_CALC_INVOICE_MEMO_#.DS Xanh
- ✅ [Finance Analyst] 'DS Đỏ' tính từ đâu, gốc bảng NSAW nào? → (KGR) DTF_CALC_INVOICE_MEMO_#.DS Đỏ
- ✅ [Finance Analyst] 'Doanh thu SP mới' tính từ đâu, gốc bảng NSAW nào? → (KGR) DTF_CALC_INVOICE_MEMO_#.Doanh thu SP mới
- ✅ [Finance Analyst] 'CKKM' tính từ đâu, gốc bảng NSAW nào? → (KGR) DTF_CALC_INVOICE_MEMO_#.CKKM Per
- ✅ [Finance Analyst] 'Quy hoạch SP' tính từ đâu, gốc bảng NSAW nào? → (KGR) DTF_CALC_INVOICE_MEMO_#.Quy hoạch SP
- ✅ [Finance Analyst] 'Doanh số thực tế' tính từ đâu, gốc bảng NSAW nào? → (KGR) DTF_CALC_INVOICE_MEMO_#.Doanh số thực tế
- ✅ [Finance Analyst] 'a9' tính từ đâu, gốc bảng NSAW nào? → TD_Metrics_Wide.a9
- ✅ [Finance Analyst] 'a4' tính từ đâu, gốc bảng NSAW nào? → TD_Metrics_Wide.a4
- ✅ [Finance Analyst] 'a20' tính từ đâu, gốc bảng NSAW nào? → TD_Metrics_Wide.a20
- ✅ [Finance Analyst] 'Tên Chuỗi' tính từ đâu, gốc bảng NSAW nào? → (KGR) DTF_CALC_INVOICE_MEMO_#.Tên Chuỗi
- ✅ [Finance Analyst] 'Tên Kênh' tính từ đâu, gốc bảng NSAW nào? → (KGR) DTF_CALC_INVOICE_MEMO_#.Tên Kênh
- ✅ [Finance Analyst] 'Tên Ngành' tính từ đâu, gốc bảng NSAW nào? → (KGR) DTF_CALC_INVOICE_MEMO_#.Tên Ngành
- ✅ [Finance Analyst] 'Model name' tính từ đâu, gốc bảng NSAW nào? → (KGR) DTF_CALC_INVOICE_MEMO_#.Model name
- ✅ [Finance Analyst] 'QUANTITY' tính từ đâu, gốc bảng NSAW nào? → (KGR) DTF_CALC_INVOICE_MEMO_#.QUANTITY
- ✅ [Finance Analyst] 'Nhóm xanh đỏ' tính từ đâu, gốc bảng NSAW nào? → (KGR) DTF_CALC_INVOICE_MEMO_#.Nhóm xanh đỏ
- ✅ [Finance Analyst] 'Tỷ trọng SP mới' tính từ đâu, gốc bảng NSAW nào? → (KGR) DTF_CALC_INVOICE_MEMO_#.Tỷ trọng SP mới

## source
- ✅ [CEO] Cần revenue theo chuoi — lấy đâu? → ['(KGR) DTF_CALC_INVOICE_MEMO_#', '(KGR) DTF_CALC_MIS']
- ✅ [CEO] Cần revenue theo kenh — lấy đâu? → ['(KGR) DTF_CALC_INVOICE_MEMO_#', '(KGR) DTF_CALC_MIS']
- ✅ [CEO] Cần revenue theo nganh — lấy đâu? → ['(KGR) DTF_CALC_INVOICE_MEMO_#', '(KGR) DTF_CALC_MIS']
- ✅ [CEO] Cần revenue theo model — lấy đâu? → ['(KGR) DTF_CALC_INVOICE_MEMO_#', '(KGR) DTF_CALC_MIS']
- ✅ [CEO] Cần revenue theo asm — lấy đâu? → ['DW_X_SALE_HISTORY_Dataset']
- ✅ [CEO] Cần revenue theo tinh — lấy đâu? → ['(KGR) DTF_CALC_MIS']
- ✅ [CFO] Cần cogs theo chuoi — lấy đâu? → ['(KGR) DTF_CALC_INVOICE_MEMO_#', '(KGR) DTF_CALC_MIS']
- ✅ [CFO] Cần cogs theo kenh — lấy đâu? → ['(KGR) DTF_CALC_INVOICE_MEMO_#', '(KGR) DTF_CALC_MIS']
- ✅ [CFO] Cần cogs theo nganh — lấy đâu? → ['(KGR) DTF_CALC_INVOICE_MEMO_#', '(KGR) DTF_CALC_MIS']
- ✅ [CFO] Cần cogs theo model — lấy đâu? → ['(KGR) DTF_CALC_INVOICE_MEMO_#', '(KGR) DTF_CALC_MIS']
- 🟡 [CFO] Cần cogs theo asm — lấy đâu? → metric+chiều có riêng, chưa cùng dataset → có thể build từ hub
- ✅ [CFO] Cần cogs theo tinh — lấy đâu? → ['(KGR) DTF_CALC_MIS']
- ✅ [CFO] Cần gross_profit theo chuoi — lấy đâu? → ['(KGR) DTF_CALC_INVOICE_MEMO_#', '(KGR) DTF_CALC_MIS']
- ✅ [CFO] Cần gross_profit theo kenh — lấy đâu? → ['(KGR) DTF_CALC_INVOICE_MEMO_#', '(KGR) DTF_CALC_MIS']
- ✅ [CFO] Cần gross_profit theo nganh — lấy đâu? → ['(KGR) DTF_CALC_INVOICE_MEMO_#', '(KGR) DTF_CALC_MIS']
- ✅ [CFO] Cần gross_profit theo model — lấy đâu? → ['(KGR) DTF_CALC_INVOICE_MEMO_#', '(KGR) DTF_CALC_MIS']
- 🟡 [CFO] Cần gross_profit theo asm — lấy đâu? → metric+chiều có riêng, chưa cùng dataset → có thể build từ hub
- ✅ [CFO] Cần gross_profit theo tinh — lấy đâu? → ['(KGR) DTF_CALC_MIS']
- ✅ [CMO] Cần ckkm theo chuoi — lấy đâu? → ['(KGR) DTF_CALC_INVOICE_MEMO_#', '(KGR) DTF_CALC_MIS']
- ✅ [CMO] Cần ckkm theo kenh — lấy đâu? → ['(KGR) DTF_CALC_INVOICE_MEMO_#', '(KGR) DTF_CALC_MIS']
- ✅ [CMO] Cần ckkm theo nganh — lấy đâu? → ['(KGR) DTF_CALC_INVOICE_MEMO_#', '(KGR) DTF_CALC_MIS']
- ✅ [CMO] Cần ckkm theo model — lấy đâu? → ['(KGR) DTF_CALC_INVOICE_MEMO_#', '(KGR) DTF_CALC_MIS']
- 🟡 [CMO] Cần ckkm theo asm — lấy đâu? → metric+chiều có riêng, chưa cùng dataset → có thể build từ hub
- ✅ [CMO] Cần ckkm theo tinh — lấy đâu? → ['(KGR) DTF_CALC_MIS']
- ✅ [CMO] Cần sp_moi theo chuoi — lấy đâu? → ['(KGR) DTF_CALC_INVOICE_MEMO_#', '(KGR) DTF_CALC_MIS']
- ✅ [CMO] Cần sp_moi theo kenh — lấy đâu? → ['(KGR) DTF_CALC_INVOICE_MEMO_#', '(KGR) DTF_CALC_MIS']
- ✅ [CMO] Cần sp_moi theo nganh — lấy đâu? → ['(KGR) DTF_CALC_INVOICE_MEMO_#', '(KGR) DTF_CALC_MIS']
- ✅ [CMO] Cần sp_moi theo model — lấy đâu? → ['(KGR) DTF_CALC_INVOICE_MEMO_#', '(KGR) DTF_CALC_MIS']
- 🟡 [CMO] Cần sp_moi theo asm — lấy đâu? → metric+chiều có riêng, chưa cùng dataset → có thể build từ hub
- ✅ [CMO] Cần sp_moi theo tinh — lấy đâu? → ['(KGR) DTF_CALC_MIS']
- ✅ [CFO] Cần aop theo chuoi — lấy đâu? → ['KGR_DS_SFC_vs_MEMO_v4_Chuoi']
- 🟡 [CFO] Cần aop theo kenh — lấy đâu? → metric+chiều có riêng, chưa cùng dataset → có thể build từ hub
- ✅ [CFO] Cần aop theo nganh — lấy đâu? → ['Daily_Nganh_Report', 'KGR_DS_SFC_vs_MEMO_v2']
- 🟡 [CFO] Cần aop theo model — lấy đâu? → metric+chiều có riêng, chưa cùng dataset → có thể build từ hub
- 🟡 [CFO] Cần aop theo asm — lấy đâu? → metric+chiều có riêng, chưa cùng dataset → có thể build từ hub
- 🟡 [CFO] Cần aop theo tinh — lấy đâu? → metric+chiều có riêng, chưa cùng dataset → có thể build từ hub
- ✅ [Supply Chain Head] Cần sfc theo chuoi — lấy đâu? → ['KGR_DS_SFC_vs_MEMO_v4_Chuoi']
- 🟡 [Supply Chain Head] Cần sfc theo kenh — lấy đâu? → metric+chiều có riêng, chưa cùng dataset → có thể build từ hub
- ✅ [Supply Chain Head] Cần sfc theo nganh — lấy đâu? → ['KGR_DS_SFC_vs_MEMO_v2', 'KGR_DS_SFC_vs_MEMO_v3']
- 🟡 [Supply Chain Head] Cần sfc theo model — lấy đâu? → metric+chiều có riêng, chưa cùng dataset → có thể build từ hub
- 🟡 [Supply Chain Head] Cần sfc theo asm — lấy đâu? → metric+chiều có riêng, chưa cùng dataset → có thể build từ hub
- 🟡 [Supply Chain Head] Cần sfc theo tinh — lấy đâu? → metric+chiều có riêng, chưa cùng dataset → có thể build từ hub
- ✅ [Supply Chain Head] Cần quantity theo chuoi — lấy đâu? → ['(KGR) DTF_CALC_INVOICE_MEMO_#', '(KGR) DTF_CALC_MIS']
- ✅ [Supply Chain Head] Cần quantity theo kenh — lấy đâu? → ['(KGR) DTF_CALC_INVOICE_MEMO_#', '(KGR) DTF_CALC_MIS']
- ✅ [Supply Chain Head] Cần quantity theo nganh — lấy đâu? → ['(KGR) DTF_CALC_INVOICE_MEMO_#', '(KGR) DTF_CALC_MIS']
- ✅ [Supply Chain Head] Cần quantity theo model — lấy đâu? → ['(KGR) DTF_CALC_INVOICE_MEMO_#', '(KGR) DTF_CALC_MIS']
- ✅ [Supply Chain Head] Cần quantity theo asm — lấy đâu? → ['DW_X_SALE_HISTORY_Dataset']
- ✅ [Supply Chain Head] Cần quantity theo tinh — lấy đâu? → ['(KGR) DTF_CALC_MIS']
- ✅ [CEO] Cần profit theo chuoi — lấy đâu? → ['(KGR) DTF_CALC_INVOICE_MEMO_#', '(KGR) DTF_CALC_MIS']
- ✅ [CEO] Cần profit theo kenh — lấy đâu? → ['(KGR) DTF_CALC_INVOICE_MEMO_#', '(KGR) DTF_CALC_MIS']
- ✅ [CEO] Cần profit theo nganh — lấy đâu? → ['(KGR) DTF_CALC_INVOICE_MEMO_#', '(KGR) DTF_CALC_MIS']
- ✅ [CEO] Cần profit theo model — lấy đâu? → ['(KGR) DTF_CALC_INVOICE_MEMO_#', '(KGR) DTF_CALC_MIS']
- 🟡 [CEO] Cần profit theo asm — lấy đâu? → metric+chiều có riêng, chưa cùng dataset → có thể build từ hub
- ✅ [CEO] Cần profit theo tinh — lấy đâu? → ['(KGR) DTF_CALC_MIS']

## meaning
- ✅ [BA] 'Xanh' nghĩa nghiệp vụ là gì? → glossary có
- ✅ [BA] 'Đỏ' nghĩa nghiệp vụ là gì? → glossary có
- ✅ [BA] 'CKKM' nghĩa nghiệp vụ là gì? → glossary có
- ✅ [BA] 'AOP' nghĩa nghiệp vụ là gì? → glossary có
- ✅ [BA] 'SFC' nghĩa nghiệp vụ là gì? → glossary có
- ✅ [BA] 'Lợi nhuận gộp' nghĩa nghiệp vụ là gì? → glossary có
- ✅ [BA] 'Giá vốn' nghĩa nghiệp vụ là gì? → glossary có
- ✅ [BA] 'Doanh thu' nghĩa nghiệp vụ là gì? → glossary có
- ✅ [BA] 'ký gửi' nghĩa nghiệp vụ là gì? → glossary có
- ✅ [BA] 'ngành' nghĩa nghiệp vụ là gì? → glossary có
- ✅ [BA] 'chuỗi' nghĩa nghiệp vụ là gì? → glossary có
- ✅ [BA] 'kênh' nghĩa nghiệp vụ là gì? → glossary có
- ✅ [BA] 'a9' nghĩa nghiệp vụ là gì? → glossary có
- ✅ [BA] 'a20' nghĩa nghiệp vụ là gì? → glossary có
- ✅ [BA] 'SP mới' nghĩa nghiệp vụ là gì? → glossary có

## impact
- ✅ [Data Engineer] Đổi bảng DW_NS_CUSTOMER_INVOICE_LINES_F thì viz/dataset nào gãy? → reverse→workbook
- ✅ [Data Engineer] Đổi bảng DW_NS_X_GIA_VON_MUC_TIEU_CT thì viz/dataset nào gãy? → reverse→workbook
- ✅ [Data Engineer] Đổi bảng DW_NS_X_TRADE_PROMOTION_LINE thì viz/dataset nào gãy? → reverse→workbook
- ✅ [Data Engineer] Đổi bảng DW_NS_X_AOP_LINE_CF thì viz/dataset nào gãy? → reverse→workbook
- ✅ [Data Engineer] Đổi bảng DW_NS_X_SFC_LINES_CF thì viz/dataset nào gãy? → reverse→workbook
- ✅ [Data Engineer] Đổi bảng DW_NS_CLASSIFICATION_D thì viz/dataset nào gãy? → reverse→workbook
- ✅ [Data Engineer] Đổi bảng DW_NS_X_CAM_CUSTOMRECORD_CSEG_SCV_CHAIN thì viz/dataset nào gãy? → reverse→workbook
- ✅ [Data Engineer] Đổi bảng DW_NS_CUSTOMER_CREDIT_LINES_F thì viz/dataset nào gãy? → reverse→workbook

## build
- ✅ [CFO] Build dashboard: revenue theo chuoi ở grain ngày — dựng từ đâu? → ['(KGR) DTF_CALC_INVOICE_MEMO_#', '(KGR) DTF_CALC_MIS']
- ✅ [CMO] Build dashboard: ckkm theo chuoi ở grain tháng — dựng từ đâu? → ['(KGR) DTF_CALC_INVOICE_MEMO_#', '(KGR) DTF_CALC_MIS']
- ✅ [Sales Head] Build dashboard: revenue theo asm ở grain tháng — dựng từ đâu? → ['DW_X_SALE_HISTORY_Dataset']
- 🟡 [Supply Chain Head] Build dashboard: sfc theo model ở grain tháng — dựng từ đâu? → metric+chiều có riêng, chưa cùng dataset → có thể build từ hub
- ✅ [CEO] Build dashboard: profit theo nganh ở grain kỳ — dựng từ đâu? → ['(KGR) DTF_CALC_INVOICE_MEMO_#', '(KGR) DTF_CALC_MIS']
- ✅ [CFO] Build dashboard: gross_profit theo kenh ở grain tháng — dựng từ đâu? → ['(KGR) DTF_CALC_INVOICE_MEMO_#', '(KGR) DTF_CALC_MIS']
- ✅ [Branch Head] Build dashboard: revenue theo don_vi ở grain ngày — dựng từ đâu? → ['(KGR) DTF_CALC_INVOICE_MEMO_#', '(KGR) DTF_CALC_MIS']
- ✅ [CMO] Build dashboard: sp_moi theo nganh ở grain tháng — dựng từ đâu? → ['(KGR) DTF_CALC_INVOICE_MEMO_#', '(KGR) DTF_CALC_MIS']

## governance
- ✅ [CFO] 'Lợi nhuận' a9 là số thực hay ước tính? → governance/glossary
- ✅ [Auditor] a10 (CP xúc tiến) có phải số cứng không? → governance/glossary
- ✅ [Auditor] Thuế tính thế nào (có hardcode)? → governance/glossary
- ✅ [CFO] Doanh thu Tập đoàn loại trừ gì (subsidiary)? → governance/glossary

## freshness
- ✅ [Data Engineer] Làm sao biết KB còn khớp OAC (dataflow đổi)? → live_query_recipes
- ✅ [Finance Analyst] Lấy SỐ hiện tại của 1 metric thế nào? → live_query_recipes

## edge
- ✅ [BA] Hỏi về workbook NGOÀI 4 cái thì sao? → examples

## precedence
- ✅ [CTO] OAC và NSAW mâu thuẫn thì tin ai? → external/README
- ✅ [CTO] Báo cáo vs dashboard lệch số thì theo cái nào? → external/README

## pitfall
- ✅ [Data Engineer] Re-aggregate %GP từ hub có đúng không? → playbook
- ✅ [Data Engineer] COGS join GVMT có bẫy gì? → playbook

## source
- ✅ [Supply Chain Head] SFC ước tính lấy dataset nào (authoritative)? → glossary

## build
- ✅ [CMO] Cần ROI khuyến mãi (CKKM) theo chuỗi — khả thi? → ['(KGR) DTF_CALC_INVOICE_MEMO_#', '(KGR) DTF_CALC_MIS']

## meaning
- ✅ [CEO] Tỷ lệ Xanh/Đỏ là gì, tính sao? → glossary

## source
- ✅ [Branch Head] Doanh thu theo tỉnh/thành? → ['(KGR) DTF_CALC_MIS']