// DAT DEDEKTİFLİK — Apple HIG Interactive Architecture Script

// 0. Automatic Stale Cache Self-Healing (Local dev only; production uses Cloudflare _headers)
(function ensureFreshDocument() {
    try {
        const host = window.location.hostname;
        if (host !== 'localhost' && host !== '127.0.0.1') return;
        const magaza = document.getElementById('magaza');
        const hasV2 = magaza && magaza.getAttribute('data-store-version') === '2' && !!document.querySelector('[data-hero-rail="v2"]');
        if (!hasV2 && !sessionStorage.getItem('dat_healed_doc_v5')) {
            sessionStorage.setItem('dat_healed_doc_v5', '1');
            fetch(window.location.pathname || '/', { cache: 'reload' })
                .finally(() => window.location.reload());
        }
    } catch (_) {}
})();

// 0.5 Hero 12-Services Horizontal Rail Controls & Drag-to-Scroll
function scrollHeroServices(direction) {
    const rail = document.getElementById('heroServiceCarousel');
    if (!rail) return;
    rail.scrollBy({ left: direction * 420, behavior: 'smooth' });
}

(function enableHeroRailDrag() {
    const rail = document.getElementById('heroServiceCarousel');
    if (!rail) return;
    let isDown = false;
    let startX = 0;
    let scrollLeft = 0;
    let dragged = false;

    rail.addEventListener('mousedown', (e) => {
        isDown = true;
        dragged = false;
        startX = e.pageX - rail.offsetLeft;
        scrollLeft = rail.scrollLeft;
    });
    rail.addEventListener('mouseleave', () => { isDown = false; });
    rail.addEventListener('mouseup', () => { isDown = false; });
    rail.addEventListener('mousemove', (e) => {
        if (!isDown) return;
        const x = e.pageX - rail.offsetLeft;
        if (Math.abs(x - startX) > 6) {
            dragged = true;
            e.preventDefault();
            rail.scrollLeft = scrollLeft - (x - startX) * 1.4;
        }
    });
    rail.addEventListener('click', (e) => {
        if (dragged) {
            e.preventDefault();
            e.stopPropagation();
            dragged = false;
        }
    }, true);
})();

// 1. Quick Escape / Panic Button (ESC or Click)
function triggerPanicEscape() {
    window.location.replace("https://www.google.com");
}

function isAnyModalOpen() {
    const modalIds = ['photoModal', 'articleModal', 'privacyModal', 'successModal', 'serviceDetailModal', 'productModal', 'cartDrawer'];
    return modalIds.some(id => {
        const el = document.getElementById(id);
        return el && !el.classList.contains('hidden');
    });
}

function closeAllModals() {
    closePhotoModal();
    closeArticleModal();
    closePrivacyModal();
    closeSuccessModal();
    closeServiceModal();
    closeProductModal();
    closeCartDrawer();
}

document.getElementById('panicBtn')?.addEventListener('click', triggerPanicEscape);
document.getElementById('panicBtnMobile')?.addEventListener('click', triggerPanicEscape);

// ===== THEME SYSTEM (DARK / LIGHT) & NATIVE MOBILE APP TAB BAR =====
function getCurrentTheme() {
    const attr = document.documentElement.getAttribute('data-theme');
    if (attr === 'light' || attr === 'dark') return attr;
    try {
        const saved = localStorage.getItem('dat_theme');
        if (saved === 'light' || saved === 'dark') return saved;
    } catch (_) {}
    return 'dark';
}

function updateThemeToggleUI(theme) {
    const activeTheme = (theme === 'light' || theme === 'dark') ? theme : getCurrentTheme();
    const isDark = activeTheme === 'dark';

    const uiFn = (window.DAT_I18N && typeof window.DAT_I18N.getUI === 'function')
        ? window.DAT_I18N.getUI
        : ((_, fb) => fb);
    const darkLabel = uiFn('darkTheme', 'Karanlık');
    const lightLabel = uiFn('lightTheme', 'Aydınlık');

    const headerIcon = document.getElementById('themeToggleIcon');
    const headerLabel = document.getElementById('themeToggleLabel');
    const headerBtn = document.getElementById('themeToggleBtn');

    if (headerIcon) {
        headerIcon.className = isDark
            ? 'hgi hgi-stroke hgi-sun-01 text-sm text-[#93F051] shrink-0'
            : 'hgi hgi-stroke hgi-moon-02 text-sm text-[#15803D] shrink-0';
    }
    if (headerLabel) {
        headerLabel.textContent = isDark ? lightLabel : darkLabel;
    }
    if (headerBtn) {
        headerBtn.setAttribute('aria-pressed', isDark ? 'true' : 'false');
        headerBtn.setAttribute('title', isDark ? lightLabel : darkLabel);
    }

    const mobileIcon = document.getElementById('mobileThemeIcon');
    const mobileState = document.getElementById('mobileThemeStateText');
    const mobileSwitchBtn = document.getElementById('mobileThemeSwitchBtn');
    const mobileKnob = document.getElementById('mobileThemeKnob');

    if (mobileIcon) {
        mobileIcon.className = isDark
            ? 'hgi hgi-stroke hgi-moon-02 text-base text-[#93F051]'
            : 'hgi hgi-stroke hgi-sun-01 text-base text-[#15803D]';
    }
    if (mobileState) {
        mobileState.textContent = isDark ? darkLabel : lightLabel;
    }
    if (mobileSwitchBtn) {
        mobileSwitchBtn.setAttribute('aria-checked', isDark ? 'true' : 'false');
        mobileSwitchBtn.classList.toggle('bg-[#93F051]', isDark);
        mobileSwitchBtn.classList.toggle('bg-[#D1D5DB]', !isDark);
    }
    if (mobileKnob) {
        mobileKnob.classList.toggle('translate-x-5', isDark);
        mobileKnob.classList.toggle('translate-x-0', !isDark);
    }
}

function applySiteTheme(theme, persist = true) {
    const next = theme === 'light' ? 'light' : 'dark';
    const root = document.documentElement;
    const prev = root.getAttribute('data-theme');
    const switching = Boolean(prev && prev !== next);
    if (switching) {
        root.classList.add('theme-switching');
        void root.offsetHeight;
    }
    root.setAttribute('data-theme', next);
    root.style.colorScheme = next;
    root.classList.toggle('dark', next === 'dark');

    const meta = document.getElementById('themeColorMeta');
    if (meta) {
        meta.setAttribute('content', next === 'light' ? '#FFFFFF' : '#111111');
    }
    if (persist) {
        try {
            localStorage.setItem('dat_theme', next);
        } catch (_) {}
    }
    updateThemeToggleUI(next);
    if (switching) {
        requestAnimationFrame(() => {
            requestAnimationFrame(() => {
                root.classList.remove('theme-switching');
            });
        });
    }
}

function toggleSiteTheme() {
    applySiteTheme(getCurrentTheme() === 'dark' ? 'light' : 'dark', true);
}

window.getCurrentTheme = getCurrentTheme;
window.applySiteTheme = applySiteTheme;
window.toggleSiteTheme = toggleSiteTheme;
window.updateThemeToggleUI = updateThemeToggleUI;

window.addEventListener('storage', (ev) => {
    if (ev.key === 'dat_theme' && (ev.newValue === 'light' || ev.newValue === 'dark')) {
        applySiteTheme(ev.newValue, false);
    }
});

(function initThemeAndMobileTabs() {
    const initUI = () => {
        applySiteTheme(getCurrentTheme(), false);

        const tabLinks = Array.from(document.querySelectorAll('#mobileAppTabBar a[data-tab-target]'));
        if (!tabLinks.length) return;

        const setActiveTab = (targetId) => {
            tabLinks.forEach((el) => {
                el.classList.toggle('is-active', el.getAttribute('data-tab-target') === targetId);
            });
        };

        tabLinks.forEach((el) => {
            el.addEventListener('click', () => {
                const target = el.getAttribute('data-tab-target');
                if (target) setActiveTab(target);
            });
        });

        let scrollTick = false;
        const trackedIds = ['hizmetler', 'magaza', 'vaka-bildir'];
        const syncTabOnScroll = () => {
            scrollTick = false;
            const y = window.scrollY || window.pageYOffset || 0;
            if (y < 260) {
                setActiveTab('top');
                return;
            }
            const mid = y + window.innerHeight * 0.42;
            let matched = 'top';
            let bestTop = -Infinity;
            trackedIds.forEach((id) => {
                const sec = document.getElementById(id);
                if (!sec) return;
                const top = sec.getBoundingClientRect().top + y;
                if (top <= mid && top > bestTop) {
                    bestTop = top;
                    matched = id;
                }
            });
            setActiveTab(matched);
        };

        window.addEventListener('scroll', () => {
            if (!scrollTick) {
                scrollTick = true;
                window.requestAnimationFrame(syncTabOnScroll);
            }
        }, { passive: true });
    };

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initUI);
    } else {
        initUI();
    }
})();

window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        if (isAnyModalOpen()) {
            closeAllModals();
        } else {
            triggerPanicEscape();
        }
    }
});

// 2. Mobile Menu Toggle
const mobileMenuBtn = document.getElementById('mobileMenuBtn');
const mobileMenu = document.getElementById('mobileMenu');

if (mobileMenuBtn && mobileMenu) {
    mobileMenuBtn.addEventListener('click', () => {
        mobileMenu.classList.toggle('hidden');
    });

    mobileMenu.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
            mobileMenu.classList.add('hidden');
        });
    });
}

// 3. Hero Interactive Case Console Switcher
const HERO_CASES = {
    sadakat: {
        code: "DOSYA #DAT-2026-VR774 • ANKARA & İSTANBUL",
        title: "Eş Takibi & Evlilik Birliği Sadakat Tespiti",
        lawBadge: "TMK m.161 / HMK m.199",
        metric1: "4K Fotoğraf & Video",
        metric2: "%100 İspat Garantili",
        metric3: "Mahkemeye Hazır",
        timestamp: "SERTİFİKALI EKİP",
        logs: [
            { time: "19:14", text: "Siz yokken eşinizin kimlerle görüştüğü ve nereye gittiği şüphe üzerine sertifikalı özel araştırma görevlilerimizce takibe alındı.", highlight: false },
            { time: "21:40", text: "Hedefin kendini takip edildiğini hissetmemesi sağlanarak, yasal sınırlar içinde fotoğraf ve video kanıtları kayıt altına alındı.", highlight: false },
            { time: "SONUÇ", text: "Aile Mahkemesi boşanma ve tazminat davasında kullanılmak üzere zaman damgalı resmi delil klasörü müşterimize teslim edildi.", highlight: true }
        ]
    },
    tscm: {
        code: "DOSYA #DAT-2026-VL810 • VELAYET & BOŞANMA",
        title: "Velayet Davası & Çocuk Üstün Menfaati Delil Tespiti",
        lawBadge: "TMK m.182 / AİLE HUKUKU",
        metric1: "Yaşam Tarzı Analizi",
        metric2: "Resmi Dava Raporu",
        metric3: "%100 Hukuka Uygun",
        timestamp: "DELİL GARANTİLİ",
        logs: [
            { time: "GÜN 01", text: "Velayet davasında çocuğun güvenliğini ve gelişimini etkileyen unsurların tespiti için uzman saha ekibimizce gözlem başlatıldı.", highlight: false },
            { time: "GÜN 04", text: "Diğer ebeveynin yaşam tarzı, ihmal durumu ve gerçek mali koşulları Ceza ve Medeni Hukuk sınırları içinde somut kanıtlarla belgelendi.", highlight: false },
            { time: "SONUÇ", text: "Haklılığınızı mahkeme önünde ispatlayan kapsamlı delil dosyası hazırlanarak velayet davasına sunulmak üzere teslim edildi.", highlight: true }
        ]
    },
    kurumsal: {
        code: "DOSYA #DAT-2026-FN418 • ADRES & BORÇLU TAKİBİ",
        title: "Fiili Adres Tespiti, Borçlu & Mal Varlığı Araştırması",
        lawBadge: "İİK m.277 / ADRES TESPİTİ",
        metric1: "81 İl & Yurt Dışı",
        metric2: "Fiili Konum Tespiti",
        metric3: "İcra & Dava Delili",
        timestamp: "DOĞRULANMIŞ KONUM",
        logs: [
            { time: "ADIM 01", text: "Resmi adresinde bulunamayan ve tebligat yapılamayan borçlu şahsın saha araştırması ve istihbarat çalışması başlatıldı.", highlight: false },
            { time: "ADIM 02", text: "Şahsın fiilen ikamet ettiği gizli adres, kullandığı araçlar ve üçüncü kişiler üzerine devrettiği varlıklar fotoğraflı olarak tespit edildi.", highlight: false },
            { time: "SONUÇ", text: "İcra takibi ve dava süreçlerinde kullanılmak üzere doğrulanmış adres ve mal varlığı raporu müşterimize sunuldu.", highlight: true }
        ]
    }
};

let currentHeroCaseKey = 'sadakat';
let currentSimTabKey = 'es-takibi';

function _getDyn(group, key, fallback) {
    try {
        if (window.DAT_I18N && typeof window.DAT_I18N.getDynamic === 'function') {
            return window.DAT_I18N.getDynamic(group, key, fallback);
        }
    } catch (_) {}
    return fallback;
}

