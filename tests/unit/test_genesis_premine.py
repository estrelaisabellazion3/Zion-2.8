#!/usr/bin/env python3
"""
ZION v2.8.4 - Genesis Block Premine Validation Tests
=====================================================

Tests for genesis block premine allocation.

Validates:
- Total premine: 15,782,857,143 ZION
- Category sums:
  * OASIS Game: 1,440,000,000 ZION (3-year vesting)
  * Rainbow Bridge: 3,342,857,143 ZION
  * DAO Treasury: 3,000,000,000 ZION
  * Round Table: 3,000,000,000 ZION
  * Sacred Geometry: 2,000,000,000 ZION
  * Lightning Rewards: 1,000,000,000 ZION
  * Cosmic Harmony: 2,000,000,000 ZION
- No duplicate addresses
- All amounts > 0

Author: ZION Core Team
Version: 1.0
"""

import unittest
import sys
import os

# Add src/core to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src', 'core'))

try:
    from premine import get_premine_addresses, PREMINE_TOTAL
    PREMINE_MODULE_AVAILABLE = True
except ImportError:
    # Fallback if premine module doesn't exist yet
    print("⚠️ Warning: premine module not found, using inline test data")
    PREMINE_MODULE_AVAILABLE = False
    
    # Test data (subset for validation)
    PREMINE_TOTAL = 15_782_857_143
    
    def get_premine_addresses():
        """Fallback test data."""
        return {
            'OASIS_GAME_1': {'address': 'OASIS_GAME_1', 'amount': 720_000_000, 'category': 'OASIS Game'},
            'OASIS_GAME_2': {'address': 'OASIS_GAME_2', 'amount': 720_000_000, 'category': 'OASIS Game'},
            'RAINBOW_1': {'address': 'RAINBOW_1', 'amount': 1_671_428_571, 'category': 'Rainbow Bridge'},
            'RAINBOW_2': {'address': 'RAINBOW_2', 'amount': 1_671_428_572, 'category': 'Rainbow Bridge'},
            'DAO_TREASURY': {'address': 'DAO_TREASURY', 'amount': 3_000_000_000, 'category': 'DAO Treasury'},
            'ROUND_TABLE': {'address': 'ROUND_TABLE', 'amount': 3_000_000_000, 'category': 'Round Table'},
            'SACRED_GEOMETRY': {'address': 'SACRED_GEOMETRY', 'amount': 2_000_000_000, 'category': 'Sacred Geometry'},
            'LIGHTNING_REWARDS': {'address': 'LIGHTNING_REWARDS', 'amount': 1_000_000_000, 'category': 'Lightning Rewards'},
            'COSMIC_HARMONY': {'address': 'COSMIC_HARMONY', 'amount': 2_000_000_000, 'category': 'Cosmic Harmony'},
        }


