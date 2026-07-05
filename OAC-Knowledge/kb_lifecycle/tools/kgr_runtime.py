#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""kgr_runtime — phân vùng đường ghi cho MỌI agent (D9/D10/INV-4). API thay cho "nhắc nhở".

MỌI đường ghi-tạm/state nằm NGOÀI cây project (để agent không crawl vào → đỡ đốt token). Hai lớp:
  • DURABLE (blackboards/locks/build_state + scratch "giữ lại được") → <state_root>/ = <workspace>/../_kgr-state/
    — SIBLING của project root: NGOÀI tầm crawl NHƯNG vẫn trong vùng backup dự án (C:\\Project\\…).
        orchestration/  (blackboards, locks, build_state, resume)   ·   work/<repo>/  (thay <repo>/_work/)
  • EPHEMERAL (scratch/extracts/dumps thuần) → %LOCALAPPDATA%/kgr-oac/runtime — ngoài repo, ngoài backup, xóa tùy ý.

Hợp đồng = env var (KHÔNG truyền qua session/MCP nên DEFAULT phải đúng khi zero-env):
  KGR_WORKSPACE, KGR_STATE_ROOT / KGR_ORCH_DIR / KGR_WORK_DIR (durable), KGR_RUNTIME_DIR / LOCALAPPDATA (ephemeral).
Self-locating: workspace = thư mục chứa cả OAC-Knowledge + OAC-Orchestrator (đi lên từ __file__); state_root = workspace.parent/_kgr-state.
Bản này là CANONICAL (OAC-Knowledge); repo khác dùng bản sao ĐÔNG CỨNG cùng nội dung (đừng sửa lệch).
"""
import os, re
from pathlib import Path

_SENTINELS = ("OAC-Knowledge", "OAC-Orchestrator")
_STATE_DIRNAME = "_kgr-state"

def _env(env):
    return os.environ if env is None else env

def workspace_root(env=None, start=None):
    e = _env(env)
    if e.get("KGR_WORKSPACE"):
        return Path(e["KGR_WORKSPACE"])
    cur = Path(start or __file__).resolve()
    for anc in (cur, *cur.parents):
        try:
            if all((anc / s).is_dir() for s in _SENTINELS):
                return anc
        except Exception:
            pass
    raise RuntimeError("Không tìm thấy workspace root (dir chứa OAC-Knowledge + OAC-Orchestrator). Đặt KGR_WORKSPACE.")

# ── DURABLE (in-backup, NGOÀI cây project) ───────────────────────────
def state_root(env=None, start=None):
    """Gốc state bền, SIBLING của workspace (ngoài crawl, trong backup). Zero-env deterministic."""
    e = _env(env)
    if e.get("KGR_STATE_ROOT"):
        return Path(e["KGR_STATE_ROOT"])
    return workspace_root(e, start).parent / _STATE_DIRNAME

def orch_dir(env=None, start=None):
    e = _env(env)
    if e.get("KGR_ORCH_DIR"):
        return Path(e["KGR_ORCH_DIR"])
    return state_root(e, start) / "orchestration"

def blackboards_dir(env=None, start=None):
    return orch_dir(env, start) / "blackboards"

def locks_dir(env=None, start=None):
    return orch_dir(env, start) / "locks"

def work_dir(repo=None, env=None, start=None):
    """Scratch 'giữ lại được' NGOÀI cây (thay <repo>/_work/). repo=None -> gốc work/."""
    e = _env(env)
    base = Path(e["KGR_WORK_DIR"]) if e.get("KGR_WORK_DIR") else state_root(e, start) / "work"
    return base / _slug(repo) if repo else base

# ── EPHEMERAL (ngoài backup) ─────────────────────────────────────────
def runtime_dir(env=None):
    e = _env(env)
    if e.get("KGR_RUNTIME_DIR"):
        return Path(e["KGR_RUNTIME_DIR"])
    la = e.get("LOCALAPPDATA")
    if la:
        return Path(la) / "kgr-oac" / "runtime"
    return Path(os.path.expanduser("~")) / ".kgr" / "runtime"   # zero-env fallback (LOCALAPPDATA có thể unset dưới MCP)

def _slug(s):
    return re.sub(r"[^0-9A-Za-z._-]+", "_", str(s)).strip("_")[:80] or "default"

def scratch_dir(session="default", env=None):
    return runtime_dir(env) / "scratch" / _slug(session)

def extracts_dir(env=None):
    return runtime_dir(env) / "extracts"

# ── helpers ──────────────────────────────────────────────────────────
def ensure(p):
    p = Path(p); p.mkdir(parents=True, exist_ok=True); return p

def scratch(name, session="default", env=None):
    """Trả path file scratch NGOÀI repo (least-resistance: ngắn hơn việc tự mở file trong cwd)."""
    return ensure(scratch_dir(session, env)) / Path(str(name)).name

def atomic_write(path, data, encoding="utf-8"):
    p = Path(path); ensure(p.parent)
    tmp = p.with_name(p.name + ".tmp")           # cùng dir => cùng volume => os.replace atomic
    with open(tmp, "w", encoding=encoding) as f:
        f.write(data)
    os.replace(tmp, p)
    return p

def where(env=None, start=None):
    return {
        "workspace": str(workspace_root(env, start)),
        "state_root (durable, NGOÀI cây, in-backup)": str(state_root(env, start)),
        "  durable_orchestration": str(orch_dir(env, start)),
        "    blackboards": str(blackboards_dir(env, start)),
        "    locks": str(locks_dir(env, start)),
        "  work (thay <repo>/_work/)": str(work_dir(env=env, start=start)),
        "    work(example repo)": str(work_dir("Dashboard-builder", env, start)),
        "ephemeral_runtime (ngoài backup, xóa được)": str(runtime_dir(env)),
        "  scratch(example)": str(scratch_dir("example", env)),
        "  extracts": str(extracts_dir(env)),
    }

if __name__ == "__main__":
    import json
    print(json.dumps(where(), ensure_ascii=False, indent=2))
