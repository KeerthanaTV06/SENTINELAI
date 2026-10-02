import React, { useState, useEffect } from 'react';
import { Activity, Server, Database, Globe, Container, Terminal, Wifi, Cloud, CheckCircle2, AlertCircle } from 'lucide-react';

export default function ConnectionBoard() {
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    const initialLogs = [
      '[SYSTEM] Initializing Sentinel-AI Connection Manager...',
      '[DOCKER] Daemon ping successful. Connected to daemon tcp://localhost:2375.',
      '[DOCKER] Discovered 4 running containers in stack sentinel-ai.',
      '[POSTGRES] Connected to postgresql://admin:***@db:5432/sentinel.',
      '[REDIS] Connected to redis://cache:6379/0.',
      '[KAFKA] Connected to broker 1. Topic: model_events initialized.',
      '[FASTAPI] Model Inference API running on port 8000.'
    ];
    setLogs(initialLogs);
    
    const interval = setInterval(() => {
      const messages = [
        '[DOCKER] Heartbeat ACK from container: sentinel-ai-api-1',
        '[KAFKA] Polled 0 new messages from topic model_events',
        '[REDIS] Cache hit ratio: 94.2%',
        '[PROMETHEUS] Metrics scraped successfully',
        '[SYSTEM] All services operating normally'
      ];
      setLogs(prev => [...prev.slice(-10), messages[Math.floor(Math.random() * messages.length)]]);
    }, 3500);

    return () => clearInterval(interval);
  }, []);

  const connections = [
    { name: 'Docker Engine', icon: Container, status: 'Connected', uptime: '14d 2h 4m', ping: '2ms', color: 'text-blue-400' },
    { name: 'PostgreSQL DB', icon: Database, status: 'Connected', uptime: '14d 2h 4m', ping: '4ms', color: 'text-indigo-400' },
    { name: 'Redis Cache', icon: Server, status: 'Connected', uptime: '14d 2h 4m', ping: '1ms', color: 'text-red-400' },
    { name: 'FastAPI Backend', icon: Activity, status: 'Connected', uptime: '2d 6h 11m', ping: '12ms', color: 'text-emerald-400' },
    { name: 'Kafka Broker', icon: Cloud, status: 'Connected', uptime: '14d 2h 4m', ping: '8ms', color: 'text-purple-400' },
    { name: 'External SIEM', icon: Globe, status: 'Warning', uptime: '0d 0h 0m', ping: 'Timeout', color: 'text-amber-400', isWarning: true }
  ];

  return (
    <div className="space-y-6 fade-in">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="p-3 bg-purple-500/10 rounded-lg">
            <Wifi className="text-purple-400" size={24} />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-gray-100">Service Connections</h2>
            <p className="text-gray-400 text-sm">Monitor system infrastructure and connectivity health.</p>
          </div>
        </div>
        
        <div className="flex gap-2">
           <span className="inline-flex items-center gap-1.5 bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 px-3 py-1.5 rounded-lg text-sm font-medium">
             <span className="relative flex h-2 w-2">
               <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
               <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
             </span>
             System Online
           </span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {connections.map((conn, idx) => (
          <div key={idx} className={`bg-[#2a2a2a] border rounded-xl p-5 transition-all hover:bg-[#2d2d2d] ${conn.isWarning ? 'border-amber-500/30 shadow-[0_0_15px_rgba(245,158,11,0.1)]' : 'border-[#3d3d3d]'}`}>
            <div className="flex justify-between items-start mb-4">
              <div className="flex items-center gap-3">
                <div className="p-2.5 bg-[#1e1e1e] rounded-lg border border-[#3d3d3d]">
                  <conn.icon className={conn.color} size={20} />
                </div>
                <div>
                  <h3 className="font-semibold text-gray-200">{conn.name}</h3>
                  <div className="flex items-center gap-1 mt-0.5">
                    {conn.isWarning ? <AlertCircle size={12} className="text-amber-400" /> : <CheckCircle2 size={12} className="text-emerald-400" />}
                    <span className={`text-xs ${conn.isWarning ? 'text-amber-400' : 'text-emerald-400'}`}>{conn.status}</span>
                  </div>
                </div>
              </div>
            </div>
            
            <div className="grid grid-cols-2 gap-4 mt-4 pt-4 border-t border-[#3d3d3d]/50">
              <div>
                <p className="text-xs text-gray-500 mb-1">Uptime</p>
                <p className="text-sm font-medium text-gray-300 font-mono">{conn.uptime}</p>
              </div>
              <div>
                <p className="text-xs text-gray-500 mb-1">Latency</p>
                <p className="text-sm font-medium text-gray-300 font-mono">{conn.ping}</p>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="bg-[#1e1e1e] border border-[#3d3d3d] rounded-xl overflow-hidden shadow-inner">
        <div className="px-4 py-3 border-b border-[#3d3d3d] flex items-center gap-2 bg-[#2a2a2a]">
          <Terminal size={16} className="text-gray-400" />
          <h3 className="text-sm font-medium text-gray-200">System Activity Log</h3>
        </div>
        <div className="p-4 h-64 overflow-y-auto font-mono text-xs text-gray-400 flex flex-col gap-1.5 custom-scrollbar">
          {logs.map((log, i) => (
            <div key={i} className="flex gap-3 hover:bg-[#2d2d2d] px-2 py-1 rounded">
              <span className="text-gray-600 shrink-0">[{new Date().toLocaleTimeString()}]</span>
              <span className={`${
                log.includes('ACK') ? 'text-emerald-400/80' : 
                log.includes('WARNING') ? 'text-amber-400/80' : 
                log.includes('ERROR') ? 'text-red-400/80' : 
                'text-gray-400'
              }`}>{log}</span>
            </div>
          ))}
          <div className="mt-2 text-indigo-400 animate-pulse">_</div>
        </div>
      </div>
    </div>
  );
}
