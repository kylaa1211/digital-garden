"""Serve Umwelt locally and open the Applications folder on macOS."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit

HOST = "127.0.0.1"
PORT = 8001
FINDER_ROUTE = "/_local/open-applications"
ROOT = Path(__file__).resolve().parent
PUBLIC_FILES = {"/", "/index.html", "/onboarding.html", "/controls.css", "/app-names.js"}


class PreviewHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args):
        super().__init__(*args, directory=str(ROOT))

    def handle_asset(self, method):
        if self.headers.get("Host") != f"{HOST}:{PORT}":
            self.send_error(403)
            return
        path = unquote(urlsplit(self.path).path)
        if path == FINDER_ROUTE:
            self.send_response(204 if sys.platform == "darwin" else 404)
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
        elif path in PUBLIC_FILES or re.fullmatch(r"/icons/[\w.-]+\.png", path):
            method()
        else:
            self.send_error(404)

    def do_GET(self):
        self.handle_asset(super().do_GET)

    def do_HEAD(self):
        self.handle_asset(super().do_HEAD)

    def do_POST(self):
        host = f"{HOST}:{PORT}"
        if self.path != FINDER_ROUTE or sys.platform != "darwin":
            self.send_error(404)
            return
        if (self.headers.get("Host") != host
                or self.headers.get("Origin") != f"http://{host}"
                or self.headers.get("X-Umwelt-Action") != "open-applications"):
            self.send_error(403)
            return
        try:
            subprocess.run(
                ["/usr/bin/open", "-a", "Finder", "/Applications"],
                check=True, timeout=5,
            )
        except (OSError, subprocess.SubprocessError):
            self.send_error(500, "Could not open Applications in Finder")
            return
        self.send_response(204)
        self.end_headers()


if __name__ == "__main__":
    print(f"Umwelt preview: http://{HOST}:{PORT}/onboarding.html", flush=True)
    with ThreadingHTTPServer((HOST, PORT), PreviewHandler) as server:
        server.serve_forever()
