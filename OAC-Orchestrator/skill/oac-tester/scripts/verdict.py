#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verdict.py — LOGIC TESTABLE của gatekeeper QA `oac-tester`.

KHÔNG gọi OAC. Chỉ 3 việc thuần:
  1. decide_verdict(checks) — quyết verdict từ list check-results theo luật DoD:
       có FAIL          -> FAIL   (ưu tiên cao nhất: có gì sai chắc = trượt)
       có BLOCKED, no FAIL -> BLOCKED (vd golden thiếu kỳ ở cổng #1 → KHÔNG auto-PASS)
       toàn PASS (và có ≥1 check) -> PASS
       rỗng             -> BLOCKED (KHÔNG bao giờ auto-PASS khi chưa chạy cổng nào)
  2. validate_record(rec) — verdict-record đúng schema cứng chưa.
  3. append_verdict(blackboard_id, rec) — ghi record vào blackboard qua
     OAC-Orchestrator/scripts/blackboard.py nếu import được; không thì trả record dict
     cho caller tự ghi (không phụ thuộc cứng vào runtime blackboard).

Schema verdict-record (khớp SKILL.md OUTPUT):
  {
    "verdict": "PASS"|"FAIL"|"BLOCKED",
    "checks": [ {"name","result","evidence","source","expected","actual"}, ... ],
    "blocking": [ ... ],           # danh sách cổng chặn (FAIL/BLOCKED) cho builder rework
    "deep_link": "<url mở artifact>",
    "verifier_run_ts": "<ISO ts>"
  }
"""
import sys, os, time, json

VERDICTS = ("PASS", "FAIL", "BLOCKED")
CHECK_RESULTS = ("PASS", "FAIL", "BLOCKED")
# Field bắt buộc trên mỗi check (evidence để không có "PASS trần không bằng chứng")
CHECK_REQUIRED = ("name", "result", "evidence")


def _result_of(check):
    """Lấy kết quả 1 check dưới dạng string upper; chấp nhận dict{'result'} hoặc string."""
    if isinstance(check, str):
        return check.strip().upper()
    if isinstance(check, dict):
        return str(check.get("result", "")).strip().upper()
    return ""


def decide_verdict(checks):
    """Quyết verdict tổng từ list check-results.

    Luật (thứ tự ưu tiên): FAIL > BLOCKED > PASS.
    - Bất kỳ check FAIL  -> "FAIL".
    - Không FAIL nhưng có BLOCKED -> "BLOCKED" (golden thiếu kỳ, chưa đủ evidence…).
    - Toàn PASS và có ≥1 check    -> "PASS".
    - Rỗng / không check nào PASS hợp lệ -> "BLOCKED" (KHÔNG auto-PASS).
    """
    if not checks:
        return "BLOCKED"
    results = [_result_of(c) for c in checks]
    if any(r == "FAIL" for r in results):
        return "FAIL"
    if any(r == "BLOCKED" for r in results):
        return "BLOCKED"
    if all(r == "PASS" for r in results):
        return "PASS"
    # có giá trị lạ (không thuộc enum) -> an toàn: BLOCKED, không PASS ngầm
    return "BLOCKED"


# alias để caller/test linh hoạt
compute_verdict = decide_verdict
verdict_from_checks = decide_verdict


def validate_record(rec):
    """Kiểm verdict-record đúng schema. Trả (ok: bool, errors: list[str])."""
    errors = []
    if not isinstance(rec, dict):
        return False, ["record không phải dict"]

    v = rec.get("verdict")
    if v not in VERDICTS:
        errors.append(f"verdict '{v}' không thuộc enum {VERDICTS}")

    checks = rec.get("checks")
    if not isinstance(checks, list) or not checks:
        errors.append("checks phải là list không rỗng")
    else:
        for i, c in enumerate(checks):
            if not isinstance(c, dict):
                errors.append(f"checks[{i}] không phải dict")
                continue
            for f in CHECK_REQUIRED:
                if not c.get(f):
                    errors.append(f"checks[{i}] thiếu field '{f}'")
            r = str(c.get("result", "")).strip().upper()
            if r and r not in CHECK_RESULTS:
                errors.append(f"checks[{i}].result '{r}' không thuộc {CHECK_RESULTS}")

    if not rec.get("deep_link"):
        errors.append("thiếu deep_link")
    if not rec.get("verifier_run_ts"):
        errors.append("thiếu verifier_run_ts")

    # nhất quán: verdict tổng phải khớp luật decide_verdict trên chính checks
    if isinstance(checks, list) and checks and v in VERDICTS:
        derived = decide_verdict(checks)
        if derived != v:
            errors.append(f"verdict '{v}' không khớp checks (luật cho ra '{derived}')")

    return (not errors), errors


# alias
validate_verdict_record = validate_record
is_valid_record = validate_record
validate = validate_record


def _now():
    return time.strftime("%Y-%m-%dT%H:%M:%S")


def build_record(checks, deep_link, blocking=None, verifier_run_ts=None):
    """Dựng verdict-record hoàn chỉnh từ checks (verdict tự suy)."""
    verdict = decide_verdict(checks)
    if blocking is None:
        blocking = [c.get("name") if isinstance(c, dict) else str(c)
                    for c in checks if _result_of(c) in ("FAIL", "BLOCKED")]
    return {
        "verdict": verdict,
        "checks": list(checks),
        "blocking": blocking,
        "deep_link": deep_link,
        "verifier_run_ts": verifier_run_ts or _now(),
    }


def _import_blackboard():
    """Thử import blackboard.py của OAC-Orchestrator. Trả module hoặc None."""
    # OAC-Orchestrator/skill/oac-tester/scripts/verdict.py -> OAC-Orchestrator/scripts/blackboard.py
    # 4× dirname: scripts -> oac-tester -> skill -> OAC-Orchestrator
    here = os.path.abspath(__file__)
    orch = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(here))))  # OAC-Orchestrator/
    bb_dir = os.path.join(orch, "scripts")
    if bb_dir not in sys.path:
        sys.path.insert(0, bb_dir)
    try:
        import blackboard  # type: ignore
        return blackboard
    except Exception:
        return None


def append_verdict(blackboard_id, record):
    """Ghi verdict-record vào blackboard qua blackboard.py nếu import được.

    Trả dict báo cáo: {"written": bool, "blackboard_id", "field", "record"}.
    Nếu KHÔNG import được blackboard -> written=False + trả record để caller tự ghi.
    Record được validate trước; record sai schema -> raise ValueError (không ghi rác).
    """
    ok, errors = validate_record(record)
    if not ok:
        raise ValueError("verdict-record không hợp lệ: " + "; ".join(errors))

    bb = _import_blackboard()
    if bb is None or not blackboard_id:
        return {"written": False, "blackboard_id": blackboard_id,
                "field": "qa_verdicts", "record": record,
                "note": "blackboard không import được / thiếu id — caller tự ghi record"}
    try:
        # append vào list qa_verdicts của blackboard (không đè record cũ)
        cur = bb._read(blackboard_id)
        lst = cur.setdefault("qa_verdicts", [])
        lst.append(record)
        bb._log(cur, "oac-tester", "verdict " + record["verdict"], record.get("deep_link", ""))
        bb._write(blackboard_id, cur)
        return {"written": True, "blackboard_id": blackboard_id,
                "field": "qa_verdicts", "record": record}
    except Exception as e:
        return {"written": False, "blackboard_id": blackboard_id,
                "field": "qa_verdicts", "record": record, "error": repr(e)}


# alias
write_verdict = append_verdict
record_verdict = append_verdict
append_record = append_verdict


if __name__ == "__main__":
    # smoke: đọc list checks JSON từ stdin, in verdict + record
    raw = sys.stdin.read().strip()
    checks = json.loads(raw) if raw else []
    rec = build_record(checks, deep_link="<deep_link>")
    print(json.dumps(rec, ensure_ascii=False, indent=2))
