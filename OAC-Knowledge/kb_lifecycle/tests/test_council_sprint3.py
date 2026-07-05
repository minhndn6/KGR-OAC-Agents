#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TDD acceptance — Council Sprint 3.

A3: guard_write.py — nhánh fail-open KHÔNG được im lặng: phải in additionalContext
    (thông tin, non-blocking) NHƯNG tuyệt đối KHÔNG set permissionDecision=allow,
    và KHÔNG làm chết session (exit 0). Deny hợp lệ vẫn ra permissionDecision=deny.
    Allow hợp lệ (source trong cây) vẫn im lặng/allow (exit 0, không permissionDecision).

A7: kgr.mcp_chrome_check(processes=, mcp_files=) — thuần/tiêm-được: đọc các .mcp.json,
    map server -> user-data-dir; so với Chrome process (CommandLine chứa --user-data-dir);
    báo: server có/thiếu process, profile trùng nhau (2 process cùng user-data-dir),
    .mcp.json parse lỗi. Test KHÔNG gọi Chrome thật.

Chạy: PYTHONUTF8=1 python kb_lifecycle/tests/test_council_sprint3.py
"""
import sys, os, json, subprocess, tempfile, shutil
from pathlib import Path

HERE = Path(__file__).resolve()
WS = HERE.parents[3]                                   # <ws>/OAC-Knowledge/kb_lifecycle/tests -> <ws>
GUARD = WS / ".claude" / "hooks" / "guard_write.py"
TOOLS = WS / "OAC-Knowledge" / "kb_lifecycle" / "tools"
sys.path.insert(0, str(TOOLS))                         # kgr, kgr_runtime

PASS = FAIL = 0
def chk(c, l):
    global PASS, FAIL
    if c: PASS += 1; print(f"  PASS  {l}")
    else: FAIL += 1; print(f"  FAIL  {l}")


# ─────────────────────────── A3 · guard_write fail-open ───────────────────────────
def _run_guard(stdin_obj_or_str, extra_env=None):
    """Chạy guard_write.py qua subprocess với stdin JSON; trả (rc, stdout, stderr)."""
    payload = stdin_obj_or_str if isinstance(stdin_obj_or_str, str) else json.dumps(stdin_obj_or_str)
    env = {**os.environ, "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"}
    if extra_env:
        env.update(extra_env)
    r = subprocess.run([sys.executable, str(GUARD)], input=payload,
                       capture_output=True, text=True, env=env, timeout=60)
    return r.returncode, (r.stdout or ""), (r.stderr or "")


def _parse_hook(stdout):
    """Trả dict hookSpecificOutput (hoặc {} nếu không có JSON)."""
    s = stdout.strip()
    if not s:
        return {}
    try:
        return (json.loads(s) or {}).get("hookSpecificOutput", {}) or {}
    except Exception:
        return {}


def a3_tests():
    print("\n== A3: guard_write.py fail-open KHÔNG im lặng ==")
    chk(GUARD.is_file(), f"guard_write.py tồn tại: {GUARD}")

    # (a) DENY-case: path _PNL_* trong cây -> permissionDecision=deny
    junk = str(WS / "_PNL_council_sprint3.md")
    rc, out, err = _run_guard({"tool_name": "Write", "tool_input": {"file_path": junk}})
    hook = _parse_hook(out)
    chk(rc == 0, "(a) deny-case exit 0 (fail-open, không chết session)")
    chk(hook.get("permissionDecision") == "deny", "(a) deny-case -> permissionDecision=deny")
    chk(bool(hook.get("permissionDecisionReason")), "(a) deny-case có reason")

    # (a2) DENY-case: file GENERATED (banner) trong cây
    tmp = Path(tempfile.mkdtemp(prefix="kgr_s3_gen_"))
    try:
        # dùng path THẬT trong cây có banner GENERATED để classify bắt được
        gen = WS / "OAC-Knowledge" / "dataflow_catalog.yaml"
        if gen.is_file():
            rc, out, err = _run_guard({"tool_name": "Edit", "tool_input": {"file_path": str(gen)}})
            hook = _parse_hook(out)
            chk(rc == 0 and hook.get("permissionDecision") == "deny",
                "(a2) file trong generated_manifest -> deny")
        else:
            chk(True, "(a2) skip: dataflow_catalog.yaml không có (không chặn gate)")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # (b) FAIL-OPEN-case: ép H.classify/load_context lỗi qua KGR_WORKSPACE trỏ vào path RÁC
    #     (không phải workspace hợp lệ) -> load_context/classify có thể raise -> nhánh except.
    #     YÊU CẦU: exit 0 + in additionalContext + KHÔNG permissionDecision (nhất là != allow).
    bad_ws = str(Path(tempfile.gettempdir()) / "kgr_no_such_ws_sprint3_zzz")
    target = str(Path(bad_ws) / "OAC-Knowledge" / "x.yaml")
    rc, out, err = _run_guard(
        {"tool_name": "Write", "tool_input": {"file_path": target}},
        extra_env={"KGR_WORKSPACE": bad_ws},
    )
    hook = _parse_hook(out)
    chk(rc == 0, "(b) fail-open exit 0 (guard KHÔNG chết session)")
    # Với bad_ws, load_context có thể vẫn chạy được (dir trống -> rules {} ) => classify=allow im lặng.
    # Điểm cốt lõi: NẾU có in gì thì phải là additionalContext, KHÔNG BAO GIỜ permissionDecision=allow.
    chk(hook.get("permissionDecision") != "allow",
        "(b) fail-open KHÔNG auto-allow (không permissionDecision=allow)")

    # (b2) FAIL-OPEN ÉP CỨNG: patch H.load_context để raise, đảm bảo nhánh except in additionalContext.
    #      Chạy guard trong-process với monkeypatch (không subprocess) để tiêm lỗi xác định.
    _a3_fail_open_inprocess()

    # (c) ALLOW-case: source hợp lệ trong cây -> im lặng/allow (exit 0, không permissionDecision)
    src = str(WS / "OAC-Knowledge" / "kb_lifecycle" / "tools" / "kgr.py")
    rc, out, err = _run_guard({"tool_name": "Edit", "tool_input": {"file_path": src}})
    hook = _parse_hook(out)
    chk(rc == 0, "(c) allow-case exit 0")
    chk("permissionDecision" not in hook, "(c) allow-case im lặng (không permissionDecision)")

    # (d) no-target (tool_input rỗng) -> allow im lặng, exit 0
    rc, out, err = _run_guard({"tool_name": "Write", "tool_input": {}})
    chk(rc == 0 and "permissionDecision" not in _parse_hook(out),
        "(d) không có target -> allow im lặng")

    # (e) stdin không parse được JSON -> allow im lặng, exit 0 (fail-open đầu vào)
    rc, out, err = _run_guard("<<<not json>>>")
    chk(rc == 0 and "permissionDecision" not in _parse_hook(out),
        "(e) stdin rác -> allow im lặng, không chết")


def _a3_fail_open_inprocess():
    """Import guard_write như module, monkeypatch để ÉP nhánh fail-open, kiểm stdout."""
    import io, importlib.util
    spec = importlib.util.spec_from_file_location("guard_write_s3", str(GUARD))
    gw = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(gw)
    except Exception as e:
        chk(False, f"(b2) import guard_write raise {e!r}")
        return

    # Ép hygiene_lib.load_context raise trong nhánh try của main()
    import hygiene_lib as H
    orig = H.load_context
    H.load_context = lambda ws: (_ for _ in ()).throw(RuntimeError("boom-inject"))

    captured = {}
    def fake_allow():
        captured["allow_called"] = True
        raise SystemExit(0)
    def fake_deny(reason):
        captured["deny_reason"] = reason
        raise SystemExit(0)

    old_stdin, old_stdout = sys.stdin, sys.stdout
    old_allow, old_deny = gw._allow, gw._deny
    gw._allow, gw._deny = fake_allow, fake_deny
    buf = io.StringIO()
    try:
        # Chỉ redirect stdout QUANH gw.main() để bắt output của guard;
        # KHÔNG nuốt các print(chk(...)) của test.
        sys.stdin = io.StringIO(json.dumps(
            {"tool_name": "Write", "tool_input": {"file_path": str(WS / "OAC-Knowledge" / "z.yaml")}}))
        sys.stdout = buf
        try:
            gw.main()
        except SystemExit:
            pass
        finally:
            sys.stdout = old_stdout
        out = buf.getvalue().strip()
        hook = {}
        if out:
            try:
                hook = (json.loads(out) or {}).get("hookSpecificOutput", {}) or {}
            except Exception:
                hook = {}
        # YÊU CẦU A3: nhánh fail-open phải in additionalContext, KHÔNG gọi _allow (im lặng)
        chk(not captured.get("allow_called"),
            "(b2) fail-open KHÔNG gọi _allow im lặng (phải THÔNG TIN)")
        chk(hook.get("hookEventName") == "PreToolUse" and bool(hook.get("additionalContext")),
            "(b2) fail-open in hookSpecificOutput.additionalContext")
        chk("permissionDecision" not in hook,
            "(b2) fail-open KHÔNG set permissionDecision (chỉ thông tin, non-blocking)")
        ctx = (hook.get("additionalContext") or "")
        chk(("work_dir" in ctx) or ("scratch" in ctx) or ("_kgr-state" in ctx),
            "(b2) additionalContext gợi ý đường ghi đúng (work_dir/scratch)")
    finally:
        sys.stdin, sys.stdout = old_stdin, old_stdout
        gw._allow, gw._deny = old_allow, old_deny
        H.load_context = orig


# ─────────────────────────── A7 · kgr.mcp_chrome_check ───────────────────────────
def _write_mcp(dirp, name, content):
    p = Path(dirp) / name
    p.write_text(content, encoding="utf-8")
    return p


def a7_tests():
    print("\n== A7: kgr.mcp_chrome_check (tiêm mcp_files + processes) ==")
    import kgr
    chk(hasattr(kgr, "mcp_chrome_check"), "kgr.mcp_chrome_check tồn tại")
    if not hasattr(kgr, "mcp_chrome_check"):
        return

    tmp = Path(tempfile.mkdtemp(prefix="kgr_s3_mcp_"))
    try:
        DIR_L = r"C:\Users\ADMIN\.cache\chrome-devtools-mcp\profile-lineage"
        DIR_D = r"C:\Users\ADMIN\.cache\chrome-devtools-mcp\profile-dashboard"
        DIR_F = r"C:\Users\ADMIN\.cache\chrome-devtools-mcp\profile-dataflow"

        good_root = _write_mcp(tmp, "root.mcp.json", json.dumps({"mcpServers": {
            "chrome-lineage": {"command": "npx", "args": [
                "-y", "chrome-devtools-mcp@1.5.0", f"--user-data-dir={DIR_L}"]}}}))
        good_dash = _write_mcp(tmp, "dash.mcp.json", json.dumps({"mcpServers": {
            "chrome-dashboard": {"command": "npx", "args": [
                "-y", "chrome-devtools-mcp@1.5.0", f"--user-data-dir={DIR_D}"]}}}))
        good_flow = _write_mcp(tmp, "flow.mcp.json", json.dumps({"mcpServers": {
            "chrome-dataflow": {"command": "npx", "args": [
                "-y", "chrome-devtools-mcp@1.5.0", f"--user-data-dir={DIR_F}"]}}}))
        broken = _write_mcp(tmp, "broken.mcp.json", "{ this is : not json ,,,")

        # ── Case 1: lineage & dashboard có process; dataflow KHÔNG; KHÔNG trùng ──
        procs = [
            f'"C:\\...\\chrome.exe" --user-data-dir={DIR_L} --other',
            f'chrome.exe --headless --user-data-dir={DIR_D}',
            'chrome.exe --user-data-dir=C:\\Some\\Unrelated\\profile',   # nhiễu, không map
        ]
        rep = kgr.mcp_chrome_check(processes=procs, mcp_files=[good_root, good_dash, good_flow])
        chk(isinstance(rep, dict), "C1: trả dict")
        servers = rep.get("servers", {})
        chk(servers.get("chrome-lineage", {}).get("running") is True, "C1: lineage running=True")
        chk(servers.get("chrome-dashboard", {}).get("running") is True, "C1: dashboard running=True")
        chk(servers.get("chrome-dataflow", {}).get("running") is False, "C1: dataflow running=False (thiếu process)")
        missing = rep.get("missing_process") or []
        chk("chrome-dataflow" in missing, "C1: dataflow trong missing_process")
        chk(not (rep.get("duplicate_profiles") or []), "C1: không có duplicate_profiles")
        chk(not (rep.get("parse_errors") or []), "C1: không có parse_errors")

        # ── Case 2: TRÙNG profile — 2 process cùng user-data-dir=lineage ──
        procs_dup = [
            f'chrome.exe --user-data-dir={DIR_L} --a',
            f'chrome.exe --user-data-dir={DIR_L} --b',   # trùng!
            f'chrome.exe --user-data-dir={DIR_D}',
        ]
        rep2 = kgr.mcp_chrome_check(processes=procs_dup, mcp_files=[good_root, good_dash, good_flow])
        dups = rep2.get("duplicate_profiles") or []
        # duplicate_profiles có thể là list[str dir] hoặc list[dict] — so khớp không phân biệt hoa/thường,
        # bỏ trailing sep (khớp cách kgr chuẩn hóa user-data-dir).
        needle = DIR_L.replace("/", "\\").rstrip("\\").lower()
        dup_blob = json.dumps(dups).replace("\\\\", "\\").lower()
        chk(bool(dups) and needle in dup_blob,
            "C2: phát hiện duplicate_profiles ở profile-lineage")
        chk(rep2.get("servers", {}).get("chrome-lineage", {}).get("running") is True,
            "C2: lineage vẫn running=True")

        # ── Case 3: .mcp.json PARSE LỖI -> parse_errors, và (nếu nối doctor) lật STATUS ──
        rep3 = kgr.mcp_chrome_check(processes=[], mcp_files=[good_root, broken])
        perr = rep3.get("parse_errors") or []
        chk(bool(perr), "C3: parse_errors không rỗng khi .mcp.json hỏng")
        chk(any(str(broken.name) in str(e) or str(broken) in str(e) for e in perr),
            "C3: parse_errors nêu tên file hỏng")
        chk(rep3.get("servers", {}).get("chrome-lineage") is not None,
            "C3: server file tốt vẫn được map dù có file hỏng")

        # ── Case 4: default mcp_files=None phải đọc 3 file THẬT (không crash) + không cần Chrome ──
        rep4 = kgr.mcp_chrome_check(processes=[])   # processes tiêm rỗng -> không đụng Chrome thật
        chk(isinstance(rep4, dict) and "servers" in rep4,
            "C4: default mcp_files (file thật) đọc được, trả servers")

    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    a3_tests()
    a7_tests()
    print(f"\n== TỔNG test_council_sprint3: PASS={PASS} FAIL={FAIL} ==")
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
