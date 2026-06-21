#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TDD P1.3 — cleanliness gate (D11/INV-4). Part A: scan() thuần (hermetic). Part B: 4 repo thật SẠCH.
Chạy: PYTHONUTF8=1 python kb_lifecycle/tests/test_clean.py"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[1] / "tools"))

PASS = FAIL = 0
def chk(c, l):
    global PASS, FAIL
    if c: PASS += 1; print(f"  PASS  {l}")
    else: FAIL += 1; print(f"  FAIL  {l}")

def main():
    import check_clean as C
    rules = C.load_rules()

    print("== Part A: scan() thuần — bắt scratch, GIỮ curated ==")
    dirty_inputs = [
        "_PNL_HANDOFF.md", "_PNL_BUILD_STATE.md", "_DB01_NOTES_DRAFT.md",
        "_build_heatmap.js", "_combochip.txt", "x.network-response",
        "blackboards/bb_1.json", "raw/__pycache__/resolver.cpython-310.pyc",
        "_orchestration.lock",
    ]
    clean_inputs = [
        "fields/_INDEX.md", "fields/_FLAGSHIP_Revenue.md", "fields/_EXAMPLES_extra.md",
        "dataset_catalog.yaml", "kb_lifecycle/STATUS.md", "kb_lifecycle/tools/kgr_runtime.py",
        ".gitattributes", ".kgr_kb_root", "learnings/log.jsonl", "DIRECTION_AND_DESIGN_v0.md",
    ]
    for f in dirty_inputs:
        chk(C.violation(f, rules) is not None, f"BẮT scratch: {f}")
    for f in clean_inputs:
        chk(C.violation(f, rules) is None, f"GIỮ hợp lệ: {f}")

    print("== Part B: repo THẬT phải sạch (monorepo hoặc 4-repo, tự thích nghi) ==")
    targets = C.repos_to_scan()
    chk(len(targets) >= 1, f"có git repo để quét ({[p.name for p in targets]})")
    viol = C.scan_all(rules)
    chk(not viol, f"repo thật SẠCH ({len(viol)} scratch tracked)" + (f" -> {viol[:5]}" if viol else ""))

    print(f"\n== TỔNG: PASS={PASS} FAIL={FAIL} ==")
    return 1 if FAIL else 0

if __name__ == "__main__":
    sys.exit(main())
