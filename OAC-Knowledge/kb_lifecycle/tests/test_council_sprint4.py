#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TDD acceptance — Council Sprint 4.

A10: skill `oac-tester` (gatekeeper QA, agent thứ-5, sub-skill của orchestrator)
  - OAC-Orchestrator/skill/oac-tester/SKILL.md TỒN TẠI, frontmatter name "oac-tester",
    description có TRIGGER (gatekeeper/verify/gác cổng).
  - Nội dung nêu đủ 7 CỔNG DoD (SỐ-KHỚP/golden, FAN-OUT, SCOPE, BRANDING, PERSIST,
    LINEAGE, DISCLOSURE), input schema (artifact_ref/task_type/period, "KHÔNG nhận" số),
    output schema (verdict PASS|FAIL|BLOCKED), vị trí workflow, giới-hạn "gate thủng".
  - scripts/verdict.py: hàm quyết verdict (all-pass→PASS; 1-fail→FAIL; blocked-no-fail→BLOCKED;
    golden-thiếu-kỳ→BLOCKED) + validate verdict-record (schema).
  - references/DoD_GATES.md tồn tại.

A11-gate: 2 builder SKILL.md + orchestrator SKILL.md có "verdict-record"/"verdict-record-id"
    (Phase done yêu cầu trích verdict-record-id PASS do oac-tester ghi).

