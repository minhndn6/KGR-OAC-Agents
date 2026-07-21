#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_mastery_section (A17) — sinh MỘT section GENERATED cho MASTERY từ learnings/log.jsonl.

Bỏ dual-write: thay vì tay-copy lesson vào MASTERY (dễ lệch), section này được SINH RA
(deterministic) từ các lesson ĐÃ PROMOTED — rồi nhúng/rebuild vào MASTERY như file GENERATED.

Nguồn: OAC-Knowledge/learnings/log.jsonl (learn2 format).
Lọc: status == "promoted" VÀ type ∈ {lesson, qa} (ví-dụ-tái-lập về OAC-mechanics).
      pending / superseded / rejected -> LOẠI.
Deterministic: sort ổn định theo (fact_key, id); KHÔNG in timestamp (không trôi giữa các lần chạy).
KHÔNG số cứng: chỉ chép topic/content của record (record đã qua gate learn2 chống số-cứng theo type).

Usage:
  python build_mastery_section.py [--log <path>] [--out <file>]
  (mặc định --log = <kb_root>/learnings/log.jsonl; không --out -> in stdout)
"""
import sys, os, json, argparse
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HERE = Path(__file__).resolve()

BANNER = "# GENERATED (từ learnings) — KHÔNG sửa tay"
_SUBHEAD = "## Bài học đã kiểm chứng (promoted)"
_NOTE = (">_Section này SINH RA từ `learnings/log.jsonl` (chỉ record `promoted`, type lesson/qa) "
         "bởi `build_mastery_section.py`. Sửa NGUỒN (learn2 promote) rồi rebuild, ĐỪNG sửa tay._")

_KEEP_TYPES = {"lesson", "qa"}


def _default_log():
    # Không hard-fail nếu import kb_paths lỗi: fallback đường tương đối tới kho.
    try:
        sys.path.insert(0, str(HERE.parent))
        import kb_paths  # noqa: E402
        return kb_paths.resolve_kb_root(start_file=str(HERE)) / "learnings" / "log.jsonl"
    except Exception:
        return HERE.parents[2] / "learnings" / "log.jsonl"


def _read_records(logp):
    p = Path(logp)
    if not p.exists():
        return []
    recs = []
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            recs.append(json.loads(line))
        except Exception:
            continue  # bỏ dòng hỏng, không crash
    return recs


def select_promoted(records):
    """Chỉ promoted + type lesson/qa. Sort ỔN ĐỊNH (fact_key, id) -> deterministic."""
    picked = [
        r for r in records
        if r.get("status") == "promoted" and r.get("type") in _KEEP_TYPES
    ]
    picked.sort(key=lambda r: (str(r.get("fact_key") or ""), str(r.get("id") or "")))
    return picked


def render_section(records):
    """Trả CHUỖI section GENERATED, deterministic, KHÔNG timestamp."""
    picked = select_promoted(records)
    lines = [BANNER, "", _SUBHEAD, "", _NOTE, ""]
    if not picked:
        lines.append("_(chưa có bài học promoted nào.)_")
        return "\n".join(lines) + "\n"
    for r in picked:
        topic = str(r.get("topic") or "").strip()
        content = str(r.get("content") or "").strip()
        fk = str(r.get("fact_key") or "").strip()
        tag = f" `<{fk}>`" if fk else ""
        lines.append(f"- **{topic}**{tag}: {content}")
    return "\n".join(lines) + "\n"


def build(logp):
    return render_section(_read_records(logp))


def main(argv=None):
    ap = argparse.ArgumentParser(description="Sinh section GENERATED cho MASTERY từ learnings promoted.")
    ap.add_argument("--log", default=None, help="đường dẫn log.jsonl (mặc định: <kb_root>/learnings/log.jsonl)")
    ap.add_argument("--out", default=None, help="ghi ra file (mặc định: in stdout)")
    args = ap.parse_args(argv)

    logp = args.log or _default_log()
    section = build(logp)

    if args.out:
        Path(args.out).write_text(section, encoding="utf-8")
    else:
        sys.stdout.write(section)
    return 0


if __name__ == "__main__":
    sys.exit(main())
