# -*- coding: utf-8 -*-
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Logo text - monokrom sade beyaz
html = html.replace(
    'DAT <span class="font-medium text-[#93F051]">DEDEKTİFLİK</span>',
    'DAT <span class="font-medium text-white">DEDEKTİFLİK</span>'
)

# 2. Header Fiyat Teklifi butonu - OpenAI saf beyaz hap buton
html = html.replace(
    'class="hidden sm:flex px-4 py-2 rounded-full bg-[#93F051] hover:bg-[#DDF95E] text-[#111111] text-xs font-medium tracking-tight transition items-center gap-1.5 active:scale-95"',
    'class="hidden sm:flex px-4 py-2 rounded-full bg-white hover:bg-neutral-200 text-black text-xs font-medium tracking-tight transition items-center gap-1.5 active:scale-95 shadow-sm"'
)

# 3. Header Sepet badge - monokrom
html = html.replace(
    'class="inline-flex items-center justify-center min-w-[18px] h-[18px] px-1 rounded-full bg-[#93F051] text-[#111111] text-[10px] font-mono font-medium"',
    'class="inline-flex items-center justify-center min-w-[18px] h-[18px] px-1 rounded-full bg-white text-black text-[10px] font-mono font-medium"'
)

# 4. Nav içindeki aktif link rengi - monokrom beyaz
html = html.replace(
    'class="px-2.5 py-1.5 rounded-full hover:bg-white/10 text-[#93F051] font-medium transition inline-flex items-center gap-1.5 whitespace-nowrap"',
    'class="px-2.5 py-1.5 rounded-full hover:bg-white/10 text-white font-medium transition inline-flex items-center gap-1.5 whitespace-nowrap"'
)
html = html.replace(
    '<span class="w-1.5 h-1.5 rounded-full bg-[#93F051] animate-pulse shrink-0"></span>',
    '<span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse shrink-0"></span>'
)

# Kaydet
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
with open("Dat/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✓ Header OpenAI monokrom rafinasyonu tamamlandı.")
