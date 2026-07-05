# -*- coding: utf-8 -*-
"""
Parser DETERMINISTIC: raw projects/json -> skeleton.json (xương sống độ-phủ).
Liệt kê ĐẦY ĐỦ canvas -> viz -> cột (col_id, display, expression, sources, format, role).
KHÔNG dùng AI, KHÔNG dùng now() (để re-parse cho kết quả y hệt -> test 'skeleton tất định').

Dùng: python build_skeleton.py <projects.json> <out_skeleton.json> "<Workbook name>"
"""
import json, sys, re, os, datetime


def load(p):
    j = json.loads(open(p, encoding="utf-8").read())
    return json.loads(j) if isinstance(j, str) else j


def clean_html(s):
    if not s:
        return s
    s = re.sub(r"<[^>]+>", "", s)
    s = (s.replace("&nbsp;", " ").replace("&amp;", "&").replace("&quot;", '"')
           .replace("​", "").replace("﻿", ""))
    return re.sub(r"\s+", " ", s).strip()


SRC_RE = re.compile(r"XSA\('([^']+)'\.'([^']+)'\)\.\"Columns\"\.\"﻿?([^\"]+)\"")


def main():
    src = sys.argv[1]
    out_path = sys.argv[2]
    wbname = sys.argv[3] if len(sys.argv) > 3 else None
    j = load(src)

    colmap = {}
    for c in j.get("criteria", {}).get("columns", {}).get("children", []):
        colmap[c["columnID"]] = (c.get("columnFormula", {}).get("expr", {}) or {}).get("expression")

    views_root = j.get("views", {}).get("children", [])
    canvases = [v for v in views_root if v.get("type") == "saw:canvas"]
    pviews = {v["viewName"]: v for v in views_root if v.get("type") == "saw:pluginView"}

    layouts = {}
    for lay in j.get("layouts", {}).get("children", []):
        vlist = []
        def walk(n):
            if isinstance(n, dict):
                c = n.get("content")
                if isinstance(c, dict) and c.get("viewName"):
                    vlist.append(c["viewName"])
                for ch in n.get("children", []) or []:
                    walk(ch)
        walk(lay)
        layouts[lay.get("name")] = vlist

    def headers_of(v):
        grid = v.get("viewConfig", {}).get("settings", {}).get("viz:grid", {})
        return {k.replace("columnHeaderProperty_", ""): val.get("headerText")
                for k, val in grid.items() if k.startswith("columnHeaderProperty_") and isinstance(val, dict)}

    def fmts_of(v):
        nf = v.get("viewConfig", {}).get("settings", {}).get("viz:chart", {})
        out = {}
        for k, val in nf.items():
            if k.startswith("bidvtchart_number_format_") and isinstance(val, dict):
                out[k.replace("bidvtchart_number_format_", "")] = f"{val.get('style')}/{val.get('maximumFractionDigits')}dp"
        return out

    def col_entry(cid, headers, fmts, role):
        expr = colmap.get(cid)
        sources = sorted({f"{m.group(2)}.{m.group(3)}" for m in SRC_RE.finditer(expr or "")})
        return {"col_id": cid, "display": headers.get(cid) or cid,
                "header_override": headers.get(cid), "expression": expr,
                "sources": sources or None, "number_format": fmts.get(cid), "role": role}

    def viz_entry(vn):
        v = pviews.get(vn)
        if not v:
            return None
        pt = v.get("pluginType", "")
        cap = clean_html(v.get("viewCaption", {}).get("caption", {}).get("text"))
        headers, fmts = headers_of(v), fmts_of(v)
        kind = ("pivot_summary" if "pivot" in pt else "table" if pt.endswith(".table")
                else "filter" if "canvasfilterviz" in pt or "listbox" in pt else "chart")
        cols, seen = [], set()
        for dm in v.get("dataModels", {}).get("children", []):
            for ed in dm.get("edges", {}).get("children", []):
                axis = ed.get("axis")
                for L in ed.get("edgeLayers", {}).get("children", []) or []:
                    cid = L.get("columnID")
                    if cid and cid not in seen:
                        seen.add(cid)
                        role = ("row_dim" if axis == "row" else "col_dim" if axis == "column"
                                else "filter_dim" if kind == "filter" else axis)
                        cols.append(col_entry(cid, headers, fmts, role))
            for L in dm.get("measuresList", {}).get("children", []) or []:
                cid = L.get("columnID")
                if cid and cid not in seen:
                    seen.add(cid)
                    cols.append(col_entry(cid, headers, fmts, "measure"))
        return {"viz": vn, "pluginType": pt, "title": cap, "kind": kind,
                "n_columns": len(cols), "columns": cols}

    skel = {"workbook": wbname, "source_file": os.path.basename(src),
            "extracted_at": datetime.datetime.utcfromtimestamp(os.path.getmtime(src)).isoformat() + "Z",
            "canvases": []}
    for cv in canvases:
        rl = cv.get("rootLayoutName")
        vizzes = [x for x in (viz_entry(vn) for vn in layouts.get(rl, [])) if x]
        skel["canvases"].append({
            "canvas": clean_html(cv.get("viewCaption", {}).get("caption", {}).get("text")),
            "canvas_id": cv["viewName"], "layout": rl, "n_viz": len(vizzes), "vizzes": vizzes})

    json.dump(skel, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    tot = sum(vz["n_columns"] for cv in skel["canvases"] for vz in cv["vizzes"])
    print(f"== {wbname} ==  {len(skel['canvases'])} canvas · "
          f"{sum(cv['n_viz'] for cv in skel['canvases'])} viz · {tot} cột (gồm filter/dim)")
    for cv in skel["canvases"]:
        print(f"  [{cv['canvas']}]  ({cv['n_viz']} viz)")
        for vz in cv["vizzes"]:
            print(f"     {vz['viz']:9} {vz['kind']:14} cols={vz['n_columns']:2}  '{vz['title']}'")
    print("-> wrote", out_path)


if __name__ == "__main__":
    main()
