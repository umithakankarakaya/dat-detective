'use client';

import React, { useState } from 'react';
import { 
  FolderKanban, 
  Layers, 
  Users2, 
  Clock, 
  Search, 
  SlidersHorizontal,
  X,
  Menu,
  ChevronRight, 
  Download, 
  Check, 
  Lock,
  ArrowLeft,
  Sparkles,
  Bot,
  Activity,
  ArrowUpRight,
  ShieldCheck,
  TrendingUp,
  Cpu,
  Mic,
  Camera,
  Fingerprint,
  FileText
} from 'lucide-react';
import { EvidenceCard, EvidenceItem } from './EvidenceCard';

const INITIAL_EVIDENCE_ITEMS: EvidenceItem[] = [
  {
    id: 'ev-1',
    code: 'EV-8841-CYBER',
    title: 'Şifreli SSD İmajı & Silinmiş WhatsApp Veritabanı',
    category: 'digital',
    classification: 'TOP SECRET',
    timestamp: 'Bugün, 14:22',
    sha256: 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
    source: 'İstanbul / Levent Ofis İncelemesi',
    status: 'analyzed',
    confidenceScore: 98,
    notes: 'DoD 5220.22-M protokolüyle silinmeye çalışılmış 1.420 adet mesaj ve mali transfer belgesi adli bilişimle kurtarıldı.',
  },
  {
    id: 'ev-2',
    code: 'EV-8842-AUDIO',
    title: 'Toplantı Odası GSM Böceğinden Alınan Ses Kaydı',
    category: 'audio',
    classification: 'SECRET',
    timestamp: 'Dün, 23:40',
    sha256: '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08',
    source: 'Ankara / Sinpaş Altınoran TSCM Taraması',
    status: 'verified',
    confidenceScore: 94,
    notes: 'Frekans gürültüsü temizlendi. Şüpheli B.K.\'nın ihale şartnamesini 3. şahsa aktardığı net ses frekansı doğrulandı.',
  },
  {
    id: 'ev-3',
    code: 'EV-8843-SURVEILLANCE',
    title: 'Fiziki Takip Fotoğraf Serisi (4K Optik Tele-Lens)',
    category: 'surveillance',
    classification: 'CONFIDENTIAL',
    timestamp: '08 Kasım, 18:15',
    sha256: '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8',
    source: 'Kartal Helis Metro Tower Çevresi',
    status: 'verified',
    confidenceScore: 99,
    notes: 'Şüpheli borçlunun kendi adına olmadığını iddia ettiği 3.4 Milyon TL değerindeki lüks aracı bizzat teslim aldığı an.',
  },
  {
    id: 'ev-4',
    code: 'EV-8844-FORENSIC',
    title: 'USB Bellek Üzerindeki Gizli Biyometrik İz',
    category: 'forensic',
    classification: 'TOP SECRET',
    timestamp: '07 Kasım, 09:30',
    sha256: '4b227777d4dd1fc61c6f884f48641d02b4d121d3fd328cb08b5531fcacdabf8a',
    source: 'Adli Bilişim Laboratuvarı',
    status: 'decrypting',
    confidenceScore: 89,
    notes: 'Donanım parmak izi eşleştirmesi devam ediyor. Şüpheli ikinci şahsın veri tabanındaki sicil kaydıyla örtüşüyor.',
  },
];

