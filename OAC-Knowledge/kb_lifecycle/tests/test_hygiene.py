#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TDD P1.2 — durable state ra khỏi repo, vào <WS>/_orchestration (in-backup), KHÔNG vào %LOCALAPPDATA% (D9/INV-4).
Chạy: PYTHONUTF8=1 python kb_lifecycle/tests/test_hygiene.py"""
import os, sys, importlib.util
from pathlib import Path

WS = Path(r"C:\Project\KGR-OAC-Agents")
BB_PY = WS / "OAC-Orchestrator" / "scripts" / "blackboard.py"

PASS = FAIL = 0
def chk(c, l):
    global PASS, FAIL
    if c: PASS += 1; print(f"  PASS  {l}")
    else: FAIL += 1; print(f"  FAIL  {l}")

def load(envpatch=None):
    old = dict(os.environ)
    try:
        for k in ("KGR_BB_DIR", "KGR_ORCH_DIR"): os.environ.pop(k, None)
        if envpatch: os.environ.update(envpatch)
        spec = importlib.util.spec_from_file_location("bb_h", str(BB_PY))
        m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
        return m
    finally:
        os.environ.clear(); os.environ.update(old)

def main():
    print("== default BB_DIR ngoài repo, trong _orchestration ==")
    m = load()
    bbd = str(m.BB_DIR)
    chk("_orchestration" in bbd and bbd.endswith(os.path.join("_orchestration", "blackboards")),
        f"BB_DIR -> _orchestration/blackboards ({bbd})")
    chk(os.path.join("OAC-Orchestrator", "blackboards") not in bbd,
        "BB_DIR KHÔNG nằm trong cây repo OAC-Orchestrator")
    la = os.environ.get("LOCALAPPDATA", "")
    chk(not (la and bbd.startswith(la)), "BB_DIR KHÔNG nằm dưới %LOCALAPPDATA% (durable phải backed-up)")

    print("== env override ==")
    m2 = load({"KGR_BB_DIR": str(WS / "_work" / "bbtest")})
    chk(str(m2.BB_DIR) == str(WS / "_work" / "bbtest"), "KGR_BB_DIR override hoạt động")

    print("== không còn bb_* state trong repo tree ==")
    repo_bb = WS / "OAC-Orchestrator" / "blackboards"
    leftover = list(repo_bb.glob("bb_*")) if repo_bb.exists() else []
    chk(not leftover, f"repo/blackboards sạch state ({len(leftover)} sót)")

    print(f"\n== TỔNG: PASS={PASS} FAIL={FAIL} ==")
    return 1 if FAIL else 0

if __name__ == "__main__":
    sys.exit(main())
