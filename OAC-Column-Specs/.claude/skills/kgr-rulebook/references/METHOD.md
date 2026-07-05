# PHƯƠNG THỨC MÔ TẢ LOGIC TÍNH (chuẩn để Kangaroo duyệt)

> Tài liệu này định nghĩa **CÁCH VIẾT cột "Cách tính" và "Loại trừ/Bộ lọc"** cho rule-book, sao cho **phía tài chính Kangaroo đọc vào là confirm được logic** (biết lấy con số nào, ở đâu, nhân/trừ với cái gì, fallback ra sao) mà KHÔNG cần đọc code/dataflow. Duyệt phương thức này xong sẽ áp dụng cho toàn bộ cột của 2 báo cáo.

## 1. Nguyên tắc nguồn
- Logic lấy từ **định nghĩa dataflow LIVE** (def) + **định nghĩa viz LIVE** (projects/json). KHÔNG suy công thức từ truy vấn SQL gộp (dễ sai do auto-aggregate/lũy kế).
- **Live = đúng** — mô tả phản ánh trung thực cơ chế đang chạy, không phán xét/không gắn cờ-lỗi.
- Mô tả bằng **ngôn ngữ nghiệp vụ**; khi cần chỉ nguồn thì gọi tên **nghiệp vụ trong ngoặc kép** ("bảng Giá vốn mục tiêu", "kế hoạch AOP"), KHÔNG dùng tên field/bảng kỹ thuật (BASE_REVENUE, DW_NS_…).

## 2. Chuẩn cột "Cách tính" — phải trả lời ĐỦ 5 ý (theo thứ tự)
1. **Công thức tổng**: nêu phép tính gốc — `= A − B`, `= X × Y`, hoặc các bước có đánh số.
2. **Mỗi thành phần lấy từ đâu + TRA THEO KHOÁ NÀO**: nguồn nghiệp vụ + khoá tra cứu (vd "tra theo mã sản phẩm + tháng"), kỳ áp dụng (vd "kỳ liền trước").
3. **Thứ tự ưu tiên / FALLBACK**: nếu nguồn 1 trống thì sang nguồn 2…, cuối cùng giá trị thay thế (vd "= 50% doanh thu").
4. **Quy ước dấu / đơn vị**: credit memo lấy dấu âm; dùng |số lượng|; kết quả là số tiền/%/tỷ lệ.
5. **Trường hợp đặc biệt / NULL**: vd hàng tặng = 0, dòng chiết khấu = 0, mẫu số = 0 thì để trống.

**Bổ sung bắt buộc (từ vòng review):**
- **Giải thích mọi mã/viết tắt ngay tại chỗ**: vd "HTL = Hàng thanh lý", "VU1 = pháp nhân Kangaroo Quốc tế". Người tài chính không phải tra cứu thêm.
- **Nêu rõ quy ước CỐ ĐỊNH + lý do**: vd "chia cho 30 là quy ước phân bổ đều, KHÔNG theo số ngày thực của tháng".
- **Nhận diện bộ lọc bằng dấu hiệu nghiệp vụ cụ thể**: vd "giao dịch ĐÃ hạch toán (đã ghi sổ kế toán kỳ đó)", "khách hàng được đánh dấu ký gửi", "dòng có vụ việc = Hàng thanh lý".
- **Với chỉ tiêu PHÁI SINH** (hiệu/tổng của chỉ tiêu khác): nói rõ **cùng phạm vi/kỳ/bộ lọc** với các chỉ tiêu nguồn, và **grain** (tổng hợp cấp tập đoàn — không khớp lại theo từng dòng hóa đơn).
- **Với chỉ tiêu PHÂN BỔ/DẪN XUẤT từ một giá trị nhóm/tập đoàn** (vd phân bổ chi phí tập đoàn về ngành): phải định nghĩa NGAY nguồn của **số gốc nhóm/tập đoàn** (lấy ở đâu, kỳ nào, loại trừ gì) hoặc trỏ tới dòng đã định nghĩa — KHÔNG để ẩn số gốc. Nếu chỉ ghi "× tỷ trọng" mà không nói số gốc tính sao → CHƯA ĐẠT.

**Tiêu chí ĐẠT (bắt buộc):** một người tài chính KGR đọc xong **tự tái lập được một dòng số** mà không phải hỏi "lấy cái gì nhân cái gì / nếu thiếu thì sao". Nếu còn phải hỏi → CHƯA ĐẠT, viết lại.

## 3. Chuẩn cột "Loại trừ / Bộ lọc" — dùng ĐÚNG từ vựng + GIÁ TRỊ cụ thể của KGR
- Nêu **giá trị thật**, không paraphrase mơ hồ:
  - Phạm vi pháp nhân: **"chỉ lấy 2 pháp nhân: Kangaroo Quốc tế (VU1) và Chi nhánh HCM"** (KHÔNG viết "ngoài tập đoàn").
  - **"loại hàng thanh lý (HTL)"**, **"loại khách ký gửi"**, **"loại kênh nội bộ"**, **"chỉ giao dịch đã hạch toán"**.
- Nếu một bộ lọc chỉ áp dụng cho vài dòng/chỉ tiêu → nói rõ dòng nào.

## 4. Ví dụ chuẩn (đối chiếu CŨ → MỚI)

