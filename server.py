#!/usr/bin/env python3
"""
DAT Özel Dedektiflik Bürosu — Yerel Geliştirme & Gerçek Zamanlı Ziyaretçi Sunucusu
Statik dosyaları (index.html, 404.html, lang, assets) sunar ve
/api/presence üzerinden kafadan uydurma olmayan gerçek eşzamanlı oturum sayımını yapar.
"""

from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs, unquote
from urllib.request import Request as UrlRequest, urlopen
from datetime import datetime
import json
import os
import re
import threading
import time

PORT = int(os.environ.get("PORT", "3000"))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SESSION_TTL_SECONDS = 15.0
ADMIN_PIN = os.environ.get("ADMIN_PIN", "2005")

_sessions_lock = threading.Lock()
_active_sessions = {}

_analytics_lock = threading.Lock()
_analytics_store = {
    "trackingSince": datetime.utcnow().isoformat() + "Z",
    "stats": {"pageViews": 0, "uniqueVisitors": 0, "whatsappClicks": 0, "phoneClicks": 0, "leadsCount": 0},
    "serviceViews": {},
    "pages": {},
    "cities": {},
    "sources": {},
    "devices": {},
    "hourly": {"date": "", "buckets": [{"v": 0, "c": 0} for _ in range(24)]},
    "leads": [],
    "recentEvents": [],
    "webhookUrl": os.environ.get("GOOGLE_APPS_SCRIPT_WEBHOOK_URL", "").strip(),
    "lastEmailStatus": None,
}
_GAS_URL_RE = re.compile(r"^https://script\.google\.com/macros/s/[A-Za-z0-9_-]+/exec$", re.I)


