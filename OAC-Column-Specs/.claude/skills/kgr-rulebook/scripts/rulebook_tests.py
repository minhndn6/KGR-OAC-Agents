# -*- coding: utf-8 -*-
"""
Rule-book ACCEPTANCE HARNESS — test-case CHUNG (mục 8a). Schema v2 (theo yêu cầu user):
  rulebook.json : {workbook, canvas, viz, is_summary, rows:[
                    {block:"column"|"metric", name, calc, exclusions, note,
                     evidence:{skeleton_ref}}]}
  skeleton.json : (từ build_skeleton.py)
  glossary.json : {terms:[{term,definition}], must_define:[...]}
Kiểm: coverage (đủ cột), grounding (mọi dòng có 'calc'), no_field_leak (không lộ field gốc),
required (name+calc), glossary (thuật ngữ bắt buộc được định nghĩa). KHÔNG còn 'trạng thái'.
Dùng: python rulebook_tests.py --skeleton s.json --rulebook r.json [--glossary g.json] | --selftest
"""
import json, re, sys, argparse, io

USER_FACING = ["name", "calc", "exclusions", "note"]
REQUIRED = ["name", "calc"]
TECH_LEAK = re.compile(
    r"(DW_NS_|DW_X_|XSA\(|_LINES_F|_HEADERS|DTF_CALC|KGR_DS_|KGR_DF_|BASE_REVENUE|BASE_AMOUNT|"
    r'BASE_QUANTITY|TD_Report_|Nganh_Report_|\."Columns"\.|ACCTTYPE|ISPOSTING|POSTINGPERIOD|'
    r"Actual_Amount|AOP_Amount_1|AOP_PER_A|AOP_AMT_A|Metric_Code|DT_grain|DT_TĐ|a5_CP|a3_Giá)")


def _canvas_refs(skel, canvas):
    refs = set()
    for c in skel.get("canvases", []):
        if c.get("canvas") != canvas:
            continue
        for v in c.get("vizzes", []):
            for col in v.get("columns", []):
                refs.add(f"{v['viz']}::{col['col_id']}")
    return refs


def check_coverage(skel, rb):
    refs = _canvas_refs(skel, rb.get("canvas"))
    referenced = set()
    for r in rb.get("rows", []):
        ev = r.get("evidence", {})
        if ev.get("skeleton_ref"):
            referenced.add(ev["skeleton_ref"])
        for x in (ev.get("skeleton_refs") or []):  # 1 dòng phủ nhiều viz giống nhau (vd 4 pivot ngành)
            referenced.add(x)
    missing, orphan = refs - referenced, referenced - refs
    msgs = []
    if not refs:
        msgs.append("skeleton rỗng cho canvas này")
    if missing:
        msgs.append(f"{len(missing)} cột live CHƯA có dòng: {sorted(missing)[:8]}")
    if orphan:
        msgs.append(f"{len(orphan)} dòng trỏ cột không tồn tại: {sorted(orphan)[:8]}")
    return (not msgs, msgs)


def check_grounding(rb):
    bad = [i for i, r in enumerate(rb.get("rows", [])) if not str(r.get("calc", "")).strip()]
    return (not bad, [f"{len(bad)} dòng thiếu 'calc' (cách tính): rows {bad[:10]}"] if bad else [])


def check_no_leak(rb):
    hits = []
    for i, r in enumerate(rb.get("rows", [])):
        for f in USER_FACING:
            v = r.get(f)
            if v and TECH_LEAK.search(str(v)):
                hits.append((i, f, TECH_LEAK.search(str(v)).group(0)))
    return (not hits, [f"Lộ field-gốc ở cột user-facing: {hits[:10]}"] if hits else [])


def check_required(rb):
    bad = [(i, f) for i, r in enumerate(rb.get("rows", [])) for f in REQUIRED if not str(r.get(f, "")).strip()]
    return (not bad, [f"Thiếu trường bắt buộc: {bad[:12]}"] if bad else [])


def check_glossary(rb, glo):
    if not glo:
        return (True, ["(bỏ qua — chưa cấp glossary.json)"])
    defined = {t["term"].strip().lower() for t in glo.get("terms", [])}
    missing = [t for t in glo.get("must_define", []) if t.strip().lower() not in defined]
    return (not missing, [f"Glossary thiếu: {missing}"] if missing else [])


def run(skel, rb, glo=None):
    return [("coverage",) + check_coverage(skel, rb),
            ("grounding",) + check_grounding(rb),
            ("no_field_leak",) + check_no_leak(rb),
            ("required_fields",) + check_required(rb),
            ("glossary",) + check_glossary(rb, glo)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--skeleton"); ap.add_argument("--rulebook"); ap.add_argument("--glossary")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    skel = json.load(open(a.skeleton, encoding="utf-8"))
    rb = json.load(open(a.rulebook, encoding="utf-8"))
    glo = json.load(open(a.glossary, encoding="utf-8")) if a.glossary else None
    allok = True
    print(f"== Harness · {rb.get('workbook','?')} / {rb.get('canvas','?')} · {len(rb.get('rows',[]))} dòng ==")
    for name, ok, msgs in run(skel, rb, glo):
        print(f"[{'PASS' if ok else 'FAIL'}] {name}")
        if not ok:
            for m in msgs:
                print("       -", m)
        allok = allok and ok
    print("=" * 40)
    print("RESULT:", "ALL PASS ✅" if allok else "FAIL ❌")
    sys.exit(0 if allok else 1)


def selftest():
    skel = {"canvases": [{"canvas": "C1", "vizzes": [{"viz": "v1", "columns": [
        {"col_id": "a"}, {"col_id": "b"}]}]}]}
    good = {"canvas": "C1", "is_summary": False, "rows": [
        {"block": "column", "name": "X", "calc": "= P − Q", "exclusions": "—", "note": "",
         "evidence": {"skeleton_ref": "v1::a"}},
        {"block": "column", "name": "Y", "calc": "tổng doanh số", "exclusions": "—", "note": "",
         "evidence": {"skeleton_ref": "v1::b"}}]}
    assert all(ok for _, ok, _ in run(skel, good)), [x for x in run(skel, good) if not x[1]]
    bad_skel = json.loads(json.dumps(skel))
    bad_skel["canvases"][0]["vizzes"][0]["columns"].append({"col_id": "c"})  # coverage
    bad = json.loads(json.dumps(good))
    bad["rows"][0]["calc"] = ""                       # grounding + required
    bad["rows"][1]["calc"] = "lấy XSA('x'.'y')"       # no_leak
    failed = {n for n, ok, _ in run(bad_skel, bad) if not ok}
    assert {"coverage", "grounding", "no_field_leak", "required_fields"} <= failed, failed
    print("SELFTEST PASS ✅ — bắt được:", sorted(failed))
    sys.exit(0)


if __name__ == "__main__":
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    except Exception:
        pass
    main()
