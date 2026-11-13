/**
 * DAT Dedektiflik — Ücretsiz Google Apps Script E-Posta Webhook
 * Alıcılar: uhakankarakaya@gmail.com, umithakankarakaya@gmail.com
 *
 * Kurulum:
 * 1. https://script.google.com/home/start adresinden "Yeni proje" açın.
 * 2. Bu dosyanın tüm içeriğini editöre yapıştırıp Kaydedin.
 * 3. Üst menüden "testWebhookEmail" fonksiyonunu seçip "Çalıştır" butonuna basın
 *    ve açılan pencerede Gmail gönderim iznini onaylayın.
 * 4. Sağ üstten "Dağıt -> Yeni dağıtım" (Deploy -> New deployment):
 *    - Tür: Web uygulaması (Web app)
 *    - Yürütme (Execute as): Ben (Me)
 *    - Erişimi olanlar (Who has access): Herkes (Anyone)
 * 5. Oluşan "https://script.google.com/macros/s/.../exec" adresini kopyalayıp
 *    script.js içindeki GOOGLE_APPS_SCRIPT_WEBHOOK_URL alanına ekleyin.
 */

const RECIPIENTS = [
  "uhakankarakaya@gmail.com",
  "umithakankarakaya@gmail.com"
];

const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const INTERNAL_KEYS = new Set(["_subject", "_template", "_captcha", "_honey", "_next", "_replyto"]);

const FIELD_LABELS = {
  name: "Ad / Unvan",
  Ad_Soyad: "Ad Soyad",
  Musteri_Adi: "Müşteri Adı",
  phone: "Telefon",
  Telefon: "Telefon",
  email: "E-Posta",
  channel: "İletişim Kanalı",
  Iletisim_Kanali: "İletişim Kanalı",
  contact: "İletişim Bilgisi",
  Iletisim: "İletişim Bilgisi",
  category: "Kategori / Hizmet",
  Kategori: "Kategori / Hizmet",
  urgency: "Aciliyet Durumu",
  Aciliyet: "Aciliyet Durumu",
  message: "Mesaj / Özet",
  Detaylar: "Vaka / Talep Detayları",
  Siparis_Kodu: "Sipariş Kodu",
  Teslimat_Adresi: "Teslimat Adresi",
  Urunler: "Ürünler",
  Toplam_Tutar: "Toplam Tutar",
  page: "Gönderilen Sayfa",
  timestamp: "Gönderim Zamanı"
};

function doGet(e) {
  return jsonResponse({
    ok: true,
    service: "DAT Dedektiflik Form Webhook",
    recipients: RECIPIENTS.length
  });
}

function doPost(e) {
  try {
    const payload = parsePayload(e);

    if (payload._honey && String(payload._honey).trim() !== "") {
      return jsonResponse({ ok: true, skipped: true });
    }

    const result = sendNotificationEmail(payload);
    appendToBoundSheetIfPresent(payload, result.subject);

    return jsonResponse({
      ok: true,
      message: "Bildirim e-postası gönderildi.",
      recipients: RECIPIENTS.length
    });
  } catch (err) {
    return jsonResponse({
      ok: false,
      error: err && err.message ? err.message : String(err)
    });
  }
}

function parsePayload(e) {
  if (e && e.postData && e.postData.contents) {
    const raw = String(e.postData.contents).trim();
    if (raw.startsWith("{")) {
      return JSON.parse(raw);
    }
  }
  if (e && e.parameter && Object.keys(e.parameter).length > 0) {
    return e.parameter;
  }
  throw new Error("Form verisi alınamadı (boş istek).");
}

