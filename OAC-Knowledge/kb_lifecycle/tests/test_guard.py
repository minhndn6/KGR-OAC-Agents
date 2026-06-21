#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TDD P2.1/2.3 — classify (kb_kinds) + anti-edit guard (guard_generated) (D1/D2/INV-2).
Part A hermetic (tamper detection); Part B KB thật (coverage gate: 0 unclassified, không hand-edit lén).
Chạy: PYTHONUTF8=1 python kb_lifecycle/tests/test_guard.py"""
import sys, tempfile, shutil
from pathlib import Path

HERE = Path(__file__).resolve()
TOOLS = HERE.parents[1] / "tools"
sys.path.insert(0, str(TOOLS))

PASS = FAIL = 0
def chk(c, l):
    global PASS, FAIL
    if c: PASS += 1; print(f"  PASS  {l}")
    else: FAIL += 1; print(f"  FAIL  {l}")

def main():
    import kb_kinds as K, guard_generated as G, kb_paths as KP
    tmp = Path(tempfile.mkdtemp(prefix="kgr_guard_"))
    try:
        kb = tmp / "kb"; (kb / "fields").mkdir(parents=True); (kb / "learnings").mkdir()
        (kb / "dataset_catalog.yaml").write_text("a: 1\n", encoding="utf-8")
        (kb / "business_glossary.yaml").write_text("g: 1\n", encoding="utf-8")
        (kb / "fields" / "Foo.md").write_text("foo\n", encoding="utf-8")
        (kb / "fields" / "_INDEX.md").write_text("idx\n", encoding="utf-8")
        (kb / "learnings" / "log.jsonl").write_text("{}\n", encoding="utf-8")
        (kb / "weird_unlisted.md").write_text("x\n", encoding="utf-8")
        kinds = {"generated_globs": ["*_catalog.yaml", "fields/*.md"], "generated_exclude": ["fields/_*.md"],
                 "curated": ["business_glossary.yaml", "fields/_*.md"], "log_globs": ["learnings/*"]}

        print("== Part A: classify ==")
        chk(K.classify("dataset_catalog.yaml", kinds) == "GENERATED", "*_catalog.yaml -> GENERATED")
        chk(K.classify("business_glossary.yaml", kinds) == "CURATED", "business_glossary -> CURATED")
        chk(K.classify("fields/Foo.md", kinds) == "GENERATED", "fields/Foo.md -> GENERATED")
        chk(K.classify("fields/_INDEX.md", kinds) == "CURATED", "fields/_INDEX.md -> CURATED (exclude thắng generated)")
        chk(K.classify("learnings/log.jsonl", kinds) == "LOG", "learnings/* -> LOG")
        chk(K.classify("weird_unlisted.md", kinds) == "UNKNOWN", "file lạ -> UNKNOWN")
        chk("weird_unlisted.md" in K.unclassified(kb, kinds), "unclassified() bắt file lạ")

        print("== Part A: guard refresh / tamper / curated-an-toàn ==")
        mani = tmp / "manifest.json"
        G.refresh(kb, manifest=mani, kinds=kinds)
        chk(G.check(kb, manifest=mani, kinds=kinds) == [], "sau refresh -> check sạch")
        (kb / "dataset_catalog.yaml").write_text("a: 999  # hand edit\n", encoding="utf-8")
        iss = G.check(kb, manifest=mani, kinds=kinds)
        chk(any(r == "dataset_catalog.yaml" and "MODIFIED" in w for r, w in iss), "hand-edit GENERATED -> MODIFIED")
        (kb / "fields" / "Bar.md").write_text("bar\n", encoding="utf-8")
        iss = G.check(kb, manifest=mani, kinds=kinds)
        chk(any("Bar.md" in r and "NEW" in w for r, w in iss), "GENERATED mới -> NEW (chưa bless)")
        (kb / "business_glossary.yaml").write_text("g: 2\n", encoding="utf-8")
        iss = G.check(kb, manifest=mani, kinds=kinds)
        chk(not any("business_glossary" in r for r, w in iss), "sửa CURATED KHÔNG bị guard (direct-edit hợp lệ)")

        print("== Part B: KB thật ==")
        kbr = KP.resolve_kb_root(start_file=str(TOOLS / "kb_kinds.py"))
        gens = G.generated_files(kbr)
        chk(len(gens) >= 7, f"≥7 file GENERATED ({len(gens)})")
        unc = K.unclassified(kbr)
        chk(unc == [], "0 file tri thức UNCLASSIFIED (coverage gate)" + (f" -> {unc}" if unc else ""))
        if not (TOOLS.parent / "generated_manifest.json").is_file():
            G.refresh(kbr)  # bootstrap baseline lần đầu
        bad = [x for x in G.check(kbr) if "MODIFIED" in x[1] or "MISSING" in x[1]]
        chk(not bad, f"không file GENERATED bị sửa lén / mất ({bad})")

        print(f"\n== TỔNG: PASS={PASS} FAIL={FAIL} ==")
        return 1 if FAIL else 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

if __name__ == "__main__":
    sys.exit(main())
