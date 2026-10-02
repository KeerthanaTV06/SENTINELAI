import os

base_dir = "c:/Users/monis/OneDrive/Documents/Desktop/New folder/AICS/SENTINELAI"

files_to_create = {
    "frontend/src/App.jsx": """import React, { useState } from 'react';
import LSTM_Dashboard from './components/LSTM_Dashboard';
import CNN_Dashboard from './components/CNN_Dashboard';
import XGBoost_Dashboard from './components/XGBoost_Dashboard';
import { Activity, Shield, Globe } from 'lucide-react';

export default function App() {
  const [activeTab, setActiveTab] = useState('lstm');

  return (
    <div className="min-h-screen bg-[#1e1e1e] text-[#e5e5e5] flex">
      {/* Sidebar Navigation */}
      <aside className="w-64 bg-[#2d2d2d] border-r border-[#3d3d3d] flex flex-col">
        <div className="p-6 border-b border-[#3d3d3d]">
          <h1 className="text-2xl font-bold tracking-tight text-[#f3f3f3]">SENTINEL<span className="text-[#d97757]">-AI</span></h1>
          <p className="text-xs text-[#a1a1aa] mt-1">Model Analytics Center</p>
        </div>
        <nav className="flex-1 p-4 space-y-2">
          <button 
            onClick={() => setActiveTab('lstm')}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-md text-sm font-medium transition-colors ${activeTab === 'lstm' ? 'bg-[#3d3d3d] text-[#d97757]' : 'text-[#a1a1aa] hover:bg-[#3d3d3d] hover:text-[#f3f3f3]'}`}>
            <Activity size={18} /> LSTM (Network)
          </button>
          <button 
            onClick={() => setActiveTab('cnn')}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-md text-sm font-medium transition-colors ${activeTab === 'cnn' ? 'bg-[#3d3d3d] text-[#d97757]' : 'text-[#a1a1aa] hover:bg-[#3d3d3d] hover:text-[#f3f3f3]'}`}>
            <Shield size={18} /> 1D-CNN (Malware)
          </button>
          <button 
            onClick={() => setActiveTab('xgboost')}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-md text-sm font-medium transition-colors ${activeTab === 'xgboost' ? 'bg-[#3d3d3d] text-[#d97757]' : 'text-[#a1a1aa] hover:bg-[#3d3d3d] hover:text-[#f3f3f3]'}`}>
            <Globe size={18} /> XGBoost (Phishing)
          </button>
        </nav>
      </aside>

      {/* Main Content */}
      <main className="flex-1 p-8 overflow-y-auto">
        {activeTab === 'lstm' && <LSTM_Dashboard />}
        {activeTab === 'cnn' && <CNN_Dashboard />}
        {activeTab === 'xgboost' && <XGBoost_Dashboard />}
      </main>
    </div>
  );
}
""",
    "frontend/src/components/LSTM_Dashboard.jsx": """import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export default function LSTM_Dashboard() {
  const rocData = [
    { fpr: 0, tpr: 0 }, { fpr: 0.1, tpr: 0.82 }, { fpr: 0.2, tpr: 0.91 },
    { fpr: 0.3, tpr: 0.94 }, { fpr: 0.5, tpr: 0.97 }, { fpr: 1, tpr: 1 }
  ];

  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      <h2 className="text-2xl font-bold text-[#f3f3f3]">LSTM Network Intrusion Detection</h2>
      
      {/* Metrics Row */}
      <div className="grid grid-cols-4 gap-4">
        {[
          { label: 'Accuracy', value: '94.2%' },
          { label: 'Precision', value: '92.8%' },
          { label: 'Recall', value: '95.1%' },
          { label: 'F1 Score', value: '93.9%' }
        ].map((m, i) => (
          <div key={i} className="bg-[#2d2d2d] border border-[#3d3d3d] p-4 rounded-lg text-center">
            <p className="text-[#a1a1aa] text-sm mb-1">{m.label}</p>
            <p className="text-3xl font-semibold text-[#f3f3f3]">{m.value}</p>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-2 gap-6">
        {/* ROC Curve */}
        <div className="bg-[#2d2d2d] border border-[#3d3d3d] p-6 rounded-lg h-80">
          <h3 className="text-lg font-medium mb-4 text-[#a1a1aa]">ROC Curve (AUC: 0.96)</h3>
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={rocData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#3d3d3d" />
              <XAxis dataKey="fpr" type="number" domain={[0, 1]} stroke="#a1a1aa" label={{ value: 'False Positive Rate', position: 'bottom', fill: '#a1a1aa' }} />
              <YAxis domain={[0, 1]} stroke="#a1a1aa" label={{ value: 'True Positive Rate', angle: -90, position: 'left', fill: '#a1a1aa' }} />
              <Tooltip contentStyle={{ backgroundColor: '#1e1e1e', borderColor: '#3d3d3d', color: '#fff' }} />
              <Line type="monotone" dataKey="tpr" stroke="#d97757" strokeWidth={3} dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Confusion Matrix */}
        <div className="bg-[#2d2d2d] border border-[#3d3d3d] p-6 rounded-lg h-80 flex flex-col">
          <h3 className="text-lg font-medium mb-4 text-[#a1a1aa]">Confusion Matrix</h3>
          <div className="flex-1 grid grid-cols-2 grid-rows-2 gap-2 text-center text-sm">
            <div className="bg-[#1e1e1e] border-l-4 border-green-500 p-4 rounded flex flex-col justify-center">
              <span className="text-[#a1a1aa]">True Negatives</span>
              <span className="text-2xl font-bold text-[#f3f3f3]">45,210</span>
            </div>
            <div className="bg-[#1e1e1e] border-l-4 border-red-500 p-4 rounded flex flex-col justify-center">
              <span className="text-[#a1a1aa]">False Positives</span>
              <span className="text-2xl font-bold text-[#d97757]">1,420</span>
            </div>
            <div className="bg-[#1e1e1e] border-l-4 border-red-500 p-4 rounded flex flex-col justify-center">
              <span className="text-[#a1a1aa]">False Negatives</span>
              <span className="text-2xl font-bold text-[#d97757]">890</span>
            </div>
            <div className="bg-[#1e1e1e] border-l-4 border-green-500 p-4 rounded flex flex-col justify-center">
              <span className="text-[#a1a1aa]">True Positives</span>
              <span className="text-2xl font-bold text-[#f3f3f3]">22,305</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
""",
    "frontend/src/components/CNN_Dashboard.jsx": """import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export default function CNN_Dashboard() {
  const trainingData = [
    { epoch: 1, loss: 0.65, val_loss: 0.60, acc: 0.70 },
    { epoch: 5, loss: 0.40, val_loss: 0.45, acc: 0.85 },
    { epoch: 10, loss: 0.25, val_loss: 0.30, acc: 0.92 },
    { epoch: 15, loss: 0.15, val_loss: 0.22, acc: 0.96 },
    { epoch: 20, loss: 0.10, val_loss: 0.18, acc: 0.98 },
  ];

  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      <h2 className="text-2xl font-bold text-[#f3f3f3]">1D-CNN Malware Classification</h2>
      
      <div className="grid grid-cols-4 gap-4">
        {[
          { label: 'Test Accuracy', value: '97.5%' },
          { label: 'Precision', value: '98.1%' },
          { label: 'Recall', value: '96.8%' },
          { label: 'F1 Score', value: '97.4%' }
        ].map((m, i) => (
          <div key={i} className="bg-[#2d2d2d] border border-[#3d3d3d] p-4 rounded-lg text-center">
            <p className="text-[#a1a1aa] text-sm mb-1">{m.label}</p>
            <p className="text-3xl font-semibold text-[#f3f3f3]">{m.value}</p>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-2 gap-6">
        {/* Loss Curve */}
        <div className="bg-[#2d2d2d] border border-[#3d3d3d] p-6 rounded-lg h-80">
          <h3 className="text-lg font-medium mb-4 text-[#a1a1aa]">Training vs Validation Loss</h3>
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={trainingData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#3d3d3d" />
              <XAxis dataKey="epoch" stroke="#a1a1aa" label={{ value: 'Epochs', position: 'bottom', fill: '#a1a1aa' }} />
              <YAxis stroke="#a1a1aa" />
              <Tooltip contentStyle={{ backgroundColor: '#1e1e1e', borderColor: '#3d3d3d', color: '#fff' }} />
              <Line type="monotone" dataKey="loss" stroke="#3b82f6" strokeWidth={2} name="Train Loss" />
              <Line type="monotone" dataKey="val_loss" stroke="#d97757" strokeWidth={2} name="Val Loss" />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Confusion Matrix */}
        <div className="bg-[#2d2d2d] border border-[#3d3d3d] p-6 rounded-lg h-80 flex flex-col">
          <h3 className="text-lg font-medium mb-4 text-[#a1a1aa]">Confusion Matrix (EMBER Dataset)</h3>
          <div className="flex-1 grid grid-cols-2 grid-rows-2 gap-2 text-center text-sm">
            <div className="bg-[#1e1e1e] border-l-4 border-green-500 p-4 rounded flex flex-col justify-center">
              <span className="text-[#a1a1aa]">True Negatives (Benign)</span>
              <span className="text-2xl font-bold text-[#f3f3f3]">14,200</span>
            </div>
            <div className="bg-[#1e1e1e] border-l-4 border-red-500 p-4 rounded flex flex-col justify-center">
              <span className="text-[#a1a1aa]">False Positives</span>
              <span className="text-2xl font-bold text-[#d97757]">280</span>
            </div>
            <div className="bg-[#1e1e1e] border-l-4 border-red-500 p-4 rounded flex flex-col justify-center">
              <span className="text-[#a1a1aa]">False Negatives</span>
              <span className="text-2xl font-bold text-[#d97757]">450</span>
            </div>
            <div className="bg-[#1e1e1e] border-l-4 border-green-500 p-4 rounded flex flex-col justify-center">
              <span className="text-[#a1a1aa]">True Positives (Malware)</span>
              <span className="text-2xl font-bold text-[#f3f3f3]">13,900</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
""",
    "frontend/src/components/XGBoost_Dashboard.jsx": """import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts';

export default function XGBoost_Dashboard() {
  const featureImp = [
    { name: 'URL Length', value: 0.32 },
    { name: 'Special Chars', value: 0.28 },
    { name: 'Domain Age', value: 0.15 },
    { name: 'HTTPS Status', value: 0.12 },
    { name: 'Subdomains', value: 0.08 },
  ];

  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      <h2 className="text-2xl font-bold text-[#f3f3f3]">XGBoost Phishing Detection</h2>
      
      <div className="grid grid-cols-4 gap-4">
        {[
          { label: 'Accuracy', value: '95.8%' },
          { label: 'Precision', value: '96.2%' },
          { label: 'Recall', value: '94.5%' },
          { label: 'F1 Score', value: '95.3%' }
        ].map((m, i) => (
          <div key={i} className="bg-[#2d2d2d] border border-[#3d3d3d] p-4 rounded-lg text-center">
            <p className="text-[#a1a1aa] text-sm mb-1">{m.label}</p>
            <p className="text-3xl font-semibold text-[#f3f3f3]">{m.value}</p>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-2 gap-6">
        {/* Feature Importance */}
        <div className="bg-[#2d2d2d] border border-[#3d3d3d] p-6 rounded-lg h-80">
          <h3 className="text-lg font-medium mb-4 text-[#a1a1aa]">Top Feature Importance</h3>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={featureImp} layout="vertical" margin={{ left: 40 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#3d3d3d" horizontal={false} />
              <XAxis type="number" stroke="#a1a1aa" />
              <YAxis dataKey="name" type="category" stroke="#a1a1aa" />
              <Tooltip contentStyle={{ backgroundColor: '#1e1e1e', borderColor: '#3d3d3d', color: '#fff' }} cursor={{fill: '#3d3d3d'}} />
              <Bar dataKey="value" fill="#d97757" radius={[0, 4, 4, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Confusion Matrix */}
        <div className="bg-[#2d2d2d] border border-[#3d3d3d] p-6 rounded-lg h-80 flex flex-col">
          <h3 className="text-lg font-medium mb-4 text-[#a1a1aa]">Confusion Matrix (PhishTank)</h3>
          <div className="flex-1 grid grid-cols-2 grid-rows-2 gap-2 text-center text-sm">
            <div className="bg-[#1e1e1e] border-l-4 border-green-500 p-4 rounded flex flex-col justify-center">
              <span className="text-[#a1a1aa]">True Negatives</span>
              <span className="text-2xl font-bold text-[#f3f3f3]">8,900</span>
            </div>
            <div className="bg-[#1e1e1e] border-l-4 border-red-500 p-4 rounded flex flex-col justify-center">
              <span className="text-[#a1a1aa]">False Positives</span>
              <span className="text-2xl font-bold text-[#d97757]">350</span>
            </div>
            <div className="bg-[#1e1e1e] border-l-4 border-red-500 p-4 rounded flex flex-col justify-center">
              <span className="text-[#a1a1aa]">False Negatives</span>
              <span className="text-2xl font-bold text-[#d97757]">510</span>
            </div>
            <div className="bg-[#1e1e1e] border-l-4 border-green-500 p-4 rounded flex flex-col justify-center">
              <span className="text-[#a1a1aa]">True Positives</span>
              <span className="text-2xl font-bold text-[#f3f3f3]">9,100</span>
            </div>
          </div>
        </div>
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
