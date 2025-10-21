'use client';

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Link from 'next/link';

// AI System Interface
interface AISystem {
  type: string;
  active: boolean;
  performance_score: number;
}

interface OrchestratorData {
  total_components: number;
  active_components: number;
  components: Record<string, AISystem>;
  system_state: string;
  orchestrator_active: boolean;
}

interface CouncilData {
  admin: string;
  councilors: number;
  sessions_held: number;
  decisions_made: number;
  ai_integrations: number;
  initialized: boolean;
}

// AI System Icons & Colors
const AI_SYSTEM_INFO: Record<string, { icon: string; color: string; name: string; category: string }> = {
  oracle_ai: { icon: '🔮', color: 'from-purple-500 to-pink-500', name: 'Oracle AI', category: 'Core' },
  cosmic_analyzer: { icon: '🌌', color: 'from-blue-500 to-cyan-500', name: 'Cosmic Analyzer', category: 'Core' },
  ai_afterburner: { icon: '🚀', color: 'from-orange-500 to-red-500', name: 'AI Afterburner', category: 'Core' },
  
  quantum_ai: { icon: '⚛️', color: 'from-indigo-500 to-purple-500', name: 'Quantum AI', category: 'Advanced' },
  gaming_ai: { icon: '🎮', color: 'from-green-500 to-teal-500', name: 'Gaming AI', category: 'Advanced' },
  lightning_ai: { icon: '⚡', color: 'from-yellow-500 to-amber-500', name: 'Lightning AI', category: 'Advanced' },
  
  bio_ai: { icon: '🧬', color: 'from-emerald-500 to-green-500', name: 'Bio AI', category: 'Specialized' },
  music_ai: { icon: '🎵', color: 'from-pink-500 to-rose-500', name: 'Music AI', category: 'Specialized' },
  trading_bot: { icon: '📈', color: 'from-cyan-500 to-blue-500', name: 'Trading Bot', category: 'Specialized' },
  blockchain_analytics: { icon: '📊', color: 'from-violet-500 to-purple-500', name: 'Blockchain Analytics', category: 'Specialized' },
  security_monitor: { icon: '🛡️', color: 'from-red-500 to-orange-500', name: 'Security Monitor', category: 'Specialized' },
  cosmic_ai: { icon: '✨', color: 'from-blue-400 to-indigo-400', name: 'Cosmic AI', category: 'Specialized' },
  
  universal_miner: { icon: '⛏️', color: 'from-amber-500 to-yellow-500', name: 'Universal Miner', category: 'Mining' },
};

