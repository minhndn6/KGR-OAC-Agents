# -*- coding: utf-8 -*-
"""100+ USE-CASE TEST — mô phỏng câu hỏi của các leader/head/chief công ty.
Chấm mỗi case PASS (KB trả lời được) / PARTIAL (cần build, có cơ chế) / GAP (thiếu).
Ghi QA_USECASES_REPORT.md + IMPROVEMENTS.md. Chạy: PYTHONUTF8=1 python raw/qa_usecases.py"""
import os, re, yaml
KB=os.environ.get("OAC_KB_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # raw -> OAC-Knowledge
def Y(p):
    with open(os.path.join(KB,p),encoding="utf-8") as f: return yaml.safe_load(f)
DS=Y("dataset_catalog.yaml")["datasets"]; FD=Y("field_dictionary.yaml")["datasets"]
GLO=Y("business_glossary.yaml"); CAP=Y("capability_map.yaml"); LIN=Y("lineage_graph.yaml")
PH=Y("physical_table_catalog.yaml")["physical_tables"]
def rd(p): return open(os.path.join(KB,p),encoding="utf-8").read() if os.path.exists(os.path.join(KB,p)) else ""
PLAYBOOK=rd("source_selection_playbook.md"); LIVE=rd("live_query_recipes.md"); GOVT=rd("governance_register.md")
GLOT=rd("business_glossary.yaml"); EXAMPLES=rd("fields/_EXAMPLES_extra.md")+rd("fields/_FLAGSHIP_LoiNhuanGopKinhDoanh.md")

bm=CAP.get("by_metric",{}); bd=CAP.get("by_dimension",{})
# index field_dictionary columns
allcols={}
for dsn,r in FD.items():
    for c,e in (r.get("columns") or {}).items():
        if isinstance(e,dict): allcols.setdefault(c.lower(),(dsn,c,e))
# lineage reverse adjacency
rev={}
for ed in LIN.get("edges",[]): rev.setdefault(ed.get("to"),[]).append(ed.get("from"))
def reach_wb(node):
    seen=set(); st=[node]
    while st:
        n=st.pop()
        if n in seen: continue
        seen.add(n)
        if str(n).startswith("workbook:") and n!=node: return True
        st+=rev.get(n,[])
    return False

def ev_trace(kw):
    k=kw.lower()
    hit=[v for c,v in allcols.items() if k in c]
    for dsn,c,e in hit:
        if e.get("physical_roots") or e.get("upstream_leaf_datasets") or e.get("derivation"): return "PASS",f"{dsn}.{c}"
    # glossary code?
    for code,m in (GLO.get("pnl_waterfall_codes") or {}).items():
        if k in (m.get("label","")+code).lower(): return "PASS",f"glossary {code}"
    return ("PARTIAL",f"{len(hit)} cột khớp nhưng chưa bottom-out") if hit else ("GAP","không thấy field")
def ev_source(mkw,dkw):
    ms=[c for c in bm if mkw in c.lower()]; dsm=set(); msd=set()
    for c in ms: msd|=set(bm[c])
    ds_=[c for c in bd if dkw in c.lower()]
    for c in ds_: dsm|=set(bd[c])
    if not ms: return "GAP",f"metric '{mkw}' không có trong capability_map"
    inter=msd & dsm
    if inter: return "PASS",f"{sorted(inter)[:2]}"
    if not ds_: return "PARTIAL",f"metric có, chiều '{dkw}' chưa index → kiểm hub/playbook"
    return "PARTIAL",f"metric+chiều có riêng, chưa cùng dataset → có thể build từ hub"
def ev_meaning(term):
    t=term.lower()
    if t in GLOT.lower(): return "PASS","glossary có"
    return "GAP","glossary thiếu"
def ev_impact(tbl):
    return ("PASS","reverse→workbook") if reach_wb(f"physical:{tbl}") else ("PARTIAL","không reverse-reach (ngoài closure?)")
def ev_doc(kw,txt,name):
    return ("PASS",name) if kw.lower() in txt.lower() else ("GAP",f"{name} thiếu '{kw}'")

# ===== CASES (persona, category, question, kind, *args) =====
C=[]
# A. TRACE (Finance Analyst / Auditor / BA) — field → gốc
for f in ["Doanh thu thực tế","Giá Vốn","LN Gộp","%GP Ròng","DS Xanh","DS Đỏ","Doanh thu SP mới","CKKM","Quy hoạch SP","Doanh số thực tế","a9","a4","a20","Tên Chuỗi","Tên Kênh","Tên Ngành","Model name","QUANTITY","Nhóm xanh đỏ","Tỷ trọng SP mới"]:
    C.append(("Finance Analyst","trace",f"'{f}' tính từ đâu, gốc bảng NSAW nào?","trace",f))
# B. SOURCE (CEO/CFO/Sales/SupplyChain/CMO/Branch) — cần M theo D
metrics=["revenue","cogs","gross_profit","ckkm","sp_moi","aop","sfc","quantity","profit"]
dims=["chuoi","kenh","nganh","model","asm","don_vi","tinh","khach","xanh_do","thoi_gian","nhom_sp"]
import itertools
persona_map={"revenue":"CEO","cogs":"CFO","gross_profit":"CFO","ckkm":"CMO","sp_moi":"CMO","aop":"CFO","sfc":"Supply Chain Head","quantity":"Supply Chain Head","profit":"CEO"}
for m in metrics:
    for d in ["chuoi","kenh","nganh","model","asm","tinh"]:
        C.append((persona_map.get(m,"BA"),"source",f"Cần {m} theo {d} — lấy đâu?","source",m,d))
# C. MEANING (BA / new exec)
for term in ["Xanh","Đỏ","CKKM","AOP","SFC","Lợi nhuận gộp","Giá vốn","Doanh thu","ký gửi","ngành","chuỗi","kênh","a9","a20","SP mới"]:
    C.append(("BA","meaning",f"'{term}' nghĩa nghiệp vụ là gì?","meaning",term))
# D. IMPACT (Data Engineer / BI Dev)
for tbl in ["DW_NS_CUSTOMER_INVOICE_LINES_F","DW_NS_X_GIA_VON_MUC_TIEU_CT","DW_NS_X_TRADE_PROMOTION_LINE","DW_NS_X_AOP_LINE_CF","DW_NS_X_SFC_LINES_CF","DW_NS_CLASSIFICATION_D","DW_NS_X_CAM_CUSTOMRECORD_CSEG_SCV_CHAIN","DW_NS_CUSTOMER_CREDIT_LINES_F"]:
    C.append(("Data Engineer","impact",f"Đổi bảng {tbl} thì viz/dataset nào gãy?","impact",tbl))
# E. BUILD/ADVISORY (Dashboard/Dataflow builder via orchestrator)
build=[("CFO","revenue","chuoi","ngày"),("CMO","ckkm","chuoi","tháng"),("Sales Head","revenue","asm","tháng"),
       ("Supply Chain Head","sfc","model","tháng"),("CEO","profit","nganh","kỳ"),("CFO","gross_profit","kenh","tháng"),
       ("Branch Head","revenue","don_vi","ngày"),("CMO","sp_moi","nganh","tháng")]
for p,m,d,g in build:
    C.append((p,"build",f"Build dashboard: {m} theo {d} ở grain {g} — dựng từ đâu?","source",m,d))
# F. GOVERNANCE / FRESHNESS / EDGE
C+=[
 ("CFO","governance","'Lợi nhuận' a9 là số thực hay ước tính?","doc_govt","ước tính"),
 ("Auditor","governance","a10 (CP xúc tiến) có phải số cứng không?","doc_govt","cứng"),
 ("Auditor","governance","Thuế tính thế nào (có hardcode)?","doc_govt","0.21"),
 ("CFO","governance","Doanh thu Tập đoàn loại trừ gì (subsidiary)?","doc_govt","whitelist"),
 ("Data Engineer","freshness","Làm sao biết KB còn khớp OAC (dataflow đổi)?","doc_live","Freshness"),
 ("Finance Analyst","freshness","Lấy SỐ hiện tại của 1 metric thế nào?","doc_live","executePreview"),
 ("BA","edge","Hỏi về workbook NGOÀI 4 cái thì sao?","doc_ex","ngoài-4"),
 ("CTO","precedence","OAC và NSAW mâu thuẫn thì tin ai?","doc_ext","OAC"),
 ("CTO","precedence","Báo cáo vs dashboard lệch số thì theo cái nào?","doc_ext","báo cáo"),
 ("Data Engineer","pitfall","Re-aggregate %GP từ hub có đúng không?","doc_play","KHÔNG SUM"),
 ("Data Engineer","pitfall","COGS join GVMT có bẫy gì?","doc_play","fan-out"),
 ("Supply Chain Head","source","SFC ước tính lấy dataset nào (authoritative)?","doc_glo","DTF_CALC_MIS"),
 ("CMO","build","Cần ROI khuyến mãi (CKKM) theo chuỗi — khả thi?","source","ckkm","chuoi"),
 ("CEO","meaning","Tỷ lệ Xanh/Đỏ là gì, tính sao?","doc_glo","Xanh"),
 ("Branch Head","source","Doanh thu theo tỉnh/thành?","source","revenue","tinh"),
]

def evaluate(kind,*a):
    if kind=="trace": return ev_trace(*a)
    if kind=="source": return ev_source(*a)
    if kind=="meaning": return ev_meaning(*a)
    if kind=="impact": return ev_impact(*a)
    if kind=="doc_govt": return ev_doc(a[0],GOVT+GLOT,"governance/glossary")
    if kind=="doc_live": return ev_doc(a[0],LIVE,"live_query_recipes")
    if kind=="doc_ex": return ev_doc(a[0],EXAMPLES,"examples")
    if kind=="doc_ext": return ev_doc(a[0],rd("external/README.md"),"external/README")
    if kind=="doc_play": return ev_doc(a[0],PLAYBOOK,"playbook")
    if kind=="doc_glo": return ev_doc(a[0],GLOT,"glossary")
    return "GAP","unknown kind"

res=[]
for i,(persona,cat,q,kind,*a) in enumerate(C,1):
    st,ev=evaluate(kind,*a); res.append((i,persona,cat,q,st,ev))

from collections import Counter
cnt=Counter(r[4] for r in res)
gaps=[r for r in res if r[4]=="GAP"]; partials=[r for r in res if r[4]=="PARTIAL"]
# REPORT
L=["# QA_USECASES_REPORT — 100+ ca dùng theo góc nhìn leaders","",
   f"Tổng {len(res)} ca · PASS={cnt['PASS']} · PARTIAL={cnt['PARTIAL']} · GAP={cnt['GAP']}",""]
cur=None
for i,p,cat,q,st,ev in res:
    if cat!=cur: L.append(f"\n## {cat}"); cur=cat
    mark={"PASS":"✅","PARTIAL":"🟡","GAP":"❌"}[st]
    L.append(f"- {mark} [{p}] {q} → {ev}")
open(os.path.join(KB,"QA_USECASES_REPORT.md"),"w",encoding="utf-8").write("\n".join(L))
# IMPROVEMENTS
I=["# IMPROVEMENTS — tổng hợp từ 100+ use-case (gap + partial)","",
   f"PASS {cnt['PASS']}/{len(res)}. Dưới đây là điểm cần cải thiện (GAP) + cần lưu ý (PARTIAL).",""]
I.append("## GAP (KB chưa trả lời được)")
if gaps:
    for i,p,cat,q,st,ev in gaps: I.append(f"- ❌ [{cat}/{p}] {q} — {ev}")
else: I.append("- (không có GAP)")
I.append("\n## PARTIAL (trả lời được nhưng cần build/lưu ý)")
seen=set()
for i,p,cat,q,st,ev in partials:
    key=(cat,ev)
    if key in seen: continue
    seen.add(key); I.append(f"- 🟡 [{cat}] {q} — {ev}")
I.append("\n## Khuyến nghị cải thiện (rút ra)")
I+=[ "- Mọi 'cần M theo D' chưa cùng dataset → là cơ hội DỰNG dataflow mới từ hub (orchestrator O1 lập kế hoạch).",
     "- Chiều chưa index trong capability_map (nếu có) → bổ sung index hoặc ghi rõ 'build từ hub'.",
     "- Metric thiếu hẳn (GAP source) → cân nhắc bổ sung vào glossary/capability hoặc nói rõ 'chưa build trong OAC'.",
     "- PARTIAL nhiều ở 1 chiều → ưu tiên dựng sẵn dataset chiều đó nếu hỏi thường xuyên."]
open(os.path.join(KB,"IMPROVEMENTS.md"),"w",encoding="utf-8").write("\n".join(I))
print(f"Tổng {len(res)} ca · PASS={cnt['PASS']} PARTIAL={cnt['PARTIAL']} GAP={cnt['GAP']}")
print("GAPs:"); [print("  ❌",r[3],"→",r[5]) for r in gaps[:30]] or print("  (none)")
