import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, AreaChart, Area, Legend } from 'recharts';

export default function CNN_Dashboard() {
  const trainingData = [
    { epoch: 1, loss: 0.65, val_loss: 0.60, acc: 0.70 },
    { epoch: 5, loss: 0.40, val_loss: 0.45, acc: 0.85 },
    { epoch: 10, loss: 0.25, val_loss: 0.30, acc: 0.92 },
    { epoch: 15, loss: 0.15, val_loss: 0.22, acc: 0.96 },
    { epoch: 20, loss: 0.10, val_loss: 0.18, acc: 0.98 },
  ];

  const shapData = [
    { feature: 'file_entropy', shap: 0.78 },
    { feature: 'api_calls', shap: 0.72 },
    { feature: 'pe_imports', shap: 0.61 },
    { feature: 'file_size', shap: 0.25 },
    { feature: 'dll_exports', shap: 0.18 }
  ];

  const driftData = [
    { day: 'Mon', dataDrift: 0.02, predDrift: 0.01 },
    { day: 'Tue', dataDrift: 0.03, predDrift: 0.02 },
    { day: 'Wed', dataDrift: 0.04, predDrift: 0.03 },
    { day: 'Thu', dataDrift: 0.04, predDrift: 0.03 },
    { day: 'Fri', dataDrift: 0.05, predDrift: 0.04 },
    { day: 'Sat', dataDrift: 0.06, predDrift: 0.05 },
    { day: 'Sun', dataDrift: 0.05, predDrift: 0.04 }
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
          <div key={i} className="bg-[#2d2d2d] border border-[#3d3d3d] p-4 rounded-lg text-center shadow-lg">
            <p className="text-[#a1a1aa] text-sm mb-1">{m.label}</p>
            <p className="text-3xl font-semibold text-[#f3f3f3]">{m.value}</p>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Loss Curve */}
        <div className="bg-[#2d2d2d] border border-[#3d3d3d] p-6 rounded-lg h-80 shadow-lg">
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
            <span className="text-xs bg-emerald-500/20 text-emerald-400 px-2 py-1 rounded border border-emerald-500/30">Stable</span>
          </div>
          <ResponsiveContainer width="100%" height="85%">
            <AreaChart data={driftData}>
              <defs>
                <linearGradient id="colorDataCNN" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#34d399" stopOpacity={0.3}/>
                  <stop offset="95%" stopColor="#34d399" stopOpacity={0}/>
                </linearGradient>
                <linearGradient id="colorPredCNN" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3}/>
                  <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#3d3d3d" />
              <XAxis dataKey="day" stroke="#a1a1aa" />
              <YAxis stroke="#a1a1aa" />
              <Tooltip contentStyle={{ backgroundColor: '#1e1e1e', borderColor: '#3d3d3d', color: '#fff' }} />
              <Legend verticalAlign="top" height={36}/>
              <Area type="monotone" dataKey="dataDrift" stroke="#34d399" fillOpacity={1} fill="url(#colorDataCNN)" name="Data Drift" />
              <Area type="monotone" dataKey="predDrift" stroke="#3b82f6" fillOpacity={1} fill="url(#colorPredCNN)" name="Prediction Drift" />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        {/* Confusion Matrix */}
        <div className="bg-[#2d2d2d] border border-[#3d3d3d] p-6 rounded-lg h-80 flex flex-col shadow-lg">
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
