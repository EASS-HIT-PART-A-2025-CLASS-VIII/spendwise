import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Lock, User, LogIn } from 'lucide-react';
import apiClient from '../api/client';

export const Login: React.FC = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const formData = new URLSearchParams();
      formData.append('username', username);
      formData.append('password', password);

      const response = await apiClient.post('/auth/token', formData, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      });

      if (response.data.access_token) {
        localStorage.setItem('token', response.data.access_token);
        window.location.href = '/';
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Invalid username or password');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#0d1117] flex items-center justify-center p-6 text-[#c9d1d9]">
      <div className="w-full max-w-md bg-[#161b22] border border-[#30363d] rounded-2xl p-10 shadow-2xl">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-black text-white tracking-tighter">
            Spend<span className="text-[#58a6ff]">Wise</span>
          </h1>
          <p className="text-[#8b949e] text-sm mt-2 font-medium">Log in to your account</p>
        </div>

        <form onSubmit={handleLogin} className="space-y-6">
          <div className="space-y-2">
            <label className="text-sm font-medium text-[#8b949e] flex items-center gap-2 px-1">
              <User size={14} /> Username
            </label>
            <input
              type="text"
              required
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full bg-[#0d1117] border border-[#30363d] rounded-xl h-12 px-4 focus:border-[#58a6ff] outline-none transition-all text-white"
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
            />
          </div>

          {error && (
            <p className="text-[#f85149] text-sm text-center font-medium bg-[#2d1616] p-2 rounded-lg border border-[#f85149]/20">
              {error}
            </p>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-[#238636] hover:bg-[#2ea043] text-white font-bold h-12 rounded-xl mt-4 transition-all flex items-center justify-center gap-2 shadow-lg disabled:opacity-50"
          >
            {loading ? (
              'Authenticating...'
            ) : (
              <>
                <LogIn size={18} /> Sign In
              </>
            )}
          </button>
        </form>

        <div className="mt-8 text-center border-t border-[#30363d] pt-6">
          <p className="text-[#8b949e] text-sm">
            New to SpendWise?{' '}
            <Link to="/register" className="text-[#58a6ff] font-bold hover:underline">
              Create an account
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};
