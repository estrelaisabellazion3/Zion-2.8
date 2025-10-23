import { NextRequest, NextResponse } from 'next/server';

const ZION_HOST = process.env.ZION_HOST || '127.0.0.1';
const ZION_ADAPTER_PORT = Number(process.env.ZION_ADAPTER_PORT || 18099);

/**
 * ZION Pool Management API - v2.8.1
 * Handles multi-algorithm mining pool operations
 */
export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const action = searchParams.get('action') || 'stats';

  try {
    let endpoint = '';

    switch (action) {
      case 'stats':
        endpoint = '/pool/stats';
        break;
      case 'miners':
        endpoint = '/pool/miners';
        break;
      case 'blocks':
        endpoint = '/pool/blocks';
        break;
      case 'algorithms':
        endpoint = '/pool/algorithms';
        break;
      case 'worker-stats':
        const address = searchParams.get('address');
        endpoint = `/pool/worker/${address}`;
        break;
      default:
        return NextResponse.json({ error: 'Unknown action' }, { status: 400 });
    }

    const response = await fetch(`http://${ZION_HOST}:${ZION_ADAPTER_PORT}${endpoint}`, {
      headers: { 'Accept': 'application/json' },
      signal: AbortSignal.timeout(5000)
    });

    if (!response.ok) {
      throw new Error(`Pool API ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();
    return NextResponse.json(data);

  } catch (error) {
    console.warn('[zion-pool-api] GET failed:', error);

    // Return fallback data
    const fallbackData = getPoolFallbackData(action);
    return NextResponse.json({
      ...fallbackData,
      _meta: {
        source: 'fallback',
        error: error instanceof Error ? error.message : 'Unknown error',
        timestamp: new Date().toISOString()
      }
    }, { status: 503 });
  }
}

/**
 * POST endpoint for pool management actions
 */
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { action, params = {} } = body;

    let endpoint = '';
    let method = 'POST';

    switch (action) {
      case 'switch-algorithm':
        endpoint = '/pool/switch-algorithm';
        break;
      case 'submit-share':
        endpoint = '/pool/submit-share';
        break;
      case 'start-mining':
        endpoint = '/pool/start';
        break;
      case 'stop-mining':
        endpoint = '/pool/stop';
        break;
      default:
        return NextResponse.json({ error: 'Unknown action' }, { status: 400 });
    }

    const response = await fetch(`http://${ZION_HOST}:${ZION_ADAPTER_PORT}${endpoint}`, {
      method,
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(params),
      signal: AbortSignal.timeout(10000)
    });

    if (!response.ok) {
      throw new Error(`Pool API ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();
    return NextResponse.json(data);

  } catch (error) {
    console.warn('[zion-pool-api] POST failed:', error);
    return NextResponse.json(
      {
        error: error instanceof Error ? error.message : 'Pool action failed',
        _meta: { source: 'error', timestamp: new Date().toISOString() }
      },
      { status: 500 }
    );
  }
}

/**
 * Fallback data for pool operations
 */
function getPoolFallbackData(action: string) {
  const fallbacks = {
    stats: {
      algorithms: ['randomx', 'yescrypt', 'autolykos2'],
      totalMiners: 2,
      totalHashrate: 15130000,
      blocksFound: 5,
      currentDifficulty: 123456,
      miners: [
        { address: 'ZION123...', hashrate: 15000000, shares: 107, algorithm: 'randomx', lastSeen: Date.now() },
        { address: 'ZION456...', hashrate: 130000, shares: 4, algorithm: 'yescrypt', lastSeen: Date.now() }
      ]
    },
    miners: [
      { address: 'ZION123...', hashrate: 15000000, shares: 107, algorithm: 'randomx', lastSeen: Date.now() },
      { address: 'ZION456...', hashrate: 130000, shares: 4, algorithm: 'yescrypt', lastSeen: Date.now() }
    ],
    blocks: [
      { height: 1234, hash: 'abc123...', timestamp: Date.now(), reward: 50.0, miner: 'ZION123...' },
      { height: 1233, hash: 'def456...', timestamp: Date.now() - 60000, reward: 50.0, miner: 'ZION456...' }
    ],
    algorithms: ['randomx', 'yescrypt', 'autolykos2']
  };

  return fallbacks[action as keyof typeof fallbacks] || fallbacks.stats;
}