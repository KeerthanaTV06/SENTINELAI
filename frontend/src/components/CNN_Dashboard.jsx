import React from 'react';
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
