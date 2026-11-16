#!/usr/bin/env python3
"""
DAT Özel Dedektiflik — Türkiye 81 İl & İlçe Yerel SEO Hakimiyet Motoru
Bu script:
1. 12 adet yüksek arama hacimli il için (Muğla, Adana, Kocaeli, Gaziantep, Eskişehir, Trabzon, Kayseri, Aydın, Balıkesir, Tekirdağ, Samsun, Diyarbakır)
   HMK m.199 / TCK m.134 uyumlu, yerel adliye ve ilçe detaylı, Schema.org LegalService + FAQPage + Breadcrumb içeren landing page'leri üretir.
2. index.html'e 7 coğrafi bölge ve 81 ilin tamamını kapsayan crawlable "Türkiye 81 İl ve İlçeleri Dedektiflik Ağı" (#turkiye-dedektif-agi) modülünü ekler.
3. index.html'deki Schema.org LegalService areaServed alanına 81 ili AdministrativeArea olarak ekler.
4. _redirects ve sitemap.xml dosyalarını günceller.
5. Dat/ dizini ile root dosyalarını birebir senkronize eder.
"""

import os
import re
import json
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DAT_DIR = os.path.join(ROOT, "Dat")

# 12 Yeni Büyükşehir & Turizm Merkezi İl Verileri
NEW_CITIES = [
    {
        "slug": "mugla-ozel-dedektif",
        "title": "Muğla Dedektif & Özel Dedektiflik Bürosu (Bodrum, Marmaris, Fethiye) | DAT",
        "description": "Muğla özel dedektiflik hizmetleri. Bodrum, Marmaris, Fethiye, Datça ve tüm ilçelerde otel/tatil eş takibi, sadakat analizi, boşanma delili ve adres tespiti.",
        "keywords": "muğla dedektif, bodrum özel dedektif, marmaris dedektif, fethiye dedektif, datça dedektif, bodrum eş takibi, muğla dedektiflik bürosu, tatilde aldatma tespiti",
        "badge": "MUĞLA & EGE KIYILARI • BODRUM • MARMARİS • FETHİYE • 13 İLÇE",
        "h1": "Muğla Dedektif: Bodrum, Marmaris, Fethiye ve 13 İlçede Özel Dedektiflik",
        "lead": "Bodrum Yarımadası, Marmaris, Fethiye, Datça, Göcek ve Milas başta olmak üzere Muğla'nın 13 ilçesinde; yaz tatili seyahat takipleri, otel/marina gözlemi, eş takibi ve boşanma delili toplamada 2005'ten bu yana 4K teleobjektiflerle %100 gizlilikle hizmet veriyoruz.",
        "image": "assets/services/es-takibi.jpg",
        "districts_title": "Muğla ve Tatil Merkezlerinde Hizmet Verdiğimiz İlçeler (13 İlçe)",
        "districts_intro": "Muğla'nın sahil şeritleri, marinaları, lüks tatil köyleri ve iç ilçelerinin tamamında yerel mobil ekiplerimizle 7/24 kesintisiz saha çalışması yürütüyoruz:",
        "districts": [
            "Bodrum", "Fethiye", "Marmaris", "Milas", "Menteşe", "Datça", "Ortaca",
            "Dalaman", "Köyceğiz", "Seydikemer", "Ula", "Yatağan", "Kavaklıdere"
        ],
        "sections": [
            ("Muğla ve Bodrum'da Tatil Seyahati & Eş Takibinde Uzman Saha Ekipleri", "Türkiye'nin en popüler tatil destinasyonu olan Muğla, özellikle yaz aylarında tek başına tatil, arkadaş grubu seyahati veya şüpheli iş gezisi kisvesi altındaki aldatma vakalarının en yoğun yaşandığı bölgedir. 20 yılı aşkın adli saha tecrübesiyle kurucumuz Ümit Hakan Karakaya liderliğindeki DAT Özel Dedektiflik ekipleri; Milas-Bodrum ve Dalaman Havalimanları transferlerinden itibaren lüks oteller, beach clublar, restoranlar ve marinalarda hedef şahsı sıfır fark edilme riskiyle gözetim altında tutar."),
            ("Bodrum, Marmaris, Fethiye ve Göcek'te Yasal Delil Sınırları (HMK m.199)", "Otel odası veya konutun içi Anayasal mahrem alandır; kapalı alana gizli kamera yerleştirmek TCK m.134 uyarınca hapis cezası gerektirir. DAT Özel Dedektiflik olarak tüm tespitlerimizi havalimanı, otel lobisi, plaj, havuz başı, restoran, tekne iskelesi gibi kamuya açık ortak alanlarda 4K teleobjektiflerle gerçekleştiriyoruz. Elde edilen deliller Bodrum, Fethiye ve Muğla Aile Mahkemelerinde tek celsede kabul görür."),
            ("Muğla Genelinde Sunduğumuz Başlıca Dedektiflik Hizmetleri", "Bölgemizde en çok talep edilen hizmetler; TMK m.161 zina ve sadakatsizlik delili tespiti, yabancı ülke vatandaşlarıyla yapılan evliliklerde geçmiş araştırması, yazlık gayrimenkul ve lüks yat/araç gibi gizlenen varlıkların İİK kapsamında tespiti, velayet davalarında çocukların tatil ortamındaki güvenliğinin gözlemlenmesi ve lüks villa/otellerde TSCM böcek taramasıdır."),
            ("Muğla ve Bodrum Adliyelerine Uygun Resmi Raporlama", "Toplanan tüm kanıtlar; tarih-saat damgalı yüksek çözünürlüklü video, fotoğraf ve dakika dakika kronolojik gözlem tutanağıyla klasörlenerek avukatınıza teslim edilir. Hiçbir şüphe havada bırakılmaz; ak ya da kara, gerçek ne ise tüm çıplaklığıyla raporlanır.")
        ],
        "faqs": [
            ("Bodrum veya Marmaris'e ne kadar sürede ekip yönlendiriyorsunuz?", "Muğla kıyı şeridinde konuşlu yazlık saha birimlerimiz talep üzerine aynı gün (2–3 saat içinde) havalimanı veya otel takibine başlayabilmektedir."),
            ("Oteldeki kişinin kiminle kaldığını tespit edebilir misiniz?", "Otel odası içine girilmez veya dinleme yapılmaz. Ancak şahsın otele kiminle giriş yaptığı, lobide, restoranda ve plajda kiminle vakit geçirdiği kamuya açık alanlarda video ve fotoğrafla HMK m.199 standartlarında belgelenir."),
            ("Yurt dışından (Almanya, İngiltere vb.) Muğla için dedektif tutabilir miyim?", "Evet. Avrupa ve yurt dışındaki müvekkillerimiz için online gizlilik sözleşmesi düzenlenmekte, operasyon Elsa paneli üzerinden şifreli olarak anbean paylaşılmaktadır."),
            ("Muğla dedektiflik ücretleri nasıl belirlenir?", "Ücretlendirme; takip yapılacak gün sayısı, bölge genişliği (örn. Bodrum-Marmaris arası intikal) ve kullanılacak teknik araçlara göre peşin ve şeffaf olarak belirlenir; gizli masraf çıkarılmaz.")
        ]
    },
    {
        "slug": "adana-ozel-dedektif",
        "title": "Adana Dedektif & Özel Dedektiflik Bürosu (Seyhan, Çukurova) | DAT",
        "description": "Adana özel dedektif bürosu. Seyhan, Çukurova, Yüreğir, Sarıçam, Ceyhan ve 15 ilçede eş takibi, boşanma delili, aldatma tespiti ve borçlu adres araştırması.",
        "keywords": "adana dedektif, adana özel dedektif, seyhan dedektif, çukurova dedektif, adana dedektiflik bürosu, eş takibi adana, adana boşanma delili, ceyhan dedektif",
        "badge": "ADANA MERKEZ & ÇUKUROVA • SEYHAN • YÜREĞİR • 15 İLÇE",
        "h1": "Adana Dedektif: Seyhan, Çukurova ve 15 İlçede Özel Dedektiflik",
        "lead": "Seyhan, Çukurova (Turgut Özal, Gazipaşa, Barajyolu), Yüreğir, Sarıçam ve Ceyhan başta olmak üzere Adana'nın 15 ilçesinde; eş takibi, sadakat doğrulaması, boşanma delili toplama ve ticari suistimal araştırmalarında 20 yılı aşkın tecrübeyle 7/24 hizmet veriyoruz.",
        "image": "assets/services/es-takibi.jpg",
        "districts_title": "Adana Genelinde Hizmet Verdiğimiz Tüm İlçeler (15 İlçe)",
        "districts_intro": "Çukurova metropolünün merkez ilçelerinden çevre sanayi ve tarım ilçelerine kadar Adana genelinde mobil dedektiflik filomuzla görev yapıyoruz:",
        "districts": [
            "Seyhan", "Çukurova", "Yüreğir", "Sarıçam", "Ceyhan", "Kozan", "İmamoğlu",
            "Karataş", "Pozantı", "Yumurtalık", "Tufanbeyli", "Feke", "Aladağ", "Saimbeyli", "Karaisalı"
        ],
        "sections": [
            ("Adana'da 20 Yılı Aşkın Güvenilir Özel Dedektiflik Hizmeti", "Çukurova bölgesinin ticaret, sanayi ve kültür başkenti olan Adana'da özel dedektiflik çalışmaları; kentin dinamik yapısını, geniş coğrafyasını ve bölge insanının hassasiyetlerini bilen deneyimli bir ekip gerektirir. DAT Özel Dedektiflik, Adana'da müvekkillerine sözleşmeli, yasalara tam uyumlu ve mutlak gizlilik prensibiyle hizmet sunmaktadır."),
            ("Seyhan, Çukurova ve Ceyhan Hatlarında 7/24 Saha Operasyonu", "Seyhan ve Çukurova'nın yoğun caddeleri, Ziyapaşa Bulvarı, Gazipaşa, Barajyolu ve Turgut Özal Bulvarı üzerindeki mekanlar, gece kulüpleri ve otellerde çift vardiyalı ekiplerimiz görev yapmaktadır. Ayrıca Adana Hacı Sabancı OSB ve Ceyhan Enerji İhtisas Bölgesi'nde kurumsal dolandırıcılık ve ticari istihbarat araştırmaları yürütülmektedir."),
            ("Adana Aile Mahkemelerine Sunulan Yasal Delil Dosyaları (HMK m.199)", "Toplanan tüm fotoğraf ve video kayıtları kamuya açık alanlarda elde edilir ve TCK m.134'e aykırı hiçbir gizli dinleme veya casus yazılım kullanılmaz. Hazırlanan adli delil dosyaları Adana Bölge Adliye Mahkemesi ve Adana Aile Mahkemelerinde doğrudan hükme esas alınmaktadır.")
        ],
        "faqs": [
            ("Adana'da ne kadar sürede takibe başlayabilirsiniz?", "Adana merkez ve çevre ilçelerde aynı gün 2-4 saat içinde saha ekibimiz göreve başlayabilir."),
            ("Görüşmeler nasıl yürütülüyor?", "Görüşmeler telefon, şifreli WhatsApp veya talep üzerine Adana'da belirlenen nezih ve güvenli bir lokasyonda yüz yüze gerçekleştirilebilir."),
            ("Elde edilen deliller mahkemede geçerli mi?", "Evet. Tüm tespitler kamuya açık alanlarda HMK m.199 uyarınca tarih-saat damgalı olarak yapılır.")
        ]
    },
    {
        "slug": "kocaeli-ozel-dedektif",
        "title": "Kocaeli Dedektif & Özel Dedektiflik Bürosu (Gebze, İzmit) | DAT",
        "description": "Kocaeli özel dedektif bürosu. Gebze, İzmit, Darıca, Körfez, Gölcük ve 12 ilçede eş takibi, kurumsal firma araştırması, marka taklidi ve böcek arama.",
        "keywords": "kocaeli dedektif, gebze özel dedektif, izmit dedektif, darıca dedektif, körfez dedektif, gölcük dedektif, gebze dedektiflik bürosu, kocaeli eş takibi",
        "badge": "KOCAELİ SANAYİ & METROPOL • GEBZE • İZMİT • 12 İLÇE",
        "h1": "Kocaeli Dedektif: Gebze, İzmit, Darıca ve 12 İlçede Özel Dedektiflik",
        "lead": "Gebze Organize Sanayi Bölgesi (GOSB), İzmit, Darıca, Körfez, Gölcük, Çayırova ve Kartepe başta olmak üzere Kocaeli'nin 12 ilçesinde; eş takibi, ticari suistimal, fabrika hırsızlığı tespiti ve TSCM böcek taramasında lider dedektiflik hizmeti.",
        "image": "assets/services/kurumsal-ve-marka-koruma.jpg",
        "districts_title": "Kocaeli Genelinde Hizmet Verdiğimiz İlçeler (12 İlçe)",
        "districts_intro": "Marmara'nın üretim ve sanayi kalbi Kocaeli'nin tüm organize sanayi bölgelerinde ve metropol ilçelerinde aktif sahadayız:",
        "districts": [
            "Gebze", "İzmit", "Darıca", "Körfez", "Gölcük", "Çayırova", "Kartepe",
            "Başiskele", "Karamürsel", "Derince", "Kandıra", "Dilovası"
        ],
        "sections": [
            ("Gebze ve İzmit'te Bireysel ve Kurumsal Dedektiflik Lideri", "Kocaeli, hem yoğun nüfusu hem de Türkiye'nin en büyük sanayi kuruluşlarına ev sahipliği yapması nedeniyle hem bireysel aile hukuku takipleri hem de kurumsal marka/suistimal araştırmalarının en sık yürütüldüğü ildir. DAT Özel Dedektiflik, Gebze ve İzmit merkezli operasyonlarıyla bölgenin en yetkin adli araştırma kadrosuna sahiptir."),
            ("Kurumsal Dedektiflik, Marka Taklidi ve TSCM Böcek Arama", "GOSB, TOSB, İMES, Dilovası ve Kartepe OSB'lerindeki fabrikalarda üretim hırsızlıkları, haksız rekabet, ticari sır ifşası ve toplantı odalarında yabancı dinleme cihazı (böcek) taraması en son teknoloji NLJD analizörleriyle icra edilmektedir.")
        ],
        "faqs": [
            ("Gebze'deki fabrikamızda böcek taraması yapabilir misiniz?", "Evet. Spektrum analizörleri ve non-linear junction detector cihazlarımızla fabrikalar ve yönetim ofisleri aynı gün taranıp temizlik raporu verilir."),
            ("Kocaeli'de eş takibi ve boşanma delili toplama süreci nasıl işler?", "Hedef şahsın günlük hareket güzergahı kamuya açık alanlarda çift vardiya sivil araç ve motosikletle izlenir; HMK m.199 formatında raporlanır.")
        ]
    },
    {
        "slug": "gaziantep-ozel-dedektif",
        "title": "Gaziantep Dedektif & Özel Dedektiflik Bürosu (Şahinbey, Şehitkamil) | DAT",
        "description": "Gaziantep özel dedektif bürosu. Şahinbey, Şehitkamil, Nizip ve tüm ilçelerde eş takibi, sadakat araştırması, borçlu tespiti ve ticari firma istihbaratı.",
        "keywords": "gaziantep dedektif, gaziantep özel dedektif, şahinbey dedektif, şehitkamil dedektif, nizip dedektif, gaziantep dedektiflik bürosu, eş takibi gaziantep",
        "badge": "GÜNEYDOĞU SANAYİ & TİCARET • ŞAHİNBEY • ŞEHİTKAMİL • 9 İLÇE",
        "h1": "Gaziantep Dedektif: Şahinbey, Şehitkamil ve 9 İlçede Özel Dedektiflik",
        "lead": "Şahinbey, Şehitkamil, Nizip ve İslahiye başta olmak üzere Gaziantep'in 9 ilçesinde; eş takibi, evlilik öncesi araştırma, borçlu adres tespiti ve Organize Sanayi Bölgesi ticari araştırmalarında 7/24 resmi sözleşmeli dedektiflik hizmeti veriyoruz.",
        "image": "assets/services/es-takibi.jpg",
        "districts_title": "Gaziantep Genelinde Hizmet Verdiğimiz İlçeler (9 İlçe)",
        "districts_intro": "Güneydoğu'nun sanayi ve ticaret lokomotifi Gaziantep'in tüm merkez ve çevre ilçelerinde görev başındayız:",
        "districts": [
            "Şahinbey", "Şehitkamil", "Nizip", "İslahiye", "Nurdağı", "Araban", "Oğuzeli", "Yavuzeli", "Karkamış"
        ],
        "sections": [
            ("Gaziantep'te Yüksek Gizlilikle Özel Araştırma", "Bölgenin köklü aile yapısı ve dinamik ticaret hacmi dikkate alınarak tüm çalışmalar mutlak gizlilik sözleşmesiyle yürütülür. Aile içi uyuşmazlıklar, çekişmeli boşanmalar ve ticari alacak araştırmaları hukuka uygun delil disipliniyle yönetilir.")
        ],
        "faqs": [
            ("Gaziantep'te bilgi gizliliği nasıl korunuyor?", "DAT Özel Dedektiflik bünyesinde tüm bilgiler 256-bit şifrelenir ve dosya tamamlandığında veriler kalıcı olarak imha edilir.")
        ]
    },
    {
        "slug": "eskisehir-ozel-dedektif",
        "title": "Eskişehir Dedektif & Özel Dedektiflik Bürosu (Odunpazarı, Tepebaşı) | DAT",
        "description": "Eskişehir özel dedektiflik hizmetleri. Odunpazarı, Tepebaşı ve tüm ilçelerde eş takibi, öğrenci takibi, boşanma delili ve adres tespiti.",
        "keywords": "eskişehir dedektif, eskişehir özel dedektif, odunpazarı dedektif, tepebaşı dedektif, eskişehir öğrenci takibi, eskişehir eş takibi, eskişehir dedektiflik bürosu",
        "badge": "İÇ ANADOLU KÜLTÜR & ÜNİVERSİTE • ODUNPAZARI • TEPEBAŞI • 14 İLÇE",
        "h1": "Eskişehir Dedektif: Odunpazarı, Tepebaşı ve 14 İlçede Özel Dedektiflik",
        "lead": "Odunpazarı, Tepebaşı, Sivrihisar ve Çifteler başta olmak üzere Eskişehir'in 14 ilçesinde; eş takibi, Anadolu ve Osmangazi Üniversiteleri öğrenci takibi, boşanma delili ve adres tespiti hizmetleri sunuyoruz.",
        "image": "assets/services/ogrenci-takibi.jpg",
        "districts_title": "Eskişehir Genelinde Hizmet Verdiğimiz İlçeler (14 İlçe)",
        "districts_intro": "Eskişehir merkez metropol ilçeleri ve çevre ilçelerinde 7/24 aktif saha operasyonu yürütüyoruz:",
        "districts": [
            "Odunpazarı", "Tepebaşı", "Sivrihisar", "Çifteler", "Seyitgazi", "Alpu", "Mihalıççık",
            "Mahmudiye", "Beylikova", "İnönü", "Günyüzü", "Han", "Sarıcakaya", "Mihalgazi"
        ],
        "sections": [
            ("Eskişehir'de Öğrenci Takibi ve Aile Hukuku Çalışmaları", "Eskişehir'in büyük bir üniversite kenti olması sebebiyle ailelerin çocuklarının güvenliği, arkadaş çevresi ve zararlı alışkanlıklardan korunması yönündeki öğrenci takibi talepleri titizlikle sonuçlandırılmaktadır.")
        ],
        "faqs": [
            ("Öğrenci takibi nasıl yapılır?", "Öğrencinin okul dışındaki sosyal çevresi, kaldığı ortamlar ve temas ettiği şahıslar rencide edilmeden uzaktan gözlemlenir ve aileye günlük raporlanır.")
        ]
    },
    {
        "slug": "trabzon-ozel-dedektif",
        "title": "Trabzon Dedektif & Özel Dedektiflik Bürosu (Ortahisar, Akçaabat) | DAT",
        "description": "Trabzon özel dedektif bürosu. Ortahisar, Akçaabat, Yomra, Of ve tüm Karadeniz ilçelerinde eş takibi, boşanma delili, adres ve miras araştırması.",
        "keywords": "trabzon dedektif, trabzon özel dedektif, ortahisar dedektif, akçaabat dedektif, yomra dedektif, of dedektif, karadeniz dedektiflik bürosu, trabzon eş takibi",
        "badge": "DOĞU KARADENİZ MERKEZ • ORTAHİSAR • AKÇAABAT • 18 İLÇE",
        "h1": "Trabzon Dedektif: Ortahisar, Akçaabat ve 18 İlçede Özel Dedektiflik",
        "lead": "Ortahisar, Akçaabat, Yomra, Of, Araklı ve Sürmene başta olmak üzere Trabzon ve Doğu Karadeniz genelinde; eş takibi, sadakat analizi, yurt dışı (Almanya/Avrupa) bağlantılı aile araştırmaları ve miras tespiti hizmeti veriyoruz.",
        "image": "assets/services/es-takibi.jpg",
        "districts_title": "Trabzon Genelinde Hizmet Verdiğimiz İlçeler (18 İlçe)",
        "districts_intro": "Trabzon'un sahil ve yayla ilçelerinin tamamında yerel arazi şartlarına uygun sivil takip birimlerimizle görevdeyiz:",
        "districts": [
            "Ortahisar", "Akçaabat", "Araklı", "Of", "Yomra", "Arsin", "Vakfıkebir", "Sürmene",
            "Maçka", "Beşikdüzü", "Çarşıbaşı", "Tonya", "Düzköy", "Çaykara", "Şalpazarı", "Hayrat", "Köprübaşı", "Dernekpazarı"
        ],
        "sections": [
            ("Karadeniz Bölgesi ve Avrupa Bağlantılı Araştırmalar", "Trabzon'da özellikle Avrupa'da (Almanya, Fransa, Belçika) yaşayıp memleketteki eşi veya gayrimenkulleri hakkında teyit almak isteyen gurbetçilerimiz için şeffaf Elsa paneliyle canlı doğrulama sağlıyoruz.")
        ],
        "faqs": [
            ("Yurt dışından Trabzon için araştırma yaptırabilir miyim?", "Evet. Gurbetçi müvekkillerimiz için online sözleşme ve günlük video/fotoğraf iletimiyle çalışma yürütülmektedir.")
        ]
    },
    {
        "slug": "kayseri-ozel-dedektif",
        "title": "Kayseri Dedektif & Özel Dedektiflik Bürosu (Melikgazi, Kocasinan) | DAT",
        "description": "Kayseri özel dedektiflik bürosu. Melikgazi, Kocasinan, Talas, Develi ve 16 ilçede eş takibi, ticari borçlu tespiti ve boşanma delili toplama.",
        "keywords": "kayseri dedektif, kayseri özel dedektif, melikgazi dedektif, kocasinan dedektif, talas dedektif, kayseri eş takibi, kayseri dedektiflik bürosu, kayseri borçlu tespiti",
        "badge": "İÇ ANADOLU TİCARET & SANAYİ • MELİKGAZİ • KOCASİNAN • 16 İLÇE",
        "h1": "Kayseri Dedektif: Melikgazi, Kocasinan, Talas ve 16 İlçede Özel Dedektiflik",
        "lead": "Melikgazi, Kocasinan, Talas ve Develi başta olmak üzere Kayseri genelinde; eş takibi, sadakat analizi, Organize Sanayi ticari alacak ve borçlu adresi tespitinde kurumsal dedektiflik desteği sağlıyoruz.",
        "image": "assets/services/adres-ve-borclu-takibi.jpg",
        "districts_title": "Kayseri Genelinde Hizmet Verdiğimiz İlçeler (16 İlçe)",
        "districts_intro": "Kayseri metropolü ve çevre sanayi ilçelerinde aktif saha takibi yürütmekteyiz:",
        "districts": [
            "Melikgazi", "Kocasinan", "Talas", "Develi", "Yahyalı", "Bünyan", "Pınarbaşı",
            "Tomarza", "Yeşilhisar", "Sarıoğlan", "Hacılar", "Sarız", "Felahiye", "Akkışla", "Özvatan", "İncesu"
        ],
        "sections": [
            ("Ticari İstihbarat ve Aile Hukuku Çözümleri", "Kayseri'nin güçlü ticaret ekosisteminde gizlenen şirket varlıkları, muvazaalı devirler ve aile mahkemelerine sunulacak meşru deliller HMK m.199 normlarında toplanır.")
        ],
        "faqs": [
            ("Borçlunun fiili adresini bulabilir misiniz?", "Evet. Resmi tebligattan kaçan şahısların fiilen yaşadığı ve çalıştığı adresler sahada fotoğrafla teyit edilir.")
        ]
    },
    {
        "slug": "aydin-ozel-dedektif",
        "title": "Aydın Dedektif & Özel Dedektiflik Bürosu (Kuşadası, Didim) | DAT",
        "description": "Aydın özel dedektiflik hizmetleri. Kuşadası, Didim, Efeler, Nazilli, Söke ve tüm ilçelerde tatil eş takibi, boşanma delili ve sadakat araştırması.",
        "keywords": "aydın dedektif, kuşadası özel dedektif, didim dedektif, efeler dedektif, nazilli dedektif, söke dedektif, kuşadası eş takibi, aydın dedektiflik bürosu",
        "badge": "EGE TURİZM & KIYI BÖLGESİ • KUŞADASI • DİDİM • 17 İLÇE",
        "h1": "Aydın Dedektif: Kuşadası, Didim, Efeler ve 17 İlçede Özel Dedektiflik",
        "lead": "Kuşadası, Didim, Efeler, Nazilli ve Söke başta olmak üzere Aydın'ın 17 ilçesinde; tatil beldelerinde eş takibi, aldatma delili toplama, yabancı evlilik araştırmaları ve TSCM böcek arama hizmetleri veriyoruz.",
        "image": "assets/services/es-takibi.jpg",
        "districts_title": "Aydın Genelinde Hizmet Verdiğimiz İlçeler (17 İlçe)",
        "districts_intro": "Kuşadası ve Didim marinalarından Efeler merkezine kadar Aydın genelinde 7/24 sahadayız:",
        "districts": [
            "Efeler", "Kuşadası", "Didim", "Nazilli", "Söke", "İncirliova", "Germencik",
            "Çine", "Bozdoğan", "Köşk", "Kuyucak", "Sultanhisar", "Karacasu", "Yenipazar", "Buharkent", "Karpuzlu", "Koçarlı"
        ],
        "sections": [
            ("Kuşadası ve Didim'de Yaz Dönemi Saha Operasyonları", "Yaz aylarında yoğunlaşan şüpheli seyahat ve otel konaklamalarında kamuya açık alanlarda yapılan 4K teleobjektifli tespitler Kuşadası ve Söke Adliyelerinde tek celsede kabul görmektedir.")
        ],
        "faqs": [
            ("Kuşadası'ndaki otel takibi ne kadar sürer?", "Genellikle 24 ila 72 saatlik yoğun saha takibiyle somut ve yasal neticeye ulaşılmaktadır.")
        ]
    },
    {
        "slug": "balikesir-ozel-dedektif",
        "title": "Balıkesir Dedektif & Özel Dedektiflik Bürosu (Edremit, Ayvalık, Bandırma) | DAT",
        "description": "Balıkesir özel dedektif bürosu. Edremit, Ayvalık, Bandırma, Burhaniye ve 20 ilçede eş takibi, tatil araştırması, miras ve boşanma delili tespiti.",
        "keywords": "balıkesir dedektif, edremit özel dedektif, ayvalık dedektif, bandırma dedektif, burhaniye dedektif, akçay dedektif, balıkesir eş takibi, balıkesir dedektiflik",
        "badge": "MARMARA & EGE KÖRFEZ HATTI • EDREMİT • AYVALIK • BANDIRMA • 20 İLÇE",
        "h1": "Balıkesir Dedektif: Edremit, Ayvalık, Bandırma ve 20 İlçede Özel Dedektiflik",
        "lead": "Edremit Körfezi (Akçay, Altınoluk), Ayvalık (Cunda), Bandırma, Burhaniye ve Karesi başta olmak üzere Balıkesir'in 20 ilçesinde; yazlık eş takibi, sadakat analizi, miras kalan mülklerin tespiti ve yasal delil toplama.",
        "image": "assets/services/es-takibi.jpg",
        "districts_title": "Balıkesir Genelinde Hizmet Verdiğimiz İlçeler (20 İlçe)",
        "districts_intro": "Körfez kıyılarından Marmara ve iç ilçelere kadar Balıkesir genelinde sahadayız:",
        "districts": [
            "Altıeylül", "Karesi", "Edremit", "Bandırma", "Ayvalık", "Burhaniye", "Gönen",
            "Bigadiç", "Susurluk", "Dursunbey", "Sındırgı", "İvrindi", "Erdek", "Havran", "Kepsut", "Manyas", "Savaştepe", "Balya", "Gömeç", "Marmara"
        ],
        "sections": [
            ("Körfez Hattında Profesyonel Takip ve Gözlem", "Edremit, Akçay, Altınoluk ve Ayvalık hattındaki yazlık siteler ve otellerde gerçekleştirilen gözlemlerle fevri kuruntular yerine somut adli gerçekler ortaya konur.")
        ],
        "faqs": [
            ("Ayvalık ve Cunda'da takip ekibiniz var mı?", "Evet. Körfez bölgesinde konuşlu mobil araç ve motosikletli ekiplerimiz anında intikal sağlamaktadır.")
        ]
    },
    {
        "slug": "tekirdag-ozel-dedektif",
        "title": "Tekirdağ Dedektif & Özel Dedektiflik Bürosu (Çorlu, Çerkezköy) | DAT",
        "description": "Tekirdağ özel dedektif bürosu. Çorlu, Süleymanpaşa, Çerkezköy, Kapaklı ve 11 ilçede eş takibi, fabrika suistimal tespiti, boşanma delili ve adres araştırması.",
        "keywords": "tekirdağ dedektif, çorlu özel dedektif, çerkezköy dedektif, süleymanpaşa dedektif, kapaklı dedektif, çorlu dedektiflik bürosu, tekirdağ eş takibi",
        "badge": "TRAKYA SANAYİ & METROPOL • ÇORLU • ÇERKEZKÖY • 11 İLÇE",
        "h1": "Tekirdağ Dedektif: Çorlu, Çerkezköy, Süleymanpaşa ve 11 İlçede Özel Dedektiflik",
        "lead": "Çorlu, Çerkezköy OSB, Süleymanpaşa ve Kapaklı başta olmak üzere Trakya'nın sanayi merkezi Tekirdağ'ın 11 ilçesinde; eş takibi, boşanma delili, Avrupa transit araştırmaları ve ticari istihbarat desteği sağlıyoruz.",
        "image": "assets/services/kurumsal-ve-marka-koruma.jpg",
        "districts_title": "Tekirdağ Genelinde Hizmet Verdiğimiz İlçeler (11 İlçe)",
        "districts_intro": "Trakya'nın kalbi Tekirdağ'ın sanayi ve merkez ilçelerinde kesintisiz sahadayız:",
        "districts": [
            "Süleymanpaşa", "Çorlu", "Çerkezköy", "Kapaklı", "Ergene", "Malkara",
            "Saray", "Hayrabolu", "Muratlı", "Şarköy", "Marmaraereğlisi"
        ],
        "sections": [
            ("Trakya ve Avrupa Kapısında Özel Araştırma", "İstanbul'a yakınlığı ve organize sanayi yoğunluğu sebebiyle Çorlu ve Çerkezköy'de hem kurumsal suistimal araştırmaları hem de sınır ötesi seyahat takipleri yürütülmektedir.")
        ],
        "faqs": [
            ("Çorlu'da aynı gün araştırma başlatılabilir mi?", "Evet. Çorlu ve Çerkezköy bölgesine İstanbul Kartal merkezimizden ve Trakya mobil birimimizden saatler içinde intikal sağlanır.")
        ]
    },
    {
        "slug": "samsun-ozel-dedektif",
        "title": "Samsun Dedektif & Özel Dedektiflik Bürosu (İlkadım, Atakum) | DAT",
        "description": "Samsun özel dedektiflik bürosu. İlkadım, Atakum, Canik, Bafra, Çarşamba ve 17 ilçede eş takibi, sadakat analizi, boşanma delili ve borçlu araştırması.",
        "keywords": "samsun dedektif, samsun özel dedektif, ilkadım dedektif, atakum dedektif, bafra dedektif, çarşamba dedektif, orta karadeniz dedektiflik, samsun eş takibi",
        "badge": "ORTA KARADENİZ METROPOL • İLKADIM • ATAKUM • BAFRA • 17 İLÇE",
        "h1": "Samsun Dedektif: İlkadım, Atakum, Bafra ve 17 İlçede Özel Dedektiflik",
        "lead": "İlkadım, Atakum sahili, Canik, Bafra ve Çarşamba başta olmak üzere Samsun'un 17 ilçesinde; eş takibi, sadakat doğrulaması, velayet araştırması ve ticari borçlu tespiti konularında resmi sözleşmeli dedektiflik hizmeti.",
        "image": "assets/services/es-takibi.jpg",
        "districts_title": "Samsun Genelinde Hizmet Verdiğimiz İlçeler (17 İlçe)",
        "districts_intro": "Karadeniz'in en büyük kenti Samsun'un tüm sahil ve ova ilçelerinde görev yapıyoruz:",
        "districts": [
            "İlkadım", "Atakum", "Canik", "Tekkeköy", "Bafra", "Çarşamba", "Terme",
            "Vezirköprü", "Havza", "Alaçam", "19 Mayıs", "Ayvacık", "Kavak", "Salıpazarı", "Asarcık", "Ladik", "Yakakent"
        ],
        "sections": [
            ("Orta Karadeniz'de Hukuki ve Şeffaf Dedektiflik", "Samsun Adliyesi Aile Mahkemelerinde geçerli HMK m.199 standartlarında fotoğraf ve video tutanaklarıyla çekişmeli boşanma süreçlerinize güçlü delil sağlıyoruz.")
        ],
        "faqs": [
            ("Samsun'da eş takibi gizli kalır mı?", "Kesinlikle evet. Hedef şahsın ve üçüncü kişilerin takipten haberdar olması imkansızdır; tüm çalışma sivil kamuflajla yürütülür.")
        ]
    },
    {
        "slug": "diyarbakir-ozel-dedektif",
        "title": "Diyarbakır Dedektif & Özel Dedektiflik Bürosu (Kayapınar, Bağlar) | DAT",
        "description": "Diyarbakır özel dedektif bürosu. Kayapınar, Bağlar, Yenişehir, Sur, Ergani ve 17 ilçede eş takibi, aile araştırması, boşanma delili ve borçlu tespiti.",
        "keywords": "diyarbakır dedektif, diyarbakır özel dedektif, kayapınar dedektif, bağlar dedektif, yenişehir dedektif, ergani dedektif, diyarbakır dedektiflik bürosu",
        "badge": "GÜNEYDOĞU ANADOLU METROPOL • KAYAPINAR • BAĞLAR • 17 İLÇE",
        "h1": "Diyarbakır Dedektif: Kayapınar, Bağlar, Yenişehir ve 17 İlçede Özel Dedektiflik",
        "lead": "Kayapınar (Diclekent, 75 Metrelik Yol), Bağlar, Yenişehir, Sur ve Ergani başta olmak üzere Diyarbakır'ın 17 ilçesinde; aile hukuku delilleri, eş takibi, güvenilirlik ve borçlu adres araştırmalarında 7/24 resmi sözleşmeli hizmet.",
        "image": "assets/services/es-takibi.jpg",
        "districts_title": "Diyarbakır Genelinde Hizmet Verdiğimiz İlçeler (17 İlçe)",
        "districts_intro": "Tarihi ve modern metropol Diyarbakır'ın tüm ilçelerinde yüksek gizlilik disipliniyle görev yapıyoruz:",
        "districts": [
            "Kayapınar", "Bağlar", "Yenişehir", "Sur", "Ergani", "Bismil", "Silvan",
            "Çınar", "Çermik", "Dicle", "Kulp", "Hani", "Maden", "Lice", "Eğil", "Hazro", "Kocaköy", "Çüngüş"
        ],
        "sections": [
            ("Diyarbakır'da Mutlak Gizlilik ve Hukuki Güvence", "Bölgenin hassas sosyal dinamikleri gözetilerek, hiçbir üçüncü şahsın haberdar olamayacağı kapalı devre operasyon protokolü uygulanır.")
        ],
        "faqs": [
            ("Diyarbakır'da çalışma yaptırmak güvenli midir?", "Evet. DAT Özel Dedektiflik tüm işlemlerini yazılı gizlilik sözleşmesiyle yürütür ve kişisel verileriniz asla üçüncü taraflarla paylaşılmaz.")
        ]
    }
]

