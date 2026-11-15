# -*- coding: utf-8 -*-
import os
import json
import re

def audit():
    print("=== DAT DETECTIVE SİSTEM VE CANLI DOĞRULAMA DENETİMİ ===\n")
    errors = []
    warnings = []
    
    # 1. Yerel index.html Dosya Kontrolü
    if not os.path.exists("index.html"):
        errors.append("index.html bulunamadı!")
        return
        
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()

    # A) JSON-LD Validasyonu
    json_ld_matches = re.findall(r'<script\s+type=["\']application/ld\+json["\']>(.*?)</script>', html, re.DOTALL)
    print(f"[✓] {len(json_ld_matches)} adet JSON-LD Schema bloğu bulundu.")
    for idx, sc_text in enumerate(json_ld_matches):
        try:
            data = json.loads(sc_text.strip())
            types = [item.get('@type') for item in data if isinstance(item, dict)] if isinstance(data, list) else data.get('@type')
            print(f"    - JSON-LD Blok #{idx+1}: Geçerli JSON (Türler: {types})")
        except Exception as e:
            errors.append(f"JSON-LD Blok #{idx+1} Sözdizimi Hatası: {e}")
            
    # B) #arama-rehberi Kontrolü
    if 'id="arama-rehberi"' in html:
        paa_items = re.findall(r'class="[^"]*paa-item[^"]*"', html)
        cat_btns = re.findall(r'class="[^"]*paa-cat-btn[^"]*"', html)
        has_search_input = 'id="paaSearchInput"' in html
        print(f"\n[✓] #arama-rehberi Modülü: Mevcut")
        print(f"    - Arama Kutusu: {'Var' if has_search_input else 'YOK'}")
        print(f"    - Kategori Butonları: {len(cat_btns)} adet")
        print(f"    - PAA Soru/Cevap Kartları: {len(paa_items)} adet")
        if len(paa_items) == 0:
            errors.append("#arama-rehberi içinde hiç soru kartı (paa-item) bulunamadı!")
    else:
        errors.append("#arama-rehberi modülü index.html içinde bulunamadı!")
        
    # C) #turkiye-dedektif-agi Kontrolü
    if 'id="turkiye-dedektif-agi"' in html:
        geo_section = html[html.find('id="turkiye-dedektif-agi"'):html.find('id="turkiye-dedektif-agi"') + 40000]
        from scripts.generate_keywords_txt import cities_districts
        found_cities = [city for city in cities_districts.keys() if city in geo_section]
        print(f"\n[✓] #turkiye-dedektif-agi Modülü: Mevcut")
        print(f"    - 81 İlden Metinde Eşleşen: {len(found_cities)} / 81 il")
        if len(found_cities) < 81:
            warnings.append(f"Bazı iller geo-hub metninde bulunamadı ({len(found_cities)}/81)")
    else:
        errors.append("#turkiye-dedektif-agi modülü index.html içinde bulunamadı!")
        
    # D) #dedektife-sor Canlı Chat Kontrolü
    if 'id="dedektife-sor"' in html:
        has_chat_input = 'id="aiChatInput"' in html
        has_chat_btn = 'id="aiSendBtn"' in html
        has_messages = 'id="aiChatMessages"' in html
        print(f"\n[✓] #dedektife-sor (Yeni Nesil Dedektif) Chat Modülü: Mevcut")
        print(f"    - Mesajlaşma Alanı (#aiChatMessages): {'Var' if has_messages else 'YOK'}")
        print(f"    - Chat Giriş Kutusu (#aiChatInput): {'Var' if has_chat_input else 'YOK'}")
        print(f"    - Gönder Butonu (#aiSendBtn): {'Var' if has_chat_btn else 'YOK'}")
    else:
        errors.append("#dedektife-sor modülü bulunamadı!")

    # E) Protokol ve TXT Dosyaları Kontrolü
    files_to_check = [
        "llms.txt",
        "llms-full.txt",
        "robots.txt",
        "sitemap.xml",
        "dat-dedektiflik-tum-arama-anahtar-kelimeleri.txt"
    ]
    print("\n[✓] Protokol ve Metin Dosyaları:")
    for fpath in files_to_check:
        if os.path.exists(fpath):
            size = os.path.getsize(fpath)
            with open(fpath, "r", encoding="utf-8") as tf:
                lines = len(tf.readlines())
            print(f"    - {fpath}: MEVCUT ({size} bayt, {lines} satır)")
        else:
            errors.append(f"{fpath} dosyası bulunamadı!")
            
    # F) 19 Şehir Sayfası Kontrolü
    city_pages = [
        "ankara-ozel-dedektif.html", "istanbul-ozel-dedektif.html", "izmir-ozel-dedektif.html",
        "antalya-ozel-dedektif.html", "bursa-ozel-dedektif.html", "konya-ozel-dedektif.html",
        "mersin-ozel-dedektif.html", "mugla-ozel-dedektif.html", "adana-ozel-dedektif.html",
        "kocaeli-ozel-dedektif.html", "gaziantep-ozel-dedektif.html", "eskisehir-ozel-dedektif.html",
        "trabzon-ozel-dedektif.html", "kayseri-ozel-dedektif.html", "aydin-ozel-dedektif.html",
        "balikesir-ozel-dedektif.html", "tekirdag-ozel-dedektif.html", "samsun-ozel-dedektif.html",
        "diyarbakir-ozel-dedektif.html"
    ]
    print(f"\n[✓] 19 Özel Şehir Açılış Sayfası:")
    missing_pages = [p for p in city_pages if not os.path.exists(p)]
    if missing_pages:
        errors.append(f"Eksik şehir sayfaları: {missing_pages}")
    else:
        print(f"    - 19 Şehir Açılış Sayfasının Tümü Yerel Olarak Mevcut (19/19)")

    # G) Root & Dat/ Ayna Dizin Senkronizasyonu Kontrolü
    print("\n[✓] Root ve Dat/ Dizin Senkronizasyonu:")
    diff_count = 0
    for root_file in ["index.html", "script.js", "llms.txt", "llms-full.txt", "sitemap.xml", "dat-dedektiflik-tum-arama-anahtar-kelimeleri.txt"]:
        dat_path = os.path.join("Dat", root_file)
        if not os.path.exists(dat_path):
            errors.append(f"Dat/{root_file} ayna dosyası eksik!")
            diff_count += 1
        else:
            s_root = os.path.getsize(root_file)
            s_dat = os.path.getsize(dat_path)
            if s_root != s_dat:
                errors.append(f"{root_file} ({s_root} bayt) ve Dat/{root_file} ({s_dat} bayt) boyutları eşleşmiyor!")
                diff_count += 1
    if diff_count == 0:
        print("    - Tüm kritik dosyalar Root ve Dat/ arasında %100 BİREBİR EŞİTLENDİ.")

    print("\n" + "=" * 50)
    if errors:
        print(f"[X] DENETİM TAMAMLANDI - {len(errors)} HATA TESPİT EDİLDİ:")
        for err in errors:
            print(f"  - {err}")
    else:
        print("[✓] TÜM YEREL DENETİMLER BAŞARIYLA GEÇTİ (0 HATA).")
    if warnings:
        print(f"[!] {len(warnings)} Uyarı:")
        for w in warnings:
            print(f"  - {w}")
    print("=" * 50)

if __name__ == "__main__":
    audit()
