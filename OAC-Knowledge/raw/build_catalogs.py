# -*- coding: utf-8 -*-
"""Deterministic builder: staging JSON -> OAC-Knowledge YAML catalogs."""
import json, os, glob, datetime, re
from collections import defaultdict, OrderedDict
import yaml

_KB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # raw -> OAC-Knowledge
_WS = os.path.dirname(_KB)
STG = next((p for p in [os.environ.get("OAC_STAGING"), os.path.join(_KB,"_work","staging"), os.path.join(_WS,"Dashboard-builder","_oac_extract")] if p and os.path.isdir(p)), os.path.join(_KB,"_work","staging"))
OUT = _KB
NSAW_TC = os.environ.get("NSAW_CLAUDE_TC") or next((p for p in [os.path.join(_WS,"NSAW_Claude","data_context","TABLE_CATALOG.yaml"), os.path.join(os.path.dirname(_WS),"NSAW_Claude","data_context","TABLE_CATALOG.yaml")] if os.path.isfile(p)), os.path.join(_WS,"NSAW_Claude","data_context","TABLE_CATALOG.yaml"))
EXTRACT_DATE = "2026-06-20"
os.makedirs(OUT, exist_ok=True)

def load(p):
    with open(os.path.join(STG, p), encoding="utf-8") as f:
        return json.load(f)

dfsteps  = load("dataflows_steps.json")
dfdigest = {d["id"]: d for d in load("dataflows_digest.json")}
physmap  = load("physical_mapping.json")
dsall    = load(os.path.join("raw","datasets_all.json"))["datasets"]
enum     = load(os.path.join("raw","catalog_enumeration.json"))
digests  = {os.path.splitext(os.path.basename(f))[0]: json.load(open(f,encoding="utf-8"))
            for f in glob.glob(os.path.join(STG,"digest","*.json"))}

WB_TITLES = {
 "DB01_Revenue_v1_1":"(KGR) DB01.Revenue_v1.1",
 "DB02_Expense_v1_1":"(KGR) DB02.Expense_v1.1",
 "BC03_04_05_SFC_MIS":"(KGR) BRD.BC03-04-05_SFC ước tính_SFC thực tế_ MIS",
 "BC01_Daily_Summary":"(KGR) BRD.BC01_Daily_Summary",
}
WB_ORDER = ["DB01_Revenue_v1_1","DB02_Expense_v1_1","BC01_Daily_Summary","BC03_04_05_SFC_MIS"]

# ---------- helpers ----------
def parse_id(s):
    if s is None: return (None,None)
    m = re.match(r"^XSA\('(.+?)'\.'(.+?)'\)$", s)
    if m: return (m.group(1), m.group(2))
    m = re.match(r"^'(.+?)'\.'(.+?)'$", s)
    if m: return (m.group(1), m.group(2))
    return (None, s)
def key(o,n): return f"{o}::{n}"
def keyid(s):
    o,n=parse_id(s); return key(o,n)
def iso_date(s): return s[:10] if s else None
def base_table(t):
    return re.sub(r"_\d+$","",t)

# ---------- NSAW existence ----------
nsaw_txt = ""
if os.path.exists(NSAW_TC):
    nsaw_txt = open(NSAW_TC,encoding="utf-8",errors="ignore").read()
def in_nsaw(tbl):
    return (tbl in nsaw_txt) or (base_table(tbl) in nsaw_txt)

# ---------- enumeration maps ----------
enum_ds = {keyid(d["id"]): d for d in enum.get("datasources",[]) if d.get("type")=="dataset"}
enum_df = {d["id"]: d for d in enum.get("dataflows",[]) if d.get("type") in ("dataflow","sequence")}
dsall_map = {keyid(d["datasetId"]): d for d in dsall}

# ---------- producer / consumer ----------
producer = defaultdict(list)
consumer = defaultdict(list)
for fid,f in dfsteps.items():
    for od in (f.get("outputDatasets") or []): producer[keyid(od)].append(fid)
    for idd in (f.get("inputDatasets") or []): consumer[keyid(idd)].append(fid)

# ---------- dataset -> physical ----------
ds2phys = {keyid(x): t for x,t in physmap.get("datasetToPhysicalTables",{}).items()}

