#!/usr/bin/env python3
"""
DAT Özel Dedektiflik Bürosu — Yerel Geliştirme & Gerçek Zamanlı Ziyaretçi Sunucusu
Statik dosyaları (index.html, 404.html, lang, assets) sunar ve
/api/presence üzerinden kafadan uydurma olmayan gerçek eşzamanlı oturum sayımını yapar.
"""

from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs
import json
import os
import threading
import time

PORT = int(os.environ.get("PORT", "3000"))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SESSION_TTL_SECONDS = 15.0

_sessions_lock = threading.Lock()
_active_sessions = {}


def _prune_and_count() -> int:
    now = time.time()
    expired = [sid for sid, ts in _active_sessions.items() if (now - ts) > SESSION_TTL_SECONDS]
    for sid in expired:
        del _active_sessions[sid]
    return len(_active_sessions)


class DatRequestHandler(SimpleHTTPRequestHandler):
    extensions_map = {
        **SimpleHTTPRequestHandler.extensions_map,
        ".webmanifest": "application/manifest+json",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def end_headers(self):
        # Geliştirme sırasında tarayıcı önbellek takılmalarını kesin olarak önle
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        self.send_header("X-Content-Type-Options", "nosniff")
        if "?v=" in self.path:
            # Eski ?v=X önbellek isteklerinde Chrome disk önbelleğini otomatik temizle
            self.send_header("Clear-Site-Data", '"cache"')
        super().end_headers()

    def _read_json_body(self) -> dict:
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            length = 0
        if length <= 0 or length > 8192:
            return {}
        raw = self.rfile.read(length)
        try:
            return json.loads(raw.decode("utf-8"))
        except Exception:
            return {}

    def _send_json(self, status: int, payload: dict):
        body = json.dumps(payload).encode("utf-8")
        try:
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        except (BrokenPipeError, ConnectionResetError):
            pass

    def copyfile(self, source, outputfile):
        try:
            super().copyfile(source, outputfile)
        except (BrokenPipeError, ConnectionResetError):
            pass

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/presence":
            qs = parse_qs(parsed.query)
            sid = (qs.get("sid") or [""])[0].strip()
            with _sessions_lock:
                if sid:
                    _active_sessions[sid] = time.time()
                count = _prune_and_count()
            self._send_json(200, {"online": count, "mode": "server", "ttlSeconds": SESSION_TTL_SECONDS})
            return

        # Dosya bulunamazsa kurumsal 404.html göster
        rel_path = parsed.path.lstrip("/")
        if rel_path and not os.path.exists(os.path.join(BASE_DIR, rel_path)):
            not_found_path = os.path.join(BASE_DIR, "404.html")
            if os.path.isfile(not_found_path):
                with open(not_found_path, "rb") as f:
                    data = f.read()
                self.send_response(404)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)
                return

        super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/presence":
            data = self._read_json_body()
            sid = str(data.get("sessionId", "")).strip()
            with _sessions_lock:
                if sid:
                    _active_sessions[sid] = time.time()
                count = _prune_and_count()
            self._send_json(200, {"online": count, "mode": "server"})
            return

        if parsed.path == "/api/presence/leave":
            data = self._read_json_body()
            sid = str(data.get("sessionId", "")).strip()
            with _sessions_lock:
                if sid and sid in _active_sessions:
                    del _active_sessions[sid]
                count = _prune_and_count()
            self._send_json(200, {"online": count, "mode": "server"})
            return

        self._send_json(404, {"error": "Not found"})

    def log_message(self, format, *args):
        # /api/presence kalp atışlarını log kirliliği yapmaması için sessize al
        if args and "/api/presence" in str(args[0]):
            return
        super().log_message(format, *args)


if __name__ == "__main__":
    server = ThreadingHTTPServer(("0.0.0.0", PORT), DatRequestHandler)
    print(f"DAT Özel Dedektiflik sunucusu http://localhost:{PORT} adresinde çalışıyor (Gerçek Zamanlı Ziyaretçi API aktif)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
