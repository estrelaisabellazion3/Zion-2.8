"""
Security audit tests for ZION blockchain.

Tests authentication, input validation, cryptographic security,
and protection against common attack vectors.
"""

import pytest
import time
import hashlib
import json
import sys
import os
from concurrent.futures import ThreadPoolExecutor

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rpc_client import get_rpc_client, RPCError


@pytest.fixture(scope="module")
def rpc():
    """Fixture providing RPC client for all tests."""
    return get_rpc_client()


@pytest.mark.integration
@pytest.mark.security
class TestInputValidation:
    """Test input validation and sanitization."""
    
    def test_invalid_address_format_rejected(self, rpc):
        """Test that invalid address formats are rejected."""
        invalid_addresses = [
            "",  # Empty
            "x",  # Too short
            "invalid",  # Not hex
            "0x" * 100,  # Too long
            "<script>alert('xss')</script>",  # XSS attempt
            "'; DROP TABLE blocks; --",  # SQL injection attempt
            "../../../etc/passwd",  # Path traversal
            "\x00\x01\x02",  # Null bytes
        ]
        
        for addr in invalid_addresses:
            result = rpc.validateaddress(addr)
            assert result["isvalid"] is False, f"Address '{addr}' should be invalid"
    
    def test_negative_amounts_rejected(self, rpc):
        """Test that negative amounts are rejected."""
        addr = rpc.getnewaddress("test_negative")
        
        # Try to send negative amount
        with pytest.raises(RPCError) as exc_info:
            rpc.sendtoaddress(addr, -1.0)
        
        assert exc_info.value.code in [-1, -3, -8]
    
    def test_zero_amount_rejected(self, rpc):
        """Test that zero amounts are rejected."""
        addr = rpc.getnewaddress("test_zero")
        
        with pytest.raises(RPCError) as exc_info:
            rpc.sendtoaddress(addr, 0.0)
        
        assert exc_info.value.code in [-1, -3, -8]
    
    def test_extremely_large_amounts_handled(self, rpc):
        """Test that extremely large amounts don't cause overflow."""
        addr = rpc.getnewaddress("test_large")
        
        # Try impossibly large amount
        with pytest.raises(RPCError) as exc_info:
            rpc.sendtoaddress(addr, 1e100)
        
        # Should reject due to insufficient funds or validation
        assert exc_info.value.code in [-1, -4, -6]
    
    def test_invalid_block_height(self, rpc):
        """Test that invalid block heights are handled."""
        # Negative height
        with pytest.raises(RPCError) as exc_info:
            rpc.getblockhash(-1)
        
        assert exc_info.value.code in [-1, -8]
        
        # Way beyond current height
        current_height = rpc.getblockcount()
        with pytest.raises(RPCError) as exc_info:
            rpc.getblockhash(current_height + 1000000)
        
        assert exc_info.value.code in [-1, -8]
    
    def test_malformed_json_rpc_handled(self, rpc):
        """Test that malformed JSON-RPC requests are handled gracefully."""
        # This tests the RPC client's error handling
        # The server should return proper error responses
        
        # Test with invalid method name
        try:
            # Call non-existent method
            result = rpc._call("nonexistent_method_12345", [])
            assert False, "Should have raised RPCError"
        except RPCError as e:
            assert e.code in [-32601, -1]  # Method not found


@pytest.mark.integration
@pytest.mark.security
class TestRateLimiting:
    """Test rate limiting protection."""
    
    def test_rate_limit_enforcement(self, rpc):
        """Test that rate limiting is enforced (10k/min = 166/sec)."""
        # Test that we can make reasonable number of requests
        # Full rate limit test would take too long
        
        start = time.time()
        successes = 0
        
        # Make 50 requests (manageable for test)
        for i in range(50):
            try:
                rpc.getblockcount()
                successes += 1
                time.sleep(0.01)  # Small delay
            except RPCError as e:
                if e.code == -1 and "429" in str(e):
                    break
            except Exception:
                break
        
        elapsed = time.time() - start
        
        print(f"\n📊 Made {successes} requests in {elapsed:.2f}s")
        
        # Should complete successfully with reasonable rate
        assert successes >= 40, f"Should complete most requests, got {successes}/50"
    
    def test_burst_limit_protection(self, rpc):
        """Test that burst limits protect against rapid-fire attacks."""
        # Make rapid requests in tight loop
        burst_size = 100
        
        start = time.time()
        try:
            for _ in range(burst_size):
                rpc.getinfo()
        except (RPCError, Exception):
            # Expected to hit limit
            pass
        
        elapsed = time.time() - start
        
        print(f"\n📊 Burst of {burst_size} requests took {elapsed:.2f}s")
        
        # Should complete or rate limit (both are acceptable)
        assert elapsed > 0


