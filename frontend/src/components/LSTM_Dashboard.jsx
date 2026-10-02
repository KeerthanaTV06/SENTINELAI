import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, AreaChart, Area, Legend } from 'recharts';

export default function LSTM_Dashboard() {
  const rocData = [
    { fpr: 0, tpr: 0 }, { fpr: 0.1, tpr: 0.82 }, { fpr: 0.2, tpr: 0.91 },
    { fpr: 0.3, tpr: 0.94 }, { fpr: 0.5, tpr: 0.97 }, { fpr: 1, tpr: 1 }
  ];

  const shapData = [
    { feature: 'duration', shap: 0.85 },
    { feature: 'src_bytes', shap: 0.65 },
    { feature: 'dst_bytes', shap: 0.55 },
    { feature: 'flag', shap: 0.40 },
    { feature: 'protocol_type', shap: 0.35 }
  ];

  const driftData = [
    { day: 'Mon', dataDrift: 0.05, predDrift: 0.02 },
    { day: 'Tue', dataDrift: 0.06, predDrift: 0.03 },
    { day: 'Wed', dataDrift: 0.04, predDrift: 0.02 },
    { day: 'Thu', dataDrift: 0.08, predDrift: 0.05 },
    { day: 'Fri', dataDrift: 0.12, predDrift: 0.09 },
    { day: 'Sat', dataDrift: 0.18, predDrift: 0.14 }, 
    { day: 'Sun', dataDrift: 0.03, predDrift: 0.02 }  
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
          <div key={i} className="bg-[#2d2d2d] border border-[#3d3d3d] p-4 rounded-lg text-center shadow-lg">
            <p className="text-[#a1a1aa] text-sm mb-1">{m.label}</p>
            <p className="text-3xl font-semibold text-[#f3f3f3]">{m.value}</p>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* ROC Curve */}
        <div className="bg-[#2d2d2d] border border-[#3d3d3d] p-6 rounded-lg h-80 shadow-lg">
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

        {/* SHAP Values */}
        <div className="bg-[#2d2d2d] border border-[#3d3d3d] p-6 rounded-lg h-80 shadow-lg">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-lg font-medium text-[#a1a1aa]">Global Feature Explanations (SHAP)</h3>
            <span className="text-xs bg-indigo-500/20 text-indigo-400 px-2 py-1 rounded border border-indigo-500/30">XAI Active</span>
          </div>
          <ResponsiveContainer width="100%" height="90%">
            <BarChart data={shapData} layout="vertical" margin={{ left: 40, right: 20 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#3d3d3d" horizontal={false} />
              <XAxis type="number" stroke="#a1a1aa" />
              <YAxis dataKey="feature" type="category" stroke="#a1a1aa" width={80} />
              <Tooltip contentStyle={{ backgroundColor: '#1e1e1e', borderColor: '#3d3d3d', color: '#fff' }} cursor={{fill: '#3d3d3d'}} />
              <Bar dataKey="shap" fill="#818cf8" radius={[0, 4, 4, 0]} name="Mean |SHAP|" />
            </BarChart>
          </ResponsiveContainer>
        </div>
        
        {/* Drift Monitoring */}
        <div className="bg-[#2d2d2d] border border-[#3d3d3d] p-6 rounded-lg h-80 shadow-lg">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-lg font-medium text-[#a1a1aa]">Drift Monitoring (PSI)</h3>
            <span className="text-xs bg-emerald-500/20 text-emerald-400 px-2 py-1 rounded border border-emerald-500/30">Monitored</span>
          </div>
          <ResponsiveContainer width="100%" height="85%">
            <AreaChart data={driftData}>
              <defs>
                <linearGradient id="colorData" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#34d399" stopOpacity={0.3}/>
                  <stop offset="95%" stopColor="#34d399" stopOpacity={0}/>
                </linearGradient>
                <linearGradient id="colorPred" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#f59e0b" stopOpacity={0.3}/>
                  <stop offset="95%" stopColor="#f59e0b" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#3d3d3d" />
              <XAxis dataKey="day" stroke="#a1a1aa" />
              <YAxis stroke="#a1a1aa" />
              <Tooltip contentStyle={{ backgroundColor: '#1e1e1e', borderColor: '#3d3d3d', color: '#fff' }} />
              <Legend verticalAlign="top" height={36}/>
              <Area type="monotone" dataKey="dataDrift" stroke="#34d399" fillOpacity={1} fill="url(#colorData)" name="Data Drift" />
              <Area type="monotone" dataKey="predDrift" stroke="#f59e0b" fillOpacity={1} fill="url(#colorPred)" name="Prediction Drift" />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        {/* Confusion Matrix */}
        <div className="bg-[#2d2d2d] border border-[#3d3d3d] p-6 rounded-lg h-80 flex flex-col shadow-lg">
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
