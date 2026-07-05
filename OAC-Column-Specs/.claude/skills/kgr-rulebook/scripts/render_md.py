# -*- coding: utf-8 -*-
"""Render rule-book ra Markdown (nhanh, dễ sửa). Convert sang Excel ở bước cuối.
Dùng: python render_md.py <glossary.json> <out.md> <rulebook1.json> [rulebook2.json ...]"""
import json, sys

glo_path, out = sys.argv[1], sys.argv[2]
rbs = sys.argv[3:]

def esc(s):
    return (str(s) if s is not None else "").replace("|", "\\|").replace("\n", " ").strip() or "—"

L = []
glo = json.load(open(glo_path, encoding="utf-8"))
L += ["# RULE-BOOK CÔNG THỨC BÁO CÁO KGR", "",
      "> Mô tả **cách tính (logic nghiệp vụ)** của từng cột và từng dòng chỉ tiêu trên báo cáo, để Kangaroo **xác nhận**. "
      "Sau khi xác nhận → đây là baseline; thay đổi sau này là change request. Cột **KGR xác nhận** điền Y/N.", "",
      "## 0. Hướng dẫn & Thuật ngữ dùng chung", "",
      "| Thuật ngữ | Định nghĩa |", "|---|---|"]
for t in glo["terms"]:
    L.append(f"| {esc(t['term'])} | {esc(t['definition'])} |")
L.append("")

QA = False  # bật khi rulebook ở pha QA (có cột qa1_*)

def table(title, rows):
    if not rows:
        return
    L.append(f"### {title}")
    L.append("")
    if QA:
        L.append("| Cột / Chỉ tiêu | Cách tính (logic nghiệp vụ) | Loại trừ / Bộ lọc | Ghi chú | Cách tính (QA) | Loại trừ-Bộ lọc (QA) | Ghi chú (QA) | KGR xác nhận |")
        L.append("|---|---|---|---|---|---|---|---|")
        for r in rows:
            L.append(f"| **{esc(r['name'])}** | {esc(r['calc'])} | {esc(r.get('exclusions'))} | {esc(r.get('note'))} | {esc(r.get('qa1_calc'))} | {esc(r.get('qa1_exclusions'))} | {esc(r.get('qa1_note'))} | ☐ |")
    else:
        L.append("| Cột / Chỉ tiêu | Cách tính (logic nghiệp vụ) | Loại trừ / Bộ lọc | Ghi chú | KGR xác nhận |")
        L.append("|---|---|---|---|---|")
        for r in rows:
            L.append(f"| **{esc(r['name'])}** | {esc(r['calc'])} | {esc(r.get('exclusions'))} | {esc(r.get('note'))} | ☐ |")
    L.append("")

for rbp in rbs:
    rb = json.load(open(rbp, encoding="utf-8"))
    QA = bool(rb.get("qa_phase"))
    L.append(f"## Báo cáo: {rb['workbook']}")
    L.append(f"**Canvas:** {rb['canvas']}  ·  **Viz:** {rb.get('viz_title','')}  ·  *(báo cáo tổng hợp — mô tả theo cả cột lẫn dòng chỉ tiêu)*")
    L.append("")
    if rb.get("is_summary"):
        table("A. Các CỘT giá trị (áp dụng cho mọi dòng)", [r for r in rb["rows"] if r["block"] == "column"])
        table("B. Các DÒNG chỉ tiêu (mỗi dòng một công thức riêng)", [r for r in rb["rows"] if r["block"] == "metric"])
    else:
        secs = {}
        for r in rb["rows"]:
            secs.setdefault(r.get("section", "Các cột"), []).append(r)
        for sec, rws in secs.items():
            table(sec, rws)

open(out, "w", encoding="utf-8").write("\n".join(L))
print("wrote", out, "|", len(L), "lines")
