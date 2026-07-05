#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""kb_gc — retention/GC cho state bền NGOÀI cây (_kgr-state). Giữ scratch/state khỏi phình vô hạn.

Chính sách (mặc định):
  • orchestration/tmp/*  &  _trash/*    → xóa nếu > tmp_days (7)
  • work/**/*.network-response, *.tmp   → xóa nếu > tmp_days
  • orchestration/blackboards/*.json    → ARCHIVE (move) sang archived/blackboards/ nếu > bb_days (30)
  • git worktree prune                  → dọn worktree mồ côi (chạy ở CLI)

An toàn: build_plan/apply_plan THUẦN (test được, truyền now_ts + state_root). CLI mặc định --dry-run;
phải --apply mới thực thi. Đặt tên kb_gc (KHÔNG 'gc') để tránh shadow stdlib gc.
"""
import os, sys, json, shutil, subprocess, time
from pathlib import Path

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parent))
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

DAY = 86400


def _older_than(p, age_days, now):
    try:
        return (now - Path(p).stat().st_mtime) > age_days * DAY
    except Exception:
        return False


def _iter_files(root):
    root = Path(root)
    if not root.is_dir():
        return
    for dp, _dirs, files in os.walk(root):
        for fn in files:
            yield Path(dp) / fn


def build_plan(state_root, now, bb_days=30, tmp_days=7):
    """THUẦN. Trả {'delete': [(path, reason)], 'archive': [(src, dst, reason)]}."""
    sr = Path(state_root)
    delete, archive = [], []

    # tmp + _trash: xóa file cũ
    for sub, why in ((sr / "orchestration" / "tmp", "orchestration/tmp cũ"),
                     (sr / "_trash", "_trash cũ")):
        for f in _iter_files(sub):
            if _older_than(f, tmp_days, now):
                delete.append((str(f), f"{why} (>{tmp_days}d)"))

    # dump ephemeral trong work/: network-response, .tmp
    for f in _iter_files(sr / "work"):
        if f.suffix in (".network-response", ".tmp") and _older_than(f, tmp_days, now):
            delete.append((str(f), f"work dump {f.suffix} (>{tmp_days}d)"))

    # blackboards cũ → archive (move, không xóa)
    bb = sr / "orchestration" / "blackboards"
    arc = sr / "archived" / "blackboards"
    for f in _iter_files(bb):
        if f.suffix in (".json", ".bak") and _older_than(f, bb_days, now):
            archive.append((str(f), str(arc / f.name), f"blackboard (>{bb_days}d) → archived"))

    return {"delete": delete, "archive": archive}


def apply_plan(plan):
    """Thực thi plan. Trả (n_deleted, n_archived, errors)."""
    n_del = n_arc = 0; errors = []
    for src, dst, _why in plan.get("archive", []):
        try:
            Path(dst).parent.mkdir(parents=True, exist_ok=True)
            shutil.move(src, dst); n_arc += 1
        except Exception as e:
            errors.append(f"archive {src}: {e}")
    for path, _why in plan.get("delete", []):
        try:
            p = Path(path)
            if p.is_dir(): shutil.rmtree(p, ignore_errors=True)
            elif p.exists(): p.unlink()
            n_del += 1
        except Exception as e:
            errors.append(f"delete {path}: {e}")
    return n_del, n_arc, errors


def worktree_prune(workspace):
    try:
        subprocess.run(["git", "-C", str(workspace), "worktree", "prune"], capture_output=True, text=True, timeout=60)
        r = subprocess.run(["git", "-C", str(workspace), "worktree", "list"], capture_output=True, text=True, timeout=60)
        return r.stdout.strip()
    except Exception as e:
        return f"(worktree prune skip: {e})"


def run(apply=False, bb_days=30, tmp_days=7):
    import kgr_runtime as RT
    sr = RT.state_root()
    ws = RT.workspace_root()
    plan = build_plan(sr, time.time(), bb_days, tmp_days)
    out = {"state_root": str(sr), "delete": plan["delete"], "archive": plan["archive"],
           "n_delete": len(plan["delete"]), "n_archive": len(plan["archive"])}
    if apply:
        n_del, n_arc, errors = apply_plan(plan)
        out["applied"] = {"deleted": n_del, "archived": n_arc, "errors": errors}
        out["worktree"] = worktree_prune(ws)
    else:
        out["mode"] = "DRY-RUN (thêm --apply để thực thi)"
    return out


def main(argv):
    apply = "--apply" in argv
    def _opt(name, default):
        for a in argv:
            if a.startswith(name + "="):
                try: return int(a.split("=", 1)[1])
                except Exception: pass
        return default
    out = run(apply=apply, bb_days=_opt("--bb-days", 30), tmp_days=_opt("--tmp-days", 7))
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
