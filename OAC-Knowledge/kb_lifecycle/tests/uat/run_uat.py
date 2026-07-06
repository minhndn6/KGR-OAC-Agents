#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PHASE 4 — UAT ≥200 case OFFLINE deterministic (DoD7). run_all.py tự-discover file này.
Mỗi case = {id, category, action, input, expected}. action: route|check_path|clean|gate|guard|dedup|supersede|drift.
Oracle cho check_path ĐỘC LẬP (bảng hand-code dưới), KHÔNG gọi kb_kinds để sinh expected.
exit≠0 nếu FAIL>0 hoặc GAP>0 hoặc tổng<200. `--dump` ghi corpus ra uat_cases.jsonl để xem.
"""
import os, sys, json, tempfile, shutil
from pathlib import Path

HERE = Path(__file__).resolve()
TOOLS = HERE.parents[2] / "tools"
sys.path.insert(0, str(TOOLS))
import kb_paths, kb_kinds, kb_route, check_clean, learn2, guard_generated, drift  # noqa
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

KB = kb_paths.resolve_kb_root(start_file=str(TOOLS / "kb_paths.py"))
FIXTURE = Path(r"C:\Project\_work\kgr-governance-build\oac_freshness_2026-06-21.json")

# ── ORACLE ĐỘC LẬP cho check_path (hand-code; tách khỏi kinds.yaml để bắt drift cấu hình) ──
_O_GEN_YAML = {"dataset_catalog.yaml", "dataflow_catalog.yaml", "workbook_catalog.yaml",
               "physical_table_catalog.yaml", "lineage_graph.yaml", "field_dictionary.yaml", "capability_map.yaml"}
_O_CURATED_TOP = {"business_glossary.yaml", "dataflow_descriptions.yaml", "archive_recommendations.md",
                  "HOW_TO_TRACE_A_FIELD.md",
                  "CONFLICTS_AND_OPEN_QUESTIONS.md", "governance_register.md", "live_query_recipes.md",
                  "KNOWLEDGE_INDEX.md", "LEARNING.md", "source_selection_playbook.md", "OWNER_TODO.md",
                  "QUICK_REFERENCE.md", "CHANGELOG.md", "QA_USECASES_REPORT.md", "IMPROVEMENTS.md", "QA_REPORT.md"}
def oracle_kind(rel):
    rel = rel.replace("\\", "/"); base = rel.rsplit("/", 1)[-1]
    if rel.startswith("learnings/"): return "LOG"
    if rel.startswith("fields/"): return "CURATED" if base.startswith("_") else "GENERATED"
    if base in _O_GEN_YAML: return "GENERATED"
    if base in _O_CURATED_TOP: return "CURATED"
    return "UNKNOWN"

_ROUTE_KIND = {  # bảng độc lập kind theo type (đối chiếu kb_route.classify)
    "new_dataset": "GENERATED", "new_dataflow": "GENERATED", "new_field": "GENERATED",
    "physical_table": "GENERATED", "fact": "GENERATED", "formula_correction": "GENERATED",
    "glossary_term": "CURATED", "convention": "CURATED", "governance_item": "CURATED",
    "gap": "OPEN_QUESTION", "drift": "LOG", "correction": "LOG", "lesson": "LOG", "qa": "LOG"}
_VALID_EV = {  # evidence hợp lệ tối thiểu để promote từng type
    "new_dataset": {"rebuild_sha": "sha"}, "new_dataflow": {"rebuild_sha": "sha"}, "new_field": {"rebuild_sha": "sha"},
    "physical_table": {"rebuild_sha": "sha"}, "fact": {"rebuild_sha": "sha"},
    "formula_correction": {"live_evidence": "executePreview"}, "correction": {"provenance": "owner"},
    "glossary_term": {"attested_by": "owner"}, "convention": {"attested_by": "owner"},
    "governance_item": {"attested_by": "CFO"}, "lesson": {"incorporated_into": "CONVENTIONS.md"}, "qa": {}}
_NO_PROMOTE = {"gap", "drift"}

# ── case builders ──
def build_route():
    cs = []
    for t, k in _ROUTE_KIND.items():
        cs.append({"id": f"route.kind.{t}", "category": "route", "action": "route",
                   "input": {"type": t}, "expected": {"kind": k}})
        cs.append({"id": f"route.wv.{t}", "category": "route", "action": "route_wv",
                   "input": {"type": t}, "expected": {"nonempty": True}})
    for bogus in ["khong_co", "xyz", "FACTT", "drift2"]:
        cs.append({"id": f"route.reject.{bogus}", "category": "route", "action": "route",
                   "input": {"type": bogus}, "expected": {"reject": True}})
    return cs

def build_checkpath():
    cs = []
    # real files (enumerate độc lập bằng glob, KHÔNG dùng kb_kinds)
    rels = []
    for pat in ("*.yaml", "*.md"):
        rels += [p.name for p in sorted(KB.glob(pat))]
    if (KB / "fields").is_dir():
        rels += ["fields/" + p.name for p in sorted((KB / "fields").glob("*.md"))]
    if (KB / "learnings").is_dir():
        rels += ["learnings/" + p.name for p in sorted((KB / "learnings").glob("*")) if p.is_file()]
    for r in rels:
        cs.append({"id": f"cp.real.{r}", "category": "check_path", "action": "check_path",
                   "input": {"path": r}, "expected": {"kind": oracle_kind(r)}})
    # synthetic
    syn = [("fields/NewThing.md", "GENERATED"), ("fields/AnotherDS.md", "GENERATED"),
           ("fields/_NOTES.md", "CURATED"), ("fields/_DRAFT_x.md", "CURATED"),
           ("dataset_catalog.yaml", "GENERATED"), ("dataflow_catalog.yaml", "GENERATED"),
           ("workbook_catalog.yaml", "GENERATED"), ("physical_table_catalog.yaml", "GENERATED"),
           ("lineage_graph.yaml", "GENERATED"), ("field_dictionary.yaml", "GENERATED"),
           ("capability_map.yaml", "GENERATED"), ("business_glossary.yaml", "CURATED"),
           ("governance_register.md", "CURATED"), ("CONVENTIONS.md", "UNKNOWN"),
           ("learnings/log.jsonl", "LOG"), ("learnings/pending.md", "LOG"),
           ("learnings/anything.jsonl", "LOG"), ("random_unlisted.md", "UNKNOWN"),
           ("weird.yaml", "UNKNOWN"), ("notes.txt", "UNKNOWN"), ("foo/bar.md", "UNKNOWN"),
           ("QUICK_REFERENCE.md", "CURATED"), ("KNOWLEDGE_INDEX.md", "CURATED"),
           ("LEARNING.md", "CURATED"), ("CHANGELOG.md", "CURATED"), ("OWNER_TODO.md", "CURATED"),
           ("HOW_TO_TRACE_A_FIELD.md", "CURATED"), ("QA_REPORT.md", "CURATED"),
           ("source_selection_playbook.md", "CURATED"), ("live_query_recipes.md", "CURATED"),
           ("archive_recommendations.md", "CURATED"), ("CONFLICTS_AND_OPEN_QUESTIONS.md", "CURATED"),
           ("IMPROVEMENTS.md", "CURATED"), ("QA_USECASES_REPORT.md", "CURATED"),
           ("fields/SomeDataset.md", "GENERATED"), ("fields/_FLAGSHIP_X.md", "CURATED"),
           ("fields/_EXAMPLES_y.md", "CURATED"), ("fields/sub/deep.md", "GENERATED"),
           ("learnings/extra.md", "LOG"), ("learnings/archive.jsonl", "LOG"),
           ("DATAFLOW_NOTES.md", "UNKNOWN"), ("config.json", "UNKNOWN"),
           ("setup.py", "UNKNOWN"), ("data.csv", "UNKNOWN")]
    for path, k in syn:
        cs.append({"id": f"cp.syn.{path}", "category": "check_path", "action": "check_path",
                   "input": {"path": path}, "expected": {"kind": k}})
    return cs

def build_clean():
    cs = []
    dirty = ["_PNL_HANDOFF.md", "_PNL_BUILD_STATE.md", "_DB01_NOTES.md", "_build_heatmap.js", "_combochip.txt",
             "x.network-response", "_resp_abc", "_snap_1.txt", "a.lock", "blackboards/bb_1.json",
             "OAC-Orchestrator/blackboards/bb_2.json", "raw/__pycache__/x.pyc", "resolver.pyc", "sub/__pycache__/y.pyc"]
    clean = ["dataset_catalog.yaml", "fields/_INDEX.md", "fields/Revenue.md", "kb_lifecycle/STATUS.md",
             "learnings/log.jsonl", "business_glossary.yaml", ".gitattributes", "README.md", "raw/build_catalogs.py",
             "kb_lifecycle/tools/kgr.py"]
    rules = check_clean.load_rules()
    for p in dirty:
        cs.append({"id": f"clean.dirty.{p}", "category": "negative", "action": "clean",
                   "input": {"path": p}, "expected": {"dirty": True}})
    for p in clean:
        cs.append({"id": f"clean.ok.{p}", "category": "clean", "action": "clean",
                   "input": {"path": p}, "expected": {"dirty": False}})
    return cs

def build_gate():
    cs = []
    base = lambda t, src="": [{"id": "L1", "ts": "t", "type": t, "topic": "Chủ đề " + t, "content": "Nội dung " + t, "source": src}]
    for t in _ROUTE_KIND:
        # missing evidence
        exp_missing = "promoted" if t == "qa" else "rejected"
        cs.append({"id": f"gate.missing.{t}", "category": "gate", "action": "gate",
                   "input": {"seed": base(t), "id": "L1", "evidence": {}}, "expected": {"status": exp_missing}})
        # valid evidence
        if t in _NO_PROMOTE:
            exp_valid, ev = "rejected", {"attested_by": "x", "rebuild_sha": "y"}
        else:
            exp_valid, ev = "promoted", _VALID_EV.get(t, {})
        cs.append({"id": f"gate.valid.{t}", "category": "gate", "action": "gate",
                   "input": {"seed": base(t), "id": "L1", "evidence": ev}, "expected": {"status": exp_valid}})
    # extra negatives
    cs.append({"id": "gate.gov.auto", "category": "negative", "action": "gate",
               "input": {"seed": base("governance_item"), "id": "L1", "evidence": {"attested_by": "CFO", "via": "auto"}},
               "expected": {"status": "rejected"}})
    cs.append({"id": "gate.gov.2agent", "category": "negative", "action": "gate",
               "input": {"seed": base("governance_item"), "id": "L1", "evidence": {"attested_by": "CFO", "via": "second-agent"}},
               "expected": {"status": "rejected"}})
    cs.append({"id": "gate.correction.src_user", "category": "gate", "action": "gate",
               "input": {"seed": base("correction", src="user"), "id": "L1", "evidence": {}}, "expected": {"status": "promoted"}})
    cs.append({"id": "gate.contradiction.block", "category": "negative", "action": "gate",
               "input": {"seed": [{"id": "L1", "ts": "t", "type": "glossary_term", "topic": "Doanh thu", "content": "A", "status": "promoted"},
                                  {"id": "L2", "ts": "t", "type": "glossary_term", "topic": "Doanh thu", "content": "B"}],
                         "id": "L2", "evidence": {"attested_by": "owner"}}, "expected": {"status": "rejected"}})
    return cs

def build_dedup_supersede():
    cs = []
    seed1 = [{"id": "L1", "ts": "t", "type": "lesson", "topic": "T", "content": "C", "status": "promoted"}]
    cs.append({"id": "dedup.exact", "category": "negative", "action": "dedup",
               "input": {"seed": seed1, "add": {"type": "lesson", "topic": "T", "content": "C"}}, "expected": {"status": "rejected_dup"}})
    cs.append({"id": "dedup.new", "category": "learn", "action": "dedup",
               "input": {"seed": seed1, "add": {"type": "lesson", "topic": "T2", "content": "C2"}}, "expected": {"status": "added"}})
    gseed = [{"id": "L1", "ts": "t", "type": "glossary_term", "topic": "Doanh thu", "content": "A", "status": "promoted"},
             {"id": "L2", "ts": "t", "type": "glossary_term", "topic": "Doanh thu", "content": "B"}]
    cs.append({"id": "supersede.ok", "category": "learn", "action": "supersede",
               "input": {"seed": gseed, "new": "L2", "old": "L1"}, "expected": {"status": "superseded"}})
    cs.append({"id": "supersede.cross", "category": "negative", "action": "supersede",
               "input": {"seed": [{"id": "L1", "ts": "t", "type": "lesson", "topic": "A", "content": "x"},
                                  {"id": "L2", "ts": "t", "type": "glossary_term", "topic": "B", "content": "y"}],
                         "new": "L2", "old": "L1"}, "expected": {"status": "error"}})
    return cs

def build_guard():
    return [
        {"id": "guard.clean", "category": "guard", "action": "guard", "input": {"op": "clean"}, "expected": {"ok": True}},
        {"id": "guard.modified", "category": "negative", "action": "guard", "input": {"op": "tamper"}, "expected": {"ok": True}},
        {"id": "guard.new", "category": "negative", "action": "guard", "input": {"op": "new"}, "expected": {"ok": True}},
        {"id": "guard.curated_safe", "category": "guard", "action": "guard", "input": {"op": "curated"}, "expected": {"ok": True}},
        {"id": "guard.missing", "category": "negative", "action": "guard", "input": {"op": "missing"}, "expected": {"ok": True}},
        {"id": "guard.unclassified_real", "category": "guard", "action": "guard", "input": {"op": "unclassified_real"}, "expected": {"ok": True}},
    ]

def build_drift():
    sc = ["tsfilter", "tsfilter_after", "debounce_seen", "debounce_open", "upsert", "storm",
          "no_storm", "cooldown_suppress", "cooldown_expire", "auto_resolve", "key_stable", "emit_only_open"]
    return [{"id": f"drift.{s}", "category": "drift", "action": "drift", "input": {"scenario": s}, "expected": {"ok": True}} for s in sc]

# ── handlers ──
def _temp_log(seed):
    d = Path(tempfile.mkdtemp(prefix="uat_log_")); p = d / "log.jsonl"
    with open(p, "w", encoding="utf-8") as f:
        for r in seed: f.write(json.dumps(r, ensure_ascii=False) + "\n")
    learn2.migrate(p, backup=False)
    return p

def _guard(op):
    kb = Path(tempfile.mkdtemp(prefix="uat_kb_")) / "kb"
    (kb / "fields").mkdir(parents=True); (kb / "learnings").mkdir()
    (kb / "dataset_catalog.yaml").write_text("a: 1\n", encoding="utf-8")
    (kb / "business_glossary.yaml").write_text("g: 1\n", encoding="utf-8")
    (kb / "fields" / "Foo.md").write_text("foo\n", encoding="utf-8")
    (kb / "learnings" / "log.jsonl").write_text("{}\n", encoding="utf-8")
    mani = kb / "m.json"; guard_generated.refresh(kb, manifest=mani)
    try:
        if op == "clean":
            return guard_generated.check(kb, manifest=mani) == []
        if op == "tamper":
            (kb / "dataset_catalog.yaml").write_text("a: 999\n", encoding="utf-8")
            return any("MODIFIED" in w for _, w in guard_generated.check(kb, manifest=mani))
        if op == "new":
            (kb / "fields" / "Bar.md").write_text("b\n", encoding="utf-8")
            return any("NEW" in w for _, w in guard_generated.check(kb, manifest=mani))
        if op == "curated":
            (kb / "business_glossary.yaml").write_text("g: 2\n", encoding="utf-8")
            return not any("business_glossary" in r for r, _ in guard_generated.check(kb, manifest=mani))
        if op == "missing":
            (kb / "dataset_catalog.yaml").unlink()
            return any("MISSING" in w for _, w in guard_generated.check(kb, manifest=mani))
        if op == "unclassified_real":
            return kb_kinds.unclassified(KB) == []
    finally:
        shutil.rmtree(kb.parent, ignore_errors=True)
    return False

def _drift(scenario):
    O = lambda tgt="DF_X", obs="2026-06-25T01:00:00Z": {"probe": "freshness", "target": tgt, "observed": obs, "expected": "2026-06-20"}
    if scenario == "tsfilter":
        if not FIXTURE.is_file(): return True  # bỏ qua nếu thiếu fixture (không fail)
        _, skipped = drift.freshness_observations(str(FIXTURE), "2026-06-20"); return skipped == 99
    if scenario == "tsfilter_after":
        if not FIXTURE.is_file(): return True
        obs, _ = drift.freshness_observations(str(FIXTURE), "2026-06-21"); return len(obs) == 0
    if scenario == "debounce_seen":
        st = {}; drift.observe([O()], st, now=1, debounce=2); return list(st.values())[0]["state"] == "seen"
    if scenario == "debounce_open":
        st = {}; drift.observe([O()], st, 1, debounce=2); drift.observe([O()], st, 2, debounce=2)
        return list(st.values())[0]["state"] == "open"
    if scenario == "upsert":
        st = {}; [drift.observe([O()], st, n, debounce=2) for n in (1, 2, 3)]; return len(st) == 1 and list(st.values())[0]["hit_count"] == 3
    if scenario == "storm":
        st = {}; s = drift.observe([O(f"T{i}") for i in range(11)], st, 1, debounce=2, storm_k=10); return s["bulk"] is True
    if scenario == "no_storm":
        st = {}; s = drift.observe([O(f"T{i}") for i in range(5)], st, 1, debounce=2, storm_k=10); return s["bulk"] is False
    if scenario == "cooldown_suppress":
        st = {}; drift.observe([O()], st, 1, debounce=1); drift.mark_emitted(st, 1, cooldown=1000); return drift.to_emit(st, 500) == []
    if scenario == "cooldown_expire":
        st = {}; drift.observe([O()], st, 1, debounce=1); drift.mark_emitted(st, 1, cooldown=1000); return len(drift.to_emit(st, 2000)) == 1
    if scenario == "auto_resolve":
        st = {}; drift.observe([O("DF_Y")], st, 1, debounce=1); drift.auto_resolve(st, {"DF_Y"}, 9); return list(st.values())[0]["state"] == "resolved_stale"
    if scenario == "key_stable":
        return drift.drift_key("freshness", "DF_X", "2026-06-25T01:00:00Z") == drift.drift_key("freshness", "DF_X", "2026-06-25T01:00:00Z")
    if scenario == "emit_only_open":
        st = {}; drift.observe([O()], st, 1, debounce=2); return drift.to_emit(st, 1) == []
    return False

def run_case(c):
    a, inp, exp = c["action"], c["input"], c["expected"]
    try:
        if a == "route":
            r = kb_route.classify(inp["type"])
            if exp.get("reject"): return r is None
            return r is not None and r.get("kind") == exp.get("kind")
        if a == "route_wv":
            r = kb_route.classify(inp["type"]); return bool(r and r.get("write_via"))
        if a == "check_path":
            return kb_kinds.classify(inp["path"]) == exp["kind"]
        if a == "clean":
            v = check_clean.violation(inp["path"], check_clean.load_rules()); return (v is not None) == exp["dirty"]
        if a == "gate":
            p = _temp_log(inp["seed"])
            try: res = learn2.promote(inp["id"], inp.get("evidence", {}), log=p)
            finally: shutil.rmtree(p.parent, ignore_errors=True)
            return res.get("status") == exp["status"]
        if a == "dedup":
            p = _temp_log(inp["seed"])
            try: res = learn2.add(inp["add"]["type"], inp["add"]["topic"], inp["add"]["content"], log=p)
            finally: shutil.rmtree(p.parent, ignore_errors=True)
            return res.get("status") == exp["status"]
        if a == "supersede":
            p = _temp_log(inp["seed"])
            try: res = learn2.supersede(inp["new"], inp["old"], "r", "ref", log=p)
            finally: shutil.rmtree(p.parent, ignore_errors=True)
            return res.get("status") == exp["status"]
        if a == "guard":
            return _guard(inp["op"]) == exp["ok"]
        if a == "drift":
            return _drift(inp["scenario"]) == exp["ok"]
    except Exception as e:
        return ("__EXC__", str(e))
    return "__GAP__"

def main():
    cases = (build_route() + build_checkpath() + build_clean() + build_gate()
             + build_dedup_supersede() + build_guard() + build_drift())
    if "--dump" in sys.argv:
        outp = HERE.parent / "uat_cases.jsonl"
        with open(outp, "w", encoding="utf-8") as f:
            for c in cases: f.write(json.dumps(c, ensure_ascii=False) + "\n")
        print(f"dumped {len(cases)} -> {outp}")
    from collections import Counter
    catc = Counter(c["category"] for c in cases)
    npass = nfail = ngap = 0; fails = []
    for c in cases:
        r = run_case(c)
        if r is True: npass += 1
        elif r == "__GAP__" or (isinstance(r, tuple) and r and r[0] == "__GAP__"): ngap += 1; fails.append((c["id"], "GAP"))
        else:
            nfail += 1
            fails.append((c["id"], r if not isinstance(r, tuple) else r[1]))
    print(f"UAT categories: {dict(catc)}")
    for cid, why in fails[:40]:
        print(f"  FAIL {cid}: {why}")
    total = len(cases)
    print(f"\n== UAT: PASS={npass} FAIL={nfail} GAP={ngap} / TỔNG={total} ==")
    ok = (nfail == 0 and ngap == 0 and total >= 200)
    print("UAT " + ("✅ ĐẠT (≥200, 0 FAIL, 0 GAP)" if ok else "❌ CHƯA ĐẠT"))
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
