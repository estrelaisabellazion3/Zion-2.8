import { NextRequest, NextResponse } from 'next/server';

const ZION_CORE_BASE = process.env.ZION_CORE_BASE || "http://localhost:8889";

/**
 * ZION Consciousness Mining Game API - v2.8.1
 * Handles XP awards, achievements, and consciousness levels
 */
export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const action = searchParams.get('action') || 'status';

  try {
    let endpoint = '';

    switch (action) {
      case 'status':
        endpoint = '/api/consciousness/status';
        break;
      case 'miners':
        endpoint = '/api/consciousness/miners';
        break;
      case 'achievements':
        endpoint = '/api/consciousness/achievements';
        break;
      case 'leaderboard':
        endpoint = '/api/consciousness/leaderboard';
        break;
      case 'miner':
        const address = searchParams.get('address');
        endpoint = `/api/consciousness/miner/${address}`;
        break;
      default:
        return NextResponse.json({ error: 'Unknown action' }, { status: 400 });
    }

    const response = await fetch(`${ZION_CORE_BASE}${endpoint}`, {
      headers: { 'Accept': 'application/json' },
      signal: AbortSignal.timeout(5000)
    });

    if (!response.ok) {
      throw new Error(`Consciousness API ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();
    return NextResponse.json(data);

  } catch (error) {
    console.warn('[zion-consciousness-api] GET failed:', error);

    const fallbackData = getConsciousnessFallbackData(action);
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
 * POST endpoint for consciousness game actions
 */
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { action, params = {} } = body;

    let endpoint = '';

    switch (action) {
      case 'meditate':
        endpoint = '/api/consciousness/meditate';
        break;
      case 'claim-achievement':
        endpoint = '/api/consciousness/claim-achievement';
        break;
      case 'upgrade-level':
        endpoint = '/api/consciousness/upgrade';
        break;
      case 'award-xp':
        endpoint = '/api/consciousness/award-xp';
        break;
      default:
        return NextResponse.json({ error: 'Unknown action' }, { status: 400 });
    }

    const response = await fetch(`${ZION_CORE_BASE}${endpoint}`, {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(params),
      signal: AbortSignal.timeout(10000)
    });

    if (!response.ok) {
      throw new Error(`Consciousness API ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();
    return NextResponse.json(data);

  } catch (error) {
    console.warn('[zion-consciousness-api] POST failed:', error);
    return NextResponse.json(
      {
        error: error instanceof Error ? error.message : 'Consciousness action failed',
        _meta: { source: 'error', timestamp: new Date().toISOString() }
      },
      { status: 500 }
    );
  }
}

/**
 * Fallback data for consciousness game
 */
function getConsciousnessFallbackData(action: string) {
  const fallbacks = {
    status: {
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
        { id: 'consciousness_awakened', name: 'Consciousness Awakened', description: 'Reach MENTAL level', unlocked: true },
        { id: 'meditation_master', name: 'Meditation Master', description: 'Complete 10 meditation sessions', unlocked: false }
      ],
      totalMiners: 2,
      totalXP: 14090,
      activeLevel: 'MENTAL'
    },
    miners: [
      { address: 'ZION123...', level: 'MENTAL', xp: 5090, achievements: 3 },
      { address: 'ZION456...', level: 'MENTAL', xp: 9000, achievements: 2 }
    ],
    achievements: [
      { id: 'first_mine', name: 'First Mine', description: 'Mine your first block', unlocked: true },
      { id: 'consciousness_awakened', name: 'Consciousness Awakened', description: 'Reach MENTAL level', unlocked: true },
      { id: 'meditation_master', name: 'Meditation Master', description: 'Complete 10 meditation sessions', unlocked: false },
      { id: 'pool_master', name: 'Pool Master', description: 'Mine 1000 shares in the pool', unlocked: false }
    ],
    leaderboard: [
      { rank: 1, address: 'ZION123...', xp: 5090 },
      { rank: 2, address: 'ZION456...', xp: 9000 },
      { rank: 3, address: 'ZION789...', xp: 2500 }
    ]
  };

  return fallbacks[action as keyof typeof fallbacks] || fallbacks.status;
}