# -*- coding: utf-8 -*-
"""QA TOÀN DIỆN — catalog/function/code/script/orchestrator/architecture.
Durable: ghi QA_REPORT.md. Chạy: PYTHONUTF8=1 PYTHONIOENCODING=utf-8 python raw/qa_full.py
Mỗi section guarded. Exit 1 nếu có FAIL (WARN/SKIP không fail)."""
import os, sys, re, json, subprocess, glob, traceback
import yaml

HERE = os.path.dirname(os.path.abspath(__file__))          # OAC-Knowledge/raw
def _first(paths, default):
    return next((p for p in paths if p and os.path.isdir(p)), default)
KB   = os.environ.get("OAC_KB_ROOT") or os.path.dirname(HERE)        # OAC-Knowledge
WS   = os.environ.get("KGR_ROOT") or os.path.dirname(KB)            # workspace (chứa các repo)
ORCH = os.path.join(WS, "OAC-Orchestrator")
STG  = _first([os.environ.get("OAC_STAGING"), os.path.join(KB, "_work", "staging"), os.path.join(WS, "Dashboard-builder", "_oac_extract")], os.path.join(KB, "_work", "staging"))
SK   = os.path.join(KB, "skill", "kgr-oac-lineage", "scripts")
SKILLS = os.path.join(os.path.expanduser("~"), ".claude", "skills")  # cài skill theo user-home (portable cross-máy)
ENV  = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8")
SECRET = re.compile("Hanoi@" + r"\d{4,}")  # ghép từ mảnh: file này KHÔNG chứa literal mật khẩu

R = []
def t(sec, tid, cond, detail=""):  R.append((sec, tid, "PASS" if cond else "FAIL", detail))
def tw(sec, tid, cond, detail=""): R.append((sec, tid, "PASS" if cond else "WARN", detail))
def ts(sec, tid, detail=""):       R.append((sec, tid, "SKIP", detail))

def Y(p):
    with open(p, encoding="utf-8") as f: return yaml.safe_load(f)
def J(p):
    with open(p, encoding="utf-8") as f: return json.load(f)
def run(cmd, cwd=None):
    try:
        p = subprocess.run(cmd, cwd=cwd, env=ENV, capture_output=True, text=True, encoding="utf-8", timeout=180)
        return p.returncode, (p.stdout or "") + (p.stderr or "")
    except Exception as e:
        return -99, f"EXC {e}"

cat = {}
for name in ["workbook_catalog","dataset_catalog","dataflow_catalog","physical_table_catalog","lineage_graph","field_dictionary","business_glossary","capability_map"]:
    try: cat[name] = Y(os.path.join(KB, name+".yaml"))
    except Exception as e: cat[name] = None; t("LOAD","load_"+name, False, str(e)[:80])
WB=(cat.get("workbook_catalog") or {}).get("workbooks",{})
DS=(cat.get("dataset_catalog") or {}).get("datasets",{})
DF=(cat.get("dataflow_catalog") or {}).get("dataflows",{})
PH=(cat.get("physical_table_catalog") or {}).get("physical_tables",{})
LIN=cat.get("lineage_graph") or {}
FD=(cat.get("field_dictionary") or {}).get("datasets",{})
GLO=cat.get("business_glossary") or {}
CAP=cat.get("capability_map") or {}