# physical usage
phys_used_by_ds=defaultdict(set); phys_used_by_df=defaultdict(set); phys_cols=defaultdict(set)
for fid,steps in physmap.get("perFlow",{}).items():
    fname=dfsteps.get(fid,{}).get("name",fid)
    for st in steps:
        for t,cols in (st.get("physTables") or {}).items():
            phys_used_by_df[t].add(fname)
            if st.get("dataset"): phys_used_by_ds[t].add(parse_id(st["dataset"])[1])
            for c in cols: phys_cols[t].add(c)

# ---------- workbook usage ----------
wb_uses_ds=defaultdict(set); ds_cols_used=defaultdict(lambda: defaultdict(set))
for slug,dg in digests.items():
    for cid,c in dg["columns"].items():
        for r in c.get("refs",[]):
            k=key(r["owner"],r["dataset"]); wb_uses_ds[k].add(slug)
            col=r.get("column") or r.get("table")
            if col: ds_cols_used[k][col].add(slug)

# closure: datasets referenced by workbooks (directly)
closure_direct = set(wb_uses_ds.keys())

# transitive closure: include upstream datasets feeding closure flows
def upstream(dskey, seen):
    for fid in producer.get(dskey,[]):
        for idd in (dfsteps[fid].get("inputDatasets") or []):
            ik=keyid(idd)
            if ik not in seen:
                seen.add(ik); upstream(ik,seen)
closure_all=set(closure_direct)
for k in list(closure_direct):
    closure_all.add(k); upstream(k,closure_all)

def ds_display(k):
    d=dsall_map.get(k) or enum_ds.get(k)
    o,n=k.split("::",1)
    return (d.get("displayName") if d and d.get("displayName") else n)
def ds_name(k): return k.split("::",1)[1]
def ds_owner(k): return k.split("::",1)[0]

def ds_type(k):
    if k in producer: return "dataflow_output"
    d=dsall_map.get(k)
    if d:
        dp=d.get("datamodelProvider") or {}
        if dp.get("provider-type")=="db": return "db_dataset"
        if d.get("provider")=="file": return "file_upload"
        return d.get("type") or "unknown"
    return "unknown"

# ===================================================================
# YAML emit setup
# ===================================================================
class Dumper(yaml.SafeDumper): pass
def str_presenter(d,data):
    if "\n" in data:
        return d.represent_scalar('tag:yaml.org,2002:str',data,style='|')
    return d.represent_scalar('tag:yaml.org,2002:str',data)
Dumper.add_representer(str,str_presenter)
Dumper.add_representer(OrderedDict, lambda dd,data: dd.represent_mapping('tag:yaml.org,2002:map', data.items()))
Dumper.add_representer(type(None), lambda dd,_: dd.represent_scalar('tag:yaml.org,2002:null',''))
def dump(obj,fname):
    with open(os.path.join(OUT,fname),"w",encoding="utf-8") as f:
        f.write(yaml.dump(obj,Dumper=Dumper,allow_unicode=True,sort_keys=False,width=120))
    print("wrote",fname, os.path.getsize(os.path.join(OUT,fname)),"bytes")