export const DetectiveDashboard: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'evidence' | 'cases' | 'suspects' | 'timeline' | 'ai'>('evidence');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [selectedEvidence, setSelectedEvidence] = useState<EvidenceItem | null>(INITIAL_EVIDENCE_ITEMS[0]);
  const [searchQuery, setSearchQuery] = useState('');
  const [inspectorOpen, setInspectorOpen] = useState(false);
  const [mobileDrawerOpen, setMobileDrawerOpen] = useState(false);
  const [isCopied, setIsCopied] = useState(false);
  const [aiPrompt, setAiPrompt] = useState('');

  const filteredEvidence = INITIAL_EVIDENCE_ITEMS.filter((item) => {
    const matchesCategory = selectedCategory === 'all' || item.category === selectedCategory;
    const matchesSearch = item.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          item.code.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          item.source.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesCategory && matchesSearch;
  });

  const handleCopyHash = (hash: string) => {
    navigator.clipboard.writeText(hash);
    setIsCopied(true);
    setTimeout(() => setIsCopied(false), 1500);
  };

  return (
    /* Metallic Architectural Frame Container (Scarlet Style) */
    <div className="min-h-screen w-full bg-[#E8EAED] p-2 sm:p-4 lg:p-6 font-sans antialiased text-[#3A3E42] flex items-center justify-center">
      
      {/* Outer Metallic Architectural Bezel */}
      <div className="w-full max-w-[1600px] h-[96vh] rounded-[28px] bg-gradient-to-b from-[#E2E5E9] via-[#D1D5DC] to-[#B8BCC6] p-1.5 shadow-[0_25px_70px_rgba(0,0,0,0.18)] border border-[rgba(255,255,255,0.8)] relative flex flex-col overflow-hidden">
        
        {/* Inner Chassis Screen */}
        <div className="w-full h-full rounded-[22px] bg-[#FFFFFF] flex overflow-hidden relative shadow-inner">
          
          {/* 1. SCARLET COMPACT ARCHITECTURAL SIDEBAR */}
          <aside className="w-20 lg:w-64 shrink-0 border-r border-[rgba(0,0,0,0.08)] bg-[#FFFFFF] flex flex-col justify-between z-20 transition-all duration-300">
            <div>
              {/* Brand Logo & Scarlet AI Beacon */}
              <div className="h-16 flex items-center justify-between px-4 lg:px-6 border-b border-[rgba(0,0,0,0.08)]">
                <div className="flex items-center gap-3">
                  <div className="h-9 w-9 rounded-xl bg-[#000000] text-[#FFFFFF] flex items-center justify-center font-medium shadow-sm shrink-0">
                    <Bot className="w-5 h-5 text-[#FFFFFF]" />
                  </div>
                  <div className="hidden lg:block">
                    <div className="text-xs font-medium text-[#000000] tracking-tight flex items-center gap-1.5">
                      <span>SCARLET // DAT</span>
                      <span className="h-1.5 w-1.5 rounded-full bg-[#000000] animate-ping"></span>
                    </div>
                    <div className="text-[10px] text-[#3A3E42]/60 font-mono">AI Agent v2.4</div>
                  </div>
                </div>
              </div>

              {/* Sidebar Quick Navigation */}
              <nav className="p-3 space-y-1.5 text-xs font-medium">
                <a
                  href="index.html"
                  className="flex items-center gap-3 rounded-xl p-3 text-[#3A3E42]/70 hover:text-[#000000] hover:bg-[#F3F4F4] transition"
                  title="Ana Sayfaya Dön"
                >
                  <ArrowLeft className="w-4 h-4 shrink-0" />
                  <span className="hidden lg:inline font-regular">Ana Sayfa</span>
                </a>

                <div className="hidden lg:block pt-3 pb-1 px-3 text-[10px] font-mono uppercase text-[#3A3E42]/40">
                  Operasyon Paneli
                </div>

                <button
                  onClick={() => setActiveTab('evidence')}
                  className={`w-full flex items-center justify-between rounded-xl p-3 transition-all duration-200 ${
                    activeTab === 'evidence' 
                      ? 'bg-[#000000] text-[#FFFFFF]' 
                      : 'text-[#3A3E42] hover:bg-[#F3F4F4]'
                  }`}
                  title="Kanıt Panosu"
                >
                  <div className="flex items-center gap-3">
                    <Layers className="w-4 h-4 shrink-0" />
                    <span className="hidden lg:inline">Kanıt Duvarı</span>
                  </div>
                  <span className={`hidden lg:inline-flex rounded-full px-2 py-0.5 text-[10px] font-mono ${activeTab === 'evidence' ? 'bg-[#FFFFFF]/20 text-[#FFFFFF]' : 'bg-[#F3F4F4] text-[#3A3E42]'}`}>
                    {INITIAL_EVIDENCE_ITEMS.length}
                  </span>
                </button>

                <button
                  onClick={() => setActiveTab('cases')}
                  className={`w-full flex items-center justify-between rounded-xl p-3 transition-all duration-200 ${
                    activeTab === 'cases' 
                      ? 'bg-[#000000] text-[#FFFFFF]' 
                      : 'text-[#3A3E42] hover:bg-[#F3F4F4]'
                  }`}
                  title="Vaka Dosyaları"
                >
                  <div className="flex items-center gap-3">
                    <FolderKanban className="w-4 h-4 shrink-0" />
                    <span className="hidden lg:inline">Vaka Dosyaları</span>
                  </div>
                  <span className={`hidden lg:inline-flex rounded-full px-2 py-0.5 text-[10px] font-mono ${activeTab === 'cases' ? 'bg-[#FFFFFF]/20 text-[#FFFFFF]' : 'bg-[#F3F4F4] text-[#3A3E42]'}`}>
                    12
                  </span>
                </button>

                <button
                  onClick={() => setActiveTab('suspects')}
                  className={`w-full flex items-center justify-between rounded-xl p-3 transition-all duration-200 ${
                    activeTab === 'suspects' 
                      ? 'bg-[#000000] text-[#FFFFFF]' 
                      : 'text-[#3A3E42] hover:bg-[#F3F4F4]'
                  }`}
                  title="Şüpheli Matrisi"
                >
                  <div className="flex items-center gap-3">
                    <Users2 className="w-4 h-4 shrink-0" />
                    <span className="hidden lg:inline">Şüpheli Matrisi</span>
                  </div>
                  <span className={`hidden lg:inline-flex rounded-full px-2 py-0.5 text-[10px] font-mono ${activeTab === 'suspects' ? 'bg-[#FFFFFF]/20 text-[#FFFFFF]' : 'bg-[#F3F4F4] text-[#3A3E42]'}`}>
                    4
                  </span>
                </button>

                <button
                  onClick={() => setActiveTab('ai')}
                  className={`w-full flex items-center justify-between rounded-xl p-3 transition-all duration-200 ${
                    activeTab === 'ai' 
                      ? 'bg-[#000000] text-[#FFFFFF]' 
                      : 'text-[#3A3E42] hover:bg-[#F3F4F4]'
                  }`}
                  title="Scarlet AI Analizi"
                >
                  <div className="flex items-center gap-3">
                    <Sparkles className="w-4 h-4 shrink-0" />
                    <span className="hidden lg:inline">AI İçgörüleri</span>
                  </div>
                  <span className="hidden lg:inline-flex h-2 w-2 rounded-full bg-[#000000]"></span>
                </button>
              </nav>
            </div>

            {/* Sidebar Agent Status */}
            <div className="p-3 lg:p-4 border-t border-[rgba(0,0,0,0.08)]">
              <div className="flex items-center gap-3 rounded-xl bg-[#F3F4F4] p-2.5">
                <div className="h-8 w-8 rounded-lg bg-[#000000] text-[#FFFFFF] flex items-center justify-center font-mono text-xs font-medium shrink-0">
                  DT
                </div>
                <div className="hidden lg:block truncate">
                  <div className="text-xs font-medium text-[#000000] truncate">Kıdemli Dedektif</div>
                  <div className="text-[10px] text-[#3A3E42]/60 font-mono truncate">AES-256 Aktif</div>
                </div>
              </div>
            </div>
          </aside>

          {/* 2. MAIN WORKSPACE */}
          <main className="flex-1 flex flex-col h-full overflow-hidden bg-[#FFFFFF]">
            
            {/* Top Operational Bar */}
            <header className="h-16 shrink-0 border-b border-[rgba(0,0,0,0.08)] px-4 sm:px-6 flex items-center justify-between z-10 bg-[#FFFFFF]">
              <div className="flex items-center gap-3">
                <button
                  onClick={() => setMobileDrawerOpen(true)}
                  className="lg:hidden p-2 rounded-xl bg-[#F3F4F4] text-[#3A3E42]"
                >
                  <Menu className="w-4 h-4" />
                </button>

                <div className="flex items-center gap-2">
                  <span className="rounded-full bg-[#F3F4F4] px-2.5 py-1 text-[11px] font-mono font-medium text-[#3A3E42]">
                    DOSYA #2024-VR774
                  </span>
                  <ChevronRight className="w-3.5 h-3.5 text-[#3A3E42]/40" />
                  <h1 className="text-xs sm:text-sm font-medium text-[#000000] tracking-tight truncate">
                    Kurumsal Varlık Transferi & Gizli Hesap Soruşturması
                  </h1>
                </div>
              </div>

              {/* Scarlet Search & Inspector Action */}
              <div className="flex items-center gap-3">
                <div className="hidden md:flex items-center rounded-xl bg-[#F3F4F4] px-3 py-1.5 text-xs w-64 border border-transparent focus-within:border-[#000000] focus-within:bg-[#FFFFFF] transition">
                  <Search className="w-3.5 h-3.5 text-[#3A3E42]/50 mr-2" />
                  <input
                    type="text"
                    placeholder="Kanıt, işlem veya şüpheli ara..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="w-full bg-transparent text-xs text-[#3A3E42] placeholder-[#3A3E42]/40 focus:outline-none"
                  />
                  <kbd className="rounded bg-[#FFFFFF] px-1.5 py-0.5 text-[9px] font-mono text-[#3A3E42]/70 border border-[rgba(0,0,0,0.06)] shadow-sm">⌘K</kbd>
                </div>

                <button
                  onClick={() => setInspectorOpen(!inspectorOpen)}
                  className={`flex items-center gap-2 rounded-xl px-3.5 py-2 text-xs font-medium transition ${
                    inspectorOpen ? 'bg-[#000000] text-[#FFFFFF]' : 'bg-[#F3F4F4] text-[#3A3E42] hover:text-[#000000]'
                  }`}
                >
                  <SlidersHorizontal className="w-3.5 h-3.5" />
                  <span className="hidden sm:inline">{inspectorOpen ? 'Müfettişi Gizle' : 'Müfettişi Aç'}</span>
                  <span className="sm:hidden">Detay</span>
                </button>
              </div>
            </header>

            {/* Scrollable Center Content */}
            <div className="flex-1 overflow-y-auto px-4 sm:px-6 lg:px-8 py-5 space-y-6 pb-24 md:pb-8">
              
              {/* SCARLET SIGNATURE BLUE BALANCE & AGENT HEALTH BANNER */}
              <div className="rounded-2xl bg-gradient-to-r from-[#1E293B] via-[#0F172A] to-[#020617] text-[#FFFFFF] p-6 sm:p-7 relative overflow-hidden shadow-lg border border-[rgba(255,255,255,0.08)]">
                {/* Subtle Ambient Mesh Sheen */}
                <div className="absolute -right-20 -top-20 w-80 h-80 bg-blue-500/10 rounded-full blur-3xl pointer-events-none"></div>

                <div className="relative z-10 grid md:grid-cols-12 gap-6 items-center">
                  <div className="md:col-span-8 space-y-3">
                    <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/10 backdrop-blur-md text-xs font-mono text-slate-300 border border-white/10">
                      <Bot className="w-3.5 h-3.5 text-blue-400" />
                      <span>SCARLET AI AGENT • GİZLİ VERİ AKIŞI AKTİF</span>
                    </div>

                    <h2 className="text-xl sm:text-2xl font-medium tracking-tight text-white">
                      Soruşturma Durumu: <span className="font-mono">Adli Delil Eşleştirme Aktif</span>
                    </h2>

                    <p className="text-xs sm:text-sm font-regular text-slate-300 leading-relaxed max-w-2xl">
                      Scarlet yapay zekâ motoru, hedef şahsın paravan şirketlerine aktarılan 28 ayrı adli delil ve işlem kaydını eşleştirdi. Mahkeme delil zinciri %98.4 doğrulukla mühürlendi.
                    </p>

                    <div className="flex flex-wrap gap-3 pt-2">
                      <button className="flex items-center gap-2 rounded-xl bg-[#FFFFFF] text-[#000000] px-4 py-2 text-xs font-medium hover:bg-slate-100 transition shadow-sm">
                        <Sparkles className="w-3.5 h-3.5" />
                        <span>AI Anomali Raporunu Üret</span>
                      </button>
                      <button className="flex items-center gap-2 rounded-xl bg-white/10 text-white px-4 py-2 text-xs font-medium hover:bg-white/15 transition border border-white/10">
                        <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
                        <span>HMK Uyumunu Doğrula</span>
                      </button>
                    </div>
                  </div>

                  <div className="md:col-span-4 grid grid-cols-2 gap-3 font-mono text-xs">
                    <div className="p-3.5 rounded-xl bg-white/5 border border-white/10">
                      <div className="text-slate-400 text-[10px]">ANOMALİ İNDEKSİ</div>
                      <div className="text-lg font-medium text-amber-400 mt-1">%99.4</div>
                      <div className="text-[10px] text-slate-400 mt-0.5">Yüksek Öncelikli</div>
                    </div>
                    <div className="p-3.5 rounded-xl bg-white/5 border border-white/10">
                      <div className="text-slate-400 text-[10px]">ADLİ DOĞRULAMA</div>
                      <div className="text-lg font-medium text-emerald-400 mt-1">24 / 28</div>
                      <div className="text-[10px] text-slate-400 mt-0.5">Mühürlü Kanıt</div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Filter Tabs */}
              <div className="flex items-center justify-between border-b border-[rgba(0,0,0,0.08)] pb-3">
                <div className="flex items-center gap-1.5 overflow-x-auto no-scrollbar py-1">
                  {[
                    { id: 'all', label: 'Tüm Deliller' },
                    { id: 'digital', label: 'Adli Bilişim' },
                    { id: 'audio', label: 'Ses Frekansları' },
                    { id: 'surveillance', label: 'Saha Takibi' },
                    { id: 'forensic', label: 'Biyometrik İzler' },
                  ].map((cat) => (
                    <button
                      key={cat.id}
                      onClick={() => setSelectedCategory(cat.id)}
                      className={`rounded-full px-3.5 py-1.5 text-xs font-medium transition-all duration-200 whitespace-nowrap ${
                        selectedCategory === cat.id
                          ? 'bg-[#000000] text-[#FFFFFF]'
                          : 'bg-[#F3F4F4] text-[#3A3E42] hover:text-[#000000]'
                      }`}
                    >
                      {cat.label}
                    </button>
                  ))}
                </div>

                <span className="text-xs font-mono text-[#3A3E42]/50 hidden sm:inline">
                  {filteredEvidence.length} Kanıt Dosyası
                </span>
              </div>

              {/* 3. SCARLET QUIET DATA TABLE (Sessiz Veri Tablosu) */}
              <div className="rounded-2xl border border-[rgba(0,0,0,0.08)] bg-[#FFFFFF] overflow-hidden shadow-[0_2px_12px_rgba(0,0,0,0.03)]">
                <div className="p-4 border-b border-[rgba(0,0,0,0.08)] flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <Activity className="w-4 h-4 text-[#3A3E42]" />
                    <h3 className="text-xs font-medium uppercase tracking-wider text-[#000000]">
                      Adli Kanıt & İşlem Çizelgesi (Audit Trail)
                    </h3>
                  </div>
                  <span className="text-[11px] font-mono text-[#3A3E42]/60">Gerçek Zamanlı Senkronize</span>
                </div>

                <div className="overflow-x-auto">
                  <table className="w-full text-left text-xs font-sans">
                    <thead className="bg-[#F3F4F4] text-[#3A3E42]/70 font-mono text-[10px] uppercase">
                      <tr>
                        <th className="py-3 px-4">Kod & İsim</th>
                        <th className="py-3 px-4">Kategori</th>
                        <th className="py-3 px-4">Zaman Damgası</th>
                        <th className="py-3 px-4">Hukuki Güven</th>
                        <th className="py-3 px-4">Durum</th>
                        <th className="py-3 px-4 text-right">Eylem</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-[rgba(0,0,0,0.06)] font-regular text-[#3A3E42]">
                      {filteredEvidence.map((item) => (
                        <tr 
                          key={item.id}
                          onClick={() => {
                            setSelectedEvidence(item);
                            setInspectorOpen(true);
                          }}
                          className={`hover:bg-[#F3F4F4]/60 cursor-pointer transition ${selectedEvidence?.id === item.id ? 'bg-[#F3F4F4]' : ''}`}
                        >
                          <td className="py-3.5 px-4">
                            <div className="font-medium text-[#000000]">{item.title}</div>
                            <div className="font-mono text-[10px] text-[#3A3E42]/60">{item.code}</div>
                          </td>
                          <td className="py-3.5 px-4 font-mono text-[11px]">
                            <span className="rounded-full bg-[#F3F4F4] px-2.5 py-1 text-[#3A3E42] border border-[rgba(0,0,0,0.06)]">
                              {item.category}
                            </span>
                          </td>
                          <td className="py-3.5 px-4 font-mono text-[11px] text-[#3A3E42]/70">
                            {item.timestamp}
                          </td>
                          <td className="py-3.5 px-4">
                            <div className="flex items-center gap-2">
                              <span className="font-medium text-[#000000]">%{item.confidenceScore}</span>
                              <div className="w-16 h-1.5 rounded-full bg-[#F3F4F4] overflow-hidden">
                                <div className="h-full bg-[#000000]" style={{ width: `${item.confidenceScore}%` }}></div>
                              </div>
                            </div>
                          </td>
                          <td className="py-3.5 px-4">
                            <span className="rounded-full bg-[#000000] text-[#FFFFFF] px-2.5 py-0.5 text-[10px] font-medium">
                              {item.status}
                            </span>
                          </td>
                          <td className="py-3.5 px-4 text-right">
                            <button className="text-xs font-medium text-[#000000] hover:underline inline-flex items-center gap-1">
                              <span>İncele</span>
                              <ArrowUpRight className="w-3 h-3" />
                            </button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>

              {/* Dynamic Evidence Cards Grid */}
              <div className="space-y-3 pt-2">
                <div className="flex items-center justify-between">
                  <h3 className="text-xs font-medium uppercase tracking-wider text-[#000000]">
                    Detaylı Kanıt Kartları
                  </h3>
                  <span className="text-[11px] text-[#3A3E42]/60">Kart görünümü</span>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {filteredEvidence.map((evidence) => (
                    <EvidenceCard
                      key={evidence.id}
                      evidence={evidence}
                      isSelected={selectedEvidence?.id === evidence.id}
                      onSelect={(ev) => {
                        setSelectedEvidence(ev);
                        setInspectorOpen(true);
                      }}
                    />
                  ))}
                </div>
              </div>

            </div>
          </main>

          {/* 4. SCARLET FORENSIC INSPECTOR PANEL */}
          {inspectorOpen && selectedEvidence && (
            <aside className="w-80 lg:w-96 shrink-0 border-l border-[rgba(0,0,0,0.08)] bg-[#FFFFFF] flex flex-col justify-between z-20 overflow-y-auto">
              <div className="p-5 sm:p-6 space-y-5">
                
                {/* Inspector Header */}
                <div className="flex items-center justify-between pb-3 border-b border-[rgba(0,0,0,0.08)]">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-mono font-medium text-[#3A3E42]">SCARLET MÜFETTİŞİ</span>
                    <span className="rounded-full bg-[#F3F4F4] text-[#3A3E42] text-[10px] font-mono px-2 py-0.5 font-medium">
                      AKTİF
                    </span>
                  </div>
                  <button onClick={() => setInspectorOpen(false)} className="text-[#3A3E42] hover:text-[#000000]">
                    <X className="w-4 h-4" />
                  </button>
                </div>

                {/* Evidence Title & Code */}
                <div className="space-y-1.5">
                  <span className="text-[11px] font-mono font-medium text-[#3A3E42]/60">{selectedEvidence.code}</span>
                  <h3 className="text-base font-medium tracking-tight text-[#000000] leading-snug">
                    {selectedEvidence.title}
                  </h3>
                  <p className="text-xs font-regular text-[#3A3E42]/80 leading-relaxed">
                    {selectedEvidence.notes}
                  </p>
                </div>

                {/* Scarlet AI Co-Pilot Insight Box */}
                <div className="rounded-xl bg-[#F3F4F4] p-4 space-y-2 border border-[rgba(0,0,0,0.06)]">
                  <div className="flex items-center gap-2 text-xs font-medium text-[#000000]">
                    <Sparkles className="w-3.5 h-3.5 text-[#000000]" />
                    <span>Scarlet AI Hukuki Çıkarımı</span>
                  </div>
                  <p className="text-[11px] text-[#3A3E42]/80 leading-relaxed font-regular">
                    Bu kanıt, karşı tarafın mal kaçırma amacıyla kurduğu paravan hesap ile doğrudan örtüşmektedir. CMK 135 ve HMK delil zincirine tam uyumludur.
                  </p>
                </div>

                {/* SHA-256 Forensic Hash Box */}
                <div className="rounded-xl bg-[#F3F4F4] p-4 space-y-3 font-mono text-xs">
                  <div className="flex items-center justify-between text-[10px] font-medium text-[#3A3E42]">
                    <span>BLOKZİNCİR MÜHRÜ (SHA-256)</span>
                    <button onClick={() => handleCopyHash(selectedEvidence.sha256)} className="text-[#000000] font-medium hover:underline">
                      {isCopied ? 'Kopyalandı!' : 'Kopyala'}
                    </button>
                  </div>
                  <div className="break-all rounded-lg bg-[#FFFFFF] p-2 text-[10px] text-[#3A3E42] border border-[rgba(0,0,0,0.06)] select-all">
                    {selectedEvidence.sha256}
                  </div>
                  <div className="space-y-1.5 pt-2 border-t border-[rgba(0,0,0,0.06)] text-[11px]">
                    <div className="flex justify-between">
                      <span className="text-[#3A3E42]/60">LOKASYON:</span>
                      <span className="text-[#000000] font-medium truncate ml-2">{selectedEvidence.source}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-[#3A3E42]/60">ZAMAN:</span>
                      <span className="text-[#000000] font-medium">{selectedEvidence.timestamp}</span>
                    </div>
                  </div>
                </div>

                {/* Linked Suspect */}
                <div className="rounded-xl bg-[#F3F4F4] p-4 space-y-3">
                  <div className="text-[10px] font-mono font-medium text-[#3A3E42]/60 uppercase">İLİŞKİLİ ŞÜPHELİ</div>
                  <div className="flex items-center gap-3">
                    <div className="h-10 w-10 rounded-full bg-[#FFFFFF] border border-[rgba(0,0,0,0.08)] flex items-center justify-center font-mono font-medium text-[#3A3E42] shrink-0">
                      B.K.
                    </div>
                    <div className="truncate">
                      <div className="text-xs font-medium text-[#000000] truncate">B**** K*****</div>
                      <div className="text-[10px] font-regular text-[#3A3E42]/70 truncate">Şirket Finans Direktörü</div>
                    </div>
                    <span className="ml-auto rounded-full bg-[#000000] text-[#FFFFFF] px-2.5 py-0.5 text-[9px] font-medium shrink-0">
                      BAŞ ŞÜPHELİ
                    </span>
                  </div>
                </div>

                {/* Action Buttons */}
                <div className="space-y-2 pt-1">
                  <button className="w-full flex items-center justify-center gap-2 rounded-xl bg-[#000000] text-[#FFFFFF] py-3 text-xs font-medium hover:bg-[#3A3E42] transition shadow-sm">
                    <Check className="w-4 h-4" />
                    <span>HMK Mahkeme Dosyasına Mühürle</span>
                  </button>
                  <button className="w-full flex items-center justify-center gap-2 rounded-xl bg-[#F3F4F4] border border-[rgba(0,0,0,0.06)] py-3 text-xs font-medium text-[#3A3E42] hover:text-[#000000] hover:bg-[#E5E7EB] transition">
                    <Download className="w-3.5 h-3.5" />
                    <span>Kriptolu Rapor İndir</span>
                  </button>
                </div>

              </div>

              <div className="p-4 border-t border-[rgba(0,0,0,0.08)] text-center text-[10px] font-mono text-[#3A3E42]/50">
                SCARLET AI & DAT DEDEKTİFLİK PROTOKOLÜ
              </div>
            </aside>
          )}

        </div>
      </div>
    </div>
  );
};
export default DetectiveDashboard;
