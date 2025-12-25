import React, { useEffect, useRef } from 'react';
import { RefreshCcw, Send, Square, Copy, Zap, Target, ShieldCheck, Sparkles } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import toast, { Toaster } from 'react-hot-toast';
import { useAI } from '../context/AIContext';

export const AIAdvisor: React.FC = () => {
  const { query, setQuery, advice, setAdvice, loading, askAI, handleStop } = useAI();
  const scrollRef = useRef<HTMLDivElement>(null);

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

  const handleAction = () => {
    if (loading) {
      handleStop();
    } else {
      askAI();
    }
  };

  const handleCopy = () => {
    if (!advice) return;
    navigator.clipboard.writeText(advice);
    toast.success('Strategic Insights Copied', {
      style: {
        background: '#161b22',
        color: '#fff',
        border: '1px solid #30363d',
      },
    });
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') {
      e.preventDefault();
      askAI();
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-10 animate-in fade-in duration-1000 pb-20">
      <Toaster position="bottom-right" />

      <header className="text-center">
        <h1 className="text-5xl font-black text-white tracking-tighter leading-none mb-2">
          Spend<span className="text-[#58a6ff]">Wise</span>
        </h1>
        <h1 className="text-3xl font-black text-white tracking-tighter leading-none">
          Intelligence
        </h1>
        <div className="h-1 w-12 bg-[#238636] mx-auto rounded-full mt-4" />
      </header>

      <div className="relative group">
        <div className="absolute -inset-1 bg-gradient-to-r from-[#238636]/10 to-[#58a6ff]/10 rounded-[2.5rem] blur opacity-25 group-hover:opacity-40 transition duration-1000"></div>
        <div className="relative bg-[#161b22] border border-[#30363d] rounded-[2rem] p-8 shadow-2xl">
          <div className="space-y-6">
            <div className="flex items-center justify-between px-1">
              <label className="text-sm font-bold text-[#8b949e] tracking-widest flex items-center gap-2">
                <Sparkles size={16} className="text-[#238636]" /> Ask Anything
              </label>
              <div className="flex gap-2">
                {suggestions.map((s) => (
                  <button
                    key={s.label}
                    onClick={() => askAI(s.label)}
                    className="hidden md:flex items-center gap-1.5 px-3 py-1.5 bg-[#0d1117] border border-[#30363d] rounded-full text-[10px] font-bold text-[#8b949e] hover:border-[#238636] hover:text-white transition-all"
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
                placeholder="Analyze my fiscal telemetry..."
                className="w-full bg-[#0d1117] border border-[#30363d] rounded-2xl min-h-[160px] p-6 focus:border-[#238636] focus:ring-1 focus:ring-[#238636] outline-none transition-all text-white text-lg leading-relaxed resize-none shadow-inner placeholder:text-[#30363d]"
              />
              <div className="absolute bottom-4 right-4 flex items-center gap-3">
                <span className="text-[10px] font-bold text-[#484f58] uppercase hidden sm:block">
                  CMD + Enter
                </span>
                <button
                  onClick={handleAction}
                  disabled={!loading && !query.trim()}
                  className={`${
                    loading ? 'bg-red-500 hover:bg-red-600' : 'bg-[#238636] hover:bg-[#2ea043]'
                  } p-4 rounded-xl text-white transition-all shadow-xl active:scale-90 flex items-center justify-center`}
                >
                  {loading ? <Square size={20} className="fill-white" /> : <Send size={20} />}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* RESTORED TELEMETRY LOADING STATE */}
      {loading && !advice && (
        <div className="flex flex-col items-center justify-center py-12 space-y-4 animate-in fade-in duration-500">
          <div className="w-12 h-12 border-4 border-[#238636]/20 border-t-[#238636] rounded-full animate-spin shadow-[0_0_20px_rgba(35,134,54,0.2)]" />
          <p className="text-[#8b949e] font-black text-[10px] animate-pulse tracking-[0.3em] uppercase">
            Processing Telemetry...
          </p>
        </div>
      )}

      {advice && (
        <div ref={scrollRef} className="animate-in slide-in-from-top-4 fade-in duration-500">
          <div className="bg-[#161b22] border border-[#30363d] rounded-[2rem] overflow-hidden shadow-2xl">
            <div className="bg-[#0d1117] px-8 py-4 border-b border-[#30363d] flex justify-between items-center">
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-[#238636] animate-pulse" />
                <span className="text-[10px] font-black text-[#8b949e] uppercase tracking-widest">
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
                          className="text-[#238636] font-black text-2xl mt-6 mb-4 tracking-tighter"
                          {...props}
                        />
                      ),
                      ul: ({ ...props }) => (
                        <ul
                          className="list-disc list-inside space-y-2 text-[#8b949e] font-medium"
                          {...props}
                        />
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
                  <span className="text-[10px] font-bold uppercase tracking-wider">
                    AI generated insight •{' '}
                    {new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </span>
                </div>
                <button
                  onClick={handleCopy}
                  className="flex items-center gap-2 px-6 py-3 bg-[#0d1117] border border-[#30363d] rounded-xl text-xs font-bold text-white hover:border-[#238636] hover:bg-[#161b22] transition-all shadow-lg active:scale-95"
                >
                  <Copy size={14} /> Copy Strategic Insights
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
