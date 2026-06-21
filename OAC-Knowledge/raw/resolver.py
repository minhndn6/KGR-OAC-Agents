# -*- coding: utf-8 -*-
"""Column-level lineage resolver for KGR OAC dataflows.
Reads full dataflow defs, builds per-step column-provenance DAG, resolves any
output column to a derivation tree bottoming out at physical DW columns,
collecting filters/joins on the path. Resolves across dataflows.
"""
import json, re, os
from collections import defaultdict

_KB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # raw -> OAC-Knowledge
_WS = os.path.dirname(_KB)
STG = next((p for p in [os.environ.get("OAC_STAGING"), os.path.join(_KB,"_work","staging"), os.path.join(_WS,"Dashboard-builder","_oac_extract")] if p and os.path.isdir(p)), os.path.join(_KB,"_work","staging"))
ALL = json.load(open(os.path.join(STG,"raw","dataflows_all.json"),encoding="utf-8"))  # {flowId: rawDef}

def parse_id(s):
    if s is None: return (None,None)
    m=re.match(r"^XSA\('(.+?)'\.'(.+?)'\)$",s) or re.match(r"^'(.+?)'\.'(.+?)'$",s)
    return (m.group(1),m.group(2)) if m else (None,s)

TBLRE=re.compile(r'^"([^"]+)"\."([^"]+)"$')
REFRE=re.compile(r'"([^"]+)"')

def find_refs(expr, env):
    """Column refs in an expression. Prefer double-quoted; if none, match bare
    identifiers against available env column names (some dataflows omit quotes)."""
    refs={}
    for rc in sorted(set(REFRE.findall(expr))):  # sorted → build reproducible (set order ngẫu nhiên giữa các run)
        refs[rc]=env.get(rc,{"k":"unknown","col":rc})
    if not refs:
        for name in sorted(env, key=len, reverse=True):
            if len(name)<2: continue
            if re.search(r'(?<![\w"])'+re.escape(name)+r'(?![\w"])', expr):
                refs[name]=env[name]
    return refs

# producer index: output dataset name -> flowId  (prefer non-archived / latest)
def build_producer_index():
    idx=defaultdict(list)
    for fid,j in ALL.items():
        dss=(j.get("definition") or {}).get("DSSDependencies") or {}
        for od in (dss.get("outputDatasets") or []):
            nm=parse_id(od.get("datasetId"))[1]
            idx[nm].append(fid)
    return idx
PRODUCERS=build_producer_index()

def pick_producer(dsname):
    cands=PRODUCERS.get(dsname,[])
    if not cands: return None
    def score(fid):
        j=ALL[fid]; path=(j.get("object-path") or "")
        lm=j.get("last-modified") or ""
        return (0 if "Archived" in path else 1, lm)
    return sorted(cands,key=score,reverse=True)[0]

