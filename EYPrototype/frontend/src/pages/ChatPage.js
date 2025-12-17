import React, { useState } from 'react';
import { AGENT_ICONS, generateNewApplication, getStatusFromProgress } from '../config/applicationTemplates';

const ChatPage = ({ setCurrentPage, setSubmittedApplications, submittedApplications }) => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'bot',
      agent: 'SalesAgent',
      timestamp: new Date(Date.now() - 3000),
      text: 'Welcome! I\'m your AI Loan Assistant. How can I help you today?\n\nI can assist with:\nLoan applications\nEligibility checks\nProduct information\nApplication status'
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [customerId, setCustomerId] = useState(null);
  const [customerData, setCustomerData] = useState({});

  const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:5000';

  const getAgentIcon = (agent) => {
    return AGENT_ICONS[agent] || '🤖';
  };

  const formatTime = (date) => {
    if (!date) return '';
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    return `${hours}:${minutes}`;
  };

  const callBackendAgent = async (message) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: message,
          customer_id: customerId,
          customer_data: customerData,
          documents: []
        })
      });

      if (!response.ok) {
        throw new Error(`Backend error: ${response.statusText}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Backend API Error:', error);
      return {
        success: false,
        error: error.message,
        response: 'Sorry, I\'m having trouble connecting to the backend. Please try again.'
      };
    }
  };

  const extractAgentFromResult = (result) => {
    // Determine which agent handled the request based on result
    if (result.sales_result) return 'SalesAgent';
    if (result.verification_result) return 'VerificationAgent';
    if (result.underwriting_result) return 'UnderwritingAgent';
    if (result.sanction_result) return 'SanctionLetterAgent';
    return 'SalesAgent'; // Default
  };

  const handleSend = async () => {
    if (input.trim()) {
      setLoading(true);
      const userMsg = { 
        id: messages.length + 1, 
        type: 'user', 
        timestamp: new Date(), 
        text: input 
      };

      // Add user message immediately
      setMessages(prevMessages => [...prevMessages, userMsg]);
      setInput('');

      try {
        // Call backend agent
        const backendResult = await callBackendAgent(input);

        if (backendResult.success) {
          // Extract agent name and response from backend result
          const agentName = extractAgentFromResult(backendResult.result || {});
          const botResponseText = backendResult.response || 'Processing completed.';

          // Add bot response
          setMessages(prevMessages => [
            ...prevMessages,
            {
              id: prevMessages.length + 1,
              type: 'bot',
              agent: agentName,
              timestamp: new Date(),
              text: botResponseText
            }
          ]);

          // Update customer data if provided in result
          if (backendResult.result && backendResult.result.customer_data) {
            setCustomerData(backendResult.result.customer_data);
          }

          // Set customer ID from first response
          if (backendResult.customer_id && !customerId) {
            setCustomerId(backendResult.customer_id);
          }

          // Handle application creation if approved
          if (backendResult.result && backendResult.result.final_decision === 'approve') {
            const newApp = generateNewApplication(
              backendResult.result.customer_data?.name || 'Applicant',
              backendResult.result.customer_data?.loan_type || 'Personal Loan',
              `₹${backendResult.result.underwriting_result?.loan_amount || 500000}`
            );
            newApp.progress = 90;
            newApp.status = getStatusFromProgress(newApp.progress);

            setSubmittedApplications([newApp, ...submittedApplications]);
          }
        } else {
          // Handle error response
          setMessages(prevMessages => [
            ...prevMessages,
            {
              id: prevMessages.length + 1,
              type: 'bot',
              agent: 'SalesAgent',
              timestamp: new Date(),
              text: backendResult.response || 'Error processing request. Please try again.'
            }
          ]);
        }
      } catch (error) {
        console.error('Error:', error);
        setMessages(prevMessages => [
          ...prevMessages,
          {
            id: prevMessages.length + 1,
            type: 'bot',
            agent: 'SalesAgent',
            timestamp: new Date(),
            text: 'Sorry, I encountered an error. Please try again.'
          }
        ]);
      } finally {
        setLoading(false);
      }
    }
  };

  // Handle Enter key
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !loading) {
      handleSend();
    }
  };

  return (
    <div className="max-w-4xl mx-auto h-auto bg-white rounded-lg shadow-sm border border-slate-200 overflow-hidden">
      {/* Chat Header */}
      <div className="bg-gradient-to-r from-indigo-600 to-indigo-700 text-white p-6">
        <h2 className="text-xl font-bold">AI Loan Assistant</h2>
        <p className="text-indigo-100 text-sm mt-1">Multi-Agent Processing System • Real-time Backend Integration</p>
      </div>

      {/* Messages Area */}
      <div className="h-[500px] overflow-y-auto p-6 space-y-4 bg-slate-50 scroll-smooth">
        {messages.length === 0 ? (
          <div className="h-full flex items-center justify-center text-center">
            <div className="text-slate-500">
              <p className="text-4xl mb-4">💬</p>
              <p className="text-lg font-medium">Start a conversation</p>
              <p className="text-sm mt-2">Ask about loans, eligibility, or submit an application</p>
            </div>
          </div>
        ) : (
          messages.map((msg) => (
            <div key={msg.id} className={`flex animate-slideIn ${msg.type === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`max-w-2xl ${msg.type === 'user' ? '' : 'w-full'}`}>
                {/* Bot Agent Info */}
                {msg.type === 'bot' && msg.agent && (
                  <div className="flex items-center space-x-2 mb-2 px-2">
                    <span className="text-lg">{getAgentIcon(msg.agent)}</span>
                    <span className="text-xs font-semibold text-slate-600">{msg.agent}</span>
                    {msg.timestamp && (
                      <span className="text-xs text-slate-400 ml-auto">{formatTime(msg.timestamp)}</span>
                    )}
                  </div>
                )}
                
                {/* Message Bubble */}
                <div
                  className={`px-4 py-3 rounded-lg shadow-sm transition-all ${
                    msg.type === 'user'
                      ? 'bg-indigo-600 text-white rounded-br-none hover:shadow-md'
                      : 'bg-white text-slate-900 border border-slate-200 rounded-bl-none hover:shadow-md'
                  }`}
                >
                  <p className="text-sm whitespace-pre-wrap">{msg.text}</p>
                  
                  {/* Timestamp for messages */}
                  {msg.timestamp && (
                    <p className={`text-xs mt-2 ${msg.type === 'user' ? 'text-indigo-100' : 'text-slate-400'}`}>
                      {formatTime(msg.timestamp)}
                    </p>
                  )}
                </div>
              </div>
            </div>
          ))
        )}
        {loading && (
          <div className="flex justify-start animate-slideIn">
            <div>
              <div className="flex items-center space-x-2 mb-2 px-2">
                <span className="text-lg">⏳</span>
                <span className="text-xs font-semibold text-slate-600">Processing...</span>
              </div>
              <div className="bg-white text-slate-900 border border-slate-200 rounded-lg rounded-bl-none px-4 py-3">
                <div className="flex space-x-2">
                  <div className="w-2 h-2 bg-slate-600 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                  <div className="w-2 h-2 bg-slate-600 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                  <div className="w-2 h-2 bg-slate-600 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Input Area */}
      <div className="bg-white border-t border-slate-200 p-6">
        <div className="flex space-x-3">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask a question or continue the conversation..."
            disabled={loading}
            className="flex-1 px-4 py-3 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-600 text-sm disabled:bg-slate-100 disabled:cursor-not-allowed transition-colors"
          />
          <button
            onClick={handleSend}
            disabled={loading}
            className="px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-all font-medium text-sm disabled:bg-slate-400 disabled:cursor-not-allowed active:scale-95"
          >
            {loading ? (
              <span className="flex items-center">
                <span className="animate-spin mr-2">⏳</span>
                Sending...
              </span>
            ) : (
              'Send'
            )}
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatPage;
