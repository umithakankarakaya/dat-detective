#!/usr/bin/env python3
"""
apply_exact_openai_screenshots.py
Systematically transforms index.html and Dat/index.html to match the 4 user screenshots of openai.com/tr-TR/:
1. Screenshot 1: Pure white header, "Nasıl yardımcı olabilirim?" Hero, rounded 720px input box with up arrow, prompt pills, widescreen feature banner.
2. Screenshot 2: "Öne Çıkan Dedektiflik Çözümlerimiz" 3-card grid with high-res cover photos.
3. Screenshot 3: "Son gelişmeler" vertical feed list with square thumbnails.
4. Screenshot 4: Pure white multi-column minimalist footer with social icons, copyright, "Çerezleri Yönet", and language selector pill.
5. ZERO GREEN throughout the entire document: all lime/neon greens replaced with sleek monochrome black/white.
"""

import os
import re

ROOT_INDEX = "index.html"
DAT_INDEX = "Dat/index.html"
BACKUP_INDEX = "index.backup-classic.html"

assert os.path.exists(ROOT_INDEX), "index.html not found!"
assert os.path.exists(BACKUP_INDEX), "Backup file index.backup-classic.html not found!"

with open(ROOT_INDEX, "r", encoding="utf-8") as f:
    content = f.read()

print(f"Original content length: {len(content)}")

# A. Set html and body tags
content = re.sub(r'<html[^>]*>', '<html lang="tr" class="light" data-theme="light">', content)
content = re.sub(
    r'<body id="top"[^>]*>',
    '<body id="top" class="bg-[#FFFFFF] text-[#000000] font-sans antialiased selection:bg-black selection:text-white relative overflow-x-clip transition-colors duration-200">',
    content
)

# B. Remove the dark obsidian ribbon above header (lines ~1633 to 1700)
# Look for <aside class="relative z-[45] bg-[#18181A] ... </aside>
ribbon_pattern = r'<!-- Matte Obsidian System Status Ribbon.*?-->\s*<aside class="relative z-\[45\] bg-\[#18181A\].*?</aside>'
m_ribbon = re.search(ribbon_pattern, content, flags=re.DOTALL)
if m_ribbon:
    print(f"Found and removing dark top ribbon ({len(m_ribbon.group(0))} chars)")
    content = content[:m_ribbon.start()] + content[m_ribbon.end():]
else:
    print("Dark ribbon not found via regex, searching exact tag...")
    start_str = '<aside class="relative z-[45] bg-[#18181A]'
    pos1 = content.find(start_str)
    if pos1 != -1:
        pos2 = content.find('</aside>', pos1)
        if pos2 != -1:
            content = content[:pos1] + content[pos2 + len('</aside>'):]
            print("Removed dark ribbon via index slice.")

