#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TDD acceptance — Council Sprint 5 (CUỐI).

A13 — lock.py chắc hơn cho đa-session (OAC-Orchestrator/lock.py):
  - renew(artifact, holder): gia hạn lock (cập nhật ts/heartbeat) tại checkpoint; CHỈ holder hiện tại.
  - STEAL window = max(2×heartbeat_interval, 600s) — KHÔNG phải TTL cứng 180s.
    Không steal trong window; steal SAU window.
  - holder = "<actor>:<uuid8>" để 2 session cùng actor phân biệt; re-entrant CHỈ khi cùng holder-uuid.
    Helper sinh holder-id ổn định theo session (env/uuid).
  - Giữ O_EXCL atomic + refuse-corrupt + release-chỉ-holder; KHÔNG phá test_orchestrator.

A12 — Chính sách sửa df/wb an toàn (POLICY, KHÔNG thực thi OAC):
  - edit_safety.backup_name(original, date_iso) -> "<original>_bk_YYYY-MM-DD" (ISO, KHÔNG ddmmyyyy).
  - detect task-type EDIT vs ADD theo mô tả/diff (KHÔNG để builder tự-khai).
  - 3 SKILL.md có policy (confirm-gate + _bk_YYYY-MM-DD + BACKUP-only).

A17 — MASTERY self-update qua GENERATED (bỏ dual-write):
  - build_mastery_section.py: đọc lesson ĐÃ PROMOTED từ learnings/log.jsonl (log GIẢ) ->
    sinh MỘT section GENERATED (deterministic, promoted-only, có banner). KHÔNG số cứng.