function sendNotificationEmail(payload) {
  const subject = String(payload._subject || "DAT Dedektiflik — Yeni Web Form Bildirimi").trim();
  const entries = buildFieldEntries(payload);

  const textLines = [
    subject,
    "----------------------------------------",
    ...entries.map(([label, val]) => `${label}: ${val}`),
    "----------------------------------------",
    `Gönderim Zamanı: ${Utilities.formatDate(new Date(), "Europe/Istanbul", "dd.MM.yyyy HH:mm:ss")}`
  ];

  const rowsHtml = entries.map(([label, val]) => `
    <tr>
      <td style="padding:12px 16px;border-bottom:1px solid #262626;color:#9CA3AF;font-size:13px;font-weight:600;width:34%;vertical-align:top;">
        ${escapeHtml(label)}
      </td>
      <td style="padding:12px 16px;border-bottom:1px solid #262626;color:#F3F4F6;font-size:14px;line-height:1.5;white-space:pre-wrap;vertical-align:top;">
        ${escapeHtml(val)}
      </td>
    </tr>
  `).join("");

  const sentAt = Utilities.formatDate(new Date(), "Europe/Istanbul", "dd.MM.yyyy HH:mm:ss");
  const htmlBody = `
    <div style="background:#0B0B0B;padding:28px 16px;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;">
      <div style="max-width:620px;margin:0 auto;background:#141414;border:1px solid #262626;border-radius:16px;overflow:hidden;">
        <div style="background:#111111;padding:20px 24px;border-bottom:2px solid #93F051;">
          <div style="color:#93F051;font-size:11px;font-weight:700;letter-spacing:1.6px;text-transform:uppercase;margin-bottom:6px;">
            DAT DEDEKTİFLİK • GİZLİ İLETİ
          </div>
          <div style="color:#FFFFFF;font-size:18px;font-weight:700;line-height:1.3;">
            ${escapeHtml(subject)}
          </div>
        </div>
        <table style="width:100%;border-collapse:collapse;background:#141414;">
          ${rowsHtml}
        </table>
        <div style="padding:14px 24px;background:#101010;color:#6B7280;font-size:12px;border-top:1px solid #222222;">
          Alıcı zaman damgası (İstanbul): ${escapeHtml(sentAt)}
        </div>
      </div>
    </div>
  `;

  const mailOptions = {
    to: RECIPIENTS.join(","),
    subject: subject,
    body: textLines.join("\n"),
    htmlBody: htmlBody,
    name: "DAT Dedektiflik Web Formu"
  };

  const replyCandidate = String(payload._replyto || payload.email || payload.Eposta || "").trim();
  if (EMAIL_REGEX.test(replyCandidate)) {
    mailOptions.replyTo = replyCandidate;
  }

  MailApp.sendEmail(mailOptions);
  return { subject };
}

function buildFieldEntries(payload) {
  const entries = [];
  Object.keys(payload).forEach((key) => {
    if (INTERNAL_KEYS.has(key)) return;
    const rawVal = payload[key];
    if (rawVal === null || rawVal === undefined) return;
    const strVal = String(rawVal).trim();
    if (!strVal) return;
    const label = FIELD_LABELS[key] || key.replace(/_/g, " ");
    entries.push([label, strVal]);
  });
  return entries;
}

function appendToBoundSheetIfPresent(payload, subject) {
  try {
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    if (!ss) return;
    const sheetName = "Form_Kayitlari";
    let sheet = ss.getSheetByName(sheetName);
    if (!sheet) {
      sheet = ss.insertSheet(sheetName);
      sheet.appendRow(["Tarih (İstanbul)", "Konu", "Ad / Müşteri", "İletişim", "Detay JSON"]);
    }
    const timestamp = Utilities.formatDate(new Date(), "Europe/Istanbul", "dd.MM.yyyy HH:mm:ss");
    const sender = String(payload.name || payload.Musteri_Adi || payload.Ad_Soyad || "-");
    const contact = String(payload.contact || payload.Iletisim || payload.Telefon || payload.phone || "-");
    sheet.appendRow([timestamp, subject, sender, contact, JSON.stringify(payload)]);
  } catch (sheetErr) {
    Logger.log("Sheet kaydı atlandı: " + sheetErr);
  }
}

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function jsonResponse(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}

/**
 * Kurulum sonrası izin vermek ve mail teslimini hemen denemek için
 * Apps Script editöründen bu fonksiyonu seçip Çalıştır'a basın.
 */
function testWebhookEmail() {
  const result = sendNotificationEmail({
    _subject: "DAT Dedektiflik — Webhook Test Bildirimi",
    name: "Sistem Testi",
    channel: "Google Apps Script",
    contact: "uhakankarakaya@gmail.com",
    category: "Kurulum Doğrulaması",
    urgency: "Normal",
    message: "Bu e-posta Google Apps Script webhook kurulumunun başarıyla çalıştığını doğrulamak için gönderildi."
  });
  Logger.log("Test e-postası gönderildi: " + result.subject);
}
