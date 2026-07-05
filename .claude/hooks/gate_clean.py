#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gate_clean — Stop hook. Chạy check_clean (tracked + physical scratch) TRƯỚC khi session kết thúc.

Có vi phạm → decision:"block" ép session dọn. Chống lặp vô hạn: nếu ĐÚNG bộ vi phạm đó tái xuất
lần Stop kế (model không tự sửa được) → cho Stop kèm cảnh báo (không block mãi).
FAIL-OPEN: mọi lỗi → allow stop (exit 0), không chặn người dùng.
"""
import sys, json, hashlib
from pathlib import Path

for _s in (sys.stdin, sys.stdout, sys.stderr):   # Windows cmd cp1252-safe; reason có tiếng Việt
    try: _s.reconfigure(encoding="utf-8")
    except Exception: pass

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[2] / "OAC-Knowledge" / "kb_lifecycle" / "tools"))


def _sig(items):
    key = "\n".join(sorted(f"{a}/{b}" for a, b, _ in items))
    return hashlib.sha256(key.encode("utf-8")).hexdigest()[:16]


def _marker():
    try:
        import kgr_runtime as RT
        return RT.scratch("gate_marker.json")
    except Exception:
        return None


def _allow():
    sys.exit(0)


def _block(reason):
    print(json.dumps({"decision": "block", "reason": reason}, ensure_ascii=True))
    sys.exit(0)


def main():
    try:
        try:
            json.load(sys.stdin)          # tiêu thụ stdin (không dùng)
        except Exception:
            pass
        import check_clean as CC
        tracked = CC.scan_all()
        phys = CC.scan_all_physical()
        viol = list(tracked) + list(phys)
        if not viol:
            mp = _marker()
            if mp and Path(mp).exists():
                try: Path(mp).unlink()
                except Exception: pass
            _allow(); return

        sig = _sig(viol)
        mp = _marker()
        prev = {}
        if mp and Path(mp).exists():
            try: prev = json.loads(Path(mp).read_text(encoding="utf-8"))
            except Exception: prev = {}
        count = prev.get("count", 0) + 1 if prev.get("sig") == sig else 1
        if mp:
            try: Path(mp).write_text(json.dumps({"sig": sig, "count": count}), encoding="utf-8")
            except Exception: pass

        listing = "\n".join(f"  - {a}/{b}   (match {pat})" for a, b, pat in viol[:20])
        more = "" if len(viol) <= 20 else f"\n  … +{len(viol)-20} file nữa"
        if count >= 2:
            sys.stderr.write(
                f"[gate_clean] VẪN còn {len(viol)} scratch trong cây sau {count} lần nhắc — CHO Stop, "
                f"nhưng hãy dọn thủ công:\n{listing}{more}\n")
            _allow(); return
        _block(
            f"Còn {len(viol)} file scratch/state nằm trong cây project (agent sẽ crawl → đốt token). "
            f"DỌN trước khi kết thúc: chuyển ra kgr_runtime.work_dir('<repo>')/scratch() hoặc xóa; "
            f"file GENERATED thì revert/rebuild. Danh sách:\n{listing}{more}\n"
            f"(Chạy: python OAC-Knowledge/kb_lifecycle/tools/check_clean.py --strict)")
    except Exception:
        _allow()


if __name__ == "__main__":
    main()
