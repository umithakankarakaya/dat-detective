'use client';

import React, { useState } from 'react';
import { 
  FileText, 
  Cpu, 
  Mic, 
  Camera, 
  Lock, 
  ExternalLink, 
  CheckCircle2, 
  AlertTriangle,
  Fingerprint
} from 'lucide-react';

export interface EvidenceItem {
  id: string;
  code: string;
  title: string;
  category: 'digital' | 'audio' | 'surveillance' | 'document' | 'forensic';
  classification: 'SECRET' | 'TOP SECRET' | 'CONFIDENTIAL';
  timestamp: string;
  sha256: string;
  source: string;
  status: 'analyzed' | 'decrypting' | 'verified';
  confidenceScore: number;
  notes?: string;
}

interface EvidenceCardProps {
  evidence: EvidenceItem;
  isSelected?: boolean;
  onSelect?: (evidence: EvidenceItem) => void;
}

export const EvidenceCard: React.FC<EvidenceCardProps> = ({
  evidence,
  isSelected = false,
  onSelect,
}) => {
  const [isCopied, setIsCopied] = useState(false);

  const getCategoryConfig = (category: EvidenceItem['category']) => {
    switch (category) {
      case 'digital':
        return { icon: <Cpu className="w-3.5 h-3.5 text-[#3A3E42]" />, label: 'Adli Bilişim' };
      case 'audio':
        return { icon: <Mic className="w-3.5 h-3.5 text-[#3A3E42]" />, label: 'Ses Analizi' };
      case 'surveillance':
        return { icon: <Camera className="w-3.5 h-3.5 text-[#3A3E42]" />, label: 'Fiziki Takip' };
      case 'forensic':
        return { icon: <Fingerprint className="w-3.5 h-3.5 text-[#3A3E42]" />, label: 'Kriminal İnceleme' };
      default:
        return { icon: <FileText className="w-3.5 h-3.5 text-[#3A3E42]" />, label: 'Belge & Kayıt' };
    }
  };

  const config = getCategoryConfig(evidence.category);

  const handleCopyHash = (e: React.MouseEvent) => {
    e.stopPropagation();
    navigator.clipboard.writeText(evidence.sha256);
    setIsCopied(true);
    setTimeout(() => setIsCopied(false), 1500);
  };

  return (
    <div
      onClick={() => onSelect?.(evidence)}
      className={`
        group relative cursor-pointer select-none rounded-2xl border p-5 sm:p-6
        transition-all duration-300 ease-apple active:scale-[0.99] font-sans
        ${isSelected 
          ? 'bg-[#FFFFFF] border-[#000000] ring-1 ring-[#000000] shadow-[0_4px_20px_rgba(0,0,0,0.08)]' 
          : 'bg-[#FFFFFF] hover:bg-[#FFFFFF] border-[rgba(0,0,0,0.08)] hover:border-[rgba(0,0,0,0.18)] shadow-[0_2px_12px_rgba(0,0,0,0.03)] hover:shadow-[0_8px_24px_rgba(0,0,0,0.06)]'
        }
      `}
    >
      {/* Top Meta Bar */}
      <div className="flex items-center justify-between gap-3">
        <div className="flex items-center gap-2">
          <div className="flex items-center gap-1.5 rounded-full bg-[#F3F4F4] px-3 py-1 text-xs font-medium text-[#3A3E42]">
            {config.icon}
            <span>{config.label}</span>
          </div>
          <span className="font-mono text-[11px] font-regular text-[#3A3E42]/60">
            {evidence.code}
          </span>
        </div>

        <div className="flex items-center gap-2">
          {evidence.classification === 'TOP SECRET' && (
            <span className="flex items-center gap-1 rounded-full bg-[#000000] text-[#FFFFFF] px-2.5 py-0.5 text-[10px] font-medium tracking-wide">
              <Lock className="w-2.5 h-2.5" /> GİZLİ
            </span>
          )}

          {evidence.status === 'verified' && (
            <span className="flex items-center gap-1 text-[11px] font-medium text-[#3A3E42]">
              <CheckCircle2 className="w-3 h-3 text-[#000000]" /> Doğrulandı
            </span>
          )}
          {evidence.status === 'decrypting' && (
            <span className="flex items-center gap-1 text-[11px] font-medium text-[#3A3E42] animate-pulse">
              <AlertTriangle className="w-3 h-3 text-[#000000]" /> Çözülüyor
            </span>
          )}
        </div>
      </div>

      {/* Title & Notes */}
      <div className="mt-4 space-y-1.5">
        <h4 className="text-base sm:text-lg font-medium tracking-tight text-[#000000] group-hover:text-[#3A3E42] transition-colors">
          {evidence.title}
        </h4>
        {evidence.notes && (
          <p className="line-clamp-2 text-xs sm:text-sm font-regular leading-relaxed text-[#3A3E42]/80">
            {evidence.notes}
          </p>
        )}
      </div>

      {/* Confidence Score Bar */}
      <div className="mt-4 space-y-1.5">
        <div className="flex items-center justify-between text-[11px] font-regular text-[#3A3E42]">
          <span>Hukuki Geçerlilik Skoru</span>
          <span className="font-medium text-[#000000]">%{evidence.confidenceScore}</span>
        </div>
        <div className="h-1.5 w-full overflow-hidden rounded-full bg-[#F3F4F4]">
          <div 
            className="h-full rounded-full bg-[#000000] transition-all duration-700 ease-apple"
            style={{ width: `${evidence.confidenceScore}%` }}
          />
        </div>
      </div>

      {/* Footer: SHA-256 Hash & Timestamp */}
      <div className="mt-5 pt-3.5 border-t border-[rgba(0,0,0,0.06)] flex items-center justify-between text-[11px] font-regular text-[#3A3E42]/70">
        <button
          onClick={handleCopyHash}
          title="SHA-256 Mührünü Kopyala"
          className="flex items-center gap-1.5 hover:text-[#000000] transition-colors"
        >
          <span className="text-[10px] text-[#3A3E42]/50 font-mono">HASH:</span>
          <span className="font-mono text-[#3A3E42] font-medium">
            {evidence.sha256.substring(0, 10)}...{evidence.sha256.substring(evidence.sha256.length - 4)}
          </span>
          <span className="text-[9px] text-[#3A3E42]/60">
            {isCopied ? '✓' : '⧉'}
          </span>
        </button>

        <div className="flex items-center gap-2">
          <span className="font-regular">{evidence.timestamp}</span>
          <ExternalLink className="w-3 h-3 opacity-0 group-hover:opacity-100 transition-opacity text-[#000000]" />
        </div>
      </div>
    </div>
  );
};
