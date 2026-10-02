import React from 'react';
import Dashboard from './components/Dashboard';

function App() {
  return (
    <div className="min-h-screen bg-[#1e1e1e] text-[#e5e5e5] p-6">
      <header className="mb-8 border-b border-[#3d3d3d] pb-4">
        <h1 className="text-3xl font-bold tracking-tight text-[#f3f3f3]">SENTINEL<span className="text-[#d97757]">-AI</span></h1>
        <p className="text-sm text-[#a1a1aa] mt-1">Autonomous Threat Detection & Mitigation Engine</p>
      </header>
      <Dashboard />
    </div>
  );
}

export default App;
