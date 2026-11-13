#!/usr/bin/env python3
"""
DAT Özel Dedektiflik — Production SEO & Multi-Language Static Page Generator
Generates:
1. Pre-rendered static locale pages: /en/, /de/, /fr/, /ar/, /ru/, /me/
2. Dedicated Turkish SEO landing pages for Google Search rankings (cities & core services)
3. Full sitemap.xml with hreflang alternates
"""

import html as html_lib
import json
import os
import re
import subprocess
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOMAIN = "https://www.datdedektiflik.com"
TODAY = "2026-11-12"

LANG_CODES = ["en", "de", "fr", "ar", "ru", "me"]
OG_LOCALES = {
    "tr": "tr_TR",
    "en": "en_US",
    "de": "de_DE",
    "fr": "fr_FR",
    "ar": "ar_AE",
    "ru": "ru_RU",
    "me": "sr_ME",
}
HTML_LANG_ATTR = {
    "tr": "tr",
    "en": "en",
    "de": "de",
    "fr": "fr",
    "ar": "ar",
    "ru": "ru",
    "me": "cnr",
}

ASSET_PREFIXES = (
    "assets/",
    "dat-logo.png",
    "favicon.ico",
    "site.webmanifest",
    "script.js",
    "i18n.js",
    "lang/",
    "hizmetler/",
    "elsa-vaka-paneli.html",
    "istanbul-ozel-dedektif.html",
    "ankara-ozel-dedektif.html",
    "izmir-ozel-dedektif.html",
    "antalya-ozel-dedektif.html",
    "bursa-ozel-dedektif.html",
)


