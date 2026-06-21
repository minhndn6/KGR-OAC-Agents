# TỒN ĐỌNG — việc cần OWNER xử lý

> Tổng hợp 2026-06-21 sau khi chạy hết phần tự động (offline UAT 209 + live UAT). Mọi phần KHÔNG cần owner đã xong.
> Trạng thái hệ: `kb_lifecycle/` đầy đủ Phase 0–4; DoD 9/9 có bằng chứng (DoD6 có live evidence). Đã push GitHub.

## 🔴 Ưu tiên cao (rủi ro/khoá tính năng)
1. **G1 — Ký GR1–GR7** (nghiệp vụ tài chính). Ngồi với kế toán, mỗi mục quyết **"cố ý giữ"** hay **"bug phải sửa"**:
   - GR1 lợi nhuận dưới-gộp = mô hình AOP (không phải thực ghi sổ) · GR2 hằng số CP xúc tiến 247.258.890 nhúng cứng · GR3 thuế ×0,21 cứng · GR4 doanh thu Tập đoàn lọc whitelist 2 pháp nhân · GR5 'Kênh nội bộ' IN('T') nghĩa chưa rõ · GR6 định nghĩa Revenue OAC≠NSAW · GR7 producer "sống" của dataset đa-producer.
   - Đây là **rủi ro tài chính lớn nhất** (số lãnh đạo đang nhìn) + chặn promote governance tự động cho tới khi ký.
2. **Bảo mật repo GitHub**: đặt repo `minhndn6/KGR-OAC-Agents` → **Private**; **đổi mật khẩu OAC** (đang plaintext trong `.secrets/oac.env`, đã gitignore nhưng nên rotate).

## 🟡 Nên làm (tiện lợi / dọn dẹp)
3. **Token OAC hay phải login lại sau tắt máy**: fix gốc = nới vòng đời token/session ở **OAC IDCS** (admin Console). Token-file chỉ "mồi 1 lần" (server xóa sau khi đọc). Chi tiết cơ chế: memory `oac-live-read-channel`.
4. **Gỡ hẳn `nsaw-oac-poc`** khỏi Claude Code: `claude mcp remove nsaw-oac-poc` (đã cấm qua memory + CLAUDE.md, nhưng config server nằm ngoài file sửa tay được).
5. **Review + promote pending learnings**: `python OAC-Knowledge/kb_lifecycle/tools/learn2.py list pending` → có L0006 (producer sống — cần owner), L0010/L0012/L0013 (lesson/correction), v.v. Promote theo typed-gate (governance/convention cần owner ký).

## 🟢 Tùy chọn (giá trị biên thấp / kỹ thuật)
6. **Live UAT exhaustive** (nếu muốn): hiện đã verify existence 63/63 + queryability 17/17 closure + structure 3 P&L. Chưa transcribe đủ 477 cột riêng lẻ (giới hạn kênh MCP: trả về context + mojibake metadata). Nếu cần từng-cột, làm thêm describe per dataset (tốn token).
7. **Hợp nhất `learn.py` ↔ `learn2.py`**: hiện skill gọi `learn.py` (cũ), `learn2.py` là bản hardened. Nên cho skill chuyển sang learn2 rồi bỏ learn.py (cần sync bản cài `~/.claude`).
8. **P0.3 EXTRACT_DATE**: pipeline build còn hằng số ngày trích cứng ở 3 builder — gom về 1 manifest khi tiện (chuẩn bị cho rebuild reproducible).
9. **Lan rule sang builder SKILL.md**: ban nsaw-oac-poc + dùng `kgr_runtime.scratch()` mới có ở workspace CLAUDE.md; có thể nhắc lại trong từng SKILL.md builder (cẩn thận qa_full S7 sync khi sửa SKILL.md đồng bộ ~/.claude).

## Đã xác minh — KHÔNG cần làm gì
- `(KGR) DTF_CALC_MIS`: ban đầu nghi "mất live" (L0011) nhưng **xác minh lại CÓ tồn tại + query được (294.294 rows)** — KB đúng; chỉ `discover_data` list thiếu nó. L0011 đã được sửa (correction trong log). Không cần sửa catalog.
