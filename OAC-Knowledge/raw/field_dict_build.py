# -*- coding: utf-8 -*-
"""P1: Build field_dictionary.yaml from the column resolver. NO numeric values."""
import json, os, re
from collections import defaultdict, OrderedDict
import yaml
import resolver as R   # resolver.py in same dir

_KB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # raw -> OAC-Knowledge
_WS = os.path.dirname(_KB)
STG=next((p for p in [os.environ.get("OAC_STAGING"), os.path.join(_KB,"_work","staging"), os.path.join(_WS,"Dashboard-builder","_oac_extract")] if p and os.path.isdir(p)), os.path.join(_KB,"_work","staging"))
OUT=_KB
EXTRACT_DATE="2026-06-20"

dscat=yaml.safe_load(open(os.path.join(OUT,"dataset_catalog.yaml"),encoding="utf-8"))["datasets"]
physmap=json.load(open(os.path.join(STG,"physical_mapping.json"),encoding="utf-8"))
import glob
digests={os.path.splitext(os.path.basename(f))[0]:json.load(open(f,encoding="utf-8"))
         for f in glob.glob(os.path.join(STG,"digest","*.json"))}
WB_TITLES={"DB01_Revenue_v1_1":"(KGR) DB01.Revenue_v1.1","DB02_Expense_v1_1":"(KGR) DB02.Expense_v1.1",
 "BC03_04_05_SFC_MIS":"(KGR) BRD.BC03-04-05_SFC ước tính_SFC thực tế_ MIS","BC01_Daily_Summary":"(KGR) BRD.BC01_Daily_Summary"}

# shown_as map: (dataset, col) -> [{workbook, field, column_id}]
shown=defaultdict(list)
for slug,dg in digests.items():
    # viz field display per columnID
    for cid,c in dg["columns"].items():
        disp=c.get("display") or cid
        for r in c.get("refs",[]):
            col=r.get("column") or r.get("table")
            shown[(r["dataset"],col)].append({"workbook":WB_TITLES.get(slug,slug),"field":disp,"column_id":cid})

def fkey(f):
    if f.get("type")=="filter": return "filter:: "+f.get("expr","")
    if f.get("type")=="join": return f"join:: {f.get('joinType')} ON {', '.join(f.get('on',[]))}"
    return json.dumps(f,ensure_ascii=False)

def dedup(seq):
    out=[];seen=set()
    for x in seq:
        if x not in seen: seen.add(x);out.append(x)
    return out

def output_step_id(fid,dsname):
    fl=R.get_flow(fid)
    for sid,s in fl.steps.items():
        if s.get("type")=="OutputDataset" and s.get("datasetName")==dsname: return sid
    return None

closure_df=[n for n,r in dscat.items() if r.get("type")=="dataflow_output" and r.get("in_closure")]
closure_db=[n for n,r in dscat.items() if r.get("type")=="db_dataset" and r.get("in_closure")]

fd=OrderedDict()
fd["_meta"]={
 "purpose":"Từ điển CẤP CỘT: mỗi field giải tới gốc (công thức→nguồn→filter→join→bảng vật lý), grain, ý nghĩa. KHÔNG lưu giá trị số (data live).",
 "extracted_live":EXTRACT_DATE,
 "principle":"NO numbers. Mọi giá trị tuyệt đối lấy LIVE qua live_query_recipe. File này chỉ mô tả CÁCH TÍNH.",
 "authority":"OAC live > NSAW_Claude (có điều kiện freshness). Trong OAC: báo cáo (BC) > dashboard (DB).",
 "business_meaning":"Ý nghĩa nghiệp vụ + độ tin của metric trụ → business_glossary.yaml. Cột raw = công thức TỰ-TẢ (direct_formula/derivation); không để placeholder chưa-điền.",
}
ds_out=OrderedDict()

