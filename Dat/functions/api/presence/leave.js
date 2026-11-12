/* Cloudflare Pages Function: /api/presence/leave
 * Immediately removes a closing browser tab/session from the active count.
 */
const SYNTHETIC_CACHE_URL = 'https://dat-presence.internal/sessions-v3';
const SESSION_TTL_MS = 15000;

export async function onRequestPost(context) {
    let sid = '';
    try {
        const body = await context.request.json();
        sid = String(body && (body.visitorId || body.sessionId) ? (body.visitorId || body.sessionId) : '').trim();
    } catch (_) {}

    const now = Date.now();
    if (sid) {
        if (context.env && context.env.PRESENCE_KV) {
            try {
                const raw = (await context.env.PRESENCE_KV.get('active_sessions_v3', 'json')) || {};
                delete raw[sid];
                const clean = {};
                for (const [k, ts] of Object.entries(raw)) {
                    if (typeof ts === 'number' && (now - ts) < SESSION_TTL_MS) clean[k] = ts;
                }
                await context.env.PRESENCE_KV.put('active_sessions_v3', JSON.stringify(clean), { expirationTtl: 60 });
            } catch (_) {}
        } else {
            try {
                const cache = caches.default;
                const cached = await cache.match(SYNTHETIC_CACHE_URL);
                if (cached) {
                    const data = (await cached.json()) || {};
                    delete data[sid];
                    const clean = {};
                    for (const [k, ts] of Object.entries(data)) {
                        if (typeof ts === 'number' && (now - ts) < SESSION_TTL_MS) clean[k] = ts;
                    }
                    context.waitUntil(
                        cache.put(
                            SYNTHETIC_CACHE_URL,
                            new Response(JSON.stringify(clean), {
                                headers: { 'Content-Type': 'application/json', 'Cache-Control': 'public, max-age=20' }
                            })
                        )
                    );
                }
            } catch (_) {}
        }
    }

    return new Response(JSON.stringify({ ok: true }), {
        status: 200,
        headers: {
            'Content-Type': 'application/json; charset=utf-8',
            'Cache-Control': 'no-store'
        }
    });
}
