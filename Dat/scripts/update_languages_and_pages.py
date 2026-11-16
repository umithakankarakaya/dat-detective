#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import shutil

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

LANG_HERO_CASES = {
    "en": {
        "code_badge": "LEGAL EVIDENCE STANDARD • HMK m.199 & TCK m.134",
        "title": "Spouse Surveillance & Family Law Evidence Standards",
        "lawBadge": "TCC Art. 161 / CCP Art. 199",
        "timestamp": "LEGAL PROCEDURE",
        "proc_title": "FORENSIC WORKFLOW & PROCEDURE",
        "metric1_label": "EVIDENCE",
        "metric1_val": "4K Visual Proof",
        "metric2_label": "CHAIN",
        "metric2_val": "Timestamped Chain",
        "metric3_label": "VALIDITY",
        "metric3_val": "Court-Admissible",
        "timeline": [
            ("STAGE 01", "A formal service contract, authorization, and strict KVKK/GDPR confidentiality protocol are signed to open the file."),
            ("STAGE 02", "With strict adherence to privacy rights, observations are conducted solely in public open spaces."),
            ("STAGE 03", "Timestamped 4K visual evidence and certified investigator reports are delivered directly to your legal counsel.")
        ],
        "dict_additions": {
            "ADLİ DELİL STANDARDI • HMK m.199 & TCK m.134": "LEGAL EVIDENCE STANDARD • HMK m.199 & TCK m.134",
            "Eş Takibi & Aile Hukuku Delil Standartları": "Spouse Surveillance & Family Law Evidence Standards",
            "HMK m.199 UYUMLU": "HMK m.199 COMPLIANT",
            "ADLİ İŞLEYİŞ VE PROSEDÜR": "FORENSIC WORKFLOW & PROCEDURE",
            "AŞAMA 01": "STAGE 01",
            "Resmi hizmet sözleşmesi, vekalet ve KVKK gizlilik protokolü imzalanarak dosya açılır.": "A formal service contract, authorization, and strict confidentiality protocol are signed to open the file.",
            "AŞAMA 02": "STAGE 02",
            "Konut ve özel hayat dokunulmazlığına tam riayet edilerek yalnızca kamuya açık alanlarda tespit icra edilir.": "With strict adherence to privacy rights, observations are conducted solely in public open spaces.",
            "AŞAMA 03": "STAGE 03",
            "Zaman damgalı 4K görsel deliller ve resmi dedektif tutanağı doğrudan avukatınıza teslim edilir.": "Timestamped 4K visual evidence and certified investigator reports are delivered directly to your legal counsel."
        },
        "heroCases_code": """    heroCases: {
        sadakat: {
            code: 'LEGAL FRAMEWORK • FAMILY LAW & FIDELITY',
            title: 'Spouse Surveillance & Family Law Evidence Standards',
            lawBadge: 'TCC Art. 161 / CCP Art. 199',
            metric1: '4K Visual Evidence',
            metric2: 'Timestamped Chain',
            metric3: 'Court-Admissible',
            timestamp: 'LEGAL PROCEDURE',
            logs: [
                { time: 'STAGE 01', text: 'A formal service contract, authorization, and strict KVKK/GDPR confidentiality protocol are signed to open the file.', highlight: false },
                { time: 'STAGE 02', text: 'With strict adherence to privacy rights, observations are conducted solely in public open spaces.', highlight: false },
                { time: 'STAGE 03', text: 'Timestamped 4K visual evidence and certified investigator reports are delivered directly to your legal counsel.', highlight: true }
            ]
        },
        tscm: {
            code: 'LEGAL FRAMEWORK • CUSTODY & DIVORCE',
            title: 'Custody Proceedings & Child Best Interest',
            lawBadge: 'TCC Art. 182 / FAMILY LAW',
            metric1: 'Living Conditions',
            metric2: 'Official Report',
            metric3: 'Court-Ready',
            timestamp: 'FORENSIC STANDARD',
            logs: [
                { time: 'STAGE 01', text: 'Statutory inquiries are launched to establish factual circumstances impacting child safety and emotional welfare.', highlight: false },
                { time: 'STAGE 02', text: 'Parental lifestyle and care compliance are documented within civil and criminal law boundaries.', highlight: false },
                { time: 'STAGE 03', text: 'An official evidence folder is compiled for evaluation by the Family Court judge.', highlight: true }
            ]
        },
        kurumsal: {
            code: 'LEGAL FRAMEWORK • DEBTORS & ASSETS',
            title: 'Actual Address & Debtor Asset Verification',
            lawBadge: 'EBL Art. 277 / ASSET TRACE',
            metric1: '81 Provinces & Global',
            metric2: 'Physical Residence Check',
            metric3: 'Enforcement Proof',
            timestamp: 'OFFICIAL REPORT',
            logs: [
                { time: 'STAGE 01', text: 'Lawful field investigation is initiated for elusive debtors unreachable for formal service.', highlight: false },
                { time: 'STAGE 02', text: 'Actual residence, commercial operations, and assets concealed or transferred to third parties are documented.', highlight: false },
                { time: 'STAGE 03', text: 'Certified verification reports are submitted for direct debt enforcement and fraudulent conveyance suits.', highlight: true }
            ]
        }
    },"""
    },
    "de": {
        "code_badge": "RECHTLICHER BEWEISSTANDARD • HMK § 199 & TCK § 134",
        "title": "Partnerobservation & Beweisstandards im Familienrecht",
        "lawBadge": "TMK § 161 / HMK § 199",
        "timestamp": "GESETZLICHES VERFAHREN",
        "proc_title": "GERICHTLICHES VERFAHREN & ABLAUF",
        "metric1_label": "BEWEIS",
        "metric1_val": "4K Bildbeweis",
        "metric2_label": "KETTE",
        "metric2_val": "Zeitstempel-Kette",
        "metric3_label": "GÜLTIGKEIT",
        "metric3_val": "Gerichtsverwertbar",
        "timeline": [
            ("STUFE 01", "Eröffnung der Akte nach Unterzeichnung von Dienstvertrag, Vollmacht und strengem Datenschutzprotokoll (DSGVO)."),
            ("STUFE 02", "Rechtskonforme Observation ausschließlich im öffentlichen Raum unter strikter Wahrung der Privatsphäre."),
            ("STUFE 03", "Übergabe zeitgestempelter 4K-Bildbeweise und offizieller Ermittlungsberichte direkt an Ihren Rechtsbeistand.")
        ],
        "dict_additions": {
            "ADLİ DELİL STANDARDI • HMK m.199 & TCK m.134": "RECHTLICHER BEWEISSTANDARD • HMK § 199 & TCK § 134",
            "Eş Takibi & Aile Hukuku Delil Standartları": "Partnerobservation & Beweisstandards im Familienrecht",
            "HMK m.199 UYUMLU": "HMK § 199 KONFORM",
            "ADLİ İŞLEYİŞ VE PROSEDÜR": "GERICHTLICHES VERFAHREN & ABLAUF",
            "AŞAMA 01": "STUFE 01",
            "Resmi hizmet sözleşmesi, vekalet ve KVKK gizlilik protokolü imzalanarak dosya açılır.": "Eröffnung der Akte nach Unterzeichnung von Dienstvertrag, Vollmacht und strengem Datenschutzprotokoll.",
            "AŞAMA 02": "STUFE 02",
            "Konut ve özel hayat dokunulmazlığına tam riayet edilerek yalnızca kamuya açık alanlarda tespit icra edilir.": "Rechtskonforme Observation ausschließlich im öffentlichen Raum unter strikter Wahrung der Privatsphäre.",
            "AŞAMA 03": "STUFE 03",
            "Zaman damgalı 4K görsel deliller ve resmi dedektif tutanağı doğrudan avukatınıza teslim edilir.": "Übergabe zeitgestempelter 4K-Bildbeweise und offizieller Ermittlungsberichte direkt an Ihren Rechtsbeistand."
        },
        "heroCases_code": """    heroCases: {
        sadakat: {
            code: 'RECHTLICHER RAHMEN • FAMILIENRECHT & TREUE',
            title: 'Partnerobservation & Beweisstandards im Familienrecht',
            lawBadge: 'TMK § 161 / HMK § 199',
            metric1: '4K Bildbeweis',
            metric2: 'Zeitstempel-Kette',
            metric3: 'Gerichtsverwertbar',
            timestamp: 'GESETZLICHES VERFAHREN',
            logs: [
                { time: 'STUFE 01', text: 'Eröffnung der Akte nach Unterzeichnung von Dienstvertrag, Vollmacht und strengem Datenschutzprotokoll (DSGVO).', highlight: false },
                { time: 'STUFE 02', text: 'Rechtskonforme Observation ausschließlich im öffentlichen Raum unter strikter Wahrung der Privatsphäre.', highlight: false },
                { time: 'STUFE 03', text: 'Übergabe zeitgestempelter 4K-Bildbeweise und offizieller Ermittlungsberichte direkt an Ihren Rechtsbeistand.', highlight: true }
            ]
        },
        tscm: {
            code: 'RECHTLICHER RAHMEN • SORGERECHT & SCHEIDUNG',
            title: 'Sorgerechtsprozesse & Kindeswohl-Beweise',
            lawBadge: 'TMK § 182 / FAMILIENRECHT',
            metric1: 'Lebensbedingungen',
            metric2: 'Offizieller Bericht',
            metric3: 'Gerichtsverwertbar',
            timestamp: 'FORENSISCHER STANDARD',
            logs: [
                { time: 'STUFE 01', text: 'Einleitung rechtlicher Recherchen zur Dokumentation von Faktoren bezüglich Kindeswohl und Sicherheit.', highlight: false },
                { time: 'STUFE 02', text: 'Dokumentation des realen Lebenswandels und der Fürsorgepflichten im Rahmen des Zivil- und Strafrechts.', highlight: false },
                { time: 'STUFE 03', text: 'Erstellung eines offiziellen Beweisdossiers zur Vorlage beim Familiengericht.', highlight: true }
            ]
        },
        kurumsal: {
            code: 'RECHTLICHER RAHMEN • SCHULDNER & VERMÖGEN',
            title: 'Tatsächliche Adresse & Schuldnervermögen',
            lawBadge: 'İİK § 277 / ERMITTLUNG',
            metric1: '81 Provinzen & Ausland',
            metric2: 'Wohnsitz-Verifikation',
            metric3: 'Vollstreckungsbeweis',
            timestamp: 'AMTLICHER BERICHT',
            logs: [
                { time: 'STUFE 01', text: 'Einleitung gesetzeskonformer Recherchen zu Schuldnern, die an der Meldeadresse unauffindbar sind.', highlight: false },
                { time: 'STUFE 02', text: 'Ermittlung des tatsächlichen Wohnsitzes, wirtschaftlicher Aktivitäten und auf Dritte übertragener Vermögenswerte.', highlight: false },
                { time: 'STUFE 03', text: 'Übergabe eines zertifizierten Ermittlungsberichts für Vollstreckungsverfahren und Anfechtungsklagen.', highlight: true }
            ]
        }
    },"""
    },
    "fr": {
        "code_badge": "STANDARD DE PREUVE JURIDIQUE • HMK art. 199 & TCK art. 134",
        "title": "Filature Conjugale & Standards Légaux de Preuve",
        "lawBadge": "CC art. 161 / CPC art. 199",
        "timestamp": "PROCÉDURE LÉGALE",
        "proc_title": "FONCTIONNEMENT JUDICIAIRE & PROCÉDURE",
        "metric1_label": "PREUVE",
        "metric1_val": "Preuves Visuelles 4K",
        "metric2_label": "CHAÎNE",
        "metric2_val": "Horodatage Certifié",
        "metric3_label": "VALIDITÉ",
        "metric3_val": "Recevable en Justice",
        "timeline": [
            ("ÉTAPE 01", "Ouverture du dossier avec signature d'un contrat officiel, mandat et protocole strict de confidentialité RGPD."),
            ("ÉTAPE 02", "Observations effectuées exclusivement dans les lieux publics dans le respect absolu de la vie privée."),
            ("ÉTAPE 03", "Remise directe à votre avocat d'un dossier horodaté de preuves 4K et rapports officiels d'enquête.")
        ],
        "dict_additions": {
            "ADLİ DELİL STANDARDI • HMK m.199 & TCK m.134": "STANDARD DE PREUVE JURIDIQUE • HMK art. 199 & TCK art. 134",
            "Eş Takibi & Aile Hukuku Delil Standartları": "Filature Conjugale & Standards Légaux de Preuve",
            "HMK m.199 UYUMLU": "CONFORME CPC art. 199",
            "ADLİ İŞLEYİŞ VE PROSEDÜR": "FONCTIONNEMENT JUDICIAIRE & PROCÉDURE",
            "AŞAMA 01": "ÉTAPE 01",
            "Resmi hizmet sözleşmesi, vekalet ve KVKK gizlilik protokolü imzalanarak dosya açılır.": "Ouverture du dossier avec signature d'un contrat officiel, mandat et protocole de confidentialité.",
            "AŞAMA 02": "ÉTAPE 02",
            "Konut ve özel hayat dokunulmazlığına tam riayet edilerek yalnızca kamuya açık alanlarda tespit icra edilir.": "Observations effectuées exclusivement dans les lieux publics dans le respect absolu de la vie privée.",
            "AŞAMA 03": "ÉTAPE 03",
            "Zaman damgalı 4K görsel deliller ve resmi dedektif tutanağı doğrudan avukatınıza teslim edilir.": "Remise directe à votre avocat d'un dossier horodaté de preuves 4K et rapports officiels d'enquête."
        },
        "heroCases_code": """    heroCases: {
        sadakat: {
            code: "CADRE JURIDIQUE • DROIT DE LA FAMILLE & FIDÉLITÉ",
            title: "Filature Conjugale & Standards Légaux de Preuve",
            lawBadge: "CC art. 161 / CPC art. 199",
            metric1: "Preuves Visuelles 4K",
            metric2: "Horodatage Certifié",
            metric3: "Recevable en Justice",
            timestamp: "PROCÉDURE LÉGALE",
            logs: [
                { time: "ÉTAPE 01", text: "Ouverture du dossier avec signature d'un contrat officiel, mandat et protocole strict de confidentialité RGPD.", highlight: false },
                { time: "ÉTAPE 02", text: "Observations effectuées exclusivement dans les lieux publics dans le respect absolu de la vie privée.", highlight: false },
                { time: "ÉTAPE 03", text: "Remise directe à votre avocat d'un dossier horodaté de preuves 4K et rapports officiels d'enquête.", highlight: true }
            ]
        },
        tscm: {
            code: "CADRE JURIDIQUE • GARDE D'ENFANTS & DIVORCE",
            title: "Droit de Garde & Intérêt Supérieur de l'Enfant",
            lawBadge: "CC art. 182 / DROIT FAMILIAL",
            metric1: "Conditions de Vie",
            metric2: "Rapport Officiel",
            metric3: "Conforme Tribunal",
            timestamp: "STANDARD JUDICIAIRE",
            logs: [
                { time: "ÉTAPE 01", text: "Enquête légale sur les circonstances matérielles affectant la sécurité et le bien-être de l'enfant.", highlight: false },
                { time: "ÉTAPE 02", text: "Documentation conforme au droit civil et pénal du mode de vie et des devoirs de garde du conjoint.", highlight: false },
                { time: "ÉTAPE 03", text: "Constitution du dossier officiel de preuves soumis à l'appréciation du Juge aux Affaires Familiales.", highlight: true }
            ]
        },
        kurumsal: {
            code: "CADRE JURIDIQUE • DÉBITEURS & ACTIFS",
            title: "Adresse Réelle & Recherche de Patrimoine",
            lawBadge: "VOIES D'EXÉCUTION art. 277",
            metric1: "81 Provinces & Étranger",
            metric2: "Confirmation Domicile",
            metric3: "Preuve pour Saisie",
            timestamp: "RAPPORT OFFICIEL",
            logs: [
                { time: "ÉTAPE 01", text: "Lancement de vérifications terrain légales pour localiser un débiteur dissimulant son adresse.", highlight: false },
                { time: "ÉTAPE 02", text: "Identification du domicile effectif, des activités commerciales et des actifs cédés à des tiers.", highlight: false },
                { time: "ÉTAPE 03", text: "Délivrance du rapport officiel pour saisie conservatoire et action paulienne.", highlight: true }
            ]
        }
    },"""
    },
    "ru": {
        "code_badge": "СТАНДАРТ СУДЕБНЫХ ДОКАЗАТЕЛЬСТВ • ГПК 199 / УК 134",
        "title": "Наблюдение за супругом и стандарты судебных доказательств",
        "lawBadge": "ГК ст. 161 / ГПК ст. 199",
        "timestamp": "ЗАКОННАЯ ПРОЦЕДУРА",
        "proc_title": "СУДЕБНЫЙ РЕГЛАМЕНТ И ПРОЦЕДУРА",
        "metric1_label": "ДОКАЗАТЕЛЬСТВА",
        "metric1_val": "Видео и фото 4K",
        "metric2_label": "ЦЕПЬ",
        "metric2_val": "Штамп времени",
        "metric3_label": "СТАТУС",
        "metric3_val": "Для суда (ГПК 199)",
        "timeline": [
            ("ЭТАП 01", "Заключение официального договора, доверенности и строгого протокола конфиденциальности."),
            ("ЭТАП 02", "Сбор сведений исключительно в общественных местах без нарушения неприкосновенности частной жизни."),
            ("ЭТАП 03", "Передача адвокату досье с материалами 4K, метками времени и протоколом частного детектива.")
        ],
        "dict_additions": {
            "ADLİ DELİL STANDARDI • HMK m.199 & TCK m.134": "СТАНДАРТ СУДЕБНЫХ ДОКАЗАТЕЛЬСТВ • ГПК 199 / УК 134",
            "Eş Takibi & Aile Hukuku Delil Standartları": "Наблюдение за супругом и стандарты судебных доказательств",
            "HMK m.199 UYUMLU": "СООТВЕТСТВУЕТ ГПК 199",
            "ADLİ İŞLEYİŞ VE PROSEDÜR": "СУДЕБНЫЙ РЕГЛАМЕНТ И ПРОЦЕДУРА",
            "AŞAMA 01": "ЭТАП 01",
            "Resmi hizmet sözleşmesi, vekalet ve KVKK gizlilik protokolü imzalanarak dosya açılır.": "Заключение официального договора, доверенности и строгого протокола конфиденциальности.",
            "AŞAMA 02": "ЭТАП 02",
            "Konut ve özel hayat dokunulmazlığına tam riayet edilerek yalnızca kamuya açık alanlarda tespit icra edilir.": "Сбор сведений исключительно в общественных местах без нарушения неприкосновенности частной жизни.",
            "AŞAMA 03": "ЭТАП 03",
            "Zaman damgalı 4K görsel deliller ve resmi dedektif tutanağı doğrudan avukatınıza teslim edilir.": "Передача адвокату досье с материалами 4K, метками времени и протоколом частного детектива."
        },
        "heroCases_code": """    heroCases: {
        sadakat: {
            code: 'ПРАВОВЫЕ РАМКИ • СЕМЕЙНОЕ ПРАВО И ВЕРНОСТЬ',
            title: 'Наблюдение за супругом и стандарты судебных доказательств',
            lawBadge: 'ГК ст. 161 / ГПК ст. 199',
            metric1: 'Видео и фото 4K',
            metric2: 'Штамп времени',
            metric3: 'Для суда (ГПК 199)',
            timestamp: 'ЗАКОННАЯ ПРОЦЕДУРА',
            logs: [
                { time: 'ЭТАП 01', text: 'Заключение официального договора, доверенности и строгого протокола конфиденциальности.', highlight: false },
                { time: 'ЭТАП 02', text: 'Сбор сведений исключительно в общественных местах без нарушения неприкосновенности частной жизни.', highlight: false },
                { time: 'ЭТАП 03', text: 'Передача адвокату досье с материалами 4K, метками времени и протоколом частного детектива.', highlight: true }
            ]
        },
        tscm: {
            code: 'ПРАВОВЫЕ РАМКИ • ОПЕКА И РАЗВОД',
            title: 'Дела об опеке и высшие интересы ребёнка',
            lawBadge: 'ГК ст. 182 / СЕМЕЙНОЕ ПРАВО',
            metric1: 'Условия жизни',
            metric2: 'Официальный отчёт',
            metric3: 'Для суда',
            timestamp: 'СУДЕБНЫЙ СТАНДАРТ',
            logs: [
                { time: 'ЭТАП 01', text: 'Начало законного расследования факторов, влияющих на безопасность и развитие ребёнка.', highlight: false },
                { time: 'ЭТАП 02', text: 'Фиксация образа жизни и исполнения родительских обязанностей в рамках гражданского права.', highlight: false },
                { time: 'ЭТАП 03', text: 'Формирование официального досье для рассмотрения судьёй по семейным делам.', highlight: true }
            ]
        },
        kurumsal: {
            code: 'ПРАВОВЫЕ РАМКИ • ДОЛЖНИКИ И АКТИВЫ',
            title: 'Фактический адрес и розыск имущества должника',
            lawBadge: 'ИСПОЛНЕНИЕ ст. 277 / РОЗЫСК',
            metric1: '81 провинция и мир',
            metric2: 'Подтверждение адреса',
            metric3: 'Для взыскания',
            timestamp: 'ОФИЦИАЛЬНЫЙ ОТЧЁТ',
            logs: [
                { time: 'ЭТАП 01', text: 'Запуск законного полевого розыска должника, уклоняющегося от официальных повесток.', highlight: false },
                { time: 'ЭТАП 02', text: 'Установление фактического места жительства, коммерческой деятельности и скрытого имущества.', highlight: false },
                { time: 'ЭТАП 03', text: 'Предоставление официального отчёта для исполнительного производства и отмены фиктивных сделок.', highlight: true }
            ]
        }
    },"""
    },
    "ar": {
        "code_badge": "معايير الأدلة القانونية • المرافعات م.199 & العقوبات م.134",
        "title": "متابعة الزوج/الزوجة ومعايير الأدلة القانونية",
        "lawBadge": "المدني م.161 / المرافعات م.199",
        "timestamp": "إجراءات قانونية",
        "proc_title": "الإجراءات والمسار القضائي",
        "metric1_label": "الأدلة",
        "metric1_val": "توثيق 4K",
        "metric2_label": "التسلسل",
        "metric2_val": "ختم زمني رسمي",
        "metric3_label": "الحجية",
        "metric3_val": "مقبول أمام المحكمة",
        "timeline": [
            ("المرحلة 01", "فتح الملف وتوقيع عقد رسمي معتمد وتوكيل وبروتوكول سرية وحماية البيانات."),
            ("المرحلة 02", "إجراء التحريات فقط في الأماكن العامة التزاماً بحرمة الحياة الخاصة والحق في الخصوصية."),
            ("المرحلة 03", "تسليم ملف الأدلة المرئية 4K المختوم زمنياً ومحضر التحري مباشرة إلى محاميكم.")
        ],
        "dict_additions": {
            "ADLİ DELİL STANDARDI • HMK m.199 & TCK m.134": "معايير الأدلة القانونية • المرافعات م.199 & العقوبات م.134",
            "Eş Takibi & Aile Hukuku Delil Standartları": "متابعة الزوج/الزوجة ومعايير الأدلة القانونية",
            "HMK m.199 UYUMLU": "متوافق مع المرافعات م.199",
            "ADLİ İŞLEYİŞ VE PROSEDÜR": "الإجراءات والمسار القضائي",
            "AŞAMA 01": "المرحلة 01",
            "Resmi hizmet sözleşmesi, vekalet ve KVKK gizlilik protokolü imzalanarak dosya açılır.": "فتح الملف وتوقيع عقد رسمي معتمد وتوكيل وبروتوكول سرية وحماية البيانات.",
            "AŞAMA 02": "المرحلة 02",
            "Konut ve özel hayat dokunulmazlığına tam riayet edilerek yalnızca kamuya açık alanlarda tespit icra edilir.": "إجراء التحريات فقط في الأماكن العامة التزاماً بحرمة الحياة الخاصة والحق في الخصوصية.",
            "AŞAMA 03": "المرحلة 03",
            "Zaman damgalı 4K görsel deliller ve resmi dedektif tutanağı doğrudan avukatınıza teslim edilir.": "تسليم ملف الأدلة المرئية 4K المختوم زمنياً ومحضر التحري مباشرة إلى محاميكم."
        },
        "heroCases_code": """    heroCases: {
        sadakat: {
            code: 'الإطار القانوني • قانون الأسرة والوفاء الزوجي',
            title: 'متابعة الزوج/الزوجة ومعايير الأدلة القانونية',
            lawBadge: 'المدني م.161 / المرافعات م.199',
            metric1: 'توثيق 4K',
            metric2: 'ختم زمني رسمي',
            metric3: 'مقبول أمام المحكمة',
            timestamp: 'إجراءات قانونية',
            logs: [
                { time: 'المرحلة 01', text: 'فتح الملف وتوقيع عقد رسمي معتمد وتوكيل وبروتوكول سرية وحماية البيانات.', highlight: false },
                { time: 'المرحلة 02', text: 'إجراء التحريات فقط في الأماكن العامة التزاماً بحرمة الحياة الخاصة والحق في الخصوصية.', highlight: false },
                { time: 'المرحلة 03', text: 'تسليم ملف الأدلة المرئية 4K المختوم زمنياً ومحضر التحري مباشرة إلى محاميكم.', highlight: true }
            ]
        },
        tscm: {
            code: 'الإطار القانوني • الحضانة والطلاق',
            title: 'قضايا الحضانة ومصلحة الطفل الفضلى',
            lawBadge: 'المدني م.182 / قانون الأسرة',
            metric1: 'الظروف المعيشية',
            metric2: 'تقرير محكمة رسمي',
            metric3: 'جاهز للمحكمة',
            timestamp: 'معيار قضائي',
            logs: [
                { time: 'المرحلة 01', text: 'بدء تحريات قانونية لتوثيق الظروف الفعلية المؤثرة على سلامة ونشأة الطفل.', highlight: false },
                { time: 'المرحلة 02', text: 'توثيق نمط حياة الطرف الآخر ورعاية الأطفال ضمن الحدود القانونية والأخلاقية.', highlight: false },
                { time: 'المرحلة 03', text: 'إعداد ملف الأدلة الرسمي لتقديمه إلى قاضي محكمة الأسرة للبت في الحضانة.', highlight: true }
            ]
        },
        kurumsal: {
            code: 'الإطار القانوني • المدينون والأصول',
            title: 'تحديد العنوان الفعلي وكشف أصول المدين',
            lawBadge: 'التنفيذ م.277 / التحري',
            metric1: '81 ولاية ودولياً',
            metric2: 'تثبيت العنوان الفعلي',
            metric3: 'دليل للحجز والتنفيذ',
            timestamp: 'تقرير رسمي',
            logs: [
                { time: 'المرحلة 01', text: 'بدء تحريات ميدانية قانونية حول المدين المتواري عن استلام التبليغات الرسمية.', highlight: false },
                { time: 'المرحلة 02', text: 'تحديد مكان السكن الفعلي والأنشطة التجارية والأصول المنقولة لأطراف ثالثة.', highlight: false },
                { time: 'المرحلة 03', text: 'تسليم تقرير التحري المعتمد لإجراءات التنفيذ الجبري ودعاوى إبطال التصرفات.', highlight: true }
            ]
        }
    },"""
    },
    "me": {
        "code_badge": "PRAVNI STANDARD DOKAZA • ZPP čl. 199 & KZ čl. 134",
        "title": "Nadzor supružnika i pravni standardi dokaza",
        "lawBadge": "PZ čl. 161 / ZPP čl. 199",
        "timestamp": "ZAKONITI POSTUPAK",
        "proc_title": "SUDSKI POSTUPAK I PROCEDURA",
        "metric1_label": "DOKAZ",
        "metric1_val": "4K Video i Foto",
        "metric2_label": "LANAC",
        "metric2_val": "Vremenski žig",
        "metric3_label": "VALIDNOST",
        "metric3_val": "Spremno za sud",
        "timeline": [
            ("FAZA 01", "Otvaranje predmeta uz ugovor o radu, punomoćje i strogi protokol o povjerljivosti podataka."),
            ("FAZA 02", "Nadzor isključivo na javnim površinama uz puno poštovanje privatnosti i nepovredivosti doma."),
            ("FAZA 03", "Predaja zvaničnog dosijea sa vremenski žigosanim 4K dokazima direktno vašem advokatu.")
        ],
        "dict_additions": {
            "ADLİ DELİL STANDARDI • HMK m.199 & TCK m.134": "PRAVNI STANDARD DOKAZA • ZPP čl. 199 & KZ čl. 134",
            "Eş Takibi & Aile Hukuku Delil Standartları": "Nadzor supružnika i pravni standardi dokaza",
            "HMK m.199 UYUMLU": "USKLAĐENO SA ZPP čl. 199",
            "ADLİ İŞLEYİŞ VE PROSEDÜR": "SUDSKI POSTUPAK I PROCEDURA",
            "AŞAMA 01": "FAZA 01",
            "Resmi hizmet sözleşmesi, vekalet ve KVKK gizlilik protokolü imzalanarak dosya açılır.": "Otvaranje predmeta uz ugovor o radu, punomoćje i strogi protokol o povjerljivosti podataka.",
            "AŞAMA 02": "FAZA 02",
            "Konut ve özel hayat dokunulmazlığına tam riayet edilerek yalnızca kamuya açık alanlarda tespit icra edilir.": "Nadzor isključivo na javnim površinama uz puno poštovanje privatnosti i nepovredivosti doma.",
            "AŞAMA 03": "FAZA 03",
            "Zaman damgalı 4K görsel deliller ve resmi dedektif tutanağı doğrudan avukatınıza teslim edilir.": "Predaja zvaničnog dosijea sa vremenski žigosanim 4K dokazima direktno vašem advokatu."
        },
        "heroCases_code": """    heroCases: {
        sadakat: {
            code: 'PRAVNI OKVIR • PORODIČNO PRAVO & VJERNOST',
            title: 'Nadzor supružnika i pravni standardi dokaza',
            lawBadge: 'PZ čl. 161 / ZPP čl. 199',
            metric1: '4K Video i Foto',
            metric2: 'Vremenski žig',
            metric3: 'Spremno za sud',
            timestamp: 'ZAKONITI POSTUPAK',
            logs: [
                { time: 'FAZA 01', text: 'Otvaranje predmeta uz ugovor o radu, punomoćje i strogi protokol o povjerljivosti podataka.', highlight: false },
                { time: 'FAZA 02', text: 'Nadzor isključivo na javnim površinama uz puno poštovanje privatnosti i nepovredivosti doma.', highlight: false },
                { time: 'FAZA 03', text: 'Predaja zvaničnog dosijea sa vremenski žigosanim 4K dokazima direktno vašem advokatu.', highlight: true }
            ]
        },
        tscm: {
            code: 'PRAVNI OKVIR • STARATELJSTVO & RAZVOD',
            title: 'Postupak starateljstva i najbolji interes djeteta',
            lawBadge: 'PZ čl. 182 / PORODIČNO PRAVO',
            metric1: 'Uslovi života',
            metric2: 'Zvanični izvještaj',
            metric3: 'Spremno za sud',
            timestamp: 'FORENZIČKI STANDARD',
            logs: [
                { time: 'FAZA 01', text: 'Pokretanje zakonite istrage činjenica koje utiču na bezbjednost i razvoj djeteta.', highlight: false },
                { time: 'FAZA 02', text: 'Dokumentovanje načina života i ispunjavanja roditeljskih obaveza u okviru građanskog prava.', highlight: false },
                { time: 'FAZA 03', text: 'Izrada zvaničnog dokaznog spisa za odlučivanje sudije za porodične odnose.', highlight: true }
            ]
        },
        kurumsal: {
            code: 'PRAVNI OKVIR • DUŽNICI & IMOVINA',
            title: 'Stvarna adresa i provjera imovine dužnika',
            lawBadge: 'ZIO čl. 277 / ISTRAGA',
            metric1: '81 Pokrajina & Svijet',
            metric2: 'Provjera adrese',
            metric3: 'Dokaz za izvršenje',
            timestamp: 'ZVANIČNI IZVJEŠTAJ',
            logs: [
                { time: 'FAZA 01', text: 'Pokretanje terenske potrage za dužnikom koji izbjegava prijem sudskih pismena.', highlight: false },
                { time: 'FAZA 02', text: 'Utvrđivanje stvarnog prebivališta, poslovnih aktivnosti i imovine prebačene na treća lica.', highlight: false },
                { time: 'FAZA 03', text: 'Uručenje verifikovanog izvještaja za potrebe prinudnog izvršenja i paulijanske tužbe.', highlight: true }
            ]
        }
    },"""
    }
}