# 81 İl Listesi (7 Coğrafi Bölgeye Göre)
TURKEY_REGIONS = [
    {
        "region_name": "Marmara Bölgesi",
        "region_id": "marmara",
        "cities": [
            {"name": "İstanbul", "slug": "istanbul-ozel-dedektif", "badge": "Merkez Büro", "districts": "Kadıköy, Beşiktaş, Şişli, Bakırköy, Ataşehir, Üsküdar, 39 İlçe"},
            {"name": "Kocaeli", "slug": "kocaeli-ozel-dedektif", "badge": "Sanayi & OSB", "districts": "Gebze, İzmit, Darıca, Körfez, Gölcük, 12 İlçe"},
            {"name": "Bursa", "slug": "bursa-ozel-dedektif", "badge": "Bölge Merkezi", "districts": "Nilüfer, Osmangazi, Yıldırım, İnegöl, Mudanya, 17 İlçe"},
            {"name": "Balıkesir", "slug": "balikesir-ozel-dedektif", "badge": "Körfez Hattı", "districts": "Edremit, Ayvalık, Bandırma, Burhaniye, Akçay, 20 İlçe"},
            {"name": "Tekirdağ", "slug": "tekirdag-ozel-dedektif", "badge": "Trakya Sanayi", "districts": "Çorlu, Çerkezköy, Süleymanpaşa, Kapaklı, 11 İlçe"},
            {"name": "Çanakkale", "slug": None, "badge": "7/24 Mobil Ağ", "districts": "Merkez, Biga, Çan, Gelibolu, Ayvacık, Bozcaada"},
            {"name": "Sakarya", "slug": None, "badge": "7/24 Mobil Ağ", "districts": "Adapazarı, Serdivan, Hendek, Akyazı, Sapanca"},
            {"name": "Edirne", "slug": None, "badge": "7/24 Mobil Ağ", "districts": "Merkez, Keşan, Uzunköprü, İpsala, Havsa"},
            {"name": "Kırklareli", "slug": None, "badge": "7/24 Mobil Ağ", "districts": "Lüleburgaz, Merkez, Babaeski, Vize"},
            {"name": "Yalova", "slug": None, "badge": "7/24 Mobil Ağ", "districts": "Merkez, Çiftlikköy, Çınarcık, Altınova"},
            {"name": "Bilecik", "slug": None, "badge": "7/24 Mobil Ağ", "districts": "Bozüyük, Merkez, Osmaneli, Söğüt"}
        ]
    },
    {
        "region_name": "Ege Bölgesi",
        "region_id": "ege",
        "cities": [
            {"name": "İzmir", "slug": "izmir-ozel-dedektif", "badge": "Bölge Merkezi", "districts": "Konak, Karşıyaka, Bornova, Alsancak, Çeşme, Urla, 30 İlçe"},
            {"name": "Muğla", "slug": "mugla-ozel-dedektif", "badge": "Turizm & Tatil", "districts": "Bodrum, Marmaris, Fethiye, Datça, Milas, Göcek, 13 İlçe"},
            {"name": "Aydın", "slug": "aydin-ozel-dedektif", "badge": "Turizm & Kıyı", "districts": "Kuşadası, Didim, Efeler, Nazilli, Söke, 17 İlçe"},
            {"name": "Denizli", "slug": None, "badge": "7/24 Mobil Ağ", "districts": "Pamukkale, Merkezefendi, Çivril, Acıpayam"},
            {"name": "Manisa", "slug": None, "badge": "7/24 Mobil Ağ", "districts": "Yunusemre, Şehzadeler, Akhisar, Turgutlu, Salihli"},
            {"name": "Afyonkarahisar", "slug": None, "badge": "7/24 Mobil Ağ", "districts": "Merkez, Sandıklı, Dinar, Bolvadin"},
            {"name": "Kütahya", "slug": None, "badge": "7/24 Mobil Ağ", "districts": "Merkez, Tavşanlı, Simav, Gediz"},
            {"name": "Uşak", "slug": None, "badge": "7/24 Mobil Ağ", "districts": "Merkez, Banaz, Eşme, Sivaslı"}
        ]
    },
    {
        "region_name": "İç Anadolu Bölgesi",
        "region_id": "ic-anadolu",
        "cities": [
            {"name": "Ankara", "slug": "ankara-ozel-dedektif", "badge": "Genel Merkez", "districts": "Çankaya, Yenimahalle, Keçiören, Gölbaşı, Etimesgut, 25 İlçe"},
            {"name": "Konya", "slug": "konya-ozel-dedektif", "badge": "Bölge Merkezi", "districts": "Selçuklu, Meram, Karatay, Ereğli, Akşehir, 31 İlçe"},
            {"name": "Eskişehir", "slug": "eskisehir-ozel-dedektif", "badge": "Üniversite & Kent", "districts": "Odunpazarı, Tepebaşı, Sivrihisar, Çifteler, 14 İlçe"},
            {"name": "Kayseri", "slug": "kayseri-ozel-dedektif", "badge": "Sanayi & Ticaret", "districts": "Melikgazi, Kocasinan, Talas, Develi, 16 İlçe"},
            {"name": "Sivas", "slug": None, "badge": "7/24 Mobil Ağ", "districts": "Merkez, Şarkışla, Yıldızeli, Suşehri"},
            {"name": "Kırıkkale", "slug": None, "badge": "7/24 Mobil Ağ", "districts": "Merkez, Yahşihan, Keskin, Bahşılı"},
            {"name": "Aksaray", "slug": None, "badge": "7/24 Mobil Ağ", "districts": "Merkez, Ortaköy, Eskil, Gülağaç"},
            {"name": "Karaman", "slug": None, "badge": "7/24 Mobil Ağ", "districts": "Merkez, Ermenek, Sarıveliler"},
            {"name": "Kırşehir", "slug": None, "badge": "7/24 Mobil Ağ", "districts": "Merkez, Kaman, Mucur, Çiçekdağı"},
            {"name": "Nevşehir", "slug": None, "badge": "Kapadokya Hattı", "districts": "Merkez, Ürgüp, Avanos, Göreme"},
            {"name": "Niğde", "slug": None, "badge": "7/24 Mobil Ağ", "districts": "Merkez, Bor, Çamardı, Ulukışla"},
            {"name": "Yozgat", "slug": None, "badge": "7/24 Mobil Ağ", "districts": "Merkez, Sorgun, Akdağmadeni, Yerköy"},
            {"name": "Çankırı", "slug": None, "badge": "7/24 Mobil Ağ", "districts": "Merkez, Çerkeş, Ilgaz, Orta"}
        ]
    },
    {
        "region_name": "Akdeniz Bölgesi",
        "region_id": "akdeniz",
        "cities": [
            {"name": "Antalya", "slug": "antalya-ozel-dedektif", "badge": "Turizm Merkezi", "districts": "Muratpaşa, Alanya, Konyaaltı, Manavgat, Kepez, Kemer, Kaş, 19 İlçe"},
            {"name": "Adana", "slug": "adana-ozel-dedektif", "badge": "Bölge Merkezi", "districts": "Seyhan, Çukurova, Yüreğir, Sarıçam, Ceyhan, Kozan, 15 İlçe"},
            {"name": "Mersin", "slug": "mersin-ozel-dedektif", "badge": "Liman & Ticaret", "districts": "Yenişehir, Mezitli, Toroslar, Tarsus, Akdeniz, Erdemli, 13 İlçe"},
            {"name": "Hatay", "slug": None, "badge": "7/24 Mobil Ağ", "districts": "Antakya, İskenderun, Defne, Samandağ, Dörtyol"},
            {"name": "Kahramanmaraş", "slug": None, "badge": "7/24 Mobil Ağ", "districts": "Onikişubat, Dulkadiroğlu, Elbistan, Afşin"},
            {"name": "Osmaniye", "slug": None, "badge": "7/24 Mobil Ağ", "districts": "Merkez, Kadirli, Düziçi, Bahçe"},
            {"name": "Isparta", "slug": None, "badge": "7/24 Mobil Ağ", "districts": "Merkez, Yalvaç, Eğirdir, Şarkikaraağaç"},
            {"name": "Burdur", "slug": None, "badge": "7/24 Mobil Ağ", "districts": "Merkez, Bucak, Gölhisar, Yeşilova"}
        ]
    },
    {
        "region_name": "Karadeniz Bölgesi",
        "region_id": "karadeniz",
        "cities": [
            {"name": "Trabzon", "slug": "trabzon-ozel-dedektif", "badge": "Bölge Merkezi", "districts": "Ortahisar, Akçaabat, Yomra, Of, Araklı, Sürmene, 18 İlçe"},
            {"name": "Samsun", "slug": "samsun-ozel-dedektif", "badge": "Bölge Merkezi", "districts": "İlkadım, Atakum, Canik, Bafra, Çarşamba, 17 İlçe"},
            {"name": "Ordu", "slug": None, "badge": "7/24 Mobil Ağ", "districts": "Altınordu, Ünye, Fatsa, Gölköy"},
            {"name": "Giresun", "slug": None, "badge": "7/24 Mobil Ağ", "districts": "Merkez, Bulancak, Espiye, Tirebolu"},
            {"name": "Rize", "slug": None, "badge": "7/24 Mobil Ağ", "districts": "Merkez, Çayeli, Ardeşen, Pazar"},
            {"name": "Zonguldak", "slug": None, "badge": "7/24 Mobil Ağ", "districts": "Merkez, Karadeniz Ereğli, Çaycuma, Devrek"},
            {"name": "Bolu", "slug": None, "badge": "7/24 Mobil Ağ", "districts": "Merkez, Gerede, Mudurnu, Mengen"},
            {"name": "Düzce", "slug": None, "badge": "7/24 Mobil Ağ", "districts": "Merkez, Akçakoca, Kaynaşlı, Gölyaka"},
            {"name": "Kastamonu", "slug": None, "badge": "7/24 Mobil Ağ", "districts": "Merkez, Tosya, Taşköprü, Cide"},
            {"name": "Tokat", "slug": None, "badge": "7/24 Mobil Ağ", "districts": "Merkez, Erbaa, Turhal, Niksar"},
            {"name": "Çorum", "slug": None, "badge": "7/24 Mobil Ağ", "districts": "Merkez, Sungurlu, Osmancık, İskilip"},
            {"name": "Sinop", "slug": None, "badge": "7/24 Mobil Ağ", "districts": "Merkez, Boyabat, Gerze, Ayancık"},
            {"name": "Amasya", "slug": None, "badge": "7/24 Mobil Ağ", "districts": "Merkez, Merzifon, Suluova, Taşova"},
            {"name": "Bartın", "slug": None, "badge": "7/24 Mobil Ağ", "districts": "Merkez, Amasra, Ulus, Kurucaşile"},
            {"name": "Karabük", "slug": None, "badge": "7/24 Mobil Ağ", "districts": "Merkez, Safranbolu, Yenice, Eskipazar"},
            {"name": "Artvin", "slug": None, "badge": "7/24 Mobil Ağ", "districts": "Merkez, Hopa, Borçka, Arhavi"},
            {"name": "Gümüşhane", "slug": None, "badge": "7/24 Mobil Ağ", "districts": "Merkez, Kelkit, Şiran, Köse"},
            {"name": "Bayburt", "slug": None, "badge": "7/24 Mobil Ağ", "districts": "Merkez, Demirözü, Aydıntepe"}
        ]
    },
    {
        "region_name": "Güneydoğu Anadolu Bölgesi",
        "region_id": "guneydogu",
        "cities": [
            {"name": "Gaziantep", "slug": "gaziantep-ozel-dedektif", "badge": "Bölge Merkezi", "districts": "Şahinbey, Şehitkamil, Nizip, İslahiye, 9 İlçe"},
            {"name": "Diyarbakır", "slug": "diyarbakir-ozel-dedektif", "badge": "Bölge Merkezi", "districts": "Kayapınar, Bağlar, Yenişehir, Sur, Ergani, 17 İlçe"},
            {"name": "Şanlıurfa", "slug": None, "badge": "7/24 Mobil Ağ", "districts": "Haliliye, Eyyübiye, Karaköprü, Siverek, Viranşehir"},
            {"name": "Mardin", "slug": None, "badge": "7/24 Mobil Ağ", "districts": "Artuklu, Kızıltepe, Midyat, Nusaybin"},
            {"name": "Batman", "slug": None, "badge": "7/24 Mobil Ağ", "districts": "Merkez, Kozluk, Sason, Beşiri"},
            {"name": "Adıyaman", "slug": None, "badge": "7/24 Mobil Ağ", "districts": "Merkez, Kahta, Besni, Gölbaşı"},
            {"name": "Siirt", "slug": None, "badge": "7/24 Mobil Ağ", "districts": "Merkez, Kurtalan, Pervari, Baykan"},
            {"name": "Kilis", "slug": None, "badge": "7/24 Mobil Ağ", "districts": "Merkez, Musabeyli, Elbeyli, Polateli"},
            {"name": "Şırnak", "slug": None, "badge": "7/24 Mobil Ağ", "districts": "Cizre, Silopi, Merkez, İdil"}
        ]
    },
    {
        "region_name": "Doğu Anadolu Bölgesi",
        "region_id": "dogu-anadolu",
        "cities": [
            {"name": "Malatya", "slug": None, "badge": "Bölge Ağı", "districts": "Battalgazi, Yeşilyurt, Doğanşehir, Akçadağ"},
            {"name": "Erzurum", "slug": None, "badge": "Bölge Ağı", "districts": "Yakutiye, Palandöken, Aziziye, Oltu, Horasan"},
            {"name": "Van", "slug": None, "badge": "Bölge Ağı", "districts": "İpekyolu, Tuşba, Edremit, Erciş, Başkale"},
            {"name": "Elazığ", "slug": None, "badge": "Bölge Ağı", "districts": "Merkez, Kovancılar, Karakoçan, Palu"},
            {"name": "Ağrı", "slug": None, "badge": "7/24 Mobil Ağ", "districts": "Merkez, Doğubayazıt, Patnos, Diyadin"},
            {"name": "Kars", "slug": None, "badge": "7/24 Mobil Ağ", "districts": "Merkez, Kağızman, Sarıkamış, Selim"},
            {"name": "Muş", "slug": None, "badge": "7/24 Mobil Ağ", "districts": "Merkez, Bulanık, Malazgirt, Varto"},
            {"name": "Bitlis", "slug": None, "badge": "7/24 Mobil Ağ", "districts": "Tatvan, Merkez, Ahlat, Güroymak"},
            {"name": "Erzincan", "slug": None, "badge": "7/24 Mobil Ağ", "districts": "Merkez, Tercan, Üzümlü, Refahiye"},
            {"name": "Bingöl", "slug": None, "badge": "7/24 Mobil Ağ", "districts": "Merkez, Genç, Solhan, Karlıova"},
            {"name": "Iğdır", "slug": None, "badge": "7/24 Mobil Ağ", "districts": "Merkez, Tuzluca, Aralık, Karakoyunlu"},
            {"name": "Hakkari", "slug": None, "badge": "7/24 Mobil Ağ", "districts": "Yüksekova, Merkez, Şemdinli, Çukurca"},
            {"name": "Ardahan", "slug": None, "badge": "7/24 Mobil Ağ", "districts": "Merkez, Göle, Çıldır, Hanak"},
            {"name": "Tunceli", "slug": None, "badge": "7/24 Mobil Ağ", "districts": "Merkez, Pertek, Mazgirt, Çemişgezek"}
        ]
    }
]

