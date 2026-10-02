import React, { useState } from 'react';
import { Cpu, Send, Zap } from 'lucide-react';

const modelInputs = {
  lstm: [
    { name: 'duration', type: 'number', label: 'Connection Duration (s)' },
    { name: 'protocol_type', type: 'text', label: 'Protocol Type (tcp/udp)' },
    { name: 'src_bytes', type: 'number', label: 'Source Bytes' },
    { name: 'dst_bytes', type: 'number', label: 'Destination Bytes' }
  ],
  cnn: [
    { name: 'file_entropy', type: 'number', label: 'File Entropy' },
    { name: 'api_calls', type: 'number', label: 'API Call Frequency' },
    { name: 'pe_imports', type: 'number', label: 'PE Imports Count' }
  ],
  xgboost: [
    { name: 'url_length', type: 'number', label: 'URL Length' },
    { name: 'has_ip', type: 'boolean', label: 'Has IP Address' },
    { name: 'domain_age', type: 'number', label: 'Domain Age (days)' }
  ]
};

export default function InferenceBoard() {
  const [selectedModel, setSelectedModel] = useState('lstm');
  const [inputData, setInputData] = useState({});
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setInputData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handlePredict = () => {
    setLoading(true);
    setTimeout(() => {
      setResult({
        prediction: Math.random() > 0.5 ? 'Malicious' : 'Benign',
        confidence: (Math.random() * 100).toFixed(2)
      });
      setLoading(false);
    }, 1200);
  };

  return (
    <div className="space-y-6 fade-in">
      <div className="flex items-center gap-3">
        <div className="p-3 bg-indigo-500/10 rounded-lg">
          <Cpu className="text-indigo-400" size={24} />
        </div>
        <div>
          <h2 className="text-2xl font-bold text-gray-100">Inference Board</h2>
          <p className="text-gray-400 text-sm">Run live predictions against deployed models.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-[#2a2a2a] rounded-xl border border-[#3d3d3d] p-6 shadow-xl">
          <h3 className="text-lg font-semibold mb-4 text-indigo-400">Model Configuration</h3>
          
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-400 mb-2">Select Model</label>
            <select 
              className="w-full bg-[#1e1e1e] border border-[#3d3d3d] rounded-lg p-3 text-gray-200 focus:outline-none focus:border-indigo-500 transition-colors"
              value={selectedModel}
              onChange={(e) => {
                setSelectedModel(e.target.value);
                setInputData({});
                setResult(null);
              }}
            >
              <option value="lstm">LSTM (Network Intrusion)</option>
              <option value="cnn">1D-CNN (Malware Detection)</option>
              <option value="xgboost">XGBoost (Phishing Detection)</option>
            </select>
          </div>

          <div className="space-y-4">
            <h4 className="text-sm font-medium text-gray-400">Input Parameters</h4>
            {modelInputs[selectedModel].map((input) => (
              <div key={input.name}>
                <label className="block text-xs text-gray-500 mb-1">{input.label}</label>
                {input.type === 'boolean' ? (
                  <div className="flex items-center">
                    <input 
                      type="checkbox"
                      name={input.name}
                      checked={inputData[input.name] || false}
                      onChange={handleInputChange}
                      className="w-5 h-5 rounded border-gray-600 bg-gray-700 text-indigo-500 focus:ring-indigo-500"
                    />
                    <span className="ml-2 text-sm text-gray-300">Yes</span>
                  </div>
                ) : (
                  <input 
                    type={input.type}
                    name={input.name}
                    value={inputData[input.name] || ''}
                    onChange={handleInputChange}
                    placeholder={`Enter ${input.label.toLowerCase()}`}
                    className="w-full bg-[#1e1e1e] border border-[#3d3d3d] rounded-lg p-2.5 text-sm text-gray-200 focus:outline-none focus:border-indigo-500 transition-colors"
                  />
                )}
              </div>
            ))}
          </div>

          <button 
            onClick={handlePredict}
            disabled={loading}
            className="w-full mt-6 bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-3 rounded-lg flex items-center justify-center gap-2 transition-all hover:shadow-lg hover:shadow-indigo-500/20 disabled:opacity-50"
          >
            {loading ? <Zap className="animate-pulse" /> : <Send size={18} />}
            {loading ? 'Processing...' : 'Run Inference'}
          </button>
        </div>

        <div className="bg-[#2a2a2a] rounded-xl border border-[#3d3d3d] p-6 shadow-xl flex flex-col">
          <h3 className="text-lg font-semibold mb-4 text-emerald-400">Output Result</h3>
          
          <div className="flex-1 flex items-center justify-center bg-[#1e1e1e] rounded-lg border border-[#3d3d3d] p-8">
            {!result && !loading && (
              <div className="text-center text-gray-500">
                <Zap size={48} className="mx-auto mb-3 opacity-20" />
                <p>Waiting for input data...</p>
              </div>
            )}
            
            {loading && (
              <div className="text-center text-indigo-400">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-500 mx-auto mb-4"></div>
                <p>Analyzing input parameters...</p>
              </div>
            )}

            {result && !loading && (
              <div className="text-center w-full fade-in">
                <div className={`inline-block p-4 rounded-full mb-4 ${result.prediction === 'Malicious' ? 'bg-red-500/10 text-red-500' : 'bg-emerald-500/10 text-emerald-500'}`}>
                  <Shield size={48} />
                </div>
                <h4 className="text-3xl font-bold text-gray-100 mb-2">{result.prediction}</h4>
                <div className="flex items-center justify-center gap-2">
                  <span className="text-gray-400">Confidence Score:</span>
                  <span className={`font-mono font-bold ${result.confidence > 90 ? 'text-emerald-400' : 'text-amber-400'}`}>
                    {result.confidence}%
                  </span>
                </div>
                
                <div className="mt-8 text-left bg-[#2a2a2a] p-4 rounded-lg border border-[#3d3d3d]">
                  <p className="text-xs text-gray-500 mb-2">RAW JSON OUTPUT</p>
                  <pre className="text-xs text-gray-300 font-mono overflow-x-auto">
{JSON.stringify({
  model: selectedModel,
  timestamp: new Date().toISOString(),
  inputs: inputData,
  prediction: result.prediction,
  confidence: parseFloat(result.confidence)
}, null, 2)}
                  </pre>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
