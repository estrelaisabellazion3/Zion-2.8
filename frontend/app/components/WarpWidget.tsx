"use client";

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Zap, ArrowRightLeft, Clock, DollarSign, CheckCircle, XCircle } from 'lucide-react';

interface WarpTransaction {
  id: string;
  source_chain: string;
  destination_chain: string;
  asset: string;
  amount: number;
  status: 'pending' | 'confirmed' | 'completed' | 'failed';
  timestamp: string;
  tx_hash?: string;
  bridge_fee: number;
  warp_speed: boolean;
}

interface WarpStats {
  total_transfers: number;
  warp_speed_count: number;
  total_volume: number;
  avg_time: number;
  success_rate: number;
}

interface WarpWidgetProps {
  className?: string;
}

export default function WarpWidget({ className = "" }: WarpWidgetProps) {
  const [transactions, setTransactions] = useState<WarpTransaction[]>([]);
  const [stats, setStats] = useState<WarpStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [showTransferForm, setShowTransferForm] = useState(false);
  const [transferLoading, setTransferLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [transferForm, setTransferForm] = useState({
    source_chain: 'ZION',
    destination_chain: 'Ethereum',
    asset: 'ZION',
    amount: ''
  });

  // Handle transfer form submission
  const handleTransferSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setTransferLoading(true);
    setError(null);

    try {
      const token = localStorage.getItem('zion_auth_token');
      if (!token) {
        throw new Error('Authentication required');
      }

      const response = await fetch('/api/warp', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(transferForm)
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Transfer failed');
      }

      const data = await response.json();

      // Add new transaction to list
      const newTx: WarpTransaction = {
        id: data.transaction.id,
        source_chain: data.transaction.source_chain,
        destination_chain: data.transaction.destination_chain,
        asset: data.transaction.asset,
        amount: data.transaction.amount,
        status: data.transaction.status,
        timestamp: new Date(data.transaction.timestamp).toLocaleString(),
        bridge_fee: data.transaction.bridge_fee,
        warp_speed: data.transaction.warp_speed
      };

      setTransactions(prev => [newTx, ...prev]);
      setShowTransferForm(false);
      setTransferForm({
        source_chain: 'ZION',
        destination_chain: 'Ethereum',
        asset: 'ZION',
        amount: ''
      });

    } catch (err) {
      setError(err instanceof Error ? err.message : 'Transfer failed');
    } finally {
      setTransferLoading(false);
    }
  };

  // Load WARP data from API
  const loadWarpData = async () => {
    try {
      const token = localStorage.getItem('zion_auth_token');
      if (!token) {
        setError('Authentication required');
        setLoading(false);
        return;
      }

      const response = await fetch('/api/warp', {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) {
        throw new Error('Failed to load WARP data');
      }

      const data = await response.json();

      setTransactions(data.transactions.map((tx: any) => ({
        id: tx.id,
        source_chain: tx.source_chain,
        destination_chain: tx.destination_chain,
        asset: tx.asset,
        amount: tx.amount,
        status: tx.status,
        timestamp: new Date(tx.timestamp).toLocaleString(),
        tx_hash: tx.tx_hash,
        bridge_fee: tx.bridge_fee,
        warp_speed: tx.warp_speed
      })));

      setStats(data.stats);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load data');
      console.error('WARP data load error:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadWarpData();
  }, []);

  const getStatusColor = (status: string) => {
    switch(status) {
      case 'completed': return 'text-green-400 bg-green-500/20';
      case 'confirmed': return 'text-blue-400 bg-blue-500/20';
      case 'pending': return 'text-yellow-400 bg-yellow-500/20';
      case 'failed': return 'text-red-400 bg-red-500/20';
      default: return 'text-gray-400 bg-gray-500/20';
    }
  };

  const getStatusIcon = (status: string) => {
    switch(status) {
      case 'completed': return <CheckCircle className="w-4 h-4" />;
      case 'confirmed': return <Clock className="w-4 h-4" />;
      case 'pending': return <div className="w-4 h-4 border-2 border-yellow-400 border-t-transparent rounded-full animate-spin" />;
      case 'failed': return <XCircle className="w-4 h-4" />;
      default: return <div className="w-4 h-4 rounded-full bg-gray-400" />;
    }
  };

  const formatTime = (ms: number): string => {
    if (ms < 1000) return `${ms}ms`;
    return `${(ms / 1000).toFixed(1)}s`;
  };

  if (loading) {
    return (
      <motion.div
        className={`bg-gradient-to-br from-purple-900/20 to-blue-900/20 border border-purple-700/30 rounded-xl p-6 ${className}`}
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <div className="flex items-center justify-center h-32">
          <div className="w-8 h-8 border-4 border-purple-500 border-t-transparent rounded-full animate-spin"></div>
        </div>
      </motion.div>
    );
  }

  return (
    <motion.div
      className={`bg-gradient-to-br from-purple-900/20 to-blue-900/20 border border-purple-700/30 rounded-xl p-6 ${className}`}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
    >
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-purple-600/30 rounded-lg">
            <Zap className="w-6 h-6 text-purple-300" />
          </div>
          <div>
            <h3 className="text-xl font-semibold text-white">🌌 WARP Bridge</h3>
            <p className="text-gray-400 text-sm">Multi-Chain Asset Transfers</p>
          </div>
        </div>

        <motion.button
          onClick={() => setShowTransferForm(!showTransferForm)}
          className="px-4 py-2 bg-cyan-600/30 hover:bg-cyan-600/50 border border-cyan-700 rounded-lg text-cyan-300 text-sm transition-colors"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          {showTransferForm ? 'Cancel' : 'New Transfer'}
        </motion.button>
      </div>

      {/* Stats */}
      {stats && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          <div className="text-center">
            <div className="text-2xl font-bold text-cyan-400">{stats.total_transfers.toLocaleString()}</div>
            <div className="text-xs text-gray-400">Total Transfers</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-green-400">{stats.warp_speed_count.toLocaleString()}</div>
            <div className="text-xs text-gray-400">WARP Speed</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-yellow-400">${stats.total_volume.toLocaleString()}</div>
            <div className="text-xs text-gray-400">Total Volume</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-purple-400">{formatTime(stats.avg_time)}</div>
            <div className="text-xs text-gray-400">Avg Time</div>
          </div>
        </div>
      )}

      {/* Transfer Form */}
      {showTransferForm && (
        <motion.div
          className="mb-6 p-4 bg-black/30 border border-cyan-500/30 rounded-lg"
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: 'auto' }}
          exit={{ opacity: 0, height: 0 }}
        >
          <h4 className="text-lg font-semibold text-cyan-300 mb-4">🚀 Initiate WARP Transfer</h4>

          {error && (
            <div className="mb-4 p-3 bg-red-900/20 border border-red-700 rounded-lg text-red-300 text-sm">
              {error}
            </div>
          )}

          <form onSubmit={handleTransferSubmit}>
            <div className="grid gap-4 md:grid-cols-2">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">From Chain</label>
                <select
                  value={transferForm.source_chain}
                  onChange={(e) => setTransferForm(prev => ({ ...prev, source_chain: e.target.value }))}
                  className="w-full px-3 py-2 bg-black/50 border border-cyan-500/30 rounded-lg text-white focus:border-cyan-400 focus:outline-none"
                >
                  <option>ZION</option>
                  <option>Ethereum</option>
                  <option>Bitcoin</option>
                  <option>Polygon</option>
                  <option>BSC</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">To Chain</label>
                <select
                  value={transferForm.destination_chain}
                  onChange={(e) => setTransferForm(prev => ({ ...prev, destination_chain: e.target.value }))}
                  className="w-full px-3 py-2 bg-black/50 border border-cyan-500/30 rounded-lg text-white focus:border-cyan-400 focus:outline-none"
                >
                  <option>Ethereum</option>
                  <option>ZION</option>
                  <option>Bitcoin</option>
                  <option>Polygon</option>
                  <option>BSC</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Asset</label>
                <select
                  value={transferForm.asset}
                  onChange={(e) => setTransferForm(prev => ({ ...prev, asset: e.target.value }))}
                  className="w-full px-3 py-2 bg-black/50 border border-cyan-500/30 rounded-lg text-white focus:border-cyan-400 focus:outline-none"
                >
                  <option>ZION</option>
                  <option>BTC</option>
                  <option>ETH</option>
                  <option>USDC</option>
                  <option>USDT</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Amount</label>
                <input
                  type="number"
                  step="0.00000001"
                  placeholder="0.00"
                  value={transferForm.amount}
                  onChange={(e) => setTransferForm(prev => ({ ...prev, amount: e.target.value }))}
                  className="w-full px-3 py-2 bg-black/50 border border-cyan-500/30 rounded-lg text-white placeholder-gray-500 focus:border-cyan-400 focus:outline-none"
                  required
                  disabled={transferLoading}
                />
              </div>
            </div>

            <div className="flex gap-3 mt-4">
              <motion.button
                type="submit"
                className="flex-1 bg-gradient-to-r from-cyan-500 to-purple-600 px-6 py-3 rounded-xl font-semibold text-white hover:from-cyan-600 hover:to-purple-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                disabled={transferLoading}
              >
                {transferLoading ? (
                  <div className="flex items-center justify-center">
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
                    Processing...
                  </div>
                ) : (
                  '⚡ WARP Transfer'
                )}
              </motion.button>
              <motion.button
                type="button"
                onClick={() => setShowTransferForm(false)}
                className="px-6 py-3 bg-gray-600/30 border border-gray-700 rounded-xl text-gray-300 hover:bg-gray-600/50 transition-colors"
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
              >
                Cancel
              </motion.button>
            </div>
          </form>
        </motion.div>
      )}

      {/* Recent Transactions */}
      <div>
        <h4 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
          <ArrowRightLeft className="w-5 h-5" />
          Recent Transfers
        </h4>

        <div className="space-y-3">
          {transactions.map((tx, index) => (
            <motion.div
              key={tx.id}
              className="bg-black/20 border border-gray-700/50 rounded-lg p-4"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
            >
              <div className="flex justify-between items-start mb-3">
                <div className="flex items-center gap-3">
                  <div className={`p-1 rounded-full ${getStatusColor(tx.status)}`}>
                    {getStatusIcon(tx.status)}
                  </div>
                  <div>
                    <div className="flex items-center gap-2 text-sm">
                      <span className="text-cyan-300 font-medium">{tx.source_chain}</span>
                      <ArrowRightLeft className="w-3 h-3 text-gray-400" />
                      <span className="text-pink-300 font-medium">{tx.destination_chain}</span>
                    </div>
                    <div className="text-xs text-gray-400">{tx.timestamp}</div>
                  </div>
                </div>

                <div className="text-right">
                  <div className="text-lg font-bold text-white">
                    {tx.amount.toFixed(8)} {tx.asset}
                  </div>
                  {tx.warp_speed && (
                    <div className="text-xs text-yellow-400 font-medium">⚡ WARP SPEED</div>
                  )}
                </div>
              </div>

              {tx.tx_hash && (
                <div className="text-xs text-gray-500 font-mono break-all">
                  TX: {tx.tx_hash.substring(0, 20)}...
                </div>
              )}

              <div className="flex justify-between items-center mt-2 text-xs text-gray-400">
                <span>Fee: {tx.bridge_fee.toFixed(8)} {tx.asset}</span>
                <span>Status: {tx.status.toUpperCase()}</span>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </motion.div>
  );
}