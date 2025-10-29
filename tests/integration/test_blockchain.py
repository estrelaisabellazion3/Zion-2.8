"""
Integration tests for ZION blockchain core functionality.

Tests blockchain info, block retrieval, difficulty, and basic queries.
"""

import pytest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rpc_client import get_rpc_client, RPCError


@pytest.fixture(scope="module")
def rpc():
    """Fixture providing RPC client for all tests."""
    return get_rpc_client()


@pytest.mark.integration
class TestBlockchainInfo:
    """Test blockchain information retrieval."""
    
    def test_getinfo(self, rpc):
        """Test getinfo RPC call."""
        info = rpc.getinfo()
        
        assert info is not None
        assert "version" in info
        assert "blocks" in info
        assert "connections" in info
        assert "difficulty" in info
        
        # Verify data types
        assert isinstance(info["version"], (int, str))
        assert isinstance(info["blocks"], int)
        assert isinstance(info["connections"], int)
        assert isinstance(info["difficulty"], (int, float))
        
        # Verify reasonable values
        assert info["blocks"] >= 0
        assert info["connections"] >= 0
        assert info["difficulty"] >= 0
        
    def test_getblockchaininfo(self, rpc):
        """Test getblockchaininfo RPC call."""
        info = rpc.getblockchaininfo()
        
        assert info is not None
        assert "chain" in info
        assert "blocks" in info
        assert "headers" in info
        assert "difficulty" in info
        
        # Verify chain name
        assert info["chain"] in ["main", "test", "regtest"]
        
        # Headers should be >= blocks (synced or ahead)
        assert info["headers"] >= info["blocks"]
        
    def test_getblockcount(self, rpc):
        """Test getblockcount RPC call."""
        count = rpc.getblockcount()
        
        assert isinstance(count, int)
        assert count >= 0
        
        # Compare with getinfo
        info = rpc.getinfo()
        assert count == info["blocks"]
        
    def test_getdifficulty(self, rpc):
        """Test getdifficulty RPC call."""
        difficulty = rpc.getdifficulty()
        
        assert isinstance(difficulty, (int, float))
        assert difficulty >= 0
        
        # Should match difficulty from getinfo
        info = rpc.getinfo()
        assert abs(difficulty - info["difficulty"]) < 0.01


@pytest.mark.integration
class TestBlockRetrieval:
    """Test block hash and data retrieval."""
    
    def test_getblockhash(self, rpc):
        """Test getblockhash for genesis block."""
        # Genesis block is always at height 0
        genesis_hash = rpc.getblockhash(0)
        
        assert isinstance(genesis_hash, str)
        assert len(genesis_hash) == 64  # SHA-256 hash in hex
        
        # Verify it's valid hex
        int(genesis_hash, 16)  # Should not raise
        
    def test_getblockhash_current(self, rpc):
        """Test getblockhash for current block."""
        block_count = rpc.getblockcount()
        
        if block_count > 0:
            latest_hash = rpc.getblockhash(block_count)
            assert isinstance(latest_hash, str)
            assert len(latest_hash) == 64
            
    def test_getblockhash_invalid(self, rpc):
        """Test getblockhash with invalid height."""
        block_count = rpc.getblockcount()
        
        # Try to get block that doesn't exist yet
        with pytest.raises(RPCError) as exc_info:
            rpc.getblockhash(block_count + 1000)
        
        # Should get error about block height out of range
        assert exc_info.value.code in [-1, -8, -5]
        
    def test_getblock_verbose(self, rpc):
        """Test getblock with verbose output (verbosity=1)."""
        genesis_hash = rpc.getblockhash(0)
        block = rpc.getblock(genesis_hash, verbosity=1)
        
        assert isinstance(block, dict)
        assert "hash" in block
        assert "height" in block
        assert "time" in block
        assert "tx" in block
        
        # Verify genesis block properties
        assert block["hash"] == genesis_hash
        assert block["height"] == 0
        assert isinstance(block["tx"], list)
        assert len(block["tx"]) >= 1  # At least coinbase transaction
        
    def test_getblock_raw(self, rpc):
        """Test getblock with raw output (verbosity=0)."""
        try:
            genesis_hash = rpc.getblockhash(0)
            block_hex = rpc.getblock(genesis_hash, verbosity=0)
            
            assert isinstance(block_hex, str)
            assert len(block_hex) > 0
            
            # Verify it's valid hex
            int(block_hex, 16)  # Should not raise
        except (RPCError, ValueError):
            # Some implementations may not support verbosity=0
            pytest.skip("Node doesn't support raw block retrieval")


