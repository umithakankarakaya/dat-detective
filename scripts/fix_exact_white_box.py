# -*- coding: utf-8 -*-
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. <html> satırını tamamen temiz light yap
html = html.replace(
    '<html lang="tr" class="scroll-smooth dark" data-theme="dark">',
    '<html lang="tr" class="scroll-smooth light" data-theme="light" style="color-scheme: light;">'
)
html = html.replace(
    '<html lang="tr" class="scroll-smooth light dark" data-theme="dark" style="color-scheme: dark;">',
    '<html lang="tr" class="scroll-smooth light" data-theme="light" style="color-scheme: light;">'
)
html = html.replace(
    '<html lang="tr" class="scroll-smooth light" data-theme="light">',
    '<html lang="tr" class="scroll-smooth light" data-theme="light" style="color-scheme: light;">'
)

# 2. Navbar Logo: "DAT" yazısının siyah olması
html = html.replace(
    '<span class="text-[17px] font-semibold tracking-[-0.03em] text-white">DAT <span class="font-normal text-neutral-600">Dedektiflik</span></span>',
    '<span class="text-[17px] font-semibold tracking-[-0.03em] text-black">DAT <span class="font-normal text-neutral-600">Dedektiflik</span></span>'
)
html = html.replace(
    '<span class="text-[17px] font-semibold tracking-[-0.03em] text-black">DAT <span class="font-normal text-neutral-600">Dedektiflik</span></span>',
    '<span class="text-[17px] font-semibold tracking-[-0.03em] text-black">DAT <span class="font-normal text-neutral-600">Dedektiflik</span></span>'
)

# 3. Konsol Kutusunu ve Prompt Haplarını kesin olarak beyaz yapan CSS
force_white_rules = """
    <style id="openai-exact-white-box">
        /* OpenAI Tam Beyaz Konsol ve Haplar */
        #aiChatInputWrap,
        .openai-box-white {
            background-color: #FFFFFF !important;
            border: 1px solid rgba(0, 0, 0, 0.14) !important;
            box-shadow: 0 2px 14px rgba(0, 0, 0, 0.04) !important;
            color: #000000 !important;
        }

        #aiChatInput {
            background-color: transparent !important;
            color: #000000 !important;
        }
        #aiChatInput::placeholder {
            color: #737373 !important;
        }

        #aiQuickChips button,
        .openai-pill-white {
            background-color: #FFFFFF !important;
            border: 1px solid rgba(0, 0, 0, 0.12) !important;
            color: #000000 !important;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02) !important;
        }
        #aiQuickChips button:hover,
        .openai-pill-white:hover {
            background-color: rgba(0, 0, 0, 0.04) !important;
            border-color: rgba(0, 0, 0, 0.20) !important;
            color: #000000 !important;
        }

        #aiSendBtn {
            background-color: #000000 !important;
            color: #FFFFFF !important;
        }
        #aiSendBtn:hover {
            background-color: #262626 !important;
        }
    </style>
"""

if 'id="openai-exact-white-box"' not in html:
    html = html.replace('</head>', force_white_rules + '\n</head>')

# 4. Konsol div'ine id="aiChatInputWrap" ve openai-box-white sınıfı ekle
html = html.replace(
    'class="max-w-[720px] mx-auto rounded-[28px] border border-black/[0.14] bg-[#FFFFFF] shadow-[0_2px_14px_rgba(0,0,0,0.04)] hover:shadow-[0_4px_20px_rgba(0,0,0,0.07)] focus-within:border-black/35 p-4 sm:p-5 transition relative"',
    'id="aiChatInputWrap" class="openai-box-white max-w-[720px] mx-auto rounded-[28px] border border-black/[0.14] bg-[#FFFFFF] shadow-[0_2px_14px_rgba(0,0,0,0.04)] hover:shadow-[0_4px_20px_rgba(0,0,0,0.07)] focus-within:border-black/35 p-4 sm:p-5 transition relative"'
)

# 5. Prompt butonlarına openai-pill-white sınıfı ekle
html = html.replace('class="px-3.5 py-1.5 rounded-full border border-black/[0.12] bg-[#FFFFFF] hover:bg-black/[0.04] text-[#000000] text-xs sm:text-[13px] transition font-normal shrink-0 shadow-xs"', 'class="openai-pill-white px-3.5 py-1.5 rounded-full border border-black/[0.12] bg-[#FFFFFF] hover:bg-black/[0.04] text-[#000000] text-xs sm:text-[13px] transition font-normal shrink-0 shadow-xs"')

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
with open("Dat/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✓ index.html ve Dat/index.html konsol kutusu ve hapları tam beyaza kilitlendi!")
