import { NextRequest, NextResponse } from 'next/server';

const ZION_CORE_BASE = process.env.ZION_CORE_BASE || "http://localhost:8889";

/**
 * ZION Lightning Network API - v2.8.1
 * Handles Lightning Network payments and channel management
 */
export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const action = searchParams.get('action') || 'channels';

  try {
    let endpoint = '';

    switch (action) {
      case 'channels':
        endpoint = '/api/lightning/channels';
        break;
      case 'payments':
        const limit = searchParams.get('limit') || '10';
        endpoint = `/api/lightning/payments?limit=${limit}`;
        break;
      case 'invoices':
        endpoint = '/api/lightning/invoices';
        break;
      case 'balance':
        endpoint = '/api/lightning/balance';
        break;
      case 'node-info':
        endpoint = '/api/lightning/node-info';
        break;
      case 'peers':
        endpoint = '/api/lightning/peers';
        break;
      default:
        return NextResponse.json({ error: 'Unknown action' }, { status: 400 });
    }

    const response = await fetch(`${ZION_CORE_BASE}${endpoint}`, {
      headers: { 'Accept': 'application/json' },
      signal: AbortSignal.timeout(5000)
    });

    if (!response.ok) {
      throw new Error(`Lightning API ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();
    return NextResponse.json(data);

  } catch (error) {
    console.warn('[zion-lightning-api] GET failed:', error);

    const fallbackData = getLightningFallbackData(action);
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
 * POST endpoint for Lightning Network operations
 */
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { action, params = {} } = body;

    let endpoint = '';

    switch (action) {
      case 'pay':
        endpoint = '/api/lightning/payments';
        break;
      case 'create-invoice':
        endpoint = '/api/lightning/invoices';
        break;
      case 'decode-invoice':
        endpoint = '/api/lightning/decode';
        break;
      case 'open-channel':
        endpoint = '/api/lightning/channels/open';
        break;
      case 'close-channel':
        endpoint = '/api/lightning/channels/close';
        break;
      case 'connect-peer':
        endpoint = '/api/lightning/peers/connect';
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
      throw new Error(`Lightning API ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();
    return NextResponse.json(data);

  } catch (error) {
    console.warn('[zion-lightning-api] POST failed:', error);
    return NextResponse.json(
      {
        error: error instanceof Error ? error.message : 'Lightning action failed',
        _meta: { source: 'error', timestamp: new Date().toISOString() }
      },
      { status: 500 }
    );
  }
}

/**
 * Fallback data for Lightning Network
 */
function getLightningFallbackData(action: string) {
  const fallbacks = {
    channels: {
      channels: [
        {
          id: 'channel1',
          capacity: 1000000,
          localBalance: 500000,
          remoteBalance: 500000,
          active: true,
          peerAlias: 'VoltageNode',
          channelPoint: 'abc123:0',
          uptime: 86400
        },
        {
          id: 'channel2',
          capacity: 2000000,
          localBalance: 1500000,
          remoteBalance: 500000,
          active: true,
          peerAlias: 'OpenNode',
          channelPoint: 'def456:1',
          uptime: 172800
        }
      ],
      totalCapacity: 3000000,
      totalLocalBalance: 2000000,
      totalRemoteBalance: 1000000,
      activeChannels: 2,
      pendingChannels: 0,
      inactiveChannels: 0
    },
    payments: {
      payments: [
        {
          paymentHash: 'pay_001',
          amount: 10000,
          fee: 1,
          status: 'succeeded',
          timestamp: new Date(Date.now() - 3600000).toISOString(),
          description: 'Coffee payment'
        },
        {
          paymentHash: 'pay_002',
          amount: 50000,
          fee: 2,
          status: 'succeeded',
          timestamp: new Date(Date.now() - 7200000).toISOString(),
          description: 'Service payment'
        }
      ]
    },
    balance: {
      totalBalance: 2000000,
      confirmedBalance: 2000000,
      unconfirmedBalance: 0,
      lockedBalance: 0
    },
    nodeInfo: {
      nodeAlias: 'ZION-TESTNET',
      nodeId: '02abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890ab',
      numChannels: 2,
      numPeers: 3,
      blockHeight: 850000,
      syncedToChain: true,
      version: '0.17.0-beta'
    },
    peers: {
      peers: [
        { pubKey: 'peer1...', address: '1.2.3.4:9735', alias: 'VoltageNode', connected: true },
        { pubKey: 'peer2...', address: '5.6.7.8:9735', alias: 'OpenNode', connected: true },
        { pubKey: 'peer3...', address: '9.10.11.12:9735', alias: 'ACINQ', connected: false }
      ]
    }
  };

  return fallbacks[action as keyof typeof fallbacks] || fallbacks.channels;
}