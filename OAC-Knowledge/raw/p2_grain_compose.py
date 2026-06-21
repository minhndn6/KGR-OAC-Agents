# -*- coding: utf-8 -*-
"""P2: derive grain per dataset, enrich db-dataset entries, write live_query_recipes."""
import json, os, re
from collections import deque, OrderedDict
import yaml
import resolver as R

_KB=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # raw -> OAC-Knowledge
_WS=os.path.dirname(_KB)
OUT=_KB; STG=next((p for p in [os.environ.get("OAC_STAGING"), os.path.join(_KB,"_work","staging"), os.path.join(_WS,"Dashboard-builder","_oac_extract")] if p and os.path.isdir(p)), os.path.join(_KB,"_work","staging"))
def loadY(p): return yaml.safe_load(open(os.path.join(OUT,p),encoding="utf-8"))
physmap=json.load(open(os.path.join(STG,"physical_mapping.json"),encoding="utf-8"))
_dsall=json.load(open(os.path.join(STG,"raw","datasets_all.json"),encoding="utf-8"))["datasets"]
DESC={R.parse_id(d["datasetId"])[1]: (d.get("description") or "") for d in _dsall}
_GRAIN_OK=re.compile(r'(đến|theo|line|per|level|invoice|credit|\bID\b|kỳ|period)', re.I)
_GRAIN_BAD=re.compile(r'20\d\d|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec', re.I)
def desc_grain(dsname):
    desc=DESC.get(dsname,"")
    m=re.search(r'[Gg]rain[^\n.]*', desc)
    if not m: return None
    g=m.group(0).strip()
    # reject garbage like "grain, May 2026"; accept only if it looks like a real grain spec
    if _GRAIN_BAD.search(g) or not _GRAIN_OK.search(g): return None
    return g

def grain_of(fid,dsname):
    fl=R.get_flow(fid)
    outsid=[sid for sid,s in fl.steps.items() if s.get("type")=="OutputDataset" and s.get("datasetName")==dsname]
    if not outsid: return None
    q=deque(fl.preds.get(outsid[0],[])); seen=set()
    while q:
        sid=q.popleft()
        if sid in seen: continue
        seen.add(sid)
        s=fl.steps.get(sid,{})
        if s.get("type")=="GroupBy":
            gb=s.get("groupByColumns") or []
            return ("group: "+", ".join(gb)) if gb else "aggregate toàn bộ (không group key)"
        for p in fl.preds.get(sid,[]): q.append(p)
    return "line-level (không GroupBy cuối)"

# ----- enrich field_dictionary -----
fd=loadY("field_dictionary.yaml")
for dsname,rec in fd["datasets"].items():
    if rec.get("type")=="dataflow_output":
        fid=rec.get("producer_flow_id")
        dg=desc_grain(dsname)
        if dg:
            rec["grain"]=dg; rec["grain_source"]="dataset description (authoritative)"
        elif fid:
            rec["grain"]=grain_of(fid,dsname) or "?"; rec["grain_source"]="heuristic: GroupBy gần Output nhất — verify qua dataflow_catalog steps"
    elif rec.get("type")=="db_dataset":
        # physical composition
        comp=None
        for xsa,tbls in physmap.get("datasetToPhysicalTables",{}).items():
            if R.parse_id(xsa)[1]==dsname: comp=sorted(tbls.keys()); break
        rec["physical_tables_composed"]=comp
        rec["internal_joins_filters"]=("Join-key & WHERE NỘI BỘ của dataset KHÔNG lộ qua API trên instance này "
            "(executePreview đọc cache XSA; endpoint dataset/datasets/metadata trả 500). Cột giữ qualifier bảng vật lý nên biết "
            "ĐỦ bảng+cột nguồn; quan hệ join theo chuẩn NetSuite (line→ACCOUNT/ITEM/PERIOD; extension→ID; segment→CSEG_*). "
            "Filter NGHIỆP VỤ quan trọng (posting/acct/subsidiary/vụ việc) nằm ở DATAFLOW tiêu thụ — xem field_dictionary cột tương ứng. confidence: join=medium.")
        rec["grain"]=("line-level" if any("LINES_F" in (t or "") for t in (comp or [])) else
                      ("header-level" if any(t.endswith("_F") for t in (comp or [])) else "dim/lookup"))
    # drop now-resolved TODO placeholder if any
fd["_meta"]["grain_note"]="grain dataflow_output = group key của GroupBy cuối trên đường tới Output; line-level nếu không có."
with open(os.path.join(OUT,"field_dictionary.yaml"),"w",encoding="utf-8") as f:
    yaml.dump(fd,f,allow_unicode=True,sort_keys=False,width=140,Dumper=_D() if False else yaml.SafeDumper)
# re-dump with block style for multiline handled by default safe dumper (ok)

# ----- add grain into dataset_catalog -----
dc=loadY("dataset_catalog.yaml")
for dsname,rec in dc["datasets"].items():
    fdrec=fd["datasets"].get(dsname)
    if fdrec and fdrec.get("grain"):
        # insert grain after in_closure
        rec["grain"]=fdrec["grain"]
with open(os.path.join(OUT,"dataset_catalog.yaml"),"w",encoding="utf-8") as f:
    yaml.dump(dc,f,allow_unicode=True,sort_keys=False,width=140,Dumper=yaml.SafeDumper)

print("grain sample:")
for n in ["(KGR) DTF_CALC_INVOICE_MEMO_#","TD_Report_Long","Nganh_Report_Long_#","TD_Report_PNL_Bridge","1. Invoice_v2","KGR_DS_SFC_vs_MEMO_v2"]:
    print("  ",n,"->",fd["datasets"].get(n,{}).get("grain"))
print("DONE P2 python")
