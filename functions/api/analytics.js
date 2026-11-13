/* Cloudflare Pages Function: /api/analytics
 *
 * - Public visitors may only POST anonymous interaction events (page_view, whatsapp_click, ...).
 * - Reading data, changing lead status and resetting REQUIRE the admin PIN
 *   (header "X-Admin-Pin"). Set a strong ADMIN_PIN in Cloudflare Pages ->
 *   Settings -> Environment variables. Lead records contain personal data (KVKK).
 * - No invented numbers: every breakdown below starts at 0 and only grows from
 *   events actually sent by visitors' browsers. The Cloudflare totals are a
 *   fixed snapshot the owner read from the Cloudflare dashboard (12.11.2026).
 * - Storage: ANALYTICS_KV binding if configured (recommended, global & durable),
 *   otherwise the per-datacenter Edge Cache (best effort, can be evicted).
 */
const STORE_VERSION = 'v4';
const SYNTHETIC_CACHE_URL = 'https://dat-analytics.internal/store-' + STORE_VERSION;
const KV_KEY = 'dat_analytics_store_' + STORE_VERSION;
const DEFAULT_PIN = '2005';

const CLOUDFLARE_SNAPSHOT = {
    label: 'Cloudflare HTTP Traffic, son 24 saat (12.11.2026 22:17 itibarıyla, elle girildi)',
    requests: 15850,
    pageViews: 1420,
    visits: 1100,
    bandwidthMB: 223.56,
    apiRequests: 2180
};

const SERVICE_PATHS = [
    ['es-takibi', 'Eş Takibi'],
    ['evlilik-oncesi', 'Evlilik Öncesi Araştırma'],
    ['velayet', 'Velayet & Boşanma'],
    ['ogrenci-takibi', 'Öğrenci Takibi'],
    ['adres', 'Adres & Borçlu Tespiti'],
    ['bilisim', 'Bilişim Dolandırıcılığı'],
    ['firma', 'Firma Araştırması'],
    ['hirsizlik', 'Hırsızlık Araştırması'],
    ['bocek', 'Böcek Tarama (TSCM)'],
    ['marka', 'Marka Taklidi Araştırması']
];

function emptyStore() {
    return {
        version: STORE_VERSION,
        trackingSince: new Date().toISOString(),
        stats: { pageViews: 0, uniqueVisitors: 0, whatsappClicks: 0, phoneClicks: 0, leadsCount: 0 },
        serviceViews: {},
        pages: {},
        cities: {},
        sources: {},
        devices: {},
        hourly: { date: '', buckets: Array.from({ length: 24 }, () => ({ v: 0, c: 0 })) },
        leads: [],
        recentEvents: [],
        webhookUrl: '',
        lastEmailStatus: null
    };
}

const GAS_URL_REGEX = /^https:\/\/script\.google\.com\/macros\/s\/[A-Za-z0-9_-]+\/exec$/i;
const FORMSUBMIT_RECIPIENTS = [
    'umithakankarakaya@gmail.com',
    'uhakankarakaya@gmail.com'
];

