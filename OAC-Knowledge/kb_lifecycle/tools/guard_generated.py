#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""guard_generated — anti-edit guard cho file GENERATED (D2/INV-2) qua HASH-MANIFEST sidecar.
KHÔNG stamp banner vào file lớn (tránh churn 13k-dòng field_dictionary); thay vào đó lưu sha256.
Semantics = giống "hash-in-banner": sau REBUILD hợp lệ -> `refresh` (re-bless); hand-edit không refresh -> `check` FAIL.
(Mạnh tương đương hash-in-banner; chống "sửa cả nguồn+output" cần rebuild-and-diff — hoãn tới khi rebuild reproducible.)

Usage:
  python guard_generated.py refresh   # tính lại manifest (chạy SAU rebuild hợp lệ)
  python guard_generated.py check     # exit≠0 nếu file generated đổi mà chưa refresh / mất / mới
"""
import sys, json, hashlib
from pathlib import Path

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parent))
import kb_kinds  # noqa: E402
import kb_paths  # noqa: E402

MANIFEST = HERE.parent.parent / "generated_manifest.json"   # kb_lifecycle/

def _sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def generated_files(kb_root, kinds=None):
    return [f for f in kb_kinds.knowledge_files(kb_root) if kb_kinds.classify(f, kinds) == "GENERATED"]

def refresh(kb_root, manifest=None, kinds=None):
    kb_root = Path(kb_root)
    m = {rel: {"sha256": _sha(kb_root / rel)} for rel in generated_files(kb_root, kinds)}
    Path(manifest or MANIFEST).write_text(json.dumps(m, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    return m

def check(kb_root, manifest=None, kinds=None):
    kb_root = Path(kb_root)
    mp = Path(manifest or MANIFEST)
    saved = json.loads(mp.read_text(encoding="utf-8")) if mp.is_file() else {}
    cur = {rel: _sha(kb_root / rel) for rel in generated_files(kb_root, kinds)}
    issues = []
    for rel, h in cur.items():
        if rel not in saved:
            issues.append((rel, "NEW (chưa bless — chạy refresh sau rebuild)"))
        elif saved[rel].get("sha256") != h:
            issues.append((rel, "MODIFIED (hand-edit? hoặc rebuild chưa refresh)"))
    for rel in saved:
        if rel not in cur:
            issues.append((rel, "MISSING (file generated biến mất)"))
    return issues

def main(argv):
    cmd = argv[0] if argv else "check"
    kb = kb_paths.resolve_kb_root(start_file=str(HERE))
    if cmd == "refresh":
        m = refresh(kb)
        print(json.dumps({"refreshed": len(m), "manifest": str(MANIFEST)}, ensure_ascii=False)); return 0
    if cmd == "check":
        iss = check(kb)
        for rel, why in iss:
            print(f"  GUARD {rel}: {why}")
        unc = kb_kinds.unclassified(kb)
        for f in unc:
            print(f"  UNCLASSIFIED {f}: thêm vào kinds.yaml")
        n = len(iss) + len(unc)
        print(f"guard_generated: {len(iss)} hash-issue, {len(unc)} unclassified.")
        return 1 if n else 0
    sys.stderr.write(__doc__ + "\n"); return 2

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