Chạy: PYTHONUTF8=1 python kb_lifecycle/tests/test_council_sprint4.py
"""
import sys, os, importlib.util
from pathlib import Path

HERE = Path(__file__).resolve()
WS = HERE.parents[3]                                   # <ws>/OAC-Knowledge/kb_lifecycle/tests -> <ws>
TESTER = WS / "OAC-Orchestrator" / "skill" / "oac-tester"
SKILL = TESTER / "SKILL.md"
VERDICT = TESTER / "scripts" / "verdict.py"
DOD = TESTER / "references" / "DoD_GATES.md"
DASH_SKILL = WS / "Dashboard-builder" / ".claude" / "skills" / "oac-dashboard-builder" / "SKILL.md"
FLOW_SKILL = WS / "Dataflow-builder" / ".claude" / "skills" / "oac-dataflow-builder" / "SKILL.md"
ORCH_SKILL = WS / "OAC-Orchestrator" / "skill" / "kgr-oac-orchestrator" / "SKILL.md"

PASS = FAIL = 0
def chk(c, l):
    global PASS, FAIL
    if c: PASS += 1; print(f"  PASS  {l}")
    else: FAIL += 1; print(f"  FAIL  {l}")


def _read(p):
    try:
        return p.read_text(encoding="utf-8")
    except Exception:
        return ""


# ─────────────────────────── A10 · cấu trúc skill oac-tester ───────────────────────────
def a10_structure_tests():
    print("\n== A10: cấu trúc skill oac-tester ==")
    chk(SKILL.is_file(), f"SKILL.md tồn tại: {SKILL}")
    txt = _read(SKILL)
    low = txt.lower()

    # frontmatter name
    chk(txt.lstrip().startswith("---"), "SKILL.md mở đầu bằng frontmatter '---'")
    chk("name: oac-tester" in low, "frontmatter name: oac-tester")

    # description có trigger từ khóa
    # lấy khối description (đến '---' đóng frontmatter thứ 2)
    fm = txt.split("---")
    desc_blob = (fm[1] if len(fm) > 2 else txt).lower()
    chk("description:" in desc_blob, "frontmatter có field description")
    chk("gatekeeper" in low, "description/nội dung có 'gatekeeper'")
    chk("verify" in low, "có trigger 'verify'")
    chk("gác cổng" in low, "có trigger 'gác cổng'")

    # 7 cổng DoD — grep 7 keyword
    gates = {
        "SỐ-KHỚP/golden": ("số-khớp" in low) or ("golden" in low),
        "FAN-OUT": "fan-out" in low,
        "SCOPE": "scope" in low,
        "BRANDING": "branding" in low,
        "PERSIST": "persist" in low,
        "LINEAGE": "lineage" in low,
        "DISCLOSURE": "disclosure" in low,
    }
    for name, ok in gates.items():
        chk(ok, f"7-cổng DoD nêu cổng: {name}")
    chk("7 cổng" in low or "7 cong" in low or "7 gate" in low, "nêu rõ '7 cổng' DoD")

    # input schema
    chk("artifact_ref" in low, "input schema có artifact_ref")
    chk("task_type" in low, "input schema có task_type")
    chk("period" in low, "input schema có period")
    chk("blackboard_id" in low, "input schema có blackboard_id")
    chk(("không nhận" in low) and ("số" in low),
        "input: nêu 'KHÔNG nhận' trường số từ builder (độc-lập)")

    # output schema — verdict enum
    chk("verdict" in low, "output schema có verdict")
    chk(("pass" in low) and ("fail" in low) and ("blocked" in low),
        "output verdict enum PASS|FAIL|BLOCKED")
    chk("deep_link" in low, "output schema có deep_link")
    chk("verifier_run_ts" in low, "output schema có verifier_run_ts")

    # vị trí workflow + giới hạn gate thủng
    chk(("tester" in low) and ("builder" in low) and ("orchestrator" in low),
        "vị trí workflow: orchestrator → builder → tester")
    chk("gate thủng" in low or "thủng" in low,
        "giới-hạn thành thật: 'gate thủng' nếu builder tự-nuốt-verdict")

    # BLOCKED khi golden thiếu kỳ; read-only
    chk("blocked" in low and ("golden" in low), "cổng #1: golden thiếu kỳ -> BLOCKED (không auto-PASS)")
    chk("read-only" in low or "read only" in low or "chỉ đọc" in low,
        "VAI: read-only reviewer (không browser-write)")

    # references + oac-native
    chk("oac-native" in low, "nêu dùng oac-native để cross-check")
    chk("kgr-oac-lineage" in low, "nêu dùng kgr-oac-lineage cho cổng LINEAGE")

    chk(DOD.is_file(), f"references/DoD_GATES.md tồn tại: {DOD}")
    dod = _read(DOD).lower()
    if dod:
        for name, key in [("SỐ-KHỚP", "golden"), ("FAN-OUT", "fan-out"),
                          ("PERSIST", "persist"), ("LINEAGE", "lineage")]:
            chk(key in dod, f"DoD_GATES.md có recipe cổng {name}")


# ─────────────────────────── A10 · verdict.py logic ───────────────────────────
def _load_verdict():
    if not VERDICT.is_file():
        return None
    spec = importlib.util.spec_from_file_location("verdict_s4", str(VERDICT))
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
        return mod
    except Exception as e:
        chk(False, f"import verdict.py raise {e!r}")
        return None


def a10_verdict_tests():
    print("\n== A10: verdict.py logic ==")
    chk(VERDICT.is_file(), f"verdict.py tồn tại: {VERDICT}")
    v = _load_verdict()
    if v is None:
        return

    # tìm hàm quyết verdict (chấp nhận vài tên hợp lý)
    decide = None
    for nm in ("decide_verdict", "compute_verdict", "resolve_verdict", "verdict_from_checks"):
        if hasattr(v, nm):
            decide = getattr(v, nm); break
    chk(decide is not None, "verdict.py có hàm quyết verdict (decide_verdict/…)")

    if decide is not None:
        c = lambda name, result, **kw: {"name": name, "result": result, **kw}

        # all-pass -> PASS
        all_pass = [c("g1", "PASS"), c("g2", "PASS"), c("g5", "PASS")]
        chk(decide(all_pass) == "PASS", "all-pass -> PASS")

        # 1 fail -> FAIL (kể cả có blocked)
        one_fail = [c("g1", "PASS"), c("g2", "FAIL"), c("g3", "BLOCKED")]
        chk(decide(one_fail) == "FAIL", "có FAIL -> FAIL (ưu tiên FAIL hơn BLOCKED)")

        # blocked-no-fail -> BLOCKED
        blk = [c("g1", "PASS"), c("g2", "BLOCKED")]
        chk(decide(blk) == "BLOCKED", "BLOCKED + không FAIL -> BLOCKED")

        # golden thiếu kỳ -> BLOCKED (không PASS)
        golden_missing = [c("g1", "BLOCKED", evidence="golden thiếu kỳ 42"),
                          c("g2", "PASS")]
        chk(decide(golden_missing) == "BLOCKED",
            "golden thiếu kỳ (cổng #1 BLOCKED) -> BLOCKED, KHÔNG auto-PASS")

        # rỗng -> KHÔNG được PASS ngầm (an toàn: BLOCKED hoặc FAIL, không PASS)
        chk(decide([]) != "PASS", "checks rỗng -> KHÔNG auto-PASS")

    # validate verdict-record
    validate = None
    for nm in ("validate_record", "validate_verdict_record", "is_valid_record", "validate"):
        if hasattr(v, nm):
            validate = getattr(v, nm); break
    chk(validate is not None, "verdict.py có hàm validate verdict-record")

    if validate is not None:
        def _ok(res):
            # cho phép trả bool hoặc (bool, errors)
            return res[0] if isinstance(res, tuple) else bool(res)

        good = {
            "verdict": "PASS",
            "checks": [{"name": "g1", "result": "PASS", "evidence": "live=golden"}],
            "blocking": [],
            "deep_link": "https://oac/…/wb",
            "verifier_run_ts": "2026-07-06T10:00:00",
        }
        chk(_ok(validate(good)), "record hợp lệ -> valid")

        bad_enum = dict(good); bad_enum["verdict"] = "MAYBE"
        chk(not _ok(validate(bad_enum)), "verdict sai enum -> invalid")

        no_deeplink = {k: v2 for k, v2 in good.items() if k != "deep_link"}
        chk(not _ok(validate(no_deeplink)), "thiếu deep_link -> invalid")

        no_ts = {k: v2 for k, v2 in good.items() if k != "verifier_run_ts"}
        chk(not _ok(validate(no_ts)), "thiếu verifier_run_ts -> invalid")

        bad_check = dict(good)
        bad_check["checks"] = [{"name": "g1"}]   # thiếu result/evidence
        chk(not _ok(validate(bad_check)), "check thiếu result/evidence -> invalid")

    # hàm append record (import blackboard nếu được; nếu không -> trả dict)
    appender = None
    for nm in ("append_verdict", "write_verdict", "record_verdict", "append_record"):
        if hasattr(v, nm):
            appender = getattr(v, nm); break
    chk(appender is not None, "verdict.py có hàm append verdict-record (blackboard/fallback dict)")


# ─────────────────────────── A11 · artifact-gate ───────────────────────────
def a11_gate_tests():
    print("\n== A11: artifact-gate (builder + orchestrator yêu cầu verdict-record) ==")
    for label, p in [("dashboard-builder", DASH_SKILL),
                     ("dataflow-builder", FLOW_SKILL),
                     ("orchestrator", ORCH_SKILL)]:
        t = _read(p).lower()
        chk("verdict-record" in t,
            f"{label} SKILL.md nhắc 'verdict-record' (gate qua oac-tester)")
    # builder phải yêu cầu verdict-record-id (id cụ thể) ở phase done
    for label, p in [("dashboard-builder", DASH_SKILL), ("dataflow-builder", FLOW_SKILL)]:
        t = _read(p).lower()
        chk("verdict-record-id" in t,
            f"{label} phase-done yêu cầu trích 'verdict-record-id' (PASS)")


def main():
    a10_structure_tests()
    a10_verdict_tests()
    a11_gate_tests()
    print(f"\n== TỔNG test_council_sprint4: PASS={PASS} FAIL={FAIL} ==")
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
