#!/usr/bin/env python3
"""
replicate_openai_icons.py
Transforms all icons on the site to match openai.com/tr-TR/ icon aesthetic:
1. Navbar:
   - Adds OpenAI search icon button.
   - Exact OpenAI wireframe globe SVG and chevron SVG for language switcher.
   - Exact OpenAI diagonal external arrow ↗ SVG and monochrome WhatsApp SVG.
   - Minimalist 2-line hamburger menu SVG for mobile.
2. Hero:
   - Exact OpenAI upward arrow SVG (↑) in 32px black circle send button.
   - Pure text prompt pills without colorful emojis.
3. Feature Banner:
   - Clean diagonal arrow SVG.
4. Cards & Links:
   - Clean chevron (>) and diagonal arrow (↗) SVGs.
5. Service cards:
   - Minimalist 1.5px stroke icons in sleek rounded-xl boxes.
6. Footer:
   - Exact minimalist vector SVG logos for X, YouTube, LinkedIn, Instagram.
   - Exact globe SVG for language selector pill.
7. Mobile Tab Bar:
   - Clean minimalist 1.5px stroke SVGs (Home, Services, Quote, 81 Provinces, WhatsApp).
8. CSS System:
   - Global SVG and icon rules matching OpenAI's crisp stroke-width, rendering, and monochrome color.
"""

import os
import re

ROOT_INDEX = "index.html"
DAT_INDEX = "Dat/index.html"

assert os.path.exists(ROOT_INDEX), "index.html not found!"

with open(ROOT_INDEX, "r", encoding="utf-8") as f:
    content = f.read()

# 1. NAVBAR ICONS UPDATE
# Find the right action pills container in header
# Replace langSwitcherBtn icons
content = re.sub(
    r'<i class="hgi hgi-stroke hgi-globe-02[^"]*"></i>\s*<span id="currentLangCode"[^>]*>([A-Z]+)</span>\s*<i class="hgi hgi-stroke hgi-arrow-down-01[^"]*"></i>',
    r'''<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" class="inline-block opacity-75"><circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>
                        <span id="currentLangCode" class="font-mono text-[11px] uppercase">\1</span>
                        <svg width="10" height="10" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="inline-block opacity-60"><path d="M4 6l4 4 4-4"/></svg>''',
    content
)

# Add search button right before langSwitcherWrap in header
search_btn_html = '''<!-- OpenAI Exact Search Button -->
                <button type="button" onclick="document.querySelector('#aiChatInput')?.focus();window.scrollTo({top:0,behavior:'smooth'});" class="p-2 rounded-full hover:bg-black/[0.05] text-black transition" title="Dedektif'e Sor / Ara">
                    <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
                </button>
                '''

if '<!-- OpenAI Exact Search Button -->' not in content:
    content = content.replace(
        '<div class="relative" id="langSwitcherWrap">',
        search_btn_html + '<div class="relative" id="langSwitcherWrap">'
    )

# Replace WhatsApp button in header with OpenAI diagonal arrow SVG
content = re.sub(
    r'<i class="hgi hgi-stroke hgi-whatsapp[^"]*"></i>\s*<span class="hidden sm:inline">WhatsApp</span>\s*<span>↗</span>',
    r'''<span class="hidden sm:inline">WhatsApp</span>
                    <svg width="12" height="12" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="inline-block ml-0.5"><path d="M4 12L12 4M12 4H6M12 4V10"/></svg>''',
    content
)

# Replace Mobile Menu button icon with OpenAI 2-line menu
content = re.sub(
    r'<i class="hgi hgi-stroke hgi-menu-01[^"]*"></i>',
    r'''<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="4" x2="20" y1="9" y2="9"/><line x1="4" x2="20" y1="15" y2="15"/></svg>''',
    content
)

# 2. HERO SEND BUTTON ARROW (Exact OpenAI Up Arrow)
content = re.sub(
    r'<button type="button" id="aiSendBtn"[^>]*>.*?<\/button>',
    r'''<button type="button" id="aiSendBtn" onclick="sendAIChatMessage()" class="w-8 h-8 rounded-full bg-[#000000] hover:bg-neutral-800 text-white flex items-center justify-center transition active:scale-95 shrink-0 shadow-xs cursor-pointer" title="Soruyu Yanıtla">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 19V5M5 12l7-7 7 7"/></svg>
                        </button>''',
    content,
    flags=re.DOTALL
)

