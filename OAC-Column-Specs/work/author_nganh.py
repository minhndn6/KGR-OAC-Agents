# -*- coding: utf-8 -*-
"""AUTHOR BC01_Summary_Ngành (4 pivot HOME/WATER/COLD&HYGEN/SANITARY CARE) theo bar METHOD.
Nguồn: df_nganh_metrics.json (KGR_DF_Nganh_Metrics_v3) + HUB. 1 bảng logic phủ cả 4 pivot (skeleton_refs)."""
import json, os
OUT = os.path.join(os.path.dirname(__file__), "rulebooks", "BC01_Summary_Nganh.json")
PIVS = ["view!20", "view!21", "view!22", "view!23"]

EXC_REV_NG = ("Lọc THEO NGÀNH của pivot (Home/Water/Cold&Hygiene/Sanitary care); và phạm vi chung: chỉ 2 pháp nhân "
              "'CTCP LD Kangaroo Quốc tế' (VU1) + 'Chi nhánh HCM'; chỉ giao dịch đã hạch toán; loại hàng thanh lý (HTL)/khách ký gửi/kênh nội bộ.")
AOP_EST = "Ước tính theo kế hoạch AOP — không phải chi phí thực phát sinh."
ALLOC_DT = "Ước tính theo AOP, phân bổ cho ngành theo tỷ trọng Doanh thu thực tế của ngành."
ALLOC_AOP = "Ước tính theo AOP, phân bổ cho ngành theo tỷ trọng Doanh số KẾ HOẠCH (AOP) của ngành."

def col(cid, name, calc, exc="—", note=""):
    return {"block": "column", "name": name, "calc": calc, "exclusions": exc, "note": note,
            "evidence": {"skeleton_refs": [f"{v}::{cid}" for v in PIVS]}}

def met(name, calc, exc="—", note=""):
    return {"block": "metric", "name": name, "calc": calc, "exclusions": exc, "note": note,
            "evidence": {"skeleton_refs": [f"{v}::Metric_Name_6" for v in PIVS]}}

cols = [
 col("Sort_Order_1", "No.", "Số thứ tự dòng chỉ tiêu (1→25), cố định; chỉ để sắp xếp."),
 col("Metric_Name_6", "Tên chỉ tiêu", "Nhãn chỉ tiêu của dòng; 25 chỉ tiêu P&L cố định (như báo cáo tập đoàn)."),
 col("AOP_GiaTri", "Doanh số AOP", "Giá trị KẾ HOẠCH (AOP) của chỉ tiêu cho RIÊNG ngành của pivot, trong kỳ (cấp ngành). Nếu chưa có kế hoạch → để trống.", note="Là số kế hoạch."),
 col("AOP_PerDS", "%/DS AOP", "= Giá trị kế hoạch của chỉ tiêu (ngành) ÷ Doanh số kế hoạch của ngành, ra %."),
 col("Actual_Amount", "Giá trị thực tế", "= Giá trị thực tế của chỉ tiêu CHO RIÊNG NGÀNH (cách tính từng chỉ tiêu xem khối B), cộng dồn từ ĐẦU THÁNG đến ngày được chọn. RIÊNG dòng 'Tỷ lệ Xanh/Đỏ': hiển thị = % doanh số Xanh của ngành = DS Xanh ÷ (DS Xanh + DS Đỏ) × 100.", exc="Lũy kế trong tháng (reset đầu tháng), đến ngày được chọn."),
 col("Actual_Amount_4", "%/ DS thực tế", "= Giá trị thực tế của chỉ tiêu (ngành) ÷ Doanh thu thực tế của NGÀNH, ra %.", exc="Không áp dụng 3 dòng: Doanh số (+VAT), Doanh thu, Tỷ lệ Xanh/Đỏ → để trống."),
 col("AOP_Amount", "Giá trị thiếu so với AOP", "= Doanh số AOP (kế hoạch của chỉ tiêu, ngành) − Giá trị thực tế (ngành). Dương = chưa đạt KH; dòng chi phí âm = chi vượt KH.", exc="Không áp dụng dòng Tỷ lệ Xanh/Đỏ → để trống."),
 col("AOP_Amount_5", "%/DS (Thiếu so với AOP)", "= (Doanh số AOP − Giá trị thực tế) (ngành) ÷ Doanh thu thực tế của ngành, ra %.", exc="Không áp dụng 3 dòng: Doanh số (+VAT), Doanh thu, Tỷ lệ Xanh/Đỏ → để trống."),
]

