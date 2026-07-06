# GENERATED-SUPPORT (pipeline tool — KHÔNG phải catalog GENERATED)
"""
merge_curated_fields.py — carry PROSE curated (grain, internal_joins_filters, _meta) từ
field_dictionary ĐỜI-TRƯỚC (prior committed) sang field_dictionary FRESH (vừa rebuild),
để tri-thức-người KHÔNG mất khi re-extract. Vá khe hở R-D2 cho field_dictionary
(sidecar dataflow_descriptions.yaml chỉ phủ mô-tả dataflow; grain/joins/_meta của
field_dictionary trước đây chưa survive rebuild → build_catalogs đặt TODO_P2).

Nguyên tắc:
- KHÔNG bịa: chỉ carry giá trị prior đã có (người-biên). Boilerplate db_dataset được
  DERIVE từ prior (chuỗi internal_joins_filters modal của các db_dataset), không hardcode.
- Residual db_dataset MỚI (không có prior): fill theo CONVENTION db_dataset của chính prior
  (grain modal = 'dim/lookup'; internal_joins_filters = boilerplate modal) + LOG để owner review.
- _meta: giữ prose prior, chỉ override extracted_live theo fresh.
- Bất kỳ TODO residual không convention-hoá được → giữ nguyên + LOG (fail validate ồn — INV-6).

Usage:
  python merge_curated_fields.py --prior <prior.yaml> --fresh <fresh.yaml> --out <out.yaml> [--json-report <r.json>]
"""
import sys, os, argparse, json, collections, copy

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import yaml
from build_catalogs import Dumper  # dùng CHÍNH dumper của pipeline → khớp style, không reflow

TODO = "TODO"
# field prose ở CẤP DATASET cần preserve/convention-fill
DS_PROSE_FIELDS = ("grain", "internal_joins_filters", "live_query_recipe")


def is_todo(v):
    return isinstance(v, str) and v.strip().startswith(TODO)


def modal_db_dataset_value(prior_ds, field):
    """Giá trị phổ biến nhất của <field> trong các db_dataset của prior (để convention-fill)."""
    ctr = collections.Counter()
    for ds, v in prior_ds.items():
        if isinstance(v, dict) and v.get("type") == "db_dataset":
            val = v.get(field)
            if isinstance(val, str) and not is_todo(val):
                ctr[val] += 1
    return ctr.most_common(1)[0][0] if ctr else None


def merge(prior, fresh):
    report = {"carried": [], "convention_filled": [], "residual_todo": [], "meta_preserved": False}
    result = copy.deepcopy(fresh)

    # --- _meta: giữ prose prior, override extracted_live theo fresh ---
    if isinstance(prior.get("_meta"), dict):
        fresh_live = (fresh.get("_meta") or {}).get("extracted_live")
        meta = copy.deepcopy(prior["_meta"])
        if fresh_live:
            meta["extracted_live"] = fresh_live
        result["_meta"] = meta
        report["meta_preserved"] = True

    p_ds = prior.get("datasets", {})
    boiler_ijf = modal_db_dataset_value(p_ds, "internal_joins_filters")
    modal_grain = modal_db_dataset_value(p_ds, "grain")  # thường 'dim/lookup'

    for ds, dv in result.get("datasets", {}).items():
        if not isinstance(dv, dict):
            continue
        p = p_ds.get(ds, {}) if isinstance(p_ds.get(ds), dict) else {}
        is_db = dv.get("type") == "db_dataset"
        # ----- dataset-level prose -----
        for f in DS_PROSE_FIELDS:
            if is_todo(dv.get(f)):
                pv = p.get(f)
                if isinstance(pv, str) and not is_todo(pv):
                    dv[f] = pv
                    report["carried"].append(f"{ds} :: {f}")
                elif is_db and f == "internal_joins_filters" and boiler_ijf:
                    dv[f] = boiler_ijf
                    report["convention_filled"].append(f"{ds} :: internal_joins_filters (db_dataset boilerplate)")
                elif is_db and f == "grain" and modal_grain:
                    dv[f] = modal_grain
                    report["convention_filled"].append(f"{ds} :: grain='{modal_grain}' (db_dataset modal — CẦN owner xác nhận)")
                else:
                    report["residual_todo"].append(f"{ds} :: {f}")
        # ----- column-level prose -----
        for col, cv in (dv.get("columns") or {}).items():
            if not isinstance(cv, dict):
                continue
            pc = (p.get("columns") or {}).get(col, {}) if isinstance(p.get("columns"), dict) else {}
            for f, val in list(cv.items()):
                if is_todo(val):
                    pv = pc.get(f)
                    if isinstance(pv, str) and not is_todo(pv):
                        cv[f] = pv
                        report["carried"].append(f"{ds} :: col[{col}] :: {f}")
                    else:
                        report["residual_todo"].append(f"{ds} :: col[{col}] :: {f}")
    return result, report


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prior", required=True)
    ap.add_argument("--fresh", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--json-report", default=None)
    a = ap.parse_args()
    with open(a.prior, encoding="utf-8") as f:
        prior = yaml.safe_load(f)
    with open(a.fresh, encoding="utf-8") as f:
        fresh = yaml.safe_load(f)
    result, report = merge(prior, fresh)
    with open(a.out, "w", encoding="utf-8") as f:
        f.write(yaml.dump(result, Dumper=Dumper, allow_unicode=True, sort_keys=False, width=120))
    print(f"carried={len(report['carried'])} convention_filled={len(report['convention_filled'])} "
          f"residual_todo={len(report['residual_todo'])} meta_preserved={report['meta_preserved']}")
    if report["convention_filled"]:
        print("-- convention_filled --")
        for x in report["convention_filled"]:
            print("  ", x)
    if report["residual_todo"]:
        print("-- RESIDUAL TODO (fail validate) --")
        for x in report["residual_todo"]:
            print("  ", x)
    if a.json_report:
        with open(a.json_report, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