# C. Build OpenAI Exact Hero + Section 1 Banner + Section 2 (3-Cards) + Section 3 (Feed)
openai_hero_and_sections = '''<!-- 1. HERO SECTION: OPENAI EXACT "NASIL YARDIMCI OLABİLİRİM?" (Screenshot 1) -->
        <section id="dedektife-sor" class="relative bg-[#FFFFFF] text-[#000000] pt-14 sm:pt-20 pb-12 sm:pb-16 overflow-hidden">
            <div class="max-w-4xl mx-auto px-4 sm:px-6 relative z-10">

                <!-- OpenAI Exact Centered Headline ("Nasıl yardımcı olabilirim?") -->
                <div class="text-center space-y-3 mb-8 sm:mb-10">
                    <h1 class="text-3xl sm:text-4xl lg:text-[42px] font-medium tracking-[-0.03em] text-[#000000] leading-tight">
                        Nasıl yardımcı olabilirim?
                    </h1>
                    <p class="text-sm sm:text-base text-[#595959] font-normal max-w-xl mx-auto leading-relaxed">
                        20 yıllık resmi adli tecrübeyle; eş takibinden velayet davalarına, mahkeme delillerinden böcek aramaya vakanızı doğrudan analiz edin.
                    </p>
                </div>

                <!-- OpenAI Exact Console Card (max-w-[720px], rounded-[28px], 1px border, subtle shadow) -->
                <div id="aiChatInputWrap" class="openai-box-white max-w-[720px] mx-auto rounded-[28px] border border-black/[0.14] bg-[#FFFFFF] shadow-[0_2px_14px_rgba(0,0,0,0.04)] hover:shadow-[0_4px_20px_rgba(0,0,0,0.08)] transition-all p-4 sm:p-5 relative">
                    <!-- Textarea Input Area -->
                    <textarea id="aiChatInput" rows="2" placeholder="Boşanma delili, eş takibi, velayet veya dedektiflik ücreti hakkında bir soru yazın..." class="w-full bg-transparent text-sm sm:text-base text-black placeholder:text-neutral-400 focus:outline-none resize-none border-0 p-0 font-normal leading-relaxed"></textarea>

                    <!-- Console Bottom Row: Assistant Mode & Round Send Button -->
                    <div class="flex items-center justify-between pt-3 mt-1 border-t border-black/[0.08]">
                        <div class="flex items-center gap-2">
                            <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-black/[0.05] text-[11px] font-medium text-black">
                                <span class="w-1.5 h-1.5 rounded-full bg-black"></span>
                                <span>Elsa v2.0 • 7/24 Şifreli Danışma</span>
                            </span>
                            <span class="text-[11px] text-neutral-500 hidden sm:inline">UÖDED Standartlarında Gizlilik</span>
                        </div>

                        <!-- Circular Send Button (OpenAI Exact 32px Round Arrow Button) -->
                        <button type="button" id="aiSendBtn" onclick="sendAIChatMessage()" class="w-8 h-8 rounded-full bg-[#000000] hover:bg-neutral-800 text-white flex items-center justify-center transition active:scale-95 shrink-0 shadow-xs cursor-pointer" title="Soruyu Yanıtla">
                            <i class="hgi hgi-stroke hgi-arrow-up-01 w-4 h-4 text-white"></i>
                        </button>
                    </div>
                </div>

                <!-- OpenAI Prompt Suggestion Pills (Centered Horizontal List) -->
                <div class="flex items-center justify-center gap-2 flex-wrap mt-4 text-sm" id="aiQuickChips">
                    <button type="button" onclick="selectAIChatPreset('dedektif-tutmak')" class="openai-pill-white px-3.5 py-1.5 rounded-full border border-black/[0.12] bg-[#FFFFFF] hover:bg-black/[0.04] text-[#000000] text-xs sm:text-[13px] transition font-normal shrink-0 shadow-xs">Dedektif ile Sohbet Edin</button>
                    <button type="button" onclick="selectAIChatPreset('aldatan-erkek')" class="openai-pill-white px-3.5 py-1.5 rounded-full border border-black/[0.12] bg-[#FFFFFF] hover:bg-black/[0.04] text-[#000000] text-xs sm:text-[13px] transition font-normal shrink-0 shadow-xs">Eş Takibi &amp; Aldatma</button>
                    <button type="button" onclick="selectAIChatPreset('delil-gecerliligi')" class="openai-pill-white px-3.5 py-1.5 rounded-full border border-black/[0.12] bg-[#FFFFFF] hover:bg-black/[0.04] text-[#000000] text-xs sm:text-[13px] transition font-normal shrink-0 shadow-xs">Mahkemede Delil Geçerliliği</button>
                    <button type="button" onclick="selectAIChatPreset('dedektif-ucretleri')" class="openai-pill-white px-3.5 py-1.5 rounded-full border border-black/[0.12] bg-[#FFFFFF] hover:bg-black/[0.04] text-[#000000] text-xs sm:text-[13px] transition font-normal shrink-0 shadow-xs">Dedektiflik Ücretleri</button>
                    <button type="button" onclick="selectAIChatPreset('cocuk-velayeti')" class="openai-pill-white px-3.5 py-1.5 rounded-full border border-black/[0.12] bg-[#FFFFFF] hover:bg-black/[0.04] text-[#000000] text-xs sm:text-[13px] transition font-normal shrink-0 shadow-xs">Velayet &amp; Delil</button>
                    <button type="button" onclick="selectAIChatPreset('bocek-arama')" class="openai-pill-white px-3.5 py-1.5 rounded-full border border-black/[0.12] bg-[#FFFFFF] hover:bg-black/[0.04] text-[#000000] text-xs sm:text-[13px] transition font-normal shrink-0 shadow-xs">Böcek Arama &amp; TSCM</button>
                    <button type="button" onclick="selectAIChatPreset('miras-borclu')" class="openai-pill-white px-3.5 py-1.5 rounded-full border border-black/[0.12] bg-[#FFFFFF] hover:bg-black/[0.04] text-[#000000] text-xs sm:text-[13px] transition font-normal shrink-0 shadow-xs">Daha fazla</button>
                </div>

                <!-- Live Conversation Messages Container (Hidden initially until asked or clicked) -->
                <div class="max-w-[720px] mx-auto mt-6 space-y-4 empty:hidden" id="aiChatMessages">
                    <div class="flex items-start gap-3 text-left animate-fadeIn">
                        <img src="assets/photos/elsa-dedektif-asistan.jpg" alt="Elsa &amp; Ümit Hakan Karakaya" class="w-8 h-8 rounded-full border border-black/10 object-cover object-top shrink-0 mt-1 shadow-xs">
                        <div class="bg-[#F7F7F8] border border-black/[0.08] rounded-2xl rounded-tl-sm p-4 sm:p-5 text-black max-w-[95%] sm:max-w-[85%] space-y-3 shadow-xs">
                            <div class="flex items-center justify-between pb-2 border-b border-black/[0.08]">
                                <div class="flex items-center gap-1.5">
                                    <span class="text-xs font-medium text-black">Yeni Nesil Dedektif (Elsa &amp; Ümit Hakan Karakaya)</span>
                                    <span class="w-1.5 h-1.5 rounded-full bg-black"></span>
                                </div>
                                <span class="text-[10px] font-mono text-neutral-500">Çevrimiçi</span>
                            </div>
                            <div class="text-xs sm:text-[13.5px] leading-relaxed text-black/85 space-y-2 font-normal">
                                <p>Merhaba! Ben DAT Özel Dedektiflik'in Yeni Nesil Dijital Asistanı <strong>Elsa</strong>. Kurucumuz <strong>Ümit Hakan Karakaya</strong>'nın 20 yılı aşkın adli saha tecrübesiyle buradayım.</p>
                                <p>Sorularınızı <strong>doğrulama yanılgısına kapılmadan</strong>, dürüst, gerçekçi ve mahkemede (HMK m.189/199) tek celsede geçerli hukuki perspektifle yanıtlıyorum.</p>
                            </div>
                        </div>
                    </div>
                </div>

            </div>

            <!-- FEATURE BANNER: OPENAI EXACT "CYBER AT FRONTIER" BANNER (Screenshot 1 Bottom) -->
            <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 mt-12 sm:mt-16">
                <div class="relative rounded-3xl overflow-hidden aspect-[16/7] sm:aspect-[21/7] bg-black text-white flex flex-col justify-between p-6 sm:p-10 lg:p-12 shadow-sm border border-black/10">
                    <img src="assets/og-banner.jpg" alt="DAT Özel Dedektiflik Adli Saha Masası" class="absolute inset-0 w-full h-full object-cover opacity-35 filter brightness-90">
                    <div class="relative z-10 flex items-center justify-between">
                        <span class="text-lg sm:text-2xl font-bold tracking-tight text-white">DAT Dedektiflik</span>
                        <span class="text-[11px] sm:text-xs font-mono uppercase tracking-wider text-white/90 border border-white/20 bg-black/40 backdrop-blur-md px-3 py-1 rounded-full">Soruşturma &amp; Adli Kanıt Masası</span>
                    </div>
                    <div class="relative z-10 max-w-2xl space-y-2">
                        <h2 class="text-xl sm:text-3xl lg:text-4xl font-semibold tracking-tight text-white leading-tight">
                            Yargıtay Uyumlu Adli Delil ve 81 İlde Gizli Saha Operasyonları
                        </h2>
                        <p class="text-xs sm:text-sm text-white/80 font-normal leading-relaxed">
                            20 yıllık resmi kurumsal tecrübe, HMK m.189/199 ve TCK m.134 tam yasal güvencesiyle tek celsede kabul gören mahkeme delilleri.
                        </p>
                    </div>
                </div>
            </div>

            <!-- 4 Metrics Row (OpenAI Minimalist Row) -->
            <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 pt-10 mt-6 grid grid-cols-2 lg:grid-cols-4 gap-6 text-center sm:text-left border-t border-black/[0.08]">
                <div class="space-y-1">
                    <div class="text-2xl sm:text-3xl font-medium text-black tracking-tight">20+ Yıl</div>
                    <div class="text-xs text-[#595959]">Resmi Kurumsal Adli Tecrübe (2004–2026)</div>
                </div>
                <div class="space-y-1">
                    <div class="text-2xl sm:text-3xl font-medium text-black tracking-tight">4.000+</div>
                    <div class="text-xs text-[#595959]">Mahkemelerde Kabul Edilen Sonuçlu Vaka</div>
                </div>
                <div class="space-y-1">
                    <div class="text-2xl sm:text-3xl font-medium text-black tracking-tight">%100 Yasal</div>
                    <div class="text-xs text-[#595959]">HMK m.199 ve TCK m.134 Delil Güvencesi</div>
                </div>
                <div class="space-y-1">
                    <div class="text-2xl sm:text-3xl font-medium text-black tracking-tight">81 İl</div>
                    <div class="text-xs text-[#595959]">Türkiye Geneli 7/24 Mobil Saha Operasyonu</div>
                </div>
            </div>

        </section>

        <!-- 2. OPENAI SECTION: EN YENİ DUYURULAR / 3-CARD GRID (Screenshot 2) -->
        <section class="py-14 sm:py-20 bg-[#FFFFFF] border-t border-black/[0.08]">
            <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
                <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-4 mb-8 sm:mb-12">
                    <div>
                        <h2 class="text-2xl sm:text-4xl font-semibold tracking-tight text-black">Öne Çıkan Dedektiflik Çözümlerimiz</h2>
                        <div class="flex items-center gap-2 mt-2 text-xs text-neutral-500">
                            <span class="font-medium text-black">Resmi Büro</span>
                            <span>12 Kas 2026</span>
                        </div>
                    </div>
                    <a href="#hizmetler" class="inline-flex items-center gap-1.5 text-sm font-medium text-black hover:opacity-70 transition">
                        <span>Tüm Hizmetleri İncele</span>
                        <span class="font-mono">&gt;</span>
                    </a>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-3 gap-6 sm:gap-8">
                    <!-- Card 1 -->
                    <a href="#hizmetler" class="group block space-y-3">
                        <div class="rounded-2xl overflow-hidden aspect-[4/3] bg-neutral-100 border border-black/[0.08]">
                            <img src="assets/services/es-takibi.jpg" alt="Eş Takibi ve Aldatma Tespiti" class="w-full h-full object-cover group-hover:scale-105 transition duration-500">
                        </div>
                        <h3 class="text-lg sm:text-xl font-semibold text-black group-hover:opacity-75 transition leading-snug">
                            Eş Takibi ve Sadakat Araştırması ile tanışın
                        </h3>
                        <div class="flex items-center gap-2 text-xs text-neutral-500">
                            <span class="font-medium text-black">Aile Hukuku</span>
                            <span>•</span>
                            <span>HMK m.189 Uyumlu Rapor</span>
                        </div>
                    </a>

                    <!-- Card 2 -->
                    <a href="#dedektife-sor" class="group block space-y-3">
                        <div class="rounded-2xl overflow-hidden aspect-[4/3] bg-neutral-100 border border-black/[0.08]">
                            <img src="assets/photos/elsa-dedektif-asistan.jpg" alt="Elsa Yapay Zeka Danışmanı" class="w-full h-full object-cover group-hover:scale-105 transition duration-500">
                        </div>
                        <h3 class="text-lg sm:text-xl font-semibold text-black group-hover:opacity-75 transition leading-snug">
                            Elsa 2.0: Yeni Nesil Yapay Zeka Danışmanı
                        </h3>
                        <div class="flex items-center gap-2 text-xs text-neutral-500">
                            <span class="font-medium text-black">Teknoloji &amp; Ön Analiz</span>
                            <span>•</span>
                            <span>7/24 Şifreli &amp; Anonim</span>
                        </div>
                    </a>

                    <!-- Card 3 -->
                    <a href="#hizmetler" class="group block space-y-3">
                        <div class="rounded-2xl overflow-hidden aspect-[4/3] bg-neutral-100 border border-black/[0.08]">
                            <img src="assets/services/firma-arastirmalari.jpg" alt="Böcek ve Casus Yazılım Arama" class="w-full h-full object-cover group-hover:scale-105 transition duration-500">
                        </div>
                        <h3 class="text-lg sm:text-xl font-semibold text-black group-hover:opacity-75 transition leading-snug">
                            TSCM Böcek ve Elektronik Dinleme Cihazı Tespiti
                        </h3>
                        <div class="flex items-center gap-2 text-xs text-neutral-500">
                            <span class="font-medium text-black">Teknik Güvenlik</span>
                            <span>•</span>
                            <span>Ev, Ofis ve Araç Taraması</span>
                        </div>
                    </a>
                </div>
            </div>
        </section>

        <!-- 3. OPENAI SECTION: SON GELİŞMELER / VERTICAL FEED LIST (Screenshot 3) -->
        <section class="py-14 sm:py-20 bg-[#FFFFFF] border-t border-black/[0.08]">
            <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
                <div class="flex items-center justify-between mb-8 sm:mb-12">
                    <h2 class="text-2xl sm:text-3xl font-semibold tracking-tight text-black">Son gelişmeler</h2>
                    <a href="#makaleler" class="text-sm font-medium text-black hover:opacity-70 transition">Daha fazlasını gör</a>
                </div>

                <div class="space-y-6 sm:space-y-8">
                    <!-- Feed Item 1 -->
                    <div class="flex items-center gap-5 sm:gap-6 group cursor-pointer" onclick="document.querySelector('#makaleler')?.scrollIntoView({behavior: 'smooth'})">
                        <div class="w-20 h-20 sm:w-28 sm:h-28 rounded-2xl bg-gradient-to-br from-amber-500 via-orange-500 to-rose-600 shrink-0 overflow-hidden shadow-xs"></div>
                        <div class="space-y-1.5 flex-1 min-w-0">
                            <h3 class="text-base sm:text-lg font-semibold text-black group-hover:opacity-70 transition leading-snug">
                                Boşanma Davalarında Sosyal Medya ve WhatsApp Yazışmalarının Mahkeme Delil Gücü
                            </h3>
                            <div class="flex items-center gap-2 text-xs text-neutral-500">
                                <span class="font-medium text-black">Hukuki Görüş</span>
                                <span>29 Eki 2026</span>
                            </div>
                        </div>
                    </div>

                    <!-- Feed Item 2 -->
                    <div class="flex items-center gap-5 sm:gap-6 group cursor-pointer" onclick="document.querySelector('#makaleler')?.scrollIntoView({behavior: 'smooth'})">
                        <div class="w-20 h-20 sm:w-28 sm:h-28 rounded-2xl bg-gradient-to-br from-amber-300 via-yellow-500 to-amber-600 shrink-0 overflow-hidden shadow-xs"></div>
                        <div class="space-y-1.5 flex-1 min-w-0">
                            <h3 class="text-base sm:text-lg font-semibold text-black group-hover:opacity-70 transition leading-snug">
                                Ticari Casusluk ve Şirket İçi Bilgi Sızıntılarının Adli Bilişim Tespiti
                            </h3>
                            <div class="flex items-center gap-2 text-xs text-neutral-500">
                                <span class="font-medium text-black">Kurumsal Güvenlik</span>
                                <span>24 Eki 2026</span>
                            </div>
                        </div>
                    </div>

                    <!-- Feed Item 3 -->
                    <div class="flex items-center gap-5 sm:gap-6 group cursor-pointer" onclick="document.querySelector('#makaleler')?.scrollIntoView({behavior: 'smooth'})">
                        <div class="w-20 h-20 sm:w-28 sm:h-28 rounded-2xl bg-gradient-to-br from-blue-400 via-indigo-500 to-pink-500 shrink-0 overflow-hidden shadow-xs"></div>
                        <div class="space-y-1.5 flex-1 min-w-0">
                            <h3 class="text-base sm:text-lg font-semibold text-black group-hover:opacity-70 transition leading-snug">
                                Velayet Uyuşmazlıklarında Çocuğun Üstün Yararı ve Yaşam Tarzı Tespiti
                            </h3>
                            <div class="flex items-center gap-2 text-xs text-neutral-500">
                                <span class="font-medium text-black">Aile Hukuku</span>
                                <span>18 Eki 2026</span>
                            </div>
                        </div>
                    </div>

                    <!-- Feed Item 4 -->
                    <div class="flex items-center gap-5 sm:gap-6 group cursor-pointer" onclick="document.querySelector('#makaleler')?.scrollIntoView({behavior: 'smooth'})">
                        <div class="w-20 h-20 sm:w-28 sm:h-28 rounded-2xl bg-gradient-to-br from-emerald-500 via-teal-600 to-cyan-700 shrink-0 overflow-hidden shadow-xs"></div>
                        <div class="space-y-1.5 flex-1 min-w-0">
                            <h3 class="text-base sm:text-lg font-semibold text-black group-hover:opacity-70 transition leading-snug">
                                Almanya ve Avrupa Gurbetçi Aileleri İçin Sınır Ötesi Araştırma Masası
                            </h3>
                            <div class="flex items-center gap-2 text-xs text-neutral-500">
                                <span class="font-medium text-black">Uluslararası</span>
                                <span>12 Eki 2026</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>'''

