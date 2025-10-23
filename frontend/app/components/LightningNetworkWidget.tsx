"use client";

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Zap, Coins, Network, TrendingUp, ArrowUpDown } from 'lucide-react';

interface LightningChannel {
  id: string;
  capacity: number;
  localBalance: number;
  remoteBalance: number;
  active: boolean;
  peerAlias?: string;
}

interface LightningStats {
  channels: LightningChannel[];
  totalCapacity: number;
  totalLocalBalance: number;
  totalRemoteBalance: number;
  activeChannels: number;
  pendingChannels: number;
  nodeAlias: string;
  nodeId: string;
}

export default function LightningNetworkWidget() {
  const [stats, setStats] = useState<LightningStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchLightningData();
    const interval = setInterval(fetchLightningData, 12000); // Update every 12 seconds
    return () => clearInterval(interval);
  }, []);

  const fetchLightningData = async () => {
    try {
      setError(null);
      const response = await fetch('/api/zion-core?endpoint=lightning-channels');
      const data = await response.json();
      setStats(data);
    } catch (err) {
      console.error('Lightning Network fetch error:', err);
      setError(err instanceof Error ? err.message : 'Failed to load lightning data');
    } finally {
      setLoading(false);
    }
  };

  const formatSats = (amount: number): string => {
    if (amount >= 100000000) return `${(amount / 100000000).toFixed(2)} ZION`;
    if (amount >= 1000000) return `${(amount / 1000000).toFixed(1)}M sats`;
    if (amount >= 1000) return `${(amount / 1000).toFixed(1)}K sats`;
    return `${amount} sats`;
  };

  const getBalanceRatio = (local: number, remote: number): number => {
    const total = local + remote;
    return total > 0 ? (local / total) * 100 : 50;
  };

  if (loading) {
    return (
      <div className="bg-gradient-to-br from-yellow-900/20 to-orange-900/20 border border-yellow-700/30 rounded-xl p-6">
        <div className="animate-pulse">
          <div className="h-6 bg-yellow-800/50 rounded mb-4"></div>
          <div className="space-y-3">
            <div className="h-4 bg-yellow-800/30 rounded"></div>
            <div className="h-4 bg-yellow-800/30 rounded"></div>
            <div className="h-4 bg-yellow-800/30 rounded"></div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <motion.div
      className="bg-gradient-to-br from-yellow-900/20 to-orange-900/20 border border-yellow-700/30 rounded-xl p-6"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
    >
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-xl font-semibold flex items-center">
          <Zap className="w-6 h-6 mr-2 text-yellow-400" />
          Lightning Network
        </h3>
        <div className="flex items-center space-x-2">
          <div className="w-2 h-2 rounded-full bg-green-400"></div>
          <span className="text-sm text-gray-400">Online</span>
        </div>
      </div>

      {error && (
        <div className="mb-4 p-3 bg-red-900/20 border border-red-700 rounded-lg">
          <p className="text-red-300 text-sm">⚠️ {error}</p>
        </div>
      )}

      {/* Node Info */}
      <div className="mb-6 p-4 bg-gray-800/30 rounded-lg border border-gray-700/30">
        <div className="flex items-center justify-between">
          <div>
            <div className="text-lg font-semibold text-yellow-300">
              {stats?.nodeAlias || 'ZION Lightning Node'}
            </div>
            <div className="text-sm text-gray-400">
              {stats?.nodeId ? `${stats.nodeId.slice(0, 12)}...${stats.nodeId.slice(-6)}` : 'Node ID'}
            </div>
          </div>
          <div className="text-right">
            <div className="text-sm text-gray-400">Channels</div>
            <div className="text-xl font-bold text-yellow-300">
              {stats?.activeChannels || 0}/{stats?.channels?.length || 0}
            </div>
          </div>
        </div>
      </div>

      {/* Stats Overview */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <div className="text-center">
          <div className="text-2xl font-bold text-yellow-300">{formatSats(stats?.totalCapacity || 0)}</div>
          <div className="text-sm text-gray-400">Total Capacity</div>
        </div>
        <div className="text-center">
          <div className="text-2xl font-bold text-green-300">{formatSats(stats?.totalLocalBalance || 0)}</div>
          <div className="text-sm text-gray-400">Local Balance</div>
        </div>
        <div className="text-center">
          <div className="text-2xl font-bold text-blue-300">{formatSats(stats?.totalRemoteBalance || 0)}</div>
          <div className="text-sm text-gray-400">Remote Balance</div>
        </div>
        <div className="text-center">
          <div className="text-2xl font-bold text-purple-300">{stats?.pendingChannels || 0}</div>
          <div className="text-sm text-gray-400">Pending</div>
        </div>
      </div>

      {/* Channels List */}
      <div className="space-y-3">
        <h4 className="text-lg font-semibold text-gray-300 mb-3 flex items-center">
          <Network className="w-5 h-5 mr-2" />
          Channels
        </h4>
        {stats?.channels?.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            <Network className="w-12 h-12 mx-auto mb-2 opacity-50" />
            <p>No channels open</p>
          </div>
        ) : (
          <div className="space-y-3 max-h-80 overflow-y-auto">
            {stats?.channels?.map((channel, index) => {
              const balanceRatio = getBalanceRatio(channel.localBalance, channel.remoteBalance);
              return (
                <motion.div
                  key={channel.id}
                  className="p-4 bg-gray-800/30 rounded-lg border border-gray-700/30"
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.1 }}
                >
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center space-x-3">
                      <div className={`w-3 h-3 rounded-full ${channel.active ? 'bg-green-400' : 'bg-red-400'}`}></div>
                      <div>
                        <div className="text-sm font-medium text-gray-300">
                          {channel.peerAlias || `Channel ${channel.id.slice(-8)}`}
                        </div>
                        <div className="text-xs text-gray-500">
                          {channel.active ? 'Active' : 'Inactive'}
                        </div>
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="text-sm font-medium text-yellow-300">
                        {formatSats(channel.capacity)}
                      </div>
                      <div className="text-xs text-gray-400">Capacity</div>
                    </div>
                  </div>

                  {/* Balance Visualization */}
                  <div className="space-y-2">
                    <div className="flex justify-between text-xs text-gray-400">
                      <span>Local: {formatSats(channel.localBalance)}</span>
                      <span>Remote: {formatSats(channel.remoteBalance)}</span>
                    </div>
                    <div className="w-full bg-gray-700 rounded-full h-2">
                      <div
                        className="bg-gradient-to-r from-green-500 to-yellow-500 h-2 rounded-full transition-all duration-500"
                        style={{ width: `${balanceRatio}%` }}
                      ></div>
                    </div>
                    <div className="flex justify-between text-xs">
                      <span className="text-green-400">{balanceRatio.toFixed(1)}% Local</span>
                      <span className="text-blue-400">{(100 - balanceRatio).toFixed(1)}% Remote</span>
                    </div>
                  </div>
                </motion.div>
              );
            })}
          </div>
        )}
      </div>

      {/* Quick Actions */}
      <div className="mt-6 pt-4 border-t border-gray-700/30">
        <div className="flex space-x-3">
          <button className="flex-1 bg-yellow-600/20 hover:bg-yellow-600/30 border border-yellow-600/50 rounded-lg py-2 px-4 text-sm font-medium text-yellow-300 transition-colors">
            Create Invoice
          </button>
          <button className="flex-1 bg-blue-600/20 hover:bg-blue-600/30 border border-blue-600/50 rounded-lg py-2 px-4 text-sm font-medium text-blue-300 transition-colors">
            Pay Invoice
          </button>
          <button className="flex-1 bg-purple-600/20 hover:bg-purple-600/30 border border-purple-600/50 rounded-lg py-2 px-4 text-sm font-medium text-purple-300 transition-colors">
            Open Channel
          </button>
        </div>
      </div>
    </motion.div>
  );
}