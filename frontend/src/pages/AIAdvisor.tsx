import React, { useEffect, useRef, useState } from 'react';
import {
  BrainCircuit,
  Check,
  Copy,
  Info,
  RefreshCcw,
  Send,
  ShieldCheck,
  Sparkles,
  Square,
  Target,
  Zap,
} from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import toast, { Toaster } from 'react-hot-toast';
import apiClient from '../api/client';

export const AIAdvisor: React.FC = () => {
  const [query, setQuery] = useState('');
  const [advice, setAdvice] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState(false);

  const scrollRef = useRef<HTMLDivElement>(null);
  const abortControllerRef = useRef<AbortController | null>(null);

  const suggestions = [
    { label: 'Optimize Burn Rate', icon: <Zap size={14} /> },
    { label: 'Analyze Grocery Spend', icon: <Target size={14} /> },
    { label: 'Subscription Audit', icon: <ShieldCheck size={14} /> },
  ];

  useEffect(() => {
    if (advice && scrollRef.current) {
      scrollRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [advice]);

  const handleStop = () => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      abortControllerRef.current = null;
      setLoading(false);
      toast.error('Analysis terminated');
    }
  };

  const handleAsk = async (explicitQuery?: string) => {
    const finalQuery = explicitQuery || query;

    if (loading) {
      handleStop();
      return;
    }

    if (!finalQuery.trim()) return;

    setLoading(true);
    setAdvice(null);

    const controller = new AbortController();
    abortControllerRef.current = controller;

    try {
      const response = await apiClient.get<{ advice: string }>('/ai/advice', {
        params: { query: finalQuery },
        signal: controller.signal,
      });
      setAdvice(response.data.advice);
      toast.success('Intelligence Synced');
    } catch (err: any) {
      if (err.name === 'CanceledError' || err.code === 'ERR_CANCELED') {
        console.log('Request manually aborted');
      } else {
        toast.error('AI Core Offline');
        setAdvice("I'm having trouble connecting to my neural network.");
      }
    } finally {
      setLoading(false);
      abortControllerRef.current = null;
    }
  };

  const handleCopy = () => {
    if (!advice) return;
    navigator.clipboard.writeText(advice);
    setCopied(true);
    toast.success('Copied to clipboard');
    setTimeout(() => setCopied(false), 2000);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') {
      e.preventDefault();
      handleAsk();
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-10 animate-in fade-in slide-in-from-bottom-6 duration-1000 pb-20">
      <Toaster position="bottom-right" />

      <header className="text-center space-y-4">
        <div className="relative inline-block">
          <div className="absolute inset-0 bg-[#238636] blur-2xl opacity-20 animate-pulse" />
          <div className="relative inline-flex p-4 bg-[#161b22] border border-[#30363d] rounded-3xl shadow-2xl">
            <BrainCircuit className="text-[#238636]" size={40} />
          </div>
        </div>
        <h1 className="text-5xl font-black text-white tracking-tighter">
          Spend<span className="text-[#6C4DFF]">Wise</span> Intelligence
        </h1>
      </header>

      <div className="relative group">
        <div className="absolute -inset-1 bg-gradient-to-r from-[#238636]/20 to-[#58a6ff]/20 rounded-[2.5rem] blur opacity-25 group-hover:opacity-50 transition duration-1000"></div>
        <div className="relative bg-[#161b22] border border-[#30363d] rounded-[2rem] p-8 shadow-2xl">
          <div className="space-y-6">
            <div className="flex items-center justify-between px-1">
              <label className="text-sm font-bold text-[#8b949e] uppercase tracking-widest flex items-center gap-2">
                <Sparkles size={16} className="text-[#238636]" /> Input Query
              </label>
              <div className="flex gap-2">
                {suggestions.map((s) => (
                  <button
                    key={s.label}
                    onClick={() => handleAsk(s.label)}
                    className="hidden md:flex items-center gap-1.5 px-3 py-1.5 bg-[#0d1117] border border-[#30363d] rounded-full text-xs font-bold text-[#c9d1d9] hover:border-[#238636] hover:text-white transition-all"
                  >
                    {s.icon} {s.label}
                  </button>
                ))}
              </div>
            </div>

            <div className="relative">
              <textarea
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Ask SpendWise about your finances..."
                className="w-full bg-[#0d1117] border border-[#30363d] rounded-2xl min-h-[160px] p-6 focus:border-[#238636] focus:ring-1 focus:ring-[#238636] outline-none transition-all text-white text-lg leading-relaxed resize-none shadow-inner"
              />
              <div className="absolute bottom-4 right-4 flex items-center gap-3">
                <span className="text-[10px] font-bold text-[#484f58] uppercase hidden sm:block">
                  CMD + Enter
                </span>
                <button
                  onClick={() => handleAsk()}
                  disabled={!loading && !query.trim()}
                  className="bg-[#238636] hover:bg-[#2ea043] p-4 rounded-xl text-white transition-all shadow-xl active:scale-90"
                >
                  {loading ? <Square size={20} className="fill-white" /> : <Send size={20} />}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      {advice && (
        <div ref={scrollRef} className="animate-in slide-in-from-top-4 fade-in duration-500">
          <div className="bg-[#161b22] border border-[#30363d] rounded-[2rem] overflow-hidden shadow-2xl">
            <div className="bg-[#0d1117] px-8 py-4 border-b border-[#30363d] flex justify-between items-center">
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-[#238636] animate-pulse" />
                <span className="text-xs font-black text-[#8b949e] uppercase tracking-tighter">
                  Strategic Analysis Complete
                </span>
              </div>
              <button
                onClick={() => setAdvice(null)}
                className="text-[#484f58] hover:text-white transition-colors"
              >
                <RefreshCcw size={14} />
              </button>
            </div>
            <div className="p-10">
              <div className="prose prose-invert max-w-none">
                <div className="text-[#e6edf3] leading-relaxed text-lg font-medium">
                  <ReactMarkdown
                    components={{
                      h3: ({ ...props }) => (
                        <h3
                          className="text-[#238636] font-black text-2xl mt-6 mb-4 tracking-tight"
                          {...props}
                        />
                      ),
                      ul: ({ ...props }) => (
                        <ul className="list-disc list-inside space-y-2 text-[#8b949e]" {...props} />
                      ),
                      strong: ({ ...props }) => (
                        <strong className="text-white font-bold" {...props} />
                      ),
                      li: ({ ...props }) => <li className="ml-4" {...props} />,
                    }}
                  >
                    {advice}
                  </ReactMarkdown>
                </div>
              </div>

              <div className="mt-10 pt-8 border-t border-[#30363d] flex flex-col sm:flex-row items-center justify-between gap-4">
                <div className="flex items-center gap-2 text-[#484f58]">
                  <Info size={14} />
                  <span className="text-[10px] font-bold uppercase tracking-wider">
                    AI generated insight •{' '}
                    {new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </span>
                </div>
                <div className="flex items-center gap-3">
                  <button
                    onClick={handleCopy}
                    className="flex items-center gap-2 px-4 py-2 bg-[#0d1117] border border-[#30363d] rounded-xl text-xs font-bold text-white hover:border-[#238636] transition-all"
                  >
                    {copied ? <Check size={14} className="text-[#238636]" /> : <Copy size={14} />}
                    {copied ? 'Copied' : 'Copy Insights'}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {loading && !advice && (
        <div className="flex flex-col items-center justify-center py-12 space-y-4">
          <div className="w-12 h-12 border-4 border-[#238636]/20 border-t-[#238636] rounded-full animate-spin" />
          <p className="text-[#8b949e] font-bold text-sm animate-pulse tracking-widest uppercase">
            Processing Telemetry...
          </p>
        </div>
      )}
    </div>
  );
};