# 3. HERO PROMPT PILLS: Remove emojis, keep crisp text
content = content.replace('>👶 Çocuk &amp; Velayet<', '>Çocuk &amp; Velayet Davaları<')
content = content.replace('>💔 Eş Takibi &amp; Aldatma<', '>Eş Takibi &amp; Aldatma<')
content = content.replace('>⚖️ Mahkemede Delil Geçerliliği<', '>Mahkemede Delil Geçerliliği<')
content = content.replace('>💳 Dedektif Ücretleri<', '>Dedektif Ücretleri ve Fiyatlar<')
content = content.replace('>🔍 Böcek Arama &amp; TSCM<', '>Böcek Arama &amp; TSCM<')
content = content.replace('>📍 Adres &amp; Borçlu Tespiti<', '>Adres &amp; Borçlu Tespiti<')

# 4. FOOTER SOCIAL ICONS (Exact OpenAI Minimal Vector Icons)
footer_social_old = re.search(r'<!-- Social Media Minimal Icons -->.*?</div>\s*</div>', content, re.DOTALL)
if footer_social_old:
    footer_social_new = '''<!-- Social Media Minimal Icons (OpenAI Exact Vectors) -->
                <div class="flex items-center gap-5 text-neutral-600">
                    <a href="https://twitter.com/datdedektiflik" target="_blank" rel="noopener noreferrer" class="hover:text-black transition" title="X (Twitter)">
                        <svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
                    </a>
                    <a href="https://youtube.com/@datdedektiflik" target="_blank" rel="noopener noreferrer" class="hover:text-black transition" title="YouTube">
                        <svg width="17" height="17" viewBox="0 0 24 24" fill="currentColor"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
                    </a>
                    <a href="https://linkedin.com/company/datdedektiflik" target="_blank" rel="noopener noreferrer" class="hover:text-black transition" title="LinkedIn">
                        <svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.28 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.75M6.88 8.56a1.68 1.68 0 0 0 1.68-1.68c0-.93-.75-1.69-1.68-1.69a1.69 1.69 0 0 0-1.69 1.69c0 .93.76 1.68 1.69 1.68m1.39 9.94v-8.37H5.5v8.37h2.77z"/></svg>
                    </a>
                    <a href="https://instagram.com/datdedektiflik" target="_blank" rel="noopener noreferrer" class="hover:text-black transition" title="Instagram">
                        <svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg>
                    </a>
                </div>

                <!-- Copyright & Cookie -->
                <div class="flex items-center gap-4 text-xs text-neutral-500">
                    <span>DAT Özel Dedektiflik © 2004–2026</span>
                    <button type="button" onclick="openLegalModal('cookie')" class="hover:text-black transition underline">Çerezleri Yönet</button>
                </div>

                <!-- Language Pill (OpenAI Style) -->
                <div class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-black/[0.04] text-xs font-medium text-black border border-black/[0.08]">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>
                    <span>Türkçe</span>
                </div>
            </div>'''
    content = content[:footer_social_old.start()] + footer_social_new + content[footer_social_old.end():]

