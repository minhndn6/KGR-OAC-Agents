#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""drift — drift store "bám kịp OAC" (D7/D8/INV-6) CÓ chống nhiễu/bão. Test OFFLINE bằng fixture freshness.
Nguyên tắc: observe → debounce (≥N) → open → emit (cooldown) → auto-resolve sau rebuild. Upsert theo drift_key.
LỌC timestamp hợp lệ (99/203 datasource thiếu lastModifiedTime — L0010) trước khi so.
State DURABLE (kgr_runtime orch_dir), KHÔNG trong repo. `now` = int (logical/epoch) để test xác định.
KHÔNG gọi OAC ở đây — chỉ xử lý observation đã có (live-probe là tầng trên, hoãn tới khi owner login).
"""
import sys, json, re, hashlib
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parent))
import kgr_runtime  # noqa: E402

TS_RE = re.compile(r"^\d{4}-\d{2}")
DEBOUNCE = 2
STORM_K = 10
COOLDOWN = 86400

def state_path():
    return kgr_runtime.orch_dir(start=str(HERE)) / "drift_state.json"

def _norm(s):
    return re.sub(r"\s+", " ", str(s).strip()).casefold()

def drift_key(probe, target, observed):
    return hashlib.sha1(f"{probe}|{target}|{_norm(observed)}".encode("utf-8")).hexdigest()[:16]

def load_state(path=None):
    p = Path(path or state_path())
    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {}

def save_state(state, path=None):
    p = Path(path or state_path()); kgr_runtime.ensure(p.parent)
    p.write_text(json.dumps(state, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")

def freshness_observations(fixture_path, baseline_iso):
    """Từ snapshot freshness → observation drift. LỌC ts không hợp lệ; chỉ asset đổi >= baseline."""
    data = json.loads(Path(fixture_path).read_text(encoding="utf-8"))
    obs, skipped = [], 0
    for it in (data.get("items") or []):
        lm = it.get("lastModified") or ""
        if not TS_RE.match(lm):
            skipped += 1; continue                      # 99 connector thiếu ts -> bỏ (chống nhiễu)
        if lm >= baseline_iso:                          # đổi tại/sau ngày trích -> nghi drift
            obs.append({"probe": "freshness", "target": it.get("name"), "observed": lm, "expected": baseline_iso})
    return obs, skipped

def observe(observations, state, now, debounce=DEBOUNCE, storm_k=STORM_K):
    """Upsert observation vào state. Debounce ≥N mới 'open'. Storm (>K NEW/lần) -> 1 bulk record."""
    new_keys = []
    for o in observations:
        k = drift_key(o["probe"], o["target"], o["observed"])
        e = state.get(k)
        if e is None:
            e = {"key": k, "probe": o["probe"], "target": o.get("target"), "observed": o.get("observed"),
                 "expected": o.get("expected"), "first_seen": now, "last_seen": now, "hit_count": 1, "state": "seen"}
            state[k] = e; new_keys.append(k)
        else:
            e["hit_count"] += 1; e["last_seen"] = now    # UPSERT: trùng -> tăng đếm, KHÔNG tạo mới
        if e["state"] == "seen" and e["hit_count"] >= debounce:   # debounce áp cho cả new lẫn cũ
            e["state"] = "open"; e["opened_ts"] = now
    summary = {"new": len(new_keys), "bulk": False}
    if len(new_keys) > storm_k:                          # storm-breaker: baseline có thể stale -> 1 record gộp
        bkey = "bulk:" + str(now)
        state[bkey] = {"key": bkey, "probe": "bulk_divergence", "target": f"{len(new_keys)} targets",
                       "state": "open", "first_seen": now, "last_seen": now, "hit_count": 1,
                       "note": "storm — nghi baseline stale; dừng emit per-item"}
        for k in new_keys:
            state[k]["state"] = "suppressed_bulk"
        summary["bulk"] = True
    summary["open"] = sum(1 for e in state.values() if e.get("state") == "open")
    return summary

def to_emit(state, now):
    out = []
    for e in state.values():
        if e.get("state") != "open":
            continue
        su = e.get("suppress_until")
        if su is not None and now < su:
            continue                                     # đang trong cooldown -> không re-surface
        out.append(e)
    return out

def mark_emitted(state, now, cooldown=COOLDOWN):
    for e in state.values():
        if e.get("state") == "open":
            e["suppress_until"] = now + cooldown

def auto_resolve(state, resolved_targets, now):
    """Sau rebuild đã hấp thụ: open/seen có target thuộc resolved_targets -> resolved_stale."""
    n = 0
    rs = set(resolved_targets)
    for e in state.values():
        if e.get("state") in ("open", "seen") and e.get("target") in rs:
            e["state"] = "resolved_stale"; e["resolved_ts"] = now; n += 1
    return n

def main(argv):
    # CLI tiện ích: từ fixture -> observe -> in summary (state durable). now lấy từ time (script thường, không phải Workflow).
    import time
    if not argv or argv[0] != "scan-fixture" or len(argv) < 3:
        sys.stderr.write("Usage: drift.py scan-fixture <fixture.json> <baseline_iso>\n"); return 2
    obs, skipped = freshness_observations(argv[1], argv[2])
    state = load_state()
    summ = observe(obs, state, int(time.time()))
    save_state(state)
    summ["skipped_no_ts"] = skipped
    print(json.dumps(summ, ensure_ascii=False)); return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
