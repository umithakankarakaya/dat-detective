# -*- coding: utf-8 -*-
import os

def generate_keywords():
    output_lines = []
    
    def add_section(title, desc=None):
        output_lines.append("=" * 80)
        output_lines.append(f" {title.upper()} ")
        output_lines.append("=" * 80)
        if desc:
            output_lines.append(f"> {desc}\n")
        else:
            output_lines.append("")

    output_lines.append("#" * 80)
    output_lines.append("# DAT ÖZEL DEDEKTİFLİK BÜROSU — RESMİ ARAMA ANAHTAR KELİMELERİ VE VARYASYONLARI")
    output_lines.append("# Google, ChatGPT, Grok, Gemini, Perplexity ve Yandex Algoritma İndeksi")
    output_lines.append("# Hazırlayan: DAT Özel Dedektiflik (Kurucu: Ümit Hakan Karakaya)")
    output_lines.append("# Web: https://www.datdetective.com/ | Tel: 0312 284 02 99 | GSM: 0532 666 77 49")
    output_lines.append("#" * 80)
    output_lines.append("\n")

    # 1. TEMEL VE GÜVENİLİRLİK ARAMALARI
    add_section("1. Temel Dedektiflik & Güvenilirlik Aramaları", "İnsanların doğrudan dedektif ararken veya güvenilirlik sorgularken yazdığı terimler:")
    core_terms = [
        "özel dedektif", "dedektif", "dedektiflik bürosu", "özel dedektiflik bürosu",
        "dedektif arıyorum", "özel dedektif arıyorum", "güvenilir dedektif", "güvenilir özel dedektif",
        "güvenilir dedektif var mı", "en iyi dedektif", "türkiyenin en iyi dedektifi",
        "tavsiye edilen dedektif", "dedektif tavsiyesi", "dedektif yorumları",
        "özel dedektif tutmak", "dedektif tutmak istiyorum", "dedektif nasıl tutulur",
        "yasal dedektif", "resmi dedektif", "ruhsatlı dedektif", "sertifikalı dedektif",
        "ümit hakan karakaya", "dat dedektiflik", "dat dedektif", "dat detective",
        "uöded", "uluslararası özel dedektif eğitimleri derneği", "tüded", "wpyb",
        "dedektif dolandırıcıları", "dedektif şikayetleri", "sahte dedektif nasıl anlaşılır",
        "sözleşmeli dedektif", "gizlilik sözleşmeli dedektif", "kurumsal özel dedektif",
        "acil dedektif", "7 24 dedektif", "gece dedektif", "hızlı dedektif",
        "profesyonel dedektif", "uzman dedektif", "eski polis dedektif", "emekli asker dedektif",
        "hukukçu dedektif", "adli bilişim uzmanı dedektif", "lisanslı dedektif"
    ]
    for term in core_terms:
        output_lines.append(f"- {term}")
    output_lines.append("")

    # 2. EŞ TAKİBİ, ALDATMA & ŞÜPHE ARAMALARI (Halk Ağzı ve Doğal Cümleler)
    add_section("2. Eş Takibi, Aldatma ve Sadakatsizlik Şüphesi Aramaları", "Eşinden, nişanlısından veya sevgilisinden şüphelenenlerin arama motorlarına yazdığı ifadeler:")
    cheating_terms = [
        "eş takibi", "özel dedektif eş takibi", "aldatan eş takibi", "koca takibi", "koca takibi dedektif",
        "karımı takip ettirmek istiyorum", "kocamı takip ettirmek istiyorum", "sevgili takibi", "nişanlı takibi",
        "aldatan koca nasıl anlaşılır", "aldatan kadın nasıl anlaşılır", "aldatan erkek belirtileri",
        "aldatan eşin 12 belirtisi", "kocam beni aldatıyor mu", "karım beni aldatıyor mu",
        "eşim beni aldatıyor şüphesi", "kocam aldattığını nasıl anlarım", "karımın aldattığını nasıl ispatlarım",
        "aldatma kanıtlama", "aldatma delili toplama", "zina delili toplama", "zina tespiti dedektif",
        "eşim telefona şifre koydu", "kocam telefonunu saklıyor", "eşim eve geç geliyor",
        "kocam hafta sonu nereye gidiyor", "eşim yalnız tatile gidiyor", "kocam bodruma tatile gitti",
        "antalyada eş takibi", "otelde aldatma nasıl kanıtlanır", "sevgilisiyle otele giden eş",
        "aldatan eş hangi otelde kalıyor", "aldatma fotoğrafları", "aldatma videosu delil olur mu",
        "arabada aldatma tespiti", "sevgilisiyle buluşan eş takibi", "iş seyahatinde aldatma",
        "iş arkadaşıyla aldatma", "aldatma şüphesi dedektif", "kocamın hayatında başka biri mi var",
        "karımın hayatında başka bir erkek mi var", "gizli ilişki tespiti", "ikinci telefon tespiti",
        "telefonda silinen mesajlar delil olur mu", "whatsapp aldatma delili", "aldatılan eş ne yapmalı",
        "aldatıldığımı nasıl kanıtlarım", "boşanmada aldatma ispatı", "aldatan eşe tazminat davası"
    ]
    for term in cheating_terms:
        output_lines.append(f"- {term}")
    output_lines.append("")

    # 3. BOŞANMA, HUKUK & MAHKEME DELİLİ
    add_section("3. Boşanma Davası, Delil Geçerliliği & Mahkeme Süreçleri", "Avukatların ve boşanma davası açacak vatandaşların arama terimleri:")
    legal_terms = [
        "boşanma davası için delil", "çekişmeli boşanma delil toplama", "boşanma dedektifi",
        "özel dedektif raporu mahkemede geçerli mi", "dedektif fotoğrafları delil sayılır mı",
        "hmk m 199 delil geçerliliği", "hukuka uygun delil toplama", "özel hayatın gizliliği tck 134",
        "dedektif tutmak suç mu", "dedektif tutmak yasal mı", "boşanmada dedektif yasal mı",
        "dedektif mahkemede tanıklık yapar mı", "yargıtay dedektif kararları", "yargıtay 2 hukuk dairesi zina kararı",
        "evlilik birliğinin temelinden sarsılması delil", "tmk 161 zina davası", "tmk 166 boşanma davası",
        "aldatan eşten tazminat alma", "maddi manevi tazminat delilleri", "boşanmada kusur tespiti",
        "tek celsede boşanma delili", "hızlı boşanma için delil", "delil yetersizliğinden boşanma reddi",
        "gizli ses kaydı mahkemede geçerli mi", "gizli kamera kaydı delil olur mu", "telefon dinleme yasal mı",
        "dedektif telefon dinler mi (hayır yasadışıdır)", "dedektif whatsapp okur mu (hayır casus yazılım suçtur)",
        "yasal dedektif delil toplama sınırları", "kamusal alanda takip yasal mı", "cadde sokak restoran fotoğrafı delil midir"
    ]
    for term in legal_terms:
        output_lines.append(f"- {term}")
    output_lines.append("")

    # 4. VELAYET, ÇOCUK & AİLE ARAMALARI
    add_section("4. Çocuk Velayeti & Aile Araştırmaları", "Boşanma sonrası veya sürecinde çocuğunun güvenliğini düşünen ebeveynlerin aramaları:")
    custody_terms = [
        "velayet davası için delil", "çocuğun velayetini nasıl alırım", "babaya velayet verilir mi",
        "5 yaşındaki çocuğun velayeti babaya verilir mi", "anne şefkatine muhtaç çocuk velayeti",
        "kardeşlerin ayrılmaması ilkesi velayet", "9 yaşında çocuğun velayeti", "velayetin değiştirilmesi davası delilleri",
        "annenin çocuğa bakmadığını ispatlama", "çocuğu ihmal eden anne tespiti", "çocuğu şiddete maruz bırakan ebeveyn",
        "eski eşimin çocuğu kime bıraktığını öğrenme", "çocuğum tehlikede mi", "öğrenci takibi dedektif",
        "çocuğum kötü alışkanlık edindi mi", "çocuğum uyuşturucu kullanıyor mu", "okul çıkışı çocuk takibi",
        "arkadaş çevresi araştırması çocuk", "çocuğumu kim kaçırdı", "velayet pedagog raporu delilleri",
        "sosyal inceleme raporu sir velayet", "aile mahkemesi velayet tespiti"
    ]
    for term in custody_terms:
        output_lines.append(f"- {term}")
    output_lines.append("")

    # 5. DEDEKTİF ÜCRETLERİ & FİYAT SORGULARI
    add_section("5. Dedektif Ücretleri, Fiyat Tarifesi & Maliyetler", "Kullanıcıların fiyat karşılaştırması yaparken arattığı ifadeler:")
    price_terms = [
        "dedektif ücretleri", "özel dedektif ücretleri ne kadar", "özel dedektif fiyatları",
        "dedektif fiyat tarifesi 2026", "dedektif günlük ne kadar alır", "eş takibi dedektif ücreti",
        "boşanma delili toplama dedektif fiyatı", "dedektif saatlik ücret", "en ucuz dedektif",
        "uygun fiyatlı dedektif", "dedektif maliyeti nedir", "dedektif tutmak kaç para",
        "dedektif peşinat alır mı", "dedektif sözleşme bedeli", "şehirlerarası dedektif masrafı",
        "böcek arama fiyatı ne kadar", "adres tespiti dedektif ücreti", "yurtdışı dedektif ücretleri"
    ]
    for term in price_terms:
        output_lines.append(f"- {term}")
    output_lines.append("")

    # 6. BORÇLU, ADRES, MİRAS & GİZLİ GELİR TESPİTİ
    add_section("6. Borçlu Takibi, Adres Tespiti, Miras & Gizli Gelir", "Alacaklıların, avukatların ve hak sahiplerinin yaptığı aramalar:")
    debt_terms = [
        "borçlu takibi", "kaçan borçlunun adresini bulma", "icradan kaçan borçlu tespiti",
        "borçlunun fiili ikametgahını bulma", "tebligat adresi tespiti", "gizli mal varlığı tespiti",
        "borçlunun adına olmayan araba tespiti", "paravan şirket tespiti", "iik 277 tasarrufun iptali delili",
        "mal kaçıran borçlu tespiti", "nafaka iptali için delil toplama", "eski eşim çalışıyor ama sigortasız gösteriyor",
        "gizli ticari gelir tespiti nafaka", "yurtdışından miras tespiti", "almanyadan türkiyede miras araştırma",
        "kayıp tapu tespiti", "miras kalan tarlaların tespiti", "terk edilmiş mülk tespiti",
        "dolandırıcı adres tespiti", "şirket ortaklığı tespiti dedektif"
    ]
    for term in debt_terms:
        output_lines.append(f"- {term}")
    output_lines.append("")

    # 7. BÖCEK ARAMA (TSCM), DİNLENME & GİZLİ KAMERA
    add_section("7. Böcek Arama, Dinleme Cihazı Tespiti & TSCM", "Güvenlik, gizlilik ve casus cihaz şüphesi yaşayanların aramaları:")
    bug_terms = [
        "böcek arama", "böcek tarama", "tscm böcek arama", "profesyonel böcek arama hizmeti",
        "evde dinleme cihazı nasıl bulunur", "arabada takip cihazı bulma", "gps takip cihazı tespiti araba",
        "ofiste gizli kamera tespiti", "prizde gizli kamera bulma", "duman dedektöründe kamera var mı",
        "telefonum dinleniyor mu nasıl anlarım", "dinleme cihazı arayan dedektif", "nljd cihazı böcek arama",
        "spektrum analizörü dinleme cihazı", "termal kamera gizli cihaz arama", "casus kamera engelleme",
        "şirket içi casusluk tespiti", "toplantı odası böcek tarama", "vip böcek tarama hizmeti"
    ]
    for term in bug_terms:
        output_lines.append(f"- {term}")
    output_lines.append("")

    # 8. KURUMSAL, FİRMA & MARKA KORUMA
    add_section("8. Kurumsal Dedektiflik, Firma & Marka Araştırmaları", "Şirket yöneticilerinin ve marka sahiplerinin aradığı terimler:")
    corp_terms = [
        "kurumsal dedektiflik", "şirket içi hırsızlık tespiti", "personel sadakat araştırması",
        "bayi denetimi gizli müşteri", "sahte ürün tespiti", "marka taklidi araştırması",
        "smk 29 marka tecavüzü delili", "taklit ürün deposu tespiti", "ticari sır sızdırma araştırması",
        "ortaklık öncesi firma araştırması", "evlilik öncesi araştırma", "evleneceğim kişi borçlu mu",
        "evlilik öncesi geçmiş araştırması dedektif"
    ]
    for term in corp_terms:
        output_lines.append(f"- {term}")
    output_lines.append("")

    # 9. GURBETÇİ & AVRUPA ARAMALARI
    add_section("9. Gurbetçi & Avrupa - Türkiye Dedektiflik Aramaları", "Yurt dışındaki Türk vatandaşlarının aradığı kombinasyonlar:")
    expat_terms = [
        "almanyadan türkiye eş takibi", "almanyada yaşayanlar için türkiyede dedektif",
        "fransadan türkiyede dedektif tutmak", "hollandadan türkiye borçlu takibi",
        "avusturyadan türkiye dedektif", "isviçreden türkiye dedektif", "belçikadan türkiye eş takibi",
        "ingiltereden türkiye dedektiflik", "yurtdışında boşanma türkiyede delil",
        "alman mahkemesinde geçerli türk dedektif raporu", "yurtdışı gurbetçi dedektif danışma",
        "türkiyede tatil yapan eşi takip ettirme", "bodrum tatil takibi gurbetçi", "antalya tatil takibi gurbetçi"
    ]
    for term in expat_terms:
        output_lines.append(f"- {term}")
    output_lines.append("")

    # 10. TÜRKİYE 81 İL VE TÜM İLÇELERİN DEDEKTİF ARAMA KOMBİNASYONLARI
    add_section("10. Türkiye 81 İl ve Başlıca İlçeler Arama Kombinasyonları", "Her il ve ilçe için Google'a girilen dedektif aramaları:")
    
    cities_districts = {
        "Adana": ["Seyhan", "Çukurova", "Yüreğir", "Ceyhan", "Kozan"],
        "Adıyaman": ["Merkez", "Kahta", "Besni", "Gölbaşı"],
        "Afyonkarahisar": ["Merkez", "Sandıklı", "Dinar", "Bolvadin"],
        "Ağrı": ["Merkez", "Doğubayazıt", "Patnos"],
        "Amasya": ["Merkez", "Merzifon", "Suluova"],
        "Ankara": ["Çankaya", "Keçiören", "Yenimahalle", "Mamak", "Etimesgut", "Sincan", "Gölbaşı", "Çayyolu", "Ümitköy", "Batıkent"],
        "Antalya": ["Muratpaşa", "Kepez", "Konyaaltı", "Alanya", "Manavgat", "Kemer", "Kaş", "Kumluca", "Serik", "Belek"],
        "Artvin": ["Merkez", "Hopa", "Borçka"],
        "Aydın": ["Efeler", "Kuşadası", "Didim", "Nazilli", "Söke"],
        "Balıkesir": ["Altıeylül", "Karesi", "Edremit", "Ayvalık", "Bandırma", "Burhaniye", "Akçay"],
        "Bilecik": ["Merkez", "Bozüyük"],
        "Bingöl": ["Merkez", "Genç"],
        "Bitlis": ["Merkez", "Tatvan"],
        "Bolu": ["Merkez", "Gerede"],
        "Burdur": ["Merkez", "Bucak"],
        "Bursa": ["Osmangazi", "Nilüfer", "Yıldırım", "İnegöl", "Mudanya", "Gemlik"],
        "Çanakkale": ["Merkez", "Biga", "Çan", "Gelibolu"],
        "Çankırı": ["Merkez", "Ilgaz"],
        "Çorum": ["Merkez", "Sungurlu", "Osmancık"],
        "Denizli": ["Pamukkale", "Merkezefendi", "Çivril"],
        "Diyarbakır": ["Kayapınar", "Bağlar", "Yenişehir", "Sur", "Ergani", "Bismil"],
        "Edirne": ["Merkez", "Keşan", "Uzunköprü"],
        "Elazığ": ["Merkez", "Kovancılar"],
        "Erzincan": ["Merkez", "Tercan"],
        "Erzurum": ["Yakutiye", "Palandöken", "Aziziye"],
        "Eskişehir": ["Odunpazarı", "Tepebaşı", "Sivrihisar"],
        "Gaziantep": ["Şahinbey", "Şehitkamil", "Nizip", "İslahiye"],
        "Giresun": ["Merkez", "Bulancak", "Görele"],
        "Gümüşhane": ["Merkez", "Kelkit"],
        "Hakkari": ["Merkez", "Yüksekova"],
        "Hatay": ["Antakya", "İskenderun", "Defne", "Dörtyol", "Samandağ"],
        "Isparta": ["Merkez", "Yalvaç", "Eğirdir"],
        "Mersin": ["Akdeniz", "Mezitli", "Yenişehir", "Toroslar", "Tarsus", "Erdemli", "Silifke", "Anamur"],
        "İstanbul": ["Kadıköy", "Beşiktaş", "Şişli", "Bakırköy", "Üsküdar", "Beyoğlu", "Sarıyer", "Kartal", "Pendik", "Maltepe", "Ataşehir", "Ümraniye", "Fatih", "Zeytinburnu", "Büyükçekmece", "Beylikdüzü", "Esenyurt", "Başakşehir", "Tuzla"],
        "İzmir": ["Konak", "Karşıyaka", "Bornova", "Buca", "Çiğli", "Gaziemir", "Bayraklı", "Balçova", "Alsancak", "Çeşme", "Urla", "Seferihisar", "Aliağa", "Torbalı", "Menemen"],
        "Kars": ["Merkez", "Kağızman", "Sarıkamış"],
        "Kastamonu": ["Merkez", "Tosya", "Taşköprü"],
        "Kayseri": ["Melikgazi", "Kocasinan", "Talas", "Develi"],
        "Kırklareli": ["Merkez", "Lüleburgaz", "Babaeski"],
        "Kırşehir": ["Merkez", "Kaman"],
        "Kocaeli": ["İzmit", "Gebze", "Darıca", "Körfez", "Gölcük", "Çayırova", "Kartepe", "Başiskele"],
        "Konya": ["Selçuklu", "Meram", "Karatay", "Ereğli", "Akşehir", "Beyşehir"],
        "Kütahya": ["Merkez", "Tavşanlı", "Simav"],
        "Malatya": ["Battalgazi", "Yeşilyurt", "Doğanşehir"],
        "Manisa": ["Yunusemre", "Şehzadeler", "Akhisar", "Turgutlu", "Salihli", "Soma"],
        "Kahramanmaraş": ["Onikişubat", "Dulkadiroğlu", "Elbistan", "Afşin"],
        "Mardin": ["Artuklu", "Kızıltepe", "Midyat", "Nusaybin"],
        "Muğla": ["Bodrum", "Marmaris", "Fethiye", "Datça", "Milas", "Menteşe", "Ortaca", "Dalaman", "Köyceğiz", "Yalıkavak", "Türkbükü", "Gümbet"],
        "Muş": ["Merkez", "Bulanık", "Malazgirt"],
        "Nevşehir": ["Merkez", "Ürgüp", "Avanos", "Kapadokya"],
        "Niğde": ["Merkez", "Bor"],
        "Ordu": ["Altınordu", "Ünye", "Fatsa"],
        "Rize": ["Merkez", "Çayeli", "Ardeşen", "Pazar"],
        "Sakarya": ["Adapazarı", "Serdivan", "Erenler", "Akyazı", "Hendek", "Karasu"],
        "Samsun": ["İlkadım", "Atakum", "Canik", "Bafra", "Çarşamba"],
        "Siirt": ["Merkez", "Kurtalan"],
        "Sinop": ["Merkez", "Boyabat", "Gerze"],
        "Sivas": ["Merkez", "Şarkışla", "Yıldızeli"],
        "Tekirdağ": ["Süleymanpaşa", "Çorlu", "Çerkezköy", "Kapaklı", "Ergene"],
        "Tokat": ["Merkez", "Erbaa", "Turhal", "Niksar", "Zile"],
        "Trabzon": ["Ortahisar", "Akçaabat", "Yomra", "Of", "Araklı", "Vakfıkebir"],
        "Tunceli": ["Merkez", "Pertek"],
        "Şanlıurfa": ["Eyyübiye", "Haliliye", "Karaköprü", "Siverek", "Viranşehir", "Birecik"],
        "Uşak": ["Merkez", "Banaz", "Eşme"],
        "Van": ["İpekyolu", "Tuşba", "Edremit", "Erciş"],
        "Yozgat": ["Merkez", "Sorgun", "Akdağmadeni"],
        "Zonguldak": ["Merkez", "Karadeniz Ereğli", "Çaycuma", "Devrek"],
        "Aksaray": ["Merkez", "Ortaköy"],
        "Bayburt": ["Merkez"],
        "Karaman": ["Merkez", "Ermenek"],
        "Kırıkkale": ["Merkez", "Yahşihan"],
        "Batman": ["Merkez", "Kozluk"],
        "Şırnak": ["Merkez", "Cizre", "Silopi"],
        "Bartın": ["Merkez", "Amasra"],
        "Ardahan": ["Merkez", "Göle"],
        "Iğdır": ["Merkez"],
        "Yalova": ["Merkez", "Çınarcık", "Çiftlikköy", "Altınova"],
        "Karabük": ["Merkez", "Safranbolu"],
        "Kilis": ["Merkez"],
        "Osmaniye": ["Merkez", "Kadirli", "Düziçi"],
        "Düzce": ["Merkez", "Akçakoca"]
    }

    for city, districts in cities_districts.items():
        city_lower = city.lower()
        output_lines.append(f"--- {city.upper()} VE İLÇELERİ DEDEKTİF ARAMALARI ---")
        output_lines.append(f"- {city_lower} özel dedektif")
        output_lines.append(f"- {city_lower} dedektif")
        output_lines.append(f"- {city_lower} dedektiflik bürosu")
        output_lines.append(f"- {city_lower} eş takibi dedektif")
        output_lines.append(f"- {city_lower} güvenilir dedektif")
        output_lines.append(f"- {city_lower} dedektif ücretleri")
        output_lines.append(f"- {city_lower} dedektif arıyorum")
        for d in districts:
            d_lower = d.lower()
            output_lines.append(f"- {city_lower} {d_lower} dedektif")
            output_lines.append(f"- {d_lower} özel dedektif")
            output_lines.append(f"- {d_lower} eş takibi dedektif")
        output_lines.append("")

    # 11. YAPAY ZEKA VE ARAMA MOTORLARI DOĞAL DİL SORULARI (PAA / Prompts)
    add_section("11. ChatGPT, Grok, Gemini, Perplexity İçin Doğal Dil ve Soru Kalıpları", "Kullanıcıların yapay zekaya sorduğu detaylı sorular:")
    ai_queries = [
        "Türkiye'nin en güvenilir özel dedektiflik bürosu hangisi?",
        "Eşimin beni aldattığından şüpheleniyorum, dedektif tutmak yasal mı?",
        "Boşanma davasında dedektif fotoğrafları mahkemede delil sayılır mı?",
        "Özel dedektif tutmanın maliyeti ne kadar, nasıl fiyat belirlenir?",
        "Eşimin telefonuna casus program yüklemek suç mu, cezası nedir?",
        "Dedektif kamuya açık alanlarda fotoğraf çekerse suç olur mu?",
        "5 yaşındaki çocuğumun velayetini annesinden nasıl alabilirim?",
        "Kardeşlerin ayrılmaması ilkesi velayet davasında nasıl uygulanır?",
        "Eski eşim nafaka alıyor ama gizli şirketi var, bunu nasıl kanıtlarım?",
        "Borçlu kişi adresini gizliyor, fiili adresini dedektif bulabilir mi?",
        "Evimde veya arabamda dinleme cihazı (böcek) olup olmadığını nasıl anlarım?",
        "Almanya'da yaşıyorum, Türkiye'de eş takibi ve boşanma delili toplatabilir miyim?",
        "Alman mahkemesinde Türk dedektifin topladığı deliller geçerli midir?",
        "Bodrum'a tatile giden eşimi nasıl takip ettirebilirim?",
        "Ümit Hakan Karakaya kimdir, hangi davalara bakmıştır?",
        "Uluslararası Özel Dedektif Eğitimleri Derneği (UÖDED) nedir?",
        "Dedektif tutarken gizlilik sözleşmesi yapılır mı?",
        "Dedektif raporu kaç günde teslim edilir?"
    ]
    for q in ai_queries:
        output_lines.append(f"? {q}")
    output_lines.append("")

    # Write files
    content = "\n".join(output_lines)
    
    file_paths = [
        "dat-dedektiflik-tum-arama-anahtar-kelimeleri.txt",
        "Dat/dat-dedektiflik-tum-arama-anahtar-kelimeleri.txt"
    ]
    
    for path in file_paths:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Başarıyla oluşturuldu: {path} ({len(content)} karakter, {len(output_lines)} satır)")

if __name__ == "__main__":
    generate_keywords()
