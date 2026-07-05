#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_clean — cleanliness gate cho CẢ 4 repo (D11/INV-4). Tracked script (chạy như test + hook),
KHÔNG dựa .git/hooks local (không clone, leak nằm ở repo không có hook).
FAIL nếu có file scratch/state bị TRACK. Scoped: KHÔNG blanket _*.md (giữ curated fields/_*.md).

Usage:
  python check_clean.py            # quét 4 repo thật, exit≠0 nếu có vi phạm
  (lib) scan(files, rules) -> [(relpath, pattern)]   # thuần, để test hermetic
"""
import os, sys, json, fnmatch, subprocess
from pathlib import Path

try: sys.stdout.reconfigure(encoding="utf-8")   # tránh crash cp1252 trên console Windows (vd chạy từ git hook)
except Exception: pass

HERE = Path(__file__).resolve()
RULES_PATH = HERE.parent.parent / "clean_rules.json"     # tools/ -> kb_lifecycle/
WS = Path(os.environ.get("KGR_WORKSPACE") or r"C:\Project\KGR-OAC-Agents")
REPOS = ["OAC-Knowledge", "OAC-Orchestrator", "Dashboard-builder", "Dataflow-builder"]

def load_rules(path=None):
    return json.load(open(path or RULES_PATH, encoding="utf-8"))

def tracked_files(repo):
    r = subprocess.run(["git", "-C", str(repo), "ls-files"], capture_output=True, text=True, timeout=120)
    return [l for l in r.stdout.splitlines() if l.strip()]

def violation(relpath, rules):
    posix = relpath.replace("\\", "/")
    base = posix.rsplit("/", 1)[-1]
    parts = posix.split("/")
    if rules.get("deny_pyc"):
        if posix.endswith(".pyc"): return "*.pyc"
        if "__pycache__" in parts: return "__pycache__"
    for pat in rules.get("deny_glob", []):
        if fnmatch.fnmatch(posix, pat) or fnmatch.fnmatch(base, pat):
            return pat
    return None

def scan(files, rules):
    out = []
    for f in files:
        p = violation(f, rules)
        if p: out.append((f, p))
    return out

def repos_to_scan():
    """Thích nghi topology: monorepo (root có .git) -> quét root; nếu không -> 4 sub-repo có .git."""
    if (WS / ".git").exists():
        return [WS]
    return [WS / r for r in REPOS if (WS / r / ".git").exists()]

def scan_all(rules=None):
    rules = rules or load_rules()
    out = []
    for p in repos_to_scan():
        for f, pat in scan(tracked_files(p), rules):
            out.append((p.name, f, pat))
    return out

# ── physical scan (INV-4) — bắt scratch nằm RÁC trong cây DÙ bị .gitignore ─────
# Lỗ hổng cũ: scan() chỉ thấy git-TRACKED → scratch gitignored (vd Dashboard-builder/_PNL_*.md,
# _pivot_*.png) vô hình với gate → báo "SẠCH" giả. scan_physical quét file VẬT LÝ ngoài các
# vùng scratch/product hợp lệ. Scratch hợp lệ phải nằm trong <repo>/_work/ (xem CONVENTIONS.md).
SCRATCH_OK_DIRS = {"_work", "_archived", ".git", ".claude", ".secrets", "__pycache__",
                   "node_modules", "raw", "learnings", "_oac_extract", "_orchestration"}
SCRATCH_EXT = (".png", ".jpg", ".jpeg", ".gif", ".json", ".txt", ".js", ".csv",
               ".html", ".network-response", ".lock")

def scan_physical(repo, rules=None):
    rules = rules or load_rules()
    repo = Path(repo); out = []
    for dp, dirs, files in os.walk(repo):
        rel = Path(dp).relative_to(repo); parts = rel.parts
        if any(p in SCRATCH_OK_DIRS for p in parts):
            dirs[:] = []; continue
        dirs[:] = [d for d in dirs if d not in SCRATCH_OK_DIRS]
        for fn in files:
            relpath = (str(rel / fn) if parts else fn).replace("\\", "/")
            pat = violation(relpath, rules)                       # named scratch (deny_glob) ở mọi nơi
            if pat is None and fn.startswith("_") and fn.lower().endswith(SCRATCH_EXT):
                pat = "_*scratch (ảnh/dump/response) ngoài _work/"
            if pat:
                out.append((relpath, pat))
    return out

def scan_all_physical(rules=None):
    rules = rules or load_rules()
    out = []
    for p in repos_to_scan():
        for f, pat in scan_physical(p, rules):
            out.append((p.name, f, pat))
    return out

def main():
    targets = repos_to_scan()
    if not targets:
        print("check_clean: KHÔNG có git repo nào (chưa init?)."); return 0
    strict = "--strict" in sys.argv
    v = scan_all()
    phys = scan_all_physical()
    for label, f, pat in v:
        print(f"  DIRTY       {label}/{f}   (match {pat})")
    for label, f, pat in phys:
        print(f"  SCRATCH-RÁC {label}/{f}   (match {pat})")
    rc = 0
    if v:
        print(f"\ncheck_clean: {len(v)} file scratch/state bị TRACK -> BẨN. Gỡ: git rm --cached + .gitignore scoped.")
        rc = 1
    if phys:
        tail = "" if strict else "  [WARN — thêm --strict để fail gate]"
        print(f"\ncheck_clean: {len(phys)} file scratch nằm RÁC trong cây (ngoài _work/). "
              f"Chuyển vào <repo>/_work/ hoặc dùng kgr_runtime.scratch().{tail}")
        if strict: rc = 1
    if not v and not phys:
        print(f"check_clean: SẠCH (quét {len(targets)} repo: {[p.name for p in targets]}).")
    return rc

if __name__ == "__main__":
    sys.exit(main())
