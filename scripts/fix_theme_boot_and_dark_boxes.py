#!/usr/bin/env python3
"""
fix_theme_boot_and_dark_boxes.py
1. Fix datThemeBoot script in <head> to forcefully enforce 'light' mode and clear any legacy 'dark' setting from localStorage.
2. Fix Cyber at Frontier banner: apply explicit style="color: #FFFFFF !important;" to ensure headings and text are crisp bright white.
3. Fix Garanti 03 card: change from bg-black text-black to clean light card with black text like Garanti 01 and 02.
4. Fix service image law badges to bg-black/80 text-white so they are 100% legible over photos.
5. Add explicit CSS rules for .text-white and .theme-dark-feature-banner.
"""

import os
import re

ROOT_INDEX = "index.html"
DAT_INDEX = "Dat/index.html"

with open(ROOT_INDEX, "r", encoding="utf-8") as f:
    content = f.read()

# 1. FIX datThemeBoot in <head>
old_boot = re.search(r'<script id="datThemeBoot">.*?</script>', content, re.DOTALL)
assert old_boot, "datThemeBoot not found!"

new_boot = '''<script id="datThemeBoot">
        (function () {
            try {
                localStorage.setItem('dat_theme', 'light');
                localStorage.removeItem('theme');
                var root = document.documentElement;
                root.setAttribute('data-theme', 'light');
                root.style.colorScheme = 'light';
                root.classList.remove('dark');
                root.classList.add('light');
            } catch (e) {}
        })();
    </script>'''

content = content[:old_boot.start()] + new_boot + content[old_boot.end():]
print("Fixed datThemeBoot to strictly enforce 'light' mode!")

# 2. FIX Cyber at Frontier Banner in Hero
old_banner_re = re.search(r'<div class="relative rounded-3xl overflow-hidden aspect-\[16/7\].*?</div>\s*</div>\s*</div>', content, re.DOTALL)
if old_banner_re:
    new_banner = '''<div class="theme-dark-feature-banner relative rounded-3xl overflow-hidden aspect-[16/7] sm:aspect-[21/7] bg-black text-white flex flex-col justify-between p-6 sm:p-10 lg:p-12 shadow-sm border border-black/10">
                    <img src="assets/og-banner.jpg" alt="DAT Özel Dedektiflik Adli Saha Masası" class="absolute inset-0 w-full h-full object-cover opacity-35 filter brightness-90">
                    <div class="relative z-10 flex items-center justify-between">
                        <span class="text-lg sm:text-2xl font-bold tracking-tight" style="color: #FFFFFF !important;">DAT Dedektiflik</span>
                        <span class="text-[11px] sm:text-xs font-mono uppercase tracking-wider border border-white/30 bg-black/60 backdrop-blur-md px-3 py-1 rounded-full" style="color: #FFFFFF !important;">Soruşturma &amp; Adli Kanıt Masası</span>
                    </div>
                    <div class="relative z-10 max-w-2xl space-y-2">
                        <h2 class="text-xl sm:text-3xl lg:text-4xl font-semibold tracking-tight leading-tight" style="color: #FFFFFF !important; -webkit-text-fill-color: #FFFFFF !important;">
                            Yargıtay Uyumlu Adli Delil ve 81 İlde Gizli Saha Operasyonları
                        </h2>
                        <p class="text-xs sm:text-sm font-normal leading-relaxed" style="color: rgba(255, 255, 255, 0.85) !important;">
                            20 yıllık resmi kurumsal tecrübe, HMK m.189/199 ve TCK m.134 tam yasal güvencesiyle tek celsede kabul gören mahkeme delilleri.
                        </p>
                    </div>
                </div>'''
    content = content[:old_banner_re.start()] + new_banner + content[old_banner_re.end():]
    print("Fixed Cyber at Frontier banner to have guaranteed bright white text!")

# 3. FIX Garanti 03 Card (from black-on-black to clean light card)
garanti_03_re = re.search(r'<div class="p-4 rounded-2xl bg-black text-black space-y-1">.*?GARANTİ 03.*?</div>', content, re.DOTALL)
if garanti_03_re:
    new_garanti_03 = '''<div class="p-4 rounded-2xl bg-[#F7F7F8] border border-black/[0.08] text-black space-y-1">
                                <div class="font-mono text-[10px] text-neutral-500 font-medium">GARANTİ 03</div>
                                <div class="text-xs font-semibold text-black">Mutlak Mahremiyet</div>
                                <p class="text-xs text-neutral-600 font-normal">Paylaştığınız tüm bilgiler katı gizlilik politikamızla korunur.</p>
                            </div>'''
    content = content[:garanti_03_re.start()] + new_garanti_03 + content[garanti_03_re.end():]
    print("Fixed Garanti 03 card to clean light card with black text!")

# 4. FIX Service Law Badges over Photos
# Replace bg-white/10 on law badges with crisp dark badge
content = re.sub(
    r'px-2\.5 py-0\.5 rounded-full bg-white/10 truncate max-w-\[170px\]',
    'px-2.5 py-0.5 rounded-full bg-black/80 text-white font-medium backdrop-blur-md truncate max-w-[170px]',
    content
)

# 5. INJECT Explicit CSS for text-white and dark banner
css_fix = '''
        /* EXPLICIT WHITE TEXT DEFINITIONS FOR DARK ELEMENTS */
        .text-white, [class*="text-white"] {
            color: #FFFFFF !important;
        }
        .theme-dark-feature-banner,
        .theme-dark-feature-banner * {
            color: #FFFFFF !important;
        }
        .theme-dark-feature-banner h2 {
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
        }
        .theme-dark-feature-banner p {
            color: rgba(255, 255, 255, 0.85) !important;
        }
'''

content = content.replace('/* ==================================================== */\n        /* ABSOLUTE HIGH-CONTRAST', css_fix + '\n        /* ==================================================== */\n        /* ABSOLUTE HIGH-CONTRAST')

# Write to root index.html and Dat/index.html
with open(ROOT_INDEX, "w", encoding="utf-8") as f:
    f.write(content)

with open(DAT_INDEX, "w", encoding="utf-8") as f:
    f.write(content)

print("Successfully updated index.html and Dat/index.html!")