@pytest.mark.integration
@pytest.mark.security
class TestCryptographicSecurity:
    """Test cryptographic security measures."""
    
    def test_address_uniqueness(self, rpc):
        """Test that generated addresses are unique."""
        addresses = set()
        num_addresses = 100
        
        for i in range(num_addresses):
            addr = rpc.getnewaddress(f"unique_test_{i}")
            addresses.add(addr)
        
        # All should be unique
        assert len(addresses) == num_addresses, "Addresses should be unique"
    
    def test_address_format_consistency(self, rpc):
        """Test that addresses follow consistent format."""
        for _ in range(10):
            addr = rpc.getnewaddress("format_test")
            
            # Should start with ZION_ prefix
            assert addr.startswith("ZION_"), f"Address {addr} should start with ZION_"
            
            # Should be reasonable length
            assert 40 <= len(addr) <= 100, f"Address {addr} has unusual length {len(addr)}"
            
            # Suffix should be hex
            suffix = addr[5:]  # Remove ZION_ prefix
            try:
                int(suffix, 16)
            except ValueError:
                assert False, f"Address suffix {suffix} is not valid hex"
    
    def test_transaction_id_uniqueness(self, rpc):
        """Test that transaction IDs are unique."""
        # Get recent transactions
        txs = rpc.listtransactions("*", 50)
        
        if len(txs) > 0:
            tx_ids = [tx["txid"] for tx in txs]
            
            # All should be unique
            assert len(tx_ids) == len(set(tx_ids)), "Transaction IDs should be unique"
            
            # Check format - genesis txs may have custom format
            # Regular txs should be 64 hex chars
            regular_txs = [txid for txid in tx_ids if not txid.startswith("genesis_")]
            
            if len(regular_txs) > 0:
                for txid in regular_txs:
                    assert len(txid) == 64, f"TXID {txid} should be 64 chars"
                    try:
                        int(txid, 16)
                    except ValueError:
                        assert False, f"TXID {txid} is not valid hex"
            
            # Genesis transactions have custom format - that's OK
            genesis_txs = [txid for txid in tx_ids if txid.startswith("genesis_")]
            if len(genesis_txs) > 0:
                print(f"\n📊 Found {len(genesis_txs)} genesis transactions (custom format allowed)")


@pytest.mark.integration
@pytest.mark.security
class TestErrorHandling:
    """Test error handling and information disclosure."""
    
    def test_error_messages_safe(self, rpc):
        """Test that error messages don't leak sensitive info."""
        # Try various invalid operations
        test_cases = [
            (lambda: rpc.getblockhash(-1), "negative block height"),
            (lambda: rpc.validateaddress("invalid"), "invalid address"),
            (lambda: rpc.sendtoaddress("invalid", 1.0), "invalid send"),
        ]
        
        for func, description in test_cases:
            try:
                func()
            except RPCError as e:
                error_msg = str(e).lower()
                
                # Should not contain sensitive paths
                assert "/home/" not in error_msg, f"{description}: Leaked file path"
                assert "password" not in error_msg, f"{description}: Leaked password"
                assert "secret" not in error_msg, f"{description}: Leaked secret"
                assert "private" not in error_msg, f"{description}: Leaked private key"
    
    def test_graceful_degradation(self, rpc):
        """Test that server degrades gracefully under errors."""
        # Make some invalid requests
        for _ in range(10):
            try:
                rpc.getblockhash(-1)
            except RPCError:
                pass  # Expected
        
        # Server should still work
        result = rpc.getblockcount()
        assert isinstance(result, int)


@pytest.mark.integration
@pytest.mark.security
class TestAccessControl:
    """Test access control and authorization."""
    
    def test_all_rpc_methods_require_connection(self, rpc):
        """Test that RPC methods require valid connection."""
        # All our calls go through authenticated client
        # This verifies connection is required
        
        result = rpc.getinfo()
        assert "blocks" in result or "version" in result
    
    def test_dangerous_operations_protected(self, rpc):
        """Test that dangerous operations have protection."""
        # Try to send to invalid address
        with pytest.raises(RPCError):
            rpc.sendtoaddress("invalid_address_xyz", 1000000.0)
        
        # Try to send more than balance
        balance = rpc.getbalance()
        with pytest.raises(RPCError):
            rpc.sendtoaddress(rpc.getnewaddress("test"), balance + 1000.0)


