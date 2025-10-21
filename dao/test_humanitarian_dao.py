#!/usr/bin/env python3
"""
Unit tests for ZION Humanitarian DAO

Tests cover:
- Proposal creation
- Voting mechanism with different ZION balances
- Vote counting and approval percentage
- Voting deadline enforcement
- Proposal execution (approved and rejected)
- Treasury balance updates
"""

import unittest
import time
import os
import sqlite3
from pathlib import Path

# Add parent directory to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from dao.humanitarian_dao import (
    HumanitarianDAO,
    ProjectCategory,
    Proposal,
    Vote,
    ProposalStatus
)


class TestHumanitarianDAO(unittest.TestCase):
    """Test suite for Humanitarian DAO"""
    
    def setUp(self):
        """Set up test database"""
        self.test_db = "test_humanitarian_dao.db"
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
        
        self.dao = HumanitarianDAO(db_path=self.test_db)
        
        # Add initial treasury funds
        self.dao.add_to_treasury(1000000.0, block_height=1, description="Test funding")
    
    def tearDown(self):
        """Clean up test database"""
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
    
    def test_01_progressive_fee_schedule(self):
        """Test progressive humanitarian fee calculation"""
        print("\n\n🧪 TEST 1: Progressive Fee Schedule")
        
        # Test Year 1 (10%)
        genesis_time = time.time()
        current_time = genesis_time + (100 * 24 * 60 * 60)  # 100 days
        HumanitarianDAO.GENESIS_TIMESTAMP = genesis_time
        
        fee = HumanitarianDAO.calculate_humanitarian_fee_percentage(current_time)
        self.assertEqual(fee, 0.10, "Year 1 should be 10%")
        print(f"✅ Year 1 (100 days): {fee * 100}% - PASSED")
        
        # Test Year 2 (15%)
        current_time = genesis_time + (500 * 24 * 60 * 60)  # 500 days
        fee = HumanitarianDAO.calculate_humanitarian_fee_percentage(current_time)
        self.assertEqual(fee, 0.15, "Year 2-3 should be 15%")
        print(f"✅ Year 2 (500 days): {fee * 100}% - PASSED")
        
        # Test Year 4 (20%)
        current_time = genesis_time + (1200 * 24 * 60 * 60)  # 1200 days
        fee = HumanitarianDAO.calculate_humanitarian_fee_percentage(current_time)
        self.assertEqual(fee, 0.20, "Year 4-5 should be 20%")
        print(f"✅ Year 4 (1200 days): {fee * 100}% - PASSED")
        
        # Test Year 6+ (25%)
        current_time = genesis_time + (2000 * 24 * 60 * 60)  # 2000 days
        fee = HumanitarianDAO.calculate_humanitarian_fee_percentage(current_time)
        self.assertEqual(fee, 0.25, "Year 6+ should be 25%")
        print(f"✅ Year 6+ (2000 days): {fee * 100}% - PASSED")
    
    def test_02_proposal_creation(self):
        """Test creating humanitarian proposals"""
        print("\n\n🧪 TEST 2: Proposal Creation")
        
        proposal = self.dao.create_proposal(
            title="Test Water Project",
            description="Test description",
            category=ProjectCategory.WATER,
            recipient_address="TEST_WALLET_123",
            recipient_organization="Test NGO",
            amount_zion=100000.0,
            amount_usd=50000.0,
            location="Test Location",
            beneficiaries=1000,
            proposer_address="PROPOSER_WALLET"
        )
        
        self.assertEqual(proposal.id, 1)
        self.assertEqual(proposal.title, "Test Water Project")
        self.assertEqual(proposal.amount_zion, 100000.0)
        self.assertEqual(proposal.status, "active")
        self.assertTrue(proposal.is_voting_open())
        
        print(f"✅ Proposal #{proposal.id} created successfully")
        print(f"   Title: {proposal.title}")
        print(f"   Amount: {proposal.amount_zion} ZION")
        print(f"   Status: {proposal.status}")
    
    def test_03_insufficient_treasury(self):
        """Test proposal creation with insufficient treasury"""
        print("\n\n🧪 TEST 3: Insufficient Treasury Handling")
        
        with self.assertRaises(ValueError) as context:
            self.dao.create_proposal(
                title="Too Expensive Project",
                description="Test",
                category=ProjectCategory.WATER,
                recipient_address="TEST_WALLET",
                recipient_organization="Test NGO",
                amount_zion=2000000.0,  # More than treasury
                amount_usd=1000000.0,
                location="Test",
                beneficiaries=100,
                proposer_address="PROPOSER"
            )
        
        self.assertIn("Insufficient treasury funds", str(context.exception))
        print(f"✅ Correctly rejected proposal exceeding treasury")
        print(f"   Error: {context.exception}")
    
    def test_04_voting_mechanism(self):
        """Test voting on proposals with different voting powers"""
        print("\n\n🧪 TEST 4: Voting Mechanism")
        
        # Create proposal
        proposal = self.dao.create_proposal(
            title="Voting Test Project",
            description="Test voting",
            category=ProjectCategory.ENVIRONMENT,
            recipient_address="TEST_WALLET",
            recipient_organization="Test NGO",
            amount_zion=50000.0,
            amount_usd=25000.0,
            location="Test",
            beneficiaries=500,
            proposer_address="PROPOSER"
        )
        
        # Voter 1: 10,000 ZION - votes FOR
        vote1 = self.dao.vote(
            proposal_id=proposal.id,
            voter_address="VOTER_1",
            voting_power=10000.0,
            support=True
        )
        
        # Voter 2: 5,000 ZION - votes AGAINST
        vote2 = self.dao.vote(
            proposal_id=proposal.id,
            voter_address="VOTER_2",
            voting_power=5000.0,
            support=False
        )
        
        # Voter 3: 8,000 ZION - votes FOR
        vote3 = self.dao.vote(
            proposal_id=proposal.id,
            voter_address="VOTER_3",
            voting_power=8000.0,
            support=True
        )
        
        # Check vote counts
        updated_proposal = self.dao.get_proposal(proposal.id)
        
        self.assertEqual(updated_proposal.votes_for, 18000.0)  # 10k + 8k
        self.assertEqual(updated_proposal.votes_against, 5000.0)
        self.assertEqual(updated_proposal.voter_count, 3)
        
        approval = updated_proposal.vote_percentage()
        self.assertAlmostEqual(approval, 78.26, places=1)  # 18000/(18000+5000) * 100
        
        print(f"✅ Votes recorded successfully")
        print(f"   FOR: {updated_proposal.votes_for} ZION (from 2 voters)")
        print(f"   AGAINST: {updated_proposal.votes_against} ZION (from 1 voter)")
        print(f"   Approval: {approval:.2f}%")
    
    def test_05_duplicate_voting_prevention(self):
        """Test that voters cannot vote twice"""
        print("\n\n🧪 TEST 5: Duplicate Vote Prevention")
        
        proposal = self.dao.create_proposal(
            title="Duplicate Vote Test",
            description="Test",
            category=ProjectCategory.EDUCATION,
            recipient_address="TEST_WALLET",
            recipient_organization="Test NGO",
            amount_zion=30000.0,
            amount_usd=15000.0,
            location="Test",
            beneficiaries=200,
            proposer_address="PROPOSER"
        )
        
        # First vote succeeds
        self.dao.vote(proposal.id, "VOTER_1", 10000.0, True)
        
        # Second vote from same address should fail
        with self.assertRaises(ValueError) as context:
            self.dao.vote(proposal.id, "VOTER_1", 10000.0, False)
        
        self.assertIn("already voted", str(context.exception))
        print(f"✅ Duplicate vote correctly prevented")
        print(f"   Error: {context.exception}")
    
    def test_06_voting_deadline_enforcement(self):
        """Test that votes after deadline are rejected"""
        print("\n\n🧪 TEST 6: Voting Deadline Enforcement")
        
        proposal = self.dao.create_proposal(
            title="Deadline Test",
            description="Test",
            category=ProjectCategory.MEDICAL,
            recipient_address="TEST_WALLET",
            recipient_organization="Test NGO",
            amount_zion=20000.0,
            amount_usd=10000.0,
            location="Test",
            beneficiaries=100,
            proposer_address="PROPOSER"
        )
        
        # Manually set deadline to past
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE proposals 
            SET voting_deadline = ? 
            WHERE id = ?
        """, (time.time() - 3600, proposal.id))  # 1 hour ago
        conn.commit()
        conn.close()
        
        # Try to vote after deadline
        with self.assertRaises(ValueError) as context:
            self.dao.vote(proposal.id, "VOTER_1", 10000.0, True)
        
        self.assertIn("Voting period ended", str(context.exception))
        print(f"✅ Late vote correctly rejected")
        print(f"   Error: {context.exception}")
    
    def test_07_proposal_execution_approved(self):
        """Test executing an approved proposal"""
        print("\n\n🧪 TEST 7: Proposal Execution (APPROVED)")
        
        initial_balance = self.dao.get_treasury_balance()
        
        proposal = self.dao.create_proposal(
            title="Approved Project",
            description="Will pass",
            category=ProjectCategory.WATER,
            recipient_address="RECIPIENT_WALLET",
            recipient_organization="Winner NGO",
            amount_zion=100000.0,
            amount_usd=50000.0,
            location="Test",
            beneficiaries=5000,
            proposer_address="PROPOSER"
        )
        
        # Vote with majority FOR (80% approval)
        self.dao.vote(proposal.id, "VOTER_1", 80000.0, True)
        self.dao.vote(proposal.id, "VOTER_2", 20000.0, False)
        
        # Set deadline to past so we can execute
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE proposals 
            SET voting_deadline = ? 
            WHERE id = ?
        """, (time.time() - 1, proposal.id))
        conn.commit()
        conn.close()
        
        # Execute proposal
        result = self.dao.execute_proposal(proposal.id)
        
        self.assertTrue(result)
        
        # Check proposal status
        executed_proposal = self.dao.get_proposal(proposal.id)
        self.assertEqual(executed_proposal.status, "executed")
        self.assertTrue(len(executed_proposal.tx_hash) > 0)
        
        # Check treasury balance decreased
        final_balance = self.dao.get_treasury_balance()
        self.assertEqual(final_balance, initial_balance - 100000.0)
        
        print(f"✅ Proposal approved and executed")
        print(f"   Approval: {executed_proposal.vote_percentage():.1f}%")
        print(f"   TX Hash: {executed_proposal.tx_hash}")
        print(f"   Treasury: {initial_balance:.2f} → {final_balance:.2f} ZION")
    
    def test_08_proposal_execution_rejected(self):
        """Test rejecting a proposal with insufficient votes"""
        print("\n\n🧪 TEST 8: Proposal Execution (REJECTED)")
        
        initial_balance = self.dao.get_treasury_balance()
        
        proposal = self.dao.create_proposal(
            title="Rejected Project",
            description="Will fail",
            category=ProjectCategory.EDUCATION,
            recipient_address="LOSER_WALLET",
            recipient_organization="Loser NGO",
            amount_zion=50000.0,
            amount_usd=25000.0,
            location="Test",
            beneficiaries=1000,
            proposer_address="PROPOSER"
        )
        
        # Vote with majority AGAINST (30% approval)
        self.dao.vote(proposal.id, "VOTER_1", 30000.0, True)
        self.dao.vote(proposal.id, "VOTER_2", 70000.0, False)
        
        # Set deadline to past
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE proposals 
            SET voting_deadline = ? 
            WHERE id = ?
        """, (time.time() - 1, proposal.id))
        conn.commit()
        conn.close()
        
        # Try to execute (should be rejected)
        result = self.dao.execute_proposal(proposal.id)
        
        self.assertFalse(result)
        
        # Check proposal status
        rejected_proposal = self.dao.get_proposal(proposal.id)
        self.assertEqual(rejected_proposal.status, "rejected")
        
        # Check treasury balance unchanged
        final_balance = self.dao.get_treasury_balance()
        self.assertEqual(final_balance, initial_balance)
        
        print(f"✅ Proposal correctly rejected")
        print(f"   Approval: {rejected_proposal.vote_percentage():.1f}%")
        print(f"   Status: {rejected_proposal.status}")
        print(f"   Treasury unchanged: {final_balance:.2f} ZION")
    
    def test_09_treasury_management(self):
        """Test treasury deposit and balance tracking"""
        print("\n\n🧪 TEST 9: Treasury Management")
        
        initial_balance = self.dao.get_treasury_balance()
        
        # Add deposits
        self.dao.add_to_treasury(50000.0, block_height=100, description="Block reward tithe")
        self.dao.add_to_treasury(30000.0, block_height=101, description="Block reward tithe")
        
        final_balance = self.dao.get_treasury_balance()
        
        self.assertEqual(final_balance, initial_balance + 80000.0)
        
        print(f"✅ Treasury management working")
        print(f"   Initial: {initial_balance:.2f} ZION")
        print(f"   Deposits: +80,000.00 ZION")
        print(f"   Final: {final_balance:.2f} ZION")
    
    def test_10_get_active_proposals(self):
        """Test retrieving only active proposals"""
        print("\n\n🧪 TEST 10: Active Proposals Query")
        
        # Create 3 proposals
        p1 = self.dao.create_proposal(
            "Project 1", "Desc", ProjectCategory.WATER,
            "ADDR1", "NGO1", 10000.0, 5000.0, "Loc1", 100, "PROP1"
        )
        
        p2 = self.dao.create_proposal(
            "Project 2", "Desc", ProjectCategory.FOOD,
            "ADDR2", "NGO2", 20000.0, 10000.0, "Loc2", 200, "PROP2"
        )
        
        p3 = self.dao.create_proposal(
            "Project 3", "Desc", ProjectCategory.SHELTER,
            "ADDR3", "NGO3", 30000.0, 15000.0, "Loc3", 300, "PROP3"
        )
        
        # Mark p2 as executed
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        cursor.execute("UPDATE proposals SET status = 'executed' WHERE id = ?", (p2.id,))
        conn.commit()
        conn.close()
        
        # Get active proposals
        active = self.dao.get_active_proposals()
        
        self.assertEqual(len(active), 2)  # p1 and p3
        active_ids = [p.id for p in active]
        self.assertIn(p1.id, active_ids)
        self.assertIn(p3.id, active_ids)
        self.assertNotIn(p2.id, active_ids)
        
        print(f"✅ Active proposals query working")
        print(f"   Total proposals: 3")
        print(f"   Active proposals: {len(active)}")
        print(f"   Executed proposals: 1")


def run_tests():
    """Run all tests with pretty output"""
    print("=" * 70)
    print("🧪 ZION HUMANITARIAN DAO - TEST SUITE")
    print("=" * 70)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestHumanitarianDAO)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 TEST SUMMARY")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"✅ Passed: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ Failed: {len(result.failures)}")
    print(f"⚠️  Errors: {len(result.errors)}")
    print("=" * 70)
    
    if result.wasSuccessful():
        print("\n🎉 ALL TESTS PASSED! DAO is ready for production.")
        return 0
    else:
        print("\n❌ SOME TESTS FAILED. Please fix before deploying.")
        return 1


if __name__ == "__main__":
    exit(run_tests())
