import React, { useState } from 'react';
import { CreditCard, Tag, FileText, Send, CheckCircle2 } from 'lucide-react';
import apiClient from '../api/client';

export const Manage: React.FC = () => {
  const [amount, setAmount] = useState('20.0');
  const [category, setCategory] = useState('');
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);

  const handleSave = async () => {
    if (!category || !amount) return;
    setLoading(true);

    try {
      await apiClient.post('/transactions', {
        amount: parseFloat(amount),
        category,
        description,
        date: new Date().toISOString()
      });

      setSuccess(true);
      setCategory('');
      setDescription('');
      setTimeout(() => setSuccess(false), 3000);
    } catch (err) {
      alert("Failed to save transaction. Check if the backend is running.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      <header>
        <h1 className="text-3xl font-bold text-white">Manage Transactions</h1>
        <p className="text-[#8b949e] mt-2">Update your financial ledger.</p>
      </header>

      <div className="bg-[#161b22] border border-[#30363d] rounded-2xl p-10 max-w-2xl shadow-2xl">
        <div className="space-y-6">
          <div className="space-y-2">
            <label className="text-sm font-medium text-[#8b949e] flex items-center gap-2 px-1">
              <CreditCard size={14} /> Amount ($)
            </label>
            <input
              type="text"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
              className="w-full bg-[#0d1117] border border-[#30363d] rounded-xl h-12 px-4 focus:border-[#58a6ff] outline-none text-white transition-colors"
            />
          </div>

          <div className="space-y-2">
            <label className="text-sm font-medium text-[#8b949e] flex items-center gap-2 px-1">
              <Tag size={14} /> Category
            </label>
            <input
              type="text"
              placeholder="e.g. Food, Rent, Tech"
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              className="w-full bg-[#0d1117] border border-[#30363d] rounded-xl h-12 px-4 focus:border-[#58a6ff] outline-none text-white transition-colors"
            />
          </div>

          <div className="space-y-2">
            <label className="text-sm font-medium text-[#8b949e] flex items-center gap-2 px-1">
              <FileText size={14} /> Description
            </label>
            <input
              type="text"
              placeholder="What was this for?"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="w-full bg-[#0d1117] border border-[#30363d] rounded-xl h-12 px-4 focus:border-[#58a6ff] outline-none text-white transition-colors"
            />
          </div>

          <button
            onClick={handleSave}
            disabled={loading}
            className={`w-full h-12 rounded-xl mt-4 font-bold flex items-center justify-center gap-2 transition-all active:scale-95 ${
              success ? "bg-[#2ea043] text-white" : "bg-[#238636] hover:bg-[#2ea043] text-white"
            }`}
          >
            {success ? (
              <><CheckCircle2 size={18} /> Transaction Saved!</>
            ) : loading ? (
              "Processing..."
            ) : (
              <><Send size={18} /> Save Transaction</>
            )}
          </button>
        </div>
      </div>






    </div>
  );
};