# ===================================================================
# 1) physical_table_catalog.yaml
# ===================================================================
VERIFIED_LIVE = {"DW_NS_CUSTOMER_INVOICE_LINES_F","DW_NS_ACCOUNT_D"}  # proven via executePreview flowSQL 2026-06-20
phys_out=OrderedDict()
phys_out["_meta"]={
 "purpose":"Tầng nền VẬT LÝ tự chứa: bảng/cột NSAW thật mà các dataflow KGR đang đọc. Trích LIVE từ định nghĩa dataflow (InputDataset.columns dạng \"TABLE\".\"col\").",
 "extracted_live":EXTRACT_DATE,
 "authority":"Đây là nguồn TƯƠI (đọc hôm nay). NSAW_Claude/data_context chỉ là tầng làm giàu ngữ nghĩa, có thể đã cũ (~2026-05) — khi mâu thuẫn, bản này THẮNG.",
 "verified_live_note":"verified_live=true: đã chứng minh resolve sống qua executePreview flowSQL hôm nay. Các bảng khác: 'via_dataflow_def' = trích từ def đọc hôm nay (chưa probe SELECT riêng).",
 "total_tables":sum(1 for t in phys_cols if t!="Metric_Dim"),
}
pt=OrderedDict()
for t in sorted(phys_cols):
    if t=="Metric_Dim":  # not a DW physical table; it's a KGR dataset used as input
        continue
    pt[t]=OrderedDict([
        ("extracted_live",EXTRACT_DATE),
        ("verified_live", True if t in VERIFIED_LIVE else "via_dataflow_def"),
        ("base_table", base_table(t) if base_table(t)!=t else None),
        ("columns_in_use", sorted(phys_cols[t])),
        ("n_columns_in_use", len(phys_cols[t])),
        ("used_by_datasets", sorted(phys_used_by_ds.get(t,[]))),
        ("used_by_dataflows", sorted(phys_used_by_df.get(t,[]))),
        ("nsaw_claude_ref", OrderedDict([
            ("table", base_table(t)),
            ("documented_in_nsaw", in_nsaw(t)),
            ("ref", NSAW_TC.replace("\\","/")),
            ("freshness","NSAW_Claude ~2026-05; verify trước khi tin ngữ nghĩa/cột"),
        ])),
    ])
    pt[t]={k:v for k,v in pt[t].items() if v is not None}
phys_out["physical_tables"]=pt
dump(phys_out,"physical_table_catalog.yaml")

# ===================================================================
# 2) dataflow_catalog.yaml
# ===================================================================
def flow_record(fid,f):
    inds=[parse_id(x)[1] for x in (f.get("inputDatasets") or [])]
    outds=[parse_id(x)[1] for x in (f.get("outputDatasets") or [])]
    steps=[]
    for s in f.get("steps",[]):
        b=OrderedDict([("step",s["stepId"]),("type",s["type"])])
        if s.get("label") and s["label"] not in (s["stepId"],): b["label"]=s["label"]
        if s["type"]=="InputDataset":
            b["input_dataset"]=parse_id(s.get("dataset"))[1]
            b["dataset_type"]=s.get("datasetType")
            if s.get("physTables"): b["physical_tables"]={k:v for k,v in s["physTables"].items()}
        elif s["type"]=="Join":
            b["join_type"]=s.get("joinType"); b["left"]=s.get("left"); b["right"]=s.get("right")
            b["on"]=[f"{j.get('leftColumn')} {j.get('operator','=')} {j.get('rightColumn')}" for j in (s.get("joinOn") or [])]
            if s.get("cond"): b["condition"]=s["cond"]
        elif s["type"]=="GroupBy":
            b["group_by"]=s.get("groupBy"); b["aggregations"]=[f"{a['as']} = {a['fn']}({a['col']})" for a in (s.get("aggr") or [])]
        elif s["type"]=="AddColumns":
            b["adds"]=[OrderedDict([("name",c["name"]),("expression",c["expression"])]) for c in (s.get("add") or [])]
        elif s["type"]=="Filter":
            b["filters"]=s.get("filters")
        elif s["type"]=="Concatenate":
            b["union_type"]=s.get("unionType"); b["left"]=s.get("left"); b["right"]=s.get("right"); b["match"]=s.get("match")
        elif s["type"]=="SelectColumns":
            b["selected_columns"]=s.get("selected")
        elif s["type"]=="RenameColumns":
            b["renames"]=[f"{r['oldName']} -> {r['newName']}" for r in (s.get("renamed") or [])]
        elif s["type"]=="OutputDataset":
            b["output_dataset"]=s.get("datasetName"); b["save_type"]=s.get("saveType"); b["output_type"]=s.get("outputType")
            if s.get("datasetDescription"): b["dataset_description"]=s["datasetDescription"]
            if s.get("outCols"): b["output_columns"]=[c["col"] for c in s["outCols"]]
        steps.append(b)
    rec=OrderedDict([
        ("dataflow_id",fid),
        ("name",f.get("name")),
        ("object_path",f.get("objectPath")),
        ("last_modified",iso_date(f.get("lastModified"))),
        ("version",f.get("version")),
        ("input_datasets",inds),
        ("output_datasets",outds),
        ("in_closure", any(keyid_of_name(o) in closure_all for o in outds) if outds else False),
        ("n_steps",len(steps)),
        ("steps",steps),
    ])
    return rec