# ===== S1 catalog deep consistency =====
try:
    bad=[f"{dsn}<-{f}" for dsn,r in DS.items() for f in (r.get("produced_by_dataflows") or []) if dsn not in ((DF.get(f) or {}).get("output_datasets") or [])]
    t("S1","1.1_produced_by_bidirectional", not bad, f"{len(bad)}: {bad[:3]}")
    bad=[f"{f}->{o}" for f,r in DF.items() for o in (r.get("output_datasets") or []) if o not in DS]
    t("S1","1.2_df_outputs_exist", not bad, f"{len(bad)}: {bad[:3]}")
    miss=sorted({i for f,r in DF.items() for i in (r.get("input_datasets") or []) if i not in DS})
    tw("S1","1.3_df_inputs_known", not miss, f"{len(miss)} input lạ: {miss[:5]}")
    titles=set(WB.keys()); bad=[f"{dsn}:{w}" for dsn,r in DS.items() for w in (r.get("used_by_workbooks") or []) if w not in titles]
    t("S1","1.4_used_by_wb_titles", not bad, f"{bad[:3]}")
    fwd={}
    for e in LIN.get("edges",[]): fwd.setdefault(e.get("from"),[]).append(e.get("to"))
    seen=set(); stack=[n for n in fwd if str(n).startswith("workbook:")]
    while stack:
        n=stack.pop()
        if n in seen: continue
        seen.add(n); stack+=fwd.get(n,[])
    unreach=[dsn for dsn,r in DS.items() if r.get("in_closure") and f"dataset:{dsn}" not in seen]
    t("S1","1.5_closure_reachable", not unreach, f"{len(unreach)}: {unreach[:5]}")
except Exception: t("S1","S1_exception", False, traceback.format_exc()[-200:])

# ===== S2 resolver/field_dictionary correctness =====
# Tầng re-derive công thức TỪ RAW (oracle độc lập). Phụ thuộc raw extract gitignored
# (_work/staging/raw/dataflows_all.json). Trên clone sạch không có file → SKIP tường minh
# (không FAIL khó hiểu): chạy raw/REBUILD để bật. Xem QA review M3.
try:
    RAW_DF = os.path.join(STG, "raw", "dataflows_all.json")
    if not os.path.exists(RAW_DF):
        ts("S2", "2.skipped_no_raw_extract", f"thiếu raw extract ({RAW_DF}) — gitignored; chạy raw/REBUILD để bật re-derivation công thức từ raw")
    else:
        sys.path.insert(0, STG)
        import resolver as RS
        def raw_add(flow_sub,col):
            for fid,jj in RS.ALL.items():
                if flow_sub in fid:
                    for s in (jj.get("definition") or {}).get("steps",[]):
                        if s.get("type")=="AddColumns":
                            for c in s.get("columns",[]):
                                if c.get("name")==col: return (c.get("expression") or "").replace(" ","")
            return None
        for dsn,flow,col in [("TD_Metrics_Wide","KGR_DF_TD_Metrics_bk","a9"),("TD_Metrics_Wide","KGR_DF_TD_Metrics_bk","a4"),("TD_Metrics_Wide","KGR_DF_TD_Metrics_bk","a20")]:
            raw=raw_add(flow,col); fdv=((FD.get(dsn) or {}).get("columns") or {}).get(col,{}).get("direct_formula","")
            t("S2",f"2.derive_{col}", bool(raw) and raw==fdv.replace(" ",""), "raw!=fd" if raw!=fdv.replace(" ","") else "")
        rev=((FD.get("(KGR) DTF_CALC_INVOICE_MEMO_#") or {}).get("columns") or {}).get("Doanh thu thực tế",{}); pr=set(rev.get("physical_roots") or [])
        t("S2","2.revenue_roots", "DW_NS_CUSTOMER_INVOICE_LINES_F.BASE_REVENUE" in pr and "DW_NS_CUSTOMER_CREDIT_LINES_F.BASE_REVENUE" in pr, "")
        cogs=((FD.get("(KGR) DTF_CALC_INVOICE_MEMO_#") or {}).get("columns") or {}).get("Giá Vốn",{}); cr=set(cogs.get("physical_roots") or [])
        t("S2","2.cogs_3tier", any("GIA_VON_MUC_TIEU" in x for x in cr) and any("GIA_VON_TON_KHO" in x for x in cr), "")
except Exception: t("S2","S2_exception", False, traceback.format_exc()[-200:])

