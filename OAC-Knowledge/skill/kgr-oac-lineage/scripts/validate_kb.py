"""
validate_kb.py — Referential-integrity checks across all 5 OAC Knowledge Base catalogs.

Usage:
    python validate_kb.py

Exits 0 if no ERRORs; exits 1 if any ERROR found.
WARNs are printed but do not affect the exit code.
"""
import sys as _sys
try: _sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass
import sys
import os
from pathlib import Path
from typing import Any, Dict, Optional

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml not installed. Run: pip install pyyaml")
    sys.exit(1)

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
def _find_kb_root():
    if os.environ.get("OAC_KB_ROOT"):
        return Path(os.environ["OAC_KB_ROOT"])
    for c in [SCRIPT_DIR.parent.parent.parent, Path(r"C:\Project\OAC-Knowledge")]:
        if (c / "lineage_graph.yaml").exists():
            return c
    return SCRIPT_DIR.parent.parent.parent
KB_ROOT = _find_kb_root()

CATALOG_FILES = {
    "physical": KB_ROOT / "physical_table_catalog.yaml",
    "dataflow": KB_ROOT / "dataflow_catalog.yaml",
    "dataset":  KB_ROOT / "dataset_catalog.yaml",
    "workbook": KB_ROOT / "workbook_catalog.yaml",
    "lineage":  KB_ROOT / "lineage_graph.yaml",
}

errors: list = []
warns: list  = []


def err(msg: str):
    errors.append(msg)
    print(f"  ERROR: {msg}")


def warn(msg: str):
    warns.append(msg)
    print(f"  WARN:  {msg}")


def load(key: str) -> Optional[dict]:
    path = CATALOG_FILES[key]
    if not path.exists():
        err(f"Catalog file missing: {path}")
        return None
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def safe_list(val: Any) -> list:
    if val is None:
        return []
    if isinstance(val, list):
        return val
    return [val]


