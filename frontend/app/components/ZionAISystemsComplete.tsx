'use client';

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Link from 'next/link';

// ==================== INTERFACES ====================

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

interface MetricsData {
  total_ai_tasks: number;
  active_components: number;
  system_performance: number;
  mining_enhancement: number;
  oracle_consensus: number;
  sacred_geometry_bonus: number;
}

// ==================== AI SYSTEM METADATA ====================

const AI_SYSTEM_CONFIG: Record<string, { 
  icon: string; 
  color: string; 
  name: string; 
  category: string;
  description: string;
}> = {
  // Core Systems
  oracle_ai: { 
    icon: '🔮', 
    color: 'from-purple-500 to-pink-500', 
    name: 'Oracle AI', 
    category: 'Core',
    description: 'Multi-source data feeds & sacred validation'
  },
  cosmic_analyzer: { 
    icon: '🌌', 
    color: 'from-blue-500 to-cyan-500', 
    name: 'Cosmic Analyzer', 
    category: 'Core',
    description: 'Advanced image processing & cosmic patterns'
  },
  ai_afterburner: { 
    icon: '🚀', 
    color: 'from-orange-500 to-red-500', 
    name: 'AI Afterburner', 
    category: 'Core',
    description: 'Performance optimization & boost systems'
  },
  
  // Advanced Systems
  quantum_ai: { 
    icon: '⚛️', 
    color: 'from-indigo-500 to-purple-500', 
    name: 'Quantum AI', 
    category: 'Advanced',
    description: 'Quantum computing integration'
  },
  gaming_ai: { 
    icon: '🎮', 
    color: 'from-green-500 to-teal-500', 
    name: 'Gaming AI', 
    category: 'Advanced',
    description: 'Gaming & Metaverse intelligence'
  },
  lightning_ai: { 
    icon: '⚡', 
    color: 'from-yellow-500 to-amber-500', 
    name: 'Lightning AI', 
    category: 'Advanced',
    description: 'Lightning Network optimization'
  },
  
  // Specialized Systems
  bio_ai: { 
    icon: '🧬', 
    color: 'from-emerald-500 to-green-500', 
    name: 'Bio AI', 
    category: 'Specialized',
    description: 'Biological data analysis'
  },
  music_ai: { 
    icon: '🎵', 
    color: 'from-pink-500 to-rose-500', 
    name: 'Music AI', 
    category: 'Specialized',
    description: 'Music generation & analysis'
  },
  trading_bot: { 
    icon: '📈', 
    color: 'from-cyan-500 to-blue-500', 
    name: 'Trading Bot', 
    category: 'Specialized',
    description: 'Automated trading strategies'
  },
  blockchain_analytics: { 
    icon: '📊', 
    color: 'from-violet-500 to-purple-500', 
    name: 'Blockchain Analytics', 
    category: 'Specialized',
    description: 'On-chain data analysis'
  },
  security_monitor: { 
    icon: '🛡️', 
    color: 'from-red-500 to-orange-500', 
    name: 'Security Monitor', 
    category: 'Specialized',
    description: 'Real-time security monitoring'
  },
  cosmic_ai: { 
    icon: '✨', 
    color: 'from-blue-400 to-indigo-400', 
    name: 'Cosmic AI', 
    category: 'Specialized',
    description: 'Cosmic data integration'
  },
  
  // Mining System
  universal_miner: { 
    icon: '⛏️', 
    color: 'from-amber-500 to-yellow-500', 
    name: 'Universal Miner', 
    category: 'Mining',
    description: 'CPU + GPU + Hybrid mining with AI optimization'
  },
};

// ==================== MAIN COMPONENT ====================

