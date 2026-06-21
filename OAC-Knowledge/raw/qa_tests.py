# -*- coding: utf-8 -*-
"""QA SUITE — kiểm thử OAC-Knowledge như QA khó tính, map vào yêu cầu user.
Chạy: PYTHONUTF8=1 python qa_tests.py   (offline; test live H1 chạy riêng qua browser)"""
import os, re, json, subprocess, sys
import yaml

KB=os.environ.get("OAC_KB_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # raw -> OAC-Knowledge
RAW=os.path.join(KB,"raw")
def Y(p): return yaml.safe_load(open(os.path.join(KB,p),encoding="utf-8"))
def J(p): return json.load(open(os.path.join(RAW,p),encoding="utf-8"))
def txt(p): return open(os.path.join(KB,p),encoding="utf-8").read()

wb=Y("workbook_catalog.yaml")["workbooks"]
ds=Y("dataset_catalog.yaml")["datasets"]
dfc=Y("dataflow_catalog.yaml")["dataflows"]
phys=Y("physical_table_catalog.yaml")["physical_tables"]
lin=Y("lineage_graph.yaml")
fd=Y("field_dictionary.yaml")["datasets"]
cap=Y("capability_map.yaml")
glo=Y("business_glossary.yaml")
ALL=J("dataflows_all.json")

results=[]
def check(tc, desc, cond, evidence=""):
    results.append((tc, "PASS" if cond else "FAIL", desc, evidence))

# ---------- A. structural / cross-file consistency ----------
# A2: every workbook field source dataset.col resolves
bad=[]
for wbn,w in wb.items():
    for cv in w["canvases"]:
        for v in cv["vizzes"]:
            for f in (v.get("fields") or []):
                for s in (f.get("sources") or []):
                    dsn=s.rsplit(".",1)[0]
                    if dsn not in ds: bad.append(f"{wbn}:{s}")
check("A2","Mọi workbook field.sources → dataset có trong dataset_catalog", not bad, f"{len(bad)} lạ: {bad[:3]}")

# A3: field_dictionary physical_roots ⊆ physical_table_catalog keys
fr_bad=set()
for dsn,r in fd.items():
    for c,e in (r.get("columns") or {}).items():
        if not isinstance(e,dict): continue
        for pr in (e.get("physical_roots") or []):
            t=pr.rsplit(".",1)[0]
            if t not in phys: fr_bad.add(t)
check("A3","Mọi physical_root trong field_dictionary tồn tại ở physical_table_catalog", not fr_bad, f"lạ: {sorted(fr_bad)[:5]}")

# A4: produced_by + dataset.physical_tables resolve
a4=[]
for dsn,r in ds.items():
    for f in (r.get("produced_by_dataflows") or []):
        if f not in dfc: a4.append(f"producer {f}")
    for t in (r.get("physical_tables") or {}):
        if t not in phys: a4.append(f"phys {t}")
check("A4","produced_by + dataset.physical_tables resolve", not a4, f"{a4[:3]}")

# ---------- B. lineage correctness (re-derive độc lập từ raw) ----------
def parse_id(s):
    m=re.match(r"^XSA\('(.+?)'\.'(.+?)'\)$",s) or re.match(r"^'(.+?)'\.'(.+?)'$",s); return m.group(2) if m else s
def raw_addcol(flow_name_sub, colname):
    for fid,jj in ALL.items():
        if flow_name_sub in fid:
            for s in (jj.get("definition") or {}).get("steps",[]):
                if s.get("type")=="AddColumns":
                    for c in s.get("columns",[]):
                        if c.get("name")==colname: return c.get("expression")
    return None
# B1: a9 formula in field_dictionary == raw def
raw_a9=raw_addcol("KGR_DF_TD_Metrics_bk","a9")
fd_a9=((fd.get("TD_Metrics_Wide") or {}).get("columns") or {}).get("a9",{}).get("direct_formula")
check("B1","a9 trong field_dictionary KHỚP raw dataflow def (không bịa)",
      bool(raw_a9) and bool(fd_a9) and raw_a9.replace(" ","")==fd_a9.replace(" ",""),
      f"raw={raw_a9!r} fd={fd_a9!r}")
# B2: revenue physical roots đúng (BASE_REVENUE invoice+credit)
rev=((fd.get("(KGR) DTF_CALC_INVOICE_MEMO_#") or {}).get("columns") or {}).get("Doanh thu thực tế",{})
prset=set(rev.get("physical_roots") or [])
check("B2","Doanh thu thực tế → BASE_REVENUE (invoice+credit)",
      "DW_NS_CUSTOMER_INVOICE_LINES_F.BASE_REVENUE" in prset and "DW_NS_CUSTOMER_CREDIT_LINES_F.BASE_REVENUE" in prset, str(sorted(prset)[:4]))
# B3: revenue filters chứa posting + income
revf=" ".join(rev.get("filters") or [])
check("B3","Filter doanh thu chứa ISPOSTING='T' + ACCTTYPE Income", "ISPOSTING" in revf and "Income" in revf, revf[:120])
# B4: COGS 3-tier tới GVMT + GVTK
cogs=((fd.get("(KGR) DTF_CALC_INVOICE_MEMO_#") or {}).get("columns") or {}).get("Giá Vốn",{})
cset=set(cogs.get("physical_roots") or [])
check("B4","Giá vốn → GVMT_CT + GVTK", any("GIA_VON_MUC_TIEU" in x for x in cset) and any("GIA_VON_TON_KHO" in x for x in cset), str(sorted(cset)[:6]))

# ---------- C. no-numbers principle ----------
ALLOW={"247258890.47","247258890.4666666","247,258,890.47"}  # governance hardcoded (được phép, có cờ)
money_re=re.compile(r"\d{1,3}(?:,\d{3}){2,}|\b\d+\s*(?:tỷ|triệu)\b")
c_hits=[]
for root,_,files in os.walk(KB):
    if os.sep+"raw" in root: continue
    for fn in files:
        if not fn.endswith((".md",".yaml")): continue
        for i,ln in enumerate(open(os.path.join(root,fn),encoding="utf-8",errors="ignore"),1):
            for m in money_re.findall(ln):
                # cho phép: hằng số cứng có cờ governance (cứng/hardcode), hoặc token whitelist
                if any(a in ln for a in ALLOW): continue
                if "cứng" in ln or "hardcode" in ln.lower() or "governance" in ln.lower(): continue
                c_hits.append(f"{fn}:{i}:{ln.strip()[:70]}")
check("C1","KHÔNG cache số tiền/giá trị (chỉ cho phép hằng số có cờ governance)", not c_hits, f"{len(c_hits)} hit: {c_hits[:3]}")
# C2: field_dictionary không có field 'value/result/total_value'
c2=[]
for dsn,r in fd.items():
    for c,e in (r.get("columns") or {}).items():
        if isinstance(e,dict) and (set(e.keys()) & {"value","result","amount"}): c2.append(f"{dsn}.{c}")
check("C2","field_dictionary không lưu trường giá trị (value/result/amount)", not c2, str(c2[:3]))

# ---------- D. consultant forward ----------
bm=cap.get("by_metric",{}); bd=cap.get("by_dimension",{})
check("D1a","capability_map.by_metric có 'revenue' gồm hub",
      any("revenue" in k for k in bm) and any("(KGR) DTF_CALC_INVOICE_MEMO_#" in v for k,v in bm.items() if "revenue" in k), "")
need_dims=["chuoi","kenh","nganh","model","asm","don_vi","tinh","thoi_gian","xanh_do"]
have=" ".join(bd.keys())
check("D1b","by_dimension phủ chuỗi/kênh/ngành/model/asm/đơn vị/tỉnh/thời gian/xanh-đỏ", all(d in have for d in need_dims), have)
check("D3","source_selection_playbook có reuse-vs-build + cạm bẫy AOP-estimate + fan-out",
      all(k in txt("source_selection_playbook.md") for k in ["Reuse","ƯỚC TÍNH","fan-out","hardcode" if False else "cứng"]), "")

# ---------- E. backward/impact via lineage_graph ----------
edges=lin["edges"]; fwd={}; rev={}
for e in edges: fwd.setdefault(e["from"],[]).append(e["to"]); rev.setdefault(e["to"],[]).append(e["from"])
def reach(start,adj,pred):
    seen=set(); st=[start]
    while st:
        n=st.pop()
        if n in seen: continue
        seen.add(n)
        if pred(n) and n!=start: return True
        st+=adj.get(n,[])
    return False
# E2: a physical table reaches up to a workbook
pnode="physical:DW_NS_CUSTOMER_INVOICE_LINES_F"
check("E2","Impact: bảng vật lý → lần ngược tới ≥1 workbook", reach(pnode,rev,lambda n:n.startswith("workbook:")), "")
# E1: a workbook node reaches down to a physical
wbnode=next((e["from"] for e in edges if e["from"].startswith("workbook:")),None)
check("E1","Trace: workbook field → xuống tới physical", bool(wbnode) and reach(wbnode,fwd,lambda n:n.startswith("physical:")), wbnode or "")

# ---------- F. precedence ----------
gtext=txt("business_glossary.yaml")
check("F1","Precedence SFC: báo cáo DTF_CALC_MIS authoritative > DB SFC_vs_MEMO",
      "DTF_CALC_MIS" in gtext and "authoritative" in gtext and "DB01" in gtext, "")
conf=txt("CONFLICTS_AND_OPEN_QUESTIONS.md")
check("F2","CONFLICTS ghi drift revenue BASE_REVENUE vs NSAW (OAC thắng)",
      "BASE_REVENUE" in conf and "theo OAC" in conf, "")
check("F3","Precedence OAC>NSAW & BC>DB nêu ở external/README + glossary",
      ("báo cáo" in txt("external/README.md") and "dashboard" in txt("external/README.md")) and "precedence" in gtext.lower(), "")

# ---------- G. physical self-containment ----------
gcnt=0; gtot=0
for dsn,r in fd.items():
    if r.get("type")!="dataflow_output": continue
    for c,e in (r.get("columns") or {}).items():
        if isinstance(e,dict) and e.get("shown_as"):
            gtot+=1
            if e.get("physical_roots") or e.get("upstream_leaf_datasets") or e.get("governance_flag") or e.get("source_note"): gcnt+=1
check("G1","Field hiển thị trên workbook đều tự-chứa tới physical (không cần NSAW)", gtot>0 and gcnt==gtot, f"{gcnt}/{gtot}")

# ---------- I. completeness ----------
check("I1","Đủ 4 workbook, mỗi wb có canvas+viz", len(wb)==4 and all(w["canvases"] and any(cv["vizzes"] for cv in w["canvases"]) for w in wb.values()), f"{len(wb)} wb")
miss_dossier=[dsn for dsn,r in fd.items() if r.get("type")=="dataflow_output" and not os.path.exists(os.path.join(KB,"fields",re.sub(r'[^0-9A-Za-z_]+','_',dsn).strip('_')+".md"))]
check("I2","Mọi dataflow_output closure có dossier fields/*.md", not miss_dossier, str(miss_dossier[:3]))
check("I3","Counts: 4 wb / 63 ds / 40 df / 60 phys", len(wb)==4 and len(ds)==63 and len(dfc)==40 and len(phys)==60, f"{len(wb)}/{len(ds)}/{len(dfc)}/{len(phys)}")

# ---------- J. archive separation ----------
arch=txt("archive_recommendations.md")
check("J1","archive_recommendations tồn tại + nêu KHÔNG dựa tên version", "version" in arch and ("KHÔNG" in arch or "không" in arch) and "ARCHIVE" in arch, "")
# archived flows (v1.0) không xuất hiện như producer authoritative trong field_dictionary
arch_flows=["(KGR) 1. DTF_CALC_INVOICE_MEMO_v1.0","KGR_DF_TD_Metrics_v1.0","(KGR) 5. DTF_CALC_MIS_v1.0"]
prod_set={r.get("producer_flow") for r in fd.values() if r.get("producer_flow")}
check("J2","Flow bản v1.0 (archive) KHÔNG là producer trong field_dictionary", not (set(arch_flows)&prod_set), str(set(arch_flows)&prod_set))

# ---------- ENC: encoding integrity ----------
import glob as _g2
_moji=re.compile(r"Ã[\x80-\xbf]|â€|á»|áº")
enc_bad=[]
for p in (_g2.glob(os.path.join(KB,"*.yaml"))+_g2.glob(os.path.join(KB,"*.md"))+_g2.glob(os.path.join(KB,"fields","*.md"))):
    try: s=open(p,encoding="utf-8",errors="strict").read()
    except UnicodeDecodeError: enc_bad.append(os.path.basename(p)+":NON-UTF8"); continue
    if "�" in s: enc_bad.append(os.path.basename(p)+":FFFD")
    if _moji.search(s): enc_bad.append(os.path.basename(p)+":moji")
check("ENC1","Encoding integrity: 0 U+FFFD / mojibake / non-UTF8 trong file curated", not enc_bad, str(enc_bad[:5]))
# round-trip sanity: a known Vietnamese diacritic survives in field_dictionary
_fdtxt=open(os.path.join(KB,"field_dictionary.yaml"),encoding="utf-8").read()
check("ENC2","Dấu tiếng Việt còn nguyên (vd 'Doanh thu thực tế','Giá Vốn')", ("thực tế" in _fdtxt) and ("Giá Vốn" in _fdtxt or "Giá vốn" in _fdtxt), "")

# ---------- report ----------
print(f"{'TC':6} {'KQ':5} MÔ TẢ")
np=nf=0
for tc,st,desc,ev in results:
    print(f"{tc:6} {st:5} {desc}")
    if st=="FAIL":
        nf+=1; print(f"        ↳ EVIDENCE: {ev}")
    else: np+=1
print(f"\nTOTAL: {np} PASS / {nf} FAIL  ({len(results)} test offline)")
sys.exit(1 if nf else 0)
