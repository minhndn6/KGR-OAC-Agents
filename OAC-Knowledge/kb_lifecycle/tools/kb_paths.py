#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""kb_paths — resolve KB root MỘT cách duy nhất + tường minh (INV-1, fix split-brain).

Thứ tự (fail loud, KHÔNG hardcode fallback mù như learn.py:17 cũ):
  1. env OAC_KB_ROOT (phải là KB hợp lệ = có marker .kgr_kb_root)
  2. walk-up từ start_file gặp marker  (đúng cho bản trong-repo)
  3. user-level registry file kb_root.txt (đúng cho bản cài ~/.claude/skills)
  4. raise KbRootError  (KHÔNG rơi vào C:\\Project\\OAC-Knowledge lạ)

Mọi ứng viên đều phải VALIDATE marker -> KB lạ (chỉ có QUICK_REFERENCE, thiếu marker) bị từ chối.
Hàm nhận env/registry_path để test hermetic; bản tiện dụng dùng os.environ thật.
"""
import os
from pathlib import Path

MARKER = ".kgr_kb_root"

class KbRootError(RuntimeError):
    """Không xác định được KB root một cách an toàn."""

def is_kb(path) -> bool:
    try:
        return (Path(path) / MARKER).is_file()
    except Exception:
        return False

def registry_file(env=None) -> Path:
    """Vị trí registry user-level (độc lập env vì env KHÔNG truyền qua session/MCP)."""
    env = os.environ if env is None else env
    base = env.get("KGR_RUNTIME_DIR") or env.get("LOCALAPPDATA")
    if base:
        return Path(base) / "kgr-oac" / "kb_root.txt"
    return Path(os.path.expanduser("~")) / ".kgr" / "kb_root.txt"

def resolve_kb_root(start_file=None, env=None, registry_path=None) -> Path:
    env = os.environ if env is None else env

    # 1) env override — phải hợp lệ, nếu trỏ KB lạ thì RAISE (không im lặng bỏ qua)
    e = env.get("OAC_KB_ROOT")
    if e:
        if is_kb(e):
            return Path(e)
        raise KbRootError(f"OAC_KB_ROOT={e!r} không phải KB hợp lệ (thiếu marker {MARKER}).")

    # 2) walk-up từ start_file (bản trong-repo)
    if start_file:
        cur = Path(start_file).resolve()
        for anc in (cur, *cur.parents):
            if is_kb(anc):
                return anc

    # 3) registry user-level (bản cài ~/.claude/skills không walk-up tới được)
    reg = Path(registry_path) if registry_path else registry_file(env)
    try:
        if reg.is_file():
            cand = reg.read_text(encoding="utf-8").strip()
            if cand and is_kb(cand):
                return Path(cand)
            if cand:
                raise KbRootError(f"Registry {reg} trỏ {cand!r} không phải KB hợp lệ (thiếu marker).")
    except KbRootError:
        raise
    except Exception:
        pass

    # 4) FAIL LOUD — không bao giờ trả KB đoán mò
    raise KbRootError(
        "Không xác định được KB root an toàn. "
        "Đặt env OAC_KB_ROOT, hoặc chạy `kgr setup` để ghi registry, "
        f"hoặc đảm bảo marker {MARKER} nằm trong cây thư mục KB.")

def write_registry(kb_root, env=None, registry_path=None) -> Path:
    """Ghi registry trỏ tới kb_root (dùng bởi `kgr setup`). kb_root phải hợp lệ."""
    if not is_kb(kb_root):
        raise KbRootError(f"{kb_root} thiếu marker {MARKER} — không ghi registry trỏ KB không hợp lệ.")
    reg = Path(registry_path) if registry_path else registry_file(env)
    reg.parent.mkdir(parents=True, exist_ok=True)
    reg.write_text(str(Path(kb_root).resolve()), encoding="utf-8")
    return reg

if __name__ == "__main__":
    try:
        print(resolve_kb_root(start_file=__file__))
    except KbRootError as ex:
        print("KbRootError:", ex)
