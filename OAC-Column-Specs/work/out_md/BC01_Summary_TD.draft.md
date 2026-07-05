# RULE-BOOK CÔNG THỨC BÁO CÁO KGR

> Mô tả **cách tính (logic nghiệp vụ)** của từng cột và từng dòng chỉ tiêu trên báo cáo, để Kangaroo **xác nhận**. Sau khi xác nhận → đây là baseline; thay đổi sau này là change request. Cột **KGR xác nhận** điền Y/N.

## 0. Hướng dẫn & Thuật ngữ dùng chung

| Thuật ngữ | Định nghĩa |
|---|---|
| Doanh số (+VAT) | Tổng giá trị bán hàng đã bao gồm thuế GTGT (doanh số gộp). |
| Doanh thu | Doanh thu THUẦN (chưa gồm VAT) từ bán hàng, sau khi trừ trả hàng/ghi có; đã loại kênh nội bộ & giao dịch tranh chấp. |
| Giá vốn | Giá vốn hàng bán (COGS): tính theo 3 lớp ưu tiên (giá vốn mục tiêu → giá vốn tồn kho → dự phòng); hàng tặng và dòng chiết khấu tính giá vốn = 0. |
| Lợi nhuận gộp | = Doanh thu − Giá vốn. |
| CKKM | Chi phí chiết khấu/khuyến mãi thương mại (chi cho chương trình khuyến mãi). |
| AOP | Kế hoạch năm (Annual Operating Plan) — mức mục tiêu/định mức được phân bổ cho từng chỉ tiêu. Là số KẾ HOẠCH, không phải thực tế. |
| Ước tính theo AOP | Giá trị KHÔNG phải chi phí thực phát sinh, mà SUY RA từ kế hoạch AOP (tỷ lệ % trên doanh thu, hoặc phân bổ theo số ngày). Áp dụng cho nhiều dòng chi phí nằm DƯỚI 'Lợi nhuận gộp'. Khi đọc các dòng này cần hiểu là ước tính. |
| Xanh / Đỏ | Phân loại sản phẩm: Xanh (nhóm ưu tiên) và Đỏ. Mỗi sản phẩm luôn thuộc đúng 1 trong 2 nhóm. |
| Tỷ lệ Xanh/Đỏ | Tỷ lệ giữa doanh số sản phẩm nhóm Xanh và nhóm Đỏ. |
| Lũy kế (AsOfDate) | Cộng dồn từ đầu kỳ đến NGÀY được chọn ở bộ lọc trên canvas. Đổi ngày → đổi số lũy kế. |
| Kênh nội bộ | Kênh bán nội bộ trong tập đoàn — KHÔNG tính vào doanh thu/doanh số thực tế (bị loại trừ). |
| %/DS | Tỷ trọng tính theo phần trăm trên Doanh số (hoặc Doanh thu) — cho biết chỉ tiêu chiếm bao nhiêu phần trăm doanh số. |

## Báo cáo: (KGR) BRD.BC01_Daily_Summary v1.1
**Canvas:** BC01_Summary_TĐ  ·  **Viz:** SUMMARY TẬP ĐOÀN  ·  *(báo cáo tổng hợp — mô tả theo cả cột lẫn dòng chỉ tiêu)*

### A. Các CỘT giá trị (áp dụng cho mọi dòng)

