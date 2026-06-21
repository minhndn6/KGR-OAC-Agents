#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TDD P0.1 — KB root resolution phải SINGLE + EXPLICIT, KHÔNG rơi vào KB lạ.
Chạy: PYTHONUTF8=1 python kb_lifecycle/tests/test_kbroot.py
Hermetic: dùng tmp dir, KHÔNG đụng KB/registry thật.
Pin contract cho kb_lifecycle/tools/kb_paths.py (viết test TRƯỚC khi impl)."""
import os, sys, tempfile, shutil
from pathlib import Path

HERE = Path(__file__).resolve()
TOOLS = HERE.parents[1] / "tools"
sys.path.insert(0, str(TOOLS))

PASS = FAIL = 0
def chk(cond, label):
    global PASS, FAIL
    if cond: PASS += 1; print(f"  PASS  {label}")
    else:    FAIL += 1; print(f"  FAIL  {label}")

def mk_kb(root, name, marker=True, quick=True):
    """Tạo 1 KB giả: có/không marker, có/không QUICK_REFERENCE (mô phỏng stray KB)."""
    d = Path(root) / name; d.mkdir(parents=True, exist_ok=True)
    if marker: (d / ".kgr_kb_root").write_text("kgr-oac-knowledge-v1\n", encoding="utf-8")
    if quick:  (d / "QUICK_REFERENCE.md").write_text("# stub\n", encoding="utf-8")
    return d

def main():
    import kb_paths as KP
    tmp = Path(tempfile.mkdtemp(prefix="kgr_kbroot_"))
    try:
        # KB thật (workspace) = có marker. KB lạ (stray) = có QUICK_REFERENCE nhưng KHÔNG marker.
        ws  = mk_kb(tmp, "workspace_kb", marker=True,  quick=True)
        stray = mk_kb(tmp, "stray_kb",   marker=False, quick=True)   # giống C:\Project\OAC-Knowledge
        reg = tmp / "registry" / "kb_root.txt"; reg.parent.mkdir(parents=True, exist_ok=True)
        reg.write_text(str(ws), encoding="utf-8")

        print("== 1. env override hợp lệ ==")
        r = KP.resolve_kb_root(env={"OAC_KB_ROOT": str(ws)})
        chk(Path(r) == ws, "OAC_KB_ROOT trỏ KB hợp lệ -> dùng nó")

        print("== 2. env override KHÔNG hợp lệ (thiếu marker) -> fail loud ==")
        try:
            KP.resolve_kb_root(env={"OAC_KB_ROOT": str(stray)}); ok = False
        except KP.KbRootError: ok = True
        chk(ok, "OAC_KB_ROOT trỏ KB lạ (no marker) -> raise, KHÔNG nuốt")

        print("== 3. walk-up từ file trong workspace KB ==")
        deep = ws / "skill" / "x" / "scripts"; deep.mkdir(parents=True, exist_ok=True)
        f = deep / "learn.py"; f.write_text("# x\n", encoding="utf-8")
        r = KP.resolve_kb_root(start_file=str(f), env={})
        chk(Path(r) == ws, "walk-up gặp marker -> workspace KB")

        print("== 4. SPLIT-BRAIN regression: chạy từ bản cài ~/.claude, dựa registry ==")
        installed = tmp / "home" / ".claude" / "skills" / "kgr-oac-lineage" / "scripts"
        installed.mkdir(parents=True, exist_ok=True)
        f2 = installed / "learn.py"; f2.write_text("# installed\n", encoding="utf-8")
        # env rỗng, walk-up KHÔNG gặp marker (cây khác), registry trỏ workspace
        r = KP.resolve_kb_root(start_file=str(f2), env={}, registry_path=str(reg))
        chk(Path(r) == ws, "bản cài -> resolve về workspace KB qua registry (KHÔNG vào stray)")
        chk(Path(r) != stray, "TUYỆT ĐỐI không rơi vào stray KB")

        print("== 5. NO silent fallback: không env, không marker, không registry -> raise ==")
        try:
            KP.resolve_kb_root(start_file=str(f2), env={}, registry_path=str(tmp/"nope.txt")); ok = False
        except KP.KbRootError: ok = True
        chk(ok, "không xác định được -> raise (KHÔNG hardcode C:\\Project\\OAC-Knowledge)")

        print("== 6. registry trỏ KB lạ (no marker) -> bị từ chối ==")
        reg2 = tmp / "reg2.txt"; reg2.write_text(str(stray), encoding="utf-8")
        try:
            KP.resolve_kb_root(start_file=str(f2), env={}, registry_path=str(reg2)); ok = False
        except KP.KbRootError: ok = True
        chk(ok, "registry trỏ KB lạ -> raise (validate marker, không tin mù)")

        print(f"\n== TỔNG: PASS={PASS} FAIL={FAIL} ==")
        return 1 if FAIL else 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

if __name__ == "__main__":
    sys.exit(main())
