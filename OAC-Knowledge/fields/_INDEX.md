# Field dossiers — giải thích mọi field theo dataset

Mỗi file `fields/<dataset>.md` liệt kê từng cột: công thức trực tiếp → bung tới bảng vật lý + filter/join + grain. NO số (lấy live).

- [(KGR) DTF_CALC_INVOICE_MEMO_#](fields/KGR_DTF_CALC_INVOICE_MEMO.md) — dataflow_output, grain: Grain dến invoice line id
- [(KGR) DTF_CALC_MIS](fields/KGR_DTF_CALC_MIS.md) — dataflow_output, grain: Grain dến invoice line id
- [Daily_Nganh_Report](fields/Daily_Nganh_Report.md) — dataflow_output, grain: group: PERIODNAME, CLASS
- [Daily_TD_Report](fields/Daily_TD_Report.md) — dataflow_output, grain: group: PERIODNAME, AsOfDate
- [KGR_DS_SFC_vs_Actual_v2](fields/KGR_DS_SFC_vs_Actual_v2.md) — dataflow_output, grain: group: POSTINGPERIOD, ID, CSEG_SCV_PRODCATG, CSEG_SCV_PRODGROUP, CSEG_SCV_MODEL, CSEG_SCV_CHAIN, CSEG_SCV_NHOMXANHDO
- [KGR_DS_SFC_vs_MEMO_v1](fields/KGR_DS_SFC_vs_MEMO_v1.md) — dataflow_output, grain: group: Tên Ngành, Nhóm SP
- [KGR_DS_SFC_vs_MEMO_v2](fields/KGR_DS_SFC_vs_MEMO_v2.md) — dataflow_output, grain: group: Tên Ngành
- [KGR_DS_SFC_vs_MEMO_v3](fields/KGR_DS_SFC_vs_MEMO_v3.md) — dataflow_output, grain: group: Tên Ngành, Nhóm SP
- [KGR_DS_SFC_vs_MEMO_v4_Chuoi](fields/KGR_DS_SFC_vs_MEMO_v4_Chuoi.md) — dataflow_output, grain: group: Tên Chuỗi
- [Nganh_Report_Long_#](fields/Nganh_Report_Long.md) — dataflow_output, grain: group: PERIODNAME, CLASS
- [Nganh_Report_Long_TD](fields/Nganh_Report_Long_TD.md) — dataflow_output, grain: group: Metric_Name, AsOfDate
- [SALE HIST w INVC](fields/SALE_HIST_w_INVC.md) — dataflow_output, grain: group: TRANDATE, SUBSIDIARY, Model name, ID CLASS, CUSTOMER, PERIODNAME, POSTINGPERIOD
- [SPmoi_ng_v3](fields/SPmoi_ng_v3.md) — dataflow_output, grain: group: PERIODNAME, AsOfDate, ID CLASS
- [TD_Metrics_Wide](fields/TD_Metrics_Wide.md) — dataflow_output, grain: group: PERIODNAME
- [TD_Report_Long](fields/TD_Report_Long.md) — dataflow_output, grain: group: PERIODNAME
- [TD_Report_PNL_Bridge](fields/TD_Report_PNL_Bridge.md) — dataflow_output, grain: group: AsOfDate
- [TD_Report_PNL_Bridge_Nganh](fields/TD_Report_PNL_Bridge_Nganh.md) — dataflow_output, grain: group: AsOfDate, ID CLASS
- [(KGR) AOP Dataset](fields/KGR_AOP_Dataset.md) — db_dataset, grain: dim/lookup
- [(KGR) CKKM TT](fields/KGR_CKKM_TT.md) — db_dataset, grain: dim/lookup
- [(KGR) Invoice_Line+Header+Pro](fields/KGR_Invoice_Line_Header_Pro.md) — db_dataset, grain: dim/lookup
- [(KGR) SFC Dataset (có AI)](fields/KGR_SFC_Dataset_c_AI.md) — db_dataset, grain: dim/lookup
- [(KGR) Tỉ lệ chi phí Lương](fields/KGR_T_l_chi_ph_L_ng.md) — db_dataset, grain: dim/lookup
- [1. Invoice_v2](fields/1_Invoice_v2.md) — db_dataset, grain: line-level
- [AOP LINE CF](fields/AOP_LINE_CF.md) — db_dataset, grain: dim/lookup
- [DW_CREDIT_MEMO](fields/DW_CREDIT_MEMO.md) — db_dataset, grain: line-level
- [DW_X_SALE_HISTORY_Dataset](fields/DW_X_SALE_HISTORY_Dataset.md) — db_dataset, grain: dim/lookup
- [Giá vốn mục tiêu](fields/Gi_v_n_m_c_ti_u.md) — db_dataset, grain: dim/lookup
- [Giá vốn tồn kho](fields/Gi_v_n_t_n_kho.md) — db_dataset, grain: dim/lookup