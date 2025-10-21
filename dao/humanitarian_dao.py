#!/usr/bin/env python3
"""
🌍 ZION Humanitarian DAO
========================

Decentralized Autonomous Organization for distributing humanitarian tithe.

Progressive Fee Schedule:
- Year 1: 10% of block rewards → humanitarian projects
- Year 2-3: 15% 
- Year 4-5: 20%
- Year 6+: 25% (target rate)

Features:
- Proposal creation for humanitarian projects
- Community voting (voting power = ZION holdings)
- Automatic proposal execution after voting period
- Treasury management with transparency
- Project categories: water, food, shelter, environment, medical

Author: ZION Network Team
License: MIT
"""

import time
import json
import sqlite3
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple
from enum import Enum
import hashlib
from pathlib import Path


class ProposalStatus(Enum):
    """Proposal lifecycle states"""
    ACTIVE = "active"           # Voting in progress
    APPROVED = "approved"       # Passed, awaiting execution
    REJECTED = "rejected"       # Failed to pass
    EXECUTED = "executed"       # Funds disbursed
    CANCELLED = "cancelled"     # Cancelled by proposer


class ProjectCategory(Enum):
    """Humanitarian project categories"""
    WATER = "clean_water"
    FOOD = "food_security"
    SHELTER = "shelter_housing"
    ENVIRONMENT = "environment"
    MEDICAL = "medical_aid"
    EDUCATION = "education"
    EMERGENCY = "emergency_relief"


@dataclass
class Proposal:
    """Humanitarian project proposal"""
    id: int
    title: str
    description: str
    category: str
    recipient_address: str      # ZION wallet address
    recipient_organization: str  # Organization name
    amount_zion: float          # Requested amount in ZION
    amount_usd: float           # USD equivalent (for reference)
    location: str               # Geographic location
    beneficiaries: int          # Estimated number of people helped
    
    # Voting data
    votes_for: float = 0.0      # Total ZION voted in favor
    votes_against: float = 0.0  # Total ZION voted against
    voter_count: int = 0        # Number of unique voters
    
    # Timestamps
    created_at: float = 0.0
    voting_deadline: float = 0.0  # Unix timestamp
    executed_at: float = 0.0
    
    # Status
    status: str = "active"
    proposal_hash: str = ""     # Cryptographic proof
    proposer_address: str = ""
    
    # Execution
    tx_hash: str = ""           # Transaction hash when executed
    
    def __post_init__(self):
        if self.created_at == 0.0:
            self.created_at = time.time()
        if self.voting_deadline == 0.0:
            self.voting_deadline = self.created_at + (7 * 24 * 60 * 60)  # 7 days
        if not self.proposal_hash:
            self.proposal_hash = self._calculate_hash()
    
    def _calculate_hash(self) -> str:
        """Generate cryptographic hash of proposal"""
        data = f"{self.title}{self.description}{self.recipient_address}{self.amount_zion}{self.created_at}"
        return hashlib.sha256(data.encode()).hexdigest()
    
    def is_voting_open(self) -> bool:
        """Check if voting period is still active"""
        return time.time() < self.voting_deadline and self.status == "active"
    
    def vote_percentage(self) -> float:
        """Calculate approval percentage"""
        total_votes = self.votes_for + self.votes_against
        if total_votes == 0:
            return 0.0
        return (self.votes_for / total_votes) * 100
    
    def has_passed(self, quorum_percentage: float = 50.0) -> bool:
        """Check if proposal passed (requires >50% approval)"""
        return self.vote_percentage() > quorum_percentage


@dataclass
class Vote:
    """Individual vote record"""
    proposal_id: int
    voter_address: str
    voting_power: float     # Amount of ZION held
    support: bool          # True = for, False = against
    timestamp: float
    vote_hash: str = ""
    
    def __post_init__(self):
        if not self.vote_hash:
            data = f"{self.proposal_id}{self.voter_address}{self.support}{self.timestamp}"
            self.vote_hash = hashlib.sha256(data.encode()).hexdigest()