def update_lang_files():
    for lang, data in LANG_HERO_CASES.items():
        for path in [f"lang/{lang}.js", f"Dat/lang/{lang}.js"]:
            full_path = os.path.join(BASE_DIR, path)
            if not os.path.exists(full_path):
                continue
            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()

            # 1. Replace heroCases block
            content = re.sub(
                r'heroCases:\s*\{[\s\S]*?\n    \},',
                data["heroCases_code"],
                content,
                count=1
            )

            # 2. In dict, remove old VR774 line if present and inject new dict additions
            content = re.sub(r'\n\s*"DOSYA #DAT-2026-VR774[^\n]*",?', '', content)

            # Add new dict keys if not present
            dict_insert_str = ""
            for k, v in data["dict_additions"].items():
                if f'"{k}"' not in content:
                    dict_insert_str += f'        "{k}": "{v}",\n'

            if dict_insert_str:
                content = content.replace('    dict: {\n', '    dict: {\n' + dict_insert_str)

            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Updated {path}")

def update_html_files():
    desktop_nav_pat = re.compile(r'\n\s*<a href="#avrupa-yorumlar" class="px-2\.5 py-1\.5 rounded-full[^\n]*>.*?</a>', re.IGNORECASE)
    mobile_nav_pat = re.compile(r'\n\s*<a href="#avrupa-yorumlar" class="flex items-center justify-between[^\n]*>[\s\S]*?</a>', re.IGNORECASE)
    section_pat = re.compile(r'\n\s*<!--\s*7\.6\s*AVRUPA MÜVEKKİL YORUMLARI \(#avrupa-yorumlar[^\n]*-->\s*<section id="avrupa-yorumlar"[\s\S]*?</section>', re.IGNORECASE)

    for lang, data in LANG_HERO_CASES.items():
        for rel_path in [f"{lang}/index.html", f"Dat/{lang}/index.html"]:
            full_path = os.path.join(BASE_DIR, rel_path)
            if not os.path.exists(full_path):
                continue
            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Remove navbar links
            content = desktop_nav_pat.sub('', content)
            content = mobile_nav_pat.sub('', content)

            # Remove avrupa-yorumlar section
            content = section_pat.sub('', content)

            # Update hcCode
            content = re.sub(
                r'<p class="text-\[10px\] font-mono text-white/55 truncate" id="hcCode">.*?</p>',
                f'<p class="text-[10px] font-mono text-white/55 truncate" id="hcCode">{data["code_badge"]}</p>',
                content
            )

            # Update hcTitle
            content = re.sub(
                r'<div class="text-\[13px\] font-medium text-\[#111111\] leading-tight truncate" id="hcTitle">.*?</div>',
                f'<div class="text-[13px] font-medium text-[#111111] leading-tight truncate" id="hcTitle">{data["title"]}</div>',
                content
            )

            # Update hcLawBadge
            content = re.sub(
                r'<span class="px-2 py-0\.5 rounded-full bg-\[#111111\] text-\[#93F051\] font-mono text-\[9\.5px\] font-medium truncate" id="hcLawBadge">.*?</span>',
                f'<span class="px-2 py-0.5 rounded-full bg-[#111111] text-[#93F051] font-mono text-[9.5px] font-medium truncate" id="hcLawBadge">{data["lawBadge"]}</span>',
                content
            )

            # Update hcTimestamp
            content = re.sub(
                r'<div class="text-\[10px\] text-\[#111111\]/75 font-mono truncate" id="hcTimestamp">.*?</div>',
                f'<div class="text-[10px] text-[#111111]/75 font-mono truncate" id="hcTimestamp">{data["timestamp"]}</div>',
                content
            )

            # Update hcMetric labels and values
            content = re.sub(
                r'<div class="bg-\[#111111\]/10 rounded-lg px-2 py-1\.5">\s*<div class="font-mono text-\[#111111\]/65 text-\[8\.5px\]">.*?</div>\s*<div class="font-medium text-\[#111111\] truncate" id="hcMetric1">.*?</div>\s*</div>',
                f'<div class="bg-[#111111]/10 rounded-lg px-2 py-1.5"><div class="font-mono text-[#111111]/65 text-[8.5px]">{data["metric1_label"]}</div><div class="font-medium text-[#111111] truncate" id="hcMetric1">{data["metric1_val"]}</div></div>',
                content
            )
            content = re.sub(
                r'<div class="bg-\[#111111\]/10 rounded-lg px-2 py-1\.5">\s*<div class="font-mono text-\[#111111\]/65 text-\[8\.5px\]">.*?</div>\s*<div class="font-medium text-\[#111111\] truncate" id="hcMetric2">.*?</div>\s*</div>',
                f'<div class="bg-[#111111]/10 rounded-lg px-2 py-1.5"><div class="font-mono text-[#111111]/65 text-[8.5px]">{data["metric2_label"]}</div><div class="font-medium text-[#111111] truncate" id="hcMetric2">{data["metric2_val"]}</div></div>',
                content
            )
            content = re.sub(
                r'<div class="bg-\[#111111\]/10 rounded-lg px-2 py-1\.5">\s*<div class="font-mono text-\[#111111\]/65 text-\[8\.5px\]">.*?</div>\s*<div class="font-medium text-\[#111111\] truncate" id="hcMetric3">.*?</div>\s*</div>',
                f'<div class="bg-[#111111]/10 rounded-lg px-2 py-1.5"><div class="font-mono text-[#111111]/65 text-[8.5px]">{data["metric3_label"]}</div><div class="font-medium text-[#111111] truncate" id="hcMetric3">{data["metric3_val"]}</div></div>',
                content
            )

            # Update procedure heading above timeline
            content = re.sub(
                r'<span class="text-\[10\.5px\] font-medium text-\[#111111\]">(?:FORENSIC TIMELINE|ADLİ ZAMAN ÇİZELGESİ|ADLİ İŞLEYİŞ VE PROSEDÜR|CHRONOLOGIE JUDICIAIRE|СУДЕБНАЯ ХРОНОЛОГИЯ|الجدول الزمني للتحري|SUDSKA HRONOLOGIJA)</span>',
                f'<span class="text-[10.5px] font-medium text-[#111111]">{data["proc_title"]}</span>',
                content
            )

            # Build new hcTimeline HTML
            t1, d1 = data["timeline"][0]
            t2, d2 = data["timeline"][1]
            t3, d3 = data["timeline"][2]

            new_timeline_html = f'''<div class="space-y-2 text-[11.5px]" id="hcTimeline">
                                                <div class="flex items-start gap-2.5">
                                                    <span class="font-mono text-[10px] bg-[#F2F2F2] text-[#111111] px-2 py-0.5 rounded-md font-medium mt-0.5 shrink-0">{t1}</span>
                                                    <p class="text-[#3A3E42] font-regular text-[11.5px] leading-snug">{d1}</p>
                                                </div>
                                                <div class="flex items-start gap-2.5">
                                                    <span class="font-mono text-[10px] bg-[#F2F2F2] text-[#111111] px-2 py-0.5 rounded-md font-medium mt-0.5 shrink-0">{t2}</span>
                                                    <p class="text-[#3A3E42] font-regular text-[11.5px] leading-snug">{d2}</p>
                                                </div>
                                                <div class="flex items-start gap-2.5">
                                                    <span class="font-mono text-[10px] bg-[#111111] text-[#93F051] px-2 py-0.5 rounded-md font-medium mt-0.5 shrink-0">{t3}</span>
                                                    <p class="text-[#111111] font-medium text-[11.5px] leading-snug">{d3}</p>
                                                </div>
                                            </div>'''

            content = re.sub(
                r'<div class="space-y-2 text-\[11\.5px\]" id="hcTimeline">[\s\S]*?</div>\s*</div>\s*<div class="pt-2 border-t border-black/',
                f'{new_timeline_html}\n                                            <div class="pt-2 border-t border-black/',
                content
            )

            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Updated {rel_path}")

if __name__ == "__main__":
    update_lang_files()
    update_html_files()
    print("Done updating languages and HTML files.")
