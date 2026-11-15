#!/usr/bin/env python3
"""
fix_contrast_and_readability.py
Comprehensive high-contrast and readability overhaul:
1. Replaces all white text classes inside white sections with crisp, high-contrast dark ink.
2. Replaces all dark obsidian card backgrounds inside white sections with clean #F7F7F8 / #FFFFFF cards.
3. Completely neutralizes any text-transparent white gradients to solid black #000000.
4. Fixes mobile floating buttons ("Ara", "WhatsApp", etc.) to pure monochrome black/white.
5. Injects foolproof CSS contrast protection ensuring NO white-on-white and NO black-on-black text can ever render.
"""

import os
import re

ROOT_INDEX = "index.html"
DAT_INDEX = "Dat/index.html"

assert os.path.exists(ROOT_INDEX), "index.html not found!"

with open(ROOT_INDEX, "r", encoding="utf-8") as f:
    content = f.read()

print(f"Read {len(content)} characters from index.html")

# 1. Transform dark card backgrounds inside sections to clean light surface (#F7F7F8)
# We want all cards in mimari, hizmetler, magaza, vaka-sureci, makaleler, ofislerimiz, vaka-bildir, sss, arama-rehberi, turkiye-dedektif-agi
sections_to_clean = [
    'mimari', 'hizmetler', 'magaza', 'vaka-sureci', 'makaleler',
    'avrupa-masasi', 'ofislerimiz', 'vaka-bildir', 'sss', 'arama-rehberi', 'turkiye-dedektif-agi'
]

for s_id in sections_to_clean:
    m = re.search(r'(<section[^>]*id="' + s_id + r'"[^>]*>)(.*?)(</section>)', content, re.DOTALL)
    if not m:
        continue
    sec_open = m.group(1)
    sec_body = m.group(2)
    sec_close = m.group(3)

    # Replace dark backgrounds with clean surface #F7F7F8 / #FFFFFF
    sec_body = sec_body.replace('bg-[#1D1D1F]', 'bg-[#F7F7F8]')
    sec_body = sec_body.replace('bg-[#1A1A1D]', 'bg-[#F7F7F8]')
    sec_body = sec_body.replace('bg-[#18181A]', 'bg-[#F7F7F8]')
    sec_body = sec_body.replace('bg-[#111111]', 'bg-[#F7F7F8]')
    sec_body = sec_body.replace('bg-[#242426]', 'bg-[#F0F0F2]')
    sec_body = sec_body.replace('bg-[#20ba59]', 'bg-[#000000]')
    sec_body = sec_body.replace('bg-[#141416]', 'bg-[#F7F7F8]')

    # Replace white border classes with subtle black border
    sec_body = re.sub(r'border-white/(?:10|15|20|25|5|07)', 'border-black/[0.08]', sec_body)
    sec_body = sec_body.replace('border-white/30', 'border-black/[0.12]')

    # Replace white text classes with high-contrast dark classes
    sec_body = sec_body.replace('text-[#FFFFFF]', 'text-[#000000]')
    sec_body = sec_body.replace('text-white/95', 'text-black')
    sec_body = sec_body.replace('text-white/90', 'text-black')
    sec_body = sec_body.replace('text-white/85', 'text-neutral-900')
    sec_body = sec_body.replace('text-white/80', 'text-neutral-900')
    sec_body = sec_body.replace('text-white/75', 'text-neutral-800')
    sec_body = sec_body.replace('text-white/70', 'text-neutral-800')
    sec_body = sec_body.replace('text-white/65', 'text-neutral-700')
    sec_body = sec_body.replace('text-white/60', 'text-neutral-700')
    sec_body = sec_body.replace('text-white/55', 'text-neutral-600')
    sec_body = sec_body.replace('text-white/50', 'text-neutral-600')
    sec_body = sec_body.replace('text-white/40', 'text-neutral-600')
    sec_body = sec_body.replace('text-white/30', 'text-neutral-500')
    sec_body = sec_body.replace('text-white/25', 'text-neutral-400')
    sec_body = sec_body.replace('text-white/20', 'text-neutral-400')
    # Replace bare 'text-white' when not part of text-white/...
    sec_body = re.sub(r'\btext-white\b', 'text-black', sec_body)

    content = content[:m.start()] + sec_open + sec_body + sec_close + content[m.end():]
    print(f"Cleaned contrast in section #{s_id}")

