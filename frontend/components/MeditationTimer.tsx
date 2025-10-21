import React, { useState, useEffect, useRef } from 'react';
import { Play, Pause, Square, Clock, TrendingUp, Award, Zap } from 'lucide-react';

interface MeditationStats {
  total_meditation_minutes: number;
  total_meditation_hours: number;
  session_count: number;
  karma_multiplier: number;
  bonus_percent: number;
  next_tier: {
    minutes_required: number;
    minutes_remaining: number;
    hours_remaining: number;
    multiplier: number;
    bonus_percent: number;
  } | null;
}

interface MeditationTimerProps {
  walletAddress: string;
  apiEndpoint?: string;
  onSessionComplete?: (duration: number, stats: MeditationStats) => void;
}

const MeditationTimer: React.FC<MeditationTimerProps> = ({
  walletAddress,
  apiEndpoint = '/api/consciousness',
  onSessionComplete
}) => {
  // Timer state
  const [isRunning, setIsRunning] = useState(false);
  const [seconds, setSeconds] = useState(0);
  const [startTime, setStartTime] = useState<number | null>(null);
  const intervalRef = useRef<NodeJS.Timeout | null>(null);

  // Stats state
  const [stats, setStats] = useState<MeditationStats | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Format time as MM:SS
  const formatTime = (totalSeconds: number): string => {
    const mins = Math.floor(totalSeconds / 60);
    const secs = totalSeconds % 60;
    return `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
  };

  // Load stats on mount
  useEffect(() => {
    fetchStats();
  }, [walletAddress]);

  // Timer effect
  useEffect(() => {
    if (isRunning) {
      intervalRef.current = setInterval(() => {
        setSeconds(s => s + 1);
      }, 1000);
    } else {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    }

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, [isRunning]);

  const fetchStats = async () => {
    try {
      setIsLoading(true);
      const response = await fetch(`${apiEndpoint}/stats?wallet=${walletAddress}`);
      if (!response.ok) throw new Error('Failed to fetch stats');
      const data = await response.json();
      setStats(data);
      setError(null);
    } catch (err) {
      setError('Failed to load consciousness stats');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleStart = () => {
    setStartTime(Date.now());
    setIsRunning(true);
  };

  const handlePause = () => {
    setIsRunning(false);
  };

  const handleStop = async () => {
    setIsRunning(false);
    
    if (seconds === 0) {
      // No session to submit
      return;
    }

    const durationMinutes = Math.floor(seconds / 60);
    
    if (durationMinutes < 1) {
      alert('Meditation session too short (minimum 1 minute)');
      setSeconds(0);
      setStartTime(null);
      return;
    }

    // Submit session
    try {
      setIsLoading(true);
      const response = await fetch(`${apiEndpoint}/session`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          wallet: walletAddress,
          duration_minutes: durationMinutes,
          session_type: 'self_reported',
          notes: `Session started at ${new Date(startTime!).toLocaleTimeString()}`
        })
      });

      if (!response.ok) throw new Error('Failed to submit session');
      
      const newStats = await response.json();
      setStats(newStats);
      
      // Success notification
      alert(`🧘 Meditation session recorded!\n${durationMinutes} minutes logged.\nNew multiplier: ${newStats.karma_multiplier.toFixed(2)}x`);
      
      // Callback
      if (onSessionComplete) {
        onSessionComplete(durationMinutes, newStats);
      }
      
      setError(null);
    } catch (err) {
      setError('Failed to submit meditation session');
      console.error(err);
    } finally {
      setIsLoading(false);
      setSeconds(0);
      setStartTime(null);
    }
  };

  const handleReset = () => {
    setIsRunning(false);
    setSeconds(0);
    setStartTime(null);
  };

  const getMultiplierColor = (multiplier: number): string => {
    if (multiplier >= 2.0) return 'text-purple-400';
    if (multiplier >= 1.6) return 'text-blue-400';
    if (multiplier >= 1.3) return 'text-green-400';
    if (multiplier >= 1.1) return 'text-yellow-400';
    return 'text-gray-400';
  };

  const getProgressPercent = (): number => {
    if (!stats || !stats.next_tier) return 100; // Max tier
    const current = stats.total_meditation_minutes;
    const target = stats.next_tier.minutes_required;
    return Math.min((current / target) * 100, 100);
  };

  return (
    <div className="bg-gradient-to-br from-gray-900 to-gray-800 rounded-lg shadow-xl p-6 text-white">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold flex items-center gap-2">
          <Clock className="w-6 h-6 text-purple-400" />
          Consciousness Mining
        </h2>
        <button
          onClick={fetchStats}
          className="px-3 py-1 text-sm bg-gray-700 hover:bg-gray-600 rounded transition-colors"
          disabled={isLoading}
        >
          {isLoading ? '⏳' : '🔄'} Refresh
        </button>
      </div>

      {error && (
        <div className="mb-4 p-3 bg-red-500/20 border border-red-500 rounded text-red-200 text-sm">
          {error}
        </div>
      )}

      {/* Timer Display */}
      <div className="mb-8 text-center">
        <div className="text-6xl font-mono font-bold mb-4 tracking-wider">
          {formatTime(seconds)}
        </div>

        {/* Timer Controls */}
        <div className="flex justify-center gap-3">
          {!isRunning ? (
            <button
              onClick={handleStart}
              className="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-500 hover:to-blue-500 rounded-lg font-semibold transition-all shadow-lg hover:shadow-xl"
            >
              <Play className="w-5 h-5" />
              Start Meditation
            </button>
          ) : (
            <>
              <button
                onClick={handlePause}
                className="flex items-center gap-2 px-6 py-3 bg-yellow-600 hover:bg-yellow-500 rounded-lg font-semibold transition-colors"
              >
                <Pause className="w-5 h-5" />
                Pause
              </button>
              <button
                onClick={handleStop}
                className="flex items-center gap-2 px-6 py-3 bg-green-600 hover:bg-green-500 rounded-lg font-semibold transition-colors"
              >
                <Square className="w-5 h-5" />
                Complete Session
              </button>
            </>
          )}
          
          {seconds > 0 && !isRunning && (
            <button
              onClick={handleReset}
              className="px-4 py-3 bg-gray-600 hover:bg-gray-500 rounded-lg transition-colors"
            >
              Reset
            </button>
          )}
        </div>
      </div>

      {/* Stats Display */}
      {stats && (
        <div className="space-y-4">
          {/* Current Multiplier */}
          <div className="bg-gray-800/50 rounded-lg p-4 border border-gray-700">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <Zap className={`w-6 h-6 ${getMultiplierColor(stats.karma_multiplier)}`} />
                <div>
                  <div className="text-sm text-gray-400">Karma Multiplier</div>
                  <div className={`text-3xl font-bold ${getMultiplierColor(stats.karma_multiplier)}`}>
                    {stats.karma_multiplier.toFixed(2)}x
                  </div>
                </div>
              </div>
              <div className="text-right">
                <div className="text-sm text-gray-400">Bonus</div>
                <div className="text-2xl font-bold text-green-400">
                  +{stats.bonus_percent.toFixed(0)}%
                </div>
              </div>
            </div>
          </div>

          {/* Progress to Next Tier */}
          {stats.next_tier ? (
            <div className="bg-gray-800/50 rounded-lg p-4 border border-gray-700">
              <div className="flex items-center gap-2 mb-2">
                <TrendingUp className="w-5 h-5 text-blue-400" />
                <div className="text-sm font-semibold">Next Tier Progress</div>
              </div>
              
              <div className="mb-2">
                <div className="flex justify-between text-xs text-gray-400 mb-1">
                  <span>{stats.karma_multiplier.toFixed(2)}x</span>
                  <span className="text-blue-400 font-semibold">
                    {stats.next_tier.multiplier.toFixed(2)}x
                  </span>
                </div>
                <div className="w-full bg-gray-700 rounded-full h-3 overflow-hidden">
                  <div
                    className="bg-gradient-to-r from-purple-600 to-blue-500 h-full transition-all duration-500"
                    style={{ width: `${getProgressPercent()}%` }}
                  />
                </div>
              </div>
              
              <div className="text-sm text-gray-300">
                <span className="text-yellow-400 font-semibold">
                  {stats.next_tier.hours_remaining.toFixed(1)} hours
                </span>
                {' '}remaining to unlock{' '}
                <span className="text-blue-400 font-semibold">
                  {stats.next_tier.multiplier.toFixed(1)}x
                </span>
                {' '}multiplier
              </div>
            </div>
          ) : (
            <div className="bg-gradient-to-r from-purple-600/20 to-blue-600/20 rounded-lg p-4 border border-purple-500">
              <div className="flex items-center gap-2">
                <Award className="w-6 h-6 text-yellow-400" />
                <div>
                  <div className="font-semibold text-yellow-400">Maximum Tier Reached!</div>
                  <div className="text-sm text-gray-300">
                    2.0x multiplier (100% bonus on all rewards)
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Total Stats */}
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-gray-800/50 rounded-lg p-3 border border-gray-700">
              <div className="text-sm text-gray-400">Total Meditation</div>
              <div className="text-2xl font-bold">{stats.total_meditation_hours.toFixed(1)}h</div>
              <div className="text-xs text-gray-500">{stats.total_meditation_minutes} minutes</div>
            </div>
            
            <div className="bg-gray-800/50 rounded-lg p-3 border border-gray-700">
              <div className="text-sm text-gray-400">Sessions</div>
              <div className="text-2xl font-bold">{stats.session_count}</div>
              <div className="text-xs text-gray-500">completed</div>
            </div>
          </div>

          {/* Info */}
          <div className="text-xs text-gray-500 text-center mt-4">
            Meditation increases your mining rewards through karma multipliers.
            More practice = higher consciousness = better rewards! 🧘✨
          </div>
        </div>
      )}
    </div>
  );
};

export default MeditationTimer;
