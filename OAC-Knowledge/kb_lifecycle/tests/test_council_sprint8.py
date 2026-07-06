#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Council Sprint-8 acceptance (TDD) — Vòng-2 C:

  R-E1  Dọn SỐ CỨNG khỏi KB (owner cấm "KB không lưu số tuyệt đối"):
        - grep khẳng định số kỳ cụ thể ĐÃ bỏ/nhãn ở MASTERY×2 + evals×2 + plan-template:
          445.043 / 713.262 / 586.292 / "period 42" / Canvas-BROKEN / 342.8B = 0 (chưa gắn nhãn).
        - GOTCHA cấu-trúc (tri-thức THIẾT KẾ) VẪN CÒN: "item-scope", "single-period" triệt fan-out,
          "713K vs 586K" mô-tả (không số tuyệt đối), "không grain Kênh".
        - hệ-số hợp-lệ GIỮ: 0.015 / rate 0.030 / a10 hằng-số P&L (có nhãn governance).

  R-H1  coverage_report.py — trần-autonomy: đọc capability_map + workbook_catalog + field_dictionary
        (+ dataset_catalog làm tổng) → % coverage + LIST vùng CHƯA map. THUẦN/tiêm-được (hermetic).
        + doctor có field 'coverage' (thông tin, KHÔNG lật STATUS).

