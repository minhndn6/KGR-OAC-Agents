#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GATE R-E1 — quét SỐ CỨNG (số tuyệt đối lớn / snapshot kỳ) trong các file KB auto-load.

Vì sao: owner cấm "KB lưu số tuyệt đối". Số kỳ cũ (445.043 / 713.262 / 586.292 / 342.8B, "period 42",
snapshot Canvas BROKEN) đóng-băng trong MASTERY/evals/plan-template → dựng "wall ảo" verify kỳ 43 bằng
số kỳ 42. Gate này FAIL nếu còn số cứng chưa XÓA/gắn-nhãn-kỳ trong:
  - Dashboard-builder/OAC_DASHBOARD_MASTERY.md
  - Dataflow-builder/OAC_DATAFLOW_MASTERY.md
  - OAC-Knowledge/... (MASTERY thứ 3 nếu có; ở đây = business_glossary a10 đã gắn nhãn governance)
  - Dashboard-builder/.claude/skills/oac-dashboard-builder/evals/evals.json
  - Dashboard-builder/.claude/skills/oac-dashboard-designer/evals/evals.json
  - Dashboard-builder/.claude/skills/oac-dashboard-builder/references/plan-template.md

SELF-CONTAINED (không import tool ngoài). ALLOWLIST cân bằng: giữ hệ-số nhỏ (0.0*/0.3*), version token
(v2/v3/a10), năm 2024-2026, hex màu (#44BA46), số cấu-hình đếm-được (59 viz / 30 node / ≤6 KPI),
và dòng có nhãn "LẤY LIVE" / "period=<" / "<kỳ>" / placeholder → KHÔNG chặn nhầm.

Chạy: PYTHONUTF8=1 python kb_lifecycle/tests/test_no_hard_numbers.py
"""
import os, re, sys
from pathlib import Path

WS = Path(os.environ.get("KGR_WORKSPACE") or r"C:\Project\KGR-OAC-Agents")

# ── các file bị GATE (auto-load / builder đọc mỗi phiên) ──────────────────────
SCANNED = [
    WS / "Dashboard-builder" / "OAC_DASHBOARD_MASTERY.md",
    WS / "Dataflow-builder" / "OAC_DATAFLOW_MASTERY.md",
    WS / "OAC-Knowledge" / "business_glossary.yaml",
    WS / "Dashboard-builder" / ".claude" / "skills" / "oac-dashboard-builder" / "evals" / "evals.json",
    WS / "Dashboard-builder" / ".claude" / "skills" / "oac-dashboard-designer" / "evals" / "evals.json",
    WS / "Dashboard-builder" / ".claude" / "skills" / "oac-dashboard-builder" / "references" / "plan-template.md",
]

# ── nhãn "đã hợp lệ hoá" 1 dòng → allowlist theo DÒNG ─────────────────────────
# Dòng có 1 trong các marker này = số đã được gắn-nhãn-kỳ / thay công thức / lấy-live → BỎ QUA.
LINE_ALLOW_MARKERS = (
    "lấy live", "lay live", "get_sfc_report", "period=<", "period = <", "<kỳ>", "<ky>",
    "<period", "=<p>", "period=<p", "governance", "số cứng", "so cung", "hằng-số-cứng",
    "hằng số cứng", "hang-so-cung", "hardcoded", "hard-number", "hard number",
    "không tái dùng", "khong tai dung", "no-hardcode", "no hardcode", "không hardcode",
    "khong hardcode",
)

# ── PATTERN số cứng cần bắt ───────────────────────────────────────────────────
# 1) golden cụ thể (dấu . hoặc , phân cách): 445.043 / 713.262 / 586.292 / 342.8B
GOLDEN_RE = re.compile(r"(?<!\d)(445|713|586)[.,]\d{3}(?!\d)")
GOLDEN_342 = re.compile(r"(?<!\d)342[.,]8\s*[Bb]\b")
# 2) số tuyệt đối lớn: ≥6 chữ số liền (223667701132) HOẶC nhóm phân-cách nghìn (342,817,830,186 / 247.258.890)
BIGNUM_PLAIN = re.compile(r"(?<!\d)\d{6,}(?:\.\d+)?(?!\d)")
BIGNUM_GROUPED = re.compile(r"(?<!\d)\d{1,3}(?:[.,]\d{3}){2,}(?:[.,]\d+)?(?!\d)")
# 3) "N tỷ" / "N triệu" với N là số có phần thập phân kỳ-cụ-thể (223,668M / 192,9 tỷ / 2,44 triệu / 213 tỷ)
TY_TRIEU = re.compile(r"(?<!\w)\d{1,4}(?:[.,]\d+)?\s*(?:tỷ|ty|triệu|trieu|[MB])\b")
# 4) "period NN" (snapshot kỳ cụ thể trong prose)
PERIOD_NN = re.compile(r"\bperiod\s*\d{2,}\b", re.IGNORECASE)
# 5) snapshot trạng thái workbook: "Canvas NN BROKEN", "N canvas ngày", "10 canvas"
CANVAS_BROKEN = re.compile(r"canvas\s*\d+\s*broken", re.IGNORECASE)

# ── ALLOWLIST cho từng match (chống false-positive hệ-số/version/năm/màu/config) ──
YEAR_RE = re.compile(r"^(19|20)\d{2}$")            # 2024/2025/2026
HEXNUM_RE = re.compile(r"[0-9a-fA-F]{6}")          # đứng sau '#': màu

def _match_allowed(m, line):
    """True nếu match này HỢP LỆ (không phải số cứng cấm)."""
    tok = m.group(0)
    low = line.lower()
    # dòng đã gắn nhãn hợp lệ hoá
    if any(mk in low for mk in LINE_ALLOW_MARKERS):
        return True
    # số nằm ngay sau '#': mã màu hex (vd #44BA46) hoặc tên workbook có #
    i = m.start()
    if i > 0 and line[i - 1] == "#":
        return True
    # version token: 'v2'/'v3'/'a10'/'a21' — chữ liền trước số
    if i > 0 and (line[i - 1].isalpha() or line[i - 1] == "_"):
        # vd 'a10', 'v3', 'BC03', 'DB01', 'MEMO_v2', 'ORA-00942' số đi sau chữ → định danh, không phải số tiền
        return True
    # năm
    digits = re.sub(r"[.,]", "", tok)
    if YEAR_RE.match(tok):
        return True
    return False


def scan_text(text):
    """Trả list (line_no, matched_token, line) các số cứng CẤM còn sót."""
    hits = []
    for ln, line in enumerate(text.splitlines(), 1):
        for rx in (GOLDEN_RE, GOLDEN_342, PERIOD_NN, CANVAS_BROKEN,
                   BIGNUM_GROUPED, BIGNUM_PLAIN, TY_TRIEU):
            for m in rx.finditer(line):
                if _match_allowed(m, line):
                    continue
                hits.append((ln, m.group(0), line.strip()[:120]))
    return hits


def main():
    total_hits = 0
    missing = 0
    print("== GATE R-E1: quét SỐ CỨNG trong file KB auto-load ==")
    for f in SCANNED:
        if not f.is_file():
            print(f"  WARN  không thấy file: {f}")
            missing += 1
            continue
        text = f.read_text(encoding="utf-8", errors="replace")
        hits = scan_text(text)
        rel = f.relative_to(WS)
        if hits:
            total_hits += len(hits)
            print(f"  FAIL  {rel} — {len(hits)} số cứng còn sót:")
            for ln, tok, line in hits[:20]:
                print(f"         L{ln}: <{tok}>  |  {line}")
            if len(hits) > 20:
                print(f"         ... (+{len(hits) - 20} nữa)")
        else:
            print(f"  PASS  {rel} — sạch số cứng")
    print(f"\n== TỔNG: {total_hits} số cứng còn sót (file thiếu: {missing}) ==")
    # file thiếu = cấu hình sai → cũng fail (INV: gate phải quét đủ)
    return 1 if (total_hits or missing) else 0


if __name__ == "__main__":
    sys.exit(main())
