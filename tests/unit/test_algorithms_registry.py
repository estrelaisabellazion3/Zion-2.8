#!/usr/bin/env python3
"""
ZION v2.8.4 - Algorithm Registry Unit Tests
============================================

Tests for src/core/algorithms.py - ASIC-only algorithm registry.

Tests:
- list_supported() returns correct availability
- get_hash() produces consistent output
- RuntimeError when algorithm unavailable
- NO SHA256 in registry (critical validation)
- Cosmic Harmony Python mode fallback

Author: ZION Core Team
Version: 1.0
"""

import unittest
import sys
import os

# Add src/core to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src', 'core'))

from algorithms import get_hash, is_available, list_supported


class TestAlgorithmsRegistry(unittest.TestCase):
    """Unit tests for ASIC-only algorithm registry."""

    def setUp(self):
        """Set up test data."""
        self.test_data = b"ZION test block data"
        self.test_nonce = 12345

    def test_list_supported_returns_dict(self):
        """Test list_supported() returns dict with availability flags."""
        supported = list_supported()
        
        self.assertIsInstance(supported, dict, "list_supported() should return dict")
        self.assertGreater(len(supported), 0, "Should have at least one algorithm")
        
        # All values should be boolean
        for algo, available in supported.items():
            self.assertIsInstance(available, bool, f"{algo} availability must be bool")

    def test_cosmic_harmony_always_available(self):
        """Test Cosmic Harmony is always available (native ZION algo)."""
        supported = list_supported()
        
        self.assertIn('cosmic_harmony', supported, "cosmic_harmony must be in registry")
        self.assertTrue(supported['cosmic_harmony'], "cosmic_harmony must always be available")

    def test_no_sha256_in_registry(self):
        """CRITICAL: Verify SHA256 is NOT in algorithm registry."""
        supported = list_supported()
        
        # SHA256 should not exist in registry
        self.assertNotIn('sha256', supported, 
                        "CRITICAL FAILURE: SHA256 found in ASIC-only registry!")
        
        # Also check is_available
        sha256_available = is_available('sha256')
        self.assertFalse(sha256_available, 
                        "CRITICAL FAILURE: SHA256 reported as available!")

    def test_get_hash_cosmic_harmony(self):
        """Test get_hash() with cosmic_harmony produces output."""
        try:
            hash_result = get_hash('cosmic_harmony', self.test_data, self.test_nonce)
            
            # Should return hex string
            self.assertIsInstance(hash_result, str, "Hash should be string")
            self.assertGreater(len(hash_result), 0, "Hash should not be empty")
            
            # Should be valid hex
            int(hash_result, 16)  # Raises ValueError if not hex
            
        except Exception as e:
            self.fail(f"cosmic_harmony hashing failed: {e}")

    def test_get_hash_consistency(self):
        """Test get_hash() produces consistent results for same input."""
        hash1 = get_hash('cosmic_harmony', self.test_data, self.test_nonce)
        hash2 = get_hash('cosmic_harmony', self.test_data, self.test_nonce)
        
        self.assertEqual(hash1, hash2, 
                        "Same input should produce same hash (deterministic)")

    def test_get_hash_different_nonces(self):
        """Test get_hash() produces different results for different nonces."""
        hash1 = get_hash('cosmic_harmony', self.test_data, 1000)
        hash2 = get_hash('cosmic_harmony', self.test_data, 2000)
        
        self.assertNotEqual(hash1, hash2, 
                           "Different nonces should produce different hashes")

    def test_unavailable_algorithm_raises_error(self):
        """Test get_hash() raises RuntimeError when algorithm unavailable."""
        # Try to use algorithm that doesn't exist
        with self.assertRaises(RuntimeError) as context:
            get_hash('fake_algorithm_xyz', self.test_data, self.test_nonce)
        
        self.assertIn('not available', str(context.exception).lower(),
                     "Error message should mention unavailability")

    def test_sha256_explicitly_rejected(self):
        """CRITICAL: Test SHA256 explicitly raises error (ASIC resistance)."""
        with self.assertRaises(RuntimeError) as context:
            get_hash('sha256', self.test_data, self.test_nonce)
        
        error_msg = str(context.exception).lower()
        self.assertIn('not available', error_msg,
                     "SHA256 should raise 'not available' error")

    def test_is_available_function(self):
        """Test is_available() helper function."""
        # Cosmic Harmony should always be available
        self.assertTrue(is_available('cosmic_harmony'), 
                       "cosmic_harmony should be available")
        
        # Fake algorithm should not be available
        self.assertFalse(is_available('nonexistent_algo'), 
                        "Nonexistent algo should not be available")
        
        # SHA256 should NOT be available
        self.assertFalse(is_available('sha256'), 
                        "SHA256 should NOT be available (ASIC-only policy)")

    def test_optional_algorithms(self):
        """Test optional algorithms (randomx, yescrypt, autolykos_v2)."""
        supported = list_supported()
        
        # These may or may not be available depending on environment
        optional_algos = ['randomx', 'yescrypt', 'autolykos_v2']
        
        for algo in optional_algos:
            if algo in supported and supported[algo]:
                # If available, should be able to hash
                try:
                    hash_result = get_hash(algo, self.test_data, self.test_nonce)
                    self.assertIsInstance(hash_result, str, 
                                        f"{algo} should return string hash")
                except Exception as e:
                    self.fail(f"{algo} marked available but hashing failed: {e}")

    def test_registry_completeness(self):
        """Test registry includes all expected ASIC-resistant algorithms."""
        supported = list_supported()
        
        # Expected algorithms (excluding optional ones that may not be installed)
        expected = ['cosmic_harmony']  # Always required
        
        for algo in expected:
            self.assertIn(algo, supported, f"{algo} must be in registry")

    def test_hash_output_format(self):
        """Test hash output format is consistent."""
        hash_result = get_hash('cosmic_harmony', self.test_data, self.test_nonce)
        
        # Should be hex string
        self.assertTrue(all(c in '0123456789abcdef' for c in hash_result.lower()),
                       "Hash should contain only hex characters")
        
        # Typical hash length (SHA-256 equivalent = 64 chars, but may vary)
        self.assertGreater(len(hash_result), 16, 
                          "Hash should be at least 16 chars")
        self.assertLess(len(hash_result), 256, 
                       "Hash should be reasonable length")