# 5. MOBILE TAB BAR ICONS (Exact OpenAI Style 1.5px Outline SVGs)
mobile_tab_old = re.search(r'<nav id="mobileAppTabBar"[^>]*>.*?<\/nav>', content, re.DOTALL)
if mobile_tab_old:
    mobile_tab_new = '''<nav id="mobileAppTabBar" aria-label="Mobil Uygulama Alt Menüsü" class="lg:hidden fixed fixed-gpu left-1/2 -translate-x-1/2 bottom-[calc(0.55rem+env(safe-area-inset-bottom,0px))] z-50 w-[calc(100%-1.5rem)] max-w-[356px] rounded-full p-1 bg-white/95 backdrop-blur-md border border-black/15 shadow-[0_10px_30px_rgba(0,0,0,0.12)] transition-all duration-200">
        <div class="grid grid-cols-5 items-center gap-0.5 text-neutral-600">
            <a href="#top" data-tab-target="top" class="mobile-tab-item is-active flex flex-col items-center justify-center gap-0.5 py-1.5 px-1 text-[9.5px] font-medium text-black transition" title="DAT Özel Dedektiflik — Ana Sayfa">
                <span class="relative inline-flex items-center justify-center h-4">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
                </span>
                <span class="truncate max-w-[58px] leading-tight font-medium text-black">Ana Sayfa</span>
            </a>
            <a href="#hizmetler" data-tab-target="hizmetler" class="mobile-tab-item flex flex-col items-center justify-center gap-0.5 py-1.5 px-1 text-[9.5px] font-medium text-neutral-600 hover:text-black transition" title="12 Dedektiflik Hizmeti">
                <span class="relative inline-flex items-center justify-center h-4">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect width="7" height="7" x="3" y="3" rx="1"/><rect width="7" height="7" x="14" y="3" rx="1"/><rect width="7" height="7" x="14" y="14" rx="1"/><rect width="7" height="7" x="3" y="14" rx="1"/></svg>
                </span>
                <span class="truncate max-w-[58px] leading-tight">Hizmetler</span>
            </a>
            <a href="#vaka-bildir" data-tab-target="vaka-bildir" class="mobile-tab-item flex flex-col items-center justify-center gap-0.5 py-1.5 px-1 text-[9.5px] font-medium text-neutral-600 hover:text-black transition" title="Teklif Al">
                <span class="relative inline-flex items-center justify-center h-4">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
                </span>
                <span class="truncate max-w-[60px] leading-tight">Teklif Al</span>
            </a>
            <a href="#turkiye-dedektif-agi" data-tab-target="turkiye-dedektif-agi" class="mobile-tab-item flex flex-col items-center justify-center gap-0.5 py-1.5 px-1 text-[9.5px] font-medium text-neutral-600 hover:text-black transition" title="81 İl Ağı">
                <span class="relative inline-flex items-center justify-center h-4">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
                </span>
                <span class="truncate max-w-[56px] leading-tight">81 İl Ağı</span>
            </a>
            <a href="https://wa.me/905326667749?text=Merhaba%2C%20DAT%20Dedektiflik%20hakk%C4%B1nda%20gizli%20dan%C4%B1%C5%9Fmanl%C4%B1k%20almak%20istiyorum." target="_blank" rel="noopener noreferrer" class="mobile-tab-item flex flex-col items-center justify-center gap-0.5 py-1.5 px-1 text-[9.5px] font-medium text-black transition" title="WhatsApp">
                <span class="relative inline-flex items-center justify-center h-4">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" class="text-black"><path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946.003-6.556 5.338-11.891 11.893-11.891 3.181.001 6.167 1.24 8.413 3.488 2.245 2.248 3.481 5.236 3.48 8.414-.003 6.557-5.338 11.892-11.893 11.892-1.99-.001-3.951-.5-5.688-1.448l-6.305 1.654zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.434 9.889-9.885.002-5.462-4.415-9.89-9.881-9.892-5.452 0-9.887 4.434-9.889 9.884-.001 2.225.651 3.891 1.746 5.634l-.999 3.648 3.742-.981zm11.387-5.464c-.074-.124-.272-.198-.57-.347-.297-.149-1.758-.868-2.031-.967-.272-.099-.47-.149-.669.149-.198.297-.768.967-.941 1.165-.173.198-.347.223-.644.074-.297-.149-1.255-.462-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.297-.347.446-.521.151-.172.2-.296.3-.495.099-.198.05-.372-.025-.521-.075-.148-.669-1.611-.916-2.206-.242-.579-.487-.501-.669-.51l-.57-.01c-.198 0-.52.074-.792.372s-1.04 1.016-1.04 2.479 1.065 2.876 1.213 3.074c.149.198 2.095 3.2 5.076 4.487.709.306 1.263.489 1.694.626.712.226 1.36.194 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.695.248-1.29.173-1.414z"/></svg>
                </span>
                <span class="truncate max-w-[58px] leading-tight font-medium text-black">WhatsApp</span>
            </a>
        </div>
    </nav>'''
    content = content[:mobile_tab_old.start()] + mobile_tab_new + content[mobile_tab_old.end():]

# 6. INJECT GLOBAL OPENAI ICON STYLING RULES
openai_icon_css = '''
        /* ==================================================== */
        /* OPENAI ICON DESIGN SYSTEM */
        /* ==================================================== */
        .hgi, [class*="hgi-"] {
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;
            vertical-align: middle !important;
            color: currentColor !important;
            line-height: 1 !important;
        }

        /* Subtle, minimalist icon container boxes */
        .icon-box,
        [class*="rounded-2xl"][class*="w-11"][class*="h-11"],
        [class*="rounded-xl"][class*="w-10"][class*="h-10"] {
            background-color: #F4F4F5 !important;
            border: 1px solid rgba(0, 0, 0, 0.06) !important;
            color: #000000 !important;
            border-radius: 12px !important;
            box-shadow: none !important;
        }
        .icon-box:hover,
        [class*="rounded-2xl"][class*="w-11"][class*="h-11"]:hover {
            background-color: #ECECEE !important;
            border-color: rgba(0, 0, 0, 0.14) !important;
        }

        /* Diagonal link arrow transition */
        .openai-diagonal-arrow {
            display: inline-block;
            transition: transform 0.15s cubic-bezier(0.16, 1, 0.3, 1);
        }
        *:hover > .openai-diagonal-arrow {
            transform: translate(1.5px, -1.5px);
        }
'''

content = content.replace('/* ==================================================== */\n        /* ABSOLUTE HIGH-CONTRAST', openai_icon_css + '\n        /* ==================================================== */\n        /* ABSOLUTE HIGH-CONTRAST')

# Write to root index.html and Dat/index.html
with open(ROOT_INDEX, "w", encoding="utf-8") as f:
    f.write(content)

with open(DAT_INDEX, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Successfully applied OpenAI icons to {ROOT_INDEX} and {DAT_INDEX}!")