def safe_dict(val: Any) -> dict:
    return val if isinstance(val, dict) else {}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print("=" * 70)
    print("OAC Knowledge Base — Referential-Integrity Validation")
    print(f"KB root: {KB_ROOT}")
    print("=" * 70)

    # Load all catalogs
    phys_raw    = load("physical")
    df_raw      = load("dataflow")
    ds_raw      = load("dataset")
    wb_raw      = load("workbook")
    lin_raw     = load("lineage")

    phys_tables  = safe_dict(phys_raw.get("physical_tables") if phys_raw else None)
    dataflows    = safe_dict(df_raw.get("dataflows")         if df_raw   else None)
    datasets     = safe_dict(ds_raw.get("datasets")          if ds_raw   else None)
    workbooks    = safe_dict(wb_raw.get("workbooks")         if wb_raw   else None)
    lin_edges    = safe_list(lin_raw.get("edges")            if lin_raw  else None)

    # -----------------------------------------------------------------------
    # (a) Workbook viz field sources → dataset_catalog
    # -----------------------------------------------------------------------
    print("\n[a] Workbook field sources → dataset_catalog")
    a_checked = a_warn = 0
    for wb_name, wb in workbooks.items():
        for canvas in safe_list(wb.get("canvases")):
            for viz in safe_list(canvas.get("vizzes")):
                for field in safe_list(viz.get("fields")):
                    for src in safe_list(field.get("sources")):
                        if not isinstance(src, str) or "." not in src:
                            continue
                        ds_name = src.split(".")[0]
                        a_checked += 1
                        if ds_name not in datasets:
                            warn(f"Workbook '{wb_name}' viz field source dataset not in dataset_catalog: '{ds_name}'")
                            a_warn += 1
    print(f"  Checked {a_checked} source references; {a_warn} WARN(s).")

    # -----------------------------------------------------------------------
    # (b) Dataflow input_datasets / output_datasets → dataset_catalog
    # -----------------------------------------------------------------------
    print("\n[b] Dataflow input/output datasets → dataset_catalog")
    b_checked = b_warn = 0
    for df_name, df in dataflows.items():
        for ds_name in safe_list(df.get("input_datasets")) + safe_list(df.get("output_datasets")):
            if ds_name is None:
                continue
            b_checked += 1
            if ds_name not in datasets:
                warn(f"Dataflow '{df_name}' references dataset not in dataset_catalog: '{ds_name}'")
                b_warn += 1
    print(f"  Checked {b_checked} dataset references; {b_warn} WARN(s).")

    # -----------------------------------------------------------------------
    # (c) Dataset produced_by_dataflows → dataflow_catalog (ERROR)
    # -----------------------------------------------------------------------
    print("\n[c] Dataset produced_by_dataflows → dataflow_catalog")
    c_checked = c_err = 0
    for ds_name, ds in datasets.items():
        for df_name in safe_list(ds.get("produced_by_dataflows")):
            if df_name is None:
                continue
            c_checked += 1
            if df_name not in dataflows:
                err(f"Dataset '{ds_name}' produced_by_dataflows has unknown dataflow: '{df_name}'")
                c_err += 1
    print(f"  Checked {c_checked} references; {c_err} ERROR(s).")

    # -----------------------------------------------------------------------
    # (d) Dataset physical_tables → physical_table_catalog (ERROR)
    # -----------------------------------------------------------------------
    print("\n[d] Dataset physical_tables → physical_table_catalog")
    d_checked = d_err = 0
    for ds_name, ds in datasets.items():
        for tbl_name in safe_dict(ds.get("physical_tables")).keys():
            if tbl_name is None:
                continue
            d_checked += 1
            if tbl_name not in phys_tables:
                err(f"Dataset '{ds_name}' physical_tables has unknown table: '{tbl_name}'")
                d_err += 1
    print(f"  Checked {d_checked} table references; {d_err} ERROR(s).")

    # -----------------------------------------------------------------------
    # (e) Lineage edge endpoints → respective catalogs
    # -----------------------------------------------------------------------
    print("\n[e] Lineage graph edges → catalog membership")
    e_checked = e_err = e_warn = 0
    for edge in lin_edges:
        for endpoint in (edge.get("from"), edge.get("to")):
            if not isinstance(endpoint, str) or ":" not in endpoint:
                continue
            node_type, node_val = endpoint.split(":", 1)
            e_checked += 1
            if node_type == "physical":
                # strip any /col suffix
                tbl = node_val.split("/")[0]
                if tbl not in phys_tables:
                    err(f"Lineage edge endpoint physical table not in catalog: '{tbl}'")
                    e_err += 1
            elif node_type == "dataset":
                ds_name = node_val.split("/")[0]
                if ds_name not in datasets:
                    warn(f"Lineage edge endpoint dataset not in catalog: '{ds_name}'")
                    e_warn += 1
    print(f"  Checked {e_checked} edge endpoints; {e_err} ERROR(s), {e_warn} WARN(s).")

    # -----------------------------------------------------------------------
    # (f) Freshness — extracted_live presence; count missing verified_live
    # -----------------------------------------------------------------------
    print("\n[f] Physical table freshness")
    f_missing_extracted = 0
    f_missing_verified  = 0
    for tbl_name, tbl in phys_tables.items():
        if not safe_dict(tbl).get("extracted_live"):
            warn(f"Physical table missing extracted_live: '{tbl_name}'")
            f_missing_extracted += 1
        vl = safe_dict(tbl).get("verified_live")
        if vl is None or vl is False:
            f_missing_verified += 1
    print(f"  Missing extracted_live: {f_missing_extracted}")
    print(f"  Missing/False verified_live (not yet probe-verified): {f_missing_verified}")

    # -----------------------------------------------------------------------
    # (g) Summary counts
    # -----------------------------------------------------------------------
    print("\n[g] Summary counts")

    n_datasets    = len(datasets)
    n_dataflows   = len(dataflows)
    n_phys        = len(phys_tables)
    n_edges       = len(lin_edges)
    n_workbooks   = len(workbooks)

    n_closure_ds  = sum(
        1 for ds in datasets.values()
        if safe_dict(ds).get("in_closure") is True
    )
    n_closure_df  = sum(
        1 for df in dataflows.values()
        if safe_dict(df).get("in_closure") is True
    )

    # Physical tables NOT documented in NSAW
    n_not_nsaw = 0
    for tbl in phys_tables.values():
        ref = safe_dict(safe_dict(tbl).get("nsaw_claude_ref"))
        if ref.get("documented_in_nsaw") is False or ref.get("documented_in_nsaw") == "false":
            n_not_nsaw += 1

    print(f"  Workbooks          : {n_workbooks}")
    print(f"  Datasets           : {n_datasets}")
    print(f"  Dataflows          : {n_dataflows}")
    print(f"  Physical tables    : {n_phys}")
    print(f"  Lineage edges      : {n_edges}")
    print(f"  Datasets in_closure: {n_closure_ds}")
    print(f"  Dataflows in_closure: {n_closure_df}")
    print(f"  Physical tables not documented_in_nsaw: {n_not_nsaw}")

    # -----------------------------------------------------------------------
    # (h) v3: field_dictionary columns bottom-out (physical/upstream/flagged)
    # -----------------------------------------------------------------------
    print("\n[h] field_dictionary bottom-out (v3)")
    import glob as _g
    try:
        fdic = yaml.safe_load(open(KB_ROOT / "field_dictionary.yaml", encoding="utf-8")) or {}
    except Exception as ex:
        fdic = {}; warn(f"field_dictionary.yaml not loaded: {ex}")
    h_total = h_gap = 0
    for dsn, rec in safe_dict(fdic.get("datasets")).items():
        for c, e in safe_dict(safe_dict(rec).get("columns")).items():
            if not isinstance(e, dict):
                continue
            h_total += 1
            if not (e.get("physical_roots") or e.get("upstream_leaf_datasets")
                    or e.get("governance_flag") or e.get("source_note")):
                h_gap += 1
    print(f"  Columns: {h_total}; chưa bottom-out & chưa gắn cờ: {h_gap}")
    if h_gap:
        warn(f"{h_gap} field columns không có physical_roots/upstream và chưa gắn cờ (review)")

    # -----------------------------------------------------------------------
    # (i) v3: capability_map references resolve to dataset_catalog
    # -----------------------------------------------------------------------
    print("\n[i] capability_map references (v3)")
    try:
        cap = yaml.safe_load(open(KB_ROOT / "capability_map.yaml", encoding="utf-8")) or {}
    except Exception as ex:
        cap = {}; warn(f"capability_map.yaml not loaded: {ex}")
    i_bad = 0
    for idx in ("by_metric", "by_dimension"):
        for concept, dss in safe_dict(cap.get(idx)).items():
            for ds in (dss or []):
                if ds not in datasets:
                    err(f"capability_map.{idx}['{concept}'] tham chiếu dataset lạ: '{ds}'"); i_bad += 1
    for ds in safe_dict(cap.get("datasets")).keys():
        if ds not in datasets:
            err(f"capability_map.datasets có dataset lạ: '{ds}'"); i_bad += 1
    print(f"  capability_map dataset refs bad: {i_bad}")

    # -----------------------------------------------------------------------
    # (j) v3: no absolute money numbers cached (heuristic, WARN)
    # -----------------------------------------------------------------------
    print("\n[j] no-cached-number heuristic (v3)")
    import re as _re
    j_hits = 0
    for fn in ["QUICK_REFERENCE.md", "CONFLICTS_AND_OPEN_QUESTIONS.md",
               "live_query_recipes.md", "source_selection_playbook.md", "business_glossary.yaml"]:
        p = KB_ROOT / fn
        if not p.exists():
            continue
        for ln in open(p, encoding="utf-8"):
            if _re.search(r"\d+\s*tỷ", ln):  # VND "tỷ" value = likely a cached number
                warn(f"{fn}: nghi số tuyệt đối (tỷ): {ln.strip()[:80]}"); j_hits += 1
    print(f"  Dòng nghi cache số (tỷ): {j_hits}  (governance hardcoded constants được phép, nằm ngoài check này)")

    # -----------------------------------------------------------------------
    # (k) v3.1: no TODO placeholders in curated files; grain coverage
    # -----------------------------------------------------------------------
    print("\n[k] no-TODO + grain coverage (v3.1)")
    k_todo = 0
    for fn in ["field_dictionary.yaml", "business_glossary.yaml", "capability_map.yaml"]:
        p = KB_ROOT / fn
        if p.exists():
            c = open(p, encoding="utf-8").read().count("TODO")
            if c:
                err(f"{fn}: còn {c} 'TODO' placeholder"); k_todo += c
    # placeholder/heuristic grain count (WARN)
    try:
        dcat = yaml.safe_load(open(KB_ROOT / "dataset_catalog.yaml", encoding="utf-8")).get("datasets", {})
    except Exception:
        dcat = {}
    k_badgrain = sum(1 for r in dcat.values()
                     if isinstance(r, dict) and (not r.get("grain") or "May 20" in str(r.get("grain"))))
    print(f"  TODO placeholders: {k_todo}; datasets thiếu grain: {k_badgrain}")
    if k_badgrain:
        warn(f"{k_badgrain} dataset thiếu/placeholder grain")

    # -----------------------------------------------------------------------
    # (l) v3.2: ENCODING INTEGRITY — chặn U+FFFD / mojibake / non-UTF8
    # -----------------------------------------------------------------------
    print("\n[l] encoding integrity (v3.2)")
    import re as _re2, glob as _glob2
    _moji = _re2.compile(r"Ã[\x80-\xbf]|â€|á»|áº|Â[\x80-\xbf]")
    l_files = l_err = 0
    targets = (_glob2.glob(str(KB_ROOT / "*.yaml")) + _glob2.glob(str(KB_ROOT / "*.md"))
               + _glob2.glob(str(KB_ROOT / "fields" / "*.md")) + _glob2.glob(str(KB_ROOT / "external" / "*.md")))
    for p in targets:
        l_files += 1
        try:
            s = open(p, encoding="utf-8", errors="strict").read()
        except UnicodeDecodeError as ex:
            err(f"NON-UTF8 file: {os.path.basename(p)} ({ex})"); l_err += 1; continue
        if "�" in s:
            err(f"U+FFFD (ký tự hỏng �) trong {os.path.basename(p)}"); l_err += 1
        if _moji.search(s):
            err(f"mojibake nghi ngờ trong {os.path.basename(p)}"); l_err += 1
    print(f"  Quét {l_files} file curated; lỗi encoding: {l_err}")

    # -----------------------------------------------------------------------
    # Final verdict
    # -----------------------------------------------------------------------
    print("\n" + "=" * 70)
    print(f"RESULT: {len(errors)} ERROR(s), {len(warns)} WARN(s)")
    if errors:
        print("\nAll ERRORs:")
        for e in errors:
            print(f"  - {e}")
    if errors:
        print("\nValidation FAILED (ERRORs found).")
        sys.exit(1)
    else:
        print("Validation PASSED (no ERRORs).")
        sys.exit(0)


if __name__ == "__main__":
    main()
