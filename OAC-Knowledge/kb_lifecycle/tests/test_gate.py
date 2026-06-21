#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TDD P3.3 — typed promote-gate (D6, KHỚP kb_route gate). Mỗi loại: thiếu evidence→reject, đủ→promoted.
governance KHÔNG auto; gap KHÔNG promote; contradiction chặn tới khi supersede.
Chạy: PYTHONUTF8=1 python kb_lifecycle/tests/test_gate.py"""
import sys, json, tempfile, shutil
from pathlib import Path

HERE = Path(__file__).resolve()
TOOLS = HERE.parents[1] / "tools"
sys.path.insert(0, str(TOOLS))

PASS = FAIL = 0
def chk(c, l):
    global PASS, FAIL
    if c: PASS += 1; print(f"  PASS  {l}")
    else: FAIL += 1; print(f"  FAIL  {l}")

def main():
    import learn2 as L, kb_route as KR
    tmp = Path(tempfile.mkdtemp(prefix="kgr_gate_"))
    log = tmp / "log.jsonl"
    try:
        def reset(recs):
            with open(log, "w", encoding="utf-8") as f:
                for r in recs: f.write(json.dumps(r, ensure_ascii=False) + "\n")
            L.migrate(log, backup=False)

        def rec(rid, typ, topic, content, status="pending", source=""):
            return {"id": rid, "ts": "t", "type": typ, "topic": topic, "content": content, "status": status, "source": source}

        print("== structural (fact/new_field): cần rebuild_sha ==")
        reset([rec("L1", "new_field", "a9 col", "ct..."), rec("L2", "fact", "grain X", "...")])
        chk(L.promote("L1", {}, log=log)["status"] == "rejected", "new_field thiếu rebuild_sha -> reject")
        chk(L.promote("L1", {"rebuild_sha": "abc123"}, log=log)["status"] == "promoted", "new_field + rebuild_sha -> promoted")

        print("== formula_correction: live_evidence HOẶC rebuild_sha ==")
        reset([rec("L1", "formula_correction", "a9 fix", "...")])
        chk(L.promote("L1", {}, log=log)["status"] == "rejected", "formula thiếu bằng chứng -> reject")
        chk(L.promote("L1", {"live_evidence": "executePreview ok"}, log=log)["status"] == "promoted", "formula + live_evidence -> promoted")

        print("== correction: provenance HOẶC source người/owner ==")
        reset([rec("L1", "correction", "3 agent", "...", source=""), rec("L2", "correction", "x", "...", source="user")])
        chk(L.promote("L1", {}, log=log)["status"] == "rejected", "correction source rỗng + no provenance -> reject")
        chk(L.promote("L2", {}, log=log)["status"] == "promoted", "correction source=user -> promoted (provenance người)")

        print("== glossary/convention: attested_by ==")
        reset([rec("L1", "glossary_term", "Doanh thu", "def...")])
        chk(L.promote("L1", {}, log=log)["status"] == "rejected", "glossary thiếu attested_by -> reject")
        chk(L.promote("L1", {"attested_by": "owner:Minh"}, log=log)["status"] == "promoted", "glossary + attested_by -> promoted")

        print("== governance: KHÔNG auto, KHÔNG second-agent, cần người ký ==")
        reset([rec("L1", "governance_item", "GR1 AOP", "...")])
        chk(L.promote("L1", {}, log=log)["status"] == "rejected", "governance thiếu attested_by -> reject")
        chk(L.promote("L1", {"attested_by": "CFO", "via": "auto"}, log=log)["status"] == "rejected", "governance via=auto -> reject (KHÔNG auto)")
        chk(L.promote("L1", {"attested_by": "CFO", "via": "second-agent"}, log=log)["status"] == "rejected", "governance second-agent -> reject")
        chk(L.promote("L1", {"attested_by": "CFO:owner ký"}, log=log)["status"] == "promoted", "governance + người ký -> promoted")

        print("== gap KHÔNG promote; lesson cần incorporated_into ==")
        reset([rec("L1", "gap", "producer sống", "..."), rec("L2", "lesson", "enc", "...")])
        chk(L.promote("L1", {"attested_by": "x", "rebuild_sha": "y"}, log=log)["status"] == "rejected", "gap -> reject promote (kể cả có evidence)")
        chk(L.promote("L2", {}, log=log)["status"] == "rejected", "lesson thiếu incorporated_into -> reject")
        chk(L.promote("L2", {"incorporated_into": "CONVENTIONS.md"}, log=log)["status"] == "promoted", "lesson + incorporated_into -> promoted")

        print("== contradiction chặn promote tới khi supersede ==")
        reset([rec("L1", "glossary_term", "Doanh thu", "def A", status="promoted"),
               rec("L2", "glossary_term", "Doanh thu", "def B khác")])
        r = L.promote("L2", {"attested_by": "owner"}, log=log)
        chk(r["status"] == "rejected" and "supersede" in r["reason"], "promote L2 (mâu thuẫn L1) -> reject, đòi supersede")
        L.supersede("L2", "L1", "cập nhật", "attested:owner", log=log)
        recs = {x["id"]: x for x in [json.loads(l) for l in open(log, encoding="utf-8") if l.strip()]}
        chk(recs["L2"]["status"] == "promoted" and recs["L1"]["status"] == "superseded", "supersede xong -> L2 promoted, L1 superseded")

        print("== consistency: mọi type của kb_route đều có quyết định gate ==")
        for t in KR.ROUTES:
            covered = (t in L._GATE) or (t in L._NO_PROMOTE)
            chk(covered, f"kb_route type '{t}' có gate/quyết định trong learn2")

        print(f"\n== TỔNG: PASS={PASS} FAIL={FAIL} ==")
        return 1 if FAIL else 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

if __name__ == "__main__":
    sys.exit(main())
