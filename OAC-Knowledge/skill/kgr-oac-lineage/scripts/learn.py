#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""learn.py — [DEPRECATED] SHIM forward sang learn2 (governance).

Bản THẬT của cơ chế học giờ là `kb_lifecycle/tools/learn2.py` (typed-gate, content_hash,
fact_key, dedup, supersede, chặn SỐ-CỨNG theo type — A5). File này GIỮ LẠI vì bản cài
`~/.claude/skills/kgr-oac-lineage/scripts/learn.py` vẫn được skill gọi; nó KHÔNG nhân bản
logic cũ nữa mà FORWARD mọi lệnh sang learn2. Nếu KHÔNG import được learn2 -> in cảnh báo
rõ + exit≠0 (KHÔNG âm thầm quay lại logic learn.py cũ).

Usage (ngữ nghĩa learn2):
  learn.py add <type> "<topic>" "<content>" ["<source>"] ["<confidence>"]
  learn.py list [status]
  learn.py promote <id> ["<evidence-json>"]   # typed-gate của learn2 (cần rebuild_sha/live_evidence/...)
  learn.py pending                             # regenerate learnings/pending.md
KHÔNG lưu số tuyệt đối (data live). Ghi CÁCH/quan hệ/bài học."""
import os, sys
from pathlib import Path

_BANNER = "[DEPRECATED] learn.py → learn2 (governance)"

def _load_learn2():
    """Tìm & import learn2 từ kb_lifecycle/tools (repo HOẶC bản cài). Fail loud nếu không thấy."""
    here = Path(__file__).resolve()
    cands = []
    # 1) repo: skill/kgr-oac-lineage/scripts/learn.py -> ../../../kb_lifecycle/tools
    for anc in here.parents:
        t = anc / "kb_lifecycle" / "tools"
        if (t / "learn2.py").is_file():
            cands.append(t)
    # 2) env override cho bản cài (nếu workspace tools nằm chỗ khác)
    envtools = os.environ.get("KGR_TOOLS_DIR")
    if envtools and (Path(envtools) / "learn2.py").is_file():
        cands.insert(0, Path(envtools))
    for t in cands:
        p = str(t)
        if p not in sys.path:
            sys.path.insert(0, p)
        try:
            import learn2  # noqa: E402
            return learn2
        except Exception:
            continue
    return None


def main(argv):
    sys.stderr.write(_BANNER + "\n")
    L2 = _load_learn2()
    if L2 is None:
        sys.stderr.write(
            "[DEPRECATED][ERROR] Không import được learn2 (kb_lifecycle/tools/learn2.py). "
            "learn.py là SHIM, KHÔNG dùng logic cũ. Chạy từ repo hoặc đặt KGR_TOOLS_DIR trỏ tools/.\n")
        return 3
    a = argv
    if len(a) < 1:
        sys.stderr.write(__doc__ + "\n"); return 2
    cmd = a[0]
    # FORWARD sang learn2 (ngữ nghĩa governance: content_hash/fact_key/typed-gate/live_evidence).
    if cmd == "add" and len(a) >= 4:
        res = L2.add(a[1], a[2], a[3], a[4] if len(a) > 4 else "", a[5] if len(a) > 5 else "medium")
        import json as _j
        print(_j.dumps(res, ensure_ascii=False))
        return 0 if str(res.get("status", "")).lower() == "added" else 1
    if cmd == "list":
        L2.lst(a[1] if len(a) > 1 else "all"); return 0
    if cmd == "promote" and len(a) >= 2:
        import json as _j
        ev = {}
        if len(a) > 2:
            try: ev = _j.loads(a[2])
            except Exception: ev = {}
        res = L2.promote(a[1], ev)
        print(_j.dumps(res, ensure_ascii=False))
        return 0 if res.get("status") == "promoted" else 1
    if cmd == "pending":
        return _pending(L2)
    sys.stderr.write(__doc__ + "\n"); return 2


def _pending(L2):
    """Regenerate learnings/pending.md từ log của learn2 (giữ hành vi cũ, dùng path learn2)."""
    log = L2.default_log()
    recs = [r for r in L2._read(log) if r.get("status") == "pending"]
    lines = ["# Pending learnings — chờ review & promote vào KB", "",
             "> Quy trình: review → cập nhật file KB phù hợp (catalog/glossary/CONFLICTS) + CHANGELOG → "
             "`learn2.py promote <id> '<evidence-json>'` (typed-gate).", ""]
    for r in recs:
        src = f"  _(nguồn: {r['source']})_" if r.get("source") else ""
        lines.append(f"- **{r['id']}** ({r['type']}, tin:{r.get('confidence','?')}) — "
                     f"**{r['topic']}**: {r['content']}" + src)
    pend = Path(log).parent / "pending.md"
    pend.parent.mkdir(parents=True, exist_ok=True)
    pend.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{len(recs)} pending → learnings/pending.md")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
