import { NextRequest, NextResponse } from 'next/server';

const ZION_CORE_BASE = process.env.ZION_CORE_BASE || "http://localhost:8889";

/**
 * ZION 2.8.1 "Estrella" TestNet API Proxy
 * Routes frontend requests to Python-native ZION backend
 * 
 * New in 2.8.1:
 * - WARP Bridge integration
 * - Consciousness Mining Game
 * - Lightning Network payments
 * - Multi-algorithm mining pool
 * - Production monitoring
 */
export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const endpoint = searchParams.get('endpoint') || 'stats';
  
  try {
    // Map frontend requests to ZION Core endpoints
    const coreEndpoints = {
      // Core system endpoints
      'stats': '/api/stats',
      'mining': '/api/mining/stats', 
      'gpu': '/api/gpu/stats',
      'lightning': '/api/lightning/stats',
      'blockchain': '/api/blockchain/stats',
      'health': '/health',
      'modules': '/health',
      
      // WARP Bridge endpoints (2.8.1)
      'warp-status': '/api/warp/status',
      'warp-transfer': '/api/warp/transfer',
      'warp-history': '/api/warp/history',
      'warp-supported-chains': '/api/warp/chains',
      
      // Consciousness Mining Game (2.8.1)
      'consciousness-status': '/api/consciousness/status',
      'consciousness-miners': '/api/consciousness/miners',
      'consciousness-achievements': '/api/consciousness/achievements',
      'consciousness-leaderboard': '/api/consciousness/leaderboard',
      
      // Lightning Network (2.8.1)
      'lightning-channels': '/api/lightning/channels',
      'lightning-payments': '/api/lightning/payments',
      'lightning-invoices': '/api/lightning/invoices',
      'lightning-balance': '/api/lightning/balance',
      
      // Multi-algorithm Mining Pool (2.8.1)
      'pool-stats': '/api/pool/stats',
      'pool-miners': '/api/pool/miners',
      'pool-blocks': '/api/pool/blocks',
      'pool-algorithms': '/api/pool/algorithms',
      
      // Production Monitoring (2.8.1)
      'monitoring-health': '/api/monitoring/health',
      'monitoring-metrics': '/api/monitoring/metrics',
      'monitoring-logs': '/api/monitoring/logs'
    };
    
    const coreEndpoint = coreEndpoints[endpoint as keyof typeof coreEndpoints] || '/api/stats';
    const response = await fetch(`${ZION_CORE_BASE}${coreEndpoint}`, {
      headers: {
        'Accept': 'application/json',
        'User-Agent': 'ZION-Frontend-v2.7'
      },
      // Add timeout for production reliability
      signal: AbortSignal.timeout(5000)
    });

    if (!response.ok) {
      throw new Error(`ZION Core ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();
    
    // Normalize data shape for frontend widgets when using aggregated stats
    const normalized = endpoint === 'stats' ? normalizeStatsForFrontend(data) : data;
    
    // Add frontend-specific metadata
    const enrichedData = {
      ...normalized,
      _meta: {
        source: 'zion-core-v2.8.1',
        endpoint: coreEndpoint,
        timestamp: new Date().toISOString(),
        frontend_version: '2.8.1'
      }
    };

    return NextResponse.json(enrichedData);
    
  } catch (error) {
    // Avoid noisy logs in production; keep concise warning
    const message = error instanceof Error ? `${error.name}: ${error.message}` : 'Unknown error';
    console.warn('[zion-core proxy] GET failed -> using fallback:', message);
    
    // Return fallback data for development/offline scenarios
    const fallbackData = getFallbackData(endpoint);
    
    return NextResponse.json({
      ...fallbackData,
      _meta: {
        source: 'fallback',
        error: error instanceof Error ? error.message : 'Unknown error',
        timestamp: new Date().toISOString()
      }
    }, { 
      status: error instanceof Error && error.name === 'AbortError' ? 408 : 503 
    });
  }
}

/**
 * POST endpoint for ZION Core commands
 */
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { action, params = {} } = body;
    
    // Map frontend actions to ZION Core commands
    const actionEndpoints = {
      // GPU mining controls
      'start_mining': '/api/gpu/start',
      'stop_mining': '/api/gpu/stop', 
      'benchmark_gpu': '/api/gpu/benchmark',
      
      // WARP Bridge actions (2.8.1)
      'warp_transfer': '/api/warp/transfer',
      'warp_estimate_fee': '/api/warp/estimate-fee',
      'warp_get_quote': '/api/warp/quote',
      
      // Consciousness Game actions (2.8.1)
      'consciousness_meditate': '/api/consciousness/meditate',
      'consciousness_claim_achievement': '/api/consciousness/claim-achievement',
      'consciousness_upgrade_level': '/api/consciousness/upgrade',
      
      // Lightning Network actions (2.8.1)
      'lightning_pay': '/api/lightning/payments',
      'lightning_create_invoice': '/api/lightning/invoices',
      'lightning_decode_invoice': '/api/lightning/decode',
      'lightning_channel_open': '/api/lightning/channels/open',
      'lightning_channel_close': '/api/lightning/channels/close',
      
      // Mining Pool actions (2.8.1)
      'pool_switch_algorithm': '/api/pool/switch-algorithm',
      'pool_get_worker_stats': '/api/pool/worker-stats',
      'pool_submit_share': '/api/pool/submit-share',
      
      // Legacy actions
      'mining_status': '/api/mining/stats'
    };
    
    const endpoint = actionEndpoints[action as keyof typeof actionEndpoints];
    if (!endpoint) {
      return NextResponse.json(
        { error: `Unknown action: ${action}` }, 
        { status: 400 }
      );
    }
    
    // Determine HTTP method based on action/endpoint
    const method = action === 'mining_status' ? 'GET' : 'POST';

    const response = await fetch(`${ZION_CORE_BASE}${endpoint}`, {
      method,
      headers: {
        'Accept': 'application/json',
        ...(method === 'POST' ? { 'Content-Type': 'application/json' } : {})
      },
      body: method === 'POST' ? JSON.stringify(params) : undefined,
      signal: AbortSignal.timeout(10000)
    });
    
    if (!response.ok) {
      throw new Error(`ZION Core ${response.status}: ${response.statusText}`);
    }
    
    const data = await response.json();
    return NextResponse.json(data);
    
  } catch (error) {
    const message = error instanceof Error ? `${error.name}: ${error.message}` : 'Unknown error';
    console.warn('[zion-core proxy] POST failed:', message);
    return NextResponse.json(
      { 
        error: error instanceof Error ? error.message : 'Command failed',
        _meta: { source: 'error', timestamp: new Date().toISOString() }
      },
      { status: 500 }
    );
  }
}

/**
 * Fallback data for offline/development mode
 */
function getFallbackData(endpoint: string) {
  const fallbacks = {
    stats: {
      system: {
        cpu: { manufacturer: 'Apple', brand: 'M1', cores: 8, speed: 3200 },
        memory: { total: 8589934592, used: 4294967296, free: 4294967296 },
        network: {}
      },
      blockchain: { height: 1234, difficulty: 123456, txCount: 567 },
      mining: { 
        hashrate: 15130000, 
        miners: 1, 
        difficulty: 123456,
        algorithm: 'RandomX',
        status: 'mining'
      },
      gpu: {
        gpus: [{
          id: 0,
          name: 'AMD Radeon RX 5600 XT',
          status: 'mining',
          hashrate: 15.13,
          temperature: 72,
          power: 180
        }],
        totalHashrate: 15.13,
        powerUsage: 180
      },
      lightning: { 
        channels: 2, 
        balance: 1000000, 
        peers: 5,
        status: 'online'
      },
      // New in 2.8.1
      warp: {
        status: 'operational',
        supportedChains: ['zion', 'ethereum', 'polygon', 'bsc', 'solana'],
        activeTransfers: 0,
        totalTransferred: 0
      },
      consciousness: {
        totalMiners: 2,
        totalXP: 14090,
        activeLevel: 'MENTAL',
        achievementsUnlocked: 5
      }
    },
    warp: {
      status: 'operational',
      supportedChains: ['zion', 'ethereum', 'polygon', 'arbitrum', 'optimism', 'avalanche', 'bsc', 'solana'],
      activeTransfers: 0,
      totalTransferred: 0,
      averageTransferTime: 969,
      successRate: 100
    },
    consciousness: {
      miners: [
        { address: 'ZION123...', level: 'MENTAL', xp: 5090, achievements: 3 },
        { address: 'ZION456...', level: 'MENTAL', xp: 9000, achievements: 2 }
      ],
      leaderboard: [
        { rank: 1, address: 'ZION123...', xp: 5090 },
        { rank: 2, address: 'ZION456...', xp: 9000 }
      ],
      achievements: [
        { id: 'first_mine', name: 'First Mine', description: 'Mine your first block', unlocked: true },
        { id: 'consciousness_awakened', name: 'Consciousness Awakened', description: 'Reach MENTAL level', unlocked: true }
      ]
    },
    lightning: {
      channels: [
        { id: 'channel1', capacity: 1000000, localBalance: 500000, remoteBalance: 500000, active: true },
        { id: 'channel2', capacity: 2000000, localBalance: 1500000, remoteBalance: 500000, active: true }
      ],
      totalCapacity: 3000000,
      totalLocalBalance: 2000000,
      totalRemoteBalance: 1000000,
      activeChannels: 2,
      pendingChannels: 0,
      nodeAlias: 'ZION-TESTNET',
      nodeId: '02abcdef...'
    },
    pool: {
      algorithms: ['randomx', 'yescrypt', 'autolykos2'],
      totalMiners: 2,
      totalHashrate: 15130000,
      blocksFound: 5,
      currentDifficulty: 123456,
      miners: [
        { address: 'ZION123...', hashrate: 15000000, shares: 107, algorithm: 'randomx' },
        { address: 'ZION456...', hashrate: 130000, shares: 4, algorithm: 'yescrypt' }
      ]
    },
    mining: {
      status: 'mining',
      hashrate: 15130000,
      miners: 1,
      algorithm: 'RandomX',
      pool: 'zion-testnet',
      shares: { accepted: 42, rejected: 1 }
    },
    gpu: {
      devices: [{
        id: 0,
        name: 'AMD Radeon RX 5600 XT', 
        vendor: 'AMD',
        status: 'mining',
        hashrate: 15.13,
        temperature: 72,
        power: 180,
        memory: 6144
      }],
      total_hashrate: 15.13,
      total_power: 180
    },
    health: {
      status: 'healthy',
      uptime: 3600000,
      modules: {
        blockchain: 'ready',
        mining: 'mining', 
        gpu: 'ready',
        lightning: 'ready',
        warp: 'operational',
        consciousness: 'active'
      }
    }
  };
  
  return fallbacks[endpoint as keyof typeof fallbacks] || fallbacks.stats;
}

/**
 * Normalize backend aggregated stats to the shape expected by UI widgets
 */
function normalizeStatsForFrontend(data: any) {
  // Ensure required top-level keys exist
  const system = data.system || {};
  const blockchain = data.blockchain || {};
  const mining = data.mining || {};
  const gpu = data.gpu || {};
  const lightning = data.lightning || {};

  // Map backend naming to widget expectations if needed
  const normalizedLightning = {
    channels: lightning.channels || [],
    totalCapacity: lightning.totalCapacity ?? 0,
    totalLocalBalance: lightning.totalLocalBalance ?? 0,
    totalRemoteBalance: lightning.totalRemoteBalance ?? 0,
    activeChannels: lightning.channelsActive ?? lightning.activeChannels ?? 0,
    pendingChannels: lightning.channelsPending ?? lightning.pendingChannels ?? 0,
    nodeAlias: lightning.nodeAlias || 'ZION-NODE',
    nodeId: lightning.nodeId || '02..'
  };

  const normalizedGPU = {
    gpus: gpu.gpus || gpu.devices || [],
    totalHashrate: gpu.totalHashrate ?? gpu.total_hashrate ?? 0,
    powerUsage: gpu.powerUsage ?? gpu.total_power ?? 0,
    averageTemperature: gpu.averageTemperature ?? 0
  };

  const normalizedMining = {
    hashrate: mining.hashrate ?? 0,
    miners: mining.miners ?? mining.minersActive ?? 0,
    difficulty: mining.difficulty ?? 0,
    algorithm: mining.algorithm || 'RandomX',
    status: mining.status || 'stopped',
    shares: mining.shares || (mining.sharesAccepted !== undefined ? { accepted: mining.sharesAccepted, rejected: mining.sharesRejected ?? 0 } : undefined)
  };

  const normalizedBlockchain = {
    height: blockchain.height ?? 0,
    difficulty: blockchain.difficulty ?? 0,
    txCount: blockchain.txCount ?? 0,
    txPoolSize: blockchain.txPoolSize ?? 0
  };

  return {
    system,
    blockchain: normalizedBlockchain,
    mining: normalizedMining,
    gpu: normalizedGPU,
    lightning: normalizedLightning
  };
}