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
        recentEvents: []
    };
}

let isolateStore = null;

async function readStore(context) {
    if (context.env && context.env.ANALYTICS_KV) {
        try {
            const raw = await context.env.ANALYTICS_KV.get(KV_KEY, 'json');
            if (raw && raw.stats) return { store: raw, backend: 'kv' };
        } catch (_) {}
    }
    try {
        const res = await caches.default.match(SYNTHETIC_CACHE_URL);
        if (res) {
            const data = await res.json();
            if (data && data.stats) return { store: data, backend: 'edge-cache' };
        }
    } catch (_) {}
    if (!isolateStore) isolateStore = emptyStore();
    return { store: isolateStore, backend: context.env && context.env.ANALYTICS_KV ? 'kv' : 'edge-cache' };
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
        if (type === 'update_lead_status' || type === 'admin_lead') {
            if (!isAdmin(context)) return jsonResponse({ error: 'unauthorized' }, 401);
        }

        const city = clip(req.headers.get('cf-ipcity') || 'Bilinmiyor', 60);
        const country = clip(req.headers.get('cf-ipcountry') || '??', 4);
        const ua = req.headers.get('user-agent') || '';
        const device = /tablet|ipad/i.test(ua) ? 'Tablet' : /mobile|iphone|android/i.test(ua) ? 'Mobil' : 'Masaüstü';
        const page = clip(body.path || body.page || '/', 160);
        const timeStr = new Date().toLocaleTimeString('tr-TR', { timeZone: 'Europe/Istanbul', hour: '2-digit', minute: '2-digit', second: '2-digit' });

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
        } else if (type === 'lead_captured' || type === 'form_submit' || type === 'admin_lead') {
            const l = body.lead || {};
            if (!l.name && !l.contact) return jsonResponse({ error: 'empty lead' }, 400);
            store.stats.leadsCount++;
            store.leads.unshift({
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
            });
            if (store.leads.length > 300) store.leads.length = 300;
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
        return jsonResponse({ status: 'ok' });
    }

    if (req.method === 'GET') {
        if (!isAdmin(context)) return jsonResponse({ error: 'unauthorized' }, 401);

        const url = new URL(req.url);
        if (url.searchParams.get('reset') === 'true') {
            await writeStore(context, emptyStore());
            return jsonResponse({ status: 'reset_ok' });
        }

        return jsonResponse({
            status: 'ok',
            backend,
            durable: backend === 'kv',
            pinIsDefault: !(context.env && context.env.ADMIN_PIN),
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
