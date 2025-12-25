import React, { useEffect, useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import {
  LayoutDashboard,
  CreditCard,
  BrainCircuit,
  FileText,
  LogOut,
  UserCircle,
} from 'lucide-react';
import { Logo } from '../components/Logo.tsx';

interface Props {
  children: React.ReactNode;
}

export const MainLayout: React.FC<Props> = ({ children }) => {
  const location = useLocation();
  const [username, setUsername] = useState('');

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      try {
        const base64Url = token.split('.')[1];
        const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
        const payload = JSON.parse(window.atob(base64));
        if (payload.sub) {
          setUsername(payload.sub);
        }
      } catch (e) {
        console.error('Token identification failed');
      }
    }
  }, []);

  const navItems = [
    { name: 'Dashboard', path: '/', icon: LayoutDashboard },
    { name: 'Manage', path: '/manage', icon: CreditCard },
    { name: 'AI Advisor', path: '/ai', icon: BrainCircuit },
    { name: 'Reports', path: '/reports', icon: FileText },
  ];

  const handleLogout = () => {
    localStorage.clear();
    window.location.href = '/login';
  };

  return (
    <div className="flex min-h-screen bg-[#0d1117] text-[#c9d1d9]">
      <aside className="w-64 bg-[#161b22] border-r border-[#30363d] flex flex-col fixed h-full">
        <div className="p-6">
          <Logo />
        </div>

        <nav className="flex-1 px-4 space-y-2">
          {navItems.map((item) => {
            const isActive = location.pathname === item.path;
            return (
              <Link
                key={item.name}
                to={item.path}
                className={`flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 ${
                  isActive
                    ? 'bg-[#238636] text-white shadow-lg shadow-[#238636]/20'
                    : 'text-[#8b949e] hover:bg-[#21262d] hover:text-white'
                }`}
              >
                <item.icon size={20} strokeWidth={isActive ? 2.5 : 2} />
                <span className={`font-bold text-sm ${isActive ? 'text-white' : ''}`}>
                  {item.name}
                </span>
              </Link>
            );
          })}
        </nav>

        <div className="p-4 bg-[#161b22] border-t border-[#30363d] space-y-2">
          <div className="group p-3 bg-[#0d1117] border border-[#30363d] rounded-2xl flex items-center gap-3 shadow-inner transition-all hover:border-[#444c56]">
            <div className="relative flex-shrink-0">
              <div className="w-2.5 h-2.5 rounded-full bg-[#238636] absolute -top-0.5 -right-0.5 border-2 border-[#0d1117] z-10" />
              <div className="w-9 h-9 rounded-xl bg-[#161b22] border border-[#30363d] flex items-center justify-center text-[#58a6ff] group-hover:text-white transition-colors">
                <UserCircle size={20} />
              </div>
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-bold text-white truncate leading-tight">
                Hello, {username || 'Executive'}
              </p>
            </div>
          </div>

          <button
            onClick={handleLogout}
            className="flex items-center gap-3 px-4 py-3 w-full text-[#8b949e] hover:text-[#f85149] transition-all duration-200 rounded-xl hover:bg-[#2d1616] group"
          >
            <LogOut size={18} className="transition-transform group-hover:-translate-x-1" />
            <span className="font-bold text-sm tracking-widest">Logout</span>
          </button>
        </div>
      </aside>

      <main className="flex-1 ml-64 p-10">
        <div className="max-w-5xl mx-auto">{children}</div>
      </main>
    </div>
  );
};
