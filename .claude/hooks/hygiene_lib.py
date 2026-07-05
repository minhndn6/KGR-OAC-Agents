#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""hygiene_lib — phân loại đích Write/Edit cho guard hook (INV-2/INV-4). PURE + testable.

Tái dùng NGUỒN CHÂN LÝ sẵn có (không copy pattern → tránh split-brain):
  • check_clean.violation + clean_rules.json  (mẫu scratch/dump: _PNL_*, *.network-response, _snap_*, *.lock…)
  • generated_manifest.json                    (danh sách file GENERATED — sửa tay là vi phạm INV-2)
  • kgr_runtime.work_dir()/scratch()           (đích ghi hợp lệ NGOÀI cây project)

classify(path, ws_root, rules, generated_abs) -> (verdict, reason)
  verdict ∈ {allow, deny_junk, deny_generated}. Hook (Hybrid): hard-deny 2 loại deny_*, còn lại allow.
"""
import json, sys
from pathlib import Path

HERE = Path(__file__).resolve()
_TOOLS = HERE.parents[2] / "OAC-Knowledge" / "kb_lifecycle" / "tools"   # <ws>/.claude/hooks -> <ws>/OAC-Knowledge/...
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))

# Ghi-tạm/state phải nằm NGOÀI cây; các dir in-tree được phép ghi trực tiếp (source/config/append-log):
_ALLOW_INTREE = {".git", ".claude", ".secrets", "raw", "learnings", "__pycache__", "node_modules"}
# Tên dir scratch/state CŨ không còn được phép ở trong cây (đã dời ra _kgr-state):
_FORBID_INTREE_DIRS = {"_work", "_orchestration", "blackboards", "locks"}
_KB_SUBDIR = "OAC-Knowledge"   # nơi chứa file GENERATED (manifest kb-root-relative)


def _violation(rel_posix, rules):
    """Reuse check_clean.violation (pure) nếu import được; fallback matcher tối thiểu."""
    try:
        import check_clean
        return check_clean.violation(rel_posix, rules or {})
    except Exception:
        import fnmatch
        base = rel_posix.rsplit("/", 1)[-1]
        for pat in (rules or {}).get("deny_glob", []):
            if fnmatch.fnmatch(rel_posix, pat) or fnmatch.fnmatch(base, pat):
                return pat
        return None


def _has_generated_banner(p):
    try:
        with open(p, "r", encoding="utf-8", errors="ignore") as f:
            head = f.read(200)
        return head.lstrip().startswith("# GENERATED")
    except Exception:
        return False


def classify(path, ws_root, rules=None, generated_abs=None):
    """PURE. path=đích Write/Edit; ws_root=workspace root; generated_abs=set[Path tuyệt đối] file GENERATED."""
    try:
        p = Path(path).resolve()
    except Exception:
        return ("allow", "")
    ws = Path(ws_root).resolve()
    try:
        rel = p.relative_to(ws).as_posix()
    except Exception:
        return ("allow", "ngoài cây project (state/scratch ngoài → OK)")   # _kgr-state, %LOCALAPPDATA%, plan file…

    parts = rel.split("/")
    # 1) Cấm tái tạo thư mục scratch/state trong cây
    if any(d in _FORBID_INTREE_DIRS for d in parts):
        return ("deny_junk",
                "Scratch/state KHÔNG được nằm trong cây project (agent sẽ crawl → đốt token). "
                "Ghi vào kgr_runtime.work_dir('<repo>') (giữ lại được) hoặc kgr_runtime.scratch('ten.ext') "
                "(xóa được) — cả hai NGOÀI project. `python OAC-Knowledge/kb_lifecycle/tools/kgr.py where`.")
    # 2) Dir in-tree được phép ghi thẳng (source/config/log; .claude ở root, raw/learnings dưới OAC-Knowledge) → allow sớm
    if any(d in _ALLOW_INTREE for d in parts):
        return ("allow", "")
    # 3) File GENERATED (manifest hoặc banner) → cấm sửa tay
    if generated_abs and p in generated_abs:
        return ("deny_generated",
                "File GENERATED (trong generated_manifest.json) — sửa NGUỒN ở raw/ rồi rebuild theo "
                "OAC-Knowledge/raw/REBUILD.md, sau đó `guard_generated.py refresh`. KHÔNG sửa tay output.")
    if _has_generated_banner(p):
        return ("deny_generated", "File có banner '# GENERATED' — sửa nguồn + rebuild, đừng sửa tay.")
    # 4) Tên khớp mẫu scratch/dump ở bất kỳ đâu trong cây → cấm (redirect ra ngoài)
    pat = _violation(rel, rules or {})
    if pat:
        return ("deny_junk",
                f"Tên khớp mẫu scratch/dump ({pat}) — ghi ra kgr_runtime.scratch()/work_dir() NGOÀI project, "
                "không để trong cây.")
    return ("allow", "")


# ── Context builder cho hook (KHÔNG dùng trong unit test — test truyền tay) ──────────
def load_context(ws_root):
    """Đọc clean_rules.json + generated_manifest.json từ đĩa; trả (rules, generated_abs)."""
    ws = Path(ws_root)
    kbl = ws / _KB_SUBDIR / "kb_lifecycle"
    rules = {}
    try:
        rules = json.loads((kbl / "clean_rules.json").read_text(encoding="utf-8"))
    except Exception:
        pass
    generated_abs = set()
    try:
        man = json.loads((kbl / "generated_manifest.json").read_text(encoding="utf-8"))
        generated_abs = {(ws / _KB_SUBDIR / rel).resolve() for rel in man.keys()}
    except Exception:
        pass
    return rules, generated_abs