class Flow:
    def __init__(self,fid):
        self.fid=fid; self.j=ALL[fid]; self.def_=self.j.get("definition") or {}
        self.steps={s["stepId"]:s for s in self.def_.get("steps",[])}
        self.preds=defaultdict(list)
        for l in self.def_.get("links",[]):
            self.preds[l["endNode"]].append(l["startNode"])
        self.env={}        # stepId -> {colName: node}
        self.active_filters={}  # stepId -> list of filter/join predicate strings
        self._order=self._topo()
        for sid in self._order: self._process(sid)

    def _topo(self):
        seen=[]; visited=set()
        def visit(s):
            if s in visited: return
            visited.add(s)
            for p in self.preds.get(s,[]): visit(p)
            seen.append(s)
        for sid in self.steps: visit(sid)
        return seen

    def _pred_env(self,sid):
        ps=self.preds.get(sid,[])
        return ps

    def _process(self,sid):
        s=self.steps[sid]; t=s.get("type")
        preds=self.preds.get(sid,[])
        # accumulate filters from preds
        af=[]
        for p in preds: af+=self.active_filters.get(p,[])
        env={}
        if t=="InputDataset":
            for c in s.get("columns",[]):
                nm=c.get("newName"); raw=c.get("name","")
                m=TBLRE.match(raw or "")
                if m: env[nm]={"k":"phys","table":m.group(1),"col":m.group(2)}
                else:
                    dsid=s.get("datasetId"); o,dn=parse_id(dsid)
                    env[nm]={"k":"upstream","dataset":dn,"col":(raw or nm).strip('"')}
            if not env:
                # dataflow-output input lists no columns in def -> pull producer's output cols
                dsid=s.get("datasetId"); o,dn=parse_id(dsid)
                pf=pick_producer(dn)
                if pf and pf not in _UNDER:
                    try:
                        for cn in get_flow(pf).output_columns().get(dn,{}):
                            env[cn]={"k":"upstream","dataset":dn,"col":cn}
                    except Exception:
                        pass
        elif t=="RenameColumns":
            base=dict(self.env.get(preds[0],{})) if preds else {}
            ren={r["oldName"]:r["newName"] for r in s.get("renamedColumns",[])}
            for k,v in base.items(): env[ren.get(k,k)]=v
        elif t=="SelectColumns":
            base=self.env.get(preds[0],{}) if preds else {}
            sel=s.get("selectedColumns",[])
            env={k:base[k] for k in sel if k in base}
            for k in sel:
                if k not in base: env[k]={"k":"unknown","col":k}
        elif t=="Filter":
            env=dict(self.env.get(preds[0],{})) if preds else {}
            for f in s.get("filter",[]):
                expr=f.get("expression")
                if expr: af=af+[{"type":"filter","step":sid,"expr":expr}]
        elif t=="AddColumns":
            env=dict(self.env.get(preds[0],{})) if preds else {}
            for c in s.get("columns",[]):
                nm=c.get("name"); expr=c.get("expression") or ""
                refs=find_refs(expr,env)
                env[nm]={"k":"expr","expr":expr,"refs":refs}
        elif t=="GroupBy":
            base=self.env.get(preds[0],{}) if preds else {}
            for g in s.get("groupByColumns",[]) or []:
                env[g]=base.get(g,{"k":"unknown","col":g})
            for a in s.get("aggrColumns",[]) or []:
                src=base.get(a.get("column"),{"k":"unknown","col":a.get("column")})
                env[a["newName"]]={"k":"agg","fn":a.get("aggrtype"),"of":src}
        elif t=="Join":
            le=self.env.get(s.get("leftDataset"),{}); ri=self.env.get(s.get("rightDataset"),{})
            env=dict(le)
            for k,v in ri.items():
                if k not in env: env[k]=v
            on=[f'{j.get("leftColumn")} {j.get("operator","=")} {j.get("rightColumn")}' for j in s.get("joinOn",[])]
            af=af+[{"type":"join","step":sid,"joinType":s.get("joinType"),"on":on}]
        elif t=="Concatenate":
            le=self.env.get(s.get("leftDataset"),{}); ri=self.env.get(s.get("rightDataset"),{})
            keys=set(le)|set(ri)
            for k in keys:
                env[k]={"k":"union","left":le.get(k),"right":ri.get(k)}
        elif t=="Branch":
            env=dict(self.env.get(preds[0],{})) if preds else {}
        elif t=="OutputDataset":
            env=dict(self.env.get(preds[0],{})) if preds else {}
        else:
            env=dict(self.env.get(preds[0],{})) if preds else {}
        self.env[sid]=env
        self.active_filters[sid]=af

    def output_columns(self):
        """Return {finalName: (node, filters)} for each OutputDataset step."""
        out={}
        for sid,s in self.steps.items():
            if s.get("type")!="OutputDataset": continue
            preds=self.preds.get(sid,[])
            base=self.env.get(preds[0],{}) if preds else {}
            af=self.active_filters.get(sid,[])
            dsname=s.get("datasetName")
            for c in s.get("customizedColumns",[]):
                nm=c.get("colName")
                node=base.get(nm,{"k":"unknown","col":nm})
                out.setdefault(dsname,{})[nm]=(node,af)
        return out

# ---------- cross-flow resolution + rendering ----------
_flow_cache={}
_UNDER=set()
def get_flow(fid):
    if fid not in _flow_cache:
        _UNDER.add(fid)
        try: _flow_cache[fid]=Flow(fid)
        finally: _UNDER.discard(fid)
    return _flow_cache[fid]

