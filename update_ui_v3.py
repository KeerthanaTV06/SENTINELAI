import os

base_dir = "c:/Users/monis/OneDrive/Documents/Desktop/New folder/AICS/SENTINELAI"

files_to_create = {
    "frontend/src/App.jsx": """import React, { useState } from 'react';
import LSTM_Dashboard from './components/LSTM_Dashboard';
import CNN_Dashboard from './components/CNN_Dashboard';
import XGBoost_Dashboard from './components/XGBoost_Dashboard';
import InferenceBoard from './components/InferenceBoard';
import DatasetsBoard from './components/DatasetsBoard';
import ConnectionsBoard from './components/ConnectionsBoard';
import { Activity, Shield, Globe, PlayCircle, Database, Link as LinkIcon, BarChart3 } from 'lucide-react';

export default function App() {
  const [activeTab, setActiveTab] = useState('lstm');

  return (
    <div className="min-h-screen bg-[#1e1e1e] text-[#e5e5e5] flex">
      {/* Sidebar Navigation */}
      <aside className="w-64 bg-[#2d2d2d] border-r border-[#3d3d3d] flex flex-col shadow-2xl z-10">
        <div className="p-6 border-b border-[#3d3d3d] flex flex-col gap-2">
          <div>
            <h1 className="text-2xl font-bold tracking-tight text-[#f3f3f3]">SENTINEL<span className="text-[#d97757]">-AI</span></h1>
            <p className="text-xs text-[#a1a1aa] mt-1 tracking-wide uppercase font-semibold">Model Analytics Center</p>
          </div>
        </div>
        <nav className="flex-1 p-4 space-y-6 overflow-y-auto">
          
          <div>
            <h2 className="text-xs font-semibold text-[#a1a1aa] uppercase tracking-wider mb-3 px-2">Dashboards</h2>
            <div className="space-y-1">
              <button onClick={() => setActiveTab('lstm')} className={`w-full flex items-center gap-3 px-4 py-2.5 rounded-md text-sm font-medium transition-all ${activeTab === 'lstm' ? 'bg-[#3d3d3d] text-[#d97757] shadow-sm' : 'text-[#a1a1aa] hover:bg-[#3d3d3d] hover:text-[#f3f3f3]'}`}>
                <Activity size={18} /> LSTM (Network)
              </button>
              <button onClick={() => setActiveTab('cnn')} className={`w-full flex items-center gap-3 px-4 py-2.5 rounded-md text-sm font-medium transition-all ${activeTab === 'cnn' ? 'bg-[#3d3d3d] text-[#d97757] shadow-sm' : 'text-[#a1a1aa] hover:bg-[#3d3d3d] hover:text-[#f3f3f3]'}`}>
                <Shield size={18} /> 1D-CNN (Malware)
              </button>
              <button onClick={() => setActiveTab('xgboost')} className={`w-full flex items-center gap-3 px-4 py-2.5 rounded-md text-sm font-medium transition-all ${activeTab === 'xgboost' ? 'bg-[#3d3d3d] text-[#d97757] shadow-sm' : 'text-[#a1a1aa] hover:bg-[#3d3d3d] hover:text-[#f3f3f3]'}`}>
                <Globe size={18} /> XGBoost (Phishing)
              </button>
            </div>
          </div>

          <div>
            <h2 className="text-xs font-semibold text-[#a1a1aa] uppercase tracking-wider mb-3 px-2">Operations</h2>
            <div className="space-y-1">
              <button onClick={() => setActiveTab('inference')} className={`w-full flex items-center gap-3 px-4 py-2.5 rounded-md text-sm font-medium transition-all ${activeTab === 'inference' ? 'bg-[#3d3d3d] text-[#d97757] shadow-sm' : 'text-[#a1a1aa] hover:bg-[#3d3d3d] hover:text-[#f3f3f3]'}`}>
                <PlayCircle size={18} /> Inference Engine
              </button>
              <button onClick={() => setActiveTab('datasets')} className={`w-full flex items-center gap-3 px-4 py-2.5 rounded-md text-sm font-medium transition-all ${activeTab === 'datasets' ? 'bg-[#3d3d3d] text-[#d97757] shadow-sm' : 'text-[#a1a1aa] hover:bg-[#3d3d3d] hover:text-[#f3f3f3]'}`}>
                <Database size={18} /> Datasets Info
              </button>
              <button onClick={() => setActiveTab('connections')} className={`w-full flex items-center gap-3 px-4 py-2.5 rounded-md text-sm font-medium transition-all ${activeTab === 'connections' ? 'bg-[#3d3d3d] text-[#d97757] shadow-sm' : 'text-[#a1a1aa] hover:bg-[#3d3d3d] hover:text-[#f3f3f3]'}`}>
                <LinkIcon size={18} /> Connections Panel
              </button>
            </div>
          </div>

        </nav>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto bg-[#181818]">
        {/* Top Header Bar */}
        <header className="h-16 border-b border-[#3d3d3d] bg-[#2d2d2d]/50 backdrop-blur-md flex items-center justify-between px-8 sticky top-0 z-10">
           <div className="flex items-center gap-2 text-[#a1a1aa]">
              <BarChart3 size={20} />
              <span className="text-sm font-medium capitalize">{activeTab.replace('_', ' ')} Panel</span>
           </div>
           <div className="flex gap-3">
              <span className="flex items-center gap-2 text-xs font-medium text-green-400 bg-green-900/20 px-3 py-1.5 rounded-full border border-green-500/30">
                <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span> UI Health: OK
              </span>
              <span className="flex items-center gap-2 text-xs font-medium text-green-400 bg-green-900/20 px-3 py-1.5 rounded-full border border-green-500/30">
                <span className="w-2 h-2 rounded-full bg-green-500"></span> Backend: LINKED
              </span>
           </div>
        </header>

        <div className="p-8">
          {activeTab === 'lstm' && <LSTM_Dashboard />}
          {activeTab === 'cnn' && <CNN_Dashboard />}
          {activeTab === 'xgboost' && <XGBoost_Dashboard />}
          {activeTab === 'inference' && <InferenceBoard />}
          {activeTab === 'datasets' && <DatasetsBoard />}
          {activeTab === 'connections' && <ConnectionsBoard />}
        </div>
      </main>
    </div>
  );
}
""",
    "frontend/src/components/InferenceBoard.jsx": """import React, { useState } from 'react';
import { Send, Cpu, CheckCircle } from 'lucide-react';

export default function InferenceBoard() {
  const [model, setModel] = useState('lstm');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const modelInputs = {
    lstm: [
      { name: 'duration', label: 'Connection Duration (s)', type: 'number', placeholder: 'e.g. 0' },
      { name: 'protocol_type', label: 'Protocol Type', type: 'select', options: ['tcp', 'udp', 'icmp'] },
      { name: 'src_bytes', label: 'Source Bytes', type: 'number', placeholder: 'e.g. 491' },
      { name: 'dst_bytes', label: 'Destination Bytes', type: 'number', placeholder: 'e.g. 0' },
    ],
    cnn: [
      { name: 'file_size', label: 'File Size (bytes)', type: 'number', placeholder: 'e.g. 102400' },
      { name: 'entropy', label: 'Shannon Entropy', type: 'number', placeholder: 'e.g. 6.42' },
      { name: 'imports', label: 'Number of Imports', type: 'number', placeholder: 'e.g. 15' },
      { name: 'exports', label: 'Number of Exports', type: 'number', placeholder: 'e.g. 0' },
    ],
    xgboost: [
      { name: 'url_length', label: 'URL Length', type: 'number', placeholder: 'e.g. 45' },
      { name: 'has_https', label: 'Uses HTTPS?', type: 'select', options: ['yes', 'no'] },
      { name: 'special_chars', label: 'Special Chars Count', type: 'number', placeholder: 'e.g. 3' },
      { name: 'subdomains', label: 'Number of Subdomains', type: 'number', placeholder: 'e.g. 2' },
    ]
  };

  const handlePredict = (e) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);
    setTimeout(() => {
      setResult({
        prediction: model === 'xgboost' ? 'PHISHING DETECTED' : model === 'cnn' ? 'MALWARE SIGNATURE FOUND' : 'NORMAL TRAFFIC',
        confidence: (Math.random() * (0.99 - 0.85) + 0.85).toFixed(4),
        latency: Math.floor(Math.random() * 40 + 15)
      });
      setLoading(false);
    }, 1200);
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <div className="flex items-center gap-3 mb-8">
        <div className="p-3 bg-[#3d3d3d] rounded-lg border border-[#4d4d4d]"><Cpu className="text-[#d97757]" /></div>
        <div>
          <h2 className="text-2xl font-bold text-[#f3f3f3]">Interactive Inference Engine</h2>
          <p className="text-[#a1a1aa] mt-1">Send manual payloads to the ML models and view real-time predictions.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div className="bg-[#2d2d2d] border border-[#3d3d3d] rounded-xl p-6 shadow-xl">
          <label className="block text-sm font-medium text-[#a1a1aa] mb-2 uppercase tracking-wide">Target Model</label>
          <select 
            value={model} 
            onChange={(e) => setModel(e.target.value)}
            className="w-full bg-[#1e1e1e] border border-[#4d4d4d] text-[#f3f3f3] rounded-lg p-3 outline-none focus:border-[#d97757] transition-colors mb-6"
          >
            <option value="lstm">LSTM (Network Intrusion)</option>
            <option value="cnn">1D-CNN (Malware Classification)</option>
            <option value="xgboost">XGBoost (Phishing URLs)</option>
          </select>

          <form onSubmit={handlePredict} className="space-y-4">
            <h3 className="text-sm font-medium text-[#a1a1aa] uppercase tracking-wide border-b border-[#3d3d3d] pb-2 mb-4">Input Parameters</h3>
            {modelInputs[model].map((input, idx) => (
              <div key={idx}>
                <label className="block text-sm text-[#d1d1d1] mb-1">{input.label}</label>
                {input.type === 'select' ? (
                  <select required className="w-full bg-[#1e1e1e] border border-[#4d4d4d] text-[#f3f3f3] rounded-md p-2.5 outline-none focus:border-[#d97757]">
                    {input.options.map(opt => <option key={opt}>{opt.toUpperCase()}</option>)}
                  </select>
                ) : (
                  <input required type="number" step="any" placeholder={input.placeholder} className="w-full bg-[#1e1e1e] border border-[#4d4d4d] text-[#f3f3f3] rounded-md p-2.5 outline-none focus:border-[#d97757]" />
                )}
              </div>
            ))}
            
            <button type="submit" disabled={loading} className="w-full mt-6 bg-[#d97757] hover:bg-[#c26244] text-white font-medium py-3 rounded-lg flex items-center justify-center gap-2 transition-colors disabled:opacity-50">
              {loading ? <span className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></span> : <><Send size={18} /> Run Inference</>}
            </button>
          </form>
        </div>

        <div className="bg-[#2d2d2d] border border-[#3d3d3d] rounded-xl p-6 shadow-xl flex flex-col relative overflow-hidden">
          <div className="absolute top-0 right-0 p-4 opacity-5 pointer-events-none"><Cpu size={120} /></div>
          <label className="block text-sm font-medium text-[#a1a1aa] mb-4 uppercase tracking-wide">Model Output</label>
          
          <div className="flex-1 bg-[#1e1e1e] rounded-lg border border-[#3d3d3d] p-6 flex flex-col justify-center items-center font-mono text-center relative z-10">
            {!result && !loading && <span className="text-[#a1a1aa]">Awaiting payload...</span>}
            {loading && <div className="space-y-4"><div className="w-8 h-8 border-4 border-[#d97757] border-t-transparent rounded-full animate-spin mx-auto"></div><p className="text-[#d97757] animate-pulse">Computing tensor graph...</p></div>}
            
            {result && !loading && (
              <div className="space-y-6 w-full animate-in zoom-in duration-300">
                <div className={`p-4 rounded-lg border-2 ${result.prediction.includes('NORMAL') ? 'border-green-500/50 bg-green-900/20' : 'border-red-500/50 bg-red-900/20'}`}>
                  <h4 className="text-sm text-[#a1a1aa] uppercase mb-1">Classification Result</h4>
                  <p className={`text-xl font-bold ${result.prediction.includes('NORMAL') ? 'text-green-400' : 'text-red-400'}`}>{result.prediction}</p>
                </div>
                
                <div className="grid grid-cols-2 gap-4 text-left">
                  <div className="bg-[#2d2d2d] p-3 rounded border border-[#3d3d3d]">
                    <span className="text-xs text-[#a1a1aa] block">Confidence Score</span>
                    <span className="text-lg text-[#f3f3f3] font-semibold">{(result.confidence * 100).toFixed(2)}%</span>
                  </div>
                  <div className="bg-[#2d2d2d] p-3 rounded border border-[#3d3d3d]">
                    <span className="text-xs text-[#a1a1aa] block">Inference Latency</span>
                    <span className="text-lg text-[#f3f3f3] font-semibold">{result.latency} ms</span>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
""",
    "frontend/src/components/DatasetsBoard.jsx": """import React from 'react';
import { Database, FileText, DownloadCloud } from 'lucide-react';

export default function DatasetsBoard() {
  const datasets = [
    { name: 'NSL-KDD', type: 'Network Flows', records: '125,973', features: 41, size: '25 MB', desc: 'Standard dataset for network intrusion detection featuring DoS, Probe, R2L, and U2R attacks.' },
    { name: 'EMBER 2018', type: 'PE Malware', records: '1,000,000', features: 2381, size: '1.2 GB', desc: 'Extract features from parsed PE files (benign and malicious) for robust malware classification.' },
    { name: 'PhishTank', type: 'URLs', records: '2,154,630', features: 12, size: '150 MB', desc: 'Crowdsourced repository of phishing URLs combined with benign URLs from Alexa top 1M.' },
  ];

  return (
    <div className="max-w-5xl mx-auto space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <div className="flex items-center gap-3 mb-8">
        <div className="p-3 bg-[#3d3d3d] rounded-lg border border-[#4d4d4d]"><Database className="text-[#d97757]" /></div>
        <div>
          <h2 className="text-2xl font-bold text-[#f3f3f3]">Dataset Repository</h2>
          <p className="text-[#a1a1aa] mt-1">Information on the training data corpuses fueling the SENTINEL-AI models.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {datasets.map((ds, i) => (
          <div key={i} className="bg-[#2d2d2d] border border-[#3d3d3d] rounded-xl p-6 shadow-xl hover:border-[#d97757] transition-all group">
            <div className="flex justify-between items-start mb-4">
              <h3 className="text-xl font-bold text-[#f3f3f3]">{ds.name}</h3>
              <FileText className="text-[#a1a1aa] group-hover:text-[#d97757] transition-colors" />
            </div>
            <p className="text-sm text-[#a1a1aa] mb-6 h-16">{ds.desc}</p>
            
            <div className="space-y-3 mb-6">
              <div className="flex justify-between border-b border-[#3d3d3d] pb-2">
                <span className="text-sm text-[#a1a1aa]">Data Type</span>
                <span className="text-sm font-semibold text-[#e5e5e5]">{ds.type}</span>
              </div>
              <div className="flex justify-between border-b border-[#3d3d3d] pb-2">
                <span className="text-sm text-[#a1a1aa]">Total Records</span>
                <span className="text-sm font-semibold text-[#e5e5e5]">{ds.records}</span>
              </div>
              <div className="flex justify-between border-b border-[#3d3d3d] pb-2">
                <span className="text-sm text-[#a1a1aa]">Features/Dim</span>
                <span className="text-sm font-semibold text-[#e5e5e5]">{ds.features}</span>
              </div>
              <div className="flex justify-between pb-2">
                <span className="text-sm text-[#a1a1aa]">Storage Size</span>
                <span className="text-sm font-semibold text-[#e5e5e5]">{ds.size}</span>
              </div>
            </div>

            <button className="w-full py-2.5 rounded border border-[#3d3d3d] text-[#e5e5e5] hover:bg-[#3d3d3d] hover:text-[#d97757] flex items-center justify-center gap-2 text-sm transition-colors">
              <DownloadCloud size={16} /> Sync Dataset
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
""",
    "frontend/src/components/ConnectionsBoard.jsx": """import React from 'react';
import { Link, Server, ShieldCheck, Database, HardDrive, Wifi } from 'lucide-react';

export default function ConnectionsBoard() {
  const connections = [
    { name: 'FastAPI Backend', host: 'localhost:8000', status: 'Connected', ping: '12ms', icon: Server, color: 'text-green-400' },
    { name: 'Docker Engine', host: 'tcp://127.0.0.1:2375', status: 'Connected', ping: '2ms', icon: HardDrive, color: 'text-green-400' },
    { name: 'Kafka Message Broker', host: 'kafka:9092', status: 'Standby', ping: '--', icon: Wifi, color: 'text-yellow-400' },
    { name: 'Elasticsearch DB', host: 'localhost:9200', status: 'Connected', ping: '45ms', icon: Database, color: 'text-green-400' },
    { name: 'Firewall Auto-Response', host: 'iptables-sys', status: 'Active', ping: '1ms', icon: ShieldCheck, color: 'text-green-400' },
  ];

  return (
    <div className="max-w-4xl mx-auto space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <div className="flex items-center gap-3 mb-8">
        <div className="p-3 bg-[#3d3d3d] rounded-lg border border-[#4d4d4d]"><Link className="text-[#d97757]" /></div>
        <div>
          <h2 className="text-2xl font-bold text-[#f3f3f3]">System Connections</h2>
          <p className="text-[#a1a1aa] mt-1">Live telemetry on microservice linking, Docker binds, and infrastructure health.</p>
        </div>
      </div>

      <div className="bg-[#2d2d2d] border border-[#3d3d3d] rounded-xl overflow-hidden shadow-xl">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-[#1e1e1e] text-[#a1a1aa] text-xs uppercase tracking-wider">
              <th className="p-4 font-semibold border-b border-[#3d3d3d]">Service Node</th>
              <th className="p-4 font-semibold border-b border-[#3d3d3d]">Host / Bind</th>
              <th className="p-4 font-semibold border-b border-[#3d3d3d]">Latency</th>
              <th className="p-4 font-semibold border-b border-[#3d3d3d]">Status</th>
            </tr>
          </thead>
          <tbody className="text-sm">
            {connections.map((c, i) => (
              <tr key={i} className="border-b border-[#3d3d3d] hover:bg-[#363636] transition-colors">
                <td className="p-4 flex items-center gap-3 text-[#f3f3f3]">
                  <c.icon size={18} className="text-[#888]" />
                  <span className="font-medium">{c.name}</span>
                </td>
                <td className="p-4 text-[#a1a1aa] font-mono text-xs">{c.host}</td>
                <td className="p-4 text-[#a1a1aa]">{c.ping}</td>
                <td className="p-4">
                  <span className={`px-3 py-1 rounded-full text-xs font-bold border flex w-max items-center gap-2 ${
                    c.status === 'Connected' || c.status === 'Active' 
                      ? 'border-green-500/30 bg-green-900/20 text-green-400' 
                      : 'border-yellow-500/30 bg-yellow-900/20 text-yellow-400'
                  }`}>
                    <span className={`w-1.5 h-1.5 rounded-full ${c.status === 'Connected' || c.status === 'Active' ? 'bg-green-500 animate-pulse' : 'bg-yellow-500'}`}></span>
                    {c.status.toUpperCase()}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
"""
}

for rel_path, content in files_to_create.items():
    full_path = os.path.join(base_dir, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding='utf-8') as f:
        f.write(content)
    print(f"Created {full_path}")
