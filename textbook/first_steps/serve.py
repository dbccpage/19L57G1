"""Loopback-only preview with portable JavaScript MIME types.

AuthorityEffect: None. No external hosting or publication.
"""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import argparse


class Handler(SimpleHTTPRequestHandler):
    extensions_map = {
        **SimpleHTTPRequestHandler.extensions_map,
        ".mjs": "text/javascript", ".js": "text/javascript",
        ".json": "application/json", ".css": "text/css",
    }

    def do_GET(self):
        # A preview must not retain a stale script or its old MIME type.
        if "If-Modified-Since" in self.headers:
            del self.headers["If-Modified-Since"]
        super().do_GET()

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    directory = Path(__file__).resolve().parent
    with ThreadingHTTPServer(("127.0.0.1", args.port), partial(Handler, directory=str(directory))) as server:
        print(f"http://127.0.0.1:{args.port}/explorer.html", flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