Chạy: PYTHONUTF8=1 python kb_lifecycle/tests/test_council_sprint5.py
"""
import sys, os, json, time, tempfile, shutil, importlib.util, subprocess
from pathlib import Path

HERE = Path(__file__).resolve()
WS = HERE.parents[3]                                   # <ws>/OAC-Knowledge/kb_lifecycle/tests -> <ws>
LOCK_PY = WS / "OAC-Orchestrator" / "lock.py"
EDIT_SAFETY = WS / "OAC-Orchestrator" / "skill" / "kgr-oac-orchestrator" / "scripts" / "edit_safety.py"
BUILD_MASTERY = WS / "OAC-Knowledge" / "kb_lifecycle" / "tools" / "build_mastery_section.py"

DASH_SKILL = WS / "Dashboard-builder" / ".claude" / "skills" / "oac-dashboard-builder" / "SKILL.md"
FLOW_SKILL = WS / "Dataflow-builder" / ".claude" / "skills" / "oac-dataflow-builder" / "SKILL.md"
ORCH_SKILL = WS / "OAC-Orchestrator" / "skill" / "kgr-oac-orchestrator" / "SKILL.md"

PASS = FAIL = 0
def chk(c, l):
    global PASS, FAIL
    if c: PASS += 1; print(f"  PASS  {l}")
    else: FAIL += 1; print(f"  FAIL  {l}")

def _read(p):
    try: return Path(p).read_text(encoding="utf-8")
    except Exception: return ""

def _load(name, path):
    if not Path(path).is_file(): return None
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod); return mod
    except Exception as e:
        chk(False, f"import {name} raise {e!r}"); return None


# ─────────────────────────── A13 · lock.py multi-session ───────────────────────────
def a13_lock_tests():
    print("\n== A13: lock.py — renew / steal-window / holder-uuid / re-entrant ==")
    chk(LOCK_PY.is_file(), f"lock.py tồn tại: {LOCK_PY}")
    # hermetic: KGR_LOCK_DIR = temp riêng
    tmp = tempfile.mkdtemp(prefix="kgr_lock_s5_")
    os.environ["KGR_LOCK_DIR"] = os.path.join(tmp, "locks")
    lk = _load("lock_s5", LOCK_PY)
    if lk is None:
        shutil.rmtree(tmp, ignore_errors=True); return
    # đảm bảo module đọc env (nếu module cache LOCK_DIR lúc import, ép lại)
    lk.LOCK_DIR = os.path.join(tmp, "locks")

    try:
        # --- helper sinh holder-id ổn định theo session ("<actor>:<uuid8>") ---
        gen = None
        for nm in ("session_holder", "holder_id", "make_holder", "new_holder"):
            if hasattr(lk, nm): gen = getattr(lk, nm); break
        chk(gen is not None, "lock.py có helper sinh holder-id (session_holder/holder_id/…)")
        if gen is not None:
            h1 = gen("dashboard"); h2 = gen("dashboard")
            chk(isinstance(h1, str) and h1.startswith("dashboard:"),
                "holder-id dạng '<actor>:<uuid8>'")
            # ổn định TRONG cùng session (gọi 2 lần -> giống nhau)
            chk(h1 == h2, "helper ổn định trong cùng session (cùng process/env -> cùng holder-id)")
            suf = h1.split(":", 1)[1]
            chk(len(suf) >= 8, "holder-id có phần uuid >= 8 ký tự")

        # --- renew: chỉ holder hiện tại gia hạn được, cập nhật ts ---
        has_renew = hasattr(lk, "renew")
        chk(has_renew, "lock.py có hàm renew(artifact, holder)")
        A = "WB.Renew"
        ok, _ = lk.acquire(A, "sessA")
        chk(ok, "acquire lock trống (sessA)")
        if has_renew:
            cur0 = lk.read(A); ts0 = cur0.get("ts")
            time.sleep(0.02)
            ok, msg = lk.renew(A, "sessA")
            chk(ok, f"renew bởi holder hiện tại OK ({msg})")
            cur1 = lk.read(A); ts1 = cur1.get("ts")
            chk(ts1 is not None and ts0 is not None and ts1 > ts0,
                "renew cập nhật ts (heartbeat tiến lên)")
            # renew bởi holder KHÁC bị từ chối
            ok, msg = lk.renew(A, "sessB")
            chk(not ok, "renew bởi holder KHÁC bị từ chối")
        lk.release(A, "sessA")

        # --- steal window = max(2×heartbeat, 600). Không steal trong window; steal SAU. ---
        B = "WB.Window"
        p = lk.path(B)
        os.makedirs(lk.LOCK_DIR, exist_ok=True)
        # heartbeat mặc định của module (nếu có), fallback 300 -> window 600
        hb = getattr(lk, "HEARTBEAT", getattr(lk, "HEARTBEAT_INTERVAL", 300))
        window = max(2 * hb, 600)
        # lock stale "vừa phải": quá TTL cũ (180/1800) NHƯNG CHƯA quá steal-window
        # -> KHÔNG được steal (đây chính là điểm QA bác renew-60/steal-180).
        aged_in = window - 60   # còn trong window
        json.dump({"artifact": B, "holder": "ghost", "ts": time.time() - aged_in,
                   "ttl": 180, "heartbeat": hb},
                  open(p, "w", encoding="utf-8"))
        ok, msg = lk.acquire(B, "thief")
        chk((not ok), f"KHÔNG steal khi CHƯA quá steal-window max(2hb,600)={window}s (msg={msg})")
        # quá steal-window -> steal được
        aged_out = window + 60
        json.dump({"artifact": B, "holder": "ghost", "ts": time.time() - aged_out,
                   "ttl": 180, "heartbeat": hb},
                  open(p, "w", encoding="utf-8"))
        ok, msg = lk.acquire(B, "thief")
        chk(ok, f"steal SAU khi quá steal-window (aged={aged_out}s) (msg={msg})")
        chk("stale" in msg.lower() or "st" in msg.lower(), "msg steal nhắc stale")
        lk.release(B, "thief")

        # cảnh báo liveness còn trong source (không tự tin steal là holder chết)
        src = _read(LOCK_PY).lower()
        chk("liveness" in src, "GIỮ cảnh báo lock.py KHÔNG kiểm liveness (orchestrator tự xác nhận)")

        # --- holder-uuid: 2 session CÙNG actor phân biệt được ---
        C = "WB.TwoSess"
        hA = "dashboard:aaaaaaaa"; hB = "dashboard:bbbbbbbb"
        ok, _ = lk.acquire(C, hA); chk(ok, "sessionA (dashboard:aaaa…) acquire OK")
        ok, msg = lk.acquire(C, hB)
        chk((not ok) and "LOCKED" in msg.upper(),
            "sessionB (dashboard:bbbb…) CÙNG actor nhưng khác uuid -> LOCKED (phân biệt)")
        # re-entrant CHỈ khi cùng holder-uuid
        ok, msg = lk.acquire(C, hA)
        chk(ok and "re-entrant" in msg.lower(), "re-entrant CHỈ khi cùng holder-uuid (hA)")
        # release sai holder bị từ chối
        ok, msg = lk.release(C, hB)
        chk(not ok, "release bởi holder-uuid khác bị từ chối")
        ok, _ = lk.release(C, hA); chk(ok, "release đúng holder-uuid OK")

    finally:
        os.environ.pop("KGR_LOCK_DIR", None)
        shutil.rmtree(tmp, ignore_errors=True)


# ─────────────────────────── A12 · edit_safety + policy ───────────────────────────
def a12_edit_safety_tests():
    print("\n== A12: edit_safety backup_name + task-type detect + policy trong SKILL.md ==")
    chk(EDIT_SAFETY.is_file(), f"edit_safety.py tồn tại: {EDIT_SAFETY}")
    es = _load("edit_safety_s5", EDIT_SAFETY)
    if es is not None:
        chk(hasattr(es, "backup_name"), "edit_safety.py có backup_name(original, date_iso)")
        if hasattr(es, "backup_name"):
            got = es.backup_name("DB01.Revenue", "2026-06-22")
            chk(got == "DB01.Revenue_bk_2026-06-22",
                f"backup_name ISO đúng khớp tiền lệ live (_bk_2026-06-22), được: {got!r}")
            # KHÔNG ddmmyyyy: 22-06-2026 không xuất hiện
            chk("22-06-2026" not in got and "220626" not in got,
                "backup_name KHÔNG dùng ddmmyyyy")
            # tên gốc có sẵn suffix vẫn append đúng ngày
            g2 = es.backup_name("KGR_DF_Nganh", "2026-07-06")
            chk(g2 == "KGR_DF_Nganh_bk_2026-07-06", f"backup_name khác: {g2!r}")

        # detect task-type EDIT vs ADD theo mô tả/diff (KHÔNG builder tự-khai)
        detect = None
        for nm in ("detect_task_type", "classify_task", "task_type", "infer_task_type"):
            if hasattr(es, nm): detect = getattr(es, nm); break
        chk(detect is not None, "edit_safety.py có hàm detect task-type (EDIT|ADD)")
        if detect is not None:
            def norm(x): return str(x).strip().upper()
            # sửa artifact CÓ SẴN -> EDIT
            r_edit = detect("Sửa lại số subtotal Kênh trên DB01.Revenue đang sai -89B",
                            target_exists=True)
            chk(norm(r_edit) == "EDIT", f"mô tả 'sửa … đang sai' + target tồn tại -> EDIT ({r_edit!r})")
            # dựng MỚI -> ADD
            r_add = detect("Tạo mới dataflow gộp doanh thu chuỗi theo ngày", target_exists=False)
            chk(norm(r_add) == "ADD", f"mô tả 'tạo mới' + target chưa có -> ADD ({r_add!r})")
            # target đã tồn tại là tín hiệu MẠNH của EDIT dù mô tả mơ hồ
            r_edit2 = detect("cập nhật canvas Overview", target_exists=True)
            chk(norm(r_edit2) == "EDIT", f"target tồn tại + 'cập nhật' -> EDIT ({r_edit2!r})")

    # policy trong 3 SKILL.md
    for label, p in [("dashboard-builder", DASH_SKILL),
                     ("dataflow-builder", FLOW_SKILL),
                     ("orchestrator", ORCH_SKILL)]:
        t = _read(p)
        low = t.lower()
        chk("_bk_yyyy-mm-dd" in low or "_bk_" in low,
            f"{label} SKILL.md nêu quy ước backup '_bk_YYYY-MM-DD'")
        chk("confirm" in low, f"{label} SKILL.md nêu confirm-gate (owner CONFIRM trước khi sửa)")
        chk("backup-only" in low or "backup only" in low or "chỉ backup" in low or "backup" in low,
            f"{label} SKILL.md nêu clone là BACKUP-only")
        chk(("edit" in low) and ("add" in low),
            f"{label} SKILL.md phân biệt task EDIT vs ADD (ADD không cần clone)")


# ─────────────────────────── A17 · build_mastery_section ───────────────────────────
def _fake_log(dirpath):
    """log.jsonl GIẢ: promoted lesson/qa + non-promoted + type khác. KHÔNG phụ thuộc log thật."""
    recs = [
        # promoted lesson liên quan OAC-mechanics -> PHẢI xuất hiện
        {"id": "L0001", "type": "lesson", "topic": "csrf save token",
         "content": "POST save workbook cần x-csrf-token; classifier chặn tự lấy.",
         "status": "promoted", "fact_key": "lesson:csrf-save-token"},
        {"id": "L0002", "type": "qa", "topic": "fan-out dedup",
         "content": "Fan-out chi phí dedup theo TRANSACTION+LINE ID.",
         "status": "promoted", "fact_key": "qa:fan-out-dedup"},
        # NON-promoted (pending) -> KHÔNG xuất hiện
        {"id": "L0003", "type": "lesson", "topic": "pending lesson chưa duyệt",
         "content": "Cái này còn pending không được nhúng.",
         "status": "pending", "fact_key": "lesson:pending"},
        # superseded -> KHÔNG xuất hiện
        {"id": "L0004", "type": "lesson", "topic": "superseded cũ",
         "content": "Fact cũ đã bị supersede.",
         "status": "superseded", "fact_key": "lesson:superseded-old"},
        # promoted nhưng type KHÔNG phải lesson/qa (vd fact) -> tùy filter; test chỉ khẳng định
        # promoted lesson/qa CHẮC CHẮN có, và pending/superseded CHẮC CHẮN không.
        {"id": "L0005", "type": "lesson", "topic": "browser profile riêng",
         "content": "Mỗi actor một profile Chrome; không kill toàn cục.",
         "status": "promoted", "fact_key": "lesson:browser-profile"},
    ]
    p = Path(dirpath) / "log.jsonl"
    with open(p, "w", encoding="utf-8") as f:
        for r in recs:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    return p


def _run_build(logp):
    """Chạy build_mastery_section.py với --log <fake>, trả stdout (str) hoặc None."""
    if not BUILD_MASTERY.is_file(): return None
    env = {**os.environ, "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"}
    r = subprocess.run([sys.executable, str(BUILD_MASTERY), "--log", str(logp)],
                       capture_output=True, text=True, encoding="utf-8", env=env)
    if r.returncode != 0:
        chk(False, f"build_mastery_section.py exit={r.returncode} stderr={ (r.stderr or '')[-300:]!r}")
        return None
    return r.stdout


def a17_mastery_tests():
    print("\n== A17: build_mastery_section — GENERATED, promoted-only, deterministic ==")
    chk(BUILD_MASTERY.is_file(), f"build_mastery_section.py tồn tại: {BUILD_MASTERY}")
    tmp = tempfile.mkdtemp(prefix="kgr_mastery_s5_")
    try:
        logp = _fake_log(tmp)
        out1 = _run_build(logp)
        if out1 is None: return
        chk(len(out1.strip()) > 0, "build_mastery_section sinh output không rỗng")

        # banner GENERATED — KHÔNG sửa tay
        low = out1.lower()
        chk("generated" in low, "output có banner GENERATED")
        chk("không sửa tay" in low or "khong sua tay" in low or "do not edit" in low,
            "banner nêu 'KHÔNG sửa tay'")

        # promoted-only: có promoted, KHÔNG có pending/superseded
        chk("csrf" in low, "promoted lesson 'csrf save token' CÓ trong output")
        chk("fan-out" in low, "promoted qa 'fan-out dedup' CÓ trong output")
        chk("browser profile" in low or "browser-profile" in low or "profile chrome" in low,
            "promoted lesson 'browser profile' CÓ trong output")
        chk("pending" not in low, "pending KHÔNG xuất hiện (topic 'pending lesson chưa duyệt' bị loại)")
        chk("supersede" not in low and "superseded" not in low,
            "superseded KHÔNG xuất hiện")

        # deterministic: chạy lần 2 -> byte-identical (không timestamp trôi)
        out2 = _run_build(logp)
        chk(out2 is not None and out1 == out2,
            "deterministic: 2 lần chạy CHO KẾT QUẢ GIỐNG HỆT (không timestamp/sort trôi)")

        # KHÔNG timestamp ISO trong output (chống trôi)
        import re as _re
        chk(_re.search(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}", out1) is None,
            "output KHÔNG chứa timestamp ISO (deterministic, không phụ thuộc giờ chạy)")

        # log RỖNG -> vẫn ra banner GENERATED (section rỗng hợp lệ), KHÔNG crash
        empty = Path(tmp) / "empty.jsonl"
        empty.write_text("", encoding="utf-8")
        out_empty = _run_build(empty)
        chk(out_empty is not None and "generated" in out_empty.lower(),
            "log rỗng -> vẫn sinh banner GENERATED (không crash)")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    a13_lock_tests()
    a12_edit_safety_tests()
    a17_mastery_tests()
    print(f"\n== TỔNG test_council_sprint5: PASS={PASS} FAIL={FAIL} ==")
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
