import React, { useEffect, useState, useRef } from 'react';
import { FileText, Download, RefreshCw, Clock, FileCheck, Search } from 'lucide-react';
import toast, { Toaster } from 'react-hot-toast';
import apiClient from '../api/client';

export const Reports: React.FC = () => {
  const [reports, setReports] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);
  const [isGenerating, setIsGenerating] = useState(false);

  // Use a ref to keep track of the count for polling comparison
  const reportCountRef = useRef(0);

  useEffect(() => {
    fetchReports();
  }, []);

  const fetchReports = async () => {
    try {
      const res = await apiClient.get<string[]>('/transactions/report/list');
      setReports(res.data);
      reportCountRef.current = res.data.length;
    } catch (err) {
      toast.error('Failed to sync vault');
    } finally {
      setLoading(false);
    }
  };

  const handleGenerate = async () => {
    if (isGenerating) return;

    setIsGenerating(true);
    try {
      await apiClient.post('/transactions/report');
      toast.success('Report generation initialized');

      let attempts = 0;
      const maxAttempts = 20; // 40 seconds total

      const interval = setInterval(async () => {
        try {
          const res = await apiClient.get<string[]>('/transactions/report/list');

          // Check if a new file has appeared in the list
          if (res.data.length > reportCountRef.current) {
            setReports(res.data);
            reportCountRef.current = res.data.length;
            setIsGenerating(false);
            clearInterval(interval);
            toast.success('Report Ready in Vault');
          } else if (attempts >= maxAttempts) {
            setIsGenerating(false);
            clearInterval(interval);
            toast.error('Generation timed out. Please refresh.');
          }
          attempts++;
        } catch (error) {
          clearInterval(interval);
          setIsGenerating(false);
        }
      }, 2000);
    } catch (err) {
      toast.error('Worker core unavailable');
      setIsGenerating(false);
    }
  };

  const handleDownload = (filename: string) => {
    // UPDATED: Points to your new mount path in main.py
    const url = `${import.meta.env.VITE_API_URL}/reports-files/${filename}`;

    // Create a temporary anchor to force download behavior
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', filename);
    link.setAttribute('target', '_blank');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
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
          className={`px-6 py-3 rounded-2xl font-bold transition-all flex items-center gap-2 group shadow-xl border ${
            isGenerating
              ? 'bg-[#0d1117] border-[#30363d] text-[#8b949e] cursor-not-allowed'
              : 'bg-[#161b22] border-[#30363d] hover:border-[#58a6ff] text-white'
          }`}
        >
          {isGenerating ? <RefreshCw className="animate-spin" size={18} /> : <FileText size={18} />}
          {isGenerating ? 'Compiling Data...' : 'Generate Statement'}
        </button>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {isGenerating && (
          <div className="bg-[#161b22] border border-[#238636] p-6 rounded-3xl animate-pulse flex flex-col justify-between">
            <div className="p-3 bg-[#238636]/10 rounded-2xl text-[#238636] w-fit">
              <RefreshCw className="animate-spin" size={24} />
            </div>
            <div className="mt-6">
              <p className="text-white font-bold text-lg">System Compiling...</p>
              <p className="text-[#8b949e] text-sm mt-1">Fetching records from SQLite...</p>
            </div>
          </div>
        )}

        {reports.map((filename) => (
          <div
            key={filename}
            className="bg-[#161b22] border border-[#30363d] p-6 rounded-3xl hover:border-[#58a6ff] transition-all group relative overflow-hidden"
          >
            <div className="flex justify-between items-start mb-6">
              <div className="p-3 bg-[#58a6ff]/10 rounded-2xl text-[#58a6ff] group-hover:bg-[#58a6ff] group-hover:text-white transition-all">
                <FileCheck size={24} />
              </div>
              <button
                onClick={() => handleDownload(filename)}
                className="p-2 bg-[#0d1117] rounded-lg text-[#484f58] hover:text-[#58a6ff] transition-colors"
                title="Download"
              >
                <Download size={18} />
              </button>
            </div>
            <div>
              <p className="text-white font-bold text-lg truncate pr-4">{filename}</p>
              <div className="flex items-center gap-4 mt-2">
                <span className="flex items-center gap-1 text-[10px] font-black uppercase text-[#8b949e] tracking-widest">
                  <Clock size={12} /> Verified
                </span>
                <span className="text-[10px] font-black uppercase text-[#238636] tracking-widest">
                  PDF Secure
                </span>
              </div>
            </div>
          </div>
        ))}

        {!loading && !isGenerating && reports.length === 0 && (
          <div className="col-span-full py-20 bg-[#161b22] border border-dashed border-[#30363d] rounded-[3rem] text-center">
            <div className="inline-flex p-5 bg-[#0d1117] rounded-full text-[#30363d] mb-4">
              <Search size={40} />
            </div>
            <p className="text-[#8b949e] font-bold text-xl">The vault is currently empty.</p>
            <p className="text-[#484f58] text-sm mt-1">
              Generate your first statement to start archiving.
            </p>
          </div>
        )}
      </div>

      <div className="bg-[#0d1117] border border-[#30363d] p-8 rounded-[2.5rem] flex flex-col md:flex-row items-center gap-6">
        <div className="p-4 bg-[#58a6ff]/10 rounded-2xl text-[#58a6ff]">
          <RefreshCw size={32} />
        </div>
        <div className="flex-1 text-center md:text-left">
          <h4 className="text-white font-bold text-lg">Background Processing Core</h4>
          <p className="text-[#8b949e] text-sm mt-1">
            Statements are compiled using an isolated Redis worker. This ensures your dashboard
            remains responsive while complex PDF calculations are performed.
          </p>
        </div>
      </div>
    </div>
  );
};