# need name->key resolver for outputs (output names are plain names; owner from producer mapping)
name_to_key={}
for k in list(producer.keys())+list(dsall_map.keys()):
    name_to_key.setdefault(k.split("::",1)[1], k)
def keyid_of_name(n):
    return name_to_key.get(n, key("?",n))

df_out=OrderedDict()
df_out["_meta"]={
 "purpose":"Mọi dataflow KGR: chuỗi step (Join/Aggregate/AddColumns/Filter/Union/Output), input→output dataset, logic biến đổi đầy đủ (expression giữ nguyên).",
 "extracted_live":EXTRACT_DATE,
 "total_dataflows":len(dfsteps),
 "note":"in_closure=true nếu output dataset nằm trong chuỗi nuôi 1 trong 4 workbook. Flow in_closure=false là ứng viên archive (xem archive_recommendations.md).",
}
flows=OrderedDict()
# sort: in_closure first, then by last_modified desc
fids_sorted=sorted(dfsteps.keys(), key=lambda x:(dfsteps[x].get("lastModified") or ""), reverse=True)
for fid in fids_sorted:
    rec=flow_record(fid,dfsteps[fid])
    flows[dfsteps[fid].get("name") or fid]=rec
df_out["dataflows"]=flows
dump(df_out,"dataflow_catalog.yaml")

# ===================================================================
# 3) dataset_catalog.yaml
# ===================================================================
all_ds_keys=set(dsall_map)|set(producer)|set(consumer)|set(wb_uses_ds)|closure_all
ds_out=OrderedDict()
ds_out["_meta"]={
 "purpose":"Mọi dataset OAC: loại (dataflow_output|db_dataset|file), dataflow sinh ra, workbook/dataflow dùng, cột workbook tham chiếu, bảng vật lý nguồn.",
 "extracted_live":EXTRACT_DATE,
 "total_datasets":len(all_ds_keys),
 "type_legend":{"dataflow_output":"output của 1 dataflow","db_dataset":"dataset nối DB (dwcs) — có thể là 1 bảng hoặc builder join nhiều bảng","file_upload":"file tải lên"},
}
dsd=OrderedDict()
for k in sorted(all_ds_keys, key=lambda x:x.split('::',1)[1].lower()):
    d=dsall_map.get(k); en=enum_ds.get(k)
    rec=OrderedDict()
    rec["name"]=ds_name(k)
    rec["display_name"]=ds_display(k)
    rec["owner"]=ds_owner(k)
    if d and d.get("description"): rec["description"]=d["description"]
    rec["type"]=ds_type(k)
    rec["produced_by_dataflows"]=[dfsteps[f].get("name") for f in producer.get(k,[])] or None
    rec["used_by_workbooks"]=sorted(WB_TITLES.get(s,s) for s in wb_uses_ds.get(k,[])) or None
    rec["used_by_dataflows"]=sorted(set(dfsteps[f].get("name") for f in consumer.get(k,[]))) or None
    rec["in_closure"]= k in closure_all
    if ds2phys.get(k):
        phys={t:c for t,c in ds2phys[k].items() if t.startswith("DW")}
        other={t:c for t,c in ds2phys[k].items() if not t.startswith("DW")}
        if phys: rec["physical_tables"]=phys
        if other: rec["file_or_other_sources"]=other
    cols=ds_cols_used.get(k)
    if cols: rec["columns_used_by_workbooks"]=sorted(cols.keys())
    if d:
        rec["data_last_modified"]=iso_date(d.get("dataLastModified"))
        rec["folder_path"]=d.get("folderPath") or (en.get("path") if en else None)
    elif en:
        rec["folder_path"]=en.get("path")
    rec={kk:vv for kk,vv in rec.items() if vv is not None}
    dsd[ds_name(k)]=rec
ds_out["datasets"]=dsd
dump(ds_out,"dataset_catalog.yaml")

