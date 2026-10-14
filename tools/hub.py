#!/usr/bin/env python3
"""Local study hub. Serves hub/ and docs/ on 127.0.0.1 and saves your answers into the repo.

  uv run python tools/hub.py            start on http://127.0.0.1:8765 and open the browser
  uv run python tools/hub.py --no-open  start without opening a browser

Answers land in progress/answers/<lesson>.json, so they are versioned in git and the tutor can read them.
Stdlib only. Binds to localhost. Every write needs the X-Hub header, which other websites cannot send
to a localhost server without a CORS preflight that this server refuses.
"""
import json, mimetypes, re, subprocess, sys, threading, webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import learn  # noqa: E402

PORT = 8765
ANS = ROOT / "progress" / "answers"
LOCK = threading.Lock()
LESSON_RE = re.compile(r"^[A-Za-z0-9_-]{1,32}$")
STATIC_ROOTS = ("hub", "docs")


def now():
    import datetime as dt
    return dt.datetime.now().isoformat(timespec="seconds")


def state_payload():
    st = learn.load_state()
    mods = []
    for m in learn.CUR["modules"]:
        mid = m["id"]
        mods.append({"id": mid, "title": m["title"], "part": m["part"], "assignment": m["assignment"],
                     "requires": m.get("requires", []), "status": st[mid]["status"],
                     "scores": learn.best_scores(mid), "mastered_on": st[mid].get("mastered_on", "")})
    lessons = {}
    for f in ANS.glob("*.json") if ANS.exists() else []:
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
            lessons[f.stem] = {"updated": d.get("_updated", ""), "fields": len([k for k in d if not k.startswith("_")])}
        except Exception:
            pass
    return {"modules": mods, "threshold": learn.THRESH, "cards_due": len(learn.due_cards()),
            "cards_total": len(learn.cards()), "lessons": lessons}


def run_lab(lab):
    r = subprocess.run([sys.executable, str(ROOT / "tools" / "learn.py"), "lab", lab], cwd=ROOT,
                       capture_output=True, text=True, timeout=180, env={**__import__("os").environ, "PYTHONUTF8": "1"})
    return {"ok": r.returncode == 0, "output": (r.stdout + r.stderr)[-6000:]}


class H(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def send_json(self, obj, code=200):
        b = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(b)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(b)

    def body(self):
        n = int(self.headers.get("Content-Length") or 0)
        return json.loads(self.rfile.read(n) or b"{}") if n else {}

    def guard(self):
        if self.headers.get("X-Hub") != "1":
            self.send_json({"error": "missing X-Hub header"}, 403)
            return False
        return True

    def do_GET(self):
        p = self.path.split("?")[0]
        if p == "/api/state":
            return self.send_json(state_payload())
        m = re.fullmatch(r"/api/answers/([A-Za-z0-9_-]{1,32})", p)
        if m:
            f = ANS / f"{m.group(1)}.json"
            return self.send_json(json.loads(f.read_text(encoding="utf-8")) if f.exists() else {})
        if p == "/api/cards/due":
            return self.send_json(learn.due_cards())
        return self.static(p)

    def do_PUT(self):
        if not self.guard():
            return
        m = re.fullmatch(r"/api/answers/([A-Za-z0-9_-]{1,32})", self.path)
        if not m:
            return self.send_json({"error": "not found"}, 404)
        ANS.mkdir(parents=True, exist_ok=True)
        f = ANS / f"{m.group(1)}.json"
        with LOCK:
            d = json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}
            d.update(self.body())
            d["_updated"] = now()
            f.write_text(json.dumps(d, indent=1, ensure_ascii=False), encoding="utf-8")
        return self.send_json({"ok": True, "updated": d["_updated"]})

    def do_POST(self):
        if not self.guard():
            return
        p = self.path
        m = re.fullmatch(r"/api/lab/(L\d+)", p)
        if m:
            try:
                return self.send_json(run_lab(m.group(1)))
            except subprocess.TimeoutExpired:
                return self.send_json({"ok": False, "output": "Timed out after 180 s."})
        m = re.fullmatch(r"/api/cards/(\d+)/review", p)
        if m:
            g = int(self.body().get("grade", -1))
            if not 0 <= g <= 5:
                return self.send_json({"error": "grade 0-5"}, 400)
            with LOCK:
                learn.card_review(int(m.group(1)), g)
            return self.send_json({"ok": True})
        if p == "/api/cards":
            b = self.body()
            with LOCK:
                learn.card_add(str(b["q"])[:400], str(b["a"])[:800], str(b.get("module", ""))[:8])
            return self.send_json({"ok": True})
        return self.send_json({"error": "not found"}, 404)

    def static(self, p):
        if p in ("/", ""):
            p = "/hub/index.html"
        parts = [x for x in p.split("/") if x]
        if not parts or parts[0] not in STATIC_ROOTS or ".." in parts:
            return self.send_json({"error": "not found"}, 404)
        f = (ROOT.joinpath(*parts)).resolve()
        if not f.is_file() or not str(f).startswith(str(ROOT.resolve())):
            return self.send_json({"error": "not found"}, 404)
        data = f.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", (mimetypes.guess_type(str(f))[0] or "application/octet-stream") + "; charset=utf-8" if f.suffix in (".html", ".js", ".css", ".json") else (mimetypes.guess_type(str(f))[0] or "application/octet-stream"))
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)


def main():
    srv = ThreadingHTTPServer(("127.0.0.1", PORT), H)
    url = f"http://127.0.0.1:{PORT}/"
    print(f"Study hub on {url}  (Ctrl+C to stop)")
    if "--no-open" not in sys.argv:
        webbrowser.open(url)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
