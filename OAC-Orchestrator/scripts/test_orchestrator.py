#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test xác định (deterministic) cho runtime orchestrator: blackboard.py + lock.py.
Tập trung vào RESILIENCE: step/retry, fail/escalate, ghi atomic + .bak, recover sau crash.
Chạy: PYTHONUTF8=1 python scripts/test_orchestrator.py   (KHÔNG đụng state thật — dùng _work/ tạm, gitignored)
"""
import os, sys, json, io, shutil, importlib.util, contextlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TMP = os.path.join(ROOT, "_work", "test_run")          # gitignored zone (temp partitioning)

def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod

def _cap(fn, *a, **k):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        fn(*a, **k)
    return buf.getvalue().strip()

PASS = FAIL = 0
def chk(cond, label):
    global PASS, FAIL
    if cond: PASS += 1; print(f"  PASS  {label}")
    else:    FAIL += 1; print(f"  FAIL  {label}")

def main():
    if os.path.isdir(TMP): shutil.rmtree(TMP, ignore_errors=True)
    os.makedirs(TMP, exist_ok=True)

    bb = _load("blackboard", os.path.join(HERE, "blackboard.py"))
    lk = _load("lock", os.path.join(ROOT, "lock.py"))
    bb.BB_DIR = os.path.join(TMP, "blackboards")        # redirect khỏi state thật
    lk.LOCK_DIR = os.path.join(TMP, "locks")

    print("== blackboard: lifecycle ==")
    bid = _cap(bb.new, "test request", "T5-2026")
    chk(bid.startswith("bb_"), "new() trả về id")
    state = bb._read(bid)
    chk(state["status"] == "active" and state["mode"] == "O1-readonly-advisory", "init status=active, mode O1")
    chk(state["period"] == "T5-2026", "period set")

    _cap(bb.setf, bid, "verdicts.crosscheck", '"PASS"')
    chk(bb._read(bid)["verdicts"]["crosscheck"] == "PASS", "set dotted field")

    print("== blackboard: step/retry/fail ==")
    _cap(bb.step, bid, "lineage", "running")
    _cap(bb.step, bid, "lineage", "running")              # attempt 2 (retry)
    st = bb._read(bid)["steps"]["lineage"]
    chk(st["attempts"] == 2, "running tăng attempts (retry counter)")
    _cap(bb.step, bid, "lineage", "ok")
    chk(bb._read(bid)["steps"]["lineage"]["state"] == "ok", "step -> ok")
    _cap(bb.step, bid, "dataflow", "fail", "run_status=fail crosscheck mismatch")
    s2 = bb._read(bid)
    chk(s2["steps"]["dataflow"]["state"] == "fail", "step -> fail ghi nhận")
    chk(s2["status"] == "failed", "step fail nâng run.status=failed")
    chk("mismatch" in (s2["steps"]["dataflow"]["last_error"] or ""), "last_error lưu lý do")

    try:
        bb.step(bid, "x", "bogus"); bogus_rejected = False
    except SystemExit:
        bogus_rejected = True
    chk(bogus_rejected, "state lạ bị từ chối")

    print("== blackboard: retry cap (max_attempts enforce) ==")
    bid2 = _cap(bb.new, "retry cap test", "T5-2026")
    for _ in range(bb.MAX_ATTEMPTS + 1):
        _cap(bb.step, bid2, "flaky", "running")
    stx = bb._read(bid2)["steps"]["flaky"]
    chk(stx["state"] == "fail" and stx["attempts"] > bb.MAX_ATTEMPTS, "running quá max_attempts -> auto fail (cap enforce)")
    chk(any(q.get("type") == "retry_exhausted" for q in bb._read(bid2)["open_questions"]), "retry exhausted -> escalate open_question")

    print("== blackboard: fail/escalate ==")
    _cap(bb.fail, bid, "producer sống chưa chốt")
    s3 = bb._read(bid)
    chk(any(q.get("type") == "failure" for q in s3["open_questions"]), "fail() đẩy open_question (escalate)")

    print("== blackboard: atomic write + .bak last-known-good ==")
    p = bb._path(bid)
    chk(os.path.exists(p + ".bak"), ".bak được tạo sau >1 lần ghi")
    # mô phỏng main hỏng (đĩa lỗi / ghi nửa vời ở tầng khác) -> _read tự lành từ .bak
    good = open(p, encoding="utf-8").read()
    open(p, "w", encoding="utf-8").write("{ corrupt json")
    healed = bb._read(bid)                                # phải phục hồi, không nổ
    chk(isinstance(healed, dict) and "request" in healed, "_read tự lành main hỏng từ .bak")

    print("== blackboard: recover sau crash ==")
    # dựng cảnh crash: 1 step 'running' + 1 file .tmp ghi-dở sót lại
    _cap(bb.step, bid, "dashboard", "running")
    open(p + ".tmp", "w", encoding="utf-8").write("{ half-written")
    rep = json.loads(_cap(bb.recover, bid))
    chk(not os.path.exists(p + ".tmp"), "recover dọn .tmp ghi-dở")
    chk(bb._read(bid)["steps"]["dashboard"]["state"] == "interrupted", "running@crash -> interrupted (resume được)")
    chk("dashboard" in rep["resume_steps"], "recover liệt kê resume_steps")
    chk(bb._read(bid)["status"] == "needs_resume", "status -> needs_resume khi còn bước dở")

    print("== lock: acquire / re-entrant / contend / steal-stale / release ==")
    ok, _ = lk.acquire("DB02.Expense", "dashboard"); chk(ok, "acquire lock trống")
    ok, _ = lk.acquire("DB02.Expense", "dashboard"); chk(ok, "re-entrant cùng holder OK")
    ok, msg = lk.acquire("DB02.Expense", "dataflow"); chk((not ok) and "LOCKED" in msg, "holder khác bị từ chối (chống last-writer-wins)")
    ok, msg = lk.release("DB02.Expense", "dataflow"); chk(not ok, "release sai holder bị từ chối")
    ok, _ = lk.acquire("DB02.Expense", "dataflow", ttl=0);
    # ttl=0 ở lần acquire này không giúp; mô phỏng stale bằng cách set ts cũ
    import time as _t
    lp = lk.path("Reload.flow")
    os.makedirs(lk.LOCK_DIR, exist_ok=True)
    json.dump({"artifact": "Reload.flow", "holder": "ghost", "ts": _t.time() - 99999, "ttl": 1800}, open(lp, "w", encoding="utf-8"))
    ok, _ = lk.acquire("Reload.flow", "dataflow"); chk(ok, "steal lock quá TTL (ghost holder)")
    ok, _ = lk.release("Reload.flow", "dataflow"); chk(ok, "release đúng holder OK")

    print(f"\n== TỔNG: PASS={PASS} FAIL={FAIL} ==")
    shutil.rmtree(TMP, ignore_errors=True)                # dọn sạch temp zone
    sys.exit(1 if FAIL else 0)

if __name__ == "__main__":
    main()