export default function ZionAISystemsComplete() {
  // State Management
  const [orchestratorData, setOrchestratorData] = useState<OrchestratorData | null>(null);
  const [councilData, setCouncilData] = useState<CouncilData | null>(null);
  const [metricsData, setMetricsData] = useState<MetricsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedCategory, setSelectedCategory] = useState<string>('All');
  const [selectedSystem, setSelectedSystem] = useState<string | null>(null);
  const [lastUpdate, setLastUpdate] = useState<Date>(new Date());

  // Data Fetching
  useEffect(() => {
    fetchAllData();
    const interval = setInterval(fetchAllData, 10000); // Every 10 seconds
    return () => clearInterval(interval);
  }, []);

  const fetchAllData = async () => {
    try {
      setError(null);
      
      // Fetch orchestrator components
      const orchRes = await fetch('/api/orchestrator?action=components');
      const orchData = await orchRes.json();
      if (orchData.success && orchData.data && orchData.data.components) {
        setOrchestratorData(orchData.data);
      } else {
        console.warn('Invalid orchestrator data:', orchData);
        setError('Invalid data from orchestrator API');
      }

      // Fetch council status
      const councilRes = await fetch('/api/orchestrator?action=council-status');
      const councilJson = await councilRes.json();
      if (councilJson.success) {
        setCouncilData(councilJson.data);
      }

      // Fetch metrics
      const metricsRes = await fetch('/api/orchestrator?action=metrics');
      const metricsJson = await metricsRes.json();
      if (metricsJson.success) {
        setMetricsData(metricsJson.data);
      }

      setLastUpdate(new Date());
      setLoading(false);
    } catch (err) {
      console.error('Failed to fetch data:', err);
      setError('Backend connection failed - Check if Flask server is running on port 8001');
      setLoading(false);
    }
  };

  // Actions
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
        alert('✅ AI Orchestration started successfully!');
        fetchAllData();
      } else {
        alert('❌ Failed to start: ' + result.error);
      }
    } catch (err) {
      alert('❌ Error starting orchestration');
    }
  };

  const conveneCouncil = async () => {
    const topic = prompt('Enter council topic for decision:');
    if (!topic) return;

    try {
      const response = await fetch('/api/orchestrator', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          action: 'convene_council',
          topic,
          urgency: 'normal'
        })
      });

      const result = await response.json();
      if (result.success) {
        alert(`✅ Council Decision: ${result.data.admin_decision}\n\nVotes: ${JSON.stringify(result.data.vote_counts)}`);
        fetchAllData();
      } else {
        alert('❌ Failed: ' + result.error);
      }
    } catch (err) {
      alert('❌ Error convening council');
    }
  };

  // Loading State
  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900 flex items-center justify-center">
        <div className="text-center">
          <div className="text-6xl mb-4 animate-pulse">🧠</div>
          <div className="text-white text-2xl">Loading AI Systems...</div>
          <div className="text-gray-400 text-sm mt-2">Connecting to orchestrator backend</div>
        </div>
      </div>
    );
  }

  // Filter Systems
  const categories = ['All', 'Core', 'Advanced', 'Specialized', 'Mining'];
  const filteredSystems = (orchestratorData && orchestratorData.components) 
    ? Object.entries(orchestratorData.components).filter(([key, _]) => {
        if (selectedCategory === 'All') return true;
        return AI_SYSTEM_CONFIG[key]?.category === selectedCategory;
      }) 
    : [];

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900 text-white">
      <div className="container mx-auto p-6">
        
        {/* ==================== HEADER ==================== */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h1 className="text-6xl font-bold mb-4 text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400">
            🧠 ZION 2.8 AI Systems
          </h1>
          <p className="text-xl text-gray-300 mb-2">
            Complete AI Orchestration Platform • {orchestratorData?.total_components || 0} AI Components Active
          </p>
          <div className="flex items-center gap-4 text-sm text-gray-400">
            <span>🕐 {lastUpdate.toLocaleTimeString()}</span>
            <span>•</span>
            <span className={error ? 'text-red-400' : 'text-green-400'}>
              {error ? '🔴 Backend Offline' : '🟢 Backend Online'}
            </span>
            {councilData && (
              <>
                <span>•</span>
                <span>🏰 {councilData.councilors} Knights</span>
              </>
            )}
          </div>
        </motion.div>

        {/* ==================== ERROR BANNER ==================== */}
        {error && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className="mb-6 p-4 bg-red-900 bg-opacity-30 border border-red-500 rounded-lg"
          >
            <p className="text-red-400 font-semibold">⚠️ {error}</p>
            <p className="text-red-300 text-sm mt-1">
              Start backend: <code className="bg-black bg-opacity-30 px-2 py-1 rounded">python3 ai_orchestrator_backend.py</code>
            </p>
          </motion.div>
        )}

        {/* ==================== STATS OVERVIEW ==================== */}
        {orchestratorData && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
            <StatsCard
              title="Total AI Systems"
              value={orchestratorData.total_components || 0}
              color="text-blue-400"
              icon="🤖"
            />
            <StatsCard
              title="Active Components"
              value={orchestratorData.active_components || 0}
              color="text-green-400"
              icon="✅"
            />
            <StatsCard
              title="System State"
              value={(orchestratorData.system_state || 'initializing').toUpperCase()}
              color="text-purple-400"
              icon="⚡"
              isText
            />
            {councilData && (
              <StatsCard
                title="Round Table Council"
                value={`${councilData.councilors || 0} Knights`}
                color="text-yellow-400"
                icon="⚔️"
                isText
              />
            )}
          </div>
        )}

        {/* ==================== ACTION BUTTONS ==================== */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
          <ActionButton
            onClick={startOrchestration}
            gradient="from-blue-500 to-purple-500"
            icon="🚀"
            text="Start Orchestration"
          />
          <ActionButton
            onClick={conveneCouncil}
            gradient="from-yellow-500 to-orange-500"
            icon="🏰"
            text="Convene Council"
          />
          <Link href="/round-table">
            <ActionButton
              gradient="from-green-500 to-teal-500"
              icon="⚔️"
              text="View Round Table"
            />
          </Link>
        </div>

        {/* ==================== METRICS DISPLAY ==================== */}
        {metricsData && (
          <div className="mb-8 p-6 bg-white bg-opacity-5 rounded-lg backdrop-blur-md border border-white border-opacity-20">
            <h2 className="text-2xl font-bold mb-4 text-green-400">📈 System Metrics</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <MetricBar
                label="System Performance"
                value={metricsData.system_performance}
                color="from-green-400 to-blue-400"
              />
              <MetricBar
                label="Mining Enhancement"
                value={metricsData.mining_enhancement}
                color="from-yellow-400 to-orange-400"
              />
              <MetricBar
                label="Oracle Consensus"
                value={metricsData.oracle_consensus}
                color="from-purple-400 to-pink-400"
              />
            </div>
          </div>
        )}

        {/* ==================== CATEGORY FILTER ==================== */}
        <div className="flex gap-2 mb-6 overflow-x-auto pb-2">
          {categories.map((category) => (
            <CategoryButton
              key={category}
              category={category}
              isSelected={selectedCategory === category}
              onClick={() => setSelectedCategory(category)}
            />
          ))}
        </div>

        {/* ==================== AI SYSTEMS GRID ==================== */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 mb-12">
          <AnimatePresence>
            {filteredSystems.map(([key, system]) => {
              const config = AI_SYSTEM_CONFIG[key] || { 
                icon: '🤖', 
                color: 'from-gray-500 to-gray-600', 
                name: key, 
                category: 'Unknown',
                description: 'AI System'
              };
              
              return (
                <AISystemCard
                  key={key}
                  systemKey={key}
                  system={system}
                  config={config}
                  isSelected={selectedSystem === key}
                  onClick={() => setSelectedSystem(selectedSystem === key ? null : key)}
                />
              );
            })}
          </AnimatePresence>
        </div>

        {/* ==================== FOOTER ==================== */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
          className="text-center mt-12 pb-8"
        >
          <p className="text-gray-500 text-sm mb-2">
            ZION 2.8 Complete AI Orchestration System
          </p>
          <p className="text-gray-600 text-xs mb-3">
            Flask Backend • Next.js Frontend • Real-time Monitoring
          </p>
          <p className="text-yellow-400 font-bold text-lg">
            JAI RAM SITA HANUMAN - ON THE STAR! ⭐
          </p>
        </motion.div>
      </div>
    </div>
  );
}

// ==================== SUB-COMPONENTS ====================

function StatsCard({ title, value, color, icon, isText = false }: { 
  title: string; 
  value: number | string; 
  color: string; 
  icon: string;
  isText?: boolean;
}) {
  return (
    <motion.div
      whileHover={{ scale: 1.05 }}
      className="p-6 bg-white bg-opacity-10 rounded-lg backdrop-blur-md border border-white border-opacity-20"
    >
      <div className="flex items-center justify-between mb-2">
        <div className="text-sm text-gray-400">{title}</div>
        <div className="text-2xl">{icon}</div>
      </div>
      <div className={`${isText ? 'text-2xl' : 'text-4xl'} font-bold ${color}`}>
        {value}
      </div>
    </motion.div>
  );
}

function ActionButton({ onClick, gradient, icon, text }: {
  onClick?: () => void;
  gradient: string;
  icon: string;
  text: string;
}) {
  return (
    <motion.button
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      onClick={onClick}
      className={`w-full py-4 px-6 bg-gradient-to-r ${gradient} rounded-lg font-bold text-lg shadow-lg hover:shadow-xl transition-shadow`}
    >
      {icon} {text}
    </motion.button>
  );
}

function MetricBar({ label, value, color }: {
  label: string;
  value: number;
  color: string;
}) {
  return (
    <div>
      <div className="flex justify-between mb-2">
        <span className="text-sm text-gray-300">{label}</span>
        <span className="text-sm font-bold text-white">{(value * 100).toFixed(1)}%</span>
      </div>
      <div className="h-3 bg-gray-700 rounded-full overflow-hidden">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${value * 100}%` }}
          transition={{ duration: 1, ease: "easeOut" }}
          className={`h-full bg-gradient-to-r ${color}`}
        />
      </div>
    </div>
  );
}

function CategoryButton({ category, isSelected, onClick }: {
  category: string;
  isSelected: boolean;
  onClick: () => void;
}) {
  return (
    <motion.button
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      onClick={onClick}
      className={`px-4 py-2 rounded-lg font-semibold transition-all ${
        isSelected
          ? 'bg-gradient-to-r from-blue-500 to-purple-500 text-white'
          : 'bg-white bg-opacity-10 text-gray-300 hover:bg-opacity-20'
      }`}
    >
      {category}
    </motion.button>
  );
}

function AISystemCard({ systemKey, system, config, isSelected, onClick }: {
  systemKey: string;
  system: AISystem;
  config: typeof AI_SYSTEM_CONFIG[string];
  isSelected: boolean;
  onClick: () => void;
}) {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.9 }}
      whileHover={{ scale: 1.05, y: -5 }}
      onClick={onClick}
      className={`relative overflow-hidden rounded-xl bg-white bg-opacity-5 backdrop-blur-md border-2 p-6 cursor-pointer group transition-all ${
        isSelected 
          ? 'border-blue-400 shadow-lg shadow-blue-500/50' 
          : 'border-white border-opacity-20 hover:border-opacity-40'
      }`}
    >
      {/* Active Indicator */}
      {system.active && (
        <div className="absolute top-3 right-3">
          <div className="w-3 h-3 bg-green-400 rounded-full animate-pulse"></div>
        </div>
      )}
      
      {/* Icon */}
      <div className={`text-6xl mb-4 bg-gradient-to-br ${config.color} bg-clip-text text-transparent filter drop-shadow-lg`}>
        {config.icon}
      </div>
      
      {/* Name */}
      <h3 className="text-xl font-bold mb-2 group-hover:text-transparent group-hover:bg-clip-text group-hover:bg-gradient-to-r group-hover:from-blue-400 group-hover:to-purple-400 transition-all">
        {config.name}
      </h3>
      
      {/* Category Badge */}
      <div className="inline-block px-3 py-1 rounded-full bg-white bg-opacity-10 text-xs font-semibold mb-3">
        {config.category}
      </div>
      
      {/* Description (shown when selected) */}
      {isSelected && (
        <motion.p
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: 'auto' }}
          exit={{ opacity: 0, height: 0 }}
          className="text-sm text-gray-300 mb-3"
        >
          {config.description}
        </motion.p>
      )}
      
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
            className={`h-full bg-gradient-to-r ${config.color}`}
          />
        </div>
      </div>
      
      {/* Hover Glow Effect */}
      <div className={`absolute inset-0 bg-gradient-to-br ${config.color} opacity-0 group-hover:opacity-10 transition-opacity pointer-events-none`}></div>
    </motion.div>
  );
}
