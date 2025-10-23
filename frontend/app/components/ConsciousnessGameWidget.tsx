"use client";

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Brain, Trophy, Star, Target, Zap } from 'lucide-react';

interface ConsciousnessMiner {
  address: string;
  level: string;
  xp: number;
  achievements: number;
}

interface ConsciousnessStats {
  miners: ConsciousnessMiner[];
  leaderboard: Array<{ rank: number; address: string; xp: number }>;
  achievements: Array<{ id: string; name: string; description: string; unlocked: boolean }>;
  totalMiners: number;
  totalXP: number;
  activeLevel: string;
}

const LEVELS = {
  'AWAKENING': { color: 'text-blue-400', bg: 'bg-blue-900/20', border: 'border-blue-700/50' },
  'MENTAL': { color: 'text-purple-400', bg: 'bg-purple-900/20', border: 'border-purple-700/50' },
  'SPIRITUAL': { color: 'text-green-400', bg: 'bg-green-900/20', border: 'border-green-700/50' },
  'COSMIC': { color: 'text-yellow-400', bg: 'bg-yellow-900/20', border: 'border-yellow-700/50' },
  'ENLIGHTENED': { color: 'text-red-400', bg: 'bg-red-900/20', border: 'border-red-700/50' }
};

export default function ConsciousnessGameWidget() {
  const [stats, setStats] = useState<ConsciousnessStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedTab, setSelectedTab] = useState<'miners' | 'leaderboard' | 'achievements'>('miners');

  useEffect(() => {
    fetchConsciousnessData();
    const interval = setInterval(fetchConsciousnessData, 15000); // Update every 15 seconds
    return () => clearInterval(interval);
  }, []);

  const fetchConsciousnessData = async () => {
    try {
      setError(null);
      const response = await fetch('/api/zion-core?endpoint=consciousness-status');
      const data = await response.json();
      setStats(data);
    } catch (err) {
      console.error('Consciousness Game fetch error:', err);
      setError(err instanceof Error ? err.message : 'Failed to load consciousness data');
    } finally {
      setLoading(false);
    }
  };

  const formatXP = (xp: number): string => {
    if (xp >= 1000000) return `${(xp / 1000000).toFixed(1)}M`;
    if (xp >= 1000) return `${(xp / 1000).toFixed(1)}K`;
    return xp.toString();
  };

  const getLevelInfo = (level: string) => {
    return LEVELS[level as keyof typeof LEVELS] || LEVELS.AWAKENING;
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
          <Brain className="w-6 h-6 mr-2 text-purple-400" />
          Consciousness Mining
        </h3>
        <div className="flex items-center space-x-2">
          <div className="text-sm text-gray-400">
            Level: <span className={`font-semibold ${getLevelInfo(stats?.activeLevel || 'AWAKENING').color}`}>
              {stats?.activeLevel || 'AWAKENING'}
            </span>
          </div>
        </div>
      </div>

      {error && (
        <div className="mb-4 p-3 bg-red-900/20 border border-red-700 rounded-lg">
          <p className="text-red-300 text-sm">⚠️ {error}</p>
        </div>
      )}

      {/* Stats Overview */}
      <div className="grid grid-cols-3 gap-4 mb-6">
        <div className="text-center">
          <div className="text-2xl font-bold text-purple-300">{stats?.totalMiners || 0}</div>
          <div className="text-sm text-gray-400">Active Miners</div>
        </div>
        <div className="text-center">
          <div className="text-2xl font-bold text-blue-300">{formatXP(stats?.totalXP || 0)}</div>
          <div className="text-sm text-gray-400">Total XP</div>
        </div>
        <div className="text-center">
          <div className="text-2xl font-bold text-green-300">{stats?.achievements?.filter(a => a.unlocked).length || 0}</div>
          <div className="text-sm text-gray-400">Achievements</div>
        </div>
      </div>

      {/* Tab Navigation */}
      <div className="flex space-x-1 mb-4 bg-gray-800/30 rounded-lg p-1">
        {[
          { id: 'miners', label: 'Miners', icon: Brain },
          { id: 'leaderboard', label: 'Leaderboard', icon: Trophy },
          { id: 'achievements', label: 'Achievements', icon: Star }
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setSelectedTab(tab.id as any)}
            className={`flex-1 flex items-center justify-center space-x-2 py-2 px-3 rounded-md text-sm font-medium transition-colors ${
              selectedTab === tab.id
                ? 'bg-purple-600 text-white'
                : 'text-gray-400 hover:text-white hover:bg-gray-700/50'
            }`}
          >
            <tab.icon className="w-4 h-4" />
            <span>{tab.label}</span>
          </button>
        ))}
      </div>

      {/* Tab Content */}
      <div className="min-h-[300px]">
        {selectedTab === 'miners' && (
          <div className="space-y-3">
            {stats?.miners?.map((miner, index) => {
              const levelInfo = getLevelInfo(miner.level);
              return (
                <motion.div
                  key={miner.address}
                  className={`p-4 ${levelInfo.bg} border ${levelInfo.border} rounded-lg`}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.1 }}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <div className={`w-3 h-3 rounded-full ${levelInfo.color.replace('text-', 'bg-')}`}></div>
                      <div>
                        <div className="text-sm font-medium text-gray-300">
                          {miner.address.slice(0, 12)}...
                        </div>
                        <div className={`text-xs ${levelInfo.color}`}>
                          {miner.level} Level
                        </div>
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="text-lg font-bold text-white">{formatXP(miner.xp)} XP</div>
                      <div className="text-xs text-gray-400">{miner.achievements} achievements</div>
                    </div>
                  </div>
                </motion.div>
              );
            }) || (
              <div className="text-center py-8 text-gray-500">
                <Brain className="w-12 h-12 mx-auto mb-2 opacity-50" />
                <p>No miners found</p>
              </div>
            )}
          </div>
        )}

        {selectedTab === 'leaderboard' && (
          <div className="space-y-2">
            {stats?.leaderboard?.map((entry, index) => (
              <motion.div
                key={entry.address}
                className="flex items-center justify-between p-3 bg-gray-800/30 rounded-lg border border-gray-700/30"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.05 }}
              >
                <div className="flex items-center space-x-3">
                  <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold ${
                    index === 0 ? 'bg-yellow-500 text-black' :
                    index === 1 ? 'bg-gray-400 text-black' :
                    index === 2 ? 'bg-orange-600 text-white' :
                    'bg-gray-700 text-white'
                  }`}>
                    {index + 1}
                  </div>
                  <div>
                    <div className="text-sm font-medium text-gray-300">
                      {entry.address.slice(0, 16)}...
                    </div>
                  </div>
                </div>
                <div className="text-lg font-bold text-purple-300">
                  {formatXP(entry.xp)} XP
                </div>
              </motion.div>
            )) || (
              <div className="text-center py-8 text-gray-500">
                <Trophy className="w-12 h-12 mx-auto mb-2 opacity-50" />
                <p>No leaderboard data</p>
              </div>
            )}
          </div>
        )}

        {selectedTab === 'achievements' && (
          <div className="grid grid-cols-1 gap-3">
            {stats?.achievements?.map((achievement, index) => (
              <motion.div
                key={achievement.id}
                className={`p-4 border rounded-lg ${
                  achievement.unlocked
                    ? 'bg-green-900/20 border-green-700/50'
                    : 'bg-gray-800/30 border-gray-700/30'
                }`}
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: index * 0.05 }}
              >
                <div className="flex items-center space-x-3">
                  <div className={`p-2 rounded-full ${
                    achievement.unlocked ? 'bg-green-600' : 'bg-gray-600'
                  }`}>
                    {achievement.unlocked ? (
                      <Star className="w-4 h-4 text-white" />
                    ) : (
                      <Target className="w-4 h-4 text-gray-400" />
                    )}
                  </div>
                  <div className="flex-1">
                    <div className={`font-medium ${achievement.unlocked ? 'text-green-300' : 'text-gray-400'}`}>
                      {achievement.name}
                    </div>
                    <div className="text-sm text-gray-500">
                      {achievement.description}
                    </div>
                  </div>
                  {achievement.unlocked && (
                    <Zap className="w-5 h-5 text-green-400" />
                  )}
                </div>
              </motion.div>
            )) || (
              <div className="text-center py-8 text-gray-500">
                <Star className="w-12 h-12 mx-auto mb-2 opacity-50" />
                <p>No achievements available</p>
              </div>
            )}
          </div>
        )}
      </div>
    </motion.div>
  );
}