#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""edit_safety — helper testable cho CHÍNH SÁCH sửa df/wb an toàn (A12).

KHÔNG thực thi gì trên OAC. Chỉ cung cấp:
  1. backup_name(original, date_iso) -> "<original>_bk_YYYY-MM-DD"
     (ISO, khớp tiền lệ live `_bk_2026-06-22`; KHÔNG ddmmyyyy).
  2. detect_task_type(description, target_exists=None, diff=None) -> "EDIT" | "ADD"
     Xác định EDIT vs ADD từ HIỆN TRẠNG (target đã tồn tại?) + mô tả/diff —
     KHÔNG để builder tự-khai. Target tồn tại = tín hiệu MẠNH của EDIT.

Chính sách (encode trong 3 SKILL.md):
  - Task EDIT (sửa df/wb có sẵn) → KHÔNG tự ý:
      (a) mặc định CẦN owner CONFIRM trước; HOẶC
      (b) chế độ AUTO (owner bảo "tự sửa"): CLONE bản gốc thành
          <tên>_bk_YYYY-MM-DD (BACKUP-only, đặt trong folder gốc) rồi sửa THẲNG bản gốc.
  - Task ADD (dựng-mới) → KHÔNG cần clone.

Usage:
  python edit_safety.py backup-name "<original>" "<YYYY-MM-DD>"
  python edit_safety.py detect "<description>" [--exists|--absent]
"""
import sys, re, datetime

_ISO_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def backup_name(original, date_iso):
    """'<original>_bk_YYYY-MM-DD'. date_iso PHẢI là ISO (YYYY-MM-DD), khớp tiền lệ live `_bk_2026-06-22`.

    Từ chối ddmmyyyy / định dạng khác để KHÔNG bao giờ sinh '_bk_22-06-2026'."""
    if original is None or str(original).strip() == "":
        raise ValueError("backup_name: 'original' rỗng")
    d = str(date_iso).strip()
    if not _ISO_RE.match(d):
        raise ValueError(f"backup_name: date_iso phải ISO 'YYYY-MM-DD' (khớp _bk_2026-06-22), được: {date_iso!r}")
    # validate là ngày thật (bắt 2026-13-40)
    try:
        datetime.date.fromisoformat(d)
    except ValueError as e:
        raise ValueError(f"backup_name: date_iso không hợp lệ: {date_iso!r} ({e})")
    return f"{str(original).strip()}_bk_{d}"


# Từ khóa mô tả: EDIT (sửa cái có sẵn) vs ADD (dựng cái mới).
_EDIT_HINTS = (
    "sửa", "sua", "fix", "chỉnh", "chinh", "cập nhật", "cap nhat", "update", "đổi", "doi",
    "change", "edit", "correct", "sai", "rework", "modify", "adjust", "relabel", "override",
    "remove", "xóa", "xoa", "bỏ", "bo ",
)
_ADD_HINTS = (
    "tạo mới", "tao moi", "tạo", "tao ", "dựng", "dung ", "dựng mới", "create", "new ", "mới",
    "moi ", "add ", "thêm mới", "them moi", "build", "gộp mới",
)


def detect_task_type(description, target_exists=None, diff=None):
    """Trả 'EDIT' hoặc 'ADD'.

    Ưu tiên TÍN HIỆU HIỆN TRẠNG (KHÔNG để builder tự-khai):
      - target_exists=True  -> EDIT (đụng artifact đã tồn tại = sửa).
      - diff cho thấy sửa dòng có sẵn (có '-'/thay-thế) -> EDIT.
      - target_exists=False -> ADD (dựng cái chưa có).
    Chỉ khi hiện-trạng KHÔNG rõ (None) mới rơi về mô-tả (heuristic từ khóa).
    """
    # 1) Hiện trạng là TÍN HIỆU MẠNH NHẤT — đè lên mô tả (builder không tự-khai được).
    if target_exists is True:
        return "EDIT"

    # 2) Diff: có dòng bị xóa/thay (đầu dòng '-' không phải '---') => đang sửa cái có sẵn.
    if diff:
        for ln in str(diff).splitlines():
            s = ln.rstrip("\r")
            if s.startswith("-") and not s.startswith("---"):
                return "EDIT"

    if target_exists is False:
        # target chưa tồn tại: dựng mới trừ khi mô tả rõ ràng là sửa (hiếm — nhưng tôn trọng mô tả EDIT mạnh)
        d = (description or "").casefold()
        if any(h in d for h in ("sửa", "sua", "fix", "correct", "rework")):
            return "EDIT"
        return "ADD"

    # 3) target_exists=None (không rõ hiện trạng) -> đọc mô tả.
    d = (description or "").casefold()
    edit_hit = any(h in d for h in _EDIT_HINTS)
    add_hit = any(h in d for h in _ADD_HINTS)
    if add_hit and not edit_hit:
        return "ADD"
    if edit_hit and not add_hit:
        return "EDIT"
    # mơ hồ/cả hai: mặc định AN TOÀN = EDIT (đòi confirm/backup còn hơn ghi đè liều).
    return "EDIT"


def _cli(argv):
    if not argv:
        sys.stderr.write(__doc__ + "\n"); return 2
    cmd = argv[0]
    if cmd == "backup-name" and len(argv) >= 3:
        print(backup_name(argv[1], argv[2])); return 0
    if cmd == "detect" and len(argv) >= 2:
        exists = None
        if "--exists" in argv: exists = True
        elif "--absent" in argv: exists = False
        print(detect_task_type(argv[1], target_exists=exists)); return 0
    sys.stderr.write(__doc__ + "\n"); return 2


if __name__ == "__main__":
    sys.exit(_cli(sys.argv[1:]))
