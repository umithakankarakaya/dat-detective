/* DAT Özel Dedektiflik — 7-Language Internationalization (i18n) Engine
 * Languages: TR (Default), EN, DE, FR, AR (RTL), RU, ME (Crnogorski/Srpski)
 * Works seamlessly both over http://localhost:3000 and file:// offline preview.
 */
(function () {
    'use strict';

    var STORAGE_KEY = 'dat_site_lang';
    var SUPPORTED_LANGS = ['tr', 'en', 'de', 'fr', 'ar', 'ru', 'me'];
    var HTML_LANG_MAP = {
        tr: 'tr',
        en: 'en',
        de: 'de',
        fr: 'fr',
        ar: 'ar',
        ru: 'ru',
        me: 'cnr'
    };

    var currentLang = 'tr';
    var captured = false;
    var origMeta = { title: '', description: '' };
    var origHtmlBlocks = []; // { el, key, html }
    var origTextNodes = [];  // { node, leading, core, trailing }
    var origAttrs = [];      // { el, attr, val }

    function normalizeStr(s) {
        return String(s || '').replace(/\s+/g, ' ').trim();
    }

    function isExcludedNode(node) {
        var el = node.nodeType === 1 ? node : node.parentElement;
        while (el && el !== document.body && el !== document.documentElement) {
            var tag = el.tagName;
            if (tag === 'SCRIPT' || tag === 'STYLE' || tag === 'NOSCRIPT' || tag === 'SVG' || tag === 'KBD' || tag === 'CODE') {
                return true;
            }
            if (el.hasAttribute('data-no-i18n') || el.hasAttribute('data-i18n-html') || el.hasAttribute('data-live-visitors')) {
                return true;
            }
            if (el.id === 'cartCountBadge' || el.id === 'storeSectionCartCount' || el.id === 'mobileTabCartBadge' || el.id === 'liveVisitorSource' || el.id === 'themeToggleLabel' || el.id === 'mobileThemeStateText') {
                return true;
            }
            el = el.parentElement;
        }
        return false;
    }

    function isExcludedAttrEl(el) {
        var cur = el;
        while (cur && cur !== document.documentElement) {
            if (cur.hasAttribute('data-no-i18n')) return true;
            cur = cur.parentElement;
        }
        return false;
    }

    function captureOriginalDOM() {
        if (captured) return;
        captured = true;

        origMeta.title = document.title || '';
        var descMeta = document.querySelector('meta[name="description"]');
        origMeta.description = descMeta ? (descMeta.getAttribute('content') || '') : '';

        // Capture [data-i18n-html] blocks first (before walking text nodes)
        var blockEls = document.querySelectorAll('[data-i18n-html]');
        for (var i = 0; i < blockEls.length; i++) {
            var bEl = blockEls[i];
            var key = bEl.getAttribute('data-i18n-html');
            if (key) {
                origHtmlBlocks.push({ el: bEl, key: key, html: bEl.innerHTML });
            }
        }

        // Capture visible text nodes via TreeWalker
        var root = document.body || document.documentElement;
        var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, null, false);
        var n;
        while ((n = walker.nextNode())) {
            if (isExcludedNode(n)) continue;
            var raw = n.nodeValue;
            if (!raw) continue;
            var m = raw.match(/^(\s*)([\s\S]*?)(\s*)$/);
            var core = m ? normalizeStr(m[2]) : '';
            if (!core) continue;
            origTextNodes.push({
                node: n,
                leading: m ? m[1] : '',
                core: core,
                trailing: m ? m[3] : ''
            });
        }

        // Capture translatable attributes
        var attrs = ['placeholder', 'title', 'aria-label'];
        var allEls = document.querySelectorAll('[placeholder],[title],[aria-label]');
        for (var j = 0; j < allEls.length; j++) {
            var el = allEls[j];
            if (isExcludedAttrEl(el)) continue;
            for (var k = 0; k < attrs.length; k++) {
                var attrName = attrs[k];
                if (el.hasAttribute(attrName)) {
                    var val = normalizeStr(el.getAttribute(attrName));
                    if (val) {
                        origAttrs.push({ el: el, attr: attrName, val: val });
                    }
                }
            }
        }
    }

    function getPack(lang) {
        var code = lang || currentLang;
        if (code === 'tr' || !window.DAT_LANGS || !window.DAT_LANGS[code]) {
            return null;
        }
        return window.DAT_LANGS[code];
    }

    function snapshotLiveCounts() {
        var visitorEl = document.querySelector('[data-live-visitors]');
        var cartSectionEl = document.getElementById('storeSectionCartCount');
        return {
            visitors: visitorEl ? visitorEl.textContent : null,
            sectionCart: cartSectionEl ? cartSectionEl.textContent : null
        };
    }

    function restoreLiveCounts(counts) {
        if (counts.visitors !== null) {
            var visNodes = document.querySelectorAll('[data-live-visitors]');
            for (var i = 0; i < visNodes.length; i++) {
                visNodes[i].textContent = counts.visitors;
            }
        }
        if (counts.sectionCart !== null) {
            var sc = document.getElementById('storeSectionCartCount');
            if (sc) sc.textContent = counts.sectionCart;
        }
    }

    function updateSwitcherUI(lang) {
        var codeBadge = document.getElementById('currentLangCode');
        if (codeBadge) {
            codeBadge.textContent = lang.toUpperCase();
        }
        var opts = document.querySelectorAll('.lang-opt-btn[data-lang-opt]');
        for (var i = 0; i < opts.length; i++) {
            var btn = opts[i];
            var optLang = btn.getAttribute('data-lang-opt');
            var active = optLang === lang;
            if (btn.closest('#mobileLangBar')) {
                if (active) {
                    btn.className = 'lang-opt-btn py-1.5 rounded-lg bg-[#93F051] text-[#111111] font-mono text-[11px] font-medium text-center transition';
                } else {
                    btn.className = 'lang-opt-btn py-1.5 rounded-lg bg-[#222224] text-white/75 font-mono text-[11px] text-center transition';
                }
            } else {
                if (active) {
                    btn.classList.add('bg-[#111111]', 'text-[#93F051]', 'font-medium');
                    btn.classList.remove('text-white/75', 'text-[#3A3E42]', 'text-[#000000]', 'hover:bg-white/10', 'hover:bg-[#F3F4F4]');
                } else {
                    btn.classList.remove('bg-[#111111]', 'text-[#93F051]', 'bg-[#FFF7ED]', 'text-[#F48120]', 'font-medium', 'text-[#000000]');
                    btn.classList.add('text-white/75', 'hover:bg-white/10');
                }
            }
        }
    }

    function applyTranslations(lang) {
        captureOriginalDOM();
        var pack = getPack(lang);

        // Direction and HTML lang attribute
        var dir = pack && pack.dir === 'rtl' ? 'rtl' : 'ltr';
        document.documentElement.dir = dir;
        document.documentElement.lang = HTML_LANG_MAP[lang] || 'tr';
        document.documentElement.setAttribute('data-lang', lang);

        function wrapLtrTokensPlain(str) {
            if (dir !== 'rtl' || !str) return str;
            // Wrap phone numbers, tracking codes & number ranges in Unicode LRI..PDI so RTL never reverses digit groups
            return String(str).replace(/((?:\+\d[\d\s()-]{5,}\d|\b0\d{2,3}[\s-]\d{3}[\s-]\d{2}[\s-]\d{2}\b|#DAT-[A-Z0-9-]+|\b\d{4}\s*[–-]\s*\d{4}\b|\+\d[\d.,]*\d|\b\d[\d.,]*\+))/g, '\u2066$1\u2069');
        }

        function wrapLtrTokensHtml(htmlStr) {
            if (dir !== 'rtl' || !htmlStr) return htmlStr;
            var segs = String(htmlStr).split(/(<[^>]+>)/g);
            var inLtrSpan = 0;
            for (var x = 0; x < segs.length; x++) {
                var seg = segs[x];
                if (!seg) continue;
                if (seg.charAt(0) === '<') {
                    if (/^<span\b[^>]*dir=['"]ltr['"]/i.test(seg)) inLtrSpan++;
                    else if (inLtrSpan > 0 && /^<\/span\s*>/i.test(seg)) inLtrSpan--;
                } else if (inLtrSpan === 0) {
                    segs[x] = seg.replace(/((?:\+\d[\d\s()-]{5,}\d|\b0\d{2,3}[\s-]\d{3}[\s-]\d{2}[\s-]\d{2}\b|#DAT-[A-Z0-9-]+|\b\d{4}\s*[–-]\s*\d{4}\b|\+\d[\d.,]*\d|\b\d[\d.,]*\+))/g, '<span dir="ltr" style="unicode-bidi:isolate">$1</span>');
                }
            }
            return segs.join('');
        }

        // Meta tags
        if (pack && pack.meta) {
            if (pack.meta.title) document.title = pack.meta.title;
            var dm = document.querySelector('meta[name="description"]');
            if (dm && pack.meta.description) dm.setAttribute('content', pack.meta.description);
        } else {
            if (origMeta.title) document.title = origMeta.title;
            var dmOrig = document.querySelector('meta[name="description"]');
            if (dmOrig && origMeta.description) dmOrig.setAttribute('content', origMeta.description);
        }

        // Snapshot dynamic numeric counters before touching HTML blocks
        var liveCounts = snapshotLiveCounts();

        // Rich HTML blocks
        for (var i = 0; i < origHtmlBlocks.length; i++) {
            var blk = origHtmlBlocks[i];
            if (pack && pack.htmlBlocks && typeof pack.htmlBlocks[blk.key] === 'string') {
                blk.el.innerHTML = wrapLtrTokensHtml(pack.htmlBlocks[blk.key]);
            } else {
                blk.el.innerHTML = blk.html;
            }
        }

        // Restore live counters inside re-rendered HTML blocks
        restoreLiveCounts(liveCounts);

        // Plain text nodes
        var phrases = pack && pack.phrases ? pack.phrases : null;
        for (var j = 0; j < origTextNodes.length; j++) {
            var entry = origTextNodes[j];
            var targetCore = (phrases && Object.prototype.hasOwnProperty.call(phrases, entry.core))
                ? phrases[entry.core]
                : entry.core;
            entry.node.nodeValue = entry.leading + wrapLtrTokensPlain(targetCore) + entry.trailing;
        }

        // Attributes
        for (var k = 0; k < origAttrs.length; k++) {
            var a = origAttrs[k];
            var targetAttr = (phrases && Object.prototype.hasOwnProperty.call(phrases, a.val))
                ? phrases[a.val]
                : a.val;
            a.el.setAttribute(a.attr, wrapLtrTokensPlain(targetAttr));
        }

        // Re-render dynamic interactive widgets from script.js
        if (typeof window.switchHeroCase === 'function' && typeof window.currentHeroCaseKey !== 'undefined') {
            try { window.switchHeroCase(window.currentHeroCaseKey); } catch (_) {}
        } else if (typeof switchHeroCase === 'function' && typeof currentHeroCaseKey !== 'undefined') {
            try { switchHeroCase(currentHeroCaseKey); } catch (_) {}
        }

        if (typeof window.selectSimulatorCase === 'function' && typeof window.currentSimTabKey !== 'undefined') {
            try { window.selectSimulatorCase(window.currentSimTabKey); } catch (_) {}
        } else if (typeof selectSimulatorCase === 'function' && typeof currentSimTabKey !== 'undefined') {
            try { selectSimulatorCase(currentSimTabKey); } catch (_) {}
        }

        if (typeof window.renderCart === 'function') {
            try { window.renderCart(); } catch (_) {}
        } else if (typeof renderCart === 'function') {
            try { renderCart(); } catch (_) {}
        }

        // Refresh open detail modals if visible
        var artModal = document.getElementById('articleModal');
        if (artModal && !artModal.classList.contains('hidden') && typeof openArticleModal === 'function' && typeof currentArticleKey !== 'undefined' && currentArticleKey) {
            try { openArticleModal(currentArticleKey); } catch (_) {}
        }
        var srvModal = document.getElementById('serviceDetailModal');
        if (srvModal && !srvModal.classList.contains('hidden') && typeof openServiceModal === 'function' && typeof currentSelectedServiceKey !== 'undefined' && currentSelectedServiceKey) {
            try { openServiceModal(currentSelectedServiceKey); } catch (_) {}
        }
        var prodModal = document.getElementById('productModal');
        if (prodModal && !prodModal.classList.contains('hidden') && typeof openProductModal === 'function' && typeof activeModalProductSku !== 'undefined' && activeModalProductSku) {
            try { openProductModal(activeModalProductSku); } catch (_) {}
        }
        var legalModal = document.getElementById('legalInfoModal');
        if (legalModal && !legalModal.classList.contains('hidden') && typeof openLegalModal === 'function' && typeof activeLegalModalType !== 'undefined' && activeLegalModalType) {
            try { openLegalModal(activeLegalModalType); } catch (_) {}
        }

        // Update live presence source badge text
        var srcBadge = document.getElementById('liveVisitorSource');
        if (srcBadge) {
            if (window.__datLastPresenceMode === 'local') {
                srcBadge.textContent = getUI('localSource', 'Tarayıcı Oturumları');
            } else if (window.__datLastPresenceMode === 'server') {
                srcBadge.textContent = getUI('serverSource', 'Sunucu Doğrulamalı');
            } else {
                srcBadge.textContent = (phrases && phrases['Doğrulanıyor...']) ? phrases['Doğrulanıyor...'] : 'Doğrulanıyor...';
            }
        }

        // Point founder biography CTAs cleanly to selected language dossier route
        var fHref = (lang === 'tr')
            ? 'umit-hakan-karakaya.html'
            : (window.location.protocol === 'file:' ? lang + '/umit-hakan-karakaya.html' : '/' + lang + '/umit-hakan-karakaya.html');
        var fBtn = document.getElementById('founderProfileLink');
        if (fBtn) fBtn.setAttribute('href', fHref);
        var fFoot = document.getElementById('footerFounderLink');
        if (fFoot) fFoot.setAttribute('href', fHref);

        updateSwitcherUI(lang);
        if (typeof window.updateThemeToggleUI === 'function') {
            window.updateThemeToggleUI();
        }
    }

    function setSiteLanguage(lang) {
        var normalized = String(lang || 'tr').toLowerCase().trim();
        if (SUPPORTED_LANGS.indexOf(normalized) === -1) {
            normalized = 'tr';
        }
        try {
            localStorage.setItem(STORAGE_KEY, normalized);
        } catch (_) {}

        // If on a static pre-rendered SEO language route (/en/, /de/, etc.), navigate cleanly to target locale URL
        if (window.DAT_STATIC_PAGE_LANG && normalized !== window.DAT_STATIC_PAGE_LANG) {
            var isFile = window.location.protocol === 'file:';
            if (isFile) {
                window.location.href = normalized === 'tr' ? '../index.html' : '../' + normalized + '/index.html';
            } else {
                window.location.href = normalized === 'tr' ? '/' : '/' + normalized + '/';
            }
            return;
        }

        currentLang = normalized;
        applyTranslations(normalized);

        var menu = document.getElementById('langDropdownMenu');
        if (menu) menu.classList.add('hidden');
        var btn = document.getElementById('langSwitcherBtn');
        if (btn) btn.setAttribute('aria-expanded', 'false');

        // Dispatch event for any optional listeners
        try {
            window.dispatchEvent(new CustomEvent('dat:langchange', { detail: { lang: normalized } }));
        } catch (_) {}
    }

    function toggleLangMenu() {
        var menu = document.getElementById('langDropdownMenu');
        var btn = document.getElementById('langSwitcherBtn');
        if (!menu) return;
        var willOpen = menu.classList.contains('hidden');
        menu.classList.toggle('hidden');
        if (btn) btn.setAttribute('aria-expanded', willOpen ? 'true' : 'false');
    }

    function getDynamic(group, key, fallback) {
        var pack = getPack(currentLang);
        if (!pack || !pack[group]) return fallback;
        if (Object.prototype.hasOwnProperty.call(pack[group], key)) {
            return pack[group][key];
        }
        return fallback;
    }

    function getUI(key, fallback) {
        var pack = getPack(currentLang);
        if (!pack || !pack.ui) return fallback;
        if (Object.prototype.hasOwnProperty.call(pack.ui, key)) {
            var val = pack.ui[key];
            if (pack.dir === 'rtl' && typeof val === 'string') {
                var re = /(\+\d[\d\s()-]{5,}\d|\b0\d{2,3}[\s-]\d{3}[\s-]\d{2}[\s-]\d{2}\b|#DAT-[A-Z0-9-]+)/g;
                return val.indexOf('<') !== -1
                    ? val.replace(re, '<span dir="ltr" style="unicode-bidi:isolate">$1</span>')
                    : val.replace(re, '\u2066$1\u2069');
            }
            return val;
        }
        return fallback;
    }

    function detectInitialLanguage() {
        try {
            var params = new URLSearchParams(window.location.search || '');
            var qLang = params.get('lang');
            if (qLang) {
                var qNorm = qLang.toLowerCase().trim();
                if (SUPPORTED_LANGS.indexOf(qNorm) !== -1) return qNorm;
            }
        } catch (_) {}
        return 'tr';
    }

    // Close dropdown when clicking outside or pressing Escape
    document.addEventListener('click', function (e) {
        var wrap = document.getElementById('langSwitcherWrap');
        var menu = document.getElementById('langDropdownMenu');
        if (!wrap || !menu || menu.classList.contains('hidden')) return;
        if (!wrap.contains(e.target)) {
            menu.classList.add('hidden');
            var btn = document.getElementById('langSwitcherBtn');
            if (btn) btn.setAttribute('aria-expanded', 'false');
        }
    });

    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') {
            var menu = document.getElementById('langDropdownMenu');
            if (menu && !menu.classList.contains('hidden')) {
                menu.classList.add('hidden');
                var btn = document.getElementById('langSwitcherBtn');
                if (btn) btn.setAttribute('aria-expanded', 'false');
            }
        }
    });

    window.toggleLangMenu = toggleLangMenu;
    window.setSiteLanguage = setSiteLanguage;
    window.DAT_I18N = {
        getLanguage: function () { return currentLang; },
        getSupportedLanguages: function () { return SUPPORTED_LANGS.slice(); },
        getDynamic: getDynamic,
        getUI: getUI,
        setLanguage: setSiteLanguage
    };

    function boot() {
        var staticLang = window.DAT_STATIC_PAGE_LANG;
        if (staticLang && SUPPORTED_LANGS.indexOf(staticLang) !== -1 && staticLang !== 'tr') {
            currentLang = staticLang;
            var pack = getPack(staticLang);
            document.documentElement.dir = (pack && pack.dir === 'rtl') ? 'rtl' : 'ltr';
            document.documentElement.lang = HTML_LANG_MAP[staticLang] || staticLang;
            updateSwitcherUI(staticLang);
            if (typeof window.switchHeroCase === 'function' && typeof currentHeroCaseKey !== 'undefined') {
                try { window.switchHeroCase(currentHeroCaseKey); } catch (_) {}
            } else if (typeof switchHeroCase === 'function' && typeof currentHeroCaseKey !== 'undefined') {
                try { switchHeroCase(currentHeroCaseKey); } catch (_) {}
            }
            if (typeof window.selectSimulatorCase === 'function' && typeof currentSimTabKey !== 'undefined') {
                try { window.selectSimulatorCase(currentSimTabKey); } catch (_) {}
            } else if (typeof selectSimulatorCase === 'function' && typeof currentSimTabKey !== 'undefined') {
                try { selectSimulatorCase(currentSimTabKey); } catch (_) {}
            }
            if (typeof renderCart === 'function') {
                try { renderCart(); } catch (_) {}
            }
            return;
        }

        captureOriginalDOM();
        var initial = detectInitialLanguage();
        currentLang = initial;
        if (initial !== 'tr') {
            applyTranslations(initial);
        } else {
            updateSwitcherUI('tr');
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', boot);
    } else {
        boot();
    }
})();