# ===== S3 scripts behavior =====
try:
    rc,o=run([sys.executable, os.path.join(SK,"trace_field.py"),"Doanh thu"]); t("S3","3.trace_match", rc==0 and ("dataset:" in o or "DTF_CALC" in o), o[:60])
    rc,o=run([sys.executable, os.path.join(SK,"trace_field.py"),"a9"]); t("S3","3.trace_fd_fallback", rc==0 and "physical_roots" in o and "BASE_REVENUE" in o, o[:60])
    rc,o=run([sys.executable, os.path.join(SK,"trace_field.py"),"zzz_nope_xyz"]); t("S3","3.trace_nomatch_graceful", rc==0, o[:60])
    rc,o=run([sys.executable, os.path.join(SK,"find_source.py"),"revenue","chuoi"]); t("S3","3.find_hub", rc==0 and "DTF_CALC_INVOICE_MEMO_#" in o, o[:60])
    rc,o=run([sys.executable, os.path.join(SK,"find_source.py"),"revenue","asm"]); t("S3","3.find_asm", rc==0 and ("SALE HIST" in o or "SALE_HISTORY" in o.replace(" ","_")), o[:60])
    rc,bid=run([sys.executable, os.path.join(ORCH,"scripts","blackboard.py"),"new","qa-test","T5-2026"]); bid=(bid.strip().splitlines() or [""])[-1]
    rc2,_=run([sys.executable, os.path.join(ORCH,"scripts","blackboard.py"),"set",bid,"phase",'"verify"'])
    rc3,g=run([sys.executable, os.path.join(ORCH,"scripts","blackboard.py"),"get",bid])
    t("S3","3.blackboard_roundtrip", bid.startswith("bb_") and rc2==0 and rc3==0 and '"verify"' in g and "O1-readonly" in g, f"bid={bid}")
    try: os.remove(os.path.join(ORCH,"blackboards",bid+".json"))
    except: pass
    rc,o1=run([sys.executable, os.path.join(ORCH,"lock.py"),"acquire","QA_WB","A","60"])
    rc2,o2=run([sys.executable, os.path.join(ORCH,"lock.py"),"acquire","QA_WB","B","60"])
    rc3,o3=run([sys.executable, os.path.join(ORCH,"lock.py"),"release","QA_WB","A"])
    t("S3","3.lock_contention", "ACQUIRED" in o1 and rc2==1 and "LOCKED" in o2 and "RELEASED" in o3, f"{o2[:24]}")
except Exception: t("S3","S3_exception", False, traceback.format_exc()[-200:])

# ===== S4 encoding (content files) =====
try:
    moji=re.compile(r"Ã[\x80-\xbf]|â€|á»|áº"); bad=[]
    for root in [KB,ORCH]:
        for dp,_,fs in os.walk(root):
            if os.sep+".git" in dp: continue
            for fn in fs:
                if not fn.endswith((".yaml",".md",".json")): continue
                p=os.path.join(dp,fn)
                try: s=open(p,encoding="utf-8",errors="strict").read()
                except UnicodeDecodeError: bad.append(fn+":NON-UTF8"); continue
                if "�" in s: bad.append(fn+":FFFD")
                elif moji.search(s): bad.append(fn+":moji")
    t("S4","4.encoding_content_files", not bad, f"{len(bad)}: {bad[:5]}")
except Exception: t("S4","S4_exception", False, traceback.format_exc()[-200:])

# ===== S5 no cached money =====
try:
    money=re.compile(r"\d{1,3}(?:[.,]\d{3}){2,}|\b\d+\s*(?:tỷ|triệu)\b"); allow=("247","governance","cứng","hardcode"); hits=[]
    for fn in ["dataset_catalog.yaml","dataflow_catalog.yaml","physical_table_catalog.yaml","capability_map.yaml","business_glossary.yaml","field_dictionary.yaml"]:
        for i,ln in enumerate(open(os.path.join(KB,fn),encoding="utf-8"),1):
            for m in money.findall(ln):
                if any(a in ln for a in allow): continue
                if any(k in ln for k in ["formula","expression","derivation","filters","joins","direct_formula","="," / ",">"]): continue
                hits.append(f"{fn}:{i}")
    t("S5","5.no_cached_money", not hits, f"{len(hits)}: {hits[:3]}")