for dsname in closure_df:
    fid=R.pick_producer(dsname)
    flowname=R.ALL[fid].get("display-name") if fid else None
    rec=OrderedDict([("type","dataflow_output"),("producer_flow",flowname),("producer_flow_id",fid),
                     ("grain","TODO_P2"),
                     ("live_query_recipe", f"executePreview stepID={output_step_id(fid,dsname)} trên flow '{flowname}' (def id {fid}); đọc flowData/flowSQL; tự aggregate theo grain cần. KHÔNG cache số.")])
    cols=OrderedDict()
    outs=R.get_flow(fid).output_columns().get(dsname,{}) if fid else {}
    for col in sorted(outs):
        node,filters=outs[col]
        acc=R.collect_physical(node)
        # direct formula summary
        k=node.get("k")
        if k=="expr": direct=node["expr"].strip()
        elif k=="agg": direct=f"{node['fn']}( {R._nodelabel(node['of']) if hasattr(R,'_nodelabel') else '...'} )"
        elif k=="phys": direct=f"physical {node['table']}.{node['col']}"
        elif k=="upstream": direct=f"← {node['dataset']}.{node['col']}"
        elif k=="union": direct="UNION(...)"
        else: direct=json.dumps(node,ensure_ascii=False)[:200]
        deps=sorted(node.get("refs",{}).keys()) if k=="expr" else None
        entry=OrderedDict()
        entry["kind"]=k
        entry["direct_formula"]=direct[:400]
        if node.get("k")=="agg": entry["aggregation"]=node.get("fn")
        if deps: entry["depends_on"]=deps
        entry["physical_roots"]=sorted(f"{t}.{c}" for t,c in acc["phys"] if (t or "").startswith("DW")) or None
        other_roots=sorted(f"{t}.{c}" for t,c in acc["phys"] if not (t or "").startswith("DW"))
        if other_roots: entry["non_physical_roots"]=other_roots
        if acc["upstream"]: entry["upstream_leaf_datasets"]=sorted(f"{d}.{c}" for d,c in acc["upstream"])
        if acc["unknown"]: entry["unresolved"]=sorted(str(x) for x in acc["unknown"])
        entry["filters"]=dedup([f["expr"] for f in filters if f.get("type")=="filter"]) or None
        entry["joins"]=dedup([f"{f.get('joinType')}: {', '.join(f.get('on',[]))}" for f in filters if f.get("type")=="join"]) or None
        deriv=R.render(node,1)
        entry["derivation"]=(deriv[:1600]+(" …[cắt]" if len(deriv)>1600 else ""))
        if not entry.get("physical_roots") and not entry.get("upstream_leaf_datasets"):
            nums=re.findall(r'(?<![\w.])\d{4,}(?:\.\d+)?', deriv)
            if nums:
                entry["governance_flag"]="HARDCODED_CONSTANT trong dataflow — số cứng, dễ lỗi thời; nên thay bằng nguồn động"
                entry["hardcoded_values_sample"]=sorted(set(nums))[:5]
            else:
                entry["source_note"]="literal/label hoặc aggregate-không-nguồn-vật-lý (không có physical root)"
        sa=shown.get((dsname,col))
        if sa: entry["shown_as"]=sa
        # business meaning lives in business_glossary.yaml (pillar metrics); raw column = công thức tự-tả.
        cols[col]={kk:vv for kk,vv in entry.items() if vv is not None}
    rec["columns"]=cols
    ds_out[dsname]=rec

for dsname in closure_db:
    o,_=None,None
    # find physical tables for this db dataset
    phys=None
    for xsa,tbls in physmap.get("datasetToPhysicalTables",{}).items():
        if R.parse_id(xsa)[1]==dsname: phys={t:c for t,c in tbls.items()}; break
    rec=OrderedDict([("type","db_dataset"),
        ("note","Dataset nối DB (dataset-builder/bảng). Cột = cột vật lý. Join keys + WHERE filter NỘI BỘ: xem flowSQL (P2) / live_query_recipe."),
        ("physical_tables",phys),
        ("internal_joins_filters","TODO_P2 (flowSQL)"),
        ("grain","TODO_P2"),
        ("live_query_recipe", f"executePreview trên InputDataset step bất kỳ đọc '{dsname}' để lấy compiled flowSQL (join+WHERE); hoặc dùng dataset trực tiếp trong workbook.")])
    # columns workbooks use
    usedcols=sorted({c for (d,c),v in shown.items() if d==dsname and c})
    if usedcols: rec["columns_used_by_workbooks"]=usedcols
    ds_out[dsname]=rec

fd["datasets"]=ds_out

class Dumper(yaml.SafeDumper): pass
Dumper.add_representer(str, lambda d,x: d.represent_scalar('tag:yaml.org,2002:str',x,style='|' if "\n" in x else None))
Dumper.add_representer(OrderedDict, lambda d,x: d.represent_mapping('tag:yaml.org,2002:map',x.items()))
Dumper.add_representer(type(None), lambda d,_: d.represent_scalar('tag:yaml.org,2002:null',''))
with open(os.path.join(OUT,"field_dictionary.yaml"),"w",encoding="utf-8") as f:
    f.write(yaml.dump(fd,Dumper=Dumper,allow_unicode=True,sort_keys=False,width=140))
n_cols=sum(len(r.get("columns",{})) for r in ds_out.values() if r.get("type")=="dataflow_output")
print("wrote field_dictionary.yaml", os.path.getsize(os.path.join(OUT,"field_dictionary.yaml")),"bytes")
print("dataflow_output datasets:",len(closure_df)," db datasets:",len(closure_db)," resolved columns:",n_cols)
# coverage: columns with empty physical_roots and not upstream (potential gaps)
gaps=[]
for dsn,r in ds_out.items():
    if r.get("type")!="dataflow_output": continue
    for c,e in r["columns"].items():
        if not e.get("physical_roots") and not e.get("upstream_leaf_datasets") and e.get("kind") not in ("unknown",):
            gaps.append(f"{dsn}.{c}")
print("columns with NO physical roots/upstream (check):",len(gaps))
for g in gaps[:20]: print("   ",g)
