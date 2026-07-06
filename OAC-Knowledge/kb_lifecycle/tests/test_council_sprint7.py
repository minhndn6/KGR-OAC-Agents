#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Council Sprint-7 acceptance (TDD) — cơ chế REFRESH an toàn (đọc-only, KHÔNG ghi đè catalog):
  R-D2  Sidecar description (chống rebuild XÓA tri-thức tay): dataflow_descriptions.yaml CURATED +
        build_catalogs.merge_descriptions() chèn lại description khi rebuild.
  R-D1  Rebuild reproducible-VERIFY: resolver staging path KHÔNG FileNotFoundError (thử raw/X và X);
        semantic_diff() bỏ _meta/order noise; --verify/--into-tmp KHÔNG ghi đè committed.
  R-A1  Reconcile live↔catalog THUẦN (added/removed/matched) + kgr refresh CLI (--check/--discover/--reconcile).
  R-G1  build_sensor.check_used_fields() phát hiện field/dataset builder dùng-thật mà thiếu trong catalog → map drift.

Chạy: PYTHONUTF8=1 python kb_lifecycle/tests/test_council_sprint7.py
HERMETIC: KHÔNG gọi oac-native. Tiêm sidecar/catalog/live giả. Ban đầu FAIL (chưa impl)."""
import os, sys, json, tempfile, importlib
from pathlib import Path

WS = Path(os.environ.get("KGR_WORKSPACE") or r"C:\Project\KGR-OAC-Agents")
KB = WS / "OAC-Knowledge"
TOOLS = KB / "kb_lifecycle" / "tools"
RAW = KB / "raw"
sys.path.insert(0, str(TOOLS))
sys.path.insert(0, str(RAW))

PASS = FAIL = 0
def chk(c, l):
    global PASS, FAIL
    if c: PASS += 1; print(f"  PASS  {l}")
    else: FAIL += 1; print(f"  FAIL  {l}")

def read(p):
    try: return Path(p).read_text(encoding="utf-8", errors="replace")
    except Exception: return ""

def _import(mod):
    try:
        if mod in sys.modules: del sys.modules[mod]
        return importlib.import_module(mod)
    except Exception as e:
        print(f"   import {mod} ERR: {e}")
        return None

# ─────────────────────────────────────────────────────────────────────────────
# R-D2 — Sidecar description CURATED + merge helper
# ─────────────────────────────────────────────────────────────────────────────
def test_rd2():
    print("== R-D2  sidecar description (chống rebuild xóa tri-thức) ==")
    import yaml
    sidecar = KB / "dataflow_descriptions.yaml"
    chk(sidecar.is_file(), "dataflow_descriptions.yaml tồn tại (sidecar CURATED)")
    txt = read(sidecar)
    low = txt.lower()
    chk("curated" in low, "sidecar có banner CURATED (sửa tay OK)")
    # có entries (map name/id -> description); ít nhất vài entry thật (~28 field ban đầu)
    data = {}
    try:
        data = yaml.safe_load(txt) or {}
    except Exception as e:
        print("   sidecar parse err:", e)
    entries = data.get("descriptions") if isinstance(data, dict) and "descriptions" in data else data
    entries = entries if isinstance(entries, dict) else {}
    chk(len(entries) >= 10, f"sidecar có >=10 entries description (được: {len(entries)})")
    # sanity: 2 dataflow chủ chốt phải có mô tả đã tách ra
    for key in ("KGR_DF_TD_Metrics_bk", "(KGR) 1. DTF_CALC_INVOICE_MEMO_#"):
        chk(key in entries and str(entries.get(key, "")).strip() != "",
            f"sidecar chứa description cho {key}")

    # merge helper THUẦN: tiêm sidecar giả + flows dict giả -> chèn đúng description
    bc = _import("build_catalogs")
    chk(bc is not None and hasattr(bc, "merge_descriptions"),
        "build_catalogs.merge_descriptions(flows, sidecar) tồn tại (pure)")
    if bc is not None and hasattr(bc, "merge_descriptions"):
        from collections import OrderedDict
        flows = OrderedDict([
            ("FlowA", OrderedDict([("name", "FlowA"), ("dataflow_id", "'o'.'FlowA'"), ("n_steps", 3)])),
            ("FlowB", OrderedDict([("name", "FlowB"), ("dataflow_id", "'o'.'FlowB'"), ("n_steps", 1)])),
        ])
        fake_sidecar = {"FlowA": "Mô tả A đã curate", "'o'.'FlowB'": "Mô tả B theo id"}
        merged = bc.merge_descriptions(flows, fake_sidecar)
        chk(merged["FlowA"].get("description") == "Mô tả A đã curate",
            "merge chèn description theo tên dataflow")
        chk(merged["FlowB"].get("description") == "Mô tả B theo id",
            "merge chèn description theo dataflow_id (fallback key)")
        # additive: flow không có sidecar -> không thêm khóa rỗng
        flows2 = OrderedDict([("FlowC", OrderedDict([("name", "FlowC")]))])
        m2 = bc.merge_descriptions(flows2, fake_sidecar)
        chk("description" not in m2["FlowC"], "flow không có sidecar entry -> KHÔNG thêm description rỗng")
        # description đứng TRƯỚC (đầu record) để đọc dễ — không bắt buộc nhưng kiểm không phá thứ tự khác
        chk(list(merged["FlowA"].keys())[0] == "description" or "description" in merged["FlowA"],
            "description được chèn vào record FlowA")

# ─────────────────────────────────────────────────────────────────────────────
# R-D1 — Rebuild reproducible-VERIFY (resolver staging + semantic_diff), KHÔNG ghi đè
# ─────────────────────────────────────────────────────────────────────────────
def test_rd1():
    print("== R-D1  rebuild reproducible-VERIFY (an toàn, không ghi đè) ==")
    bc = _import("build_catalogs")
    chk(bc is not None, "build_catalogs import được (không crash top-level)")
    if bc is None:
        return
    # resolver staging path: hàm THUẦN thử raw/X rồi X (fallback) -> KHÔNG FileNotFoundError khi
    # JSON nằm ở gốc staging (raw/ backup) thay vì raw/raw/.
    chk(hasattr(bc, "stg_path"), "build_catalogs.stg_path(rel, stg) resolver tồn tại")
    if hasattr(bc, "stg_path"):
        with tempfile.TemporaryDirectory() as d:
            dd = Path(d)
            # staging giả kiểu 'raw backup': datasets_all.json Ở GỐC (không có raw/ subdir)
            (dd / "datasets_all.json").write_text('{"datasets":[]}', encoding="utf-8")
            got = bc.stg_path(os.path.join("raw", "datasets_all.json"), str(dd))
            chk(Path(got).is_file(), "stg_path fallback: raw/X không có -> tìm thấy X ở gốc staging")
            # staging giả kiểu 'work/staging': JSON dưới raw/
            sub = dd / "raw"; sub.mkdir()
            (sub / "catalog_enumeration.json").write_text("{}", encoding="utf-8")
            got2 = bc.stg_path(os.path.join("raw", "catalog_enumeration.json"), str(dd))
            chk(Path(got2).is_file() and got2.replace("\\", "/").endswith("raw/catalog_enumeration.json"),
                "stg_path ưu tiên raw/X khi tồn tại")
            # file thật sự thiếu -> trả path 'raw/X' (để lỗi có thông điệp rõ) hoặc raise được test riêng
            missing = bc.stg_path("nope.json", str(dd))
            chk(isinstance(missing, str), "stg_path trả str kể cả khi thiếu (caller quyết lỗi)")

    # semantic_diff: bỏ _meta + noise order -> 2 catalog 'giống về nội dung' = reproducible
    chk(hasattr(bc, "semantic_diff"), "build_catalogs.semantic_diff(a, b) tồn tại (pure)")
    if hasattr(bc, "semantic_diff"):
        a = {"_meta": {"extracted_live": "2026-06-20", "total": 2},
             "dataflows": {"F1": {"name": "F1", "n_steps": 3}, "F2": {"name": "F2"}}}
        # b: _meta khác ngày (noise) + thứ tự key đảo, nhưng NỘI DUNG như a
        b = {"_meta": {"extracted_live": "2026-07-06", "total": 2},
             "dataflows": {"F2": {"name": "F2"}, "F1": {"n_steps": 3, "name": "F1"}}}
        d1 = bc.semantic_diff(a, b)
        chk((d1 == {} or d1 is None or d1.get("reproducible") is True or d1.get("differs") is False),
            "semantic_diff bỏ _meta/order noise -> 2 catalog coi như reproducible")
        # b2: nội dung THẬT khác (n_steps đổi) -> phải báo lệch
        b2 = {"_meta": {"extracted_live": "2026-07-06"},
              "dataflows": {"F1": {"name": "F1", "n_steps": 99}, "F2": {"name": "F2"}}}
        d2 = bc.semantic_diff(a, b2)
        differs = bool(d2) and (d2 != {}) and (d2.get("reproducible") is not True) and (d2.get("differs") is not False)
        chk(differs, "semantic_diff phát hiện lệch nội dung thật (n_steps 3 vs 99)")

    # An toàn: build_catalogs có chế độ --verify/--into-tmp (KHÔNG ghi đè committed)
    bctxt = read(RAW / "build_catalogs.py")
    chk(("--verify" in bctxt) or ("--into-tmp" in bctxt) or ("into_tmp" in bctxt),
        "build_catalogs có chế độ --verify/--into-tmp (rebuild ra thư mục TẠM, không ghi đè)")
    chk(("scratch" in bctxt) or ("kgr_runtime" in bctxt) or ("tmp" in bctxt.lower()),
        "verify-mode dùng thư mục tạm (kgr_runtime.scratch / tmp) chứ không OUT committed")

# ─────────────────────────────────────────────────────────────────────────────
# R-A1 — Reconcile live↔catalog thuần + kgr refresh CLI
# ─────────────────────────────────────────────────────────────────────────────
def test_ra1():
    print("== R-A1  reconcile live↔catalog + kgr refresh CLI ==")
    kgr = _import("kgr")
    chk(kgr is not None and hasattr(kgr, "reconcile_datasets"),
        "kgr.reconcile_datasets(live_names, catalog_names) tồn tại (pure/tiêm-được)")
    if kgr is not None and hasattr(kgr, "reconcile_datasets"):
        live = ["DS_A", "DS_B", "DS_NEW"]
        catalog = ["DS_A", "DS_B", "DS_ZOMBIE"]
        rec = kgr.reconcile_datasets(live, catalog)
        added = set(rec.get("added") or [])
        removed = set(rec.get("removed") or [])
        matched = set(rec.get("matched") or [])
        chk(added == {"DS_NEW"}, f"reconcile added = live-only (được: {sorted(added)})")
        chk(removed == {"DS_ZOMBIE"}, f"reconcile removed(zombie) = catalog-only (được: {sorted(removed)})")
        chk(matched == {"DS_A", "DS_B"}, f"reconcile matched = giao (được: {sorted(matched)})")
        # counts
        chk(rec.get("n_live") == 3 and rec.get("n_catalog") == 3, "reconcile báo n_live/n_catalog")
        # rỗng cả hai -> không lỗi
        empty = kgr.reconcile_datasets([], [])
        chk((empty.get("added") == [] and empty.get("removed") == [] and empty.get("matched") == []),
            "reconcile([],[]) -> mọi list rỗng, không lỗi")

    # cmd_refresh dispatch: --check / --discover / --reconcile / (no flag)
    chk(kgr is not None and hasattr(kgr, "cmd_refresh"), "kgr.cmd_refresh(rest) tồn tại")
    # CLI routing table có 'refresh'
    kgrtxt = read(TOOLS / "kgr.py")
    chk('"refresh"' in kgrtxt or "'refresh'" in kgrtxt, "kgr.py main() dispatch có 'refresh'")
    # các cờ được nhận diện
    for flag in ("--check", "--discover", "--reconcile"):
        chk(flag in kgrtxt, f"cmd_refresh nhận cờ {flag}")
    # --check phải TÁI SỬ DỤNG freshness_check (R-A2), KHÔNG copy logic
    chk("freshness_check" in kgrtxt, "refresh --check tái dùng freshness_check (R-A2)")
    # --discover gọi oac-native (runtime), nhưng lỗi -> báo rõ + exit≠0 (không giả số)
    chk(("oac-native" in kgrtxt) or ("discover_data" in kgrtxt) or ("oac_native" in kgrtxt),
        "refresh --discover tham chiếu kênh oac-native discover_data (LIVE, read-only)")

    # CLI dispatch thực: gọi 'refresh --check' hermetic (không cần live) -> exit 0/1 hợp lệ, có output
    import subprocess
    env = {**os.environ, "PYTHONUTF8": "1"}
    KGRPY = TOOLS / "kgr.py"
    r = subprocess.run([sys.executable, str(KGRPY), "refresh", "--check"],
                       capture_output=True, text=True, env=env)
    chk(r.returncode in (0, 1), f"kgr refresh --check chạy được (exit {r.returncode})")
    chk(("status" in (r.stdout or "").lower()) or ("fresh" in (r.stdout or "").lower())
        or ("extracted" in (r.stdout or "").lower()),
        "kgr refresh --check in báo cáo staleness")

# ─────────────────────────────────────────────────────────────────────────────
# R-G1 — build_sensor drift (field/dataset dùng-thật vắng catalog)
# ─────────────────────────────────────────────────────────────────────────────
def test_rg1():
    print("== R-G1  build-path drift-sensor ==")
    bs = _import("build_sensor")
    chk(bs is not None and hasattr(bs, "check_used_fields"),
        "build_sensor.check_used_fields(used, field_dict, dataset_catalog) tồn tại")
    if bs is None or not hasattr(bs, "check_used_fields"):
        return
    # field_dict giả: field_name -> {...}; dataset_catalog giả: {datasets:{name:{...}}}
    field_dict = {"Doanh thu thực tế": {"dataset": "DS_KNOWN"}, "Giá Vốn": {"dataset": "DS_KNOWN"}}
    dataset_catalog = {"datasets": {"DS_KNOWN": {"name": "DS_KNOWN"}}}

    # (1) used có field LẠ + dataset LẠ -> flag drift
    used = [
        {"field": "Doanh thu thực tế", "dataset": "DS_KNOWN"},
        {"field": "FIELD_LẠ_CHƯA_MAP", "dataset": "DS_KNOWN"},
        {"field": "Giá Vốn", "dataset": "DS_ZOMBIE_KO_CO"},
    ]
    res = bs.check_used_fields(used, field_dict, dataset_catalog)
    drift = res.get("drift") or res.get("missing") or {}
    # gom lại các field/dataset lạ (chấp nhận nhiều shape)
    flat = json.dumps(res, ensure_ascii=False)
    chk("FIELD_LẠ_CHƯA_MAP" in flat, "sensor phát hiện field lạ chưa map trong field_dict")
    chk("DS_ZOMBIE_KO_CO" in flat, "sensor phát hiện dataset lạ chưa có trong dataset_catalog")
    chk(bool(res.get("has_drift")) is True or bool(drift), "sensor báo has_drift=True khi có field/dataset lạ")
    # gợi ý learn2 entry (return dict, KHÔNG tự ghi)
    chk(("learn2" in flat.lower()) or ("suggest" in flat.lower()) or ("propose" in res or "suggestions" in res),
        "sensor gợi ý learn2 entry (return dict, không tự ghi)")

    # (2) used HỢP LỆ hoàn toàn -> sạch, has_drift False
    used_ok = [{"field": "Doanh thu thực tế", "dataset": "DS_KNOWN"},
               {"field": "Giá Vốn", "dataset": "DS_KNOWN"}]
    res2 = bs.check_used_fields(used_ok, field_dict, dataset_catalog)
    d2 = res2.get("drift") or res2.get("missing") or {}
    chk((not res2.get("has_drift")) and (not d2), "used hợp lệ -> sensor sạch (has_drift False)")

    # (3) builder SKILL.md có 1 dòng đối chiếu field/nguồn dùng-thật vs catalog
    builders = [
        WS / "Dashboard-builder" / ".claude" / "skills" / "oac-dashboard-builder" / "SKILL.md",
        WS / "Dataflow-builder" / ".claude" / "skills" / "oac-dataflow-builder" / "SKILL.md",
    ]
    any_hit = False
    for f in builders:
        t = read(f).lower()
        if ("build_sensor" in t) or ("đối chiếu" in t and "catalog" in t and ("learn2" in t or "drift" in t)):
            any_hit = True
    chk(any_hit, "builder SKILL.md có dòng: sau build đối chiếu field/nguồn dùng-thật vs catalog -> propose learn2")

def main():
    test_rd2()
    test_rd1()
    test_ra1()
    test_rg1()
    print(f"\n== TỔNG Sprint-7: PASS={PASS} FAIL={FAIL} ==")
    return 1 if FAIL else 0

if __name__ == "__main__":
    sys.exit(main())
