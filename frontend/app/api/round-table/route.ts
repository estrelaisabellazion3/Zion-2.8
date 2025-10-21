import { NextRequest, NextResponse } from 'next/server';

// Mock data - replace with actual Python backend integration
const COUNCILORS = [
  {
    name: 'Sir Lancelot',
    title: 'Guardian of Security',
    virtue: 'PROTECTION',
    element: 'Fire',
    chakra: 'Root',
    apostle: 'Peter',
    specialty: [
      'Cryptography & Encryption',
      'Penetration Testing',
      'Threat Detection',
      'Private Key Protection',
      'Smart Contract Auditing'
    ],
    wisdom_quote: 'A chain is only as strong as its weakest link. I protect every link.',
    stats: { wisdom: 95, courage: 100, compassion: 75, logic: 90 },
    circle: 1,
    position: 1,
    ai_integration: 'Security Monitor',
    status: 'active'
  },
  // Add more councilors...
];

const SESSIONS = [
  {
    id: 1,
    topic: 'Quantum-Resistant Cryptography Implementation',
    urgency: 'HIGH',
    votes: { support: 12, against: 0, abstain: 0 },
    decision: 'APPROVED',
    admin_reasoning: 'The Council has spoken with 12 voices in favor. Quantum protection shall be our shield.',
    timestamp: new Date().toISOString(),
    councilors_present: 12
  },
  {
    id: 2,
    topic: 'ZION 2.8 TestNet Launch Preparation',
    urgency: 'CRITICAL',
    votes: { support: 11, against: 0, abstain: 1 },
    decision: 'IN PROGRESS',
    admin_reasoning: 'The sacred preparations continue. The TestNet shall rise with divine perfection.',
    timestamp: new Date().toISOString(),
    councilors_present: 12
  }
];

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const action = searchParams.get('action');

  try {
    switch (action) {
      case 'councilors':
        return NextResponse.json({
          success: true,
          data: {
            admin: 'Maitreya Buddha',
            total_councilors: 12,
            councilors: COUNCILORS
          }
        });

      case 'sessions':
        const limit = parseInt(searchParams.get('limit') || '10');
        return NextResponse.json({
          success: true,
          data: {
            total_sessions: SESSIONS.length,
            sessions: SESSIONS.slice(0, limit)
          }
        });

      case 'status':
        return NextResponse.json({
          success: true,
          data: {
            admin: 'Maitreya Buddha',
            councilors: 12,
            active_councilors: 12,
            sessions_held: SESSIONS.length,
            decisions_made: SESSIONS.filter(s => s.decision === 'APPROVED').length,
            ai_integrations: 3,
            initialized: true,
            timestamp: new Date().toISOString()
          }
        });

      case 'councilor':
        const name = searchParams.get('name');
        const councilor = COUNCILORS.find(c => 
          c.name.toLowerCase().includes(name?.toLowerCase() || '')
        );
        
        if (!councilor) {
          return NextResponse.json({
            success: false,
            error: 'Councilor not found'
          }, { status: 404 });
        }

        return NextResponse.json({
          success: true,
          data: councilor
        });

      default:
        return NextResponse.json({
          success: true,
          data: {
            message: 'ZION 2.8 Round Table Council API',
            endpoints: {
              'GET ?action=councilors': 'Get all councilors',
              'GET ?action=sessions&limit=10': 'Get recent council sessions',
              'GET ?action=status': 'Get system status',
              'GET ?action=councilor&name=lancelot': 'Get specific councilor',
              'POST': 'Convene council session'
            }
          }
        });
    }
  } catch (error) {
    console.error('Round Table API error:', error);
    return NextResponse.json({
      success: false,
      error: 'Internal server error'
    }, { status: 500 });
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { action, topic, urgency = 'normal' } = body;

    if (action === 'convene') {
      // Simulate council decision
      const newSession = {
        id: SESSIONS.length + 1,
        topic: topic || 'General Council Session',
        urgency: urgency.toUpperCase(),
        votes: { 
          support: Math.floor(Math.random() * 3) + 10, 
          against: Math.floor(Math.random() * 2), 
          abstain: Math.floor(Math.random() * 2) 
        },
        decision: 'APPROVED',
        admin_reasoning: 'The Council has deliberated and reached divine consensus.',
        timestamp: new Date().toISOString(),
        councilors_present: 12
      };

      SESSIONS.unshift(newSession);

      return NextResponse.json({
        success: true,
        data: {
          message: 'Council session convened successfully',
          session: newSession
        }
      });
    }

    return NextResponse.json({
      success: false,
      error: 'Invalid action'
    }, { status: 400 });

  } catch (error) {
    console.error('Round Table POST error:', error);
    return NextResponse.json({
      success: false,
      error: 'Invalid request body'
    }, { status: 400 });
  }
}
