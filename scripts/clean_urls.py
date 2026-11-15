#!/usr/bin/env python3
"""
Temiz URL normalizasyonu (Cloudflare Pages uyumu).

Cloudflare Pages "/sayfa.html" adreslerini 308 ile "/sayfa" adresine yönlendirir.
Canonical / hreflang / sitemap / iç linkler ".html" gösterdiğinde Google
"Yönlendirmeli sayfa" + "Canonical çakışması" sinyali alır ve sayfaları dizine eklemeyebilir.
Bu betik tüm yayın dosyalarında ".html" uzantılı site içi adresleri uzantısız hale getirir.

build_seo.py sonunda otomatik çalışır; tek başına da çalıştırılabilir:
    python3 scripts/clean_urls.py
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOMAIN = "https://www.datdetective.com"
SKIP_DIRS = {"_archive_raw", "node_modules", ".git", "yeni-medya", "Dat Evraklar", "functions", "src"}

# 1) Mutlak site adresleri: https://www.datdetective.com/x/y.html -> /x/y ; /x/index.html -> /x/
ABS_RE = re.compile(re.escape(DOMAIN) + r"/((?:[A-Za-z0-9_\-]+/)*)([A-Za-z0-9_\-]+)\.html(?=[\"'#?<\s)])")

def _abs_sub(m):
    folder, name = m.group(1), m.group(2)
    if name == "index":
        return f"{DOMAIN}/{folder}"
    return f"{DOMAIN}/{folder}{name}"

# 2) Göreli iç linkler: href="../hizmetler/es-takibi.html#x" -> href="../hizmetler/es-takibi#x"
REL_RE = re.compile(r"""(href=)(["'])((?:\.\./|\./)*(?:[A-Za-z0-9_\-]+/)*)([A-Za-z0-9_\-]+)\.html([#?][^"']*)?\2""")

def _rel_sub(m):
    attr, q, folder, name, tail = m.group(1), m.group(2), m.group(3), m.group(4), m.group(5) or ""
    if name == "404":
        return m.group(0)
    if name == "index":
        target = folder or "./"
    else:
        target = folder + name
    return f"{attr}{q}{target}{tail}{q}"


SEO_LINK_TITLES = [
    ("ankara-ozel-dedektif", "Ankara Dedektif & Özel Dedektiflik Bürosu — Çankaya Merkez ve 25 İlçede Eş Takibi, Boşanma Delili"),
    ("istanbul-ozel-dedektif", "İstanbul Dedektif & Özel Dedektiflik Bürosu — Kartal Merkez ve 39 İlçede Eş Takibi, Hukuki Araştırma"),
    ("izmir-ozel-dedektif", "İzmir Dedektif & Özel Dedektiflik Bürosu — Konak, Karşıyaka, Bornova, Çeşme ve 30 İlçede Özel Dedektif"),
    ("mersin-ozel-dedektif", "Mersin Dedektif & Özel Dedektiflik Bürosu — Yenişehir, Mezitli, Tarsus, Erdemli ve 13 İlçede Özel Dedektif"),
    ("konya-ozel-dedektif", "Konya Dedektif & Özel Dedektiflik Bürosu — Selçuklu, Meram, Karatay, Ereğli, Kulu ve 31 İlçede Özel Dedektif"),
    ("antalya-ozel-dedektif", "Antalya Dedektiflik & Özel Dedektif Bürosu — Muratpaşa, Konyaaltı, Alanya, Manavgat ve 19 İlçede Dedektiflik"),
    ("bursa-ozel-dedektif", "Bursa Dedektif & Özel Dedektiflik Bürosu — Nilüfer, Osmangazi, Yıldırım, İnegöl ve 17 İlçede Özel Dedektif"),
    ("hizmetler/es-takibi", "Eş Takibi, Aldatma Tespiti ve Boşanma Davası Hukuka Uygun Delil Toplama — DAT Özel Dedektiflik"),
    ("hizmetler/evlilik-oncesi-arastirma", "Evlilik Öncesi Araştırma ve Nişanlı Geçmiş Tahkikatı — %100 Gizli Dedektiflik Hizmeti"),
    ("hizmetler/velayet-bosanma", "Velayet ve Boşanma Davaları İçin Somut Delil ve Gelir Tespiti — DAT Özel Dedektiflik"),
    ("hizmetler/ogrenci-takibi", "Öğrenci Takibi ve Genç Güvenliği Araştırması — Ebeveynlere Özel Gizli Gözlem"),
    ("hizmetler/adres-ve-borclu-takibi", "Fiili Adres Tespiti, Kayıp Şahıs ve Borçlu Mal Varlığı Araştırması — DAT Özel Dedektiflik"),
    ("hizmetler/bilisim-dolandiriciligi", "Bilişim Dolandırıcılığı, Siber İz ve Dijital Delil Tespiti — DAT Özel Dedektiflik"),
    ("hizmetler/firma-arastirmasi", "Kurumsal Firma Araştırması, Ticari İstihbarat ve Ortaklık Öncesi Doğrulama — DAT Dedektiflik"),
    ("hizmetler/hirsizlik-arastirmasi", "İşyeri, Fabrika ve Depo Hırsızlık Araştırması & İç Suistimal Tespiti — DAT Dedektiflik"),
    ("hizmetler/marka-taklidi-arastirmasi", "Marka Taklidi, Sahte Ürün Tespiti ve SMK m.29 Baskın Delili — WPYB & DAT Dedektiflik"),
    ("hizmetler/bocek-tarama-tscm", "Profesyonel Böcek Arama, Dinleme Cihazı ve Gizli Kamera Tespiti (TSCM) — DAT Dedektiflik"),
    ("hizmetler/kurumsal-ve-marka-koruma", "Kurumsal Araştırma, Marka Koruma ve WPYB Global Hizmetleri — DAT Özel Dedektiflik"),
    ("umit-hakan-karakaya", "Ümit Hakan Karakaya Kimdir? — DAT Özel Dedektiflik Kurucusu, UÖDED & TÜDED Başkanı"),
    ("elsa-vaka-paneli", "Elsa Dijital Dedektif Asistanı ve Canlı Vaka Takip Paneli — DAT Özel Dedektiflik"),
    ("#dedektife-sor", "Dedektif'e Sor — Dedektif Tutmak, Dedektif Ücretleri ve Yasal Süreçler Hakkında Uzman Cevapları"),
    ("#ofislerimiz", "DAT Özel Dedektiflik Bürosu Merkez ve Bölge Büroları — Ankara, İstanbul, İzmir, Mersin, Konya, Antalya"),
    ("#hizmetler", "Özel Dedektiflik Hizmetlerimiz — Eş Takibi, Evlilik Öncesi, Adres Tespiti ve Kurumsal Araştırma"),
    ("#kurumsal", "Hakkımızda & Kurumsal Kimlik — 2005'ten Bugüne 4.000+ Vaka Tecrübesiyle DAT Özel Dedektiflik"),
    ("#makaleler", "Hukuki Rehber, Makaleler ve Basın Arşivi — DAT Özel Dedektiflik Bürosu"),
    ("#video-arsivi", "Video Arşivi, TV Yayınları ve Ödül Törenleri — DAT Özel Dedektiflik Bürosu"),
    ("#basin-galerisi", "Basında Biz, Sertifikalar ve Kongre Fotoğraf Arşivi — DAT Özel Dedektiflik"),
    ("#magaza", "DAT Güvenlik ve Anti-Casusluk Donanım Mağazası — Profesyonel Böcek Arama Dedektörleri"),
    ("#avrupa-masasi", "Almanya ve Avrupa Gurbetçi Özel Dedektiflik Masası — Türkiye'de Eş Takibi ve Miras Araştırması"),
    ("#vaka-bildir", "Ücretsiz Ön Görüşme, Vaka Bildirimi ve Dedektif Fiyat Teklifi Formu — DAT Özel Dedektiflik"),
    ("#sss", "Özel Dedektiflik Hakkında Sıkça Sorulan Sorular, Ücretler ve Hukuki Geçerlilik"),
    ("wa.me/905326667749", "7/24 WhatsApp Özel Dedektif Danışma Hattı: 0532 666 77 49 — DAT Özel Dedektiflik"),
    ("tel:+903122840299", "DAT Özel Dedektiflik Ankara Merkez Büro Sabit Telefon: 0312 284 02 99"),
    ("tel:+905326667749", "DAT Özel Dedektiflik 7/24 Acil Mobil Hat: 0532 666 77 49"),
    ("mailto:info@datdetective.com", "DAT Özel Dedektiflik Bürosu Resmi E-Posta İletişimi: info@datdetective.com"),
    ("instagram.com/datdedektiflik", "DAT Özel Dedektiflik Bürosu Resmi Instagram Hesabı (@datdedektiflik)"),
    ("facebook.com/DatDedektiflik", "DAT Özel Dedektiflik Bürosu Resmi Facebook Sayfası"),
    ("x.com/datdedektif", "DAT Özel Dedektiflik Bürosu Resmi X (Twitter) Hesabı"),
    ("/en/", "DAT Private Detective Agency Turkey — English Homepage"),
    ("/de/", "DAT Privatdetektei Türkei — Deutsche Startseite"),
    ("/fr/", "Agence de Détective Privé DAT Turquie — Accueil Français"),
    ("/ar/", "مكتب دات للتحقيقات الخاصة في تركيا — الصفحة الرئيسية"),
    ("/ru/", "Частное детективное агентство DAT в Турции — Главная"),
    ("/me/", "DAT Privatna Detektivska Agencija — Crnogorski / Srpski"),
]

A_TAG_RE = re.compile(r"<a\s+([^>]*?)>", re.S)


def _add_link_title(m):
    attrs = m.group(1)
    if re.search(r'\btitle\s*=', attrs, re.I):
        return m.group(0)
    href_m = re.search(r'\bhref\s*=\s*(["\'])(.*?)\1', attrs, re.I)
    if not href_m:
        return m.group(0)
    href = href_m.group(2)
    chosen_title = None
    for key, desc in SEO_LINK_TITLES:
        if key in href:
            chosen_title = desc
            break
    if not chosen_title:
        if href in ("./", "/", "index", "../", "../../"):
            chosen_title = "DAT Özel Dedektiflik Bürosu Ana Sayfa — Sertifikalı Özel Dedektif Hizmetleri"
        else:
            chosen_title = "DAT Özel Dedektiflik Bürosu — 7/24 Yasal ve Gizli Özel Dedektiflik Hizmetleri"
    return f'<a {attrs} title="{chosen_title}">'


def normalize_text(text, is_html):
    out = ABS_RE.sub(_abs_sub, text)
    if is_html:
        out = REL_RE.sub(_rel_sub, out)
        out = A_TAG_RE.sub(_add_link_title, out)
    return out


def normalize_redirects(path):
    """_redirects hedeflerindeki .html'i temizle (200 rewrite satırları hariç: dosyaya işaret etmeli)."""
    with open(path, "r", encoding="utf-8") as f:
        lines = f.read().split("\n")
    changed = 0
    for i, line in enumerate(lines):
        parts = line.split()
        if len(parts) >= 3 and not line.lstrip().startswith("#") and parts[2].startswith("30"):
            tgt = parts[1]
            if tgt.endswith(".html") and tgt.startswith("/"):
                new = tgt[:-5]
                if new.endswith("/index"):
                    new = new[:-5]
                lines[i] = line.replace(" " + tgt + " ", " " + new + " ", 1)
                changed += lines[i] != line
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return changed


def run(root=ROOT):
    changed_files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")]
        for fn in filenames:
            if not (fn.endswith(".html") or fn == "sitemap.xml" or fn == "robots.txt"):
                continue
            if fn in ("yonetim-paneli.html",):
                continue
            p = os.path.join(dirpath, fn)
            with open(p, "r", encoding="utf-8") as f:
                src = f.read()
            dst = normalize_text(src, fn.endswith(".html"))
            if dst != src:
                with open(p, "w", encoding="utf-8") as f:
                    f.write(dst)
                changed_files.append(os.path.relpath(p, root))
    redir = os.path.join(root, "_redirects")
    n_redir = normalize_redirects(redir) if os.path.isfile(redir) else 0
    return changed_files, n_redir


if __name__ == "__main__":
    files, n = run()
    print(f"CLEAN URLS: {len(files)} dosya güncellendi, _redirects: {n} satır")
    for f in files:
        print("  -", f)