# Replace exactly from `<section id="dedektife-sor"` to its closing `</section>`
hero_start = content.find('<section id="dedektife-sor"')
assert hero_start != -1, "Cannot find <section id='dedektife-sor'"
hero_end = content.find('</section>', hero_start) + len('</section>')
print(f"Replacing hero section from index {hero_start} to {hero_end}")
content = content[:hero_start] + openai_hero_and_sections + content[hero_end:]

# D. Build OpenAI Exact Multi-Column Pure White Footer (Screenshot 4)
openai_footer = '''<footer class="bg-[#FFFFFF] border-t border-black/[0.08] pt-16 pb-28 lg:pb-16 text-neutral-600 text-xs font-normal">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            
            <!-- Top Logo & Brand Row -->
            <div class="flex items-center justify-between pb-10 border-b border-black/[0.08] mb-12">
                <a href="/" class="flex items-center gap-2.5 text-black hover:opacity-80 transition">
                    <img src="dat-logo.png" alt="DAT Özel Dedektiflik Logo" class="w-7 h-7 rounded-full object-cover">
                    <span class="text-base font-semibold tracking-tight text-black">DAT <span class="font-normal text-neutral-500">Dedektiflik</span></span>
                </a>
                <span class="text-[11px] text-neutral-500 font-mono">UÖDED Kurucusu • Sertifikalı Büro</span>
            </div>

            <!-- Multi-Column Links Grid (Screenshot 4 Style) -->
            <div class="grid grid-cols-2 md:grid-cols-5 gap-8 sm:gap-10 mb-16 text-left">
                
                <!-- Column 1: Araştırma & Hizmetler -->
                <div class="space-y-3">
                    <h4 class="text-black font-semibold text-sm tracking-tight">Hizmetler</h4>
                    <ul class="space-y-2.5 text-xs text-neutral-600">
                        <li><a href="#hizmetler" class="hover:text-black transition">Eş Takibi &amp; Aldatma</a></li>
                        <li><a href="#hizmetler" class="hover:text-black transition">Boşanma Delili Toplama</a></li>
                        <li><a href="#hizmetler" class="hover:text-black transition">Velayet &amp; Çocuk Koruma</a></li>
                        <li><a href="#hizmetler" class="hover:text-black transition">Böcek Arama (TSCM)</a></li>
                        <li><a href="#hizmetler" class="hover:text-black transition">Adres &amp; Borçlu Tespiti</a></li>
                        <li><a href="#hizmetler" class="hover:text-black transition">Firma &amp; Şirket Araştırması</a></li>
                        <li><a href="#hizmetler" class="hover:text-black transition">Bilişim &amp; Dolandırıcılık</a></li>
                    </ul>
                </div>

                <!-- Column 2: 81 İl Dedektif Ağı -->
                <div class="space-y-3">
                    <h4 class="text-black font-semibold text-sm tracking-tight">Bölgeler</h4>
                    <ul class="space-y-2.5 text-xs text-neutral-600">
                        <li><a href="#turkiye-dedektif-agi" class="hover:text-black transition">Ankara Dedektiflik</a></li>
                        <li><a href="#turkiye-dedektif-agi" class="hover:text-black transition">İstanbul Özel Dedektiflik</a></li>
                        <li><a href="#turkiye-dedektif-agi" class="hover:text-black transition">İzmir Özel Dedektiflik</a></li>
                        <li><a href="#turkiye-dedektif-agi" class="hover:text-black transition">Bursa &amp; Antalya Masası</a></li>
                        <li><a href="#turkiye-dedektif-agi" class="hover:text-black transition">81 İl Operasyon Ağı</a></li>
                        <li><a href="#avrupa-masasi" class="hover:text-black transition">Avrupa Masası (Almanya)</a></li>
                        <li><a href="#arama-rehberi" class="hover:text-black transition">İl &amp; İlçe Arama Rehberi</a></li>
                    </ul>
                </div>

                <!-- Column 3: Hukuk & Delil Standartları -->
                <div class="space-y-3">
                    <h4 class="text-black font-semibold text-sm tracking-tight">Hukuk &amp; Mevzuat</h4>
                    <ul class="space-y-2.5 text-xs text-neutral-600">
                        <li><a href="#delil-standartlari" class="hover:text-black transition">HMK m.189/199 Delil Kriteri</a></li>
                        <li><a href="#delil-standartlari" class="hover:text-black transition">TCK m.134 Casus Yazılım Yasağı</a></li>
                        <li><a href="#delil-standartlari" class="hover:text-black transition">Yargıtay Emsal Kararları</a></li>
                        <li><button type="button" onclick="openLegalModal('gizlilik')" class="hover:text-black transition text-left">Gizlilik Taahhütnamesi</button></li>
                        <li><button type="button" onclick="openLegalModal('kvkk')" class="hover:text-black transition text-left">KVKK Aydınlatma Metni</button></li>
                        <li><button type="button" onclick="openLegalModal('sozlesme')" class="hover:text-black transition text-left">Resmi Sözleşme Prosedürü</button></li>
                    </ul>
                </div>

                <!-- Column 4: Kurumsal -->
                <div class="space-y-3">
                    <h4 class="text-black font-semibold text-sm tracking-tight">Kurumsal</h4>
                    <ul class="space-y-2.5 text-xs text-neutral-600">
                        <li><a href="#mimari" class="hover:text-black transition">Hakkımızda</a></li>
                        <li><a href="#mimari" class="hover:text-black transition">Ümit Hakan Karakaya</a></li>
                        <li><a href="#mimari" class="hover:text-black transition">UÖDED Kuruculuğu</a></li>
                        <li><a href="#makaleler" class="hover:text-black transition">Basın &amp; Televizyon</a></li>
                        <li><a href="#vaka-sureci" class="hover:text-black transition">Çalışma Metodolojisi</a></li>
                        <li><a href="#ofislerimiz" class="hover:text-black transition">Ankara Çankaya Merkez Büro</a></li>
                    </ul>
                </div>

                <!-- Column 5: İletişim & Destek -->
                <div class="space-y-3">
                    <h4 class="text-black font-semibold text-sm tracking-tight">İletişim &amp; Destek</h4>
                    <ul class="space-y-2.5 text-xs text-neutral-600">
                        <li><a href="tel:+903122840299" class="hover:text-black font-medium text-black transition">0312 284 02 99</a></li>
                        <li><a href="https://wa.me/905326667749" target="_blank" rel="noopener noreferrer" class="hover:text-black font-medium text-black transition">0532 666 77 49 (WhatsApp)</a></li>
                        <li><a href="#dedektife-sor" class="hover:text-black transition">Elsa Yapay Zeka Danışmanı</a></li>
                        <li><a href="#sss" class="hover:text-black transition">Sıkça Sorulan Sorular (S.S.S.)</a></li>
                        <li><a href="#vaka-bildir" class="hover:text-black transition">Gizli Teklif Formu</a></li>
                    </ul>
                </div>

            </div>

            <!-- Bottom Row: Social Icons, Copyright, Language Selector (Screenshot 4 Bottom) -->
            <div class="pt-8 border-t border-black/[0.08] flex flex-col sm:flex-row items-center justify-between gap-4">
                
                <!-- Social Media Minimal Icons -->
                <div class="flex items-center gap-4 text-neutral-700">
                    <a href="https://twitter.com/datdedektiflik" target="_blank" rel="noopener noreferrer" class="hover:text-black transition" title="X (Twitter)">
                        <i class="hgi hgi-stroke hgi-new-twitter w-4 h-4"></i>
                    </a>
                    <a href="https://youtube.com/@datdedektiflik" target="_blank" rel="noopener noreferrer" class="hover:text-black transition" title="YouTube">
                        <i class="hgi hgi-stroke hgi-youtube w-4 h-4"></i>
                    </a>
                    <a href="https://linkedin.com/company/datdedektiflik" target="_blank" rel="noopener noreferrer" class="hover:text-black transition" title="LinkedIn">
                        <i class="hgi hgi-stroke hgi-linkedin-02 w-4 h-4"></i>
                    </a>
                    <a href="https://instagram.com/datdedektiflik" target="_blank" rel="noopener noreferrer" class="hover:text-black transition" title="Instagram">
                        <i class="hgi hgi-stroke hgi-instagram w-4 h-4"></i>
                    </a>
                </div>

                <!-- Copyright & Cookie -->
                <div class="flex items-center gap-4 text-xs text-neutral-500">
                    <span>DAT Özel Dedektiflik © 2004–2026</span>
                    <button type="button" onclick="openLegalModal('cookie')" class="hover:text-black transition underline">Çerezleri Yönet</button>
                </div>

                <!-- Language Pill (OpenAI Style) -->
                <div class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-black/[0.04] text-xs font-medium text-black border border-black/[0.08]">
                    <i class="hgi hgi-stroke hgi-globe-02 w-3.5 h-3.5"></i>
                    <span>Türkçe</span>
                </div>

            </div>

        </div>
    </footer>'''