except Exception: t("S5","S5_exception", False, traceback.format_exc()[-200:])

# ===== S6 orchestrator =====
try:
    ac=Y(os.path.join(ORCH,"agent_contracts.yaml")); agents=ac.get("agents",{})
    t("S6","6.contracts_3_agents", set(agents.keys())=={"kgr-oac-lineage","oac-dataflow-builder","oac-dashboard-builder"}, str(list(agents.keys())))
    miss=[a for a,r in agents.items() if not (r.get("owns") and r.get("must_not"))]
    t("S6","6.contracts_fields", not miss, str(miss))
    t("S6","6.nsaw_backend", "nsaw-knowledge" not in agents and "nsaw-knowledge" in (ac.get("backends") or {}), "")
    bt=J(os.path.join(ORCH,"blackboard.template.json")); t("S6","6.bb_template", "period" in bt and "verdicts" in bt and "kb_freshness" in bt, "")
    bs=J(os.path.join(ORCH,"blackboard_schema.json")); t("S6","6.bb_schema", "fields" in bs, "")
    fours=[os.path.basename(fn) for fn in glob.glob(os.path.join(ORCH,"*.md")) if re.search(r"4\s*agent", open(fn,encoding="utf-8").read(), re.I)]
    t("S6","6.no_4agent_stray", not fours, str(fours))
except Exception: t("S6","S6_exception", False, traceback.format_exc()[-200:])

# ===== S7 architecture / git / skill-sync =====
try:
    pm=(cat.get("physical_table_catalog") or {}).get("_meta",{})
    t("S7","7.physical_count", pm.get("total_tables")==len(PH), f"meta={pm.get('total_tables')} actual={len(PH)}")
    t("S7","7.workbooks_4", len(WB)==4, str(len(WB)))
    def same(a,b):
        try: return open(a,encoding="utf-8").read()==open(b,encoding="utf-8").read()
        except: return False
    t("S7","7.lineage_skill_synced", same(os.path.join(KB,"skill","kgr-oac-lineage","SKILL.md"), os.path.join(SKILLS,"kgr-oac-lineage","SKILL.md")), "")
    t("S7","7.orch_skill_synced", same(os.path.join(ORCH,"skill","kgr-oac-orchestrator","SKILL.md"), os.path.join(SKILLS,"kgr-oac-orchestrator","SKILL.md")), "")
    t("S7","7.validate_synced", same(os.path.join(SK,"validate_kb.py"), os.path.join(SKILLS,"kgr-oac-lineage","scripts","validate_kb.py")), "")
    for d in ["OAC-Knowledge","OAC-Orchestrator","Dashboard-builder","Dataflow-builder"]:
        rc,o=run(["git","ls-files"], cwd=os.path.join(WS,d)); bad=False
        for f in o.splitlines():
            try:
                if f and SECRET.search(open(os.path.join(WS,d,f),encoding="utf-8",errors="ignore").read()): bad=True; break
            except: pass
        t("S7",f"7.git_{d}_no_secret", not bad, "")
except Exception: t("S7","S7_exception", False, traceback.format_exc()[-200:])

# ===== S8 fold validate_kb + qa_tests =====
try:
    rc,o=run([sys.executable, os.path.join(SK,"validate_kb.py")]); t("S8","8.validate_kb", bool(re.search(r"RESULT: 0 ERROR", o)), (o.strip().splitlines() or [""])[-1])
    rc,o=run([sys.executable, os.path.join(KB,"raw","qa_tests.py")]); m=re.search(r"TOTAL: (\d+) PASS / (\d+) FAIL", o); t("S8","8.qa_tests", bool(m) and m.group(2)=="0", m.group(0) if m else "no-total")
except Exception: t("S8","S8_exception", False, traceback.format_exc()[-200:])

