// ZION 2.8.1 "Estrella" - Production Data Types
// WARP Engine Era - Multi-Chain, Consciousness Mining, Lightning Network

export interface ZionProductionStats {
  timestamp: string;
  source: 'production-91.98.122.165';
  simulation: false;
  version: '2.8.1-production';

  // Multi-algorithm mining pool data (2.8.1)
  mining?: {
    hashrate: number;
    miners_connected: number;
    blocks_found: number;
    difficulty: number;
    algorithms: string[];
    current_algorithm: string;
    pool_address: string;
    shares_accepted: number;
    shares_rejected: number;
    consciousness_miners: number;
    total_xp_awarded: number;
  };

  // Enhanced blockchain data (2.8.1)
  blockchain?: {
    height: number;
    hash: string;
    difficulty: number;
    network_hashrate: number;
    tx_count: number;
    mempool_size: number;
    warp_transfers: number;
    lightning_channels: number;
  };

  // Enhanced node status (2.8.1)
  node?: {
    peers: number;
    sync_progress: number;
    uptime: number;
    version: string;
    warp_engine_status: 'active' | 'standby' | 'error';
    consciousness_level: string;
  };

  // WARP Bridge status (2.8.1)
  warp?: {
    chains: string[];
    transfers_total: number;
    volume_24h: number;
    status: 'operational' | 'syncing' | 'error';
    average_transfer_time: number;
    success_rate: number;
    supported_assets: string[];
  };

  // Consciousness Mining Game (2.8.1)
  consciousness?: {
    total_miners: number;
    total_xp: number;
    active_level: string;
    achievements_unlocked: number;
    meditation_sessions: number;
  };

  // Lightning Network (2.8.1)
  lightning?: {
    channels: number;
    capacity: number;
    local_balance: number;
    remote_balance: number;
    active_channels: number;
    pending_channels: number;
    node_alias: string;
    node_id: string;
  };
}

export interface ZionRealTimeConfig {
  productionServer: '91.98.122.165';
  noSimulations: true;
  realDataOnly: true;
  warpEngineVersion: '2.8.1';
  endpoints: {
    miningPool: 'http://91.98.122.165:3335';
    blockchain: 'http://91.98.122.165:18089';
    warpBridge: 'http://91.98.122.165:9000';
    consciousnessGame: 'http://91.98.122.165:9001';
    lightningNetwork: 'http://91.98.122.165:9002';
  };
}

// ============================================================================
// WARP BRIDGE TYPES (2.8.1)
// ============================================================================

export interface WarpTransaction {
  tx_id: string;
  source_chain: WarpChainType;
  destination_chain: WarpChainType;
  amount: number;
  asset: string;
  status: 'pending' | 'confirmed' | 'completed' | 'failed';
  lightning_payment_hash?: string;
  ankr_rpc_calls: number;
  total_time_ms: number;
  fee_total: number;
  timestamp: string;
  user_id?: string;
  recipient_address?: string;
}

export enum WarpChainType {
  ZION = 'zion',
  ETHEREUM = 'ethereum',
  POLYGON = 'polygon',
  ARBITRUM = 'arbitrum',
  OPTIMISM = 'optimism',
  AVALANCHE = 'avalanche',
  BSC = 'bsc',
  SOLANA = 'solana',
  FANTOM = 'fantom',
  GNOSIS = 'gnosis',
  BASE = 'base',
  CELO = 'celo'
}

export interface WarpStats {
  status: 'operational' | 'maintenance' | 'error';
  supportedChains: string[];
  activeTransfers: number;
  totalTransferred: number;
  averageTransferTime: number;
  successRate: number;
  supportedAssets: string[];
}

// ============================================================================
// CONSCIOUSNESS MINING GAME TYPES (2.8.1)
// ============================================================================

export interface ConsciousnessMiner {
  address: string;
  level: ConsciousnessLevel;
  xp: number;
  achievements: number;
  meditation_sessions: number;
  last_active: number;
}

export enum ConsciousnessLevel {
  AWAKENING = 'AWAKENING',
  MENTAL = 'MENTAL',
  SPIRITUAL = 'SPIRITUAL',
  COSMIC = 'COSMIC',
  ENLIGHTENED = 'ENLIGHTENED'
}

export interface ConsciousnessAchievement {
  id: string;
  name: string;
  description: string;
  unlocked: boolean;
  xp_reward: number;
  rarity: 'common' | 'rare' | 'epic' | 'legendary';
}

export interface ConsciousnessStats {
  miners: ConsciousnessMiner[];
  leaderboard: Array<{ rank: number; address: string; xp: number }>;
  achievements: ConsciousnessAchievement[];
  totalMiners: number;
  totalXP: number;
  activeLevel: string;
}

// ============================================================================
// LIGHTNING NETWORK TYPES (2.8.1)
// ============================================================================

export interface LightningChannel {
  id: string;
  capacity: number;
  localBalance: number;
  remoteBalance: number;
  active: boolean;
  peerAlias?: string;
  channelPoint: string;
  uptime: number;
}

export interface LightningPayment {
  paymentHash: string;
  amount: number;
  fee: number;
  status: 'pending' | 'succeeded' | 'failed';
  timestamp: string;
  description?: string;
  invoice?: string;
}

export interface LightningInvoice {
  paymentHash: string;
  paymentRequest: string;
  amount: number;
  description: string;
  expiry: number;
  timestamp: string;
  settled: boolean;
}

export interface LightningStats {
  channels: LightningChannel[];
  payments: LightningPayment[];
  invoices: LightningInvoice[];
  totalCapacity: number;
  totalLocalBalance: number;
  totalRemoteBalance: number;
  activeChannels: number;
  pendingChannels: number;
  nodeAlias: string;
  nodeId: string;
}

// ============================================================================
// MULTI-ALGORITHM MINING POOL TYPES (2.8.1)
// ============================================================================

export interface PoolMiner {
  address: string;
  hashrate: number;
  shares: number;
  algorithm: MiningAlgorithm;
  lastSeen: number;
  worker_count: number;
  total_earned: number;
}

export enum MiningAlgorithm {
  RANDOMX = 'randomx',
  YESCRYPT = 'yescrypt',
  AUTOLYKOS2 = 'autolykos2'
}

export interface PoolBlock {
  height: number;
  hash: string;
  timestamp: number;
  reward: number;
  miner: string;
  algorithm: MiningAlgorithm;
  difficulty: number;
}

export interface PoolStats {
  algorithms: string[];
  totalMiners: number;
  totalHashrate: number;
  blocksFound: number;
  currentDifficulty: number;
  miners: PoolMiner[];
  blocks: PoolBlock[];
  consciousnessMiners: number;
  totalXPAwarded: number;
}

// ============================================================================
// MONITORING TYPES (2.8.1)
// ============================================================================

export interface HealthCheck {
  component: string;
  status: 'healthy' | 'degraded' | 'unhealthy' | 'offline';
  last_check: number;
  response_time: number;
  error_message?: string;
  metrics?: Record<string, any>;
}

export interface MonitoringStats {
  uptime: number;
  total_requests: number;
  error_rate: number;
  avg_response_time: number;
  components: HealthCheck[];
  alerts: Alert[];
}

export interface Alert {
  id: string;
  severity: 'info' | 'warning' | 'error' | 'critical';
  message: string;
  timestamp: number;
  resolved: boolean;
}