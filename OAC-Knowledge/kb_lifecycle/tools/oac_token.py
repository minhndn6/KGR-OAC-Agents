#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""oac_token.py — quản lý token OAC cho MCP `oac-native` (hết cảnh đăng nhập thủ công).

    python oac_token.py status            # token còn sống? còn bao lâu? có refreshToken?
    python oac_token.py refresh           # TỰ GIA HẠN bằng refreshToken — KHÔNG cần đăng nhập
    python oac_token.py load [file]       # nạp token mới (mặc định: tokens*.json MỚI NHẤT trong Downloads)
    python oac_token.py auto              # status → hết hạn/sắp hết thì tự refresh (dùng cho doctor/cron)

Vì sao có tool này: config `oac-native` trong ~/.claude.json trỏ token path TÊN CHÍNH XÁC
(`tokens.json`), nhưng Chrome tải về luôn là `tokens (N).json` → copy nguyên tên = MCP không thấy
token → "gián đoạn". Tool tự đọc path+URL TỪ CHÍNH config nên không bao giờ sai tên nữa.

BẢO MẬT: KHÔNG BAO GIỜ in giá trị token (chỉ in độ dài + claim exp/sub). File ghi xong siết ACL owner-only.
Exit code: 0 = token LIVE · 1 = hết hạn/thiếu/lỗi  (dùng được trong script).
"""
import sys, os, json, base64, glob, shutil, subprocess, urllib.request, urllib.error
import datetime as _dt

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

REFRESH_PATH = "/api/20210901/security/tokens/token/refresh"
WARN_SECONDS = 300  # còn dưới 5 phút coi như "sắp hết" → auto refresh


# ── đọc cấu hình THẬT của oac-native (không hardcode) ────────────────────────
def mcp_config(server="oac-native"):
    """Trả (url, token_path) đọc từ ~/.claude.json → mcpServers[server].args."""
    cfg = os.path.join(os.path.expanduser("~"), ".claude.json")
    try:
        with open(cfg, encoding="utf-8") as f:
            d = json.load(f)
        args = (d.get("mcpServers", {}).get(server) or {}).get("args") or []
    except Exception as e:
        raise SystemExit(f"KHÔNG đọc được {cfg}: {e}")
    url = next((a for a in args if str(a).startswith("http")), None)
    tok = next((a for a in args if str(a).lower().endswith(".json")
                and "mcp-connect" not in str(a).lower()), None)
    if not url or not tok:
        raise SystemExit(f"config '{server}' thiếu url/token-path. args={args}")
    return url.rstrip("/"), tok


# ── JWT: chỉ ĐỌC claim, không verify chữ ký (đủ để biết còn hạn) ─────────────
def jwt_claims(token):
    try:
        payload = token.split(".")[1]
        payload += "=" * (-len(payload) % 4)
        return json.loads(base64.urlsafe_b64decode(payload))
    except Exception:
        return {}


def read_tokens(path):
    if not os.path.isfile(path):
        return None
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"  ⚠ token file hỏng ({e})")
        return None


def write_tokens(path, obj):
    """Ghi nguyên tử + siết ACL owner-only (tương đương chmod 600)."""
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)
    os.replace(tmp, path)
    if os.name == "nt":
        user = os.environ.get("USERNAME", "")
        subprocess.run(["icacls", path, "/inheritance:r", "/grant:r", f"{user}:(R,W)"],
                       capture_output=True)
    else:
        os.chmod(path, 0o600)


def _left(claims):
    """Trả (giây_còn_lại, chuỗi_mô_tả). None nếu không có exp."""
    exp = claims.get("exp")
    if not exp:
        return None, "không đọc được exp"
    now = _dt.datetime.now(_dt.timezone.utc).timestamp()
    secs = int(exp - now)
    when = _dt.datetime.fromtimestamp(exp, _dt.timezone.utc).astimezone()
    if secs <= 0:
        return secs, f"HẾT HẠN {-secs // 60} phút trước (lúc {when:%Y-%m-%d %H:%M})"
    return secs, f"còn {secs // 60} phút {secs % 60}s (hết lúc {when:%Y-%m-%d %H:%M})"


# ── lệnh ─────────────────────────────────────────────────────────────────────
def cmd_status(quiet=False):
    url, path = mcp_config()
    tk = read_tokens(path)
    if not quiet:
        print(f"OAC       : {url}")
        print(f"Token file: {path}")
    if tk is None:
        print("  ❌ KHÔNG có token file (đúng tên `tokens.json`?) → chạy: oac_token.py load")
        return 1, None, None
    at, rt = tk.get("accessToken"), tk.get("refreshToken")
    if not at:
        print("  ❌ thiếu accessToken")
        return 1, tk, path
    c = jwt_claims(at)
    secs, desc = _left(c)
    live = secs is not None and secs > 0
    if not quiet:
        print(f"  user        : {c.get('sub', '?')}")
        print(f"  accessToken : {'✅ LIVE' if live else '❌ HẾT HẠN'} — {desc}")
        print(f"  refreshToken: {'✅ CÓ (' + str(len(rt)) + ' ký tự)' if rt else '❌ KHÔNG có'}")
        if live and rt:
            print("  → gia hạn: `oac_token.py refresh` (phải chạy TRƯỚC khi hết hạn)")
        elif not live:
            print("  ⚠ ĐÃ hết hạn ⇒ refresh KHÔNG cứu được (endpoint đòi token còn hạn).")
            print("     → tải token mới → `oac_token.py load` → hẹn giờ `oac_token.py auto` để khỏi hết hạn nữa.")
    return (0 if live else 1), tk, path


def cmd_refresh():
    """Gọi endpoint refresh bằng refreshToken → ghi accessToken mới. KHÔNG cần đăng nhập."""
    url, path = mcp_config()
    tk = read_tokens(path)
    if not tk or not tk.get("refreshToken"):
        print("❌ không có refreshToken → phải tải token mới (oac_token.py load)")
        return 1
    secs, desc = _left(jwt_claims(tk.get("accessToken", "")))
    if secs is not None and secs <= 0:
        # BẢN CHẤT (verified 2026-07-21): endpoint refresh ĐÒI accessToken CÒN HẠN trong header.
        # Hết hạn rồi thì gateway trả 401 (HTML) — refresh KHÔNG cứu được nữa.
        print(f"❌ accessToken {desc} → refresh KHÔNG dùng được nữa.")
        print("   Endpoint refresh đòi access-token CÒN HẠN ⇒ phải gia hạn TRƯỚC khi hết.")
        print("   Cách xử: tải token mới 1 lần (OAC → Profile → Access Tokens → Download)")
        print("            → `oac_token.py load` → rồi hẹn giờ chạy `oac_token.py auto` để không bao giờ hết hạn nữa.")
        return 1

    req = urllib.request.Request(
        url + REFRESH_PATH,
        data=tk["refreshToken"].encode("utf-8"),
        method="POST",
        headers={"Authorization": "Bearer " + tk.get("accessToken", ""),
                 "Content-Type": "text/plain",
                 "Accept": "application/json",
                 "User-Agent": "oac-token-tool/1.0"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            body = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", "replace")
        if raw.lstrip().startswith("<"):
            print(f"❌ refresh FAIL (HTTP {e.code}, trả HTML) — access-token hết hạn HOẶC WAF chặn.")
            print("   → tải token mới 1 lần rồi dùng `auto` định kỳ (xem README lệnh).")
        else:
            print(f"❌ refresh FAIL (HTTP {e.code}): {raw[:200]}")
        return 1
    except Exception as e:
        print(f"❌ refresh lỗi mạng: {e}")
        return 1

    new = dict(tk)
    for k in ("accessToken", "refreshToken", "expiresIn"):
        if body.get(k):
            new[k] = body[k]
    if new.get("accessToken") == tk.get("accessToken"):
        print("⚠ server không trả accessToken mới — kiểm tra lại endpoint/quyền.")
        return 1
    write_tokens(path, new)
    _, desc = _left(jwt_claims(new["accessToken"]))
    print(f"✅ ĐÃ GIA HẠN (không cần đăng nhập) — accessToken mới {desc}")
    print(f"   ghi vào: {path} (ACL owner-only)")
    print("   → reconnect MCP `oac-native` (hoặc mở session mới) nếu nó cache token lúc khởi động.")
    return 0


def cmd_load(src=None):
    """Nạp token mới: mặc định lấy tokens*.json MỚI NHẤT trong Downloads, tự đổi tên đúng."""
    url, path = mcp_config()
    if not src:
        dl = os.path.join(os.path.expanduser("~"), "Downloads")
        cands = glob.glob(os.path.join(dl, "tokens*.json"))
        if not cands:
            print(f"❌ không thấy tokens*.json trong {dl} → tải từ OAC: Profile → Access Tokens → Download")
            return 1
        src = max(cands, key=os.path.getmtime)
    if not os.path.isfile(src):
        print(f"❌ không thấy file: {src}")
        return 1
    try:
        with open(src, encoding="utf-8") as f:
            new = json.load(f)
    except Exception as e:
        print(f"❌ file không phải JSON hợp lệ: {e}")
        return 1
    if not new.get("accessToken"):
        print("❌ file thiếu accessToken — đây có phải tokens.json tải từ OAC không?")
        return 1
    c = jwt_claims(new["accessToken"])
    secs, desc = _left(c)
    if secs is not None and secs <= 0:
        print(f"⚠ token trong file ĐÃ HẾT HẠN ({desc}) — vẫn nạp, nhưng nên refresh/tải lại.")
    if os.path.isfile(path):
        bak = path + ".bak-" + _dt.datetime.now().strftime("%Y%m%d-%H%M%S")
        shutil.copy2(path, bak)
    write_tokens(path, new)
    print(f"✅ ĐÃ NẠP: {os.path.basename(src)} → {path}  (đổi đúng tên + ACL owner-only)")
    print(f"   user={c.get('sub', '?')} · accessToken {desc}")
    print(f"   refreshToken: {'CÓ → về sau chỉ cần `refresh`, khỏi đăng nhập' if new.get('refreshToken') else 'KHÔNG'}")
    return 0


def cmd_auto():
    """Dùng cho doctor/cron: còn hạn thì thôi, sắp/đã hết thì tự refresh."""
    rc, tk, path = cmd_status(quiet=True)
    secs = None
    if tk and tk.get("accessToken"):
        secs, _ = _left(jwt_claims(tk["accessToken"]))
    if secs is not None and secs > WARN_SECONDS:
        print(f"✅ token còn {secs // 60} phút — không cần làm gì")
        return 0
    print("⏳ token hết/sắp hết → tự refresh…")
    return cmd_refresh()


def main(argv):
    cmd = (argv[0] if argv else "status").lower()
    if cmd == "status":
        return cmd_status()[0]
    if cmd == "refresh":
        return cmd_refresh()
    if cmd == "load":
        return cmd_load(argv[1] if len(argv) > 1 else None)
    if cmd == "auto":
        return cmd_auto()
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
