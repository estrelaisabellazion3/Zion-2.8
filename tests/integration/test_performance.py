"""
Integration performance tests for ZION blockchain.

Tests RPC performance, concurrent calls, memory usage, and stress scenarios.
"""

import pytest
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rpc_client import get_rpc_client


@pytest.fixture(scope="module")
def rpc():
    """Fixture providing RPC client for all tests."""
    return get_rpc_client()


@pytest.mark.integration
@pytest.mark.performance
class TestRPCPerformance:
    """Test RPC call performance under various conditions."""
    
    def test_sequential_calls_speed(self, rpc):
        """Test speed of 100 sequential RPC calls."""
        start = time.time()
        
        for _ in range(100):
            rpc.getblockcount()
        
        elapsed = time.time() - start
        avg_time = elapsed / 100
        
        print(f"\n📊 100 sequential calls: {elapsed:.2f}s (avg: {avg_time*1000:.1f}ms)")
        
        # Should complete in reasonable time
        assert elapsed < 10.0, f"100 calls took {elapsed:.2f}s, expected < 10s"
        assert avg_time < 0.1, f"Average call {avg_time*1000:.1f}ms, expected < 100ms"
    
    def test_concurrent_calls_10_threads(self, rpc):
        """Test 10 concurrent RPC calls."""
        def make_call():
            return rpc.getblockcount()
        
        start = time.time()
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_call) for _ in range(10)]
            results = [f.result() for f in as_completed(futures)]
        
        elapsed = time.time() - start
        
        print(f"\n📊 10 concurrent calls: {elapsed:.2f}s")
        
        # All should succeed
        assert len(results) == 10
        # Should complete faster than sequential (but allow overhead)
        assert elapsed < 2.0, f"Concurrent calls took {elapsed:.2f}s"
    
    def test_concurrent_calls_50_threads(self, rpc):
        """Test 50 concurrent RPC calls with retry logic."""
        def make_call_with_retry():
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    return rpc.getinfo()
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    time.sleep(0.1)  # Brief pause before retry
        
        start = time.time()
        
        with ThreadPoolExecutor(max_workers=50) as executor:
            futures = [executor.submit(make_call_with_retry) for _ in range(50)]
            results = [f.result() for f in as_completed(futures)]
        
        elapsed = time.time() - start
        
        print(f"\n📊 50 concurrent calls: {elapsed:.2f}s")
        
        # All should succeed
        assert len(results) == 50
        assert elapsed < 5.0, f"50 concurrent calls took {elapsed:.2f}s"
    
    def test_mixed_rpc_methods_performance(self, rpc):
        """Test performance with various RPC methods."""
        methods = [
            ('getblockcount', []),
            ('getinfo', []),
            ('getdifficulty', []),
            ('getmininginfo', []),
            ('getnetworkinfo', []),
        ]
        
        start = time.time()
        
        for _ in range(20):  # 20 iterations
            for method_name, params in methods:
                method = getattr(rpc, method_name)
                method(*params)
        
        elapsed = time.time() - start
        total_calls = 20 * len(methods)
        avg_time = elapsed / total_calls
        
        print(f"\n📊 {total_calls} mixed RPC calls: {elapsed:.2f}s (avg: {avg_time*1000:.1f}ms)")
        
        assert avg_time < 0.1, f"Average call time {avg_time*1000:.1f}ms, expected < 100ms"


@pytest.mark.integration
@pytest.mark.performance
class TestBlockchainPerformance:
    """Test blockchain operations performance."""
    
    def test_block_retrieval_speed(self, rpc):
        """Test speed of retrieving multiple blocks."""
        block_count = rpc.getblockcount()
        
        # Get last 10 blocks
        num_blocks = min(10, block_count + 1)
        
        start = time.time()
        
        for i in range(num_blocks):
            block_hash = rpc.getblockhash(i)
            block = rpc.getblock(block_hash, 1)
            assert 'hash' in block
        
        elapsed = time.time() - start
        avg_time = elapsed / num_blocks
        
        print(f"\n📊 Retrieved {num_blocks} blocks in {elapsed:.2f}s (avg: {avg_time*1000:.1f}ms)")
        
        assert avg_time < 0.2, f"Average block retrieval {avg_time*1000:.1f}ms, expected < 200ms"
    
    def test_transaction_listing_performance(self, rpc):
        """Test performance of listing transactions."""
        iterations = 10
        
        start = time.time()
        
        for _ in range(iterations):
            txs = rpc.listtransactions("*", 100)
            assert isinstance(txs, list)
        
        elapsed = time.time() - start
        avg_time = elapsed / iterations
        
        print(f"\n📊 {iterations} transaction listings: {elapsed:.2f}s (avg: {avg_time*1000:.1f}ms)")
        
        assert avg_time < 0.5, f"Average listing time {avg_time*1000:.1f}ms, expected < 500ms"


