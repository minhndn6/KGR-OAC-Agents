#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""kgr — entrypoint CLI cho workspace KGR-OAC-Agents (D12). Giúp BẤT KỲ AI/người nào
khám phá: ghi scratch ở đâu, ghi tri thức vào đâu, KB có khỏe không.

Usage:
  python kgr.py where      # in các đường ghi (durable NGOÀI cây vs ephemeral)
  python kgr.py doctor      # health-check: KB root, registry, repo sạch
  python kgr.py setup       # ghi registry kb_root + cấu hình git core.hooksPath=.githooks (shared pre-commit)
  python kgr.py gc [--apply]# retention: dọn tmp/_trash/dump cũ + archive blackboard cũ ở _kgr-state
  python kgr.py route ...   # -> kb_route.py (P2.2): "tri thức loại X ghi vào đâu"
  python kgr.py refresh [--check|--discover|--reconcile]  # cơ chế REFRESH đọc-only:
        # --check staleness (R-A2) · --discover oac-native discover_data LIVE · --reconcile live↔dataset_catalog
        # (không cờ) = --check + --reconcile, in drift gọn. KHÔNG ghi OAC, KHÔNG ghi đè catalog.
"""
import sys, os, json, subprocess, hashlib, glob
from pathlib import Path

try: sys.stdout.reconfigure(encoding="utf-8")   # an toàn console cp1252 (Windows)
except Exception: pass

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parent))
import kgr_runtime as RT   # noqa: E402
import kb_paths as KP      # noqa: E402


def _learn_py_repo():
    """Đường dẫn learn.py bản trong-repo (skill/kgr-oac-lineage/scripts/learn.py)."""
    for anc in (HERE, *HERE.parents):
        cand = anc / "skill" / "kgr-oac-lineage" / "scripts" / "learn.py"
        if cand.is_file():
            return cand
    # fallback: từ KB root
    try:
        kb = KP.resolve_kb_root(start_file=str(HERE))
        c = kb / "skill" / "kgr-oac-lineage" / "scripts" / "learn.py"
        if c.is_file():
            return c
    except Exception:
        pass
    return None


def _sha(p):
    try:
        return hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]
    except Exception:
        return None


def _find_installed_learn_py():
    """Tìm bản learn.py ĐÃ CÀI (~/.claude/skills/.../scripts/learn.py) qua HOME + glob."""
    pats = [
        os.path.join(os.path.expanduser("~"), ".claude", "skills", "kgr-oac-lineage", "scripts", "learn.py"),
        os.path.join(os.path.expanduser("~"), ".claude", "skills", "**", "kgr-oac-lineage", "scripts", "learn.py"),
    ]
    for pat in pats:
        for m in glob.glob(pat, recursive=True):
            if os.path.isfile(m):
                return Path(m)
    return None


def learn_governance():
    """INV-6 fail-ồn: learn.py PHẢI là shim forward learn2; nếu bản-cài lệch repo -> cảnh báo.
    Trả dict + cờ 'ok' để doctor quyết STATUS."""
    out = {}
    repo = _learn_py_repo()
    if repo is None:
        out["is_shim"] = False; out["shim"] = "learn_py_not_found"
        out["installed_copy"] = "n/a"; out["ok"] = False
        return out
    src = ""
    try:
        src = repo.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        out["is_shim"] = False; out["shim"] = f"read_error: {e}"
        out["installed_copy"] = "n/a"; out["ok"] = False
        return out
    is_shim = ("learn2" in src) and ("import" in src.lower()) and ("deprecated" in src.lower())
    out["is_shim"] = is_shim
    out["shim"] = "ok" if is_shim else "NOT-SHIM (learn.py không forward learn2 — INV-6 fail ồn)"
    out["repo_learn_py"] = str(repo)
    inst = _find_installed_learn_py()
    # STATUS/ok do IS-SHIM quyết (INV-6: learn.py phải là shim forward learn2, nếu KHÔNG -> ATTENTION).
    # MISMATCH bản-cài = CẢNH BÁO ồn (surfaced 'warning'), KHÔNG tự lật exit-code — sync là việc lúc commit.
    ok = is_shim
    if inst is None:
        out["installed_copy"] = "not-found (chạy từ repo)"
    else:
        rh, ih = _sha(repo), _sha(inst)
        if rh == ih:
            out["installed_copy"] = {"status": "in-sync", "path": str(inst)}
        else:
            out["installed_copy"] = {"status": "MISMATCH", "path": str(inst),
                                     "repo_sha": rh, "installed_sha": ih,
                                     "hint": "đồng bộ bản cài ~/.claude với repo (INV-6) — chạy lúc commit"}
            out["warning"] = "installed learn.py LỆCH repo shim — cần sync ~/.claude (INV-6 fail ồn)"
    out["ok"] = ok
    return out

# ── A7: .mcp.json vs Chrome process (drift đa-instance) ──────────────────────────
import re as _re

_UDD_RE = _re.compile(r"--user-data-dir[=\s]+(\"[^\"]+\"|'[^']+'|\S+)")


def _default_mcp_files():
    """3 .mcp.json THẬT: root + Dashboard-builder + Dataflow-builder."""
    try:
        ws = RT.workspace_root(start=str(HERE))
    except Exception:
        ws = Path(r"C:\Project\KGR-OAC-Agents")
    return [ws / ".mcp.json", ws / "Dashboard-builder" / ".mcp.json", ws / "Dataflow-builder" / ".mcp.json"]


def _extract_udd(cmdline):
    """Lấy --user-data-dir=... từ 1 CommandLine string (bỏ quote). None nếu không có."""
    if not cmdline:
        return None
    m = _UDD_RE.search(str(cmdline))
    if not m:
        return None
    v = m.group(1)
    if len(v) >= 2 and v[0] in "\"'" and v[-1] == v[0]:
        v = v[1:-1]
    return v.rstrip("\\/").strip() or None


def _norm_udd(p):
    """Chuẩn hóa user-data-dir để so trùng (case-insensitive trên Windows, bỏ trailing sep)."""
    if not p:
        return None
    return str(p).replace("/", "\\").rstrip("\\").lower()


def _read_chrome_processes():
    """Danh sách CommandLine của chrome.exe đang chạy (Windows). Fail-open → [] nếu không lấy được."""
    ps = (r"Get-CimInstance Win32_Process -Filter \"name='chrome.exe'\" "
          r"| Select-Object -ExpandProperty CommandLine")
    for cmd in (["powershell", "-NoProfile", "-NonInteractive", "-Command", ps],
                ["wmic", "process", "where", "name='chrome.exe'", "get", "CommandLine"]):
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=25)
            if r.returncode == 0 and r.stdout:
                lines = [ln.strip() for ln in r.stdout.splitlines() if ln.strip()]
                lines = [ln for ln in lines if ln.lower() != "commandline"]
                if lines:
                    return lines
        except Exception:
            continue
    return []


def mcp_chrome_check(processes=None, mcp_files=None):
    """THUẦN/tiêm-được. Đọc các .mcp.json → map server→user-data-dir; so với Chrome process (CommandLine).
    Báo: server nào có/thiếu process, profile nào chạy trùng (2 process cùng user-data-dir = nguy cơ SingletonLock),
    .mcp.json nào parse lỗi. processes/mcp_files tiêm để test hermetic; default = đọc file + process THẬT.
    """
    files = mcp_files if mcp_files is not None else _default_mcp_files()
    procs = processes if processes is not None else _read_chrome_processes()

    servers = {}          # server -> {"user_data_dir", "norm", "source", "running"}
    parse_errors = []
    for f in files:
        f = Path(f)
        if not f.is_file():
            continue
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except Exception as e:
            parse_errors.append(f"{f}: {e}")
            continue
        for name, spec in (data.get("mcpServers") or {}).items():
            udd = None
            for a in (spec.get("args") or []):
                udd = _extract_udd(a)
                if udd:
                    break
            servers[name] = {"user_data_dir": udd, "norm": _norm_udd(udd),
                             "source": str(f), "running": False}

    # user-data-dir đang chạy (từ process) → đếm để bắt trùng
    running_norm = {}     # norm_udd -> count
    proc_udds = []
    for cl in (procs or []):
        u = _extract_udd(cl)
        n = _norm_udd(u)
        proc_udds.append({"user_data_dir": u, "norm": n})
        if n:
            running_norm[n] = running_norm.get(n, 0) + 1

    for name, info in servers.items():
        info["running"] = bool(info["norm"]) and running_norm.get(info["norm"], 0) >= 1

    missing_process = sorted([n for n, i in servers.items() if not i["running"]])
    # trùng profile: bất kỳ user-data-dir nào có ≥2 process (bất kể có trong .mcp.json hay không)
    duplicate_profiles = []
    for n, c in running_norm.items():
        if c >= 2:
            owners = sorted([sn for sn, si in servers.items() if si["norm"] == n])
            duplicate_profiles.append({"user_data_dir": n, "process_count": c, "servers": owners})

    return {
        "servers": servers,
        "missing_process": missing_process,
        "duplicate_profiles": duplicate_profiles,
        "parse_errors": parse_errors,
        "process_count": len(proc_udds),
    }


# ── R-A2: staleness gate (INV-6 fail-ồn) — tuổi catalog so now ───────────────────
import datetime as _dt

_FRESH_WARN_DAYS = 7    # >7 ngày -> WARN
_FRESH_STALE_DAYS = 14  # >14 ngày -> STALE (góp phần STATUS=ATTENTION)
_FRESH_CATALOGS = ("dataflow_catalog.yaml", "workbook_catalog.yaml",
                   "dataset_catalog.yaml", "field_dictionary.yaml")
_EXTRACTED_RE = _re.compile(r"extracted_live\s*:\s*['\"]?(\d{4}-\d{2}-\d{2})")


def _catalog_dir():
    """Thư mục chứa các catalog YAML = KB root."""
    return KP.resolve_kb_root(start_file=str(HERE))


def freshness_check(catalog_dir=None, now=None, files=None):
    """THUẦN/tiêm-được. Đọc max(extracted_live) từ _meta các catalog → tuổi so `now`.
    >14 ngày = STALE, >7 = WARN, else OK (INV-6: map cũ phải FAIL ồn, không im lặng).
    catalog_dir/now/files tiêm để test hermetic; default = KB root + hôm nay + 4 catalog chuẩn.
    """
    cd = Path(catalog_dir) if catalog_dir is not None else None
    if cd is None:
        try:
            cd = _catalog_dir()
        except Exception as e:
            return {"status": "UNKNOWN", "error": f"catalog_dir: {e}", "max_extracted_live": None}
    if now is None:
        now = _dt.date.today()
    names = files if files is not None else _FRESH_CATALOGS

    per_file = {}
    dates = []
    for n in names:
        p = cd / n
        if not p.is_file():
            continue
        try:
            txt = p.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        m = _EXTRACTED_RE.search(txt)
        if not m:
            continue
        ds = m.group(1)
        per_file[n] = ds
        try:
            dates.append(_dt.date.fromisoformat(ds))
        except Exception:
            pass

    if not dates:
        return {"status": "UNKNOWN", "max_extracted_live": None, "per_file": per_file,
                "note": "không đọc được extracted_live từ catalog nào (INV-6: nghi ngờ, cần kiểm)"}

    newest = max(dates)
    age = (now - newest).days
    if age > _FRESH_STALE_DAYS:
        status = "STALE"
    elif age > _FRESH_WARN_DAYS:
        status = "WARN"
    else:
        status = "OK"
    return {
        "status": status,
        "max_extracted_live": newest.isoformat(),
        "age_days": age,
        "warn_after_days": _FRESH_WARN_DAYS,
        "stale_after_days": _FRESH_STALE_DAYS,
        "per_file": per_file,
        "hint": ("map catalog CŨ — refresh (rebuild raw/REBUILD.md) TRƯỚC khi tin lineage/số"
                 if status == "STALE" else None),
    }


# ── R-A1: reconcile live↔catalog (đọc-only) ─────────────────────────────────────
def reconcile_datasets(live_names, catalog_names):
    """THUẦN/tiêm-được: so tên dataset LIVE vs catalog. Trả {added, removed(zombie), matched, n_live, n_catalog}.
      added   = có LIVE nhưng KHÔNG trong catalog (dataset mới, catalog cần bổ sung).
      removed = có trong catalog nhưng KHÔNG còn LIVE (zombie — nguồn đã xóa/đổi tên).
      matched = giao (khớp cả hai).
    So theo tên chuẩn hóa (strip); giữ tên gốc trong output. KHÔNG gọi oac-native (CLI mới làm việc đó)."""
    def norm(s): return str(s).strip()
    live_map = {norm(x): x for x in (live_names or [])}
    cat_map = {norm(x): x for x in (catalog_names or [])}
    lset, cset = set(live_map), set(cat_map)
    added = sorted(live_map[k] for k in (lset - cset))
    removed = sorted(cat_map[k] for k in (cset - lset))
    matched = sorted(live_map[k] for k in (lset & cset))
    return {"added": added, "removed": removed, "matched": matched,
            "n_live": len(lset), "n_catalog": len(cset),
            "n_added": len(added), "n_removed": len(removed), "n_matched": len(matched)}


def _catalog_dataset_names(catalog_dir=None):
    """Đọc dataset_catalog.yaml -> list tên dataset (khóa 'datasets'). Thiếu/parse lỗi -> []."""
    try:
        import yaml
    except Exception:
        return []
    cd = Path(catalog_dir) if catalog_dir is not None else None
    if cd is None:
        try: cd = _catalog_dir()
        except Exception: return []
    p = cd / "dataset_catalog.yaml"
    if not p.is_file():
        return []
    try:
        data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    except Exception:
        return []
    ds = data.get("datasets") or {}
    return list(ds.keys()) if isinstance(ds, dict) else []


def _discover_live_datasets():
    """Gọi oac-native discover_data(datasets) LIVE (read-only) qua runtime bridge.
    Trả (names, error). CLI-only (KHÔNG dùng trong test hermetic). Lỗi -> ([], 'thông điệp')."""
    # Kênh oac-native chạy trong runtime MCP; khi chạy kgr.py CLI thuần KHÔNG có bridge sẵn.
    # Cách thực dụng: gọi qua helper live_discover.py nếu có (owner wire), else báo blocker rõ.
    here = HERE.parent
    for cand in (here / "live_discover.py",
                 KP.resolve_kb_root(start_file=str(HERE)) / "kb_lifecycle" / "tools" / "live_discover.py"):
        try:
            if cand.is_file():
                r = subprocess.run([sys.executable, str(cand), "--datasets"],
                                   capture_output=True, text=True, timeout=120)
                if r.returncode == 0 and r.stdout.strip():
                    try:
                        data = json.loads(r.stdout)
                        names = data.get("datasets") or data.get("names") or []
                        if isinstance(names, list):
                            return names, None
                    except Exception as e:
                        return [], f"parse live_discover output lỗi: {e}"
                return [], f"live_discover exit {r.returncode}: {(r.stderr or r.stdout or '').strip()[:200]}"
        except Exception as e:
            return [], f"live_discover chạy lỗi: {e}"
    return [], ("oac-native discover_data KHÔNG khả dụng ở CLI thuần (cần bridge live_discover.py do owner wire, "
                "hoặc chạy discover_data trong phiên MCP). KHÔNG giả số.")


def cmd_refresh(rest):
    """kgr refresh — cơ chế REFRESH (đọc-only). Cờ:
      --check     : staleness (tái dùng freshness_check R-A2).
      --discover  : gọi oac-native discover_data LIVE -> list tên dataset (lỗi -> exit≠0, không giả).
      --reconcile : so tên dataset LIVE vs dataset_catalog -> {added, removed(zombie), matched}.
      (không cờ)  : --check + --reconcile, in báo cáo drift gọn.
    df/wb enumerate cần chrome REST -> ghi TODO/partial; phần dataset làm được ngay qua oac-native."""
    rest = rest or []
    flags = set(a for a in rest if a.startswith("--"))
    do_check = "--check" in flags
    do_discover = "--discover" in flags
    do_reconcile = "--reconcile" in flags
    if not (do_check or do_discover or do_reconcile):
        do_check = do_reconcile = True   # mặc định

    out = {}
    rc = 0

    if do_check:
        try:
            out["freshness"] = freshness_check()
        except Exception as e:
            out["freshness"] = {"status": "UNKNOWN", "error": str(e)}
        if out["freshness"].get("status") == "STALE":
            rc = 1   # INV-6 fail-ồn

    live_names = None
    if do_discover or do_reconcile:
        live_names, err = _discover_live_datasets()
        out["discover"] = {"n_live": len(live_names or []), "error": err}
        if do_discover:
            out["discover"]["datasets"] = sorted(live_names or [])
        if err:
            # LIVE không lấy được -> báo rõ + exit≠0 (KHÔNG giả số/không im lặng)
            rc = 1

    if do_reconcile:
        if live_names and not out.get("discover", {}).get("error"):
            catalog_names = _catalog_dataset_names()
            rec = reconcile_datasets(live_names, catalog_names)
            out["reconcile"] = rec
            if rec.get("n_added") or rec.get("n_removed"):
                out["reconcile"]["drift"] = True
        else:
            out["reconcile"] = {"error": "không có danh sách LIVE (discover lỗi) -> không reconcile được",
                                "todo": "df/wb enumerate cần chrome REST — phần dataset cần oac-native discover_data live"}
            rc = rc or 1

    out["_note"] = ("refresh đọc-only: KHÔNG ghi OAC, KHÔNG ghi đè catalog. df/wb enumerate = TODO (chrome REST). "
                    "Rebuild reproducible-verify: python OAC-Knowledge/raw/build_catalogs.py --verify")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return rc


def cmd_where():
    print(json.dumps(RT.where(), ensure_ascii=False, indent=2)); return 0

def cmd_setup():
    kb = KP.resolve_kb_root(start_file=str(HERE))
    reg = KP.write_registry(kb)
    out = {"registry": str(reg), "kb_root": str(kb)}
    # Shared pre-commit: trỏ git.hooksPath vào .githooks (versioned, clone theo — thay .git/hooks local-only).
    try:
        ws = RT.workspace_root(start=str(HERE))
        if (ws / ".githooks").is_dir():
            subprocess.run(["git", "-C", str(ws), "config", "core.hooksPath", ".githooks"],
                           capture_output=True, text=True, timeout=30)
            out["core_hooksPath"] = ".githooks"
    except Exception as e:
        out["hooksPath_err"] = str(e)
    print(json.dumps(out, ensure_ascii=False, indent=2)); return 0

def cmd_gc(rest):
    import kb_gc
    return kb_gc.main(rest)

def cmd_doctor():
    rep = {}
    try:
        rep["kb_root"] = str(KP.resolve_kb_root(start_file=str(HERE))); rep["kb_root_ok"] = True
    except Exception as e:
        rep["kb_root_ok"] = False; rep["kb_root_err"] = str(e)
    reg = KP.registry_file(); rep["registry"] = str(reg); rep["registry_ok"] = reg.is_file()
    try:
        rep["runtime_ephemeral"] = str(RT.runtime_dir()); rep["durable_orchestration"] = str(RT.orch_dir(start=str(HERE)))
    except Exception as e:
        rep["runtime_err"] = str(e)
    try:
        import check_clean as CC
        dirty = [f"{lbl}/{f}" for lbl, f, _ in CC.scan_all()]
        rep["repos_clean"] = (len(dirty) == 0); rep["dirty"] = dirty
        phys = [f"{lbl}/{f}" for lbl, f, _ in CC.scan_all_physical()]   # INV-4: scratch RÁC dù gitignored
        rep["physical_scratch"] = phys
    except Exception as e:
        rep["repos_clean"] = None; rep["clean_err"] = str(e); phys = []
    try:
        lg = learn_governance()
    except Exception as e:
        lg = {"is_shim": False, "shim": f"error: {e}", "installed_copy": "n/a", "ok": False}
    rep["learn_governance"] = lg
    try:
        mc = mcp_chrome_check()   # đọc .mcp.json + Chrome process thật; fail-open bên trong
    except Exception as e:
        mc = {"error": str(e), "parse_errors": []}
    rep["mcp_chrome"] = mc
    try:
        fr = freshness_check()   # đọc max(extracted_live) từ catalog thật; hermetic-injectable
    except Exception as e:
        fr = {"status": "UNKNOWN", "error": str(e), "max_extracted_live": None}
    rep["freshness"] = fr
    # THÔNG TIN/cảnh báo: KHÔNG tự lật STATUS trừ khi .mcp.json PARSE LỖI (drift cấu hình thật).
    mcp_ok = not (mc.get("parse_errors") or [])
    # INV-6 fail-ồn: catalog STALE (>14 ngày) góp phần ATTENTION. WARN/OK/UNKNOWN không lật STATUS.
    fresh_ok = fr.get("status") != "STALE"
    ok = bool(rep.get("kb_root_ok") and rep.get("repos_clean")
              and not rep.get("physical_scratch") and lg.get("ok") and mcp_ok and fresh_ok)
    rep["STATUS"] = "OK" if ok else "ATTENTION"
    print(json.dumps(rep, ensure_ascii=False, indent=2))
    return 0 if ok else 1

def cmd_route(rest):
    try:
        import kb_route
    except ImportError:
        print(json.dumps({"error": "kb_route chưa có (P2.2)"}, ensure_ascii=False)); return 2
    return kb_route.cli(rest)

def main(argv):
    a = argv or ["where"]
    cmd, rest = a[0], a[1:]
    table = {"where": lambda: cmd_where(), "setup": lambda: cmd_setup(),
             "doctor": lambda: cmd_doctor(), "gc": lambda: cmd_gc(rest), "route": lambda: cmd_route(rest),
             "refresh": lambda: cmd_refresh(rest)}
    if cmd in table:
        return table[cmd]()
    sys.stderr.write(__doc__ + "\n")
    return 2

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