@pytest.mark.integration
class TestNetworkInfo:
    """Test network information and connectivity."""
    
    def test_getnetworkinfo(self, rpc):
        """Test getnetworkinfo RPC call."""
        try:
            info = rpc.getnetworkinfo()
            
            assert info is not None
            assert "version" in info
            assert "subversion" in info
            assert "protocolversion" in info
            
            # Verify protocol version is reasonable
            assert info["protocolversion"] > 0
        except RPCError:
            # Some older nodes may not have this method
            pytest.skip("getnetworkinfo not available on this node")
            
    def test_getconnectioncount(self, rpc):
        """Test getconnectioncount RPC call."""
        count = rpc.getconnectioncount()
        
        assert isinstance(count, int)
        assert count >= 0
        
        # Should match connection count from getinfo
        info = rpc.getinfo()
        assert count == info["connections"]
        
    def test_getpeerinfo(self, rpc):
        """Test getpeerinfo RPC call."""
        peers = rpc.getpeerinfo()
        
        assert isinstance(peers, list)
        
        # If we have peers, verify their structure
        if len(peers) > 0:
            peer = peers[0]
            assert "addr" in peer
            assert "version" in peer
            
            # Verify connection count matches
            count = rpc.getconnectioncount()
            assert len(peers) == count


@pytest.mark.integration
class TestMiningInfo:
    """Test mining information retrieval."""
    
    def test_getmininginfo(self, rpc):
        """Test getmininginfo RPC call."""
        info = rpc.getmininginfo()
        
        assert info is not None
        assert "blocks" in info
        assert "difficulty" in info
        assert "networkhashps" in info
        
        # Verify data types
        assert isinstance(info["blocks"], int)
        assert isinstance(info["difficulty"], (int, float))
        assert isinstance(info["networkhashps"], (int, float))
        
        # Verify reasonable values
        assert info["blocks"] >= 0
        assert info["difficulty"] >= 0
        assert info["networkhashps"] >= 0
        
    def test_getnetworkhashps(self, rpc):
        """Test getnetworkhashps RPC call."""
        hashps = rpc.getnetworkhashps()
        
        assert isinstance(hashps, (int, float))
        assert hashps >= 0
        
        # Should match mining info
        mining_info = rpc.getmininginfo()
        assert abs(hashps - mining_info["networkhashps"]) < 1000


@pytest.mark.integration
class TestUtilityMethods:
    """Test utility RPC methods."""
    
    def test_help_general(self, rpc):
        """Test help RPC call without parameters."""
        help_text = rpc.help()
        
        assert isinstance(help_text, str)
        assert len(help_text) > 0
        
        # Should contain some common commands
        assert "getinfo" in help_text.lower() or "help" in help_text.lower()
        
    def test_help_specific_command(self, rpc):
        """Test help for specific command."""
        help_text = rpc.help("getinfo")
        
        assert isinstance(help_text, str)
        assert len(help_text) > 0
        assert "getinfo" in help_text.lower()


# Performance benchmark tests
@pytest.mark.integration
@pytest.mark.slow
class TestPerformance:
    """Test RPC performance and responsiveness."""
    
    def test_getinfo_performance(self, rpc, benchmark=None):
        """Benchmark getinfo RPC call."""
        import time
        
        start = time.time()
        info = rpc.getinfo()
        elapsed = time.time() - start
        
        assert info is not None
        assert elapsed < 1.0  # Should complete in under 1 second
        
    def test_multiple_calls_performance(self, rpc):
        """Test performance of multiple consecutive RPC calls."""
        import time
        
        start = time.time()
        
        # Make 10 consecutive calls
        for _ in range(10):
            rpc.getblockcount()
            
        elapsed = time.time() - start
        
        # 10 calls should complete in under 5 seconds
        assert elapsed < 5.0
        
        # Average time per call
        avg_time = elapsed / 10
        assert avg_time < 0.5  # Average under 500ms per call


if __name__ == "__main__":
    # Allow running tests directly
    pytest.main([__file__, "-v"])
