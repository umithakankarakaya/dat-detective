#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

NEW_CHAT_SECTION_HTML = """        <!-- 3. YENİ NESİL DEDEKTİF / DEDEKTİF'E SOR (#dedektife-sor - Studio Obsidian Dark #111111) -->
        <section id="dedektife-sor" class="py-14 sm:py-20 bg-[#111111] text-[#FFFFFF] border-y border-white/10 relative overflow-hidden">
            <!-- Subtle Radial Ambient Glow -->
            <div class="pointer-events-none absolute -top-40 left-1/2 -translate-x-1/2 w-[700px] h-[350px] bg-[#93F051]/10 rounded-full blur-[120px]"></div>

            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 space-y-8 sm:space-y-10">

                <!-- Header -->
                <div class="text-center max-w-4xl mx-auto space-y-3.5">
                    <div class="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-[#1D1D1F] border border-[#93F051]/30 text-xs font-medium text-[#FFFFFF]">
                        <span class="w-2 h-2 rounded-full bg-[#93F051] animate-pulse"></span>
                        <span class="text-[#93F051] font-mono uppercase tracking-wider text-[11px]">YENİ NESİL DEDEKTİF • CANLI SOHBET &amp; ADLİ DANIŞMANLIK</span>
                    </div>
                    <h2 class="apple-heading text-3xl sm:text-4xl lg:text-5xl font-medium text-[#FFFFFF] tracking-tight">
                        Yeni Nesil Dedektif'e Sor
                    </h2>
                    <p class="text-sm sm:text-base text-white/75 leading-relaxed font-regular max-w-3xl mx-auto">
                        Dedektiflik dünyasında kuruntuları körükleyen sahte şüphe oranlarına, klişe vaatlere veya yasadışı yöntem tuzaklarına yer yok. <strong>20 yılı aşkın tecrübesiyle kurucumuz Ümit Hakan Karakaya</strong> ve dijital asistanımız <strong>Elsa</strong> rehberliğinde; sorularınızı <strong>doğrulama yanılgısına (yankı odasına) kapılmadan</strong>, dürüst, gerçekçi ve mahkemede geçerli hukuki perspektifle yanıtlıyoruz.
                    </p>
                </div>

                <!-- Chat Studio Card (Apple-style Dark Frame) -->
                <div class="rounded-[28px] sm:rounded-[32px] bg-[#161618] border border-white/10 overflow-hidden shadow-2xl grid lg:grid-cols-12 items-stretch">
                    
                    <!-- Left Sidebar (lg:col-span-4): Advisor Profile + Quick Topic Chips + Direct Contacts -->
                    <div class="lg:col-span-4 bg-[#121214] p-5 sm:p-6 border-b lg:border-b-0 lg:border-r border-white/10 flex flex-col justify-between space-y-5">
                        <div class="space-y-4">
                            <!-- Advisor Card -->
                            <div class="rounded-2xl bg-[#18181A] border border-white/10 p-3.5 flex items-center gap-3">
                                <div class="relative w-12 h-12 rounded-full overflow-hidden shrink-0 border border-[#93F051]/50">
                                    <img src="assets/photos/elsa-dedektif-asistan.jpg" alt="Elsa — Yeni Nesil Dedektif Asistanı" class="w-full h-full object-cover object-top">
                                    <span class="absolute bottom-0 right-0 w-3 h-3 rounded-full bg-[#93F051] border-2 border-[#121214]"></span>
                                </div>
                                <div class="min-w-0 flex-1">
                                    <div class="text-xs sm:text-[13px] font-medium text-white flex items-center justify-between">
                                        <span class="truncate">Elsa &amp; Ümit Hakan Karakaya</span>
                                    </div>
                                    <div class="text-[10.5px] text-[#93F051] font-mono truncate">Yeni Nesil Dedektif • Çevrimiçi</div>
                                    <div class="text-[10px] text-white/50 truncate">UÖDED Başkanı • 20+ Yıl Adli Deneyim</div>
                                </div>
                            </div>

                            <!-- Anti Echo-Chamber Principle Note -->
                            <div class="rounded-xl bg-[#93F051]/5 border border-[#93F051]/20 p-3 text-[11px] text-white/80 leading-relaxed space-y-1">
                                <div class="font-mono text-[#93F051] text-[10px] font-bold uppercase tracking-wider flex items-center gap-1.5">
                                    <i class="hgi hgi-stroke hgi-shield-check w-3.5 h-3.5"></i>
                                    <span>Yankı Odasından Uzak İlke</span>
                                </div>
                                <p>Sorularınız kuruntuları körüklemek için değil; soğukkanlı hukuki gerçekler, HMK m.199 ve TCK m.134 sınırları doğrultusunda dürüst ve objektif olarak yanıtlanır.</p>
                            </div>

                            <!-- Quick Topics -->
                            <div class="space-y-2">
                                <div class="flex items-center justify-between">
                                    <span class="text-[10.5px] font-mono text-white/60 uppercase tracking-wider">HIZLI KONULAR (1 TIKLA SORUN)</span>
                                    <span class="text-[9.5px] font-mono text-[#93F051]">9 Başlık</span>
                                </div>
                                <div class="grid grid-cols-1 gap-1.5 max-h-[280px] overflow-y-auto pr-1 scrollbar-thin scrollbar-thumb-white/10" id="aiQuickChips">
                                    <button type="button" onclick="selectAIChatPreset('dedektif-tutmak')" class="w-full text-left px-3 py-2 rounded-xl bg-[#1D1D1F] hover:bg-[#252528] text-white/80 hover:text-white text-xs border border-white/10 flex items-center justify-between transition group">
                                        <span class="flex items-center gap-2 truncate">
                                            <span class="text-sm shrink-0">🕵️‍♂️</span>
                                            <span class="truncate">Dedektif Tutmak Yasal mı?</span>
                                        </span>
                                        <i class="hgi hgi-stroke hgi-arrow-right-01 w-3 h-3 text-white/40 group-hover:text-[#93F051] shrink-0"></i>
                                    </button>
                                    <button type="button" onclick="selectAIChatPreset('dedektif-ucretleri')" class="w-full text-left px-3 py-2 rounded-xl bg-[#1D1D1F] hover:bg-[#252528] text-white/80 hover:text-white text-xs border border-white/10 flex items-center justify-between transition group">
                                        <span class="flex items-center gap-2 truncate">
                                            <span class="text-sm shrink-0">💳</span>
                                            <span class="truncate">Dedektif Ücretleri Ne Kadar?</span>
                                        </span>
                                        <i class="hgi hgi-stroke hgi-arrow-right-01 w-3 h-3 text-white/40 group-hover:text-[#93F051] shrink-0"></i>
                                    </button>
                                    <button type="button" onclick="selectAIChatPreset('delil-gecerliligi')" class="w-full text-left px-3 py-2 rounded-xl bg-[#1D1D1F] hover:bg-[#252528] text-white/80 hover:text-white text-xs border border-white/10 flex items-center justify-between transition group">
                                        <span class="flex items-center gap-2 truncate">
                                            <span class="text-sm shrink-0">⚖️</span>
                                            <span class="truncate">Deliller Mahkemede Geçerli mi?</span>
                                        </span>
                                        <i class="hgi hgi-stroke hgi-arrow-right-01 w-3 h-3 text-white/40 group-hover:text-[#93F051] shrink-0"></i>
                                    </button>
                                    <button type="button" onclick="selectAIChatPreset('almanya-es-takibi')" class="w-full text-left px-3 py-2 rounded-xl bg-[#1D1D1F] hover:bg-[#252528] text-white/80 hover:text-white text-xs border border-white/10 flex items-center justify-between transition group">
                                        <span class="flex items-center gap-2 truncate">
                                            <span class="text-sm shrink-0">🇩🇪</span>
                                            <span class="truncate">Almanya &amp; Avrupa Eş Takibi</span>
                                        </span>
                                        <i class="hgi hgi-stroke hgi-arrow-right-01 w-3 h-3 text-white/40 group-hover:text-[#93F051] shrink-0"></i>
                                    </button>
                                    <button type="button" onclick="selectAIChatPreset('aldatan-erkek')" class="w-full text-left px-3 py-2 rounded-xl bg-[#1D1D1F] hover:bg-[#252528] text-white/80 hover:text-white text-xs border border-white/10 flex items-center justify-between transition group">
                                        <span class="flex items-center gap-2 truncate">
                                            <span class="text-sm shrink-0">💔</span>
                                            <span class="truncate">Aldatma Belirtileri &amp; Delil Sınırı</span>
                                        </span>
                                        <i class="hgi hgi-stroke hgi-arrow-right-01 w-3 h-3 text-white/40 group-hover:text-[#93F051] shrink-0"></i>
                                    </button>
                                    <button type="button" onclick="selectAIChatPreset('tatilde-aldatma')" class="w-full text-left px-3 py-2 rounded-xl bg-[#1D1D1F] hover:bg-[#252528] text-white/80 hover:text-white text-xs border border-white/10 flex items-center justify-between transition group">
                                        <span class="flex items-center gap-2 truncate">
                                            <span class="text-sm shrink-0">🏖️</span>
                                            <span class="truncate">Şüpheli Tatil &amp; Seyahat Takibi</span>
                                        </span>
                                        <i class="hgi hgi-stroke hgi-arrow-right-01 w-3 h-3 text-white/40 group-hover:text-[#93F051] shrink-0"></i>
                                    </button>
                                    <button type="button" onclick="selectAIChatPreset('miras-borclu')" class="w-full text-left px-3 py-2 rounded-xl bg-[#1D1D1F] hover:bg-[#252528] text-white/80 hover:text-white text-xs border border-white/10 flex items-center justify-between transition group">
                                        <span class="flex items-center gap-2 truncate">
                                            <span class="text-sm shrink-0">📍</span>
                                            <span class="truncate">Adres &amp; Gizli Borçlu Tespiti</span>
                                        </span>
                                        <i class="hgi hgi-stroke hgi-arrow-right-01 w-3 h-3 text-white/40 group-hover:text-[#93F051] shrink-0"></i>
                                    </button>
                                    <button type="button" onclick="selectAIChatPreset('nafaka-gelir')" class="w-full text-left px-3 py-2 rounded-xl bg-[#1D1D1F] hover:bg-[#252528] text-white/80 hover:text-white text-xs border border-white/10 flex items-center justify-between transition group">
                                        <span class="flex items-center gap-2 truncate">
                                            <span class="text-sm shrink-0">🏢</span>
                                            <span class="truncate">Nafaka İptali İçin Gelir Tespiti</span>
                                        </span>
                                        <i class="hgi hgi-stroke hgi-arrow-right-01 w-3 h-3 text-white/40 group-hover:text-[#93F051] shrink-0"></i>
                                    </button>
                                    <button type="button" onclick="selectAIChatPreset('dedektif-olmak')" class="w-full text-left px-3 py-2 rounded-xl bg-[#1D1D1F] hover:bg-[#252528] text-white/80 hover:text-white text-xs border border-white/10 flex items-center justify-between transition group">
                                        <span class="flex items-center gap-2 truncate">
                                            <span class="text-sm shrink-0">🎓</span>
                                            <span class="truncate">Özel Dedektif Nasıl Olunur?</span>
                                        </span>
                                        <i class="hgi hgi-stroke hgi-arrow-right-01 w-3 h-3 text-white/40 group-hover:text-[#93F051] shrink-0"></i>
                                    </button>
                                </div>
                            </div>
                        </div>

                        <!-- 7/24 Direct Helpline Footer in Sidebar -->
                        <div class="pt-3 border-t border-white/10 flex items-center justify-between gap-2 text-[11px]">
                            <div class="text-white/60">
                                <div>7/24 Resmi Danışma:</div>
                                <a href="tel:03122840299" class="font-mono text-white hover:text-[#93F051] font-medium transition">0312 284 02 99</a>
                            </div>
                            <a href="https://wa.me/905326667749?text=Merhaba%20%C3%9Cmit%20Bey%2C%20Yeni%20Nesil%20Dedektif%20(Dedektif'e%20Sor)%20alan%C4%B1ndan%20yaz%C4%B1yorum.%20Dan%C4%B1%C5%9Fmanl%C4%B1k%20almak%20istiyorum." target="_blank" rel="noopener noreferrer" class="px-3 py-1.5 rounded-lg bg-[#25D366] text-[#111111] font-medium text-[10.5px] flex items-center gap-1 hover:bg-[#20ba59] transition" title="7/24 WhatsApp Özel Dedektif Danışma Hattı: 0532 666 77 49 — DAT Özel Dedektiflik">
                                <i class="hgi hgi-stroke hgi-whatsapp w-3.5 h-3.5"></i>
                                <span>0532 666 77 49</span>
                            </a>
                        </div>
                    </div>

                    <!-- Right Main Chat Panel (lg:col-span-8): Chat Header, Message Scroll Area, Docked Input -->
                    <div class="lg:col-span-8 flex flex-col justify-between bg-[#18181A] min-h-[580px] max-h-[720px] relative">
                        
                        <!-- Chat Header -->
                        <div class="p-3.5 sm:p-4 px-5 bg-[#141416] border-b border-white/10 flex items-center justify-between shrink-0">
                            <div class="flex items-center gap-2.5">
                                <div class="w-8 h-8 rounded-full bg-[#1D1D1F] border border-[#93F051]/40 flex items-center justify-center shrink-0">
                                    <i class="hgi hgi-stroke hgi-message-programming w-4 h-4 text-[#93F051]"></i>
                                </div>
                                <div>
                                    <div class="text-xs sm:text-sm font-medium text-white flex items-center gap-2">
                                        <span>Yeni Nesil Dedektif'e Sor</span>
                                        <span class="w-2 h-2 rounded-full bg-[#93F051] animate-ping"></span>
                                    </div>
                                    <div class="text-[10px] text-white/50 font-mono">Dürüst, Rasyonel &amp; Hukuka Uygun Canlı Danışman</div>
                                </div>
                            </div>
                            <button type="button" onclick="resetAIChat()" class="px-2.5 py-1 rounded-lg bg-white/5 hover:bg-white/10 text-white/60 hover:text-white text-[10.5px] font-mono flex items-center gap-1 transition" title="Sohbeti Temizle ve Başa Dön">
                                <i class="hgi hgi-stroke hgi-reload w-3 h-3"></i>
                                <span>Sohbeti Sıfırla</span>
                            </button>
                        </div>

                        <!-- Chat Messages Container (Scrollable) -->
                        <div class="flex-1 p-4 sm:p-6 space-y-4 overflow-y-auto scrollbar-thin scrollbar-thumb-white/15" id="aiChatMessages">
                            <!-- Populated dynamically by script.js -->
                        </div>

                        <!-- Chat Footer / Input Area -->
                        <div class="p-3 sm:p-4 bg-[#141416] border-t border-white/10 space-y-2.5 shrink-0">
                            <!-- Mobile-only horizontal chip scroll -->
                            <div class="flex lg:hidden items-center gap-1.5 overflow-x-auto pb-1 scrollbar-none text-[10.5px]">
                                <button type="button" onclick="selectAIChatPreset('dedektif-tutmak')" class="whitespace-nowrap px-2.5 py-1 rounded-full bg-white/5 text-white/80 border border-white/10 shrink-0">🕵️‍♂️ Yasal mı?</button>
                                <button type="button" onclick="selectAIChatPreset('dedektif-ucretleri')" class="whitespace-nowrap px-2.5 py-1 rounded-full bg-white/5 text-white/80 border border-white/10 shrink-0">💳 Ücretler</button>
                                <button type="button" onclick="selectAIChatPreset('delil-gecerliligi')" class="whitespace-nowrap px-2.5 py-1 rounded-full bg-white/5 text-white/80 border border-white/10 shrink-0">⚖️ Delil Geçerliliği</button>
                                <button type="button" onclick="selectAIChatPreset('almanya-es-takibi')" class="whitespace-nowrap px-2.5 py-1 rounded-full bg-white/5 text-white/80 border border-white/10 shrink-0">🇩🇪 Almanya/Avrupa</button>
                                <button type="button" onclick="selectAIChatPreset('aldatan-erkek')" class="whitespace-nowrap px-2.5 py-1 rounded-full bg-white/5 text-white/80 border border-white/10 shrink-0">💔 Eş Takibi</button>
                                <button type="button" onclick="selectAIChatPreset('tatilde-aldatma')" class="whitespace-nowrap px-2.5 py-1 rounded-full bg-white/5 text-white/80 border border-white/10 shrink-0">🏖️ Tatil Takibi</button>
                                <button type="button" onclick="selectAIChatPreset('miras-borclu')" class="whitespace-nowrap px-2.5 py-1 rounded-full bg-white/5 text-white/80 border border-white/10 shrink-0">📍 Borçlu Tespiti</button>
                            </div>

                            <!-- Input Row -->
                            <div class="flex items-end gap-2 bg-[#1A1A1D] border border-white/15 focus-within:border-[#93F051] rounded-2xl p-1.5 pl-3 transition shadow-inner">
                                <textarea id="aiChatInput" rows="1" placeholder="Yeni Nesil Dedektif'e merak ettiğiniz konuyu dürüstçe sorun..." class="flex-1 bg-transparent border-0 text-xs sm:text-sm text-white placeholder-white/40 focus:outline-none resize-none py-2 max-h-28 leading-relaxed"></textarea>
                                <button type="button" id="aiSendBtn" onclick="sendAIChatMessage()" class="px-4 sm:px-5 py-2.5 rounded-xl bg-[#93F051] hover:bg-[#82dc43] text-[#111111] font-semibold text-xs sm:text-sm flex items-center justify-center gap-1.5 shrink-0 transition active:scale-95 shadow-md shadow-[#93F051]/20">
                                    <span>Yeni Nesil Dedektif'e Sor</span>
                                    <i class="hgi hgi-stroke hgi-sent w-4 h-4 text-[#111111]"></i>
                                </button>
                            </div>

                            <!-- Trust Badges -->
                            <div class="flex items-center justify-center gap-3 sm:gap-4 text-[10px] sm:text-[10.5px] font-mono text-white/50">
                                <span class="flex items-center gap-1"><i class="hgi hgi-stroke hgi-security-check w-3 h-3 text-[#93F051]"></i> %100 Anonim</span>
                                <span>•</span>
                                <span class="flex items-center gap-1"><i class="hgi hgi-stroke hgi-shield-tick w-3 h-3 text-[#93F051]"></i> Kayıt Tutulmaz</span>
                                <span>•</span>
                                <span class="flex items-center gap-1"><i class="hgi hgi-stroke hgi-lock-password w-3 h-3 text-[#93F051]"></i> 256-Bit SSL</span>
                                <span>•</span>
                                <span class="flex items-center gap-1"><i class="hgi hgi-stroke hgi-justice-scale-01 w-3 h-3 text-[#93F051]"></i> HMK m.199 Uyumlu</span>
                            </div>
                        </div>

                    </div>

                </div>

            </div>
        </section>"""

def update_index_files():
    for fpath in ["index.html", "Dat/index.html"]:
        full_path = os.path.join(BASE_DIR, fpath)
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()

        content = re.sub(
            r'<!-- 3\. YENİ NESİL DEDEKTİF / DEDEKTİF\'E SOR[\s\S]*?</section>',
            NEW_CHAT_SECTION_HTML.strip(),
            content,
            count=1
        )

        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated {fpath} with Chat Studio UI.")

if __name__ == "__main__":
    update_index_files()
