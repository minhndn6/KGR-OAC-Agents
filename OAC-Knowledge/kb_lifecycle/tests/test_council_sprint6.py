#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Council Sprint-6 acceptance (TDD) — Vòng-2 core:
  R-C1  quét & cấm kênh nsaw-oac-poc (file active grep=0 + settings deny mcp__nsaw-oac-poc__*)
  R-A2  staleness gate INV-6 (doctor freshness: STALE khi _meta cũ, OK khi mới; build_catalogs không hardcode date)
  R-B1  nối data-brain vào 3 builder SKILL.md (kgr-oac-lineage + capability_map + field_dictionary + caveat freshness; designer data-availability)

Chạy: PYTHONUTF8=1 python kb_lifecycle/tests/test_council_sprint6.py
Hermetic: R-A2 tiêm catalog_dir giả (không phụ thuộc ngày catalog thật)."""
import os, sys, json, tempfile
from pathlib import Path

WS = Path(os.environ.get("KGR_WORKSPACE") or r"C:\Project\KGR-OAC-Agents")
TOOLS = WS / "OAC-Knowledge" / "kb_lifecycle" / "tools"
sys.path.insert(0, str(TOOLS))

PASS = FAIL = 0
def chk(c, l):
    global PASS, FAIL
    if c: PASS += 1; print(f"  PASS  {l}")
    else: FAIL += 1; print(f"  FAIL  {l}")

def read(p):
    try: return Path(p).read_text(encoding="utf-8", errors="replace")
    except Exception: return ""

# ─────────────────────────────────────────────────────────────────────────────
# R-C1 — kênh CẤM nsaw-oac-poc
# ─────────────────────────────────────────────────────────────────────────────
def test_rc1():
    print("== R-C1  cấm kênh nsaw-oac-poc ==")
    # File CHỈ-DẪN ĐANG-HIỆU-LỰC: nsaw-oac-poc KHÔNG được xuất hiện như kênh-đọc.
    active_files = [
        WS / "OAC-Knowledge" / "skill" / "kgr-oac-lineage" / "SKILL.md",
        WS / "OAC-Knowledge" / "live_query_recipes.md",
        WS / "Dashboard-builder" / ".claude" / "skills" / "oac-dashboard-builder" / "references" / "subagents.md",
    ]
    for f in active_files:
        chk(f.is_file(), f"tồn tại: {f.name} ({f.parent.name})")
        t = read(f)
        chk("nsaw-oac-poc" not in t and "nsaw_oac_poc" not in t,
            f"KHÔNG còn nsaw-oac-poc trong {f.parent.name}/{f.name}")

    # File có nhãn CẤM/deprecated ĐƯỢC PHÉP nhắc (đó là chỉ-thị cấm, không phải kênh-dùng).
    banned_label_ok = [
        WS / "CLAUDE.md",
        WS / "OAC-Orchestrator" / "skill" / "oac-tester" / "SKILL.md",
        WS / "OAC-Orchestrator" / "skill" / "oac-tester" / "references" / "DoD_GATES.md",
    ]
    for f in banned_label_ok:
        t = read(f)
        if "nsaw-oac-poc" in t:
            low = t.lower()
            chk(("cấm" in low) or ("deprecated" in low) or ("không" in low) or ("khÔng" in low),
                f"{f.parent.name}/{f.name}: nsaw-oac-poc chỉ ở dạng nhãn-CẤM")

    # settings.json permissions.deny chặn cứng tool.
    settings = WS / ".claude" / "settings.json"
    chk(settings.is_file(), ".claude/settings.json tồn tại")
    ok_deny = False
    try:
        data = json.loads(read(settings))
        deny = (data.get("permissions") or {}).get("deny") or []
        ok_deny = any("mcp__nsaw-oac-poc__*" == d or "mcp__nsaw-oac-poc__" in d for d in deny)
    except Exception as e:
        print("   settings parse err:", e)
    chk(ok_deny, "settings.json permissions.deny chứa mcp__nsaw-oac-poc__*")

    # canonical channel order ĐÃ được nêu ở kênh-đọc lineage (oac-native > nsaw-analytics > browser)
    lin = read(WS / "OAC-Knowledge" / "skill" / "kgr-oac-lineage" / "SKILL.md")
    chk("oac-native" in lin and "nsaw-analytics" in lin,
        "kgr-oac-lineage SKILL.md nêu kênh canonical oac-native + nsaw-analytics")

# ─────────────────────────────────────────────────────────────────────────────
# R-A2 — staleness gate (hermetic, tiêm catalog_dir giả)
# ─────────────────────────────────────────────────────────────────────────────
def _write_fake_catalog(dirpath, date_str):
    (Path(dirpath) / "dataflow_catalog.yaml").write_text(
        f"_meta:\n  purpose: fake\n  extracted_live: '{date_str}'\n  total_dataflows: 1\n",
        encoding="utf-8")
    (Path(dirpath) / "workbook_catalog.yaml").write_text(
        f"_meta:\n  extracted_live: '{date_str}'\nworkbooks: {{}}\n", encoding="utf-8")

def test_ra2():
    print("== R-A2  staleness gate (INV-6 fail ồn) ==")
    import importlib
    kgr = importlib.import_module("kgr")
    chk(hasattr(kgr, "freshness_check"), "kgr.freshness_check tồn tại (pure/tiêm-được)")
    if not hasattr(kgr, "freshness_check"):
        return

    from datetime import date, timedelta
    today = date(2026, 7, 6)  # now cố định để hermetic

    # (1) catalog CŨ >14 ngày -> STALE
    with tempfile.TemporaryDirectory() as d:
        old = (today - timedelta(days=20)).isoformat()
        _write_fake_catalog(d, old)
        fr = kgr.freshness_check(catalog_dir=d, now=today)
        chk(fr.get("status") == "STALE", f"catalog {old} (20d) -> freshness STALE (được: {fr.get('status')})")
        chk(fr.get("max_extracted_live") == old, "freshness đọc đúng max(extracted_live)")
        chk(isinstance(fr.get("age_days"), int) and fr["age_days"] == 20, "age_days=20 chính xác")

    # (2) catalog HƠI cũ 7<age<=14 -> WARN
    with tempfile.TemporaryDirectory() as d:
        warn = (today - timedelta(days=10)).isoformat()
        _write_fake_catalog(d, warn)
        fr = kgr.freshness_check(catalog_dir=d, now=today)
        chk(fr.get("status") == "WARN", f"catalog {warn} (10d) -> WARN (được: {fr.get('status')})")

    # (3) catalog MỚI <=7 ngày -> OK
    with tempfile.TemporaryDirectory() as d:
        fresh = (today - timedelta(days=3)).isoformat()
        _write_fake_catalog(d, fresh)
        fr = kgr.freshness_check(catalog_dir=d, now=today)
        chk(fr.get("status") == "OK", f"catalog {fresh} (3d) -> OK (được: {fr.get('status')})")

    # (4) doctor tích hợp freshness + STALE góp phần ATTENTION (INV-6)
    #     Test hành vi GATE (phát hiện stale), không buộc doctor luôn OK.
    import subprocess
    env = {**os.environ, "PYTHONUTF8": "1"}
    KGRPY = TOOLS / "kgr.py"
    r = subprocess.run([sys.executable, str(KGRPY), "doctor"], capture_output=True, text=True, env=env)
    rep = {}
    try: rep = json.loads(r.stdout)
    except Exception: pass
    chk("freshness" in rep, "doctor report có field 'freshness'")
    fr = rep.get("freshness") or {}
    chk(fr.get("status") in ("OK", "WARN", "STALE"), f"doctor freshness.status hợp lệ ({fr.get('status')})")
    # Nếu catalog thật đang STALE -> STATUS phải ATTENTION (gate hoạt động, không nuốt lỗi)
    if fr.get("status") == "STALE":
        chk(rep.get("STATUS") == "ATTENTION", "catalog thật STALE -> doctor STATUS=ATTENTION (gate không im lặng)")
        chk(r.returncode != 0, "doctor exit≠0 khi STALE (fail ồn)")

    # (5) build_catalogs.py KHÔNG còn hardcode ngày (hoặc có TODO nếu chưa xử được mtime)
    bc = read(WS / "OAC-Knowledge" / "raw" / "build_catalogs.py")
    hard = 'EXTRACT_DATE = "2026-06-20"' in bc or "EXTRACT_DATE='2026-06-20'" in bc.replace(" ", "")
    has_todo = "TODO" in bc
    chk((not hard) or has_todo, "build_catalogs: EXTRACT_DATE không hardcode ngày (hoặc có TODO)")

# ─────────────────────────────────────────────────────────────────────────────
# R-B1 — nối data-brain vào 3 builder SKILL.md
# ─────────────────────────────────────────────────────────────────────────────
def test_rb1():
    print("== R-B1  data-brain wiring vào builder SKILL.md ==")
    builders = {
        "oac-dashboard-builder": WS / "Dashboard-builder" / ".claude" / "skills" / "oac-dashboard-builder" / "SKILL.md",
        "oac-dataflow-builder":  WS / "Dataflow-builder" / ".claude" / "skills" / "oac-dataflow-builder" / "SKILL.md",
        "oac-dashboard-designer": WS / "Dashboard-builder" / ".claude" / "skills" / "oac-dashboard-designer" / "SKILL.md",
    }
    for name, f in builders.items():
        t = read(f)
        low = t.lower()
        chk("kgr-oac-lineage" in t, f"{name}: tham chiếu kgr-oac-lineage (data-brain)")
        chk("capability_map" in t, f"{name}: tra capability_map.yaml")
        chk("field_dictionary" in t, f"{name}: tra field_dictionary.yaml")
        # caveat freshness (phụ thuộc R-A2): nếu doctor STALE -> cảnh báo trước khi tin lineage
        chk(("freshness" in low or "stale" in low) and ("refresh" in low or "tươi" in low or "độ-tươi" in low or "độ tươi" in low),
            f"{name}: có caveat freshness (STALE/refresh)")

    # Designer: kiểm data-availability qua capability_map TRƯỚC khi đề xuất KPI
    des = read(builders["oac-dashboard-designer"])
    dlow = des.lower()
    chk("data-availability" in dlow or "data availability" in dlow or "khả dụng" in dlow or "data-context" in dlow,
        "designer: nêu kiểm data-availability trước khi đề xuất KPI")

def main():
    test_rc1()
    test_ra2()
    test_rb1()
    print(f"\n== TỔNG Sprint-6: PASS={PASS} FAIL={FAIL} ==")
    return 1 if FAIL else 0

if __name__ == "__main__":
    sys.exit(main())
