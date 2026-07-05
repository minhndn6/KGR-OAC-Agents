#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TDD — hygiene_lib.classify: guard Write/Edit (Hybrid) đưa scratch/state ra NGOÀI cây, cấm sửa GENERATED.
Chạy: PYTHONUTF8=1 python kb_lifecycle/tests/test_hooks.py"""
import sys, tempfile, shutil
from pathlib import Path

HERE = Path(__file__).resolve()
WS_REAL = HERE.parents[3]                                  # <ws>/OAC-Knowledge/kb_lifecycle/tests -> <ws>
sys.path.insert(0, str(WS_REAL / ".claude" / "hooks"))    # hygiene_lib

PASS = FAIL = 0
def chk(c, l):
    global PASS, FAIL
    if c: PASS += 1; print(f"  PASS  {l}")
    else: FAIL += 1; print(f"  FAIL  {l}")

RULES = {"deny_glob": ["_PNL_*", "_snap_*", "*.network-response", "*.lock"], "deny_pyc": True}

def main():
    import hygiene_lib as H
    tmp = Path(tempfile.mkdtemp(prefix="kgr_hook_"))
    try:
        ws = tmp / "KGR-OAC-Agents"
        (ws / "OAC-Knowledge").mkdir(parents=True)
        (ws / "OAC-Knowledge" / "learnings").mkdir()
        (ws / "OAC-Knowledge" / "raw").mkdir()
        (ws / "Dashboard-builder").mkdir()
        (ws / ".claude").mkdir()
        gen = (ws / "OAC-Knowledge" / "dataflow_catalog.yaml"); gen.write_text("x", encoding="utf-8")
        generated_abs = {gen.resolve()}

        def v(path):
            return H.classify(path, ws, RULES, generated_abs)[0]

        print("== NGOÀI cây → allow ==")
        chk(v(tmp / "_kgr-state" / "work" / "Dashboard-builder" / "note.md") == "allow", "_kgr-state (sibling) → allow")
        chk(v(Path(tempfile.gettempdir()) / "whatever.md") == "allow", "path ngoài workspace → allow")

        print("== scratch/state trong cây → deny_junk (redirect ra ngoài) ==")
        chk(v(ws / "Dashboard-builder" / "_work" / "x.md") == "deny_junk", "<repo>/_work/ → deny_junk")
        chk(v(ws / "_orchestration" / "blackboards" / "bb.json") == "deny_junk", "_orchestration/ → deny_junk")
        chk(v(ws / "_PNL_report.md") == "deny_junk", "_PNL_* (deny_glob) → deny_junk")
        chk(v(ws / "Dashboard-builder" / "_snap_1.png") == "deny_junk", "_snap_* → deny_junk")
        chk(v(ws / "OAC-Knowledge" / "resp.network-response") == "deny_junk", "*.network-response → deny_junk")

        print("== file GENERATED → deny_generated ==")
        chk(v(gen) == "deny_generated", "trong generated_manifest → deny_generated")
        ban = ws / "OAC-Knowledge" / "some_gen.md"; ban.write_text("# GENERATED do-not-edit\n", encoding="utf-8")
        chk(v(ban) == "deny_generated", "banner '# GENERATED' → deny_generated")

        print("== source/config/log hợp lệ trong cây → allow ==")
        chk(v(ws / "OAC-Knowledge" / "learnings" / "log.jsonl") == "allow", "learnings/ (append-log) → allow")
        chk(v(ws / "OAC-Knowledge" / "raw" / "build_x.py") == "allow", "raw/ (source) → allow")
        chk(v(ws / "OAC-Knowledge" / "business_glossary.yaml") == "allow", "curated yaml (không generated) → allow")
        chk(v(ws / ".claude" / "settings.json") == "allow", ".claude/ config → allow")
        chk(v(ws / "OAC-Knowledge" / "kb_lifecycle" / "tools" / "kgr.py") == "allow", "source .py → allow")

        print("== FAIL-OPEN: rules None / generated None không crash ==")
        try:
            r = H.classify(ws / "OAC-Knowledge" / "x.yaml", ws, None, None)
            chk(r[0] == "allow", "rules/generated None → allow, không raise")
        except Exception as e:
            chk(False, f"raise {e!r} (đáng lẽ fail-open)")

        print("== load_context đọc được rules/manifest thật (repo hiện tại) ==")
        try:
            rl, ga = H.load_context(WS_REAL)
            chk(isinstance(rl, dict) and isinstance(ga, set), "load_context trả (dict, set)")
        except Exception as e:
            chk(False, f"load_context raise {e!r}")

        print(f"\n== TỔNG: PASS={PASS} FAIL={FAIL} ==")
        return 1 if FAIL else 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

if __name__ == "__main__":
    sys.exit(main())
