#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

LANG_CONFIGS = {
    "en": {
        "badge": "NEXT GEN DETECTIVE • LIVE FORENSIC CHAT STUDIO",
        "title": "Ask Next Gen Detective",
        "subtitle": "No alarmist hype or echo-chamber confirmation bias. Guided by founder <strong>Ümit Hakan Karakaya</strong> (20+ years forensic experience) and AI Assistant <strong>Elsa</strong>, we provide honest, objective, and court-admissible legal analysis within statutory boundaries (CCP Art. 199 & TCC Art. 134).",
        "advisor_name": "Elsa & Ümit Hakan Karakaya",
        "advisor_status": "Next Gen Detective • Online",
        "advisor_sub": "President of UÖDED • 20+ Yrs Forensic Exp.",
        "policy_title": "Anti-Echo Chamber Policy",
        "policy_text": "Inquiries are addressed objectively within statutory boundaries (CCP Art. 199 & TCC Art. 134), dispelling paranoia rather than feeding unverified suspicions.",
        "topics_title": "POPULAR TOPICS (1-CLICK ASK)",
        "topics_count": "9 Topics",
        "topics": [
            ("dedektif-tutmak", "🕵️‍♂️", "Is Hiring a Detective Legal?"),
            ("dedektif-ucretleri", "💳", "How Are Fees Calculated?"),
            ("delil-gecerliligi", "⚖️", "Is Evidence Court-Admissible?"),
            ("almanya-es-takibi", "🇩🇪", "Spouse Surveillance from Europe"),
            ("aldatan-erkek", "💔", "Infidelity Signs & Limits"),
            ("tatilde-aldatma", "🏖️", "Suspicious Travel / Vacation"),
            ("miras-borclu", "📍", "Asset & Address Tracing"),
            ("nafaka-gelir", "🏢", "Alimony Hidden Income Trace"),
            ("dedektif-olmak", "🎓", "How to Become a Detective?")
        ],
        "helpline_label": "24/7 Official Helpline:",
        "chat_status": "Honest, Rational & Court-Admissible Live Assistant",
        "reset_btn": "Reset Chat",
        "placeholder": "Ask Next Gen Detective your question honestly...",
        "send_btn": "Ask Next Gen Detective",
        "trust_1": "100% Anonymous",
        "trust_2": "Zero Logs",
        "trust_3": "256-Bit SSL",
        "trust_4": "CCP Art. 199 Fit"
    },
    "de": {
        "badge": "NEXT GEN DETEKTIV • LIVE FORENSIK CHAT-STUDIO",
        "title": "Frag den Next Gen Detektiv",
        "subtitle": "Keine unbegründete Panikmache oder Echokammer-Täuschung. Unter der Leitung von Gründer <strong>Ümit Hakan Karakaya</strong> (20+ Jahre forensische Erfahrung) und KI-Assistentin <strong>Elsa</strong> beantworten wir Ihre Fragen ehrlich, rational und gerichtsverwertbar im Rahmen von HMK § 199 & TCK § 134.",
        "advisor_name": "Elsa & Ümit Hakan Karakaya",
        "advisor_status": "Next Gen Detektiv • Online",
        "advisor_sub": "Präsident der UÖDED • 20+ Jahre Erfahrung",
        "policy_title": "Echokammer-freies Prinzip",
        "policy_text": "Ihre Fragen werden nüchtern und gesetzeskonform (HMK § 199 & TCK § 134) beantwortet, um reale rechtliche Klarheit statt unbegründeter Paranoia zu schaffen.",
        "topics_title": "HÄUFIGE THEMEN (1-KLICK FRAGE)",
        "topics_count": "9 Themen",
        "topics": [
            ("dedektif-tutmak", "🕵️‍♂️", "Ist ein Detektiv legal?"),
            ("dedektif-ucretleri", "💳", "Wie hoch sind die Kosten?"),
            ("delil-gecerliligi", "⚖️", "Sind Beweise gerichtsverwertbar?"),
            ("almanya-es-takibi", "🇩🇪", "Observation aus Europa in TR"),
            ("aldatan-erkek", "💔", "Untreue-Anzeichen & Beweisgrenzen"),
            ("tatilde-aldatma", "🏖️", "Verdächtige Urlaubsreisen"),
            ("miras-borclu", "📍", "Wohnsitz- & Vermögenssuche"),
            ("nafaka-gelir", "🏢", "Unterhalt & verdecktes Einkommen"),
            ("dedektif-olmak", "🎓", "Wie wird man Detektiv?")
        ],
        "helpline_label": "24/7 Amtliche Auskunft:",
        "chat_status": "Ehrlicher, rationaler & gerichtsverwertbarer Live-Berater",
        "reset_btn": "Chat zurücksetzen",
        "placeholder": "Stellen Sie Ihre Frage offen und ehrlich an den Next Gen Detektiv...",
        "send_btn": "Frag den Next Gen Detektiv",
        "trust_1": "100 % Anonym",
        "trust_2": "Keine Speicherung",
        "trust_3": "256-Bit SSL",
        "trust_4": "HMK § 199 Konform"
    },
    "fr": {
        "badge": "DÉTECTIVE NOUVELLE GÉNÉRATION • CHAT LIVE FORENSIQUE",
        "title": "Demandez au Détective Nouvelle Génération",
        "subtitle": "Pas de fausse panique ni d'effet de bulle d'écho. Sous la direction du fondateur <strong>Ümit Hakan Karakaya</strong> (20+ ans d'expérience) et de l'assistante IA <strong>Elsa</strong>, nous répondons à vos interrogations de manière honnête, rationnelle et recevable en justice (CPC art. 199).",
        "advisor_name": "Elsa & Ümit Hakan Karakaya",
        "advisor_status": "Détective Nouvelle Génération • En ligne",
        "advisor_sub": "Président UÖDED • 20+ Ans d'Expérience",
        "policy_title": "Principe Hors Bulle d'Écho",
        "policy_text": "Vos questions sont traitées avec rigueur selon les lois strictes sur la vie privée (CPC art. 199 & TCK art. 134), garantissant une analyse juridique lucide.",
        "topics_title": "SUJETS FRÉQUENTS (1 CLIC)",
        "topics_count": "9 Sujets",
        "topics": [
            ("dedektif-tutmak", "🕵️‍♂️", "Engager un détective est-il légal ?"),
            ("dedektif-ucretleri", "💳", "Combien coûte un détective ?"),
            ("delil-gecerliligi", "⚖️", "Les preuves sont-elles recevables ?"),
            ("almanya-es-takibi", "🇩🇪", "Filature depuis l'Europe en Turquie"),
            ("aldatan-erkek", "💔", "Signes d'infidélité & cadre légal"),
            ("tatilde-aldatma", "🏖️", "Vacances & voyages suspects"),
            ("miras-borclu", "📍", "Recherche d'adresse & patrimoine"),
            ("nafaka-gelir", "🏢", "Revenus cachés pour pension"),
            ("dedektif-olmak", "🎓", "Comment devenir détective ?")
        ],
        "helpline_label": "Consultation Officielle 24/7 :",
        "chat_status": "Conseiller Live Honnête & Conforme Tribunal",
        "reset_btn": "Réinitialiser",
        "placeholder": "Posez votre question en toute franchise au Détective Nouvelle Génération...",
        "send_btn": "Demandez au Détective",
        "trust_1": "100 % Anonyme",
        "trust_2": "Aucun Enregistrement",
        "trust_3": "SSL 256-Bit",
        "trust_4": "Conforme CPC art. 199"
    },
    "ru": {
        "badge": "ДЕТЕКТИВ НОВОГО ПОКОЛЕНИЯ • ОНЛАЙН-ЧАТ КОНСУЛЬТАЦИЯ",
        "title": "Спросить Детектива Нового Поколения",
        "subtitle": "Без раздувания необоснованных страхов и ловушек предвзятости. Под руководством основателя <strong>Юмита Хакана Каракая</strong> (20+ лет судебно-следственного опыта) и ИИ-ассистента <strong>Эльзы</strong> мы даем честные, рациональные и применимые в суде ответы (ГПК ст. 199 / УК ст. 134).",
        "advisor_name": "Эльза и Юмит Хакан Каракая",
        "advisor_status": "Детектив Нового Поколения • Онлайн",
        "advisor_sub": "Президент UÖDED • 20+ Лет Опыта",
        "policy_title": "Принцип вне предвзятости",
        "policy_text": "Вопросы разбираются объективно в правовых рамках неприкосновенности частной жизни, отсеивая домыслы и необоснованные подозрения.",
        "topics_title": "ЧАСТЫЕ ВОПРОСЫ (В 1 КЛИК)",
        "topics_count": "9 Тем",
        "topics": [
            ("dedektif-tutmak", "🕵️‍♂️", "Законно ли нанимать детектива?"),
            ("dedektif-ucretleri", "💳", "Сколько стоят услуги?"),
            ("delil-gecerliligi", "⚖️", "Примет ли суд доказательства?"),
            ("almanya-es-takibi", "🇩🇪", "Слежка за супругом из Европы"),
            ("aldatan-erkek", "💔", "Признаки измены и границы закона"),
            ("tatilde-aldatma", "🏖️", "Подозрительный отпуск и поездки"),
            ("miras-borclu", "📍", "Поиск адреса и скрытых активов"),
            ("nafaka-gelir", "🏢", "Скрытие доходов при алиментах"),
            ("dedektif-olmak", "🎓", "Как стать частным детективом?")
        ],
        "helpline_label": "Круглосуточная справка 24/7:",
        "chat_status": "Честный, рациональный и судебный онлайн-советник",
        "reset_btn": "Сброс чата",
        "placeholder": "Задайте ваш вопрос Детективу Нового Поколения...",
        "send_btn": "Спросить Детектива",
        "trust_1": "100% Анонимно",
        "trust_2": "Без логов",
        "trust_3": "256-Bit SSL",
        "trust_4": "ГПК ст. 199"
    },
    "ar": {
        "badge": "محقّق الجيل الجديد • منصة الاستشارة والدردشة القضائية",
        "title": "اسأل محقّق الجيل الجديد",
        "subtitle": "لا مكان للمبالغات أو تأجيج الشكوك غير المبررة. بإشراف المؤسس <strong>أوميت هاكان كاراكايا</strong> (خبرة أكثر من 20 عاماً) ومساعدتنا الرقمية <strong>إلسا</strong>، نمنحك إجابات عقلانية وموضوعية وصالحة للاستخدام القضائي (المرافعات م.199).",
        "advisor_name": "إلسا وأوميت هاكان كاراكايا",
        "advisor_status": "محقّق الجيل الجديد • متصل الآن",
        "advisor_sub": "رئيس UÖDED • خبرة 20+ عاماً",
        "policy_title": "مبدأ الابتعاد عن فخاخ الوهم",
        "policy_text": "يتم تحليل أسئلتكم بموضوعية تامة ووفق أحكام القانون وحماية الخصوصية، حرصاً على أموالكم وحقوقكم المشروعة.",
        "topics_title": "مواضيع سريعة (بنقرة واحدة)",
        "topics_count": "9 مواضيع",
        "topics": [
            ("dedektif-tutmak", "🕵️‍♂️", "هل الاستعانة بمحقق قانونية؟"),
            ("dedektif-ucretleri", "💳", "كم تبلغ أسعار المحقق الخاص؟"),
            ("delil-gecerliligi", "⚖️", "هل الأدلة مقبولة في المحكمة؟"),
            ("almanya-es-takibi", "🇩🇪", "متابعة الزوج/الزوجة من أوروبا"),
            ("aldatan-erkek", "💔", "علامات الخيانة والحدود القانونية"),
            ("tatilde-aldatma", "🏖️", "العطلات والرحلات المشبوهة"),
            ("miras-borclu", "📍", "تحديد العناوين وكشف المدينين"),
            ("nafaka-gelir", "🏢", "كشف الدخل المخفي لإلغاء النفقة"),
            ("dedektif-olmak", "🎓", "كيف تصبح محققاً خاصاً معتمداً؟")
        ],
        "helpline_label": "استشارة رسمية على مدار الساعة:",
        "chat_status": "مستشار قانوني مباشر وصادق",
        "reset_btn": "إعادة ضبط المحادثة",
        "placeholder": "اكتب سؤالك بكل صراحة لمحقّق الجيل الجديد...",
        "send_btn": "اسأل محقّق الجيل الجديد",
        "trust_1": "مجهول الهوية 100%",
        "trust_2": "لا يتم حفظ السجلات",
        "trust_3": "تشفير SSL 256-Bit",
        "trust_4": "المرافعات م.199"
    },
    "me": {
        "badge": "DETEKTIV NOVE GENERACIJE • LIVE FORENZIČKI ČET",
        "title": "Pitajte Detektiva Nove Generacije",
        "subtitle": "Bez raspirivanja paranoje i predrasuda potvrđivanja. Pod vođstvom osnivača <strong>Ümita Hakana Karakaye</strong> (20+ godina forenzičkog iskustva) i AI asistentkinje <strong>Else</strong>, nudimo iskrene, racionalne i sudski validne odgovore u zakonskim okvirima (ZPP čl. 199).",
        "advisor_name": "Elsa & Ümit Hakan Karakaya",
        "advisor_status": "Detektiv Nove Generacije • Aktivan",
        "advisor_sub": "Predsjednik UÖDED • 20+ Godina Iskustva",
        "policy_title": "Princip bez zablude potvrđivanja",
        "policy_text": "Vaša pitanja se analiziraju hladne glave i strogo zakonito, štiteći vas od nepotrebnih troškova i neosnovanih sumnji.",
        "topics_title": "BRZE TEME (1 KLIK)",
        "topics_count": "9 Tema",
        "topics": [
            ("dedektif-tutmak", "🕵️‍♂️", "Da li je angažovanje detektiva legalno?"),
            ("dedektif-ucretleri", "💳", "Koliko koštaju usluge detektiva?"),
            ("delil-gecerliligi", "⚖️", "Da li su dokazi priznati na sudu?"),
            ("almanya-es-takibi", "🇩🇪", "Nadzor supružnika iz inostranstva"),
            ("aldatan-erkek", "💔", "Znaci nevjere & zakonske granice"),
            ("tatilde-aldatma", "🏖️", "Sumnjiva putovanja i odmori"),
            ("miras-borclu", "📍", "Pronalaženje adrese i dužnika"),
            ("nafaka-gelir", "🏢", "Skriveni prihodi za ukidanje alimentacije"),
            ("dedektif-olmak", "🎓", "Kako postati licencirani detektiv?")
        ],
        "helpline_label": "24/7 Zvanične konsultacije:",
        "chat_status": "Iskren, racionalan i zakonit online savjetnik",
        "reset_btn": "Restartuj čet",
        "placeholder": "Postavite pitanje Detektivu Nove Generacije...",
        "send_btn": "Pitajte Detektiva",
        "trust_1": "100% Anonimno",
        "trust_2": "Bez evidencije",
        "trust_3": "256-Bit SSL",
        "trust_4": "Usklađeno sa ZPP čl. 199"
    }
}

