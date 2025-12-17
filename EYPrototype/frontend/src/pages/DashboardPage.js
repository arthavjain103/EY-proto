import React, { useState, useEffect } from 'react';

const DashboardPage = ({ setCurrentPage, setApplicationData, submittedApplications }) => {
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(true);
  const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:5000';

  // Fetch applications from backend
  useEffect(() => {
    const fetchApplications = async () => {
      try {
        setLoading(true);
        const response = await fetch(`${API_BASE_URL}/api/applications`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          }
        });

        if (response.ok) {
          const data = await response.json();
          setApplications(data.applications || []);
        } else {
          // Fallback to submitted applications
          setApplications(submittedApplications && submittedApplications.length > 0 
            ? submittedApplications 
            : []);
        }
      } catch (error) {
        console.error('Error fetching applications:', error);
        // Fallback to submitted applications
        setApplications(submittedApplications && submittedApplications.length > 0 
          ? submittedApplications 
          : []);
      } finally {
        setLoading(false);
      }
    };

    fetchApplications();
  }, [submittedApplications, API_BASE_URL]);

  // Calculate stats dynamically
  const totalApps = applications.length;
  const approvedCount = applications.filter(a => a.status === 'approved').length;
  const inProgressCount = applications.filter(a => ['underwriting', 'verification', 'processing'].includes(a.status)).length;
  const pendingCount = applications.filter(a => a.status === 'pending').length;

  const stats = [
    { label: 'Total Applications', value: totalApps.toString(), color: 'indigo' },
    { label: 'Approved', value: approvedCount.toString(), color: 'green' },
    { label: 'In Progress', value: inProgressCount.toString(), color: 'blue' },
    { label: 'Pending', value: pendingCount.toString(), color: 'orange' }
  ];

  const getStatusColor = (status) => {
    const colors = {
      approved: 'bg-green-50 text-green-700 border border-green-200',
      underwriting: 'bg-blue-50 text-blue-700 border border-blue-200',
      verification: 'bg-indigo-50 text-indigo-700 border border-indigo-200',
      pending: 'bg-orange-50 text-orange-700 border border-orange-200',
      processing: 'bg-purple-50 text-purple-700 border border-purple-200',
      rejected: 'bg-red-50 text-red-700 border border-red-200'
    };
    return colors[status] || colors.pending;
  };

  const getProgressColor = (status) => {
    const colors = {
      approved: 'bg-green-500',
      underwriting: 'bg-blue-500',
      verification: 'bg-indigo-500',
      pending: 'bg-orange-500',
      processing: 'bg-purple-500',
      rejected: 'bg-red-500'
    };
    return colors[status] || colors.pending;
  };

  return (
    <div className="space-y-8">
      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {stats.map((stat, idx) => (
          <div key={idx} className="bg-white rounded-lg p-6 shadow-sm border border-slate-200 hover:shadow-lg hover:border-indigo-300 transition-all duration-300 cursor-pointer group">
            <p className="text-slate-600 text-sm font-medium mb-2 group-hover:text-indigo-600 transition-colors">{stat.label}</p>
            <p className={`text-3xl font-bold text-${stat.color}-600 transition-transform group-hover:scale-110`}>{stat.value}</p>
            <div className="mt-3 h-1 bg-slate-100 rounded-full overflow-hidden">
              <div className={`h-full bg-${stat.color}-500 rounded-full transition-all duration-1000`} style={{ width: '70%' }}></div>
            </div>
          </div>
        ))}
      </div>

      {/* Applications List */}
      <div className="bg-white rounded-lg shadow-sm border border-slate-200 overflow-hidden">
        <div className="p-6 border-b border-slate-200 flex justify-between items-center bg-gradient-to-r from-slate-50 to-indigo-50">
          <div>
            <h2 className="text-xl font-bold text-slate-900">📋 Recent Applications</h2>
            <p className="text-sm text-slate-500 mt-1">Fetching from database...</p>
          </div>
          <button
            onClick={() => setCurrentPage('application')}
            className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 active:scale-95 transition-all font-medium shadow-md hover:shadow-lg"
          >
            ➕ New Application
          </button>
        </div>

        {loading ? (
          <div className="p-6 text-center">
            <div className="inline-block">
              <div className="w-12 h-12 border-4 border-slate-200 border-t-indigo-600 rounded-full animate-spin"></div>
            </div>
            <p className="mt-4 text-slate-600">Loading applications...</p>
          </div>
        ) : applications.length === 0 ? (
          <div className="p-6 text-center text-slate-500">
            <p>No applications found</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-slate-100 border-b border-slate-200">
                <tr>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-slate-900">Applicant</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-slate-900">Type</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-slate-900">Amount</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-slate-900">Status</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-slate-900">Progress</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-slate-900">Date</th>
                </tr>
              </thead>
            <tbody className="divide-y divide-slate-200">
              {applications.map((app) => (
                <tr key={app.id} className="hover:bg-indigo-50 transition-colors duration-200 cursor-pointer group">
                  <td className="px-6 py-4 text-sm font-medium text-slate-900 group-hover:text-indigo-600">{app.name}</td>
                  <td className="px-6 py-4 text-sm text-slate-600">{app.type}</td>
                  <td className="px-6 py-4 text-sm font-semibold text-slate-900">{app.amount}</td>
                  <td className="px-6 py-4">
                    <span className={`px-3 py-1 rounded-full text-xs font-medium capitalize ${getStatusColor(app.status)} transition-all`}>
                      {app.status}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center space-x-2">
                      <div className="w-24 bg-slate-200 rounded-full h-2 overflow-hidden">
                        <div
                          className={`h-2 rounded-full ${getProgressColor(app.status)} transition-all duration-1000`}
                          style={{ width: `${app.progress}%` }}
                        />
                      </div>
                      <span className="text-xs font-semibold text-slate-700 w-8">{app.progress}%</span>
                    </div>
                  </td>
                  <td className="px-6 py-4 text-sm text-slate-600">{app.date}</td>
                </tr>
              ))}
            </tbody>
          </table>
            </div>
        )}
      </div>
    </div>
  );
};

export default DashboardPage;