**a) Giá vốn**
- ❌ CŨ (sơ sài): "tính theo 3 lớp ưu tiên (mục tiêu → tồn kho → dự phòng)."
- ✅ MỚI: *Giá vốn hàng bán của một dòng = **đơn giá vốn × số lượng (|SL|)**. Đơn giá vốn lấy theo 3 lớp ưu tiên: **(1)** "Giá vốn mục tiêu" — tra theo **mã sản phẩm (MSP) + tháng** của giao dịch; nếu có thì dùng. **(2)** Nếu không có → "Giá vốn tồn kho" — tra theo **mã item + pháp nhân + kỳ**; nếu có thì dùng. **(3)** Nếu vẫn không có → **= 50% doanh thu thực tế của dòng**. Quy ước: dòng điều chỉnh giảm (credit memo) lấy **dấu âm**; **hàng tặng** mà doanh thu = 0 → giá vốn = 0; **dòng chiết khấu** → giá vốn = 0.*

**b) Doanh thu** (đã nâng theo review)
- ✅ MỚI: *Tổng **doanh thu thuần (chưa VAT)** của các dòng hóa đơn bán hàng, **hợp nhất** với chứng từ điều chỉnh giảm (credit memo). Cách tính 1 dòng: lấy doanh thu gốc chưa VAT của dòng (giá bán đã trừ chiết khấu trên hóa đơn; các dòng chiết khấu là dòng riêng) **× dấu** (hóa đơn bán = +, credit memo = −); cộng dồn theo kỳ. Chỉ lấy phát sinh thuộc **tài khoản doanh thu**.* — **Loại trừ:** *chỉ 2 pháp nhân "CTCP LD Kangaroo Quốc tế" (VU1) và "Chi nhánh HCM"; chỉ giao dịch **đã hạch toán** (đã ghi sổ kế toán kỳ tương ứng); loại dòng có **vụ việc = Hàng thanh lý (HTL)**; loại **khách hàng được đánh dấu ký gửi**; loại giao dịch thuộc **kênh nội bộ**.*

**c) CP nhân viên BO** (ví dụ chính bạn nêu — đã nâng theo review)
- ✅ MỚI: *Chi phí nhân viên back-office — **ước tính theo kế hoạch, phân bổ theo ngày**. = **(số thứ tự ngày trong tháng của ngày được chọn — ví dụ chọn 16/05 → 16) × (định mức chi phí nhân viên BO của THÁNG theo kế hoạch ÷ 30)**. Mẫu số **30 là quy ước cố định** (luôn 30, KHÔNG đổi theo số ngày thực của tháng). "Định mức tháng" lấy từ **kế hoạch AOP loại "kế hoạch chi phí", năm hiện hành, cấp tập đoàn**, theo đúng chỉ tiêu "CP nhân viên BO". Nếu tháng đó **không có định mức kế hoạch → chi phí = 0**. Đây là **chi phí ƯỚC TÍNH** (phân bổ kế hoạch), KHÔNG phải chi phí thực phát sinh.*

**d) Lợi nhuận gộp** (chỉ tiêu phái sinh — đã nâng theo review)
- ✅ MỚI: *= **Doanh thu − Giá vốn**, trong đó Doanh thu và Giá vốn là 2 chỉ tiêu cùng bảng, **cùng phạm vi pháp nhân/kỳ/bộ lọc** (như mô tả ở 2 chỉ tiêu đó) và **cùng lũy kế đến ngày được chọn**. Là hiệu của 2 dòng đã **tổng hợp cấp tập đoàn** (không khớp lại theo từng dòng hóa đơn).*

## 5. Quy trình REVIEW khách quan (sub-agent đóng vai tài chính Kangaroo)
- Sau khi soạn mô tả một báo cáo, gọi **sub-agent "Reviewer tài chính KGR"**: agent này **KHÔNG được xem dataflow/def**, chỉ đọc bản mô tả như một người tài chính, chấm theo **rubric** (mục 6). Mục tiêu: phát hiện chỗ mô tả còn mơ hồ/thiếu, **trước khi** đưa Kangaroo.
- Mỗi dòng → verdict **ĐẠT / CHƯA ĐẠT** + (nếu chưa đạt) **câu hỏi mà người tài chính vẫn phải hỏi**. Dòng CHƯA ĐẠT → tác giả viết lại → review lại, lặp tới khi 100% ĐẠT.
- Đây là cổng chất lượng KHÁCH QUAN (người chấm ≠ người viết), bổ sung cho harness máy (coverage/no-leak…).

## 6. Rubric chấm độ rõ (mỗi mô tả)
1. **Tự tái lập được?** Người tài chính có thể tự tính 1 dòng số từ mô tả không? (không/được)
2. **Đủ nguồn + khoá?** Mỗi thành phần có nói rõ lấy ở đâu, tra theo khoá nào, kỳ nào? 
3. **Có fallback/đặc biệt?** Nêu rõ thứ tự ưu tiên + trường hợp thiếu/NULL?
4. **Loại trừ cụ thể?** Dùng giá trị/từ vựng KGR thật, không mơ hồ?
5. **Không thuật ngữ kỹ thuật khó hiểu?** Không có tên field/bảng hệ thống?
→ ĐẠT khi cả 5 ý "có". Bất kỳ ý "không" → CHƯA ĐẠT + ghi câu hỏi còn vướng.

## 7. Test case cho reviewer (hiệu chỉnh để chấm đúng tay)
- **Mẫu ĐẠT**: mô tả Giá vốn (mục 4a) → reviewer phải chấm ĐẠT.
- **Mẫu CHƯA ĐẠT**: "Giá vốn: tính theo 3 lớp ưu tiên (mục tiêu → tồn kho → dự phòng)" → reviewer phải chấm CHƯA ĐẠT và hỏi: "lấy đơn giá ở đâu, tra theo gì, fallback bao nhiêu %?".
- Reviewer chấm sai 2 mẫu mồi này → loại bỏ kết quả, chỉnh prompt reviewer.
