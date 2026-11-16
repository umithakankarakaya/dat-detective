# -*- coding: utf-8 -*-
import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. En üstteki 3px yeşil çizgiyi tamamen kaldır
html = re.sub(r'<!-- Studio Top Accent Line.*?</div>', '', html, flags=re.DOTALL)
html = html.replace('<div class="h-[3px] w-full bg-[#93F051] relative z-50"></div>', '')

# 2. Üstteki yeşil noktalı ticker çubuğunu tamamen kaldır (OpenAI'da böyle bir çubuk yok)
html = re.sub(r'<div class="bg-white text-black/60 py-1 px-4.*?</div>\s*</div>', '', html, flags=re.DOTALL)
html = re.sub(r'<div class="bg-\[#111111\] text-white/70 py-1\.5 px-4.*?</div>\s*</div>', '', html, flags=re.DOTALL)

# 3. Yüzen yeşil butonları (Floating Docks) temizle / monokrom yap
html = html.replace('bg-[#93F051]', 'bg-black text-white')
html = html.replace('text-[#93F051]', 'text-black')
html = html.replace('border-[#93F051]', 'border-black')
html = html.replace('bg-[#25D366]', 'bg-black text-white')
html = html.replace('text-[#25D366]', 'text-black')
html = html.replace('bg-emerald-500', 'bg-black')
html = html.replace('bg-emerald-400', 'bg-black')
html = html.replace('text-emerald-500', 'text-black')
html = html.replace('text-emerald-400', 'text-black')
html = html.replace('text-emerald-600', 'text-black')
html = html.replace('hover:bg-[#DDF95E]', 'hover:bg-neutral-800')
html = html.replace('hover:bg-[#82dc43]', 'hover:bg-neutral-800')
html = html.replace('hover:border-[#93F051]', 'hover:border-black')
html = html.replace('selection:bg-[#93F051]', 'selection:bg-black')

# 4. Floating dock'taki butonları monokrom siyah yap
html = html.replace(
    '<a href="tel:+903122840299" title="7/24 Merkez Danışma Hattı: 0312 284 02 99" class="inline-flex items-center gap-2 bg-[#93F051] hover:bg-[#DDF95E] text-[#111111] text-[11px] font-medium py-2 px-3.5 rounded-full shadow-[0_10px_28px_rgba(147,240,81,0.25)] transition-all duration-200 active:scale-95 whitespace-nowrap">',
    '<a href="tel:+903122840299" title="7/24 Merkez Danışma Hattı: 0312 284 02 99" class="inline-flex items-center gap-2 bg-black hover:bg-neutral-800 text-white text-[11px] font-medium py-2 px-3.5 rounded-full shadow-md transition-all duration-200 active:scale-95 whitespace-nowrap">'
)
html = html.replace(
    '<span class="w-2 h-2 rounded-full bg-[#93F051] pulse-dot shrink-0"></span>',
    ''
)

# 5. OpenAI Monokrom Kural Blokunu Enjekte Et (Sıfır Yeşil Garantisi)
zero_green_css = """
    <style id="openai-zero-green-guarantee">
        /* SIFIR YEŞİL GARANTİSİ - TAM OPENAI MONOKROM */
        :root {
            --color-accent: #000000 !important;
        }

        /* Tüm yeşil tonlarını monokrom siyah ve griye zorla */
        [class*="text-[#93F051]"],
        [class*="text-emerald-"],
        [class*="text-[#25D366]"] {
            color: #000000 !important;
        }

        [class*="bg-[#93F051]"],
        [class*="bg-emerald-"],
        [class*="bg-[#25D366]"] {
            background-color: #000000 !important;
            color: #FFFFFF !important;
        }

        /* WhatsApp butonu OpenAI tarzı siyah hap buton */
        a[href*="wa.me"],
        a[href*="whatsapp"] {
            background-color: #000000 !important;
            color: #FFFFFF !important;
        }
        a[href*="wa.me"]:hover,
        a[href*="whatsapp"]:hover {
            background-color: #262626 !important;
        }
        a[href*="wa.me"] i,
        a[href*="whatsapp"] i {
            color: #FFFFFF !important;
        }

        /* Hero zemin ve öğeleri tam beyaz */
        #dedektife-sor {
            background-color: #FFFFFF !important;
            color: #000000 !important;
        }
        #dedektife-sor * {
            border-color: rgba(0, 0, 0, 0.12);
        }
        #dedektife-sor h1 {
            color: #000000 !important;
        }

        /* Konsol kutusu tam beyaz */
        #aiChatInputWrap {
            background-color: #FFFFFF !important;
            border: 1px solid rgba(0, 0, 0, 0.14) !important;
            box-shadow: 0 2px 14px rgba(0, 0, 0, 0.04) !important;
        }
        #aiChatInput {
            color: #000000 !important;
            background: transparent !important;
        }
        #aiChatInput::placeholder {
            color: #737373 !important;
        }

        /* Prompt hapları tam beyaz */
        #aiQuickChips button {
            background-color: #FFFFFF !important;
            border: 1px solid rgba(0, 0, 0, 0.12) !important;
            color: #000000 !important;
        }
        #aiQuickChips button:hover {
            background-color: rgba(0, 0, 0, 0.04) !important;
            border-color: rgba(0, 0, 0, 0.20) !important;
        }

        /* Gönder butonu yuvarlak siyah */
        #aiSendBtn {
            background-color: #000000 !important;
            color: #FFFFFF !important;
            border-radius: 9999px !important;
        }
        #aiSendBtn i {
            color: #FFFFFF !important;
        }
    </style>
"""

if 'id="openai-zero-green-guarantee"' not in html:
    html = html.replace('</head>', zero_green_css + '\n</head>')

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
with open("Dat/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✓ index.html ve Dat/index.html dosyalarından yeşil renkler tamamen temizlendi!")
