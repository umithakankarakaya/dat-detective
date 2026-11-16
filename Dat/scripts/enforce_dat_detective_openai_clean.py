#!/usr/bin/env python3
"""
enforce_dat_detective_openai_clean.py
1. Fixes Brand Name to 'DAT Detective' everywhere (navbar logo, banner, footer, title, script, html).
2. Fixes 'Son gelişmeler' section by replacing empty gradient colored boxes with real editorial photography.
3. Completely purges all greens (#15803D, etc.) and coral/oranges (#FA7E61, #FDE2DB) from CSS and HTML.
4. Enforces high-contrast OpenAI black & white typography.
5. Fixes the unreadable black-on-black button in #kurucu.
"""

import os
import re

FILES = ["index.html", "Dat/index.html", "script.js", "Dat/script.js", "umit-hakan-karakaya.html"]

for fpath in FILES:
    if not os.path.exists(fpath):
        continue
    
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. BRAND NAME: "biz Dat Detective iz"
    content = content.replace("DAT Dedektiflik", "DAT Detective")
    content = content.replace("DAT DEDEKTİFLİK", "DAT DETECTIVE")
    content = content.replace("dat dedektiflik", "dat detective")
    
    # Navbar Logo check
    content = re.sub(
        r'<span class="text-\[17px\] font-semibold tracking-\[-0\.03em\]"[^>]*>DAT\s*<span[^>]*>[^<]+</span></span>',
        '<span class="text-[17px] font-semibold tracking-[-0.03em]" style="color: #000000 !important;">DAT <span class="font-normal text-neutral-600" style="color: #595959 !important;">Detective</span></span>',
        content
    )

    if fpath.endswith(".html"):
        # 2. SON GELİŞMELER: REAL PHOTOS
        content = re.sub(
            r'<div class="w-20 h-20 sm:w-28 sm:h-28 rounded-2xl bg-gradient-to-br from-amber-[^"]*"></div>',
            '<div class="w-20 h-20 sm:w-28 sm:h-28 rounded-2xl bg-neutral-100 border border-black/[0.08] shrink-0 overflow-hidden shadow-xs"><img src="assets/services/es-takibi.jpg" alt="Boşanma Davaları ve Dijital Delil" class="w-full h-full object-cover group-hover:scale-105 transition duration-500"></div>',
            content
        )
        content = re.sub(
            r'<div class="w-20 h-20 sm:w-28 sm:h-28 rounded-2xl bg-gradient-to-br from-blue-[^"]*"></div>',
            '<div class="w-20 h-20 sm:w-28 sm:h-28 rounded-2xl bg-neutral-100 border border-black/[0.08] shrink-0 overflow-hidden shadow-xs"><img src="assets/services/velayet-bosanma.jpg" alt="Velayet Davaları ve Yaşam Tarzı Tespiti" class="w-full h-full object-cover group-hover:scale-105 transition duration-500"></div>',
            content
        )
        content = re.sub(
            r'<div class="w-20 h-20 sm:w-28 sm:h-28 rounded-2xl bg-gradient-to-br from-emerald-[^"]*"></div>',
            '<div class="w-20 h-20 sm:w-28 sm:h-28 rounded-2xl bg-neutral-100 border border-black/[0.08] shrink-0 overflow-hidden shadow-xs"><img src="assets/photos/turkiye-romanya-isbirligi.jpg" alt="Avrupa ve Sınır Ötesi Araştırma Masası" class="w-full h-full object-cover group-hover:scale-105 transition duration-500"></div>',
            content
        )

        # 3. FIX #KURUCU SECTION SPECIFICS (Image 1)
        # Fix the invisible black-on-black button:
        content = re.sub(
            r'<a id="founderProfileLink"[^>]*class="[^"]*bg-black[^"]*text-black[^"]*"',
            '<a id="founderProfileLink" href="umit-hakan-karakaya" class="px-6 py-3 rounded-full bg-black hover:bg-neutral-800 text-white text-xs font-medium inline-flex items-center gap-2 transition shadow-sm"',
            content
        )
        content = content.replace(
            'bg-[#FA7E61] text-xs font-medium text-[#111111]',
            'bg-[#F4F4F5] border border-black/[0.08] text-xs font-medium text-black'
        )
        content = content.replace(
            'text-[10px] font-mono text-[#FA7E61] uppercase',
            'text-[10px] font-mono text-neutral-400 uppercase'
        )

        # 4. PURGE ALL ORANGE / CORAL
        content = content.replace('text-[#FA7E61]', 'text-neutral-700')
        content = content.replace('fill="#FA7E61"', 'fill="#111111"')
        content = content.replace('stroke="#FA7E61"', 'stroke="#111111"')
        content = content.replace('bg-[#FA7E61]', 'bg-[#F7F7F8] border border-black/[0.08] text-black')
        content = content.replace('style="background:#FA7E61"', 'class="bg-black text-white"')
        content = content.replace('bg-[#FDE2DB]', 'bg-[#F7F7F8] border border-black/[0.08]')
        content = content.replace('background:#FA7E61', 'background:#111111')
        content = content.replace('rgba(250, 126, 97, 0.38)', 'rgba(17, 17, 17, 0.25)')
        content = content.replace('#FA7E61', '#111111')

        # 5. PURGE ALL GREEN
        content = content.replace('color: #15803D !important;', 'color: #000000 !important;')
        content = content.replace('--dat-accent: #15803D;', '--dat-accent: #000000;')
        content = content.replace('text-[#15803D]', 'text-black')
        content = content.replace('bg-[#15803D]', 'bg-black')
        content = content.replace('hover:text-[#15803D]', 'hover:text-black')
        content = content.replace('#15803D', '#000000')

        # 6. ENFORCE STRICT HIGH CONTRAST TYPOGRAPHY
        # Make sure no strong/b tags are ever green, and all paragraphs are crisp black/gray
        strict_css = """
        /* ==================================================== */
        /* OPENAI MONOCHROME & HIGH-CONTRAST TYPOGRAPHY LOCK    */
        /* ==================================================== */
        body {
            background-color: #FFFFFF !important;
            color: #111111 !important;
        }
        strong, b {
            color: #000000 !important;
            font-weight: 600 !important;
            -webkit-text-fill-color: #000000 !important;
        }
        p {
            color: #1F2937 !important;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #000000 !important;
            -webkit-text-fill-color: #000000 !important;
        }
        """
        if "OPENAI MONOCHROME & HIGH-CONTRAST TYPOGRAPHY LOCK" not in content:
            content = content.replace('</style>', strict_css + '\n    </style>', 1)

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Processed {fpath}")
