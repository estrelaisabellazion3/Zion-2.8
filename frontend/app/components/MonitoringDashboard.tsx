"use client";

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Activity, AlertTriangle, CheckCircle, XCircle, TrendingUp, Server, Zap, Brain } from 'lucide-react';
import { HealthCheck, MonitoringStats, Alert } from '../types/production';

export default function MonitoringDashboard() {
  const [stats, setStats] = useState<MonitoringStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedTab, setSelectedTab] = useState<'overview' | 'components' | 'alerts'>('overview');

  useEffect(() => {
    fetchMonitoringData();
    const interval = setInterval(fetchMonitoringData, 30000); // Update every 30 seconds
    return () => clearInterval(interval);
  }, []);

  const fetchMonitoringData = async () => {
    try {
      setError(null);
      const response = await fetch('/api/zion-core?endpoint=monitoring-health');
      const data = await response.json();
      setStats(data);
    } catch (err) {
      console.error('Monitoring fetch error:', err);
      setError(err instanceof Error ? err.message : 'Failed to load monitoring data');
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'healthy': return 'text-green-400';
      case 'degraded': return 'text-yellow-400';
      case 'unhealthy': return 'text-red-400';
      case 'offline': return 'text-gray-400';
      default: return 'text-gray-400';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'healthy': return <CheckCircle className="w-5 h-5 text-green-400" />;
      case 'degraded': return <AlertTriangle className="w-5 h-5 text-yellow-400" />;
      case 'unhealthy': return <XCircle className="w-5 h-5 text-red-400" />;
      case 'offline': return <XCircle className="w-5 h-5 text-gray-400" />;
      default: return <Activity className="w-5 h-5 text-gray-400" />;
    }
  };

  const getAlertSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical': return 'text-red-400 bg-red-900/20 border-red-700/50';
      case 'error': return 'text-red-300 bg-red-900/20 border-red-700/50';
      case 'warning': return 'text-yellow-300 bg-yellow-900/20 border-yellow-700/50';
      case 'info': return 'text-blue-300 bg-blue-900/20 border-blue-700/50';
      default: return 'text-gray-300 bg-gray-900/20 border-gray-700/50';
    }
  };

  const formatUptime = (seconds: number): string => {
    const days = Math.floor(seconds / 86400);
    const hours = Math.floor((seconds % 86400) / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);

    if (days > 0) return `${days}d ${hours}h ${minutes}m`;
    if (hours > 0) return `${hours}h ${minutes}m`;
    return `${minutes}m`;
  };

  if (loading) {
    return (
      <div className="bg-gradient-to-br from-slate-900/20 to-gray-900/20 border border-slate-700/30 rounded-xl p-6">
        <div className="animate-pulse">
          <div className="h-6 bg-slate-800/50 rounded mb-4"></div>
          <div className="space-y-3">
            <div className="h-4 bg-slate-800/30 rounded"></div>
            <div className="h-4 bg-slate-800/30 rounded"></div>
            <div className="h-4 bg-slate-800/30 rounded"></div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <motion.div
      className="bg-gradient-to-br from-slate-900/20 to-gray-900/20 border border-slate-700/30 rounded-xl p-6"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
    >
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-xl font-semibold flex items-center">
          <Activity className="w-6 h-6 mr-2 text-slate-400" />
          System Monitoring
        </h3>
        <div className="flex items-center space-x-2">
          <div className="w-2 h-2 rounded-full bg-green-400"></div>
          <span className="text-sm text-gray-400">Live</span>
        </div>
      </div>

      {error && (
        <div className="mb-4 p-3 bg-red-900/20 border border-red-700 rounded-lg">
          <p className="text-red-300 text-sm">⚠️ {error}</p>
        </div>
      )}

      {/* Tab Navigation */}
      <div className="flex space-x-1 mb-6 bg-gray-800/30 rounded-lg p-1">
        {[
          { id: 'overview', label: 'Overview', icon: TrendingUp },
          { id: 'components', label: 'Components', icon: Server },
          { id: 'alerts', label: 'Alerts', icon: AlertTriangle }
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setSelectedTab(tab.id as any)}
            className={`flex-1 flex items-center justify-center space-x-2 py-2 px-3 rounded-md text-sm font-medium transition-colors ${
              selectedTab === tab.id
                ? 'bg-slate-600 text-white'
                : 'text-gray-400 hover:text-white hover:bg-gray-700/50'
            }`}
          >
            <tab.icon className="w-4 h-4" />
            <span>{tab.label}</span>
          </button>
        ))}
      </div>

      {/* Tab Content */}
      <div className="min-h-[400px]">
        {selectedTab === 'overview' && (
          <div className="space-y-6">
            {/* Key Metrics */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="text-center">
                <div className="text-2xl font-bold text-green-300">{formatUptime(stats?.uptime || 0)}</div>
                <div className="text-sm text-gray-400">Uptime</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-blue-300">{stats?.total_requests || 0}</div>
                <div className="text-sm text-gray-400">Total Requests</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-yellow-300">{((stats?.error_rate || 0) * 100).toFixed(2)}%</div>
                <div className="text-sm text-gray-400">Error Rate</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-purple-300">{stats?.avg_response_time || 0}ms</div>
                <div className="text-sm text-gray-400">Avg Response</div>
              </div>
            </div>

            {/* Component Status Summary */}
            <div className="space-y-3">
              <h4 className="text-lg font-semibold text-gray-300">Component Status</h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {stats?.components?.slice(0, 6).map((component, index) => (
                  <motion.div
                    key={component.component}
                    className="flex items-center justify-between p-3 bg-gray-800/30 rounded-lg border border-gray-700/30"
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.1 }}
                  >
                    <div className="flex items-center space-x-3">
                      {getStatusIcon(component.status)}
                      <div>
                        <div className="text-sm font-medium text-gray-300 capitalize">
                          {component.component.replace('_', ' ')}
                        </div>
                        <div className="text-xs text-gray-500">
                          {component.response_time}ms response
                        </div>
                      </div>
                    </div>
                    <div className={`text-sm font-medium capitalize ${getStatusColor(component.status)}`}>
                      {component.status}
                    </div>
                  </motion.div>
                ))}
              </div>
            </div>
          </div>
        )}

        {selectedTab === 'components' && (
          <div className="space-y-4">
            {stats?.components?.map((component, index) => (
              <motion.div
                key={component.component}
                className="p-4 bg-gray-800/30 rounded-lg border border-gray-700/30"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.05 }}
              >
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center space-x-3">
                    {getStatusIcon(component.status)}
                    <div>
                      <div className="text-lg font-medium text-gray-300 capitalize">
                        {component.component.replace('_', ' ')}
                      </div>
                      <div className="text-sm text-gray-500">
                        Last checked: {new Date(component.last_check * 1000).toLocaleTimeString()}
                      </div>
                    </div>
                  </div>
                  <div className={`px-3 py-1 rounded-full text-sm font-medium capitalize ${getStatusColor(component.status)} bg-current/10`}>
                    {component.status}
                  </div>
                </div>

                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-3">
                  <div>
                    <div className="text-sm text-gray-400">Response Time</div>
                    <div className="text-lg font-bold text-white">{component.response_time}ms</div>
                  </div>
                  {component.metrics && Object.entries(component.metrics).slice(0, 3).map(([key, value]) => (
                    <div key={key}>
                      <div className="text-sm text-gray-400 capitalize">{key.replace('_', ' ')}</div>
                      <div className="text-lg font-bold text-white">{String(value)}</div>
                    </div>
                  ))}
                </div>

                {component.error_message && (
                  <div className="mt-3 p-3 bg-red-900/20 border border-red-700/50 rounded-lg">
                    <div className="flex items-center space-x-2">
                      <AlertTriangle className="w-4 h-4 text-red-400" />
                      <span className="text-sm text-red-300">{component.error_message}</span>
                    </div>
                  </div>
                )}
              </motion.div>
            )) || (
              <div className="text-center py-8 text-gray-500">
                <Server className="w-12 h-12 mx-auto mb-2 opacity-50" />
                <p>No component data available</p>
              </div>
            )}
          </div>
        )}

        {selectedTab === 'alerts' && (
          <div className="space-y-3">
            {stats?.alerts?.length === 0 ? (
              <div className="text-center py-8 text-gray-500">
                <CheckCircle className="w-12 h-12 mx-auto mb-2 opacity-50" />
                <p>No active alerts</p>
              </div>
            ) : (
              stats?.alerts?.map((alert, index) => (
                <motion.div
                  key={alert.id}
                  className={`p-4 border rounded-lg ${getAlertSeverityColor(alert.severity)}`}
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: index * 0.05 }}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <div className={`p-1 rounded-full ${
                        alert.severity === 'critical' ? 'bg-red-600' :
                        alert.severity === 'error' ? 'bg-red-500' :
                        alert.severity === 'warning' ? 'bg-yellow-500' :
                        'bg-blue-500'
                      }`}>
                        {alert.severity === 'critical' || alert.severity === 'error' ? (
                          <XCircle className="w-3 h-3 text-white" />
                        ) : alert.severity === 'warning' ? (
                          <AlertTriangle className="w-3 h-3 text-white" />
                        ) : (
                          <Activity className="w-3 h-3 text-white" />
                        )}
                      </div>
                      <div>
                        <div className="font-medium text-white">
                          {alert.message}
                        </div>
                        <div className="text-sm opacity-75">
                          {new Date(alert.timestamp * 1000).toLocaleString()}
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center space-x-2">
                      <span className={`px-2 py-1 rounded text-xs font-medium uppercase ${
                        alert.severity === 'critical' ? 'bg-red-600 text-white' :
                        alert.severity === 'error' ? 'bg-red-500 text-white' :
                        alert.severity === 'warning' ? 'bg-yellow-500 text-black' :
                        'bg-blue-500 text-white'
                      }`}>
                        {alert.severity}
                      </span>
                      {alert.resolved && (
                        <CheckCircle className="w-4 h-4 text-green-400" />
                      )}
                    </div>
                  </div>
                </motion.div>
              ))
            )}
          </div>
        )}
      </div>
    </motion.div>
  );
}