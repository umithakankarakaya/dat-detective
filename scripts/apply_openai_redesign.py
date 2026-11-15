# -*- coding: utf-8 -*-
import os
import re

def apply_redesign():
    print("=== OPENAI ULTRA-MINIMALIST DÖNÜŞÜM BAŞLATILIYOR ===")
    
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Navbar'ı OpenAI stiline göre rafine et
    # Navbar'daki cart ve butonları temiz, minimal monochrome hale getir
    # Logo text / brand
    html = re.sub(
        r'<header class="sticky top-0 z-40 bg-\[#111111\]/95 backdrop-blur-md border-b border-white/\[0\.08\] text-\[#FFFFFF\]">',
        '<header class="sticky top-0 z-40 bg-[#080808]/95 backdrop-blur-md border-b border-white/10 text-[#FFFFFF]">',
        html
    )

    # 2. Eski Hero (satır ~1602 - 2032) ve eski #dedektife-sor (satır ~2315 - 2552) tespiti
    hero_start = html.find('<!-- 1. HERO SECTION: OBSIDIAN STUDIO STAGE')
    if hero_start == -1:
        hero_start = html.find('<section class="relative bg-[#111111] text-[#FFFFFF] pt-7')
    
    mimari_start = html.find('<!-- 2. KURUCU MİMARİ VE KURUMSAL OTORİTE')
    if mimari_start == -1:
        mimari_start = html.find('<section id="mimari"')

    dedektife_sor_start = html.find('<!-- 3. YENİ NESİL DEDEKTİF / DEDEKTİF\'E SOR')
    if dedektife_sor_start == -1:
        dedektife_sor_start = html.find('<section id="dedektife-sor"')

    hizmetler_start = html.find('<!-- 4. 12 OFFICIAL SERVICES')
    if hizmetler_start == -1:
        hizmetler_start = html.find('<section id="hizmetler"')

    print(f"Bölüm İndeksleri: Hero: {hero_start}, Mimari: {mimari_start}, Dedektife-Sor: {dedektife_sor_start}, Hizmetler: {hizmetler_start}")

    if hero_start == -1 or mimari_start == -1 or dedektife_sor_start == -1 or hizmetler_start == -1:
        print("HATA: İndeksler tam bulunamadı, script durduruldu.")
        return

    # OpenAI Dedektif'e Sor Hero Bölümü HTML
    new_hero_html = """<!-- 1. HERO SECTION: OPENAI ULTRA-MINIMALIST DEDEKTİF'E SOR CONSOLE -->
        <section id="dedektife-sor" class="relative bg-[#080808] text-[#FFFFFF] pt-8 pb-14 sm:pt-14 sm:pb-20 border-b border-white/10 overflow-hidden">
            <!-- Subtle Ambient Radial Glow -->
            <div class="pointer-events-none absolute -top-40 left-1/2 -translate-x-1/2 w-[800px] h-[400px] bg-white/[0.03] rounded-full blur-[140px]"></div>

            <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 space-y-8 sm:space-y-10">
                
                <!-- OpenAI Hero Header -->
                <div class="text-center space-y-4 max-w-3xl mx-auto">
                    <div class="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-white/[0.05] border border-white/10 text-[11px] font-mono tracking-widest text-neutral-300 uppercase">
                        <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
                        <span>YENİ NESİL ADLİ DANIŞMANLIK • 20+ YILLIK SAHA TECRÜBESİ</span>
                    </div>
                    
                    <h1 class="text-3xl sm:text-5xl lg:text-6xl font-normal tracking-[-0.03em] text-white leading-[1.12]">
                        Doğrulama yanılgısına yer yok.<br>
                        <span class="text-neutral-400">Sadece somut gerçekler ve yasal deliller.</span>
                    </h1>
                    
                    <p class="text-sm sm:text-base text-neutral-400 font-light leading-relaxed max-w-2xl mx-auto">
                        Kurucumuz <strong>Ümit Hakan Karakaya</strong> ve yeni nesil dijital asistanımız <strong>Elsa</strong> rehberliğinde; kuruntuları körükleyen sahte şüphe oranlarına değil, mahkemede tek celsede kabul edilen HMK m.199 normlarında hukuki gerçeklere dayalı canlı danışmanlık.
                    </p>
                </div>

                <!-- OpenAI ChatGPT-style Console Card -->
                <div class="rounded-3xl bg-[#111113] border border-white/15 overflow-hidden shadow-2xl transition">
                    
                    <!-- Console Top Header -->
                    <div class="px-5 py-3.5 bg-[#161618] border-b border-white/10 flex items-center justify-between">
                        <div class="flex items-center gap-3">
                            <div class="relative w-9 h-9 rounded-full overflow-hidden border border-white/20 shrink-0">
                                <img src="assets/photos/elsa-dedektif-asistan.jpg" alt="Elsa &amp; Ümit Hakan Karakaya" class="w-full h-full object-cover object-top">
                                <span class="absolute bottom-0 right-0 w-2.5 h-2.5 rounded-full bg-emerald-400 border-2 border-[#161618]"></span>
                            </div>
                            <div>
                                <div class="text-xs sm:text-sm font-medium text-white flex items-center gap-2">
                                    <span>Yeni Nesil Dedektif'e Sor</span>
                                    <span class="text-[10px] font-mono px-2 py-0.5 rounded-full bg-white/10 text-neutral-300">Canlı Danışman</span>
                                </div>
                                <div class="text-[10.5px] text-neutral-400 font-mono">Elsa &amp; Ümit Hakan Karakaya (UÖDED Başkanı)</div>
                            </div>
                        </div>
                        
                        <button type="button" onclick="resetAIChat()" class="px-3 py-1.5 rounded-full bg-white/5 hover:bg-white/10 text-neutral-300 hover:text-white text-[11px] font-mono flex items-center gap-1.5 transition" title="Sohbeti Sıfırla">
                            <i class="hgi hgi-stroke hgi-reload w-3 h-3"></i>
                            <span>Sıfırla</span>
                        </button>
                    </div>

                    <!-- Scrollable Conversation Stream -->
                    <div class="p-4 sm:p-6 space-y-4 max-h-[380px] sm:max-h-[440px] overflow-y-auto scrollbar-thin scrollbar-thumb-white/15" id="aiChatMessages">
                        <div class="flex items-start gap-3 text-left animate-fadeIn">
                            <img src="assets/photos/elsa-dedektif-asistan.jpg" alt="Elsa &amp; Ümit Hakan Karakaya" class="w-8 h-8 rounded-full border border-white/20 object-cover object-top shrink-0 mt-1 shadow-sm">
                            <div class="bg-[#18181B] border border-white/10 rounded-2xl rounded-tl-sm p-4 sm:p-5 text-white max-w-[95%] sm:max-w-[85%] space-y-3.5 shadow-lg">
                                <div class="flex items-center justify-between pb-2 border-b border-white/10">
                                    <div class="flex items-center gap-1.5">
                                        <span class="text-xs font-medium text-white">Yeni Nesil Dedektif (Elsa &amp; Ümit Hakan Karakaya)</span>
                                        <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
                                    </div>
                                    <span class="text-[10px] font-mono text-neutral-400">Çevrimiçi</span>
                                </div>
                                <div class="text-xs sm:text-[13px] leading-relaxed text-neutral-300 space-y-2">
                                    <p>Merhaba! Ben DAT Özel Dedektiflik'in Yeni Nesil Dijital Asistanı <strong>Elsa</strong>. Kurucumuz <strong>Ümit Hakan Karakaya</strong>'nın 20 yılı aşkın dedektiflik ve adli bilişim tecrübesiyle buradayım.</p>
                                    <p>Burada kuruntuları körükleyen sahte şüphe oranlarına, klişe vaatlere veya yasadışı yöntem tuzaklarına (telefon dinleme, casus yazılım gibi TCK m.134 suçlarına) yer yok. Sorularınızı <strong>doğrulama yanılgısına kapılmadan</strong>, dürüst, gerçekçi ve mahkemede (HMK m.199) tek celsede geçerli hukuki perspektifle yanıtlıyorum.</p>
                                    <p class="text-neutral-400 font-mono text-[11px] pt-1">Aşağıdaki hızlı konulardan birini seçebilir veya kendi vakanızı doğrudan aşağıdaki kutuya yazabilirsiniz:</p>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Console Input Area (OpenAI Style) -->
                    <div class="p-4 sm:p-5 bg-[#161618] border-t border-white/10 space-y-3">
                        
                        <!-- Input Box -->
                        <div class="flex flex-col sm:flex-row items-stretch sm:items-end gap-2.5 bg-[#0A0A0B] border border-white/15 focus-within:border-white/40 rounded-2xl p-2.5 sm:p-2 sm:pl-4 transition shadow-inner">
                            <textarea id="aiChatInput" rows="2" placeholder="Vakanızı, şüphenizi veya hukuki sorunuzu buraya yazın (örn: Eşim Bodrum'a tatile gitti, 5 yaşında kızımın velayeti, HMK m.199 delil geçerliliği, ücretler...)" class="flex-1 bg-transparent border-0 text-xs sm:text-sm text-white placeholder-neutral-500 focus:outline-none resize-none py-1.5 sm:py-2 max-h-32 leading-relaxed font-light"></textarea>
                            
                            <button type="button" id="aiSendBtn" onclick="sendAIChatMessage()" class="px-5 py-3 sm:py-2.5 rounded-xl bg-white text-black hover:bg-neutral-200 font-medium text-xs sm:text-sm flex items-center justify-center gap-2 shrink-0 transition active:scale-95 shadow-md">
                                <span>Soruyu Yanıtla</span>
                                <i class="hgi hgi-stroke hgi-arrow-right-01 w-4 h-4 text-black"></i>
                            </button>
                        </div>

                        <!-- Suggestion Chips (OpenAI Style Prompts) -->
                        <div class="space-y-1.5">
                            <div class="flex items-center justify-between text-[10.5px] font-mono text-neutral-400">
                                <span>HIZLI SENARYOLAR (1 TIKLA BAŞLATIN):</span>
                                <span class="text-neutral-500">8 Başlık</span>
                            </div>
                            <div class="flex items-center gap-1.5 overflow-x-auto pb-1 scrollbar-none text-[11px]" id="aiQuickChips">
                                <button type="button" onclick="selectAIChatPreset('cocuk-velayeti')" class="whitespace-nowrap px-3 py-1.5 rounded-full bg-white/5 hover:bg-white/10 text-neutral-300 hover:text-white border border-white/10 transition shrink-0">👶 Çocuk &amp; Velayet (TMK 182)</button>
                                <button type="button" onclick="selectAIChatPreset('dedektif-tutmak')" class="whitespace-nowrap px-3 py-1.5 rounded-full bg-white/5 hover:bg-white/10 text-neutral-300 hover:text-white border border-white/10 transition shrink-0">🕵️‍♂️ Dedektif Tutmak Yasal mı?</button>
                                <button type="button" onclick="selectAIChatPreset('dedektif-ucretleri')" class="whitespace-nowrap px-3 py-1.5 rounded-full bg-white/5 hover:bg-white/10 text-neutral-300 hover:text-white border border-white/10 transition shrink-0">💳 Dedektif Ücretleri &amp; Fiyatlar</button>
                                <button type="button" onclick="selectAIChatPreset('delil-gecerliligi')" class="whitespace-nowrap px-3 py-1.5 rounded-full bg-white/5 hover:bg-white/10 text-neutral-300 hover:text-white border border-white/10 transition shrink-0">⚖️ Mahkemede Delil Geçerliliği</button>
                                <button type="button" onclick="selectAIChatPreset('aldatan-erkek')" class="whitespace-nowrap px-3 py-1.5 rounded-full bg-white/5 hover:bg-white/10 text-neutral-300 hover:text-white border border-white/10 transition shrink-0">💔 Eş Takibi &amp; Aldatma Belirtileri</button>
                                <button type="button" onclick="selectAIChatPreset('tatilde-aldatma')" class="whitespace-nowrap px-3 py-1.5 rounded-full bg-white/5 hover:bg-white/10 text-neutral-300 hover:text-white border border-white/10 transition shrink-0">🏖️ Tatil &amp; Şüpheli Seyahat</button>
                                <button type="button" onclick="selectAIChatPreset('bocek-arama')" class="whitespace-nowrap px-3 py-1.5 rounded-full bg-white/5 hover:bg-white/10 text-neutral-300 hover:text-white border border-white/10 transition shrink-0">🔍 Böcek Arama &amp; TSCM</button>
                                <button type="button" onclick="selectAIChatPreset('miras-borclu')" class="whitespace-nowrap px-3 py-1.5 rounded-full bg-white/5 hover:bg-white/10 text-neutral-300 hover:text-white border border-white/10 transition shrink-0">📍 Adres &amp; Gizli Borçlu Tespiti</button>
                            </div>
                        </div>

                        <!-- Trust Badges & 7/24 Direct WhatsApp Link -->
                        <div class="pt-2 border-t border-white/10 flex flex-col sm:flex-row items-center justify-between gap-3 text-[11px] font-mono text-neutral-400">
                            <div class="flex flex-wrap items-center justify-center gap-3">
                                <span class="flex items-center gap-1"><i class="hgi hgi-stroke hgi-security-check w-3.5 h-3.5 text-emerald-400"></i> %100 Anonim</span>
                                <span>•</span>
                                <span class="flex items-center gap-1"><i class="hgi hgi-stroke hgi-shield-tick w-3.5 h-3.5 text-emerald-400"></i> Kayıt Tutulmaz</span>
                                <span>•</span>
                                <span class="flex items-center gap-1"><i class="hgi hgi-stroke hgi-justice-scale-01 w-3.5 h-3.5 text-emerald-400"></i> HMK m.199 Uyumlu</span>
                            </div>

                            <a href="https://wa.me/905326667749?text=Merhaba%20%C3%9Cmit%20Bey%2C%20Yeni%20Nesil%20Dedektif'e%20Sor%20alan%C4%B1ndan%20yaz%C4%B1yorum.%20Dan%C4%B1%C5%9Fmanl%C4%B1k%20almak%20istiyorum." target="_blank" rel="noopener noreferrer" class="text-white hover:text-emerald-400 flex items-center gap-1.5 font-medium transition" title="7/24 WhatsApp Özel Dedektif Danışma Hattı">
                                <i class="hgi hgi-stroke hgi-whatsapp w-4 h-4 text-[#25D366]"></i>
                                <span>WhatsApp Doğrudan Danışma: 0532 666 77 49</span>
                            </a>
                        </div>

                    </div>
                </div>

                <!-- 4-Column Minimal Metrics (OpenAI Stat Bar) -->
                <div class="pt-6 border-t border-white/10 grid grid-cols-2 lg:grid-cols-4 gap-6 text-center sm:text-left">
                    <div class="space-y-1">
                        <div class="text-2xl sm:text-3xl font-light text-white tracking-tight">20+ Yıl</div>
                        <div class="text-xs text-neutral-400 font-light">2005'ten Bugüne Kesintisiz Adli Saha Deneyimi</div>
                    </div>
                    <div class="space-y-1">
                        <div class="text-2xl sm:text-3xl font-light text-white tracking-tight">4.000+</div>
                        <div class="text-xs text-neutral-400 font-light">Tek Celsede Kabul Edilen Hukuki Delil ve Rapor</div>
                    </div>
                    <div class="space-y-1">
                        <div class="text-2xl sm:text-3xl font-light text-white tracking-tight">%100 Yasal</div>
                        <div class="text-xs text-neutral-400 font-light">HMK m.199 ve TCK m.134 Sınırlarında Kanıt</div>
                    </div>
                    <div class="space-y-1">
                        <div class="text-2xl sm:text-3xl font-light text-white tracking-tight">81 İl &amp; Global</div>
                        <div class="text-xs text-neutral-400 font-light">İstanbul, Ankara, Karadağ ve ABD Temsilcilikleri</div>
                    </div>
                </div>

            </div>
        </section>
        
        """

    # Şimdi:
    # 1. hero_start ile mimari_start arasını new_hero_html ile değiştir.
    # 2. dedektife_sor_start ile hizmetler_start arasını (eski alt chat bölümü) kaldır, çünkü artık en başta!
    part1 = html[:hero_start]
    part2 = new_hero_html
    part3 = html[mimari_start:dedektife_sor_start]
    part4 = html[hizmetler_start:]

    new_html = part1 + part2 + part3 + part4
    
    # 3. Hizmetler bölümündeki renkleri ve butonları OpenAI monokrom tarzına rafine et
    # #hizmetler arka planını soft beyaz / monokrom yap
    new_html = new_html.replace('section id="hizmetler" class="py-12 sm:py-16 bg-[#F2F2F2]"', 'section id="hizmetler" class="py-14 sm:py-20 bg-[#F9F9FB] border-t border-black/[0.08]"')
    
    # Dosyaları güncelle (hem root hem Dat/)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(new_html)
    with open("Dat/index.html", "w", encoding="utf-8") as f:
        f.write(new_html)

    print("✓ index.html ve Dat/index.html başarıyla güncellendi!")

if __name__ == "__main__":
    apply_redesign()