class TestASICResistancePolicy(unittest.TestCase):
    """Tests specifically for ASIC resistance enforcement."""

    def test_no_asic_algorithms_in_registry(self):
        """Verify NO ASIC-friendly algorithms in registry."""
        supported = list_supported()
        
        # ASIC-friendly algorithms that should NOT be present
        forbidden = ['sha256', 'sha256d', 'scrypt']  # scrypt is ASIC-mineable now
        
        for algo in forbidden:
            self.assertNotIn(algo, supported, 
                           f"ASIC-friendly algorithm {algo} found in registry!")

    def test_all_supported_are_asic_resistant(self):
        """Verify all supported algorithms are ASIC-resistant."""
        supported = list_supported()
        
        # ASIC-resistant algorithms
        asic_resistant = ['cosmic_harmony', 'randomx', 'yescrypt', 'autolykos_v2']
        
        for algo in supported.keys():
            self.assertIn(algo, asic_resistant, 
                         f"Unknown algorithm {algo} - verify ASIC resistance!")


if __name__ == '__main__':
    print("🧪 ZION v2.8.4 - Algorithm Registry Unit Tests")
    print("=" * 60)
    print()
    
    # Run tests with verbose output
    suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print()
    print("=" * 60)
    
    if result.wasSuccessful():
        print("✅ All tests passed! Algorithm registry is ASIC-only compliant.")
        sys.exit(0)
    else:
        print("❌ Some tests failed! Review algorithm registry implementation.")
        sys.exit(1)
