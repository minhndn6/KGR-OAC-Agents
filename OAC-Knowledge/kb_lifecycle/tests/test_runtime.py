#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TDD P1.1 — kgr_runtime: tách DURABLE (backed-up, trong workspace) vs EPHEMERAL (ngoài, %LOCALAPPDATA%) (D9/D10/INV-4).
Chạy: PYTHONUTF8=1 python kb_lifecycle/tests/test_runtime.py"""
import os, sys, tempfile, shutil
from pathlib import Path

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[1] / "tools"))

PASS = FAIL = 0
def chk(c, l):
    global PASS, FAIL
    if c: PASS += 1; print(f"  PASS  {l}")
    else: FAIL += 1; print(f"  FAIL  {l}")

def main():
    import kgr_runtime as R
    tmp = Path(tempfile.mkdtemp(prefix="kgr_rt_"))
    try:
        ws = tmp / "ws"
        (ws / "OAC-Knowledge").mkdir(parents=True)
        (ws / "OAC-Orchestrator").mkdir(parents=True)
        fake = ws / "OAC-Knowledge" / "kb_lifecycle" / "tools" / "kgr_runtime.py"
        fake.parent.mkdir(parents=True); fake.write_text("#", encoding="utf-8")

        print("== workspace_root ==")
        chk(R.workspace_root(start=str(fake), env={}) == ws, "walk-up tìm dir chứa 2 sentinel repo")
        chk(R.workspace_root(env={"KGR_WORKSPACE": str(ws)}) == ws, "KGR_WORKSPACE override")
        try: R.workspace_root(start=str(tmp / "nowhere" / "x.py"), env={}); ok=False
        except RuntimeError: ok=True
        chk(ok, "không tìm thấy -> raise (không đoán mò)")

        print("== DURABLE (backed-up, trong workspace) ==")
        bb = R.blackboards_dir(start=str(fake), env={})
        chk(bb == ws / "_orchestration" / "blackboards", "blackboards_dir = ws/_orchestration/blackboards")
        chk(str(ws) in str(bb), "durable NẰM TRONG workspace (in-backup)")
        chk(R.locks_dir(start=str(fake), env={}) == ws / "_orchestration" / "locks", "locks_dir = ws/_orchestration/locks")
        chk(R.orch_dir(env={"KGR_ORCH_DIR": str(tmp / "o")}) == tmp / "o", "KGR_ORCH_DIR override")

        print("== EPHEMERAL runtime ==")
        chk(R.runtime_dir(env={"KGR_RUNTIME_DIR": str(tmp / "rt")}) == tmp / "rt", "KGR_RUNTIME_DIR override")
        chk(R.runtime_dir(env={"LOCALAPPDATA": str(tmp / "LA")}) == tmp / "LA" / "kgr-oac" / "runtime", "default %LOCALAPPDATA%/kgr-oac/runtime")
        chk(R.runtime_dir(env={}) == Path(os.path.expanduser("~")) / ".kgr" / "runtime", "zero-env -> ~/.kgr/runtime")

        print("== DURABLE vs EPHEMERAL phải KHÁC gốc ==")
        sc = R.scratch_dir("sess A/b\\c", env={"KGR_RUNTIME_DIR": str(tmp / "rt")})
        chk(str(tmp / "rt") in str(sc) and "scratch" in str(sc).replace("\\", "/"), "scratch_dir dưới runtime/scratch")
        chk(str(ws) not in str(sc), "scratch KHÔNG trong workspace (ephemeral, không backup)")
        chk("/" not in sc.name and "\\" not in sc.name, "session slug an toàn (không path-sep)")

        print("== helpers ==")
        sp = R.scratch("note.md", session="s1", env={"KGR_RUNTIME_DIR": str(tmp / "rt")})
        chk(sp.name == "note.md" and sp.parent.is_dir(), "scratch(name) tạo dir + trả path file")
        tgt = tmp / "out" / "x.json"
        R.atomic_write(tgt, '{"a":1}')
        chk(tgt.is_file() and tgt.read_text(encoding="utf-8") == '{"a":1}', "atomic_write ghi (tmp cùng dir => cùng volume)")
        chk(not list((tmp / "out").glob("*.tmp")), "không để lại .tmp")

        print(f"\n== TỔNG: PASS={PASS} FAIL={FAIL} ==")
        return 1 if FAIL else 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

if __name__ == "__main__":
    sys.exit(main())