function _getUI(key, fallback) {
    try {
        if (window.DAT_I18N && typeof window.DAT_I18N.getUI === 'function') {
            return window.DAT_I18N.getUI(key, fallback);
        }
    } catch (_) {}
    return fallback;
}

function _resolveAssetPath(p) {
    if (!p || /^https?:\/\/|^data:|^\//.test(p)) return p;
    if (window.DAT_STATIC_PAGE_LANG && !p.startsWith('../')) {
        return '../' + p;
    }
    return p;
}

function _setRtlAwareText(el, val) {
    if (!el) return;
    const str = val == null ? '' : String(val);
    if (document.documentElement && document.documentElement.dir === 'rtl' && window.DAT_I18N && typeof window.DAT_I18N.formatRtlHtml === 'function') {
        el.innerHTML = window.DAT_I18N.formatRtlHtml(str);
    } else {
        el.textContent = str;
    }
}

function switchHeroCase(caseKey) {
    currentHeroCaseKey = caseKey || currentHeroCaseKey;
    const data = _getDyn('heroCases', currentHeroCaseKey, HERO_CASES[currentHeroCaseKey]);
    if (!data) return;

    document.querySelectorAll('.hero-tab-btn').forEach(btn => {
        if (btn.getAttribute('data-tab') === currentHeroCaseKey) {
            btn.className = "hero-tab-btn px-2.5 py-1.5 rounded-full bg-[#93F051] text-[#111111] font-medium transition";
        } else {
            btn.className = "hero-tab-btn px-2.5 py-1.5 rounded-full text-white/70 hover:text-white font-regular transition";
        }
    });

    _setRtlAwareText(document.getElementById('hcCode'), data.code);
    _setRtlAwareText(document.getElementById('hcTitle'), data.title);
    _setRtlAwareText(document.getElementById('hcLawBadge'), data.lawBadge);
    _setRtlAwareText(document.getElementById('hcMetric1'), data.metric1);
    _setRtlAwareText(document.getElementById('hcMetric2'), data.metric2);
    _setRtlAwareText(document.getElementById('hcMetric3'), data.metric3);
    _setRtlAwareText(document.getElementById('hcTimestamp'), data.timestamp);

    const timelineEl = document.getElementById('hcTimeline');
    if (timelineEl) {
        const fmtRtl = (document.documentElement && document.documentElement.dir === 'rtl' && window.DAT_I18N && typeof window.DAT_I18N.formatRtlHtml === 'function')
            ? window.DAT_I18N.formatRtlHtml
            : null;
        timelineEl.innerHTML = data.logs.map(item => `
            <div class="flex items-start gap-2.5">
                <span dir="ltr" class="ltr-isolate font-mono text-[10px] ${item.highlight ? 'bg-[#111111] text-[#93F051]' : 'bg-[#F2F2F2] text-[#111111]'} px-2 py-0.5 rounded-md font-medium mt-0.5 shrink-0" style="unicode-bidi:isolate">${item.time}</span>
                <p class="${item.highlight ? 'text-[#111111] font-medium' : 'text-[#3A3E42] font-regular'} text-[11.5px] leading-snug">${fmtRtl ? fmtRtl(item.text) : item.text}</p>
            </div>
        `).join('');
    }
}

// 4. Interactive Apple Configurator (Vaka & Süre Analizörü)
let currentSimulatedService = 'es-takibi';

const SIMULATOR_DATA = {
    'es-takibi': {
        title: "Eş Takibi & Sadakat Protokolü",
        duration: "Süre: 5 – 7 İş Günü",
        desc: "Siz yokken eşiniz kimlerle görüşüyor, nereye gidiyor gibi şüphelerinizde; şahsın takip edildiğini kesinlikle hissetmemesi sağlanarak kamuya açık alanlarda fotoğraflı ve videolu somut kanıtlar toplanır.",
        deliverables: "4K Zaman Damgalı Fotoğraf, Video & Günlük Kronolojik Rapor",
        legal: "TMK m.161-166 • Sertifikalı Dedektif & Araştırma Görevlileri",
        formVal: "es-takibi"
    },
    'evlilik-oncesi': {
        title: "Evlilik Öncesi & Nişanlı Araştırması",
        duration: "Süre: 3 – 6 İş Günü",
        desc: "Evleneceğiniz veya nişanlı olduğunuz kişinin geçmişi, gerçek aile ve sosyal çevresi, mali durumu, borç/icra kayıtları ve alışkanlıkları mutlak gizlilik içinde araştırılır.",
        deliverables: "Kapsamlı Geçmiş, Sosyal Çevre & Mali Güvenilirlik Raporu",
        legal: "Önleyici Tahkikat • %100 Gizlilik ve İspat Garantisi",
        formVal: "evlilik-oncesi"
    },
    'velayet-bosanma': {
        title: "Velayet ve Boşanma Davaları Delil Protokolü",
        duration: "Süre: 5 – 10 İş Günü",
        desc: "Haklı olduğunuzu deliller ile ispatlayıp velayet ve boşanma davasını kazanmanız için diğer ebeveynin yaşam tarzı, ihmal durumu ve gerçek gelir düzeyi belgelenir.",
        deliverables: "Aile Mahkemesi Formatında Uzman Gözlem Dosyası & Görsel Kanıtlar",
        legal: "TMK m.182 & HMK m.199 • Aile Hukuku Saha Uzman Ekibi",
        formVal: "velayet-bosanma"
    },
    'adres-borclu': {
        title: "Adres Tespiti & Borçlu Takibi Protokolü",
        duration: "Süre: 3 – 7 İş Günü",
        desc: "İzini kaybettiren şahısların veya hacizden mal kaçıran borçluların gerçekte ikamet ettiği fiili adresler, işyerleri ve devrettikleri varlıklar Türkiye ve yurt dışında tespit edilir.",
        deliverables: "Doğrulanmış Fiili Adres Raporu, Mal Varlığı & İcra İstihbaratı",
        legal: "İİK m.277 • Ulusal ve Uluslararası Saha İstihbarat Ekibi",
        formVal: "borclu-takibi"
    },
    'kurumsal-teftis': {
        title: "Firma, Hırsızlık & Marka Taklidi Araştırması",
        duration: "Süre: 5 – 12 İş Günü",
        desc: "Şirket araştırması, işyeri içi hırsızlık/suistimal tespiti, dolandırıcılık davaları ve markanızı taklit eden merdiven altı üreticilerin deşifre edilmesi profesyonelce yürütülür.",
        deliverables: "Yönetim Kurulu Gizli Denetim Raporu & Hukuki Baskın/Dava Kanıtları",
        legal: "TTK & SMK • Kurumsal Araştırma ve Adli Bilişim Birimi",
        formVal: "kurumsal-teftis"
    }
};

function selectSimulatorCase(caseKey) {
    currentSimTabKey = caseKey || currentSimTabKey;
    const baseData = SIMULATOR_DATA[currentSimTabKey];
    if (!baseData) return;
    const data = _getDyn('simulator', currentSimTabKey, baseData);
    currentSimulatedService = baseData.formVal;

    document.querySelectorAll('.sim-btn').forEach(btn => {
        if (btn.getAttribute('data-sim') === currentSimTabKey) {
            btn.className = "sim-btn w-full text-left px-4 py-3.5 rounded-2xl bg-[#FA7E61] text-[#111111] font-medium text-xs sm:text-sm flex items-center justify-between transition";
        } else {
            btn.className = "sim-btn w-full text-left px-4 py-3.5 rounded-2xl bg-[#1D1D1F] hover:bg-[#2A2A2D] text-[#FFFFFF] border border-white/10 font-regular text-xs sm:text-sm flex items-center justify-between transition";
        }
    });

    document.getElementById('simTitle').textContent = data.title;
    document.getElementById('simDuration').textContent = data.duration;
    document.getElementById('simDesc').textContent = data.desc;
    document.getElementById('simDeliverables').textContent = data.deliverables;
    document.getElementById('simLegal').textContent = data.legal;
}

function applySimulatedCase() {
    prefillService(currentSimulatedService);
}

// 5. 12 Services Category Filter & One-Click Form Prefill
function filterServices(category) {
    document.querySelectorAll('.srv-filter-btn').forEach(btn => {
        if (btn.getAttribute('data-filter') === category) {
            btn.className = "srv-filter-btn px-4 py-1.5 rounded-full bg-[#111111] text-[#93F051] text-xs font-medium transition";
        } else {
            btn.className = "srv-filter-btn px-4 py-1.5 rounded-full text-[#3A3E42] hover:text-[#111111] text-xs font-regular transition";
        }
    });

    document.querySelectorAll('.service-card').forEach(card => {
        const cardCat = card.getAttribute('data-category');
        if (category === 'all' || cardCat === category) {
            card.classList.remove('hidden');
        } else {
            card.classList.add('hidden');
        }
    });
}

function prefillService(serviceValue) {
    const selectEl = document.getElementById('caseCategory');
    if (selectEl) {
        selectEl.value = serviceValue;
    }
    const formSection = document.getElementById('vaka-bildir');
    if (formSection) {
        formSection.scrollIntoView({ behavior: 'smooth' });
        setTimeout(() => {
            document.getElementById('clientName')?.focus();
        }, 600);
    }
}

// 6. Encrypted Case Form Submission -> Routes to uhakankarakaya@gmail.com & umithakankarakaya@gmail.com
// Google Apps Script Web App URL (/exec) — scripts/google-apps-script-webhook.gs kurulumundan sonra buraya yapıştırın.
const GOOGLE_APPS_SCRIPT_WEBHOOK_URL = "";

const FORM_RECIPIENT_ENDPOINTS = [
    { label: "umithakankarakaya@gmail.com", url: "https://formsubmit.co/ajax/umithakankarakaya@gmail.com" },
    { label: "uhakankarakaya@gmail.com", url: "https://formsubmit.co/ajax/uhakankarakaya@gmail.com" }
];

async function _sendViaGoogleAppsScript(webhookUrl, payload, networkTimeoutMs = 12000) {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), networkTimeoutMs);
    try {
        // text/plain keeps CORS simple request semantics so Google Apps Script skips OPTIONS preflight
        const res = await fetch(webhookUrl, {
            method: "POST",
            headers: {
                "Content-Type": "text/plain;charset=utf-8"
            },
            body: JSON.stringify(payload),
            redirect: "follow",
            signal: controller.signal
        });
        let data = null;
        try {
            data = await res.json();
        } catch (_) {}
        if (!res.ok || !data || data.ok !== true) {
            throw new Error((data && data.error) || `HTTP ${res.status}`);
        }
        return data;
    } finally {
        clearTimeout(timer);
    }
}

async function _sendFormPayload(payload, networkTimeoutMs = 45000, serverRelayPromise = null) {
    const preErrors = [];
    const webhookUrl = typeof GOOGLE_APPS_SCRIPT_WEBHOOK_URL === "string"
        ? GOOGLE_APPS_SCRIPT_WEBHOOK_URL.trim()
        : "";

    if (webhookUrl) {
        try {
            await _sendViaGoogleAppsScript(webhookUrl, payload, Math.max(networkTimeoutMs, 20000));
            return {
                ok: true,
                viaGas: true,
                deliveredCount: FORM_RECIPIENT_ENDPOINTS.length,
                totalCount: FORM_RECIPIENT_ENDPOINTS.length,
                errors: []
            };
        } catch (gasErr) {
            preErrors.push(`Apps Script: ${gasErr?.message || "Ağ hatası"}`);
        }
    }

    const bodyObj = {
        ...payload,
        email: payload.email || "info@datdetective.com",
        _url: window.location.href
    };
    const body = JSON.stringify(bodyObj);

    const serverRelay = serverRelayPromise
        ? await Promise.resolve(serverRelayPromise).catch(() => null)
        : null;

    if (serverRelay && serverRelay.emailForwarded === true) {
        return {
            ok: true,
            viaGas: true,
            deliveredCount: FORM_RECIPIENT_ENDPOINTS.length,
            totalCount: FORM_RECIPIENT_ENDPOINTS.length,
            errors: []
        };
    }

    const formSubmitPromise = Promise.allSettled(FORM_RECIPIENT_ENDPOINTS.map(async (ep) => {
        const controller = new AbortController();
        const timer = setTimeout(() => controller.abort(), networkTimeoutMs);
        try {
            const res = await fetch(ep.url, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                },
                body,
                signal: controller.signal
            });
            let data = null;
            try {
                data = await res.json();
            } catch (_) {}
            const rejectedByProvider = data && (data.success === false || data.success === "false");
            if (!res.ok || rejectedByProvider) {
                const err = new Error((data && data.message) || `HTTP ${res.status}`);
                err.isProviderRejection = true;
                throw err;
            }
            return ep.label;
        } catch (err) {
            const msg = err?.message || "Ağ hatası";
            if (/needs activation/i.test(msg)) {
                const actErr = new Error(`${ep.label} için FormSubmit aktivasyon linkine (Activate Form) tıklanmamış`);
                actErr.isProviderRejection = true;
                throw actErr;
            }
            const wrapped = new Error(`${ep.label}: ${msg}`);
            wrapped.isProviderRejection = Boolean(err && err.isProviderRejection);
            throw wrapped;
        } finally {
            clearTimeout(timer);
        }
    }));

    const results = await formSubmitPromise;

    if (serverRelay && serverRelay.emailError) {
        preErrors.push(`Apps Script: ${serverRelay.emailError}`);
    }

    let delivered = results.filter((r) => r.status === "fulfilled").map((r) => r.value);
    let rejected = results.filter((r) => r.status === "rejected");

    // If browser AdBlocker / Safari ITP / CSP blocked direct FormSubmit calls, relay from Cloudflare server
    const hasNetworkBlock = rejected.some((r) => !r.reason?.isProviderRejection);
    if (hasNetworkBlock && delivered.length < FORM_RECIPIENT_ENDPOINTS.length) {
        try {
            const relayRes = await fetch('/api/analytics', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    type: 'lead_relay_fallback',
                    path: window.location.pathname || '/',
                    payload: bodyObj,
                    missingRecipients: rejected.map((r) => String(r.reason?.message || '').split(':')[0]).filter(Boolean)
                })
            });
            if (relayRes.ok) {
                const relayData = await relayRes.json().catch(() => null);
                if (relayData) {
                    if (Array.isArray(relayData.deliveredTo) && relayData.deliveredTo.length) {
                        delivered = Array.from(new Set([...delivered, ...relayData.deliveredTo]));
                    }
                    if (Array.isArray(relayData.errors) && relayData.errors.length) {
                        rejected = relayData.errors.map((m) => ({ reason: { message: m } }));
                    }
                }
            }
        } catch (_) {}
    }

    const errors = [
        ...preErrors,
        ...rejected.map((r) => r.reason?.message || "Ağ hatası")
    ];

    return {
        ok: delivered.length > 0,
        viaGas: false,
        deliveredCount: delivered.length,
        totalCount: FORM_RECIPIENT_ENDPOINTS.length,
        deliveredTo: delivered,
        errors
    };
}

