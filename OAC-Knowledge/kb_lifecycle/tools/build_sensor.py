#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_sensor — R-G1: drift-sensor giữ-map-tươi TẬN-DỤNG lúc build.

Ý tưởng rẻ nhất: sau khi builder (dashboard/dataflow) build XONG, nó biết CHÍNH XÁC nó đã dùng
field/nguồn nào THẬT. Đối chiếu tập dùng-thật đó với catalog (field_dictionary + dataset_catalog):
field/dataset builder DÙNG mà catalog KHÔNG có = "map drift" (catalog cũ hoặc builder dùng nguồn lạ).
-> flag + gợi ý entry learn2 để review/promote. HÀM THUẦN: return dict, KHÔNG tự ghi gì.

API:
  check_used_fields(used, field_dict, dataset_catalog) -> {
      has_drift: bool,
      missing_fields: [ {field, dataset} ... ],   # field không có trong field_dict
      missing_datasets: [ dataset ... ],           # dataset không có trong dataset_catalog
      drift: {...},                                # gom lại cho tiện đọc
      suggestions: [ {learn2 entry đề xuất} ... ], # gợi ý (KHÔNG tự ghi)
  }

`used` = list các dict {"field": <tên field>, "dataset": <tên dataset>} builder dùng-thật.
`field_dict` = dict {field_name -> {...}} (nạp từ field_dictionary.yaml, khóa 'fields' hoặc phẳng).
`dataset_catalog` = dict {"datasets": {name -> {...}}} (hoặc phẳng {name -> {...}}).
"""
from __future__ import annotations
import json
import sys


def _field_keys(field_dict):
    if not isinstance(field_dict, dict):
        return set()
    inner = field_dict.get("fields") if "fields" in field_dict else field_dict
    if isinstance(inner, dict):
        return set(inner.keys())
    if isinstance(inner, list):
        # list các record có 'name'/'field'
        out = set()
        for r in inner:
            if isinstance(r, dict):
                nm = r.get("name") or r.get("field")
                if nm:
                    out.add(nm)
        return out
    return set()


def _dataset_keys(dataset_catalog):
    if not isinstance(dataset_catalog, dict):
        return set()
    inner = dataset_catalog.get("datasets") if "datasets" in dataset_catalog else dataset_catalog
    if isinstance(inner, dict):
        return set(inner.keys())
    if isinstance(inner, list):
        out = set()
        for r in inner:
            if isinstance(r, dict):
                nm = r.get("name")
                if nm:
                    out.add(nm)
        return out
    return set()


def _norm(s):
    return str(s).strip() if s is not None else ""


def check_used_fields(used, field_dict, dataset_catalog):
    """THUẦN: phát hiện field/dataset builder DÙNG-THẬT mà catalog KHÔNG có (map drift).
    Trả dict (KHÔNG tự ghi). suggestions = gợi ý entry learn2 để owner/review promote."""
    fk = _field_keys(field_dict)
    dk = _dataset_keys(dataset_catalog)
    fk_norm = {_norm(x) for x in fk}
    dk_norm = {_norm(x) for x in dk}

    missing_fields = []
    missing_datasets_set = []
    suggestions = []
    seen_ds = set()

    for u in (used or []):
        if not isinstance(u, dict):
            continue
        field = u.get("field")
        dataset = u.get("dataset")
        fnorm = _norm(field)
        dnorm = _norm(dataset)

        if field is not None and fnorm and fnorm not in fk_norm:
            missing_fields.append({"field": field, "dataset": dataset})
            suggestions.append({
                "type": "field_drift",
                "field": field,
                "dataset": dataset,
                "learn2_entry": {
                    "kind": "field_map_candidate",
                    "field": field,
                    "dataset": dataset,
                    "note": ("builder DÙNG-THẬT field này nhưng field_dictionary KHÔNG có "
                             "-> map cũ hoặc field mới; review rồi promote."),
                },
            })

        if dataset is not None and dnorm and dnorm not in dk_norm and dnorm not in seen_ds:
            seen_ds.add(dnorm)
            missing_datasets_set.append(dataset)
            suggestions.append({
                "type": "dataset_drift",
                "dataset": dataset,
                "learn2_entry": {
                    "kind": "dataset_map_candidate",
                    "dataset": dataset,
                    "note": ("builder DÙNG-THẬT dataset này nhưng dataset_catalog KHÔNG có "
                             "-> zombie/mới/đổi tên; chạy `kgr refresh --reconcile` + review."),
                },
            })

    has_drift = bool(missing_fields or missing_datasets_set)
    return {
        "has_drift": has_drift,
        "missing_fields": missing_fields,
        "missing_datasets": missing_datasets_set,
        "drift": {"fields": missing_fields, "datasets": missing_datasets_set} if has_drift else {},
        "suggestions": suggestions,
        "n_used": len([u for u in (used or []) if isinstance(u, dict)]),
    }


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    # demo nhanh (stdin JSON: {used, field_dict, dataset_catalog})
    try:
        payload = json.load(sys.stdin)
    except Exception:
        payload = {}
    res = check_used_fields(payload.get("used", []),
                            payload.get("field_dict", {}),
                            payload.get("dataset_catalog", {}))
    print(json.dumps(res, ensure_ascii=False, indent=2))
    sys.exit(1 if res["has_drift"] else 0)
