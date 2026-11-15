# -*- coding: utf-8 -*-
with open("script.js", "r", encoding="utf-8") as f:
    js = f.read()

# 1. User Bubble OpenAI stili: Saf sade gri hap balon
old_user_bubble = """        <div class="bg-[#242426] border border-[#93F051]/30 rounded-2xl rounded-tr-sm p-3.5 sm:p-4 text-white max-w-[85%] sm:max-w-[75%] space-y-1 shadow-md">
            <div class="text-[10px] font-mono text-[#93F051] flex items-center justify-end gap-1">
                <span>Siz</span>
                <span>•</span>
                <span>${timeStr}</span>
            </div>
            <p class="text-xs sm:text-[13px] leading-relaxed text-left text-white/95">${escapedQuery}</p>
        </div>"""

new_user_bubble = """        <div class="bg-[#F4F4F5] border border-black/[0.08] rounded-2xl rounded-tr-sm p-3.5 sm:p-4 text-black max-w-[85%] sm:max-w-[75%] space-y-1 shadow-xs">
            <div class="text-[10px] font-mono text-[#71717A] flex items-center justify-end gap-1">
                <span>Siz</span>
                <span>•</span>
                <span>${timeStr}</span>
            </div>
            <p class="text-xs sm:text-[13.5px] leading-relaxed text-left text-black font-normal">${escapedQuery}</p>
        </div>"""

js = js.replace(old_user_bubble, new_user_bubble)

# 2. Typing indicator
old_typing = """        <img src="assets/photos/elsa-dedektif-asistan.jpg" alt="Elsa & Ümit Hakan Karakaya" class="w-8 h-8 rounded-full border border-[#93F051]/50 object-cover object-top shrink-0 mt-1 shadow-sm">
        <div class="bg-[#111111] border border-white/10 rounded-2xl rounded-tl-sm px-4 py-3 text-white flex items-center gap-2.5 shadow-sm">
            <span class="text-xs text-white/70">Yeni Nesil Dedektif yanıt hazırlıyor</span>
            <span class="inline-flex gap-1 items-center">
                <span class="w-1.5 h-1.5 rounded-full bg-[#93F051] animate-bounce"></span>
                <span class="w-1.5 h-1.5 rounded-full bg-[#93F051] animate-bounce [animation-delay:0.15s]"></span>
                <span class="w-1.5 h-1.5 rounded-full bg-[#93F051] animate-bounce [animation-delay:0.3s]"></span>
            </span>
        </div>"""

new_typing = """        <img src="assets/photos/elsa-dedektif-asistan.jpg" alt="Elsa & Ümit Hakan Karakaya" class="w-8 h-8 rounded-full border border-black/10 object-cover object-top shrink-0 mt-1 shadow-xs">
        <div class="bg-[#FFFFFF] border border-black/[0.12] rounded-2xl rounded-tl-sm px-4 py-3 text-black flex items-center gap-2.5 shadow-xs">
            <span class="text-xs text-neutral-600 font-normal">Yanıt hazırlanıyor</span>
            <span class="inline-flex gap-1 items-center">
                <span class="w-1.5 h-1.5 rounded-full bg-black animate-bounce"></span>
                <span class="w-1.5 h-1.5 rounded-full bg-black animate-bounce [animation-delay:0.15s]"></span>
                <span class="w-1.5 h-1.5 rounded-full bg-black animate-bounce [animation-delay:0.3s]"></span>
            </span>
        </div>"""

js = js.replace(old_typing, new_typing)

# 3. Response Bubble OpenAI Card
old_resp_header = """            <img src="assets/photos/elsa-dedektif-asistan.jpg" alt="Elsa & Ümit Hakan Karakaya" class="w-8 h-8 rounded-full border border-[#93F051]/50 object-cover object-top shrink-0 mt-1 shadow-sm">
            <div class="bg-[#111111] border border-white/10 rounded-2xl rounded-tl-sm p-4 sm:p-5 text-white max-w-[95%] sm:max-w-[85%] space-y-3.5 shadow-lg">
                <div class="flex flex-wrap items-center justify-between gap-2 pb-2.5 border-b border-white/10">
                    <div class="flex items-center gap-1.5">
                        <span class="text-xs font-medium text-white">Yeni Nesil Dedektif (Elsa &amp; Ümit Hakan Karakaya)</span>
                        <span class="w-1.5 h-1.5 rounded-full bg-[#93F051]"></span>
                    </div>
                    <span class="px-2 py-0.5 rounded-full bg-[#93F051]/15 border border-[#93F051]/30 text-[#93F051] text-[9.5px] font-mono font-medium">${data.riskScore || 'DÜRÜST HUKUKİ ANALİZ'}</span>
                </div>"""

new_resp_header = """            <img src="assets/photos/elsa-dedektif-asistan.jpg" alt="Elsa & Ümit Hakan Karakaya" class="w-8 h-8 rounded-full border border-black/10 object-cover object-top shrink-0 mt-1 shadow-xs">
            <div class="bg-[#FFFFFF] border border-black/[0.14] rounded-2xl rounded-tl-sm p-4 sm:p-5 text-black max-w-[95%] sm:max-w-[85%] space-y-3.5 shadow-sm">
                <div class="flex flex-wrap items-center justify-between gap-2 pb-2.5 border-b border-black/[0.08]">
                    <div class="flex items-center gap-1.5">
                        <span class="text-xs font-medium text-black">Yeni Nesil Dedektif (Elsa &amp; Ümit Hakan Karakaya)</span>
                        <span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
                    </div>
                    <span class="px-2.5 py-0.5 rounded-full bg-black/[0.05] border border-black/[0.08] text-black text-[9.5px] font-mono font-medium">${data.riskScore || 'DÜRÜST HUKUKİ ANALİZ'}</span>
                </div>"""

js = js.replace(old_resp_header, new_resp_header)

# Accents in response body
js = js.replace('text-[#93F051] font-medium text-xs', 'text-black font-semibold text-xs')
js = js.replace('text-white/80', 'text-neutral-700')
js = js.replace('border-white/10', 'border-black/[0.08]')
js = js.replace('text-white/50', 'text-neutral-500')
js = js.replace('class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-[#25D366] hover:bg-[#20ba59] text-[#111111] font-medium text-xs transition"', 'class="inline-flex items-center gap-1.5 px-4 py-2 rounded-full bg-black hover:bg-neutral-800 text-white font-medium text-xs transition shadow-sm"')

with open("script.js", "w", encoding="utf-8") as f:
    f.write(js)
with open("Dat/script.js", "w", encoding="utf-8") as f:
    f.write(js)

print("✓ script.js ve Dat/script.js OpenAI stiline uyarlandı!")
