#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TDD — ACCEPTANCE cho Council-v3 Sprint 1 (A2/A4/A6/A7/A8/A9/A11).
Kiểm docs/config đã sửa đúng chưa. BAN ĐẦU FAIL (chưa implement) = đúng tinh thần TDD.
Chạy: PYTHONUTF8=1 python kb_lifecycle/tests/test_council_sprint1.py
Convention: chk(cond,label) + exit 1 nếu có FAIL (giống test_hooks.py / test_gc.py).
A9 là kiểm MỀM (chỉ WARN, không fail) vì có thể bị blocker mạng."""
import sys, json, re
from pathlib import Path

HERE = Path(__file__).resolve()
WS = HERE.parents[3]  # <ws>/OAC-Knowledge/kb_lifecycle/tests -> <ws>

PASS = FAIL = WARN = 0
def chk(c, l):
    global PASS, FAIL
    if c: PASS += 1; print(f"  PASS  {l}")
    else: FAIL += 1; print(f"  FAIL  {l}")
def warn(c, l):
    global WARN
    if not c:
        WARN += 1; print(f"  WARN  {l}")
    else:
        print(f"  ok    {l}")

# ---- Đường dẫn target (đọc thật, không đoán) ----
DASH_MASTERY   = WS / "Dashboard-builder" / "OAC_DASHBOARD_MASTERY.md"
DASH_CHANGELOG = WS / "Dashboard-builder" / "OAC_DASHBOARD_MASTERY.CHANGELOG.md"
DF_MASTERY     = WS / "Dataflow-builder" / "OAC_DATAFLOW_MASTERY.md"
DF_CHANGELOG   = WS / "Dataflow-builder" / "OAC_DATAFLOW_MASTERY.CHANGELOG.md"
MCP_ROOT  = WS / ".mcp.json"
MCP_DASH  = WS / "Dashboard-builder" / ".mcp.json"
MCP_DF    = WS / "Dataflow-builder" / ".mcp.json"
SETTINGS  = WS / ".claude" / "settings.json"
CONTRACTS = WS / "OAC-Orchestrator" / "agent_contracts.yaml"
CONCURR   = WS / "OAC-Orchestrator" / "concurrency_model.md"
CLAUDEMD  = WS / "CLAUDE.md"

def rd(p):
    return p.read_text(encoding="utf-8") if p.exists() else ""

def section(text, start_pat, level="## "):
    """Trả slice từ heading khớp start_pat tới heading kế cùng cấp (hoặc EOF)."""
    lines = text.splitlines()
    out, capturing = [], False
    for ln in lines:
        if re.match(start_pat, ln):
            capturing = True; out.append(ln); continue
        if capturing and ln.startswith(level):
            break
        if capturing:
            out.append(ln)
    return "\n".join(out)

def sec1(text):
    """§1 = từ '## 1.' tới '## ' kế tiếp."""
    return section(text, r"^## 1[\.\s]", level="## ")

def count_changelog_lines(text):
    """Đếm dòng bullet dạng '- 2026-...' LIÊN TIẾP dài nhất (streak) — dấu hiệu khối changelog inline."""
    best = cur = 0
    for ln in text.splitlines():
        if re.match(r"^\s*-\s*⚠?\s*2026-\d", ln) or re.match(r"^\s*-\s*2026-\d", ln):
            cur += 1; best = max(best, cur)
        else:
            # dòng con thụt vào (tiếp nối 1 entry) không phá streak
            if re.match(r"^\s{2,}", ln) and cur > 0:
                continue
            cur = 0
    return best

def main():
    global PASS, FAIL, WARN

    # =========================================================
    print("== A4: tách CHANGELOG khỏi 2 MASTERY ==")
    for name, mastery, clog in [
        ("Dashboard", DASH_MASTERY, DASH_CHANGELOG),
        ("Dataflow",  DF_MASTERY,   DF_CHANGELOG),
    ]:
        chk(clog.exists(), f"A4 [{name}] file .CHANGELOG.md TỒN TẠI: {clog.name}")
        chk(len(rd(clog).strip()) > 200, f"A4 [{name}] .CHANGELOG.md non-empty (>200 char)")
        # .CHANGELOG.md phải chứa các entry lịch sử thật (dòng '- 2026-')
        chk(rd(clog).count("2026-") >= 3, f"A4 [{name}] .CHANGELOG.md giữ ≥3 mốc '2026-' (không mất chữ)")
        mtext = rd(mastery)
        # MASTERY KHÔNG còn khối changelog inline dày (>=3 dòng '- 2026-' liên tiếp)
        streak = count_changelog_lines(mtext)
        chk(streak < 3, f"A4 [{name}] MASTERY không còn khối ≥3 dòng '- 2026-' liên tiếp (streak={streak})")
        # CÓ dòng trỏ tới .CHANGELOG.md
        chk(clog.name in mtext, f"A4 [{name}] MASTERY có dòng trỏ tới {clog.name}")

    # =========================================================
    print("== A2: nhận-thức Chrome SingletonLock trong §1 mỗi MASTERY ==")
    for name, mastery in [("Dashboard", DASH_MASTERY), ("Dataflow", DF_MASTERY)]:
        s1 = sec1(rd(mastery))
        chk("SingletonLock" in s1, f"A2 [{name}] §1 chứa 'SingletonLock'")
        chk(("KHÔNG kill" in s1) or ("không cần kill" in s1) or ("KHÔNG cần kill" in s1),
            f"A2 [{name}] §1 chứa 'KHÔNG kill'/'không cần kill'")
        chk(("--isolated" in s1) or ("profile khác" in s1) or ("một profile khác" in s1),
            f"A2 [{name}] §1 nói mở profile khác / --isolated là hợp lệ")

    # =========================================================
    print("== A6: screenshot flags trong 3 .mcp.json + ưu tiên take_snapshot ==")
    for name, mcp in [("root", MCP_ROOT), ("dashboard", MCP_DASH), ("dataflow", MCP_DF)]:
        raw = rd(mcp)
        try:
            obj = json.loads(raw); parsed = True
        except Exception as e:
            parsed = False; print(f"    (json error {mcp}: {e})")
        chk(parsed, f"A6 [{name}] .mcp.json parse JSON OK")
        # tìm server chrome-* và kiểm 2 flag nằm trong args của nó
        found_fmt = found_w = False
        if parsed:
            for sv, cfg in obj.get("mcpServers", {}).items():
                if sv.startswith("chrome"):
                    args = cfg.get("args", [])
                    if "--screenshotFormat=webp" in args: found_fmt = True
                    if "--screenshotMaxWidth=1400" in args: found_w = True
        chk(found_fmt, f"A6 [{name}] server chrome-* có '--screenshotFormat=webp'")
        chk(found_w,   f"A6 [{name}] server chrome-* có '--screenshotMaxWidth=1400'")

    for name, mastery in [("Dashboard", DASH_MASTERY), ("Dataflow", DF_MASTERY)]:
        s1 = sec1(rd(mastery))
        chk("take_snapshot" in s1, f"A6 [{name}] §1 có quy tắc ưu tiên 'take_snapshot'")

    # =========================================================
    print("== A8: chặn đọc Login Data + cookie-first (Dashboard) ==")
    sraw = rd(SETTINGS)
    try:
        sobj = json.loads(sraw); sparsed = True
    except Exception as e:
        sparsed = False; print(f"    (settings json error: {e})")
    chk(sparsed, "A8 settings.json parse JSON OK")
    deny = []
    if sparsed:
        deny = sobj.get("permissions", {}).get("deny", [])
    chk(any("Login Data" in d for d in deny), "A8 permissions.deny có rule chặn 'Login Data'")
    chk(any(d.strip() == "Read(**/Login Data)" for d in deny),
        "A8 deny chứa đúng 'Read(**/Login Data)'")
    chk(any("Login Data/**" in d for d in deny),
        "A8 deny chứa rule 'Read(**/Login Data/**)'")
    # MASTERY Dashboard: cookie-first + login 1 lần
    dm = rd(DASH_MASTERY)
    chk(("cookie-first" in dm) or ("cookie" in dm), "A8 [Dashboard] MASTERY nhắc 'cookie'/'cookie-first'")
    chk(("login 1 lần" in dm) or ("bấm login" in dm) or ("bấm đăng nhập" in dm),
        "A8 [Dashboard] MASTERY nói 'login 1 lần'/'bấm login'")

    # =========================================================
    print("== A7: sửa drift chrome-lineage 'chưa tạo/đề xuất' → 'ĐÃ tạo ./.mcp.json' ==")
    ctext = rd(CONTRACTS)
    cctext = rd(CONCURR)
    # Không còn nói chrome-lineage 'chưa tạo'/'đề xuất' (case-insensitive cho chắc)
    def no_stale(txt, label):
        low = txt.lower()
        stale = ("chưa tạo" in low) or ("đề xuất — chưa tạo" in low)
        chk(not stale, f"A7 [{label}] không còn cụm 'chưa tạo' cho chrome-lineage")
    no_stale(ctext, "agent_contracts.yaml")
    # concurrency_model dùng 'TẠO MỚI' ở bảng → phải đổi thành ĐÃ tạo
    low_cc = cctext.lower()
    chk(("./.mcp.json" in ctext) or ("đã tạo" in ctext.lower()),
        "A7 [agent_contracts.yaml] có './.mcp.json' hoặc 'ĐÃ tạo'")
    chk(("./.mcp.json" in cctext) or ("đã tạo" in low_cc),
        "A7 [concurrency_model.md] có './.mcp.json' hoặc 'ĐÃ tạo'")
    chk("tạo mới" not in low_cc, "A7 [concurrency_model.md] không còn 'TẠO MỚI' cho chrome-lineage")

    # =========================================================
    print("== A11: routing section trong CLAUDE.md gốc ==")
    cmd = rd(CLAUDEMD)
    chk("orchestrator" in cmd, "A11 CLAUDE.md chứa 'orchestrator'")
    chk("KHÔNG tự thực thi" in cmd, "A11 CLAUDE.md chứa 'KHÔNG tự thực thi' (routing)")
    chk(("## 0" in cmd) or ("Định tuyến" in cmd) or ("Routing" in cmd) or ("routing" in cmd),
        "A11 CLAUDE.md có mục §0/Định tuyến/routing")

    # =========================================================
    print("== A9 (MỀM — chỉ WARN, không fail vì có thể blocker mạng) ==")
    for name, mcp in [("root", MCP_ROOT), ("dashboard", MCP_DASH), ("dataflow", MCP_DF)]:
        raw = rd(mcp)
        warn("chrome-devtools-mcp@latest" not in raw,
             f"A9 [{name}] đã pin version (không còn '@latest')")

    print(f"\n== TỔNG: PASS={PASS} FAIL={FAIL} WARN={WARN} ==")
    return 1 if FAIL else 0

if __name__ == "__main__":
    sys.exit(main())
