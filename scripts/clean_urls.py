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
DOMAIN = "https://www.datdedektiflik.com"
SKIP_DIRS = {"_archive_raw", "node_modules", ".git", "yeni-medya", "Dat Evraklar", "functions", "src"}

# 1) Mutlak site adresleri: https://www.datdedektiflik.com/x/y.html -> /x/y ; /x/index.html -> /x/
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


def normalize_text(text, is_html):
    out = ABS_RE.sub(_abs_sub, text)
    if is_html:
        out = REL_RE.sub(_rel_sub, out)
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