# Replace exactly from `<footer` to `</footer>`
footer_start = content.find('<footer')
assert footer_start != -1, "Cannot find <footer"
footer_end = content.find('</footer>', footer_start) + len('</footer>')
print(f"Replacing footer from index {footer_start} to {footer_end}")
content = content[:footer_start] + openai_footer + content[footer_end:]

# E. Fix the SVG Metaball in `mimari` (no green #93F051!)
content = content.replace('fill="#93F051"', 'fill="#000000"')
content = content.replace('drop-shadow-[0_14px_28px_rgba(147,240,81,0.28)]', 'drop-shadow-[0_8px_20px_rgba(0,0,0,0.12)]')
content = content.replace('decoration-[#93F051]', 'decoration-black')
content = content.replace('underline decoration-4 underline-offset-4', '')
# Make sure the text on top of the black metaball is white
content = content.replace('font-normal text-[#111111] leading-none tracking-tight">2005<', 'font-normal text-white leading-none tracking-tight">2005<')
content = content.replace('text-[10px] font-medium text-[#111111]/80 mt-1">Kuruluş Yılı<', 'text-[10px] font-medium text-white/80 mt-1">Kuruluş Yılı<')
content = content.replace('font-normal text-[#111111] leading-none tracking-tight">4.000+<', 'font-normal text-white leading-none tracking-tight">4.000+<')
content = content.replace('text-[10px] font-medium text-[#111111]/80 mt-1">Çözümlenen Dosya<', 'text-[10px] font-medium text-white/80 mt-1">Çözümlenen Dosya<')

