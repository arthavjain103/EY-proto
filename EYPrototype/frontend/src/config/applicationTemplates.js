// Configuration - Utilities and Constants
// All dynamic data comes from backend API

// Loan types (used in ApplicationPage form)
export const LOAN_TYPES = [
  'Personal Loan',
  'Home Loan',
  'Business Loan',
  'Education Loan',
  'Auto Loan',
  'Gold Loan'
];

// Application statuses
export const APPLICATION_STATUSES = [
  'pending',
  'processing',
  'verification',
  'underwriting',
  'approved',
  'rejected'
];

// Status progress mapping
export const STATUS_PROGRESS = {
  'pending': { min: 0, max: 20, label: 'Pending' },
  'processing': { min: 20, max: 40, label: 'Processing' },
  'verification': { min: 40, max: 70, label: 'Verification' },
  'underwriting': { min: 70, max: 95, label: 'Underwriting' },
  'approved': { min: 95, max: 100, label: 'Approved' },
  'rejected': { min: 0, max: 100, label: 'Rejected' }
};

// Generate new application for form submission
export const generateNewApplication = (customerName, loanType, loanAmount) => {
  const today = new Date().toISOString().split('T')[0];
  const randomProgress = Math.floor(Math.random() * 20) + 20;
  
  return {
    id: `APP-${Math.random().toString(36).substr(2, 9).toUpperCase()}`,
    name: customerName || 'New Applicant',
    type: loanType || 'Personal Loan',
    amount: loanAmount || '₹1,00,000',
    date: today,
    progress: randomProgress,
    status: 'pending',
    email: `applicant-${Date.now()}@email.com`
  };
};

// Get status from progress percentage
export const getStatusFromProgress = (progress) => {
  if (progress >= 95) return 'approved';
  if (progress >= 70) return 'underwriting';
  if (progress >= 40) return 'verification';
  if (progress >= 20) return 'processing';
  return 'pending';
};

// Interest rates by loan type
export const INTEREST_RATES = {
  'Personal Loan': { min: 7.5, max: 12, default: 8.5 },
  'Home Loan': { min: 6.5, max: 8.5, default: 7.5 },
  'Business Loan': { min: 8, max: 14, default: 10.5 },
  'Education Loan': { min: 7, max: 10, default: 8.5 },
  'Auto Loan': { min: 6.5, max: 10, default: 8 },
  'Gold Loan': { min: 7, max: 12, default: 9 }
};

// Tenure options (in months) by loan type
export const TENURE_OPTIONS = {
  'Personal Loan': [12, 24, 36, 48, 60],
  'Home Loan': [60, 120, 180, 240],
  'Business Loan': [12, 36, 60, 84],
  'Education Loan': [60, 120, 180],
  'Auto Loan': [36, 48, 60],
  'Gold Loan': [12, 24, 36]
};

// Loan limits by type
export const LOAN_LIMITS = {
  'Personal Loan': { min: 50000, max: 5000000 },
  'Home Loan': { min: 1000000, max: 10000000 },
  'Business Loan': { min: 500000, max: 10000000 },
  'Education Loan': { min: 500000, max: 2000000 },
  'Auto Loan': { min: 200000, max: 5000000 },
  'Gold Loan': { min: 100000, max: 1000000 }
};

// Calculate EMI (Equated Monthly Installment)
export const calculateEMI = (principal, annualRate, tenure) => {
  const monthlyRate = annualRate / 100 / 12;
  const monthlyTenure = tenure;
  
  if (monthlyRate === 0) {
    return Math.round(principal / monthlyTenure);
  }
  
  const emi = (principal * monthlyRate * Math.pow(1 + monthlyRate, monthlyTenure)) / 
              (Math.pow(1 + monthlyRate, monthlyTenure) - 1);
  
  return Math.round(emi);
};

// Calculate total interest paid
export const calculateTotalInterest = (principal, emi, tenure) => {
  return Math.round((emi * tenure) - principal);
};

// Agent icons for chat display
export const AGENT_ICONS = {
  'SalesAgent': '💼',
  'VerificationAgent': '✓',
  'UnderwritingAgent': '🔍',
  'SanctionLetterAgent': '📋'
};

// Agent color themes for chat display
export const AGENT_COLORS = {
  'SalesAgent': 'bg-blue-50 border-blue-200',
  'VerificationAgent': 'bg-green-50 border-green-200',
  'UnderwritingAgent': 'bg-indigo-50 border-indigo-200',
  'SanctionLetterAgent': 'bg-purple-50 border-purple-200'
};
