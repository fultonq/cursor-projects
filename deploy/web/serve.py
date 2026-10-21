#!/usr/bin/env python3
"""Local/dev static server with SPA fallback (same as Render rewrite)."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent


class SpaHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self):
        path = (ROOT / self.path.lstrip("/").split("?", 1)[0]).resolve()
        if self.path in ("/", "") or path.is_file():
            return super().do_GET()
        self.path = "/index.html"
        return super().do_GET()


if __name__ == "__main__":
    ThreadingHTTPServer(("0.0.0.0", 4173), SpaHandler).serve_forever()