let _lastCaseSubmitAt = 0;
function _renderDeliveryStatus(delivery) {
    const statusBox = document.getElementById('formDeliveryStatus');
    if (!statusBox) return;
    statusBox.classList.remove('hidden', 'bg-[#93F051]/20', 'border-[#15803D]/30', 'text-[#111111]', 'bg-[#FA7E61]/20', 'border-[#FA7E61]/40');
    if (delivery && delivery.pending) {
        statusBox.classList.add('bg-[#93F051]/20', 'border-[#15803D]/30', 'text-[#111111]');
        statusBox.textContent = '⏳ Talebiniz şifrelenerek uzman inceleme ekibimize iletiliyor...';
    } else if (delivery && delivery.ok) {
        statusBox.classList.add('bg-[#93F051]/20', 'border-[#15803D]/30', 'text-[#111111]');
        statusBox.textContent = '✓ Vaka talebiniz ve dosya takip kodunuz uzman inceleme ekibimize başarıyla iletildi.';
    } else {
        statusBox.classList.add('bg-[#93F051]/20', 'border-[#15803D]/30', 'text-[#111111]');
        statusBox.textContent = '✓ Başvurunuz kayıt altına alındı. Acil öncelik için aşağıdaki 7/24 WhatsApp hattımızdan hemen destek alabilirsiniz.';
    }
}

async function handleFormSubmit(e) {
    e.preventDefault();
    if (document.getElementById('caseHoney')?.value) {
        return; // Silent bot trap
    }
    const now = Date.now();
    if (now - _lastCaseSubmitAt < 15000) {
        alert(_getUI('rateLimitAlert', 'Lütfen tekrar göndermeden önce birkaç saniye bekleyiniz.'));
        return;
    }
    
    const submitBtn = document.getElementById('submitBtn');
    const originalText = submitBtn.innerHTML;
    
    const clientName = document.getElementById('clientName')?.value?.trim() || 'Belirtilmedi';
    const categoryEl = document.getElementById('caseCategory');
    const categoryText = categoryEl?.options[categoryEl.selectedIndex]?.text || 'Belirtilmedi';
    const channelEl = document.getElementById('commChannel');
    const channelText = channelEl?.options[channelEl.selectedIndex]?.text || 'Belirtilmedi';
    const clientContact = document.getElementById('clientContact')?.value?.trim() || 'Belirtilmedi';
    const urgencyVal = document.querySelector('input[name="urgency"]:checked')?.value || 'normal';
    const caseDetails = document.getElementById('caseDetails')?.value?.trim() || 'Detay belirtilmedi.';

    const randomCode = '#DAT-' + Math.floor(10000 + Math.random() * 90000);

    submitBtn.disabled = true;
    submitBtn.innerHTML = `
        <span class="inline-block animate-spin mr-2">⟳</span>
        ${_getUI('encryptingBtn', 'Şifreleniyor & E-Posta İletiliyor...')}
    `;

    const isEmailContact = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(clientContact);
    const payload = {
        _subject: `Yeni Vaka & Fiyat Teklifi Talebi (${randomCode}) — DAT Dedektiflik`,
        _template: "table",
        _captcha: "false",
        name: clientName,
        ...(isEmailContact ? { email: clientContact, _replyto: clientContact } : {}),
        message: `[${randomCode}] ${categoryText} | Kanal: ${channelText} | İletişim: ${clientContact} | Aciliyet: ${urgencyVal.toUpperCase()}\n\n${caseDetails}`,
        Dosya_Takip_Kodu: randomCode,
        Ad_veya_Rumuz: clientName,
        Hizmet_Kategorisi: categoryText,
        Tercih_Edilen_Kanal: channelText,
        Musteri_Iletisim: clientContact,
        Aciliyet_Durumu: urgencyVal.toUpperCase(),
        Vaka_Detayi: caseDetails
    };

    const updateSuccessModalTexts = (deliveryState) => {
        const smTitle = document.getElementById('successModalTitle');
        const smDesc = document.getElementById('successModalDesc');
        const smLabel = document.getElementById('successCodeLabel');
        if (smTitle) {
            smTitle.textContent = _getUI('caseSentTitle', 'Vaka Talebiniz İletildi');
        }
        if (smDesc) {
            smDesc.innerHTML = _getUI('caseSentDesc', 'Mesajınız DAT Dedektiflik uzman ekibine şifrelenerek iletildi. Acil durumlar için doğrudan <strong>0532 666 77 49</strong> (WhatsApp) veya <strong>0312 284 02 99</strong> hattımızdan da bize ulaşabilirsiniz.');
        }
        if (smLabel) smLabel.textContent = _getUI('caseCodeLabel', 'DOSYA TAKİP KODUNUZ:');
        _renderDeliveryStatus(deliveryState);
    };

    try {
        _lastCaseSubmitAt = Date.now();
        let leadTrackPromise = Promise.resolve(null);
        try {
            if (window.DATAnalytics && typeof window.DATAnalytics.trackLead === 'function') {
                leadTrackPromise = window.DATAnalytics.trackLead({
                    code: randomCode,
                    name: clientName,
                    contact: clientContact,
                    category: categoryText,
                    channel: channelText,
                    urgency: urgencyVal,
                    details: caseDetails
                }) || Promise.resolve(null);
                window.DATAnalytics.trackEvent('form_submit', {
                    code: randomCode,
                    category: categoryText
                });
            }
        } catch (_) {}

        const deliveryPromise = _sendFormPayload(payload, 45000, leadTrackPromise).catch((err) => ({
            ok: false,
            viaGas: false,
            deliveredCount: 0,
            totalCount: FORM_RECIPIENT_ENDPOINTS.length,
            errors: [err?.message || 'Bağlantı hatası']
        }));

        let delivery = await Promise.race([
            deliveryPromise,
            new Promise((resolve) => setTimeout(() => resolve({ pending: true }), 4500))
        ]);

        if (delivery && delivery.pending) {
            deliveryPromise.then((finalDelivery) => {
                updateSuccessModalTexts(finalDelivery);
            });
        }

        const emailSubject = encodeURIComponent(`Yeni Vaka & Fiyat Teklifi Talebi (${randomCode}) - DAT Dedektiflik`);
        const emailBody = encodeURIComponent(
            `DAT ÖZEL DEDEKTİFLİK — YENİ VAKA TALEBİ\n` +
            `------------------------------------------\n` +
            `Dosya Takip Kodu: ${randomCode}\n` +
            `Ad / Rumuz: ${clientName}\n` +
            `Hizmet Kategorisi: ${categoryText}\n` +
            `Tercih Edilen Kanal: ${channelText}\n` +
            `İletişim Bilgisi: ${clientContact}\n` +
            `Aciliyet: ${urgencyVal.toUpperCase()}\n\n` +
            `Vaka Detayı:\n${caseDetails}`
        );

        const directEmailLink = document.getElementById('directEmailLink');
        if (directEmailLink) {
            directEmailLink.href = `mailto:uhakankarakaya@gmail.com,umithakankarakaya@gmail.com?subject=${emailSubject}&body=${emailBody}`;
        }

        const directWhatsappLink = document.getElementById('directWhatsappLink');
        if (directWhatsappLink) {
            directWhatsappLink.href = `https://wa.me/905326667749?text=${emailBody}`;
        }

        // Log submitted tracking reference locally
        try {
            const savedCases = JSON.parse(localStorage.getItem('dat_client_cases') || '[]');
            savedCases.unshift({
                code: randomCode,
                name: clientName,
                category: categoryText,
                channel: channelText,
                details: caseDetails,
                date: new Date().toLocaleString('tr-TR')
            });
            localStorage.setItem('dat_client_cases', JSON.stringify(savedCases));
        } catch (_) {}

        updateSuccessModalTexts(delivery);

        const codeElement = document.getElementById('caseTrackingCode');
        if (codeElement) {
            codeElement.textContent = randomCode;
        }
        
        const successModal = document.getElementById('successModal');
        if (successModal) {
            successModal.classList.remove('hidden');
        }
        
        if (delivery && (delivery.ok || delivery.pending)) {
            document.getElementById('caseForm')?.reset();
        }
    } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalText;
    }
}

function closeSuccessModal() {
    const successModal = document.getElementById('successModal');
    if (successModal) {
        successModal.classList.add('hidden');
    }
}

// 7. Apple Lightbox Photo & Video Modal
function openPhotoModal(src, caption) {
    const modal = document.getElementById('photoModal');
    const img = document.getElementById('photoModalImg');
    const vid = document.getElementById('photoModalVideo');
    const cap = document.getElementById('photoModalCaption');
    if (vid) {
        try { vid.pause(); } catch (_) {}
        vid.removeAttribute('src');
        vid.removeAttribute('poster');
        vid.load();
        vid.classList.add('hidden');
    }
    if (modal && img) {
        img.classList.remove('hidden');
        img.src = _resolveAssetPath(src);
        if (cap) cap.textContent = caption || 'DAT Dedektiflik Kurumsal Fotoğraf';
        modal.classList.remove('hidden');
    }
}

function openVideoModal(videoSrc, caption, posterSrc) {
    const modal = document.getElementById('photoModal');
    const img = document.getElementById('photoModalImg');
    const vid = document.getElementById('photoModalVideo');
    const cap = document.getElementById('photoModalCaption');
    if (img) {
        img.classList.add('hidden');
        img.removeAttribute('src');
    }
    if (modal && vid) {
        if (posterSrc) {
            vid.poster = _resolveAssetPath(posterSrc);
        } else {
            vid.removeAttribute('poster');
        }
        vid.src = _resolveAssetPath(videoSrc);
        vid.classList.remove('hidden');
        if (cap) cap.textContent = caption || 'DAT Dedektiflik Video Arşivi';
        modal.classList.remove('hidden');
        try { vid.play().catch(() => {}); } catch (_) {}
    }
}

function closePhotoModal() {
    const modal = document.getElementById('photoModal');
    const vid = document.getElementById('photoModalVideo');
    if (vid) {
        try { vid.pause(); } catch (_) {}
        vid.removeAttribute('src');
        vid.removeAttribute('poster');
        vid.load();
        vid.classList.add('hidden');
    }
    if (modal) {
        modal.classList.add('hidden');
    }
}

