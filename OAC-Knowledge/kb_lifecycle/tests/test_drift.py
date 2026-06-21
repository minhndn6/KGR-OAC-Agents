#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TDD P3.4 — drift store: lọc ts + upsert + debounce + storm-breaker + cooldown + auto-resolve (D7/D8/INV-6).
OFFLINE: fixture freshness + observation giả lập. KHÔNG gọi OAC.
Chạy: PYTHONUTF8=1 python kb_lifecycle/tests/test_drift.py"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[1] / "tools"))
FIXTURE = Path(r"C:\Project\_work\kgr-governance-build\oac_freshness_2026-06-21.json")

PASS = FAIL = 0
def chk(c, l):
    global PASS, FAIL
    if c: PASS += 1; print(f"  PASS  {l}")
    else: FAIL += 1; print(f"  FAIL  {l}")

def main():
    import drift as D

    print("== lọc ts hợp lệ từ fixture (bỏ 99 connector thiếu ts) ==")
    if FIXTURE.is_file():
        obs, skipped = D.freshness_observations(str(FIXTURE), "2026-06-20")
        chk(skipped == 99, f"bỏ đúng 99 asset thiếu lastModifiedTime (skipped={skipped})")
        chk(all(D.TS_RE.match(o["observed"]) for o in obs), "mọi observation có ts hợp lệ")
        # 2026-06-20 là ngày trích: vài dataflow sửa trong ngày -> có obs; KHÔNG cái nào > 2026-06-21
        obs2, _ = D.freshness_observations(str(FIXTURE), "2026-06-21")
        chk(len(obs2) == 0, "không asset nào đổi SAU 2026-06-21 (KB đồng bộ)")
    else:
        chk(False, "thiếu fixture freshness")

    print("== drift_key + upsert (trùng -> hit_count++, KHÔNG tạo mới) ==")
    st = {}
    o = [{"probe": "freshness", "target": "DF_X", "observed": "2026-06-25T01:00:00Z", "expected": "2026-06-20"}]
    D.observe(o, st, now=100, debounce=2)
    chk(len(st) == 1 and list(st.values())[0]["state"] == "seen", "lần 1 -> seen (chưa open: debounce)")
    chk(D.to_emit(st, 100) == [], "seen -> chưa emit")
    D.observe(o, st, now=200, debounce=2)
    chk(list(st.values())[0]["state"] == "open" and list(st.values())[0]["hit_count"] == 2, "lần 2 -> open (debounce đạt)")
    chk(len(D.to_emit(st, 200)) == 1, "open -> emit")
    D.observe(o, st, now=300, debounce=2)
    chk(len(st) == 1 and list(st.values())[0]["hit_count"] == 3, "lần 3 -> UPSERT (vẫn 1 record, hit_count=3)")

    print("== cooldown / suppress_until ==")
    D.mark_emitted(st, now=300, cooldown=1000)
    chk(D.to_emit(st, 400) == [], "trong cooldown -> không re-surface")
    chk(len(D.to_emit(st, 1400)) == 1, "hết cooldown -> surface lại")

    print("== storm-breaker (>K NEW/lần -> 1 bulk, không emit per-item) ==")
    st2 = {}
    many = [{"probe": "freshness", "target": f"T{i}", "observed": "2026-06-25T00:00:00Z", "expected": "2026-06-20"} for i in range(11)]
    summ = D.observe(many, st2, now=1, debounce=2, storm_k=10)
    chk(summ["bulk"] is True, "11 NEW > storm_k=10 -> bulk")
    chk(any(e.get("probe") == "bulk_divergence" for e in st2.values()), "có record bulk_divergence")
    chk(all(e["state"] != "open" for e in st2.values() if e.get("probe") == "freshness"), "per-item KHÔNG open (suppressed_bulk)")

    print("== auto-resolve sau rebuild ==")
    st3 = {}
    oy = [{"probe": "freshness", "target": "DF_Y", "observed": "2026-06-25T00:00:00Z", "expected": "2026-06-20"}]
    D.observe(oy, st3, now=1, debounce=1)  # debounce=1 -> open ngay
    chk(list(st3.values())[0]["state"] == "open", "DF_Y open")
    n = D.auto_resolve(st3, {"DF_Y"}, now=999)
    chk(n == 1 and list(st3.values())[0]["state"] == "resolved_stale", "rebuild hấp thụ -> resolved_stale")

    print(f"\n== TỔNG: PASS={PASS} FAIL={FAIL} ==")
    return 1 if FAIL else 0

if __name__ == "__main__":
    sys.exit(main())