Chạy: PYTHONUTF8=1 python kb_lifecycle/tests/test_council_sprint8.py
HERMETIC: coverage_report tiêm catalog giả. Ban đầu FAIL (chưa impl / chưa dọn)."""
import os, sys, json, importlib, subprocess
from pathlib import Path

WS = Path(os.environ.get("KGR_WORKSPACE") or r"C:\Project\KGR-OAC-Agents")
KB = WS / "OAC-Knowledge"
TOOLS = KB / "kb_lifecycle" / "tools"
sys.path.insert(0, str(TOOLS))

PASS = FAIL = 0
def chk(c, l):
    global PASS, FAIL
    if c: PASS += 1; print(f"  PASS  {l}")
    else: FAIL += 1; print(f"  FAIL  {l}")

def read(p):
    try: return Path(p).read_text(encoding="utf-8", errors="replace")
    except Exception: return ""

def _import(mod):
    try:
        if mod in sys.modules: del sys.modules[mod]
        return importlib.import_module(mod)
    except Exception as e:
        print(f"   import {mod} ERR: {e}")
        return None

DASH_MASTERY = WS / "Dashboard-builder" / "OAC_DASHBOARD_MASTERY.md"
FLOW_MASTERY = WS / "Dataflow-builder" / "OAC_DATAFLOW_MASTERY.md"
EVAL_BUILDER = WS / "Dashboard-builder" / ".claude" / "skills" / "oac-dashboard-builder" / "evals" / "evals.json"
EVAL_DESIGNER = WS / "Dashboard-builder" / ".claude" / "skills" / "oac-dashboard-designer" / "evals" / "evals.json"
PLAN_TMPL = WS / "Dashboard-builder" / ".claude" / "skills" / "oac-dashboard-builder" / "references" / "plan-template.md"

# ─────────────────────────────────────────────────────────────────────────────
# R-E1 — số kỳ cụ thể đã bỏ/nhãn; GOTCHA cấu-trúc còn nguyên
# ─────────────────────────────────────────────────────────────────────────────
def test_re1_numbers_removed():
    print("== R-E1  số cứng cụ thể đã bỏ/gắn-nhãn (grep=0) ==")
    # các token số cứng CẤM (dạng . và ,) — phải 0 lần trong mỗi file gated
    banned = ["445.043", "445,043", "713.262", "713,262", "586.292", "586,292",
              "342.8B", "342,8B", "period 42", "223.668M", "223,668M",
              "223,667,701,132", "342,817,830,186", "2,44 triệu",
              "313.894", "313,894", "192,9 tỷ", "300 tỷ"]
    files = {
        "DASH_MASTERY": read(DASH_MASTERY),
        "FLOW_MASTERY": read(FLOW_MASTERY),
        "EVAL_BUILDER": read(EVAL_BUILDER),
        "EVAL_DESIGNER": read(EVAL_DESIGNER),
        "PLAN_TMPL": read(PLAN_TMPL),
    }
    for name, txt in files.items():
        for tok in banned:
            chk(tok not in txt, f"{name}: KHÔNG còn '{tok}'")
    # "Canvas NN BROKEN" snapshot đã xóa khỏi FLOW_MASTERY
    import re
    chk(not re.search(r"canvas\s*\d+\s*broken", files["FLOW_MASTERY"], re.IGNORECASE),
        "FLOW_MASTERY: snapshot 'Canvas NN BROKEN' đã XÓA")
    chk(not re.search(r"\bperiod\s*4\d\b", files["DASH_MASTERY"], re.IGNORECASE),
        "DASH_MASTERY: 'period 4x' snapshot đã bỏ/nhãn")


def test_re1_gotchas_kept():
    print("== R-E1  GOTCHA cấu-trúc (tri-thức THIẾT KẾ) VẪN CÒN ==")
    dash = read(DASH_MASTERY)
    flow = read(FLOW_MASTERY)
    # item-scope: tri-thức "713K vs 586K = item-scope, không phải bug" — mô tả giữ, số bỏ
    chk("item-scope" in dash.lower() or "item scope" in dash.lower(),
        "DASH_MASTERY: gotcha 'item-scope' còn (giải thích 713K vs 586K)")
    chk("item-scope" in flow.lower() or "item scope" in flow.lower(),
        "FLOW_MASTERY: gotcha 'item-scope' còn")
    # single-period triệt fan-out
    chk("single-period" in flow.lower() and "fan-out" in flow.lower(),
        "FLOW_MASTERY: gotcha 'single-period triệt fan-out' còn")
    chk("fan-out" in dash.lower(), "DASH_MASTERY: diagnostics fan-out còn")
    # không grain Kênh (actual N/A) — tri-thức thiết-kế, giữ
    chk(("không có grain kênh" in flow.lower()) or ("không grain kênh" in flow.lower())
        or ("grain kênh" in flow.lower()),
        "FLOW_MASTERY: gotcha 'MEMO# không grain Kênh' còn")
    # màu Kangaroo (hex) giữ nguyên
    chk("#44BA46" in dash and "#F16522" in dash and "#636466" in dash,
        "DASH_MASTERY: hex màu Kangaroo giữ nguyên")
    # taxonomy config-number giữ (59 viz / 30 step)
    chk("59" in dash, "DASH_MASTERY: '59 loại viz' giữ (config đếm được, không phải số tiền)")
    chk("30 STEP" in flow or "30 step" in flow.lower(), "FLOW_MASTERY: '30 step' giữ")


def test_re1_coeffs_kept():
    print("== R-E1  hệ-số công-thức hợp-lệ GIỮ (a10/thuế/rate) ==")
    glo = read(KB / "business_glossary.yaml")
    # a10 hằng-số P&L: giữ nhưng có nhãn governance/số-cứng
    chk("a10" in glo, "business_glossary: a10 còn")
    chk(("governance" in glo.lower()) and (("số cứng" in glo.lower()) or ("hằng" in glo.lower())),
        "business_glossary: a10/thuế có nhãn governance + 'số cứng' (hằng-số hợp lệ, không tái dùng)")
    # thuế suất 0.21 (hệ số) giữ
    chk("0.21" in glo, "business_glossary: thuế suất 0.21 (hệ số) giữ")


def test_re1_gate_present():
    print("== R-E1  gate test_no_hard_numbers có + trong auto-discover ==")
    gate = KB / "kb_lifecycle" / "tests" / "test_no_hard_numbers.py"
    chk(gate.is_file(), "test_no_hard_numbers.py tồn tại (self-contained gate)")
    # run_all auto-discover test_*.py → gate tự vào (không cần sửa run_all)
    ra = read(KB / "kb_lifecycle" / "tests" / "run_all.py")
    chk('glob("test_*.py")' in ra or "glob('test_*.py')" in ra,
        "run_all.py auto-discover test_*.py (gate tự nạp)")
    # gate PHẢI xanh SAU khi dọn (chạy trực tiếp)
    env = {**os.environ, "PYTHONUTF8": "1"}
    r = subprocess.run([sys.executable, str(gate)], capture_output=True, text=True, env=env)
    chk(r.returncode == 0, f"gate test_no_hard_numbers PASS sau khi dọn (exit {r.returncode})")


# ─────────────────────────────────────────────────────────────────────────────
# R-H1 — coverage_report THUẦN/tiêm-được
# ─────────────────────────────────────────────────────────────────────────────
def test_rh1_pure():
    print("== R-H1  coverage_report.compute (hermetic, tiêm catalog giả) ==")
    cov = _import("coverage_report")
    chk(cov is not None and hasattr(cov, "compute_coverage"),
        "coverage_report.compute_coverage(capability_map, dataset_catalog, workbook_catalog, field_dictionary) tồn tại")
    if cov is None or not hasattr(cov, "compute_coverage"):
        return
    # catalog GIẢ: universe = 4 datasets; capability_map map 2; field_dict map 3; workbook 1
    capability_map = {"datasets": {"DS_A": {}, "DS_B": {}}}
    dataset_catalog = {"datasets": {"DS_A": {}, "DS_B": {}, "DS_C": {}, "DS_D": {}}}
    field_dictionary = {"datasets": {"DS_A": {}, "DS_B": {}, "DS_C": {}}}
    workbook_catalog = {"workbooks": {
        "WB1": {"n_datasources": 4, "n_datasources_used": 2, "n_canvases": 3},
    }}
    rep = cov.compute_coverage(capability_map, dataset_catalog, workbook_catalog, field_dictionary)

    ds = rep.get("datasets", {})
    chk(ds.get("total") == 4, f"total datasets = 4 (universe từ dataset_catalog) [{ds.get('total')}]")
    chk(ds.get("mapped_capability") == 2, f"mapped in capability_map = 2 [{ds.get('mapped_capability')}]")
    chk(abs(ds.get("pct_capability", 0) - 50.0) < 0.01, f"pct capability = 50% [{ds.get('pct_capability')}]")
    missing = set(ds.get("missing_capability") or [])
    chk(missing == {"DS_C", "DS_D"}, f"missing_capability = DS_C,DS_D [{sorted(missing)}]")
    chk(ds.get("mapped_field_dict") == 3, f"mapped in field_dictionary = 3 [{ds.get('mapped_field_dict')}]")
    fdmiss = set(ds.get("missing_field_dict") or [])
    chk(fdmiss == {"DS_D"}, f"missing_field_dict = DS_D [{sorted(fdmiss)}]")

    wb = rep.get("workbooks", {})
    chk(wb.get("total") == 1, "workbooks total = 1")
    chk(wb.get("datasources_total") == 4 and wb.get("datasources_used") == 2,
        "workbook datasource used/total = 2/4")

    # blind spots: list vùng CHƯA map để owner biết "dựng wb trên data chưa đụng"
    chk("DS_C" in json.dumps(rep, ensure_ascii=False) and "DS_D" in json.dumps(rep, ensure_ascii=False),
        "report liệt kê vùng mù (DS_C/DS_D) cho owner")

    # edge: universe rỗng → không chia 0
    empty = cov.compute_coverage({"datasets": {}}, {"datasets": {}}, {"workbooks": {}}, {"datasets": {}})
    chk(empty.get("datasets", {}).get("pct_capability") in (0, 0.0, None),
        "universe rỗng → pct=0/None (không ZeroDivision)")


def test_rh1_real_load():
    print("== R-H1  coverage_report chạy trên catalog THẬT (read-only) ==")
    cov = _import("coverage_report")
    if cov is None or not hasattr(cov, "load_and_compute"):
        chk(cov is not None and hasattr(cov, "load_and_compute"),
            "coverage_report.load_and_compute(kb_root=None) tồn tại (đọc catalog thật)")
        return
    rep = cov.load_and_compute(kb_root=str(KB))
    ds = rep.get("datasets", {})
    chk((ds.get("total") or 0) >= 20, f"đọc dataset_catalog thật, total>=20 [{ds.get('total')}]")
    chk(0 <= (ds.get("pct_capability") or 0) <= 100, "pct_capability trong [0,100]")
    chk(isinstance(ds.get("missing_capability"), list), "missing_capability là list (vùng mù)")
    # CLI chạy được, in JSON
    env = {**os.environ, "PYTHONUTF8": "1"}
    r = subprocess.run([sys.executable, str(TOOLS / "coverage_report.py")],
                       capture_output=True, text=True, env=env)
    chk(r.returncode == 0, f"coverage_report.py CLI exit 0 [{r.returncode}]")
    chk(("coverage" in (r.stdout or "").lower()) or ("pct" in (r.stdout or "").lower())
        or ("datasets" in (r.stdout or "").lower()),
        "CLI in báo cáo coverage (JSON)")


def test_rh1_doctor_wired():
    print("== R-H1  doctor có field 'coverage' (thông tin, KHÔNG lật STATUS) ==")
    kgrtxt = read(TOOLS / "kgr.py")
    chk("coverage" in kgrtxt, "kgr.py tham chiếu coverage")
    chk("coverage_report" in kgrtxt or "compute_coverage" in kgrtxt or "load_and_compute" in kgrtxt,
        "cmd_doctor nối coverage_report vào rep")
    # doctor chạy được + có field coverage + STATUS KHÔNG bị coverage lật
    env = {**os.environ, "PYTHONUTF8": "1"}
    r = subprocess.run([sys.executable, str(TOOLS / "kgr.py"), "doctor"],
                       capture_output=True, text=True, env=env)
    out = r.stdout or ""
    chk("coverage" in out.lower(), "doctor output có field coverage")
    try:
        rep = json.loads(out)
        chk("coverage" in rep, "doctor JSON có key 'coverage'")
        # coverage KHÔNG nằm trong công thức STATUS: dù coverage thấp, STATUS vẫn do các gate khác quyết
        # (kiểm gián tiếp: coverage có pct nhưng STATUS chỉ OK/ATTENTION theo clean/root/…)
        chk(rep.get("STATUS") in ("OK", "ATTENTION"), "doctor STATUS vẫn OK/ATTENTION hợp lệ")
    except Exception as e:
        chk(False, f"doctor output parse JSON được ({e})")


def main():
    test_re1_numbers_removed()
    test_re1_gotchas_kept()
    test_re1_coeffs_kept()
    test_re1_gate_present()
    test_rh1_pure()
    test_rh1_real_load()
    test_rh1_doctor_wired()
    print(f"\n== TỔNG Sprint-8: PASS={PASS} FAIL={FAIL} ==")
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