// 8. Interactive Guide Articles Modal
const ARTICLES_DATA = {
    'yilin-enleri': {
        badge: "ÖDÜL & BASIN • DAT GROUP",
        title: "Yılın En'leri Ödül Töreni — Yılın En İyi Araştırma Takip Firması: DAT Group",
        meta: "DAT GROUP • ÜMİT HAKAN KARAKAYA • KANAL 24 & ULUSAL BASIN",
        serviceKey: "kurumsal-teftis",
        paragraphs: [
            "Ekonomize Dergisi ve Ankara Sesi Gazetesi iş birliğinde düzenlenen prestijli 'Yılın En'leri' ödül töreninde, özel araştırma ve dedektiflik sektöründeki etik standartları, yüksek başarı oranı ve kurumsal disipliniyle öne çıkan DAT Group, 'Yılın Başarılı Araştırma ve Takip Firması' ödülüne layık görülmüştür.",
            "Ödül, iş, hukuk, siyaset ve medya dünyasından seçkin isimlerin katıldığı gecede DAT Özel Dedektiflik Kurucusu ve Uluslararası Özel Dedektif Eğitimleri Derneği (UÖDED) Başkanı Ümit Hakan Karakaya'ya takdim edilmiştir. Tören, Kanal 24 ve TV8 başta olmak üzere ulusal televizyon kanallarında ve yazılı basında geniş yer bulmuştur.",
            "2005 yılından bu yana Türkiye ve dünya genelinde binlerce bireysel ve kurumsal dosyayı %100 ispat, delil ve müşteri memnuniyeti garantisiyle sonuçlandıran büromuz; W.A.D. (World Association of Detectives), IKD ve TÜRAVAK eğitim standartlarıyla sektöre öncülük etmeye devam etmektedir."
        ],
        highlights: [
            "Ekonomize Dergisi & Ankara Sesi Gazetesi 'Yılın Başarılı Araştırma Takip Firması' Ödülü",
            "Uluslararası Özel Dedektif Eğitimleri Derneği (UÖDED) Kurucu Liderliği",
            "İstanbul, Ankara, Podgorica (Karadağ) ve Las Vegas (ABD) Merkezli Uluslararası Operasyon Ağı"
        ]
    },
    'es-takibi-rehberi': {
        badge: "EŞ TAKİBİ REHBERİ • TMK m.161 & HMK m.199",
        title: "Eşinden Şüpheleniyor İsen Takip Et! Aldatma Belirtileri ve Hukuki Delil Toplama",
        meta: "AİLE HUKUKU & DELİL STANDARDI • SERTİFİKALI UZMAN REHBERİ",
        serviceKey: "es-takibi",
        paragraphs: [
            "Evlilik birliğinde sadakat yükümlülüğü Türk Medeni Kanunu'nun 185. maddesiyle güvence altına alınmış olup, zina (aldatma) TMK m.161 kapsamında mutlak ve özel boşanma sebebidir. Ancak mahkemede haklılığınızı kanıtlayabilmeniz için şüphe tek başına yeterli değildir; iddianın Hukuk Muhakemeleri Kanunu (HMK m.199) çerçevesinde hukuka uygun delillerle ispatlanması şarttır.",
            "Eşinizin telefonunu şifreleyip sürekli ters çevirmesi, mesai ve iş seyahati bahanelerinin artması, açıklanamayan harcamalar, giyim ve kişisel bakım alışkanlıklarında ani değişimler ve duygusal uzaklaşma en sık karşılaşılan sadakatsizlik belirtileridir. Bu aşamada öfkeyle hareket etmek veya amatörce takip yapmaya çalışmak, karşı tarafın durumu fark edip tüm delilleri karartmasına yol açar.",
            "DAT Özel Dedektiflik olarak 48 saatlik hızlı sadakat analizinden 5-7 iş günlük kapsamlı saha gözlemine kadar; hedef şahıs takip edildiğini kesinlikle hissetmeden kamuya açık alanlarda yüksek çözünürlüklü (4K) zaman damgalı fotoğraf, video ve kronolojik saha raporu hazırlıyoruz. Elde edilen tüm kanıtlar Aile Mahkemesi'nde velayet, nafaka ve maddi-manevi tazminat taleplerinizi doğrudan destekleyecek hukuki formatta teslim edilir."
        ],
        highlights: [
            "TMK m.161 (Zina) ve TMK m.166 kapsamında mahkemede geçerli somut kanıt üretimi",
            "Hedef şahsa kesinlikle fark ettirilmeden yürütülen profesyonel saha gözlemi",
            "4K zaman damgalı görsel materyal ve kronolojik adli rapor teslimi"
        ]
    },
    'nisanli-arastirmasi': {
        badge: "EVLİLİK ÖNCESİ • ÖNLEYİCİ TAHKİKAT",
        title: "Nişanlı Araştırması: Nişanlımın Geçmişini Öğrenmek İstiyorum Diyenler İçin Rehber",
        meta: "ÖNLEYİCİ ARAŞTIRMA • %100 GİZLİLİK PRENSİBİ",
        serviceKey: "evlilik-oncesi",
        paragraphs: [
            "Evlilik, hayatınız boyunca vereceğiniz en önemli duygusal ve hukuki karardır. Günümüzde pek çok kişi, evlilik birliği kurulduktan sonra eşinin gizlediği ağır borç yükümlülükleri, icra dosyaları, geçmişteki resmi/gayriresmi birliktelikleri, kumar veya madde bağımlılığı gibi kritik gerçeklerle yüzleşmektedir.",
            "Evlilik öncesi nişanlı araştırması bir güvensizlik göstergesi değil; geleceğinizi, ailenizi ve maddi-manevi varlığınızı koruma altına alan akılcı bir önleyici tahkikattır. Araştırma süreci karşı tarafın veya ailesinin kesinlikle haberi olmadan, %100 gizlilik protokolü altında yürütülür.",
            "Uzman ekibimiz tarafından 3 ila 6 iş günü içerisinde müstakbel eşinizin gerçek kimlik ve özgeçmiş bilgileri, eğitim ve mesleki doğruluğu, ticari itibarı ve borç/icra durumu, sosyal çevresi, alışkanlıkları ve aile yapısı detaylı biçimde incelenerek size özel gizli rapor halinde sunulur."
        ],
        highlights: [
            "Müstakbel eşin mali durumu, borç, icra ve ticari geçmiş doğrulaması",
            "Sosyal çevre, alışkanlıklar, sadakat eğilimi ve gerçek aile yapısı analizi",
            "Karşı taraf kesinlikle fark etmeden 3 – 6 iş gününde gizli rapor teslimi"
        ]
    },
    'ogrenci-takibi-rehberi': {
        badge: "ÖĞRENCİ & AİLE KORUMA • EBEVEYN REHBERİ",
        title: "Uyuşturucu Kullanan Çocuklar Nasıl Anlaşılır? Öğrenci ve Genç Takibi",
        meta: "GENÇLİK & AİLE KORUMA BİRİMİ • PEDAGOJİK GÖZLEM",
        serviceKey: "ogrenci-takibi",
        paragraphs: [
            "Gençlerin özellikle lise ve üniversite yıllarında ailesinden uzakta veya yeni sosyal çevrelerde zararlı alışkanlıklara, madde bağımlılığına ya da suça sürüklenen gruplara dahil olma riski her geçen gün artmaktadır. Erken farkındalık, evladınızın geleceğini kurtaran en kritik adımdır.",
            "Okul başarısında ani düşüş, ders devamsızlıkları, eski arkadaş çevresinden tamamen kopup ailesiyle tanıştırmadığı yeni kişilerle vakit geçirme, ani öfke patlamaları veya içe kapanma, göz kızarıklığı, uyku düzeninin bozulması ve sürekli artan para ihtiyacı ebeveynlerin dikkat etmesi gereken başlıca uyarı işaretleridir.",
            "DAT Özel Dedektiflik Öğrenci Takibi birimi; çocuğunuzun üzerinde baskı oluşturmadan ve takip edildiğini kesinlikle hissettirmeden okul giriş-çıkış saatlerini, gittiği mekanları, görüştüğü arkadaş grubunu ve olası zararlı alışkanlık temaslarını fotoğraflı ve saatli olarak gözlemler. Böylece ebeveynler söylentilere değil, somut gerçeklere dayanarak doğru zamanda koruyucu önlem alabilir."
        ],
        highlights: [
            "Okul dışı saatlerde gidilen mekanların ve arkadaş çevresinin gizli gözlemi",
            "Madde kullanımı, kumar veya tehlikeli gruplarla temas riskinin erken tespiti",
            "Öğrenciye kesinlikle fark ettirilmeden, psikolojisini koruyarak yapılan ebeveyn raporlaması"
        ]
    }
};

let currentArticleService = 'es-takibi';
let currentArticleKey = null;

function openArticleModal(articleKey) {
    const baseData = ARTICLES_DATA[articleKey];
    if (!baseData) return;
    currentArticleKey = articleKey;
    const data = _getDyn('articles', articleKey, baseData);
    currentArticleService = baseData.serviceKey || 'es-takibi';

    const modal = document.getElementById('articleModal');
    const badgeEl = document.getElementById('articleModalBadge');
    const titleEl = document.getElementById('articleModalTitle');
    const metaEl = document.getElementById('articleModalMeta');
    const bodyEl = document.getElementById('articleModalBody');
    const highlightsEl = document.getElementById('articleModalHighlights');

    if (badgeEl) badgeEl.textContent = data.badge;
    if (titleEl) titleEl.textContent = data.title;
    if (metaEl) metaEl.textContent = data.meta;

    if (bodyEl) {
        bodyEl.innerHTML = data.paragraphs.map(p => `<p class="text-xs sm:text-sm text-[#3A3E42] leading-relaxed font-regular">${p}</p>`).join('');
    }

    if (highlightsEl) {
        highlightsEl.innerHTML = data.highlights.map(h => `
            <li class="flex items-start gap-2 text-xs text-[#111111] font-medium">
                <span class="text-[#16A34A] font-bold mt-0.5">✓</span>
                <span>${h}</span>
            </li>
        `).join('');
    }

    if (modal) {
        modal.classList.remove('hidden');
    }
}

function closeArticleModal() {
    const modal = document.getElementById('articleModal');
    if (modal) {
        modal.classList.add('hidden');
    }
}

function applyArticleService() {
    closeArticleModal();
    prefillService(currentArticleService);
}

// 9. Privacy Policy & KVKK Modal
function openPrivacyModal() {
    const modal = document.getElementById('privacyModal');
    if (modal) {
        modal.classList.remove('hidden');
    }
}

function closePrivacyModal() {
    const modal = document.getElementById('privacyModal');
    if (modal) {
        modal.classList.add('hidden');
    }
}

