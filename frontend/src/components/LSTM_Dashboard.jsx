import React from 'react';
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
