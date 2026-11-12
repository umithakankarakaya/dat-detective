/* Cloudflare Pages Function: /api/presence
 * Provides real concurrent active-visitor session tracking on Cloudflare Edge.
 * Uses env.PRESENCE_KV if configured, with zero-config Edge Cache fallback.
 */
const SESSION_TTL_MS = 15000;
const SYNTHETIC_CACHE_URL = 'https://dat-presence.internal/sessions';
let isolateSessions = new Map();

function pruneMap(mapObj, now) {
    const clean = {};
    for (const [sid, ts] of Object.entries(mapObj || {})) {
        if (typeof ts === 'number' && (now - ts) < SESSION_TTL_MS) {
            clean[sid] = ts;
        }
    }
    return clean;
}

async function readSessions(context, now) {
    // 1. Optional KV Namespace binding for strict cross-POP accuracy
    if (context.env && context.env.PRESENCE_KV) {
        try {
            const raw = await context.env.PRESENCE_KV.get('active_sessions', 'json');
            return { sessions: pruneMap(raw, now), source: 'cloudflare-kv' };
        } catch (_) {}
    }

    // 2. Zero-config Cloudflare Cache API + Isolate memory fallback
    let cachedMap = {};
    try {
        const cache = caches.default;
        const cached = await cache.match(SYNTHETIC_CACHE_URL);
        if (cached) {
            cachedMap = await cached.json();
        }
    } catch (_) {}

    const merged = pruneMap(cachedMap, now);
    for (const [sid, ts] of isolateSessions.entries()) {
        if ((now - ts) < SESSION_TTL_MS) {
            merged[sid] = Math.max(merged[sid] || 0, ts);
        } else {
            isolateSessions.delete(sid);
        }
    }
    return { sessions: merged, source: 'cloudflare-edge' };
}

async function writeSessions(context, sessions) {
    if (context.env && context.env.PRESENCE_KV) {
        try {
            await context.env.PRESENCE_KV.put('active_sessions', JSON.stringify(sessions), {
                expirationTtl: 60
            });
            return;
        } catch (_) {}
    }

    try {
        const cache = caches.default;
        const res = new Response(JSON.stringify(sessions), {
            headers: {
                'Content-Type': 'application/json',
                'Cache-Control': 'public, max-age=20'
            }
        });
        context.waitUntil(cache.put(SYNTHETIC_CACHE_URL, res));
    } catch (_) {}
}

function jsonResponse(payload, status = 200) {
    return new Response(JSON.stringify(payload), {
        status,
        headers: {
            'Content-Type': 'application/json; charset=utf-8',
            'Cache-Control': 'no-store, no-cache, must-revalidate, max-age=0',
            'X-Content-Type-Options': 'nosniff'
        }
    });
}

export async function onRequest(context) {
    const req = context.request;
    const now = Date.now();
    let sid = '';

    if (req.method === 'POST') {
        try {
            const body = await req.json();
            sid = String(body && body.sessionId ? body.sessionId : '').trim();
        } catch (_) {}
    } else if (req.method === 'GET') {
        const url = new URL(req.url);
        sid = (url.searchParams.get('sid') || '').trim();
    } else if (req.method === 'OPTIONS') {
        return new Response(null, { status: 204 });
    } else {
        return jsonResponse({ error: 'Method not allowed' }, 405);
    }

    const { sessions, source } = await readSessions(context, now);
    if (sid && sid.length <= 96) {
        sessions[sid] = now;
        isolateSessions.set(sid, now);
    }

    await writeSessions(context, sessions);
    const count = Math.max(1, Object.keys(sessions).length);

    return jsonResponse({
        online: count,
        mode: 'server',
        provider: source,
        ttlSeconds: SESSION_TTL_MS / 1000
    });
}