export default function ZionAISystemsPage() {
  const [orchestratorData, setOrchestratorData] = useState<OrchestratorData | null>(null);
  const [councilData, setCouncilData] = useState<CouncilData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedCategory, setSelectedCategory] = useState<string>('All');
  const [lastUpdate, setLastUpdate] = useState<Date>(new Date());

  useEffect(() => {
    fetchAllData();
    const interval = setInterval(fetchAllData, 10000);
    return () => clearInterval(interval);
  }, []);

  const fetchAllData = async () => {
    try {
      setError(null);
      
      // Fetch orchestrator data
      const orchRes = await fetch('/api/orchestrator?action=components');
      const orchData = await orchRes.json();
      if (orchData.success) {
        setOrchestratorData(orchData.data);
      }

      // Fetch council data
      const councilRes = await fetch('/api/orchestrator?action=council-status');
      const councilJson = await councilRes.json();
      if (councilJson.success) {
        setCouncilData(councilJson.data);
      }

      setLastUpdate(new Date());
      setLoading(false);
    } catch (err) {
      console.error('Failed to fetch data:', err);
      setError('Failed to connect to AI backend');
      setLoading(false);
    }
  };

  const startOrchestration = async () => {
    try {
      const response = await fetch('/api/orchestrator', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          action: 'start_orchestration',
          mining_enhancement: true,
          oracle_feeds: true,
          sacred_enhancement: true
        })
      });

      const result = await response.json();
      if (result.success) {
        alert('✅ Orchestration started successfully!');
        fetchAllData();
      } else {
        alert('❌ Failed: ' + result.error);
      }
    } catch (err) {
      alert('❌ Error starting orchestration');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900 flex items-center justify-center">
        <div className="text-white text-2xl">🔄 Loading AI Systems...</div>
      </div>
    );
  }

  const categories = ['All', 'Core', 'Advanced', 'Specialized', 'Mining'];
  
  const filteredSystems = orchestratorData ? Object.entries(orchestratorData.components).filter(([key, _]) => {
    if (selectedCategory === 'All') return true;
    return AI_SYSTEM_INFO[key]?.category === selectedCategory;
  }) : [];

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900 text-white p-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-8"
      >
        <h1 className="text-6xl font-bold mb-4 text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400">
          🧠 ZION 2.8 AI Systems
        </h1>
        <p className="text-xl text-gray-300">
          Complete AI Orchestration System • 13 AI Components • Round Table Council
        </p>
        <p className="text-sm text-gray-500 mt-2">
          Last updated: {lastUpdate.toLocaleTimeString()} • Backend: {error ? '🔴 Offline' : '🟢 Online'}
        </p>
      </motion.div>

      {error && (
        <div className="mb-6 p-4 bg-red-900 bg-opacity-30 border border-red-500 rounded-lg">
          <p className="text-red-400">⚠️ {error}</p>
        </div>
      )}

      {/* Stats Overview */}
      {orchestratorData && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <motion.div
            whileHover={{ scale: 1.05 }}
            className="p-6 bg-white bg-opacity-10 rounded-lg backdrop-blur-md border border-white border-opacity-20"
          >
            <div className="text-sm text-gray-400">Total AI Systems</div>
            <div className="text-4xl font-bold text-blue-400">{orchestratorData.total_components}</div>
          </motion.div>
          
          <motion.div
            whileHover={{ scale: 1.05 }}
            className="p-6 bg-white bg-opacity-10 rounded-lg backdrop-blur-md border border-white border-opacity-20"
          >
            <div className="text-sm text-gray-400">Active Components</div>
            <div className="text-4xl font-bold text-green-400">{orchestratorData.active_components}</div>
          </motion.div>
          
          <motion.div
            whileHover={{ scale: 1.05 }}
            className="p-6 bg-white bg-opacity-10 rounded-lg backdrop-blur-md border border-white border-opacity-20"
          >
            <div className="text-sm text-gray-400">System State</div>
            <div className="text-2xl font-bold text-purple-400">{orchestratorData.system_state}</div>
          </motion.div>
          
          {councilData && (
            <motion.div
              whileHover={{ scale: 1.05 }}
              className="p-6 bg-white bg-opacity-10 rounded-lg backdrop-blur-md border border-white border-opacity-20"
            >
              <div className="text-sm text-gray-400">Round Table</div>
              <div className="text-2xl font-bold text-yellow-400">{councilData.councilors} Knights</div>
            </motion.div>
          )}
        </div>
      )}

      {/* Action Buttons */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={startOrchestration}
          className="py-4 px-6 bg-gradient-to-r from-blue-500 to-purple-500 rounded-lg font-bold text-lg shadow-lg"
        >
          🚀 Start Orchestration
        </motion.button>

        <Link href="/round-table">
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="w-full py-4 px-6 bg-gradient-to-r from-yellow-500 to-orange-500 rounded-lg font-bold text-lg shadow-lg"
          >
            ⚔️ View Round Table
          </motion.button>
        </Link>

        <Link href="/ai-orchestrator">
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="w-full py-4 px-6 bg-gradient-to-r from-green-500 to-teal-500 rounded-lg font-bold text-lg shadow-lg"
          >
            📊 Orchestrator Dashboard
          </motion.button>
        </Link>
      </div>

      {/* Category Filter */}
      <div className="flex gap-2 mb-6 overflow-x-auto pb-2">
        {categories.map((category) => (
          <motion.button
            key={category}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => setSelectedCategory(category)}
            className={`px-4 py-2 rounded-lg font-semibold transition-all ${
              selectedCategory === category
                ? 'bg-gradient-to-r from-blue-500 to-purple-500 text-white'
                : 'bg-white bg-opacity-10 text-gray-300 hover:bg-opacity-20'
            }`}
          >
            {category}
          </motion.button>
        ))}
      </div>

      {/* AI Systems Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        <AnimatePresence>
          {filteredSystems.map(([key, system]) => {
            const info = AI_SYSTEM_INFO[key] || { 
              icon: '🤖', 
              color: 'from-gray-500 to-gray-600', 
              name: key, 
              category: 'Unknown' 
            };
            
            return (
              <motion.div
                key={key}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.9 }}
                whileHover={{ scale: 1.05, y: -5 }}
                className="relative overflow-hidden rounded-xl bg-white bg-opacity-5 backdrop-blur-md border border-white border-opacity-20 p-6 cursor-pointer group"
              >
                {/* Active Indicator */}
                {system.active && (
                  <div className="absolute top-3 right-3">
                    <div className="w-3 h-3 bg-green-400 rounded-full animate-pulse"></div>
                  </div>
                )}
                
                {/* Icon */}
                <div className={`text-6xl mb-4 bg-gradient-to-br ${info.color} bg-clip-text text-transparent filter drop-shadow-lg`}>
                  {info.icon}
                </div>
                
                {/* Name */}
                <h3 className="text-xl font-bold mb-2 group-hover:text-transparent group-hover:bg-clip-text group-hover:bg-gradient-to-r group-hover:from-blue-400 group-hover:to-purple-400 transition-all">
                  {info.name}
                </h3>
                
                {/* Category Badge */}
                <div className="inline-block px-3 py-1 rounded-full bg-white bg-opacity-10 text-xs font-semibold mb-3">
                  {info.category}
                </div>
                
                {/* Status */}
                <div className="flex items-center gap-2 mb-2">
                  <div className={`w-2 h-2 rounded-full ${system.active ? 'bg-green-400' : 'bg-gray-500'}`}></div>
                  <span className="text-sm text-gray-400">
                    {system.active ? 'Active' : 'Inactive'}
                  </span>
                </div>
                
                {/* Performance Score */}
                <div className="mt-4">
                  <div className="text-xs text-gray-400 mb-1">Performance</div>
                  <div className="h-2 bg-gray-700 rounded-full overflow-hidden">
                    <motion.div
                      initial={{ width: 0 }}
                      animate={{ width: `${(system.performance_score || 0) * 100}%` }}
                      transition={{ duration: 1, delay: 0.2 }}
                      className={`h-full bg-gradient-to-r ${info.color}`}
                    />
                  </div>
                </div>
                
                {/* Hover Glow Effect */}
                <div className={`absolute inset-0 bg-gradient-to-br ${info.color} opacity-0 group-hover:opacity-10 transition-opacity pointer-events-none`}></div>
              </motion.div>
            );
          })}
        </AnimatePresence>
      </div>

      {/* Footer */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.5 }}
        className="mt-12 text-center"
      >
        <p className="text-gray-500 text-sm mb-2">
          ZION 2.8 Universal AI System • Powered by Flask + Next.js
        </p>
        <p className="text-yellow-400 font-bold text-lg">
          JAI RAM SITA HANUMAN - ON THE STAR! ⭐
        </p>
      </motion.div>
    </div>
  );
}
