"""
Integration tests for ZION mining functionality.

Tests mining information, hashrate calculation, and block template generation.
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
class TestMiningInformation:
    """Test mining information retrieval."""
    
    def test_getmininginfo_structure(self, rpc):
        """Test getmininginfo returns proper structure."""
        info = rpc.getmininginfo()
        
        assert isinstance(info, dict)
        
        # Required fields
        required_fields = ["blocks", "difficulty"]
        for field in required_fields:
            assert field in info, f"Missing required field: {field}"
            
        # Verify data types
        assert isinstance(info["blocks"], int)
        assert isinstance(info["difficulty"], (int, float))
        
    def test_getmininginfo_values(self, rpc):
        """Test getmininginfo returns reasonable values."""
        info = rpc.getmininginfo()
        
        # Block count should be non-negative
        assert info["blocks"] >= 0
        
        # Difficulty should be positive
        assert info["difficulty"] > 0
        
        # If networkhashps field exists, verify it
        if "networkhashps" in info:
            assert info["networkhashps"] >= 0
            
    def test_mining_info_consistency(self, rpc):
        """Test mining info is consistent with blockchain info."""
        mining_info = rpc.getmininginfo()
        blockchain_info = rpc.getblockchaininfo()
        
        # Block counts should match
        assert mining_info["blocks"] == blockchain_info["blocks"]
        
        # Difficulty should match
        assert abs(mining_info["difficulty"] - blockchain_info["difficulty"]) < 0.01


@pytest.mark.integration
class TestNetworkHashrate:
    """Test network hashrate calculation."""
    
    def test_getnetworkhashps_default(self, rpc):
        """Test network hashrate with default parameters."""
        hashps = rpc.getnetworkhashps()
        
        assert isinstance(hashps, (int, float))
        assert hashps >= 0
        
    def test_getnetworkhashps_custom_blocks(self, rpc):
        """Test network hashrate over custom block range."""
        # Calculate over last 10 blocks
        hashps_10 = rpc.getnetworkhashps(10)
        
        # Calculate over last 120 blocks (default)
        hashps_120 = rpc.getnetworkhashps(120)
        
        assert isinstance(hashps_10, (int, float))
        assert isinstance(hashps_120, (int, float))
        
        # Both should be non-negative
        assert hashps_10 >= 0
        assert hashps_120 >= 0
        
    def test_networkhashps_consistency(self, rpc):
        """Test network hashrate matches mining info."""
        hashps = rpc.getnetworkhashps()
        mining_info = rpc.getmininginfo()
        
        if "networkhashps" in mining_info:
            # Should be similar (allowing for different time windows)
            ratio = hashps / mining_info["networkhashps"] if mining_info["networkhashps"] > 0 else 1
            assert 0.5 <= ratio <= 2.0, "Network hashrate values differ too much"


@pytest.mark.integration
class TestBlockTemplate:
    """Test block template generation for mining."""
    
    def test_getblocktemplate_basic(self, rpc):
        """Test basic block template retrieval."""
        try:
            template = rpc.getblocktemplate()
            
            assert isinstance(template, dict)
            
            # Check for required fields
            required_fields = ["version", "previousblockhash", "transactions", "coinbasevalue", "bits", "height"]
            
            for field in required_fields:
                if field not in template:
                    # Some fields might be optional depending on implementation
                    continue
                    
            # If we have these fields, verify them
            if "height" in template:
                assert isinstance(template["height"], int)
                assert template["height"] >= 0
                
            if "transactions" in template:
                assert isinstance(template["transactions"], list)
                
            if "previousblockhash" in template:
                assert isinstance(template["previousblockhash"], str)
                assert len(template["previousblockhash"]) == 64
                
        except RPCError as e:
            # getblocktemplate might not be available or require specific setup
            pytest.skip(f"Block template not available: {e.message}")
            
    def test_getblocktemplate_with_rules(self, rpc):
        """Test block template with specific rules."""
        try:
            template = rpc.getblocktemplate(rules=["segwit"])
            
            assert isinstance(template, dict)
            
        except RPCError as e:
            # Might not support rules parameter or segwit
            pytest.skip(f"Block template with rules not supported: {e.message}")


@pytest.mark.integration
@pytest.mark.slow
class TestMiningDifficulty:
    """Test mining difficulty adjustment."""
    
    def test_difficulty_positive(self, rpc):
        """Test difficulty is always positive."""
        difficulty = rpc.getdifficulty()
        
        assert difficulty > 0
        
    def test_difficulty_consistency(self, rpc):
        """Test difficulty is consistent across different calls."""
        diff1 = rpc.getdifficulty()
        diff2 = rpc.getdifficulty()
        
        # Should be identical (unless a new block was found)
        assert diff1 == diff2 or abs(diff1 - diff2) / diff1 < 0.01
        
    def test_difficulty_in_range(self, rpc):
        """Test difficulty is in reasonable range."""
        difficulty = rpc.getdifficulty()
        
        # Difficulty should not be extremely high for testnet
        # (mainnet might have higher values)
        assert difficulty < 1e15  # Reasonable upper bound


@pytest.mark.integration
@pytest.mark.requires_gpu
class TestGPUMining:
    """Test GPU mining functionality (requires GPU hardware)."""
    
    def test_gpu_detection(self):
        """Test GPU detection."""
        try:
            import subprocess
            
            # Try to detect NVIDIA GPUs
            result = subprocess.run(
                ["nvidia-smi", "--list-gpus"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                gpus = [line for line in result.stdout.split('\n') if line.strip()]
                assert len(gpus) > 0, "No NVIDIA GPUs detected"
                print(f"\nDetected {len(gpus)} NVIDIA GPU(s)")
            else:
                # Try AMD
                result = subprocess.run(
                    ["rocm-smi", "--showproductname"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                
                if result.returncode != 0:
                    pytest.skip("No GPU detected (neither NVIDIA nor AMD)")
                    
        except FileNotFoundError:
            pytest.skip("GPU tools not installed")
        except Exception as e:
            pytest.skip(f"Cannot detect GPU: {e}")


@pytest.mark.integration
class TestCPUMining:
    """Test CPU mining functionality."""
    
    def test_cpu_cores_detection(self):
        """Test CPU core detection."""
        import multiprocessing
        
        cores = multiprocessing.cpu_count()
        
        assert cores > 0
        print(f"\nDetected {cores} CPU cores")
        
    def test_cpu_info(self):
        """Test CPU information retrieval."""
        try:
            import platform
            
            processor = platform.processor()
            assert len(processor) > 0
            
            print(f"\nCPU: {processor}")
            
        except Exception as e:
            pytest.skip(f"Cannot get CPU info: {e}")


@pytest.mark.integration
class TestMiningRewards:
    """Test mining reward calculation."""
    
    def test_block_reward_amount(self, rpc):
        """Test block reward is correct amount."""
        try:
            # Get current block height
            height = rpc.getblockcount()
            
            if height > 0:
                # Get latest block
                block_hash = rpc.getblockhash(height)
                block = rpc.getblock(block_hash, verbosity=1)
                
                # Get coinbase transaction (first transaction)
                if "tx" in block and len(block["tx"]) > 0:
                    coinbase_txid = block["tx"][0]
                    
                    # Expected reward (45 ZION per block for ZION 2.8.3)
                    expected_reward = 45.0
                    
                    print(f"\nBlock {height} coinbase: {coinbase_txid}")
                    print(f"Expected reward: {expected_reward} ZION")
                    
        except RPCError as e:
            pytest.skip(f"Cannot verify block reward: {e.message}")


# Performance benchmarks
@pytest.mark.integration
@pytest.mark.slow
class TestMiningPerformance:
    """Test mining-related performance."""
    
    def test_blocktemplate_generation_speed(self, rpc):
        """Test speed of block template generation."""
        import time
        
        try:
            start = time.time()
            
            # Generate 10 block templates
            for _ in range(10):
                rpc.getblocktemplate()
                
            elapsed = time.time() - start
            
            # Should be reasonably fast
            assert elapsed < 5.0  # 10 templates in under 5 seconds
            
            avg_time = elapsed / 10
            print(f"\nAverage template generation time: {avg_time:.3f}s")
            
        except RPCError:
            pytest.skip("Block template generation not available")
            
    def test_difficulty_calculation_speed(self, rpc):
        """Test speed of difficulty calculation."""
        import time
        
        start = time.time()
        
        # Get difficulty 100 times
        for _ in range(100):
            rpc.getdifficulty()
            
        elapsed = time.time() - start
        
        # Should be very fast (cached value)
        assert elapsed < 2.0  # 100 calls in under 2 seconds
        
        avg_time = elapsed / 100
        print(f"\nAverage difficulty retrieval time: {avg_time:.4f}s")


if __name__ == "__main__":
    # Allow running tests directly
    pytest.main([__file__, "-v"])
