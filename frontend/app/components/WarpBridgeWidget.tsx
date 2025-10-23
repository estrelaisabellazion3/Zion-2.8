"use client";

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Zap, ArrowRightLeft, Clock, CheckCircle, AlertCircle } from 'lucide-react';

interface WarpTransaction {
  tx_id: string;
  source_chain: string;
  destination_chain: string;
  amount: number;
  asset: string;
  status: string;
  total_time_ms: number;
  fee_total: number;
  timestamp: string;
}

interface WarpStats {
  status: string;
  supportedChains: string[];
  activeTransfers: number;
  totalTransferred: number;
  averageTransferTime: number;
  successRate: number;
}

export default function WarpBridgeWidget() {
  const [stats, setStats] = useState<WarpStats | null>(null);
  const [recentTransfers, setRecentTransfers] = useState<WarpTransaction[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchWarpData();
    const interval = setInterval(fetchWarpData, 10000); // Update every 10 seconds
    return () => clearInterval(interval);
  }, []);

  const fetchWarpData = async () => {
    try {
      setError(null);

      // Fetch WARP status
      const statusResponse = await fetch('/api/zion-core?endpoint=warp-status');
      const statusData = await statusResponse.json();
      setStats(statusData);

      // Fetch recent transfers
      const transfersResponse = await fetch('/api/zion-core?endpoint=warp-history');
      const transfersData = await transfersResponse.json();
      setRecentTransfers(transfersData.transfers || []);

    } catch (err) {
      console.error('WARP Bridge fetch error:', err);
      setError(err instanceof Error ? err.message : 'Failed to load WARP data');
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'completed': return 'text-green-400';
      case 'pending': return 'text-yellow-400';
      case 'failed': return 'text-red-400';
      default: return 'text-gray-400';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status.toLowerCase()) {
      case 'completed': return <CheckCircle className="w-4 h-4 text-green-400" />;
      case 'pending': return <Clock className="w-4 h-4 text-yellow-400" />;
      case 'failed': return <AlertCircle className="w-4 h-4 text-red-400" />;
      default: return <ArrowRightLeft className="w-4 h-4 text-gray-400" />;
    }
  };

  if (loading) {
    return (
      <div className="bg-gradient-to-br from-purple-900/20 to-blue-900/20 border border-purple-700/30 rounded-xl p-6">
        <div className="animate-pulse">
          <div className="h-6 bg-purple-800/50 rounded mb-4"></div>
          <div className="space-y-3">
            <div className="h-4 bg-purple-800/30 rounded"></div>
            <div className="h-4 bg-purple-800/30 rounded"></div>
            <div className="h-4 bg-purple-800/30 rounded"></div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <motion.div
      className="bg-gradient-to-br from-purple-900/20 to-blue-900/20 border border-purple-700/30 rounded-xl p-6"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
    >
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-xl font-semibold flex items-center">
          <Zap className="w-6 h-6 mr-2 text-purple-400" />
          WARP Bridge
        </h3>
        <div className="flex items-center space-x-2">
          <div className={`w-2 h-2 rounded-full ${stats?.status === 'operational' ? 'bg-green-400' : 'bg-red-400'}`}></div>
          <span className="text-sm text-gray-400 capitalize">{stats?.status || 'unknown'}</span>
        </div>
      </div>

      {error && (
        <div className="mb-4 p-3 bg-red-900/20 border border-red-700 rounded-lg">
          <p className="text-red-300 text-sm">⚠️ {error}</p>
        </div>
      )}

      {/* Stats Overview */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <div className="text-center">
          <div className="text-2xl font-bold text-purple-300">{stats?.supportedChains?.length || 0}</div>
          <div className="text-sm text-gray-400">Supported Chains</div>
        </div>
        <div className="text-center">
          <div className="text-2xl font-bold text-blue-300">{stats?.activeTransfers || 0}</div>
          <div className="text-sm text-gray-400">Active Transfers</div>
        </div>
        <div className="text-center">
          <div className="text-2xl font-bold text-green-300">{stats?.averageTransferTime || 0}ms</div>
          <div className="text-sm text-gray-400">Avg Transfer Time</div>
        </div>
        <div className="text-center">
          <div className="text-2xl font-bold text-yellow-300">{stats?.successRate || 0}%</div>
          <div className="text-sm text-gray-400">Success Rate</div>
        </div>
      </div>

      {/* Recent Transfers */}
      <div className="space-y-3">
        <h4 className="text-lg font-semibold text-gray-300 mb-3">Recent Transfers</h4>
        {recentTransfers.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            <ArrowRightLeft className="w-12 h-12 mx-auto mb-2 opacity-50" />
            <p>No recent transfers</p>
          </div>
        ) : (
          <div className="space-y-2 max-h-64 overflow-y-auto">
            {recentTransfers.slice(0, 5).map((transfer) => (
              <motion.div
                key={transfer.tx_id}
                className="flex items-center justify-between p-3 bg-gray-800/30 rounded-lg border border-gray-700/30"
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
              >
                <div className="flex items-center space-x-3">
                  {getStatusIcon(transfer.status)}
                  <div>
                    <div className="flex items-center space-x-2">
                      <span className="text-sm font-medium text-gray-300">
                        {transfer.source_chain.toUpperCase()}
                      </span>
                      <ArrowRightLeft className="w-3 h-3 text-gray-500" />
                      <span className="text-sm font-medium text-gray-300">
                        {transfer.destination_chain.toUpperCase()}
                      </span>
                    </div>
                    <div className="text-xs text-gray-500">
                      {transfer.amount} {transfer.asset} • {new Date(transfer.timestamp).toLocaleTimeString()}
                    </div>
                  </div>
                </div>
                <div className="text-right">
                  <div className={`text-sm font-medium ${getStatusColor(transfer.status)}`}>
                    {transfer.status.toUpperCase()}
                  </div>
                  <div className="text-xs text-gray-500">
                    {transfer.total_time_ms}ms
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        )}
      </div>

      {/* Supported Chains */}
      {stats?.supportedChains && (
        <div className="mt-6">
          <h4 className="text-sm font-semibold text-gray-400 mb-2">Supported Chains</h4>
          <div className="flex flex-wrap gap-2">
            {stats.supportedChains.map((chain) => (
              <span
                key={chain}
                className="px-2 py-1 bg-purple-900/30 border border-purple-700/50 rounded text-xs text-purple-300"
              >
                {chain.toUpperCase()}
              </span>
            ))}
          </div>
        </div>
      )}
    </motion.div>
  );
}