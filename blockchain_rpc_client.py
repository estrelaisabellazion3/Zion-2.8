#!/usr/bin/env python3
"""
ZION Blockchain RPC Client for Pool Integration
Communicates with running blockchain process via HTTP RPC
"""

import requests
import json
import logging
import time
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)

class ZionBlockchainRPCClient:
    """RPC client to communicate with blockchain process via HTTP"""
    
    def __init__(self, host: str = 'localhost', port: int = 8545):
        self.host = host
        self.port = port
        self.url = f"http://{host}:{port}"
        self.rpc_id = 0
        self.session = requests.Session()
        self.session.timeout = 10  # 10 second timeout
    
    def _send_rpc(self, method: str, params: List[Any] = None) -> Optional[Dict]:
        """Send JSON-RPC request to blockchain via HTTP"""
        if params is None:
            params = []
        
        self.rpc_id += 1
        request = {
            "jsonrpc": "2.0",
            "id": self.rpc_id,
            "method": method,
            "params": params
        }
        
        try:
            headers = {'Content-Type': 'application/json'}
            response = self.session.post(self.url, json=request, headers=headers, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            if "error" in result and result["error"] is not None:
                logger.error(f"RPC error: {result['error']}")
                return None
            return result
            
        except requests.exceptions.RequestException as e:
            logger.debug(f"HTTP RPC connection error: {e}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"❌ Invalid JSON response: {e}")
            return None
    
    # ==========================================
    # BLOCKCHAIN QUERIES
    # ==========================================
    
    def get_height(self) -> int:
        """Get current blockchain height"""
        try:
            response = self._send_rpc("getblockcount")
            if response and "result" in response:
                return response["result"]
        except Exception as e:
            logger.error(f"Failed to get height: {e}")
        return -1
    
    def get_block(self, height: int) -> Optional[Dict]:
        """Get block by height"""
        try:
            response = self._send_rpc("getblock", [height])
            if response and "result" in response:
                return response["result"]
        except Exception as e:
            logger.error(f"Failed to get block {height}: {e}")
        return None
    
    def get_balance(self, address: str) -> float:
        """Get balance for address"""
        try:
            response = self._send_rpc("getbalance", [address])
            if response and "result" in response:
                return response["result"]
        except Exception as e:
            logger.error(f"Failed to get balance for {address}: {e}")
        return 0.0
    
    def get_pending_transactions(self) -> List[Dict]:
        """Get pending transactions in mempool"""
        try:
            response = self._send_rpc("getrawmempool", [True])  # verbose=true
            if response and "result" in response:
                return response["result"]
        except Exception as e:
            logger.error(f"Failed to get pending transactions: {e}")
        return []
    
    # ==========================================
    # BLOCKCHAIN MUTATIONS
    # ==========================================
    
    def create_transaction(self, from_addr: str, to_addr: str, amount: float, message: str = "") -> Optional[str]:
        """
        Create a transaction
        Returns transaction hash if successful
        """
        try:
            response = self._send_rpc("sendtransaction", [from_addr, to_addr, amount, message])
            if response and "result" in response:
                return response["result"]  # Returns tx hash
            else:
                logger.error(f"RPC error: {response}")
        except Exception as e:
            logger.error(f"Failed to create transaction: {e}")
        return None
    
    def mine_block(self, coinbase_address: str) -> Optional[str]:
        """
        Mine one block
        Returns block hash if successful
        """
        try:
            response = self._send_rpc("mine_block", [coinbase_address])
            if response and "result" in response:
                return response["result"]  # Returns block hash
            else:
                logger.error(f"RPC error: {response}")
        except Exception as e:
            logger.error(f"Failed to mine block: {e}")
        return None
    
    def submit_share(self, nonce: str, job_id: str, address: str) -> bool:
        """
        Submit a share (for share tracking without mining full block)
        """
        try:
            response = self._send_rpc("submit_share", [nonce, job_id, address])
            if response and "result" in response:
                return response["result"]
        except Exception as e:
            logger.error(f"Failed to submit share: {e}")
        return False
    
    # ==========================================
    # UTILITY METHODS
    # ==========================================
    
    def health_check(self) -> bool:
        """Check if blockchain is alive"""
        try:
            response = self._send_rpc("getblockcount")
            return response is not None and "result" in response
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False
    
    def close(self):
        """Close HTTP session"""
        if self.session:
            self.session.close()


# ==========================================
# TESTING
# ==========================================

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Test connection
    client = ZionBlockchainRPCClient()
    
    if client.health_check():
        print("✅ Blockchain RPC is alive!")
        height = client.get_height()
        print(f"Current height: {height}")
    else:
        print("❌ Cannot connect to blockchain RPC")
    
    client.close()
