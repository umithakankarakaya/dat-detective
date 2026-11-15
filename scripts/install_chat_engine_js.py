#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

CHAT_JS_CODE = '''// 10. Yeni Nesil Dedektif'e Sor (Canlı Adli Chat Alanı)
let aiChatInitialized = false;

function _getCurrentTimeStr() {
    const now = new Date();
    return String(now.getHours()).padStart(2, '0') + ':' + String(now.getMinutes()).padStart(2, '0');
}

function initAIChat() {
    const container = document.getElementById('aiChatMessages');
    if (!container) return;
    
    // Setup initial welcome bubble if empty
    if (!container.hasChildNodes() || container.children.length === 0) {
        resetAIChat();
    }

    const input = document.getElementById('aiChatInput');
    if (input && !input.dataset.listenerAttached) {
        input.dataset.listenerAttached = 'true';
        input.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = Math.min(this.scrollHeight, 120) + 'px';
        });
        input.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendAIChatMessage();
            }
        });
    }
    aiChatInitialized = true;
}

function resetAIChat() {
    const container = document.getElementById('aiChatMessages');
    if (!container) return;
    const timeStr = _getCurrentTimeStr();

    container.innerHTML = `
        <div class="flex items-start gap-3 text-left animate-fadeIn">
            <img src="assets/photos/elsa-dedektif-asistan.jpg" alt="Elsa & Ümit Hakan Karakaya" class="w-8 h-8 rounded-full border border-[#93F051]/50 object-cover object-top shrink-0 mt-1 shadow-sm">
            <div class="bg-[#111111] border border-white/10 rounded-2xl rounded-tl-sm p-4 sm:p-5 text-white max-w-[95%] sm:max-w-[85%] space-y-3.5 shadow-lg">
                <div class="flex items-center justify-between pb-2 border-b border-white/10">
                    <div class="flex items-center gap-1.5">
                        <span class="text-xs font-medium text-white">Yeni Nesil Dedektif (Elsa &amp; Ümit Hakan Karakaya)</span>
                        <span class="w-1.5 h-1.5 rounded-full bg-[#93F051]"></span>
                    </div>
                    <span class="text-[10px] font-mono text-white/40">${timeStr}</span>
                </div>
                <div class="text-xs sm:text-[13px] leading-relaxed text-white/85 space-y-2">
                    <p>Merhaba! Ben DAT Özel Dedektiflik'in Yeni Nesil Dijital Asistanı <strong>Elsa</strong>. Kurucumuz <strong>Ümit Hakan Karakaya</strong>'nın 20 yılı aşkın dedektiflik ve adli bilişim tecrübesiyle buradayım.</p>
                    <p>Burada kuruntuları körükleyen sahte şüphe oranları veya yankı odası tuzaklarına yer yok. Dosyanızı dürüst, rasyonel ve <strong>HMK m.199 / TCK m.134</strong> yasal sınırları içinde değerlendiriyoruz.</p>
                    <p class="text-[#93F051] font-medium pt-1">Aşağıdaki popüler başlıklardan birine tıklayarak anında yanıt alabilir veya sorunuzu doğrudan yazıp <strong>"Yeni Nesil Dedektif'e Sor"</strong> butonuna basabilirsiniz:</p>
                </div>
                <div class="flex flex-wrap gap-1.5 pt-1">
                    <button type="button" onclick="selectAIChatPreset('dedektif-tutmak')" class="px-2.5 py-1.5 rounded-lg bg-white/5 hover:bg-[#93F051]/15 text-white/85 hover:text-[#93F051] border border-white/10 hover:border-[#93F051]/40 text-xs transition">🕵️‍♂️ Dedektif Tutmak Yasal mı?</button>
                    <button type="button" onclick="selectAIChatPreset('dedektif-ucretleri')" class="px-2.5 py-1.5 rounded-lg bg-white/5 hover:bg-[#93F051]/15 text-white/85 hover:text-[#93F051] border border-white/10 hover:border-[#93F051]/40 text-xs transition">💳 Ücretler Nasıl Belirlenir?</button>
                    <button type="button" onclick="selectAIChatPreset('delil-gecerliligi')" class="px-2.5 py-1.5 rounded-lg bg-white/5 hover:bg-[#93F051]/15 text-white/85 hover:text-[#93F051] border border-white/10 hover:border-[#93F051]/40 text-xs transition">⚖️ Deliller Mahkemede Geçerli mi?</button>
                    <button type="button" onclick="selectAIChatPreset('almanya-es-takibi')" class="px-2.5 py-1.5 rounded-lg bg-white/5 hover:bg-[#93F051]/15 text-white/85 hover:text-[#93F051] border border-white/10 hover:border-[#93F051]/40 text-xs transition">🇩🇪 Almanya/Avrupa Eş Takibi</button>
                    <button type="button" onclick="selectAIChatPreset('aldatan-erkek')" class="px-2.5 py-1.5 rounded-lg bg-white/5 hover:bg-[#93F051]/15 text-white/85 hover:text-[#93F051] border border-white/10 hover:border-[#93F051]/40 text-xs transition">💔 Eş Takibi &amp; Aldatma Tespiti</button>
                </div>
            </div>
        </div>
    `;
    _scrollAIChatToBottom();
}

function _scrollAIChatToBottom() {
    const container = document.getElementById('aiChatMessages');
    if (container) {
        setTimeout(() => {
            container.scrollTo({ top: container.scrollHeight, behavior: 'smooth' });
        }, 50);
    }
}

function selectAIChatPreset(key) {
    if (AI_PRESETS[key]) {
        currentAIPreset = key;
        sendAIChatMessage(AI_PRESETS[key].query, key);
    }
}

// Backwards compatibility alias
function selectAIPreset(key) {
    selectAIChatPreset(key);
}

function sendAIChatMessage(overrideQuery, explicitPresetKey) {
    const container = document.getElementById('aiChatMessages');
    const input = document.getElementById('aiChatInput');
    const sendBtn = document.getElementById('aiSendBtn');

    const rawQuery = (typeof overrideQuery === 'string' && overrideQuery.trim().length > 0) 
        ? overrideQuery.trim() 
        : (input ? input.value.trim() : '');

    if (!rawQuery) {
        if (input) input.focus();
        return;
    }

    if (input) {
        input.value = '';
        input.style.height = 'auto';
    }

    if (!container) return;

    const timeStr = _getCurrentTimeStr();

    // 1. Render User Message Bubble
    const escapedQuery = rawQuery.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    const userBubble = document.createElement('div');
    userBubble.className = 'flex justify-end text-right animate-fadeIn';
    userBubble.innerHTML = `
        <div class="bg-[#242426] border border-[#93F051]/30 rounded-2xl rounded-tr-sm p-3.5 sm:p-4 text-white max-w-[85%] sm:max-w-[75%] space-y-1 shadow-md">
            <div class="text-[10px] font-mono text-[#93F051] flex items-center justify-end gap-1">
                <span>Siz</span>
                <span>•</span>
                <span>${timeStr}</span>
            </div>
            <p class="text-xs sm:text-[13px] leading-relaxed text-left text-white/95">${escapedQuery}</p>
        </div>
    `;
    container.appendChild(userBubble);
    _scrollAIChatToBottom();

    // 2. Render Typing Indicator
    const typingIndicator = document.createElement('div');
    typingIndicator.id = 'aiTypingIndicator';
    typingIndicator.className = 'flex items-start gap-3 text-left animate-fadeIn';
    typingIndicator.innerHTML = `
        <img src="assets/photos/elsa-dedektif-asistan.jpg" alt="Elsa & Ümit Hakan Karakaya" class="w-8 h-8 rounded-full border border-[#93F051]/50 object-cover object-top shrink-0 mt-1 shadow-sm">
        <div class="bg-[#111111] border border-white/10 rounded-2xl rounded-tl-sm px-4 py-3 text-white flex items-center gap-2.5 shadow-sm">
            <span class="text-xs text-white/70">Yeni Nesil Dedektif yanıt hazırlıyor</span>
            <span class="inline-flex gap-1 items-center">
                <span class="w-1.5 h-1.5 rounded-full bg-[#93F051] animate-bounce"></span>
                <span class="w-1.5 h-1.5 rounded-full bg-[#93F051] animate-bounce [animation-delay:0.15s]"></span>
                <span class="w-1.5 h-1.5 rounded-full bg-[#93F051] animate-bounce [animation-delay:0.3s]"></span>
            </span>
        </div>
    `;
    container.appendChild(typingIndicator);
    _scrollAIChatToBottom();

    if (sendBtn) sendBtn.disabled = true;

    // 3. Process matched data
    const query = rawQuery.toLowerCase();
    let matchedKey = explicitPresetKey || null;

    if (!matchedKey) {
        if (query.includes('ücret') || query.includes('ucret') || query.includes('fiyat') || query.includes('ne kadar') || query.includes('maliyet') || query.includes('kaç para')) {
            matchedKey = 'dedektif-ucretleri';
        } else if (query.includes('dedektif olmak') || query.includes('nasıl dedektif') || query.includes('eğitim') || query.includes('sertifika') || query.includes('uöded') || query.includes('meslek')) {
            matchedKey = 'dedektif-olmak';
        } else if (query.includes('dedektif tutmak') || query.includes('nasıl tutulur') || query.includes('sözleşme') || query.includes('güvenilir')) {
            matchedKey = 'dedektif-tutmak';
        } else if (query.includes('tatil') || query.includes('antalya') || query.includes('bodrum') || query.includes('otel') || query.includes('seyahat')) {
            matchedKey = 'tatilde-aldatma';
        } else if (query.includes('miras') || query.includes('borç') || query.includes('borc') || query.includes('adres') || query.includes('tapu') || query.includes('gayrimenkul')) {
            matchedKey = 'miras-borclu';
        } else if (query.includes('nafaka') || query.includes('gelir') || query.includes('şirket') || query.includes('sirket')) {
            matchedKey = 'nafaka-gelir';
        } else if (query.includes('delil') || query.includes('mahkeme') || query.includes('yasal') || query.includes('geçerli') || query.includes('kanun') || query.includes('hukuk')) {
            matchedKey = 'delil-gecerliligi';
        } else if (query.includes('erkek') || query.includes('aldat') || query.includes('belirti') || query.includes('işaret') || query.includes('eş takibi') || query.includes('es takibi')) {
            matchedKey = 'aldatan-erkek';
        } else if (query.includes('almanya') || query.includes('avusturya') || query.includes('fransa') || query.includes('belçika') || query.includes('yurt dışı') || query.includes('gurbet')) {
            matchedKey = 'almanya-es-takibi';
        }
    }

    let data;
    const isCustom = Boolean(rawQuery && rawQuery.length > 5 && !explicitPresetKey);

    if (matchedKey && AI_PRESETS[matchedKey]) {
        data = Object.assign({}, AI_PRESETS[matchedKey]);
        if (isCustom) {
            data.waText = `Merhaba Ümit Bey, web sitenizdeki Yeni Nesil Dedektif (Dedektif'e Sor) alanından yazıyorum.\\n\\nSorum: "${rawQuery}"\\n\\nBu konu hakkında dürüst ve objektif hukuki danışmanlık almak istiyorum.`;
        }
    } else if (isCustom) {
        data = {
            query: rawQuery,
            riskScore: "DÜRÜST & OBJEKTİF ÖN DEĞERLENDİRME",
            riskColor: "#93F051",
            p1Title: "1. YANKI ODASINDAN UZAK RASYONEL DEĞERLENDİRME",
            p1Desc: `Belirttiğiniz durum ("${rawQuery.slice(0, 75)}..."), kuruntuları körükleyen değil, soğukkanlı ve rasyonel bir süzgeçten geçirilmelidir. İnsan psikolojisi şüphe anında yalnızca kendi endişesini doğrulayan işaretleri görme eğilimindedir (yankı odası etkisi). Oysa kurucumuz Ümit Hakan Karakaya'nın 20 yılı aşkın tecrübesi gösterir ki; somut kanıt olmadan peşin hüküm vermek ve fevri adımlar atmak hem maddi kayba hem de hak kaybına yol açar.`,
            p2Title: "2. DÜRÜST HUKUKİ GERÇEKLER & MEŞRU DELİL SINIRI (HMK m.199)",
            p2Desc: "İnternette vadedilen telefon casus yazılımları, WhatsApp sızmaları veya ortam dinlemeleri TCK m.134 kapsamında hapis cezası gerektiren suçlardır ve mahkemelerde aleyhinize döner. Gerçek dedektiflik; yalnızca kamuya açık alanlarda, konut ve özel hayat dokunulmazlığını ihlal etmeden HMK m.199 standartlarında 4K tarih-saat damgalı yasal delil üretmektir.",
            p3Items: [
                { bad: true, label: "Fevri Yüzleşmeden Kaçının", text: "Elinizde resmi delil olmadan karşı tarafla yüzleşmek yalnızca delillerin karartılmasına ve savunma geliştirmesine yarar." },
                { bad: true, label: "Gereksiz Masrafa Girmeyin", text: "Her şüphede dedektif tutulmaz; önce hukuki altyapının ve somut riskin varlığı netleştirilmelidir." },
                { bad: false, label: "Ümit Hakan Karakaya ile Doğrudan Görüşün", text: "Dosyanızın dedektiflik çalışmasına uygun olup olmadığını dürüst bir ön görüşmeyle ücretsiz analiz edelim." }
            ],
            waText: `Merhaba Ümit Bey, web sitenizdeki Yeni Nesil Dedektif (Dedektif'e Sor) alanından yazıyorum.\\n\\nSorum / Durumum: "${rawQuery}"\\n\\nBu konu hakkında dürüst ve objektif hukuki danışmanlık almak istiyorum.`
        };
    } else {
        data = Object.assign({}, AI_PRESETS[currentAIPreset] || AI_PRESETS['dedektif-tutmak']);
    }

    setTimeout(() => {
        const ind = document.getElementById('aiTypingIndicator');
        if (ind) ind.remove();

        if (sendBtn) sendBtn.disabled = false;

        const p3ItemsHtml = (data.p3Items || []).map(item => `
            <li class="flex items-start gap-1.5 ${item.bad ? 'text-rose-300' : 'text-[#93F051]'} text-xs">
                <span class="font-bold">${item.bad ? '✕' : '✓'}</span>
                <span><strong>${item.label}:</strong> <span class="text-white/80">${item.text}</span></span>
            </li>
        `).join('');

        const respBubble = document.createElement('div');
        respBubble.className = 'flex items-start gap-3 text-left animate-fadeIn';
        respBubble.innerHTML = `
            <img src="assets/photos/elsa-dedektif-asistan.jpg" alt="Elsa & Ümit Hakan Karakaya" class="w-8 h-8 rounded-full border border-[#93F051]/50 object-cover object-top shrink-0 mt-1 shadow-sm">
            <div class="bg-[#111111] border border-white/10 rounded-2xl rounded-tl-sm p-4 sm:p-5 text-white max-w-[95%] sm:max-w-[85%] space-y-3.5 shadow-lg">
                <div class="flex flex-wrap items-center justify-between gap-2 pb-2.5 border-b border-white/10">
                    <div class="flex items-center gap-1.5">
                        <span class="text-xs font-medium text-white">Yeni Nesil Dedektif (Elsa &amp; Ümit Hakan Karakaya)</span>
                        <span class="w-1.5 h-1.5 rounded-full bg-[#93F051]"></span>
                    </div>
                    <span class="px-2 py-0.5 rounded-full bg-[#93F051]/15 border border-[#93F051]/30 text-[#93F051] text-[9.5px] font-mono font-medium">${data.riskScore || 'DÜRÜST HUKUKİ ANALİZ'}</span>
                </div>
                
                <div class="space-y-2.5 text-xs sm:text-[13px] leading-relaxed">
                    <div class="space-y-1">
                        <div class="text-[#93F051] font-medium text-xs flex items-center gap-1.5">
                            <i class="hgi hgi-stroke hgi-alert-circle w-3.5 h-3.5"></i>
                            <span>${data.p1Title}</span>
                        </div>
                        <p class="text-white/80">${data.p1Desc}</p>
                    </div>

                    <div class="space-y-1">
                        <div class="text-[#93F051] font-medium text-xs flex items-center gap-1.5">
                            <i class="hgi hgi-stroke hgi-justice-scale-01 w-3.5 h-3.5"></i>
                            <span>${data.p2Title}</span>
                        </div>
                        <p class="text-white/80">${data.p2Desc}</p>
                    </div>

                    <div class="space-y-1">
                        <div class="text-[#93F051] font-medium text-xs flex items-center gap-1.5">
                            <i class="hgi hgi-stroke hgi-shield-alert w-3.5 h-3.5"></i>
                            <span>3. DÜRÜST DEDEKTİFLİK VE KORUYUCU TAVSİYELER</span>
                        </div>
                        <ul class="space-y-1 pt-0.5">
                            ${p3ItemsHtml}
                        </ul>
                    </div>
                </div>

                <div class="pt-2.5 border-t border-white/10 flex flex-wrap items-center justify-between gap-2">
                    <span class="text-[10px] text-white/50 font-mono">${timeStr} • HMK m.199 &amp; TCK m.134 Uyumlu</span>
                    <a href="https://wa.me/905326667749?text=${encodeURIComponent(data.waText)}" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-[#25D366] hover:bg-[#20ba59] text-[#111111] font-medium text-xs transition">
                        <i class="hgi hgi-stroke hgi-whatsapp w-3.5 h-3.5"></i>
                        <span>Ümit Hakan Karakaya'ya WhatsApp'tan Sorun</span>
                    </a>
                </div>
            </div>
        `;
        container.appendChild(respBubble);
        _scrollAIChatToBottom();

        // Track event
        if (window.DATAnalytics) {
            window.DATAnalytics.trackEvent('ai_detective_chat', {
                preset: matchedKey || 'custom',
                hasCustomQuery: isCustom
            });
        }
    }, 550);
}

// Backwards compatibility alias
function runDetectiveAI() {
    sendAIChatMessage();
}

// Boot AI chat on ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAIChat);
} else {
    initAIChat();
}
'''

def update_script_files():
    for fpath in ["script.js", "Dat/script.js"]:
        full_path = os.path.join(BASE_DIR, fpath)
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Replace from `function selectAIPreset` down to `runDetectiveAI` function end
        old_pattern = re.compile(r'function selectAIPreset\(key\)\s*\{[\s\S]*?function runDetectiveAI\(\)\s*\{[\s\S]*?\n\}', re.MULTILINE)
        if old_pattern.search(content):
            content = old_pattern.sub(CHAT_JS_CODE.strip(), content)
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Updated {fpath} with Chat Engine.")
        else:
            print(f"Pattern not found in {fpath}!")

if __name__ == "__main__":
    update_script_files()