# F. Transform dark section backgrounds to light/white
content = content.replace('section id="makaleler" class="py-12 sm:py-16 bg-[#111111] text-[#FFFFFF]"', 'section id="makaleler" class="py-14 sm:py-20 bg-[#FFFFFF] text-[#000000] border-t border-black/[0.08]"')
content = content.replace('section id="vaka-bildir" class="py-12 sm:py-16 bg-[#111111] text-[#FFFFFF]"', 'section id="vaka-bildir" class="py-14 sm:py-20 bg-[#FFFFFF] text-[#000000] border-t border-black/[0.08]"')
content = content.replace('section id="arama-rehberi" class="py-14 sm:py-20 bg-[#111111] text-[#FFFFFF] border-t border-white/10 relative"', 'section id="arama-rehberi" class="py-14 sm:py-20 bg-[#FFFFFF] text-[#000000] border-t border-black/[0.08] relative"')
content = content.replace('section id="turkiye-dedektif-agi" class="py-14 sm:py-20 bg-[#141416] text-[#FFFFFF] border-y border-white/10 relative"', 'section id="turkiye-dedektif-agi" class="py-14 sm:py-20 bg-[#FFFFFF] text-[#000000] border-t border-black/[0.08] relative"')
content = content.replace('bg-[#F2F2F2]', 'bg-[#FFFFFF]')

