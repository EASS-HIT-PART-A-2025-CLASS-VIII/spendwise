import React, { useEffect, useState } from 'react';
import { Activity, Calendar, TrendingUp, Zap, ArrowRight, BarChart3 } from 'lucide-react';
import {
  Area,
  AreaChart,
  Cell,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';
import { useNavigate } from 'react-router-dom';
import apiClient from '../api/client';

export const Dashboard: React.FC = () => {
  const [stats, setStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    apiClient
      .get('/transactions/stats/detailed')
      .then((res) => setStats(res.data))
      .finally(() => setLoading(false));
  }, []);

  if (loading)
    return (
      <div className="h-[80vh] flex items-center justify-center">
        <div className="flex flex-col items-center gap-4">
          <div className="w-12 h-12 border-4 border-[#58a6ff]/20 border-t-[#58a6ff] rounded-full animate-spin" />
          <span className="text-[#8b949e] font-bold text-xs uppercase tracking-widest">
            Synchronizing Telemetry
          </span>
        </div>
      </div>
    );

  if (!stats || stats.history.length === 0) {
    return (
      <div className="h-[80vh] flex flex-col items-center justify-center text-center animate-in fade-in zoom-in duration-700">
        <div className="relative mb-8">
          <div className="absolute inset-0 bg-[#58a6ff] blur-3xl opacity-10 animate-pulse" />
          <div className="relative w-24 h-24 bg-[#161b22] border border-[#30363d] rounded-[2.5rem] flex items-center justify-center text-[#58a6ff] shadow-2xl">
            <BarChart3 size={40} />
          </div>
        </div>
        <h2 className="text-4xl font-black text-white tracking-tighter">Initialize Your Ledger</h2>
        <p className="text-[#8b949e] mt-4 max-w-sm font-medium leading-relaxed">
          Your executive dashboard is currently offline. Deploy your first transaction to activate
          category mixing and velocity analytics.
        </p>
        <button
          onClick={() => navigate('/manage')}
          className="mt-10 px-10 py-4 bg-white text-black font-black rounded-2xl hover:bg-[#f6f8fa] transition-all shadow-xl uppercase tracking-widest text-[10px] flex items-center gap-3 group"
        >
          Record First Entry{' '}
          <ArrowRight size={16} className="group-hover:translate-x-1 transition-transform" />
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-1000">
      <header className="flex justify-between items-center">
        <h1 className="text-4xl font-black text-white tracking-tighter">
          Executive <span className="text-[#58a6ff]">Summary</span>
        </h1>
        <div className="bg-[#161b22] border border-[#30363d] px-4 py-2 rounded-xl text-sm text-[#8b949e] flex items-center gap-2 font-bold uppercase tracking-tighter">
          <Calendar size={16} className="text-[#58a6ff]" />{' '}
          {new Date().toLocaleDateString('en-US', { month: 'long', year: 'numeric' })}
        </div>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <MetricCard
          label="Monthly Burn"
          value={`$${stats.monthly_burn.toLocaleString()}`}
          trend={`${stats.trend_pct}%`}
          isUp={stats.trend_pct > 0}
          icon={<Zap size={20} />}
        />
        <MetricCard
          label="Daily Velocity"
          value={`$${stats.daily_avg.toFixed(2)}`}
          trend="Stable"
          isUp={null}
          icon={<Activity size={20} />}
        />
        <MetricCard
          label="Efficiency"
          value={`${stats.efficiency_score}/100`}
          trend="Optimized"
          isUp={null}
          icon={<TrendingUp size={20} />}
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="bg-[#161b22] border border-[#30363d] rounded-3xl p-8 shadow-2xl">
          <h3 className="text-[10px] font-black uppercase tracking-[0.2em] text-[#8b949e] mb-6">
            Category Mix
          </h3>
          <div className="h-[250px]">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={stats.categories}
                  innerRadius={70}
                  outerRadius={90}
                  paddingAngle={8}
                  dataKey="value"
                >
                  {stats.categories.map((_: any, i: number) => (
                    <Cell
                      key={i}
                      fill={['#58a6ff', '#238636', '#f85149', '#d29922'][i % 4]}
                      stroke="none"
                    />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#0d1117',
                    border: 'none',
                    borderRadius: '12px',
                  }}
                  itemStyle={{ color: 'white' }}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="lg:col-span-2 bg-[#161b22] border border-[#30363d] rounded-3xl p-8 shadow-2xl">
          <h3 className="text-[10px] font-black uppercase tracking-[0.2em] text-[#8b949e] mb-6">
            Spending Velocity (30D)
          </h3>
          <div className="h-[250px]">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={stats.history}>
                <defs>
                  <linearGradient id="colorAmt" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#58a6ff" stopOpacity={0.3} />
                    <stop offset="95%" stopColor="#58a6ff" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <XAxis dataKey="date" hide />
                <YAxis hide />
                <Tooltip contentStyle={{ backgroundColor: '#0d1117', border: 'none' }} />
                <Area
                  type="monotone"
                  dataKey="amount"
                  stroke="#58a6ff"
                  fillOpacity={1}
                  fill="url(#colorAmt)"
                  strokeWidth={3}
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
};

const MetricCard = ({ label, value, trend, isUp, icon }: any) => (
  <div className="bg-[#161b22] border border-[#30363d] p-8 rounded-[2rem] group hover:border-[#444c56] transition-all shadow-xl">
    <div className="flex justify-between items-start mb-6">
      <div className="p-3 bg-[#0d1117] rounded-2xl text-[#58a6ff] border border-[#30363d] group-hover:bg-[#58a6ff] group-hover:text-white transition-all">
        {icon}
      </div>
      {isUp !== null && (
        <span
          className={`text-[10px] font-black px-2 py-1 rounded-lg uppercase tracking-tighter ${
            isUp ? 'bg-red-500/10 text-red-500' : 'bg-green-500/10 text-green-500'
          }`}
        >
          {trend}
        </span>
      )}
    </div>
    <p className="text-[10px] font-black text-[#8b949e] uppercase tracking-[0.2em]">{label}</p>
    <h2 className="text-4xl font-black text-white mt-1 tracking-tighter">{value}</h2>
  </div>
);
