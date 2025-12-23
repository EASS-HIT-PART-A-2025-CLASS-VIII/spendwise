import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { LayoutDashboard, CreditCard, BrainCircuit, FileText, LogOut } from 'lucide-react';
import { Logo } from '../components/Logo.tsx';

interface Props {
  children: React.ReactNode;
}

export const MainLayout: React.FC<Props> = ({ children }) => {
  const location = useLocation();

  const navItems = [
    { name: 'Dashboard', path: '/', icon: LayoutDashboard },
    { name: 'Manage', path: '/manage', icon: CreditCard },
    { name: 'AI Advisor', path: '/ai', icon: BrainCircuit },
    { name: 'Reports', path: '/reports', icon: FileText },
  ];

  const handleLogout = () => {
    localStorage.clear(); // Clears token
    window.location.href = '/login'; // Full reload to clear app state
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
                    ? 'bg-[#238636] text-white shadow-lg'
                    : 'text-[#8b949e] hover:bg-[#21262d] hover:text-white'
                }`}
              >
                <item.icon size={20} strokeWidth={isActive ? 2.5 : 2} />
                <span className="font-medium">{item.name}</span>
              </Link>
            );
          })}
        </nav>

        <div className="p-4 border-t border-[#30363d]">
          <button
            onClick={handleLogout}
            className="flex items-center gap-3 px-4 py-3 w-full text-[#8b949e] hover:text-[#f85149] transition-colors rounded-xl hover:bg-[#2d1616]"
          >
            <LogOut size={20} />
            <span className="font-medium">Logout</span>
          </button>
        </div>
      </aside>

      <main className="flex-1 ml-64 p-10">
        <div className="max-w-5xl mx-auto">{children}</div>
      </main>
    </div>
  );
};
