# -*- coding: utf-8 -*-
"""AUTHOR BC01_Summary_TĐ (view!9) theo bar METHOD. Nguồn: df_tdmetrics_live.json + HUB + projects.json.
Xuất rulebooks/BC01_Summary_TD.json (schema gọn: block/name/calc/exclusions/note/evidence)."""
import json, os

OUT = os.path.join(os.path.dirname(__file__), "rulebooks", "BC01_Summary_TD.json")

EXC_REV = ("Chỉ 2 pháp nhân 'CTCP LD Kangaroo Quốc tế' (VU1) và 'Chi nhánh HCM'; chỉ giao dịch đã hạch toán "
           "(đã ghi sổ kế toán kỳ tương ứng); loại dòng có vụ việc = Hàng thanh lý (HTL); loại khách hàng "
           "được đánh dấu ký gửi; loại giao dịch thuộc kênh nội bộ.")
AOP_EST = "Ước tính theo kế hoạch AOP — không phải chi phí thực phát sinh."
LK = "Lũy kế đến ngày được chọn ở bộ lọc (AsOfDate); đổi ngày → đổi số."

def col(cid, name, calc, exc="—", note=""):
    return {"block": "column", "name": name, "calc": calc, "exclusions": exc, "note": note,
            "evidence": {"skeleton_ref": f"view!9::{cid}"}}

def met(name, calc, exc="—", note=""):
    return {"block": "metric", "name": name, "calc": calc, "exclusions": exc, "note": note,
            "evidence": {"skeleton_ref": "view!9::Metric_Name"}}

cols = [
 col("Sort_Order_2", "No.", "Số thứ tự dòng chỉ tiêu (1→25), cố định theo trình tự bảng lãi lỗ; chỉ để sắp xếp, không phải số liệu."),
 col("Metric_Name", "Tên chỉ tiêu", "Nhãn chỉ tiêu của dòng (chiều dòng của bảng); danh mục 25 chỉ tiêu P&L cố định."),
 col("AOP_Amount_1", "Doanh số AOP",
     "Giá trị KẾ HOẠCH (AOP) của chỉ tiêu trong kỳ — lấy trực tiếp từ bản kế hoạch năm (AOP) đã phân bổ cho từng chỉ tiêu, theo kỳ (tháng) và cấp tập đoàn. Nếu kỳ đó chưa có kế hoạch cho chỉ tiêu → để trống.",
     note="Là số kế hoạch, không phải thực tế."),
 col("AOP_Per", "%/DS AOP",
     "Phần trăm KẾ HOẠCH của chỉ tiêu trên doanh số — lấy trực tiếp tỷ lệ %/doanh số trong bản kế hoạch AOP của chỉ tiêu (theo kỳ, cấp tập đoàn)."),
 col("LuyKe_GiaTri", "Giá trị thực tế",
     "= Giá trị thực tế của chỉ tiêu (cách tính từng chỉ tiêu xem khối B bên dưới), CỘNG DỒN từ ĐẦU THÁNG đến ngày được chọn. RIÊNG dòng 'Tỷ lệ Xanh/Đỏ': cột này hiển thị = % doanh số Xanh = Doanh số Xanh ÷ (Doanh số Xanh + Doanh số Đỏ) × 100.",
     exc="Lũy kế trong THÁNG (reset đầu mỗi tháng), đến ngày được chọn ở bộ lọc; đổi ngày → đổi số."),
 col("LuyKe_PerDS", "%/ DS thực tế",
     "= Giá trị thực tế của chỉ tiêu ÷ Doanh thu thực tế (cùng lũy kế đến ngày được chọn), ra %.",
     exc="Không áp dụng cho 3 dòng: Doanh số (+VAT), Doanh thu, Tỷ lệ Xanh/Đỏ → để trống."),
 col("Thieu_GiaTri", "Giá trị thiếu so với AOP",
     "= Doanh số AOP (kế hoạch của chỉ tiêu) − Giá trị thực tế của chỉ tiêu. Dương = chưa đạt kế hoạch; riêng các dòng chi phí, số âm = chi VƯỢT kế hoạch.",
     exc="Không áp dụng dòng Tỷ lệ Xanh/Đỏ → để trống."),
 col("Thieu_PerDS", "%/DS (Thiếu so với AOP)",
     "= (Doanh số AOP − Giá trị thực tế) ÷ Doanh thu thực tế, ra %.",
     exc="Không áp dụng 3 dòng: Doanh số (+VAT), Doanh thu, Tỷ lệ Xanh/Đỏ → để trống."),
]