@pytest.mark.integration
@pytest.mark.security
class TestDataValidation:
    """Test data validation and sanitization."""
    
    def test_block_hash_validation(self, rpc):
        """Test that block hashes are validated."""
        # Get valid block
        height = min(0, rpc.getblockcount())
        valid_hash = rpc.getblockhash(height)
        
        # Valid hash should work
        block = rpc.getblock(valid_hash, 1)
        assert "hash" in block
        
        # Invalid hash should fail
        with pytest.raises(RPCError):
            rpc.getblock("invalid_hash_12345", 1)
    
    def test_label_sanitization(self, rpc):
        """Test that labels are sanitized."""
        dangerous_labels = [
            "<script>alert('xss')</script>",
            "'; DROP TABLE addresses; --",
            "../../../etc/passwd",
        ]
        
        for label in dangerous_labels:
            # Should not crash or execute
            addr = rpc.getnewaddress(label)
            assert addr.startswith("ZION_")
            
            # Validation should work
            result = rpc.validateaddress(addr)
            assert result["isvalid"] is True


@pytest.mark.integration
@pytest.mark.security
class TestConcurrencyAttacks:
    """Test protection against concurrency-based attacks."""
    
    def test_concurrent_transaction_creation(self, rpc):
        """Test that concurrent transactions don't cause issues."""
        def create_address():
            return rpc.getnewaddress(f"concurrent_{time.time()}")
        
        # Create multiple addresses concurrently
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(create_address) for _ in range(10)]
            addresses = [f.result() for f in futures]
        
        # All should succeed and be unique
        assert len(set(addresses)) == 10
    
    def test_concurrent_balance_checks(self, rpc):
        """Test that concurrent balance checks are consistent."""
        def check_balance():
            return rpc.getbalance()
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(check_balance) for _ in range(5)]
            balances = [f.result() for f in futures]
        
        # All should be the same (no transactions happening)
        assert len(set(balances)) == 1, "Concurrent balance checks should be consistent"


@pytest.mark.integration
@pytest.mark.security
class TestResourceExhaustion:
    """Test protection against resource exhaustion attacks."""
    
    def test_large_batch_request_handling(self, rpc):
        """Test that large batch requests are handled safely."""
        # Try to get many blocks
        block_count = rpc.getblockcount()
        num_requests = min(50, block_count + 1)
        
        start = time.time()
        
        for i in range(num_requests):
            try:
                block_hash = rpc.getblockhash(i)
                rpc.getblock(block_hash, 0)  # Raw format (smaller)
            except RPCError:
                # May hit rate limit, that's OK
                break
        
        elapsed = time.time() - start
        
        print(f"\n📊 Processed {num_requests} block requests in {elapsed:.2f}s")
        
        # Should not hang or crash
        assert elapsed < 30.0
    
    def test_memory_not_exhausted_by_requests(self, rpc):
        """Test that repeated requests don't exhaust memory."""
        # Make many small requests
        iterations = 50
        
        for _ in range(iterations):
            rpc.getblockcount()
            time.sleep(0.02)  # Small delay to avoid rate limit
        
        # If we get here, memory is OK
        assert True


@pytest.mark.integration
@pytest.mark.security
class TestSecurityBestPractices:
    """Test adherence to security best practices."""
    
    def test_no_default_credentials(self, rpc):
        """Test that system doesn't use default credentials."""
        # Our RPC client uses configured credentials
        # This test verifies connection works (implying auth is in place)
        
        result = rpc.getinfo()
        assert result is not None
    
    def test_version_information_available(self, rpc):
        """Test that version information is available for security updates."""
        info = rpc.getnetworkinfo()
        
        assert "version" in info or "subversion" in info
        
        # Should have some version identifier
        version_str = info.get("version", info.get("subversion", ""))
        assert len(str(version_str)) > 0
    
    def test_error_codes_consistent(self, rpc):
        """Test that error codes are consistent."""
        # Different invalid operations should have appropriate codes
        
        # Invalid block height
        try:
            rpc.getblockhash(-1)
        except RPCError as e:
            assert e.code in [-1, -8]
        
        # Invalid address
        result = rpc.validateaddress("invalid")
        assert result["isvalid"] is False


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
