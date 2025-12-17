import React, { useState } from 'react';
import './App.css';
import DashboardPage from './pages/DashboardPage';
import ChatPage from './pages/ChatPage';
import ApplicationPage from './pages/ApplicationPage';
import LoginSignupPage from './pages/LoginSignupPage';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userData, setUserData] = useState(null);
  const [currentPage, setCurrentPage] = useState('dashboard');
  const [applicationData, setApplicationData] = useState(null);
  const [submittedApplications, setSubmittedApplications] = useState([
    {
      id: 'APP-001',
      name: 'Rajesh Kumar',
      amount: '₹5,00,000',
      status: 'approved',
      date: '2024-12-10',
      progress: 100,
      type: 'Personal',
      email: 'rajesh@email.com'
    },
    {
      id: 'APP-002',
      name: 'Priya Singh',
      amount: '₹10,00,000',
      status: 'underwriting',
      date: '2024-12-09',
      progress: 65,
      type: 'Home',
      email: 'priya@email.com'
    },
    {
      id: 'APP-003',
      name: 'Amit Patel',
      amount: '₹2,50,000',
      status: 'verification',
      date: '2024-12-08',
      progress: 40,
      type: 'Business',
      email: 'amit@email.com'
    },
    {
      id: 'APP-004',
      name: 'Neha Sharma',
      amount: '₹7,50,000',
      status: 'pending',
      date: '2024-12-07',
      progress: 20,
      type: 'Education',
      email: 'neha@email.com'
    }
  ]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      {/* Show Login/Signup if not logged in */}
      {!isLoggedIn ? (
        <LoginSignupPage 
          setCurrentPage={setCurrentPage} 
          setIsLoggedIn={setIsLoggedIn}
          setUserData={setUserData}
        />
      ) : (
        <>
          {/* Navigation Header */}
          <nav className="bg-white shadow-sm border-b border-slate-200">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
              <div className="flex justify-between items-center h-16">
                <div className="flex items-center space-x-8">
                  <h1 className="text-2xl font-bold text-slate-900">LoanFlow</h1>
                  <div className="hidden md:flex space-x-4">
                    <button
                      onClick={() => setCurrentPage('dashboard')}
                      className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                        currentPage === 'dashboard'
                          ? 'text-indigo-600 border-b-2 border-indigo-600'
                          : 'text-slate-600 hover:text-slate-900'
                      }`}
                    >
                      Dashboard
                    </button>
                    <button
                      onClick={() => setCurrentPage('application')}
                      className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                        currentPage === 'application'
                          ? 'text-indigo-600 border-b-2 border-indigo-600'
                          : 'text-slate-600 hover:text-slate-900'
                      }`}
                    >
                      New Application
                    </button>
                    <button
                      onClick={() => setCurrentPage('chat')}
                      className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                        currentPage === 'chat'
                          ? 'text-indigo-600 border-b-2 border-indigo-600'
                          : 'text-slate-600 hover:text-slate-900'
                      }`}
                    >
                      AI Assistant
                    </button>
                  </div>
                </div>
                <div className="flex items-center space-x-4">
                  <div className="hidden sm:block text-sm text-slate-600">
                    Welcome, <span className="font-semibold">{userData?.name || 'User'}</span>
                  </div>
                  <button
                    onClick={() => {
                      setIsLoggedIn(false);
                      setUserData(null);
                      setCurrentPage('dashboard');
                    }}
                    className="px-4 py-2 text-sm font-medium text-indigo-600 hover:text-indigo-700 transition-colors border border-indigo-600 rounded-lg hover:bg-indigo-50"
                  >
                    Logout
                  </button>
                </div>
              </div>
            </div>
          </nav>

          {/* Main Content */}
          <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
            {currentPage === 'dashboard' && <DashboardPage setCurrentPage={setCurrentPage} setApplicationData={setApplicationData} submittedApplications={submittedApplications} />}
            {currentPage === 'application' && <ApplicationPage setCurrentPage={setCurrentPage} setSubmittedApplications={setSubmittedApplications} submittedApplications={submittedApplications} />}
            {currentPage === 'chat' && <ChatPage setCurrentPage={setCurrentPage} setSubmittedApplications={setSubmittedApplications} submittedApplications={submittedApplications} />}
          </main>
        </>
      )}
    </div>
  );
}

export default App;