def generate_section_html(cfg):
    topics_html = ""
    mobile_topics_html = ""
    for key, icon, label in cfg["topics"]:
        topics_html += f'''                                    <button type="button" onclick="selectAIChatPreset('{key}')" class="w-full text-left px-3 py-2 rounded-xl bg-[#1D1D1F] hover:bg-[#252528] text-white/80 hover:text-white text-xs border border-white/10 flex items-center justify-between transition group">
                                        <span class="flex items-center gap-2 truncate">
                                            <span class="text-sm shrink-0">{icon}</span>
                                            <span class="truncate">{label}</span>
                                        </span>
                                        <i class="hgi hgi-stroke hgi-arrow-right-01 w-3 h-3 text-white/40 group-hover:text-[#93F051] shrink-0"></i>
                                    </button>\n'''
        short_lbl = label.split('?')[0].split('&')[0].strip()
        mobile_topics_html += f'''                                <button type="button" onclick="selectAIChatPreset('{key}')" class="whitespace-nowrap px-2.5 py-1 rounded-full bg-white/5 text-white/80 border border-white/10 shrink-0">{icon} {short_lbl}</button>\n'''

    return f"""        <!-- 3. YENİ NESİL DEDEKTİF / DEDEKTİF'E SOR (#dedektife-sor - Studio Obsidian Dark #111111) -->
        <section id="dedektife-sor" class="py-14 sm:py-20 bg-[#111111] text-[#FFFFFF] border-y border-white/10 relative overflow-hidden">
            <!-- Subtle Radial Ambient Glow -->
            <div class="pointer-events-none absolute -top-40 left-1/2 -translate-x-1/2 w-[700px] h-[350px] bg-[#93F051]/10 rounded-full blur-[120px]"></div>

            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 space-y-8 sm:space-y-10">

                <!-- Header -->
                <div class="text-center max-w-4xl mx-auto space-y-3.5">
                    <div class="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-[#1D1D1F] border border-[#93F051]/30 text-xs font-medium text-[#FFFFFF]">
                        <span class="w-2 h-2 rounded-full bg-[#93F051] animate-pulse"></span>
                        <span class="text-[#93F051] font-mono uppercase tracking-wider text-[11px]">{cfg["badge"]}</span>
                    </div>
                    <h2 class="apple-heading text-3xl sm:text-4xl lg:text-5xl font-medium text-[#FFFFFF] tracking-tight">
                        {cfg["title"]}
                    </h2>
                    <p class="text-sm sm:text-base text-white/75 leading-relaxed font-regular max-w-3xl mx-auto">
                        {cfg["subtitle"]}
                    </p>
                </div>

                <!-- Chat Studio Card (Apple-style Dark Frame) -->
                <div class="rounded-[28px] sm:rounded-[32px] bg-[#161618] border border-white/10 overflow-hidden shadow-2xl grid lg:grid-cols-12 items-stretch">
                    
                    <!-- Left Sidebar (lg:col-span-4): Advisor Profile + Quick Topic Chips + Direct Contacts -->
                    <div class="order-2 lg:order-1 lg:col-span-4 bg-[#121214] p-5 sm:p-6 border-t lg:border-t-0 lg:border-r border-white/10 flex flex-col justify-between space-y-5">
                        <div class="space-y-4">
                            <!-- Advisor Card -->
                            <div class="rounded-2xl bg-[#18181A] border border-white/10 p-3.5 flex items-center gap-3">
                                <div class="relative w-12 h-12 rounded-full overflow-hidden shrink-0 border border-[#93F051]/50">
                                    <img src="../assets/photos/elsa-dedektif-asistan.jpg" alt="Elsa — Next Gen Detective Assistant" class="w-full h-full object-cover object-top">
                                    <span class="absolute bottom-0 right-0 w-3 h-3 rounded-full bg-[#93F051] border-2 border-[#121214]"></span>
                                </div>
                                <div class="min-w-0 flex-1">
                                    <div class="text-xs sm:text-[13px] font-medium text-white flex items-center justify-between">
                                        <span class="truncate">{cfg["advisor_name"]}</span>
                                    </div>
                                    <div class="text-[10.5px] text-[#93F051] font-mono truncate">{cfg["advisor_status"]}</div>
                                    <div class="text-[10px] text-white/50 truncate">{cfg["advisor_sub"]}</div>
                                </div>
                            </div>

                            <!-- Anti Echo-Chamber Principle Note -->
                            <div class="rounded-xl bg-[#93F051]/5 border border-[#93F051]/20 p-3 text-[11px] text-white/80 leading-relaxed space-y-1">
                                <div class="font-mono text-[#93F051] text-[10px] font-bold uppercase tracking-wider flex items-center gap-1.5">
                                    <i class="hgi hgi-stroke hgi-shield-check w-3.5 h-3.5"></i>
                                    <span>{cfg["policy_title"]}</span>
                                </div>
                                <p>{cfg["policy_text"]}</p>
                            </div>

                            <!-- Quick Topics -->
                            <div class="space-y-2">
                                <div class="flex items-center justify-between">
                                    <span class="text-[10.5px] font-mono text-white/60 uppercase tracking-wider">{cfg["topics_title"]}</span>
                                    <span class="text-[9.5px] font-mono text-[#93F051]">{cfg["topics_count"]}</span>
                                </div>
                                <div class="grid grid-cols-1 gap-1.5 max-h-[280px] overflow-y-auto pr-1 scrollbar-thin scrollbar-thumb-white/10" id="aiQuickChips">
{topics_html.rstrip()}
                                </div>
                            </div>
                        </div>

                        <!-- 7/24 Direct Helpline Footer in Sidebar -->
                        <div class="pt-3 border-t border-white/10 flex items-center justify-between gap-2 text-[11px]">
                            <div class="text-white/60">
                                <div>{cfg["helpline_label"]}</div>
                                <a href="tel:03122840299" class="font-mono text-white hover:text-[#93F051] font-medium transition">0312 284 02 99</a>
                            </div>
                            <a href="https://wa.me/905326667749?text=Hello%20DAT%20Detective" target="_blank" rel="noopener noreferrer" class="px-3 py-1.5 rounded-lg bg-[#25D366] text-[#111111] font-medium text-[10.5px] flex items-center gap-1 hover:bg-[#20ba59] transition" title="7/24 WhatsApp: +90 532 666 77 49">
                                <i class="hgi hgi-stroke hgi-whatsapp w-3.5 h-3.5"></i>
                                <span>+90 532 666 77 49</span>
                            </a>
                        </div>
                    </div>

                    <!-- Right Main Chat Panel (lg:col-span-8): Chat Header, Message Scroll Area, Docked Input -->
                    <div class="order-1 lg:order-2 lg:col-span-8 flex flex-col justify-between bg-[#18181A] min-h-[520px] sm:min-h-[580px] max-h-[720px] relative">
                        
                        <!-- Chat Header -->
                        <div class="p-3.5 sm:p-4 px-5 bg-[#141416] border-b border-white/10 flex items-center justify-between shrink-0">
                            <div class="flex items-center gap-2.5">
                                <div class="w-8 h-8 rounded-full bg-[#1D1D1F] border border-[#93F051]/40 flex items-center justify-center shrink-0">
                                    <i class="hgi hgi-stroke hgi-message-programming w-4 h-4 text-[#93F051]"></i>
                                </div>
                                <div>
                                    <div class="text-xs sm:text-sm font-medium text-white flex items-center gap-2">
                                        <span>{cfg["title"]}</span>
                                        <span class="w-2 h-2 rounded-full bg-[#93F051] animate-ping"></span>
                                    </div>
                                    <div class="text-[10px] text-white/50 font-mono">{cfg["chat_status"]}</div>
                                </div>
                            </div>
                            <button type="button" onclick="resetAIChat()" class="px-2.5 py-1 rounded-lg bg-white/5 hover:bg-white/10 text-white/60 hover:text-white text-[10.5px] font-mono flex items-center gap-1 transition" title="{cfg["reset_btn"]}">
                                <i class="hgi hgi-stroke hgi-reload w-3 h-3"></i>
                                <span>{cfg["reset_btn"]}</span>
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
{mobile_topics_html.rstrip()}
                            </div>

                            <!-- Input Row -->
                            <div class="flex items-end gap-2 bg-[#1A1A1D] border border-white/15 focus-within:border-[#93F051] rounded-2xl p-1.5 pl-3 transition shadow-inner">
                                <textarea id="aiChatInput" rows="1" placeholder="{cfg["placeholder"]}" class="flex-1 bg-transparent border-0 text-xs sm:text-sm text-white placeholder-white/40 focus:outline-none resize-none py-2 max-h-28 leading-relaxed"></textarea>
                                <button type="button" id="aiSendBtn" onclick="sendAIChatMessage()" class="px-4 sm:px-5 py-2.5 rounded-xl bg-[#93F051] hover:bg-[#82dc43] text-[#111111] font-semibold text-xs sm:text-sm flex items-center justify-center gap-1.5 shrink-0 transition active:scale-95 shadow-md shadow-[#93F051]/20">
                                    <span>{cfg["send_btn"]}</span>
                                    <i class="hgi hgi-stroke hgi-sent w-4 h-4 text-[#111111]"></i>
                                </button>
                            </div>

                            <!-- Trust Badges -->
                            <div class="flex items-center justify-center gap-3 sm:gap-4 text-[10px] sm:text-[10.5px] font-mono text-white/50">
                                <span class="flex items-center gap-1"><i class="hgi hgi-stroke hgi-security-check w-3 h-3 text-[#93F051]"></i> {cfg["trust_1"]}</span>
                                <span>•</span>
                                <span class="flex items-center gap-1"><i class="hgi hgi-stroke hgi-shield-tick w-3 h-3 text-[#93F051]"></i> {cfg["trust_2"]}</span>
                                <span>•</span>
                                <span class="flex items-center gap-1"><i class="hgi hgi-stroke hgi-lock-password w-3 h-3 text-[#93F051]"></i> {cfg["trust_3"]}</span>
                                <span>•</span>
                                <span class="flex items-center gap-1"><i class="hgi hgi-stroke hgi-justice-scale-01 w-3 h-3 text-[#93F051]"></i> {cfg["trust_4"]}</span>
                            </div>
                        </div>

                    </div>

                </div>

            </div>
        </section>"""

