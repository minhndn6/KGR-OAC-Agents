#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""find_source.py — gợi ý dataset nguồn cho 'cần metric M [theo chiều D]'.
Usage: python find_source.py "<metric keyword>" ["<dimension keyword>"]
Đọc capability_map.yaml + dataset_catalog.yaml. KHÔNG trả số (data live)."""
import os, sys
from pathlib import Path
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
try: import yaml
except ImportError: print("cần pyyaml"); sys.exit(1)

SCRIPT_DIR=Path(__file__).resolve().parent
def find_root():
    if os.environ.get("OAC_KB_ROOT"): return Path(os.environ["OAC_KB_ROOT"])
    for c in [SCRIPT_DIR.parent.parent.parent, Path(r"C:\Project\OAC-Knowledge")]:
        if (c/"capability_map.yaml").exists(): return c
    return SCRIPT_DIR.parent.parent.parent
KB=find_root()

cap=yaml.safe_load(open(KB/"capability_map.yaml",encoding="utf-8"))
dc=yaml.safe_load(open(KB/"dataset_catalog.yaml",encoding="utf-8"))["datasets"]

def search(idx, kw):
    kw=kw.lower(); hits={}
    for concept, dss in idx.items():
        if kw in concept.lower(): hits[concept]=dss
    return hits

def main():
    if len(sys.argv)<2:
        print("Usage: find_source.py \"<metric>\" [\"<dimension>\"]");
        print("\nMetric concepts:", list(cap.get("by_metric",{}).keys()))
        print("Dimension concepts:", list(cap.get("by_dimension",{}).keys())); return
    metric=sys.argv[1]; dim=sys.argv[2] if len(sys.argv)>2 else None
    mh=search(cap.get("by_metric",{}), metric)
    print(f"# Nguồn cho metric ~ '{metric}'"+(f" theo chiều ~ '{dim}'" if dim else ""))
    if not mh: print("  (không khớp concept metric; thử keyword khác hoặc xem business_glossary.yaml)")
    cand=set()
    for c,dss in mh.items():
        print(f"\n## {c}");
        for ds in dss: cand.add(ds)
    if dim:
        dh=search(cap.get("by_dimension",{}), dim)
        dimds=set().union(*dh.values()) if dh else set()
        inter=[d for d in cand if d in dimds]
        print(f"\n=> Dataset có CẢ metric+dimension: {sorted(inter) if inter else '(không có — cân nhắc extend hub hoặc dựng mới, xem source_selection_playbook.md)'}")
        cand=set(inter) if inter else cand
    print("\n# Chi tiết dataset ứng viên (chọn theo precedence BC>DB, grain phù hợp):")
    for ds in sorted(cand):
        r=dc.get(ds,{})
        print(f"  - {ds}: grain={r.get('grain')}, type={r.get('type')}, used_by={r.get('used_by_workbooks')}")
    print("\n(Re-aggregate được nếu grain nguồn mịn hơn. Số: lấy LIVE — live_query_recipes.md.)")

if __name__=="__main__": main()
