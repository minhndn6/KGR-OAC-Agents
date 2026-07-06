#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""File-based write-lock theo artifact (workbook path / dataflow id) cho orchestrator.
Reads KHÔNG cần lock; chỉ writer (dashboard-builder/dataflow-builder) acquire trước khi Save/Run.
Usage:
  python lock.py acquire "<artifact>" "<holder>" [ttl_sec]
  python lock.py renew   "<artifact>" "<holder>"      # gia hạn tại checkpoint (chỉ holder hiện tại)
  python lock.py release "<artifact>" "<holder>"
  python lock.py status  "<artifact>"
  holder nên là '<actor>:<uuid8>' (lock.session_holder("<actor>")) để 2 phiên cùng actor phân biệt được.
"""
import sys, os, json, time, re, uuid, hashlib

# Lock dir NGOÀI cây project (_kgr-state sibling; ngoài crawl, trong backup) — tự-định-vị, override KGR_LOCK_DIR/KGR_STATE_ROOT.
_WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # OAC-Orchestrator -> workspace
_STATE = os.environ.get("KGR_STATE_ROOT") or os.path.join(os.path.dirname(_WS), "_kgr-state")
LOCK_DIR = os.environ.get("KGR_LOCK_DIR") or os.path.join(_STATE, "orchestration", "locks")
DEFAULT_TTL = 1800  # 30'

# Heartbeat/liveness (A13): holder PHẢI renew() định kỳ mỗi HEARTBEAT giây tại checkpoint.
# Steal window = max(2×HEARTBEAT, 600) — chỉ steal khi quá HẲN 1 nhịp heartbeat lỡ (KHÔNG dùng TTL cứng 180s;
# QA đã bác renew-60/steal-180 vì cửa sổ quá hẹp → cướp nhầm holder đang sống).
HEARTBEAT = 300
def steal_window(hb=None):
    hb = HEARTBEAT if hb is None else hb
    return max(2 * hb, 600)

def slug(a): return re.sub(r'[^0-9A-Za-z._-]+', '_', a).strip('_')[:120]
def path(a): return os.path.join(LOCK_DIR, slug(a) + ".lock")

# ── Holder-id ổn định theo PHIÊN: "<actor>:<uuid8>" ──
# 2 session CÙNG actor (vd 'dashboard') phải phân biệt được → re-entrant CHỈ khi CÙNG holder-uuid.
# uuid ổn định trong 1 process/phiên: seed từ env (KGR_SESSION_ID / máy+pid) nên gọi 2 lần trong cùng
# phiên trả GIỐNG NHAU, nhưng process khác → uuid khác (LOCKED).
def _session_seed():
    return (os.environ.get("KGR_SESSION_ID")
            or os.environ.get("CLAUDE_SESSION_ID")
            or f"{uuid.getnode()}:{os.getpid()}")

def session_holder(actor="agent"):
    """Sinh holder-id ổn định theo phiên: '<actor>:<uuid8>'. Cùng phiên → cùng id; phiên khác → khác id."""
    suf = hashlib.sha256(_session_seed().encode("utf-8")).hexdigest()[:8]
    return f"{actor}:{suf}"

# alias để orchestrator gọi tên nào cũng được
holder_id = session_holder

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

def _stale_after(cur):
    """Thời điểm (giây kể từ ts) mà lock được coi là stale = steal-window theo heartbeat của lock đó.
    Ưu tiên heartbeat lưu trong lock; fallback HEARTBEAT hiện tại → window = max(2×hb, 600)."""
    hb = cur.get("heartbeat", HEARTBEAT)
    try: hb = float(hb)
    except (TypeError, ValueError): hb = HEARTBEAT
    return steal_window(hb)

def acquire(a, holder, ttl=DEFAULT_TTL):
    os.makedirs(LOCK_DIR, exist_ok=True)
    p = path(a); now = time.time()
    payload = {"artifact": a, "holder": holder, "ts": now, "ttl": ttl, "heartbeat": HEARTBEAT}
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
        # STALE = quá STEAL-WINDOW = max(2×heartbeat, 600s) KHÔNG renew (KHÔNG phải TTL cứng).
        # Trong window → coi holder còn sống, TỪ CHỐI (chống cướp nhầm holder đang chạy chậm/giữa 2 nhịp).
        age = now - cur.get("ts", 0)
        window = _stale_after(cur)
        if age < window:
            return False, f"LOCKED by {cur.get('holder')} (còn {int(window - age)}s tới steal-window)"
        # quá steal-window = stale. CẢNH BÁO: lock.py KHÔNG kiểm được LIVENESS; orchestrator PHẢI
        # tự xác nhận holder cũ không còn sống (đã chết) trước khi TIN steal — steal-window chỉ là
        # ngưỡng "đủ lâu không heartbeat", không đảm bảo holder đã chết (failure_policy.recovery.stale_lock).
        _atomic_write(p, payload); return True, f"ACQUIRED by {holder} (stole stale của {cur.get('holder')})"
    # cur is None (file vừa biến mất sau khi O_EXCL báo tồn tại) → ghi lại
    _atomic_write(p, payload); return True, f"ACQUIRED by {holder}"

def renew(a, holder):
    """Gia hạn lock tại checkpoint: cập nhật ts/heartbeat để KHÔNG bị steal. CHỈ holder hiện tại renew được.
    Trả (True, msg) nếu gia hạn OK; (False, msg) nếu không phải holder / không có lock / lock hỏng."""
    cur = read(a)
    if not cur:
        return False, f"REFUSED: '{a}' không có lock để renew"
    if cur.get("corrupt"):
        return False, f"REFUSED: lock '{a}' corrupt — không renew (xác minh thủ công)"
    if cur.get("holder") != holder:
        return False, f"REFUSED: held by {cur.get('holder')}, not {holder}"
    payload = dict(cur)
    payload["ts"] = time.time()
    payload["heartbeat"] = payload.get("heartbeat", HEARTBEAT)
    _atomic_write(path(a), payload)
    return True, f"RENEWED by {holder}"

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
    if cmd == "acquire":   ok, msg = acquire(art, holder, ttl)
    elif cmd == "renew":   ok, msg = renew(art, holder)
    else:                  ok, msg = release(art, holder)
    print(msg); sys.exit(0 if ok else 1)