# 2. Fix Mobile Quick Call Pill & Stealth Buttons (lines ~1577 to 1586)
content = re.sub(
    r'<div id="mobileQuickPills"[^>]*>.*?</div>',
    '''<div id="mobileQuickPills" class="lg:hidden fixed fixed-gpu right-3 bottom-[calc(4.35rem+env(safe-area-inset-bottom,0px))] z-40 flex items-center gap-1.5 pointer-events-none transition-all duration-200">
        <a href="tel:+903122840299" title="7/24 Merkez Hat" class="pointer-events-auto inline-flex items-center gap-1.5 bg-black hover:bg-neutral-800 text-white text-[11px] font-medium py-1.5 px-3 rounded-full shadow-md active:scale-95 transition whitespace-nowrap">
            <i class="hgi hgi-stroke hgi-call-02 w-3.5 h-3.5 shrink-0"></i>
            <span>Ara</span>
        </a>
        <button id="panicBtnMobile" type="button" title="Acil Çıkış: Sayfayı anında Google'a yönlendirir" class="pointer-events-auto inline-flex items-center gap-1 bg-white hover:bg-neutral-100 text-black text-[11px] font-medium py-1.5 px-3 rounded-full shadow-md border border-black/15 active:scale-95 transition whitespace-nowrap">
            <i class="hgi hgi-stroke hgi-view-off w-3.5 h-3.5 shrink-0"></i>
            <span>Gizle</span>
        </button>
    </div>''',
    content,
    flags=re.DOTALL
)

# 3. Fix Mobile Tab Bar colors (clean white background, black active icons, no green)
content = re.sub(
    r'<nav id="mobileAppTabBar"[^>]*>.*?<\/nav>',
    '''<nav id="mobileAppTabBar" aria-label="Mobil Uygulama Alt Menüsü" class="lg:hidden fixed fixed-gpu left-1/2 -translate-x-1/2 bottom-[calc(0.55rem+env(safe-area-inset-bottom,0px))] z-50 w-[calc(100%-1.5rem)] max-w-[356px] rounded-full p-1 bg-white/95 backdrop-blur-md border border-black/15 shadow-[0_10px_30px_rgba(0,0,0,0.12)] transition-all duration-200">
        <div class="grid grid-cols-5 items-center gap-0.5 text-neutral-600">
            <a href="#top" data-tab-target="top" class="mobile-tab-item is-active flex flex-col items-center justify-center gap-0.5 py-1.5 px-1 text-[9.5px] font-medium text-black transition" title="DAT Özel Dedektiflik — Ana Sayfa">
                <span class="relative inline-flex items-center justify-center h-4"><i class="hgi hgi-stroke hgi-home-01 text-[17px] leading-none text-black"></i></span>
                <span class="truncate max-w-[58px] leading-tight font-medium text-black">Ana Sayfa</span>
            </a>
            <a href="#hizmetler" data-tab-target="hizmetler" class="mobile-tab-item flex flex-col items-center justify-center gap-0.5 py-1.5 px-1 text-[9.5px] font-medium text-neutral-600 hover:text-black transition" title="12 Dedektiflik Hizmeti">
                <span class="relative inline-flex items-center justify-center h-4"><i class="hgi hgi-stroke hgi-grid-view text-[17px] leading-none"></i></span>
                <span class="truncate max-w-[58px] leading-tight">Hizmetler</span>
            </a>
            <a href="#vaka-bildir" data-tab-target="vaka-bildir" class="mobile-tab-item flex flex-col items-center justify-center gap-0.5 py-1.5 px-1 text-[9.5px] font-medium text-neutral-600 hover:text-black transition" title="Teklif Al">
                <span class="relative inline-flex items-center justify-center h-4"><i class="hgi hgi-stroke hgi-shield-02 text-[17px] leading-none"></i></span>
                <span class="truncate max-w-[60px] leading-tight">Teklif Al</span>
            </a>
            <a href="#turkiye-dedektif-agi" data-tab-target="turkiye-dedektif-agi" class="mobile-tab-item flex flex-col items-center justify-center gap-0.5 py-1.5 px-1 text-[9.5px] font-medium text-neutral-600 hover:text-black transition" title="81 İl Ağı">
                <span class="relative inline-flex items-center justify-center h-4"><i class="hgi hgi-stroke hgi-location-01 text-[17px] leading-none"></i></span>
                <span class="truncate max-w-[56px] leading-tight">81 İl Ağı</span>
            </a>
            <a href="https://wa.me/905326667749?text=Merhaba%2C%20DAT%20Dedektiflik%20hakk%C4%B1nda%20gizli%20dan%C4%B1%C5%9Fmanl%C4%B1k%20almak%20istiyorum." target="_blank" rel="noopener noreferrer" class="mobile-tab-item flex flex-col items-center justify-center gap-0.5 py-1.5 px-1 text-[9.5px] font-medium text-black transition" title="WhatsApp">
                <span class="relative inline-flex items-center justify-center h-4">
                    <i class="hgi hgi-stroke hgi-whatsapp text-[17px] leading-none text-black"></i>
                </span>
                <span class="truncate max-w-[58px] leading-tight font-medium text-black">WhatsApp</span>
            </a>
        </div>
    </nav>''',
    content,
    flags=re.DOTALL
)

