#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TDD P3.1+3.2 — learn2: content_hash/fact_key + migrate + dedup + contradiction + supersede (D5/INV-5).
Part A hermetic (temp log); Part B migrate trên BẢN SAO log thật (không đụng log thật trong test).
Chạy: PYTHONUTF8=1 python kb_lifecycle/tests/test_learn2.py"""
import os, sys, json, tempfile, shutil
from pathlib import Path

HERE = Path(__file__).resolve()
TOOLS = HERE.parents[1] / "tools"
sys.path.insert(0, str(TOOLS))

PASS = FAIL = 0
def chk(c, l):
    global PASS, FAIL
    if c: PASS += 1; print(f"  PASS  {l}")
    else: FAIL += 1; print(f"  FAIL  {l}")

def write_log(p, recs):
    with open(p, "w", encoding="utf-8") as f:
        for r in recs: f.write(json.dumps(r, ensure_ascii=False) + "\n")

def read_log(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]

def main():
    import learn2 as L, kb_paths as KP
    tmp = Path(tempfile.mkdtemp(prefix="kgr_learn2_"))
    try:
        log = tmp / "log.jsonl"
        # old-format (no hash/fact_key)
        write_log(log, [
            {"id": "L0001", "ts": "t", "type": "lesson", "topic": "enc", "content": "abc", "status": "promoted"},
            {"id": "L0002", "ts": "t", "type": "glossary_term", "topic": "Doanh thu", "content": "def A", "status": "promoted"},
        ])

        print("== 3.1 migrate (backfill, idempotent) ==")
        L.migrate(log, backup=False)
        recs = read_log(log)
        chk(all("content_hash" in r and "fact_key" in r for r in recs), "mọi record có content_hash + fact_key")
        chk(all("supersedes" in r and "superseded_by" in r for r in recs), "có supersedes/superseded_by")
        b1 = log.read_bytes(); L.migrate(log, backup=False); b2 = log.read_bytes()
        chk(b1 == b2, "migrate idempotent (chạy lại không đổi)")

        print("== 3.2 dedup ==")
        r1 = L.add("lesson", "topic X", "content X", log=log)
        chk(r1["status"] == "added", "add mới -> added")
        r2 = L.add("lesson", "topic X", "content X", log=log)
        chk(r2["status"] == "rejected_dup" and r2["existing"] == r1["id"], "add trùng content_hash -> rejected_dup")
        chk(len(read_log(log)) == 3, "không tạo record trùng (vẫn 3)")

        print("== 3.2 contradiction ==")
        # thêm glossary 'Doanh thu' nội dung KHÁC (cùng fact_key với L0002 promoted)
        rc = L.add("glossary_term", "Doanh thu", "def B (khác)", log=log)
        chk(rc["status"] == "added", "add glossary khác nội dung -> added (chưa promote)")
        contra = L.find_contradictions(rc["id"], log=log)
        chk("L0002" in contra, "find_contradictions: cùng fact_key khác nội dung -> phát hiện L0002 promoted")

        print("== 3.2 supersede (append + lật trạng thái, audit, KHÔNG xóa) ==")
        sp = L.supersede(rc["id"], "L0002", "định nghĩa Doanh thu cập nhật", "attested:owner", log=log)
        chk(sp["status"] == "superseded", "supersede OK")
        recs = {r["id"]: r for r in read_log(log)}
        chk(recs["L0002"]["status"] == "superseded" and recs["L0002"]["superseded_by"] == rc["id"], "old: superseded + superseded_by")
        chk("L0002" in recs[rc["id"]]["supersedes"] and recs[rc["id"]]["status"] == "promoted", "new: supersedes[old] + promoted")
        chk("L0002" in [r["id"] for r in read_log(log)], "old record VẪN còn (audit, không xóa)")
        # supersede chéo chủ thể -> chặn
        bad = L.supersede(rc["id"], "L0001", "x", "y", log=log)
        chk(bad["status"] == "error", "supersede khác fact_key -> chặn (không trộn chủ thể)")

        print("== Part B: migrate BẢN SAO log THẬT (10+ record) ==")
        real = KP.resolve_kb_root(start_file=str(TOOLS / "kb_paths.py")) / "learnings" / "log.jsonl"
        if real.is_file():
            cp = tmp / "real_copy.jsonl"; shutil.copy2(real, cp)
            n0 = len(read_log(cp)); L.migrate(cp, backup=False); rr = read_log(cp)
            chk(len(rr) == n0 >= 10, f"giữ nguyên số record ({n0})")
            chk(all("content_hash" in r and "fact_key" in r for r in rr), "log thật: mọi record backfill được")
            active = [r for r in rr if r.get("status") in ("pending", "promoted")]
            hashes = [r["content_hash"] for r in active]
            chk(len(hashes) == len(set(hashes)), "log thật: không 2 record ACTIVE trùng content_hash")
        else:
            chk(False, "không tìm thấy log thật")

        print(f"\n== TỔNG: PASS={PASS} FAIL={FAIL} ==")
        return 1 if FAIL else 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

if __name__ == "__main__":
    sys.exit(main())