# ===== S9 completeness/typing/counts =====
try:
    bad=[]
    for dsn,r in DS.items():
        ty=r.get("type")
        if ty=="dataflow_output" and not r.get("produced_by_dataflows"): bad.append(f"{dsn}:no-producer")
        if ty=="db_dataset" and r.get("in_closure") and not (r.get("physical_tables") or r.get("file_or_other_sources") or r.get("note") or r.get("internal_joins_filters")): bad.append(f"{dsn}:no-source")
    t("S9","9.1_typing_closure", not bad, f"{bad[:4]}")
    noout=[f for f,r in DF.items() if not r.get("output_datasets")]
    tw("S9","9.2_dataflow_output", not noout, f"{len(noout)} no-output (archive cand, OK): {noout}")
    bad=[]
    for tn,r in PH.items():
        if not r.get("columns_in_use"): bad.append(tn+":no-cols")
        if not r.get("nsaw_claude_ref"): bad.append(tn+":no-ref")
        if not (r.get("used_by_dataflows") or r.get("used_by_datasets")): bad.append(tn+":no-usedby")
    t("S9","9.3_physical_complete", not bad, f"{bad[:4]}")
    bm=CAP.get("by_metric",{}); bd=CAP.get("by_dimension",{}); cds=CAP.get("datasets",{})
    t("S9","9.4_capability", bool(bm) and bool(bd) and bool(cds), f"by_metric={len(bm)} by_dim={len(bd)}")
    codes=set((GLO.get("pnl_waterfall_codes") or {}).keys()); need={f"a{i}" for i in range(1,21)}; missing=need-codes-{"a22","a23"}
    t("S9","9.5_glossary_codes", len(missing)<=2 and bool(GLO.get("core_metrics")), f"missing={sorted(missing)}")
    dsnames=list(DS.keys()); badsrc=[k for k,m in (GLO.get("core_metrics") or {}).items() if m.get("authoritative_source") and not any(dn in m["authoritative_source"] for dn in dsnames)]
    tw("S9","9.5b_glossary_src", not badsrc, f"{badsrc}")
    qr=open(os.path.join(KB,"QUICK_REFERENCE.md"),encoding="utf-8").read(); drift=[]
    for word,n in [("dataset",len(DS)),("dataflow",len(DF))]:
        nums=set(int(x) for x in re.findall(r"\*{0,2}(\d+)\*{0,2}\s*"+word, qr))
        if nums and n not in nums: drift.append(f"{word}:{sorted(nums)}≠{n}")
    tw("S9","9.6_count_consistency", not drift, f"{drift}")
    medge=re.search(r"\*{0,2}(\d+)\*{0,2}\s*lineage edge", qr)
    tw("S9","9.6c_edge_count", bool(medge) and int(medge.group(1))==len(LIN.get("edges",[])), f"doc={medge.group(1) if medge else None} actual={len(LIN.get('edges',[]))}")
    # snapshot counts — CẬP NHẬT khi refresh catalog (⑥ 2026-07-06: ds 63→67, df 40→36 sau khi bỏ 12 zombie + thêm 8)
    t("S9","9.6b_counts_regression", len(DS)==67 and len(DF)==36 and len(PH)==60, f"{len(DS)}/{len(DF)}/{len(PH)}")
    term=set(LIN.get("terminal_physical_nodes",[])); badterm=[x for x in term if x.replace("physical:","") not in PH]
    t("S9","9.7_lineage_terminals", not badterm, f"{badterm[:4]}")
except Exception: t("S9","S9_exception", False, traceback.format_exc()[-200:])

