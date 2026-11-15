# -*- coding: utf-8 -*-
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Logo "DAT" yazısına doğrudan inline style vererek CSS dark override'ı tamamen ez
html = html.replace(
    '<span class="text-[17px] font-semibold tracking-[-0.03em] text-black">DAT <span class="font-normal text-neutral-600">Dedektiflik</span></span>',
    '<span class="text-[17px] font-semibold tracking-[-0.03em]" style="color: #000000 !important;">DAT <span class="font-normal text-neutral-600" style="color: #595959 !important;">Dedektiflik</span></span>'
)

# 2. Üstteki yeşil ticker çubuğu yerine OpenAI gibi temiz minimal ince çizgi yap veya gizle
html = html.replace(
    'class="bg-[#111111] text-white/70 py-1.5 px-4 text-[10.5px] border-b border-white/5 flex items-center justify-between"',
    'class="bg-white text-black/60 py-1 px-4 text-[10.5px] border-b border-black/[0.06] flex items-center justify-between"'
)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
with open("Dat/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✓ Logo ve üst çubuk OpenAI siyah/beyaz paletine tam eşitlendi!")