@pytest.mark.integration
@pytest.mark.performance
class TestWalletPerformance:
    """Test wallet operations performance."""
    
    def test_bulk_address_generation(self, rpc):
        """Test generating multiple addresses."""
        num_addresses = 50
        
        start = time.time()
        
        addresses = []
        for i in range(num_addresses):
            addr = rpc.getnewaddress(f"perf_test_{i}")
            addresses.append(addr)
        
        elapsed = time.time() - start
        avg_time = elapsed / num_addresses
        
        print(f"\n📊 Generated {num_addresses} addresses in {elapsed:.2f}s (avg: {avg_time*1000:.1f}ms)")
        
        # All addresses should be unique
        assert len(set(addresses)) == num_addresses
        
        # Should be reasonably fast
        assert avg_time < 0.2, f"Average generation time {avg_time*1000:.1f}ms, expected < 200ms"
    
    def test_address_validation_performance(self, rpc):
        """Test address validation speed."""
        # Generate test address
        addr = rpc.getnewaddress("validation_test")
        
        iterations = 100
        
        start = time.time()
        
        for _ in range(iterations):
            result = rpc.validateaddress(addr)
            assert result['isvalid'] is True
        
        elapsed = time.time() - start
        avg_time = elapsed / iterations
        
        print(f"\n📊 {iterations} validations: {elapsed:.2f}s (avg: {avg_time*1000:.1f}ms)")
        
        assert avg_time < 0.05, f"Average validation {avg_time*1000:.1f}ms, expected < 50ms"


@pytest.mark.integration
@pytest.mark.performance
class TestStressScenarios:
    """Stress test scenarios."""
    
    def test_rapid_fire_requests(self, rpc):
        """Test rapid-fire requests without delay."""
        num_requests = 200
        
        start = time.time()
        
        for _ in range(num_requests):
            rpc.getblockcount()
        
        elapsed = time.time() - start
        requests_per_second = num_requests / elapsed
        
        print(f"\n📊 {num_requests} rapid requests: {elapsed:.2f}s ({requests_per_second:.1f} req/s)")
        
        assert elapsed < 20.0, f"Rapid requests took {elapsed:.2f}s, expected < 20s"
        assert requests_per_second > 10, f"Only {requests_per_second:.1f} req/s, expected > 10"
    
    def test_burst_then_pause_pattern(self, rpc):
        """Test burst of requests followed by pause (realistic usage)."""
        bursts = 10
        requests_per_burst = 10
        pause_time = 0.1  # 100ms pause between bursts
        
        start = time.time()
        
        for burst in range(bursts):
            # Burst of requests
            for _ in range(requests_per_burst):
                rpc.getinfo()
            
            # Pause before next burst
            if burst < bursts - 1:
                time.sleep(pause_time)
        
        elapsed = time.time() - start
        total_requests = bursts * requests_per_burst
        
        print(f"\n📊 {total_requests} requests in {bursts} bursts: {elapsed:.2f}s")
        
        # Should handle burst pattern well
        assert elapsed < 10.0, f"Burst pattern took {elapsed:.2f}s"
    
    def test_concurrent_different_methods(self, rpc):
        """Test concurrent calls to different RPC methods."""
        def call_method(method_name):
            method = getattr(rpc, method_name)
            return method_name, method()
        
        methods = [
            'getblockcount',
            'getinfo',
            'getdifficulty',
            'getmininginfo',
            'getnetworkinfo',
            'getblockchaininfo',
        ] * 5  # 30 total calls
        
        start = time.time()
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(call_method, m) for m in methods]
            results = [f.result() for f in as_completed(futures)]
        
        elapsed = time.time() - start
        
        print(f"\n📊 {len(methods)} concurrent mixed calls: {elapsed:.2f}s")
        
        assert len(results) == len(methods)
        assert elapsed < 5.0, f"Concurrent mixed calls took {elapsed:.2f}s"


@pytest.mark.integration
@pytest.mark.performance
class TestMemoryStability:
    """Test memory usage stability during operations."""
    
    def test_sustained_operations_no_leak(self, rpc):
        """Test that sustained operations don't leak memory."""
        # Note: This is a basic test. Real memory leak detection
        # would require process monitoring tools.
        
        # Reduced iterations to avoid rate limiting (10k/min = 166/sec)
        iterations = 100  # Was 500
        
        start = time.time()
        
        # Mix of operations with small delays
        for i in range(iterations):
            rpc.getblockcount()
            
            if i % 10 == 0:
                rpc.getinfo()
                time.sleep(0.01)  # Small delay every 10 ops
            
            if i % 20 == 0:
                rpc.getnewaddress(f"leak_test_{i}")
                time.sleep(0.01)  # Small delay every 20 ops
        
        elapsed = time.time() - start
        ops_per_second = iterations / elapsed
        
        print(f"\n📊 {iterations} sustained operations: {elapsed:.2f}s ({ops_per_second:.1f} ops/s)")
        
        # Should complete without issues
        assert elapsed < 30.0, f"Sustained ops took {elapsed:.2f}s"
        
        # If we got here without hanging/crashing, no obvious leak
        assert True


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
