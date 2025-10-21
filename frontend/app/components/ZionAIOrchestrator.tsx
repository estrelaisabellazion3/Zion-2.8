'use client';

import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import Link from 'next/link';

interface OrchestratorStatus {
  total_components: number;
  active_components: number;
  components: string[];
  system_state: string;
  orchestrator_active: boolean;
}

interface CouncilStatus {
  admin: string;
  councilors: number;
  sessions_held: number;
  decisions_made: number;
  ai_integrations: number;
}

interface SystemMetrics {
  total_ai_tasks: number;
  active_components: number;
  system_performance: number;
  mining_enhancement: number;
  oracle_consensus: number;
  sacred_geometry_bonus: number;
}

export default function ZionAIOrchestrator() {
  const [orchestratorStatus, setOrchestratorStatus] = useState<OrchestratorStatus | null>(null);
  const [councilStatus, setCouncilStatus] = useState<CouncilStatus | null>(null);
  const [metrics, setMetrics] = useState<SystemMetrics | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [lastUpdate, setLastUpdate] = useState<Date>(new Date());

  useEffect(() => {
    fetchAllData();
    const interval = setInterval(fetchAllData, 10000); // Every 10 seconds
    return () => clearInterval(interval);
  }, []);

  const fetchAllData = async () => {
    try {
      setError(null);
      
      // Fetch orchestrator status
      const statusRes = await fetch('/api/orchestrator?action=status');
      const statusData = await statusRes.json();
      if (statusData.success && statusData.data) {
        setOrchestratorStatus(statusData.data);
      }

      // Fetch council status
      const councilRes = await fetch('/api/orchestrator?action=council-status');
      const councilData = await councilRes.json();
      if (councilData.success && councilData.data) {
        setCouncilStatus(councilData.data);
      }

      // Fetch metrics
      const metricsRes = await fetch('/api/orchestrator?action=metrics');
      const metricsData = await metricsRes.json();
      if (metricsData.success && metricsData.data) {
        setMetrics(metricsData.data);
      }

      setLastUpdate(new Date());
      setLoading(false);
    } catch (err) {
      console.error('Failed to fetch orchestrator data:', err);
      setError('Failed to connect to AI Orchestrator');
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
        alert('❌ Failed to start orchestration: ' + result.error);
      }
    } catch (err) {
      alert('❌ Error starting orchestration');
    }
  };

  const conveneCouncil = async () => {
    const topic = prompt('Enter council topic:');
    if (!topic) return;

    const urgency = prompt('Enter urgency (low/normal/high/critical):', 'normal');

    try {
      const response = await fetch('/api/orchestrator', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          action: 'convene_council',
          topic,
          urgency: urgency || 'normal'
        })
      });

      const result = await response.json();
      if (result.success) {
        alert(`✅ Council Decision: ${result.data.admin_decision}\n\nVotes: ${JSON.stringify(result.data.vote_counts)}`);
        fetchAllData();
      } else {
        alert('❌ Failed to convene council: ' + result.error);
      }
    } catch (err) {
      alert('❌ Error convening council');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900 flex items-center justify-center">
        <div className="text-white text-2xl">Loading AI Orchestrator...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900 text-white p-8">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-8"
      >
        <h1 className="text-5xl font-bold mb-4 text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-400">
          🧠 ZION 2.8 AI Orchestrator
        </h1>
        <p className="text-gray-400">
          Master Coordinator • AI Components • Round Table Council Integration
        </p>
        <p className="text-sm text-gray-500 mt-2">
          Last updated: {lastUpdate.toLocaleTimeString()}
        </p>
      </motion.div>

      {error && (
        <div className="mb-6 p-4 bg-red-900 bg-opacity-30 border border-red-500 rounded-lg">
          <p className="text-red-400">⚠️ {error}</p>
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

        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={conveneCouncil}
          className="py-4 px-6 bg-gradient-to-r from-yellow-500 to-orange-500 rounded-lg font-bold text-lg shadow-lg"
        >
          🏰 Convene Council
        </motion.button>

        <Link href="/round-table">
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="w-full py-4 px-6 bg-gradient-to-r from-green-500 to-teal-500 rounded-lg font-bold text-lg shadow-lg"
          >
            ⚔️ View Round Table
          </motion.button>
        </Link>
      </div>

      {/* Orchestrator Status */}
      {orchestratorStatus && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8 p-6 bg-white bg-opacity-5 rounded-lg border border-white border-opacity-20"
        >
          <h2 className="text-2xl font-bold mb-4 text-blue-400">📊 Orchestrator Status</h2>
          
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
            <div className="p-4 bg-white bg-opacity-5 rounded-lg">
              <div className="text-sm text-gray-400">System State</div>
              <div className="text-2xl font-bold text-green-400">{orchestratorStatus.system_state}</div>
            </div>
            
            <div className="p-4 bg-white bg-opacity-5 rounded-lg">
              <div className="text-sm text-gray-400">Total Components</div>
              <div className="text-2xl font-bold">{orchestratorStatus.total_components}</div>
            </div>
            
            <div className="p-4 bg-white bg-opacity-5 rounded-lg">
              <div className="text-sm text-gray-400">Active Components</div>
              <div className="text-2xl font-bold text-green-400">{orchestratorStatus.active_components}</div>
            </div>
            
            <div className="p-4 bg-white bg-opacity-5 rounded-lg">
              <div className="text-sm text-gray-400">Orchestrator</div>
              <div className="text-2xl font-bold">
                {orchestratorStatus.orchestrator_active ? '🟢 ACTIVE' : '⚪ IDLE'}
              </div>
            </div>
          </div>

          <div>
            <h3 className="text-lg font-bold mb-2 text-purple-400">Active Components:</h3>
            <div className="flex flex-wrap gap-2">
              {orchestratorStatus.components.map((comp, idx) => (
                <div
                  key={idx}
                  className="px-3 py-1 bg-purple-500 bg-opacity-20 rounded-full text-sm border border-purple-500"
                >
                  {comp}
                </div>
              ))}
            </div>
          </div>
        </motion.div>
      )}

      {/* Council Status */}
      {councilStatus && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="mb-8 p-6 bg-white bg-opacity-5 rounded-lg border border-white border-opacity-20"
        >
          <h2 className="text-2xl font-bold mb-4 text-yellow-400">🏰 Round Table Council</h2>
          
          <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
            <div className="p-4 bg-white bg-opacity-5 rounded-lg">
              <div className="text-sm text-gray-400">Admin</div>
              <div className="text-lg font-bold text-yellow-400">{councilStatus.admin}</div>
            </div>
            
            <div className="p-4 bg-white bg-opacity-5 rounded-lg">
              <div className="text-sm text-gray-400">Councilors</div>
              <div className="text-2xl font-bold">{councilStatus.councilors}/12</div>
            </div>
            
            <div className="p-4 bg-white bg-opacity-5 rounded-lg">
              <div className="text-sm text-gray-400">Sessions Held</div>
              <div className="text-2xl font-bold">{councilStatus.sessions_held}</div>
            </div>
            
            <div className="p-4 bg-white bg-opacity-5 rounded-lg">
              <div className="text-sm text-gray-400">Decisions Made</div>
              <div className="text-2xl font-bold text-green-400">{councilStatus.decisions_made}</div>
            </div>
            
            <div className="p-4 bg-white bg-opacity-5 rounded-lg">
              <div className="text-sm text-gray-400">AI Integrations</div>
              <div className="text-2xl font-bold text-blue-400">{councilStatus.ai_integrations}</div>
            </div>
          </div>
        </motion.div>
      )}

      {/* System Metrics */}
      {metrics && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="p-6 bg-white bg-opacity-5 rounded-lg border border-white border-opacity-20"
        >
          <h2 className="text-2xl font-bold mb-4 text-green-400">📈 System Metrics</h2>
          
          <div className="space-y-4">
            <div>
              <div className="flex justify-between mb-2">
                <span>System Performance</span>
                <span className="font-bold">{(metrics.system_performance * 100).toFixed(1)}%</span>
              </div>
              <div className="h-3 bg-gray-700 rounded overflow-hidden">
                <div 
                  className="h-full bg-gradient-to-r from-green-400 to-blue-400"
                  style={{ width: `${metrics.system_performance * 100}%` }}
                />
              </div>
            </div>

            <div>
              <div className="flex justify-between mb-2">
                <span>Mining Enhancement</span>
                <span className="font-bold">{(metrics.mining_enhancement * 100).toFixed(1)}%</span>
              </div>
              <div className="h-3 bg-gray-700 rounded overflow-hidden">
                <div 
                  className="h-full bg-gradient-to-r from-yellow-400 to-orange-400"
                  style={{ width: `${metrics.mining_enhancement * 100}%` }}
                />
              </div>
            </div>

            <div>
              <div className="flex justify-between mb-2">
                <span>Oracle Consensus</span>
                <span className="font-bold">{(metrics.oracle_consensus * 100).toFixed(1)}%</span>
              </div>
              <div className="h-3 bg-gray-700 rounded overflow-hidden">
                <div 
                  className="h-full bg-gradient-to-r from-purple-400 to-pink-400"
                  style={{ width: `${metrics.oracle_consensus * 100}%` }}
                />
              </div>
            </div>

            <div>
              <div className="flex justify-between mb-2">
                <span>Sacred Geometry Bonus</span>
                <span className="font-bold">{(metrics.sacred_geometry_bonus * 100).toFixed(1)}%</span>
              </div>
              <div className="h-3 bg-gray-700 rounded overflow-hidden">
                <div 
                  className="h-full bg-gradient-to-r from-cyan-400 to-teal-400"
                  style={{ width: `${metrics.sacred_geometry_bonus * 100}%` }}
                />
              </div>
            </div>

            <div className="pt-4 border-t border-gray-700">
              <div className="text-sm text-gray-400">Total AI Tasks Completed</div>
              <div className="text-3xl font-bold">{metrics.total_ai_tasks}</div>
            </div>
          </div>
        </motion.div>
      )}

      {/* Footer */}
      <div className="mt-8 text-center text-gray-500 text-sm">
        <p>ZION 2.8 AI Master Orchestrator • Integrated with Round Table Council</p>
        <p className="mt-2 text-yellow-400 font-bold">JAI RAM SITA HANUMAN - ON THE STAR! ⭐</p>
      </div>
    </div>
  );
}
