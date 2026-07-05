# -*- coding: utf-8 -*-
"""
Áp kết quả QA vào rulebook JSON (thêm cột qa1_*; KHÔNG đụng cột gốc).
- mode qa1: từ file QA1 (reviews) → set qa1_calc/qa1_exclusions/qa1_note cho dòng "cần sửa"
  (dùng suggest; nếu có live_check mà chưa có suggest → đặt marker '⟂LIVE_CHECK: ...' để session resolve);
  dòng "OK"/không có review → "(Giữ nguyên)". Set qa_phase=true.
- mode qa2: từ file QA2 (edits) → ghi đè qa1_* bằng bản trau chuốt.
Dùng: python qa_apply.py --mode qa1|qa2 --rulebook <rb.json> --qa <qa.json>
Khớp dòng theo (section, name); nếu QA không nêu section → khớp theo name.
"""
import json, argparse

ap = argparse.ArgumentParser()
ap.add_argument("--mode", required=True)
ap.add_argument("--rulebook", required=True)
ap.add_argument("--qa", required=True)
a = ap.parse_args()

rb = json.load(open(a.rulebook, encoding="utf-8"))
qa = json.load(open(a.qa, encoding="utf-8"))
rows = rb["rows"]


def find(name, section):
    name = (name or "").strip()
    if section:
        sec = section.strip()
        m = [r for r in rows if (r.get("name") or "").strip() == name and (r.get("section") or "").strip() == sec]
        if m:
            return m
    return [r for r in rows if (r.get("name") or "").strip() == name]


n = 0
if a.mode == "qa1":
    rb["qa_phase"] = True
    for v in qa.get("reviews", []):
        if v.get("verdict") != "cần sửa":
            continue
        s = v.get("suggest") or {}
        lc = (v.get("live_check") or "").strip()
        for row in find(v.get("name"), v.get("section")):
            calc = (s.get("calc") or "").strip()
            row["qa1_calc"] = calc or (("⟂LIVE_CHECK: " + lc) if lc else "(Giữ nguyên)")
            row["qa1_exclusions"] = (s.get("exclusions") or "").strip() or "(Giữ nguyên)"
            row["qa1_note"] = (s.get("note") or "").strip() or "(Giữ nguyên)"
            row["_qa1_issues"] = v.get("issues")
            n += 1
    for r in rows:  # dòng chưa được QA1 đụng tới
        r.setdefault("qa1_calc", "(Giữ nguyên)")
        r.setdefault("qa1_exclusions", "(Giữ nguyên)")
        r.setdefault("qa1_note", "(Giữ nguyên)")
elif a.mode == "qa2":
    for e in qa.get("edits", []):
        for row in find(e.get("name"), e.get("section")):
            for f in ("qa1_calc", "qa1_exclusions", "qa1_note"):
                if e.get(f):
                    row[f] = e[f]
            n += 1

json.dump(rb, open(a.rulebook, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"{a.mode}: áp {n} dòng; qa_phase={rb.get('qa_phase')}")
pending = [r.get("name") for r in rows if "⟂LIVE_CHECK" in (str(r.get("qa1_calc", "")) + str(r.get("qa1_note", "")))]
if pending:
    print("LIVE_CHECK còn treo:", pending)