# G. Replace all occurrences of #93F051 and #DDF95E with #000000
content = content.replace('#93F051', '#000000')
content = content.replace('#DDF95E', '#000000')

# H. Update Desktop Floating Dock to OpenAI Monochrome Style
desktop_dock_match = re.search(r'<div id="desktopFloatingDock"[^>]*>.*?</div>\s*</div>', content, flags=re.DOTALL)
if desktop_dock_match:
    openai_desktop_dock = '''<div id="desktopFloatingDock" class="hidden lg:flex fixed fixed-gpu bottom-5 right-5 z-50 flex-row flex-wrap justify-end items-center gap-2 max-w-[calc(100vw-2.5rem)]">
        <a href="https://wa.me/905326667749?text=Merhaba%2C%20DAT%20Dedektiflik%20hakk%C4%B1nda%20gizli%20dan%C4%B1%C5%9Fmanl%C4%B1k%20almak%20istiyorum." target="_blank" rel="noopener noreferrer" title="WhatsApp Danışma Hattı: +90 532 666 77 49" class="group inline-flex items-center gap-2 bg-black hover:bg-neutral-800 text-white text-[12px] font-medium py-2 px-4 rounded-full shadow-lg border border-black transition-all active:scale-95 whitespace-nowrap">
            <i class="hgi hgi-stroke hgi-whatsapp w-3.5 h-3.5 text-white shrink-0"></i>
            <span class="tracking-tight">WhatsApp Danış ↗</span>
        </a>
        <a href="tel:+903122840299" title="7/24 Merkez Danışma Hattı: 0312 284 02 99" class="inline-flex items-center gap-2 bg-white hover:bg-neutral-100 text-black text-[12px] font-medium py-2 px-4 rounded-full shadow-lg border border-black/15 transition-all active:scale-95 whitespace-nowrap">
            <i class="hgi hgi-stroke hgi-call-02 w-3.5 h-3.5 text-black shrink-0"></i>
            <span class="tracking-tight">0312 284 02 99</span>
        </a>
    </div>'''
    content = content[:desktop_dock_match.start()] + openai_desktop_dock + content[desktop_dock_match.end():]

