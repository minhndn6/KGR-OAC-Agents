#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TDD P1.4 — entrypoint cho AI lạ: workspace CLAUDE.md + `kgr` CLI (D12).
Chạy: PYTHONUTF8=1 python kb_lifecycle/tests/test_entrypoint.py"""
import os, sys, subprocess, json
from pathlib import Path

WS = Path(os.environ.get("KGR_WORKSPACE") or r"C:\Project\KGR-OAC-Agents")
KGR = WS / "OAC-Knowledge" / "kb_lifecycle" / "tools" / "kgr.py"
CLAUDEMD = WS / "CLAUDE.md"
ENV = {**os.environ, "PYTHONUTF8": "1"}

PASS = FAIL = 0
def chk(c, l):
    global PASS, FAIL
    if c: PASS += 1; print(f"  PASS  {l}")
    else: FAIL += 1; print(f"  FAIL  {l}")

def run(*args):
    return subprocess.run([sys.executable, str(KGR), *args], capture_output=True, text=True, env=ENV)

def main():
    print("== workspace CLAUDE.md (parent chung, AI auto-đọc) ==")
    chk(CLAUDEMD.is_file(), "C:/Project/KGR-OAC-Agents/CLAUDE.md tồn tại")
    if CLAUDEMD.is_file():
        t = CLAUDEMD.read_text(encoding="utf-8").lower()
        for tok in ["kgr", "scratch", "kb_route", "_kgr-state", "không ghi"]:
            chk(tok.lower() in t, f"CLAUDE.md nhắc '{tok}'")

    print("== kgr CLI ==")
    chk(KGR.is_file(), "tools/kgr.py tồn tại")
    w = run("where")
    chk(w.returncode == 0 and "kgr-oac" in w.stdout and "_kgr-state" in w.stdout, "`kgr where` in runtime + durable root (NGOÀI cây)")
    d = run("doctor")
    ok_json = False; rep = {}
    try: rep = json.loads(d.stdout); ok_json = True
    except Exception: pass
    chk(ok_json, "`kgr doctor` in JSON hợp lệ")
    chk(rep.get("kb_root_ok") is True, "doctor: kb_root resolve OK (single, không split-brain)")
    chk(rep.get("repos_clean") is True, "doctor: 4 repo sạch")
    chk(d.returncode == 0, "doctor exit 0 khi healthy")
    s = run("setup")
    chk(s.returncode == 0 and "kb_root" in s.stdout, "`kgr setup` ghi registry (idempotent)")
    u = run("bogus_cmd")
    chk(u.returncode != 0, "lệnh lạ -> exit≠0 (không im lặng)")

    print(f"\n== TỔNG: PASS={PASS} FAIL={FAIL} ==")
    return 1 if FAIL else 0

if __name__ == "__main__":
    sys.exit(main())
