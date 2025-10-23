import { NextRequest, NextResponse } from 'next/server';
import jwt from 'jsonwebtoken';
import bcrypt from 'bcryptjs';
import { z } from 'zod';

// JWT Secret (in production, use environment variable)
const JWT_SECRET = process.env.JWT_SECRET || 'zion-warp-bridge-secret-key';

// Login schema validation
const loginSchema = z.object({
  email: z.string().email(),
  password: z.string().min(1),
});

// In-memory user store (in production, use database)
// This should be shared with register endpoint
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
  provider: 'local' | 'google';
}

// Global users store (in production, use proper database)
declare global {
  var zionUsers: User[] | undefined;
}

if (!global.zionUsers) {
  global.zionUsers = [];
}

const users = global.zionUsers;

// Login endpoint
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { email, password } = loginSchema.parse(body);

    // Find user
    const user = users.find(u => u.email === email);
    if (!user) {
      return NextResponse.json(
        { error: 'Invalid email or password' },
        { status: 401 }
      );
    }

    // Check if user is local (has password)
    if (user.provider !== 'local' || !user.passwordHash) {
      return NextResponse.json(
        { error: 'This account uses a different login method. Please use Google sign-in.' },
        { status: 401 }
      );
    }

    // Verify password
    const isValidPassword = await bcrypt.compare(password, user.passwordHash);
    if (!isValidPassword) {
      return NextResponse.json(
        { error: 'Invalid email or password' },
        { status: 401 }
      );
    }

    // Update last login
    user.lastLogin = new Date().toISOString();

    // Generate JWT token
    const token = jwt.sign(
      {
        userId: user.id,
        username: user.username,
        email: user.email,
        role: user.role,
        provider: user.provider,
      },
      JWT_SECRET,
      { expiresIn: '7d' }
    );

    // Return user data (without password hash)
    const { passwordHash: _, ...userResponse } = user;

    return NextResponse.json({
      user: userResponse,
      token,
      message: 'Login successful',
    });

  } catch (error) {
    if (error instanceof z.ZodError) {
      return NextResponse.json(
        { error: 'Invalid input', details: error.errors },
        { status: 400 }
      );
    }

    console.error('Login error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}