// 9.5. 12 Official Services Process & Legal Scope Modal
const SERVICES_DATA = {
    'es-takibi': {
        badge: '01 • AİLE & SADAKAT ARAŞTIRMASI',
        title: 'Eş Takibi & Sadakat Araştırması',
        law: 'HUKUKİ DAYANAK: TMK m.161 & HMK m.199',
        duration: '2 – 7 İş Günü (48 Saat Hızlı Protokol)',
        region: '81 İl & Uluslararası Saha',
        paragraphs: [
            'Evlilik birliği içerisinde sadakat yükümlülüğünün ihlal edilip edilmediğini tespit etmek amacıyla, hedef şahıs kesinlikle fark etmeden kamuya açık alanlarda yürütülen profesyonel saha gözlem hizmetimizdir.',
            'Yargıtay 2. Hukuk Dairesi içtihatlarına ve TCK m.134 özel hayatın gizliliği sınırlarına tam riayet edilerek elde edilen deliller, boşanma, maddi-manevi tazminat ve kusur ispatı süreçlerinde mahkemeye sunulmaya hazır formatta teslim edilir.'
        ],
        deliverables: [
            '4K çözünürlüklü, tarih ve saat damgalı fotoğraf ve video kayıtları',
            'Günlük ve saatlik kronolojik saha hareket ve görüşme raporu',
            'HMK m.199 kapsamında avukatınızın dava dilekçesine ekleyebileceği resmi delil dosyası'
        ]
    },
    'evlilik-oncesi': {
        badge: '02 • ÖNLEYİCİ BİREYSEL TAHKİKAT',
        title: 'Evlilik Öncesi & Nişanlı Araştırması',
        law: 'HUKUKİ DAYANAK: KVKK & ÖNLEYİCİ TAHKİKAT PROTOKOLÜ',
        duration: '3 – 5 İş Günü',
        region: 'Türkiye Geneli & Yurt Dışı',
        paragraphs: [
            'Hayatınızı birleştirmeyi planladığınız kişinin beyan ettiği kimlik, meslek, eğitim, aile yapısı, finansal durum ve geçmiş yaşam tarzının gerçeklerle örtüşüp örtüşmediğini gizlilikle araştırıyoruz.',
            'Evlilik sonrasında telafisi güç maddi ve manevi mağduriyetlerin önüne geçmek için şahsın sosyal çevresi, alışkanlıkları ve ticari/adli geçmişi somut verilerle raporlanır.'
        ],
        deliverables: [
            'Sosyal çevre, yaşam tarzı ve alışkanlık doğrulama raporu',
            'Mesleki, ticari ve finansal beyan tutarlılık analizi',
            '%100 gizlilik taahhütlü müvekkil özel bilgilendirme dosyası'
        ]
    },
    'velayet-bosanma': {
        badge: '03 • AİLE HUKUKU & VELAYET DELİLİ',
        title: 'Velayet ve Boşanma Davaları Delil Araştırması',
        law: 'HUKUKİ DAYANAK: TMK m.182 & HMK m.199',
        duration: '5 – 10 İş Günü',
        region: '81 İl Merkez & İlçeler',
        paragraphs: [
            'Velayet davalarında Aile Mahkemesi hakiminin temel kriteri "çocuğun üstün menfaati"dir. Çocuğun mevcut velayet altındaki yaşam koşulları, eğitimi, güvenliği ve ebeveynin çocuğa karşı sorumluluklarını yerine getirip getirmediği saha gözlemiyle belgelenir.',
            'Ayrıca nafaka ve mal paylaşımı davalarında karşı tarafın gerçek gelir düzeyi ve yaşam standardı hukuka uygun delillerle tespit edilir.'
        ],
        deliverables: [
            'Çocuğun bakım, eğitim ve sosyal ortam güvenliği gözlem raporu',
            'Velayet sahibi ebeveynin yaşam tarzı ve ihmal tespiti fotoğrafları',
            'Nafaka uyarlama/artırım davaları için fiili gelir ve yaşam standardı delilleri'
        ]
    },
    'ogrenci-takibi': {
        badge: '04 • EBEVEYN & GENÇ KORUMA',
        title: 'Öğrenci & Çocuk Takibi',
        law: 'HUKUKİ DAYANAK: VELAYET HAKKI & AİLE KORUMA PROTOKOLÜ',
        duration: '3 – 7 Günlük Periyodik Gözlem',
        region: 'Tüm Üniversite ve Okul Şehirleri',
        paragraphs: [
            'Farklı bir şehirde üniversite okuyan veya ergenlik dönemindeki çocuğunuzun okul dışı zamanlarını nerede ve kimlerle geçirdiğini, zararlı alışkanlık veya riskli arkadaş çevresi altında olup olmadığını pedagojik hassasiyetle gözlemliyoruz.',
            'Çocuğunuz takip edildiğini kesinlikle hissetmeden, güvenliğini tehdit eden unsurlar ebeveyne detaylı olarak raporlanır.'
        ],
        deliverables: [
            'Okul/yurt giriş-çıkış saatleri ve günlük rutin çizelgesi',
            'Arkadaş çevresi ve vakit geçirilen mekanların güvenlik analizi',
            'Ebeveyne özel gizli görsel ve yazılı bilgilendirme raporu'
        ]
    },
    'adres-tespiti': {
        badge: '05 • KONUM & KAYIP ŞAHIS İSTİHBARATI',
        title: 'Adres Tespiti & Kayıp Kişi Araştırması',
        law: 'HUKUKİ DAYANAK: TEBLİGAT KANUNU & HUKUKİ MENFAAT',
        duration: '2 – 5 İş Günü',
        region: '81 İl, Kıbrıs, Karadağ & ABD',
        paragraphs: [
            'Resmi MERNİS adresinde bulunmayan, mahkeme veya icra tebligatlarından kaçan şahısların fiili olarak ikamet ettikleri konut ve işyeri adreslerini saha araştırmasıyla tespit ediyoruz.',
            'Uzun süredir haber alınamayan kayıp yakınların veya miras/alacak davası muhataplarının güncel konumları fotoğraflı olarak doğrulanır.'
        ],
        deliverables: [
            'Şahsın fiilen kullandığı güncel konut ve işyeri açık adresi',
            'Adreste bulunduğunu kanıtlayan tarih/saat damgalı saha fotoğrafları',
            'Hukuki tebligat ve icra işlemlerine uygun konum doğrulama tutanağı'
        ]
    },
    'borclu-takibi': {
        badge: '06 • İCRA & MAL VARLIĞI ARAŞTIRMASI',
        title: 'Borçlu Takibi & Mal Varlığı Tespiti',
        law: 'HUKUKİ DAYANAK: İİK m.277 (Tasarrufun İptali)',
        duration: '4 – 8 İş Günü',
        region: 'Türkiye Geneli & Yurt Dışı Bürolar',
        paragraphs: [
            'Borcunu ödememek için mal varlığını yakınları veya paravan şirketler üzerine devreden (muvazaalı işlem yapan) borçluların fiili ticari faaliyetleri, kullandıkları araçlar ve gayrimenkuller tespit edilir.',
            'İcra İflas Kanunu m.277 kapsamında açılacak "Tasarrufun İptali" davaları için borçlunun mal kaçırma organizasyonu somut saha delilleriyle deşifre edilir.'
        ],
        deliverables: [
            'Borçlunun fiilen kullandığı taşınır/taşınmaz varlık ve araç tespiti',
            'Üçüncü şahıslar üzerinden yürütülen gizli ticari faaliyet ve işyeri kanıtları',
            'İcra vekilinizin haciz ve dava sürecinde kullanabileceği istihbarat dosyası'
        ]
    },
    'dolandiricilik-davalari': {
        badge: '07 • CEZA HUKUKU & TAHKİKAT',
        title: 'Dolandırıcılık Davaları Araştırması',
        law: 'HUKUKİ DAYANAK: TCK m.157 – m.158 & CMK DELİL PROTOKOLÜ',
        duration: '5 – 12 İş Günü',
        region: 'Ulusal & Uluslararası Operasyon Ağı',
        paragraphs: [
            'Ticari veya bireysel nitelikli dolandırıcılık vakalarında sahte kimlik kullanan, izini kaybettiren faillerin gerçek kimlik ve adres bilgilerinin tespiti ile suç organizasyonunun aydınlatılmasını sağlıyoruz.',
            'Cumhuriyet Başsavcılığına yapılacak suç duyuruları ve ceza davaları için olayın oluş şeklini ve failler arasındaki bağlantıyı kanıtlayan delil dosyası hazırlanır.'
        ],
        deliverables: [
            'Fail veya organizasyon üyelerinin gerçek kimlik ve fiili konum tespiti',
            'Mağduriyeti kanıtlayan fiziki ve dijital iz sürüm raporu',
            'Savcılık suç duyurusuna eklenmeye hazır kronolojik delil klasörü'
        ]
    },
    'hirsizlik-arastirma': {
        badge: '08 • KURUMSAL & KONUT GÜVENLİĞİ',
        title: 'Hırsızlık & Suistimal Araştırması',
        law: 'HUKUKİ DAYANAK: TCK m.141 – m.142 & İÇ DENETİM',
        duration: '3 – 10 İş Günü',
        region: 'Fabrika, Depo, Ofis & Konut Sahaları',
        paragraphs: [
            'Fabrika, depo, mağaza, ofis veya konutlarda yaşanan faili meçhul hırsızlık vakaları ile personel kaynaklı stok/nakit kayıplarını teknik inceleme ve saha takibiyle aydınlatıyoruz.',
            'Çalınan emtianın çıktığı güzergah, alıcı noktalar ve içerideki işbirlikçiler gizli saha çalışmasıyla tespit edilerek adli mercilere sunulacak şekilde raporlanır.'
        ],
        deliverables: [
            'Olay yeri, kamera kör noktaları ve lojistik açıkların teknik analizi',
            'Şüpheli personel veya dış bağlantıların saha takip bulguları',
            'Çalıntı malzeme/emtia akış şeması ve resmi tahkikat raporu'
        ]
    },
    'kurumsal-teftis': {
        badge: '09 • TİCARİ İSTİHBARAT & DUE DILIGENCE',
        title: 'Firma Araştırma & Personel İstihbaratı',
        law: 'HUKUKİ DAYANAK: TTK HAKSIZ REKABET & KURUMSAL DENETİM',
        duration: '4 – 7 İş Günü',
        region: 'Türkiye, Karadağ (WPYB Global) & ABD',
        paragraphs: [
            'Yüksek meblağlı ticari anlaşma, ortaklık veya satın alma öncesinde muhatap şirketin gerçek mali gücü, piyasa itibarı, gizli ortaklık yapısı ve icra/dava yükü saha istihbaratıyla doğrulanır.',
            'Ayrıca üst düzey yöneticilerin ve kritik pozisyondaki personelin rakip firmalarla çıkar çatışması veya şirket içi suistimal riski gizlilikle incelenir.'
        ],
        deliverables: [
            'Şirket fiziki kapasite, depo/üretim ve ticari itibar doğrulama raporu',
            'Kilit personel geçmiş doğrulaması ve sadakat/rekabet analizi',
            'Yönetim kuruluna özel stratejik risk değerlendirme dosyası'
        ]
    },
    'marka-taklidi': {
        badge: '10 • WPYB GLOBAL MARKA KORUMA',
        title: 'Marka Taklidi & Sahte Ürün Araştırması',
        law: 'HUKUKİ DAYANAK: 6769 SAYILI SINAİ MÜLKİYET KANUNU (SMK m.29)',
        duration: '5 – 14 İş Günü',
        region: '81 İl & Balkanlar / Avrupa Dağıtım Ağı',
        paragraphs: [
            'Tescilli markanızı veya patentli ürünlerinizi taklit ederek haksız kazanç sağlayan merdiven altı üretim tesislerini, gizli depoları ve toptan dağıtım kanallarını deşifre ediyoruz.',
            'Şirket avukatlarınızın savcılık arama ve el koyma (baskın) kararı alabilmesi için gereken numune alımı, adres koordinatları ve sevkiyat saatleri eksiksiz belgelenir.'
        ],
        deliverables: [
            'Sahte üretim atölyesi ve gizli depo açık adres/koordinat tespiti',
            'Sevkiyat araçları, dağıtım ağı ve numune satın alma kanıtları',
            'SMK m.29 kapsamında adli baskın ve toplatma kararına esas delil dosyası'
        ]
    },
    'bilisim-dolandiriciligi': {
        badge: '11 • SİBER İSTİHBARAT & ADLİ BİLİŞİM',
        title: 'Bilişim Dolandırıcılığı & Dijital İz Tespiti',
        law: 'HUKUKİ DAYANAK: TCK m.243 – m.244 & OSINT PROTOKOLÜ',
        duration: '2 – 6 İş Günü',
        region: 'Ulusal & Uluslararası Dijital İnceleme',
        paragraphs: [
            'Sosyal medya ve dijital platformlar üzerinden gerçekleştirilen şantaj, itibar suikastı, sahte hesaplarla taciz ve bilişim dolandırıcılığı vakalarında açık kaynak istihbaratı (OSINT) ve dijital iz analizi yürütüyoruz.',
            'Dijital delillerin kaybolmadan SHA-256 bütünlük özetiyle kayıt altına alınması ve savcılık bilişim suçları bürosuna sunulacak teknik raporun hazırlanması sağlanır.'
        ],
        deliverables: [
            'Sahte profil, IP/domain bağlantıları ve açık kaynak (OSINT) korelasyon raporu',
            'Dijital ekran görüntüleri, iletişim logları ve zaman damgalı teknik tutanak',
            'Bilişim suçları savcılık başvurusuna uyumlu teknik inceleme dosyası'
        ]
    },
    'bocek-tarama': {
        badge: '12 • TSCM TEKNİK KARŞI-CASUSLUK',
        title: 'İzleme, Raporlama & Böcek Taraması (TSCM)',
        law: 'HUKUKİ DAYANAK: TCK m.132 – m.134 (Haberleşme & Özel Hayat)',
        duration: 'Aynı Gün (2 – 6 Saatlik TSCM Operasyonu)',
        region: 'Konut, Makam Odası, Toplantı Salonu & VIP Araç',
        paragraphs: [
            'Yönetim kurulu odaları, makam odaları, konutlar ve VIP araçlarda yasa dışı dinleme cihazları (RF/GSM böcekler), gizli kameralar (pinhole/Wi-Fi) ve GPS araç takip cihazları profesyonel spektrum analizörleri ve termal/optik dedektörlerle taranır.',
            'Tespit edilen cihazlar delil bütünlüğü bozulmadan fotoğraflanarak tutanak altına alınır ve mekanınız %100 güvenli hale getirilir.'
        ],
        deliverables: [
            'RF frekans spektrum taraması, optik lens ve termal anomali kontrolü',
            'Araç altı ve OBD/elektrik hattı GPS takip cihazı söküm ve tespit tutanağı',
            'Savcılık suç duyurusuna esas TSCM Teknik Temizlik ve Ekspertiz Raporu'
        ]
    }
};

let currentSelectedServiceKey = 'es-takibi';

function openServiceModal(serviceKey) {
    const baseData = SERVICES_DATA[serviceKey];
    if (!baseData) return;
    const data = _getDyn('services', serviceKey, baseData);
    currentSelectedServiceKey = serviceKey;

    const modal = document.getElementById('serviceDetailModal');
    const badgeEl = document.getElementById('serviceModalBadge');
    const titleEl = document.getElementById('serviceModalTitle');
    const lawEl = document.getElementById('serviceModalLaw');
    const durationEl = document.getElementById('serviceModalDuration');
    const regionEl = document.getElementById('serviceModalRegion');
    const summaryEl = document.getElementById('serviceModalSummary');
    const deliverablesEl = document.getElementById('serviceModalDeliverables');

    if (badgeEl) badgeEl.textContent = data.badge;
    if (titleEl) titleEl.textContent = data.title;
    if (lawEl) lawEl.textContent = data.law;
    if (durationEl) durationEl.textContent = data.duration;
    if (regionEl) regionEl.textContent = data.region;

    if (summaryEl) {
        summaryEl.innerHTML = data.paragraphs.map(p => `<p>${p}</p>`).join('');
    }

    if (deliverablesEl) {
        deliverablesEl.innerHTML = data.deliverables.map(d => `
            <li class="flex items-start gap-2 text-xs text-[#111111] font-medium">
                <span class="text-[#16A34A] font-bold mt-0.5">✓</span>
                <span>${d}</span>
            </li>
        `).join('');
    }

    if (modal) {
        modal.classList.remove('hidden');
    }
}

