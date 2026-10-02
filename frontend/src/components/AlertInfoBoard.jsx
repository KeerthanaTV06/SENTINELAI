import React, { useState } from 'react';
import { Bell, Mail, CheckCircle2, AlertTriangle, Send } from 'lucide-react';

export default function AlertInfoBoard() {
  const [emailInput, setEmailInput] = useState('');
  const [savedEmails, setSavedEmails] = useState([
    { email: 'admin@sentinel-ai.sec', status: 'Active' }
  ]);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!emailInput) return;
    
    setIsSubmitting(true);
    // Simulate API call
    setTimeout(() => {
      setSavedEmails(prev => [...prev, { email: emailInput, status: 'Active' }]);
      setEmailInput('');
      setIsSubmitting(false);
    }, 800);
  };

  return (
    <div className="space-y-6 fade-in">
      <div className="flex items-center gap-3">
        <div className="p-3 bg-rose-500/10 rounded-lg">
          <Bell className="text-rose-400" size={24} />
        </div>
        <div>
          <h2 className="text-2xl font-bold text-gray-100">Alert Information</h2>
          <p className="text-gray-400 text-sm">Configure email notifications for model drift and system degradation.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Configuration Panel */}
        <div className="bg-[#2a2a2a] rounded-xl border border-[#3d3d3d] p-6 shadow-xl">
          <h3 className="text-lg font-semibold mb-4 text-rose-400 flex items-center gap-2">
            <AlertTriangle size={20} />
            Add Alert Recipient
          </h3>
          
          <p className="text-sm text-gray-400 mb-6">
            Register an email address to receive immediate notifications when Population Stability Index (PSI) thresholds are breached or when the FastAPI inference backend experiences downtime.
          </p>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-400 mb-2">Email Address</label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Mail size={18} className="text-gray-500" />
                </div>
                <input 
                  type="email"
                  value={emailInput}
                  onChange={(e) => setEmailInput(e.target.value)}
                  placeholder="security-team@company.com"
                  className="w-full bg-[#1e1e1e] border border-[#3d3d3d] rounded-lg pl-10 pr-4 py-3 text-sm text-gray-200 focus:outline-none focus:border-rose-500 transition-colors placeholder-gray-600"
                  required
                />
              </div>
            </div>

            <button 
              type="submit"
              disabled={isSubmitting || !emailInput}
              className="w-full bg-rose-600 hover:bg-rose-700 text-white font-medium py-3 rounded-lg flex items-center justify-center gap-2 transition-all hover:shadow-lg hover:shadow-rose-500/20 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isSubmitting ? (
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
              ) : (
                <>
                  <Send size={18} /> Enable Alerts
                </>
              )}
            </button>
          </form>
        </div>

        {/* Active Subscriptions */}
        <div className="bg-[#2a2a2a] rounded-xl border border-[#3d3d3d] p-6 shadow-xl">
          <h3 className="text-lg font-semibold mb-4 text-gray-200">Active Subscriptions</h3>
          
          {savedEmails.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-48 border border-dashed border-[#3d3d3d] rounded-lg bg-[#1e1e1e]">
              <Mail size={32} className="text-gray-600 mb-2" />
              <p className="text-sm text-gray-500">No email alerts configured.</p>
            </div>
          ) : (
            <div className="space-y-3">
              {savedEmails.map((item, idx) => (
                <div key={idx} className="flex items-center justify-between p-4 bg-[#1e1e1e] border border-[#3d3d3d] rounded-lg animate-in slide-in-from-bottom-2 fade-in duration-300">
                  <div className="flex items-center gap-3">
                    <div className="p-2 bg-emerald-500/10 rounded-full">
                      <CheckCircle2 size={20} className="text-emerald-400" />
                    </div>
                    <div>
                      <p className="font-medium text-gray-200">{item.email}</p>
                      <p className="text-xs text-emerald-500 font-semibold mt-0.5 uppercase tracking-wider">
                        Notified
                      </p>
                    </div>
                  </div>
                  <span className="text-xs text-gray-500">Subscribed</span>
                </div>
              ))}
            </div>
          )}
          
          <div className="mt-6 p-4 bg-blue-500/10 border border-blue-500/20 rounded-lg">
            <h4 className="text-sm font-medium text-blue-400 mb-1">How it works</h4>
            <p className="text-xs text-gray-400">
              When drift > 0.1 is detected in the data streams (Kafka), the MLOps pipeline will automatically trigger an email to all addresses listed above before initiating the automated retraining sequence.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
