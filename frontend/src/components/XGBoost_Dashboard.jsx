import React from 'react';
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
