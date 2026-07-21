#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""OAC Token Manager — app cửa sổ để NẠP token OAC (không cần gõ lệnh).

Dùng khi nào: tải token mới từ OAC (Profile → Access Tokens → Download) → mở app này
→ bấm "Chọn file token…" → bấm "NẠP TOKEN". Xong. App tự đặt đúng chỗ/đúng tên mà
MCP `oac-native` cần, tự siết quyền file, tự backup bản cũ.

Chạy: python oac_token_gui.py   (hoặc double-click file OAC-Token.bat)
Lõi xử lý dùng chung với oac_token.py (một nguồn sự thật).
"""
import os, sys, io, glob, threading, datetime as _dt
from contextlib import redirect_stdout

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import oac_token as core  # noqa: E402

try:
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox
except Exception:
    print("Thiếu tkinter — cài Python bản có tcl/tk rồi chạy lại.")
    raise

DOWNLOADS = os.path.join(os.path.expanduser("~"), "Downloads")
OK, BAD, WARN = "#1d9e75", "#e24b4a", "#ba7517"


def _capture(fn, *a):
    """Chạy hàm của core, thu output text để đổ vào ô Log."""
    buf = io.StringIO()
    try:
        with redirect_stdout(buf):
            rc = fn(*a)
    except SystemExit as e:
        return 1, f"{buf.getvalue()}\n{e}"
    except Exception as e:
        return 1, f"{buf.getvalue()}\nLỖI: {e}"
    return rc, buf.getvalue()


class App:
    def __init__(self, root):
        self.root = root
        self.picked = None
        root.title("OAC Token Manager")
        root.geometry("720x520")
        root.minsize(660, 480)

        pad = dict(padx=14, pady=6)
        ttk.Label(root, text="OAC Token Manager", font=("Segoe UI", 15, "bold")).pack(anchor="w", padx=14, pady=(12, 0))
        ttk.Label(root, text="Tải token mới từ OAC → chọn file → bấm NẠP TOKEN.",
                  foreground="#5f5e5a").pack(anchor="w", padx=14)

        # ── khối trạng thái ──
        box = ttk.LabelFrame(root, text=" Trạng thái token hiện tại ")
        box.pack(fill="x", **pad)
        self.lbl_state = ttk.Label(box, text="đang kiểm…", font=("Segoe UI", 13, "bold"))
        self.lbl_state.pack(anchor="w", padx=12, pady=(10, 2))
        self.lbl_user = ttk.Label(box, text="")
        self.lbl_user.pack(anchor="w", padx=12)
        self.lbl_exp = ttk.Label(box, text="")
        self.lbl_exp.pack(anchor="w", padx=12)
        self.lbl_path = ttk.Label(box, text="", foreground="#5f5e5a")
        self.lbl_path.pack(anchor="w", padx=12, pady=(0, 10))

        # ── chọn file ──
        pick = ttk.LabelFrame(root, text=" Nạp token mới ")
        pick.pack(fill="x", **pad)
        row = ttk.Frame(pick)
        row.pack(fill="x", padx=12, pady=(10, 4))
        ttk.Button(row, text="📂  Chọn file token…", command=self.choose).pack(side="left")
        self.lbl_pick = ttk.Label(row, text="  (chưa chọn)", foreground="#5f5e5a")
        self.lbl_pick.pack(side="left", padx=8)
        row2 = ttk.Frame(pick)
        row2.pack(fill="x", padx=12, pady=(0, 10))
        self.btn_load = ttk.Button(row2, text="⬆  NẠP TOKEN", command=self.do_load, state="disabled")
        self.btn_load.pack(side="left")
        ttk.Button(row2, text="🔄  Gia hạn ngay", command=self.do_refresh).pack(side="left", padx=6)
        ttk.Button(row2, text="↻  Kiểm tra lại", command=self.refresh_status).pack(side="left")

        # ── log ──
        lg = ttk.LabelFrame(root, text=" Nhật ký ")
        lg.pack(fill="both", expand=True, **pad)
        self.log = tk.Text(lg, height=9, wrap="word", font=("Consolas", 9))
        self.log.pack(fill="both", expand=True, padx=10, pady=10)
        self.log.configure(state="disabled")

        self.refresh_status()
        self.suggest_newest()

    # ── helpers ──
    def say(self, msg):
        self.log.configure(state="normal")
        self.log.insert("end", f"[{_dt.datetime.now():%H:%M:%S}] {msg.rstrip()}\n")
        self.log.see("end")
        self.log.configure(state="disabled")

    def suggest_newest(self):
        """Tự gợi ý file tokens*.json mới nhất trong Downloads."""
        c = glob.glob(os.path.join(DOWNLOADS, "tokens*.json"))
        if not c:
            return
        newest = max(c, key=os.path.getmtime)
        age = (_dt.datetime.now() - _dt.datetime.fromtimestamp(os.path.getmtime(newest)))
        mins = int(age.total_seconds() // 60)
        human = f"{mins} phút trước" if mins < 90 else f"{mins // 60} giờ trước"
        self.set_pick(newest, note=f" (gợi ý: mới nhất — {human})")
        self.say(f"Gợi ý file mới nhất trong Downloads: {os.path.basename(newest)} ({human})")

    def set_pick(self, path, note=""):
        self.picked = path
        self.lbl_pick.config(text=f"  {os.path.basename(path)}{note}")
        self.btn_load.config(state="normal")

    def choose(self):
        p = filedialog.askopenfilename(
            title="Chọn file token tải từ OAC",
            initialdir=DOWNLOADS,
            filetypes=[("Token JSON", "tokens*.json"), ("JSON", "*.json"), ("Tất cả", "*.*")],
        )
        if p:
            self.set_pick(p)
            self.say(f"Đã chọn: {p}")

    # ── hành động ──
    def refresh_status(self):
        try:
            url, path = core.mcp_config()
        except SystemExit as e:
            self.lbl_state.config(text="❌ Không đọc được cấu hình", foreground=BAD)
            self.say(str(e))
            return
        self.lbl_path.config(text=f"Đích: {path}")
        tk_ = core.read_tokens(path)
        if not tk_ or not tk_.get("accessToken"):
            self.lbl_state.config(text="❌ CHƯA CÓ TOKEN", foreground=BAD)
            self.lbl_user.config(text="")
            self.lbl_exp.config(text="→ Chọn file token rồi bấm NẠP TOKEN")
            return
        c = core.jwt_claims(tk_["accessToken"])
        secs, desc = core._left(c)
        live = secs is not None and secs > 0
        soon = live and secs < 600
        self.lbl_state.config(
            text="✅ CÒN SỐNG" if live and not soon else ("⚠ SẮP HẾT HẠN" if soon else "❌ ĐÃ HẾT HẠN"),
            foreground=OK if (live and not soon) else (WARN if soon else BAD),
        )
        self.lbl_user.config(text=f"Tài khoản: {c.get('sub', '?')}")
        rt = "có refreshToken → gia hạn được" if tk_.get("refreshToken") else "KHÔNG có refreshToken"
        self.lbl_exp.config(text=f"{desc}  ·  {rt}")

    def do_load(self):
        if not self.picked:
            return
        rc, out = _capture(core.cmd_load, self.picked)
        for line in out.splitlines():
            if line.strip():
                self.say(line)
        self.refresh_status()
        if rc == 0:
            messagebox.showinfo("Xong", "Đã nạp token.\n\nMở lại session Claude (hoặc reconnect MCP oac-native) để nó dùng token mới.")
        else:
            messagebox.showwarning("Chưa nạp được", "Xem Nhật ký để biết lý do.")

    def do_refresh(self):
        def run():
            rc, out = _capture(core.cmd_refresh)
            for line in out.splitlines():
                if line.strip():
                    self.say(line)
            self.refresh_status()
        threading.Thread(target=run, daemon=True).start()
        self.say("Đang gọi gia hạn…")


if __name__ == "__main__":
    root = tk.Tk()
    try:
        ttk.Style().theme_use("vista")
    except Exception:
        pass
    App(root)
    root.mainloop()
