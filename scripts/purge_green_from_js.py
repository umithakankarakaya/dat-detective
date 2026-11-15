# -*- coding: utf-8 -*-
with open("script.js", "r", encoding="utf-8") as f:
    js = f.read()

js = js.replace('#93F051', '#000000')
js = js.replace('#25D366', '#000000')
js = js.replace('bg-emerald-500', 'bg-black')
js = js.replace('text-[#93F051]', 'text-black')
js = js.replace('bg-[#93F051]', 'bg-black text-white')
js = js.replace('border-[#93F051]', 'border-black')
js = js.replace('text-[#15803D]', 'text-black')

with open("script.js", "w", encoding="utf-8") as f:
    f.write(js)
with open("Dat/script.js", "w", encoding="utf-8") as f:
    f.write(js)

print("✓ script.js ve Dat/script.js dosyalarından tüm yeşil renkler temizlendi!")
