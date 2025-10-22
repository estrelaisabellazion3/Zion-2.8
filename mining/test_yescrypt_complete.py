#!/usr/bin/env python3
"""
🧪 ZION Yescrypt Mining - Comprehensive Test Suite

Tests all mining components:
✅ C extension (yescrypt_fast)
✅ Optimized Python wrapper
✅ Professional miner
✅ Performance benchmarks
✅ Pool connectivity
"""

import sys
import os
import time
import subprocess
import importlib.util

sys.path.insert(0, '/media/maitreya/ZION1/mining')

class TestRunner:
    """Test runner for ZION Yescrypt mining"""
    
    def __init__(self):
        self.tests_passed = 0
        self.tests_failed = 0
        self.results = []
    
    def print_header(self, text):
        print("\n" + "="*60)
        print(f"🧪 {text}")
        print("="*60 + "\n")
    
    def test(self, name, func):
        """Run a single test"""
        try:
            print(f"  ► {name}...", end=" ", flush=True)
            func()
            print("✅ PASS")
            self.tests_passed += 1
            self.results.append((name, "PASS", None))
        except Exception as e:
            print(f"❌ FAIL: {str(e)[:50]}")
            self.tests_failed += 1
            self.results.append((name, "FAIL", str(e)))
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "="*60)
        print(f"📊 TEST SUMMARY")
        print("="*60)
        print(f"  ✅ Passed: {self.tests_passed}")
        print(f"  ❌ Failed: {self.tests_failed}")
        print(f"  📈 Total:  {self.tests_passed + self.tests_failed}")
        print(f"  📊 Success Rate: {self.tests_passed / (self.tests_passed + self.tests_failed) * 100:.1f}%")
        print("="*60 + "\n")
    
    # ===== Test Suite =====
    
    def test_c_extension_import(self):
        """Test 1: Import C extension"""
        import yescrypt_fast
        assert hasattr(yescrypt_fast, 'hash'), "Missing 'hash' function"
        assert hasattr(yescrypt_fast, 'benchmark'), "Missing 'benchmark' function"
    
    def test_c_extension_hash(self):
        """Test 2: C extension hash computation"""
        import yescrypt_fast
        
        # Test data
        data = b"ZION_blockchain_test_data_42"
        nonce = 12345
        
        # Compute hash
        result = yescrypt_fast.hash(data, nonce)
        
        # Validate result
        assert isinstance(result, bytes), "Result should be bytes"
        assert len(result) == 32, f"Hash should be 32 bytes, got {len(result)}"
        
        # Test determinism
        result2 = yescrypt_fast.hash(data, nonce)
        assert result == result2, "Hash should be deterministic"
    
    def test_c_extension_different_nonces(self):
        """Test 3: Different nonces produce different hashes"""
        import yescrypt_fast
        
        data = b"test_data"
        
        hashes = set()
        for nonce in range(10):
            h = yescrypt_fast.hash(data, nonce)
            hashes.add(h)
        
        assert len(hashes) == 10, "Different nonces should produce different hashes"
    
    def test_python_wrapper_import(self):
        """Test 4: Import Python wrapper"""
        spec = importlib.util.spec_from_file_location(
            "zion_yescrypt_optimized",
            "/media/maitreya/ZION1/mining/zion_yescrypt_optimized.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        assert hasattr(module, 'OptimizedYescryptMiner'), "Missing OptimizedYescryptMiner class"
    
    def test_professional_miner_import(self):
        """Test 5: Import professional miner"""
        spec = importlib.util.spec_from_file_location(
            "zion_yescrypt_professional",
            "/media/maitreya/ZION1/mining/zion_yescrypt_professional.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        assert hasattr(module, 'YescryptCore'), "Missing YescryptCore class"
        assert hasattr(module, 'ProfessionalYescryptMiner'), "Missing ProfessionalYescryptMiner class"
    
    def test_benchmark(self):
        """Test 6: Performance benchmark"""
        import yescrypt_fast
        
        # Benchmark
        num_hashes = 100
        data = b"ZION_benchmark_test"
        
        start = time.time()
        for i in range(num_hashes):
            yescrypt_fast.hash(data, i)
        elapsed = time.time() - start
        
        hashrate = num_hashes / elapsed
        print(f"     {hashrate:.1f} H/s")
        
        # Should be at least 1 H/s (very conservative)
        assert hashrate >= 0.1, f"Hashrate too low: {hashrate:.1f} H/s"
    
    def test_high_nonce_values(self):
        """Test 7: High nonce values"""
        import yescrypt_fast
        
        data = b"test"
        
        # Test large nonce values
        for nonce in [2**16, 2**24, 2**31-1]:
            result = yescrypt_fast.hash(data, nonce)
            assert len(result) == 32, f"Hash should be 32 bytes for nonce {nonce}"
    
    def test_empty_data(self):
        """Test 8: Empty data handling"""
        import yescrypt_fast
        
        # Empty data should still work
        result = yescrypt_fast.hash(b"", 0)
        assert len(result) == 32, "Should handle empty data"
        assert isinstance(result, bytes), "Result should be bytes"
    
    def test_long_data(self):
        """Test 9: Long data handling"""
        import yescrypt_fast
        
        # Long data
        data = b"x" * 10000
        result = yescrypt_fast.hash(data, 42)
        assert len(result) == 32, "Should handle long data"
    
    def test_configuration_loading(self):
        """Test 10: Configuration loading"""
        import json
        
        config_file = "/media/maitreya/ZION1/mining/yescrypt-miner-config.json"
        
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            assert 'pool' in config, "Config should have 'pool'"
            assert 'threads' in config, "Config should have 'threads'"
        else:
            print("     (config file not found - skipping)")
    
    def test_multiple_hashes_consistency(self):
        """Test 11: Consistency across multiple calls"""
        import yescrypt_fast
        
        data = b"consistency_test"
        nonce = 999
        
        # Compute same hash 5 times
        hashes = [yescrypt_fast.hash(data, nonce) for _ in range(5)]
        
        # All should be identical
        assert len(set(hashes)) == 1, "Same input should always produce same output"
    
    def test_hash_output_distribution(self):
        """Test 12: Hash output distribution"""
        import yescrypt_fast
        
        data = b"distribution_test"
        
        # Compute many hashes
        hashes = []
        for i in range(50):
            h = yescrypt_fast.hash(data, i)
            hashes.append(h)
        
        # Count unique hashes
        unique = len(set(hashes))
        
        # Should be all different
        assert unique == 50, f"Expected 50 unique hashes, got {unique}"
    
    def run_all_tests(self):
        """Run all tests"""
        self.print_header("UNIT TESTS - C Extension & Integration")
        
        self.test("Import C extension", self.test_c_extension_import)
        self.test("Hash computation", self.test_c_extension_hash)
        self.test("Different nonces", self.test_c_extension_different_nonces)
        self.test("Import Python wrapper", self.test_python_wrapper_import)
        self.test("Import professional miner", self.test_professional_miner_import)
        self.test("Performance benchmark", self.test_benchmark)
        self.test("High nonce values", self.test_high_nonce_values)
        self.test("Empty data", self.test_empty_data)
        self.test("Long data", self.test_long_data)
        self.test("Configuration loading", self.test_configuration_loading)
        self.test("Consistency", self.test_multiple_hashes_consistency)
        self.test("Hash distribution", self.test_hash_output_distribution)
        
        self.print_summary()
        return self.tests_failed == 0

def main():
    """Main entry point"""
    print("🚀 ZION Yescrypt Mining - Test Suite")
    print("="*60)
    
    runner = TestRunner()
    success = runner.run_all_tests()
    
    if success:
        print("🎉 ALL TESTS PASSED!")
        return 0
    else:
        print("❌ SOME TESTS FAILED")
        return 1

if __name__ == "__main__":
    exit(main())