def update_localized_index():
    for lang, cfg in LANG_CONFIGS.items():
        sec_html = generate_section_html(cfg)
        for rel_path in [f"{lang}/index.html", f"Dat/{lang}/index.html"]:
            full_path = os.path.join(BASE_DIR, rel_path)
            if not os.path.exists(full_path):
                continue
            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()

            content = re.sub(
                r'<!--\s*3\.\s*DEDEKTİF\'E SOR[\s\S]*?</section>',
                sec_html.strip(),
                content,
                count=1
            )

            # Update navbar links if present
            content = re.sub(
                r'<a href="#dedektife-sor" class="px-2\.5 py-1\.5 rounded-full hover:bg-white/10 text-\[#93F051\] font-medium transition inline-flex items-center gap-1\.5 whitespace-nowrap"[^>]*>[\s\S]*?</a>',
                f'<a href="#dedektife-sor" class="px-2.5 py-1.5 rounded-full hover:bg-white/10 text-[#93F051] font-medium transition inline-flex items-center gap-1.5 whitespace-nowrap"><span class="w-1.5 h-1.5 rounded-full bg-[#93F051] animate-pulse shrink-0"></span><span>{cfg["title"]}</span></a>',
                content
            )

            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Updated {rel_path} with localized Chat Studio.")

if __name__ == "__main__":
    update_localized_index()
