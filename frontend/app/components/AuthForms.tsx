"use client";

import { useState } from 'react';
import { motion } from 'framer-motion';
import Link from 'next/link';

interface LoginFormProps {
  onLogin: (email: string, password: string) => Promise<void>;
  loading: boolean;
  error: string | null;
}

export function LoginForm({ onLogin, loading, error }: LoginFormProps) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await onLogin(email, password);
  };

  return (
    <motion.div
      className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-black text-white flex items-center justify-center p-6"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
    >
      <motion.div
        className="bg-gradient-to-br from-gray-800 to-gray-900 p-8 rounded-2xl border border-purple-500/30 max-w-md w-full"
        initial={{ scale: 0.9, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ delay: 0.2 }}
      >
        <div className="text-center mb-8">
          <Link href="/" className="inline-block mb-4">
            <motion.div
              className="text-4xl font-bold bg-gradient-to-r from-cyan-400 via-purple-400 to-pink-400 bg-clip-text text-transparent"
              whileHover={{ scale: 1.05 }}
            >
              🌟 ZION
            </motion.div>
          </Link>
          <h1 className="text-2xl font-semibold text-white mb-2">Welcome Back</h1>
          <p className="text-gray-400">Sign in to access your WARP Bridge dashboard</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          {error && (
            <motion.div
              className="p-3 bg-red-900/20 border border-red-700 rounded-lg text-red-300 text-sm"
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
            >
              {error}
            </motion.div>
          )}

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Email Address
            </label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-4 py-3 bg-black/50 border border-cyan-500/30 rounded-lg text-white placeholder-gray-500 focus:border-cyan-400 focus:outline-none transition-colors"
              placeholder="your@email.com"
              required
              disabled={loading}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Password
            </label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-3 bg-black/50 border border-cyan-500/30 rounded-lg text-white placeholder-gray-500 focus:border-cyan-400 focus:outline-none transition-colors"
              placeholder="••••••••"
              required
              disabled={loading}
            />
          </div>

          <motion.button
            type="submit"
            className="w-full bg-gradient-to-r from-cyan-500 to-purple-600 px-6 py-3 rounded-xl font-semibold text-white hover:from-cyan-600 hover:to-purple-700 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            disabled={loading}
          >
            {loading ? (
              <div className="flex items-center justify-center">
                <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
                Signing In...
              </div>
            ) : (
              '🚀 Sign In'
            )}
          </motion.button>
        </form>

        <div className="mt-6 text-center">
          <p className="text-gray-400 text-sm">
            Don't have an account?{' '}
            <Link href="/register" className="text-cyan-400 hover:text-cyan-300 transition-colors">
              Sign up here
            </Link>
          </p>
        </div>

        <div className="mt-8 pt-6 border-t border-gray-700">
          <div className="text-center text-xs text-gray-500">
            🌌 ZION Blockchain v2.8.1 "Estrella"<br/>
            Multi-Chain WARP Bridge Dashboard
          </div>
        </div>
      </motion.div>
    </motion.div>
  );
}

interface RegisterFormProps {
  onRegister: (username: string, email: string, password: string) => Promise<void>;
  loading: boolean;
  error: string | null;
}

export function RegisterForm({ onRegister, loading, error }: RegisterFormProps) {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (password !== confirmPassword) {
      return;
    }
    await onRegister(username, email, password);
  };

  return (
    <motion.div
      className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-black text-white flex items-center justify-center p-6"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
    >
      <motion.div
        className="bg-gradient-to-br from-gray-800 to-gray-900 p-8 rounded-2xl border border-purple-500/30 max-w-md w-full"
        initial={{ scale: 0.9, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ delay: 0.2 }}
      >
        <div className="text-center mb-8">
          <Link href="/" className="inline-block mb-4">
            <motion.div
              className="text-4xl font-bold bg-gradient-to-r from-cyan-400 via-purple-400 to-pink-400 bg-clip-text text-transparent"
              whileHover={{ scale: 1.05 }}
            >
              🌟 ZION
            </motion.div>
          </Link>
          <h1 className="text-2xl font-semibold text-white mb-2">Join ZION</h1>
          <p className="text-gray-400">Create your account to access the WARP Bridge</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          {error && (
            <motion.div
              className="p-3 bg-red-900/20 border border-red-700 rounded-lg text-red-300 text-sm"
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
            >
              {error}
            </motion.div>
          )}

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Username
            </label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full px-4 py-3 bg-black/50 border border-cyan-500/30 rounded-lg text-white placeholder-gray-500 focus:border-cyan-400 focus:outline-none transition-colors"
              placeholder="your_username"
              required
              disabled={loading}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Email Address
            </label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-4 py-3 bg-black/50 border border-cyan-500/30 rounded-lg text-white placeholder-gray-500 focus:border-cyan-400 focus:outline-none transition-colors"
              placeholder="your@email.com"
              required
              disabled={loading}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Password
            </label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-3 bg-black/50 border border-cyan-500/30 rounded-lg text-white placeholder-gray-500 focus:border-cyan-400 focus:outline-none transition-colors"
              placeholder="••••••••"
              required
              disabled={loading}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Confirm Password
            </label>
            <input
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              className="w-full px-4 py-3 bg-black/50 border border-cyan-500/30 rounded-lg text-white placeholder-gray-500 focus:border-cyan-400 focus:outline-none transition-colors"
              placeholder="••••••••"
              required
              disabled={loading}
            />
            {password && confirmPassword && password !== confirmPassword && (
              <p className="text-red-400 text-sm mt-1">Passwords do not match</p>
            )}
          </div>

          <motion.button
            type="submit"
            className="w-full bg-gradient-to-r from-cyan-500 to-purple-600 px-6 py-3 rounded-xl font-semibold text-white hover:from-cyan-600 hover:to-purple-700 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            disabled={loading || password !== confirmPassword}
          >
            {loading ? (
              <div className="flex items-center justify-center">
                <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
                Creating Account...
              </div>
            ) : (
              '🌟 Create Account'
            )}
          </motion.button>
        </form>

        <div className="mt-6 text-center">
          <p className="text-gray-400 text-sm">
            Already have an account?{' '}
            <Link href="/login" className="text-cyan-400 hover:text-cyan-300 transition-colors">
              Sign in here
            </Link>
          </p>
        </div>

        <div className="mt-8 pt-6 border-t border-gray-700">
          <div className="text-center text-xs text-gray-500">
            🌌 ZION Blockchain v2.8.1 "Estrella"<br/>
            Multi-Chain WARP Bridge Dashboard
          </div>
        </div>
      </motion.div>
    </motion.div>
  );
}