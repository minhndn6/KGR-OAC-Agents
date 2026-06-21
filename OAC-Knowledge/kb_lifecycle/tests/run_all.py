#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Chạy toàn bộ test kb_lifecycle (deterministic, offline) + regression gate suite cũ.
Usage: PYTHONUTF8=1 python kb_lifecycle/tests/run_all.py [--with-legacy]
Mỗi test_*.py là script tự-chứa trả exit code (0=pass). --with-legacy chạy thêm validate_kb/qa_full/test_orchestrator (AC7)."""
import os, sys, subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
WS = Path(r"C:\Project\KGR-OAC-Agents")
ENV = {**os.environ, "PYTHONUTF8": "1"}

def run(label, args, cwd=None):
    r = subprocess.run(args, cwd=cwd, env=ENV, capture_output=True, text=True)
    tail = "\n".join((r.stdout or "").strip().splitlines()[-3:])
    ok = r.returncode == 0
    print(f"[{'OK ' if ok else 'FAIL'}] {label}")
    if not ok:
        print("   " + (tail.replace("\n", "\n   ") or (r.stderr or '')[-300:]))
    return ok

def main():
    with_legacy = "--with-legacy" in sys.argv
    results = []
    print("== kb_lifecycle unit/UAT tests ==")
    for t in sorted(HERE.glob("test_*.py")):
        results.append(run(t.stem, [sys.executable, str(t)]))
    # UAT corpus runner (nếu có)
    uat = HERE / "uat" / "run_uat.py"
    if uat.is_file():
        results.append(run("uat_corpus", [sys.executable, str(uat)]))
    if with_legacy:
        print("\n== legacy regression gate (AC7) ==")
        kb = WS / "OAC-Knowledge"
        results.append(run("validate_kb", [sys.executable, "skill/kgr-oac-lineage/scripts/validate_kb.py"], cwd=str(kb)))
        results.append(run("qa_full", [sys.executable, "qa_full.py"], cwd=str(kb / "raw")))
        results.append(run("test_orchestrator", [sys.executable, "scripts/test_orchestrator.py"], cwd=str(WS / "OAC-Orchestrator")))
    npass = sum(results); n = len(results)
    print(f"\n== RUN_ALL: {npass}/{n} suites OK ==")
    return 0 if npass == n else 1

if __name__ == "__main__":
    sys.exit(main())
