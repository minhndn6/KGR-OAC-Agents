#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""learn2 — lớp learn HARDENED (D5/INV-5) trên CÙNG learnings/log.jsonl với learn.py.
Tương thích ngược: chỉ THÊM field (content_hash, fact_key, supersedes, superseded_by, attested_by, verify_ref).
learn.py (skill gọi) KHÔNG đổi. Typed promote-gate (D6) ở task 3.3.

Usage:
  python learn2.py migrate                                  # backfill content_hash/fact_key (idempotent; backup scratch)
  python learn2.py add <type> "<topic>" "<content>" ["src"] ["conf"]   # dedup theo content_hash
  python learn2.py contradictions <id|fact_key>
  python learn2.py supersede <new_id> <old_id> "<reason>" "<verify_ref>"
  python learn2.py list [status]
"""
import os, sys, json, time, re, hashlib, shutil
from pathlib import Path

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parent))
import kb_paths      # noqa: E402
import kgr_runtime   # noqa: E402

ACTIVE = {"pending", "promoted"}   # record còn hiệu lực (chưa rejected/superseded)

def default_log():
    return kb_paths.resolve_kb_root(start_file=str(HERE)) / "learnings" / "log.jsonl"

def _now():  return time.strftime("%Y-%m-%dT%H:%M:%S")
def _norm(s): return re.sub(r"\s+", " ", (s or "").strip()).casefold()

def content_hash(rec):
    base = "|".join(_norm(rec.get(k)) for k in ("type", "topic", "content"))
    return hashlib.sha256(base.encode("utf-8")).hexdigest()[:16]

_PREFIX = {"formula_correction": "formula", "formula": "formula", "fact": "fact", "correction": "fact",
           "glossary_term": "glossary", "convention": "convention", "governance_item": "gov",
           "gap": "gap", "drift": "drift", "lesson": "lesson", "qa": "qa"}

def fact_key(rec):
    slug = re.sub(r"[^0-9a-z]+", "-", (rec.get("topic") or "").casefold()).strip("-")[:60] or "x"
    return f"{_PREFIX.get(rec.get('type'), rec.get('type') or 'misc')}:{slug}"

def _read(log):
    log = Path(log)
    if not log.exists(): return []
    return [json.loads(l) for l in open(log, encoding="utf-8") if l.strip()]

def _write(log, recs):
    log = Path(log); log.parent.mkdir(parents=True, exist_ok=True)
    with open(log, "w", encoding="utf-8") as f:
        for r in recs:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

def migrate(log=None, backup=True):
    log = Path(log or default_log()); recs = _read(log)
    if backup and recs:
        bdir = kgr_runtime.ensure(kgr_runtime.scratch_dir("learn-migrate"))
        shutil.copy2(log, bdir / ("log.jsonl.bak." + _now().replace(":", "")))
    changed = 0
    for r in recs:
        if "content_hash" not in r: r["content_hash"] = content_hash(r); changed += 1
        if "fact_key" not in r:     r["fact_key"] = fact_key(r); changed += 1
        if "supersedes" not in r:   r["supersedes"] = []
        if "superseded_by" not in r: r["superseded_by"] = None
    _write(log, recs)
    return {"records": len(recs), "changed": changed}

def add(typ, topic, content, source="", conf="medium", log=None):
    log = Path(log or default_log()); recs = _read(log)
    probe = {"type": typ, "topic": topic, "content": content}
    ch = content_hash(probe)
    for r in recs:
        if r.get("content_hash") == ch and r.get("status") in ACTIVE:
            return {"status": "rejected_dup", "existing": r["id"]}
    if re.search(r"\d{1,3}(?:[.,]\d{3}){2,}|\b\d+\s*(?:tỷ|triệu)\b", content or ""):
        sys.stderr.write("⚠️ content có vẻ chứa SỐ tuyệt đối — KB không lưu số (data live).\n")
    nid = f"L{len(recs) + 1:04d}"
    full = {"id": nid, "ts": _now(), "type": typ, "topic": topic, "content": content, "source": source,
            "confidence": conf, "status": "pending", "content_hash": ch, "fact_key": fact_key(probe),
            "supersedes": [], "superseded_by": None}
    recs.append(full); _write(log, recs)
    near = [r["id"] for r in recs if r.get("fact_key") == full["fact_key"] and r["id"] != nid and r.get("status") in ACTIVE]
    return {"status": "added", "id": nid, "fact_key": full["fact_key"], "near_dup": near}

def find_contradictions(target, log=None):
    recs = _read(log or default_log())
    tgt = next((r for r in recs if r.get("id") == target), None)
    fk = tgt["fact_key"] if tgt else target
    th = tgt.get("content_hash") if tgt else None
    return [r["id"] for r in recs if r.get("fact_key") == fk and r.get("status") == "promoted" and r.get("content_hash") != th]

def supersede(new_id, old_id, reason, verify_ref, log=None):
    log = Path(log or default_log()); recs = _read(log)
    idx = {r.get("id"): r for r in recs}
    if new_id not in idx or old_id not in idx:
        return {"status": "error", "msg": "id không tồn tại"}
    nw, od = idx[new_id], idx[old_id]
    if nw.get("fact_key") != od.get("fact_key"):
        return {"status": "error", "msg": f"fact_key khác ({nw.get('fact_key')} vs {od.get('fact_key')}) — không supersede chéo chủ thể"}
    od["status"] = "superseded"; od["superseded_by"] = new_id; od["superseded_ts"] = _now()
    nw.setdefault("supersedes", [])
    if old_id not in nw["supersedes"]: nw["supersedes"].append(old_id)
    nw["status"] = "promoted"; nw["supersede_reason"] = reason; nw["verify_ref"] = verify_ref; nw["promoted_ts"] = _now()
    _write(log, recs)
    return {"status": "superseded", "old": old_id, "new": new_id}

# ── Typed promote-gate (D6) — KHỚP kb_route.classify(type).gate ──
# need_any: thỏa nếu MỘT nhóm key có đủ (truthy) trong evidence. [[]] = nhẹ (review).
_GATE = {
    "new_dataset":      {"need_any": [["rebuild_sha"]]},
    "new_dataflow":     {"need_any": [["rebuild_sha"]]},
    "new_field":        {"need_any": [["rebuild_sha"]]},
    "physical_table":   {"need_any": [["rebuild_sha"]]},
    "fact":             {"need_any": [["rebuild_sha"]]},
    "formula_correction": {"need_any": [["rebuild_sha"], ["live_evidence"]]},
    "correction":       {"need_any": [["provenance"]], "source_ok": ["user", "owner"]},
    "glossary_term":    {"need_any": [["attested_by"]]},
    "convention":       {"need_any": [["attested_by"]]},
    "governance_item":  {"need_any": [["attested_by"]], "human_only": True},
    "lesson":           {"need_any": [["incorporated_into"]]},
    "qa":               {"need_any": [[]]},
}
_NO_PROMOTE = {"gap", "drift"}   # gap → open-question; drift → drift store (không promote thành fact)

def promote(rid, evidence=None, log=None):
    """Promote theo loại + chặn contradiction chưa supersede. Trả {status, reason}."""
    evidence = evidence or {}
    log = Path(log or default_log()); recs = _read(log)
    idx = {r.get("id"): r for r in recs}
    if rid not in idx:
        return {"status": "error", "msg": f"{rid} không tồn tại"}
    rec = idx[rid]; typ = rec.get("type")
    if typ in _NO_PROMOTE:
        return {"status": "rejected", "reason": f"type '{typ}' KHÔNG promote thành fact (→ open-question / drift store)"}
    contra = [c for c in find_contradictions(rid, log=log) if c != rid]
    if contra:
        return {"status": "rejected", "reason": f"mâu thuẫn với {contra} (cùng fact_key, promoted) — phải `supersede` trước"}
    rule = _GATE.get(typ)
    if rule is None:
        return {"status": "rejected", "reason": f"type '{typ}' chưa có gate (thêm vào _GATE)"}
    if rule.get("human_only") and str(evidence.get("via", "")).lower() in ("auto", "second-agent", "llm"):
        return {"status": "rejected", "reason": "governance KHÔNG auto/second-agent — cần người (owner/CFO) ký"}
    src_ok = any(k in (rec.get("source", "") or "").lower() for k in rule.get("source_ok", []))
    satisfied = any(all(evidence.get(k) for k in req) for req in rule["need_any"])
    if not (satisfied or src_ok):
        need = " HOẶC ".join("+".join(r) or "(review)" for r in rule["need_any"])
        extra = f" hoặc source∈{rule['source_ok']}" if rule.get("source_ok") else ""
        return {"status": "rejected", "reason": f"thiếu bằng chứng cho '{typ}': cần {need}{extra}"}
    rec["status"] = "promoted"; rec["promoted_ts"] = _now()
    for k in ("rebuild_sha", "live_evidence", "attested_by", "incorporated_into", "provenance", "verify_ref", "via"):
        if evidence.get(k): rec[k] = evidence[k]
    _write(log, recs)
    return {"status": "promoted", "id": rid, "type": typ}

def lst(status="all", log=None):
    for r in _read(log or default_log()):
        if status == "all" or r.get("status") == status:
            print(f"{r.get('id')} [{r.get('status')}] {r.get('type')} <{r.get('fact_key')}>: {r.get('topic')}")

def cli(argv):
    if not argv: sys.stderr.write(__doc__ + "\n"); return 2
    cmd = argv[0]
    if cmd == "migrate":
        print(json.dumps(migrate(), ensure_ascii=False)); return 0
    if cmd == "add" and len(argv) >= 4:
        print(json.dumps(add(argv[1], argv[2], argv[3], argv[4] if len(argv) > 4 else "", argv[5] if len(argv) > 5 else "medium"), ensure_ascii=False)); return 0
    if cmd == "contradictions" and len(argv) >= 2:
        print(json.dumps(find_contradictions(argv[1]), ensure_ascii=False)); return 0
    if cmd == "supersede" and len(argv) >= 5:
        print(json.dumps(supersede(argv[1], argv[2], argv[3], argv[4]), ensure_ascii=False)); return 0
    if cmd == "promote" and len(argv) >= 2:
        ev = {}
        if len(argv) > 2:
            try: ev = json.loads(argv[2])
            except Exception: ev = {}
        r = promote(argv[1], ev)
        print(json.dumps(r, ensure_ascii=False))
        return 0 if r.get("status") == "promoted" else 1
    if cmd == "list":
        lst(argv[1] if len(argv) > 1 else "all"); return 0
    sys.stderr.write(__doc__ + "\n"); return 2

if __name__ == "__main__":
    sys.exit(cli(sys.argv[1:]))