# ===== S10 doc-link integrity =====
try:
    bad=[]; ref_re=re.compile(r"`?([A-Za-z0-9_\-/]+\.(?:yaml|md|py))`?")
    NSAW=os.environ.get("NSAW_CLAUDE_ROOT") or _first([os.path.join(WS,"NSAW_Claude","data_context"), os.path.join(os.path.dirname(WS),"NSAW_Claude","data_context")], os.path.join(WS,"NSAW_Claude","data_context"))
    md_files=[f for f in glob.glob(os.path.join(KB,"*.md")) if os.path.basename(f)!="QA_REPORT.md"]+[os.path.join(KB,"skill","kgr-oac-lineage","SKILL.md")]+glob.glob(os.path.join(KB,"skill","kgr-oac-lineage","references","*.md"))
    for mf in md_files:
        try: s=open(mf,encoding="utf-8").read()
        except: continue
        for ref in set(ref_re.findall(s)):
            try:
                if ref.startswith("http") or ".secrets" in ref or len(ref)>120: continue
                bn=os.path.basename(ref)
                cands=[os.path.join(KB,ref),os.path.join(os.path.dirname(mf),ref),os.path.join(KB,"skill","kgr-oac-lineage",ref),os.path.join(KB,"skill","kgr-oac-lineage","scripts",bn),os.path.join(KB,"raw",bn),os.path.join(KB,"fields",bn),
                       os.path.join(NSAW,bn),os.path.join(ORCH,bn),os.path.join(ORCH,"scripts",bn)]  # cross-repo refs hợp lệ
                ok=any(os.path.exists(c) for c in cands)
            except: ok=True
            if not ok and (ref.endswith(".yaml") or bn in ("validate_kb.py","trace_field.py","find_source.py","build_catalogs.py","qa_tests.py","decode_double_json.py","find_source.py")):
                bad.append(f"{os.path.basename(mf)}→{ref}")
    tw("S10","10.doc_links_exist", not bad, f"{bad[:6]}")
except Exception: t("S10","S10_exception", False, traceback.format_exc()[-200:])

# ===== S11 script edge cases =====
try:
    rc,o=run([sys.executable, os.path.join(SK,"find_source.py")]); t("S11","11.find_usage", "Usage" in o or "concept" in o, o[:50])
    rc,o=run([sys.executable, os.path.join(ORCH,"scripts","blackboard.py"),"get","bb_nope"]); t("S11","11.bb_get_missing", rc!=0 or "Errno" in o or "No such" in o, "no-crash")
    rc,o=run([sys.executable, os.path.join(ORCH,"lock.py"),"status","NEVER"]); t("S11","11.lock_status_missing", rc==0 and ("null" in o or "None" in o), o[:30])
    rc,o=run([sys.executable, os.path.join(SK,"validate_kb.py")], cwd=WS); t("S11","11.validate_root_resolve", "RESULT" in o, "")
except Exception: t("S11","S11_exception", False, traceback.format_exc()[-200:])

# ===== S12 ops hygiene =====
try:
    t("S12","12.precommit_hook", os.path.exists(os.path.join(WS,".git","hooks","pre-commit")) or os.path.exists(os.path.join(KB,".git","hooks","pre-commit")), "")
    gi=open(os.path.join(KB,".gitignore"),encoding="utf-8").read(); t("S12","12.gitignore_rules", ".secrets" in gi and "raw/" in gi, "")
    leak=[]
    for d in ["OAC-Knowledge","OAC-Orchestrator","Dashboard-builder","Dataflow-builder"]:
        rc,o=run(["git","ls-files"], cwd=os.path.join(WS,d))
        if any(".secrets" in ln or ln.endswith(".env") for ln in o.splitlines()): leak.append(d)
    t("S12","12.secrets_untracked", not leak, str(leak))
    t("S12","12.secret_store_exists", any(os.path.exists(os.path.join(b,".secrets","oac.env")) for b in [WS, os.path.dirname(WS)]), "")
except Exception: t("S12","S12_exception", False, traceback.format_exc()[-200:])