mets = [
 met("Doanh số (+VAT)",
     "Doanh số bán hàng đã gồm thuế GTGT, lũy kế trong tháng đến ngày được chọn. Mỗi dòng = doanh thu thuần của dòng + thuế GTGT đầu ra của dòng (lấy theo SỐ THUẾ GTGT ghi trên từng dòng hóa đơn, tức theo thuế suất của dòng — không phải một suất cố định). Hợp nhất hóa đơn bán (dấu +) và chứng từ điều chỉnh giảm/credit memo (dấu −).",
     exc=EXC_REV),
 met("Doanh thu",
     "Doanh thu THUẦN (chưa VAT) từ bán hàng, lũy kế đến ngày chọn. Mỗi dòng = doanh thu gốc chưa VAT của dòng (giá bán đã trừ chiết khấu trên hóa đơn; các dòng chiết khấu là dòng riêng) × dấu (hóa đơn bán = +, credit memo = −); cộng dồn. Chỉ lấy phát sinh thuộc tài khoản doanh thu.",
     exc=EXC_REV),
 met("Giá vốn",
     "Tổng giá vốn hàng bán, lũy kế đến ngày chọn. Giá vốn 1 dòng = đơn giá vốn × số lượng (lấy trị tuyệt đối số lượng). Đơn giá vốn theo 3 lớp ưu tiên: (1) 'Giá vốn mục tiêu' tra theo mã sản phẩm (MSP) + tháng giao dịch; (2) nếu không có → 'Giá vốn tồn kho' tra theo mã item + pháp nhân + kỳ; (3) nếu vẫn không có → = 50% doanh thu thực tế của dòng. Credit memo lấy dấu âm.",
     exc="Hàng tặng (free-gift) mà doanh thu = 0 → giá vốn = 0; dòng chiết khấu → giá vốn = 0; phạm vi pháp nhân/hạch toán như Doanh thu."),
 met("Lợi nhuận gộp",
     "= Doanh thu − Giá vốn (hai chỉ tiêu cùng bảng, cùng phạm vi/kỳ/lũy kế). Là hiệu của 2 TỔNG cấp tập đoàn — không khớp lại theo từng dòng hóa đơn."),
 met("CP chiết khấu khuyến mại",
     "= Doanh thu thực tế của dòng × tỷ lệ CKKM, lũy kế đến ngày chọn. Tỷ lệ CKKM lấy từ chương trình khuyến mãi (trade promotion), là tỷ lệ % TRUNG BÌNH CỘNG theo THÁNG cho từng tổ hợp; khớp vào dòng hóa đơn ưu tiên theo (Model sản phẩm + Kênh bán + kỳ); nếu không có → theo (Model sản phẩm + Chuỗi + kỳ); nếu không có → 0. (Model = cấp model của sản phẩm; Kênh = kênh bán; Chuỗi = chuỗi bán hàng.)",
     exc="Cùng phạm vi với Doanh thu (2 pháp nhân VU1 + HCM; đã hạch toán; loại hàng thanh lý (HTL)/khách ký gửi/kênh nội bộ)."),
 met("CP nhân viên KD",
     "= phần trăm kế hoạch (theo AOP) của chỉ tiêu 'CP nhân viên KD' × Doanh thu thực tế. Phần trăm kế hoạch lấy từ bản kế hoạch AOP (loại 'kế hoạch chi phí'), theo kỳ, cấp tập đoàn.",
     note=AOP_EST),
 met("CP roadshow hội nghị",
     "= phần trăm kế hoạch (theo AOP) của chỉ tiêu 'CP roadshow hội nghị' × Doanh thu thực tế.", note=AOP_EST),
 met("CP công tác tiếp khách KD",
     "= phần trăm kế hoạch (theo AOP) của chỉ tiêu 'CP công tác tiếp khách KD' × Doanh thu thực tế.", note=AOP_EST),
 met("Lợi nhuận gộp Kinh doanh",
     "= Lợi nhuận gộp − CP chiết khấu khuyến mại − CP nhân viên KD − CP roadshow hội nghị − CP công tác tiếp khách KD.",
     note="Trong đó CP nhân viên KD / roadshow / công tác là ước tính theo AOP."),
 met("CP xúc tiến bán hàng",
     "= (số thứ tự ngày trong tháng của ngày được chọn — ví dụ chọn 16/05 → 16) × (định mức chi phí xúc tiến của THÁNG theo kế hoạch ÷ 30). Mẫu số 30 là quy ước cố định (luôn 30, không đổi theo số ngày thực của tháng). Định mức lấy từ kế hoạch AOP chỉ tiêu 'CP xúc tiến bán hàng', cấp tập đoàn.",
     note=AOP_EST),
 met("Lợi nhuận xúc tiến bán hàng", "= Lợi nhuận gộp Kinh doanh − CP xúc tiến bán hàng."),
 met("CP nhân viên BO",
     "= (số thứ tự ngày trong tháng của ngày được chọn) × (định mức chi phí nhân viên back-office của THÁNG theo kế hoạch ÷ 30). Mẫu số 30 cố định. Định mức lấy từ kế hoạch AOP chỉ tiêu 'CP nhân viên BO', cấp tập đoàn. Nếu tháng đó không có định mức → 0.",
     note=AOP_EST),
 met("Lợi nhuận nhân viên", "= Lợi nhuận xúc tiến bán hàng − CP nhân viên BO."),
 met("CP quản lý vận hành",
     "Dòng tổng hợp = CP vận chuyển + CP bảo hành + CP tài chính + CP dự phòng tồn kho thanh lý + CP khác (5 thành phần xem các dòng tương ứng bên dưới).",
     note="Các thành phần là chi phí ước tính theo AOP / định mức."),
 met("CP vận chuyển",
     "= phần trăm kế hoạch (theo AOP) của chỉ tiêu 'CP vận chuyển' × Doanh thu thực tế.", note=AOP_EST),
 met("CP bảo hành",
     "= phần trăm kế hoạch (theo AOP) của chỉ tiêu 'CP bảo hành' × Doanh thu thực tế.", note=AOP_EST),
 met("CP tài chính",
     "= phần trăm kế hoạch (theo AOP) của chỉ tiêu 'CP tài chính' × Doanh thu thực tế.", note=AOP_EST),
 met("CP khác",
     "= (số thứ tự ngày trong tháng của ngày được chọn) × (định mức 'chi phí khác' của THÁNG theo kế hoạch ÷ 30). Mẫu số 30 cố định.",
     note=AOP_EST),
 met("Thu nhập khác",
     "Doanh thu thuần của các dòng thuộc ngành 'Khác', lũy kế đến ngày chọn. Ngành 'Khác' = phần ngoài 4 ngành hàng chính (Water care, Home care, Cold & Hygiene care, Sanitary care). Ngành của mỗi dòng xác định theo phân loại ngành (CLASS) ghi trên dòng hóa đơn tại thời điểm phát sinh.",
     exc="Cùng phạm vi với Doanh thu.",
     note="Phần doanh thu ngành Khác này được CỘNG vào khi tính 'Lợi nhuận quản lý vận hành'."),
 met("Lợi nhuận quản lý vận hành", "= Lợi nhuận nhân viên − CP quản lý vận hành + Thu nhập khác."),
 met("CP dự phòng hoạt động năm trước", "= 21% × Lợi nhuận quản lý vận hành.",
     note="Định mức 21% cố định; áp trên Lợi nhuận quản lý vận hành của KỲ HIỆN TẠI (tên dòng theo nhãn báo cáo)."),
 met("Lợi nhuận trước thuế", "= Lợi nhuận quản lý vận hành − CP dự phòng hoạt động năm trước."),
 met("Lợi nhuận sau thuế",
     "= Nếu Lợi nhuận trước thuế > 0 thì giữ lại 80% (× 0,8); nếu ≤ 0 thì giữ nguyên.",
     note="Giữ lại 80% là QUY ƯỚC cố định trong báo cáo (không phải thuế suất thuế TNDN thực)."),
 met("Tỷ lệ Xanh/Đỏ",
     "Giá trị gốc = Doanh số nhóm Xanh ÷ Doanh số nhóm Đỏ (nếu Đỏ = 0 → để trống). Trên báo cáo, cột 'Giá trị thực tế' quy đổi thành % doanh số Xanh = Doanh số Xanh ÷ (Doanh số Xanh + Doanh số Đỏ) × 100.",
     exc="Chỉ sản phẩm có phân loại Xanh/Đỏ (mỗi SP luôn thuộc 1 trong 2)."),
 met("CP dự phòng tồn kho thanh lý", "= 1,5% × Doanh thu thực tế.",
     note="Định mức 1,5% cố định; là một thành phần của 'CP quản lý vận hành'."),
]

rb = {"workbook": "(KGR) BRD.BC01_Daily_Summary v1.1", "canvas": "BC01_Summary_TĐ",
      "viz": "view!9", "viz_title": "SUMMARY TẬP ĐOÀN", "is_summary": True, "rows": cols + mets}
os.makedirs(os.path.dirname(OUT), exist_ok=True)
json.dump(rb, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"wrote {OUT}: {len(cols)} cột + {len(mets)} chỉ tiêu")
