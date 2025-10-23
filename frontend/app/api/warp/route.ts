import { NextRequest, NextResponse } from 'next/server';

const ZION_CORE_BASE = process.env.ZION_CORE_BASE || "http://localhost:8889";

/**
 * ZION WARP Bridge API - v2.8.1
 * Handles multi-chain transfers and bridge operations
 */
export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const action = searchParams.get('action') || 'status';

  try {
    let endpoint = '';

    switch (action) {
      case 'status':
        endpoint = '/api/warp/status';
        break;
      case 'transfer':
        const txId = searchParams.get('txId');
        endpoint = `/api/warp/transfer/${txId}`;
        break;
      case 'history':
        const address = searchParams.get('address');
        const limit = searchParams.get('limit') || '10';
        endpoint = `/api/warp/history?address=${address}&limit=${limit}`;
        break;
      case 'chains':
        endpoint = '/api/warp/chains';
        break;
      case 'quote':
        const fromChain = searchParams.get('from');
        const toChain = searchParams.get('to');
        const amount = searchParams.get('amount');
        endpoint = `/api/warp/quote?from=${fromChain}&to=${toChain}&amount=${amount}`;
        break;
      default:
        return NextResponse.json({ error: 'Unknown action' }, { status: 400 });
    }

    const response = await fetch(`${ZION_CORE_BASE}${endpoint}`, {
      headers: { 'Accept': 'application/json' },
      signal: AbortSignal.timeout(5000)
    });

    if (!response.ok) {
      throw new Error(`WARP API ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();
    return NextResponse.json(data);

  } catch (error) {
    console.warn('[zion-warp-api] GET failed:', error);

    const fallbackData = getWarpFallbackData(action);
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
 * POST endpoint for WARP bridge operations
 */
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { action, params = {} } = body;

    let endpoint = '';

    switch (action) {
      case 'transfer':
        endpoint = '/api/warp/transfer';
        break;
      case 'estimate-fee':
        endpoint = '/api/warp/estimate-fee';
        break;
      case 'get-quote':
        endpoint = '/api/warp/quote';
        break;
      case 'cancel-transfer':
        endpoint = '/api/warp/cancel';
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
      signal: AbortSignal.timeout(15000) // Longer timeout for transfers
    });

    if (!response.ok) {
      throw new Error(`WARP API ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();
    return NextResponse.json(data);

  } catch (error) {
    console.warn('[zion-warp-api] POST failed:', error);
    return NextResponse.json(
      {
        error: error instanceof Error ? error.message : 'WARP action failed',
        _meta: { source: 'error', timestamp: new Date().toISOString() }
      },
      { status: 500 }
    );
  }
}

/**
 * Fallback data for WARP bridge
 */
function getWarpFallbackData(action: string) {
  const fallbacks = {
    status: {
      status: 'operational',
      supportedChains: ['zion', 'ethereum', 'polygon', 'arbitrum', 'optimism', 'avalanche', 'bsc', 'solana'],
      activeTransfers: 0,
      totalTransferred: 0,
      averageTransferTime: 969,
      successRate: 100
    },
    history: {
      transfers: [
        {
          tx_id: 'warp_001',
          source_chain: 'zion',
          destination_chain: 'ethereum',
          amount: 1000,
          asset: 'ZION',
          status: 'completed',
          total_time_ms: 850,
          fee_total: 0.001,
          timestamp: new Date(Date.now() - 3600000).toISOString()
        },
        {
          tx_id: 'warp_002',
          source_chain: 'polygon',
          destination_chain: 'zion',
          amount: 500,
          asset: 'MATIC',
          status: 'completed',
          total_time_ms: 920,
          fee_total: 0.0005,
          timestamp: new Date(Date.now() - 7200000).toISOString()
        }
      ]
    },
    chains: [
      { id: 'zion', name: 'ZION', nativeAsset: 'ZION', rpcUrl: 'https://zion.network/rpc' },
      { id: 'ethereum', name: 'Ethereum', nativeAsset: 'ETH', rpcUrl: 'https://mainnet.infura.io/v3/YOUR_KEY' },
      { id: 'polygon', name: 'Polygon', nativeAsset: 'MATIC', rpcUrl: 'https://polygon-rpc.com' },
      { id: 'bsc', name: 'BSC', nativeAsset: 'BNB', rpcUrl: 'https://bsc-dataseed.binance.org' },
      { id: 'solana', name: 'Solana', nativeAsset: 'SOL', rpcUrl: 'https://api.mainnet.solana.com' }
    ],
    quote: {
      fromChain: 'zion',
      toChain: 'ethereum',
      amount: 1000,
      estimatedFee: 0.001,
      estimatedTime: 1000,
      exchangeRate: 1.0,
      validUntil: new Date(Date.now() + 300000).toISOString()
    }
  };

  return fallbacks[action as keyof typeof fallbacks] || fallbacks.status;
}