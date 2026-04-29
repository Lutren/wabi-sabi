#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer

HOST = "127.0.0.1"
PORT = 4444

HTML = b"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>ClaudioOS Mission Control</title>
<style>
body{font-family:system-ui,Segoe UI,sans-serif;margin:32px;background:#101418;color:#f1f5f9}
button{padding:10px 14px;margin:4px;border:1px solid #475569;background:#1e293b;color:#f8fafc}
pre{background:#020617;border:1px solid #334155;padding:16px;white-space:pre-wrap}
</style>
</head>
<body>
<h1>ClaudioOS Mission Control</h1>
<button onclick="health()">Guardian Health</button>
<button onclick="safe()">Safe Decision</button>
<button onclick="danger()">Dangerous Decision</button>
<button onclick="events()">Events</button>
<pre id="out">Ready.</pre>
<script>
const out=document.getElementById('out');
async function show(p){out.textContent=JSON.stringify(await p,null,2)}
async function health(){show((await fetch('http://127.0.0.1:4787/health')).json())}
async function events(){show((await fetch('http://127.0.0.1:4787/events')).json())}
async function decide(payload){show((await fetch('http://127.0.0.1:4787/decide',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)})).json())}
async function safe(){decide({action:'local_render',evidence:true,R:0.22,epsilon:0.1})}
async function danger(){decide({action:'publish',tags:['publish'],evidence:true,R:0.22,epsilon:0.1})}
</script>
</body>
</html>
"""


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(HTML)))
        self.end_headers()
        self.wfile.write(HTML)

    def log_message(self, fmt, *args):
        return


if __name__ == "__main__":
    print(f"claudio-dashboard listening on http://{HOST}:{PORT}")
    HTTPServer((HOST, PORT), Handler).serve_forever()

