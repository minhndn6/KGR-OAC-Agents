#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TDD acceptance — Council Sprint 2 (A1 nối learn2-shim + doctor + call-sites; A5 gate số-cứng theo type).
Self-contained: chk() + exit 1 nếu có FAIL. Hermetic (temp log), KHÔNG đụng log thật.
Chạy: PYTHONUTF8=1 python kb_lifecycle/tests/test_council_sprint2.py

Test BAN ĐẦU FAIL (chưa implement) là ĐÚNG — đây là spec chấp nhận cho Sprint 2.
"""
import os, sys, json, tempfile, shutil, subprocess, re
from pathlib import Path

HERE = Path(__file__).resolve()
TOOLS = HERE.parents[1] / "tools"                       # kb_lifecycle/tools
KB = HERE.parents[2]                                     # OAC-Knowledge
LEARN_PY = KB / "skill" / "kgr-oac-lineage" / "scripts" / "learn.py"
KGR_PY = TOOLS / "kgr.py"
KB_ROUTE_PY = TOOLS / "kb_route.py"
LEARNING_MD = KB / "LEARNING.md"
PENDING_MD = KB / "learnings" / "pending.md"
OWNER_PENDING_MD = TOOLS.parent / "OWNER_PENDING.md"    # kb_lifecycle/OWNER_PENDING.md
SKILL_LINEAGE = KB / "skill" / "kgr-oac-lineage" / "SKILL.md"
SKILL_ORCH = Path(r"C:\Project\KGR-OAC-Agents\OAC-Orchestrator\skill\kgr-oac-orchestrator\SKILL.md")

sys.path.insert(0, str(TOOLS))

PASS = FAIL = 0
def chk(c, l):
    global PASS, FAIL
    if c: PASS += 1; print(f"  PASS  {l}")
    else: FAIL += 1; print(f"  FAIL  {l}")

def read_log(p):
    p = Path(p)
    if not p.exists(): return []
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]

def is_reject(res):
    """True nếu learn2.add coi input là bị CHẶN (số-cứng): status bắt đầu 'rejected'
    HOẶC có cờ rejected/blocked. (add trả dict; nếu implement raise thì caller bắt riêng.)"""
    if not isinstance(res, dict): return False
    st = str(res.get("status", "")).lower()
    return st.startswith("reject") or bool(res.get("blocked")) or bool(res.get("rejected"))

def is_added(res):
    return isinstance(res, dict) and str(res.get("status", "")).lower() == "added"

def safe_add(L, *a, **kw):
    """Gọi L.add; nếu implement chọn raise cho số-cứng thì quy về dict rejected."""
    try:
        return L.add(*a, **kw)
    except Exception as e:
        return {"status": "rejected_raise", "reason": str(e)}


# ─────────────────────────────────────────────────────────────────────────────
# A5 — learn2 chặn SỐ CỨNG theo TYPE
# ─────────────────────────────────────────────────────────────────────────────
def test_a5_gate_by_type(L, tmp):
    print("== A5: gate số-cứng theo type (fact/formula_correction/physical_table REJECT; lesson/qa/open-question CHO PHÉP) ==")

    # --- các TYPE cấu trúc + content có SỐ TUYỆT ĐỐI LỚN → PHẢI bị chặn, KHÔNG ghi record ---
    hard_number_contents = [
        ("351 tỷ",                 '"N tỷ" — số tuyệt đối'),
        ("doanh thu 445.043",      "số ≥5 chữ số có dấu chấm ngăn"),
        ("chốt 12,345 đơn",        "số ≥5 chữ số có dấu phẩy ngăn (12,345)"),
        ("tăng 56%",               "phần trăm nguyên"),
        ("lệch 12,3%",             "phần trăm thập phân (dấu phẩy)"),
        ("giá 3.141,59",           "thập-phân lớn 3.141,59"),
        ("khoảng 9 triệu",         '"N triệu"'),
        ("value 1.234.567",        "1.234.567 (nghìn phân cách dấu chấm)"),
        ("value 1,234,567",        "1,234,567 (nghìn phân cách dấu phẩy)"),
        ("id 987654",              "≥5 chữ số liền (987654)"),
    ]
    for typ in ("fact", "formula_correction", "physical_table"):
        for i, (content, desc) in enumerate(hard_number_contents):
            log = tmp / f"a5_{typ}_{i}.jsonl"
            n_before = len(read_log(log))
            res = safe_add(L, typ, f"topic {typ} {i}", content, log=str(log))
            chk(is_reject(res), f"type={typ}: content [{desc}] -> REJECT ({content!r})")
            chk(len(read_log(log)) == n_before, f"type={typ}: record KHÔNG được ghi khi bị chặn ({content!r})")

    # --- TYPE ví-dụ-tái-lập (lesson/qa/open-question/gap) + số → ĐƯỢC PHÉP ---
    for typ in ("lesson", "qa"):
        for i, (content, desc) in enumerate(hard_number_contents[:5]):
            log = tmp / f"a5_ok_{typ}_{i}.jsonl"
            res = safe_add(L, typ, f"ok {typ} {i}", content, log=str(log))
            chk(is_added(res), f"type={typ}: content có số [{desc}] -> ĐƯỢC PHÉP (ví-dụ tái lập)")
            chk(len(read_log(log)) == 1, f"type={typ}: record ĐƯỢC ghi ({content!r})")

    # open-question: nếu implement dùng type 'open-question' cho gap → cũng phải cho số.
    for typ in ("open-question",):
        log = tmp / f"a5_oq_{typ}.jsonl"
        res = safe_add(L, typ, "cần chốt", "sample 12,345 đơn", log=str(log))
        # chấp nhận: added (nếu type tồn tại) — KHÔNG được reject vì số
        chk(not is_reject(res), f"type={typ}: có số -> KHÔNG bị chặn vì số (đó là ví dụ)")

    # --- HỆ-SỐ NHỎ / tỉ-lệ công thức / token version → KHÔNG bị chặn nhầm dù type cấu trúc ---
    small_ok = [
        ("0.015",  "hệ số nhỏ 0.015"),
        ("0.30",   "hệ số nhỏ 0.30"),
        ("rate 0.25 của AOP", "tỉ lệ 0.25 trong công thức"),
        ("flow v3", '"v3" token version'),
        ("cột a10", '"a10" mã cột'),
        ("×0,21 thuế", "hệ số 0,21"),
    ]
    for i, (content, desc) in enumerate(small_ok):
        log = tmp / f"a5_small_{i}.jsonl"
        res = safe_add(L, "fact", f"small {i}", content, log=str(log))
        chk(is_added(res), f"type=fact: [{desc}] -> KHÔNG chặn nhầm số nhỏ/tỉ-lệ/token ({content!r})")


# ─────────────────────────────────────────────────────────────────────────────
# A5 — regex bắt số (mở rộng): bắt đúng số lớn, KHÔNG bắt số nhỏ/token
# ─────────────────────────────────────────────────────────────────────────────
def test_a5_regex(L):
    print("== A5: regex bắt số lớn (mở rộng) — KHÔNG bắt hệ-số nhỏ / token ==")
    # Implement PHẢI phơi 1 hàm nhận biết số-cứng. Chấp các tên khả dĩ.
    detect = None
    for name in ("has_hard_number", "is_hard_number", "_has_hard_number",
                 "contains_absolute_number", "_HARD_NUM", "HARD_NUM_RE", "_NUM_RE"):
        obj = getattr(L, name, None)
        if obj is None:
            continue
        if callable(obj):
            detect = obj; break
        if hasattr(obj, "search"):     # compiled regex
            detect = (lambda rx: (lambda s: bool(rx.search(s))))(obj); break
    if detect is None:
        chk(False, "learn2 phơi hàm/regex nhận-biết-số-cứng (has_hard_number / HARD_NUM_RE ...) để test & tái dùng")
        return

    must_hit = ["1.234.567", "1,234,567", "45%", "12,3%", "3.141,59", "9 triệu",
                "351 tỷ", "445.043", "12,345", "987654"]
    must_miss = ["0.015", "0.30", "v3", "a10", "0,21", "rate 0.25", "GR7", "L0006"]
    for s in must_hit:
        chk(bool(detect(s)), f"regex BẮT số lớn: {s!r}")
    for s in must_miss:
        chk(not bool(detect(s)), f"regex KHÔNG bắt (nhỏ/token): {s!r}")


# ─────────────────────────────────────────────────────────────────────────────
# A1 — shim: learn.py FORWARD sang learn2 (ghi record kiểu learn2: content_hash + fact_key)
# ─────────────────────────────────────────────────────────────────────────────
def test_a1_shim_source(src):
    print("== A1: learn.py là SHIM forward → learn2 (governance) ==")
    low = src.lower()
    chk("learn2" in src, "learn.py có tham chiếu 'learn2' (forward target)")
    chk("[deprecated]" in low or "deprecated" in low, "learn.py in banner DEPRECATED")
    # KHÔNG còn tự xử lý số bằng warn-cũ như logic gốc (đã forward, không âm thầm dùng logic cũ):
    chk("import" in low and "learn2" in low, "learn.py IMPORT learn2 (không nhân bản logic gate)")


def _make_temp_kb(tmp):
    """Tạo 1 KB tối thiểu (marker .kgr_kb_root + learnings/) để CÔ LẬP: learn.py & learn2 resolve
    KB qua OAC_KB_ROOT env → ghi vào ĐÂY, TUYỆT ĐỐI không đụng log thật."""
    kb = tmp / "kb"; (kb / "learnings").mkdir(parents=True, exist_ok=True)
    (kb / ".kgr_kb_root").write_text("test-kb\n", encoding="utf-8")
    return kb

def test_a1_shim_runtime(tmp):
    print("== A1: chạy learn.py add -> đi qua learn2 (record có content_hash + fact_key), banner DEPRECATED ==")
    kb = _make_temp_kb(tmp)                                  # CÔ LẬP — không đụng log thật
    env = {**os.environ, "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8", "OAC_KB_ROOT": str(kb)}
    r = subprocess.run([sys.executable, str(LEARN_PY), "add", "lesson", "shim topic", "shim content no-number"],
                       cwd=str(KB), env=env, capture_output=True, text=True)
    out = (r.stdout or "") + (r.stderr or "")
    chk("deprecated" in out.lower(), f"CLI in banner DEPRECATED (stdout/stderr). Got: {out[:160]!r}")

    # forward THẬT: record ghi vào KB cô lập PHẢI mang ngữ nghĩa learn2 (content_hash + fact_key)
    tlog = kb / "learnings" / "log.jsonl"
    recs = read_log(tlog)
    chk(len(recs) >= 1, "learn.py add ghi được record (vào KB cô lập)")
    chk(bool(recs) and "content_hash" in recs[-1] and "fact_key" in recs[-1],
        "record shim forward mang content_hash + fact_key (ngữ nghĩa learn2, không phải learn.py cũ)")

    # import-fail thì exit≠0 (không âm thầm): kiểm SOURCE có nhánh exit≠0 khi import learn2 fail.
    src = LEARN_PY.read_text(encoding="utf-8", errors="replace").lower()
    has_fail_branch = ("except" in src and ("exit" in src or "systemexit" in src or "sys.exit" in src))
    chk(has_fail_branch, "learn.py có nhánh import-fail -> exit≠0 (không âm thầm dùng logic cũ)")


def test_a1_shim_forwards_record(L, tmp):
    print("== A1: bản learn2 vẫn ghi record chuẩn (content_hash + fact_key) — nền tảng shim forward ==")
    log = tmp / "fwd.jsonl"
    res = safe_add(L, "lesson", "forward topic", "nội dung không số", log=str(log))
    chk(is_added(res), "learn2.add lesson -> added")
    recs = read_log(log)
    chk(len(recs) == 1 and "content_hash" in recs[0] and "fact_key" in recs[0],
        "record có content_hash + fact_key (ngữ nghĩa learn2)")


# ─────────────────────────────────────────────────────────────────────────────
# A1 — doctor: field "learn_governance" (+ STATUS ATTENTION nếu learn.py KHÔNG phải shim)
# ─────────────────────────────────────────────────────────────────────────────
def test_a1_doctor():
    print("== A1: kgr.py doctor có field 'learn_governance' (shim ok + installed_copy) ==")
    env = {**os.environ, "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"}
    r = subprocess.run([sys.executable, str(KGR_PY), "doctor"], env=env, capture_output=True, text=True)
    out = r.stdout or ""
    try:
        rep = json.loads(out)
    except Exception:
        chk(False, f"doctor phải in JSON parse được. Got: {out[:200]!r}")
        return
    chk("learn_governance" in rep, "doctor output có key 'learn_governance'")
    lg = rep.get("learn_governance")
    if isinstance(lg, dict):
        chk("shim" in lg or "learn_py_is_shim" in lg or "is_shim" in lg,
            "learn_governance báo trạng thái shim (shim/is_shim)")
        chk("installed_copy" in lg or "installed" in lg,
            "learn_governance báo installed_copy (found/not-found/mismatch)")
    else:
        chk(False, f"learn_governance nên là dict mô tả (shim + installed_copy). Got: {type(lg).__name__}")


def test_a1_doctor_attention_when_not_shim(tmp):
    print("== A1: doctor -> STATUS ATTENTION khi learn.py KHÔNG phải shim (INV-6 fail ồn) ==")
    # Sao chép cây tối thiểu? Không khả thi rẻ. Thay vào: kiểm hàm doctor logic nếu phơi được,
    # else kiểm bằng cách tạm ghi learn.py giả (KHÔNG shim) rồi khôi phục.
    env = {**os.environ, "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"}
    orig_bytes = LEARN_PY.read_bytes()               # BYTE-level: khôi phục KHÔNG đổi line-ending
    try:
        # ghi 1 learn.py "cũ" không có marker 'learn2'
        LEARN_PY.write_bytes(b"#!/usr/bin/env python3\nprint('legacy learn, no forward')\n")
        r = subprocess.run([sys.executable, str(KGR_PY), "doctor"], env=env, capture_output=True, text=True)
        out = r.stdout or ""
        try:
            rep = json.loads(out)
        except Exception:
            chk(False, f"doctor JSON parse được (non-shim case). Got: {out[:200]!r}")
            return
        chk(rep.get("STATUS") == "ATTENTION",
            "learn.py KHÔNG-shim -> doctor STATUS=ATTENTION (fail ồn)")
        lg = rep.get("learn_governance")
        chk(isinstance(lg, dict) and (str(lg).lower().find("shim") >= 0),
            "learn_governance phản ánh non-shim (báo lỗi shim)")
    finally:
        LEARN_PY.write_bytes(orig_bytes)              # KHÔI PHỤC nguyên byte (giữ CRLF)


# ─────────────────────────────────────────────────────────────────────────────
# A1 — call-sites: đã trỏ learn2, không còn 'learn.py add' trần / write_via 'learn.py'
# ─────────────────────────────────────────────────────────────────────────────
def test_a1_callsites():
    print("== A1: call-sites trỏ learn2 (không còn learn.py trần) ==")

    # 1) kb_route.py: write_via không còn "learn.py" (đã là learn2)
    route_src = KB_ROUTE_PY.read_text(encoding="utf-8", errors="replace")
    chk('"write_via": "learn.py"' not in route_src and "'write_via': 'learn.py'" not in route_src,
        "kb_route.py: không còn write_via 'learn.py' trần")
    chk("learn2" in route_src, "kb_route.py: có tham chiếu learn2")
    # bảng ROUTES: các LOG-type (correction/lesson/qa) target/write_via trỏ learn2
    try:
        import importlib
        if "kb_route" in sys.modules:
            importlib.reload(sys.modules["kb_route"])
        import kb_route as R
        for t in ("correction", "lesson", "qa"):
            r = R.classify(t)
            wv = str(r.get("write_via", "")) + " " + str(r.get("target", ""))
            chk("learn2" in wv and "learn.py add" not in wv,
                f"kb_route.classify({t}): write_via/target trỏ learn2, không 'learn.py add'")
    except Exception as e:
        chk(False, f"import/kb_route.classify lỗi: {e}")

    # 2) LEARNING.md: không còn lệnh 'learn.py add' trần (phải là learn2)
    lm = LEARNING_MD.read_text(encoding="utf-8", errors="replace")
    chk(not re.search(r"(?<!learn2\.py)\blearn\.py add\b", lm) or "learn2" in lm,
        "LEARNING.md: lệnh add trỏ learn2 (không 'learn.py add' trần)")
    chk("learn2" in lm, "LEARNING.md: có tham chiếu learn2")

    # 3) pending.md: quy trình promote trỏ learn2
    pm = PENDING_MD.read_text(encoding="utf-8", errors="replace")
    chk("learn2" in pm and "learn.py promote" not in pm,
        "pending.md: promote trỏ learn2 (không 'learn.py promote' trần)")

    # 4) OWNER_PENDING.md: đã trỏ learn2 (không còn khuyến nghị dùng learn.py cũ như đích)
    op = OWNER_PENDING_MD.read_text(encoding="utf-8", errors="replace")
    chk("learn2" in op, "OWNER_PENDING.md: có tham chiếu learn2")

    # 5) SKILL.md kgr-oac-lineage: add + promote trỏ learn2
    sl = SKILL_LINEAGE.read_text(encoding="utf-8", errors="replace")
    chk("learn2" in sl, "SKILL.md (lineage): có tham chiếu learn2 (add/promote)")

    # 6) SKILL.md orchestrator: trỏ learn2
    if SKILL_ORCH.is_file():
        so = SKILL_ORCH.read_text(encoding="utf-8", errors="replace")
        chk("learn2" in so, "SKILL.md (orchestrator): có tham chiếu learn2")
    else:
        chk(False, f"không thấy SKILL.md orchestrator: {SKILL_ORCH}")


# ─────────────────────────────────────────────────────────────────────────────
def main():
    import learn2 as L
    tmp = Path(tempfile.mkdtemp(prefix="kgr_sprint2_"))
    try:
        # A5
        test_a5_gate_by_type(L, tmp)
        test_a5_regex(L)
        # A1 shim
        src = LEARN_PY.read_text(encoding="utf-8", errors="replace")
        test_a1_shim_source(src)
        test_a1_shim_runtime(tmp)
        test_a1_shim_forwards_record(L, tmp)
        # A1 doctor
        test_a1_doctor()
        test_a1_doctor_attention_when_not_shim(tmp)
        # A1 call-sites
        test_a1_callsites()

        print(f"\n== TỔNG SPRINT2: PASS={PASS} FAIL={FAIL} ==")
        return 1 if FAIL else 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