ALL_81_CITY_NAMES = sorted([city["name"] for reg in TURKEY_REGIONS for city in reg["cities"]])

def generate_city_landing_html(c):
    """ankara-ozel-dedektif.html şablonuyla birebir uyumlu modern Apple Obsidian landing page üretir."""
    districts_schema = json.dumps([{"@type": "AdministrativeArea", "name": d} for d in c["districts"]], ensure_ascii=False)
    faq_schema = json.dumps([{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in c["faqs"]], ensure_ascii=False)
    
    districts_chips = "\n".join([
        f'<span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-mono bg-white/5 border border-white/10 text-white/90 hover:border-[#93F051]/50 transition cursor-default">📍 {d}</span>'
        for d in c["districts"]
    ])
    
    sections_html = ""
    for h, p in c["sections"]:
        sections_html += f"""
        <div class="space-y-3 pt-6 border-t border-white/10">
            <h3 class="text-xl sm:text-2xl font-medium text-white tracking-tight">{h}</h3>
            <p class="text-sm sm:text-base text-white/75 leading-relaxed font-regular">{p}</p>
        </div>"""

    faq_html = ""
    for q, a in c["faqs"]:
        faq_html += f"""
        <details class="group bg-[#18181A] border border-white/10 rounded-2xl p-4 sm:p-5 transition">
            <summary class="font-medium text-sm sm:text-base text-white flex items-center justify-between cursor-pointer list-none">
                <span>{q}</span>
                <i class="hgi hgi-stroke hgi-arrow-down-01 w-4 h-4 text-[#93F051] group-open:rotate-180 transition-transform"></i>
            </summary>
            <p class="mt-3 text-xs sm:text-sm text-white/75 leading-relaxed pt-2 border-t border-white/10">{a}</p>
        </details>"""

    wa_text = f"Merhaba Ümit Bey, {c['h1'].split(':')[0]} sayfanızdan yazıyorum. Bölgemizde hukuki delil toplama ve özel dedektiflik hizmeti almak istiyorum."
    wa_encoded = wa_text.replace(" ", "%20")

    html = f"""<!DOCTYPE html>
<html lang="tr" class="scroll-smooth dark" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
    <script id="datThemeBoot">
        (function () {{
            try {{
                var saved = localStorage.getItem('dat_theme');
                var theme = (saved === 'light' || saved === 'dark') ? saved : 'dark';
                var root = document.documentElement;
                root.setAttribute('data-theme', theme);
                root.style.colorScheme = theme;
                if (theme === 'dark') root.classList.add('dark'); else root.classList.remove('dark');
                var meta = document.getElementById('themeColorMeta');
                if (meta) meta.setAttribute('content', theme === 'light' ? '#FFFFFF' : '#111111');
            }} catch (e) {{}}
        }})();
    </script>
    <title>{c['title']}</title>
    <meta name="description" content="{c['description']}">
    <meta name="keywords" content="{c['keywords']}">
    <meta name="robots" content="index, follow, max-image-preview:large">
    <meta id="themeColorMeta" name="theme-color" content="#111111">
    <link rel="canonical" href="https://www.datdetective.com/{c['slug']}">
    <link rel="icon" type="image/png" href="dat-logo.png">
    <link rel="shortcut icon" href="favicon.ico">
    <link rel="preconnect" href="https://cdn.tailwindcss.com" crossorigin>
    <link rel="preconnect" href="https://use.hugeicons.com" crossorigin>
    <meta property="og:type" content="article">
    <meta property="og:locale" content="tr_TR">
    <meta property="og:url" content="https://www.datdetective.com/{c['slug']}">
    <meta property="og:site_name" content="DAT Özel Dedektiflik Bürosu">
    <meta property="og:title" content="{c['title']}">
    <meta property="og:description" content="{c['description']}">
    <meta property="og:image" content="https://www.datdetective.com/assets/og-banner.jpg">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:image" content="https://www.datdetective.com/assets/og-banner.jpg">
    <script type="application/ld+json">[
      {{
        "@context": "https://schema.org",
        "@type": "LegalService",
        "name": "{c['h1']} — DAT Özel Dedektiflik",
        "url": "https://www.datdetective.com/{c['slug']}",
        "image": "https://www.datdetective.com/assets/og-banner.jpg",
        "telephone": "+90-532-666-77-49",
        "email": "info@datdetective.com",
        "founder": {{"@type": "Person", "name": "Ümit Hakan Karakaya"}},
        "foundingDate": "2005",
        "areaServed": {districts_schema}
      }},
      {{
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
          {{"@type": "ListItem", "position": 1, "name": "Ana Sayfa", "item": "https://www.datdetective.com/"}},
          {{"@type": "ListItem", "position": 2, "name": "{c['h1']}", "item": "https://www.datdetective.com/{c['slug']}"}}
        ]
      }},
      {{
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": {faq_schema}
      }}
    ]</script>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://use.hugeicons.com/font/icons.css">
    <style>
        *:not(.hgi):not([class*="hgi-"]) {{ font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important; }}
        .hgi {{ display: inline-flex; align-items: center; justify-content: center; line-height: 1; vertical-align: middle; }}
        html[data-theme="dark"], html[data-theme="dark"] body {{ background-color: #111111 !important; color: #F5F5F7 !important; }}
    </style>
</head>
<body class="bg-[#111111] text-[#FFFFFF] antialiased selection:bg-[#93F051] selection:text-[#111111]">

    <!-- Header Navigation -->
    <header class="sticky top-0 z-50 bg-[#111111]/90 backdrop-blur-md border-b border-white/10 px-4 sm:px-8 py-3.5 flex items-center justify-between">
        <a href="./" class="flex items-center gap-3 group">
            <img src="dat-logo.png" alt="DAT Özel Dedektiflik" class="w-8 h-8 rounded-full border border-[#93F051]/40 object-cover">
            <div>
                <div class="text-sm font-semibold tracking-tight text-white group-hover:text-[#93F051] transition">DAT DEDEKTİFLİK</div>
                <div class="text-[10px] text-white/50 font-mono">2005'TEN BUGÜNE SEKTÖR LİDERİ</div>
            </div>
        </a>
        <div class="flex items-center gap-3">
            <a href="tel:03122840299" class="hidden sm:inline-flex items-center gap-1.5 text-xs font-mono text-white/80 hover:text-white transition">
                <i class="hgi hgi-stroke hgi-call w-3.5 h-3.5 text-[#93F051]"></i>
                <span>0312 284 02 99</span>
            </a>
            <a href="https://wa.me/905326667749?text={wa_encoded}" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-full bg-[#93F051] hover:bg-[#82dc43] text-[#111111] font-semibold text-xs transition">
                <i class="hgi hgi-stroke hgi-whatsapp w-4 h-4 text-[#111111]"></i>
                <span>WhatsApp 7/24</span>
            </a>
        </div>
    </header>

    <!-- Main Content Container -->
    <main class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-10 sm:py-16 space-y-12">

        <!-- Breadcrumb -->
        <nav class="flex items-center gap-2 text-xs font-mono text-white/50">
            <a href="./" class="hover:text-[#93F051] transition">Ana Sayfa</a>
            <span>/</span>
            <span class="text-white/80">{c['h1'].split(':')[0]}</span>
        </nav>

        <!-- Hero Section -->
        <div class="space-y-4">
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/5 border border-[#93F051]/40 text-xs font-medium text-[#93F051]">
                <span class="w-2 h-2 rounded-full bg-[#93F051] animate-pulse"></span>
                <span>{c['badge']}</span>
            </div>
            <h1 class="text-3xl sm:text-4xl lg:text-5xl font-medium text-white tracking-tight leading-tight">
                {c['h1']}
            </h1>
            <p class="text-base sm:text-lg text-white/80 leading-relaxed font-regular max-w-3xl">
                {c['lead']}
            </p>
        </div>

        <!-- Districts Grid -->
        <div class="rounded-2xl bg-[#161618] border border-white/10 p-5 sm:p-7 space-y-4 shadow-xl">
            <div class="space-y-1">
                <h2 class="text-lg sm:text-xl font-medium text-white flex items-center gap-2">
                    <i class="hgi hgi-stroke hgi-location-01 w-5 h-5 text-[#93F051]"></i>
                    <span>{c['districts_title']}</span>
                </h2>
                <p class="text-xs sm:text-sm text-white/70 leading-relaxed">{c['districts_intro']}</p>
            </div>
            <div class="flex flex-wrap gap-2 pt-2">
                {districts_chips}
            </div>
        </div>

        <!-- Detailed Legal & Operational Sections -->
        <div class="space-y-8">
            {sections_html}
        </div>

        <!-- FAQ Section -->
        <div class="space-y-5 pt-8 border-t border-white/10">
            <h2 class="text-2xl font-medium text-white tracking-tight flex items-center gap-2">
                <i class="hgi hgi-stroke hgi-help-circle w-6 h-6 text-[#93F051]"></i>
                <span>Sıkça Sorulan Sorular ({c['h1'].split(':')[0]})</span>
            </h2>
            <div class="space-y-3">
                {faq_html}
            </div>
        </div>

        <!-- Bottom Action CTA Card -->
        <div class="rounded-3xl bg-gradient-to-br from-[#18181A] to-[#121214] border border-[#93F051]/30 p-6 sm:p-10 text-center space-y-6 shadow-2xl">
            <div class="space-y-2 max-w-2xl mx-auto">
                <span class="text-xs font-mono text-[#93F051] uppercase tracking-wider">%100 Gizlilik &amp; Hukuki Güvence</span>
                <h2 class="text-2xl sm:text-3xl font-medium text-white">{c['h1'].split(':')[0]} İçin Doğrudan Ön Görüşme Yapın</h2>
                <p class="text-sm text-white/75 leading-relaxed">Kurucumuz Ümit Hakan Karakaya liderliğindeki uzman adli dedektiflik ekibimizle görüşerek vakanızı şeffaf ve hukuka uygun şekilde değerlendirin.</p>
            </div>
            <div class="flex flex-wrap items-center justify-center gap-4 pt-2">
                <a href="https://wa.me/905326667749?text={wa_encoded}" target="_blank" rel="noopener noreferrer" class="px-6 py-3 rounded-xl bg-[#25D366] hover:bg-[#20ba59] text-[#111111] font-semibold text-sm flex items-center gap-2 transition shadow-lg">
                    <i class="hgi hgi-stroke hgi-whatsapp w-5 h-5"></i>
                    <span>WhatsApp Doğrudan Danışma Hattı</span>
                </a>
                <a href="tel:03122840299" class="px-6 py-3 rounded-xl bg-white/10 hover:bg-white/15 text-white font-medium text-sm flex items-center gap-2 transition border border-white/10">
                    <i class="hgi hgi-stroke hgi-call w-4 h-4 text-[#93F051]"></i>
                    <span>0312 284 02 99</span>
                </a>
            </div>
            <div class="flex items-center justify-center gap-4 text-[11px] font-mono text-white/50 pt-2">
                <span>🛡️ HMK m.199 Uyumlu</span>
                <span>•</span>
                <span>⚖️ TCK m.134 Saygılı</span>
                <span>•</span>
                <span>🔒 256-Bit SSL Şifreli</span>
            </div>
        </div>

    </main>

    <!-- Footer -->
    <footer class="bg-[#141416] border-t border-white/10 py-8 px-4 text-center text-xs text-white/50 space-y-2">
        <p>© 2005 - 2026 DAT Özel Dedektiflik Bürosu. Tüm hakları saklıdır.</p>
        <p>Helis Metro Tower Kartal / İstanbul • Konutkent Çankaya / Ankara • WPYB Global Podgorica / Karadağ • Las Vegas / ABD</p>
    </footer>

    <script src="script.js?v=8.2"></script>
</body>
</html>"""
    return html

def build_81_provinces_section_html():
    """index.html için 7 coğrafi bölge ve 81 ilin tamamını içeren zengin SEO Geo-Hub bölümü üretir."""
    tabs_nav = []
    panels_html = []
    
    for idx, reg in enumerate(TURKEY_REGIONS):
        active_cls = "bg-[#93F051] text-[#111111] font-semibold shadow-sm" if idx == 0 else "bg-white/5 text-white/70 hover:text-white hover:bg-white/10"
        hidden_cls = "" if idx == 0 else "hidden"
        
        tabs_nav.append(f"""
        <button type="button" onclick="switchGeoRegion('{reg['region_id']}')" id="geoTabBtn-{reg['region_id']}" class="geo-tab-btn px-3.5 py-1.5 rounded-full text-xs font-mono transition shrink-0 {active_cls}">
            {reg['region_name']} ({len(reg['cities'])} İl)
        </button>""")
        
        cities_cards = []
        for city in reg["cities"]:
            wa_text = f"Merhaba Ümit Bey, {city['name']} bölgesinde özel dedektiflik hizmeti ve hukuki delil toplama danışmanlığı almak istiyorum."
            wa_encoded = wa_text.replace(" ", "%20")
            
            if city["slug"]:
                link_html = f"""<a href="{city['slug']}.html" title="{city['name']} Özel Dedektiflik Hizmeti ve İlçe Bilgileri" class="inline-flex items-center gap-1 text-xs font-semibold text-[#93F051] hover:underline">
                    <span>{city['name']} Dedektif Sayfası</span>
                    <i class="hgi hgi-stroke hgi-arrow-right-01 w-3 h-3"></i>
                </a>"""
            else:
                link_html = f"""<a href="https://wa.me/905326667749?text={wa_encoded}" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-1 text-xs font-semibold text-[#93F051] hover:underline" title="{city['name']} Özel Dedektif Danışmanlığı">
                    <span>{city['name']} 7/24 Saha Danışma</span>
                    <i class="hgi hgi-stroke hgi-whatsapp w-3 h-3 text-[#25D366]"></i>
                </a>"""

            cities_cards.append(f"""
            <div class="rounded-2xl bg-[#1A1A1D] border border-white/10 hover:border-[#93F051]/40 p-4 space-y-2.5 transition group">
                <div class="flex items-center justify-between">
                    <h4 class="text-sm font-semibold text-white flex items-center gap-1.5">
                        <span class="text-xs">📍</span>
                        <span>{city['name']} Dedektif</span>
                    </h4>
                    <span class="px-2 py-0.5 rounded-full text-[9.5px] font-mono bg-white/5 border border-white/10 text-[#93F051]">{city['badge']}</span>
                </div>
                <div class="text-[11px] text-white/60 line-clamp-2 leading-relaxed">
                    <strong class="text-white/80">Kapsanan İlçeler:</strong> {city['districts']}
                </div>
                <div class="pt-2 border-t border-white/10 flex items-center justify-between">
                    <span class="text-[10px] font-mono text-white/40">HMK m.199 Uyumlu</span>
                    {link_html}
                </div>
            </div>""")

        panels_html.append(f"""
        <div id="geoPanel-{reg['region_id']}" class="geo-region-panel grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3 {hidden_cls}">
            {"".join(cities_cards)}
        </div>""")

    section_html = f"""
        <!-- 81 İL & İLÇE ULUSAL DEDEKTİFLİK HİZMET AĞI (#turkiye-dedektif-agi) -->
        <section id="turkiye-dedektif-agi" class="py-14 sm:py-20 bg-[#141416] text-[#FFFFFF] border-y border-white/10 relative">
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-8">
                
                <div class="text-center max-w-3xl mx-auto space-y-3">
                    <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#1D1D1F] border border-[#93F051]/30 text-xs font-medium text-[#93F051]">
                        <span class="w-2 h-2 rounded-full bg-[#93F051] animate-pulse"></span>
                        <span>TÜRKİYE'NİN 81 İLİ VE TÜM İLÇELERİNDE 7/24 AKTİF MOBİL SAHA AĞI</span>
                    </div>
                    <h2 class="apple-heading text-3xl sm:text-4xl font-medium text-white tracking-tight">
                        81 İl &amp; İlçe Özel Dedektiflik Hizmet Ağı
                    </h2>
                    <p class="text-sm sm:text-base text-white/75 leading-relaxed font-regular">
                        DAT Özel Dedektiflik Bürosu; İstanbul ve Ankara merkez ofisleri koordinasyonunda, <strong>Türkiye'nin 81 ilinin tamamında ve yüzlerce ilçesinde</strong> eş takibi, sadakat analizi, boşanma delili toplama, borçlu adresi tespiti ve TSCM böcek arama operasyonlarını 2005'ten bu yana kesintisiz yönetmektedir.
                    </p>
                </div>

                <!-- Region Filter Tabs -->
                <div class="flex items-center gap-2 overflow-x-auto pb-2 scrollbar-none justify-start lg:justify-center">
                    {"".join(tabs_nav)}
                </div>

                <!-- Panels Container -->
                <div class="min-h-[320px]">
                    {"".join(panels_html)}
                </div>

                <!-- Direct Assistance Banner -->
                <div class="rounded-2xl bg-[#1A1A1D] border border-white/10 p-4 sm:p-5 flex flex-col sm:flex-row items-center justify-between gap-4">
                    <div class="space-y-1 text-center sm:text-left">
                        <div class="text-xs sm:text-sm font-semibold text-white flex items-center justify-center sm:justify-start gap-1.5">
                            <i class="hgi hgi-stroke hgi-shield-security w-4 h-4 text-[#93F051]"></i>
                            <span>İliniz veya İlçeniz İçin Özel Delil Danışmanlığı Alın</span>
                        </div>
                        <p class="text-xs text-white/60">Tüm saha çalışmalarımız TCK m.134 sınırlarına ve HMK m.199 yasal delil standartlarına tam uyumludur.</p>
                    </div>
                    <div class="flex items-center gap-2.5 shrink-0">
                        <a href="tel:03122840299" class="px-4 py-2 rounded-xl bg-white/10 hover:bg-white/15 text-white text-xs font-mono font-medium transition">
                            0312 284 02 99
                        </a>
                        <a href="https://wa.me/905326667749?text=Merhaba%20%C3%9Cmit%20Bey%2C%20T%C3%BCrkiye%2081%20il%20alan%C4%B1ndan%20yaz%C4%B1yorum.%20%C4%B0lim%20i%C3%A7in%20dan%C4%B1%C5%9Fmanl%C4%B1k%20almak%20istiyorum." target="_blank" rel="noopener noreferrer" class="px-4 py-2 rounded-xl bg-[#25D366] hover:bg-[#20ba59] text-[#111111] text-xs font-semibold flex items-center gap-1.5 transition">
                            <i class="hgi hgi-stroke hgi-whatsapp w-4 h-4"></i>
                            <span>7/24 WhatsApp</span>
                        </a>
                    </div>
                </div>

            </div>
        </section>

        <script>
        function switchGeoRegion(regionId) {{
            document.querySelectorAll('.geo-region-panel').forEach(function(p) {{ p.classList.add('hidden'); }});
            document.querySelectorAll('.geo-tab-btn').forEach(function(b) {{
                b.className = 'geo-tab-btn px-3.5 py-1.5 rounded-full text-xs font-mono transition shrink-0 bg-white/5 text-white/70 hover:text-white hover:bg-white/10';
            }});
            var panel = document.getElementById('geoPanel-' + regionId);
            var btn = document.getElementById('geoTabBtn-' + regionId);
            if (panel) panel.classList.remove('hidden');
            if (btn) btn.className = 'geo-tab-btn px-3.5 py-1.5 rounded-full text-xs font-mono transition shrink-0 bg-[#93F051] text-[#111111] font-semibold shadow-sm';
        }}
        </script>
    """
    return section_html

def main():
    print("--- 1. YENİ 12 BÜYÜKŞEHİR & TURİZM LANDING PAGE ÜRETİMİ ---")
    for c in NEW_CITIES:
        html = generate_city_landing_html(c)
        out_file = os.path.join(ROOT, f"{c['slug']}.html")
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Generated: {c['slug']}.html")

    print("\n--- 2. INDEX.HTML'E 81 İL GEODİRECTORY MODÜLÜ ENTEGRASYONU ---")
    with open(os.path.join(ROOT, "index.html"), "r", encoding="utf-8") as f:
        idx_content = f.read()

    geo_section = build_81_provinces_section_html()
    
    if 'id="turkiye-dedektif-agi"' in idx_content:
        # replace existing
        idx_content = re.sub(r'<!-- 81 İL & İLÇE ULUSAL DEDEKTİFLİK HİZMET AĞI.*?<\/script>', geo_section, idx_content, flags=re.DOTALL)
        print("Updated existing #turkiye-dedektif-agi in index.html")
    else:
        # insert right before footer
        target_str = '<footer class="bg-[#111111] border-t border-white/10'
        if target_str in idx_content:
            idx_content = idx_content.replace(target_str, geo_section + "\n    " + target_str)
            print("Inserted #turkiye-dedektif-agi before footer in index.html")
        else:
            print("WARNING: Footer tag not matched directly!")

    # 3. SCHEMA.ORG LEGALSERVICE AREA SERVED ALANINA 81 İLİ EKLE
    area_served_json = json.dumps([{"@type": "AdministrativeArea", "name": c} for c in ALL_81_CITY_NAMES], ensure_ascii=False)
    # Match "areaServed": ["TR", "CY", ... ] in schema
    old_area_served_pattern = r'"areaServed":\s*\[\s*"TR",\s*"CY",\s*"GE",\s*"ME",\s*"US",\s*"EU"\s*\]'
    new_area_served = f'"areaServed": {area_served_json}'
    if re.search(old_area_served_pattern, idx_content):
        idx_content = re.sub(old_area_served_pattern, new_area_served, idx_content)
        print("Updated Schema.org areaServed with all 81 provinces in index.html")

    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
        f.write(idx_content)

    print("\n--- 3. _REDIRECTS VE SITEMAP.XML GÜNCELLEMESİ ---")
    # _redirects
    with open(os.path.join(ROOT, "_redirects"), "r", encoding="utf-8") as f:
        red_content = f.read()

    new_redirects_lines = []
    for c in NEW_CITIES:
        clean_rule = f"/{c['slug']} /{c['slug']}.html 200"
        if clean_rule not in red_content:
            new_redirects_lines.append(clean_rule)
        
        # Legacy uppercase rule
        city_upper = c['slug'].split('-')[0].upper()
        leg_rule = f"/Dedektif/ozel-dedektif-{city_upper}* /{c['slug']} 301"
        if leg_rule not in red_content:
            new_redirects_lines.append(leg_rule)

    if new_redirects_lines:
        red_content = "\n".join(new_redirects_lines) + "\n\n" + red_content
        with open(os.path.join(ROOT, "_redirects"), "w", encoding="utf-8") as f:
            f.write(red_content)
        print(f"Added {len(new_redirects_lines)} routing rules to _redirects")

    # sitemap.xml
    with open(os.path.join(ROOT, "sitemap.xml"), "r", encoding="utf-8") as f:
        sitemap_content = f.read()

    new_sitemap_urls = []
    for c in NEW_CITIES:
        url_loc = f"https://www.datdetective.com/{c['slug']}"
        if url_loc not in sitemap_content:
            entry = f"""  <url>
    <loc>{url_loc}</loc>
    <lastmod>2026-11-15</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.85</priority>
  </url>"""
            new_sitemap_urls.append(entry)

    if new_sitemap_urls:
        insert_marker = "</urlset>"
        if insert_marker in sitemap_content:
            sitemap_content = sitemap_content.replace(insert_marker, "\n".join(new_sitemap_urls) + "\n" + insert_marker)
            with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
                f.write(sitemap_content)
            print(f"Added {len(new_sitemap_urls)} new city landing pages to sitemap.xml")

    print("\n--- 4. LLMS.TXT GÜNCELLEMESİ ---")
    with open(os.path.join(ROOT, "llms.txt"), "r", encoding="utf-8") as f:
        llms_content = f.read()

    geo_llms_entry = "\n## Türkiye 81 İl ve İlçe Özel Dedektiflik Hizmet Ağı (Nationwide Coverage)\n"
    geo_llms_entry += "DAT Özel Dedektiflik, Türkiye'nin 81 ilinin tamamında ve tüm ilçelerinde (Bodrum, Marmaris, Fethiye, Gebze, Çorlu, Alanya, Çankaya vb.) HMK m.199 yasal delil standartlarında hizmet vermektedir:\n"
    for reg in TURKEY_REGIONS:
        city_list = ", ".join([c["name"] for c in reg["cities"]])
        geo_llms_entry += f"- {reg['region_name']}: {city_list}\n"

    if "## Türkiye 81 İl ve İlçe" not in llms_content:
        llms_content += "\n" + geo_llms_entry
        with open(os.path.join(ROOT, "llms.txt"), "w", encoding="utf-8") as f:
            f.write(llms_content)
        print("Updated llms.txt with 81 provinces nationwide directory")

    print("\n--- 5. DAT/ DİZİNİ İLE SENKRONİZASYON ---")
    sync_files = [
        "index.html", "_redirects", "sitemap.xml", "llms.txt"
    ] + [f"{c['slug']}.html" for c in NEW_CITIES]
    
    for sf in sync_files:
        src = os.path.join(ROOT, sf)
        dst = os.path.join(DAT_DIR, sf)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"Synced to Dat/: {sf}")

    print("\n>>> BAŞARIYLA TAMAMLANDI! 81 İL YEREL SEO ALTYAPISI KURULDU.")

if __name__ == "__main__":
    main()
