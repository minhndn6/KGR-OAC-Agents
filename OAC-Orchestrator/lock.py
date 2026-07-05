#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""File-based write-lock theo artifact (workbook path / dataflow id) cho orchestrator.
Reads KHÔNG cần lock; chỉ writer (dashboard-builder/dataflow-builder) acquire trước khi Save/Run.
Usage:
  python lock.py acquire "<artifact>" "<holder>" [ttl_sec]
  python lock.py release "<artifact>" "<holder>"
  python lock.py status  "<artifact>"
"""
import sys, os, json, time, re

# Lock dir NGOÀI cây project (_kgr-state sibling; ngoài crawl, trong backup) — tự-định-vị, override KGR_LOCK_DIR/KGR_STATE_ROOT.
_WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # OAC-Orchestrator -> workspace
_STATE = os.environ.get("KGR_STATE_ROOT") or os.path.join(os.path.dirname(_WS), "_kgr-state")
LOCK_DIR = os.environ.get("KGR_LOCK_DIR") or os.path.join(_STATE, "orchestration", "locks")
DEFAULT_TTL = 1800  # 30'

def slug(a): return re.sub(r'[^0-9A-Za-z._-]+', '_', a).strip('_')[:120]
def path(a): return os.path.join(LOCK_DIR, slug(a) + ".lock")

def read(a):
    p = path(a)
    if not os.path.exists(p): return None
    try: return json.load(open(p, encoding="utf-8"))
    except Exception: return {"corrupt": True}

def _atomic_write(p, payload):
    """tmp + os.replace => không bao giờ để lại lock-file ghi nửa vời (corrupt)."""
    tmp = p + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False)
    os.replace(tmp, p)

def acquire(a, holder, ttl=DEFAULT_TTL):
    os.makedirs(LOCK_DIR, exist_ok=True)
    p = path(a); now = time.time()
    payload = {"artifact": a, "holder": holder, "ts": now, "ttl": ttl}
    # Fast path ATOMIC: O_EXCL create — nếu lock trống, CHỈ 1 writer thắng cuộc đua
    # (chống TOCTOU last-writer-wins: trước đây 2 writer cùng read trống rồi cùng ghi).
    try:
        fd = os.open(p, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False)
        return True, f"ACQUIRED by {holder}"
    except FileExistsError:
        pass
    cur = read(a)
    if cur and cur.get("corrupt"):
        # KHÔNG steal âm thầm lock hỏng. Trước đây bất kỳ ai cũng cướp được (bỏ qua TTL),
        # mà lock hỏng chính là sản phẩm của 1 lần ghi crash giữa chừng → vỡ loại-trừ tương hỗ.
        return False, f"REFUSED: lock '{a}' corrupt — cần xác minh thủ công rồi 'release'/xóa file"
    if cur:
        if cur.get("holder") == holder:
            _atomic_write(p, payload); return True, f"ACQUIRED by {holder} (re-entrant)"
        if now - cur.get("ts", 0) < cur.get("ttl", DEFAULT_TTL):
            return False, f"LOCKED by {cur.get('holder')} (còn {int(cur['ttl']-(now-cur['ts']))}s)"
        # quá TTL = stale. CẢNH BÁO: lock.py KHÔNG kiểm được liveness; orchestrator PHẢI
        # tự xác nhận holder cũ không còn sống trước khi tin steal (failure_policy.recovery.stale_lock).
        _atomic_write(p, payload); return True, f"ACQUIRED by {holder} (stole stale của {cur.get('holder')})"
    # cur is None (file vừa biến mất sau khi O_EXCL báo tồn tại) → ghi lại
    _atomic_write(p, payload); return True, f"ACQUIRED by {holder}"

def release(a, holder):
    cur = read(a)
    if not cur: return True, "no lock"
    if cur.get("holder") != holder:
        return False, f"REFUSED: held by {cur.get('holder')}, not {holder}"
    os.remove(path(a)); return True, "RELEASED"

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(2)
    cmd, art = sys.argv[1], sys.argv[2]
    if cmd == "status":
        print(json.dumps(read(art), ensure_ascii=False)); sys.exit(0)
    holder = sys.argv[3] if len(sys.argv) > 3 else "?"
    ttl = int(sys.argv[4]) if len(sys.argv) > 4 else DEFAULT_TTL
    ok, msg = (acquire(art, holder, ttl) if cmd == "acquire" else release(art, holder))
    print(msg); sys.exit(0 if ok else 1)
