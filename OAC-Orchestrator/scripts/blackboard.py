#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Blackboard runtime cho orchestrator (O1 read-only/advisory).
State object dùng chung; orchestrator là single-writer. KHÔNG lưu số tuyệt đối.

Bền vững (xem agent_contracts.yaml failure_policy.recovery):
  - Ghi atomic: tmp -> os.replace; giữ .bak last-known-good => crash khi ghi KHÔNG hỏng state.
  - step/fail/recover: theo dõi trạng thái từng bước để resume sạch sau lỗi/crash/compact.

Usage:
  python blackboard.py new "<request>" ["<period>"]            -> tạo instance, in id
  python blackboard.py get  <id>
  python blackboard.py set  <id> <dotted.field> <json_value>
  python blackboard.py log  <id> <agent> <action> "<summary>"
  python blackboard.py step <id> <name> <pending|running|ok|fail|skipped|interrupted> ["<error>"]
  python blackboard.py fail <id> "<reason>"                     -> đánh dấu run failed + escalate
  python blackboard.py recover <id>                             -> phục hồi sau crash, in report JSON
  python blackboard.py list
"""
import sys, os, json, time, re, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # OAC-Orchestrator/
_WS = os.path.dirname(ROOT)  # workspace root
# D9: durable resume state NGOÀI cây repo (agent không crawl → đỡ token) và KHÔNG ở %LOCALAPPDATA% (wipe = mất recover).
# Đặt ở <workspace>.parent/_kgr-state/orchestration/blackboards: SIBLING project (ngoài crawl) NHƯNG trong backup.
# Giữ BB_DIR là biến global (test_orchestrator.py reassign được); override qua env KGR_BB_DIR/KGR_ORCH_DIR/KGR_STATE_ROOT.
_STATE = os.environ.get("KGR_STATE_ROOT") or os.path.join(os.path.dirname(_WS), "_kgr-state")
BB_DIR = os.environ.get("KGR_BB_DIR") or os.path.join(
    os.environ.get("KGR_ORCH_DIR") or os.path.join(_STATE, "orchestration"), "blackboards")
TEMPLATE = os.path.join(ROOT, "blackboard.template.json")
STEP_STATES = ("pending", "running", "ok", "fail", "skipped", "interrupted")
MAX_ATTEMPTS = 3   # failure_policy.retry.max_attempts — enforce ở code, không chỉ trên giấy

def _load_tpl():
    with open(TEMPLATE, encoding="utf-8") as f:
        return json.load(f)

def _path(bid): return os.path.join(BB_DIR, bid + ".json")

def _valid(p):
    try:
        with open(p, encoding="utf-8") as f:
            json.load(f)
        return True
    except Exception:
        return False

def _read(bid):
    """Crash-safe read: main là authoritative (os.replace atomic). Nếu main hỏng/mất,
    thử phục hồi từ .bak. .tmp sót lại = ghi dở -> bỏ qua (để recover dọn)."""
    p = _path(bid)
    if not _valid(p):
        bak = p + ".bak"
        if _valid(bak):
            shutil.copy2(bak, p)            # tự lành từ last-known-good
        else:
            raise SystemExit(f"blackboard {bid} hỏng và không có .bak hợp lệ — chạy 'recover {bid}'")
    with open(p, encoding="utf-8") as f:
        return json.load(f)

def _write(bid, obj):
    os.makedirs(BB_DIR, exist_ok=True)
    obj["updated_at"] = _now()
    p = _path(bid); tmp = p + ".tmp"
    if os.path.exists(p):
        try: shutil.copy2(p, p + ".bak")    # last-known-good trước khi đè
        except Exception: pass
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    os.replace(tmp, p)                       # atomic: crash => hoặc bản cũ, hoặc bản mới, không bao giờ nửa vời

def _now():  # ISO-ish; ok for a runtime helper (not a Workflow script)
    return time.strftime("%Y-%m-%dT%H:%M:%S")

def _log(bb, agent, action, summary):
    bb.setdefault("log", []).append({"ts": _now(), "agent": agent, "action": action, "summary": str(summary)[:120]})

def new(request, period=None):
    bb = _load_tpl()
    bb["request"] = request
    if period: bb["period"] = period
    bb["mode"] = "O1-readonly-advisory"   # ghi rõ: KHÔNG tự ghi OAC
    bb["status"] = "active"
    bb.setdefault("steps", {})
    _log(bb, "orchestrator", "create", request[:80])
    bid = "bb_" + re.sub(r"[^0-9]", "", _now())[-12:]
    _write(bid, bb)
    print(bid)

def setf(bid, dotted, raw):
    bb = _read(bid)
    try: val = json.loads(raw)
    except Exception: val = raw
    node = bb; keys = dotted.split(".")
    for k in keys[:-1]: node = node.setdefault(k, {})
    node[keys[-1]] = val
    _log(bb, "orchestrator", "set " + dotted, str(val)[:80])
    _write(bid, bb); print("ok")

def logf(bid, agent, action, summary):
    bb = _read(bid)
    _log(bb, agent, action, summary)
    _write(bid, bb); print("ok")

def step(bid, name, state, error=None):
    if state not in STEP_STATES:
        raise SystemExit(f"state phải thuộc {STEP_STATES}")
    bb = _read(bid)
    steps = bb.setdefault("steps", {})
    st = steps.setdefault(name, {"state": "pending", "attempts": 0, "last_error": None})
    if state == "running":
        st["attempts"] = st.get("attempts", 0) + 1   # đếm cho retry (failure_policy.retry.max_attempts)
        if st["attempts"] > MAX_ATTEMPTS:
            # ENFORCE retry cap: cạn retry -> fail + escalate, KHÔNG để vòng lặp vô hạn
            # (failure_policy.retry.on_exhausted; "đã từng 529 Overloaded ×2").
            st["state"] = "fail"
            st["last_error"] = f"retry exhausted: attempts={st['attempts']} > max_attempts={MAX_ATTEMPTS}"
            bb["status"] = "failed"
            bb.setdefault("open_questions", []).append(
                {"ts": _now(), "type": "retry_exhausted", "detail": f"step '{name}' cạn retry ({st['attempts']} lần)"})
            _log(bb, "orchestrator", f"step {name} -> fail (retry exhausted)", st["last_error"])
            _write(bid, bb)
            print(json.dumps(st, ensure_ascii=False)); return
    st["state"] = state
    if error: st["last_error"] = error[:200]
    if state == "fail":
        bb["status"] = "failed"
    _log(bb, "orchestrator", f"step {name} -> {state}", error or "")
    _write(bid, bb)
    print(json.dumps(st, ensure_ascii=False))

def fail(bid, reason):
    bb = _read(bid)
    bb["status"] = "failed"
    bb.setdefault("open_questions", []).append({"ts": _now(), "type": "failure", "detail": reason[:200]})
    _log(bb, "orchestrator", "FAIL", reason)
    _write(bid, bb); print("failed")

def recover(bid):
    """Phục hồi sau crash/compact. main an toàn nhờ os.replace; việc của recover:
    (1) lành main từ .bak nếu cần, (2) dọn .tmp ghi-dở, (3) step 'running' lúc crash -> 'interrupted'
    (resume được), (4) liệt kê blocker (open_questions, write_lock_holder cần verify)."""
    p = _path(bid); tmp = p + ".tmp"; bak = p + ".bak"
    report = {"id": bid, "actions": [], "issues": []}
    if not _valid(p):
        if _valid(bak):
            shutil.copy2(bak, p); report["actions"].append("restored main from .bak")
        else:
            report["issues"].append("main missing/corrupt & no valid .bak — UNRECOVERABLE")
            print(json.dumps(report, ensure_ascii=False, indent=2)); return
    if os.path.exists(tmp):
        try: os.remove(tmp); report["actions"].append("removed stale .tmp (interrupted write; main intact)")
        except Exception as e: report["issues"].append(f".tmp cleanup failed: {e}")
    bb = _read(bid)
    for name, st in (bb.get("steps") or {}).items():
        if st.get("state") == "running":
            st["state"] = "interrupted"
            report["actions"].append(f"step '{name}' running@crash -> interrupted (resumable, attempts={st.get('attempts')})")
    if bb.get("open_questions"):
        report["issues"].append(f"{len(bb['open_questions'])} open_question(s) chặn — cần owner/user")
    if bb.get("write_lock_holder"):
        report["issues"].append(f"write_lock_holder={bb['write_lock_holder']} — verify 'lock.py status' trước khi resume write")
    interrupted = [n for n, s in (bb.get("steps") or {}).items() if s.get("state") in ("interrupted", "fail", "pending")]
    bb["status"] = "needs_resume" if interrupted else bb.get("status", "active")
    report["status"] = bb["status"]
    report["resume_steps"] = interrupted
    _log(bb, "orchestrator", "recover", f"status={bb['status']} resume={interrupted}")
    _write(bid, bb)
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    a = sys.argv
    if len(a) < 2: print(__doc__); sys.exit(2)
    cmd = a[1]
    if cmd == "new": new(a[2], a[3] if len(a) > 3 else None)
    elif cmd == "get": print(json.dumps(_read(a[2]), ensure_ascii=False, indent=2))
    elif cmd == "set": setf(a[2], a[3], a[4])
    elif cmd == "log": logf(a[2], a[3], a[4], a[5] if len(a) > 5 else "")
    elif cmd == "step": step(a[2], a[3], a[4], a[5] if len(a) > 5 else None)
    elif cmd == "fail": fail(a[2], a[3])
    elif cmd == "recover": recover(a[2])
    elif cmd == "list":
        print("\n".join(sorted(f[:-5] for f in os.listdir(BB_DIR) if f.endswith(".json"))) if os.path.isdir(BB_DIR) else "(none)")
    else: print("unknown cmd"); sys.exit(2)