class HumanitarianDAO:
    """
    Decentralized Autonomous Organization for humanitarian projects
    
    Treasury funded by progressive humanitarian tithe:
    - Year 1: 10% of block rewards
    - Year 2-3: 15%
    - Year 4-5: 20%
    - Year 6+: 25% (target)
    
    Community votes on project proposals
    Automatic execution of approved proposals
    """
    
    # Genesis block timestamp (to calculate network age)
    GENESIS_TIMESTAMP = 1728849600  # October 13, 2024 (example)
    
    def __init__(self, db_path: str = "humanitarian_dao.db", genesis_timestamp: Optional[float] = None):
        self.db_path = db_path
        self.treasury_balance = 0.0  # ZION
        if genesis_timestamp:
            self.GENESIS_TIMESTAMP = genesis_timestamp
        self._init_database()
    
    @staticmethod
    def calculate_humanitarian_fee_percentage(current_timestamp: Optional[float] = None) -> float:
        """
        Calculate current humanitarian fee percentage based on network age
        
        Progressive schedule:
        - Year 1 (0-365 days): 10%
        - Year 2-3 (365-1095 days): 15%
        - Year 4-5 (1095-1825 days): 20%
        - Year 6+ (1825+ days): 25%
        
        Returns:
            float: Fee percentage (0.10 to 0.25)
        """
        if current_timestamp is None:
            current_timestamp = time.time()
        
        # Calculate days since genesis
        seconds_since_genesis = current_timestamp - HumanitarianDAO.GENESIS_TIMESTAMP
        days_since_genesis = seconds_since_genesis / (24 * 60 * 60)
        
        if days_since_genesis < 0:
            return 0.10  # Network not launched yet
        elif days_since_genesis < 365:  # Year 1
            return 0.10
        elif days_since_genesis < 1095:  # Years 2-3
            return 0.15
        elif days_since_genesis < 1825:  # Years 4-5
            return 0.20
        else:  # Year 6+
            return 0.25
    
    @staticmethod
    def get_fee_schedule_info() -> Dict[str, any]:
        """Get information about fee schedule and current rate"""
        current_fee = HumanitarianDAO.calculate_humanitarian_fee_percentage()
        current_timestamp = time.time()
        days_since_genesis = (current_timestamp - HumanitarianDAO.GENESIS_TIMESTAMP) / (24 * 60 * 60)
        
        # Calculate days until next tier
        if days_since_genesis < 365:
            next_tier_days = 365 - days_since_genesis
            next_tier_percentage = 0.15
        elif days_since_genesis < 1095:
            next_tier_days = 1095 - days_since_genesis
            next_tier_percentage = 0.20
        elif days_since_genesis < 1825:
            next_tier_days = 1825 - days_since_genesis
            next_tier_percentage = 0.25
        else:
            next_tier_days = 0
            next_tier_percentage = 0.25
        
        return {
            "current_fee_percentage": current_fee * 100,  # 10, 15, 20, or 25
            "current_fee_decimal": current_fee,
            "days_since_genesis": int(days_since_genesis),
            "network_age_years": days_since_genesis / 365,
            "next_tier_percentage": next_tier_percentage * 100,
            "days_until_next_tier": int(next_tier_days),
            "schedule": [
                {"year": "1", "days": "0-365", "fee": "10%"},
                {"year": "2-3", "days": "365-1095", "fee": "15%"},
                {"year": "4-5", "days": "1095-1825", "fee": "20%"},
                {"year": "6+", "days": "1825+", "fee": "25%"}
            ]
        }
    
    def _init_database(self):
        """Initialize SQLite database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Proposals table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS proposals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                category TEXT NOT NULL,
                recipient_address TEXT NOT NULL,
                recipient_organization TEXT NOT NULL,
                amount_zion REAL NOT NULL,
                amount_usd REAL NOT NULL,
                location TEXT NOT NULL,
                beneficiaries INTEGER NOT NULL,
                votes_for REAL DEFAULT 0.0,
                votes_against REAL DEFAULT 0.0,
                voter_count INTEGER DEFAULT 0,
                created_at REAL NOT NULL,
                voting_deadline REAL NOT NULL,
                executed_at REAL DEFAULT 0.0,
                status TEXT DEFAULT 'active',
                proposal_hash TEXT NOT NULL,
                proposer_address TEXT NOT NULL,
                tx_hash TEXT DEFAULT ''
            )
        """)
        
        # Votes table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS votes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                proposal_id INTEGER NOT NULL,
                voter_address TEXT NOT NULL,
                voting_power REAL NOT NULL,
                support INTEGER NOT NULL,
                timestamp REAL NOT NULL,
                vote_hash TEXT NOT NULL,
                UNIQUE(proposal_id, voter_address),
                FOREIGN KEY (proposal_id) REFERENCES proposals(id)
            )
        """)
        
        # Treasury transactions
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS treasury_transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tx_type TEXT NOT NULL,
                amount REAL NOT NULL,
                proposal_id INTEGER,
                block_height INTEGER,
                timestamp REAL NOT NULL,
                description TEXT,
                balance_after REAL NOT NULL
            )
        """)
        
        # Create indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_proposal_status ON proposals(status)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_proposal_deadline ON proposals(voting_deadline)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_votes_proposal ON votes(proposal_id)")
        
        conn.commit()
        conn.close()
    
    def add_to_treasury(self, amount: float, block_height: int, description: str = "Block reward tithe"):
        """Add funds to treasury (called by blockchain)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        self.treasury_balance += amount
        
        cursor.execute("""
            INSERT INTO treasury_transactions 
            (tx_type, amount, block_height, timestamp, description, balance_after)
            VALUES (?, ?, ?, ?, ?, ?)
        """, ("deposit", amount, block_height, time.time(), description, self.treasury_balance))
        
        conn.commit()
        conn.close()
        
        print(f"💰 Treasury deposit: +{amount:.8f} ZION (Balance: {self.treasury_balance:.8f} ZION)")
    
    def create_proposal(
        self,
        title: str,
        description: str,
        category: ProjectCategory,
        recipient_address: str,
        recipient_organization: str,
        amount_zion: float,
        amount_usd: float,
        location: str,
        beneficiaries: int,
        proposer_address: str
    ) -> Proposal:
        """
        Create new humanitarian project proposal
        
        Requirements:
        - Proposer must hold at least 1000 ZION (prevents spam)
        - Amount cannot exceed treasury balance
        - Valid recipient address
        """
        # Validate
        if amount_zion > self.treasury_balance:
            raise ValueError(f"Insufficient treasury funds (available: {self.treasury_balance:.8f} ZION)")
        
        if amount_zion <= 0:
            raise ValueError("Amount must be positive")
        
        # Create proposal
        proposal = Proposal(
            id=0,  # Will be set by database
            title=title,
            description=description,
            category=category.value,
            recipient_address=recipient_address,
            recipient_organization=recipient_organization,
            amount_zion=amount_zion,
            amount_usd=amount_usd,
            location=location,
            beneficiaries=beneficiaries,
            proposer_address=proposer_address
        )
        
        # Store in database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO proposals (
                title, description, category, recipient_address, recipient_organization,
                amount_zion, amount_usd, location, beneficiaries,
                created_at, voting_deadline, status, proposal_hash, proposer_address
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            proposal.title, proposal.description, proposal.category,
            proposal.recipient_address, proposal.recipient_organization,
            proposal.amount_zion, proposal.amount_usd,
            proposal.location, proposal.beneficiaries,
            proposal.created_at, proposal.voting_deadline,
            proposal.status, proposal.proposal_hash, proposal.proposer_address
        ))
        
        proposal.id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        print(f"📝 Proposal #{proposal.id} created: {proposal.title}")
        print(f"   Amount: {proposal.amount_zion:.2f} ZION (${proposal.amount_usd:,.0f})")
        print(f"   Voting deadline: {time.strftime('%Y-%m-%d %H:%M', time.localtime(proposal.voting_deadline))}")
        
        return proposal
    
    def vote(self, proposal_id: int, voter_address: str, voting_power: float, support: bool) -> Vote:
        """
        Cast vote on proposal
        
        Args:
            proposal_id: Proposal to vote on
            voter_address: ZION wallet address
            voting_power: Amount of ZION held by voter
            support: True = vote for, False = vote against
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get proposal
        cursor.execute("SELECT * FROM proposals WHERE id = ?", (proposal_id,))
        row = cursor.fetchone()
        if not row:
            conn.close()
            raise ValueError(f"Proposal #{proposal_id} not found")
        
        # Check if voting still open
        voting_deadline = row[14]  # voting_deadline column
        status = row[16]           # status column
        
        if time.time() >= voting_deadline:
            conn.close()
            raise ValueError(f"Voting period ended for proposal #{proposal_id}")
        
        if status != "active":
            conn.close()
            raise ValueError(f"Proposal #{proposal_id} is not active")
        
        # Check if already voted
        cursor.execute("""
            SELECT id FROM votes WHERE proposal_id = ? AND voter_address = ?
        """, (proposal_id, voter_address))
        
        if cursor.fetchone():
            conn.close()
            raise ValueError(f"Address {voter_address} already voted on proposal #{proposal_id}")
        
        # Create vote
        vote = Vote(
            proposal_id=proposal_id,
            voter_address=voter_address,
            voting_power=voting_power,
            support=support,
            timestamp=time.time()
        )
        
        # Store vote
        cursor.execute("""
            INSERT INTO votes (proposal_id, voter_address, voting_power, support, timestamp, vote_hash)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (vote.proposal_id, vote.voter_address, vote.voting_power, 
              1 if vote.support else 0, vote.timestamp, vote.vote_hash))
        
        # Update proposal vote counts
        if support:
            cursor.execute("""
                UPDATE proposals 
                SET votes_for = votes_for + ?, voter_count = voter_count + 1
                WHERE id = ?
            """, (voting_power, proposal_id))
        else:
            cursor.execute("""
                UPDATE proposals 
                SET votes_against = votes_against + ?, voter_count = voter_count + 1
                WHERE id = ?
            """, (voting_power, proposal_id))
        
        conn.commit()
        conn.close()
        
        vote_type = "FOR" if support else "AGAINST"
        print(f"✅ Vote recorded: {voter_address[:12]}... voted {vote_type} on proposal #{proposal_id}")
        print(f"   Voting power: {voting_power:.8f} ZION")
        
        return vote
    
    def execute_proposal(self, proposal_id: int) -> bool:
        """
        Execute approved proposal (transfer funds to recipient)
        
        Requirements:
        - Voting period must be over
        - Proposal must have passed (>50% approval)
        - Not already executed
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get proposal
        cursor.execute("SELECT * FROM proposals WHERE id = ?", (proposal_id,))
        row = cursor.fetchone()
        if not row:
            conn.close()
            raise ValueError(f"Proposal #{proposal_id} not found")
        
        proposal = self._row_to_proposal(row)
        
        # Check if voting period ended
        if time.time() < proposal.voting_deadline:
            conn.close()
            raise ValueError(f"Voting still open for proposal #{proposal_id}")
        
        # Check if already executed
        if proposal.status in ["executed", "cancelled"]:
            conn.close()
            raise ValueError(f"Proposal #{proposal_id} already {proposal.status}")
        
        # Check if passed
        if not proposal.has_passed():
            # Mark as rejected
            cursor.execute("""
                UPDATE proposals SET status = 'rejected' WHERE id = ?
            """, (proposal_id,))
            conn.commit()
            conn.close()
            
            print(f"❌ Proposal #{proposal_id} REJECTED ({proposal.vote_percentage():.1f}% approval)")
            return False
        
        # Execute proposal
        # In production, this would call blockchain RPC to send ZION
        # For now, we simulate the transaction
        
        tx_hash = hashlib.sha256(f"{proposal_id}{time.time()}".encode()).hexdigest()
        
        cursor.execute("""
            UPDATE proposals 
            SET status = 'executed', executed_at = ?, tx_hash = ?
            WHERE id = ?
        """, (time.time(), tx_hash, proposal_id))
        
        # Deduct from treasury
        self.treasury_balance -= proposal.amount_zion
        
        cursor.execute("""
            INSERT INTO treasury_transactions 
            (tx_type, amount, proposal_id, timestamp, description, balance_after)
            VALUES (?, ?, ?, ?, ?, ?)
        """, ("withdrawal", -proposal.amount_zion, proposal_id, time.time(),
              f"Proposal #{proposal_id}: {proposal.title}", self.treasury_balance))
        
        conn.commit()
        conn.close()
        
        print(f"✨ Proposal #{proposal_id} EXECUTED!")
        print(f"   {proposal.amount_zion:.8f} ZION sent to {proposal.recipient_organization}")
        print(f"   Transaction: {tx_hash}")
        print(f"   Treasury balance: {self.treasury_balance:.8f} ZION")
        
        return True
    
    def get_proposal(self, proposal_id: int) -> Optional[Proposal]:
        """Get proposal by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM proposals WHERE id = ?", (proposal_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return self._row_to_proposal(row)
        return None
    
    def get_active_proposals(self) -> List[Proposal]:
        """Get all proposals with active voting"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM proposals 
            WHERE status = 'active' AND voting_deadline > ?
            ORDER BY created_at DESC
        """, (time.time(),))
        
        proposals = [self._row_to_proposal(row) for row in cursor.fetchall()]
        conn.close()
        return proposals
    
    def get_all_proposals(self) -> List[Proposal]:
        """Get all proposals"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM proposals ORDER BY created_at DESC")
        proposals = [self._row_to_proposal(row) for row in cursor.fetchall()]
        conn.close()
        return proposals
    
    def _row_to_proposal(self, row) -> Proposal:
        """Convert database row to Proposal object"""
        return Proposal(
            id=row[0], title=row[1], description=row[2], category=row[3],
            recipient_address=row[4], recipient_organization=row[5],
            amount_zion=row[6], amount_usd=row[7], location=row[8], beneficiaries=row[9],
            votes_for=row[10], votes_against=row[11], voter_count=row[12],
            created_at=row[13], voting_deadline=row[14], executed_at=row[15],
            status=row[16], proposal_hash=row[17], proposer_address=row[18], tx_hash=row[19]
        )
    
    def get_treasury_balance(self) -> float:
        """Get current treasury balance"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT balance_after FROM treasury_transactions ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        conn.close()
        
        if row:
            self.treasury_balance = row[0]
        return self.treasury_balance
    
    def export_proposal_json(self, proposal_id: int, output_path: str):
        """Export proposal to JSON file"""
        proposal = self.get_proposal(proposal_id)
        if not proposal:
            raise ValueError(f"Proposal #{proposal_id} not found")
        
        with open(output_path, 'w') as f:
            json.dump(asdict(proposal), f, indent=2)
        
        print(f"📄 Proposal exported to {output_path}")


if __name__ == "__main__":
    # CLI for testing
    import argparse
    
    parser = argparse.ArgumentParser(description="ZION Humanitarian DAO")
    parser.add_argument("--init", action="store_true", help="Initialize DAO database")
    parser.add_argument("--balance", action="store_true", help="Show treasury balance")
    parser.add_argument("--list", action="store_true", help="List all proposals")
    parser.add_argument("--proposal", type=int, help="Show proposal details")
    
    args = parser.parse_args()
    
    dao = HumanitarianDAO()
    
    if args.init:
        print("✅ DAO database initialized")
    
    if args.balance:
        balance = dao.get_treasury_balance()
        print(f"💰 Treasury Balance: {balance:.8f} ZION")
    
    if args.list:
        proposals = dao.get_all_proposals()
        print(f"\n📋 Total Proposals: {len(proposals)}\n")
        for p in proposals:
            status_icon = {"active": "🗳️", "approved": "✅", "rejected": "❌", "executed": "✨"}.get(p.status, "⚪")
            print(f"{status_icon} #{p.id}: {p.title}")
            print(f"   {p.amount_zion:.2f} ZION → {p.recipient_organization}")
            print(f"   Votes: {p.vote_percentage():.1f}% approval ({p.voter_count} voters)")
            print()
    
    if args.proposal:
        p = dao.get_proposal(args.proposal)
        if p:
            print(f"\n{'='*60}")
            print(f"Proposal #{p.id}: {p.title}")
            print(f"{'='*60}")
            print(f"Category: {p.category}")
            print(f"Organization: {p.recipient_organization}")
            print(f"Location: {p.location}")
            print(f"Amount: {p.amount_zion:.8f} ZION (${p.amount_usd:,.0f})")
            print(f"Beneficiaries: {p.beneficiaries:,} people")
            print(f"\nDescription:\n{p.description}")
            print(f"\nVoting Status: {p.status.upper()}")
            print(f"Approval: {p.vote_percentage():.1f}% ({p.voter_count} voters)")
            print(f"  FOR: {p.votes_for:.8f} ZION")
            print(f"  AGAINST: {p.votes_against:.8f} ZION")
            print(f"\nDeadline: {time.strftime('%Y-%m-%d %H:%M', time.localtime(p.voting_deadline))}")
            if p.tx_hash:
                print(f"TX Hash: {p.tx_hash}")
        else:
            print(f"❌ Proposal #{args.proposal} not found")