def load_all_lang_packs():
    jsc_cmd = """
    var window = {};
    ["en","de","fr","ar","ru","me"].forEach(function(c){
        load("%s/lang/" + c + ".js");
    });
    print(JSON.stringify(window.DAT_LANGS));
    """ % ROOT
    res = subprocess.run(
        ["/System/Library/Frameworks/JavaScriptCore.framework/Versions/Current/Helpers/jsc", "-e", jsc_cmd],
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(res.stdout)


def rewrite_rel_url(url, lang):
    if not url or url.startswith("#") or url.startswith("http") or url.startswith("mailto:") or url.startswith("tel:") or url.startswith("javascript:") or url.startswith("../"):
        return url
    if url == "./":
        return "../"
    if url in ("en/", "de/", "fr/", "ar/", "ru/", "me/"):
        return "./" if url.rstrip("/") == lang else f"../{url}"
    for pref in ASSET_PREFIXES:
        if url.startswith(pref):
            return "../" + url
    return url


_RTL_NUM_RE = re.compile(
    r"(\+\d[\d\s()-]{5,}\d|\(\s*0\d{2,3}\s*\)\s*\d{3}[\s-]\d{2}[\s-]\d{2}|\b(?:0\d{2,3}|\d{3})[\s-]\d{3}[\s-]\d{2}[\s-]\d{2}\b|\+90\s*5XX\s*XXX\s*XX\s*XX|#DAT-[A-Z0-9-]+|[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}|@[a-zA-Z0-9._-]+|\b\d{4}\s*[–-]\s*\d{4}\b|\+\d[\d.,]*\d|\b\d[\d.,]*\+)"
)


def wrap_rtl_plain(s, is_rtl):
    if not is_rtl or not s:
        return s
    return _RTL_NUM_RE.sub(lambda m: f"\u2066{m.group(1)}\u2069", s)


def wrap_rtl_text_to_html(s):
    if not s:
        return s
    out = []
    last = 0
    for m in _RTL_NUM_RE.finditer(s):
        if m.start() > last:
            out.append(html_lib.escape(s[last:m.start()], quote=False))
        out.append(
            f'<span dir="ltr" class="ltr-isolate" style="unicode-bidi:isolate">{html_lib.escape(m.group(1), quote=False)}</span>'
        )
        last = m.end()
    if last < len(s):
        out.append(html_lib.escape(s[last:], quote=False))
    return "".join(out)


def wrap_rtl_html(s, is_rtl):
    if not is_rtl or not s:
        return s
    parts = re.split(r'(<[^>]+>)', s)
    in_ltr_span = 0
    out = []
    for part in parts:
        if not part:
            continue
        if part.startswith("<"):
            if re.match(r'<(?:span|bdi)\b[^>]*(?:dir=["\']ltr["\']|ltr-isolate)', part, re.I):
                in_ltr_span += 1
            elif in_ltr_span > 0 and re.match(r'</(?:span|bdi)\s*>', part, re.I):
                in_ltr_span -= 1
            out.append(part)
        elif in_ltr_span > 0:
            out.append(part)
        else:
            out.append(_RTL_NUM_RE.sub(lambda m: f'<span dir="ltr" class="ltr-isolate" style="unicode-bidi:isolate">{m.group(1)}</span>', part))
    return "".join(out)


def translate_html_text(text, phrases, is_rtl=False, plain_rtl=False):
    m = re.match(r"^(\s*)([\s\S]*?)(\s*)$", text)
    if not m:
        return text
    lead, body, trail = m.groups()
    unescaped = html_lib.unescape(body)
    norm = re.sub(r"\s+", " ", unescaped).strip()
    if not norm:
        return text
    translated = phrases.get(norm)
    if translated is None:
        if not is_rtl or not _RTL_NUM_RE.search(unescaped):
            return text
        source = unescaped
    else:
        source = translated
    if is_rtl:
        rendered = wrap_rtl_plain(source, True) if plain_rtl else wrap_rtl_text_to_html(source)
        return f"{lead}{rendered}{trail}"
    return f"{lead}{html_lib.escape(source, quote=False)}{trail}"


class LocalePageRenderer(HTMLParser):
    VOID_TAGS = {"br", "hr", "img", "input", "meta", "link", "source"}

    def __init__(self, lang, pack):
        super().__init__(convert_charrefs=False)
        self.lang = lang
        self.pack = pack
        self.phrases = pack.get("phrases", {})
        self.html_blocks = pack.get("htmlBlocks", {})
        self.meta = pack.get("meta", {})
        self.out = []
        self.stack = []
        self.text_buf = []
        self.skip_block_depth = 0
        self.in_title = False
        self.in_lang_code_badge = False

    def flush_text(self):
        if not self.text_buf:
            return
        raw = "".join(self.text_buf)
        self.text_buf = []
        if self.skip_block_depth > 0:
            return
        if self.in_title and self.meta.get("title"):
            self.out.append(html_lib.escape(self.meta["title"], quote=False))
            return
        if self.in_lang_code_badge:
            self.out.append(self.lang.upper())
            return
        if not self.is_text_excluded():
            is_rtl = (self.pack.get("dir") == "rtl") and not self.is_in_ltr_ancestor()
            self.out.append(translate_html_text(raw, self.phrases, is_rtl, plain_rtl=self.is_plain_text_tag()))
        else:
            self.out.append(raw)

    def is_in_ltr_ancestor(self):
        for _, attrs in self.stack:
            if attrs.get("dir") == "ltr":
                return True
            cls = attrs.get("class", "")
            if cls and "ltr-isolate" in cls.split():
                return True
        return False

    def is_plain_text_tag(self):
        return any(tag in ("title", "option", "textarea", "select") for tag, _ in self.stack)

    def is_text_excluded(self):
        for tag, attrs in self.stack:
            if tag in ("script", "style", "noscript", "svg", "kbd", "code", "head"):
                return True
            if "data-no-i18n" in attrs or "data-i18n-html" in attrs or "data-live-visitors" in attrs:
                return True
            if attrs.get("id") in ("cartCountBadge", "storeSectionCartCount"):
                return True
        return False

    def is_attr_excluded(self):
        return any("data-no-i18n" in attrs for _, attrs in self.stack)

    def render_attrs(self, tag, attrs_list):
        attr_dict = dict(attrs_list)
        parts = []
        excluded_attr = self.is_attr_excluded()

        # Meta overrides
        name_val = attr_dict.get("name", "")
        prop_val = attr_dict.get("property", "")
        rel_val = attr_dict.get("rel", "")

        for k, v in attrs_list:
            if tag == "html" and k == "lang":
                v = HTML_LANG_ATTR.get(self.lang, self.lang)
            elif tag == "meta" and name_val == "description" and k == "content" and self.meta.get("description"):
                v = self.meta["description"]
            elif tag == "meta" and prop_val == "og:title" and k == "content" and self.meta.get("title"):
                v = self.meta["title"]
            elif tag == "meta" and prop_val == "og:description" and k == "content" and self.meta.get("description"):
                v = self.meta["description"]
            elif tag == "meta" and name_val == "twitter:title" and k == "content" and self.meta.get("title"):
                v = self.meta["title"]
            elif tag == "meta" and name_val == "twitter:description" and k == "content" and self.meta.get("description"):
                v = self.meta["description"]
            elif tag == "meta" and prop_val == "og:locale" and k == "content":
                v = OG_LOCALES.get(self.lang, "en_US")
            elif tag == "meta" and prop_val == "og:url" and k == "content":
                v = f"{DOMAIN}/{self.lang}/"
            elif tag == "link" and rel_val == "canonical" and k == "href":
                v = f"{DOMAIN}/{self.lang}/"
            elif k in ("src", "href") and v is not None:
                v = rewrite_rel_url(v, self.lang)
            elif not excluded_attr and k in ("placeholder", "title", "aria-label") and v is not None:
                norm = re.sub(r"\s+", " ", v).strip()
                v = self.phrases.get(norm, v)
                if self.pack.get("dir") == "rtl":
                    v = wrap_rtl_plain(v, True)

            if v is None:
                parts.append(k)
            else:
                escaped = html_lib.escape(v, quote=True)
                parts.append(f'{k}="{escaped}"')

        if tag == "html" and self.pack.get("dir") == "rtl" and "dir" not in attr_dict:
            parts.append('dir="rtl"')
        elif tag == "html" and "dir" not in attr_dict:
            parts.append('dir="ltr"')

        return (" " + " ".join(parts)) if parts else ""

    def handle_decl(self, decl):
        self.flush_text()
        self.out.append(f"<!{decl}>")

    def handle_comment(self, data):
        self.flush_text()
        if self.skip_block_depth == 0:
            self.out.append(f"<!--{data}-->")

    def handle_starttag(self, tag, attrs):
        self.flush_text()
        attr_dict = dict(attrs)
        if self.skip_block_depth > 0:
            if tag not in self.VOID_TAGS:
                self.skip_block_depth += 1
            return

        if tag == "script" and (attr_dict.get("src") or "").split("?")[0] == "script.js":
            self.out.append(f'<script>window.DAT_STATIC_PAGE_LANG = "{self.lang}";</script>\n    ')

        self.stack.append((tag, attr_dict))
        self.out.append(f"<{tag}{self.render_attrs(tag, attrs)}>")

        if tag == "title":
            self.in_title = True
        if attr_dict.get("id") == "currentLangCode":
            self.in_lang_code_badge = True

        block_key = attr_dict.get("data-i18n-html")
        if block_key and block_key in self.html_blocks:
            blk_val = self.html_blocks[block_key]
            if self.pack.get("dir") == "rtl":
                blk_val = wrap_rtl_html(blk_val, True)
            self.out.append(blk_val)
            self.skip_block_depth = 1

        if tag in self.VOID_TAGS:
            self.stack.pop()

    def handle_startendtag(self, tag, attrs):
        self.flush_text()
        if self.skip_block_depth > 0:
            return
        self.stack.append((tag, dict(attrs)))
        self.out.append(f"<{tag}{self.render_attrs(tag, attrs)} />")
        self.stack.pop()

    def handle_endtag(self, tag):
        self.flush_text()
        if self.skip_block_depth > 0:
            if tag not in self.VOID_TAGS:
                self.skip_block_depth -= 1
            if self.skip_block_depth == 0:
                if self.stack and self.stack[-1][0] == tag:
                    self.stack.pop()
                self.out.append(f"</{tag}>")
            return

        if tag == "title":
            self.in_title = False
        if self.in_lang_code_badge and tag == "span":
            self.in_lang_code_badge = False

        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                self.stack = self.stack[:i]
                break
        self.out.append(f"</{tag}>")

    def handle_data(self, data):
        if self.skip_block_depth == 0:
            self.text_buf.append(data)

    def handle_entityref(self, name):
        if self.skip_block_depth == 0:
            self.text_buf.append(f"&{name};")

    def handle_charref(self, name):
        if self.skip_block_depth == 0:
            self.text_buf.append(f"&#{name};")

    def close(self):
        self.flush_text()
        super().close()


JSONLD_KEY_MAP = {
    "DAT Özel Dedektiflik Hizmetleri": "12 Resmi Araştırma Hizmetimiz",
    "DAT Özel Dedektiflik Bürosu": "DAT ÖZEL DEDEKTİFLİK BÜROSU",
    "Eş Takibi & Sadakat Araştırması": "Eş Takibi & Sadakat Araştırması",
    "Evlilik Öncesi & Nişanlı Araştırması": "Evlilik Öncesi & Nişanlı Araştırması",
    "Velayet ve Boşanma Davaları Delil Araştırması": "Velayet ve Boşanma Davaları",
    "Adres Tespiti, Kayıp Şahıs ve Borçlu Takibi": "Adres Tespiti & Kayıp Kişi Araştırması",
    "Böcek Arama & TSCM Karşı-Casusluk": "Böcek Arama (TSCM)",
    "Kurumsal Firma Araştırması ve WPYB Marka Koruma": "Marka Taklidi & Sahte Ürün Araştırması",
}


def localize_json_ld(rendered, code, pack):
    """Translate <script type='application/ld+json'> schemas for static locale pages."""
    phrases = pack.get("phrases", {})
    meta = pack.get("meta", {})
    match = re.search(
        r'(<script\s+type=["\']application/ld\+json["\']\s*>)([\s\S]*?)(</script>)',
        rendered,
        flags=re.IGNORECASE,
    )
    if not match:
        return rendered

    try:
        data = json.loads(match.group(2))
    except Exception:
        return rendered

    def tr_key(text):
        mapped = JSONLD_KEY_MAP.get(text, text)
        return phrases.get(mapped, phrases.get(text, text))

    items = data if isinstance(data, list) else [data]
    for obj in items:
        if not isinstance(obj, dict):
            continue
        otype = obj.get("@type")
        if otype == "LegalService":
            if meta.get("description"):
                obj["description"] = meta["description"]
            obj["url"] = f"{DOMAIN}/{code}/"
            catalog = obj.get("hasOfferCatalog")
            if isinstance(catalog, dict):
                if catalog.get("name"):
                    catalog["name"] = tr_key(catalog["name"])
                for offer in catalog.get("itemListElement", []):
                    svc = offer.get("itemOffered") if isinstance(offer, dict) else None
                    if isinstance(svc, dict) and svc.get("name"):
                        svc["name"] = tr_key(svc["name"])
        elif otype == "WebSite":
            if obj.get("name"):
                obj["name"] = tr_key(obj["name"])
            obj["url"] = f"{DOMAIN}/{code}/"
            obj["inLanguage"] = HTML_LANG_ATTR.get(code, code)
        elif otype == "FAQPage":
            for q in obj.get("mainEntity", []):
                if not isinstance(q, dict):
                    continue
                if q.get("name"):
                    q["name"] = phrases.get(q["name"], q["name"])
                acc = q.get("acceptedAnswer")
                if isinstance(acc, dict) and acc.get("text"):
                    acc["text"] = phrases.get(acc["text"], acc["text"])

    localized_json = json.dumps(data, ensure_ascii=False, indent=6)
    return rendered[: match.start(2)] + "\n" + localized_json + "\n    " + rendered[match.end(2) :]


def build_locale_pages(index_src, langs):
    generated = []
    for code in LANG_CODES:
        pack = langs[code]
        renderer = LocalePageRenderer(code, pack)
        renderer.feed(index_src)
        rendered = "".join(renderer.out)
        rendered = localize_json_ld(rendered, code, pack)
        # Also rewrite footer lang switcher exact active style or openPhotoModal string asset paths
        out_dir = os.path.join(ROOT, code)
        os.makedirs(out_dir, exist_ok=True)
        out_file = os.path.join(out_dir, "index.html")
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(rendered)
        generated.append(f"{code}/")
    return generated


SEO_LANDING_PAGES = [
    {
        "rel_path": "istanbul-ozel-dedektif.html",
        "title": "İstanbul Özel Dedektif Bürosu (Kartal Merkez) — DAT Dedektiflik",
        "description": "İstanbul Avrupa ve Anadolu yakasının tüm 39 ilçesinde 2005'ten beri Ümit Hakan Karakaya liderliğinde 4.000+ vaka deneyimiyle eş takibi, boşanma delili, adres ve firma araştırması.",
        "keywords": "istanbul özel dedektif, istanbul dedektiflik bürosu, kartal dedektif, kadıköy özel dedektif, beşiktaş özel dedektif, eş takibi istanbul",
        "badge": "İSTANBUL MERKEZ BÜRO • 39 İLÇE 7/24 SAHA EKİBİ",
        "h1": "İstanbul Özel Dedektiflik ve Resmi Araştırma Hizmetleri",
        "lead": "Helis Metro Tower (Kartal / İstanbul) merkez büromuzdan Kadıköy, Beşiktaş, Şişli, Bakırköy, Ataşehir, Sarıyer ve Büyükçekmece dahil 39 ilçede %100 ispat ve yasal delil garantisiyle 7/24 görev yapıyoruz.",
        "image": "assets/services/es-takibi.jpg",
        "law": "TMK m.161 • HMK m.199 • TCK m.134 Tam Uyumlu",
        "form_cat": "es-takibi",
        "sections": [
            ("İstanbul Genelinde 7/24 Mobil Saha Gözetimi", "İstanbul'un yoğun trafiği, Boğaz geçişleri ve çok merkezli yapısı nedeniyle amatör takip girişimleri dakikalar içinde fark edilir ve davadaki delil gücünüzü yok eder. DAT Özel Dedektiflik, İstanbul'un iki yakasında konuşlu çift vardiya saha ekipleriyle hedef şahıs fark etmeden 4K zaman damgalı görüntüleme yürütür."),
            ("İstanbul Merkez Ofisimizde Sunulan Başlıca Hizmetler", "Aile Hukuku davalarına yönelik eş takibi ve velayet delil toplama dosyalarından; İkitelli, Tuzla, Dudullu ve Gebze sanayi hatlarında marka taklidi baskın araştırmalarına, Boğaziçi ve Levent plazalarında VIP makam odası ve araç TSCM böcek taramalarına kadar 12 ana uzmanlıkta yazılı sözleşmeli hizmet veriyoruz."),
            ("Kartal Helis Metro Tower Merkez Ofis Güvencesi", "Sadece telefon veya internet sitesinden açık adres vermeden çalışan yetkisiz kişilerden farklı olarak, İstanbul Kartal Metro çıkışındaki resmi merkez ofisimizde yüz yüze ön görüşme ve imzalı gizlilik sözleşmesi düzenliyoruz.")
        ],
        "deliverables": [
            "İstanbul 39 ilçede aynı gün saha ekibi yönlendirme imkanı",
            "Aile Mahkemesi (Çağlayan, Kartal, Bakırköy Adliyeleri) formatında delil klasörü",
            "4.000+ sonuçlandırılmış dosya tecrübesi ve %100 memnuniyet garantisi"
        ],
        "faqs": [
            ("İstanbul içinde ne kadar sürede ekip çıkarabiliyorsunuz?", "İstanbul Kartal merkezli mobil ekiplerimiz acil vakalarda aynı gün (2–4 saat içinde) saha gözetimine başlayabilir."),
            ("Görüşmeleri İstanbul ofisinizde yüz yüze yapabilir miyiz?", "Evet. Helis Metro Tower Kat:16 Kartal merkez büromuzda randevu alarak bizzat kurucu ve uzman ekibimizle görüşebilirsiniz."),
            ("İstanbul özel dedektiflik ücretleri nasıl belirlenir?", "Ücretlendirme vaka türüne, takip yapılacak yaka ve ilçe sayısına, ekip yoğunluğuna ve çalışma süresine göre Kartal merkez ofisimizde yapılan ön görüşmede netleştirilir; gizli ek masraf çıkarılmaz."),
            ("İstanbul'da elde edilen fotoğraf ve video delilleri Aile Mahkemesinde geçerli mi?", "Evet. TCK m.134 sınırlarına uyularak kamuya açık mekanlarda elde edilen tarih/saat damgalı görüntüler HMK m.199 kapsamında İstanbul Aile Mahkemelerine sunulabilir.")
        ]
    },
    {
        "rel_path": "ankara-ozel-dedektif.html",
        "title": "Ankara Özel Dedektif Bürosu (Çankaya / Konutkent) — DAT Dedektiflik",
        "description": "Ankara Çankaya, Konutkent, Yenimahalle ve tüm başkent ilçelerinde 2005'ten beri resmi büro güvencesiyle eş takibi, evlilik öncesi araştırma, adres tespiti ve TSCM böcek arama.",
        "keywords": "ankara özel dedektif, çankaya dedektif, ankara dedektiflik bürosu, eş takibi ankara, konutkent dedektif",
        "badge": "ANKARA OFİS • ÇANKAYA / KONUTKENT",
        "h1": "Ankara Özel Dedektiflik ve Hukuki Delil Toplama",
        "lead": "Konutkent 3029. Cadde (Çankaya / Ankara) büromuz ile Çankaya, Çayyolu, Oran, GOP, Yenimahalle ve Batıkent başta olmak üzere Başkent genelinde resmi sözleşmeli özel araştırma hizmeti sunuyoruz.",
        "image": "assets/photos/yilin-enleri-odul-1.jpg",
        "law": "TÜRAVAK Aile Hukuku Normları • HMK m.199",
        "form_cat": "es-takibi",
        "sections": [
            ("Başkent Protokolüne ve Gizliliğe Uygun Operasyon Disiplini", "Ankara; bürokrasi, savunma, hukuk ve iş dünyasının kalbi olması nedeniyle sıfır hata ve azami gizlilik gerektirir. Ümit Hakan Karakaya liderliğindeki Ankara ekibimiz 2005 yılından bu yana Yüksek Yargı içtihatlarına tam uyumlu delil standartlarıyla çalışmaktadır."),
            ("Ankara'da En Yoğun Talep Edilen 5 Başlık", "Başkentte özellikle eş takibi ve zina ispatı, kamu ve özel sektör yönetici odalarında TSCM dinleme cihazı (böcek) taraması, evlilik öncesi nişanlı tahkikatı, icradan mal kaçıran borçluların fiili adres tespiti ve üniversite öğrenci güvenliği alanlarında 7/24 görev yapıyoruz."),
            ("Ekonomize & Ankara Sesi Yılın Firması Ödüllü Kurum", "Ankara Sesi Gazetesi ve Ekonomize Dergisi işbirliğiyle verilen 'Yılın Başarılı Araştırma Takip Firması' ödülü Ankara merkezli köklü kurumsal geçmişimizin tescilidir.")
        ],
        "deliverables": [
            "Çankaya Konutkent ofisimizde gizlilik sözleşmeli ön değerlendirme",
            "TCK m.134 özel hayat sınırlarına tam saygılı mahkeme dosyası",
            "0312 284 02 99 sabit merkez hattımızla 7/24 kesintisiz erişim"
        ],
        "faqs": [
            ("Ankara dışı çevre illere (Eskişehir, Konya, Kırıkkale) hizmet var mı?", "Evet. Ankara merkezimiz İç Anadolu ve tüm 81 ile talep üzerine mobil saha ekibi yönlendirmektedir."),
            ("Sabit telefonunuzdan mesai dışı da ulaşabilir miyiz?", "Merkez hattımız 0312 284 02 99 ve WhatsApp hattımız 0532 666 77 49 günün 24 saati nöbetçi uzmanlara bağlıdır."),
            ("Ankara Konutkent büronuzda yazılı gizlilik sözleşmesi yapılıyor mu?", "Evet. Tüm bireysel ve kurumsal dosyalarda Çankaya Konutkent ofisimizde karşılıklı yazılı gizlilik sözleşmesi imzalanır ve resmi e-Fatura düzenlenir."),
            ("Ankara'da makam odası ve araç böcek taraması (TSCM) ne kadar sürer?", "10 kHz – 24 GHz RF spektrum analizörleri ve NLJD cihazlarıyla standart makam ofisi ve VIP araç taraması aynı gün 2 ila 5 saat içinde tamamlanır.")
        ]
    },
    {
        "rel_path": "izmir-ozel-dedektif.html",
        "title": "İzmir Özel Dedektif Bürosu (Alsancak / Karşıyaka / Bornova) — DAT Dedektiflik",
        "description": "İzmir Konak, Alsancak, Karşıyaka, Bornova, Bayraklı ve Çeşme genelinde 2005'ten beri resmi sözleşmeli eş takibi, boşanma delili, adres tespiti ve kurumsal araştırmalar.",
        "keywords": "izmir özel dedektif, izmir dedektiflik bürosu, karşıyaka dedektif, alsancak dedektif, eş takibi izmir, çeşme özel dedektif",
        "badge": "İZMİR & EGE BÖLGESİ • 30 İLÇE 7/24 SAHA EKİBİ",
        "h1": "İzmir Özel Dedektiflik ve Ege Bölgesi Delil Araştırması",
        "lead": "Konak, Alsancak, Karşıyaka, Bornova, Bayraklı, Buca ve Çeşme–Urla sahil hattı dahil İzmir'in 30 ilçesinde %100 gizlilik, yazılı sözleşme ve mahkemede geçerli delil standardıyla 7/24 hizmet veriyoruz.",
        "image": "assets/photos/yilin-enleri-odul-2.jpg",
        "law": "TMK m.161 • HMK m.199 • TCK m.134 Tam Uyumlu",
        "form_cat": "es-takibi",
        "sections": [
            ("İzmir ve Ege Sahil Hattında Çift Vardiya Saha Operasyonu", "İzmir şehir merkezindeki yoğun trafik ile Çeşme, Urla, Alaçatı ve Kuşadası gibi sezonluk geçiş noktaları profesyonel araç-ekip rotasyonu gerektirir. Ege mobil ekibimiz hedef şahsa hissettirmeden 4K zaman damgalı görüntüleme ve mekan kronolojisi oluşturur."),
            ("Ege Bölgesinde En Sık Talep Edilen Dosyalar", "Aile Hukuku (zina ispatı, velayet ve mal kaçırma), yazlık/kışlık dönemlerde nişanlı veya eş gözlemi, İzmir serbest bölge ve sanayi hatlarında şirket/ortaklık tahkikatı ile tebligat adresi tespiti başlıca uzmanlıklarımızdır."),
            ("Resmi Sözleşme, Fatura ve UÖDED Güvencesi", "İzmir ve çevre illerdeki (Manisa, Aydın, Muğla, Denizli) tüm araştırmalar Ümit Hakan Karakaya koordinasyonunda imzalı gizlilik sözleşmesi ve KVKK veri imha taahhüdüyle yürütülür.")
        ],
        "deliverables": [
            "İzmir 30 ilçe ile Çeşme, Bodrum ve Kuşadası hattında mobil takip ekibi",
            "İzmir Aile ve İcra Mahkemelerine uygun HMK m.199 uyumlu rapor",
            "7/24 WhatsApp (0532 666 77 49) ve merkez hat (0312 284 02 99) desteği"
        ],
        "faqs": [
            ("İzmir merkez dışında Çeşme, Urla veya Bodrum için hizmet alabilir miyiz?", "Evet. İzmir mobil ekibimiz Ege Bölgesi'ndeki tüm tatil beldeleri ve çevre illere (Aydın, Muğla, Manisa) aynı gün yönlendirilir."),
            ("İzmir'de eş takibi ve boşanma delili ne kadar sürede tamamlanır?", "Hızlı şüphe doğrulaması için 48 saatlik ekspres takip, kapsamlı dava klasörleri için ise ortalama 3–7 iş günü saha gözlemi uygulanır."),
            ("Elde edilen görseller İzmir mahkemelerinde delil olarak kabul edilir mi?", "Özel hayat alanına müdahale edilmeden yalnızca kamuya açık mekanlarda elde edilen zaman damgalı görüntüler HMK m.199 kapsamında hukuka uygun delil niteliğindedir."),
            ("İzmir büro ön görüşmesi ve sözleşme süreci nasıl işler?", "Randevu ve dosya kapsamı belirlendikten sonra resmi gizlilik sözleşmeniz hazırlanır; çalışma süresince tek muhatap ve mutlak kimlik gizliliği sağlanır.")
        ]
    },
    {
        "rel_path": "antalya-ozel-dedektif.html",
        "title": "Antalya Özel Dedektif Bürosu (Lara / Konyaaltı / Alanya) — DAT Dedektiflik",
        "description": "Antalya Muratpaşa, Lara, Konyaaltı, Alanya, Kemer ve Belek'te çok dilli (TR/EN/RU/DE) eş takibi, otel/tatil dönemi saha gözlemi, adres tespiti ve uluslararası tahkikat.",
        "keywords": "antalya özel dedektif, antalya dedektiflik bürosu, alanya dedektif, kemer dedektif, lara dedektif, eş takibi antalya",
        "badge": "ANTALYA & AKDENİZ • ÇOK DİLLİ (TR/EN/RU/DE) EKİP",
        "h1": "Antalya Özel Dedektiflik ve Çok Dilli Akdeniz Saha Ekibi",
        "lead": "Muratpaşa, Lara, Konyaaltı, Kemer, Belek, Side ve Alanya hattında hem Türkçe hem de İngilizce, Rusça ve Almanca bilen profesyonel kadromuzla turizm ve ikamet odaklı tüm araştırmaları yürütüyoruz.",
        "image": "assets/photos/uluslararasi-kongre-sahne.jpg",
        "law": "TMK m.161 • MÖHUK • HMK m.199 Uyumlu",
        "form_cat": "es-takibi",
        "sections": [
            ("Turizm, Otel ve Yazlık Bölgelerde Hassas Saha Gözlemi", "Antalya ve Alanya; yabancı uyruklu evlilikler, kısa süreli tatil/iş seyahatleri ve rezidans yaşamı nedeniyle standart takip yöntemlerinin yetersiz kaldığı özel bir coğrafyadır. DAT saha ekibi kamuya açık otel çevreleri, marinalar ve şehir merkezlerinde sıfır fark edilme riskiyle çalışır."),
            ("Yabancı Uyruklu Dosyalar ve Çapraz Sınır Araştırmaları", "Avrupa, Rusya ve BDT ülkelerinden Antalya'ya gelen şahıslara yönelik evlilik öncesi tahkikat, boşanma/velayet delili ve taşınmaz/ticari dolandırıcılık araştırmalarında uluslararası ağımız (WPYB Global) eş zamanlı destek verir."),
            ("Konut, Rezidans ve Yat/Araç TSCM Böcek Taraması", "Antalya'da iş insanları ve yönetici konutlarında gizli kamera, RF dinleme cihazı ve araç GPS takip modülü taramaları profesyonel spektrum analizörleriyle aynı gün gerçekleştirilir.")
        ],
        "deliverables": [
            "Antalya merkez, Alanya, Kemer, Kaş ve Belek'te aynı gün mobil ekip",
            "Yabancı uyruklu muhataplar için EN / RU / DE uyumlu uluslararası tahkikat",
            "Mahkemede geçerli tarih-saat damgalı kanıt ve konum raporu"
        ],
        "faqs": [
            ("Alanya, Kemer veya Belek'teki otel çevresi için takip yapılabilir mi?", "Evet. Otel iç özel alanlarına (oda vb.) girilmeden yalnızca halka ve müşteriye açık genel alan, giriş-çıkış ve çevre güzergahlarında yasal gözlem yapılır."),
            ("Yabancı uyruklu nişanlı veya eş için araştırma hizmeti veriyor musunuz?", "Evet. Antalya yerleşik veya yurt dışı bağlantılı yabancı uyruklu şahıslar için evlilik öncesi ve ticari güvenlik araştırması yürütüyoruz."),
            ("Antalya'da çalışma başlatmak için bizzat Antalya'da olmam şart mı?", "Hayır. Yurt dışından veya farklı illerden çevrimiçi ön görüşme ve dijital gizlilik sözleşmesi ile çalışmayı aynı gün başlatabilirsiniz."),
            ("Antalya dışı çevre illere (Isparta, Burdur, Mersin) ekip gidiyor mu?", "Evet, Akdeniz bölge ekibimiz talep doğrultusunda tüm çevre il ve ilçelere kesintisiz hizmet vermektedir.")
        ]
    },
    {
        "rel_path": "bursa-ozel-dedektif.html",
        "title": "Bursa Özel Dedektif Bürosu (Nilüfer / Osmangazi / İnegöl) — DAT Dedektiflik",
        "description": "Bursa Nilüfer, Osmangazi, Yıldırım, Mudanya ve İnegöl'de resmi dedektiflik: eş takibi, aile hukuku delilleri, fabrika/sanayi hırsızlık ve marka taklidi araştırmaları.",
        "keywords": "bursa özel dedektif, bursa dedektiflik bürosu, nilüfer dedektif, inegöl dedektif, eş takibi bursa, kurumsal araştırma bursa",
        "badge": "BURSA & GÜNEY MARMARA • AİLE + SANAYİ UZMANLIĞI",
        "h1": "Bursa Özel Dedektiflik, Aile Hukuku ve Sanayi Tahkikatı",
        "lead": "Nilüfer, Osmangazi, Yıldırım, Mudanya ve İnegöl başta olmak üzere Bursa'nın 17 ilçesinde bireysel aile dosyalarının yanında OSB ve ticari işletmelere özel iç suistimal ve marka koruma hizmeti sunuyoruz.",
        "image": "assets/photos/kiu-sertifika-programi.jpg",
        "law": "TMK m.161 • TTK Haksız Rekabet • SMK m.29",
        "form_cat": "es-takibi",
        "sections": [
            ("Bursa Merkez ve Marmara Geçiş Hattında Kesintisiz Takip", "Osmangazi Köprüsü, İstanbul–Bursa–İzmir otoyolu ve feribot hatları nedeniyle Bursa'daki vakalar şehirlerarası hareketlilik içerir. İstanbul Kartal merkezimizle koordineli çalışan Bursa saha ekibimiz şehir içi ve şehirlerarası geçişleri kopmadan kayıt altına alır."),
            ("Sanayi, Otomotiv ve Tekstil Sektöründe Kurumsal İstihbarat", "Bursa Organize Sanayi Bölgeleri ve İnegöl mobilya/tekstil merkezlerinde personel hırsızlığı, tedarikçi suistimali, rakip haksız rekabeti ve taklit ürün üretiminin belgelenmesi konusunda savcılık baskınına hazır dosyalar oluşturuyoruz."),
            ("Bireysel Aile Dosyalarında Kanuni Çerçeve", "Eş takibi, evlilik öncesi araştırma, öğrenci güvenliği ve velayet/nafaka gelir tespiti işlemlerinin tamamı TCK m.134'e tam uyumlu şekilde yürütülür.")
        ],
        "deliverables": [
            "Nilüfer, Osmangazi, Mudanya ve İnegöl'de hızlı mobil ekip koordinasyonu",
            "İstanbul–Bursa hattında kesintisiz şehirlerarası saha takibi",
            "Bireysel aile hukuku ve OSB kurumsal hırsızlık/marka taklidi raporlaması"
        ],
        "faqs": [
            ("İstanbul–Bursa arasında sık seyahat eden eş veya personel takip edilebiliyor mu?", "Evet. Kartal (İstanbul) ve Bursa saha ekiplerimiz feribot ve otoyol güzergahlarında vardiya devri yaparak kesintisiz takip sağlar."),
            ("Bursa'daki fabrikamızda yaşanan hammadde ve malzeme kayıpları için çalışıyor musunuz?", "Evet. Depo, sevkiyat ve vardiya çıkışlarında yasal gözetim yaparak iç suistimal veya dış işbirlikçileri savcılık dosyasına uygun şekilde tespit ediyoruz."),
            ("Bursa öğrenci takibi hizmeti üniversite kampüs çevresini kapsıyor mu?", "Evet, Bursa Uludağ Üniversitesi çevresinde ebeveyn talebiyle çocuğun güvenliği ve riskli çevre tespiti gizlilikle yapılmaktadır."),
            ("Çalışma öncesi resmi sözleşme ve fatura veriliyor mu?", "Tüm bireysel ve kurumsal Bursa dosyalarında yazılı gizlilik sözleşmesi ve resmi e-Fatura düzenlenir.")
        ]
    },
    {
        "rel_path": "hizmetler/es-takibi.html",
        "title": "Eş Takibi & Sadakat Araştırması (48 Saat / 7 Gün) — DAT Dedektiflik",
        "description": "Şüphelendiğiniz durumlarda eş takibi nasıl yapılır? TMK m.161 ve HMK m.199 kapsamında mahkemede geçerli 4K zaman damgalı delil dosyası ve %100 ispat garantisi.",
        "keywords": "eş takibi, aldatma tespiti, boşanma delili, zina ispatı, özel dedektif eş takibi, sadakat araştırması",
        "badge": "01 • AİLE HUKUKU • TMK m.161 & HMK m.199",
        "h1": "Eş Takibi ve Hukuka Uygun Aldatma Delili Toplama",
        "lead": "Siz yokken eşinizin kimlerle görüştüğünü ve nereye gittiğini; hedef şahsa kesinlikle fark ettirmeden kamuya açık alanlarda 4K zaman damgalı fotoğraf, video ve kronolojik saha raporuyla ispatlıyoruz.",
        "image": "assets/services/es-takibi.jpg",
        "law": "TMK m.161 (Zina) • TMK m.166 • HMK m.199",
        "form_cat": "es-takibi",
        "sections": [
            ("Neden Amatörce Takip Tehlikelidir?", "Eşinden şüphelenen birçok kişi kendi başına GPS takmaya çalışmak, izinsiz ses kaydı almak veya telefon şifresi kırmak gibi yöntemlere yönelir. Bu adımlar TCK m.132-134 kapsamında suç teşkil eder ve Yargıtay kararlarına göre 'hukuka aykırı delil' sayıldığı için boşanma davanızı kaybettirebilir."),
            ("48 Saat Ekspres ve 5–7 Gün Kapsamlı Gözlem Süreci", "Sertifikalı araştırma görevlilerimiz yalnızca kamuya açık mekanlarda (restoran, otel giriş-çıkış, AVM, otopark, halka açık cadde) objektif gözlem yaparak hukuka uygun somut kanıt üretir. Dilerseniz 48 saatlik hızlı analiz protokolüyle şüphenizi netleştirebilir, dilerseniz kapsamlı dava klasörü hazırlatabilirsiniz."),
            ("Mahkemede Geçerli Rapor Formatı", "Teslim edilen her klasörde tarih/saat damgalı yüksek çözünürlüklü görseller, araç-mekan kronolojisi ve avukatınızın dava dilekçesine ekleyebileceği tarafsız saha özet tutanağı yer alır.")
        ],
        "deliverables": [
            "Hedefe kesinlikle fark ettirilmeden profesyonel kamuya açık alan takibi",
            "4K zaman damgalı fotoğraf, video ve saatlik hareket dökümü",
            "%100 ispat garantisi ve yazılı sözleşme kapsamında memnuniyet güvencesi"
        ],
        "faqs": [
            ("Elde ettiğiniz kanıtlar boşanma ve tazminat davasında geçerli mi?", "Evet. TCK m.134 özel hayat sınırları ihlal edilmeden, tamamen kamuya açık alanlarda elde edilen veriler HMK m.199 çerçevesinde hukuka uygun delil niteliğindedir."),
            ("Takip edildiğini anlama riski var mı?", "2005'ten bu yana 4.000'in üzerinde vaka tamamlamış tecrübeli ve döngüsel araç/personel değişimi kullanan ekiplerle fark edilme riskini sıfıra indiriyoruz."),
            ("Eş takibi hizmeti ortalama kaç gün sürer ve 48 saatlik seçenek var mı?", "Hızlı sadakat doğrulaması için 48 saatlik ekspres takip seçeneğimiz bulunur; kapsamlı boşanma ve tazminat dosyaları ise genellikle 3 ila 7 iş gününde tamamlanır."),
            ("Eş takibi ücretleri nasıl belirlenir ve gizlilik nasıl korunur?", "Ücret dosya kapsamına, şehir sayısına ve ekip/gün süresine göre sözleşme öncesi şeffaf biçimde belirlenir; kimliğiniz ve tüm kayıtlar mutlak gizlilikle korunur.")
        ]
    },
    {
        "rel_path": "hizmetler/evlilik-oncesi-arastirma.html",
        "title": "Evlilik Öncesi & Nişanlı Araştırması — %100 Gizli Tahkikat | DAT",
        "description": "Nişanlınızın veya müstakbel eşinizin geçmişi, borç/icra durumu, sosyal çevresi ve gerçek yaşam tarzı hakkında evlilik öncesi tamamen gizli araştırma hizmeti.",
        "keywords": "evlilik öncesi araştırma, nişanlı araştırması, nişanlımın geçmişini öğrenmek istiyorum, evlilik öncesi dedektif",
        "badge": "02 • ÖNLEYİCİ TAHKİKAT • %100 GİZLİLİK",
        "h1": "Evlilik Öncesi ve Nişanlı Geçmiş Araştırması",
        "lead": "Evlilik kararınızı vermeden önce müstakbel eşinizin beyan ettiği kimlik, meslek, aile yapısı, mali güvenilirlik ve sosyal çevre gerçeklerini karşı taraf hiç hissetmeden 3–6 iş gününde doğruluyoruz.",
        "image": "assets/services/evlilik-oncesi.jpg",
        "law": "KVKK Uyumu • Önleyici Bireysel Tahkikat",
        "form_cat": "evlilik-oncesi",
        "sections": [
            ("Evlilik Öncesi Neden Profesyonel Doğrulama Gerekir?", "Son yıllarda evlilik sonrasında ortaya çıkan ağır gizli borçlar, icra takipleri, önceki resmi/gayriresmi birliktelikler, kumar/madde bağımlılıkları veya sahte kariyer beyanları aile birliğini daha ilk aylarda yıkmaktadır."),
            ("Araştırma Kapsamında Neler İncelenir?", "3 ila 6 iş günü içinde kişinin fiili meslek ve çalışma düzeni, ticari itibarı, sosyal çevresi, müdavimi olduğu mekanlar, alışkanlıkları ve aile çevresine dair beyanlarının tutarlılığı gizlilik içinde saha gözlemiyle araştırılır."),
            ("Sıfır İfşa Garantisi", "Ne nişanlınız ne de ailesi veya ortak çevreniz bir araştırma yapıldığını asla bilmez. Teslim edilen gizli rapor sonrasında tüm kayıtlar sistemlerimizden silinir.")
        ],
        "deliverables": [
            "3–6 iş gününde eksiksiz sosyal çevre, kariyer ve yaşam tarzı raporu",
            "Mali tutarlılık, alışkanlıklar ve beyan doğrulama bulguları",
            "%100 gizlilik ve veri imha garantili müvekkil dosyası"
        ],
        "faqs": [
            ("Nişanlımın veya ailesinin araştırma yaptırdığımı öğrenmesi mümkün mü?", "Kesinlikle hayır. Tüm saha teyitleri pasif ve gizli gözlem kurallarıyla yürütülür; üçüncü kişilere tek kelime bilgi verilmez."),
            ("Yurt dışında yaşayan nişanlı için de araştırma yapıyor musunuz?", "Evet. Türkiye dışı Avrupa, Kıbrıs, Karadağ, Batum ve ABD merkezlerimiz aracılığıyla yurt dışı dosyaları da inceliyoruz."),
            ("Evlilik öncesi araştırmada tam olarak hangi başlıklar incelenir?", "Beyan edilen meslek ve çalışma düzeni, sosyal çevre ve müdavim mekanlar, fiili yaşam standardı ve mali tutarlılık kamuya açık gözlem ve açık kaynak analiziyle doğrulanır."),
            ("Nişanlı araştırması kaç günde teslim edilir ve sözleşme yapılır mı?", "Standart dosyalar 3 ila 6 iş gününde yazılı ve görselli gizli raporla teslim edilir; teslimat sonrasında sözleşme gereği tüm veriler sistemlerden silinir.")
        ]
    },
    {
        "rel_path": "hizmetler/velayet-bosanma.html",
        "title": "Velayet & Boşanma Davaları Delil Araştırması — DAT Dedektiflik",
        "description": "Çocuğun üstün menfaatini ispatlamak, velayet davasını kazanmak, nafaka ve mal paylaşımında gizlenen geliri belgelemek için resmi saha delil dosyası.",
        "keywords": "velayet davası delil, boşanma davası dedektif, çocuğun üstün menfaati, nafaka gelir tespiti",
        "badge": "03 • AİLE HUKUKU • TMK m.182 & HMK m.199",
        "h1": "Velayet ve Boşanma Davaları İçin Somut Delil Tespiti",
        "lead": "Aile Mahkemesi hakiminin temel ölçütü olan 'çocuğun üstün menfaati' ilkesini kanıtlamak, diğer ebeveynin yaşam tarzını, ihmal unsurlarını ve gizlenen gerçek gelirini belgelemek için yanınızdayız.",
        "image": "assets/services/velayet-bosanma.jpg",
        "law": "TMK m.182 (Velayet) • HMK m.199",
        "form_cat": "velayet-bosanma",
        "sections": [
            ("Velayet Davalarında Mahkemenin Baktığı Somut Kriterler", "Haklı olmanız yetmez; çocuğun kim yanında kaldığında okul, bakım, psikolojik güvenlik ve ahlaki ortam açısından daha iyi şartlara sahip olacağını mahkemeye göstermeniz gerekir. Bakıcı ihmalleri, çocuğun tehlikeli ortamlarda bırakılması veya düzensiz yaşam koşulları saha gözlemiyle belgelenir."),
            ("Nafaka ve Tazminat İçin Gerçek Gelir Araştırması", "Resmi bordrolarda asgari ücret görünürken lüks araçlar kullanan, kayıt dışı ortaklık veya işyeri işleten karşı tarafın fiili yaşam standardı somut fotoğraflı delillerle ortaya konur."),
            ("Avukatlarla Eşgüdümlü Dosya Hazırlığı", "Hazırlanan velayet ve boşanma delil paketi avukatınızın dava stratejisine tam uyumlu kronolojik formatta teslim edilir.")
        ],
        "deliverables": [
            "Çocuğun bakım, eğitim ve sosyal çevre güvenliği gözlem raporu",
            "Diğer ebeveynin ihmal ve yaşam standardı kanıt fotoğrafları",
            "Nafaka artırım/uyarlama davalarına yönelik fiili gelir tespiti"
        ],
        "faqs": [
            ("Devam eden velayet veya nafaka davam için delil toplayabilir misiniz?", "Evet. Dava devam ederken de avukatınızın talep edeceği delil sunma sürelerine paralel hızlı saha çalışması yürütüyoruz."),
            ("Öğrenci / ergenlik çağındaki çocuklar için takip yapıyor musunuz?", "Evet. Velayeti sizde olan çocuğunuzun okul dışı riskli arkadaş çevresi için pedagojik hassasiyetle gizli gözlem sağlıyoruz."),
            ("Nafaka davası için karşı tarafın gizlenen fiili geliri nasıl belgelenir?", "Resmi bordrolarda düşük gelir gösterirken lüks yaşam süren veya kayıt dışı işyeri işleten tarafın fiili çalışma düzeni ve yaşam standardı kamuya açık saha gözlemiyle belgelenir."),
            ("Velayet dosyası hazırlık süreci ortalama kaç gün sürer?", "Avukatınızın dava takvimine paralel olarak standart velayet ve ihmal tespiti dosyaları genellikle 5 ila 10 iş günü içinde mahkemeye hazır formatta tamamlanır.")
        ]
    },
    {
        "rel_path": "hizmetler/adres-ve-borclu-takibi.html",
        "title": "Adres Tespiti, Kayıp Şahıs & Borçlu Mal Varlığı Takibi — DAT",
        "description": "Tebligat yapılamayan kişilerin fiili adres tespiti, kayıp şahıs araştırması ve İİK m.277 kapsamında mal kaçıran borçluların varlık tespiti.",
        "keywords": "adres tespiti, borçlu takibi, mal varlığı tespiti, tasarrufun iptali delili, kayıp kişi bulma",
        "badge": "05–06 • İCRA & KONUM İSTİHBARATI • İİK m.277",
        "h1": "Fiili Adres Tespiti ve Borçlu Mal Varlığı Araştırması",
        "lead": "Resmi kayıt adresinde bulunmayan muhatapların fiilen yaşadığı konut/işyeri adreslerini ve yakınları üzerine mal kaçıran borçluların gizli varlıklarını Türkiye ve yurt dışında tespit ediyoruz.",
        "image": "assets/services/borclu-takibi.jpg",
        "law": "Tebligat Kanunu • İİK m.277 (Tasarrufun İptali)",
        "form_cat": "borclu-takibi",
        "sections": [
            ("İzini Kaybettiren Borçlu ve Tebligattan Kaçan Muhataplar", "İcra veya alacak davalarındaki en büyük tıkanıklık muhataba tebligat yapılamaması ve borçlunun kağıt üzerinde sıfır mal varlığı göstermesidir. Saha ekibimiz şahsın gerçekten nerede yaşadığını ve fiilen hangi işletme/aracı kullandığını tespit eder."),
            ("Muvazaalı Devir ve Tasarrufun İptali Delilleri", "Borçlunun alacaklıdan mal kaçırmak için akrabalarına devrettiği taşınmaz, şirket veya araçları bizzat kullanmaya devam ettiğini belgeleyerek icra avukatınızın İİK m.277 davasında elini güçlendiriyoruz."),
            ("Yurt Dışına Çıkan Şahıslar ve Kayıp Yakınlar", "Balkanlar (Karadağ / WPYB Global), Kıbrıs, Avrupa ve ABD ağımızla yurt dışına taşınan veya uzun süredir haber alınamayan yakınlar için de konum doğrulaması sunuyoruz.")
        ],
        "deliverables": [
            "Konut ve fiili çalışma adresi + tarih damgalı doğrulama fotoğrafı",
            "Kullanılan araçlar, işyeri bağlantıları ve gizli ticari faaliyet raporu",
            "İcra ve alacak avukatlarına hazır konum & istihbarat dosyası"
        ],
        "faqs": [
            ("Yıllardır kayıp olan mirasçı veya akrabayı bulabiliyor musunuz?", "Evet, yasal menfaatiniz (miras, aile bağı veya alacak hakkı) söz konusu olduğunda yurtiçi ve yurtdışı fiili adres tespiti yapıyoruz."),
            ("Ortalama sonuç alma süresi nedir?", "Adres tespiti ve borçlu saha araştırmaları dosya niteliğine göre ortalama 2 ila 8 iş gününde sonuçlanır."),
            ("Borçlunun üçüncü şahıslara devrettiği mal varlıkları nasıl tespit edilir?", "İİK m.277 tasarrufun iptali davalarına esas olmak üzere borçlunun yakınları üzerine devrettiği taşınmaz, şirket veya araçları fiilen kullanmaya devam ettiği saha doğrulamasıyla belgelenir."),
            ("Yurt dışına kaçan borçlu veya muhataplar için araştırma yapıyor musunuz?", "Evet. Türkiye'nin 81 ilinin yanı sıra Kıbrıs, Batum, Karadağ (Podgorica), Avrupa ve ABD ağımızda fiili konum doğrulaması yürütüyoruz.")
        ]
    },
    {
        "rel_path": "hizmetler/bocek-tarama-tscm.html",
        "title": "Böcek Arama & TSCM Casusluk Önleme Hizmeti — DAT Dedektiflik",
        "description": "Konut, yönetim kurulu odası, makam ofisi ve VIP araçlarda RF spektrum analizörü, termal kamera ve optik detektör ile profesyonel gizli kamera ve dinleme cihazı (böcek) taraması.",
        "keywords": "böcek arama, dinleme cihazı tespiti, gizli kamera bulma, tscm hizmeti, araç gps tarama",
        "badge": "12 • TSCM KARŞI-CASUSLUK • TCK m.132–134",
        "h1": "Profesyonel Böcek Arama ve Gizli Kamera Tespiti (TSCM)",
        "lead": "Konutunuzda, makam odanızda, toplantı salonunuzda ve VIP aracınızda yasa dışı yerleştirilmiş RF/Wi-Fi/GSM dinleme böceklerini, mikro kameraları ve gizli GPS takip cihazlarını aynı gün gelişmiş donanımlarla temizliyoruz.",
        "image": "assets/services/izleme-raporlama.jpg",
        "law": "TCK m.132–134 (Haberleşme & Özel Hayatın Gizliliği)",
        "form_cat": "bocek-tarama",
        "sections": [
            ("Ucuz El Dedektörleri Neden Yeterli Değildir?", "Yeni nesil Wi-Fi burst vericiler, sadece ses varken kayıt yapıp gece paket gönderen GSM modülleri veya kapalı durumdaki pasif mikro kameralar basit sinyal çubuklarıyla tespit edilemez. Profesyonel 10 kHz – 24 GHz spektrum analizörü, non-linear junction detector (NLJD) ve termal/optik tarama şarttır."),
            ("VIP Araç Altı, OBD ve İç Döşeme GPS Taraması", "Şirket yöneticilerinin veya bireysel müşterilerin araçlarına gizlice yerleştirilen mıknatıslı ya da sigorta/OBD kutusuna gizlenen takip cihazları lift/endoskopi ve RF taramasıyla tespit edilir."),
            ("Yasal Tutanak ve Savcılık Delili", "Tarama sonucunda cihaz tespit edilirse cihazın delil bütünlüğü ve parmak izi potansiyeli korunarak fotoğraflı ekspertiz raporu düzenlenir.")
        ],
        "deliverables": [
            "Geniş bant RF spektrum analizi, priz/tavan/mobilya ve NLJD fiziksel kontrol",
            "Kızılötesi optik gizli lens (pinhole kamera) ve termal ısı izi taraması",
            "Resmi TSCM Teknik Temizlik ve Savcılık Ekspertiz Raporu"
        ],
        "faqs": [
            ("Böcek arama işlemi ne kadar sürer?", "Daire veya standart ofislerde ortalama 2–4 saat, geniş plaza katları ve VIP araç kombinesinde aynı gün 4–6 saat içinde tamamlanır."),
            ("Tarama cihazını kendim satın alabilir miyim?", "Evet, sitemizdeki DAT Mağaza bölümünden BTK/CE sertifikalı kişisel RF Guard S3 dedektör ve Faraday kılıfı faturalı olarak sipariş verebilirsiniz."),
            ("Araçta gizli GPS takip cihazı veya GSM dinleme böceği tespit edilebilir mi?", "Evet. VIP binek ve makam araçlarının şasi altı, tampon içi, sigorta ve OBD portları endoskopik inceleme ve geniş bant RF analizörüyle taranarak gizli takip modülleri çıkarılır."),
            ("Tarama sonucunda dinleme cihazı bulunursa hukuki süreç nasıl işler?", "Cihazın yeri ve delil bütünlüğü bozulmadan fotoğraflı TSCM Teknik Ekspertiz Raporu düzenlenir; TCK m.132–134 kapsamında savcılık suç duyurusunda resmi delil olarak kullanılabilir.")
        ]
    },
    {
        "rel_path": "hizmetler/kurumsal-ve-marka-koruma.html",
        "title": "Firma Araştırma, İşyeri Hırsızlık & Marka Taklidi — DAT / WPYB",
        "description": "Şirket due diligence araştırması, personel suistimal ve hırsızlık tespiti, ticari dolandırıcılık ve SMK m.29 kapsamında sahte/taklit ürün baskın delil toplama.",
        "keywords": "firma araştırması, marka taklidi araştırma, işyeri hırsızlık dedektifi, kurumsal istihbarat, wpyb global",
        "badge": "07–10 • KURUMSAL & MARKA KORUMA • TTK & SMK m.29",
        "h1": "Kurumsal Firma Araştırmaları, İç Suistimal ve Marka Taklidi",
        "lead": "Ortaklık ve ticaret öncesi firma gerçeklik denetimi, fabrika/depo içi gizli hırsızlık aydınlatma, ticari dolandırıcılık ve tescilli markanızı taklit eden merdiven altı üreticilerin deşifresi.",
        "image": "assets/services/marka-taklidi.jpg",
        "law": "TTK Haksız Rekabet • SMK m.29 • TCK m.141–158",
        "form_cat": "kurumsal-teftis",
        "sections": [
            ("Ticari İstihbarat ve Ortaklık Öncesi Risk Analizi", "Yüksek hacimli ticari anlaşmalar öncesinde karşı şirketin gerçek üretim/depo kapasitesi, piyasa itibarı, fiili ortakları ve icra riskleri sahada teyit edilir. Kilit yöneticilerin rakip firmalarla gizli çıkar çatışması olup olmadığı gizlilikle araştırılır."),
            ("WPYB Global ile Marka Taklidi ve Sahte Ürün Mücadelesi", "Tescilli marka ve patentlerinizi kopyalayan gizli atölyeler, depolar ve toptan sevkiyat ağları saha takibi ve faturalı numune alımıyla belgelenir. Şirket avukatlarınızın savcılık arama ve el koyma (baskın) kararı çıkarabileceği eksiksiz dosya hazırlanır."),
            ("Fabrika, Mağaza ve Depo İçi Hırsızlık Çözümleri", "Kamera kör noktalarından çıkarılan emtia, araç-lojistik sızıntıları ve içerideki işbirlikçiler gizli gözetim ile deşifre edilir.")
        ],
        "deliverables": [
            "Yönetim kuruluna özel gizli firma doğrulama ve rekabet riski raporu",
            "SMK m.29 baskın ve el koyma kararına esas koordinatlı sahte üretim dosyası",
            "Hırsızlık ve bilişim dolandırıcılığı vakalarında savcılık suç duyurusu klasörü"
        ],
        "faqs": [
            ("Balkanlar ve Avrupa kaynaklı sahte üreticiler için çalışıyor musunuz?", "Evet. Podgorica (Karadağ) WPYB Global büromuz Türkiye, Balkanlar ve Avrupa dağıtım koridorlarında doğrudan marka koruma operasyonu yürütür."),
            ("Kurumsal çalışmalarınızda sözleşme ve fatura düzenleniyor mu?", "Tüm kurumsal ve bireysel araştırmalarımız resmi yazılı sözleşme ve fatura kapsamında yürütülür."),
            ("Sahte ürün baskınları (SMK m.29) için nasıl bir delil dosyası hazırlanıyor?", "Gizli atölye ve depo konumları, fiili üretim/sevkiyat akışı ve faturalı numune temini belgelenerek şirket avukatınızın savcılık el koyma kararı alabileceği koordinatlı dosya hazırlanır."),
            ("Personel hırsızlığı ve gizli rekabet ihlallerinde ne kadar sürede sonuç alınır?", "Kamera kör noktalarından mal çıkışı, lojistik sızıntısı ve gizli ortaklık vakaları kapsamına göre 5 ila 10 iş gününde somut raporla netleştirilir.")
        ]
    },
    {
        "rel_path": "hizmetler/ogrenci-takibi.html",
        "title": "Öğrenci Takibi & Genç Güvenliği Araştırması — DAT Dedektiflik",
        "description": "Okul dışı çevre güvenliği, arkadaş grubu risk analizi, zararlı alışkanlık önleme ve şehir dışı üniversite öğrenci güvenliği için pedagojik hassasiyetle profesyonel saha gözlemi.",
        "keywords": "öğrenci takibi, çocuk takibi dedektif, üniversite öğrenci güvenliği, zararlı alışkanlık tespiti, ebeveyn gözlem hizmeti",
        "badge": "04 • AİLE KORUMA • PEDAGOJİK HASSASİYET",
        "h1": "Öğrenci Takibi ve Genç Güvenliği Araştırması",
        "lead": "Özellikle lise ve şehir dışındaki üniversite çağındaki evladınızın okul dışı zamanını kimlerle, hangi ortamlarda geçirdiğini; gencin psikolojisini ve itibarını hiç zedelemeden anne-babaya objektif raporla bildiriyoruz.",
        "image": "assets/services/ogrenci-takibi.jpg",
        "law": "TMK Ebeveyn Velayet Sorumluluğu • Tam Gizlilik",
        "form_cat": "ogrenci-takibi",
        "sections": [
            ("Erken Tespit Neden Hayat Kurtarır?", "Şehir değiştirerek üniversiteye başlayan veya lise çağında okul dışı çevresi hızla değişen gençler; yasa dışı bahis, zararlı madde çevreleri, akran zorbalığı veya manipülatif arkadaşlıklarla aile fark etmeden karşı karşıya kalabilmektedir."),
            ("Gençlere Hissettirmeden Uzman Gözlem", "DAT Dedektiflik, çocuk ve gençlik dosyalarında standart sert takip yerine ebeveyn talebi çerçevesinde yalnızca okul çıkışı, yurt/kampüs çevresi ve sosyal mekanlarda görünmez pasif gözlem uygular."),
            ("Ebeveyne Yapıcı ve Kanıtlı Bilgilendirme", "Teslim edilen rapor; çocuğun düzenli devam durumu, görüştüğü riskli kişi veya mekan bilgileri ve zaman damgalı gözlem notlarından oluşur; ebeveynin doğru müdahalesine rehberlik eder.")
        ],
        "deliverables": [
            "Evlada kesinlikle hissettirilmeden 5–7 günlük sosyal çevre & mekan gözlemi",
            "Riskli arkadaş grubu, devam durumu ve güvenlik tehdidi tespiti",
            "Yalnızca yasal veli / ebeveyne teslim edilen gizli rapor"
        ],
        "faqs": [
            ("Çocuğum takip edildiğini fark ederse aramızdaki güven bozulur mu?", "Kesinlikle hayır. Öğrenci dosyalarında özel eğitimli, göze batmayan sivil ekipler görev alır ve öğrencinin özel alanlarına müdahale edilmez."),
            ("Farklı bir şehirde üniversite okuyan çocuğumuz için hizmet alabilir miyiz?", "Evet. İstanbul, Ankara, İzmir, Antalya, Bursa, Eskişehir ve diğer 81 ildeki üniversite şehirlerinde aktif saha ağımız mevcuttur."),
            ("18 yaşından büyük üniversite öğrencisi için yasal süreç nasıldır?", "Kamuya açık mekan ve kampüs dışı genel çevrelerde yasal sınırlar korunarak anne-baba adına güvenlik gözlemi yürütülür; özel haberleşme ihlali kesinlikle yapılmaz."),
            ("Öğrenci takibi hizmeti kaç gün sürer?", "Alışkanlık döngüsünü net görmek için genellikle hafta içi ve hafta sonunu kapsayan 5 ila 7 günlük gözlem paketi önerilir.")
        ]
    },
    {
        "rel_path": "hizmetler/bilisim-dolandiriciligi.html",
        "title": "Bilişim Dolandırıcılığı & Siber İz Delil Tespiti — DAT Dedektiflik",
        "description": "Sahte yatırım/kripto platformları, internet dolandırıcılığı, kimlik hırsızlığı, şantaj ve ticari dolandırıcılık vakalarında savcılık suç duyurusuna uygun OSINT ve teknik delil dosyası.",
        "keywords": "bilişim dolandırıcılığı tespiti, internet dolandırıcılığı delil, dolandırıcılık davaları dedektif, şantaj araştırması, kripto dolandırıcılığı",
        "badge": "06–08 • SİBER İSTİHBARAT & SAVCILIK DELİLİ • TCK m.158",
        "h1": "Bilişim Dolandırıcılığı ve Siber İz Delil Tespiti",
        "lead": "Çevrimiçi yatırım, kripto, e-ticaret, aşk/romantizm veya ticari ödeme tuzaklarıyla gerçekleştirilen dolandırıcılık ve dijital şantaj olaylarında faillerin açık kaynak izlerini, saha bağlantılarını ve teknik delillerini savcılık başvurusuna hazır hale getiriyoruz.",
        "image": "assets/services/bilisim-dolandiriciligi.jpg",
        "law": "TCK m.158 (Nitelikli Dolandırıcılık) • 5651 & CMK Delil Standartları",
        "form_cat": "bilisim-dolandiriciligi",
        "sections": [
            ("Sadece Ekran Görüntüsü Neden Savcılıkta Yetersiz Kalır?", "Dolandırıcılar sohbetleri siler, alan adlarını kapatır ve paravan şirketler kurar. Sıradan ekran görüntüleri manipüle edilebilir bulunduğu için hash doğrulamalı zaman damgası, alan adı/şirket izi ve paravan muhatapların fiili adres bağlantısı şarttır."),
            ("Dijital OSINT + Saha İstihbaratı Birleşimi", "DAT Özel Dedektiflik yalnızca dijital açık kaynak analiziyle (OSINT) yetinmez; Türkiye ve yurt dışında (Karadağ, Kıbrıs, Batum, AB, ABD) tespit edilen paravan adres ve fiziki temas noktalarını sahada da teyit eder."),
            ("Avukatlarla Koordineli Ceza & Tazminat Klasörü", "Hazırlanan teknik ve saha bulguları Cumhuriyet Başsavcılığı suç duyurusu dilekçenize eklenebilecek sistematik kronolojiyle sunulur.")
        ],
        "deliverables": [
            "Açık kaynak (OSINT), paravan firma, alan adı ve iletişim ağı analizi",
            "Zaman damgalı, değiştirilmemiş dijital kanıt & delil bütünlüğü tutanağı",
            "Varsa Türkiye/yurt dışı fiziki ofis veya fail bağlantı doğrulaması"
        ],
        "faqs": [
            ("Kayıp kripto veya EFT transferini doğrudan geri alabilir misiniz?", "Para blokesi ve iade kararı yalnızca Cumhuriyet Savcılığı ve mahkemelerce verilir; biz savcılığın somut adım atabilmesi için fail kimlik/iz ve paravan şirket delillerini toplarız."),
            ("Özel fotoğraf/video şantajı vakalarında gizlilik nasıl sağlanır?", "Tüm şantaj ve siber tehdit dosyaları yüksek gizlilik protokolüyle ele alınır; hiçbir kayıt üçüncü taraflarla paylaşılmaz ve işlem sonunda imha edilir."),
            ("Hukuka aykırı hackleme veya yasa dışı veri çekme yapıyor musunuz?", "Kesinlikle hayır. Tüm çalışmalarımız TCK çerçevesinde yasal açık kaynak araştırması (OSINT), dijital delil sabitleme ve fiziki saha doğrulamasına dayanır."),
            ("Bilişim dolandırıcılığı araştırması kaç gün sürer?", "Ön dijital iz ve teknik doğrulama raporu vakaya göre genellikle 3 ila 7 iş gününde tamamlanır.")
        ]
    },
    {
        "rel_path": "hizmetler/firma-arastirmasi.html",
        "title": "Firma Araştırması, Due Diligence & Ticari İstihbarat — DAT Dedektiflik",
        "description": "Ortaklık, bayilik, yüksek tutarlı vadeli satış veya yatırım öncesi rakip ve muhatap şirketin fiili kapasitesi, gizli icra/borç itibarı ve yönetici güvenilirliği araştırması.",
        "keywords": "firma araştırması, şirket istihbaratı, ticari due diligence, ortaklık öncesi araştırma, çalışan geçmiş araştırması",
        "badge": "09 • KURUMSAL İSTİHBARAT • TTK & TİCARET GÜVENLİĞİ",
        "h1": "Kurumsal Firma Araştırması ve Ticari İstihbarat",
        "lead": "Büyük tutarlı vadeli ticaret, ortaklık, tedarik anlaşması veya kritik yönetici alımı öncesinde karşı firmanın kağıt üzerindeki vitrini ile sahadaki gerçek gücünü birbirinden ayırarak şirketinizi ağır mali kayıplardan koruyoruz.",
        "image": "assets/services/firma-arastirmalari.jpg",
        "law": "TTK Basiretli Tacir İlkesi • KVKK Kurumsal Uyum",
        "form_cat": "firma-arastirmasi",
        "sections": [
            ("Kağıt Üzerindeki Şirketlere Karşı Saha Teyidi", "Günümüzde pek çok ticari dolandırıcılık, yalnızca sanal ofis gösterip yüksek kredi/çek limiti açtıran paravan şirketlerle yapılmaktadır. Saha ekibimiz muhatap şirketin fabrika, depo, sevkiyat ve fiili çalışan kapasitesini yerinde gözlemler."),
            ("Ortaklık ve Kilit Yönetici Güvenilirlik Analizi", "Üst düzey yönetici veya yeni iş ortağının önceki ticari sicil itibarı, piyasadaki ödeme disiplini ve rakip firmalarla gizli çıkar çatışması yaşayıp yaşamadığı ticari sır ilkelerine saygıyla incelenir."),
            ("Yurt İçi ve Yurt Dışı Tedarik Zinciri Doğrulaması", "Türkiye'nin yanı sıra Balkanlar (Karadağ / WPYB Global), Kıbrıs, Avrupa ve ABD merkezli ticari partnerler için de yerinde doğrulama raporu sunuyoruz.")
        ],
        "deliverables": [
            "Fiili fabrika, depo, showroom ve operasyon kapasitesi saha doğrulaması",
            "Piyasa itibarı, ticari devamlılık ve paravan şirket risk değerlendirmesi",
            "Yönetim kuruluna özel özet karar raporu ve belgeli bulgular"
        ],
        "faqs": [
            ("Araştırılan şirketin bundan haberi olur mu?", "Kesinlikle olmaz. Tüm saha teyitleri ve açık kaynak analizleri firmanın ticari işleyişini ve gizliliği etkilemeden yürütülür."),
            ("Sadece İstanbul ve Ankara'daki şirketleri mi inceliyorsunuz?", "Hayır. Türkiye'nin tüm sanayi bölgelerinde (Bursa, Gaziantep, Konya, Kayseri, İzmir, Adana) ve yurt dışı ofis ağımızda inceleme yapıyoruz."),
            ("Kurumsal hizmet bedeli için resmi fatura kesiliyor mu?", "Evet. Tüm firma araştırmaları için yazılı gizlilik sözleşmesi ve %100 resmi kurumsal e-Fatura düzenlenir."),
            ("Bir firma istihbarat raporu kaç günde hazırlanır?", "Tek merkezli yerli şirketlerde 3–5 iş günü, çok şubeli veya yurt dışı bağlantılı şirketlerde 5–10 iş günü içinde teslim edilir.")
        ]
    },
    {
        "rel_path": "hizmetler/hirsizlik-arastirmasi.html",
        "title": "İşyeri & Kurumsal Hırsızlık Araştırması — DAT Dedektiflik",
        "description": "Fabrika, depo, mağaza, şantiye ve şirket içi emtia/nakit hırsızlıkları, zimmet ve içeriden sızıntı vakalarında gizli gözetim ile fail ve işbirlikçi tespiti.",
        "keywords": "hırsızlık araştırması, işyeri hırsızlık dedektifi, depo hırsızlığı tespiti, şirket içi suistimal, zimmet araştırması",
        "badge": "10 • KURUMSAL GÜVENLİK • TCK m.141–155",
        "h1": "İşyeri Hırsızlığı ve İç Suistimal Araştırması",
        "lead": "Fabrika, depo, zincir mağaza, lojistik filosu veya ev/ofis ortamında tekrarlayan stok açıkları, hammadde kayıpları ve içeriden bilgi/mal sızıntılarını kamera kör noktalarını aşan saha takibiyle çözüme kavuşturuyoruz.",
        "image": "assets/services/hirsizlik-arastirma.jpg",
        "law": "TCK m.141–142 (Hırsızlık) • TCK m.155 (Güveni Kötüye Kullanma)",
        "form_cat": "hirsizlik-arastirmasi",
        "sections": [
            ("Kayıp Stoklar Nasıl Dışarı Çıkarılıyor?", "Kurumsal hırsızlıkların %70'inden fazlası içerideki bir personelin sevkiyat şoförü veya dış alıcıyla kurduğu koordinasyon sonucu gerçekleşir. İçeride sorgu başlatmak failleri sadece izlerini yok etmeye iter; oysa tesis dışı sessiz takip gerçek zinciri ortaya çıkarır."),
            ("Sevkiyat, Araç Rotası ve Çalıntı Malın Satış Noktası", "Şüpheli çıkışların gerçekleştiği vardiya saatlerinden itibaren araçların güzergahı, malı boşalttığı gizli depolar ve ikinci el/piyasa alıcıları fotoğraflı olarak belgelenir."),
            ("Savcılık ve İş Hukuku (4857 SK m.25/II) Delil Dosyası", "Toplanan hukuka uygun kanıtlar hem Cumhuriyet Savcılığı suç duyurusunda hem de haklı nedenle iş akdi feshinde şirketinizi tazminat yükünden korur.")
        ],
        "deliverables": [
            "Tesis dışı sevkiyat rotası, gizli buluşma ve boşaltma noktalarının tespiti",
            "İçerideki işbirlikçi ve dış alıcı ağını gösteren zaman damgalı dosya",
            "Savcılık ve İş Mahkemesi kullanımına uygun kronolojik tutanak"
        ],
        "faqs": [
            ("Şüphelendiğimiz personele hiçbir şey hissettirmeden tespit yapılabilir mi?", "Evet. Tüm gözlem ve takip çalışmaları işletme dışından yürütülerek içeride panik veya delil karartma oluşması engellenir."),
            ("Elde edilen belgeler kıdem/ihbar tazminatsız fesih (haklı fesih) için geçerli midir?", "Kamuya açık alanlarda hukuka uygun şekilde elde edilen tarih-saat damgalı bulgular şirket avukatınızın 4857 sayılı İş Kanunu m.25/II dosyasını destekler."),
            ("Bireysel ev veya villa hırsızlığı sonrası da araştırma yapıyor musunuz?", "Evet, kolluk başvurunuza ek olarak şüpheli çevre veya kayıp eşya ticari izleri konusunda yasal sınırlar içinde saha desteği sunuyoruz."),
            ("Depo ve fabrika hırsızlık araştırması ortalama kaç gün sürer?", "Vardiya ve sevkiyat döngüsüne göre genellikle 5 ila 12 iş günü içinde somut fail/adres tespiti yapılır.")
        ]
    },
    {
        "rel_path": "hizmetler/marka-taklidi-arastirmasi.html",
        "title": "Marka Taklidi, Sahte Ürün & WPYB Baskın Delili — DAT",
        "description": "Tescilli markanızı taklit eden gizli üretim atölyeleri, depolar ve toptan dağıtım ağlarının deşifresi; SMK m.29 kapsamında savcılık arama ve el koyma (baskın) kararına esas dosya.",
        "keywords": "marka taklidi araştırması, sahte ürün tespiti, wpyb global, smk 29 baskın delili, patent taklidi dedektif",
        "badge": "11 • WPYB GLOBAL & FİKRİ MÜLKİYET • SMK m.29",
        "h1": "Marka Taklidi, Sahte Ürün ve Fikri Mülkiyet Koruması",
        "lead": "Sektörde WPYB (World Protection Your Brand) markasıyla öncülük ettiğimiz marka koruma operasyonlarıyla; tescilli markanızı kopyalayan merdiven altı üreticileri, depoları ve toptan kanalları baskın kararına hazır delillerle deşifre ediyoruz.",
        "image": "assets/services/marka-taklidi.jpg",
        "law": "6769 Sayılı Sınai Mülkiyet Kanunu (SMK m.29–30) • TTK Haksız Rekabet",
        "form_cat": "marka-taklidi",
        "sections": [
            ("Yalnızca Perakendeciyi Yakalamak Neden Çözüm Değildir?", "Çarşı veya e-ticaret pazaryerlerindeki küçük satıcılara yapılan baskınlar taklit üretimi durdurmaz; ertesi gün aynı mal başka dükkandan çıkar. Gerçek çözüm, perakendeciden geriye giderek ana toptancı ve gizli imalathaneyi bulmaktır."),
            ("Faturalı Test Alımı (Trap Purchase) ve Üretim Hattı Takibi", "Saha uzmanlarımız şüpheli noktalardan hukuka uygun faturalı/fişli test alımı gerçekleştirir, teslimat araçlarını imalathane ve ana depoya kadar takip ederek adres ve plaka verilerini mahkeme standartlarında belgeler."),
            ("Türkiye + Balkanlar + Avrupa Gümrük & Dağıtım Ağı (WPYB)", "Karadağ (Podgorica) WPYB Global büromuz, Türkiye çıkışlı veya Balkanlar üzerinden Avrupa'ya uzanan sahte ürün koridorlarında da marka sahiplerine doğrudan saha desteği sağlar.")
        ],
        "deliverables": [
            "Gizli imalathane, etiketleme atölyesi ve ana depo açık adres koordinatları",
            "Savcılık arama ve el koyma (baskın) talebine esas faturalı test alımı & fotoğraflar",
            "Marka vekili ve şirket avukatınızla ortak operasyon planlaması"
        ],
        "faqs": [
            ("Hazırladığınız dosya savcılıktan arama ve el koyma kararı çıkartmak için yeterli olur mu?", "Evet. SMK m.29 kapsamında mahkemelerin aradığı açık adres, aktif ticari satış kanıtı (test alımı) ve görsel eşleşme unsurları eksiksiz sunulur."),
            ("E-ticaret sitelerinde (Instagram, pazaryerleri) markamızı taklit edenleri bulabiliyor musunuz?", "Evet. Çevrimiçi satıcının gönderim yaptığı gerçek depo/atölye çıkışı test siparişi ve lojistik doğrulamasıyla sahada tespit edilir."),
            ("Yurt dışına ihraç edilen taklit ürünler için de çalışma yapıyor musunuz?", "Evet, WPYB Global (Podgorica) ve uluslararası partner ağımızla sınır ötesi taklit koridorlarını takip ediyoruz."),
            ("Marka koruma dosyası ne kadar sürede tamamlanır?", "Tekil satıcıdan ana depoya uzanan tespitler genellikle 5 ila 10 iş gününde baskın başvurusuna hazır hale getirilir.")
        ]
    }
]


SUBPAGE_THEME_BOOT = '''    <script id="datThemeBoot">
        (function () {
            try {
                var saved = localStorage.getItem('dat_theme');
                var theme = (saved === 'light' || saved === 'dark') ? saved : 'dark';
                var root = document.documentElement;
                root.setAttribute('data-theme', theme);
                root.style.colorScheme = theme;
                if (theme === 'dark') root.classList.add('dark'); else root.classList.remove('dark');
                var meta = document.getElementById('themeColorMeta');
                if (meta) meta.setAttribute('content', theme === 'light' ? '#FFFFFF' : '#111111');
            } catch (e) {}
        })();
    </script>'''

SUBPAGE_STUDIO_CSS = '''        *:not(.hgi):not([class*="hgi-"]) { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important; }
        .hgi { display: inline-flex; align-items: center; justify-content: center; line-height: 1; vertical-align: middle; }
        .hgi.w-3\\.5 { font-size: 14px; }
        .hgi.w-4 { font-size: 16px; }
        .hgi.w-5 { font-size: 20px; }
        .studio-lime-btn { background-color: #93F051; color: #111111; }
        .studio-lime-btn:hover { background-color: #DDF95E; color: #111111; }
        [dir="rtl"] .ltr-isolate, [dir="rtl"] [dir="ltr"] { direction: ltr; unicode-bidi: isolate; }
        html.theme-switching,
        html.theme-switching *,
        html.theme-switching *::before,
        html.theme-switching *::after {
            transition: none !important;
            transition-duration: 0s !important;
        }

        /* Studio Obsidian (Dark) + Crisp Daylight (Light) Synchronized Theme */
        html[data-theme="dark"], html[data-theme="dark"] body {
            background-color: #111111 !important;
            color: #F5F5F7 !important;
        }
        html[data-theme="dark"] .studio-header {
            background-color: rgba(17, 17, 17, 0.88) !important;
            border-color: rgba(255, 255, 255, 0.09) !important;
        }
        html[data-theme="dark"] .studio-surface {
            background-color: #1C1C1F !important;
            border-color: rgba(255, 255, 255, 0.09) !important;
            color: #F5F5F7 !important;
        }
        html[data-theme="dark"] .studio-surface-soft {
            background-color: #18181A !important;
            border-color: rgba(255, 255, 255, 0.09) !important;
            color: #F5F5F7 !important;
        }
        html[data-theme="dark"] .studio-pill-muted {
            background-color: #242428 !important;
            border-color: rgba(255, 255, 255, 0.12) !important;
            color: #F5F5F7 !important;
        }
        html[data-theme="dark"] .studio-pill-muted:hover {
            background-color: #93F051 !important;
            color: #111111 !important;
            border-color: transparent !important;
        }
        html[data-theme="dark"] .studio-pill-muted:hover * {
            color: #111111 !important;
        }
        html[data-theme="dark"] .studio-title { color: #FFFFFF !important; }
        html[data-theme="dark"] .studio-body { color: #D4D4D8 !important; }
        html[data-theme="dark"] .studio-muted { color: #A1A1AA !important; }
        html[data-theme="dark"] .studio-accent-text { color: #93F051 !important; }
        html[data-theme="dark"] .studio-badge {
            background-color: #242428 !important;
            border-color: rgba(147, 240, 81, 0.35) !important;
            color: #93F051 !important;
        }
        html[data-theme="dark"] .studio-footer {
            background-color: #161618 !important;
            border-color: rgba(255, 255, 255, 0.08) !important;
            color: #A1A1AA !important;
        }
        html[data-theme="dark"] .studio-divider { border-color: rgba(255, 255, 255, 0.10) !important; }

        html[data-theme="light"], html[data-theme="light"] body {
            background-color: #F6F7F8 !important;
            color: #111111 !important;
        }
        html[data-theme="light"] .studio-header {
            background-color: rgba(255, 255, 255, 0.94) !important;
            border-color: rgba(17, 17, 17, 0.10) !important;
        }
        html[data-theme="light"] .studio-surface {
            background-color: #FFFFFF !important;
            border-color: rgba(17, 17, 17, 0.09) !important;
            color: #111111 !important;
        }
        html[data-theme="light"] .studio-surface-soft {
            background-color: #ECEEF2 !important;
            border-color: rgba(17, 17, 17, 0.08) !important;
            color: #111111 !important;
        }
        html[data-theme="light"] .studio-pill-muted {
            background-color: #ECEEF2 !important;
            border-color: rgba(17, 17, 17, 0.10) !important;
            color: #111111 !important;
        }
        html[data-theme="light"] .studio-pill-muted:hover {
            background-color: #111111 !important;
            color: #FFFFFF !important;
        }
        html[data-theme="light"] .studio-pill-muted:hover * {
            color: #FFFFFF !important;
        }
        html[data-theme="light"] .studio-title { color: #111111 !important; }
        html[data-theme="light"] .studio-body { color: #3A3E42 !important; }
        html[data-theme="light"] .studio-muted { color: #4B5563 !important; }
        html[data-theme="light"] .studio-accent-text { color: #15803D !important; }
        html[data-theme="light"] .studio-badge {
            background-color: #E6FAD8 !important;
            border-color: rgba(21, 128, 61, 0.25) !important;
            color: #15803D !important;
        }
        html[data-theme="light"] .studio-footer {
            background-color: #ECEEF2 !important;
            border-color: rgba(17, 17, 17, 0.10) !important;
            color: #374151 !important;
        }
        html[data-theme="light"] .studio-divider { border-color: rgba(17, 17, 17, 0.10) !important; }
        html[data-theme="light"] .studio-keep-dark {
            background-color: #111111 !important;
            color: #FFFFFF !important;
            border-color: rgba(255, 255, 255, 0.12) !important;
        }
        html[data-theme="light"] .studio-keep-dark .studio-lime-ink { color: #93F051 !important; }
        html[data-theme="light"] .studio-keep-dark .studio-coral-ink { color: #FA7E61 !important; }'''

SUBPAGE_THEME_SCRIPT = '''        (function syncSubpageThemeUI() {
            function refresh(t) {
                var ico = document.getElementById('themeToggleIcon');
                var lbl = document.getElementById('themeToggleLabel');
                var meta = document.getElementById('themeColorMeta');
                if (ico) ico.className = 'hgi hgi-stroke w-3.5 h-3.5 text-[#93F051] ' + (t === 'light' ? 'hgi-moon-02' : 'hgi-sun-03');
                if (lbl) lbl.textContent = t === 'light' ? 'Koyu' : 'Açık';
                if (meta) meta.setAttribute('content', t === 'light' ? '#FFFFFF' : '#111111');
            }
            window.toggleSiteTheme = function () {
                var root = document.documentElement;
                var cur = root.getAttribute('data-theme') === 'light' ? 'light' : 'dark';
                var next = cur === 'dark' ? 'light' : 'dark';
                root.classList.add('theme-switching');
                void root.offsetHeight;
                root.setAttribute('data-theme', next);
                root.style.colorScheme = next;
                root.classList.toggle('dark', next === 'dark');
                try { localStorage.setItem('dat_theme', next); } catch (_) {}
                refresh(next);
                requestAnimationFrame(function () {
                    requestAnimationFrame(function () {
                        root.classList.remove('theme-switching');
                    });
                });
            };
            refresh(document.documentElement.getAttribute('data-theme') === 'light' ? 'light' : 'dark');
        })();'''


def build_turkish_seo_pages():
    pages_meta = []
    # Quick nav map for cross-linking
    sibling_links = [
        ("umit-hakan-karakaya.html", "Ümit Hakan Karakaya"),
        ("elsa-vaka-paneli.html", "Elsa Vaka Paneli"),
        ("istanbul-ozel-dedektif.html", "İstanbul Büro"),
        ("ankara-ozel-dedektif.html", "Ankara Büro"),
        ("izmir-ozel-dedektif.html", "İzmir Dedektif"),
        ("antalya-ozel-dedektif.html", "Antalya Dedektif"),
        ("bursa-ozel-dedektif.html", "Bursa Dedektif"),
        ("hizmetler/es-takibi.html", "Eş Takibi"),
        ("hizmetler/evlilik-oncesi-arastirma.html", "Evlilik Öncesi"),
        ("hizmetler/velayet-bosanma.html", "Velayet & Boşanma"),
        ("hizmetler/ogrenci-takibi.html", "Öğrenci Takibi"),
        ("hizmetler/adres-ve-borclu-takibi.html", "Adres & Borçlu"),
        ("hizmetler/bilisim-dolandiriciligi.html", "Bilişim Dolandırıcılığı"),
        ("hizmetler/firma-arastirmasi.html", "Firma Araştırmaları"),
        ("hizmetler/hirsizlik-arastirmasi.html", "Hırsızlık Araştırmaları"),
        ("hizmetler/marka-taklidi-arastirmasi.html", "Marka Taklidi"),
        ("hizmetler/bocek-tarama-tscm.html", "Böcek Arama (TSCM)"),
        ("hizmetler/kurumsal-ve-marka-koruma.html", "Kurumsal & WPYB"),
    ]

    for pg in SEO_LANDING_PAGES:
        rel = pg["rel_path"]
        depth = rel.count("/")
        prefix = "../" * depth
        canonical = f"{DOMAIN}/{rel}"
        breadcrumb_items = [
            {"@type": "ListItem", "position": 1, "name": "Ana Sayfa", "item": f"{DOMAIN}/"},
            {"@type": "ListItem", "position": 2, "name": pg["h1"], "item": canonical},
        ]
        faq_entities = [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in pg["faqs"]
        ]
        schema = [
            {
                "@context": "https://schema.org",
                "@type": "LegalService",
                "name": f"{pg['h1']} — DAT Özel Dedektiflik",
                "url": canonical,
                "image": f"{DOMAIN}/{pg['image']}",
                "telephone": "+90-532-666-77-49",
                "email": "info@datdedektiflik.com",
                "founder": {"@type": "Person", "name": "Ümit Hakan Karakaya"},
                "foundingDate": "2005",
            },
            {
                "@context": "https://schema.org",
                "@type": "BreadcrumbList",
                "itemListElement": breadcrumb_items,
            },
            {
                "@context": "https://schema.org",
                "@type": "FAQPage",
                "mainEntity": faq_entities,
            },
        ]

        sections_html = "\n".join(
            f'''<section class="studio-surface bg-[#1C1C1F] rounded-3xl p-6 sm:p-8 border border-white/[0.09] shadow-sm space-y-3">
                <h2 class="studio-title text-lg sm:text-xl font-medium text-[#FFFFFF] tracking-tight">{html_lib.escape(sec_t)}</h2>
                <p class="studio-body text-sm sm:text-[15px] text-white/80 leading-relaxed">{html_lib.escape(sec_b)}</p>
            </section>'''
            for sec_t, sec_b in pg["sections"]
        )

        deliv_html = "\n".join(
            f'<li class="flex items-start gap-2.5 text-sm text-[#FFFFFF]/95"><span class="studio-lime-ink text-[#93F051] font-bold">✓</span><span>{html_lib.escape(d)}</span></li>'
            for d in pg["deliverables"]
        )

        faqs_html = "\n".join(
            f'''<div class="studio-surface-soft p-5 rounded-2xl bg-[#18181A] border border-white/[0.09] space-y-2">
                <h3 class="studio-title text-[15px] font-medium text-[#FFFFFF]">{html_lib.escape(q)}</h3>
                <p class="studio-body text-sm sm:text-[15px] text-white/75 leading-relaxed">{html_lib.escape(a)}</p>
            </div>'''
            for q, a in pg["faqs"]
        )

        sib_html = "\n".join(
            f'<a href="{prefix}{s_path}" class="px-3.5 py-2 rounded-full text-xs font-medium transition border {"studio-lime-btn border-transparent shadow-sm" if s_path == rel else "studio-pill-muted bg-[#242428] border-white/10 text-white/85"}">{html_lib.escape(s_lbl)}</a>'
            for s_path, s_lbl in sibling_links
        )

        page_html = f'''<!DOCTYPE html>
<html lang="tr" class="scroll-smooth dark" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
{SUBPAGE_THEME_BOOT}
    <title>{html_lib.escape(pg["title"])}</title>
    <meta name="description" content="{html_lib.escape(pg["description"])}">
    <meta name="keywords" content="{html_lib.escape(pg["keywords"])}">
    <meta name="robots" content="index, follow, max-image-preview:large">
    <meta id="themeColorMeta" name="theme-color" content="#111111">
    <link rel="canonical" href="{canonical}">
    <link rel="icon" type="image/png" href="{prefix}dat-logo.png">
    <link rel="shortcut icon" href="{prefix}favicon.ico">
    <link rel="preconnect" href="https://cdn.tailwindcss.com" crossorigin>
    <link rel="preconnect" href="https://use.hugeicons.com" crossorigin>
    <meta property="og:type" content="article">
    <meta property="og:locale" content="tr_TR">
    <meta property="og:url" content="{canonical}">
    <meta property="og:site_name" content="DAT Özel Dedektiflik Bürosu">
    <meta property="og:title" content="{html_lib.escape(pg["title"])}">
    <meta property="og:description" content="{html_lib.escape(pg["description"])}">
    <meta property="og:image" content="{DOMAIN}/{pg["image"]}">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:image" content="{DOMAIN}/{pg["image"]}">
    <script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://use.hugeicons.com/font/icons.css">
    <style>
{SUBPAGE_STUDIO_CSS}
    </style>
</head>
<body class="bg-[#111111] text-[#F5F5F7] antialiased selection:bg-[#93F051] selection:text-[#111111]">
    <div class="h-[3px] w-full bg-[#93F051]"></div>

    <header class="studio-header sticky top-0 z-40 bg-[#111111]/90 backdrop-blur-xl border-b border-white/[0.09]">
        <div class="max-w-6xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between gap-2 sm:gap-3">
            <a href="{prefix}index.html" class="flex items-center gap-3 group min-w-0">
                <img src="{prefix}dat-logo.png" alt="DAT Dedektiflik Logo" class="w-10 h-10 rounded-full object-cover ring-2 ring-[#93F051]/70 shrink-0">
                <div class="leading-none min-w-0">
                    <div class="studio-title text-sm font-medium text-[#FFFFFF] truncate">DAT <span class="studio-accent-text text-[#93F051]">DEDEKTİFLİK</span></div>
                    <p class="studio-muted text-[10px] font-mono text-white/60 uppercase mt-0.5 truncate">2005'ten Bugüne • 4.000+ Vaka</p>
                </div>
            </a>
            <div class="flex items-center gap-2 shrink-0">
                <button id="themeToggleBtn" type="button" onclick="toggleSiteTheme()" class="studio-pill-muted inline-flex items-center gap-1.5 px-2.5 sm:px-3 py-1.5 rounded-full bg-[#242428] border border-white/15 text-[11px] font-medium transition">
                    <i id="themeToggleIcon" class="hgi hgi-stroke hgi-sun-03 w-3.5 h-3.5 text-[#93F051]"></i>
                    <span id="themeToggleLabel" class="hidden sm:inline">Açık</span>
                </button>
                <a href="https://wa.me/905326667749" target="_blank" rel="noopener noreferrer" class="hidden sm:inline-flex items-center gap-1.5 px-3.5 py-2 rounded-full studio-pill-muted bg-[#242428] border border-white/10 text-xs font-medium transition">
                    <i class="hgi hgi-stroke hgi-whatsapp w-4 h-4 text-[#93F051]"></i>
                    <span>0532 666 77 49</span>
                </a>
                <a href="{prefix}index.html#vaka-bildir" class="inline-flex items-center gap-1.5 px-4 py-2 rounded-full studio-lime-btn text-xs font-medium shadow-sm transition whitespace-nowrap">
                    <span>Fiyat Teklifi Al</span>
                </a>
            </div>
        </div>
    </header>

    <main class="max-w-5xl mx-auto px-4 sm:px-6 py-7 sm:py-10 space-y-7 sm:space-y-8">
        <!-- Breadcrumb -->
        <nav aria-label="Breadcrumb" class="studio-muted text-xs font-mono text-white/60 flex items-center gap-2">
            <a href="{prefix}index.html" class="hover:underline studio-accent-text text-[#93F051]">Ana Sayfa</a>
            <span>/</span>
            <span class="studio-title text-[#FFFFFF] font-medium truncate">{html_lib.escape(pg["h1"])}</span>
        </nav>

        <!-- Studio Hero Card -->
        <div class="studio-surface-soft grid lg:grid-cols-12 gap-8 items-center bg-[#18181A] rounded-[28px] p-6 sm:p-9 border border-white/[0.09] shadow-2xl">
            <div class="lg:col-span-7 space-y-4">
                <span class="studio-badge inline-block px-3 py-1 rounded-full bg-[#242428] border border-[#93F051]/35 text-[#93F051] font-mono text-[11px] font-medium">{html_lib.escape(pg["badge"])}</span>
                <h1 class="studio-title text-2xl sm:text-4xl font-medium text-[#FFFFFF] leading-tight tracking-tight">{html_lib.escape(pg["h1"])}</h1>
                <p class="studio-body text-sm sm:text-base text-white/80 leading-relaxed">{html_lib.escape(pg["lead"])}</p>
                <div class="studio-accent-text text-xs font-mono text-[#93F051] pt-1">{html_lib.escape(pg["law"])}</div>
                <div class="flex flex-wrap gap-3 pt-2">
                    <a href="https://wa.me/905326667749" target="_blank" rel="noopener noreferrer" class="px-6 py-3 rounded-full studio-lime-btn text-xs font-medium inline-flex items-center gap-2 shadow-lg transition">
                        <i class="hgi hgi-stroke hgi-whatsapp w-4 h-4"></i>
                        <span>7/24 WhatsApp: 0532 666 77 49</span>
                    </a>
                    <a href="tel:+903122840299" class="studio-keep-dark px-5 py-3 rounded-full bg-[#242428] hover:bg-[#2E2E34] text-[#FFFFFF] border border-white/15 text-xs font-medium inline-flex items-center gap-2 transition">
                        <i class="hgi hgi-stroke hgi-call-02 w-4 h-4 studio-lime-ink text-[#93F051]"></i>
                        <span>Merkez: 0312 284 02 99</span>
                    </a>
                </div>
            </div>
            <div class="lg:col-span-5">
                <div class="rounded-2xl overflow-hidden border border-white/15 shadow-2xl aspect-[4/3] bg-[#111111]">
                    <img src="{prefix}{pg["image"]}" alt="{html_lib.escape(pg["h1"])}" class="w-full h-full object-cover">
                </div>
            </div>
        </div>

        <!-- Detailed Legal & Operational Content -->
        <div class="grid gap-5">
            {sections_html}
        </div>

        <!-- Deliverables Box -->
        <div class="studio-keep-dark bg-[#111111] text-[#FFFFFF] rounded-3xl p-6 sm:p-8 space-y-4 shadow-2xl border border-white/15">
            <div class="font-mono text-[11px] studio-coral-ink text-[#FA7E61] uppercase tracking-wider">DAT ÖZEL DEDEKTİFLİK • RESMİ TESLİMAT STANDARTLARI</div>
            <ul class="space-y-2.5">
                {deliv_html}
            </ul>
        </div>

        <!-- FAQs -->
        <section class="space-y-4">
            <h2 class="studio-title text-xl font-medium text-[#FFFFFF] tracking-tight">Sıkça Sorulan Sorular</h2>
            <div class="grid sm:grid-cols-2 gap-4">
                {faqs_html}
            </div>
        </section>

        <!-- Cross-Navigation across Services & Cities -->
        <section class="studio-divider pt-5 border-t border-white/10 space-y-3">
            <div class="studio-muted text-xs font-mono text-white/60 uppercase">Diğer Uzmanlık Alanlarımız & Merkezlerimiz</div>
            <div class="flex flex-wrap gap-2">
                {sib_html}
                <a href="{prefix}index.html#magaza" class="studio-badge px-3.5 py-2 rounded-full bg-[#242428] border border-[#93F051]/35 text-[#93F051] text-xs font-medium hover:opacity-90 transition">DAT Donanım Mağazası</a>
            </div>
        </section>
    </main>

    <footer class="studio-footer bg-[#161618] border-t border-white/[0.08] py-8 px-4 text-center text-xs text-white/60 space-y-2">
        <div>&copy; 2005 – 2026 DAT ÖZEL DEDEKTİFLİK BÜROSU (DAT Group) • Ümit Hakan Karakaya • UÖDED Kurucu Üyesi</div>
        <div>İstanbul (Kartal) • Ankara (Çankaya) • Podgorica (Karadağ) • Las Vegas (ABD) • <a href="{prefix}index.html" class="studio-accent-text text-[#93F051] underline">Ana Sayfaya Dön</a></div>
    </footer>
    <script>
{SUBPAGE_THEME_SCRIPT}
    </script>
</body>
</html>'''

        out_path = os.path.join(ROOT, rel)
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(page_html)
        pages_meta.append(canonical)
    return pages_meta


def build_sitemap(founder_urls, seo_urls):
    def make_hreflang_block(suffix=""):
        return "\n".join(
            [f'    <xhtml:link rel="alternate" hreflang="{HTML_LANG_ATTR[c]}" href="{DOMAIN}/{"" if c == "tr" else c + "/"}{suffix}"/>' for c in ["tr"] + LANG_CODES]
            + [f'    <xhtml:link rel="alternate" hreflang="x-default" href="{DOMAIN}/{suffix}"/>']
        )

    entries = []
    # Root + 6 locale roots
    root_alt = make_hreflang_block("")
    for c in ["tr"] + LANG_CODES:
        loc = f"{DOMAIN}/" if c == "tr" else f"{DOMAIN}/{c}/"
        prio = "1.0" if c == "tr" else "0.9"
        entries.append(
            f'''  <url>
    <loc>{loc}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>{prio}</priority>
{root_alt}
  </url>'''
        )

    # Founder biography across all 7 languages
    founder_alt = make_hreflang_block("umit-hakan-karakaya.html")
    for idx, url in enumerate(founder_urls):
        prio = "0.85" if idx == 0 else "0.8"
        entries.append(
            f'''  <url>
    <loc>{url}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>{prio}</priority>
{founder_alt}
  </url>'''
        )

    for url in seo_urls:
        entries.append(
            f'''  <url>
    <loc>{url}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>'''
        )

    entries.append(
        f'''  <url>
    <loc>{DOMAIN}/elsa-vaka-paneli.html</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.85</priority>
  </url>'''
    )

    sitemap_xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
{chr(10).join(entries)}
</urlset>
'''
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap_xml)
    return len(entries)


FOUNDER_I18N = {
    "tr": {
        "dir": "ltr",
        "brand_sub": "Kurucu Profili & Basın Arşivi",
        "nav_press": "Basın & Ödüller",
        "nav_cta": "7/24 Danışmanlık Al",
        "home": "Ana Sayfa",
        "breadcrumb": "Ümit Hakan Karakaya Kimdir?",
        "portrait_alt": "Ümit Hakan Karakaya — DAT Özel Dedektiflik Kurucusu",
        "birth_lbl": "Ankara Doğum",
        "est_lbl": "DAT Kuruluş",
        "cases_val": "4.000+",
        "cases_lbl": "Yönetilen Vaka",
        "hero_badge": "KURUCU ÖZEL DEDEKTİF • ARAŞTIRMACI-YAZAR • STK BAŞKANI",
        "h1": "Ümit Hakan Karakaya Kimdir?",
        "hero_p": "1973 yılında Ankara'da doğan <strong>Ümit Hakan Karakaya</strong>, Türk Silahlı Kuvvetleri'nde <strong>F-16 uçak teknisyeni (Astsubay)</strong> olarak görev yaptıktan sonra askerî görevinden ayrılarak <strong>Uluslararası Hukuk</strong> lisans eğitimiyle saha tecrübesini hukuk disipliniyle birleştirmiştir. 2005 yılında temellerini attığı <strong>DAT Özel Dedektiflik Bürosu (DAT Group)</strong> ile bugüne kadar <strong>4.000'in üzerinde vakayı</strong> sonuçlandırmıştır.",
        "quote": "“Türk hukuk sisteminde en yetkili hâkimler aile mahkemesi hâkimleridir... ‘Gitsin dedektif araştırsın’ diyecek bu cesur hâkimi arıyorum.” — <span class=\"not-italic font-medium text-[#000000]\">ÜSTAD Avukatlık Meslek Dergisi Söyleşisi</span>",
        "btn_wa": "Doğrudan Büro İletişimi: 0532 666 77 49",
        "btn_home": "Ana Sayfaya Dön",
        "title": "Ümit Hakan Karakaya Kimdir? | Özgeçmiş, Kitaplar, Ödüller & DAT Özel Dedektiflik",
        "description": "1973 Ankara doğumlu Ümit Hakan Karakaya kimdir? Eski TSK F-16 uçak teknisyeni, Uluslararası Hukuk mezunu, DAT Özel Dedektiflik kurucusu, UÖDED & TÜDED Başkanı, WPYB lideri, The Detective's Eye yazarı ve Hayalime Renk Ver / UKAİM sosyal sorumluluk öncüsü.",
        "keywords": "ümit hakan karakaya, ümit hakan karakaya kimdir, dat dedektiflik kurucusu, uöded başkanı, tüded, wpyb global, the detectives eye, özel dedektif dergisi, hayalime renk ver, ukaim",
        "person_name": "Ümit Hakan Karakaya",
        "job_title": "Kurucu Özel Dedektif, Araştırmacı-Yazar, UÖDED & TÜDED Kurucu Başkanı",
        "birth_place": "Ankara, Türkiye",
        "nationality": "Turkish",
        "cards": [
            ("01 • ASKERÎ DİSİPLİN & HUKUK EĞİTİMİ", "TSK F-16 Geçmişi ve Hukuk Formasyonu", "Türk Silahlı Kuvvetleri'nde F-16 savaş uçakları teknisyeni (Astsubay) olarak edindiği yüksek hassasiyet ve operasyon disiplini, sivil araştırma kariyerinin temelini oluşturmuştur. Ardından <strong>Uluslararası Hukuk</strong> lisans eğitimini tamamlayan Karakaya; <strong>Türkiye Barolar Birliği Vakfı (TÜRAVAK)</strong> <em>Aile Hukuku İleri Eğitim Sertifikası</em> ve <strong>Kıbrıs İlim Üniversitesi (KİÜ)</strong> <em>Adli Bilimler, Olay Yeri İnceleme ve Özel Dedektiflik Sertifika Programı</em> ile delil toplama standartlarını hukuk çerçevesine oturtmuştur."),
            ("02 • DAT GROUP (2005 – BUGÜN)", "DAT Özel Dedektiflik ve Uluslararası Ofisler", "2005 yılında kurduğu <strong>DAT Özel Dedektiflik Bürosu</strong> çatısı altında eş takibi, evlilik öncesi araştırma, velayet ve boşanma davaları için yasal delil derleme, adres ve borçlu tespiti ile TSCM böcek tarama alanlarında Türkiye'nin 81 ilinde <strong>4.000+ dosya</strong> yönetmiştir. Kurumsal yapısını İstanbul (Kartal) ve Ankara (Çankaya) merkezlerinin yanı sıra <strong>Podgorica (Karadağ — WPYB Global)</strong> ve <strong>Las Vegas (ABD)</strong> ofisleriyle uluslararası ölçeğe taşımıştır."),
            ("03 • DERNEKÇİLİK & MARKA KORUMA", "TÜDED, UÖDED Başkanlıkları ve WPYB Global", "Türkiye'de özel dedektiflik mesleğinin yasal statü kazanması, meslek etiği kurallarının yerleşmesi ve kayıt dışı korsan yapılarla mücadele amacıyla <strong>Tüm Özel Dedektifler ve Araştırma Takip Uzmanları Derneği (TÜDED)</strong> ve <strong>Uluslararası Özel Dedektif Eğitimleri Derneği (UÖDED)</strong>'in kurucu başkanlığını üstlenmiş; <em>1. Uluslararası Özel Dedektifler Konferansı</em>'na öncülük etmiştir. Ayrıca sahte/taklit ürünlerle mücadele eden <strong>WPYB (We Protect Your Brand)</strong> ve <em>WPYB Akademi Marka Dedektifliği Eğitimi</em> organizasyonlarına liderlik etmektedir."),
            ("04 • YAYINLAR, KİTAP & ÖDÜLLER", "\"The Detective's Eye\", Dergiler ve Ulusal Basın", "Özel araştırma yöntemleri ve saha tecrübelerini aktardığı <strong><em>“The Detective’s Eye — In Search of Secrets and Traces”</em></strong> kitabının yazarıdır. Sektörel yayın <strong><em>Özel Dedektif Dergisi</em></strong>'nin imtiyaz sahipliği ve genel yayın yönetmenliğini yapmış; <em>ÜSTAD Avukatlık Meslek Dergisi</em>, <em>PI Magazin</em>, <em>Kanal 24</em>, <em>TV8</em>, <em>Dedektif Haber</em>, <em>Hürriyet</em> ve <em>Bolu Gündem</em> mecralarında yer almıştır. Ekonomize &amp; Ankara Sesi <em>Yılın En'leri</em> töreninde DAT Group adına <strong>\"Yılın Başarılı Araştırma Takip Firması\"</strong> ve <strong>Kristal Onur Ödülü</strong>'ne layık görülmüştür."),
        ],
        "social_badge": "05 • SOSYAL SORUMLULUK & ÇOCUK KORUMA ÇALIŞMALARI",
        "social_h2": "Hayalime Renk Ver Derneği (Oyuncak Kütüphanesi) & UKAİM",
        "social_p": "Mesleki çalışmalarının yanı sıra toplumsal fayda projeleriyle de kamuoyunda tanınan Ümit Hakan Karakaya; kızı Elif'in oyuncaklarıyla atılan adımlarla kurulan, geri dönüşüm bilinciyle dezavantajlı çocuklara ücretsiz oyuncak ulaştıran <strong>Hayalime Renk Ver Derneği</strong> ve <strong>Oyuncak Kütüphanesi</strong> projesinin kurucu yöneticileri arasında yer alarak sosyal sorumluluk ödülleri kazanmıştır. Ayrıca <strong>Uluslararası Kayıp Çocuk Araştırma ve İstismar Önleme Derneği (UKAİM)</strong> bünyesinde kayıp çocukların bulunması, istismarın önlenmesi ve afet dönemlerinde refakatsiz kalan çocukların güvenliğine yönelik kamuoyu bilgilendirmeleri yapmıştır.",
        "gallery_title": "Belge, Ödül Töreni & Basın Arşivi",
        "gallery_hint": "Büyütmek için tıklayın",
        "gallery": [
            ("assets/photos/wpyb-marka-dedektifligi-panel.jpg", "WPYB Akademi — Marka Dedektifliği Eğitimi & Taklit Ürünlerle Mücadele Paneli"),
            ("assets/photos/yilin-enleri-odul-1.jpg", "Yılın En'leri Ödül Töreni — DAT Group & Ümit Hakan Karakaya"),
            ("assets/photos/turavak-aile-hukuku-sertifika.jpg", "Türkiye Barolar Birliği Vakfı (TÜRAVAK) — Aile Hukuku İleri Eğitim Sertifikası"),
            ("assets/photos/uoded-imza-toreni.jpg", "UÖDED Kurucu Başkanı Ümit Hakan Karakaya — Sertifika & Çalıştay İmza Töreni"),
            ("assets/photos/ozel-dedektif-dergisi-kapak.jpg", "Özel Dedektif Dergisi 4. Sayı — Ümit Hakan Karakaya Kapak Röportajı"),
            ("assets/photos/ustad-dergi-roportaj.jpg", "ÜSTAD Avukatlık Meslek Dergisi — Kanuna Uygun Delil & Özel Dedektiflik Söyleşisi"),
            ("assets/photos/kiu-sertifika-programi.jpg", "Kıbrıs İlim Üniversitesi (KİÜ) Adli Bilimler ve Özel Dedektiflik Sertifika Programı"),
            ("assets/photos/zirve-odul-toreni-kristal.jpg", "Yılın En'leri Zirvesi — Kristal Onur Ödülü Takdim Töreni"),
        ],
        "faq_title": "Ümit Hakan Karakaya Hakkında Sıkça Sorulan Sorular",
        "faqs": [
            ("Ümit Hakan Karakaya kimdir?", "1973 Ankara doğumlu Türk özel dedektif, araştırmacı-yazar ve sivil toplum kuruluşu yöneticisidir. Türk Silahlı Kuvvetleri'nde F-16 uçak teknisyeni (Astsubay) olarak görev yaptıktan sonra Uluslararası Hukuk lisans eğitimi almış ve 2005 yılında DAT Özel Dedektiflik Bürosu'nu (DAT Group) kurmuştur."),
            ("Hangi mesleki dernek ve platformların kurucusu / başkanıdır?", "Türkiye'de özel dedektiflik mesleğinin yasal statü ve etik normlara kavuşması için Tüm Özel Dedektifler ve Araştırma Takip Uzmanları Derneği (TÜDED) ile Uluslararası Özel Dedektif Eğitimleri Derneği (UÖDED)'in kurucu başkanlığını üstlenmiş; ayrıca taklit ürün ve marka koruma alanında WPYB (We Protect Your Brand) yapılanmasına liderlik etmektedir."),
            ("Yayımladığı kitap ve medya çalışmaları nelerdir?", "Özel araştırmacılık ve saha dinamiklerini ele aldığı \"The Detective's Eye — In Search of Secrets and Traces\" kitabının yazarıdır. Özel Dedektif Dergisi'nin imtiyaz sahipliği ve genel yayın yönetmenliğini yürütmüş; Kanal 24, TV8, ÜSTAD Avukatlık Meslek Dergisi, PI Magazin, Dedektif Haber, Hürriyet ve Bolu Gündem gibi mecralarda açıklamaları yer almıştır."),
            ("Sosyal sorumluluk alanındaki çalışmaları nelerdir?", "Kızı Elif'ten ilhamla dezavantajlı çocuklara ücretsiz oyuncak desteği sunan Hayalime Renk Ver Derneği (Oyuncak Kütüphanesi) girişiminin kurucuları arasında yer almış, ayrıca Uluslararası Kayıp Çocuk Araştırma ve İstismar Önleme Derneği (UKAİM) bünyesinde çocuk güvenliği ve kayıp çocuk farkındalık çalışmaları yürütmüştür."),
        ],
        "cross_title": "Diğer Sayfalarımız & Hizmetlerimiz",
        "cross_links": [("index.html", "Ana Sayfa"), ("istanbul-ozel-dedektif.html", "İstanbul Büro"), ("ankara-ozel-dedektif.html", "Ankara Büro"), ("hizmetler/es-takibi.html", "Eş Takibi"), ("hizmetler/kurumsal-ve-marka-koruma.html", "Kurumsal & WPYB")],
        "cross_cta": "Ücretsiz Ön Görüşme",
        "footer_1": "&copy; 2005 – 2026 DAT ÖZEL DEDEKTİFLİK BÜROSU (DAT Group) • Ümit Hakan Karakaya • UÖDED Kurucu Başkanı",
        "footer_2": "İstanbul (Kartal) • Ankara (Çankaya) • Podgorica (Karadağ) • Las Vegas (ABD)",
    },
    "en": {
        "dir": "ltr",
        "brand_sub": "Founder Profile & Press Dossier",
        "nav_press": "Press & Awards",
        "nav_cta": "24/7 Consultation",
        "home": "Home",
        "breadcrumb": "Who Is Ümit Hakan Karakaya?",
        "portrait_alt": "Ümit Hakan Karakaya — Founder of DAT Private Detective Agency",
        "birth_lbl": "Born in Ankara",
        "est_lbl": "DAT Founded",
        "cases_val": "4,000+",
        "cases_lbl": "Cases Led",
        "hero_badge": "FOUNDING PRIVATE DETECTIVE • AUTHOR • ASSOCIATION PRESIDENT",
        "h1": "Who Is Ümit Hakan Karakaya?",
        "hero_p": "Born in Ankara in 1973, <strong>Ümit Hakan Karakaya</strong> served in the Turkish Armed Forces as an <strong>F-16 aircraft technician (NCO)</strong> before integrating operational military precision with an <strong>International Law</strong> bachelor's degree. In 2005, he founded <strong>DAT Private Detective Agency (DAT Group)</strong> and has overseen over <strong>4,000 cases</strong> nationwide and internationally.",
        "quote": "“Within the Turkish legal framework, family court judges hold broader authority than criminal courts... I am looking for that courageous judge ready to say: Let the private investigator uncover the facts.” — <span class=\"not-italic font-medium text-[#000000]\">ÜSTAD Bar Association Journal Interview</span>",
        "btn_wa": "Direct Bureau Line: +90 532 666 77 49",
        "btn_home": "Back to Homepage",
        "title": "Who Is Ümit Hakan Karakaya? | Biography, Book, Awards & DAT Detective",
        "description": "Official profile of Ümit Hakan Karakaya (born 1973, Ankara): former TSK F-16 aircraft technician, International Law graduate, founder of DAT Private Detective Agency, president of UÖDED & TÜDED, leader of WPYB Global, author of The Detective's Eye, and co-founder of Hayalime Renk Ver / UKAİM.",
        "keywords": "ümit hakan karakaya, who is umit hakan karakaya, dat detective founder, uöded, tüded, wpyb global, the detectives eye, hayalime renk ver, ukaim",
        "person_name": "Ümit Hakan Karakaya",
        "job_title": "Founding Private Detective, Author, Founding President of UÖDED & TÜDED",
        "birth_place": "Ankara, Turkey",
        "nationality": "Turkish",
        "cards": [
            ("01 • MILITARY PRECISION & LAW", "TSK F-16 Service & Legal Education", "Having served as an F-16 fighter aircraft technician (NCO) in the Turkish Armed Forces, Karakaya carried strict technical discipline and field vigilance into private investigation. After completing his degree in <strong>International Law</strong>, he reinforced lawful evidence standards through the <strong>Union of Turkish Bar Associations Foundation (TÜRAVAK)</strong> <em>Advanced Family Law Certificate</em> and the <strong>Cyprus Science University (KİÜ)</strong> <em>Forensic Sciences &amp; Private Investigation Program</em>."),
            ("02 • DAT GROUP (2005 – PRESENT)", "DAT Detective & International Bureaus", "Founded in 2005, <strong>DAT Private Detective Agency</strong> operates across all 81 provinces of Turkey with <strong>4,000+ closed cases</strong> in spouse surveillance, pre-marital verification, child custody &amp; divorce evidence, debtor/address tracing, and TSCM counter-surveillance sweeps. The agency expands internationally via offices in Istanbul (Kartal), Ankara (Çankaya), <strong>Podgorica (Montenegro — WPYB Global)</strong>, and <strong>Las Vegas (USA)</strong>."),
            ("03 • ASSOCIATIONS & BRAND PROTECTION", "TÜDED, UÖDED Presidencies & WPYB Global", "To formalize statutory regulation, ethical standards, and anti-fraud oversight in private investigation, Karakaya founded and chaired <strong>TÜDED</strong> (All Private Detectives Association) and <strong>UÖDED</strong> (International Private Detective Trainings Association), spearheading the <em>1st International Private Investigators Conference</em>. He also leads global anti-counterfeiting platform <strong>WPYB (We Protect Your Brand)</strong> and <em>WPYB Academy</em> brand investigator trainings."),
            ("04 • BOOK, PUBLICATIONS & AWARDS", "\"The Detective's Eye\", Press & National Honors", "He is the author of <strong><em>“The Detective’s Eye — In Search of Secrets and Traces”</em></strong> covering investigation methods and field realities. He served as publisher and editor-in-chief of <strong><em>Özel Dedektif Dergisi</em></strong>, and appeared across <em>ÜSTAD Law Journal</em>, <em>PI Magazine</em>, <em>Kanal 24</em>, <em>TV8</em>, <em>Dedektif Haber</em>, <em>Hürriyet</em>, and <em>Bolu Gündem</em>. DAT Group and Karakaya received the <strong>\"Successful Research &amp; Investigation Firm of the Year\"</strong> and <strong>Crystal Honor Award</strong> at the <em>Best of the Year</em> ceremony."),
        ],
        "social_badge": "05 • SOCIAL IMPACT & CHILD PROTECTION",
        "social_h2": "Hayalime Renk Ver Association (Toy Library) & UKAİM",
        "social_p": "Beyond investigation, Ümit Hakan Karakaya is recognized for civic initiatives: he is among the founding leaders of the <strong>Hayalime Renk Ver Association</strong> and its recycling-powered <strong>Toy Library</strong> inspired by his daughter Elif, providing free toys to disadvantaged children and earning multiple social responsibility awards. Through <strong>UKAİM</strong> (International Missing Children Research &amp; Abuse Prevention Association), he has also issued public child-safety guidance during disaster response efforts.",
        "gallery_title": "Verified Certificates, Awards & Press Archive",
        "gallery_hint": "Click any photo to enlarge",
        "gallery": [
            ("assets/photos/wpyb-marka-dedektifligi-panel.jpg", "WPYB Academy — Brand Detective Training & Anti-Counterfeiting Panel"),
            ("assets/photos/yilin-enleri-odul-1.jpg", "Best of the Year Awards Ceremony — DAT Group & Ümit Hakan Karakaya"),
            ("assets/photos/turavak-aile-hukuku-sertifika.jpg", "Turkish Bar Associations Foundation (TÜRAVAK) — Family Law Certificate"),
            ("assets/photos/uoded-imza-toreni.jpg", "UÖDED Founding President Ümit Hakan Karakaya — Certificate Signing Ceremony"),
            ("assets/photos/ozel-dedektif-dergisi-kapak.jpg", "Özel Dedektif Dergisi Issue #4 — Cover Interview with Ümit Hakan Karakaya"),
            ("assets/photos/ustad-dergi-roportaj.jpg", "ÜSTAD Bar Association Journal — Lawful Evidence Interview"),
            ("assets/photos/kiu-sertifika-programi.jpg", "Cyprus Science University (KİÜ) Forensic Science & Investigation Program"),
            ("assets/photos/zirve-odul-toreni-kristal.jpg", "Best of the Year Summit — Crystal Honor Award Presentation"),
        ],
        "faq_title": "Frequently Asked Questions About Ümit Hakan Karakaya",
        "faqs": [
            ("Who is Ümit Hakan Karakaya?", "Born in Ankara in 1973, he is a Turkish private investigator, author, and NGO leader. After serving in the Turkish Armed Forces as an F-16 aircraft technician (NCO), he completed an International Law degree and founded DAT Private Detective Agency (DAT Group) in 2005."),
            ("Which associations and platforms did he found?", "He founded and chaired TÜDED and UÖDED to establish statutory norms and training standards for private detectives in Turkey, and leads WPYB (We Protect Your Brand) for corporate anti-counterfeiting investigations."),
            ("What book and media appearances is he known for?", "He authored \"The Detective's Eye — In Search of Secrets and Traces\", published Özel Dedektif Dergisi, and has been featured in ÜSTAD Legal Journal, PI Magazine, Kanal 24, TV8, Dedektif Haber, Hürriyet, and Bolu Gündem."),
            ("What are his social responsibility projects?", "Inspired by his daughter Elif, he co-led the Hayalime Renk Ver Association and its free Toy Library for children, and participated in UKAİM initiatives focused on missing children and child protection."),
        ],
        "cross_title": "Related Bureau Pages & Services",
        "cross_links": [("index.html", "Homepage"), ("../istanbul-ozel-dedektif.html", "Istanbul Office (TR)"), ("../ankara-ozel-dedektif.html", "Ankara Office (TR)"), ("../hizmetler/es-takibi.html", "Spouse Surveillance (TR)"), ("../hizmetler/kurumsal-ve-marka-koruma.html", "Corporate & WPYB (TR)")],
        "cross_cta": "Free Consultation",
        "footer_1": "&copy; 2005 – 2026 DAT PRIVATE DETECTIVE AGENCY (DAT Group) • Ümit Hakan Karakaya • UÖDED Founder",
        "footer_2": "Istanbul (Kartal) • Ankara (Çankaya) • Podgorica (Montenegro) • Las Vegas (USA)",
    },
    "de": {
        "dir": "ltr",
        "brand_sub": "Gründerprofil & Pressearchiv",
        "nav_press": "Presse & Auszeichnungen",
        "nav_cta": "24/7 Beratung",
        "home": "Startseite",
        "breadcrumb": "Wer ist Ümit Hakan Karakaya?",
        "portrait_alt": "Ümit Hakan Karakaya — Gründer der DAT Privatdetektei",
        "birth_lbl": "Geb. in Ankara",
        "est_lbl": "DAT Gründung",
        "cases_val": "4.000+",
        "cases_lbl": "Geleitete Fälle",
        "hero_badge": "GRÜNDER & PRIVATDETEKTIV • AUTOR • VERBANDSPRÄSIDENT",
        "h1": "Wer ist Ümit Hakan Karakaya?",
        "hero_p": "Der 1973 in Ankara geborene <strong>Ümit Hakan Karakaya</strong> diente zunächst als <strong>F-16-Flugzeugtechniker (Unteroffizier)</strong> in den türkischen Streitkräften, bevor er diese Präzision mit einem Studium des <strong>Internationalen Rechts</strong> verband und 2005 die <strong>DAT Privatdetektei (DAT Group)</strong> gründete. Bis heute leitete er über <strong>4.000 nationale und internationale Fälle</strong>.",
        "quote": "„Im türkischen Rechtssystem besitzen Familiengerichte umfassendere Befugnisse als Strafgerichte... Ich suche jenen mutigen Richter, der sagt: Ein Detektiv soll ermitteln.“ — <span class=\"not-italic font-medium text-[#000000]\">ÜSTAD Anwaltsmagazin</span>",
        "btn_wa": "Direktkontakt Büro: +90 532 666 77 49",
        "btn_home": "Zur Startseite",
        "title": "Wer ist Ümit Hakan Karakaya? | Biografie, Buch, Preise & DAT Detektei",
        "description": "Offizielles Profil von Ümit Hakan Karakaya (geb. 1973, Ankara): Ex-F-16-Techniker, Abschluss in Internationalem Recht, Gründer der DAT Detektei, Präsident von UÖDED & TÜDED, Leiter von WPYB, Autor von The Detective's Eye sowie Hayalime Renk Ver / UKAİM.",
        "keywords": "ümit hakan karakaya, wer ist umit hakan karakaya, dat detektei gründer, uöded, tüded, wpyb global, the detectives eye, hayalime renk ver, ukaim",
        "person_name": "Ümit Hakan Karakaya",
        "job_title": "Gründer & Chefermittler, Autor, Präsident von UÖDED & TÜDED",
        "birth_place": "Ankara, Türkei",
        "nationality": "Turkish",
        "cards": [
            ("01 • MILITÄR & RECHTSBILDUNG", "F-16-Dienst & Rechtswissenschaft", "Als ehemaliger F-16-Kampfjet-Techniker (Unteroffizier) der türkischen Streitkräfte übertrug Karakaya höchste technische Präzision in die Ermittlungspraxis. Mit seinem Studium des <strong>Internationalen Rechts</strong>, dem <strong>TÜRAVAK</strong>-Zertifikat für Familienrecht sowie dem <strong>KİÜ</strong>-Zertifikatsprogramm für Forensik sichert er rechtskonforme Beweisführung."),
            ("02 • DAT GROUP (SEIT 2005)", "DAT Detektei & Internationale Büros", "Unter dem Dach der 2005 gegründeten <strong>DAT Privatdetektei</strong> betreute er über <strong>4.000 Fälle</strong> in allen 81 Provinzen der Türkei (Partnerobservation, Vorehe-Prüfung, Sorgerechtsbeweise, Adress-/Schuldnerermittlung, TSCM-Abhörschutz) mit Büros in Istanbul, Ankara, <strong>Podgorica (Montenegro — WPYB Global)</strong> und <strong>Las Vegas (USA)</strong>."),
            ("03 • VERBÄNDE & MARKENSCHUTZ", "TÜDED, UÖDED & WPYB Global", "Zur gesetzlichen Verankerung und Ethik-Normierung des Detektivberufs gründete er <strong>TÜDED</strong> und <strong>UÖDED</strong> und initiierte die <em>1. Internationale Detektivkonferenz</em>. Zudem leitet er die globale Anti-Produktpiraterie-Plattform <strong>WPYB (We Protect Your Brand)</strong> sowie die <em>WPYB Akademie</em>."),
            ("04 • BUCH, MEDIEN & PREISE", "„The Detective's Eye“, Fachpresse & Awards", "Autor des Fachbuchs <strong><em>„The Detective’s Eye — In Search of Secrets and Traces“</em></strong> sowie Herausgeber von <strong><em>Özel Dedektif Dergisi</em></strong>. Zahlreiche Beiträge in <em>ÜSTAD</em>, <em>PI Magazin</em>, <em>Kanal 24</em>, <em>TV8</em>, <em>Hürriyet</em> und <em>Bolu Gündem</em>; ausgezeichnet bei den <em>Best of the Year Awards</em> mit dem <strong>Kristall-Ehrenpreis</strong>."),
        ],
        "social_badge": "05 • SOZIALES ENGAGEMENT & KINDERSCHUTZ",
        "social_h2": "Hayalime Renk Ver (Spielzeugbibliothek) & UKAİM",
        "social_p": "Inspiriert durch seine Tochter Elif gehört Ümit Hakan Karakaya zu den Gründern des Vereins <strong>Hayalime Renk Ver</strong> und der kostenlosen <strong>Spielzeugbibliothek</strong> für benachteiligte Kinder (ausgezeichnet mit Sozialpreisen). Im Rahmen von <strong>UKAİM</strong> setzt er sich zudem für die Suche nach vermissten Kindern und den Schutz unbegleiteter Kinder in Krisenzeiten ein.",
        "gallery_title": "Zertifikate, Preise & Pressearchiv",
        "gallery_hint": "Zum Vergrößern anklicken",
        "gallery": [
            ("assets/photos/wpyb-marka-dedektifligi-panel.jpg", "WPYB Akademie — Markendetektiv-Schulung & Anti-Piraterie-Panel"),
            ("assets/photos/yilin-enleri-odul-1.jpg", "Best of the Year Preisverleihung — DAT Group & Ümit Hakan Karakaya"),
            ("assets/photos/turavak-aile-hukuku-sertifika.jpg", "Türkische Rechtsanwaltsstiftung (TÜRAVAK) — Familienrecht-Zertifikat"),
            ("assets/photos/uoded-imza-toreni.jpg", "UÖDED-Gründungspräsident Ümit Hakan Karakaya — Zertifikatsunterzeichnung"),
            ("assets/photos/ozel-dedektif-dergisi-kapak.jpg", "Özel Dedektif Dergisi Ausgabe 4 — Titelinterview Ümit Hakan Karakaya"),
            ("assets/photos/ustad-dergi-roportaj.jpg", "ÜSTAD Anwaltsfachmagazin — Interview zu legaler Beweiserhebung"),
            ("assets/photos/kiu-sertifika-programi.jpg", "Zypern Wissenschaftsuniversität (KİÜ) Forensik- & Detektivprogramm"),
            ("assets/photos/zirve-odul-toreni-kristal.jpg", "Best of the Year Gipfel — Überreichung des Kristall-Ehrenpreises"),
        ],
        "faq_title": "Häufige Fragen zu Ümit Hakan Karakaya",
        "faqs": [
            ("Wer ist Ümit Hakan Karakaya?", "Geboren 1973 in Ankara, ist er türkischer Privatdetektiv, Fachbuchautor und Verbandspräsident. Nach seiner Zeit als F-16-Techniker in den türkischen Streitkräften studierte er Internationales Recht und gründete 2005 die DAT Privatdetektei."),
            ("Welche Verbände und Plattformen leitet er?", "Er gründete TÜDED und UÖDED zur gesetzlichen Regulierung und Ausbildung im Detektivwesen und leitet die Markenschutz-Plattform WPYB (We Protect Your Brand)."),
            ("Welche Bücher und Medienauftritte gibt es?", "Er schrieb „The Detective's Eye — In Search of Secrets and Traces“, leitete Özel Dedektif Dergisi und trat bei Kanal 24, TV8, ÜSTAD, Hürriyet und Bolu Gündem auf."),
            ("Welche sozialen Projekte unterstützt er?", "Mit Hayalime Renk Ver (Spielzeugbibliothek) und UKAİM engagiert er sich nachhaltig für benachteiligte und vermisste Kinder."),
        ],
        "cross_title": "Weitere Seiten & Büros",
        "cross_links": [("index.html", "Startseite"), ("../istanbul-ozel-dedektif.html", "Büro Istanbul (TR)"), ("../ankara-ozel-dedektif.html", "Büro Ankara (TR)"), ("../hizmetler/es-takibi.html", "Partnerobservation (TR)"), ("../hizmetler/kurumsal-ve-marka-koruma.html", "Unternehmen & WPYB (TR)")],
        "cross_cta": "Kostenlose Erstberatung",
        "footer_1": "&copy; 2005 – 2026 DAT DETEKTEI (DAT Group) • Ümit Hakan Karakaya • UÖDED-Gründer",
        "footer_2": "Istanbul (Kartal) • Ankara (Çankaya) • Podgorica (Montenegro) • Las Vegas (USA)",
    },
    "fr": {
        "dir": "ltr",
        "brand_sub": "Profil du Fondateur & Dossier Presse",
        "nav_press": "Presse & Prix",
        "nav_cta": "Consultation 24h/24",
        "home": "Accueil",
        "breadcrumb": "Qui est Ümit Hakan Karakaya ?",
        "portrait_alt": "Ümit Hakan Karakaya — Fondateur de DAT Détective Privé",
        "birth_lbl": "Né à Ankara",
        "est_lbl": "Création DAT",
        "cases_val": "4 000+",
        "cases_lbl": "Dossiers dirigés",
        "hero_badge": "FONDATEUR DÉTECTIVE PRIVÉ • AUTEUR • PRÉSIDENT ASSOCIATIF",
        "h1": "Qui est Ümit Hakan Karakaya ?",
        "hero_p": "Né à Ankara en 1973, <strong>Ümit Hakan Karakaya</strong> a servi dans l'Armée de l'Air turque comme <strong>technicien sur avions de chasse F-16 (sous-officier)</strong> avant d'allier discipline opérationnelle et diplôme de <strong>Droit International</strong> pour fonder en 2005 le cabinet <strong>DAT Détective Privé (DAT Group)</strong>, avec plus de <strong>4 000 affaires résolues</strong>.",
        "quote": "« Dans le système juridique turc, les juges aux affaires familiales disposent d'une autorité encore plus vaste... Je cherche ce juge courageux qui dira : Que le détective enquête ! » — <span class=\"not-italic font-medium text-[#000000]\">Revue juridique ÜSTAD</span>",
        "btn_wa": "Ligne directe bureau : +90 532 666 77 49",
        "btn_home": "Retour à l'accueil",
        "title": "Qui est Ümit Hakan Karakaya ? | Biographie, Livre & DAT Détective",
        "description": "Biographie officielle d'Ümit Hakan Karakaya (né en 1973 à Ankara) : ancien technicien F-16, diplômé en droit international, fondateur de DAT Détective, président UÖDED & TÜDED, leader WPYB, auteur de The Detective's Eye et cofondateur Hayalime Renk Ver / UKAİM.",
        "keywords": "ümit hakan karakaya, biographie umit hakan karakaya, dat detective, uöded, tüded, wpyb, the detectives eye, hayalime renk ver, ukaim",
        "person_name": "Ümit Hakan Karakaya",
        "job_title": "Détective Privé Fondateur, Auteur, Président Fondateur UÖDED & TÜDED",
        "birth_place": "Ankara, Turquie",
        "nationality": "Turkish",
        "cards": [
            ("01 • RIGUEUR MILITAIRE & DROIT", "Parcours F-16 & Formation Juridique", "Ancien technicien aéronautique sur chasseurs F-16 au sein des Forces Armées Turques, Karakaya a transposé cette rigueur vers l'investigation légale. Diplômé en <strong>Droit International</strong>, il détient la certification avancée en droit de la famille de la Fondation du Barreau Turc (<strong>TÜRAVAK</strong>) et le certificat en sciences forensiques de l'Université <strong>KİÜ</strong>."),
            ("02 • DAT GROUP (DEPUIS 2005)", "DAT Détective & Bureaux Internationaux", "Fondé en 2005, <strong>DAT Détective Privé</strong> a résolu plus de <strong>4 000 dossiers</strong> dans les 81 provinces de Turquie (filature conjugale, enquêtes prénuptiales, garde d'enfants, recherche de débiteurs et dépistage TSCM), via ses bureaux d'Istanbul, Ankara, <strong>Podgorica (Monténégro — WPYB Global)</strong> et <strong>Las Vegas (États-Unis)</strong>."),
            ("03 • ASSOCIATIONS & ANTI-CONTREFAÇON", "Présidences TÜDED, UÖDED & WPYB Global", "Engagé pour doter la profession d'un statut légal et d'une déontologie stricte, il a fondé et présidé <strong>TÜDED</strong> et <strong>UÖDED</strong> et lancé la <em>1re Conférence Internationale des Détectives Privés</em>. Il dirige également la plateforme mondiale de protection des marques <strong>WPYB (We Protect Your Brand)</strong> et l'académie <em>WPYB Academy</em>."),
            ("04 • LIVRE, REVUES & DISTINCTIONS", "« The Detective's Eye », Presse & Prix", "Auteur de l'ouvrage <strong><em>« The Detective’s Eye — In Search of Secrets and Traces »</em></strong> et rédacteur en chef de la revue <strong><em>Özel Dedektif Dergisi</em></strong>. Ses analyses ont été relayées sur <em>ÜSTAD</em>, <em>PI Magazin</em>, <em>Kanal 24</em>, <em>TV8</em>, <em>Hürriyet</em> et <em>Bolu Gündem</em>, récompensées par le titre de <strong>Meilleure Entreprise de l'Année</strong> et le <strong>Prix d'Honneur Cristal</strong>."),
        ],
        "social_badge": "05 • ENGAGEMENT SOCIAL & PROTECTION DE L'ENFANCE",
        "social_h2": "Association Hayalime Renk Ver (Ludothèque) & UKAİM",
        "social_p": "Inspiré par sa fille Elif, Ümit Hakan Karakaya figure parmi les fondateurs de l'association <strong>Hayalime Renk Ver</strong> et de sa <strong>Ludothèque solidaire gratuite</strong> dédiée aux enfants défavorisés (primée pour son impact social). Au sein d'<strong>UKAİM</strong>, il participe également à la sensibilisation et à la protection des enfants disparus ou isolés lors de crises.",
        "gallery_title": "Archives Presse, Certificats & Remises de Prix",
        "gallery_hint": "Cliquez pour agrandir",
        "gallery": [
            ("assets/photos/wpyb-marka-dedektifligi-panel.jpg", "WPYB Academy — Formation Détective des Marques & Lutte Anti-Contrefaçon"),
            ("assets/photos/yilin-enleri-odul-1.jpg", "Cérémonie Best of the Year — DAT Group & Ümit Hakan Karakaya"),
            ("assets/photos/turavak-aile-hukuku-sertifika.jpg", "Fondation du Barreau de Turquie (TÜRAVAK) — Certificat Droit de la Famille"),
            ("assets/photos/uoded-imza-toreni.jpg", "Président fondateur UÖDED Ümit Hakan Karakaya — Remise de certificats"),
            ("assets/photos/ozel-dedektif-dergisi-kapak.jpg", "Özel Dedektif Dergisi N° 4 — Interview de couverture"),
            ("assets/photos/ustad-dergi-roportaj.jpg", "Revue juridique ÜSTAD — Entretien sur la preuve licite"),
            ("assets/photos/kiu-sertifika-programi.jpg", "Université des Sciences de Chypre (KİÜ) — Sciences Forensiques"),
            ("assets/photos/zirve-odul-toreni-kristal.jpg", "Sommet de l'Année — Remise du Prix d'Honneur Cristal"),
        ],
        "faq_title": "Questions Fréquentes sur Ümit Hakan Karakaya",
        "faqs": [
            ("Qui est Ümit Hakan Karakaya ?", "Né en 1973 à Ankara, détective privé turc, auteur et président associatif. Ancien technicien F-16 dans l'Armée de l'Air turque, diplômé en Droit International, il a fondé DAT Détective Privé en 2005."),
            ("Quelles associations et plateformes dirige-t-il ?", "Il a fondé et présidé TÜDED et UÖDED pour la réglementation et la formation professionnelle des détectives, et dirige la plateforme anti-contrefaçon WPYB."),
            ("Quelles sont ses publications et apparitions médiatiques ?", "Il est l'auteur de « The Detective's Eye — In Search of Secrets and Traces », directeur d'Özel Dedektif Dergisi et invité sur Kanal 24, TV8, ÜSTAD, Hürriyet et Bolu Gündem."),
            ("Quels projets sociaux mène-t-il ?", "Avec Hayalime Renk Ver (Ludothèque solidaire) et UKAİM, il agit pour les droits et la sécurité des enfants."),
        ],
        "cross_title": "Autres Pages & Services",
        "cross_links": [("index.html", "Accueil"), ("../istanbul-ozel-dedektif.html", "Bureau Istanbul (TR)"), ("../ankara-ozel-dedektif.html", "Bureau Ankara (TR)"), ("../hizmetler/es-takibi.html", "Filature Conjugale (TR)"), ("../hizmetler/kurumsal-ve-marka-koruma.html", "Entreprises & WPYB (TR)")],
        "cross_cta": "Consultation Gratuite",
        "footer_1": "&copy; 2005 – 2026 DAT DÉTECTIVE (DAT Group) • Ümit Hakan Karakaya • Fondateur UÖDED",
        "footer_2": "Istanbul (Kartal) • Ankara (Çankaya) • Podgorica (Monténégro) • Las Vegas (USA)",
    },
    "ar": {
        "dir": "rtl",
        "brand_sub": "ملف المؤسس والأرشيف الإعلامي",
        "nav_press": "الصحافة والجوائز",
        "nav_cta": "استشارة 24/7",
        "home": "الرئيسية",
        "breadcrumb": "من هو أوميت هاكان قرة قايا؟",
        "portrait_alt": "أوميت هاكان قرة قايا — مؤسس مكتب DAT للتحريات الخاصة",
        "birth_lbl": "مواليد أنقرة",
        "est_lbl": "تأسيس DAT",
        "cases_val": "+4,000",
        "cases_lbl": "قضية مُدارة",
        "hero_badge": "محقق خاص ومؤسس • باحث ومؤلف • رئيس جمعيات مهنية",
        "h1": "من هو أوميت هاكان قرة قايا؟",
        "hero_p": "وُلد <strong>أوميت هاكان قرة قايا</strong> في أنقرة عام 1973، وخدم في القوات المسلحة التركية بصفته <strong>فني مقاتلات F-16 (ضابط صف)</strong> قبل أن يجمع بين الانضباط العسكري وشهادة البكالوريوس في <strong>القانون الدولي</strong> ليؤسس عام 2005 مكتب <strong>DAT للتحريات الخاصة (DAT Group)</strong>، ويدير حتى اليوم أكثر من <strong>4,000 قضية</strong> داخل تركيا وخارجها.",
        "quote": "«في النظام القضائي التركي يمتلك قضاة محاكم الأسرة صلاحيات واسعة تفوق غيرهم... وأنا أبحث عن ذلك القاضي الشجاع الذي يقول: ليتولَّ المحقق الخاص تقصي الحقائق». — <span class=\"not-italic font-medium text-[#000000]\">حوار مجلة ÜSTAD للمحاماة</span>",
        "btn_wa": "اتصال المكتب المباشر: +90 532 666 77 49",
        "btn_home": "العودة للرئيسية",
        "title": "من هو أوميت هاكان قرة قايا؟ | السيرة الذاتية، الكتاب، الجوائز ومكتب DAT",
        "description": "السيرة الرسمية لأوميت هاكان قرة قايا (مواليد أنقرة 1973): فني طائرات F-16 سابق، خريج القانون الدولي، مؤسس مكتب DAT للتحريات الخاصة، رئيس UÖDED وTÜDED، قائد منصة WPYB، ومؤلف كتاب The Detective's Eye.",
        "keywords": "أوميت هاكان قرة قايا, من هو أوميت هاكان قرة قايا, مكتب DAT للتحريات, UÖDED, TÜDED, WPYB, The Detectives Eye, Hayalime Renk Ver, UKAİM",
        "person_name": "Ümit Hakan Karakaya (أوميت هاكان قرة قايا)",
        "job_title": "مؤسس مكتب تحريات خاصة، مؤلف وباحث، رئيس جمعيتي UÖDED وTÜDED",
        "birth_place": "أنقرة، تركيا",
        "nationality": "Turkish",
        "cards": [
            ("01 • الانضباط العسكري والقانون", "خدمة F-16 في القوات المسلحة والتأهيل القانوني", "شكّلت خدمته العسكرية كفني مقاتلات F-16 (ضابط صف) أساس الدقة الميدانية والالتزام الإجرائي في مسيرته المدنية. وبعد حصوله على بكالوريوس <strong>القانون الدولي</strong>، عزز معايير الأدلة القانونية عبر شهادة <strong>مؤسسة نقابات المحامين التركية (TÜRAVAK)</strong> المتقدمة في قانون الأسرة وبرنامج العلوم الجنائية بجامعة <strong>KİÜ</strong>."),
            ("02 • مجموعة DAT (منذ 2005)", "مكتب DAT للتحريات والفروع الدولية", "أشرف عبر مكتب <strong>DAT للتحريات الخاصة</strong> الذي أسسه عام 2005 على أكثر من <strong>4,000 قضية</strong> في 81 ولاية تركية بمجالات مراقبة الزوج/الزوجة، تحريات ما قبل الزواج، أدلة الحضانة والطلاق، تتبع المدينين والعناوين، وكشف التنصت TSCM عبر مقراته في إسطنبول وأنقرة و<strong>بودغوريتسا (WPYB Global)</strong> و<strong>لاس فيغاس (الولايات المتحدة)</strong>."),
            ("03 • الجمعيات وحماية العلامات", "رئاسة TÜDED وUÖDED ومنصة WPYB", "سعياً لتقنين مهنة التحريات الخاصة وترسيخ أخلاقياتها ومواجهة الكيانات غير المرخصة، أسس وترأس جمعيتي <strong>TÜDED</strong> و<strong>UÖDED</strong> وقاد المؤتمر الدولي الأول للمحققين الخاصين. كما يتولى قيادة منصة مكافحة التزييف وحماية العلامات التجارية <strong>WPYB (We Protect Your Brand)</strong> وأكاديميتها التدريبية."),
            ("04 • الكتاب والصحافة والجوائز", "كتاب «عين المحقق»، المجلات والتكريمات", "مؤلف كتاب <strong><em>«The Detective’s Eye — In Search of Secrets and Traces»</em></strong> وصاحب امتياز ورئيس تحرير مجلة <strong><em>Özel Dedektif Dergisi</em></strong>. نُشرت حواراته في مجلة <em>ÜSTAD</em> و<em>PI Magazin</em> وقناتي <em>Kanal 24</em> و<em>TV8</em> وصحيفة <em>Hürriyet</em>؛ ونال جائزة <strong>«أفضل شركة أبحاث ومراقبة للعام»</strong> و<strong>درع التكريم الكريستالي</strong>."),
        ],
        "social_badge": "05 • المسؤولية الاجتماعية وحماية الطفولة",
        "social_h2": "جمعية Hayalime Renk Ver (مكتبة الألعاب) ومنظمة UKAİM",
        "social_p": "إلى جانب عمله المهني، يشارك أوميت هاكان قرة قايا في مبادرات مجتمعية بارزة؛ فهو من مؤسسي جمعية <strong>Hayalime Renk Ver</strong> ومشروع <strong>مكتبة الألعاب المجانية</strong> المستلهم من ابنته إيليف لدعم الأطفال المحتاجين. كما شارك ضمن جمعية <strong>UKAİM</strong> في التوعية بالبحث عن الأطفال المفقودين وحماية الأطفال غير المصحوبين خلال الكوارث.",
        "gallery_title": "أرشيف الشهادات والجوائز والتغطيات الصحفية",
        "gallery_hint": "اضغط للتكبير",
        "gallery": [
            ("assets/photos/wpyb-marka-dedektifligi-panel.jpg", "أكاديمية WPYB — ندوة تدريبية حول محققي العلامات التجارية ومكافحة التزييف"),
            ("assets/photos/yilin-enleri-odul-1.jpg", "حفل جوائز الأفضل للعام — مجموعة DAT وأوميت هاكان قرة قايا"),
            ("assets/photos/turavak-aile-hukuku-sertifika.jpg", "مؤسسة نقابات المحامين (TÜRAVAK) — شهادة قانون الأسرة المتقدمة"),
            ("assets/photos/uoded-imza-toreni.jpg", "مراسم توقيع الشهادات وورشة العمل برئاسة أوميت هاكان قرة قايا"),
            ("assets/photos/ozel-dedektif-dergisi-kapak.jpg", "مجلة المحقق الخاص العدد الرابع — حوار الغلاف مع أوميت هاكان قرة قايا"),
            ("assets/photos/ustad-dergi-roportaj.jpg", "حوار مجلة المحاماة ÜSTAD حول الأدلة المشروعة"),
            ("assets/photos/kiu-sertifika-programi.jpg", "برنامج جامعة قبرص للعلوم (KİÜ) في العلوم الجنائية والتحري"),
            ("assets/photos/zirve-odul-toreni-kristal.jpg", "قمة الأفضل للعام — تسلم درع التكريم الكريستالي"),
        ],
        "faq_title": "الأسئلة الشائعة حول أوميت هاكان قرة قايا",
        "faqs": [
            ("من هو أوميت هاكان قرة قايا؟", "محقق خاص تركي وباحث ومؤلف من مواليد أنقرة عام 1973. عمل فني طائرات F-16 في القوات المسلحة التركية، وحصل على شهادة القانون الدولي، وأسس مكتب DAT للتحريات الخاصة عام 2005."),
            ("ما الجمعيات والمنصات التي يرأسها أو أسسها؟", "أسس وترأس جمعيتي TÜDED وUÖDED لتنظيم مهنة التحريات وتدريب كوادرها، كما يقود منصة WPYB لحماية العلامات التجارية ومكافحة المنتجات المقلدة."),
            ("ما أبرز إصداراته وظهوره الإعلامي؟", "ألف كتاب «The Detective's Eye — In Search of Secrets and Traces»، وتولى رئاسة تحرير مجلة Özel Dedektif Dergisi، وظهر في ÜSTAD وKanal 24 وTV8 وHürriyet."),
            ("ما مبادراته في المسؤولية الاجتماعية؟", "ساهم في تأسيس جمعية Hayalime Renk Ver ومكتبة الألعاب للأطفال، كما شارك في جهود جمعية UKAİM لحماية الأطفال والبحث عن المفقودين."),
        ],
        "cross_title": "روابط وصفحات أخرى",
        "cross_links": [("index.html", "الصفحة الرئيسية"), ("../istanbul-ozel-dedektif.html", "فرع إسطنبول (TR)"), ("../ankara-ozel-dedektif.html", "فرع أنقرة (TR)"), ("../hizmetler/es-takibi.html", "مراقبة الشريك (TR)"), ("../hizmetler/kurumsal-ve-marka-koruma.html", "حماية الشركات WPYB (TR)")],
        "cross_cta": "استشارة مجانية",
        "footer_1": "&copy; 2005 – 2026 مكتب DAT للتحريات الخاصة (DAT Group) • أوميت هاكان قرة قايا • مؤسس UÖDED",
        "footer_2": "إسطنبول (كارتال) • أنقرة (جانكايا) • بودغوريتسا (الجبل الأسود) • لاس فيغاس (الولايات المتحدة)",
    },
    "ru": {
        "dir": "ltr",
        "brand_sub": "Профиль основателя и пресс-архив",
        "nav_press": "Пресса и награды",
        "nav_cta": "Консультация 24/7",
        "home": "Главная",
        "breadcrumb": "Кто такой Юмит Хакан Каракая?",
        "portrait_alt": "Юмит Хакан Каракая — основатель агентства DAT Детектив",
        "birth_lbl": "Род. в Анкаре",
        "est_lbl": "Основание DAT",
        "cases_val": "4 000+",
        "cases_lbl": "Проведённых дел",
        "hero_badge": "ОСНОВАТЕЛЬ И ЧАСТНЫЙ ДЕТЕКТИВ • АВТОР • ГЛАВА АССОЦИАЦИЙ",
        "h1": "Кто такой Юмит Хакан Каракая?",
        "hero_p": "Родившийся в Анкаре в 1973 году <strong>Юмит Хакан Каракая</strong> служил в Вооружённых силах Турции <strong>авиатехником истребителей F-16 (унтер-офицер)</strong>, после чего объединил армейскую дисциплину с дипломом в области <strong>международного права</strong>. В 2005 году он основал агентство <strong>DAT Детектив (DAT Group)</strong> и возглавил свыше <strong>4 000 расследований</strong>.",
        "quote": "«В турецкой судебной системе судьи по семейным делам обладают широчайшими полномочиями... Я ищу того смелого судью, который скажет: Пусть факты проверит частный детектив». — <span class=\"not-italic font-medium text-[#000000]\">Интервью журналу адвокатуры ÜSTAD</span>",
        "btn_wa": "Прямая линия офиса: +90 532 666 77 49",
        "btn_home": "На главную",
        "title": "Кто такой Юмит Хакан Каракая? | Биография, книга, награды и DAT Детектив",
        "description": "Официальная биография Юмита Хакана Каракая (род. 1973, Анкара): бывший техник F-16 ВВС Турции, диплом международного права, основатель DAT Детектив, президент UÖDED и TÜDED, лидер WPYB, автор книги The Detective's Eye и сооснователь Hayalime Renk Ver / UKAİM.",
        "keywords": "юмит хакан каракая, кто такой юмит хакан каракая, dat детектив, uöded, tüded, wpyb global, the detectives eye, hayalime renk ver, ukaim",
        "person_name": "Ümit Hakan Karakaya (Юмит Хакан Каракая)",
        "job_title": "Основатель и частный детектив, автор, президент UÖDED и TÜDED",
        "birth_place": "Анкара, Турция",
        "nationality": "Turkish",
        "cards": [
            ("01 • ВОЕННАЯ ШКОЛА И ПРАВО", "Служба F-16 и юридическая подготовка", "Служба техником боевых самолётов F-16 в ВВС Турции сформировала высокий стандарт оперативной дисциплины. Окончив факультет <strong>международного права</strong>, Каракая закрепил стандарты допустимости доказательств сертификатами <strong>TÜRAVAK</strong> (Фонд коллегии адвокатов Турции) по семейному праву и программой криминалистики <strong>KİÜ</strong>."),
            ("02 • DAT GROUP (С 2005 ГОДА)", "Агентство DAT Детектив и международные офисы", "Основанное в 2005 году агентство <strong>DAT</strong> закрыло свыше <strong>4 000 дел</strong> во всех 81 провинции Турции — от семейных проверок и сбора доказательств для суда до розыска адресов/должников и поиска жучков (TSCM). Сеть охватывает Стамбул, Анкару, <strong>Подгорицу (Черногория — WPYB Global)</strong> и <strong>Лас-Вегас (США)</strong>."),
            ("03 • АССОЦИАЦИИ И ЗАЩИТА БРЕНДОВ", "Президентство в TÜDED, UÖDED и WPYB Global", "Добиваясь законодательного статуса и этических норм детективной деятельности, он основал и возглавил <strong>TÜDED</strong> и <strong>UÖDED</strong>, проведя <em>1-ю Международную конференцию частных детективов</em>. Также руководит платформой защиты брендов от контрафакта <strong>WPYB (We Protect Your Brand)</strong> и академией <em>WPYB</em>."),
            ("04 • КНИГА, ПУБЛИКАЦИИ И НАГРАДЫ", "«The Detective's Eye», журналы и пресса", "Автор международной книги <strong><em>«The Detective’s Eye — In Search of Secrets and Traces»</em></strong> и главный редактор журнала <strong><em>Özel Dedektif Dergisi</em></strong>. Экспертные интервью выходили в <em>ÜSTAD</em>, <em>PI Magazin</em>, <em>Kanal 24</em>, <em>TV8</em>, <em>Hürriyet</em> и <em>Bolu Gündem</em>. Награждён премией <strong>«Лучшая исследовательская компания года»</strong> и <strong>Хрустальным орденом почёта</strong>."),
        ],
        "social_badge": "05 • СОЦИАЛЬНЫЕ ИНИЦИАТИВЫ И ЗАЩИТА ДЕТЕЙ",
        "social_h2": "Ассоциация Hayalime Renk Ver (Библиотека игрушек) и UKAİM",
        "social_p": "Вдохновившись примером дочери Элиф, Юмит Хакан Каракая стал сооснователем организации <strong>Hayalime Renk Ver</strong> и бесплатной <strong>Библиотеки игрушек</strong> для нуждающихся детей (отмеченной социальными премиями). Также в составе <strong>UKAİM</strong> он выступает за поиск пропавших детей и защиту несовершеннолетних в период стихийных бедствий.",
        "gallery_title": "Архив сертификатов, наград и публикаций в прессе",
        "gallery_hint": "Нажмите для увеличения",
        "gallery": [
            ("assets/photos/wpyb-marka-dedektifligi-panel.jpg", "Академия WPYB — Панель по защите брендов и борьбе с контрафактом"),
            ("assets/photos/yilin-enleri-odul-1.jpg", "Церемония Best of the Year — DAT Group и Юмит Хакан Каракая"),
            ("assets/photos/turavak-aile-hukuku-sertifika.jpg", "Фонд коллегии адвокатов Турции (TÜRAVAK) — Сертификат по семейному праву"),
            ("assets/photos/uoded-imza-toreni.jpg", "Глава UÖDED Юмит Хакан Каракая — Церемония подписания сертификатов"),
            ("assets/photos/ozel-dedektif-dergisi-kapak.jpg", "Özel Dedektif Dergisi №4 — Обложка и интервью с Юмитом Хаканом Каракая"),
            ("assets/photos/ustad-dergi-roportaj.jpg", "Юридический журнал ÜSTAD — Интервью о законных доказательствах"),
            ("assets/photos/kiu-sertifika-programi.jpg", "Университет наук Кипра (KİÜ) — Программа криминалистики"),
            ("assets/photos/zirve-odul-toreni-kristal.jpg", "Саммит Best of the Year — Вручение Хрустальной награды"),
        ],
        "faq_title": "Частые вопросы о Юмите Хакане Каракая",
        "faqs": [
            ("Кто такой Юмит Хакан Каракая?", "Турецкий частный детектив, автор и общественный деятель (род. 1973 в Анкаре). Бывший техник истребителей F-16 в ВВС Турции, выпускник факультета международного права и основатель агентства DAT (2005)."),
            ("Какие организации и платформы он возглавляет?", "Он основал и возглавил профессиональные ассоциации TÜDED и UÖDED, а также руководит платформой защиты брендов WPYB (We Protect Your Brand)."),
            ("Какие книги и публикации у него выходили?", "Автор книги «The Detective's Eye — In Search of Secrets and Traces», издатель Özel Dedektif Dergisi; выступал на Kanal 24, TV8, в журнале ÜSTAD, Hürriyet и Bolu Gündem."),
            ("Какими социальными проектами он занимается?", "Он участвовал в создании бесплатной Библиотеки игрушек Hayalime Renk Ver для детей и инициативах UKAİM по защите несовершеннолетних."),
        ],
        "cross_title": "Другие разделы и услуги",
        "cross_links": [("index.html", "Главная"), ("../istanbul-ozel-dedektif.html", "Офис Стамбул (TR)"), ("../ankara-ozel-dedektif.html", "Офис Анкара (TR)"), ("../hizmetler/es-takibi.html", "Семейный контроль (TR)"), ("../hizmetler/kurumsal-ve-marka-koruma.html", "Бизнес и WPYB (TR)")],
        "cross_cta": "Бесплатная консультация",
        "footer_1": "&copy; 2005 – 2026 DAT ДЕТЕКТИВ (DAT Group) • Юмит Хакан Каракая • Основатель UÖDED",
        "footer_2": "Стамбул (Картал) • Анкара (Чанкая) • Подгорица (Черногория) • Лас-Вегас (США)",
    },
    "me": {
        "dir": "ltr",
        "brand_sub": "Profil osnivača i press arhiva",
        "nav_press": "Štampa i nagrade",
        "nav_cta": "Konsultacije 24/7",
        "home": "Početna",
        "breadcrumb": "Ko je Ümit Hakan Karakaya?",
        "portrait_alt": "Ümit Hakan Karakaya — Osnivač agencije DAT Detektiv",
        "birth_lbl": "Rođen u Ankari",
        "est_lbl": "Osnivanje DAT",
        "cases_val": "4.000+",
        "cases_lbl": "Vođenih predmeta",
        "hero_badge": "OSNIVAČ I PRIVATNI DETEKTIV • AUTOR • PREDSJEDNIK UDRUŽENJA",
        "h1": "Ko je Ümit Hakan Karakaya?",
        "hero_p": "Rođen 1973. u Ankari, <strong>Ümit Hakan Karakaya</strong> služio je u Oružanim snagama Turske kao <strong>tehničar borbenih aviona F-16 (podoficir)</strong>, a potom je vojnu disciplinu povezao sa diplomom <strong>Međunarodnog prava</strong> i 2005. godine osnovao agenciju <strong>DAT Detektiv (DAT Group)</strong>, sa preko <strong>4.000 uspješno riješenih slučajeva</strong>.",
        "quote": "„U pravnom sistemu Turske sudije porodičnog suda imaju najšira ovlašćenja... Tražim tog hrabrog sudiju koji će reći: Neka privatni detektiv istraži činjenice.“ — <span class=\"not-italic font-medium text-[#000000]\">Intervju za advokatski časopis ÜSTAD</span>",
        "btn_wa": "Direktna linija biroa: +90 532 666 77 49",
        "btn_home": "Nazad na početnu",
        "title": "Ko je Ümit Hakan Karakaya? | Biografija, knjiga, nagrade i DAT Detektiv",
        "description": "Zvanični profil Ümit Hakan Karakaya (rođen 1973, Ankara): bivši F-16 tehničar, diplomirani pravnik međunarodnog prava, osnivač agencije DAT Detektiv, predsjednik UÖDED & TÜDED, lider WPYB Global, autor knjige The Detective's Eye i suosnivač Hayalime Renk Ver / UKAİM.",
        "keywords": "ümit hakan karakaya, ko je umit hakan karakaya, dat detektiv, uöded, tüded, wpyb global, the detectives eye, hayalime renk ver, ukaim",
        "person_name": "Ümit Hakan Karakaya",
        "job_title": "Osnivač i privatni detektiv, autor, predsjednik UÖDED i TÜDED",
        "birth_place": "Ankara, Turska",
        "nationality": "Turkish",
        "cards": [
            ("01 • VOJNA DISCIPLINA I PRAVO", "Služba na F-16 i pravno obrazovanje", "Iskustvo tehničara borbenih aviona F-16 u turskim oružanim snagama dalo mu je izuzetnu operativnu preciznost. Nakon studija <strong>Međunarodnog prava</strong>, usavršio je standarde zakonitog prikupljanja dokaza kroz sertifikat <strong>TÜRAVAK</strong> za porodično pravo i program forenzičkih nauka na Univerzitetu <strong>KİÜ</strong>."),
            ("02 • DAT GROUP (OD 2005.)", "DAT Detektiv i međunarodne kancelarije", "Pod okriljem agencije <strong>DAT Detektiv</strong>, osnovane 2005. godine, vodio je više od <strong>4.000 predmeta</strong> (provjera bračne vjernosti, predbračne istrage, dokazi za starateljstvo i razvod, traganje za dužnicima, TSCM zaštita) putem centara u Istanbulu, Ankari, <strong>Podgorici (Crna Gora — WPYB Global)</strong> i <strong>Las Vegasu (SAD)</strong>."),
            ("03 • UDRUŽENJA I ZAŠTITA BRENDOVA", "Predsjedavanje TÜDED-om, UÖDED-om i WPYB Global", "U cilju zakonskog uređenja i etičkih standarda detektivske struke osnovao je i vodio <strong>TÜDED</strong> i <strong>UÖDED</strong> te pokrenuo <em>1. Međunarodnu konferenciju privatnih detektiva</em>. Takođe vodi platformu za zaštitu brendova od falsifikata <strong>WPYB (We Protect Your Brand)</strong> i <em>WPYB Akademiju</em>."),
            ("04 • KNJIGA, ČASOPISI I NAGRADE", "„The Detective's Eye“, mediji i priznanja", "Autor je knjige <strong><em>„The Detective’s Eye — In Search of Secrets and Traces“</em></strong> i glavni urednik časopisa <strong><em>Özel Dedektif Dergisi</em></strong>. Objavljivan je u <em>ÜSTAD</em>, <em>PI Magazin</em>, na TV <em>Kanal 24</em>, <em>TV8</em>, u <em>Hürriyet</em> i <em>Bolu Gündem</em>; dobitnik je nagrade <strong>„Najuspješnija istraživačka firma godine“</strong> i <strong>Kristalne nagrade časti</strong>."),
        ],
        "social_badge": "05 • DRUŠTVENA ODGOVORNOST I ZAŠTITA DJECE",
        "social_h2": "Udruženje Hayalime Renk Ver (Biblioteka igračaka) i UKAİM",
        "social_p": "Inspirisan svojom kćerkom Elif, Ümit Hakan Karakaya je među osnivačima humanitarnog udruženja <strong>Hayalime Renk Ver</strong> i besplatne <strong>Biblioteke igračaka</strong> za djecu u potrebi (nagrađene društvenim priznanjima). Kroz <strong>UKAİM</strong> aktivno doprinosi podizanju svijesti o potrazi za nestalom djecom i njihovoj bezbjednosti u kriznim situacijama.",
        "gallery_title": "Arhiva sertifikata, nagrada i medijskih nastupa",
        "gallery_hint": "Kliknite za uvećanje",
        "gallery": [
            ("assets/photos/wpyb-marka-dedektifligi-panel.jpg", "WPYB Akademija — Obuka detektiva za brendove i borba protiv falsifikata"),
            ("assets/photos/yilin-enleri-odul-1.jpg", "Svečanost Najbolji u godini — DAT Group & Ümit Hakan Karakaya"),
            ("assets/photos/turavak-aile-hukuku-sertifika.jpg", "Fondacija advokatske komore (TÜRAVAK) — Sertifikat porodičnog prava"),
            ("assets/photos/uoded-imza-toreni.jpg", "Predsjednik UÖDED-a Ümit Hakan Karakaya — Potpisivanje sertifikata"),
            ("assets/photos/ozel-dedektif-dergisi-kapak.jpg", "Özel Dedektif Dergisi broj 4 — Naslovni intervju"),
            ("assets/photos/ustad-dergi-roportaj.jpg", "Advokatski časopis ÜSTAD — Intervju o zakonitim dokazima"),
            ("assets/photos/kiu-sertifika-programi.jpg", "Kiparski univerzitet nauka (KİÜ) — Program forenzike i istrage"),
            ("assets/photos/zirve-odul-toreni-kristal.jpg", "Samit Najbolji u godini — Dodjela Kristalne nagrade časti"),
        ],
        "faq_title": "Česta pitanja o Ümit Hakan Karakaya",
        "faqs": [
            ("Ko je Ümit Hakan Karakaya?", "Turski privatni detektiv, autor i predsjednik strukovnih udruženja, rođen 1973. u Ankari. Nakon službe F-16 tehničara u vojsci završio je Međunarodno pravo i 2005. osnovao DAT Detektiv."),
            ("Koja udruženja i platforme vodi?", "Osnivač je i predsjednik TÜDED-a i UÖDED-a, kao i lider platforme WPYB (We Protect Your Brand) za borbu protiv falsifikovanih proizvoda."),
            ("Koje knjige i nastupe u medijima ima?", "Autor je knjige „The Detective's Eye — In Search of Secrets and Traces“, urednik Özel Dedektif Dergisi, te gost na Kanal 24, TV8, u časopisu ÜSTAD i listu Hürriyet."),
            ("Koji su njegovi društveni projekti?", "Suosnivač je besplatne Biblioteke igračaka Hayalime Renk Ver i učesnik UKAİM aktivnosti za zaštitu i pronalazak djece."),
        ],
        "cross_title": "Ostale stranice i kancelarije",
        "cross_links": [("index.html", "Početna"), ("../istanbul-ozel-dedektif.html", "Kancelarija Istanbul (TR)"), ("../ankara-ozel-dedektif.html", "Kancelarija Ankara (TR)"), ("../hizmetler/es-takibi.html", "Praćenje partnera (TR)"), ("../hizmetler/kurumsal-ve-marka-koruma.html", "Korporativno i WPYB (TR)")],
        "cross_cta": "Besplatne konsultacije",
        "footer_1": "&copy; 2005 – 2026 DAT DETEKTIV (DAT Group) • Ümit Hakan Karakaya • Osnivač UÖDED-a",
        "footer_2": "Istanbul (Kartal) • Ankara (Çankaya) • Podgorica (Crna Gora) • Las Vegas (SAD)",
    },
}


def build_founder_pages():
    all_langs = ["tr"] + LANG_CODES
    founder_urls = []

    hreflang_links = "\n    ".join(
        [f'<link rel="alternate" hreflang="{HTML_LANG_ATTR[c]}" href="{DOMAIN}/{"" if c == "tr" else c + "/"}umit-hakan-karakaya.html">' for c in all_langs]
        + [f'<link rel="alternate" hreflang="x-default" href="{DOMAIN}/umit-hakan-karakaya.html">']
    )

    for code in all_langs:
        f = FOUNDER_I18N[code]
        is_root = (code == "tr")
        prefix = "" if is_root else "../"
        canonical = f"{DOMAIN}/{'umit-hakan-karakaya.html' if is_root else code + '/umit-hakan-karakaya.html'}"
        founder_urls.append(canonical)

        def founder_href(target_code):
            if is_root:
                return "umit-hakan-karakaya.html" if target_code == "tr" else f"{target_code}/umit-hakan-karakaya.html"
            if target_code == "tr":
                return "../umit-hakan-karakaya.html"
            if target_code == code:
                return "umit-hakan-karakaya.html"
            return f"../{target_code}/umit-hakan-karakaya.html"

        lang_nav_html = "\n                ".join(
            f'<a href="{founder_href(c)}" onclick="try{{localStorage.setItem(\'dat_site_lang\',\'{c}\')}}catch(_){{}}" class="px-2 py-1 rounded-full font-mono text-[10px] font-medium transition border {"studio-lime-btn border-transparent shadow-sm" if c == code else "studio-pill-muted bg-[#242428] border-white/10 text-white/80"}">{c.upper()}</a>'
            for c in all_langs
        )

        schema = [
            {
                "@context": "https://schema.org",
                "@type": "ProfilePage",
                "url": canonical,
                "name": f["title"],
                "inLanguage": HTML_LANG_ATTR[code],
                "dateModified": TODAY,
                "mainEntity": {"@id": f"{DOMAIN}/umit-hakan-karakaya.html#person"},
            },
            {
                "@context": "https://schema.org",
                "@type": "Person",
                "@id": f"{DOMAIN}/umit-hakan-karakaya.html#person",
                "name": f["person_name"],
                "birthDate": "1973",
                "birthPlace": {"@type": "Place", "name": f["birth_place"]},
                "nationality": f["nationality"],
                "jobTitle": f["job_title"],
                "description": f["description"],
                "url": canonical,
                "image": f"{DOMAIN}/assets/photos/wpyb-marka-dedektifligi-panel.jpg",
                "worksFor": {"@id": f"{DOMAIN}/#organization"},
            },
            {
                "@context": "https://schema.org",
                "@type": "Book",
                "name": "The Detective's Eye — In Search of Secrets and Traces",
                "author": {"@id": f"{DOMAIN}/umit-hakan-karakaya.html#person"},
                "inLanguage": "en",
            },
            {
                "@context": "https://schema.org",
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": f["home"], "item": f"{DOMAIN}/{'' if is_root else code + '/'}"},
                    {"@type": "ListItem", "position": 2, "name": f["breadcrumb"], "item": canonical},
                ],
            },
            {
                "@context": "https://schema.org",
                "@type": "FAQPage",
                "mainEntity": [
                    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                    for q, a in f["faqs"]
                ],
            },
        ]

        cards_html = "\n".join(
            f'''<article class="studio-surface bg-[#1C1C1F] rounded-3xl p-6 sm:p-7 border border-white/[0.09] shadow-sm space-y-3">
                <span class="studio-badge font-mono text-[10px] px-2.5 py-0.5 rounded-full bg-[#242428] text-[#93F051] border border-[#93F051]/35">{badge}</span>
                <h2 class="studio-title text-lg font-medium text-[#FFFFFF]">{h2}</h2>
                <p class="studio-body text-sm sm:text-[15px] text-white/80 leading-relaxed">{body}</p>
            </article>'''
            for badge, h2, body in f["cards"]
        )

        gallery_html = "\n".join(
            f'''<button type="button" onclick="openBioPhoto('{prefix}{img}', '{html_lib.escape(cap, quote=True)}')" class="studio-surface group text-left rtl:text-right bg-[#1C1C1F] rounded-2xl p-2.5 border border-white/[0.09] shadow-sm hover:shadow-md transition">
                <div class="relative aspect-[4/3] rounded-xl overflow-hidden bg-[#111111]">
                    <img src="{prefix}{img}" loading="lazy" decoding="async" alt="{html_lib.escape(cap, quote=True)}" class="w-full h-full object-cover object-top group-hover:scale-105 transition duration-500">
                </div>
                <p class="studio-title mt-2 px-1 text-xs sm:text-[13px] font-medium text-[#FFFFFF] leading-snug">{html_lib.escape(cap)}</p>
            </button>'''
            for img, cap in f["gallery"]
        )

        faqs_html = "\n".join(
            f'''<div class="studio-surface-soft p-5 rounded-2xl bg-[#18181A] border border-white/[0.09] space-y-2">
                <h3 class="studio-title text-[15px] font-medium text-[#FFFFFF]">{html_lib.escape(q)}</h3>
                <p class="studio-body text-sm sm:text-[15px] text-white/75 leading-relaxed">{html_lib.escape(a)}</p>
            </div>'''
            for q, a in f["faqs"]
        )

        cross_html = "\n                ".join(
            f'<a href="{href}" class="studio-pill-muted px-3.5 py-2 rounded-full bg-[#242428] border border-white/10 text-white/85 text-xs font-medium transition">{html_lib.escape(lbl)}</a>'
            for href, lbl in f["cross_links"]
        )

        page_html = f'''<!DOCTYPE html>
<html lang="{HTML_LANG_ATTR[code]}" dir="{f['dir']}" class="scroll-smooth dark" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
{SUBPAGE_THEME_BOOT}
    <title>{html_lib.escape(f["title"])}</title>
    <meta name="description" content="{html_lib.escape(f["description"])}">
    <meta name="keywords" content="{html_lib.escape(f["keywords"])}">
    <meta name="robots" content="index, follow, max-image-preview:large">
    <meta id="themeColorMeta" name="theme-color" content="#111111">
    <link rel="canonical" href="{canonical}">
    {hreflang_links}
    <link rel="icon" type="image/png" href="{prefix}dat-logo.png">
    <link rel="shortcut icon" href="{prefix}favicon.ico">
    <link rel="preconnect" href="https://cdn.tailwindcss.com" crossorigin>
    <link rel="preconnect" href="https://use.hugeicons.com" crossorigin>
    <meta property="og:type" content="profile">
    <meta property="profile:first_name" content="Ümit Hakan">
    <meta property="profile:last_name" content="Karakaya">
    <meta property="og:locale" content="{OG_LOCALES[code]}">
    <meta property="og:url" content="{canonical}">
    <meta property="og:site_name" content="DAT Özel Dedektiflik Bürosu">
    <meta property="og:title" content="{html_lib.escape(f["title"])}">
    <meta property="og:description" content="{html_lib.escape(f["description"])}">
    <meta property="og:image" content="{DOMAIN}/assets/photos/wpyb-marka-dedektifligi-panel.jpg">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:image" content="{DOMAIN}/assets/photos/wpyb-marka-dedektifligi-panel.jpg">
    <script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://use.hugeicons.com/font/icons.css">
    <style>
{SUBPAGE_STUDIO_CSS}
    </style>
</head>
<body class="bg-[#111111] text-[#F5F5F7] antialiased selection:bg-[#93F051] selection:text-[#111111]">
    <div class="h-[3px] w-full bg-[#93F051]"></div>

    <header class="studio-header sticky top-0 z-40 bg-[#111111]/90 backdrop-blur-xl border-b border-white/[0.09]">
        <div class="max-w-6xl mx-auto px-4 sm:px-6 min-h-16 py-2 flex flex-wrap items-center justify-between gap-2 sm:gap-3">
            <a href="index.html" class="flex items-center gap-3 group">
                <img src="{prefix}dat-logo.png" alt="DAT Dedektiflik Logo" class="w-10 h-10 rounded-full object-cover ring-2 ring-[#93F051]/70">
                <div class="leading-none">
                    <div class="studio-title text-sm font-medium text-[#FFFFFF]">DAT <span class="studio-accent-text text-[#93F051]">DEDEKTİFLİK</span></div>
                    <p class="studio-muted text-[10px] font-mono text-white/60 uppercase mt-0.5">{html_lib.escape(f["brand_sub"])}</p>
                </div>
            </a>
            <div class="flex flex-wrap items-center gap-2">
                <nav aria-label="Language Switcher" class="flex items-center gap-1">
                {lang_nav_html}
                </nav>
                <button id="themeToggleBtn" type="button" onclick="toggleSiteTheme()" aria-label="Theme" class="studio-pill-muted inline-flex items-center justify-center w-8 h-8 rounded-full bg-[#242428] border border-white/15 text-[11px] font-medium transition">
                    <i id="themeToggleIcon" class="hgi hgi-stroke hgi-sun-03 w-3.5 h-3.5 text-[#93F051]"></i>
                </button>
                <a href="index.html#makaleler" class="hidden md:inline-flex items-center gap-1.5 px-3.5 py-2 rounded-full studio-pill-muted bg-[#242428] border border-white/10 text-xs font-medium transition">
                    <span>{html_lib.escape(f["nav_press"])}</span>
                </a>
                <a href="index.html#vaka-bildir" class="inline-flex items-center gap-1.5 px-4 py-2 rounded-full studio-lime-btn text-xs font-medium shadow-sm transition">
                    <span>{html_lib.escape(f["nav_cta"])}</span>
                </a>
            </div>
        </div>
    </header>

    <main class="max-w-5xl mx-auto px-4 sm:px-6 py-7 sm:py-10 space-y-7 sm:space-y-8">
        <nav aria-label="Breadcrumb" class="studio-muted text-xs font-mono text-white/60 flex items-center gap-2">
            <a href="index.html" class="studio-accent-text text-[#93F051] hover:underline">{html_lib.escape(f["home"])}</a>
            <span>/</span>
            <span class="studio-title text-[#FFFFFF] font-medium">{html_lib.escape(f["breadcrumb"])}</span>
        </nav>

        <section class="studio-surface-soft grid lg:grid-cols-12 gap-8 items-center bg-[#18181A] rounded-[28px] p-6 sm:p-9 border border-white/[0.09] shadow-2xl">
            <div class="lg:col-span-5 space-y-3">
                <button type="button" onclick="openBioPhoto('{prefix}assets/photos/wpyb-marka-dedektifligi-panel.jpg', '{html_lib.escape(f['portrait_alt'], quote=True)}')" class="w-full rounded-2xl overflow-hidden border border-white/15 shadow-xl aspect-[4/3] bg-[#111111] block group">
                    <img src="{prefix}assets/photos/wpyb-marka-dedektifligi-panel.jpg" alt="{html_lib.escape(f['portrait_alt'], quote=True)}" class="w-full h-full object-cover object-top group-hover:scale-105 transition duration-500">
                </button>
                <div class="grid grid-cols-3 gap-2 text-center">
                    <div class="studio-surface p-2.5 rounded-xl bg-[#1C1C1F] border border-white/[0.08]">
                        <div class="studio-title text-sm font-medium text-[#FFFFFF]">1973</div>
                        <div class="studio-muted text-[10px] font-mono text-white/60">{html_lib.escape(f["birth_lbl"])}</div>
                    </div>
                    <div class="studio-surface p-2.5 rounded-xl bg-[#1C1C1F] border border-white/[0.08]">
                        <div class="studio-title text-sm font-medium text-[#FFFFFF]">2005</div>
                        <div class="studio-muted text-[10px] font-mono text-white/60">{html_lib.escape(f["est_lbl"])}</div>
                    </div>
                    <div class="studio-surface p-2.5 rounded-xl bg-[#1C1C1F] border border-white/[0.08]">
                        <div class="studio-accent-text text-sm font-medium text-[#93F051]">{wrap_rtl_text_to_html(f["cases_val"]) if f["dir"] == "rtl" else html_lib.escape(f["cases_val"])}</div>
                        <div class="studio-muted text-[10px] font-mono text-white/60">{html_lib.escape(f["cases_lbl"])}</div>
                    </div>
                </div>
            </div>

            <div class="lg:col-span-7 space-y-4">
                <span class="studio-badge inline-block px-3 py-1 rounded-full bg-[#242428] border border-[#93F051]/35 text-[#93F051] font-mono text-[11px] font-medium">{html_lib.escape(f["hero_badge"])}</span>
                <h1 class="studio-title text-2xl sm:text-4xl font-medium text-[#FFFFFF] leading-tight tracking-tight">{html_lib.escape(f["h1"])}</h1>
                <p class="studio-body text-sm sm:text-base text-white/80 leading-relaxed">{f["hero_p"]}</p>
                <blockquote class="studio-surface p-4 rounded-2xl bg-[#1C1C1F] border border-white/[0.09] text-xs studio-body text-white/80 italic leading-relaxed">{f["quote"]}</blockquote>
                <div class="flex flex-wrap gap-3 pt-1">
                    <a href="https://wa.me/905326667749" target="_blank" rel="noopener noreferrer" class="px-5 py-3 rounded-full studio-lime-btn text-xs font-medium inline-flex items-center gap-2 shadow-lg transition">
                        <i class="hgi hgi-stroke hgi-whatsapp w-4 h-4"></i>
                        <span>{wrap_rtl_text_to_html(f["btn_wa"]) if f["dir"] == "rtl" else html_lib.escape(f["btn_wa"])}</span>
                    </a>
                    <a href="index.html" class="studio-keep-dark px-5 py-3 rounded-full bg-[#242428] hover:bg-[#2E2E34] border border-white/15 text-[#FFFFFF] text-xs font-medium inline-flex items-center gap-2 transition">
                        <span>{html_lib.escape(f["btn_home"])}</span>
                    </a>
                </div>
            </div>
        </section>

        <section class="grid md:grid-cols-2 gap-5">
            {cards_html}
        </section>

        <section class="studio-keep-dark bg-[#111111] text-[#FFFFFF] rounded-[28px] p-6 sm:p-9 space-y-4 shadow-2xl border border-white/15">
            <div class="font-mono text-xs studio-coral-ink text-[#FA7E61] uppercase tracking-wider">{html_lib.escape(f["social_badge"])}</div>
            <h2 class="text-xl sm:text-2xl font-medium">{html_lib.escape(f["social_h2"])}</h2>
            <p class="text-sm sm:text-[15px] text-white/80 leading-relaxed">{f["social_p"]}</p>
        </section>

        <section class="space-y-4">
            <div class="flex items-center justify-between">
                <h2 class="studio-title text-xl font-medium text-[#FFFFFF] tracking-tight">{html_lib.escape(f["gallery_title"])}</h2>
                <span class="studio-muted text-xs font-mono text-white/60">{html_lib.escape(f["gallery_hint"])}</span>
            </div>
            <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
                {gallery_html}
            </div>
        </section>

        <section class="space-y-4">
            <h2 class="studio-title text-xl font-medium text-[#FFFFFF] tracking-tight">{html_lib.escape(f["faq_title"])}</h2>
            <div class="grid sm:grid-cols-2 gap-4">
                {faqs_html}
            </div>
        </section>

        <section class="studio-divider pt-5 border-t border-white/10 space-y-3">
            <div class="studio-muted text-xs font-mono text-white/60 uppercase">{html_lib.escape(f["cross_title"])}</div>
            <div class="flex flex-wrap gap-2">
                {cross_html}
                <a href="index.html#vaka-bildir" class="px-3.5 py-2 rounded-full studio-lime-btn text-xs font-medium">{html_lib.escape(f["cross_cta"])}</a>
            </div>
        </section>
    </main>

    <div id="bioPhotoModal" class="fixed inset-0 z-50 hidden bg-[#000000]/85 backdrop-blur-md flex items-center justify-center p-4" onclick="closeBioPhoto()">
        <div class="studio-surface relative max-w-3xl w-full bg-[#1C1C1F] border border-white/15 rounded-3xl overflow-hidden shadow-2xl" onclick="event.stopPropagation()">
            <button type="button" onclick="closeBioPhoto()" class="studio-keep-dark absolute top-3 right-3 rtl:right-auto rtl:left-3 z-10 w-9 h-9 rounded-full bg-[#111111]/85 text-[#FFFFFF] flex items-center justify-center hover:bg-[#93F051] hover:text-[#111111] transition">
                <i class="hgi hgi-stroke hgi-cancel-01 w-4 h-4"></i>
            </button>
            <img id="bioPhotoImg" src="" alt="" class="w-full max-h-[75vh] object-contain bg-[#111111]">
            <div id="bioPhotoCap" class="studio-title studio-divider p-4 text-xs sm:text-sm font-medium text-[#FFFFFF] border-t border-white/10"></div>
        </div>
    </div>

    <footer class="studio-footer bg-[#161618] border-t border-white/[0.08] py-8 px-4 text-center text-xs text-white/60 space-y-2">
        <div>{wrap_rtl_html(f["footer_1"], f["dir"] == "rtl")}</div>
        <div>{html_lib.escape(f["footer_2"])} • <a href="index.html" class="studio-accent-text text-[#93F051] underline">{html_lib.escape(f["btn_home"])}</a></div>
    </footer>

    <script>
        try {{ localStorage.setItem('dat_site_lang', '{code}'); }} catch (_) {{}}
{SUBPAGE_THEME_SCRIPT}
        function openBioPhoto(src, cap) {{
            document.getElementById('bioPhotoImg').src = src;
            document.getElementById('bioPhotoImg').alt = cap;
            document.getElementById('bioPhotoCap').textContent = cap;
            document.getElementById('bioPhotoModal').classList.remove('hidden');
        }}
        function closeBioPhoto() {{
            document.getElementById('bioPhotoModal').classList.add('hidden');
        }}
        document.addEventListener('keydown', function(e) {{
            if (e.key === 'Escape') closeBioPhoto();
        }});
    </script>
</body>
</html>'''

        out_path = os.path.join(ROOT, "umit-hakan-karakaya.html" if is_root else os.path.join(code, "umit-hakan-karakaya.html"))
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as fh:
            fh.write(page_html)
    return founder_urls


def main():
    with open(os.path.join(ROOT, "index.html"), "r", encoding="utf-8") as f:
        index_src = f.read()
    langs = load_all_lang_packs()
    built_locales = build_locale_pages(index_src, langs)
    founder_urls = build_founder_pages()
    built_seo = build_turkish_seo_pages()
    sitemap_count = build_sitemap(founder_urls, built_seo)
    print(f"BUILT LOCALES ({len(built_locales)}):", built_locales)
    print(f"BUILT FOUNDER BIO PAGES ({len(founder_urls)}):", founder_urls)
    print(f"BUILT TURKISH SEO PAGES ({len(built_seo)}):", [os.path.basename(u) for u in built_seo])
    print(f"SITEMAP TOTAL URLS: {sitemap_count}")


if __name__ == "__main__":
    main()
