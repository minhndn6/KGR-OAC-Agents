#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""coverage_report — trần-autonomy của data-brain (R-H1, Council Sprint-8).

Đọc capability_map.yaml + dataset_catalog.yaml + workbook_catalog.yaml + field_dictionary.yaml →
báo cáo: bao nhiêu dataset/subject-area ĐƯỢC map trong data-brain vs TỔNG (universe = dataset_catalog)
→ % coverage + LIST vùng CHƯA map. Owner nhìn vào biết "dựng workbook trên mảng data chưa đụng" =
vào vùng MÙ (chưa có lineage/field-dict → builder-agent 0-hit).

Read-only, THUẦN (compute_coverage tiêm-được để test hermetic) + load_and_compute() đọc catalog thật.
KHÔNG gọi oac-native, KHÔNG ghi gì. compute_coverage() = pure function.

Chạy CLI: PYTHONUTF8=1 python kb_lifecycle/tools/coverage_report.py   # in JSON báo cáo coverage
"""
import sys, os, json
from pathlib import Path

try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

HERE = Path(__file__).resolve()


def _ds_names(catalog):
    """Trích set tên dataset từ 1 catalog dict có shape {datasets: {name: {...}}}."""
    if not isinstance(catalog, dict):
        return set()
    d = catalog.get("datasets")
    if isinstance(d, dict):
        return set(d.keys())
    if isinstance(d, list):
        # list các entry có 'name'
        out = set()
        for e in d:
            if isinstance(e, dict) and e.get("name"):
                out.add(e["name"])
        return out
    return set()


def _pct(num, den):
    if not den:
        return 0.0
    return round(100.0 * num / den, 1)


def compute_coverage(capability_map, dataset_catalog, workbook_catalog, field_dictionary):
    """PURE. Nhận 4 catalog dict (đã parse) → báo cáo coverage.

    Universe (TỔNG) = tên dataset trong dataset_catalog (danh mục đầy đủ enumerate-được).
    - mapped_capability = giao với capability_map.datasets (data-brain có 'lấy X ở đâu').
    - mapped_field_dict = giao với field_dictionary.datasets (có lineage cấp-cột).
    - missing_* = universe − mapped (VÙNG MÙ, list ra để owner biết).
    Workbooks: đếm workbook + tổng/used datasource (từ n_datasources / n_datasources_used).
    An toàn ZeroDivision khi universe rỗng.
    """
    universe = _ds_names(dataset_catalog)
    cap = _ds_names(capability_map)
    fd = _ds_names(field_dictionary)

    mapped_cap = universe & cap
    mapped_fd = universe & fd
    missing_cap = sorted(universe - cap)
    missing_fd = sorted(universe - fd)
    # dataset xuất hiện trong data-brain nhưng KHÔNG có trong dataset_catalog (zombie/tên lệch)
    orphan_cap = sorted(cap - universe)

    total = len(universe)
    ds_report = {
        "total": total,
        "mapped_capability": len(mapped_cap),
        "pct_capability": _pct(len(mapped_cap), total),
        "missing_capability": missing_cap,
        "mapped_field_dict": len(mapped_fd),
        "pct_field_dict": _pct(len(mapped_fd), total),
        "missing_field_dict": missing_fd,
        "orphan_capability": orphan_cap,
    }

    # workbooks
    wbs = {}
    if isinstance(workbook_catalog, dict):
        wbs = workbook_catalog.get("workbooks") or {}
    if not isinstance(wbs, dict):
        wbs = {}
    ds_total = ds_used = 0
    per_wb = {}
    for name, w in wbs.items():
        if not isinstance(w, dict):
            continue
        nt = w.get("n_datasources") or 0
        nu = w.get("n_datasources_used") or 0
        ds_total += int(nt)
        ds_used += int(nu)
        per_wb[name] = {"n_datasources": nt, "n_datasources_used": nu,
                        "n_canvases": w.get("n_canvases")}
    wb_report = {
        "total": len(wbs),
        "datasources_total": ds_total,
        "datasources_used": ds_used,
        "pct_datasources_used": _pct(ds_used, ds_total),
        "per_workbook": per_wb,
    }

    return {
        "datasets": ds_report,
        "workbooks": wb_report,
        "note": ("coverage = tỷ lệ dataset TRONG data-brain (capability_map/field_dictionary) so với "
                 "universe (dataset_catalog). missing_* = VÙNG MÙ: dựng wb ở đó = builder 0-hit lineage."),
    }


# ── đọc catalog thật ─────────────────────────────────────────────────────────
def _resolve_kb_root(kb_root=None):
    if kb_root:
        return Path(kb_root)
    # thử kb_paths.resolve_kb_root
    try:
        sys.path.insert(0, str(HERE.parent))
        import kb_paths as KP
        return Path(KP.resolve_kb_root(start_file=str(HERE)))
    except Exception:
        # fallback: đi lên tìm thư mục chứa dataset_catalog.yaml
        for anc in (HERE, *HERE.parents):
            if (anc / "dataset_catalog.yaml").is_file():
                return anc
        return HERE.parents[2]  # OAC-Knowledge


def _load_yaml(p):
    try:
        import yaml
        return yaml.safe_load(Path(p).read_text(encoding="utf-8", errors="replace")) or {}
    except Exception:
        return {}


def load_and_compute(kb_root=None):
    """Đọc 4 catalog thật từ KB root → compute_coverage. Read-only."""
    root = _resolve_kb_root(kb_root)
    cap = _load_yaml(root / "capability_map.yaml")
    dsc = _load_yaml(root / "dataset_catalog.yaml")
    wbc = _load_yaml(root / "workbook_catalog.yaml")
    fd = _load_yaml(root / "field_dictionary.yaml")
    rep = compute_coverage(cap, dsc, wbc, fd)
    rep["kb_root"] = str(root)
    return rep


def coverage_summary(kb_root=None):
    """Bản GỌN cho doctor (thông tin, KHÔNG lật STATUS): pct + count vùng mù."""
    try:
        rep = load_and_compute(kb_root)
    except Exception as e:
        return {"status": "UNKNOWN", "error": str(e)}
    ds = rep.get("datasets", {})
    wb = rep.get("workbooks", {})
    return {
        "datasets_total": ds.get("total"),
        "datasets_mapped_capability": ds.get("mapped_capability"),
        "pct_capability": ds.get("pct_capability"),
        "pct_field_dict": ds.get("pct_field_dict"),
        "blind_spots_capability": len(ds.get("missing_capability") or []),
        "workbooks_total": wb.get("total"),
        "hint": ("dataset chưa map (missing_capability) = vùng mù cho builder-agent; "
                 "chạy `coverage_report.py` xem list đầy đủ"),
    }


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    kb = None
    for i, a in enumerate(argv):
        if a in ("--kb-root", "--kb") and i + 1 < len(argv):
            kb = argv[i + 1]
    rep = load_and_compute(kb)
    print(json.dumps(rep, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
