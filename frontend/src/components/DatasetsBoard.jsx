import React from 'react';
import { Database, FileText, BarChart3, DatabaseZap } from 'lucide-react';

export default function DatasetsBoard() {
  const datasets = [
    {
      id: 1,
      name: 'NSL-KDD Network Logs',
      type: 'Network Traffic',
      size: '2.4 GB',
      samples: '1,245,000',
      status: 'Active',
      lastUpdated: '2 hours ago',
      description: 'Comprehensive network traffic data for training the LSTM Intrusion Detection model.'
    },
    {
      id: 2,
      name: 'Malware PE Binaries v3',
      type: 'Executables',
      size: '14.8 GB',
      samples: '85,400',
      status: 'Active',
      lastUpdated: '1 day ago',
      description: 'Extracted features from PE files used for the 1D-CNN Malware classification model.'
    },
    {
      id: 3,
      name: 'Phishing URL Corpus',
      type: 'Text/Metadata',
      size: '850 MB',
      samples: '3,100,500',
      status: 'Syncing',
      lastUpdated: 'Just now',
      description: 'Curated list of benign and malicious URLs with semantic features for XGBoost.'
    }
  ];

  return (
    <div className="space-y-6 fade-in">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="p-3 bg-blue-500/10 rounded-lg">
            <Database className="text-blue-400" size={24} />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-gray-100">Datasets</h2>
            <p className="text-gray-400 text-sm">Manage and monitor training/testing corpora.</p>
          </div>
        </div>
        <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors flex items-center gap-2">
          <DatabaseZap size={16} />
          Connect Data Source
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-[#2a2a2a] border border-[#3d3d3d] rounded-xl p-6 flex items-center gap-4">
          <div className="p-4 bg-gray-800 rounded-full border border-gray-700">
            <Database className="text-blue-400" size={24} />
          </div>
          <div>
            <p className="text-sm text-gray-400">Total Volume</p>
            <p className="text-2xl font-bold text-gray-100">18.05 GB</p>
          </div>
        </div>
        <div className="bg-[#2a2a2a] border border-[#3d3d3d] rounded-xl p-6 flex items-center gap-4">
          <div className="p-4 bg-gray-800 rounded-full border border-gray-700">
            <FileText className="text-emerald-400" size={24} />
          </div>
          <div>
            <p className="text-sm text-gray-400">Total Samples</p>
            <p className="text-2xl font-bold text-gray-100">4,430,900</p>
          </div>
        </div>
        <div className="bg-[#2a2a2a] border border-[#3d3d3d] rounded-xl p-6 flex items-center gap-4">
          <div className="p-4 bg-gray-800 rounded-full border border-gray-700">
            <BarChart3 className="text-purple-400" size={24} />
          </div>
          <div>
            <p className="text-sm text-gray-400">Active Pipelines</p>
            <p className="text-2xl font-bold text-gray-100">3</p>
          </div>
        </div>
      </div>

      <div className="bg-[#2a2a2a] border border-[#3d3d3d] rounded-xl overflow-hidden shadow-lg">
        <div className="px-6 py-4 border-b border-[#3d3d3d]">
          <h3 className="text-lg font-semibold text-gray-200">Registered Datasets</h3>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-[#1e1e1e] text-gray-400 text-xs uppercase tracking-wider">
                <th className="px-6 py-4 font-medium">Dataset Name</th>
                <th className="px-6 py-4 font-medium">Type</th>
                <th className="px-6 py-4 font-medium">Size</th>
                <th className="px-6 py-4 font-medium">Samples</th>
                <th className="px-6 py-4 font-medium">Status</th>
                <th className="px-6 py-4 font-medium text-right">Last Updated</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#3d3d3d]">
              {datasets.map((ds) => (
                <tr key={ds.id} className="hover:bg-[#333] transition-colors group">
                  <td className="px-6 py-4">
                    <div className="font-medium text-gray-200">{ds.name}</div>
                    <div className="text-xs text-gray-500 mt-1 max-w-xs truncate">{ds.description}</div>
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-300">
                    <span className="bg-gray-800 px-2 py-1 rounded text-xs border border-gray-700">
                      {ds.type}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-300">{ds.size}</td>
                  <td className="px-6 py-4 text-sm text-gray-300 font-mono">{ds.samples}</td>
                  <td className="px-6 py-4 text-sm">
                    <span className={`inline-flex items-center gap-1.5 px-2 py-1 rounded-full text-xs font-medium border ${
                      ds.status === 'Active' 
                        ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20' 
                        : 'bg-amber-500/10 text-amber-400 border-amber-500/20 animate-pulse'
                    }`}>
                      <span className={`w-1.5 h-1.5 rounded-full ${ds.status === 'Active' ? 'bg-emerald-400' : 'bg-amber-400'}`}></span>
                      {ds.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-400 text-right whitespace-nowrap">
                    {ds.lastUpdated}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
