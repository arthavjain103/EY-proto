import React, { useState } from 'react';
import { LOAN_TYPES, getStatusFromProgress } from '../config/applicationTemplates';

const ApplicationPage = ({ setCurrentPage, setSubmittedApplications, submittedApplications }) => {
  const [formData, setFormData] = useState({
    fullName: '',
    email: '',
    phone: '',
    loanType: 'personal',
    amount: '',
    purpose: '',
    employmentStatus: 'employed',
    annualIncome: '',
    creditScore: '750',
    agreeTerms: false
  });

  const [submitted, setSubmitted] = useState(false);
  const [appId, setAppId] = useState('');

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Generate application ID
    const newAppId = `APP-${String(Date.now()).slice(-6)}`;
    setAppId(newAppId);
    
    // Get current date in YYYY-MM-DD format
    const today = new Date();
    const dateStr = today.toISOString().split('T')[0]; // 2025-12-16 format
    
    // Create new application object with proper status based on progress
    const progress = 25;
    const status = getStatusFromProgress(progress);
    
    const newApp = {
      id: newAppId,
      name: formData.fullName,
      amount: '₹' + parseInt(formData.amount).toLocaleString('en-IN'),
      status: status,
      date: dateStr,
      progress: progress,
      type: formData.loanType.charAt(0).toUpperCase() + formData.loanType.slice(1) + ' Loan',
      email: formData.email
    };
    
    // Add to submitted applications
    if (setSubmittedApplications) {
      setSubmittedApplications([newApp, ...(submittedApplications || [])]);
    }
    
    setSubmitted(true);
    setTimeout(() => {
      setCurrentPage('dashboard');
    }, 3000);
  };

  if (submitted) {
    return (
      <div className="max-w-2xl mx-auto bg-white rounded-lg shadow-sm border border-slate-200 p-12 text-center">
        <div className="mb-4 text-6xl">✓</div>
        <h2 className="text-3xl font-bold text-slate-900 mb-2">Application Submitted!</h2>
        <p className="text-slate-600 mb-6">Your loan application has been submitted successfully. You'll receive updates via email shortly.</p>
        <div className="space-y-2 text-sm text-slate-600 mb-8 bg-slate-50 p-4 rounded-lg border border-slate-200">
          <p><strong>Application ID:</strong> {appId}</p>
          <p><strong>Applicant:</strong> {formData.fullName}</p>
          <p><strong>Loan Amount:</strong> ₹{parseInt(formData.amount).toLocaleString('en-IN')}</p>
          <p><strong>Loan Type:</strong> {formData.loanType.charAt(0).toUpperCase() + formData.loanType.slice(1)} Loan</p>
          <p><strong>Status:</strong> <span className="px-2 py-1 bg-orange-50 text-orange-700 rounded text-xs font-medium">Pending</span></p>
        </div>
        <p className="text-xs text-slate-500 mb-6">Redirecting to Dashboard in 3 seconds...</p>
        <button
          onClick={() => setCurrentPage('dashboard')}
          className="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors font-medium"
        >
          Go to Dashboard
        </button>
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto bg-white rounded-lg shadow-sm border border-slate-200 p-8">
      <h2 className="text-2xl font-bold text-slate-900 mb-8">New Loan Application</h2>

      <form onSubmit={handleSubmit} className="space-y-8">
        {/* Personal Information */}
        <div>
          <h3 className="text-lg font-semibold text-slate-900 mb-4 pb-4 border-b border-slate-200">Personal Information</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">Full Name *</label>
              <input
                type="text"
                name="fullName"
                value={formData.fullName}
                onChange={handleChange}
                required
                className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-600"
                placeholder="John Doe"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">Email *</label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                required
                className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-600"
                placeholder="john@example.com"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">Phone Number *</label>
              <input
                type="tel"
                name="phone"
                value={formData.phone}
                onChange={handleChange}
                required
                className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-600"
                placeholder="+91 98765 43210"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">Employment Status</label>
              <select
                name="employmentStatus"
                value={formData.employmentStatus}
                onChange={handleChange}
                className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-600"
              >
                <option value="employed">Employed</option>
                <option value="self-employed">Self-Employed</option>
                <option value="unemployed">Unemployed</option>
              </select>
            </div>
          </div>
        </div>

        {/* Financial Information */}
        <div>
          <h3 className="text-lg font-semibold text-slate-900 mb-4 pb-4 border-b border-slate-200">Financial Information</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">Annual Income *</label>
              <input
                type="number"
                name="annualIncome"
                value={formData.annualIncome}
                onChange={handleChange}
                required
                className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-600"
                placeholder="500000"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">Credit Score</label>
              <input
                type="number"
                name="creditScore"
                value={formData.creditScore}
                onChange={handleChange}
                className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-600"
                placeholder="750"
              />
            </div>
          </div>
        </div>

        {/* Loan Details */}
        <div>
          <h3 className="text-lg font-semibold text-slate-900 mb-4 pb-4 border-b border-slate-200">Loan Details</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">Loan Type *</label>
              <select
                name="loanType"
                value={formData.loanType}
                onChange={handleChange}
                className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-600"
              >
                {LOAN_TYPES.map((type, idx) => (
                  <option key={idx} value={type.toLowerCase().replace(' loan', '')}>
                    {type}
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">Loan Amount (₹) *</label>
              <input
                type="number"
                name="amount"
                value={formData.amount}
                onChange={handleChange}
                required
                className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-600"
                placeholder="500000"
              />
            </div>
            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-slate-700 mb-2">Purpose of Loan</label>
              <textarea
                name="purpose"
                value={formData.purpose}
                onChange={handleChange}
                className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-600"
                placeholder="Please describe the purpose of this loan..."
                rows="3"
              />
            </div>
          </div>
        </div>

        {/* Terms */}
        <div className="bg-slate-50 rounded-lg p-6 border border-slate-200">
          <label className="flex items-start space-x-3">
            <input
              type="checkbox"
              name="agreeTerms"
              checked={formData.agreeTerms}
              onChange={handleChange}
              required
              className="mt-1 w-4 h-4 border-slate-300 rounded focus:ring-2 focus:ring-indigo-600"
            />
            <span className="text-sm text-slate-700">
              I agree to the <a href="#" className="text-indigo-600 hover:text-indigo-700 font-medium">Terms and Conditions</a> and <a href="#" className="text-indigo-600 hover:text-indigo-700 font-medium">Privacy Policy</a>
            </span>
          </label>
        </div>

        {/* Submit */}
        <div className="flex space-x-4 pt-6 border-t border-slate-200">
          <button
            type="submit"
            disabled={!formData.agreeTerms}
            className="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors font-medium disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Submit Application
          </button>
          <button
            type="button"
            onClick={() => setCurrentPage('dashboard')}
            className="px-6 py-2 border border-slate-300 text-slate-700 rounded-lg hover:bg-slate-50 transition-colors font-medium"
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
};

export default ApplicationPage;
