"""
Integration tests for ZION wallet functionality.

Tests wallet creation, address generation, balance checking, and transactions.
"""

import pytest
import sys
import os
import time

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rpc_client import get_rpc_client, RPCError


@pytest.fixture(scope="module")
def rpc():
    """Fixture providing RPC client for all tests."""
    return get_rpc_client()


@pytest.mark.integration
class TestAddressGeneration:
    """Test address generation and validation."""
    
    def test_getnewaddress(self, rpc):
        """Test generating new receiving address."""
        address = rpc.getnewaddress()
        
        assert isinstance(address, str)
        assert len(address) > 20  # ZION addresses should be reasonable length
        
        # Verify it's a valid address
        validation = rpc.validateaddress(address)
        assert validation["isvalid"] is True
        
    def test_getnewaddress_with_label(self, rpc):
        """Test generating address with label."""
        label = "test_wallet_integration"
        address = rpc.getnewaddress(label)
        
        assert isinstance(address, str)
        
        # Verify address is valid
        validation = rpc.validateaddress(address)
        assert validation["isvalid"] is True
        
    def test_multiple_addresses(self, rpc):
        """Test generating multiple unique addresses."""
        addresses = set()
        
        for i in range(5):
            addr = rpc.getnewaddress(f"test_addr_{i}")
            addresses.add(addr)
            
        # All addresses should be unique
        assert len(addresses) == 5
        
        # All should be valid
        for addr in addresses:
            validation = rpc.validateaddress(addr)
            assert validation["isvalid"] is True


@pytest.mark.integration
class TestAddressValidation:
    """Test address validation."""
    
    def test_validateaddress_valid(self, rpc):
        """Test validating a valid address."""
        # Generate a new address first
        address = rpc.getnewaddress()
        
        validation = rpc.validateaddress(address)
        
        assert isinstance(validation, dict)
        assert "isvalid" in validation
        assert validation["isvalid"] is True
        assert "address" in validation
        assert validation["address"] == address
        
    def test_validateaddress_invalid(self, rpc):
        """Test validating an invalid address."""
        invalid_address = "invalid_zion_address_12345"
        
        validation = rpc.validateaddress(invalid_address)
        
        assert isinstance(validation, dict)
        assert "isvalid" in validation
        assert validation["isvalid"] is False
        
    def test_validateaddress_empty(self, rpc):
        """Test validating empty address."""
        validation = rpc.validateaddress("")
        
        assert validation["isvalid"] is False


@pytest.mark.integration
class TestBalance:
    """Test wallet balance retrieval."""
    
    def test_getbalance(self, rpc):
        """Test getting wallet balance."""
        balance = rpc.getbalance()
        
        assert isinstance(balance, (int, float))
        assert balance >= 0
        
    def test_getbalance_with_confirmations(self, rpc):
        """Test balance with different confirmation requirements."""
        # Balance with 1 confirmation
        balance_1 = rpc.getbalance("*", 1)
        
        # Balance with 6 confirmations
        balance_6 = rpc.getbalance("*", 6)
        
        assert isinstance(balance_1, (int, float))
        assert isinstance(balance_6, (int, float))
        
        # Balance with more confirmations should be <= balance with fewer
        assert balance_6 <= balance_1
        
    def test_listunspent(self, rpc):
        """Test listing unspent transaction outputs."""
        unspent = rpc.listunspent()
        
        assert isinstance(unspent, list)
        
        # If we have unspent outputs, verify their structure
        if len(unspent) > 0:
            utxo = unspent[0]
            
            assert "txid" in utxo
            assert "vout" in utxo
            assert "address" in utxo
            assert "amount" in utxo
            assert "confirmations" in utxo
            
            # Verify data types
            assert isinstance(utxo["txid"], str)
            assert isinstance(utxo["vout"], int)
            assert isinstance(utxo["address"], str)
            assert isinstance(utxo["amount"], (int, float))
            assert isinstance(utxo["confirmations"], int)
            
            # Verify reasonable values
            assert len(utxo["txid"]) == 64  # SHA-256 hash
            assert utxo["vout"] >= 0
            assert utxo["amount"] > 0
            assert utxo["confirmations"] >= 0
            
    def test_listunspent_filtered(self, rpc):
        """Test listunspent with address filter."""
        # Get a new address
        address = rpc.getnewaddress("test_filter")
        
        # List unspent for this specific address
        unspent = rpc.listunspent(1, 9999999, [address])
        
        assert isinstance(unspent, list)
        
        # All results should be for our address
        for utxo in unspent:
            assert utxo["address"] == address


