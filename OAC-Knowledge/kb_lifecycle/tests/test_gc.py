#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TDD — kb_gc: retention cho _kgr-state (xóa tmp/_trash/dump cũ; archive blackboard cũ). Hermetic.
Chạy: PYTHONUTF8=1 python kb_lifecycle/tests/test_gc.py"""
import os, sys, tempfile, shutil, time
from pathlib import Path

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[1] / "tools"))

PASS = FAIL = 0
def chk(c, l):
    global PASS, FAIL
    if c: PASS += 1; print(f"  PASS  {l}")
    else: FAIL += 1; print(f"  FAIL  {l}")

def _mk(p, age_days, now):
    p = Path(p); p.parent.mkdir(parents=True, exist_ok=True); p.write_text("x", encoding="utf-8")
    ts = now - age_days * 86400
    os.utime(p, (ts, ts))
    return p

def main():
    import kb_gc
    now = time.time()
    tmp = Path(tempfile.mkdtemp(prefix="kgr_gc_"))
    try:
        sr = tmp / "_kgr-state"
        old_tmp   = _mk(sr / "orchestration" / "tmp" / "chunk.txt", 30, now)
        new_tmp   = _mk(sr / "orchestration" / "tmp" / "fresh.txt", 1, now)
        old_trash = _mk(sr / "_trash" / "old.bin", 30, now)
        old_resp  = _mk(sr / "work" / "Dashboard-builder" / "_r.network-response", 10, now)
        keep_work = _mk(sr / "work" / "Dashboard-builder" / "notes.md", 10, now)   # không phải dump → giữ
        old_bb    = _mk(sr / "orchestration" / "blackboards" / "bb_old.json", 60, now)
        new_bb    = _mk(sr / "orchestration" / "blackboards" / "bb_new.json", 5, now)

        plan = kb_gc.build_plan(sr, now, bb_days=30, tmp_days=7)
        dpaths = {d[0] for d in plan["delete"]}
        apaths = {a[0] for a in plan["archive"]}

        print("== build_plan phân loại đúng ==")
        chk(str(old_tmp) in dpaths, "tmp cũ (>7d) → delete")
        chk(str(new_tmp) not in dpaths, "tmp mới (1d) → GIỮ")
        chk(str(old_trash) in dpaths, "_trash cũ → delete")
        chk(str(old_resp) in dpaths, "work/*.network-response cũ → delete")
        chk(str(keep_work) not in dpaths, "work/notes.md (không dump) → GIỮ")
        chk(str(old_bb) in apaths, "blackboard cũ (>30d) → archive")
        chk(str(new_bb) not in apaths and str(new_bb) not in dpaths, "blackboard mới → GIỮ nguyên chỗ")

        print("== apply_plan thực thi (move + delete) ==")
        n_del, n_arc, errors = kb_gc.apply_plan(plan)
        chk(not errors, f"không lỗi ({errors})")
        chk(not old_tmp.exists() and not old_trash.exists() and not old_resp.exists(), "file cũ đã xóa")
        chk(new_tmp.exists() and keep_work.exists() and new_bb.exists(), "file mới còn nguyên")
        chk(not old_bb.exists(), "blackboard cũ đã rời chỗ cũ")
        chk((sr / "archived" / "blackboards" / "bb_old.json").exists(), "blackboard cũ nằm ở archived/ (không mất)")

        print("== dry-run KHÔNG đụng đĩa ==")
        old2 = _mk(sr / "_trash" / "again.bin", 30, now)
        plan2 = kb_gc.build_plan(sr, now, tmp_days=7)
        chk(str(old2) in {d[0] for d in plan2["delete"]}, "build_plan thấy file mới tạo")
        chk(old2.exists(), "chưa apply → file vẫn còn (dry-run an toàn)")

        print(f"\n== TỔNG: PASS={PASS} FAIL={FAIL} ==")
        return 1 if FAIL else 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

if __name__ == "__main__":
    sys.exit(main())
