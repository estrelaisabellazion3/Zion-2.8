import { NextRequest, NextResponse } from 'next/server';
import jwt from 'jsonwebtoken';
import { z } from 'zod';
import crypto from 'crypto';

// JWT Secret (in production, use environment variable)
const JWT_SECRET = process.env.JWT_SECRET || 'zion-warp-bridge-secret-key';

// Wallet login schema validation
const walletLoginSchema = z.object({
  walletAddress: z.string().regex(/^Z3[a-fA-F0-9]{60}$/, 'Invalid ZION wallet address'),
  signature: z.string(),
  message: z.string(),
});

// In-memory user store (shared with other auth endpoints)
interface User {
  id: string;
  username: string;
  email: string;
  passwordHash: string;
  apiKey: string;
  role: string;
  createdAt: string;
  lastLogin?: string;
  dailyLimit: number;
  totalVolume: number;
  walletAddress?: string;
}

// Global users store
// Using a simple in-memory store for demo purposes
let zionUsers: User[] = [];

// Generate API key
function generateApiKey(): string {
  return 'zion_wallet_' + Math.random().toString(36).substr(2, 9) + Date.now().toString(36);
}

// Verify wallet signature (simplified - in production use proper crypto verification)
function verifyWalletSignature(walletAddress: string, message: string, signature: string): boolean {
  // This is a simplified verification for demo purposes
  // In production, you would verify the signature cryptographically
  // For ZION addresses, you'd verify against the blockchain

  try {
    // Basic signature format check
    if (!signature.startsWith('0x') || signature.length !== 132) {
      return false;
    }

    // Check if message contains wallet address
    if (!message.includes(walletAddress)) {
      return false;
    }

    // Check timestamp (prevent replay attacks)
    const timestamp = message.match(/Timestamp: (\d+)/)?.[1];
    if (!timestamp) return false;

    const messageTime = parseInt(timestamp);
    const now = Date.now();
    const fiveMinutes = 5 * 60 * 1000;

    if (Math.abs(now - messageTime) > fiveMinutes) {
      return false; // Message too old
    }

    return true;
  } catch (error) {
    console.error('Signature verification error:', error);
    return false;
  }
}

// Wallet authentication endpoint
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { walletAddress, signature, message } = walletLoginSchema.parse(body);

    // Verify signature
    const isValidSignature = verifyWalletSignature(walletAddress, message, signature);
    if (!isValidSignature) {
      return NextResponse.json(
        { error: 'Invalid signature' },
        { status: 401 }
      );
    }

    // Find or create user by wallet address
    let user = zionUsers.find((u: User) => u.walletAddress === walletAddress);

    if (!user) {
      // Create new user for this wallet
      user = {
        id: Date.now().toString(),
        username: `wallet_${walletAddress.slice(-8)}`,
        email: `${walletAddress.slice(-8)}@zion.wallet`,
        passwordHash: '', // No password for wallet auth
        apiKey: generateApiKey(),
        role: 'wallet_user',
        createdAt: new Date().toISOString(),
        walletAddress,
        dailyLimit: 5000.0, // Higher limit for wallet users
        totalVolume: 0.0,
      };
      zionUsers.push(user);
    }

    // Update last login
    user.lastLogin = new Date().toISOString();

    // Generate JWT token
    const token = jwt.sign(
      {
        userId: user.id,
        username: user.username,
        email: user.email,
        walletAddress: user.walletAddress,
        role: user.role,
        authType: 'wallet',
      },
      JWT_SECRET,
      { expiresIn: '7d' }
    );

    // Return user data (without password hash)
    const { passwordHash: _, ...userResponse } = user;

    return NextResponse.json({
      user: userResponse,
      token,
      message: 'Wallet authentication successful',
    });

  } catch (error) {
    if (error instanceof z.ZodError) {
      return NextResponse.json(
        { error: 'Invalid input', details: error.errors },
        { status: 400 }
      );
    }

    console.error('Wallet auth error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

// Get authentication message for wallet signing
export async function GET(request: NextRequest) {
  try {
    const timestamp = Date.now();
    const message = `ZION WARP Bridge Authentication\n\nWallet Address: [YOUR_WALLET_ADDRESS]\nTimestamp: ${timestamp}\n\nSign this message to authenticate with ZION.`;

    return NextResponse.json({
      message,
      timestamp,
      expiresIn: 300000, // 5 minutes
    });

  } catch (error) {
    console.error('Get auth message error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}