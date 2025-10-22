import { NextRequest, NextResponse } from 'next/server';
import jwt from 'jsonwebtoken';
import bcrypt from 'bcryptjs';
import { z } from 'zod';

// JWT Secret (in production, use environment variable)
const JWT_SECRET = process.env.JWT_SECRET || 'zion-warp-bridge-secret-key';

// User schema validation
const registerSchema = z.object({
  username: z.string().min(3).max(50),
  email: z.string().email(),
  password: z.string().min(8),
});

const loginSchema = z.object({
  email: z.string().email(),
  password: z.string().min(1),
});

// In-memory user store (in production, use database)
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
}

const users: User[] = [];

// Generate API key
function generateApiKey(): string {
  return 'zion_' + Math.random().toString(36).substr(2, 9) + Date.now().toString(36);
}

// Register endpoint
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { username, email, password } = registerSchema.parse(body);

    // Check if user already exists
    const existingUser = users.find(u => u.email === email || u.username === username);
    if (existingUser) {
      return NextResponse.json(
        { error: 'User already exists' },
        { status: 409 }
      );
    }

    // Hash password
    const passwordHash = await bcrypt.hash(password, 12);

    // Create user
    const user: User = {
      id: Date.now().toString(),
      username,
      email,
      passwordHash,
      apiKey: generateApiKey(),
      role: 'user',
      createdAt: new Date().toISOString(),
      dailyLimit: 1000.0, // $1000 daily limit
      totalVolume: 0.0,
    };

    users.push(user);

    // Generate JWT token
    const token = jwt.sign(
      {
        userId: user.id,
        username: user.username,
        email: user.email,
        role: user.role,
      },
      JWT_SECRET,
      { expiresIn: '7d' }
    );

    // Return user data (without password hash)
    const { passwordHash: _, ...userResponse } = user;

    return NextResponse.json({
      user: userResponse,
      token,
      message: 'Registration successful',
    });

  } catch (error) {
    if (error instanceof z.ZodError) {
      return NextResponse.json(
        { error: 'Invalid input', details: error.errors },
        { status: 400 }
      );
    }

    console.error('Registration error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}