#!/usr/bin/env python3
"""
ZION Blockchain RPC Client for Pool Integration
Communicates with running blockchain process via RPC
"""

import socket
import json
import logging
import time
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)

class ZionBlockchainRPCClient:
    """RPC client to communicate with blockchain process"""
    
    def __init__(self, host: str = 'localhost', port: int = 8545):
        self.host = host
        self.port = port
        self.rpc_id = 0
        self.socket = None
        self.connected = False
        self._connect()
    
    def _connect(self) -> bool:
        """Connect to blockchain RPC server"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(5)
            self.socket.connect((self.host, self.port))
            self.connected = True
            logger.info(f"✅ Connected to blockchain RPC at {self.host}:{self.port}")
            return True
        except Exception as e:
            logger.warning(f"⚠️  Failed to connect to blockchain RPC: {e}")
            self.connected = False
            return False
    
    def _send_rpc(self, method: str, params: List[Any] = None) -> Optional[Dict]:
        """Send JSON-RPC request to blockchain"""
        if not self.connected:
            if not self._connect():
                return None
        
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
            # Send request
            request_json = json.dumps(request)
            self.socket.sendall(request_json.encode() + b'\n')
            
            # Receive response
            response_data = b''
            while True:
                chunk = self.socket.recv(4096)
                if not chunk:
                    break
                response_data += chunk
                # Try to parse complete JSON
                try:
                    response = json.loads(response_data)
                    return response
                except json.JSONDecodeError:
                    continue
            
            return None
        except Exception as e:
            logger.error(f"❌ RPC error: {e}")
            self.connected = False
            self._connect()  # Try to reconnect
            return None
    
    # ==========================================
    # BLOCKCHAIN QUERIES
    # ==========================================
    
    def get_height(self) -> int:
        """Get current blockchain height"""
        try:
            response = self._send_rpc("get_height")
            if response and "result" in response:
                return response["result"]
        except Exception as e:
            logger.error(f"Failed to get height: {e}")
        return -1
    
    def get_block(self, height: int) -> Optional[Dict]:
        """Get block by height"""
        try:
            response = self._send_rpc("get_block", [height])
            if response and "result" in response:
                return response["result"]
        except Exception as e:
            logger.error(f"Failed to get block {height}: {e}")
        return None
    
    def get_balance(self, address: str) -> float:
        """Get balance for address"""
        try:
            response = self._send_rpc("get_balance", [address])
            if response and "result" in response:
                return response["result"]
        except Exception as e:
            logger.error(f"Failed to get balance for {address}: {e}")
        return 0.0
    
    def get_pending_transactions(self) -> List[Dict]:
        """Get pending transactions in mempool"""
        try:
            response = self._send_rpc("get_pending_transactions")
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
            response = self._send_rpc("create_transaction", [from_addr, to_addr, amount, message])
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
            response = self._send_rpc("get_height")
            return response is not None and "result" in response
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False
    
    def close(self):
        """Close RPC connection"""
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
        self.connected = False


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