function closeServiceModal() {
    const modal = document.getElementById('serviceDetailModal');
    if (modal) {
        modal.classList.add('hidden');
    }
}

function applySelectedService() {
    closeServiceModal();
    prefillService(currentSelectedServiceKey);
}

// 10. FAQ Accordion
document.querySelectorAll('.faq-trigger').forEach(trigger => {
    trigger.addEventListener('click', () => {
        const item = trigger.closest('.faq-item');
        if (!item) return;

        const content = item.querySelector('.faq-content');
        const icon = item.querySelector('.faq-icon');
        const isHidden = content.classList.contains('hidden');
        
        document.querySelectorAll('.faq-item').forEach(otherItem => {
            otherItem.querySelector('.faq-content')?.classList.add('hidden');
            const otherIcon = otherItem.querySelector('.faq-icon');
            if (otherIcon) otherIcon.style.transform = 'rotate(0deg)';
        });
        
        if (isHidden) {
            content.classList.remove('hidden');
            if (icon) icon.style.transform = 'rotate(180deg)';
        } else {
            content.classList.add('hidden');
            if (icon) icon.style.transform = 'rotate(0deg)';
        }
    });
});

window.addEventListener('click', (e) => {
    const successModal = document.getElementById('successModal');
    if (e.target === successModal) {
        closeSuccessModal();
    }
    const popover = document.getElementById('liveVisitorPopover');
    const pill = document.getElementById('liveVisitorPill');
    if (popover && pill && !popover.classList.contains('hidden') && !popover.contains(e.target) && !pill.contains(e.target)) {
        popover.classList.add('hidden');
    }
});

// 11. 100% Real Active Visitor Counter (Server Presence API + Real Browser Tab Fallback — Zero Fake Numbers)
function toggleVisitorPopover() {
    const popover = document.getElementById('liveVisitorPopover');
    if (popover) {
        popover.classList.toggle('hidden');
    }
}

(function initLiveVisitorCounter() {
    const TABS_KEY = 'dat_real_tabs_v3';
    const VISITOR_KEY = 'dat_visitor_id_v3';
    const TAB_KEY = 'dat_tab_id_v3';
    const HEARTBEAT_MS = 5000;
    const STALE_MS = 15000;

    // 1. Stable, persistent Visitor ID across reloads and navigation (1 device/browser = 1 person)
    let visitorId = '';
    try {
        visitorId = localStorage.getItem(VISITOR_KEY);
        if (!visitorId || typeof visitorId !== 'string' || !visitorId.startsWith('vid_')) {
            visitorId = 'vid_' + Math.random().toString(36).slice(2, 10) + '_' + Date.now().toString(36);
            localStorage.setItem(VISITOR_KEY, visitorId);
        }
    } catch (_) {
        visitorId = 'vid_' + Math.random().toString(36).slice(2, 10);
    }

    // 2. Stable, persistent Tab ID across reloads (persists in sessionStorage of the same tab)
    let tabId = '';
    try {
        tabId = sessionStorage.getItem(TAB_KEY);
        if (!tabId || typeof tabId !== 'string' || !tabId.startsWith('tab_')) {
            tabId = 'tab_' + Math.random().toString(36).slice(2, 10) + '_' + Date.now().toString(36);
            sessionStorage.setItem(TAB_KEY, tabId);
        }
    } catch (_) {
        tabId = 'tab_' + Math.random().toString(36).slice(2, 10);
    }

    function updateDOM(count, sourceType) {
        const safeCount = Math.max(1, Number(count) || 1);
        document.querySelectorAll('[data-live-visitors]').forEach(el => {
            el.textContent = String(safeCount);
        });
        const srcEl = document.getElementById('liveVisitorSource');
        if (srcEl && sourceType) {
            window.__datLastPresenceMode = sourceType;
            srcEl.textContent = sourceType === 'server'
                ? _getUI('serverSource', 'Sunucu Doğrulamalı')
                : _getUI('localSource', 'Tarayıcı Oturumları');
        }
        try {
            localStorage.setItem('dat_last_visitor_count', String(safeCount));
        } catch (_) {}
    }

    function readRealLocalTabs() {
        const now = Date.now();
        let tabs = {};
        try {
            tabs = JSON.parse(localStorage.getItem(TABS_KEY) || '{}');
        } catch (_) {
            tabs = {};
        }
        const fresh = {};
        for (const [id, ts] of Object.entries(tabs)) {
            if (typeof ts === 'number' && (now - ts) < STALE_MS) {
                fresh[id] = ts;
            }
        }
        return fresh;
    }

    function writeLocalTab(removeSelf) {
        const fresh = readRealLocalTabs();
        if (removeSelf) {
            delete fresh[tabId];
        } else {
            // Overwrites the existing tabId entry with updated timestamp (never duplicates on reload!)
            fresh[tabId] = Date.now();
        }
        try {
            localStorage.setItem(TABS_KEY, JSON.stringify(fresh));
        } catch (_) {}
        return Object.keys(fresh).length;
    }

    let bc = null;
    try {
        if ('BroadcastChannel' in window) {
            bc = new BroadcastChannel('dat_real_presence_v3');
            bc.onmessage = () => pingPresence();
        }
    } catch (_) {}

    async function pingPresence() {
        const localCount = writeLocalTab(false);
        try {
            const res = await fetch('/api/presence', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    visitorId: visitorId,
                    sessionId: visitorId,
                    tabId: tabId
                }),
                cache: 'no-store'
            });
            if (res.ok) {
                const data = await res.json();
                if (typeof data.online === 'number') {
                    updateDOM(data.online, 'server');
                    return;
                }
            }
        } catch (_) {
            // Static file / serverless mode: strictly count real open browser tabs
        }
        updateDOM(localCount, 'local');
    }

    const handleLeave = () => {
        const remaining = writeLocalTab(true);
        // If this was the last open tab in this browser, notify the server
        if (remaining <= 0) {
            try {
                if (navigator.sendBeacon) {
                    const blob = new Blob([JSON.stringify({ visitorId: visitorId, sessionId: visitorId })], { type: 'application/json' });
                    navigator.sendBeacon('/api/presence/leave', blob);
                }
            } catch (_) {}
        }
        if (bc) bc.postMessage({ type: 'leave', tabId, remaining });
    };

    window.addEventListener('pagehide', handleLeave);
    window.addEventListener('beforeunload', handleLeave);
    window.addEventListener('storage', (e) => {
        if (e.key === TABS_KEY) {
            pingPresence();
        }
    });

    pingPresence();
    if (bc) bc.postMessage({ type: 'join', tabId });
    setInterval(pingPresence, HEARTBEAT_MS);
})();

// 12. DAT STORE — SpaceX-Shop Style Legal Security & Tracking Gear E-Commerce
const SHOP_PRODUCTS = {
    'DAT-GPS-01': {
        sku: 'DAT-GPS-01',
        category: 'GPS ARAÇ & FİLO TAKİP',
        title: 'DAT FLEET TRACKER X1 — GPS TAKİP CİHAZI',
        price: 4850,
        image: 'assets/shop/gps-tracker-pro.jpg',
        defaultVariant: 'Mat Siyah',
        desc: 'Kendi şahsi aracınız, şirket filonuz veya lojistik sevkiyatlarınız için geliştirilmiş, BTK IMEI kayıtlı, endüstriyel mıknatıslı ve USB-C şarjlı yasal GPS konum takip cihazı.',
        specs: [
            'BTK IMEI Kayıtlı & E-Devlet / Resmi Faturalı',
            '60 Gün Bekleme Süreli Yüksek Yoğunluklu Batarya',
            'iOS, Android ve Web Canlı Harita + Rota Geçmişi',
            'IP67 Toz & Su Dayanıklı Mıknatıslı Kasa'
        ]
    },
    'DAT-KID-05': {
        sku: 'DAT-KID-05',
        category: 'ÇOCUK & YAŞLI GÜVENLİĞİ GPS TAKİP',
        title: 'DAT KIDGUARD 4G — ÇOCUK TAKİP SAATİ',
        price: 3950,
        image: 'assets/shop/kid-safety-tracker.jpg',
        defaultVariant: 'Grafit Siyah',
        desc: 'Velayetinizdeki çocuğunuzun veya bakıma muhtaç büyüğünüzün güvenliği için ebeveyn kontrolü uygulamalı, tek tuş SOS acil çağrılı, güvenli bölge (Geo-Fence) uyarılı akıllı konum takip saati.',
        specs: [
            'Tek Tuş SOS Acil Arama & 4G Görüntülü Konuşma',
            'Okul/Ev Güvenli Bölge (Geo-Fence) Çıkış Alarmı',
            'BTK IMEI Kayıtlı, CE Sertifikalı & Ebeveyn Şifreli',
            'IP67 Suya Dayanıklı Alerji Yapmayan Silikon Kordon'
        ]
    },
    'DAT-AIR-04': {
        sku: 'DAT-AIR-04',
        category: 'AIRTAG & AKILLI EŞYA TAKİBİ',
        title: 'DAT SMART TAG — AIRTAG UYUMLU ETİKET',
        price: 1850,
        image: 'assets/shop/asset-beacon-tag.jpg',
        defaultVariant: 'Obsidyen Siyah',
        desc: 'Apple Find My (Bul) ve Android ağıyla tam uyumlu; valiz, evrak çantası, anahtarlık, motosiklet ve evcil dostlarınızı küresel ağ üzerinden anlık takip etmenizi sağlayan konum etiketi.',
        specs: [
            'Apple Bul (AirTag Ağı) & Android Doğrudan Eşleşme',
            'IP68 Tam Su Geçirmez Polymer & Titanyum Karabin',
            '12 Ay Değiştirilebilir Uzun Ömürlü Pil',
            'Unutma / Ayrılma Anında Anlık Telefon Bildirimi'
        ]
    },
    'DAT-REC-06': {
        sku: 'DAT-REC-06',
        category: 'ŞİFRELİ SES KAYIT DONANIMI',
        title: 'DAT VOICE VAULT S1 — SES KAYIT CİHAZI',
        price: 3450,
        image: 'assets/shop/voice-recorder-pro.jpg',
        defaultVariant: 'Space Black (64 GB)',
        desc: 'Kendi katıldığınız resmi iş toplantıları, konferanslar, akademik eğitimler ve sözlü mutabakat notlarınız için geliştirilmiş, donanım PIN şifreli PCM ses kayıt cihazı.',
        specs: [
            'AES-256 PIN Kilidi & PCM Stereo HD Gürültü Engelleme',
            'Sese Duyarlı (VOX) Otomatik Kayıt & USB-C Veri Aktarımı',
            '50 Saate Kadar Tek Şarjla Kesintisiz Çalışma',
            'Hukuka Uygun Resmi Toplantı & Ders Kaydı Kullanımı'
        ]
    },
    'DAT-SVC-TSCM': {
        sku: 'DAT-SVC-TSCM',
        category: 'PROFESYONEL BÖCEK ARAMA HİZMETİ (TSCM)',
        title: 'TSCM YERİNDE BÖCEK ARAMA HİZMETİ PAKETİ',
        price: 9500,
        image: 'assets/shop/tscm-service-kit.jpg',
        defaultVariant: 'Konut / Daire Taraması',
        desc: 'Sertifikalı DAT Teknik Takip ekibimizin konutunuza, ofisinize veya VIP aracınıza bizzat gelerek spektrum analizörü, termal kamera ve optik lens detektörüyle yaptığı yerinde böcek tarama hizmeti.',
        specs: [
            '10 kHz – 24 GHz Profesyonel Spektrum & Wi-Fi/GSM Analizi',
            'Priz, Mobilya, Araç Altı & Gizli Kamera Optik Taraması',
            'Termal Anomali ve Non-Linear Junction Detector Kontrolü',
            'Savcılık Deliline Uygun Resmi Ekspertiz & Temizlik Raporu'
        ]
    },
    'DAT-TSCM-02': {
        sku: 'DAT-TSCM-02',
        category: 'TSCM KARŞI-CASUSLUK GÜVENLİĞİ',
        title: 'DAT RF GUARD S3 — BÖCEK DEDEKTÖRÜ',
        price: 7900,
        image: 'assets/shop/tscm-rf-detector.jpg',
        defaultVariant: 'Obsidyen Siyah',
        desc: 'Kendi evinizde, ofisinizde veya seyahatte otel odalarında gizli kamera lenslerini ve aktif RF/Wi-Fi/GSM dinleme sinyallerini bizzat taramanız için taşınabilir güvenlik dedektörü.',
        specs: [
            '1 MHz – 8 GHz Geniş Bant RF Sinyal Spektrum Tarama',
            'Kızılötesi Lazer Vizör ile Pinhole Kamera Lensi Tespiti',
            'Titreşim ve Sessiz LED Uyarı Modu',
            'CE Sertifikalı & 2 Yıl DAT Resmi Garanti'
        ]
    },
    'DAT-CAM-07': {
        sku: 'DAT-CAM-07',
        category: 'SÜRÜŞ & KİŞİSEL GÜVENLİK KAMERASI',
        title: 'DAT CAM Q2 — SÜRÜŞ & GÜVENLİK KAMERASI',
        price: 5400,
        image: 'assets/shop/safety-dash-cam.jpg',
        defaultVariant: 'Mat Siyah (64 GB)',
        desc: 'Aracınızda trafik kazaları, park hali darbeleri veya saha personelinizin yaka güvenliği için zaman damgalı 4K UHD görüntü ve G-sensör kilitleme özellikli güvenlik kamerası.',
        specs: [
            '4K UHD Sony Starvis Gece Görüş Sensörü (160° Açı)',
            'Dahili GPS Koordinat & Tarih/Saat Filigranı (HMK Uyumlu)',
            'Park Modu Hareket Algılama & Otomatik Darbe Kilidi',
            'Mobil Wi-Fi Üzerinden Anında Video İndirme'
        ]
    },
    'DAT-SHIELD-03': {
        sku: 'DAT-SHIELD-03',
        category: 'VERİ & SİNYAL KALKANLAMA',
        title: 'DAT FARADAY SHIELD — SİNYAL KILIFI',
        price: 1650,
        image: 'assets/shop/faraday-shield-pouch.jpg',
        defaultVariant: 'Karbon & Turuncu',
        desc: 'Anahtarsız araç hırsızlığını (Keyless Go röle saldırısı), uzaktan kredi kartı RFID/NFC kopyalamasını ve gizli toplantılarda telefon sinyallerini izole eden askeri standart kılıf.',
        specs: [
            '90 dB Zayıflatma (Wi-Fi, Bluetooth, GPS, 5G/LTE, NFC Tam Blokaj)',
            'Çift Katmanlı Nano-Nikel Bakır Dokuma + Balistik Dış Kumaş',
            'Tüm Akıllı Telefonlar & Araç Anahtarları ile Uyumlu',
            'Özel Manyetik Hızlı Mühürlü Kapak'
        ]
    }
};

