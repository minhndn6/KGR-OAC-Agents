#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TDD P0.2 — pin determinism: .gitattributes (LF) + KHÔNG track pyc/__pycache__ (INV-3, V2/V4).
Chạy: PYTHONUTF8=1 python kb_lifecycle/tests/test_determinism.py
Vì sao: core.autocrlf=true + thiếu .gitattributes -> hash/diff guard false-positive đa máy.
"""
import subprocess
from pathlib import Path

WS = Path(r"C:\Project\KGR-OAC-Agents")
REPOS = ["OAC-Knowledge", "OAC-Orchestrator", "Dashboard-builder", "Dataflow-builder"]
TYPES_LF = [".py", ".md", ".yaml", ".yml", ".json", ".txt"]

PASS = FAIL = 0
def chk(cond, label):
    global PASS, FAIL
    if cond: PASS += 1; print(f"  PASS  {label}")
    else:    FAIL += 1; print(f"  FAIL  {label}")

def tracked(repo):
    p = WS / repo
    try:
        out = subprocess.run(["git", "-C", str(p), "ls-files"], capture_output=True, text=True, timeout=60)
        return out.stdout.splitlines()
    except Exception as e:
        return [f"__ERR__{e}"]

def main():
    for r in REPOS:
        ga = WS / r / ".gitattributes"
        print(f"== {r} ==")
        ok_exists = ga.is_file()
        chk(ok_exists, f"{r}/.gitattributes tồn tại")
        if ok_exists:
            txt = ga.read_text(encoding="utf-8", errors="ignore").lower()
            chk("eol=lf" in txt, f"{r}/.gitattributes có rule eol=lf")
            covered = all(any(t.lstrip(".") in ln and "eol=lf" in ln for ln in txt.splitlines()) for t in TYPES_LF)
            chk(covered, f"{r} pin LF cho {TYPES_LF}")
        files = tracked(r)
        pyc = [f for f in files if f.endswith(".pyc") or "__pycache__" in f]
        chk(not pyc, f"{r}: KHÔNG track pyc/__pycache__ ({len(pyc)} thấy)")

    print(f"\n== TỔNG: PASS={PASS} FAIL={FAIL} ==")
    return 1 if FAIL else 0

if __name__ == "__main__":
    import sys; sys.exit(main())
