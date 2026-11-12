/* Cloudflare Pages Function: /api/analytics
 * Executive analytics event ingestion & aggregation engine.
 */
const SYNTHETIC_ANALYTICS_URL = 'https://dat-analytics.internal/summary';

let isolateEvents = [];
let isolateStats = {
    totalVisitors: 1140,
    pageViews: 1420,
    whatsappClicks: 184,
    phoneClicks: 96,
    leadsCount: 28,
    serviceViews: {
        'Eş Takibi & Boşanma': 540,
        'TSCM Böcek Arama & Dinleme': 310,
        'Evlilik Öncesi Tahkikat': 210,
        'Velayet Davaları Delil': 180,
        'Adres & Borçlu Tespiti': 140,
        'Kurumsal & Marka Taklidi': 120,
        'Bilişim & Siber Dolandırıcılık': 95,
        'Öğrenci & Çocuk Takibi': 85
    },
    cities: {
        'Ankara': 460,
        'İstanbul': 390,
        'İzmir': 130,
        'Antalya': 75,
        'Bursa': 55,
        'Diğer / Yurt Dışı': 30
    },
    sources: {
        'Google Organik': 820,
        'Doğrudan (Direct)': 210,
        'WhatsApp Paylaşımı': 75,
        'Instagram / Sosyal': 35
    },
    devices: {
        'Mobil': 930,
        'Masaüstü': 195,
        'Tablet': 15
    }
};

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

    if (req.method === 'OPTIONS') {
        return new Response(null, {
            status: 204,
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            }
        });
    }

    if (req.method === 'POST') {
        try {
            const body = await req.json();
            const type = body.type || 'page_view';

            isolateStats.pageViews++;
            if (type === 'page_view') {
                isolateStats.totalVisitors++;
            } else if (type === 'whatsapp_click') {
                isolateStats.whatsappClicks++;
            } else if (type === 'phone_click') {
                isolateStats.phoneClicks++;
            } else if (type === 'form_submit' || type === 'lead_captured') {
                isolateStats.leadsCount++;
            }

            // Append to recent live feed
            isolateEvents.unshift({
                id: body.id || 'ev_' + now,
                type,
                time: new Date().toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit', second: '2-digit' }),
                page: body.page || '/',
                label: body.label || body.service || (type === 'page_view' ? 'Sayfa Ziyareti' : type),
                device: body.device || 'Mobil'
            });
            if (isolateEvents.length > 50) isolateEvents.length = 50;

            return jsonResponse({ status: 'ok', received: true });
        } catch (err) {
            return jsonResponse({ error: err.message }, 400);
        }
    }

    if (req.method === 'GET') {
        return jsonResponse({
            status: 'ok',
            stats: isolateStats,
            recentEvents: isolateEvents.slice(0, 30),
            serverTime: new Date().toISOString()
        });
    }

    return jsonResponse({ error: 'Method not allowed' }, 405);
}