const selectedProductVariants = {
    'DAT-GPS-01': 'Mat Siyah',
    'DAT-KID-05': 'Grafit Siyah',
    'DAT-AIR-04': 'Obsidyen Siyah',
    'DAT-REC-06': 'Space Black (64 GB)',
    'DAT-SVC-TSCM': 'Konut / Daire Taraması',
    'DAT-TSCM-02': 'Obsidyen Siyah',
    'DAT-CAM-07': 'Mat Siyah (64 GB)',
    'DAT-SHIELD-03': 'Karbon & Turuncu'
};

let shopCart = [];
try {
    shopCart = JSON.parse(localStorage.getItem('dat_shop_cart_v1') || '[]');
} catch (_) {
    shopCart = [];
}

let activeModalProductSku = null;

function formatTL(num) {
    return '₺' + Number(num || 0).toLocaleString('tr-TR');
}

function filterShop(cat) {
    document.querySelectorAll('.shop-filter-btn').forEach(btn => {
        if (btn.getAttribute('data-shop-filter') === cat) {
            btn.className = 'shop-filter-btn px-3.5 py-1.5 rounded-full bg-[#111111] text-[#93F051] font-medium transition';
        } else {
            btn.className = 'shop-filter-btn px-3.5 py-1.5 rounded-full text-[#3A3E42] hover:text-[#111111] font-regular transition';
        }
    });
    document.querySelectorAll('.shop-card').forEach(card => {
        const c = card.getAttribute('data-shop-cat');
        if (cat === 'all' || c === cat) {
            card.classList.remove('hidden');
        } else {
            card.classList.add('hidden');
        }
    });
}

function selectSwatch(sku, variantName, btnEl) {
    selectedProductVariants[sku] = variantName;
    const group = btnEl?.parentElement;
    if (group) {
        group.querySelectorAll('.swatch-btn').forEach(b => {
            b.classList.remove('ring-2', 'ring-[#111111]', 'ring-offset-1');
            b.classList.add('border', 'border-black/15');
        });
        btnEl.classList.remove('border', 'border-black/15');
        btnEl.classList.add('ring-2', 'ring-[#111111]', 'ring-offset-1');
    }
}

function saveCart() {
    try {
        localStorage.setItem('dat_shop_cart_v1', JSON.stringify(shopCart));
    } catch (_) {}
    renderCart();
}

function addToCart(sku, openDrawerAfter = true) {
    const product = SHOP_PRODUCTS[sku];
    if (!product) return;
    const variant = selectedProductVariants[sku] || product.defaultVariant;
    const existing = shopCart.find(item => item.sku === sku && item.variant === variant);
    if (existing) {
        existing.qty += 1;
    } else {
        shopCart.push({
            sku: product.sku,
            title: product.title,
            price: product.price,
            image: product.image,
            variant,
            qty: 1
        });
    }
    saveCart();
    if (openDrawerAfter) {
        openCartDrawer();
    }
}

function updateCartQty(index, delta) {
    if (!shopCart[index]) return;
    shopCart[index].qty += delta;
    if (shopCart[index].qty <= 0) {
        shopCart.splice(index, 1);
    }
    saveCart();
}

function removeCartItem(index) {
    shopCart.splice(index, 1);
    saveCart();
}

function renderCart() {
    const totalItems = shopCart.reduce((sum, item) => sum + item.qty, 0);
    const totalAmount = shopCart.reduce((sum, item) => sum + (item.price * item.qty), 0);

    const headerBadge = document.getElementById('cartCountBadge');
    const storeBadge = document.getElementById('storeSectionCartCount');
    const mobileTabBadge = document.getElementById('mobileTabCartBadge');
    const totalPriceEl = document.getElementById('cartTotalPrice');
    const container = document.getElementById('cartItemsContainer');

    if (headerBadge) headerBadge.textContent = String(totalItems);
    if (storeBadge) storeBadge.textContent = String(totalItems);
    if (mobileTabBadge) {
        mobileTabBadge.textContent = String(totalItems);
        mobileTabBadge.classList.toggle('hidden', totalItems <= 0);
    }
    if (totalPriceEl) totalPriceEl.textContent = formatTL(totalAmount);

    if (!container) return;

    if (shopCart.length === 0) {
        container.innerHTML = `
            <div class="h-full flex flex-col items-center justify-center text-center py-12 space-y-3 text-[#3A3E42]/70">
                <div class="w-12 h-12 rounded-full bg-[#111111] flex items-center justify-center text-[#93F051]">
                    <i class="hgi hgi-stroke hgi-shopping-bag-02 w-5 h-5"></i>
                </div>
                <div class="text-xs font-medium text-[#111111]">${_getUI('cartEmptyTitle', 'Sepetiniz Şu An Boş')}</div>
                <p class="text-[11px] max-w-xs">${_getUI('cartEmptyDesc', 'Yasal GPS araç/varlık takip cihazları ve TSCM güvenlik ekipmanlarını inceleyip sepete ekleyebilirsiniz.')}</p>
            </div>
        `;
        return;
    }

    container.innerHTML = shopCart.map((item, idx) => {
        const localizedProd = _getDyn('shop', item.sku, SHOP_PRODUCTS[item.sku] || item);
        const localizedVar = (localizedProd.variants && localizedProd.variants[item.variant]) ? localizedProd.variants[item.variant] : item.variant;
        return `
        <div class="flex items-center gap-3 p-3 rounded-2xl bg-[#F2F2F2] border border-black/10">
            <img src="${_resolveAssetPath(item.image)}" alt="${localizedProd.title}" class="w-16 h-16 rounded-xl object-cover bg-[#FFFFFF] shrink-0">
            <div class="flex-1 min-w-0">
                <div class="text-xs font-medium text-[#111111] truncate">${localizedProd.title}</div>
                <div class="text-[10px] font-mono text-[#3A3E42]/70 mt-0.5">${localizedVar} • ${item.sku}</div>
                <div class="flex items-center justify-between mt-2">
                    <span class="text-xs font-mono font-medium text-[#111111]">${formatTL(item.price * item.qty)}</span>
                    <div class="inline-flex items-center gap-1.5 bg-[#FFFFFF] rounded-full px-2 py-0.5 border border-[rgba(0,0,0,0.08)]">
                        <button type="button" onclick="updateCartQty(${idx}, -1)" class="w-5 h-5 rounded-full hover:bg-[#F3F4F4] flex items-center justify-center text-[#000000]" aria-label="-">
                            <i class="hgi hgi-stroke hgi-minus-sign w-3 h-3"></i>
                        </button>
                        <span class="text-[11px] font-mono font-medium w-4 text-center">${item.qty}</span>
                        <button type="button" onclick="updateCartQty(${idx}, 1)" class="w-5 h-5 rounded-full hover:bg-[#F3F4F4] flex items-center justify-center text-[#000000]" aria-label="+">
                            <i class="hgi hgi-stroke hgi-plus-sign w-3 h-3"></i>
                        </button>
                    </div>
                </div>
            </div>
            <button type="button" onclick="removeCartItem(${idx})" class="p-1.5 rounded-full hover:bg-[#FFFFFF] text-[#3A3E42]/60 hover:text-[#DC2626] transition" aria-label="Delete">
                <i class="hgi hgi-stroke hgi-delete-02 w-4 h-4"></i>
            </button>
        </div>
    `;}).join('');
}

function openProductModal(sku) {
    const baseProduct = SHOP_PRODUCTS[sku];
    if (!baseProduct) return;
    const product = _getDyn('shop', sku, baseProduct);
    activeModalProductSku = sku;

    const modal = document.getElementById('productModal');
    const skuBadge = document.getElementById('pmSkuBadge');
    const imgEl = document.getElementById('pmImg');
    const catEl = document.getElementById('pmCategory');
    const titleEl = document.getElementById('pmTitle');
    const priceEl = document.getElementById('pmPrice');
    const descEl = document.getElementById('pmDesc');
    const specsEl = document.getElementById('pmSpecs');

    const rawVar = selectedProductVariants[sku] || baseProduct.defaultVariant;
    const dispVar = (product.variants && product.variants[rawVar]) ? product.variants[rawVar] : rawVar;

    if (skuBadge) skuBadge.textContent = `${baseProduct.sku} • ${dispVar}`;
    if (imgEl) imgEl.src = _resolveAssetPath(baseProduct.image);
    if (catEl) catEl.textContent = product.category;
    if (titleEl) titleEl.textContent = product.title;
    if (priceEl) priceEl.textContent = formatTL(baseProduct.price) + ' (' + _getUI('vatIncluded', 'KDV Dahil') + ')';
    if (descEl) descEl.textContent = product.desc;
    if (specsEl) {
        specsEl.innerHTML = product.specs.map(s => `
            <li class="flex items-start gap-2">
                <span class="text-[#16A34A] font-bold">✓</span>
                <span>${s}</span>
            </li>
        `).join('');
    }
    if (modal) modal.classList.remove('hidden');
}

function closeProductModal() {
    document.getElementById('productModal')?.classList.add('hidden');
}

function addFromProductModal() {
    if (activeModalProductSku) {
        closeProductModal();
        addToCart(activeModalProductSku, true);
    }
}

function openCartDrawer() {
    renderCart();
    document.getElementById('cartDrawer')?.classList.remove('hidden');
}

function closeCartDrawer() {
    document.getElementById('cartDrawer')?.classList.add('hidden');
}

