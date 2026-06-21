#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""kb_route — "tri thức loại X ghi vào ĐÂU và NHƯ THẾ NÀO?" (D4/D6, owner goal #1: chống chồng chéo/rác/sai cấu trúc).
Bất kỳ AI nào gọi 1 lệnh là biết đích hợp lệ — hết "đoán".

Usage:
  python kb_route.py classify --type <loại>     # đích + write_via + forbidden + validate + gate
  python kb_route.py check-path <file>          # file này thuộc loại gì, sửa kiểu gì
  python kb_route.py list                        # liệt kê loại

Exit: 0 ok · 3 type lạ (KHÔNG misroute âm thầm) · 2 sai cú pháp.
"""
import sys, json, argparse

try: sys.stdout.reconfigure(encoding="utf-8")   # an toàn console cp1252 (Windows)
except Exception: pass

_VAL_STRUCT = ["validate_kb.py", "raw/qa_full.py"]

def _gen(target, forbidden, gate, note):
    return {"kind": "GENERATED", "target": target, "write_via": "rebuild",
            "forbidden": forbidden, "validate": _VAL_STRUCT, "gate": gate, "note": note}

def _curated(target, gate, note):
    return {"kind": "CURATED", "target": target, "write_via": "direct-edit",
            "forbidden": "đừng để builder ghi đè (không phải file sinh ra)", "validate": ["validate_kb.py"],
            "gate": gate, "note": note}

ROUTES = {
    # ── Cấu trúc (GENERATED): SỬA NGUỒN rồi REBUILD, KHÔNG sửa tay catalog ──
    "new_dataset":  _gen("raw/ staging extract → rebuild (raw/REBUILD.md)", "sửa tay dataset_catalog.yaml",
                         "rebuild SHA + validate_kb/qa_full PASS", "Re-extract dataset rồi build_catalogs.py."),
    "new_dataflow": _gen("raw/ staging extract → rebuild", "sửa tay dataflow_catalog.yaml",
                         "rebuild SHA + qa PASS", "Re-extract dataflow def rồi rebuild."),
    "new_field":    _gen("raw/ → field_dict_build.py (rebuild)", "sửa tay field_dictionary.yaml / fields/*.md",
                         "rebuild SHA + qa PASS", "Field sinh ra từ resolver; sửa nguồn def."),
    "physical_table": _gen("raw/ → rebuild physical_table_catalog", "sửa tay physical_table_catalog.yaml",
                         "rebuild SHA + (verify_live nếu probe được)", "Bảng vật lý suy từ dataflow def/flowSQL."),
    "fact":         _gen("raw/ → rebuild catalog tương ứng", "sửa tay file catalog GENERATED",
                         "rebuild SHA + qa PASS", "Fact cấu trúc PHẢI qua rebuild deterministic, không patch YAML."),
    "formula_correction": _gen("sửa def dataflow nguồn → rebuild field_dictionary", "sửa tay công thức trong field_dictionary.yaml",
                         "bằng chứng LIVE (executePreview/flowSQL) HOẶC rebuild SHA", "Công thức sai = sửa ở dataflow nguồn rồi rebuild."),
    # ── Ngữ nghĩa người viết (CURATED): sửa trực tiếp + cổng theo loại ──
    "glossary_term": _curated("business_glossary.yaml", "attested_by (vai owner) + nguồn định nghĩa; KHÔNG auto",
                         "Không kiểm-live-được → cần người xác nhận, không để LLM tự promote."),
    "convention":   _curated("CONVENTIONS.md / source_selection_playbook.md", "attested_by + nơi quy ước được ghi; KHÔNG auto",
                         "Quy ước nghiệp vụ/vận hành — second-agent KHÔNG đủ cho claim ngữ nghĩa."),
    "governance_item": _curated("governance_register.md", "owner/CFO KÝ + link GR; KHÔNG auto, KHÔNG second-agent",
                         "Blast radius cao (chạm P&L) → bắt buộc người ký (GR1–GR7)."),
    # ── Khác ──
    "gap":   {"kind": "OPEN_QUESTION", "target": "CONFLICTS_AND_OPEN_QUESTIONS.md (+ learn.py add gap)",
              "write_via": "open-question", "forbidden": "promote 'gap' thành fact trong KB",
              "validate": ["validate_kb.py"], "gate": "chuyển owner; KHÔNG thành fact", "note": "Gap là câu hỏi mở, không phải tri thức khẳng định."},
    "drift": {"kind": "LOG", "target": "drift store (Phase 3) / learn.py add drift", "write_via": "drift.py upsert",
              "forbidden": "append thô mỗi lần probe (gây bão)", "validate": [], "gate": "auto-ack sau ≥2 lần; incorporate qua rebuild",
              "note": "LỌC timestamp hợp lệ trước khi so (99/203 datasource thiếu ts — L0010); dedup theo drift_key."},
    "correction": {"kind": "LOG", "target": "learnings/log.jsonl (learn.py add correction) → promote", "write_via": "learn.py",
              "forbidden": "ghi đè fact cũ không audit", "validate": ["validate_kb.py"], "gate": "provenance người/owner; mâu thuẫn → supersede",
              "note": "Sửa từ người có thẩm quyền; nếu trái fact cũ → supersede có audit."},
    "lesson": {"kind": "LOG", "target": "learnings/log.jsonl (learn.py add lesson)", "write_via": "learn.py",
              "forbidden": "coi lesson vận hành như fact cấu trúc", "validate": [], "gate": "incorporated_into pointer; second-agent OK",
              "note": "Bài học vận hành/AI, blast radius thấp."},
    "qa":    {"kind": "LOG", "target": "learnings/log.jsonl (learn.py add qa)", "write_via": "learn.py",
              "forbidden": "", "validate": [], "gate": "review", "note": "Ghi nhận kết quả QA/kiểm thử."},
}

def classify(ktype):
    return ROUTES.get(ktype)

# ── check-path: file đang xét thuộc loại nào (v1 theo tên; P2.1 sẽ đổi sang banner) ──
_GENERATED_YAML = {"dataset_catalog.yaml", "dataflow_catalog.yaml", "workbook_catalog.yaml",
                   "physical_table_catalog.yaml", "lineage_graph.yaml", "field_dictionary.yaml", "capability_map.yaml"}
_CURATED = {"business_glossary.yaml", "governance_register.md", "live_query_recipes.md", "source_selection_playbook.md",
            "conflicts_and_open_questions.md", "conventions.md", "how_to_trace_a_field.md", "knowledge_index.md",
            "quick_reference.md", "changelog.md", "archive_recommendations.md", "owner_todo.md", "learning.md"}

def _fallback_kind(posix):
    base = posix.rsplit("/", 1)[-1]; low = base.lower()
    if "learnings/" in posix or base == "log.jsonl": return "LOG"
    if base in _GENERATED_YAML: return "GENERATED"
    if ("/fields/" in "/" + posix or posix.startswith("fields/")) and low.endswith(".md"):
        return "CURATED" if base.startswith("_") else "GENERATED"
    if low in _CURATED: return "CURATED"
    return "UNKNOWN"

def check_path(path):
    """Ưu tiên kb_kinds (authoritative theo kinds.yaml); fallback heuristic nếu kinds không nạp được."""
    posix = str(path).replace("\\", "/")
    kind = None
    try:
        import kb_kinds
        kind = kb_kinds.classify(posix)
    except Exception:
        kind = None
    if not kind or kind == "UNKNOWN":
        fb = _fallback_kind(posix)
        kind = fb if fb != "UNKNOWN" else (kind or "UNKNOWN")
    wv = {"GENERATED": "rebuild", "CURATED": "direct-edit", "LOG": "learn.py (append-only)"}.get(kind, "?")
    note = {"GENERATED": "Sinh ra; ĐỪNG sửa tay — sửa nguồn rồi rebuild (raw/REBUILD.md).",
            "CURATED": "File người viết; sửa trực tiếp + validate.",
            "LOG": "Append-only; không sửa record cũ.",
            "UNKNOWN": "Chưa phân loại — thêm vào kinds.yaml."}.get(kind, "")
    return {"path": posix, "kind": kind, "write_via": wv, "note": note}

def cli(argv):
    ap = argparse.ArgumentParser(prog="kb_route", add_help=True)
    sub = ap.add_subparsers(dest="cmd")
    c = sub.add_parser("classify"); c.add_argument("--type", required=True); c.add_argument("--format", default="json")
    cp = sub.add_parser("check-path"); cp.add_argument("path")
    sub.add_parser("list")
    try:
        ns = ap.parse_args(argv)
    except SystemExit:
        return 2
    if ns.cmd == "classify":
        r = classify(ns.type)
        if r is None:
            print(json.dumps({"error": "unknown type", "type": ns.type, "known": sorted(ROUTES)}, ensure_ascii=False))
            return 3
        print(json.dumps({"type": ns.type, **r}, ensure_ascii=False, indent=2)); return 0
    if ns.cmd == "check-path":
        print(json.dumps(check_path(ns.path), ensure_ascii=False, indent=2)); return 0
    if ns.cmd == "list":
        print(json.dumps(sorted(ROUTES), ensure_ascii=False)); return 0
    ap.print_help(); return 2

if __name__ == "__main__":
    sys.exit(cli(sys.argv[1:]))
