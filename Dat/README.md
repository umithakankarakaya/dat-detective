# 🕵️‍♂️ DAT Dedektiflik & Kriminal İstihbarat Bürosu

Özel araştırma, teknik takip, kurumsal teftiş ve adli bilişim hizmetleri için tasarlanmış yüksek atmosferli, modern ve noir temalı dedektiflik web sitesi.

---

## 🌟 Öne Çıkan Özellikler

- **Noir Atmosfer & Siber Güvenlik Teması**: Koyu tonlar, kırmızı/kehribar vurgular, radar/scanline ızgara efekti ve mühür detayları.
- **Acil Çıkış (Panic Button)**: Klavyeden `ESC` tuşuna basıldığında veya butona tıklandığında sayfayı anında Google'a yönlendirerek gizlilik sağlar.
- **İnteraktif Vaka Dosyaları**: Tıklandığında açılan vaka simülasyonları ve delil kartları (ileride eklenecek dedektiflik mini oyunu için hazır altyapı).
- **Şifreli Vaka Başvuru Formu**: Kod adı, aciliyet derecesi ve gizli iletişim kanalları (Signal, WhatsApp, ProtonMail) ile AES-256 simülasyonlu form ve takip kodu üretimi.
- **S.S.S. Akordeon**: Merak edilen yasal ve operasyonel sorular.
- **Sıfır Bağımlılık (Zero Dependencies)**: Node.js veya npm kurulumu gerektirmez, doğrudan her tarayıcıda anında çalışır.

---

## 🚀 Bilgisayarınızda Çalıştırma ve Önizleme

Terminalde bu klasördeyken aşağıdaki komutu çalıştırabilirsiniz:

```bash
python3 server.py
```

Ardından tarayıcınızdan `http://localhost:3000` adresine girerek sitenizi ve gerçek zamanlı ziyaretçi sayacını (`/api/presence`) hemen canlı görebilirsiniz.
*(Alternatif olarak statik mod için `python3 -m http.server 3000` da kullanılabilir.)*

---

## 📦 GitHub'a Yükleme Adımları

1. [GitHub](https://github.com) hesabınıza giriş yapın.
2. Sağ üstten **`+` -> New repository** butonuna tıklayın.
3. Repository adına örneğin `dedektiflik-sitesi` yazın ve **Create repository** deyin.
4. Terminalde şu 3 komutu çalıştırın (kendi repo linkinizi yazarak):

```bash
git add .
git commit -m "feat: ilk dedektiflik sitesi surumu"
git remote add origin https://github.com/KULLANICI_ADINIZ/dedektiflik-sitesi.git
git push -u origin main
```

---

## ⚡ Vercel ile Canlı Yayına Alma (Ücretsiz)

1. [Vercel](https://vercel.com) sitesine gidip **GitHub ile Giriş Yap**ın.
2. **"Add New..." -> "Project"** butonuna tıklayın.
3. GitHub'a yüklediğiniz `dedektiflik-sitesi` reposunu seçip **"Deploy"** butonuna basın.
4. Yaklaşık 10 saniye içinde siteniz `https://dedektiflik-sitesi.vercel.app` şeklinde dünya çapında ücretsiz olarak yayına girer!
