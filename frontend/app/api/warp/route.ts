import { NextRequest, NextResponse } from 'next/server';
import jwt from 'jsonwebtoken';

// JWT Secret (in production, use environment variable)
const JWT_SECRET = process.env.JWT_SECRET || 'zion-warp-bridge-secret-key';

// Mock data for demonstration (in production, connect to real WARP Bridge)
const mockTransactions = [
  {
    id: 'warp_001',
    source_chain: 'ZION',
    destination_chain: 'Ethereum',
    asset: 'ZION',
    amount: 42.108,
    status: 'completed',
    timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
    tx_hash: '0xa1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6',
    bridge_fee: 0.001,
    warp_speed: true,
    user_id: 'user_123'
  },
  {
    id: 'warp_002',
    source_chain: 'Bitcoin',
    destination_chain: 'ZION',
    asset: 'BTC',
    amount: 0.00021,
    status: 'confirmed',
    timestamp: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString(),
    tx_hash: 'bc1qa1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6',
    bridge_fee: 0.00001,
    warp_speed: false,
    user_id: 'user_123'
  },
  {
    id: 'warp_003',
    source_chain: 'Ethereum',
    destination_chain: 'Polygon',
    asset: 'USDC',
    amount: 150.00,
    status: 'pending',
    timestamp: new Date(Date.now() - 30 * 60 * 1000).toISOString(),
    bridge_fee: 0.50,
    warp_speed: true,
    user_id: 'user_123'
  }
];

const mockStats = {
  total_transfers: 1247,
  warp_speed_count: 892,
  total_volume: 156780.50,
  avg_time: 1850,
  success_rate: 99.2,
  active_bridges: ['ZION', 'Ethereum', 'Bitcoin', 'Polygon', 'BSC'],
  supported_assets: ['ZION', 'BTC', 'ETH', 'USDC', 'USDT']
};

// Get user's WARP transactions
export async function GET(request: NextRequest) {
  try {
    // Verify JWT token
    const authHeader = request.headers.get('authorization');
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return NextResponse.json(
        { error: 'Authorization required' },
        { status: 401 }
      );
    }

    const token = authHeader.substring(7);
    let decoded;

    try {
      decoded = jwt.verify(token, JWT_SECRET) as any;
    } catch (error) {
      return NextResponse.json(
        { error: 'Invalid token' },
        { status: 401 }
      );
    }

    const userId = decoded.userId;

    // In production, fetch from database
    // For now, return mock data filtered by user
    const userTransactions = mockTransactions.filter(tx => tx.user_id === userId);

    return NextResponse.json({
      transactions: userTransactions,
      stats: mockStats,
      user: {
        id: userId,
        total_transfers: userTransactions.length,
        total_volume: userTransactions.reduce((sum, tx) => sum + tx.amount, 0),
        warp_speed_transfers: userTransactions.filter(tx => tx.warp_speed).length
      }
    });

  } catch (error) {
    console.error('WARP API error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

// Initiate new WARP transfer
export async function POST(request: NextRequest) {
  try {
    // Verify JWT token
    const authHeader = request.headers.get('authorization');
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return NextResponse.json(
        { error: 'Authorization required' },
        { status: 401 }
      );
    }

    const token = authHeader.substring(7);
    let decoded;

    try {
      decoded = jwt.verify(token, JWT_SECRET) as any;
    } catch (error) {
      return NextResponse.json(
        { error: 'Invalid token' },
        { status: 401 }
      );
    }

    const userId = decoded.userId;
    const body = await request.json();

    const { source_chain, destination_chain, asset, amount } = body;

    // Basic validation
    if (!source_chain || !destination_chain || !asset || !amount) {
      return NextResponse.json(
        { error: 'Missing required fields' },
        { status: 400 }
      );
    }

    if (amount <= 0) {
      return NextResponse.json(
        { error: 'Invalid amount' },
        { status: 400 }
      );
    }

    // In production, this would:
    // 1. Validate user balance
    // 2. Create WARP transfer via production bridge
    // 3. Return transaction details

    // For now, create mock transaction
    const newTransaction = {
      id: `warp_${Date.now()}`,
      source_chain,
      destination_chain,
      asset,
      amount: parseFloat(amount),
      status: 'pending',
      timestamp: new Date().toISOString(),
      bridge_fee: amount * 0.001, // 0.1% fee
      warp_speed: amount < 100, // Small transfers get WARP speed
      user_id: userId
    };

    // Simulate processing delay
    setTimeout(() => {
      newTransaction.status = 'confirmed';
      // In production, update database
    }, 2000);

    return NextResponse.json({
      success: true,
      transaction: newTransaction,
      message: 'WARP transfer initiated successfully'
    });

  } catch (error) {
    console.error('WARP transfer error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}