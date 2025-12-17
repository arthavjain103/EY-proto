import React, { useState } from 'react';

const LoginSignupPage = ({ setCurrentPage, setIsLoggedIn, setUserData }) => {
  const [isSignup, setIsSignup] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [fullName, setFullName] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  // Hardcoded credentials for demo
  const demoCredentials = [
    { email: 'demo@example.com', password: 'demo123', name: 'Rajesh Kumar' },
    { email: 'user@example.com', password: 'password123', name: 'Priya Desai' },
    { email: 'test@example.com', password: 'test123', name: 'Amit Patel' }
  ];

  const handleLogin = (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    // Simulate API call delay
    setTimeout(() => {
      const validUser = demoCredentials.find(
        (cred) => cred.email === email && cred.password === password
      );

      if (validUser) {
        setIsLoggedIn(true);
        setUserData({
          email: validUser.email,
          name: validUser.name
        });
        setCurrentPage('dashboard');
      } else {
        setError('Invalid email or password. Try demo@example.com / demo123');
      }
      setLoading(false);
    }, 1000);
  };

  const handleSignup = (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    // Simulate API call delay
    setTimeout(() => {
      if (password !== confirmPassword) {
        setError('Passwords do not match!');
        setLoading(false);
        return;
      }

      if (password.length < 6) {
        setError('Password must be at least 6 characters!');
        setLoading(false);
        return;
      }

      // Success - log them in
      setIsLoggedIn(true);
      setUserData({
        email: email,
        name: fullName
      });
      setCurrentPage('dashboard');
      setLoading(false);
    }, 1000);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-slate-50 to-blue-50 flex items-center justify-center px-4">
      {/* Background decorative elements */}
      <div className="absolute top-10 left-10 w-72 h-72 bg-indigo-200 opacity-20 rounded-full blur-3xl"></div>
      <div className="absolute bottom-10 right-10 w-96 h-96 bg-blue-200 opacity-20 rounded-full blur-3xl"></div>

      <div className="relative z-10 w-full max-w-md">
        {/* Logo & Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-indigo-900 mb-2">LoanFlow</h1>
          <p className="text-indigo-600">Smart Loan Processing Platform</p>
        </div>

        {/* Auth Form Card */}
        <div className="bg-white rounded-2xl shadow-lg p-8 border border-indigo-100">
          {/* Tab Switch */}
          <div className="flex gap-4 mb-8">
            <button
              onClick={() => {
                setIsSignup(false);
                setError('');
              }}
              className={`flex-1 py-2 px-4 rounded-lg font-semibold transition-all ${
                !isSignup
                  ? 'bg-indigo-600 text-white'
                  : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
              }`}
            >
              Login
            </button>
            <button
              onClick={() => {
                setIsSignup(true);
                setError('');
              }}
              className={`flex-1 py-2 px-4 rounded-lg font-semibold transition-all ${
                isSignup
                  ? 'bg-indigo-600 text-white'
                  : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
              }`}
            >
              Sign Up
            </button>
          </div>

          {/* Form */}
          <form onSubmit={isSignup ? handleSignup : handleLogin} className="space-y-4">
            {/* Full Name (Signup only) */}
            {isSignup && (
              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-2">
                  Full Name
                </label>
                <input
                  type="text"
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  placeholder="Enter your full name"
                  className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:border-transparent"
                  required={isSignup}
                />
              </div>
            )}

            {/* Email */}
            <div>
              <label className="block text-sm font-semibold text-slate-700 mb-2">
                Email Address
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="your@email.com"
                className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:border-transparent"
                required
              />
            </div>

            {/* Password */}
            <div>
              <label className="block text-sm font-semibold text-slate-700 mb-2">
                Password
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:border-transparent"
                required
              />
            </div>

            {/* Confirm Password (Signup only) */}
            {isSignup && (
              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-2">
                  Confirm Password
                </label>
                <input
                  type="password"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  placeholder="••••••••"
                  className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:border-transparent"
                  required={isSignup}
                />
              </div>
            )}

            {/* Error Message */}
            {error && (
              <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
                <p className="text-red-700 text-sm font-medium">{error}</p>
              </div>
            )}

            {/* Submit Button */}
            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 bg-indigo-600 text-white font-bold rounded-lg hover:bg-indigo-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? (
                <span className="flex items-center justify-center">
                  <span className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></span>
                  Processing...
                </span>
              ) : isSignup ? (
                'Create Account'
              ) : (
                'Login'
              )}
            </button>
          </form>

          {/* Divider */}
          <div className="my-6 flex items-center">
            <div className="flex-1 h-px bg-slate-300"></div>
            <span className="px-4 text-slate-500 text-sm">or</span>
            <div className="flex-1 h-px bg-slate-300"></div>
          </div>

          {/* Social Login (Optional) */}
          <div className="grid grid-cols-2 gap-4">
            <button className="py-2 px-4 border border-slate-300 rounded-lg hover:bg-slate-50 transition-colors font-medium text-slate-700 text-sm">
              Google
            </button>
            <button className="py-2 px-4 border border-slate-300 rounded-lg hover:bg-slate-50 transition-colors font-medium text-slate-700 text-sm">
              LinkedIn
            </button>
          </div>

          {/* Footer Text */}
          <div className="mt-6 text-center text-sm text-slate-600">
            {isSignup ? (
              <>
                Already have an account?{' '}
                <button
                  onClick={() => setIsSignup(false)}
                  className="text-indigo-600 hover:text-indigo-700 font-semibold"
                >
                  Login here
                </button>
              </>
            ) : (
              <>
                Don't have an account?{' '}
                <button
                  onClick={() => setIsSignup(true)}
                  className="text-indigo-600 hover:text-indigo-700 font-semibold"
                >
                  Sign up now
                </button>
              </>
            )}
          </div>
        </div>

        {/* Features */}
        <div className="mt-8 grid grid-cols-3 gap-4">
          <div className="text-center text-indigo-700">
            <div className="text-2xl mb-2">—</div>
            <p className="text-xs font-medium">Fast Approval</p>
          </div>
          <div className="text-center text-indigo-700">
            <div className="text-2xl mb-2">—</div>
            <p className="text-xs font-medium">Secure & Safe</p>
          </div>
          <div className="text-center text-indigo-700">
            <div className="text-2xl mb-2">—</div>
            <p className="text-xs font-medium">AI Powered</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginSignupPage;
