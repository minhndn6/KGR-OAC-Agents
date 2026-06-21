#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TDD P2.2 — kb_route: "ghi tri thức loại X vào đâu?" (D4, owner goal #1). ≥12 type, JSON, check-path, exit≠0 type lạ.
Chạy: PYTHONUTF8=1 python kb_lifecycle/tests/test_route.py"""
import os, sys, subprocess
from pathlib import Path

HERE = Path(__file__).resolve()
TOOLS = HERE.parents[1] / "tools"
sys.path.insert(0, str(TOOLS))
ENV = {**os.environ, "PYTHONUTF8": "1"}

PASS = FAIL = 0
def chk(c, l):
    global PASS, FAIL
    if c: PASS += 1; print(f"  PASS  {l}")
    else: FAIL += 1; print(f"  FAIL  {l}")

def run(script, *a):
    return subprocess.run([sys.executable, str(TOOLS / script), *a], capture_output=True, text=True, env=ENV)

def main():
    import kb_route as KR
    TYPES = ["new_dataset", "new_dataflow", "new_field", "physical_table", "fact",
             "formula_correction", "glossary_term", "convention", "governance_item",
             "gap", "drift", "correction", "lesson", "qa"]
    print(f"== classify mọi type ({len(TYPES)}) ==")
    chk(len(TYPES) >= 12, f"≥12 type ({len(TYPES)})")
    for t in TYPES:
        r = KR.classify(t)
        ok = r and r.get("target") and r.get("write_via") and isinstance(r.get("validate"), list) and r.get("kind")
        chk(bool(ok), f"classify {t}: đủ kind/target/write_via/validate")

    print("== routing đúng bản chất ==")
    chk(KR.classify("new_field")["write_via"] == "rebuild", "new_field -> rebuild (GENERATED, không sửa tay)")
    chk(KR.classify("new_dataset")["kind"] == "GENERATED", "new_dataset -> GENERATED")
    chk(KR.classify("glossary_term")["write_via"] == "direct-edit", "glossary_term -> direct-edit (CURATED)")
    gov = KR.classify("governance_item")
    chk(gov["kind"] == "CURATED" and ("ký" in gov.get("gate", "") or "owner" in gov.get("gate", "").lower()) and "auto" in gov.get("gate", "").lower(),
        "governance_item -> human sign-off, KHÔNG auto")
    chk(KR.classify("gap")["kind"] == "OPEN_QUESTION", "gap -> open question (KHÔNG promote thành fact)")
    chk(KR.classify("drift")["write_via"].startswith("drift"), "drift -> drift store (upsert)")
    chk(KR.classify("formula_correction")["kind"] == "GENERATED", "formula_correction -> GENERATED (fix nguồn+rebuild)")
    chk(KR.classify("không_tồn_tại") is None, "type lạ -> None")

    print("== check-path (file -> kind) ==")
    chk(KR.check_path("dataset_catalog.yaml")["kind"] == "GENERATED", "dataset_catalog.yaml -> GENERATED")
    chk("rebuild" in KR.check_path("field_dictionary.yaml")["write_via"], "field_dictionary.yaml -> rebuild")
    chk(KR.check_path("business_glossary.yaml")["kind"] == "CURATED", "business_glossary.yaml -> CURATED")
    chk(KR.check_path("learnings/log.jsonl")["kind"] == "LOG", "learnings/log.jsonl -> LOG")
    chk(KR.check_path("fields/_INDEX.md")["kind"] == "CURATED", "fields/_INDEX.md -> CURATED (không generated)")
    chk(KR.check_path("fields/Revenue_DT.md")["kind"] == "GENERATED", "fields/<name>.md -> GENERATED dossier")

    print("== CLI exit codes + JSON ==")
    r0 = run("kb_route.py", "classify", "--type", "new_field")
    chk(r0.returncode == 0 and "rebuild" in r0.stdout, "CLI classify hợp lệ -> exit 0 + JSON")
    r3 = run("kb_route.py", "classify", "--type", "bogus")
    chk(r3.returncode == 3, "CLI type lạ -> exit 3 (không misroute âm thầm)")
    cp = run("kb_route.py", "check-path", "dataset_catalog.yaml")
    chk(cp.returncode == 0 and "GENERATED" in cp.stdout, "CLI check-path -> exit 0")
    kg = run("kgr.py", "route", "classify", "--type", "glossary_term")
    chk(kg.returncode == 0 and "direct-edit" in kg.stdout, "`kgr route` ủy quyền sang kb_route OK")

    print(f"\n== TỔNG: PASS={PASS} FAIL={FAIL} ==")
    return 1 if FAIL else 0

if __name__ == "__main__":
    sys.exit(main())
