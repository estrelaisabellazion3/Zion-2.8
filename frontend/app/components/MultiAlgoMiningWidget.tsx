"use client";

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Cpu, HardDrive, Zap, TrendingUp, Settings, Play, Pause } from 'lucide-react';

interface PoolMiner {
  address: string;
  hashrate: number;
  shares: number;
  algorithm: string;
  lastSeen: number;
}

interface PoolStats {
  algorithms: string[];
  totalMiners: number;
  totalHashrate: number;
  blocksFound: number;
  currentDifficulty: number;
  miners: PoolMiner[];
}

const ALGORITHM_COLORS = {
  'randomx': { bg: 'bg-blue-900/20', border: 'border-blue-700/50', text: 'text-blue-300' },
  'yescrypt': { bg: 'bg-green-900/20', border: 'border-green-700/50', text: 'text-green-300' },
  'autolykos2': { bg: 'bg-purple-900/20', border: 'border-purple-700/50', text: 'text-purple-300' },
  'default': { bg: 'bg-gray-900/20', border: 'border-gray-700/50', text: 'text-gray-300' }
};

export default function MultiAlgoMiningWidget() {
  const [stats, setStats] = useState<PoolStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedAlgorithm, setSelectedAlgorithm] = useState<string>('all');

  useEffect(() => {
    fetchPoolData();
    const interval = setInterval(fetchPoolData, 8000); // Update every 8 seconds
    return () => clearInterval(interval);
  }, []);

  const fetchPoolData = async () => {
    try {
      setError(null);
      const response = await fetch('/api/zion-core?endpoint=pool-stats');
      const data = await response.json();
      setStats(data);
    } catch (err) {
      console.error('Pool stats fetch error:', err);
      setError(err instanceof Error ? err.message : 'Failed to load pool data');
    } finally {
      setLoading(false);
    }
  };

  const formatHashrate = (hashrate: number): string => {
    if (hashrate >= 1e12) return `${(hashrate / 1e12).toFixed(2)} TH/s`;
    if (hashrate >= 1e9) return `${(hashrate / 1e9).toFixed(2)} GH/s`;
    if (hashrate >= 1e6) return `${(hashrate / 1e6).toFixed(2)} MH/s`;
    if (hashrate >= 1e3) return `${(hashrate / 1e3).toFixed(2)} KH/s`;
    return `${hashrate.toFixed(2)} H/s`;
  };

  const getAlgorithmColor = (algorithm: string) => {
    return ALGORITHM_COLORS[algorithm as keyof typeof ALGORITHM_COLORS] || ALGORITHM_COLORS.default;
  };

  const filteredMiners = stats?.miners?.filter(miner =>
    selectedAlgorithm === 'all' || miner.algorithm === selectedAlgorithm
  ) || [];

  const algorithmStats = stats?.algorithms?.map(algo => {
    const algoMiners = stats.miners?.filter(m => m.algorithm === algo) || [];
    const algoHashrate = algoMiners.reduce((sum, m) => sum + m.hashrate, 0);
    return { algorithm: algo, miners: algoMiners.length, hashrate: algoHashrate };
  }) || [];

  if (loading) {
    return (
      <div className="bg-gradient-to-br from-green-900/20 to-teal-900/20 border border-green-700/30 rounded-xl p-6">
        <div className="animate-pulse">
          <div className="h-6 bg-green-800/50 rounded mb-4"></div>
          <div className="space-y-3">
            <div className="h-4 bg-green-800/30 rounded"></div>
            <div className="h-4 bg-green-800/30 rounded"></div>
            <div className="h-4 bg-green-800/30 rounded"></div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <motion.div
      className="bg-gradient-to-br from-green-900/20 to-teal-900/20 border border-green-700/30 rounded-xl p-6"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
    >
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-xl font-semibold flex items-center">
          <Cpu className="w-6 h-6 mr-2 text-green-400" />
          Multi-Algorithm Pool
        </h3>
        <div className="flex items-center space-x-2">
          <div className="w-2 h-2 rounded-full bg-green-400"></div>
          <span className="text-sm text-gray-400">Active</span>
        </div>
      </div>

      {error && (
        <div className="mb-4 p-3 bg-red-900/20 border border-red-700 rounded-lg">
          <p className="text-red-300 text-sm">⚠️ {error}</p>
        </div>
      )}

      {/* Pool Overview */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <div className="text-center">
          <div className="text-2xl font-bold text-green-300">{stats?.totalMiners || 0}</div>
          <div className="text-sm text-gray-400">Total Miners</div>
        </div>
        <div className="text-center">
          <div className="text-2xl font-bold text-blue-300">{formatHashrate(stats?.totalHashrate || 0)}</div>
          <div className="text-sm text-gray-400">Pool Hashrate</div>
        </div>
        <div className="text-center">
          <div className="text-2xl font-bold text-purple-300">{stats?.blocksFound || 0}</div>
          <div className="text-sm text-gray-400">Blocks Found</div>
        </div>
        <div className="text-center">
          <div className="text-2xl font-bold text-yellow-300">{stats?.currentDifficulty || 0}</div>
          <div className="text-sm text-gray-400">Difficulty</div>
        </div>
      </div>

      {/* Algorithm Filter */}
      <div className="mb-4">
        <div className="flex flex-wrap gap-2">
          <button
            onClick={() => setSelectedAlgorithm('all')}
            className={`px-3 py-1 rounded-full text-sm font-medium transition-colors ${
              selectedAlgorithm === 'all'
                ? 'bg-green-600 text-white'
                : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
            }`}
          >
            All Algorithms
          </button>
          {stats?.algorithms?.map((algo) => (
            <button
              key={algo}
              onClick={() => setSelectedAlgorithm(algo)}
              className={`px-3 py-1 rounded-full text-sm font-medium transition-colors ${
                selectedAlgorithm === algo
                  ? 'bg-green-600 text-white'
                  : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
              }`}
            >
              {algo.toUpperCase()}
            </button>
          ))}
        </div>
      </div>

      {/* Algorithm Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        {algorithmStats.map((stat) => {
          const colors = getAlgorithmColor(stat.algorithm);
          return (
            <div key={stat.algorithm} className={`p-4 ${colors.bg} border ${colors.border} rounded-lg`}>
              <div className="flex items-center justify-between mb-2">
                <span className={`text-sm font-medium ${colors.text}`}>
                  {stat.algorithm.toUpperCase()}
                </span>
                <TrendingUp className="w-4 h-4 text-gray-400" />
              </div>
              <div className="space-y-1">
                <div className="flex justify-between text-sm">
                  <span className="text-gray-400">Miners:</span>
                  <span className="text-white font-medium">{stat.miners}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-400">Hashrate:</span>
                  <span className="text-white font-medium">{formatHashrate(stat.hashrate)}</span>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Miners List */}
      <div className="space-y-3">
        <h4 className="text-lg font-semibold text-gray-300 mb-3 flex items-center">
          <HardDrive className="w-5 h-5 mr-2" />
          Active Miners ({filteredMiners.length})
        </h4>
        {filteredMiners.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            <Cpu className="w-12 h-12 mx-auto mb-2 opacity-50" />
            <p>No miners found</p>
          </div>
        ) : (
          <div className="space-y-2 max-h-80 overflow-y-auto">
            {filteredMiners.map((miner, index) => {
              const colors = getAlgorithmColor(miner.algorithm);
              const isOnline = Date.now() - miner.lastSeen < 300000; // 5 minutes

              return (
                <motion.div
                  key={miner.address}
                  className={`p-3 ${colors.bg} border ${colors.border} rounded-lg`}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.05 }}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <div className={`w-3 h-3 rounded-full ${isOnline ? 'bg-green-400' : 'bg-red-400'}`}></div>
                      <div>
                        <div className="text-sm font-medium text-gray-300">
                          {miner.address.slice(0, 16)}...
                        </div>
                        <div className={`text-xs ${colors.text}`}>
                          {miner.algorithm.toUpperCase()}
                        </div>
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="text-sm font-medium text-white">
                        {formatHashrate(miner.hashrate)}
                      </div>
                      <div className="text-xs text-gray-400">
                        {miner.shares} shares
                      </div>
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
          <button className="flex-1 bg-green-600/20 hover:bg-green-600/30 border border-green-600/50 rounded-lg py-2 px-4 text-sm font-medium text-green-300 transition-colors flex items-center justify-center">
            <Play className="w-4 h-4 mr-2" />
            Start Mining
          </button>
          <button className="flex-1 bg-red-600/20 hover:bg-red-600/30 border border-red-600/50 rounded-lg py-2 px-4 text-sm font-medium text-red-300 transition-colors flex items-center justify-center">
            <Pause className="w-4 h-4 mr-2" />
            Stop Mining
          </button>
          <button className="flex-1 bg-blue-600/20 hover:bg-blue-600/30 border border-blue-600/50 rounded-lg py-2 px-4 text-sm font-medium text-blue-300 transition-colors flex items-center justify-center">
            <Settings className="w-4 h-4 mr-2" />
            Configure
          </button>
        </div>
      </div>
    </motion.div>
  );
}