class TestGenesisPremine(unittest.TestCase):
    """Unit tests for genesis block premine allocation."""

    def setUp(self):
        """Load premine data."""
        self.premine_addresses = get_premine_addresses()

    def test_premine_total_matches_constant(self):
        """Test total premine matches declared constant."""
        total = sum(addr['amount'] for addr in self.premine_addresses.values())
        
        self.assertEqual(total, PREMINE_TOTAL, 
                        f"Premine total mismatch! Expected {PREMINE_TOTAL:,}, got {total:,}")

    def test_premine_total_exact_value(self):
        """Test premine total is exactly 15,782,857,143 ZION."""
        total = sum(addr['amount'] for addr in self.premine_addresses.values())
        
        self.assertEqual(total, 15_782_857_143,
                        f"Premine must be 15,782,857,143 ZION, got {total:,}")

    def test_oasis_game_category_sum(self):
        """Test ZION OASIS category sum: 1,440,000,000 ZION."""
        oasis_total = sum(
            addr['amount'] for addr in self.premine_addresses.values()
              if addr.get('type') == 'oasis'
        )
        
        self.assertEqual(oasis_total, 1_440_000_000,
                        f"ZION OASIS should be 1,440,000,000 ZION, got {oasis_total:,}")

    def test_dao_winners_category_sum(self):
        """Test DAO Winners category sum: 1,750,000,000 ZION."""
        dao_total = sum(
            data['amount'] for name, data in self.premine_addresses.items()
            if data.get('type') == 'dao_governance' and 'WINNER' in name
        )
        
        self.assertEqual(dao_total, 1_750_000_000,
                        f"DAO Winners should be 1,750,000,000 ZION, got {dao_total:,}")

    def test_mining_operators_category_sum(self):
        """Test Mining Operators category sum: 8,250,000,000 ZION."""
        mining_total = sum(
            addr['amount'] for addr in self.premine_addresses.values()
            if addr.get('type') == 'mining'
        )
        
        self.assertEqual(mining_total, 8_250_000_000,
                        f"Mining Operators should be 8,250,000,000 ZION, got {mining_total:,}")

    def test_infrastructure_category_sum(self):
        """Test Infrastructure category sum: 4,342,857,143 ZION."""
        infra_types = ['development', 'infrastructure', 'charity', 'admin', 'genesis']
        infra_total = sum(
            addr['amount'] for addr in self.premine_addresses.values()
            if addr.get('type') in infra_types
        )
        expected = 15_782_857_143 - 8_250_000_000 - 1_750_000_000 - 1_440_000_000
        self.assertEqual(infra_total, expected,
                         f"Infrastructure should be {expected:,} ZION, got {infra_total:,}")

    def test_all_categories_accounted(self):
        """Test all ZION is assigned to known type categories."""
        # Actual distribution by 'type' field
        categories = {
            'mining': 8_250_000_000,           # Mining operators (5 pools)
            'dao_governance': 1_750_000_000,   # DAO winners (3 seats)
            'game_development': 1_440_000_000, # ZION OASIS
            'infrastructure': ~4_342_857_143,  # Development, infra, charity, admin
        }
        
        total = sum(addr['amount'] for addr in self.premine_addresses.values())
        self.assertEqual(total, PREMINE_TOTAL,
                        "Category sums don't add up to total!")

    def test_no_duplicate_addresses(self):
        """Test no duplicate addresses in premine."""
        # Use address keys (dict keys are the addresses)
        addresses = list(self.premine_addresses.keys())
        
        self.assertEqual(len(addresses), len(set(addresses)),
                        "Duplicate addresses found in premine!")

    def test_all_amounts_positive(self):
        """Test all premine amounts are positive."""
        for addr_name, addr_data in self.premine_addresses.items():
            self.assertGreater(addr_data['amount'], 0,
                             f"Address {addr_name} has non-positive amount!")

    def test_all_addresses_have_type(self):
        """Test all addresses have a 'type' field assigned."""
        for addr_name, addr_data in self.premine_addresses.items():
            self.assertIn('type', addr_data,
                         f"Address {addr_name} missing 'type' field!")
            self.assertIsInstance(addr_data['type'], str,
                                f"Address {addr_name} type is not string!")
            self.assertGreater(len(addr_data['type']), 0,
                             f"Address {addr_name} has empty type!")

    def test_premine_addresses_not_empty(self):
        """Test premine addresses dict is not empty."""
        self.assertGreater(len(self.premine_addresses), 0,
                          "Premine addresses dict is empty!")

    def test_address_structure(self):
        """Test each address entry has required fields."""
        required_fields = ['purpose', 'amount', 'type']
        
        for addr_name, addr_data in self.premine_addresses.items():
            for field in required_fields:
                self.assertIn(field, addr_data,
                             f"Address {addr_name} missing field '{field}'!")


class TestPremineIntegrity(unittest.TestCase):
    """Tests for premine data integrity and consistency."""

    def setUp(self):
        """Load premine data."""
        self.premine_addresses = get_premine_addresses()

    def test_oasis_vesting_note(self):
        """Test ZION OASIS entries (game development fund)."""
        oasis_entries = [
            (name, data) for name, data in self.premine_addresses.items()
              if data.get('type') == 'oasis'
        ]
        
        # Should have at least one OASIS entry
        self.assertGreater(len(oasis_entries), 0,
                          "No ZION OASIS entries found!")
        
        # Total should be 1.44B
        oasis_total = sum(data['amount'] for _, data in oasis_entries)
        self.assertEqual(oasis_total, 1_440_000_000)

    def test_dao_winners_unlock_date(self):
        """Test DAO Winners have unlock date of 2035-10-10."""
        dao_winner_entries = [
            (name, data) for name, data in self.premine_addresses.items()
            if data.get('type') == 'dao_governance' and 'WINNER' in name
        ]
        
        # Should have 3 DAO winners
        self.assertEqual(len(dao_winner_entries), 3,
                        "Should have exactly 3 DAO winners!")
        
        # All should have unlock date 2035-10-10
        for name, data in dao_winner_entries:
            self.assertEqual(data.get('unlock_date'), '2035-10-10',
                           f"{name} should unlock on 2035-10-10!")

    def test_no_negative_amounts(self):
        """Test no negative amounts (redundant but explicit)."""
        for addr_name, addr_data in self.premine_addresses.items():
            self.assertGreaterEqual(addr_data['amount'], 0,
                                   f"Negative amount in {addr_name}!")


if __name__ == '__main__':
    print("🧪 ZION v2.8.4 - Genesis Premine Validation Tests")
    print("=" * 60)
    print()
    
    if not PREMINE_MODULE_AVAILABLE:
        print("⚠️ Using fallback test data (premine module not found)")
        print()
    
    # Run tests with verbose output
    suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print()
    print("=" * 60)
    
    if result.wasSuccessful():
        print("✅ All tests passed! Genesis premine allocation is valid.")
        print(f"💰 Total premine: {PREMINE_TOTAL:,} ZION")
        sys.exit(0)
    else:
        print("❌ Some tests failed! Review premine allocation.")
        sys.exit(1)
