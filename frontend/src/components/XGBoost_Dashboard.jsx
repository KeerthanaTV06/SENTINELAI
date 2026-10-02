import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, AreaChart, Area, Legend } from 'recharts';

export default function XGBoost_Dashboard() {
  const shapData = [
    { feature: 'URL Length', shap: 0.35 },
    { feature: 'Special Chars', shap: 0.28 },
    { feature: 'Domain Age', shap: 0.15 },
    { feature: 'HTTPS Status', shap: 0.12 },
    { feature: 'Subdomains', shap: 0.10 },
  ];

  const driftData = [
    { day: 'Mon', dataDrift: 0.08, predDrift: 0.04 },
    { day: 'Tue', dataDrift: 0.07, predDrift: 0.05 },
    { day: 'Wed', dataDrift: 0.09, predDrift: 0.06 },
    { day: 'Thu', dataDrift: 0.15, predDrift: 0.11 }, // Spiked due to new phishing campaign
    { day: 'Fri', dataDrift: 0.04, predDrift: 0.03 }, // Retrained
    { day: 'Sat', dataDrift: 0.03, predDrift: 0.02 },
    { day: 'Sun', dataDrift: 0.04, predDrift: 0.03 }
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
          <div key={i} className="bg-[#2d2d2d] border border-[#3d3d3d] p-4 rounded-lg text-center shadow-lg">
            <p className="text-[#a1a1aa] text-sm mb-1">{m.label}</p>
            <p className="text-3xl font-semibold text-[#f3f3f3]">{m.value}</p>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* SHAP Feature Importance */}
        <div className="bg-[#2d2d2d] border border-[#3d3d3d] p-6 rounded-lg h-80 shadow-lg">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-lg font-medium text-[#a1a1aa]">SHAP Value (Impact on Output)</h3>
            <span className="text-xs bg-indigo-500/20 text-indigo-400 px-2 py-1 rounded border border-indigo-500/30">TreeSHAP</span>
          </div>
          <ResponsiveContainer width="100%" height="90%">
            <BarChart data={shapData} layout="vertical" margin={{ left: 60, right: 20 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#3d3d3d" horizontal={false} />
              <XAxis type="number" stroke="#a1a1aa" />
              <YAxis dataKey="feature" type="category" stroke="#a1a1aa" width={100} />
              <Tooltip contentStyle={{ backgroundColor: '#1e1e1e', borderColor: '#3d3d3d', color: '#fff' }} cursor={{fill: '#3d3d3d'}} />
              <Bar dataKey="shap" fill="#d97757" radius={[0, 4, 4, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Drift Monitoring */}
        <div className="bg-[#2d2d2d] border border-[#3d3d3d] p-6 rounded-lg h-80 shadow-lg">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-lg font-medium text-[#a1a1aa]">Data & Prediction Drift (PSI)</h3>
            <span className="text-xs bg-amber-500/20 text-amber-400 px-2 py-1 rounded border border-amber-500/30">Recent Retrain</span>
          </div>
          <ResponsiveContainer width="100%" height="85%">
            <AreaChart data={driftData}>
              <defs>
                <linearGradient id="colorDataXGB" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#34d399" stopOpacity={0.3}/>
                  <stop offset="95%" stopColor="#34d399" stopOpacity={0}/>
                </linearGradient>
                <linearGradient id="colorPredXGB" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#d97757" stopOpacity={0.3}/>
                  <stop offset="95%" stopColor="#d97757" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#3d3d3d" />
              <XAxis dataKey="day" stroke="#a1a1aa" />
              <YAxis stroke="#a1a1aa" />
              <Tooltip contentStyle={{ backgroundColor: '#1e1e1e', borderColor: '#3d3d3d', color: '#fff' }} />
              <Legend verticalAlign="top" height={36}/>
              <Area type="monotone" dataKey="dataDrift" stroke="#34d399" fillOpacity={1} fill="url(#colorDataXGB)" name="Data Drift" />
              <Area type="monotone" dataKey="predDrift" stroke="#d97757" fillOpacity={1} fill="url(#colorPredXGB)" name="Prediction Drift" />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        {/* Confusion Matrix */}
        <div className="bg-[#2d2d2d] border border-[#3d3d3d] p-6 rounded-lg h-80 flex flex-col lg:col-span-2 shadow-lg">
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
