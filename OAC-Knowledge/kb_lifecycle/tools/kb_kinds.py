#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""kb_kinds — phân loại file tri thức (GENERATED|CURATED|LOG|UNKNOWN) theo kinds.yaml (D1/INV-2).
Nguồn chân lý cho kb_route.check_path, guard_generated, và validator coverage."""
import fnmatch
from pathlib import Path
import yaml

HERE = Path(__file__).resolve()
KINDS_PATH = HERE.parent.parent / "kinds.yaml"   # kb_lifecycle/kinds.yaml

def load_kinds(path=None):
    with open(path or KINDS_PATH, encoding="utf-8") as f:
        return yaml.safe_load(f)

def _match(posix, base, globs):
    return any(fnmatch.fnmatch(posix, g) or fnmatch.fnmatch(base, g) for g in (globs or []))

def classify(relpath, kinds=None):
    kinds = kinds if kinds is not None else load_kinds()
    posix = str(relpath).replace("\\", "/").lstrip("./")
    base = posix.rsplit("/", 1)[-1]
    if _match(posix, base, kinds.get("log_globs")):       return "LOG"
    if _match(posix, base, kinds.get("curated")):         return "CURATED"   # gồm fields/_*.md
    if _match(posix, base, kinds.get("generated_exclude")): return "CURATED"
    if _match(posix, base, kinds.get("generated_globs")): return "GENERATED"
    return "UNKNOWN"

def knowledge_files(kb_root):
    """Phạm vi file TRI THỨC cần phân loại (KHÔNG gồm code/meta: kb_lifecycle, raw, skill, external)."""
    kb = Path(kb_root); out = []
    for pat in ("*.yaml", "*.md"):
        out += [p.name for p in sorted(kb.glob(pat))]
    fd = kb / "fields"
    if fd.is_dir():
        out += ["fields/" + p.name for p in sorted(fd.glob("*.md"))]
    ld = kb / "learnings"
    if ld.is_dir():
        out += ["learnings/" + p.name for p in sorted(ld.glob("*")) if p.is_file()]
    return out

def unclassified(kb_root, kinds=None):
    kinds = kinds if kinds is not None else load_kinds()
    return [f for f in knowledge_files(kb_root) if classify(f, kinds) == "UNKNOWN"]

if __name__ == "__main__":
    import sys, json, kb_paths  # noqa
    kb = kb_paths.resolve_kb_root(start_file=str(HERE))
    files = knowledge_files(kb)
    from collections import Counter
    cnt = Counter(classify(f) for f in files)
    print(json.dumps({"kb": str(kb), "counts": dict(cnt), "unclassified": unclassified(kb)}, ensure_ascii=False, indent=2))
