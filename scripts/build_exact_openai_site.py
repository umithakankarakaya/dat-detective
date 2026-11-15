# -*- coding: utf-8 -*-
import os
import re

def build_site():
    print("=== OPENAI.COM/TR-TR TAM BEYAZ & FONT DÖNÜŞÜMÜ BAŞLIYOR ===")
    
    with open("index.backup-classic.html", "r", encoding="utf-8") as f:
        html = f.read()

    # 1. OpenAI Font & CSS System
    openai_head_css = """
    <!-- OpenAI Exact Typography & Color System -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style id="openai-exact-system">
        :root {
            --font-openai: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            --color-bg-primary: #FFFFFF;
            --color-text-primary: #000000;
            --color-text-secondary: #595959;
            --color-border-subtle: rgba(0, 0, 0, 0.12);
        }

        body {
            font-family: var(--font-openai) !important;
            letter-spacing: -0.015em;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }

        h1, h2, h3, h4, h5, h6, .apple-heading {
            font-family: var(--font-openai) !important;
            letter-spacing: -0.025em !important;
        }

        /* OpenAI Card Styles */
        .openai-card {
            background-color: #FFFFFF !important;
            border: 1px solid rgba(0, 0, 0, 0.12) !important;
            border-radius: 24px !important;
            transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
        }
        .openai-card:hover {
            border-color: rgba(0, 0, 0, 0.24) !important;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04) !important;
        }
    </style>
    """

    if 'id="openai-exact-system"' not in html:
        html = html.replace('</head>', openai_head_css + '\n</head>')

    # 2. Header (Navbar) - OpenAI Pure White Minimalist Header
    header_start = html.find('<header')
    header_end = html.find('</header>') + len('</header>')
    
    openai_header = """<!-- OPENAI EXACT NAVBAR -->
    <header id="openai-nav" class="sticky top-0 z-50 bg-white/95 backdrop-blur-md border-b border-black/[0.08] text-black">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between gap-4">
            
            <!-- Left: Brand / Logo -->
            <div class="flex items-center gap-8">
                <a href="/" class="flex items-center gap-2.5 text-black hover:opacity-80 transition group" title="DAT Özel Dedektiflik — Ana Sayfa">
                    <img src="dat-logo.png" alt="DAT Logo" class="w-7 h-7 rounded-full object-cover">
                    <span class="text-[17px] font-semibold tracking-[-0.03em] text-black">DAT <span class="font-normal text-neutral-600">Dedektiflik</span></span>
                </a>

                <!-- Desktop Nav Links -->
                <nav class="hidden lg:flex items-center gap-6 text-[14px] font-normal text-black/80">
                    <a href="#hizmetler" class="hover:text-black transition">12 Hizmet</a>
                    <a href="#delil-standartlari" class="hover:text-black transition">Delil &amp; Hukuk</a>
                    <a href="#turkiye-dedektif-agi" class="hover:text-black transition">81 İl Ağı</a>
                    <a href="#arama-rehberi" class="hover:text-black transition">Arama Rehberi</a>
                    <a href="#mimari" class="hover:text-black transition">Hakkımızda</a>
                    <a href="#ofislerimiz" class="hover:text-black transition">Ofisler</a>
                    <a href="#sss" class="hover:text-black transition">S.S.S.</a>
                </nav>
            </div>

            <!-- Right: Action Pills (OpenAI Style) -->
            <div class="flex items-center gap-2 sm:gap-3 shrink-0">
                <!-- Dil / Lang -->
                <div class="relative" id="langSwitcherWrap">
                    <button type="button" onclick="toggleLangMenu()" id="langSwitcherBtn" class="px-2.5 py-1.5 rounded-full bg-black/[0.04] hover:bg-black/[0.08] text-black text-xs font-medium transition flex items-center gap-1 border border-black/[0.08]">
                        <i class="hgi hgi-stroke hgi-globe-02 w-3.5 h-3.5 text-black/70"></i>
                        <span id="currentLangCode" class="font-mono text-[11px] uppercase">TR</span>
                        <i class="hgi hgi-stroke hgi-arrow-down-01 w-3 h-3 opacity-60"></i>
                    </button>
                    <div id="langDropdownMenu" class="hidden absolute right-0 mt-2 w-48 rounded-2xl bg-white border border-black/10 shadow-xl p-1.5 z-50 space-y-0.5 text-xs text-black">
                        <button type="button" onclick="setSiteLanguage('tr')" data-lang-opt="tr" class="lang-opt-btn w-full text-left px-3 py-2 rounded-xl flex items-center justify-between bg-black/[0.05] text-black font-medium transition"><span>Türkçe</span><span class="font-mono text-[10px] opacity-80">TR</span></button>
                        <button type="button" onclick="setSiteLanguage('en')" data-lang-opt="en" class="lang-opt-btn w-full text-left px-3 py-2 rounded-xl flex items-center justify-between hover:bg-black/[0.04] transition text-black/75"><span>English</span><span class="font-mono text-[10px] opacity-60">EN</span></button>
                        <button type="button" onclick="setSiteLanguage('de')" data-lang-opt="de" class="lang-opt-btn w-full text-left px-3 py-2 rounded-xl flex items-center justify-between hover:bg-black/[0.04] transition text-black/75"><span>Deutsch</span><span class="font-mono text-[10px] opacity-60">DE</span></button>
                        <button type="button" onclick="setSiteLanguage('fr')" data-lang-opt="fr" class="lang-opt-btn w-full text-left px-3 py-2 rounded-xl flex items-center justify-between hover:bg-black/[0.04] transition text-black/75"><span>Français</span><span class="font-mono text-[10px] opacity-60">FR</span></button>
                        <button type="button" onclick="setSiteLanguage('ar')" data-lang-opt="ar" class="lang-opt-btn w-full text-left px-3 py-2 rounded-xl flex items-center justify-between hover:bg-black/[0.04] transition text-black/75"><span>العربية</span><span class="font-mono text-[10px] opacity-60">AR</span></button>
                        <button type="button" onclick="setSiteLanguage('ru')" data-lang-opt="ru" class="lang-opt-btn w-full text-left px-3 py-2 rounded-xl flex items-center justify-between hover:bg-black/[0.04] transition text-black/75"><span>Русский</span><span class="font-mono text-[10px] opacity-60">RU</span></button>
                    </div>
                </div>

                <!-- Sabit Tel Pill (OpenAI "Bizimle konuşun" stili) -->
                <a href="tel:03122840299" class="hidden sm:inline-flex items-center gap-1.5 px-3.5 py-2 rounded-full bg-black/[0.04] hover:bg-black/[0.08] text-black text-[13px] font-medium transition" title="Ankara Merkez Büro: 0312 284 02 99">
                    <span>0312 284 02 99</span>
                </a>

                <!-- WhatsApp Pill (OpenAI "ChatGPT'yi dene" siyah pill butonu) -->
                <a href="https://wa.me/905326667749?text=Merhaba%20%C3%9Cmit%20Bey%2C%20web%20sitenizden%20yaz%C4%B1yorum.%20Dan%C4%B1%C5%9Fmanl%C4%B1k%20almak%20istiyorum." target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-1.5 px-4 py-2 rounded-full bg-black hover:bg-neutral-800 text-white text-[13px] font-medium transition active:scale-95 shadow-sm" title="7/24 WhatsApp Özel Dedektif Danışma Hattı">
                    <i class="hgi hgi-stroke hgi-whatsapp w-4 h-4 text-[#25D366]"></i>
                    <span class="hidden sm:inline">WhatsApp</span>
                    <span>↗</span>
                </a>

                <!-- Mobile Menu Toggle -->
                <button id="mobileMenuBtn" aria-label="Menüyü aç/kapat" class="lg:hidden p-2 rounded-full bg-black/[0.04] text-black hover:bg-black/[0.08] transition">
                    <i class="hgi hgi-stroke hgi-menu-01 w-5 h-5"></i>
                </button>
            </div>
        </div>

        <!-- Mobile Drawer Menu -->
        <div id="mobileMenuDrawer" class="hidden lg:hidden bg-white border-b border-black/10 px-5 py-4 space-y-2 text-sm text-black">
            <a href="#hizmetler" class="block py-2 border-b border-black/[0.06] text-black/80 hover:text-black">12 Resmi Hizmetimiz</a>
            <a href="#delil-standartlari" class="block py-2 border-b border-black/[0.06] text-black/80 hover:text-black">Delil &amp; Hukuk (HMK m.199)</a>
            <a href="#turkiye-dedektif-agi" class="block py-2 border-b border-black/[0.06] text-black/80 hover:text-black">81 İl &amp; İlçe Ağı</a>
            <a href="#arama-rehberi" class="block py-2 border-b border-black/[0.06] text-black/80 hover:text-black">Arama &amp; Bilgi Rehberi</a>
            <a href="#mimari" class="block py-2 border-b border-black/[0.06] text-black/80 hover:text-black">Hakkımızda &amp; UÖDED</a>
            <a href="#ofislerimiz" class="block py-2 border-b border-black/[0.06] text-black/80 hover:text-black">Ofislerimiz</a>
            <a href="#sss" class="block py-2 text-black/80 hover:text-black">S.S.S.</a>
            <div class="pt-3 grid grid-cols-2 gap-2">
                <a href="tel:03122840299" class="flex items-center justify-center py-2.5 bg-black/[0.04] text-black rounded-full text-xs font-medium">0312 284 02 99</a>
                <a href="https://wa.me/905326667749" target="_blank" class="flex items-center justify-center py-2.5 bg-black text-white rounded-full text-xs font-medium">WhatsApp ↗</a>
            </div>
        </div>
    </header>"""

    html = html[:header_start] + openai_header + html[header_end:]

    # 3. Section Boundary Indices
    hero_start = html.find('<!-- 1. HERO SECTION')
    if hero_start == -1: hero_start = html.find('<section class="relative bg-[#111111]')

    mimari_start = html.find('<section id="mimari"')
    dedektife_sor_start = html.find('<section id="dedektife-sor"')
    hizmetler_start = html.find('<section id="hizmetler"')

    print(f"İndeksler: Hero: {hero_start}, Mimari: {mimari_start}, Dedektife-Sor: {dedektife_sor_start}, Hizmetler: {hizmetler_start}")
    assert hero_start > 0 and mimari_start > hero_start and dedektife_sor_start > mimari_start and hizmetler_start > dedektife_sor_start

    # OpenAI Hero (Birebir openai.com/tr-TR/ "Nasıl yardımcı olabilirim?")
    openai_hero = """<!-- 1. HERO SECTION: OPENAI EXACT "NASIL YARDIMCI OLABİLİRİM?" KONSOLU -->
        <section id="dedektife-sor" class="relative bg-[#FFFFFF] text-[#000000] pt-20 sm:pt-28 pb-14 sm:pb-20 overflow-hidden">
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
                <div class="max-w-[720px] mx-auto rounded-[28px] border border-black/[0.14] bg-[#FFFFFF] shadow-[0_2px_14px_rgba(0,0,0,0.04)] hover:shadow-[0_4px_20px_rgba(0,0,0,0.07)] focus-within:border-black/35 p-4 sm:p-5 transition relative">
                    
                    <!-- Textarea Input Area -->
                    <textarea id="aiChatInput" rows="2" placeholder="Vakanızı veya sorunuzu buraya yazın (örn: Eşim telefonuna şifre koydu, 5 yaşında kızımın velayeti, HMK m.199 delil geçerliliği, dedektif ücretleri...)" class="w-full bg-transparent border-none text-[#000000] placeholder-[#737373] text-[15px] sm:text-[16px] focus:outline-none resize-none leading-relaxed font-normal"></textarea>
                    
                    <!-- Bottom Action Row Inside Card -->
                    <div class="pt-2 flex items-center justify-between gap-3 border-t border-black/[0.06] mt-2">
                        <div class="flex items-center gap-2 text-[11px] font-mono text-[#8C8C8C]">
                            <span class="flex items-center gap-1"><span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span> %100 Anonim</span>
                            <span>•</span>
                            <span>Kayıt Tutulmaz</span>
                            <span class="hidden sm:inline">•</span>
                            <span class="hidden sm:inline">HMK m.199 Uyumlu</span>
                        </div>

                        <!-- Circular Send Button (OpenAI Exact 32px Round Arrow Button) -->
                        <button type="button" id="aiSendBtn" onclick="sendAIChatMessage()" class="w-8 h-8 rounded-full bg-[#000000] hover:bg-neutral-800 text-[#FFFFFF] flex items-center justify-center transition active:scale-95 shrink-0 shadow-sm" title="Soruyu Yanıtla">
                            <i class="hgi hgi-stroke hgi-arrow-up-01 w-4 h-4 text-white"></i>
                        </button>
                    </div>
                </div>

                <!-- OpenAI Prompt Suggestion Pills (Centered Horizontal List) -->
                <div class="flex items-center justify-center gap-2 flex-wrap mt-4 text-sm" id="aiQuickChips">
                    <button type="button" onclick="selectAIChatPreset('cocuk-velayeti')" class="px-3.5 py-1.5 rounded-full border border-black/[0.12] bg-[#FFFFFF] hover:bg-black/[0.04] text-[#000000] text-xs sm:text-[13px] transition font-normal shrink-0 shadow-xs">👶 Çocuk &amp; Velayet</button>
                    <button type="button" onclick="selectAIChatPreset('aldatan-erkek')" class="px-3.5 py-1.5 rounded-full border border-black/[0.12] bg-[#FFFFFF] hover:bg-black/[0.04] text-[#000000] text-xs sm:text-[13px] transition font-normal shrink-0 shadow-xs">💔 Eş Takibi &amp; Aldatma</button>
                    <button type="button" onclick="selectAIChatPreset('delil-gecerliligi')" class="px-3.5 py-1.5 rounded-full border border-black/[0.12] bg-[#FFFFFF] hover:bg-black/[0.04] text-[#000000] text-xs sm:text-[13px] transition font-normal shrink-0 shadow-xs">⚖️ Mahkemede Delil Geçerliliği</button>
                    <button type="button" onclick="selectAIChatPreset('dedektif-ucretleri')" class="px-3.5 py-1.5 rounded-full border border-black/[0.12] bg-[#FFFFFF] hover:bg-black/[0.04] text-[#000000] text-xs sm:text-[13px] transition font-normal shrink-0 shadow-xs">💳 Dedektif Ücretleri</button>
                    <button type="button" onclick="selectAIChatPreset('bocek-arama')" class="px-3.5 py-1.5 rounded-full border border-black/[0.12] bg-[#FFFFFF] hover:bg-black/[0.04] text-[#000000] text-xs sm:text-[13px] transition font-normal shrink-0 shadow-xs">🔍 Böcek Arama &amp; TSCM</button>
                    <button type="button" onclick="selectAIChatPreset('miras-borclu')" class="px-3.5 py-1.5 rounded-full border border-black/[0.12] bg-[#FFFFFF] hover:bg-black/[0.04] text-[#000000] text-xs sm:text-[13px] transition font-normal shrink-0 shadow-xs">📍 Adres &amp; Borçlu Tespiti</button>
                </div>

                <!-- Live Conversation Messages Container (Hidden initially until asked or clicked) -->
                <div class="max-w-[720px] mx-auto mt-6 space-y-4 empty:hidden" id="aiChatMessages">
                    <div class="flex items-start gap-3 text-left animate-fadeIn">
                        <img src="assets/photos/elsa-dedektif-asistan.jpg" alt="Elsa &amp; Ümit Hakan Karakaya" class="w-8 h-8 rounded-full border border-black/10 object-cover object-top shrink-0 mt-1 shadow-xs">
                        <div class="bg-[#F7F7F8] border border-black/[0.08] rounded-2xl rounded-tl-sm p-4 sm:p-5 text-black max-w-[95%] sm:max-w-[85%] space-y-3 shadow-xs">
                            <div class="flex items-center justify-between pb-2 border-b border-black/[0.08]">
                                <div class="flex items-center gap-1.5">
                                    <span class="text-xs font-medium text-black">Yeni Nesil Dedektif (Elsa &amp; Ümit Hakan Karakaya)</span>
                                    <span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
                                </div>
                                <span class="text-[10px] font-mono text-neutral-500">Çevrimiçi</span>
                            </div>
                            <div class="text-xs sm:text-[13.5px] leading-relaxed text-black/85 space-y-2 font-normal">
                                <p>Merhaba! Ben DAT Özel Dedektiflik'in Yeni Nesil Dijital Asistanı <strong>Elsa</strong>. Kurucumuz <strong>Ümit Hakan Karakaya</strong>'nın 20 yılı aşkın adli saha tecrübesiyle buradayım.</p>
                                <p>Burada kuruntuları körükleyen sahte şüphe oranlarına veya yasadışı yöntem tuzaklarına (TCK m.134 casus yazılım suçlarına) yer yok. Sorularınızı <strong>doğrulama yanılgısına kapılmadan</strong>, dürüst, gerçekçi ve mahkemede (HMK m.199) tek celsede geçerli hukuki perspektifle yanıtlıyorum.</p>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- OpenAI Two Featured Cards Section (Matches OpenAI /tr-TR/ Hero Bottom Grid) -->
                <div class="max-w-5xl mx-auto grid md:grid-cols-2 gap-4 sm:gap-6 mt-14 sm:mt-18 pt-10 border-t border-black/[0.08]">
                    <!-- Card 1: Founder & Authority -->
                    <div class="openai-card p-6 sm:p-8 flex flex-col justify-between space-y-6">
                        <div class="space-y-3">
                            <div class="text-[11px] font-mono tracking-widest text-[#595959] uppercase">2005'TEN BUGÜNE • ADLİ SAHA LİDERLİĞİ</div>
                            <h3 class="text-xl sm:text-2xl font-medium tracking-tight text-black">Ümit Hakan Karakaya &amp; UÖDED Güvencesi</h3>
                            <p class="text-xs sm:text-sm text-[#595959] leading-relaxed font-normal">
                                Uluslararası Hukuk mezunu, emekli TSK mensubu ve UÖDED Kurucu Başkanı Ümit Hakan Karakaya liderliğinde; 4.000'in üzerinde sonuçlandırılmış dosya ve resmi yazılı gizlilik sözleşmesi garantisi.
                            </p>
                        </div>
                        <div class="pt-4 border-t border-black/[0.06] flex items-center justify-between text-xs">
                            <span class="font-mono text-black/70">İstanbul &bull; Ankara &bull; Karadağ &bull; ABD</span>
                            <a href="#mimari" class="font-medium text-black hover:underline flex items-center gap-1">İncele ↗</a>
                        </div>
                    </div>

                    <!-- Card 2: Legal Evidence Standards -->
                    <div class="openai-card p-6 sm:p-8 flex flex-col justify-between space-y-6" id="delil-standartlari">
                        <div class="space-y-3">
                            <div class="text-[11px] font-mono tracking-widest text-[#595959] uppercase">HMK M.199 &bull; TCK M.134 UYUMU</div>
                            <h3 class="text-xl sm:text-2xl font-medium tracking-tight text-black">Mahkemede Tek Celsede Geçerli Delil Standartları</h3>
                            <p class="text-xs sm:text-sm text-[#595959] leading-relaxed font-normal">
                                Telefon dinleme ve casus yazılım gibi 2 ila 5 yıl hapis cezası gerektiren suçlara asla tevessül edilmez. Kamuya açık alanlarda elde edilen tarih-saat damgalı 4K gözlem raporlarıyla aile ve ticaret mahkemelerinde hüküm kurduran yasal delil toplanır.
                            </p>
                        </div>
                        <div class="pt-4 border-t border-black/[0.06] flex items-center justify-between text-xs">
                            <span class="font-mono text-emerald-600">%100 Hukuki Meşruiyet</span>
                            <a href="#hizmetler" class="font-medium text-black hover:underline flex items-center gap-1">12 Hizmeti Gör ↗</a>
                        </div>
                    </div>
                </div>

                <!-- 4 Metrics Row (OpenAI Subtle Stat Divider) -->
                <div class="max-w-5xl mx-auto pt-8 mt-6 grid grid-cols-2 lg:grid-cols-4 gap-6 text-center sm:text-left">
                    <div class="space-y-1">
                        <div class="text-2xl sm:text-3xl font-medium text-black tracking-tight">20+ Yıl</div>
                        <div class="text-xs text-[#595959]">2005'ten Bugüne Resmi Saha Tecrübesi</div>
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

            </div>
        </section>
        """

    # Parçaları birleştir:
    # 1. Başlangıçtan hero_start'a kadar
    # 2. openai_hero
    # 3. mimari_start'tan dedektife_sor_start'a kadar (mimari bölümü)
    # 4. hizmetler_start'tan sonuna kadar (tüm 12 hizmet, magaza, makaleler, ofisler, arama rehberi, 81 il vb. hepsi korunuyor!)
    new_html = html[:hero_start] + openai_hero + html[mimari_start:dedektife_sor_start] + html[hizmetler_start:]
    
    # 4. Dosyaları yaz
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(new_html)
    with open("Dat/index.html", "w", encoding="utf-8") as f:
        f.write(new_html)

    print("✓ index.html ve Dat/index.html başarıyla oluşturuldu! Toplam karakter:", len(new_html))

if __name__ == "__main__":
    build_site()
