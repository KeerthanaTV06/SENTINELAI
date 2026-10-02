import React, { useState } from 'react';
import LSTM_Dashboard from './components/LSTM_Dashboard';
import CNN_Dashboard from './components/CNN_Dashboard';
import XGBoost_Dashboard from './components/XGBoost_Dashboard';
import InferenceBoard from './components/InferenceBoard';
import DatasetsBoard from './components/DatasetsBoard';
import ConnectionBoard from './components/ConnectionBoard';
import { Activity, Shield, Globe, Cpu, Database, Wifi, Menu, Zap } from 'lucide-react';

export default function App() {
  const [activeTab, setActiveTab] = useState('lstm');

  const navItems = [
    { id: 'lstm', label: 'LSTM (Network)', icon: Activity, section: 'Models' },
    { id: 'cnn', label: '1D-CNN (Malware)', icon: Shield, section: 'Models' },
    { id: 'xgboost', label: 'XGBoost (Phishing)', icon: Globe, section: 'Models' },
    { id: 'inference', label: 'Inference', icon: Cpu, section: 'Operations' },
    { id: 'datasets', label: 'Datasets', icon: Database, section: 'Operations' },
    { id: 'connections', label: 'Connections', icon: Wifi, section: 'System' }
  ];

  return (
    <div className="min-h-screen bg-[#121212] text-[#e5e5e5] flex font-sans selection:bg-indigo-500/30">
      {/* Sidebar Navigation */}
      <aside className="w-72 bg-[#1a1a1a] border-r border-[#2d2d2d] flex flex-col shadow-2xl z-10 relative">
        <div className="p-6 border-b border-[#2d2d2d] flex flex-col relative overflow-hidden">
          <div className="absolute top-0 right-0 w-32 h-32 bg-indigo-500/10 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2"></div>
          
          <div className="flex items-center gap-3 mb-6 relative z-10">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center shadow-lg shadow-indigo-500/20">
              <Zap className="text-white fill-white/20" size={20} />
            </div>
            <div>
              <h1 className="text-2xl font-black tracking-tight text-white flex items-center gap-1">
                SENTINEL<span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-purple-400">AI</span>
              </h1>
              <p className="text-[10px] uppercase tracking-widest text-indigo-300/70 font-semibold mt-0.5">Model Analytics Center</p>
            </div>
          </div>
          
          <div className="flex gap-2 relative z-10">
             <div className="flex-1 bg-emerald-500/10 border border-emerald-500/20 rounded-lg py-2 px-3 flex flex-col items-center justify-center">
               <span className="text-[10px] text-emerald-400/80 uppercase font-bold tracking-wider mb-0.5">System</span>
               <span className="text-xs font-semibold text-emerald-300 flex items-center gap-1.5">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 shadow-[0_0_5px_#34d399]"></span> OK
               </span>
             </div>
             <div className="flex-1 bg-indigo-500/10 border border-indigo-500/20 rounded-lg py-2 px-3 flex flex-col items-center justify-center">
               <span className="text-[10px] text-indigo-400/80 uppercase font-bold tracking-wider mb-0.5">Backend</span>
               <span className="text-xs font-semibold text-indigo-300 flex items-center gap-1.5">
                  <span className="w-1.5 h-1.5 rounded-full bg-indigo-400 shadow-[0_0_5px_#818cf8]"></span> LIVE
               </span>
             </div>
          </div>
        </div>
        
        <nav className="flex-1 p-4 space-y-6 overflow-y-auto custom-scrollbar">
          {['Models', 'Operations', 'System'].map((section) => (
            <div key={section}>
              <h3 className="text-xs font-bold text-gray-500 uppercase tracking-wider mb-3 px-3">{section}</h3>
              <div className="space-y-1">
                {navItems.filter(item => item.section === section).map((item) => (
                  <button 
                    key={item.id}
                    onClick={() => setActiveTab(item.id)}
                    className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-200 group ${
                      activeTab === item.id 
                        ? 'bg-gradient-to-r from-indigo-500/20 to-purple-500/10 text-indigo-300 border border-indigo-500/20 shadow-[0_4px_20px_-5px_rgba(99,102,241,0.15)]' 
                        : 'text-gray-400 hover:bg-[#252525] hover:text-gray-200 border border-transparent'
                    }`}>
                    <item.icon size={18} className={`${activeTab === item.id ? 'text-indigo-400' : 'text-gray-500 group-hover:text-gray-300'} transition-colors`} /> 
                    {item.label}
                  </button>
                ))}
              </div>
            </div>
          ))}
        </nav>
        
        <div className="p-4 border-t border-[#2d2d2d] bg-[#161616]">
          <div className="flex items-center gap-3 px-3 py-2 rounded-lg bg-[#222] border border-[#333]">
             <div className="w-8 h-8 rounded-full bg-gradient-to-br from-gray-700 to-gray-900 flex items-center justify-center border border-gray-600 shadow-inner">
               <span className="text-xs font-bold text-gray-300">AD</span>
             </div>
             <div>
               <p className="text-sm font-medium text-gray-200">Admin User</p>
               <p className="text-[10px] text-gray-500">Security Team</p>
             </div>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto relative bg-[#121212]">
        <div className="absolute top-0 left-0 w-full h-64 bg-gradient-to-b from-indigo-900/10 to-transparent pointer-events-none"></div>
        <div className="p-8 max-w-7xl mx-auto relative z-10">
          {activeTab === 'lstm' && <LSTM_Dashboard />}
          {activeTab === 'cnn' && <CNN_Dashboard />}
          {activeTab === 'xgboost' && <XGBoost_Dashboard />}
          {activeTab === 'inference' && <InferenceBoard />}
          {activeTab === 'datasets' && <DatasetsBoard />}
          {activeTab === 'connections' && <ConnectionBoard />}
        </div>
      </main>
    </div>
  );
}