| Cột / Chỉ tiêu | Cách tính (logic nghiệp vụ) | Loại trừ / Bộ lọc | Ghi chú | KGR xác nhận |
|---|---|---|---|---|
| **No.** | Số thứ tự dòng chỉ tiêu (1→25), cố định theo trình tự bảng lãi lỗ. | — | — | ☐ |
| **Tên chỉ tiêu** | Nhãn của dòng chỉ tiêu (chiều dòng của bảng). | — | — | ☐ |
| **Doanh số AOP** | Giá trị KẾ HOẠCH (AOP) của chỉ tiêu trong kỳ. | — | Là số kế hoạch, không phải thực tế. | ☐ |
| **%/DS AOP** | = Giá trị kế hoạch của chỉ tiêu ÷ Doanh số kế hoạch (ra %). | — | — | ☐ |
| **Giá trị thực tế** | = Lũy kế giá trị thực tế của chỉ tiêu (cộng dồn). RIÊNG dòng 'Tỷ lệ Xanh/Đỏ': hiển thị = % doanh số Xanh = Doanh số Xanh ÷ (Doanh số Xanh + Doanh số Đỏ) × 100. | Lũy kế đến ngày được chọn ở bộ lọc (AsOfDate). | — | ☐ |
| **%/ DS thực tế** | = Giá trị thực tế của chỉ tiêu ÷ Doanh thu thực tế (ra %). | Không áp dụng cho 3 dòng: Doanh số (+VAT), Doanh thu, Tỷ lệ Xanh/Đỏ → để trống. | — | ☐ |
| **Giá trị thiếu so với AOP** | = Doanh số AOP (kế hoạch của chỉ tiêu) − Giá trị thực tế. Dương = chưa đạt KH; với dòng chi phí, âm = chi VƯỢT kế hoạch. | Không áp dụng dòng Tỷ lệ Xanh/Đỏ → để trống. | — | ☐ |
| **%/DS (Thiếu so với AOP)** | = (Doanh số AOP − Giá trị thực tế) ÷ Doanh thu thực tế (ra %). | Không áp dụng 3 dòng: Doanh số (+VAT), Doanh thu, Tỷ lệ Xanh/Đỏ → để trống. | — | ☐ |

### B. Các DÒNG chỉ tiêu (mỗi dòng một công thức riêng)