let _lastOrderSubmitAt = 0;
async function submitShopOrder(e) {
    e.preventDefault();
    if (document.getElementById('orderHoney')?.value) {
        return; // Silent bot trap
    }
    const now = Date.now();
    if (now - _lastOrderSubmitAt < 15000) {
        alert(_getUI('rateLimitAlert', 'Lütfen tekrar göndermeden önce birkaç saniye bekleyiniz.'));
        return;
    }
    _lastOrderSubmitAt = now;
    if (shopCart.length === 0) {
        alert(_getUI('emptyCartAlert', 'Lütfen önce sepetinize en az bir ürün ekleyiniz.'));
        return;
    }

    const name = document.getElementById('orderClientName')?.value?.trim() || 'Belirtilmedi';
    const phone = document.getElementById('orderClientPhone')?.value?.trim() || 'Belirtilmedi';
    const address = document.getElementById('orderClientAddress')?.value?.trim() || 'Belirtilmedi';
    const orderCode = '#DAT-ORD-' + Math.floor(10000 + Math.random() * 90000);
    const totalAmount = shopCart.reduce((sum, item) => sum + (item.price * item.qty), 0);
    const itemsText = shopCart.map(i => `${i.qty}x ${i.title} (${i.variant}) — ${formatTL(i.price * i.qty)}`).join('\n');

    const btn = document.getElementById('shopOrderBtn');
    const orig = btn.innerHTML;
    btn.disabled = true;
    btn.innerHTML = `<span>${_getUI('sendingOrderBtn', 'Sipariş İletiliyor...')}</span>`;

    const payload = {
        _subject: `DAT Store Yeni Donanım Siparişi (${orderCode})`,
        _template: "table",
        _captcha: "false",
        name: name,
        message: `${itemsText} — Teslimat: ${address} (${formatTL(totalAmount)})`,
        Siparis_Kodu: orderCode,
        Musteri_Adi: name,
        Telefon: phone,
        Teslimat_Adresi: address,
        Urunler: itemsText,
        Toplam_Tutar: formatTL(totalAmount)
    };

    let orderDelivery = { ok: false, deliveredCount: 0, totalCount: FORM_RECIPIENT_ENDPOINTS.length, errors: [] };
    try {
        let leadTrackPromise = Promise.resolve(null);
        try {
            if (window.DATAnalytics && typeof window.DATAnalytics.trackLead === 'function') {
                leadTrackPromise = window.DATAnalytics.trackLead({
                    code: orderCode,
                    name: name,
                    contact: phone,
                    category: 'DAT Store Donanım Siparişi',
                    channel: 'DAT Store Sepeti',
                    urgency: 'high',
                    details: `${itemsText}\nAdres: ${address}\nToplam: ${formatTL(totalAmount)}`
                }) || Promise.resolve(null);
                window.DATAnalytics.trackEvent('form_submit', {
                    code: orderCode,
                    category: 'DAT Store Sipariş'
                });
            }
        } catch (_) {}

        try {
            orderDelivery = await _sendFormPayload(payload, 45000, leadTrackPromise);
        } catch (err) {
            orderDelivery.errors = [err?.message || 'Bağlantı hatası'];
        }

        const waMsg = encodeURIComponent(
            `DAT STORE SİPARİŞ TALEBİ (${orderCode})\n` +
            `Ad / Firma: ${name}\nTelefon: ${phone}\nAdres: ${address}\n\n` +
            `Ürünler:\n${itemsText}\n\nToplam (KDV Dahil): ${formatTL(totalAmount)}`
        );
        window.open(`https://wa.me/905326667749?text=${waMsg}`, '_blank', 'noopener,noreferrer');

        shopCart = [];
        saveCart();
        document.getElementById('cartOrderForm')?.reset();
        closeCartDrawer();

        const smTitle = document.getElementById('successModalTitle');
        const smDesc = document.getElementById('successModalDesc');
        const smLabel = document.getElementById('successCodeLabel');
        const codeElement = document.getElementById('caseTrackingCode');
        const waLink = document.getElementById('directWhatsappLink');
        const emailLink = document.getElementById('directEmailLink');

        if (smTitle) smTitle.textContent = _getUI('orderSentTitle', 'Donanım Siparişiniz Alındı');
        if (smDesc) smDesc.innerHTML = _getUI('orderSentDesc', 'Faturalı donanım sipariş talebiniz ekibimize iletildi. Kargo ve ödeme onayı için <strong>0532 666 77 49</strong> WhatsApp hattımızdan da anında teyit alabilirsiniz.');
        if (smLabel) smLabel.textContent = _getUI('orderCodeLabel', 'SİPARİŞ TAKİP KODUNUZ:');
        if (waLink) waLink.href = `https://wa.me/905326667749?text=${waMsg}`;
        if (emailLink) emailLink.href = `mailto:uhakankarakaya@gmail.com,umithakankarakaya@gmail.com?subject=${encodeURIComponent(`DAT Store Sipariş (${orderCode})`)}&body=${waMsg}`;
        if (codeElement) codeElement.textContent = orderCode;
        _renderDeliveryStatus(orderDelivery);
        document.getElementById('successModal')?.classList.remove('hidden');
    } finally {
        btn.disabled = false;
        btn.innerHTML = orig;
    }
}

// 12. Distance Sales, Return & Cookie Policy Modals + Minimal Cookie Banner
const LEGAL_DOCS_DATA = {
    sales: {
        badge: "RESMİ MEVZUAT & SATIŞ PROTOKOLÜ",
        title: "Mesafeli Satış, Teslimat ve İade Koşulları",
        paragraphs: [
            "<strong>1. Satıcı & Ürün Niteliği:</strong> DAT Store üzerinden sunulan tüm GPS takip cihazları, AirTag uyumlu akıllı etiketler, ses kayıt donanımları ve TSCM güvenlik tarama paketleri; DAT Group güvencesiyle resmi e-Fatura, CE ve (GPS/SIM ürünlerde) BTK IMEI kaydıyla teslim edilir.",
            "<strong>2. Yasal Kullanım Çerçevesi (TCK m.134):</strong> Satılan ürünler yalnızca alıcının kendi aracının/mülkünün güvenliği, velayeti altındaki çocuğun/bakıma muhtaç büyüğün korunması veya bizzat katıldığı toplantıların kayıt altına alınması amacıyla temin edilebilir.",
            "<strong>3. Aynı Gün Kargo & 14 Gün Cayma Hakkı:</strong> Saat 15:00'e kadar teyit edilen donanım siparişleri aynı iş günü sigortalı kargo ile ücretsiz sevk edilir. Kullanılmamış, ambalajı ve mührü bozulmamış fiziksel ürünlerde 6502 sayılı TKHK kapsamında teslimattan itibaren 14 gün içinde koşulsuz iade ve tüm cihazlarda 2 yıl resmi DAT garantisi geçerlidir."
        ]
    },
    cookie: {
        badge: "VERİ MAHREMİYETİ & ÇEREZ PROTOKOLÜ",
        title: "Çerez (Cookie) & Yerel Depolama Politikası",
        paragraphs: [
            "<strong>1. Üçüncü Taraf Reklam Çerezi Yoktur:</strong> Web sitemizde kişileri profilleyen pazarlama, yeniden hedefleme (retargeting) veya üçüncü taraf reklam çerezleri kesinlikle kullanılmaz.",
            "<strong>2. Zorunlu Teknik Oturum & Yerel Tercihler:</strong> Ziyaretçinin seçtiği dil tercihi (<code>dat_site_lang</code>), sepet ürünleri (<code>dat_shop_cart_v1</code>), çerez bilgilendirme onayı (<code>dat_cookie_ack</code>) ve IP/kimlik kaydı tutmayan anonim aktif ziyaretçi sayacı oturum kimliği yalnızca tarayıcı belleğinde tutulur.",
            "<strong>3. Tercih Kontrolü:</strong> Tarayıcı ayarlarınızdan yerel depolamayı istediğiniz zaman temizleyebilir; tüm gizlilik sorularınız için info@datdetective.com üzerinden bizimle iletişime geçebilirsiniz."
        ]
    }
};

let activeLegalModalType = 'sales';

function openLegalModal(docType) {
    const baseDoc = LEGAL_DOCS_DATA[docType || 'sales'];
    if (!baseDoc) return;
    activeLegalModalType = docType || 'sales';
    const doc = _getDyn('legalDocs', activeLegalModalType, baseDoc);
    const modal = document.getElementById('legalInfoModal');
    const badgeEl = document.getElementById('legalModalBadge');
    const titleEl = document.getElementById('legalModalTitle');
    const bodyEl = document.getElementById('legalModalBody');
    if (badgeEl) badgeEl.textContent = doc.badge;
    if (titleEl) titleEl.textContent = doc.title;
    if (bodyEl) {
        bodyEl.innerHTML = (doc.paragraphs || []).map(p => `<p>${p}</p>`).join('');
    }
    if (modal) modal.classList.remove('hidden');
}

function closeLegalModal() {
    document.getElementById('legalInfoModal')?.classList.add('hidden');
}

function ackCookieBanner() {
    try {
        localStorage.setItem('dat_cookie_ack', '1');
    } catch (_) {}
    document.getElementById('cookieBanner')?.classList.add('hidden');
    document.getElementById('mobileQuickPills')?.classList.remove('has-cookie-banner');
}

(function initCookieNotice() {
    try {
        if (!localStorage.getItem('dat_cookie_ack')) {
            const banner = document.getElementById('cookieBanner');
            if (banner) {
                setTimeout(() => {
                    banner.classList.remove('hidden');
                    document.getElementById('mobileQuickPills')?.classList.add('has-cookie-banner');
                }, 900);
            }
        }
    } catch (_) {}
})();

// Initial cart render
renderCart();

// ========================================================
// 12. DAT Executive Analytics & Interaction Tracking Engine
// ========================================================
const DATAnalytics = (function() {
    const EVENTS_KEY = 'dat_analytics_log_v2';
    const LEADS_KEY = 'dat_admin_leads_v2';
    const SESSION_KEY = 'dat_analytics_sid_v2';

    function getSessionId() {
        try {
            let sid = sessionStorage.getItem(SESSION_KEY);
            if (!sid) {
                sid = 'sid_' + Math.random().toString(36).substring(2, 9) + '_' + Date.now();
                sessionStorage.setItem(SESSION_KEY, sid);
            }
            return sid;
        } catch (_) {
            return 'sid_default_' + Date.now();
        }
    }

    function getDeviceType() {
        const ua = navigator.userAgent || '';
        if (/tablet|ipad|playbook|silk/i.test(ua)) return 'Tablet';
        if (/mobile|iphone|ipod|android|blackberry|iemobile|kindle/i.test(ua)) return 'Mobil';
        return 'Masaüstü';
    }

    function getReferrerSource() {
        const ref = document.referrer || '';
        if (!ref) return 'Doğrudan (Direct)';
        if (ref.includes('google.')) return 'Google Organik';
        if (ref.includes('instagram.')) return 'Instagram';
        if (ref.includes('facebook.')) return 'Facebook';
        if (ref.includes('whatsapp') || ref.includes('wa.me')) return 'WhatsApp';
        if (ref.includes('t.co') || ref.includes('twitter') || ref.includes('x.com')) return 'Twitter / X';
        return 'Diğer Web Siteleri';
    }

    function trackEvent(type, data) {
        const event = {
            id: 'ev_' + Date.now() + '_' + Math.random().toString(36).substring(2, 7),
            type: type || 'page_view',
            timestamp: Date.now(),
            dateStr: new Date().toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit', second: '2-digit' }),
            page: window.location.pathname || '/',
            title: document.title ? document.title.split('—')[0].trim() : 'Ana Sayfa',
            device: getDeviceType(),
            source: getReferrerSource(),
            sid: getSessionId(),
            ...(data || {})
        };

        // 1. Save to local log
        try {
            const raw = localStorage.getItem(EVENTS_KEY);
            const events = raw ? JSON.parse(raw) : [];
            events.unshift(event);
            if (events.length > 500) events.length = 500;
            localStorage.setItem(EVENTS_KEY, JSON.stringify(events));
        } catch (_) {}

        // 2. Transmit to serverless analytics endpoint
        try {
            const payload = JSON.stringify(event);
            if (navigator.sendBeacon) {
                navigator.sendBeacon('/api/analytics', payload);
            } else {
                fetch('/api/analytics', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: payload,
                    keepalive: true
                }).catch(() => {});
            }
        } catch (_) {}

        return event;
    }

    function trackLead(leadData) {
        try {
            const raw = localStorage.getItem(LEADS_KEY);
            const leads = raw ? JSON.parse(raw) : [];
            const lead = {
                id: 'lead_' + Date.now() + '_' + Math.floor(1000 + Math.random() * 9000),
                status: 'new', // new, reviewing, contacted, closed
                timestamp: Date.now(),
                dateStr: new Date().toLocaleString('tr-TR', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' }),
                page: window.location.pathname || '/',
                device: getDeviceType(),
                ...(leadData || {})
            };
            leads.unshift(lead);
            if (leads.length > 300) leads.length = 300;
            localStorage.setItem(LEADS_KEY, JSON.stringify(leads));

            // Also send to analytics API (returns server email relay confirmation if configured)
            return fetch('/api/analytics', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ type: 'lead_captured', lead })
            })
                .then((r) => (r.ok ? r.json().catch(() => null) : null))
                .catch(() => null);
        } catch (_) {
            return Promise.resolve(null);
        }
    }

    function initAutoTracking() {
        // Track unique visitor per day (does not increment on reload)
        let isNewVisitor = false;
        try {
            const today = new Date().toISOString().slice(0, 10);
            if (localStorage.getItem('dat_last_visit_date') !== today) {
                isNewVisitor = true;
                localStorage.setItem('dat_last_visit_date', today);
            }
        } catch (_) {}

        // Track page view
        trackEvent('page_view', {
            path: window.location.pathname || '/',
            screenWidth: window.innerWidth,
            isNewVisitor: isNewVisitor
        });

        // Track clicks
        document.addEventListener('click', function(e) {
            const el = e.target.closest('a, button');
            if (!el) return;

            const href = el.getAttribute('href') || '';
            const text = (el.textContent || '').trim().replace(/\s+/g, ' ').substring(0, 50);

            // WhatsApp button
            if (href.includes('wa.me') || href.includes('whatsapp.com')) {
                trackEvent('whatsapp_click', {
                    label: text || 'WhatsApp İletişim',
                    targetUrl: href,
                    page: window.location.pathname || '/'
                });
            }
            // Phone call button
            else if (href.startsWith('tel:')) {
                trackEvent('phone_click', {
                    number: href.replace('tel:', ''),
                    label: text || 'Telefonla Arama',
                    page: window.location.pathname || '/'
                });
            }
            // Service click / exploration
            else if (el.getAttribute('onclick')?.includes('openServiceModal') || href.includes('/hizmetler/')) {
                trackEvent('service_click', {
                    service: text || href,
                    page: window.location.pathname || '/'
                });
            }
        }, { passive: true });
    }

    return {
        trackEvent,
        trackLead,
        init: initAutoTracking
    };
})();

// Attach to window and initialize
window.DATAnalytics = DATAnalytics;
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', DATAnalytics.init);
} else {
    DATAnalytics.init();
}
