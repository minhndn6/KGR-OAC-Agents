#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""learn.py — cơ chế HỌC/tích lũy tri thức cho consultant.
Append-only log các fact/correction/gap/qa phát hiện khi làm việc → review → promote vào KB.
Usage:
  learn.py add <type> "<topic>" "<content>" ["<source>"] ["<confidence>"]
      type: fact | correction | gap | qa | lesson
  learn.py list [status]            # status: pending|promoted|all (default all)
  learn.py promote <id> ["<note>"]  # đánh dấu đã đưa vào KB
  learn.py pending                  # regenerate learnings/pending.md
KHÔNG lưu số tuyệt đối (data live). Ghi CÁCH/quan hệ/bài học."""
import os, sys, json, time, re
from pathlib import Path

_KB_MARKER = ".kgr_kb_root"
def _is_kb(p):
    try: return (Path(p)/_KB_MARKER).is_file()
    except Exception: return False
def _kb_registry():
    base = os.environ.get("KGR_RUNTIME_DIR") or os.environ.get("LOCALAPPDATA")
    if base: return Path(base)/"kgr-oac"/"kb_root.txt"
    return Path(os.path.expanduser("~"))/".kgr"/"kb_root.txt"
def kb_root():
    # INV-1: resolve KB root DUY NHẤT + tường minh; KHÔNG hardcode fallback mù.
    # Spec + test: kb_lifecycle/tools/kb_paths.py, kb_lifecycle/tests/test_kbroot.py.
    e = os.environ.get("OAC_KB_ROOT")
    if e:
        if _is_kb(e): return Path(e)
        raise SystemExit(f"OAC_KB_ROOT={e} thiếu marker {_KB_MARKER} — KB không hợp lệ.")
    cur = Path(__file__).resolve()                 # walk-up: đúng cho bản trong-repo
    for anc in (cur, *cur.parents):
        if _is_kb(anc): return anc
    reg = _kb_registry()                            # registry: đúng cho bản cài ~/.claude/skills
    if reg.is_file():
        cand = reg.read_text(encoding="utf-8").strip()
        if cand and _is_kb(cand): return Path(cand)
    raise SystemExit("Không xác định được KB root (đặt OAC_KB_ROOT hoặc chạy `kgr setup`). "
                     "Đã bỏ fallback C:\\Project\\OAC-Knowledge (chống split-brain).")
KB=kb_root(); LD=KB/"learnings"; LOG=LD/"log.jsonl"
def _now(): return time.strftime("%Y-%m-%dT%H:%M:%S")

def _read():
    if not LOG.exists(): return []
    return [json.loads(l) for l in open(LOG,encoding="utf-8") if l.strip()]
def _append(rec):
    LD.mkdir(exist_ok=True)
    with open(LOG,"a",encoding="utf-8") as f: f.write(json.dumps(rec,ensure_ascii=False)+"\n")

def add(typ,topic,content,source="",conf="medium"):
    recs=_read(); nid=f"L{len(recs)+1:04d}"
    if re.search(r"\d{1,3}(?:[.,]\d{3}){2,}|\b\d+\s*(?:tỷ|triệu)\b", content):
        print("⚠️ Cảnh báo: content có vẻ chứa SỐ tuyệt đối — KB không lưu số (data live). Ghi CÁCH tính thay vì giá trị.")
    rec={"id":nid,"ts":_now(),"type":typ,"topic":topic,"content":content,"source":source,"confidence":conf,"status":"pending"}
    _append(rec); print(nid)

def lst(status="all"):
    for r in _read():
        if status=="all" or r.get("status")==status:
            print(f"{r['id']} [{r['status']}] {r['type']}: {r['topic']} — {r['content'][:80]}")

def promote(rid,note=""):
    recs=_read(); found=False
    for r in recs:
        if r["id"]==rid: r["status"]="promoted"; r["promote_note"]=note; r["promoted_ts"]=_now(); found=True
    if found:
        with open(LOG,"w",encoding="utf-8") as f:
            for r in recs: f.write(json.dumps(r,ensure_ascii=False)+"\n")
        print(f"{rid} → promoted")
    else: print(f"{rid} không thấy")

def pending():
    recs=[r for r in _read() if r.get("status")=="pending"]
    lines=["# Pending learnings — chờ review & promote vào KB","",
           "> Quy trình: review → cập nhật file KB phù hợp (catalog/glossary/CONFLICTS) + CHANGELOG → `learn.py promote <id>`.",""]
    for r in recs:
        lines.append(f"- **{r['id']}** ({r['type']}, tin:{r['confidence']}) — **{r['topic']}**: {r['content']}"+(f"  _(nguồn: {r['source']})_" if r.get('source') else ""))
    (LD).mkdir(exist_ok=True)
    open(LD/"pending.md","w",encoding="utf-8").write("\n".join(lines))
    print(f"{len(recs)} pending → learnings/pending.md")

if __name__=="__main__":
    a=sys.argv
    if len(a)<2: print(__doc__); sys.exit(2)
    if a[1]=="add" and len(a)>=5: add(a[2],a[3],a[4], a[5] if len(a)>5 else "", a[6] if len(a)>6 else "medium")
    elif a[1]=="list": lst(a[2] if len(a)>2 else "all")
    elif a[1]=="promote" and len(a)>=3: promote(a[2], a[3] if len(a)>3 else "")
    elif a[1]=="pending": pending()
    else: print(__doc__); sys.exit(2)
