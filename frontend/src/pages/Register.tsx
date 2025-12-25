import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Lock, User, ShieldCheck, AlertCircle } from 'lucide-react';
import apiClient from '../api/client';
import toast, { Toaster } from 'react-hot-toast';

export const Register: React.FC = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [loading, setLoading] = useState(false);

  const validateForm = () => {
    const hasNumber = /\d/.test(password);
    const hasSpecial = /[^A-Za-z0-9]/.test(password);

    if (username.length < 4) {
      toast.error('Username must be at least 4 characters');
      return false;
    }
    if (password.length < 8) {
      toast.error('Password must be at least 8 characters');
      return false;
    }
    if (!hasNumber || !hasSpecial) {
      toast.error('Password requires 1 number and 1 special character');
      return false;
    }
    if (password !== confirmPassword) {
      toast.error('Passwords do not match');
      return false;
    }
    return true;
  };

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validateForm()) return;

    setLoading(true);

    try {
      const response = await apiClient.post('/auth/register', {
        username,
        password,
      });

      if (response.data.access_token) {
        localStorage.setItem('token', response.data.access_token);
        toast.success('Registration successful. Access granted.');

        setTimeout(() => {
          window.location.href = '/';
        }, 1000);
      }
    } catch (err: any) {
      const detail = err.response?.data?.detail;
      toast.error(typeof detail === 'string' ? detail : 'System registration error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#0d1117] flex items-center justify-center p-6 text-[#c9d1d9]">
      <Toaster position="bottom-right" />
      <div className="w-full max-w-md bg-[#161b22] border border-[#30363d] rounded-2xl p-10 shadow-2xl">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-black text-white tracking-tighter">
            Spend<span className="text-[#58a6ff]">Wise</span>
          </h1>
          <p className="text-[#8b949e] text-sm mt-2 font-medium">Create your account today</p>
        </div>

        <form onSubmit={handleRegister} className="space-y-4">
          <div className="space-y-2">
            <label className="text-sm font-medium text-[#8b949e] flex items-center gap-2 px-1">
              <User size={14} /> Username
            </label>
            <input
              type="text"
              required
              value={username}
              onChange={(e) => setUsername(e.target.value.toLowerCase().trim())}
              className="w-full bg-[#0d1117] border border-[#30363d] rounded-xl h-12 px-4 focus:border-[#58a6ff] outline-none transition-all text-white"
              placeholder="johndoe"
            />
          </div>

          <div className="space-y-2">
            <label className="text-sm font-medium text-[#8b949e] flex items-center gap-2 px-1">
              <Lock size={14} /> Password
            </label>
            <input
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full bg-[#0d1117] border border-[#30363d] rounded-xl h-12 px-4 focus:border-[#58a6ff] outline-none transition-all text-white"
              placeholder="••••••••"
            />
          </div>

          <div className="space-y-2">
            <label className="text-sm font-medium text-[#8b949e] flex items-center gap-2 px-1">
              <ShieldCheck size={14} /> Confirm Password
            </label>
            <input
              type="password"
              required
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              className={`w-full bg-[#0d1117] border rounded-xl h-12 px-4 outline-none transition-all text-white ${
                confirmPassword && password !== confirmPassword
                  ? 'border-red-500/50'
                  : 'border-[#30363d]'
              }`}
              placeholder="••••••••"
            />
            {confirmPassword && password !== confirmPassword && (
              <p className="text-red-500 text-xs font-bold flex items-center gap-1 mt-1 ml-1">
                <AlertCircle size={12} /> Passwords do not match
              </p>
            )}
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-[#238636] hover:bg-[#2ea043] text-white font-bold h-12 rounded-xl mt-4 transition-all shadow-lg disabled:opacity-50"
          >
            {loading ? 'Processing...' : 'Sign Up'}
          </button>
        </form>

        <div className="mt-8 text-center border-t border-[#30363d] pt-6">
          <p className="text-[#8b949e] text-sm">
            Already registered?{' '}
            <Link to="/login" className="text-[#58a6ff] font-bold hover:underline">
              Sign In
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};