# ===================================================================
# 4) workbook_catalog.yaml
# ===================================================================
wb_out=OrderedDict()
wb_out["_meta"]={
 "purpose":"4 workbook KGR: canvas -> viz (loại chart) -> measure/dim -> dataset.column nguồn. + datasource đính kèm (used/unused).",
 "extracted_live":EXTRACT_DATE,
}
wbd=OrderedDict()
for slug in WB_ORDER:
    dg=digests[slug]
    used_ds=set()
    for cid,c in dg["columns"].items():
        for r in c.get("refs",[]): used_ds.add(r["dataset"])
    datasources=[]
    for ds in dg["datasources"]:
        datasources.append(OrderedDict([("name",ds["name"]),("owner",ds["owner"]),("used", ds["name"] in used_ds)]))
    canvases=[]
    for cv in dg["canvases"]:
        vz=[]
        for vn in cv["views"]:
            v=dg["vizzes"].get(vn)
            if not v: continue
            measures=[]
            for cidu in v["columnIDs"]:
                col=dg["columns"].get(cidu)
                if not col: continue
                refs=col.get("refs",[])
                src=[f'{r["dataset"]}.{r.get("column") or r.get("table")}' for r in refs]
                measures.append(OrderedDict([("field", col.get("display") or cidu),("column_id",cidu),
                                             ("expression", col.get("expr")),("sources", src or None)]))
            measures=[{k2:v2 for k2,v2 in m.items() if v2 is not None} for m in measures]
            vz.append(OrderedDict([("view",vn),("chart_type",v["pluginType"]),("title",v.get("caption")),("fields",measures)]))
        canvases.append(OrderedDict([("canvas",cv["caption"]),("view",cv["viewName"]),("n_viz",len(vz)),("vizzes",vz)]))
    wbd[WB_TITLES[slug]]=OrderedDict([
        ("slug",slug),
        ("n_datasources",len(datasources)),
        ("n_datasources_used",sum(1 for d in datasources if d["used"])),
        ("datasources",datasources),
        ("n_canvases",len(canvases)),
        ("canvases",canvases),
    ])
wb_out["workbooks"]=wbd
dump(wb_out,"workbook_catalog.yaml")

# ===================================================================
# 5) lineage_graph.yaml
# ===================================================================
edges=[]
# viz -> dataset.col
for slug in WB_ORDER:
    dg=digests[slug]
    for cid,c in dg["columns"].items():
        for r in c.get("refs",[]):
            col=r.get("column") or r.get("table") or "?"
            edges.append({"from":f"workbook:{slug}/{cid}","to":f"dataset:{r['dataset']}/{col}"})
            # bridge col-node -> dataset-node so graph is traversable end-to-end
            edges.append({"from":f"dataset:{r['dataset']}/{col}","to":f"dataset:{r['dataset']}"})
# dataset -> producing flow ; flow -> input dataset
for fid,f in dfsteps.items():
    fname=f.get("name")
    for od in (f.get("outputDatasets") or []):
        edges.append({"from":f"dataset:{parse_id(od)[1]}","to":f"dataflow:{fname}"})
    for idd in (f.get("inputDatasets") or []):
        edges.append({"from":f"dataflow:{fname}","to":f"dataset:{parse_id(idd)[1]}"})
# dataset -> physical
for k,tbls in ds2phys.items():
    for t in tbls:
        if t=="Metric_Dim": continue
        edges.append({"from":f"dataset:{ds_name(k)}","to":f"physical:{t}"})
lg=OrderedDict()
lg["_meta"]={"purpose":"Edge list traversable: workbook->dataset->dataflow->dataset(upstream)->physical. Dùng trace_field.py.",
             "extracted_live":EXTRACT_DATE,"n_edges":len(edges),
             "node_types":["workbook:<slug>/<columnID>","dataset:<name>[/<col>]","dataflow:<name>","physical:<DW_TABLE>"]}
lg["terminal_physical_nodes"]=sorted(f"physical:{t}" for t in phys_cols if t!="Metric_Dim")
lg["edges"]=edges
dump(lg,"lineage_graph.yaml")

print("\nCLOSURE datasets:",len(closure_all)," | direct:",len(closure_direct))
print("DONE")
