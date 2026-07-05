#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""guard_write — PreToolUse hook (Write|Edit|NotebookEdit). Chặn ghi-sai NGAY lúc xảy ra (Hybrid).

FAIL-OPEN tuyệt đối: mọi lỗi → exit 0 (allow) + log; guard KHÔNG BAO GIỜ làm chết session.
Cơ chế deny = JSON hookSpecificOutput.permissionDecision="deny" + reason (feedback để model tự sửa path).
"""
import sys, json
from pathlib import Path

for _s in (sys.stdin, sys.stdout, sys.stderr):   # Windows cmd có thể là cp1252; path/reason có tiếng Việt
    try: _s.reconfigure(encoding="utf-8")
    except Exception: pass

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parent))                                   # hygiene_lib
sys.path.insert(0, str(HERE.parents[2] / "OAC-Knowledge" / "kb_lifecycle" / "tools"))  # kgr_runtime


def _log(msg):
    try:
        import kgr_runtime as RT
        p = RT.scratch("guard_write.log")
        with open(p, "a", encoding="utf-8") as f:
            f.write(msg + "\n")
    except Exception:
        pass


def _allow():
    sys.exit(0)   # không in gì = defer về permission flow bình thường


def _deny(reason):
    # ensure_ascii=True: JSON thuần ASCII (\uXXXX) → bất chấp console encoding; Claude Code decode lại đúng tiếng Việt.
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": reason,
    }}, ensure_ascii=True))
    sys.exit(0)


def _hint_paths():
    """Đường ghi đúng THẬT (qua kgr_runtime) để nhét vào additionalContext; fail-open nếu RT lỗi."""
    try:
        import kgr_runtime as RT
        return str(RT.work_dir("<repo>")), str(RT.scratch("ten.ext"))
    except Exception:
        return (r"C:\Project\_kgr-state\work\<repo>\ (kgr_runtime.work_dir)",
                r"%LOCALAPPDATA%\kgr-oac\runtime\... (kgr_runtime.scratch)")


def _context(target, err):
    """Fail-open KHÔNG im lặng: THÔNG TIN cho model (non-blocking) — KHÔNG set permissionDecision.
    additionalContext là field hợp lệ của PreToolUse hook; bản Claude Code không hỗ trợ sẽ bỏ qua field lạ → an toàn.
    """
    work, scr = _hint_paths()
    msg = (f"[guard_write] Không đánh giá được path {target!r} vì {err}. "
           f"Hãy TỰ kiểm ghi đúng chỗ: scratch/state ra NGOÀI cây project — "
           f"kgr_runtime.work_dir('<repo>') → {work} (giữ lại được) "
           f"hoặc kgr_runtime.scratch('ten.ext') → {scr} (xóa được). "
           f"KHÔNG ghi _work/ / _PNL_* / dump / file GENERATED trong cây (INV-4).")
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "additionalContext": msg,
    }}, ensure_ascii=True))
    sys.exit(0)   # non-blocking: KHÔNG permissionDecision → không auto-allow, chỉ inject context


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        _allow(); return
    ti = data.get("tool_input") or {}
    target = ti.get("file_path") or ti.get("notebook_path") or ti.get("path")
    if not target:
        _allow(); return
    try:
        import hygiene_lib as H
        import kgr_runtime as RT
        ws = RT.workspace_root()
        rules, generated_abs = H.load_context(ws)
        verdict, reason = H.classify(target, ws, rules, generated_abs)
    except Exception as e:
        _log(f"[fail-open] {target!r}: {e!r}")
        _context(target, repr(e)); return   # fail-open KHÔNG im lặng: THÔNG TIN (non-blocking), KHÔNG auto-allow
    if verdict in ("deny_junk", "deny_generated"):
        _deny(reason)
    else:
        _allow()


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception:
        sys.exit(0)   # backstop fail-open