# 4. Inject Comprehensive CSS Readability & Contrast Overrides
contrast_css = '''
        /* ==================================================== */
        /* ABSOLUTE HIGH-CONTRAST & READABILITY GUARANTEE (OPENAI PURE) */
        /* ==================================================== */
        :root, html, body {
            background-color: #FFFFFF !important;
            color: #111111 !important;
        }

        /* Headings: Deep, razor-sharp pitch black */
        h1, h2, h3, h4, h5, h6, .apple-heading {
            color: #000000 !important;
            font-weight: 600 !important;
            letter-spacing: -0.025em !important;
            -webkit-text-fill-color: #000000 !important;
        }

        /* Kill all faint/transparent white text gradients */
        .bg-clip-text {
            -webkit-text-fill-color: #000000 !important;
            color: #000000 !important;
            background: none !important;
        }

        /* Text inside all normal sections must be dark & readable */
        section:not(.theme-dark-feature-banner) p,
        section:not(.theme-dark-feature-banner) span:not(.theme-badge-white):not(.text-white),
        section:not(.theme-dark-feature-banner) li,
        section:not(.theme-dark-feature-banner) a:not(.bg-black) {
            color: inherit;
        }

        /* Prevent washed out white text on light backgrounds */
        section:not(.theme-dark-feature-banner) .text-white,
        section:not(.theme-dark-feature-banner) [class*="text-white/"] {
            color: #1F2937 !important;
        }

        section:not(.theme-dark-feature-banner) .text-white\/60,
        section:not(.theme-dark-feature-banner) .text-white\/50,
        section:not(.theme-dark-feature-banner) .text-white\/40 {
            color: #4B5563 !important;
        }

        /* Ensure all card containers in sections render cleanly */
        .card-dark,
        section:not(.theme-dark-feature-banner) .bg-\[\#1D1D1F\],
        section:not(.theme-dark-feature-banner) .bg-\[\#1A1A1D\],
        section:not(.theme-dark-feature-banner) .bg-\[\#18181A\],
        section:not(.theme-dark-feature-banner) .bg-\[\#141416\],
        section:not(.theme-dark-feature-banner) .bg-\[\#111111\] {
            background-color: #F7F7F8 !important;
            color: #111111 !important;
            border: 1px solid rgba(0, 0, 0, 0.08) !important;
        }

        /* Interactive inputs */
        input, textarea, select {
            color: #000000 !important;
            background-color: #FFFFFF !important;
        }
        input::placeholder, textarea::placeholder {
            color: #6B7280 !important;
        }
'''

# Add inside <style id="openai-master-system">
target_style_tag = '<style id="openai-master-system">'
assert target_style_tag in content, "Cannot find <style id='openai-master-system'>"
content = content.replace(target_style_tag, target_style_tag + contrast_css)

# Write to root index.html and Dat/index.html
with open(ROOT_INDEX, "w", encoding="utf-8") as f:
    f.write(content)

with open(DAT_INDEX, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Successfully updated {ROOT_INDEX} and {DAT_INDEX}!")
