// ZION 2.7.5 TestNet - Real Production Data Fetcher
// Connects ONLY to production server 91.98.122.165
// NO MOCK DATA, NO SIMULATIONS

import { ZionProductionStats } from '../types/production';

export class ZionProductionClient {
  private readonly SERVER = '91.98.122.165';
  private readonly ENDPOINTS = {
    mining: `http://${this.SERVER}:3335/stats`,
    blockchain: `http://${this.SERVER}:18089/get_info`, 
    bridge: `http://${this.SERVER}:9000/api/status`
  };

  async fetchRealStats(): Promise<ZionProductionStats> {
    const timestamp = new Date().toISOString();
    const stats: ZionProductionStats = {
      timestamp,
      source: 'production-91.98.122.165',
      simulation: false,
      version: '2.7.5-production'
    };

    try {
      // Real mining pool data
      const miningResponse = await fetch(this.ENDPOINTS.mining, { 
        signal: AbortSignal.timeout(5000) 
      });
      if (miningResponse.ok) {
        const miningData = await miningResponse.json();
        stats.mining = {
          hashrate: miningData.hashrate || 0,
          miners_connected: miningData.miners || 0,
          blocks_found: miningData.blocks || 0,
          difficulty: miningData.difficulty || 0,
          algorithm: 'RandomX',
          pool_address: miningData.address || '',
          shares_accepted: miningData.shares_accepted || 0,
          shares_rejected: miningData.shares_rejected || 0
        };
      }
    } catch (error) {
      console.error('Mining pool fetch failed:', error);
    }

    try {
      // Real blockchain data  
      const blockchainResponse = await fetch(this.ENDPOINTS.blockchain, {
        signal: AbortSignal.timeout(5000)
      });
      if (blockchainResponse.ok) {
        const blockchainData = await blockchainResponse.json();
        stats.blockchain = {
          height: blockchainData.height || 0,
          hash: blockchainData.top_block_hash || '',
          difficulty: blockchainData.difficulty || 0,
          network_hashrate: blockchainData.hashrate || 0,
          tx_count: blockchainData.tx_count || 0,
          mempool_size: blockchainData.tx_pool_size || 0
        };
      }
    } catch (error) {
      console.error('Blockchain fetch failed:', error);
    }

    try {
      // Real bridge data
      const bridgeResponse = await fetch(this.ENDPOINTS.bridge, {
        signal: AbortSignal.timeout(5000)
      });
      if (bridgeResponse.ok) {
        const bridgeData = await bridgeResponse.json();
        stats.bridge = {
          chains: bridgeData.chains || [],
          transfers_total: bridgeData.transfers || 0,
          volume_24h: bridgeData.volume || 0,
          status: bridgeData.status || 'error'
        };
      }
    } catch (error) {
      console.error('Bridge fetch failed:', error);
    }

    return stats;
  }

  // Health check - ping production server
  async isProductionOnline(): Promise<boolean> {
    try {
      const response = await fetch(`http://${this.SERVER}:18089/get_height`, {
        signal: AbortSignal.timeout(3000)
      });
      return response.ok;
    } catch {
      return false;
    }
  }
}