# -*- coding: utf-8 -*-
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. <html> etiketini light moda al
html = html.replace(
    '<html lang="tr" class="scroll-smooth dark" data-theme="dark">',
    '<html lang="tr" class="scroll-smooth light" data-theme="light">'
)
html = html.replace(
    '<html lang="tr" class="scroll-smooth dark">',
    '<html lang="tr" class="scroll-smooth light" data-theme="light">'
)

# 2. Theme init script: Varsayılan temayı light yap
theme_init_old = """            var saved = localStorage.getItem('dat_theme');
            var theme = saved || 'dark';"""

theme_init_new = """            var saved = localStorage.getItem('dat_theme');
            var theme = saved || 'light';"""

html = html.replace(theme_init_old, theme_init_new)

# 3. <body> etiketini temiz beyaz yap
html = html.replace(
    '<body class="bg-[#111111] text-[#FFFFFF] font-sans antialiased overflow-x-hidden selection:bg-[#93F051] selection:text-[#111111]">',
    '<body class="bg-[#FFFFFF] text-[#000000] font-sans antialiased overflow-x-hidden selection:bg-black selection:text-white">'
)

# 4. OpenAI Global CSS kurallarını enforce et
openai_force_css = """
    <style id="openai-strict-palette">
        :root, html, body {
            background-color: #FFFFFF !important;
            color: #000000 !important;
            font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
        }

        #dedektife-sor {
            background-color: #FFFFFF !important;
            color: #000000 !important;
        }

        #dedektife-sor h1 {
            color: #000000 !important;
            font-weight: 500 !important;
            letter-spacing: -0.03em !important;
        }

        #dedektife-sor p {
            color: #595959 !important;
        }

        /* OpenAI Hero Input Box */
        .openai-console-box {
            background-color: #FFFFFF !important;
            border: 1px solid rgba(0, 0, 0, 0.14) !important;
            border-radius: 28px !important;
            box-shadow: 0 2px 14px rgba(0, 0, 0, 0.04) !important;
        }
        .openai-console-box:focus-within {
            border-color: rgba(0, 0, 0, 0.35) !important;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08) !important;
        }

        /* OpenAI Prompt Pills */
        .openai-prompt-pill {
            background-color: #FFFFFF !important;
            border: 1px solid rgba(0, 0, 0, 0.12) !important;
            color: #000000 !important;
            border-radius: 9999px !important;
            font-size: 13px !important;
            font-weight: 400 !important;
            padding: 6px 14px !important;
            transition: all 0.15s ease !important;
        }
        .openai-prompt-pill:hover {
            background-color: rgba(0, 0, 0, 0.04) !important;
            border-color: rgba(0, 0, 0, 0.20) !important;
        }

        /* OpenAI Circular Send Button */
        .openai-send-btn {
            background-color: #000000 !important;
            color: #FFFFFF !important;
            width: 32px !important;
            height: 32px !important;
            border-radius: 50% !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            border: none !important;
            cursor: pointer !important;
        }
        .openai-send-btn:hover {
            background-color: #262626 !important;
        }

        /* OpenAI Featured Cards */
        .openai-featured-card {
            background-color: #FFFFFF !important;
            border: 1px solid rgba(0, 0, 0, 0.10) !important;
            border-radius: 24px !important;
        }
        .openai-featured-card:hover {
            border-color: rgba(0, 0, 0, 0.22) !important;
            box-shadow: 0 4px 18px rgba(0, 0, 0, 0.04) !important;
        }
    </style>
"""

if 'id="openai-strict-palette"' not in html:
    html = html.replace('</head>', openai_force_css + '\n</head>')

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
with open("Dat/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✓ index.html ve Dat/index.html OpenAI saf beyaz temaya kilitlendi!")
