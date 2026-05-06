#!/usr/bin/env python
"""Mini Office local browser runner."""

import argparse
import json
import http.server
import os
import socketserver
import sys
import webbrowser
from pathlib import Path

DEFAULT_PORT = int(os.environ.get("MINI_OFFICE_PORT", "8000"))
DIRECTORY = Path(__file__).parent.resolve()


class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


class CustomHandler(http.server.SimpleHTTPRequestHandler):
    """Serve Mini Office static files."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        """Serve index.html for the app root."""
        if self.path == "/":
            self.path = "/index.html"
        return super().do_GET()

    def log_message(self, format, *args):
        """Print a compact local log."""
        print(f"[{self.log_date_time_string()}] {args[0]}")


def build_parser():
    parser = argparse.ArgumentParser(description="Run Mini Office locally.")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--no-browser", action="store_true")
    parser.add_argument("--status", action="store_true", help="Print runtime status and exit.")
    return parser


def runtime_status(port=DEFAULT_PORT):
    index_path = DIRECTORY / "index.html"
    return {
        "product": "Mini Office",
        "profile": "local_static_app",
        "directory": str(DIRECTORY),
        "index_exists": index_path.exists(),
        "port": port,
    }


def main(argv=None):
    """Run the local Mini Office static app."""
    args = build_parser().parse_args(argv)
    if args.status:
        print(json.dumps(runtime_status(args.port), indent=2))
        return 0

    os.chdir(DIRECTORY)

    status = runtime_status(args.port)
    if not status["index_exists"]:
        print(f"ERROR: index.html not found in {DIRECTORY}")
        return 1

    with ReusableTCPServer(("127.0.0.1", args.port), CustomHandler) as httpd:
        url = f"http://127.0.0.1:{args.port}"

        print("MINI OFFICE - local browser runner")
        print(f"Server: {url}")
        print(f"Directory: {DIRECTORY}")
        print("Press Ctrl+C to stop")

        if not args.no_browser and os.environ.get("MINI_OFFICE_NO_BROWSER") != "1":
            try:
                webbrowser.open(url, new=2)
                print(f"Browser opening: {url}")
            except Exception:
                print(f"Open manually: {url}")

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopping server...")
            httpd.shutdown()
        return 0


if __name__ == "__main__":
    sys.exit(main())
