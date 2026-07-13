#!/usr/bin/env python3
"""Tiny demo service for the sandbox platform.

Only the Python standard library — no pip install, so the container build never
flakes on a package registry. Change GREETING (or VERSION) below, publish, send
it to review, push to GitHub: that whole loop is what this repo exists to test.
"""
import json
import os
import socket
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

GREETING = "Hello from the sandbox! 👋"
VERSION = "1.0.0"
DEFAULT_PORT = 8000


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="text/html; charset=utf-8"):
        data = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path == "/health":
            self._send(200, json.dumps({"status": "ok"}), "application/json")
        elif self.path == "/api/info":
            info = {
                "service": "sandbox-demo",
                "version": VERSION,
                "greeting": GREETING,
                "host": socket.gethostname(),
                "time": datetime.now(timezone.utc).isoformat(),
            }
            self._send(200, json.dumps(info, ensure_ascii=False), "application/json")
        else:
            page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>sandbox demo</title>
<style>
  body {{ font-family: system-ui, -apple-system, sans-serif; margin: 0;
         display: grid; place-items: center; min-height: 100vh;
         background: #0f172a; color: #e2e8f0; }}
  .card {{ text-align: center; padding: 2.5rem 3rem; background: #1e293b;
          border-radius: 16px; box-shadow: 0 10px 40px rgba(0,0,0,.45); }}
  h1 {{ margin: 0 0 .5rem; font-size: 2rem; }}
  p {{ margin: .35rem 0; }}
  .meta {{ color: #94a3b8; font-size: .9rem; margin-top: 1.25rem; }}
  .footer {{ color: #64748b; font-size: .8rem; margin-top: .75rem; }}
  code {{ color: #7dd3fc; }}
</style></head>
<body><div class="card">
  <h1>{GREETING}</h1>
  <p>version <code>{VERSION}</code></p>
  <p>host <code>{socket.gethostname()}</code></p>
  <p class="meta">try <code>/health</code> and <code>/api/info</code></p>
  <p class="footer">running in the sandbox ✨</p>
</div></body></html>"""
            self._send(200, page)

    def log_message(self, fmt, *args):
        pass  # keep container logs quiet


if __name__ == "__main__":
    port = int(os.environ.get("PORT", DEFAULT_PORT))
    print(f"sandbox-demo v{VERSION} listening on :{port}", flush=True)
    ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()