def resolve_dataset_col(dsname,col,depth=0,seen=None):
    """Resolve a (dataset,col) to a node tree, crossing into producer flow."""
    seen=seen or set()
    key=(dsname,col)
    if key in seen or depth>40: return {"k":"cycle","dataset":dsname,"col":col}
    seen=seen|{key}
    fid=pick_producer(dsname)
    if not fid: return {"k":"leaf_dataset","dataset":dsname,"col":col}
    fl=get_flow(fid)
    outs=fl.output_columns().get(dsname,{})
    if col not in outs: return {"k":"missing","dataset":dsname,"col":col,"flow":fl.j.get("display-name")}
    node,filters=outs[col]
    return {"k":"resolved","dataset":dsname,"col":col,"flow":fl.j.get("display-name"),
            "node":node,"filters":filters,"flow_obj":fid}

def collect_physical(node,acc=None,fl=None,seen=None):
    """Walk a node tree; return set of physical (table.col) and unresolved upstreams."""
    acc=acc if acc is not None else {"phys":set(),"upstream":set(),"unknown":set()}
    seen=seen if seen is not None else set()
    if not isinstance(node,dict): return acc
    k=node.get("k")
    if k=="phys": acc["phys"].add((node["table"],node["col"]))
    elif k=="upstream":
        r=resolve_dataset_col(node["dataset"],node["col"])
        if r.get("k")=="resolved": collect_physical(r["node"],acc,seen=seen)
        elif r.get("k")=="leaf_dataset": acc["upstream"].add((node["dataset"],node["col"]))
        else: acc["unknown"].add((node["dataset"],node["col"]))
    elif k=="expr":
        for rc,rn in node.get("refs",{}).items(): collect_physical(rn,acc,seen=seen)
    elif k=="agg": collect_physical(node.get("of"),acc,seen=seen)
    elif k=="union":
        collect_physical(node.get("left"),acc,seen=seen); collect_physical(node.get("right"),acc,seen=seen)
    elif k=="unknown": acc["unknown"].add((None,node.get("col")))
    return acc

def render(node,indent=0,seen=None):
    seen=seen or set()
    pad="  "*indent
    if not isinstance(node,dict): return pad+str(node)
    k=node.get("k")
    if k=="phys": return f"{pad}• physical: {node['table']}.{node['col']}"
    if k=="upstream":
        r=resolve_dataset_col(node["dataset"],node["col"])
        if r.get("k")=="resolved":
            return f"{pad}← dataset {node['dataset']}.{node['col']}  (df: {r['flow']})\n"+render(r["node"],indent+1,seen)
        return f"{pad}← dataset {node['dataset']}.{node['col']}  [{r.get('k')}]"
    if k=="expr":
        lines=[f"{pad}= {node['expr'].strip()[:300]}"]
        for rc,rn in node.get("refs",{}).items():
            lines.append(f"{pad}  ↳ \"{rc}\":")
            lines.append(render(rn,indent+2,seen))
        return "\n".join(lines)
    if k=="agg": return f"{pad}= {node['fn']}(...)\n"+render(node.get("of"),indent+1,seen)
    if k=="union": return f"{pad}UNION:\n"+render(node.get("left"),indent+1,seen)+"\n"+render(node.get("right"),indent+1,seen)
    if k=="unknown": return f"{pad}? {node.get('col')}"
    return f"{pad}{json.dumps(node,ensure_ascii=False)[:120]}"

if __name__=="__main__":
    import sys
    # quick test
    for ds,col in [("(KGR) DTF_CALC_INVOICE_MEMO_#","Doanh thu thực tế"),
                   ("(KGR) DTF_CALC_INVOICE_MEMO_#","Giá Vốn")]:
        print("="*70); print(f"{ds} . {col}")
        r=resolve_dataset_col(ds,col)
        if r.get("k")=="resolved":
            print("PRODUCER FLOW:",r["flow"])
            print("FILTERS/JOINS on path:")
            for f in r["filters"]: print("   ",json.dumps(f,ensure_ascii=False)[:160])
            acc=collect_physical(r["node"])
            print("PHYSICAL ROOTS:",sorted(acc["phys"]))
            if acc["upstream"]: print("UPSTREAM(leaf ds):",sorted(acc["upstream"]))
            if acc["unknown"]: print("UNKNOWN:",sorted(x for x in acc["unknown"]))
            print("DERIVATION:"); print(render(r["node"],1))
        else: print("  ",r)
