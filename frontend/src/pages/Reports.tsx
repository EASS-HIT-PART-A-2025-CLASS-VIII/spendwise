import React, { useEffect, useState } from 'react';
import {
  FileText,
  Download,
  RefreshCw,
  Clock,
  ChevronRight,
  FileCheck,
  Search,
} from 'lucide-react';
import toast, { Toaster } from 'react-hot-toast';
import apiClient from '../api/client';

export const Reports: React.FC = () => {
  const [reports, setReports] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);
  const [isGenerating, setIsGenerating] = useState(false);

  useEffect(() => {
    fetchReports();
  }, []);

  const fetchReports = async () => {
    try {
      const res = await apiClient.get<string[]>('/transactions/report/list');
      setReports(res.data);
    } catch (err) {
      toast.error('Failed to sync vault');
    } finally {
      setLoading(false);
    }
  };

  const handleGenerate = async () => {
    setIsGenerating(true);
    try {
      await apiClient.post('/transactions/report');
      toast.success('Report generation initialized');
      // Polling for the new file
      setTimeout(fetchReports, 3000);
    } catch (err) {
      toast.error('Worker core unavailable');
    } finally {
      setIsGenerating(false);
    }
  };

  const handleDownload = (filename: string) => {
    const url = `${import.meta.env.VITE_API_URL}/static/reports/${filename}`;
    window.open(url, '_blank');
  };

  return (
    <div className="max-w-6xl mx-auto space-y-8 animate-in fade-in duration-700">
      <Toaster position="bottom-right" />

      <header className="flex justify-between items-end">
        <div>
          <h1 className="text-4xl font-black text-white tracking-tighter">
            Executive <span className="text-[#58a6ff]">Vault</span>
          </h1>
          <p className="text-[#8b949e] font-medium mt-1">
            Archived financial statements and PDF exports.
          </p>
        </div>
        <button
          onClick={handleGenerate}
          disabled={isGenerating}
          className="bg-[#161b22] border border-[#30363d] hover:border-[#58a6ff] text-white px-6 py-3 rounded-2xl font-bold transition-all flex items-center gap-2 group shadow-xl"
        >
          {isGenerating ? <RefreshCw className="animate-spin" size={18} /> : <FileText size={18} />}
          {isGenerating ? 'Compiling Data...' : 'Generate Statement'}
        </button>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {/* Active Generation Card */}
        {isGenerating && (
          <div className="bg-[#161b22] border border-[#238636] p-6 rounded-3xl animate-pulse">
            <div className="flex justify-between items-start mb-4">
              <div className="p-3 bg-[#238636]/10 rounded-2xl text-[#238636]">
                <RefreshCw className="animate-spin" size={24} />
              </div>
            </div>
            <p className="text-white font-bold text-lg">Current Month Statement</p>
            <p className="text-[#8b949e] text-sm mt-1">Aggregating telemetry logs...</p>
          </div>
        )}

        {/* Existing Reports */}
        {reports.length > 0
          ? reports.map((filename, i) => (
              <div
                key={i}
                className="bg-[#161b22] border border-[#30363d] p-6 rounded-3xl hover:border-[#58a6ff] transition-all group cursor-pointer"
                onClick={() => handleDownload(filename)}
              >
                <div className="flex justify-between items-start mb-6">
                  <div className="p-3 bg-[#58a6ff]/10 rounded-2xl text-[#58a6ff] group-hover:bg-[#58a6ff] group-hover:text-white transition-all">
                    <FileCheck size={24} />
                  </div>
                  <div className="p-2 bg-[#0d1117] rounded-lg text-[#484f58]">
                    <Download size={16} />
                  </div>
                </div>
                <div>
                  <p className="text-white font-bold text-lg truncate">{filename}</p>
                  <div className="flex items-center gap-4 mt-2">
                    <div className="flex items-center gap-1 text-[10px] font-black uppercase text-[#8b949e] tracking-widest">
                      <Clock size={12} /> Ready
                    </div>
                    <div className="text-[10px] font-black uppercase text-[#238636] tracking-widest">
                      PDF format
                    </div>
                  </div>
                </div>
              </div>
            ))
          : !loading &&
            !isGenerating && (
              <div className="col-span-full py-20 bg-[#161b22] border border-dashed border-[#30363d] rounded-[3rem] text-center">
                <div className="inline-flex p-5 bg-[#0d1117] rounded-full text-[#30363d] mb-4">
                  <Search size={40} />
                </div>
                <p className="text-[#8b949e] font-bold text-xl">The vault is currently empty.</p>
                <p className="text-[#484f58] text-sm mt-1">
                  Generate your first statement to see it here.
                </p>
              </div>
            )}
      </div>

      {/* Info Section */}
      <div className="bg-[#0d1117] border border-[#30363d] p-8 rounded-[2.5rem] flex flex-col md:flex-row items-center gap-6">
        <div className="p-4 bg-[#58a6ff]/10 rounded-2xl text-[#58a6ff]">
          <RefreshCw size={32} />
        </div>
        <div className="flex-1 text-center md:text-left">
          <h4 className="text-white font-bold text-lg">Auto-Archiving Intelligence</h4>
          <p className="text-[#8b949e] text-sm mt-1">
            Reports are generated using our background worker core. This ensures zero downtime while
            your statements are being encrypted and compiled.
          </p>
        </div>
      </div>
    </div>
  );
};
