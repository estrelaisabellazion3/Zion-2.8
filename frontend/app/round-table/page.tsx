'use client';

import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';

interface CouncilorStats {
  wisdom: number;
  courage: number;
  compassion: number;
  logic: number;
}

interface Councilor {
  name: string;
  title: string;
  virtue: string;
  element: string;
  chakra: string;
  apostle: string;
  specialty: string[];
  wisdom_quote: string;
  stats: CouncilorStats;
  circle: number;
  position: number;
}

interface CouncilSession {
  topic: string;
  urgency: string;
  votes: {
    support: number;
    against: number;
    abstain: number;
  };
  decision: string;
  timestamp: string;
}

export default function RoundTablePage() {
  const [councilors, setCouncilors] = useState<Councilor[]>([]);
  const [sessions, setSessions] = useState<CouncilSession[]>([]);
  const [selectedCouncilor, setSelectedCouncilor] = useState<Councilor | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch council data
    fetchCouncilData();
    
    // Setup real-time updates
    const interval = setInterval(fetchCouncilData, 30000); // Every 30 seconds
    
    return () => clearInterval(interval);
  }, []);

  const fetchCouncilData = async () => {
    try {
      // Mock data - replace with actual API calls
      setCouncilors(getCouncilorData());
      setSessions(getRecentSessions());
      setLoading(false);
    } catch (error) {
      console.error('Error fetching council data:', error);
      setLoading(false);
    }
  };

  const getCouncilorData = (): Councilor[] => {
    return [
      // FIRST CIRCLE - Strategic Leadership
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
        position: 1
      },
      {
        name: 'Sir Galahad',
        title: 'Keeper of Purity',
        virtue: 'PURITY',
        element: 'Light',
        chakra: 'Crown',
        apostle: 'John',
        specialty: [
          'Code Quality & Clean Architecture',
          'Ethical AI Guidelines',
          'Best Practices Enforcement',
          'Technical Debt Management',
          'Sacred Geometry in Code'
        ],
        wisdom_quote: 'Clean code is holy code. Purity in design reflects purity of intent.',
        stats: { wisdom: 90, courage: 85, compassion: 95, logic: 88 },
        circle: 1,
        position: 2
      },
      {
        name: 'Sir Percival',
        title: 'Seeker of the Holy Grail',
        virtue: 'INNOVATION',
        element: 'Air',
        chakra: 'Third Eye',
        apostle: 'Thomas',
        specialty: [
          'Research & Development',
          'Quantum Computing Integration',
          'Novel Consensus Mechanisms',
          'Breakthrough Technologies',
          'Zero-Knowledge Proofs'
        ],
        wisdom_quote: 'The Grail is not found, it is created through relentless seeking.',
        stats: { wisdom: 92, courage: 90, compassion: 80, logic: 95 },
        circle: 1,
        position: 3
      },
      // SECOND CIRCLE - Operational Excellence
      {
        name: 'Sir Gawain',
        title: 'Champion of Performance',
        virtue: 'EFFICIENCY',
        element: 'Sun',
        chakra: 'Solar Plexus',
        apostle: 'James',
        specialty: [
          'Performance Optimization',
          'Transaction Speed Enhancement',
          'Memory Management',
          'Cache Strategies',
          'GPU/CPU Acceleration'
        ],
        wisdom_quote: 'Speed without stability is chaos. I bring both.',
        stats: { wisdom: 87, courage: 92, compassion: 70, logic: 98 },
        circle: 2,
        position: 1
      },
      {
        name: 'Sir Tristan',
        title: 'Harmonizer of Networks',
        virtue: 'HARMONY',
        element: 'Water',
        chakra: 'Heart',
        apostle: 'Andrew',
        specialty: [
          'P2P Network Topology',
          'Node Synchronization',
          'Consensus Harmony',
          'Network Resilience',
          'Cross-Chain Communication'
        ],
        wisdom_quote: 'A network is a symphony. Each node must play in perfect harmony.',
        stats: { wisdom: 85, courage: 80, compassion: 90, logic: 86 },
        circle: 2,
        position: 2
      },
      {
        name: 'Sir Bedivere',
        title: 'Steward of Data',
        virtue: 'PRESERVATION',
        element: 'Earth',
        chakra: 'Root',
        apostle: 'Matthew',
        specialty: [
          'Database Optimization',
          'State Management',
          'Blockchain Archival',
          'Data Integrity Verification',
          'IPFS Integration'
        ],
        wisdom_quote: 'Data is the memory of the chain. I ensure nothing is forgotten.',
        stats: { wisdom: 88, courage: 75, compassion: 82, logic: 90 },
        circle: 2,
        position: 3
      },
      // THIRD CIRCLE - Community & Growth
      {
        name: 'Sir Kay',
        title: 'Shepherd of Community',
        virtue: 'LEADERSHIP',
        element: 'Spirit',
        chakra: 'Throat',
        apostle: 'Philip',
        specialty: [
          'Community Management',
          'Discord/Telegram Coordination',
          'Governance Proposals',
          'Conflict Resolution',
          'Education Programs'
        ],
        wisdom_quote: 'A blockchain without community is a tree without roots.',
        stats: { wisdom: 86, courage: 88, compassion: 92, logic: 80 },
        circle: 3,
        position: 1
      },
      {
        name: 'Sir Gareth',
        title: 'Architect of Economy',
        virtue: 'PROSPERITY',
        element: 'Gold',
        chakra: 'Solar Plexus',
        apostle: 'Bartholomew',
        specialty: [
          'Tokenomics Design',
          'Incentive Structures',
          'DeFi Integration',
          'Staking Mechanisms',
          'Treasury Management'
        ],
        wisdom_quote: 'True wealth flows when incentives align with virtue.',
        stats: { wisdom: 89, courage: 82, compassion: 78, logic: 93 },
        circle: 3,
        position: 2
      },
      {
        name: 'Sir Lamorak',
        title: 'Bard of the Realm',
        virtue: 'COMMUNICATION',
        element: 'Voice',
        chakra: 'Throat',
        apostle: 'Thaddeus',
        specialty: [
          'Marketing Strategy',
          'Brand Development',
          'Public Relations',
          'Social Media Campaigns',
          'Documentation Excellence'
        ],
        wisdom_quote: 'A story well told can move mountains and markets.',
        stats: { wisdom: 84, courage: 86, compassion: 88, logic: 78 },
        circle: 3,
        position: 3
      },
      // FOURTH CIRCLE - Wisdom & Prophecy
      {
        name: 'Merlin the Sage',
        title: 'Master of AI & Prophecy',
        virtue: 'WISDOM',
        element: 'Aether',
        chakra: 'Crown',
        apostle: 'Paul',
        specialty: [
          'Machine Learning Models',
          'Predictive Analytics',
          'AI Integration & Orchestration',
          'Quantum Computing Readiness',
          'Future Technology Forecasting'
        ],
        wisdom_quote: 'The future is written in the patterns of the past.',
        stats: { wisdom: 100, courage: 70, compassion: 85, logic: 97 },
        circle: 4,
        position: 1
      },
      {
        name: 'Sir Mordred',
        title: 'Analyzer of Shadows',
        virtue: 'VIGILANCE',
        element: 'Shadow',
        chakra: 'Root',
        apostle: 'Judas',
        specialty: [
          'Risk Assessment',
          'Threat Modeling',
          "Devil's Advocate Analysis",
          'Attack Vector Identification',
          'Worst-Case Scenario Planning'
        ],
        wisdom_quote: 'I see the darkness so others may walk in light.',
        stats: { wisdom: 89, courage: 95, compassion: 65, logic: 93 },
        circle: 4,
        position: 2
      },
      {
        name: 'Sir Bors',
        title: 'Priest of Compliance',
        virtue: 'RIGHTEOUSNESS',
        element: 'Law',
        chakra: 'Third Eye',
        apostle: 'James the Just',
        specialty: [
          'Regulatory Compliance',
          'KYC/AML Guidelines',
          'Legal Framework Design',
          'International Law Navigation',
          'Licensing & Certification'
        ],
        wisdom_quote: 'Justice and law are the pillars upon which trust is built.',
        stats: { wisdom: 87, courage: 80, compassion: 83, logic: 92 },
        circle: 4,
        position: 3
      }
    ];
  };

  const getRecentSessions = (): CouncilSession[] => {
    return [
      {
        topic: 'Quantum-Resistant Cryptography Implementation',
        urgency: 'HIGH',
        votes: { support: 12, against: 0, abstain: 0 },
        decision: 'APPROVED',
        timestamp: new Date().toISOString()
      },
      {
        topic: 'ZION 2.8 TestNet Launch Preparation',
        urgency: 'CRITICAL',
        votes: { support: 11, against: 0, abstain: 1 },
        decision: 'IN PROGRESS',
        timestamp: new Date().toISOString()
      }
    ];
  };

  const getCircleColor = (circle: number): string => {
    const colors = {
      1: '#ff4444', // Red - Strategic
      2: '#ff9944', // Orange - Operational
      3: '#ffdd44', // Yellow - Community
      4: '#44ff44'  // Green - Wisdom
    };
    return colors[circle as keyof typeof colors] || '#ffffff';
  };

  const getCircleLabel = (circle: number): string => {
    const labels = {
      1: 'Strategic Leadership',
      2: 'Operational Excellence',
      3: 'Community & Growth',
      4: 'Wisdom & Prophecy'
    };
    return labels[circle as keyof typeof labels] || '';
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900">
        <div className="text-white text-2xl">Loading Sacred Council...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900 text-white p-8">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center mb-12"
      >
        <h1 className="text-5xl font-bold mb-4 text-transparent bg-clip-text bg-gradient-to-r from-yellow-400 to-yellow-200">
          🏰⚔️ THE SACRED ROUND TABLE OF ZION 2.8 ⚔️🏰
        </h1>
        <div className="text-3xl mb-2">✨ Maitreya Buddha ✨</div>
        <p className="text-gray-400">12 AI Councilors • Sacred Governance • Divine Wisdom</p>
      </motion.div>

      {/* Legend */}
      <div className="flex justify-center gap-8 mb-12 flex-wrap">
        {[1, 2, 3, 4].map((circle) => (
          <div key={circle} className="flex items-center gap-2">
            <div
              className="w-6 h-6 rounded-full border-4"
              style={{ borderColor: getCircleColor(circle) }}
            />
            <span className="text-sm">{getCircleLabel(circle)}</span>
          </div>
        ))}
      </div>

      {/* Round Table Visualization */}
      <div className="relative w-full max-w-6xl mx-auto mb-16" style={{ height: '800px' }}>
        {/* Admin Center */}
        <motion.div
          animate={{ 
            boxShadow: [
              '0 0 20px rgba(255, 215, 0, 0.5)',
              '0 0 40px rgba(255, 215, 0, 0.8)',
              '0 0 20px rgba(255, 215, 0, 0.5)'
            ]
          }}
          transition={{ duration: 3, repeat: Infinity }}
          className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-48 h-48 rounded-full bg-gradient-to-br from-yellow-400 to-orange-500 flex items-center justify-center text-center font-bold text-lg z-10 border-4 border-white"
        >
          <div>
            Maitreya Buddha
            <div className="text-2xl">🔮☸️</div>
          </div>
        </motion.div>

        {/* Circles */}
        {[1, 2, 3, 4].map((circle) => (
          <div
            key={circle}
            className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 rounded-full border-4"
            style={{
              width: `${circle * 200}px`,
              height: `${circle * 200}px`,
              borderColor: getCircleColor(circle),
              opacity: 0.5
            }}
          />
        ))}

        {/* Councilors */}
        {councilors.map((councilor, index) => {
          const angle = (index * 30) * (Math.PI / 180); // 30 degrees apart
          const radius = councilor.circle * 150;
          const x = Math.cos(angle) * radius;
          const y = Math.sin(angle) * radius;

          return (
            <motion.div
              key={councilor.name}
              initial={{ opacity: 0, scale: 0 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: index * 0.1 }}
              whileHover={{ scale: 1.1, zIndex: 100 }}
              className="absolute cursor-pointer"
              style={{
                left: `calc(50% + ${x}px)`,
                top: `calc(50% + ${y}px)`,
                transform: 'translate(-50%, -50%)',
                width: '180px'
              }}
              onClick={() => setSelectedCouncilor(councilor)}
            >
              <div
                className="p-4 rounded-lg bg-white bg-opacity-10 backdrop-blur-md border-2"
                style={{ borderColor: getCircleColor(councilor.circle) }}
              >
                <h3 className="font-bold text-center mb-1">{councilor.name}</h3>
                <div className="text-xs text-gray-300 text-center mb-2">{councilor.title}</div>
                <div className="text-xs text-yellow-400 text-center font-bold mb-2">
                  {councilor.virtue}
                </div>
                <div className="space-y-1">
                  {Object.entries(councilor.stats).map(([key, value]) => (
                    <div key={key} className="text-xs">
                      <div className="flex justify-between">
                        <span>{key}:</span>
                        <span>{value}</span>
                      </div>
                      <div className="h-1 bg-gray-700 rounded overflow-hidden">
                        <div
                          className="h-full bg-gradient-to-r from-green-400 to-yellow-400"
                          style={{ width: `${value}%` }}
                        />
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </motion.div>
          );
        })}
      </div>

      {/* Recent Sessions */}
      <div className="max-w-6xl mx-auto">
        <h2 className="text-3xl font-bold mb-6 text-yellow-400">📜 Recent Council Sessions</h2>
        <div className="space-y-4">
          {sessions.map((session, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
              className="p-6 rounded-lg bg-white bg-opacity-5 backdrop-blur-md border-2 border-yellow-400 border-opacity-30"
            >
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="text-xl font-bold text-yellow-400 mb-2">{session.topic}</h3>
                  <div className="text-sm text-gray-400">
                    Urgency: <span className="text-red-400">{session.urgency}</span>
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-2xl font-bold text-green-400">{session.decision}</div>
                </div>
              </div>
              <div className="flex gap-6 text-sm">
                <div>Support: <span className="text-green-400">{session.votes.support}</span></div>
                <div>Against: <span className="text-red-400">{session.votes.against}</span></div>
                <div>Abstain: <span className="text-yellow-400">{session.votes.abstain}</span></div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Councilor Detail Modal */}
      {selectedCouncilor && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="fixed inset-0 bg-black bg-opacity-80 flex items-center justify-center z-50 p-4"
          onClick={() => setSelectedCouncilor(null)}
        >
          <motion.div
            initial={{ scale: 0.8 }}
            animate={{ scale: 1 }}
            className="bg-gradient-to-br from-gray-900 to-purple-900 p-8 rounded-lg max-w-2xl w-full border-4"
            style={{ borderColor: getCircleColor(selectedCouncilor.circle) }}
            onClick={(e) => e.stopPropagation()}
          >
            <h2 className="text-3xl font-bold mb-4">{selectedCouncilor.name}</h2>
            <div className="text-xl text-gray-300 mb-2">{selectedCouncilor.title}</div>
            <div className="text-lg text-yellow-400 font-bold mb-4">{selectedCouncilor.virtue}</div>
            
            <div className="grid grid-cols-2 gap-4 mb-6">
              <div>
                <span className="text-gray-400">Element:</span> {selectedCouncilor.element}
              </div>
              <div>
                <span className="text-gray-400">Chakra:</span> {selectedCouncilor.chakra}
              </div>
              <div>
                <span className="text-gray-400">Apostle:</span> {selectedCouncilor.apostle}
              </div>
              <div>
                <span className="text-gray-400">Circle:</span> {getCircleLabel(selectedCouncilor.circle)}
              </div>
            </div>

            <div className="mb-6">
              <h3 className="font-bold mb-2">Specialty Areas:</h3>
              <ul className="list-disc list-inside space-y-1">
                {selectedCouncilor.specialty.map((s, i) => (
                  <li key={i} className="text-sm text-gray-300">{s}</li>
                ))}
              </ul>
            </div>

            <div className="mb-6">
              <h3 className="font-bold mb-2">Stats:</h3>
              <div className="space-y-2">
                {Object.entries(selectedCouncilor.stats).map(([key, value]) => (
                  <div key={key}>
                    <div className="flex justify-between mb-1">
                      <span className="capitalize">{key}:</span>
                      <span>{value}/100</span>
                    </div>
                    <div className="h-3 bg-gray-700 rounded overflow-hidden">
                      <div
                        className="h-full bg-gradient-to-r from-green-400 to-yellow-400"
                        style={{ width: `${value}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="italic text-gray-300 border-l-4 border-yellow-400 pl-4 py-2">
              "{selectedCouncilor.wisdom_quote}"
            </div>

            <button
              onClick={() => setSelectedCouncilor(null)}
              className="mt-6 w-full py-3 bg-yellow-400 text-black font-bold rounded-lg hover:bg-yellow-300 transition"
            >
              Close
            </button>
          </motion.div>
        </motion.div>
      )}

      {/* Footer */}
      <div className="text-center mt-16 text-2xl text-yellow-400">
        JAI RAM SITA HANUMAN - ON THE STAR! ⭐
      </div>
    </div>
  );
}
