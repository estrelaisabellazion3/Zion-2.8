"""
ZION RPC Client for Testing

This module provides a simple RPC client for interacting with the ZION blockchain
during testing. It wraps the JSON-RPC 2.0 protocol used by the zion-cli.
"""

import json
import requests
from typing import Any, Dict, List, Optional, Union
from requests.auth import HTTPBasicAuth


class ZionRPCClient:
    """Client for making RPC calls to ZION blockchain node."""
    
    def __init__(
        self,
        host: str = "localhost",
        port: int = 8332,
        username: str = "zionrpc",
        password: str = "zionpass",
        timeout: int = 30,
        use_https: bool = False
    ):
        """
        Initialize ZION RPC client.
        
        Args:
            host: Node hostname or IP address
            port: RPC port (default: 8332)
            username: RPC username
            password: RPC password
            timeout: Request timeout in seconds
            use_https: Use HTTPS instead of HTTP
        """
        protocol = "https" if use_https else "http"
        self.url = f"{protocol}://{host}:{port}"
        self.auth = HTTPBasicAuth(username, password)
        self.timeout = timeout
        self.request_id = 0
        
    def _call(self, method: str, params: Optional[List[Any]] = None) -> Any:
        """
        Make RPC call to node.
        
        Args:
            method: RPC method name
            params: Method parameters (optional)
            
        Returns:
            Result from RPC call
            
        Raises:
            RPCError: If RPC call fails
        """
        self.request_id += 1
        
        payload = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": method,
            "params": params or []
        }
        
        try:
            response = requests.post(
                self.url,
                json=payload,
                auth=self.auth,
                timeout=self.timeout,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            
            data = response.json()
            
            if "error" in data and data["error"] is not None:
                raise RPCError(
                    code=data["error"].get("code", -1),
                    message=data["error"].get("message", "Unknown error")
                )
                
            return data.get("result")
            
        except requests.exceptions.RequestException as e:
            raise RPCError(code=-1, message=f"Connection error: {str(e)}")
    
    # Blockchain Methods
    def getinfo(self) -> Dict[str, Any]:
        """Get general blockchain information."""
        return self._call("getinfo")
    
    def getblockchaininfo(self) -> Dict[str, Any]:
        """Get blockchain state information."""
        return self._call("getblockchaininfo")
    
    def getblockcount(self) -> int:
        """Get current block height."""
        return self._call("getblockcount")
    
    def getblockhash(self, height: int) -> str:
        """Get block hash at given height."""
        return self._call("getblockhash", [height])
    
    def getblock(self, block_hash: str, verbosity: int = 1) -> Union[str, Dict]:
        """Get block data."""
        return self._call("getblock", [block_hash, verbosity])
    
    def getdifficulty(self) -> float:
        """Get current mining difficulty."""
        return self._call("getdifficulty")
    
    # Wallet Methods
    def getnewaddress(self, label: str = "") -> str:
        """Generate new receiving address."""
        return self._call("getnewaddress", [label])
    
    def getbalance(self, account: str = "*", minconf: int = 1) -> float:
        """Get wallet balance."""
        return self._call("getbalance", [account, minconf])
    
    def listunspent(
        self,
        minconf: int = 1,
        maxconf: int = 9999999,
        addresses: Optional[List[str]] = None
    ) -> List[Dict]:
        """List unspent transaction outputs."""
        params = [minconf, maxconf]
        if addresses:
            params.append(addresses)
        return self._call("listunspent", params)
    
    def listtransactions(
        self,
        account: str = "*",
        count: int = 10,
        skip: int = 0
    ) -> List[Dict]:
        """List recent transactions."""
        return self._call("listtransactions", [account, count, skip])
    
    def gettransaction(self, txid: str) -> Dict[str, Any]:
        """Get detailed transaction information."""
        return self._call("gettransaction", [txid])
    
    def sendtoaddress(
        self,
        address: str,
        amount: float,
        comment: str = "",
        comment_to: str = ""
    ) -> str:
        """Send ZION to address. Returns transaction ID."""
        params = [address, amount]
        if comment:
            params.append(comment)
        if comment_to:
            params.append(comment_to)
        return self._call("sendtoaddress", params)
    
    def sendmany(
        self,
        from_account: str,
        amounts: Dict[str, float],
        minconf: int = 1,
        comment: str = ""
    ) -> str:
        """Send to multiple addresses. Returns transaction ID."""
        params = [from_account, amounts, minconf]
        if comment:
            params.append(comment)
        return self._call("sendmany", params)
    
    # Mining Methods
    def getmininginfo(self) -> Dict[str, Any]:
        """Get mining-related information."""
        return self._call("getmininginfo")
    
    def getnetworkhashps(self, blocks: int = 120, height: int = -1) -> float:
        """Get estimated network hash rate."""
        return self._call("getnetworkhashps", [blocks, height])
    
    def getblocktemplate(self, rules: Optional[List[str]] = None) -> Dict:
        """Get block template for mining."""
        params = []
        if rules:
            params.append({"rules": rules})
        return self._call("getblocktemplate", params)
    
    def submitblock(self, hexdata: str) -> Optional[str]:
        """Submit mined block. Returns None on success."""
        return self._call("submitblock", [hexdata])
    
    # Network Methods
    def getpeerinfo(self) -> List[Dict]:
        """Get information about connected peers."""
        return self._call("getpeerinfo")
    
    def getconnectioncount(self) -> int:
        """Get number of connections to other nodes."""
        return self._call("getconnectioncount")
    
    def getnetworkinfo(self) -> Dict[str, Any]:
        """Get network information."""
        return self._call("getnetworkinfo")
    
    def addnode(self, node: str, command: str = "add") -> None:
        """Add or remove node from peer list."""
        self._call("addnode", [node, command])
    
    # Utility Methods
    def validateaddress(self, address: str) -> Dict[str, Any]:
        """Validate ZION address."""
        return self._call("validateaddress", [address])
    
    def estimatefee(self, nblocks: int = 6) -> float:
        """Estimate transaction fee."""
        return self._call("estimatefee", [nblocks])
    
    def help(self, command: str = "") -> str:
        """Get help for RPC commands."""
        params = [command] if command else []
        return self._call("help", params)


class RPCError(Exception):
    """Exception raised for RPC errors."""
    
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message
        super().__init__(f"RPC Error {code}: {message}")


# Convenience function for quick client creation
def get_rpc_client(
    host: str = "localhost",
    port: int = 8332,
    username: str = "zionrpc",
    password: str = "zionpass"
) -> ZionRPCClient:
    """
    Get configured RPC client.
    
    Args:
        host: Node hostname
        port: RPC port
        username: RPC username
        password: RPC password
        
    Returns:
        Configured ZionRPCClient instance
    """
    return ZionRPCClient(host=host, port=port, username=username, password=password)