mets = [
 met("Doanh số (+VAT)", "Doanh số bán hàng gồm thuế GTGT CỦA RIÊNG NGÀNH, lũy kế trong tháng đến ngày chọn. Mỗi dòng = doanh thu thuần + thuế GTGT đầu ra (theo số thuế ghi trên dòng hóa đơn). Hợp nhất hóa đơn (dấu +) và credit memo (dấu −).", exc=EXC_REV_NG),
 met("Doanh thu", "Doanh thu THUẦN (chưa VAT) của riêng ngành, lũy kế đến ngày chọn (hóa đơn − credit memo, doanh thu gốc đã trừ chiết khấu trên hóa đơn).", exc=EXC_REV_NG),
 met("Giá vốn", "Tổng giá vốn hàng bán của riêng ngành. Giá vốn 1 dòng = đơn giá vốn × |số lượng|; đơn giá theo 3 lớp: (1) 'Giá vốn mục tiêu' tra mã SP (MSP)+tháng; (2) thiếu → 'Giá vốn tồn kho' tra mã item+pháp nhân+kỳ; (3) thiếu → 50% doanh thu của dòng. Credit memo âm.", exc="Hàng tặng (DT=0)/dòng chiết khấu → 0; lọc theo ngành + phạm vi như Doanh thu."),
 met("Lợi nhuận gộp", "= Doanh thu (ngành) − Giá vốn (ngành). Là hiệu của 2 tổng cấp ngành — không khớp lại theo từng dòng hóa đơn."),
 met("CP chiết khấu khuyến mại", "= Doanh thu thực tế của dòng (ngành) × tỷ lệ CKKM. Tỷ lệ CKKM từ chương trình khuyến mãi (trade promotion), trung bình cộng theo tháng; ưu tiên (Model SP + Kênh + kỳ) → (Model SP + Chuỗi + kỳ) → 0.", exc="Lọc theo ngành + phạm vi như Doanh thu."),
 met("CP nhân viên KD", "= phần trăm kế hoạch (theo AOP) của chỉ tiêu 'CP nhân viên KD' × Doanh thu thực tế CỦA NGÀNH.", note=AOP_EST),
 met("CP roadshow hội nghị", "= phần trăm kế hoạch (theo AOP) của chỉ tiêu 'CP roadshow hội nghị' × Doanh thu thực tế của ngành.", note=AOP_EST),
 met("CP công tác tiếp khách KD", "= phần trăm kế hoạch (theo AOP) của chỉ tiêu 'CP công tác tiếp khách KD' × Doanh thu thực tế của ngành.", note=AOP_EST),
 met("Lợi nhuận gộp Kinh doanh", "= Lợi nhuận gộp − CP chiết khấu khuyến mại − CP nhân viên KD − CP roadshow hội nghị − CP công tác tiếp khách KD (tất cả của ngành).", note="Gồm các chi phí ước tính theo AOP."),
 met("CP xúc tiến bán hàng", "= CP xúc tiến bán hàng của TẬP ĐOÀN × (Doanh số KẾ HOẠCH của ngành ÷ Doanh số KẾ HOẠCH của tập đoàn). (CP xúc tiến tập đoàn = số ngày trong tháng đến ngày chọn × định mức tháng theo AOP ÷ 30.)", note=ALLOC_AOP),
 met("Lợi nhuận xúc tiến bán hàng", "= Lợi nhuận gộp Kinh doanh − CP xúc tiến bán hàng (ngành)."),
 met("CP nhân viên BO", "= CP nhân viên BO của TẬP ĐOÀN × (Doanh số KẾ HOẠCH của ngành ÷ Doanh số KẾ HOẠCH của tập đoàn).", note=ALLOC_AOP),
 met("Lợi nhuận nhân viên", "= Lợi nhuận xúc tiến bán hàng − CP nhân viên BO (ngành)."),
 met("CP quản lý vận hành", "Dòng tổng hợp = TỔNG ĐÚNG 5 dòng chi phí bên dưới trong bảng này (CÙNG GIÁ TRỊ với các dòng đó): 'CP vận chuyển' + 'CP bảo hành' + 'CP tài chính' + 'CP dự phòng tồn kho thanh lý' + 'CP khác'.", note="Các thành phần đều là chi phí ước tính theo AOP/định mức — xem đúng từng dòng tương ứng."),
 met("CP vận chuyển", "= phần trăm kế hoạch (theo AOP) của chỉ tiêu 'CP vận chuyển' × Doanh thu thực tế của ngành.", note=AOP_EST),
 met("CP bảo hành", "= phần trăm kế hoạch (theo AOP) của chỉ tiêu 'CP bảo hành' × Doanh thu thực tế của ngành.", note=AOP_EST),
 met("CP tài chính", "= phần trăm kế hoạch (theo AOP) của chỉ tiêu 'CP tài chính' × Doanh thu thực tế của ngành.", note=AOP_EST),
 met("CP khác", "= CP khác của TẬP ĐOÀN × (Doanh số KẾ HOẠCH của ngành ÷ Doanh số KẾ HOẠCH của tập đoàn).", note=ALLOC_AOP),
 met("Thu nhập khác", "= Thu nhập khác của TẬP ĐOÀN × (Doanh số KẾ HOẠCH của ngành ÷ Doanh số KẾ HOẠCH của tập đoàn). 'Thu nhập khác của tập đoàn' = doanh thu của các dòng thuộc ngành 'Khác' (ngoài 4 ngành chính Water/Home/Cold & Hygiene/Sanitary care; ngành xác định theo phân loại ngành ghi trên dòng hóa đơn), lũy kế đến ngày chọn, cùng phạm vi loại trừ như Doanh thu.", note="Phân bổ về ngành theo tỷ trọng AOP doanh số; được cộng khi tính Lợi nhuận quản lý vận hành."),
 met("Lợi nhuận quản lý vận hành", "= Lợi nhuận nhân viên − CP quản lý vận hành + Thu nhập khác (ngành)."),
 met("CP dự phòng hoạt động năm trước", "= 21% × Lợi nhuận quản lý vận hành (ngành).", note="Định mức 21% cố định; áp trên LN quản lý vận hành kỳ hiện tại (tên dòng theo nhãn báo cáo)."),
 met("Lợi nhuận trước thuế", "= Lợi nhuận quản lý vận hành − CP dự phòng hoạt động năm trước (ngành)."),
 met("Lợi nhuận sau thuế", "= Nếu Lợi nhuận trước thuế > 0 thì giữ lại 80% (× 0,8); nếu ≤ 0 giữ nguyên.", note="80% là QUY ƯỚC cố định trong báo cáo (không phải thuế suất TNDN thực)."),
 met("Tỷ lệ Xanh/Đỏ", "Giá trị gốc = Doanh số nhóm Xanh ÷ Doanh số nhóm Đỏ (của ngành; Đỏ=0 → để trống). Cột 'Giá trị thực tế' quy đổi thành % doanh số Xanh = DS Xanh ÷ (DS Xanh + DS Đỏ) × 100.", exc="Chỉ sản phẩm có phân loại Xanh/Đỏ, trong ngành."),
 met("CP dự phòng tồn kho thanh lý", "= 1,5% × Doanh thu thực tế của ngành.", note="Định mức 1,5% cố định; là một thành phần của 'CP quản lý vận hành'."),
]

rb = {"workbook": "(KGR) BRD.BC01_Daily_Summary v1.1", "canvas": "BC01_Summary_Ngành",
      "viz": "view!20–view!23",
      "viz_title": "4 pivot theo ngành: HOME / WATER / COLD & HYGEN / SANITARY CARE — mỗi pivot áp đúng công thức dưới đây, LỌC THEO NGÀNH tương ứng",
      "is_summary": True, "rows": cols + mets}
os.makedirs(os.path.dirname(OUT), exist_ok=True)
json.dump(rb, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"wrote {OUT}: {len(cols)} cột + {len(mets)} chỉ tiêu (phủ 4 pivot ngành)")