async function relayViaFormSubmitServer(payload, targetList = FORMSUBMIT_RECIPIENTS) {
    const cleanPayload = (payload && typeof payload === 'object') ? { ...payload } : {};
    if (!cleanPayload.email) cleanPayload.email = 'info@datdedektiflik.com';
    const body = JSON.stringify(cleanPayload);
    const deliveredTo = [];
    const errors = [];

    await Promise.all(targetList.map(async (recipient) => {
        if (!FORMSUBMIT_RECIPIENTS.includes(recipient)) return;
        const controller = new AbortController();
        const timer = setTimeout(() => controller.abort(), 12000);
        try {
            const res = await fetch(`https://formsubmit.co/ajax/${recipient}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    'Origin': 'https://www.datdedektiflik.com',
                    'Referer': 'https://www.datdedektiflik.com/'
                },
                body,
                signal: controller.signal
            });
            const data = await res.json().catch(() => null);
            const rejected = data && (data.success === false || data.success === 'false');
            if (!res.ok || rejected) {
                const rawMsg = (data && data.message) || `HTTP ${res.status}`;
                if (/needs activation/i.test(rawMsg)) {
                    errors.push(`${recipient} için FormSubmit aktivasyon linkine (Activate Form) tıklanmamış`);
                } else {
                    errors.push(`${recipient}: ${rawMsg}`);
                }
            } else {
                deliveredTo.push(recipient);
            }
        } catch (err) {
            errors.push(`${recipient}: ${err && err.message ? err.message : 'Sunucu ağ hatası'}`);
        } finally {
            clearTimeout(timer);
        }
    }));

    return { ok: deliveredTo.length > 0, deliveredTo, errors };
}

function normalizeStore(raw) {
    const base = emptyStore();
    if (!raw || typeof raw !== 'object') return base;
    if (typeof raw.webhookUrl !== 'string') raw.webhookUrl = '';
    if (!('lastEmailStatus' in raw)) raw.lastEmailStatus = null;
    if (!raw.leads) raw.leads = [];
    if (!raw.recentEvents) raw.recentEvents = [];
    return raw;
}

async function forwardToGasWebhook(gasUrl, emailPayload) {
    const cleanUrl = String(gasUrl || '').trim();
    if (!cleanUrl) return { ok: false, provider: 'gas', error: 'Webhook URL tanımlı değil.' };
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), 8500);
    try {
        const res = await fetch(cleanUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'text/plain;charset=utf-8' },
            body: JSON.stringify(emailPayload),
            redirect: 'follow',
            signal: controller.signal
        });
        const rawText = await res.text().catch(() => '');
        let parsed = null;
        try { parsed = JSON.parse(rawText); } catch (_) {}
        if (!parsed) {
            const authWall = /accounts\.google\.com|ServiceLogin/i.test(rawText) || /<html/i.test(rawText);
            return {
                ok: false,
                provider: 'Google Apps Script (Gmail)',
                httpStatus: res.status,
                error: authWall
                    ? 'Apps Script "Erişimi olanlar: Herkes (Anyone)" olarak dağıtılmamış veya Google oturumu istiyor.'
                    : `Apps Script beklenmeyen yanıt döndürdü (HTTP ${res.status}).`
            };
        }
        if (!res.ok || parsed.ok !== true) {
            return {
                ok: false,
                provider: 'Google Apps Script (Gmail)',
                httpStatus: res.status,
                error: parsed.error || `HTTP ${res.status}`
            };
        }
        return {
            ok: true,
            provider: 'Google Apps Script (Gmail)',
            httpStatus: res.status,
            recipients: parsed.recipients || 2,
            message: parsed.message || 'E-posta Gmail üzerinden iletildi.'
        };
    } catch (err) {
        return {
            ok: false,
            provider: 'Google Apps Script (Gmail)',
            error: err && err.name === 'AbortError' ? 'Zaman aşımı (8.5 sn)' : (err && err.message ? err.message : 'Bağlantı hatası')
        };
    } finally {
        clearTimeout(timer);
    }
}

let isolateStore = null;

async function readStore(context) {
    if (context.env && context.env.ANALYTICS_KV) {
        try {
            const raw = await context.env.ANALYTICS_KV.get(KV_KEY, 'json');
            if (raw && raw.stats) return { store: normalizeStore(raw), backend: 'kv' };
        } catch (_) {}
    }
    try {
        const res = await caches.default.match(SYNTHETIC_CACHE_URL);
        if (res) {
            const data = await res.json();
            if (data && data.stats) return { store: normalizeStore(data), backend: 'edge-cache' };
        }
    } catch (_) {}
    if (!isolateStore) isolateStore = emptyStore();
    return { store: normalizeStore(isolateStore), backend: context.env && context.env.ANALYTICS_KV ? 'kv' : 'edge-cache' };
}

async function writeStore(context, store) {
    isolateStore = store;
    if (context.env && context.env.ANALYTICS_KV) {
        try {
            await context.env.ANALYTICS_KV.put(KV_KEY, JSON.stringify(store));
            return;
        } catch (_) {}
    }
    try {
        const res = new Response(JSON.stringify(store), {
            headers: { 'Content-Type': 'application/json', 'Cache-Control': 'public, max-age=2592000' }
        });
        context.waitUntil(caches.default.put(SYNTHETIC_CACHE_URL, res));
    } catch (_) {}
}

function jsonResponse(payload, status = 200) {
    return new Response(JSON.stringify(payload), {
        status,
        headers: {
            'Content-Type': 'application/json; charset=utf-8',
            'Cache-Control': 'no-store, no-cache, must-revalidate, max-age=0',
            'X-Content-Type-Options': 'nosniff',
            'X-Robots-Tag': 'noindex'
        }
    });
}

function isAdmin(context) {
    const expected = String((context.env && context.env.ADMIN_PIN) || DEFAULT_PIN);
    const given = context.request.headers.get('x-admin-pin') || '';
    if (given.length !== expected.length) return false;
    let diff = 0;
    for (let i = 0; i < expected.length; i++) diff |= expected.charCodeAt(i) ^ given.charCodeAt(i);
    return diff === 0;
}

function inc(obj, key, by = 1) {
    if (!key) return;
    obj[key] = (obj[key] || 0) + by;
}

function clip(v, n) {
    return String(v == null ? '' : v).slice(0, n);
}

function trHourAndDate() {
    const parts = new Intl.DateTimeFormat('en-CA', {
        timeZone: 'Europe/Istanbul', year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', hour12: false
    }).formatToParts(new Date());
    const get = (t) => parts.find((p) => p.type === t)?.value;
    return { date: `${get('year')}-${get('month')}-${get('day')}`, hour: Number(get('hour')) % 24 };
}

function bumpHourly(store, kind) {
    const { date, hour } = trHourAndDate();
    if (!store.hourly || store.hourly.date !== date) {
        store.hourly = { date, buckets: Array.from({ length: 24 }, () => ({ v: 0, c: 0 })) };
    }
    store.hourly.buckets[hour][kind] += 1;
}

export async function onRequest(context) {
    const req = context.request;

    if (req.method === 'OPTIONS') {
        return new Response(null, {
            status: 204,
            headers: {
                'Access-Control-Allow-Origin': 'https://www.datdedektiflik.com',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, X-Admin-Pin'
            }
        });
    }

    const { store, backend } = await readStore(context);

    if (req.method === 'POST') {
        let body;
        try {
            body = JSON.parse(await req.text());
        } catch (_) {
            return jsonResponse({ error: 'bad json' }, 400);
        }
        const type = clip(body.type || 'page_view', 40);

        // Admin-only mutations
        if (['update_lead_status', 'admin_lead', 'save_email_webhook', 'test_email_webhook', 'resend_formsubmit_activation'].includes(type)) {
            if (!isAdmin(context)) return jsonResponse({ error: 'unauthorized' }, 401);
        }

        const envGasUrl = (context.env && context.env.GOOGLE_APPS_SCRIPT_WEBHOOK_URL)
            ? String(context.env.GOOGLE_APPS_SCRIPT_WEBHOOK_URL).trim()
            : '';

        if (type === 'save_email_webhook') {
            const nextUrl = String(body.webhookUrl || '').trim();
            if (nextUrl && !GAS_URL_REGEX.test(nextUrl)) {
                return jsonResponse({ error: 'Geçersiz URL. Adres https://script.google.com/macros/s/.../exec formatında olmalıdır.' }, 400);
            }
            store.webhookUrl = nextUrl;
            await writeStore(context, store);
            const activeUrl = envGasUrl || store.webhookUrl;
            return jsonResponse({
                status: 'ok',
                webhookConfigured: !!activeUrl,
                webhookSource: envGasUrl ? 'env' : (store.webhookUrl ? 'kv' : 'none'),
                webhookUrl: store.webhookUrl
            });
        }

        if (type === 'test_email_webhook') {
            const submittedUrl = String(body.webhookUrl || '').trim();
            if (submittedUrl) {
                if (!GAS_URL_REGEX.test(submittedUrl)) {
                    return jsonResponse({ error: 'Geçersiz URL. Adres https://script.google.com/macros/s/.../exec formatında olmalıdır.' }, 400);
                }
                store.webhookUrl = submittedUrl;
            }
            const activeUrl = submittedUrl || envGasUrl || store.webhookUrl;
            if (!activeUrl) {
                return jsonResponse({ error: 'Önce Google Apps Script /exec adresini yapıştırın.' }, 400);
            }
            const testResult = await forwardToGasWebhook(activeUrl, {
                _subject: 'DAT Dedektiflik — Yönetim Paneli Canlı Gmail Testi',
                name: 'Sistem Doğrulama Testi',
                channel: 'Yönetim Paneli -> Google Apps Script',
                contact: 'uhakankarakaya@gmail.com / umithakankarakaya@gmail.com',
                category: 'E-Posta Teslimat Kontrolü',
                urgency: 'NORMAL',
                message: `Bu e-posta ${new Date().toLocaleString('tr-TR', { timeZone: 'Europe/Istanbul' })} tarihinde Yönetim Paneli test butonundan gönderildi.`
            });
            store.lastEmailStatus = {
                at: new Date().toISOString(),
                code: 'PANEL-TEST',
                ok: !!testResult.ok,
                provider: testResult.provider || 'Google Apps Script',
                error: testResult.error || null
            };
            await writeStore(context, store);
            return jsonResponse({
                status: 'ok',
                testResult,
                webhookConfigured: !!(envGasUrl || store.webhookUrl),
                webhookSource: envGasUrl ? 'env' : (store.webhookUrl ? 'kv' : 'none'),
                lastEmailStatus: store.lastEmailStatus
            });
        }

        if (type === 'resend_formsubmit_activation') {
            const requestedTarget = String(body.recipient || '').trim();
            const targetList = FORMSUBMIT_RECIPIENTS.includes(requestedTarget)
                ? [requestedTarget]
                : FORMSUBMIT_RECIPIENTS;
            const relay = await relayViaFormSubmitServer({
                _subject: 'DAT Dedektiflik — Alıcı Aktivasyon & Doğrulama Testi',
                name: 'DAT Yönetim Paneli Kontrolü',
                email: 'info@datdedektiflik.com',
                message: `Bu istek ${new Date().toLocaleString('tr-TR', { timeZone: 'Europe/Istanbul' })} tarihinde Yönetim Paneli üzerinden aktivasyon/teslimat doğrulaması için tetiklendi.`
            }, targetList);
            return jsonResponse({ status: 'ok', ...relay });
        }

        const city = clip(req.headers.get('cf-ipcity') || 'Bilinmiyor', 60);
        const country = clip(req.headers.get('cf-ipcountry') || '??', 4);
        const ua = req.headers.get('user-agent') || '';
        const device = /tablet|ipad/i.test(ua) ? 'Tablet' : /mobile|iphone|android/i.test(ua) ? 'Mobil' : 'Masaüstü';
        const page = clip(body.path || body.page || '/', 160);
        const timeStr = new Date().toLocaleTimeString('tr-TR', { timeZone: 'Europe/Istanbul', hour: '2-digit', minute: '2-digit', second: '2-digit' });
        let emailDeliveryResult = null;

        if (type === 'page_view') {
            store.stats.pageViews++;
            inc(store.pages, page);
            bumpHourly(store, 'v');
            if (body.isNewVisitor) {
                store.stats.uniqueVisitors++;
                inc(store.devices, device);
                inc(store.cities, country === 'TR' ? city : `${city} (${country})`);
                inc(store.sources, clip(body.source || 'Doğrudan (Direct)', 40));
            }
            const svc = SERVICE_PATHS.find(([needle]) => page.includes(needle));
            if (svc) inc(store.serviceViews, svc[1]);
        } else if (type === 'whatsapp_click') {
            store.stats.whatsappClicks++;
            bumpHourly(store, 'c');
        } else if (type === 'phone_click') {
            store.stats.phoneClicks++;
            bumpHourly(store, 'c');
        } else if (type === 'lead_captured' || type === 'admin_lead') {
            const l = body.lead || {};
            if (!l.name && !l.contact) return jsonResponse({ error: 'empty lead' }, 400);
            store.stats.leadsCount++;
            const savedLead = {
                id: clip(l.id || 'lead_' + Date.now(), 60),
                code: clip(l.code || '#DAT-' + Math.floor(10000 + Math.random() * 90000), 20),
                name: clip(l.name || 'İsimsiz', 80),
                contact: clip(l.contact || l.phone || '', 60),
                category: clip(l.category || 'Belirtilmedi', 80),
                channel: clip(l.channel || 'Web Form', 40),
                urgency: ['normal', 'high', 'critical'].includes(l.urgency) ? l.urgency : 'normal',
                status: 'new',
                isTest: !!l.isTest,
                dateStr: new Date().toLocaleString('tr-TR', { timeZone: 'Europe/Istanbul', day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' }),
                details: clip(l.details || '', 2000),
                city
            };
            store.leads.unshift(savedLead);
            if (store.leads.length > 300) store.leads.length = 300;

            const activeGasUrl = envGasUrl || store.webhookUrl || '';
            if (activeGasUrl && type === 'lead_captured' && !savedLead.isTest) {
                emailDeliveryResult = await forwardToGasWebhook(activeGasUrl, {
                    _subject: `Yeni Vaka Talebi (${savedLead.code}) — DAT Dedektiflik`,
                    Dosya_Takip_Kodu: savedLead.code,
                    Ad_veya_Rumuz: savedLead.name,
                    Hizmet_Kategorisi: savedLead.category,
                    Tercih_Edilen_Kanal: savedLead.channel,
                    Musteri_Iletisim: savedLead.contact,
                    Aciliyet_Durumu: savedLead.urgency.toUpperCase(),
                    Vaka_Detayi: savedLead.details,
                    Sehir: savedLead.city,
                    Sayfa: page
                });
                store.lastEmailStatus = {
                    at: new Date().toISOString(),
                    code: savedLead.code,
                    ok: !!emailDeliveryResult.ok,
                    provider: emailDeliveryResult.provider || 'Google Apps Script',
                    error: emailDeliveryResult.error || null
                };
            }
        } else if (type === 'lead_relay_fallback') {
            const p = body.payload || {};
            if (!p.message && !p.Ad_veya_Rumuz && !p.name) {
                return jsonResponse({ error: 'empty relay payload' }, 400);
            }
            const missing = Array.isArray(body.missingRecipients)
                ? body.missingRecipients.filter((r) => FORMSUBMIT_RECIPIENTS.includes(r))
                : [];
            const relay = await relayViaFormSubmitServer(p, missing.length ? missing : FORMSUBMIT_RECIPIENTS);
            store.lastEmailStatus = {
                at: new Date().toISOString(),
                code: clip(p.Dosya_Takip_Kodu || 'RELAY', 24),
                ok: relay.ok,
                provider: 'FormSubmit (Cloudflare Sunucu Yedek)',
                error: relay.errors.length ? relay.errors.join(' | ') : null
            };
            await writeStore(context, store);
            return jsonResponse({ status: 'ok', ...relay });
        } else if (type === 'form_submit') {
            // Telemetry ping after lead submission
        } else if (type === 'update_lead_status') {
            const target = store.leads.find((x) => x.id === body.leadId);
            if (target && ['new', 'reviewing', 'contacted', 'closed'].includes(body.newStatus)) target.status = body.newStatus;
        } else if (type !== 'service_click') {
            return jsonResponse({ status: 'ignored' });
        }

        if (type !== 'update_lead_status') {
            store.recentEvents.unshift({
                id: 'ev_' + Date.now() + '_' + Math.random().toString(36).slice(2, 6),
                type,
                time: timeStr,
                page,
                label: clip(body.label || body.service || (type === 'page_view' ? 'Sayfa ziyareti' : type), 90),
                device,
                city,
                country
            });
            if (store.recentEvents.length > 100) store.recentEvents.length = 100;
        }

        await writeStore(context, store);
        return jsonResponse({
            status: 'ok',
            emailForwarded: Boolean(emailDeliveryResult && emailDeliveryResult.ok),
            emailProvider: emailDeliveryResult ? (emailDeliveryResult.provider || 'Google Apps Script') : null,
            emailError: emailDeliveryResult && !emailDeliveryResult.ok ? emailDeliveryResult.error : null
        });
    }

    if (req.method === 'GET') {
        if (!isAdmin(context)) return jsonResponse({ error: 'unauthorized' }, 401);

        const url = new URL(req.url);
        if (url.searchParams.get('reset') === 'true') {
            await writeStore(context, emptyStore());
            return jsonResponse({ status: 'reset_ok' });
        }

        const envGasUrl = (context.env && context.env.GOOGLE_APPS_SCRIPT_WEBHOOK_URL)
            ? String(context.env.GOOGLE_APPS_SCRIPT_WEBHOOK_URL).trim()
            : '';

        return jsonResponse({
            status: 'ok',
            backend,
            durable: backend === 'kv',
            pinIsDefault: !(context.env && context.env.ADMIN_PIN),
            webhookConfigured: !!(envGasUrl || store.webhookUrl),
            webhookSource: envGasUrl ? 'env' : (store.webhookUrl ? 'kv' : 'none'),
            webhookUrl: store.webhookUrl || '',
            lastEmailStatus: store.lastEmailStatus || null,
            cloudflareSnapshot: CLOUDFLARE_SNAPSHOT,
            trackingSince: store.trackingSince,
            stats: store.stats,
            serviceViews: store.serviceViews,
            pages: store.pages,
            cities: store.cities,
            sources: store.sources,
            devices: store.devices,
            hourly: store.hourly,
            leads: store.leads,
            recentEvents: store.recentEvents.slice(0, 50),
            serverTime: new Date().toISOString()
        });
    }

    return jsonResponse({ error: 'Method not allowed' }, 405);
}