| Cột / Chỉ tiêu | Cách tính (logic nghiệp vụ) | Loại trừ / Bộ lọc | Ghi chú | KGR xác nhận |
|---|---|---|---|---|
| **Doanh số (+VAT)** | Tổng doanh số bán hàng đã gồm thuế GTGT (lũy kế đến ngày chọn). | Loại kênh bán nội bộ, pháp nhân ngoài tập đoàn, giao dịch tranh chấp (HTL); chỉ giao dịch đã hạch toán doanh thu. | — | ☐ |
| **Doanh thu** | Doanh thu thuần (chưa gồm VAT) từ bán hàng, sau trả hàng/ghi có. | Loại kênh bán nội bộ, pháp nhân ngoài tập đoàn, giao dịch tranh chấp (HTL); chỉ giao dịch đã hạch toán doanh thu. | — | ☐ |
| **Giá vốn** | Giá vốn hàng bán: tính theo 3 lớp ưu tiên (giá vốn mục tiêu → giá vốn tồn kho → dự phòng). | Hàng tặng (free-gift) và dòng chiết khấu: giá vốn = 0. | — | ☐ |
| **Lợi nhuận gộp** | = Doanh thu − Giá vốn. | — | — | ☐ |
| **CP chiết khấu khuyến mại** | Tổng chi phí chiết khấu/khuyến mãi (CKKM) thực tế từ các chương trình khuyến mãi. | — | — | ☐ |
| **CP nhân viên KD** | = (tỷ lệ % kế hoạch của chỉ tiêu này theo AOP) × Doanh thu thực tế. | — | Ước tính theo kế hoạch AOP — KHÔNG phải chi phí thực phát sinh. | ☐ |
| **CP roadshow hội nghị** | = (tỷ lệ % kế hoạch theo AOP) × Doanh thu thực tế. | — | Ước tính theo kế hoạch AOP — KHÔNG phải chi phí thực phát sinh. | ☐ |
| **CP công tác tiếp khách KD** | = (tỷ lệ % kế hoạch theo AOP) × Doanh thu thực tế. | — | Ước tính theo kế hoạch AOP — KHÔNG phải chi phí thực phát sinh. | ☐ |
| **Lợi nhuận gộp Kinh doanh** | = Lợi nhuận gộp − CP chiết khấu khuyến mại − CP nhân viên KD − CP roadshow hội nghị − CP công tác tiếp khách KD. | — | Có trừ một số chi phí ước tính theo AOP (nhân viên KD / roadshow / công tác). | ☐ |
| **CP xúc tiến bán hàng** | = (số ngày trong tháng tính đến ngày chọn) × (định mức xúc tiến của THÁNG theo kế hoạch ÷ 30). | — | Ước tính theo AOP, phân bổ theo số ngày. | ☐ |
| **Lợi nhuận xúc tiến bán hàng** | = Lợi nhuận gộp Kinh doanh − CP xúc tiến bán hàng. | — | — | ☐ |
| **CP nhân viên BO** | = (số ngày trong tháng đến ngày chọn) × (định mức nhân viên back-office THÁNG ÷ 30). | — | Ước tính theo AOP, phân bổ theo số ngày. | ☐ |
| **Lợi nhuận nhân viên** | = Lợi nhuận xúc tiến bán hàng − CP nhân viên BO. | — | — | ☐ |
| **CP quản lý vận hành** | = CP vận chuyển + CP bảo hành + CP tài chính + CP dự phòng tồn kho thanh lý + CP khác (tổng nhóm chi phí vận hành). | — | Là dòng tổng hợp; các thành phần ước tính theo AOP. | ☐ |
| **CP vận chuyển** | = (tỷ lệ % kế hoạch theo AOP) × Doanh thu thực tế. | — | Ước tính theo kế hoạch AOP — KHÔNG phải chi phí thực phát sinh. | ☐ |
| **CP bảo hành** | = (tỷ lệ % kế hoạch theo AOP) × Doanh thu thực tế. | — | Ước tính theo kế hoạch AOP — KHÔNG phải chi phí thực phát sinh. | ☐ |
| **CP tài chính** | = (tỷ lệ % kế hoạch theo AOP) × Doanh thu thực tế. | — | Ước tính theo kế hoạch AOP — KHÔNG phải chi phí thực phát sinh. | ☐ |
| **CP khác** | = (số ngày trong tháng đến ngày chọn) × (định mức 'chi phí khác' THÁNG ÷ 30). | — | Ước tính theo AOP, phân bổ theo số ngày. | ☐ |
| **Thu nhập khác** | Doanh thu của ngành khác (ngoài 4 ngành hàng chính). | Giao dịch thuộc nhóm 'ngành khác'. | — | ☐ |
| **Lợi nhuận quản lý vận hành** | = Lợi nhuận nhân viên − CP quản lý vận hành + Thu nhập khác. | — | — | ☐ |
| **CP dự phòng hoạt động năm trước** | = 21% × Lợi nhuận quản lý vận hành. | — | Định mức 21% cố định trong cách tính. | ☐ |
| **Lợi nhuận trước thuế** | = Lợi nhuận quản lý vận hành − CP dự phòng hoạt động năm trước. | — | — | ☐ |
| **Lợi nhuận sau thuế** | = Nếu Lợi nhuận trước thuế > 0 thì giữ lại 80% (× 0,8); nếu ≤ 0 thì giữ nguyên. | — | Định mức 80% cố định trong cách tính. | ☐ |
| **Tỷ lệ Xanh/Đỏ** | Giá trị gốc = Doanh số nhóm Xanh ÷ Doanh số nhóm Đỏ (nếu Đỏ = 0 thì để trống). Trên báo cáo, cột 'Giá trị thực tế' quy đổi thành % doanh số Xanh = Doanh số Xanh ÷ (Doanh số Xanh + Doanh số Đỏ) × 100. | Chỉ sản phẩm có phân loại Xanh/Đỏ (mỗi SP luôn thuộc 1 trong 2). | — | ☐ |
| **CP dự phòng tồn kho thanh lý** | = 1,5% × Doanh thu thực tế. | — | Định mức 1,5% cố định; là một thành phần của 'CP quản lý vận hành'. | ☐ |
