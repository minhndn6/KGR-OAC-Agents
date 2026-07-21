"""
trace_field.py — trace field/node lineage in the OAC Knowledge Base.

Usage:
    python trace_field.py "<substring>"

Finds all nodes in lineage_graph.yaml whose name contains <substring>
(case-insensitive) and prints:
  - DOWNSTREAM: walks edges FROM the matched node toward physical: terminals.
  - UPSTREAM: for dataset: and physical: nodes, walks edges TO the node
    (who uses it).

Handles cycles. Prints readable indented trees.
"""
import sys
import os
from pathlib import Path
from typing import Dict, List, Set

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml not installed. Run: pip install pyyaml")
    sys.exit(1)

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

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
LINEAGE_FILE = KB_ROOT / "lineage_graph.yaml"


def load_graph() -> dict:
    if not LINEAGE_FILE.exists():
        print(f"ERROR: lineage file not found: {LINEAGE_FILE}")
        sys.exit(1)
    with open(LINEAGE_FILE, encoding="utf-8") as f:
        return yaml.safe_load(f)


def build_adjacency(edges: list):
    """Return forward (from->to) and reverse (to->from) adjacency dicts."""
    fwd: Dict[str, List[str]] = {}
    rev: Dict[str, List[str]] = {}
    for e in (edges or []):
        src, dst = e.get("from", ""), e.get("to", "")
        if not src or not dst:
            continue
        fwd.setdefault(src, []).append(dst)
        rev.setdefault(dst, []).append(src)
    return fwd, rev


def find_matches(all_nodes: Set[str], substring: str) -> List[str]:
    sub_lower = substring.lower()
    return sorted(n for n in all_nodes if sub_lower in n.lower())


import re as _re

_GLOSSARY_CACHE = None
def _glossary_codes():
    """(pnl_waterfall_codes, MANDATORY_DISCLOSURE) từ business_glossary.yaml — cache 1 lần."""
    global _GLOSSARY_CACHE
    if _GLOSSARY_CACHE is None:
        try:
            g = yaml.safe_load(open(KB_ROOT / "business_glossary.yaml", encoding="utf-8")) or {}
        except Exception:
            g = {}
        _GLOSSARY_CACHE = ((g.get("pnl_waterfall_codes") or {}),
                           ((g.get("_meta") or {}).get("MANDATORY_DISCLOSURE") or "").strip())
    return _GLOSSARY_CACHE

_ESTIMATE_BASES = {"aop_estimate", "hardcoded_rate", "derived_mixed"}
def _disclosure_for(col):
    """Cảnh báo governance cho 1 cột P&L (a-code) dựa trên business_glossary.
    Bịt khoảng trống: field_dictionary chỉ gắn governance_flag cho a10; mọi dòng
    ước tính-AOP / số-cứng / lợi nhuận-disclosure khác (a6-a9, a12-a21) trước đây
    KHÔNG hiện cảnh báo khi trace. Đây là disclosure GR1/GR3 lấy thẳng từ glossary."""
    m = _re.match(r"(a\d+)", str(col).strip())
    if not m:
        return None
    codes, mandatory = _glossary_codes()
    info = codes.get(m.group(1))
    if not isinstance(info, dict):
        return None
    if info.get("basis") in _ESTIMATE_BASES or info.get("governance") or info.get("disclosure_required"):
        parts = [str(info["governance"])] if info.get("governance") else []
        if mandatory:
            parts.append(mandatory)
        return " | ".join(parts) or "ƯỚC TÍNH theo AOP / số cứng — xem governance_register.md"
    return None


def fd_search(substring: str):
    """Fallback: search field_dictionary.yaml columns (internal dataflow columns)."""
    fp = KB_ROOT / "field_dictionary.yaml"
    if not fp.exists():
        print("  (field_dictionary.yaml không có)"); return
    fd = yaml.safe_load(open(fp, encoding="utf-8")) or {}
    sub = substring.lower(); hits = 0
    for dsn, rec in (fd.get("datasets") or {}).items():
        for col, e in ((rec or {}).get("columns") or {}).items():
            if sub in col.lower() and isinstance(e, dict):
                hits += 1
                print("=" * 70)
                print(f"{dsn} . {col}")
                if e.get("direct_formula"): print(f"  formula: {e['direct_formula']}")
                # GR1/GR3 disclosure — hiện TRƯỚC physical_roots để không bị che bởi danh
                # sách bảng vật lý thật (vốn làm field ước tính trông như có gốc đầy đủ).
                _disc = _disclosure_for(col)
                if _disc: print(f"  ⚠️ DISCLOSURE (GR1/GR3): {_disc}")
                if e.get("physical_roots"): print(f"  physical_roots: {e['physical_roots']}")
                if e.get("non_physical_roots"): print(f"  non_physical_roots: {e['non_physical_roots']}")
                if e.get("filters"): print(f"  filters: {e['filters'][:4]}")
                if e.get("governance_flag"): print(f"  ⚠️ {e['governance_flag']}")
                if e.get("derivation"): print("  derivation:\n" + "\n".join("    "+l for l in e['derivation'].splitlines()[:14]))
                print()
    if not hits:
        print(f"  Không thấy cột chứa '{substring}'. Thử business_glossary.yaml / fields/*.md.")


def print_tree(node: str, adj: Dict[str, List[str]], visited: Set[str],
               indent: int = 0, direction_label: str = ""):
    prefix = "  " * indent
    tag = f"  [{direction_label}]" if direction_label else ""
    cycle_note = "  *** CYCLE ***" if node in visited else ""
    print(f"{prefix}{node}{tag}{cycle_note}")
    if node in visited:
        return
    visited = visited | {node}  # immutable copy per branch
    for neighbor in adj.get(node, []):
        print_tree(neighbor, adj, visited, indent + 1)


def collect_all_nodes(edges: list) -> Set[str]:
    nodes: Set[str] = set()
    for e in (edges or []):
        nodes.add(e.get("from", ""))
        nodes.add(e.get("to", ""))
    nodes.discard("")
    return nodes


def main():
    if len(sys.argv) < 2:
        print("Usage: python trace_field.py \"<substring>\"")
        sys.exit(1)

    substring = sys.argv[1]
    graph = load_graph()
    edges = graph.get("edges", [])
    all_nodes = collect_all_nodes(edges)
    fwd, rev = build_adjacency(edges)

    matches = find_matches(all_nodes, substring)
    if not matches:
        print(f"No lineage_graph nodes for '{substring}'. Tìm trong field_dictionary (cột nội bộ dataflow)...\n")
        fd_search(substring)
        sys.exit(0)

    print(f"Found {len(matches)} matching node(s) for '{substring}':\n")

    for node in matches:
        print("=" * 70)
        print(f"NODE: {node}")

        node_type = node.split(":")[0] if ":" in node else ""

        # Downstream (toward physical terminals)
        if node in fwd or node_type == "workbook":
            print("\n  [DOWNSTREAM — toward physical tables]")
            visited: Set[str] = set()
            for child in fwd.get(node, []):
                print_tree(child, fwd, visited | {node}, indent=2)
            if not fwd.get(node):
                print("    (no downstream edges)")

        # Upstream (who feeds this node / who uses it)
        if node_type in ("dataset", "physical", "dataflow"):
            print("\n  [UPSTREAM — who feeds / uses this node]")
            parents = rev.get(node, [])
            if parents:
                visited2: Set[str] = set()
                for parent in parents:
                    print_tree(parent, rev, visited2 | {node}, indent=2)
            else:
                print("    (no upstream edges — this may be a root source)")

        print()


if __name__ == "__main__":
    main()
