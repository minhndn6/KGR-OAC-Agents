# -*- coding: utf-8 -*-
"""P3a: capability_map.yaml + per-dataset field dossiers (fields/*.md) from field_dictionary."""
import os, re, yaml
from collections import OrderedDict, defaultdict

OUT=os.environ.get("OAC_KB_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # raw -> OAC-Knowledge
fd=yaml.safe_load(open(os.path.join(OUT,"field_dictionary.yaml"),encoding="utf-8"))
dc=yaml.safe_load(open(os.path.join(OUT,"dataset_catalog.yaml"),encoding="utf-8"))["datasets"]

# concept keyword maps (Vietnamese + English) on column names
DIM_CONCEPTS={
 "chuoi (chain)": ["chuỗi","chain"],
 "kenh (channel/SC)": ["kênh","channel"," sc"],
 "nganh (class)": ["ngành","class","prodcatg"],
 "model": ["model"],
 "nhom_sp (product group)": ["nhóm sp","prodgroup","nhóm sản"],
 "asm": ["asm"],
 "don_vi (subsidiary)": ["đơn vị","subsidiary","subsidi"],
 "tinh (province)": ["tỉnh","province","geo_ten"],
 "khach (customer)": ["khách","customer"],
 "xanh_do": ["xanh","đỏ","nhomxanhdo","xd"],
 "thoi_gian (time)": ["trandate","period","ngày","date","month","tuần","week","asofdate","posting"],
 "metric_code (P&L chỉ tiêu)": ["metric_code","chỉ tiêu","metric_name"],
}
MET_CONCEPTS={
 "revenue (doanh thu/doanh số)": ["doanh thu","doanh số","revenue","net_amount","base_revenue"],
 "cogs (giá vốn)": ["giá vốn","gía vốn","cogs","gvmt","gvtk"],
 "gross_profit (LN gộp)": ["ln gộp","lãi gộp","gross","%gp","gp ròng","gp%"],
 "ckkm (chiết khấu KM)": ["ckkm","cpkm","khuyến mãi","trade_promotion","chiết khấu"],
 "sp_moi (sản phẩm mới)": ["sp mới","sp_moi","new-product","new product","spmoi"],
 "aop (kế hoạch)": ["aop","kế hoạch","ke_hoach"],
 "sfc (ước tính)": ["sfc","ước tính","sl_thuc_te","sl_ke_hoach"],
 "quantity (sản lượng)": ["quantity","sản lượng"," sl ","số lượng"],
 "profit (lợi nhuận)": ["lợi nhuận","lngiao","lnst","profit","a9","a11","a13","a20"],
}
def concepts(name, mp):
    n=(name or "").lower(); hit=[]
    for c,kws in mp.items():
        if any(k in n for k in kws): hit.append(c)
    return hit

def is_measure(col, e):
    if not isinstance(e,dict): return False
    if e.get("aggregation"): return True
    nm=col.lower()
    if any(k in nm for k in ["doanh","ln ","lãi","%","gp","ckkm","cp ","amount","quantity","số","giá vốn","revenue","sum","aop","sfc","tỷ trọng","sl_"]): return True
    # numeric physical roots
    return False

# ---- per dataset capability + dossiers ----
os.makedirs(os.path.join(OUT,"fields"),exist_ok=True)
cap_ds=OrderedDict()
by_dim=defaultdict(set); by_met=defaultdict(set)

def safe(n): return re.sub(r'[^0-9A-Za-z_]+','_',n).strip('_')

idx_lines=["# Field dossiers — giải thích mọi field theo dataset","",
           "Mỗi file `fields/<dataset>.md` liệt kê từng cột: công thức trực tiếp → bung tới bảng vật lý + filter/join + grain. NO số (lấy live).",""]

for dsname,rec in fd["datasets"].items():
    cols=rec.get("columns") or {}
    dims=[]; mets=[]
    for c,e in cols.items():
        (mets if is_measure(c,e) else dims).append(c)
    # also db-dataset columns_used_by_workbooks
    if rec.get("type")=="db_dataset":
        for c in (rec.get("columns_used_by_workbooks") or []):
            (mets if is_measure(c,{}) else dims).append(c)
    grain=rec.get("grain") or dc.get(dsname,{}).get("grain")
    cap_ds[dsname]=OrderedDict([("type",rec.get("type")),("grain",grain),
        ("dimensions",sorted(set(dims))),("measures",sorted(set(mets))),
        ("produced_by",rec.get("producer_flow")),("used_by_workbooks",dc.get(dsname,{}).get("used_by_workbooks"))])
    # concept indices
    for c in set(dims):
        for con in concepts(c,DIM_CONCEPTS): by_dim[con].add(dsname)
    for c in set(mets):
        for con in concepts(c,MET_CONCEPTS): by_met[con].add(dsname)
    # dossier md
    L=[f"# {dsname}","",f"- **type**: {rec.get('type')}",f"- **grain**: {grain}  ({rec.get('grain_source','')})",
       f"- **producer_flow**: {rec.get('producer_flow','')}",
       f"- **used_by_workbooks**: {dc.get(dsname,{}).get('used_by_workbooks')}",
       f"- **physical_tables**: {rec.get('physical_tables_composed') or list((rec.get('physical_tables') or {}).keys())}",""]
    if rec.get("type")=="db_dataset":
        L.append(f"> {rec.get('internal_joins_filters','')}")
        L.append("")
    L.append("## Cột")
    for c in sorted(cols):
        e=cols[c]
        if not isinstance(e,dict): continue
        L.append(f"### {c}")
        if e.get("direct_formula"): L.append(f"- formula: `{e['direct_formula']}`")
        if e.get("aggregation"): L.append(f"- aggregation: {e['aggregation']}")
        if e.get("physical_roots"): L.append(f"- physical_roots: {e['physical_roots']}")
        if e.get("upstream_leaf_datasets"): L.append(f"- upstream: {e['upstream_leaf_datasets']}")
        if e.get("filters"): L.append(f"- filters: {e['filters']}")
        if e.get("joins"): L.append(f"- joins: {e['joins']}")
        if e.get("governance_flag"): L.append(f"- ⚠️ {e['governance_flag']} ({e.get('hardcoded_values_sample')})")
        if e.get("shown_as"): L.append(f"- shown_as: {[s['field']+' @'+s['workbook'] for s in e['shown_as']][:6]}")
        L.append("")
    fn=os.path.join(OUT,"fields",safe(dsname)+".md")
    open(fn,"w",encoding="utf-8").write("\n".join(L))
    idx_lines.append(f"- [{dsname}](fields/{safe(dsname)}.md) — {rec.get('type')}, grain: {grain}")

open(os.path.join(OUT,"fields","_INDEX.md"),"w",encoding="utf-8").write("\n".join(idx_lines))

cap=OrderedDict()
cap["_meta"]={"purpose":"Tra nhanh: metric/dimension nào lấy được ở dataset nào, grain nào. Dùng khi builder hỏi 'cần X theo Y lấy đâu'.",
 "extracted_live":"2026-06-20","note":"NO số. Authoritative khi trùng: OAC>NSAW; BC(báo cáo)>DB(dashboard)."}
cap["by_dimension"]={k:sorted(v) for k,v in sorted(by_dim.items())}
cap["by_metric"]={k:sorted(v) for k,v in sorted(by_met.items())}
cap["datasets"]=cap_ds
class _D(yaml.SafeDumper): pass
_D.add_representer(OrderedDict, lambda d,x: d.represent_mapping('tag:yaml.org,2002:map',x.items()))
_D.add_representer(type(None), lambda d,_: d.represent_scalar('tag:yaml.org,2002:null',''))
with open(os.path.join(OUT,"capability_map.yaml"),"w",encoding="utf-8") as f:
    yaml.dump(cap,f,Dumper=_D,allow_unicode=True,sort_keys=False,width=140)
print("wrote capability_map.yaml + fields/*.md (",len(cap_ds),"datasets )")
print("by_metric concepts:",list(cap["by_metric"].keys()))
print("by_dimension concepts:",list(cap["by_dimension"].keys()))