def _forward_gas_webhook(webhook_url: str, payload: dict) -> dict:
    clean_url = (webhook_url or "").strip()
    if not clean_url:
        return {"ok": False, "provider": "Google Apps Script", "error": "Webhook URL tanımlı değil."}
    try:
        req = UrlRequest(
            clean_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "text/plain;charset=utf-8"},
            method="POST",
        )
        with urlopen(req, timeout=8.5) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            try:
                parsed = json.loads(raw)
            except Exception:
                return {"ok": False, "provider": "Google Apps Script", "httpStatus": resp.status, "error": "Apps Script erişim izni 'Herkes (Anyone)' olmalı veya beklenmeyen yanıt döndü."}
            if not parsed.get("ok"):
                return {"ok": False, "provider": "Google Apps Script", "httpStatus": resp.status, "error": parsed.get("error") or f"HTTP {resp.status}"}
            return {"ok": True, "provider": "Google Apps Script (Gmail)", "httpStatus": resp.status, "recipients": parsed.get("recipients", 2), "message": parsed.get("message", "E-posta iletildi.")}
    except Exception as exc:
        return {"ok": False, "provider": "Google Apps Script (Gmail)", "error": str(exc)}


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

        if parsed.path == "/api/analytics":
            if self.headers.get("X-Admin-Pin", "") != ADMIN_PIN:
                self._send_json(401, {"error": "unauthorized"})
                return
            qs = parse_qs(parsed.query)
            if (qs.get("reset") or [""])[0] == "true":
                with _analytics_lock:
                    _analytics_store["stats"] = {"pageViews": 0, "uniqueVisitors": 0, "whatsappClicks": 0, "phoneClicks": 0, "leadsCount": 0}
                    _analytics_store["serviceViews"] = {}
                    _analytics_store["pages"] = {}
                    _analytics_store["cities"] = {}
                    _analytics_store["sources"] = {}
                    _analytics_store["devices"] = {}
                    _analytics_store["leads"] = []
                    _analytics_store["recentEvents"] = []
                self._send_json(200, {"status": "reset_ok"})
                return
            with _analytics_lock:
                snap = dict(_analytics_store)
            self._send_json(200, {
                "status": "ok",
                "backend": "local-dev",
                "durable": False,
                "pinIsDefault": ADMIN_PIN == "2005",
                "webhookConfigured": bool(snap.get("webhookUrl")),
                "webhookSource": "local" if snap.get("webhookUrl") else "none",
                "webhookUrl": snap.get("webhookUrl", ""),
                "lastEmailStatus": snap.get("lastEmailStatus"),
                "trackingSince": snap["trackingSince"],
                "stats": snap["stats"],
                "serviceViews": snap["serviceViews"],
                "pages": snap["pages"],
                "cities": snap["cities"],
                "sources": snap["sources"],
                "devices": snap["devices"],
                "hourly": snap["hourly"],
                "leads": snap["leads"],
                "recentEvents": snap["recentEvents"][:50],
                "serverTime": datetime.utcnow().isoformat() + "Z",
            })
            return

        # Cloudflare Pages gibi uzantısız temiz URL desteği (/hizmetler/es-takibi -> es-takibi.html)
        rel_path = unquote(parsed.path).lstrip("/")
        if rel_path and not os.path.exists(os.path.join(BASE_DIR, rel_path)) \
                and os.path.isfile(os.path.join(BASE_DIR, rel_path.rstrip("/") + ".html")):
            self.path = "/" + rel_path.rstrip("/") + ".html" + (("?" + parsed.query) if parsed.query else "")
            rel_path = rel_path.rstrip("/") + ".html"

        # Dosya bulunamazsa kurumsal 404.html göster
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

        if parsed.path == "/api/analytics":
            data = self._read_json_body()
            ev_type = str(data.get("type", "page_view"))[:40]
            admin_only = ev_type in ("update_lead_status", "admin_lead", "save_email_webhook", "test_email_webhook")
            if admin_only and self.headers.get("X-Admin-Pin", "") != ADMIN_PIN:
                self._send_json(401, {"error": "unauthorized"})
                return

            if ev_type == "save_email_webhook":
                url_val = str(data.get("webhookUrl", "")).strip()
                if url_val and not _GAS_URL_RE.match(url_val):
                    self._send_json(400, {"error": "Geçersiz URL. https://script.google.com/macros/s/.../exec formatında olmalıdır."})
                    return
                with _analytics_lock:
                    _analytics_store["webhookUrl"] = url_val
                self._send_json(200, {"status": "ok", "webhookConfigured": bool(url_val), "webhookUrl": url_val})
                return

            if ev_type == "test_email_webhook":
                url_val = str(data.get("webhookUrl", "")).strip()
                with _analytics_lock:
                    if url_val:
                        if not _GAS_URL_RE.match(url_val):
                            self._send_json(400, {"error": "Geçersiz URL. https://script.google.com/macros/s/.../exec formatında olmalıdır."})
                            return
                        _analytics_store["webhookUrl"] = url_val
                    target_url = url_val or _analytics_store.get("webhookUrl", "")
                if not target_url:
                    self._send_json(400, {"error": "Önce Google Apps Script /exec adresini yapıştırın."})
                    return
                res = _forward_gas_webhook(target_url, {
                    "_subject": "DAT Dedektiflik — Yerel Sunucu Canlı Gmail Testi",
                    "name": "Sistem Doğrulama Testi",
                    "channel": "Yönetim Paneli -> Google Apps Script",
                    "contact": "uhakankarakaya@gmail.com / umithakankarakaya@gmail.com",
                    "category": "E-Posta Teslimat Kontrolü",
                    "urgency": "NORMAL",
                    "message": "Yerel sunucu üzerinden Google Apps Script Gmail testi.",
                })
                with _analytics_lock:
                    _analytics_store["lastEmailStatus"] = {
                        "at": datetime.utcnow().isoformat() + "Z",
                        "code": "PANEL-TEST",
                        "ok": bool(res.get("ok")),
                        "provider": res.get("provider"),
                        "error": res.get("error"),
                    }
                self._send_json(200, {"status": "ok", "testResult": res, "webhookConfigured": bool(target_url)})
                return

            email_res = None
            page = str(data.get("path") or data.get("page") or "/")[:160]
            ua = self.headers.get("User-Agent", "")
            dev = "Tablet" if re.search(r"tablet|ipad", ua, re.I) else ("Mobil" if re.search(r"mobile|iphone|android", ua, re.I) else "Masaüstü")
            now_hour = datetime.now().hour
            time_str = datetime.now().strftime("%H:%M:%S")
            with _analytics_lock:
                if ev_type == "page_view":
                    _analytics_store["stats"]["pageViews"] += 1
                    _analytics_store["pages"][page] = _analytics_store["pages"].get(page, 0) + 1
                    _analytics_store["hourly"]["buckets"][now_hour]["v"] += 1
                    if data.get("isNewVisitor"):
                        _analytics_store["stats"]["uniqueVisitors"] += 1
                        _analytics_store["devices"][dev] = _analytics_store["devices"].get(dev, 0) + 1
                elif ev_type == "whatsapp_click":
                    _analytics_store["stats"]["whatsappClicks"] += 1
                    _analytics_store["hourly"]["buckets"][now_hour]["c"] += 1
                elif ev_type == "phone_click":
                    _analytics_store["stats"]["phoneClicks"] += 1
                    _analytics_store["hourly"]["buckets"][now_hour]["c"] += 1
                elif ev_type in ("lead_captured", "admin_lead"):
                    l = data.get("lead") or {}
                    saved = {
                        "id": str(l.get("id") or f"lead_{int(time.time()*1000)}"),
                        "code": str(l.get("code") or "#DAT-LOCAL"),
                        "name": str(l.get("name") or "İsimsiz")[:80],
                        "contact": str(l.get("contact") or l.get("phone") or "")[:60],
                        "category": str(l.get("category") or "Belirtilmedi")[:80],
                        "channel": str(l.get("channel") or "Web Form")[:40],
                        "urgency": l.get("urgency") if l.get("urgency") in ("normal", "high", "critical") else "normal",
                        "status": "new",
                        "isTest": bool(l.get("isTest")),
                        "dateStr": datetime.now().strftime("%d.%m.%Y %H:%M"),
                        "details": str(l.get("details") or "")[:2000],
                        "city": "Localhost",
                    }
                    _analytics_store["stats"]["leadsCount"] += 1
                    _analytics_store["leads"].insert(0, saved)
                    hook_url = _analytics_store.get("webhookUrl", "") if (ev_type == "lead_captured" and not saved["isTest"]) else ""
                elif ev_type == "update_lead_status":
                    hook_url = ""
                    for item in _analytics_store["leads"]:
                        if item["id"] == data.get("leadId"):
                            item["status"] = data.get("newStatus")
                else:
                    hook_url = ""
                if ev_type not in ("lead_captured", "admin_lead"):
                    hook_url = ""
                if ev_type != "update_lead_status":
                    _analytics_store["recentEvents"].insert(0, {
                        "id": f"ev_{int(time.time()*1000)}",
                        "type": ev_type,
                        "time": time_str,
                        "page": page,
                        "label": str(data.get("label") or data.get("service") or ev_type)[:90],
                        "device": dev,
                        "city": "Localhost",
                        "country": "TR",
                    })
                    del _analytics_store["recentEvents"][100:]
            if hook_url:
                email_res = _forward_gas_webhook(hook_url, {"_subject": f"Yeni Vaka Talebi ({saved['code']})", "Dosya_Takip_Kodu": saved["code"], "Ad_veya_Rumuz": saved["name"], "Hizmet_Kategorisi": saved["category"], "Musteri_Iletisim": saved["contact"], "Vaka_Detayi": saved["details"]})
                with _analytics_lock:
                    _analytics_store["lastEmailStatus"] = {"at": datetime.utcnow().isoformat() + "Z", "code": saved["code"], "ok": bool(email_res.get("ok")), "provider": email_res.get("provider"), "error": email_res.get("error")}
            self._send_json(200, {
                "status": "ok",
                "emailForwarded": bool(email_res and email_res.get("ok")),
                "emailProvider": email_res.get("provider") if email_res else None,
                "emailError": email_res.get("error") if email_res and not email_res.get("ok") else None,
            })
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