@pytest.mark.integration
class TestTransactionHistory:
    """Test transaction history retrieval."""
    
    def test_listtransactions(self, rpc):
        """Test listing recent transactions."""
        transactions = rpc.listtransactions()
        
        assert isinstance(transactions, list)
        
        # If we have transactions, verify their structure
        if len(transactions) > 0:
            tx = transactions[0]
            
            assert "txid" in tx
            assert "amount" in tx
            assert "confirmations" in tx
            
            # Verify data types
            assert isinstance(tx["txid"], str)
            assert isinstance(tx["amount"], (int, float))
            assert isinstance(tx["confirmations"], int)
            
    def test_listtransactions_limited(self, rpc):
        """Test listing limited number of transactions."""
        # Request only 5 transactions
        transactions = rpc.listtransactions("*", 5)
        
        assert isinstance(transactions, list)
        assert len(transactions) <= 5
        
    def test_gettransaction(self, rpc):
        """Test getting specific transaction details."""
        # First get a transaction ID from recent transactions
        transactions = rpc.listtransactions()
        
        if len(transactions) > 0:
            txid = transactions[0]["txid"]
            
            # Get detailed transaction info
            tx_detail = rpc.gettransaction(txid)
            
            assert isinstance(tx_detail, dict)
            assert "txid" in tx_detail
            assert tx_detail["txid"] == txid
            assert "amount" in tx_detail
            assert "confirmations" in tx_detail
        else:
            pytest.skip("No transactions available to test")


@pytest.mark.integration
@pytest.mark.requires_network
class TestTransactionSending:
    """Test transaction sending functionality."""
    
    @pytest.fixture
    def test_addresses(self, rpc):
        """Generate test addresses for transaction tests."""
        return {
            "addr1": rpc.getnewaddress("test_send_1"),
            "addr2": rpc.getnewaddress("test_send_2"),
            "addr3": rpc.getnewaddress("test_send_3")
        }
    
    def test_sendtoaddress_insufficient_funds(self, rpc, test_addresses):
        """Test sending with insufficient funds (should fail)."""
        balance = rpc.getbalance()
        
        # Try to send more than we have
        with pytest.raises(RPCError) as exc_info:
            rpc.sendtoaddress(test_addresses["addr1"], balance + 1000)
        
        # Should get insufficient funds error
        assert exc_info.value.code in [-1, -4, -6]
        
    def test_sendtoaddress_with_sufficient_funds(self, rpc, test_addresses):
        """Test sending transaction (only if wallet has funds)."""
        balance = rpc.getbalance()
        
        if balance >= 1.0:  # Only test if we have at least 1 ZION
            # Send small amount
            amount = 0.1
            
            try:
                txid = rpc.sendtoaddress(test_addresses["addr1"], amount)
                
                assert isinstance(txid, str)
                assert len(txid) == 64  # Transaction ID is SHA-256 hash
                
                # Verify transaction appears in history
                time.sleep(1)  # Give node time to process
                tx_detail = rpc.gettransaction(txid)
                assert tx_detail["txid"] == txid
                
            except RPCError as e:
                # Might fail if wallet is locked or other issues
                pytest.skip(f"Cannot send transaction: {e.message}")
        else:
            pytest.skip("Insufficient balance to test transaction sending")
    
    def test_sendmany(self, rpc, test_addresses):
        """Test sending to multiple addresses."""
        balance = rpc.getbalance()
        
        if balance >= 1.0:  # Need sufficient balance
            amounts = {
                test_addresses["addr1"]: 0.1,
                test_addresses["addr2"]: 0.15,
                test_addresses["addr3"]: 0.2
            }
            
            try:
                txid = rpc.sendmany("", amounts)
                
                assert isinstance(txid, str)
                assert len(txid) == 64
                
                # Verify transaction
                time.sleep(1)
                tx_detail = rpc.gettransaction(txid)
                assert tx_detail["txid"] == txid
                
            except RPCError as e:
                pytest.skip(f"Cannot send multi-recipient transaction: {e.message}")
        else:
            pytest.skip("Insufficient balance to test sendmany")


@pytest.mark.integration
class TestFeeEstimation:
    """Test transaction fee estimation."""
    
    def test_estimatefee(self, rpc):
        """Test estimating transaction fee."""
        try:
            fee = rpc.estimatefee(6)  # Fee for 6-block confirmation
            
            # Fee should be numeric (might be -1 if not enough data)
            assert isinstance(fee, (int, float))
            
            if fee > 0:
                # Fee should be reasonable (not extremely high)
                assert fee < 10.0  # Less than 10 ZION per kB
                
        except RPCError:
            # Some nodes may not support fee estimation
            pytest.skip("Fee estimation not available on this node")


# Performance tests
@pytest.mark.integration
@pytest.mark.slow
class TestWalletPerformance:
    """Test wallet operation performance."""
    
    def test_address_generation_speed(self, rpc):
        """Test speed of generating multiple addresses."""
        import time
        
        start = time.time()
        
        # Generate 100 addresses
        for i in range(100):
            rpc.getnewaddress(f"perf_test_{i}")
            
        elapsed = time.time() - start
        
        # Should complete in reasonable time
        assert elapsed < 30.0  # 100 addresses in under 30 seconds
        
        # Average time per address
        avg_time = elapsed / 100
        print(f"\nAverage address generation time: {avg_time:.3f}s")
        
    def test_balance_check_speed(self, rpc):
        """Test speed of balance checking."""
        import time
        
        start = time.time()
        
        # Check balance 50 times
        for _ in range(50):
            rpc.getbalance()
            
        elapsed = time.time() - start
        
        # Should be fast
        assert elapsed < 10.0  # 50 calls in under 10 seconds
        
        avg_time = elapsed / 50
        print(f"\nAverage balance check time: {avg_time:.3f}s")


if __name__ == "__main__":
    # Allow running tests directly
    pytest.main([__file__, "-v"])
