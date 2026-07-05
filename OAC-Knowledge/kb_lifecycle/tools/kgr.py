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
    ok = bool(rep.get("kb_root_ok") and rep.get("repos_clean")
              and not rep.get("physical_scratch") and lg.get("ok"))
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
             "doctor": lambda: cmd_doctor(), "gc": lambda: cmd_gc(rest), "route": lambda: cmd_route(rest)}
    if cmd in table:
        return table[cmd]()
    sys.stderr.write(__doc__ + "\n")
    return 2

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
