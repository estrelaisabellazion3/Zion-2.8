// ZION 2.7.5 TestNet - Production Data Types
// NO SIMULATIONS - Only real production server data

export interface ZionProductionStats {
  timestamp: string;
  source: 'production-91.98.122.165';
  simulation: false;
  version: '2.7.5-production';
  
  // Real mining pool data
  mining?: {
    hashrate: number;
    miners_connected: number;
    blocks_found: number;
    difficulty: number;
    algorithm: 'RandomX';
    pool_address: string;
    shares_accepted: number;
    shares_rejected: number;
  };
  
  // Real blockchain data
  blockchain?: {
    height: number;
    hash: string;
    difficulty: number;
    network_hashrate: number;
    tx_count: number;
    mempool_size: number;
  };
  
  // Real node status
  node?: {
    peers: number;
    sync_progress: number;
    uptime: number;
    version: string;
  };
  
  // Real bridge status
  bridge?: {
    chains: string[];
    transfers_total: number;
    volume_24h: number;
    status: 'active' | 'syncing' | 'error';
  };
}

export interface ZionRealTimeConfig {
  productionServer: '91.98.122.165';
  noSimulations: true;
  realDataOnly: true;
  endpoints: {
    miningPool: 'http://91.98.122.165:3335';
    blockchain: 'http://91.98.122.165:18089';
    bridge: 'http://91.98.122.165:9000';
  };
}