# ===== S13 cross-file integrity =====
try:
    # 13.1 glossary pnl-code formula KHỚP field_dictionary (TD_Metrics_Wide)
    codes=GLO.get("pnl_waterfall_codes") or {}; wcols=((FD.get("TD_Metrics_Wide") or {}).get("columns") or {})
    mismatch=[]
    for code in ["a4","a9","a20"]:
        gf=(codes.get(code) or {}).get("formula","")
        ff=(wcols.get(code) or {}).get("direct_formula","")
        if gf and ff:
            norm=lambda s: re.sub(r'\s+','',s).replace('"','').replace("−","-").replace("–","-")
            if norm(gf)!=norm(ff): mismatch.append(f"{code}: glo!=fd")
    t("S13","13.1_glossary_fd_formula_match", not mismatch, f"{mismatch}")
    # 13.3 type non-contradiction: db_dataset không có produced_by
    bad=[dsn for dsn,r in DS.items() if r.get("type")=="db_dataset" and r.get("produced_by_dataflows")]
    t("S13","13.3_type_no_contradiction", not bad, f"{bad[:4]}")
    # 13.5 field_dictionary dataset keys ⊆ dataset_catalog
    bad=[k for k in FD if k not in DS]
    t("S13","13.5_fd_keys_in_dscat", not bad, f"{bad[:4]}")
    # 13.6 capability_map.datasets keys ⊆ dataset_catalog
    bad=[k for k in (CAP.get("datasets") or {}) if k not in DS]
    t("S13","13.6_cap_keys_in_dscat", not bad, f"{bad[:4]}")
    # 13.7 archive_recommendations tồn tại + mention ARCHIVE + KHÔNG dựa tên version
    ar=open(os.path.join(KB,"archive_recommendations.md"),encoding="utf-8").read()
    t("S13","13.7_archive_doc", "ARCHIVE" in ar and ("version" in ar or "v2/v3" in ar) and len(ar)>500, "")
    # 13.8 mọi 'shown_as' field trỏ workbook có thật
    titles=set(WB.keys()); bad=[]
    for dsn,r in FD.items():
        for c,e in (r.get("columns") or {}).items():
            if isinstance(e,dict):
                for sa in (e.get("shown_as") or []):
                    if sa.get("workbook") not in titles: bad.append(f"{dsn}.{c}")
    t("S13","13.8_shown_as_wb_real", not bad, f"{bad[:4]}")
    # 13.9 field_dictionary physical_roots (bảng DW) ⊆ physical_table_catalog (validate_kb chỉ kiểm dataset.physical_tables, bỏ sót fd roots)
    rb=set()
    for dsn,r in FD.items():
        for c,e in (r.get("columns") or {}).items():
            if isinstance(e,dict):
                for pr in (e.get("physical_roots") or []):
                    tb=str(pr).split(".")[0]
                    if tb.startswith("DW") and tb not in PH: rb.add(tb)
    t("S13","13.9_fd_roots_in_phys", not rb, f"{sorted(rb)[:4]}")
except Exception: t("S13","S13_exception", False, traceback.format_exc()[-200:])

# ===== REPORT =====
from collections import Counter
cnt=Counter(s for _,_,s,_ in R)
lines=["# QA_REPORT — toàn diện","",f"PASS={cnt['PASS']} FAIL={cnt['FAIL']} WARN={cnt['WARN']}  (tổng {len(R)})",""]
cur=None
for sec,tid,st,det in R:
    if sec!=cur: lines.append(f"\n## {sec}"); cur=sec
    mark={"PASS":"✅","FAIL":"❌","WARN":"⚠️","SKIP":"⏭️"}[st]
    lines.append(f"- {mark} `{tid}`"+(f" — {det}" if det and st!="PASS" else ""))
open(os.path.join(KB,"QA_REPORT.md"),"w",encoding="utf-8").write("\n".join(lines))
print("\n".join(f"{st} {sec}/{tid} {det if st!='PASS' else ''}" for sec,tid,st,det in R if st!="PASS") or "ALL PASS")
print(f"\nPASS={cnt['PASS']} FAIL={cnt['FAIL']} WARN={cnt['WARN']} (tổng {len(R)})")
sys.exit(1 if cnt["FAIL"] else 0)
