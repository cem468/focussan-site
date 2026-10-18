"""Local preview that behaves like the host: /x serves x.html, unknown paths get 404.html,
and /galeri style redirects from _redirects are applied.  usage: python _araclar/serve.py [port]"""
import http.server
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REDIRECTS = {}
for line in open(os.path.join(ROOT, '_redirects'), encoding='utf-8'):
    parts = line.split()
    if len(parts) >= 2:
        REDIRECTS[parts[0]] = parts[1]


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=ROOT, **k)

    def do_GET(self):
        path = self.path.split('?')[0].split('#')[0]
        if path in REDIRECTS:
            self.send_response(301)
            self.send_header('Location', REDIRECTS[path])
            self.end_headers()
            return
        if path != '/' and path.endswith('/'):
            self.send_response(308)
            self.send_header('Location', path.rstrip('/'))
            self.end_headers()
            return
        local = os.path.join(ROOT, path.lstrip('/'))
        if path != '/' and not os.path.splitext(path)[1] and os.path.isfile(local + '.html'):
            self.path = path + '.html'
        elif path != '/' and not os.path.exists(local):
            body = open(os.path.join(ROOT, '404.html'), 'rb').read()
            self.send_response(404)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        super().do_GET()


port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
http.server.ThreadingHTTPServer(('', port), Handler).serve_forever()
