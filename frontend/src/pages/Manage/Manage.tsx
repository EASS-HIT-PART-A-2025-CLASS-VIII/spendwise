import React, { useEffect, useState } from 'react';
import {
  AlignLeft,
  Calendar,
  DollarSign,
  Edit3,
  Filter,
  Plus,
  Search,
  Tag,
  Trash2,
  X,
} from 'lucide-react';
import toast, { Toaster } from 'react-hot-toast'; // New import
import apiClient from '../../api/client';
import { type Transaction, type TransactionFormFields } from './types';

export const Manage: React.FC = () => {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [isModalOpen, setIsModalOpen] = useState<boolean>(false);
  const [editingTransaction, setEditingTransaction] = useState<Transaction | null>(null);
  const [search, setSearch] = useState<string>('');
  const [selectedCategory, setSelectedCategory] = useState<string>('All');

  const [formData, setFormData] = useState<TransactionFormFields>({
    category: '',
    amount: '',
    description: '',
  });

  useEffect(() => {
    fetchTransactions();
  }, []);

  const fetchTransactions = async (): Promise<void> => {
    try {
      const res = await apiClient.get<Transaction[]>('/transactions');
      setTransactions(res.data);
    } catch (err) {
      toast.error('Could not sync ledger history');
    }
  };

  const handleOpenCreate = () => {
    setEditingTransaction(null);
    setFormData({ category: '', amount: '', description: '' });
    setIsModalOpen(true);
  };

  const handleOpenEdit = (t: Transaction) => {
    setEditingTransaction(t);
    setFormData({
      category: t.category,
      amount: t.amount.toString(),
      description: t.description || '',
    });
    setIsModalOpen(true);
  };

  const handleSubmit = async (e: React.FormEvent): Promise<void> => {
    e.preventDefault();
    const payload = {
      category: formData.category,
      amount: parseFloat(formData.amount),
      description: formData.description || '',
      date: editingTransaction ? editingTransaction.date : new Date(),
    };

    // Use toast.promise for an even sleeker loading state
    const action = editingTransaction
      ? apiClient.put(`/transactions/${editingTransaction.id}`, payload)
      : apiClient.post('/transactions', payload);

    toast.promise(
      action,
      {
        loading: editingTransaction ? 'Updating record...' : 'Creating entry...',
        success: () => {
          setIsModalOpen(false);
          fetchTransactions();
          return editingTransaction ? 'Transaction updated' : 'Transaction created';
        },
        error: 'Failed to authorize transaction',
      },
      {
        style: {
          background: '#161b22',
          color: '#fff',
          border: '1px solid #30363d',
          borderRadius: '12px',
          fontSize: '14px',
          fontWeight: 'bold',
        },
        iconTheme: {
          primary: '#238636',
          secondary: '#fff',
        },
      }
    );
  };

  const handleDelete = async (id: number): Promise<void> => {
    if (!confirm('Are you sure you want to delete this entry?')) return;
    try {
      await apiClient.delete(`/transactions/${id}`);
      setTransactions((prev) => prev.filter((t) => t.id !== id));
      toast.success('Record purged successfully', {
        style: {
          background: '#161b22',
          color: '#fff',
          border: '1px solid #30363d',
          borderRadius: '12px',
        },
      });
    } catch (err) {
      toast.error('Failed to delete transaction');
    }
  };

  const uniqueCategories = ['All', ...Array.from(new Set(transactions.map((t) => t.category)))];

  const filtered: Transaction[] = transactions.filter((t) => {
    const matchesSearch =
      t.category.toLowerCase().includes(search.toLowerCase()) ||
      t.description?.toLowerCase().includes(search.toLowerCase());
    const matchesCategory = selectedCategory === 'All' || t.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  return (
    <div className="max-w-6xl mx-auto space-y-8 animate-in fade-in duration-700">
      {/* Toast container configuration */}
      <Toaster position="bottom-right" reverseOrder={false} />

      <header className="flex justify-between items-center">
        <h1 className="text-4xl font-black text-white tracking-tighter">
          Transaction <span className="text-[#238636]">Ledger</span>
        </h1>
        <button
          onClick={handleOpenCreate}
          className="bg-[#238636] hover:bg-[#2ea043] text-white px-6 py-3 rounded-2xl font-bold transition-all shadow-lg active:scale-95 flex items-center gap-2"
        >
          <Plus size={20} /> Add Entry
        </button>
      </header>

      <div className="bg-[#161b22] border border-[#30363d] rounded-3xl overflow-hidden shadow-2xl">
        <div className="p-6 border-b border-[#30363d] flex flex-col md:flex-row gap-4 justify-between items-center">
          <div className="relative w-full max-w-md">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-[#8b949e]" size={18} />
            <input
              type="text"
              placeholder="Search history..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full bg-[#0d1117] border border-[#30363d] rounded-xl py-3 pl-12 pr-4 text-white focus:border-[#58a6ff] outline-none transition-all"
            />
          </div>

          <div className="flex items-center gap-2 bg-[#0d1117] border border-[#30363d] p-1 rounded-xl">
            <Filter size={16} className="ml-3 text-[#8b949e]" />
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="bg-transparent text-white text-sm p-2 outline-none cursor-pointer pr-8"
            >
              {uniqueCategories.map((cat) => (
                <option key={cat} value={cat} className="bg-[#161b22]">
                  {cat}
                </option>
              ))}
            </select>
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left">
            <thead>
              <tr className="text-[#8b949e] text-xs uppercase font-bold tracking-widest bg-[#0d1117]/50">
                <th className="px-8 py-5">Category</th>
                <th className="px-8 py-5">Description</th>
                <th className="px-8 py-5">Date</th>
                <th className="px-8 py-5 text-right">Amount</th>
                <th className="px-8 py-5 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#30363d]">
              {filtered.map((t) => (
                <tr key={t.id} className="group hover:bg-[#21262d]/50 transition-all">
                  <td className="px-8 py-6">
                    <div className="flex items-center gap-3">
                      <div className="w-8 h-8 rounded-lg bg-[#238636]/10 flex items-center justify-center text-[#238636] border border-[#238636]/20 font-bold text-xs">
                        {t.category[0].toUpperCase()}
                      </div>
                      <span className="text-white font-bold">{t.category}</span>
                    </div>
                  </td>
                  <td className="px-8 py-6">
                    <span className="text-[#8b949e] text-sm font-medium">
                      {t.description || '—'}
                    </span>
                  </td>
                  <td className="px-8 py-6">
                    <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-[#161b22] text-[#8b949e] text-[10px] font-bold uppercase border border-[#30363d] w-fit">
                      <Calendar size={12} className="text-[#238636]" />
                      {new Date(t.date).toLocaleDateString('en-GB', {
                        day: '2-digit',
                        month: 'short',
                        year: 'numeric',
                      })}
                    </span>
                  </td>
                  <td className="px-8 py-6 text-right">
                    <span className="text-white font-mono font-bold text-lg">
                      ${t.amount.toFixed(2)}
                    </span>
                  </td>
                  <td className="px-8 py-6 text-right">
                    <div className="flex items-center justify-end gap-2 md:opacity-0 group-hover:opacity-100 transition-all">
                      <button
                        onClick={() => handleOpenEdit(t)}
                        className="p-2 text-[#8b949e] hover:text-[#58a6ff] hover:bg-[#58a6ff]/10 rounded-lg transition-all"
                      >
                        <Edit3 size={18} />
                      </button>
                      <button
                        onClick={() => handleDelete(t.id)}
                        className="p-2 text-[#8b949e] hover:text-red-500 hover:bg-red-500/10 rounded-lg transition-all"
                      >
                        <Trash2 size={18} />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {isModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-md animate-in fade-in duration-200">
          <div className="bg-[#161b22] border border-[#444c56] w-full max-w-md rounded-[2rem] shadow-2xl overflow-hidden animate-in zoom-in-95 duration-200">
            <div className="p-6 border-b border-[#30363d] flex justify-between items-center bg-[#0d1117]">
              <h2 className="text-xl font-bold text-white tracking-tight">
                {editingTransaction ? 'Edit Transaction' : 'New Transaction'}
              </h2>
              <button
                onClick={() => setIsModalOpen(false)}
                className="p-2 hover:bg-[#30363d] rounded-full text-[#8b949e] transition-colors"
              >
                <X size={20} />
              </button>
            </div>

            <form onSubmit={handleSubmit} className="p-8 space-y-5">
              <div className="space-y-2">
                <label className="text-sm font-semibold text-[#8b949e] flex items-center gap-2">
                  <Tag size={16} className="text-[#238636]" /> Category
                </label>
                <input
                  required
                  value={formData.category}
                  onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                  className="w-full bg-[#0d1117] border border-[#30363d] rounded-2xl p-4 text-white outline-none focus:border-[#238636] transition-all"
                />
              </div>

              <div className="space-y-2">
                <label className="text-sm font-semibold text-[#8b949e] flex items-center gap-2">
                  <DollarSign size={16} className="text-[#238636]" /> Amount
                </label>
                <input
                  required
                  type="number"
                  step="0.01"
                  value={formData.amount}
                  onChange={(e) => setFormData({ ...formData, amount: e.target.value })}
                  className="w-full bg-[#0d1117] border border-[#30363d] rounded-2xl p-4 text-white outline-none focus:border-[#238636] transition-all"
                />
              </div>

              <div className="space-y-2">
                <label className="text-sm font-semibold text-[#8b949e] flex items-center gap-2">
                  <AlignLeft size={16} className="text-[#238636]" /> Notes
                </label>
                <textarea
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  className="w-full bg-[#0d1117] border border-[#30363d] rounded-2xl p-4 text-white outline-none focus:border-[#238636] transition-all h-24 resize-none"
                />
              </div>

              <div className="pt-4">
                <button
                  type="submit"
                  className="w-full bg-[#238636] hover:bg-[#2ea043] text-white font-black py-4 rounded-2xl transition-all shadow-lg active:scale-[0.98] tracking-widest"
                >
                  {editingTransaction ? 'Update Transaction' : 'Add Transaction'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