# I. Clean & Enforce Master OpenAI CSS System in <head>
css_system = '''<!-- OpenAI Exact Fonts & Design System Override -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style id="openai-master-system">
        :root, html, body {
            background-color: #FFFFFF !important;
            color: #000000 !important;
            font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
            letter-spacing: -0.012em;
        }

        h1, h2, h3, h4, h5, h6 {
            font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
            letter-spacing: -0.025em !important;
            color: #000000 !important;
        }

        /* SIFIR YEŞİL - TAM MONOKROM OPENAI SİSTEMİ */
        *:not(.hgi):not([class*="hgi-"]) {
            border-color: rgba(0, 0, 0, 0.08);
        }

        /* Tüm yeşil öğeleri siyaha ve beyaza zorla */
        .text-green-500, .text-green-600, .text-emerald-500, .text-emerald-600,
        [class*="text-[#93F051]"], [class*="text-[#25D366]"], [class*="text-[#DDF95E]"] {
            color: #000000 !important;
        }

        .bg-green-500, .bg-green-600, .bg-emerald-500, .bg-emerald-600,
        [class*="bg-[#93F051]"], [class*="bg-[#25D366]"], [class*="bg-[#DDF95E]"] {
            background-color: #000000 !important;
            color: #FFFFFF !important;
        }

        /* Pulse Dot yeşil olamaz, monokrom siyah */
        .pulse-dot {
            background-color: #000000 !important;
        }

        /* Konsol Kutusu ve Haplar */
        #aiChatInputWrap, .openai-box-white {
            background-color: #FFFFFF !important;
            border: 1px solid rgba(0, 0, 0, 0.14) !important;
            box-shadow: 0 2px 14px rgba(0, 0, 0, 0.04) !important;
        }
        #aiChatInputWrap:focus-within {
            border-color: rgba(0, 0, 0, 0.35) !important;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08) !important;
        }

        #aiQuickChips button, .openai-pill-white {
            background-color: #FFFFFF !important;
            border: 1px solid rgba(0, 0, 0, 0.12) !important;
            color: #000000 !important;
        }
        #aiQuickChips button:hover, .openai-pill-white:hover {
            background-color: rgba(0, 0, 0, 0.04) !important;
            border-color: rgba(0, 0, 0, 0.20) !important;
        }

        #aiSendBtn {
            background-color: #000000 !important;
            color: #FFFFFF !important;
            border-radius: 9999px !important;
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

        /* Navbar */
        #openai-nav {
            background-color: rgba(255, 255, 255, 0.95) !important;
            border-bottom: 1px solid rgba(0, 0, 0, 0.08) !important;
        }
    </style>'''

# Place css_system right before </head>
head_end = content.find('</head>')
assert head_end != -1, "Cannot find </head>"
content = content[:head_end] + css_system + "\n" + content[head_end:]

# Write to root index.html
with open(ROOT_INDEX, "w", encoding="utf-8") as f:
    f.write(content)

# Write to Dat/index.html mirror
with open(DAT_INDEX, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Done! New content length: {len(content)}")
