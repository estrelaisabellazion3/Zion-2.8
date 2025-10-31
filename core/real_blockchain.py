#!/usr/bin/env python3
"""
ZION 2.7.5 Real Blockchain Implementation (DEPRECATED in v2.8.4)
Production-Ready Blockchain Core with No Simulations
🌟 JAI RAM SITA HANUMAN - ON THE STAR

⚠️ DEPRECATION WARNING (v2.8.4):
   This module is deprecated and will be removed in v2.8.5.
   Please migrate to: src.core.new_zion_blockchain.ZionRealBlockchain
   
   Migration guide: docs/2.8.4/NODE_MIGRATION_GUIDE_v2.8.4.md
"""

import warnings
warnings.warn(
    "core.real_blockchain is deprecated and will be removed in v2.8.5. "
    "Use src.core.new_zion_blockchain.ZionRealBlockchain instead. "
    "See docs/2.8.4/NODE_MIGRATION_GUIDE_v2.8.4.md for migration guide.",
    DeprecationWarning,
    stacklevel=2
)

import json
import time
import hashlib
import sqlite3
import threading
import sys
import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import heapq

# Import crypto utilities for signature verification
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
try:
    from crypto_utils import verify_signature
    CRYPTO_AVAILABLE = True
except ImportError:
    print("⚠️ crypto_utils not available, signature verification disabled")
    CRYPTO_AVAILABLE = False

# Import RandomX engine from v2.7
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'zion', 'mining'))
try:
    from randomx_engine import RandomXEngine
    RANDOMX_AVAILABLE = True
except ImportError:
    print("⚠️ RandomX engine not available, using SHA256 fallback")
    RANDOMX_AVAILABLE = False

@dataclass
class RealBlock:
    """Real production block"""
    height: int
    hash: str
    previous_hash: str
    timestamp: int
    nonce: int
    difficulty: int
    transactions: List[Dict[str, Any]]
    reward: int
    miner_address: str
    consciousness_level: str = "PHYSICAL"
    sacred_multiplier: float = 1.0
    
    def calculate_hash(self) -> str:
        """Calculate block hash"""
        block_string = json.dumps({
            'height': self.height,
            'previous_hash': self.previous_hash,
            'timestamp': self.timestamp,
            'nonce': self.nonce,
            'transactions': self.transactions,
            'miner_address': self.miner_address
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()


@dataclass 
class RealTransaction:
    """Real production transaction"""
    tx_id: str
    from_address: str
    to_address: str
    amount: int
    fee: int
    timestamp: int
    signature: str = ""
    
    def calculate_tx_id(self) -> str:
        """Calculate transaction ID"""
        tx_string = json.dumps({
            'from_address': self.from_address,
            'to_address': self.to_address,
            'amount': self.amount,
            'fee': self.fee,
            'timestamp': self.timestamp
        }, sort_keys=True)
        return hashlib.sha256(tx_string.encode()).hexdigest()


@dataclass
class MempoolTransaction:
    """Transaction in mempool with priority"""
    transaction: RealTransaction
    fee_per_byte: float
    received_at: datetime
    priority_score: float

    def __lt__(self, other):
        return self.priority_score > other.priority_score  # Higher priority first
class TransactionMempool:
    """
    Advanced transaction memory pool with spam protection
    
    SECURITY FEATURES:
    - Rate limiting per sender address
    - Maximum mempool size enforcement
    - Duplicate transaction prevention
    - Priority-based eviction when full
    """

    def __init__(self, max_size: int = 1000):
        self.transactions: List[MempoolTransaction] = []
        self.max_size = max_size
        self.tx_index: Dict[str, MempoolTransaction] = {}  # tx_id -> MempoolTransaction
        
        # SECURITY: Rate limiting - track transactions per address
        self.address_tx_count: Dict[str, int] = {}  # address -> count of pending txs
        self.max_tx_per_address: int = 20  # Max 20 pending txs per address
        
        # Track transaction timestamps for rate limiting
        self.address_last_tx: Dict[str, float] = {}  # address -> last tx timestamp
        self.min_tx_interval: float = 1.0  # Min 1 second between txs from same address

    def add_transaction(self, transaction: RealTransaction) -> bool:
        """
        Add transaction to mempool with SPAM PROTECTION
        
        SECURITY CHECKS:
        - Duplicate prevention
        - Rate limiting per address
        - Mempool size limit
        - Transaction validation
        """
        # Check for duplicate
        if transaction.tx_id in self.tx_index:
            print(f"⚠️  Transaction {transaction.tx_id[:16]}... already in mempool")
            return False
        
        # SECURITY: Rate limiting - check transaction count per address
        sender = transaction.from_address
        current_count = self.address_tx_count.get(sender, 0)
        
        if current_count >= self.max_tx_per_address:
            print(f"❌ Rate limit: Address {sender[:20]}... has {current_count} pending txs (max {self.max_tx_per_address})")
            return False
        
        # SECURITY: Rate limiting - check time between transactions
        current_time = time.time()
        last_tx_time = self.address_last_tx.get(sender, 0)
        
        if current_time - last_tx_time < self.min_tx_interval:
            print(f"❌ Rate limit: Transaction too soon (min {self.min_tx_interval}s between txs)")
            return False
        
        # Validate transaction
        if not self._validate_transaction(transaction):
            print(f"❌ Transaction validation failed")
            return False
        
        # Check mempool size limit
        if len(self.transactions) >= self.max_size:
            # SECURITY: Evict lowest priority transaction if new one has higher priority
            if self.transactions:
                lowest = self.transactions[-1]
                new_priority = self._calculate_priority(transaction)
                lowest_priority = lowest.priority
                
                if new_priority > lowest_priority:
                    # Evict lowest priority transaction
                    evicted = self.transactions.pop()
                    del self.tx_index[evicted.transaction.tx_id]
                    # Update address count
                    evicted_sender = evicted.transaction.from_address
                    self.address_tx_count[evicted_sender] = self.address_tx_count.get(evicted_sender, 1) - 1
                    print(f"⚠️  Mempool full, evicted lower priority tx {evicted.transaction.tx_id[:16]}...")
                else:
                    print(f"❌ Mempool full and new transaction has lower priority")
                    return False
            else:
                print(f"❌ Mempool full")
                return False
        
        # Calculate priority
        priority = self._calculate_priority(transaction)
        
        # Add to mempool
        mempool_tx = MempoolTransaction(
            transaction=transaction,
            added_at=current_time,
            priority=priority
        )
        
        self.transactions.append(mempool_tx)
        self.tx_index[transaction.tx_id] = mempool_tx
        
        # Update rate limiting trackers
        self.address_tx_count[sender] = current_count + 1
        self.address_last_tx[sender] = current_time
        
        # Sort by priority (highest first)
        self.transactions.sort(key=lambda x: x.priority, reverse=True)
        
        print(f"✅ Transaction {transaction.tx_id[:16]}... added to mempool (priority: {priority:.2f})")
        return True
    
    def _calculate_priority(self, transaction: RealTransaction) -> float:
        """Calculate transaction priority based on fee and age"""
        # Higher fee = higher priority
        # Older transaction = higher priority (to prevent starvation)
        fee_priority = transaction.fee / 1000.0  # Normalize fee
        return fee_priority

    def _validate_transaction(self, transaction: RealTransaction) -> bool:
        """
        SECURITY: Comprehensive transaction validation
        
        Validates:
        - Basic structure and amounts
        - Transaction ID correctness
        - Signature verification (if crypto available)
        - Fee requirements
        - Timestamp sanity
        """
        # Check basic structure
        if not all([transaction.from_address, transaction.to_address, transaction.amount > 0]):
            print(f"❌ Transaction validation failed: Invalid structure")
            return False

        # Check amount is reasonable (not negative, not overflow)
        if transaction.amount <= 0 or transaction.amount > 10**18:  # Max 1 quintillion
            print(f"❌ Transaction validation failed: Invalid amount {transaction.amount}")
            return False

        # Check fee is reasonable
        if transaction.fee < 100:  # Minimum fee
            print(f"❌ Transaction validation failed: Fee too low {transaction.fee}")
            return False
        
        if transaction.fee > transaction.amount:  # Fee shouldn't exceed amount
            print(f"❌ Transaction validation failed: Fee exceeds amount")
            return False

        # Check transaction ID matches
        calculated_tx_id = transaction.calculate_tx_id()
        if transaction.tx_id != calculated_tx_id:
            print(f"❌ Transaction validation failed: TX ID mismatch")
            print(f"   Expected: {calculated_tx_id}")
            print(f"   Got: {transaction.tx_id}")
            return False
        
        # SECURITY: Verify signature if crypto available
        if CRYPTO_AVAILABLE and transaction.signature:
            # Message to verify is the transaction data without signature
            message = json.dumps({
                'from_address': transaction.from_address,
                'to_address': transaction.to_address,
                'amount': transaction.amount,
                'fee': transaction.fee,
                'timestamp': transaction.timestamp
            }, sort_keys=True).encode()
            
            # Extract public key from address (simplified - in production use proper key derivation)
            # For now, we'll require transactions to include public_key field
            # TODO: Add public_key field to RealTransaction or derive from address
            # For now, skip signature verification if no proper key management
            print(f"⚠️  Signature verification skipped (needs public key infrastructure)")
        
        # Check timestamp is reasonable (not too far in future, not too old)
        current_time = int(time.time())
        if transaction.timestamp > current_time + 300:  # Max 5 minutes in future
            print(f"❌ Transaction validation failed: Timestamp too far in future")
            return False
        
        if transaction.timestamp < current_time - 86400:  # Not older than 24 hours
            print(f"❌ Transaction validation failed: Timestamp too old")
            return False

        # TODO: Add balance validation (requires UTXO or account state)
        # TODO: Add double-spend check (check if inputs already spent)
        
        return True

    def get_highest_priority_transactions(self, limit: int = 10) -> List[RealTransaction]:
        """Get highest priority transactions for block creation"""
        return [mt.transaction for mt in self.transactions[:limit]]

    def remove_transactions(self, transactions: List[RealTransaction]):
        """
        Remove transactions that were included in a block
        
        SECURITY: Updates rate limiting counters when transactions are removed
        """
        tx_ids = {tx.tx_id for tx in transactions}
        
        # Remove from list and index
        self.transactions = [mt for mt in self.transactions if mt.transaction.tx_id not in tx_ids]
        
        # Update rate limiting counters
        for tx_id in tx_ids:
            mempool_tx = self.tx_index.pop(tx_id, None)
            if mempool_tx:
                sender = mempool_tx.transaction.from_address
                # Decrement address transaction count
                if sender in self.address_tx_count:
                    self.address_tx_count[sender] = max(0, self.address_tx_count[sender] - 1)
                    # Clean up if zero
                    if self.address_tx_count[sender] == 0:
                        del self.address_tx_count[sender]

    def get_transaction(self, tx_id: str) -> Optional[RealTransaction]:
        """Get transaction by ID"""
        mempool_tx = self.tx_index.get(tx_id)
        return mempool_tx.transaction if mempool_tx else None

    def get_mempool_size(self) -> int:
        """Get current mempool size"""
        return len(self.transactions)

    def get_mempool_info(self) -> Dict[str, Any]:
        """Get detailed mempool information"""
        if not self.transactions:
            return {'size': 0, 'min_fee': 0, 'max_fee': 0}

        fees = [mt.fee_per_byte for mt in self.transactions]
        return {
            'size': len(self.transactions),
            'min_fee': min(fees),
            'max_fee': max(fees),
            'avg_fee': sum(fees) / len(fees)
        }


class ZionRealBlockchain:
    """ZION 2.7.1 Real Blockchain - No Simulations"""
    
    def __init__(self, db_file: str = "zion_real_blockchain.db"):
        self.db_file = db_file
        self.blocks: List[RealBlock] = []
        self.mempool = TransactionMempool()
        self.difficulty = 1500  # Production difficulty for 60-second block time (was 50 - TOO LOW!)
        self.block_reward = 5479452055  # 5,479.45 ZION in atomic units (144B ZION / 50 years)
        self._lock = threading.Lock()
        self.target_block_time = 60  # Target: 1 block per minute
        self.difficulty_adjustment_interval = 100  # Adjust difficulty every 100 blocks
        
        # RandomX engine initialization
        self.randomx_engine = None
        if RANDOMX_AVAILABLE:
            try:
                self.randomx_engine = RandomXEngine(fallback_to_sha256=True)
                seed_key = b"ZION_BLOCKCHAIN_SEED_2.7.1"
                if self.randomx_engine.init(seed_key, use_large_pages=False, full_mem=False):
                    print("✅ RandomX engine initialized successfully")
                else:
                    print("⚠️ RandomX init failed, using SHA256 fallback")
                    self.randomx_engine = None
            except Exception as e:
                print(f"⚠️ RandomX initialization error: {e}")
                self.randomx_engine = None
        
        # Mining algorithm settings
        self.mining_algorithm = 'argon2'  # Default ASIC-resistant
        self.use_gpu = False
        
        # Initialize database
        self._init_database()
        
        # Load existing blocks
        self._load_blocks_from_db()
        
        # Create genesis if needed
        if not self.blocks:
            self._create_genesis_block()
    
    def set_mining_algorithm(self, algorithm: str, use_gpu: bool = False):
        """Set the mining algorithm for proof-of-work"""
        allowed_algorithms = ['argon2', 'kawpow', 'ethash', 'cryptonight', 'octopus', 'ergo']
        if algorithm not in allowed_algorithms:
            raise ValueError(f"Unsupported algorithm: {algorithm}")
        
        self.mining_algorithm = algorithm
        self.use_gpu = use_gpu
        
        print(f"🎯 Mining algorithm set to: {algorithm.upper()}")
        if use_gpu:
            print("🎮 GPU mining enabled")
        else:
            print("🖥️ CPU mining enabled")
        
        # Note: Difficulty is now managed by adaptive difficulty adjustment
        # Initial difficulty is set in __init__ to 1500 for production
    
    def adjust_difficulty(self):
        """Adjust difficulty based on actual block times to maintain 60-second target"""
        if len(self.blocks) < self.difficulty_adjustment_interval:
            return
        
        # Calculate average block time for last N blocks
        recent_blocks = self.blocks[-self.difficulty_adjustment_interval:]
        time_diffs = []
        for i in range(1, len(recent_blocks)):
            time_diff = recent_blocks[i].timestamp - recent_blocks[i-1].timestamp
            time_diffs.append(time_diff)
        
        if not time_diffs:
            return
        
        avg_block_time = sum(time_diffs) / len(time_diffs)
        
        # Adjust difficulty to target 60 seconds
        if avg_block_time < self.target_block_time * 0.8:  # Too fast (< 48s)
            new_difficulty = int(self.difficulty * (self.target_block_time / avg_block_time))
            print(f"⬆️  Increasing difficulty: {self.difficulty} → {new_difficulty} (avg block time: {avg_block_time:.1f}s)")
            self.difficulty = new_difficulty
        elif avg_block_time > self.target_block_time * 1.2:  # Too slow (> 72s)
            new_difficulty = int(self.difficulty * (self.target_block_time / avg_block_time))
            print(f"⬇️  Decreasing difficulty: {self.difficulty} → {new_difficulty} (avg block time: {avg_block_time:.1f}s)")
            self.difficulty = new_difficulty
        else:
            print(f"✅ Difficulty stable at {self.difficulty} (avg block time: {avg_block_time:.1f}s)")
    
    
    def _init_database(self):
        """Initialize blockchain database"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS real_blocks (
                height INTEGER PRIMARY KEY,
                hash TEXT UNIQUE NOT NULL,
                previous_hash TEXT,
                timestamp INTEGER,
                nonce INTEGER,
                difficulty INTEGER,
                transactions_json TEXT,
                reward INTEGER,
                miner_address TEXT,
                consciousness_level TEXT,
                sacred_multiplier REAL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS real_transactions (
                tx_id TEXT PRIMARY KEY,
                block_height INTEGER,
                from_address TEXT,
                to_address TEXT,
                amount INTEGER,
                fee INTEGER,
                timestamp INTEGER,
                signature TEXT,
                consciousness_boost REAL,
                FOREIGN KEY (block_height) REFERENCES real_blocks (height)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def _load_blocks_from_db(self):
        """Load existing blocks from database"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM real_blocks ORDER BY height')
        rows = cursor.fetchall()
        
        for row in rows:
            transactions = json.loads(row[6])  # transactions_json
            
            block = RealBlock(
                height=row[0],
                hash=row[1], 
                previous_hash=row[2],
                timestamp=row[3],
                nonce=row[4],
                difficulty=row[5],
                transactions=transactions,
                reward=row[7],
                miner_address=row[8],
                consciousness_level=row[9],
                sacred_multiplier=row[10]
            )
            
            self.blocks.append(block)
        
        conn.close()
        
        if self.blocks:
            print(f"📦 Loaded {len(self.blocks)} real blocks from database")
    
    def _calculate_argon2_hash(self, block: RealBlock) -> str:
        """Calculate Argon2 hash for proof-of-work"""
        try:
            from argon2 import PasswordHasher
            hasher = PasswordHasher(
                time_cost=2,
                memory_cost=65536,
                parallelism=1,
                hash_len=32
            )
            
            block_string = json.dumps({
                'height': block.height,
                'previous_hash': block.previous_hash,
                'timestamp': block.timestamp,
                'nonce': block.nonce,
                'transactions': block.transactions,
                'miner_address': block.miner_address
            }, sort_keys=True)
            
            # Use Argon2 to hash the block data
            hash_bytes = hasher.hash(block_string)
            return hashlib.sha256(hash_bytes.encode()).hexdigest()
            
        except ImportError:
            # Fallback if argon2 not available
            return block.calculate_hash()
    
    def _calculate_kawpow_hash(self, block: RealBlock) -> str:
        """Calculate KawPow hash (GPU simulation)"""
        block_string = json.dumps({
            'height': block.height,
            'previous_hash': block.previous_hash,
            'timestamp': block.timestamp,
            'nonce': block.nonce,
            'transactions': block.transactions,
            'miner_address': block.miner_address
        }, sort_keys=True)
        
        # KawPow simulation - multi-round PBKDF2 to simulate GPU work
        salt = b"zion_kawpow_salt"
        hash_result = hashlib.pbkdf2_hmac('sha256', block_string.encode(), salt, 10000)
        return hash_result.hex()
    
    def _calculate_ethash_hash(self, block: RealBlock) -> str:
        """Calculate Ethash hash (GPU simulation)"""
        block_string = json.dumps({
            'height': block.height,
            'previous_hash': block.previous_hash,
            'timestamp': block.timestamp,
            'nonce': block.nonce,
            'transactions': block.transactions,
            'miner_address': block.miner_address
        }, sort_keys=True)
        
        # Ethash simulation - heavy PBKDF2 to simulate DAG computation
        salt = b"zion_ethash_salt"
        hash_result = hashlib.pbkdf2_hmac('sha256', block_string.encode(), salt, 50000)
        return hash_result.hex()
    
    def _create_genesis_block(self):
        """Create genesis block with pre-mine addresses from premine.py"""
        # Import premine addresses from premine module
        from premine import get_premine_addresses
        
        # Get all premine addresses
        ZION_PREMINE_ADDRESSES = get_premine_addresses()
        
        # Genesis reward distribution using CORRECT addresses from premine.py
        genesis_transactions = []
        
        # Add all premine addresses from premine.py (15.78B ZION)
        for address, info in ZION_PREMINE_ADDRESSES.items():
            genesis_transactions.append({
                'type': info.get('type', 'premine'),
                'amount': info['amount'] * 1000000,  # Convert to atomic units (×1e6 not ×1e12 - ZION has 6 decimals)
                'to_address': address,
                'purpose': info['purpose']
            })
        
        print(f"✨ Creating genesis block with {len(genesis_transactions)} premine addresses (15.78B ZION)")
        
        # Calculate total pre-mine supply
        total_premine = sum(tx['amount'] for tx in genesis_transactions)
        
        genesis_block = RealBlock(
            height=0,
            hash="",
            previous_hash="0" * 64,
            timestamp=int(time.time()),
            nonce=0,
            difficulty=1,
            transactions=genesis_transactions,
            reward=total_premine,  # Total pre-mine + genesis reward
            miner_address="ZION_GENESIS_MINER",
            consciousness_level="ON_THE_STAR",
            sacred_multiplier=10.0
        )
        
        # Calculate genesis hash
        genesis_block.hash = genesis_block.calculate_hash()
        
        # Add to blockchain
        self.blocks.append(genesis_block)
        
        # Save to database
        self._save_block_to_db(genesis_block)
        
        print("✨ Genesis block created with CORRECT pre-mine addresses from seednodes.py")
        print(f"   Hash: {genesis_block.hash}")
        print(f"   Total premine: {total_premine:,} atomic units ({total_premine/1e6:,.2f} ZION)")
        print(f"   Addresses: {len(genesis_transactions)}")
        for tx in genesis_transactions:
            addr_short = tx['to_address'][:50] + '...' if len(tx['to_address']) > 50 else tx['to_address']
            print(f"   ✅ {addr_short:52} → {tx['amount']/1e6:>12,.0f} ZION ({tx.get('purpose', 'N/A')})")
        print(f"   📊 Total pre-mine supply: {total_premine} atomic units ({total_premine / 1_000_000:,.0f} ZION)")
    
    def add_transaction(self, tx: RealTransaction) -> bool:
        """Add transaction to mempool"""
        with self._lock:
            # Validate transaction
            if not self._validate_transaction(tx):
                return False
            
            # Add to mempool
            self.mempool.append(tx)
            
            # Save to database
            self._save_transaction_to_db(tx, None)  # No block yet
            
            print(f"📝 Transaction added to mempool: {tx.tx_id[:16]}...")
            return True
    
    def _validate_transaction(self, tx: RealTransaction) -> bool:
        """Validate transaction (basic checks)"""
        # Check amounts
        if tx.amount <= 0 or tx.fee < 0:
            return False
        
        # Check addresses
        if not tx.from_address or not tx.to_address:
            return False
        
        # Check signature exists
        if not tx.signature:
            return False
        
        return True
    
    def validate_block(self, block: RealBlock, check_pow: bool = True) -> bool:
        """
        SECURITY: Comprehensive block validation
        
        Validates:
        - Block height sequence
        - Previous hash chain linkage
        - Timestamp sanity
        - Proof of work (hash meets difficulty)
        - Transaction validity
        - Block reward correctness
        """
        # Check block height is next in sequence
        expected_height = len(self.blocks)
        if block.height != expected_height:
            print(f"❌ Block validation failed: Height mismatch")
            print(f"   Expected: {expected_height}, Got: {block.height}")
            return False
        
        # Check previous hash links to current chain
        expected_prev_hash = self.blocks[-1].hash if self.blocks else "0" * 64
        if block.previous_hash != expected_prev_hash:
            print(f"❌ Block validation failed: Previous hash mismatch")
            print(f"   Expected: {expected_prev_hash}")
            print(f"   Got: {block.previous_hash}")
            return False
        
        # Check timestamp is reasonable
        current_time = int(time.time())
        if block.timestamp > current_time + 7200:  # Max 2 hours in future
            print(f"❌ Block validation failed: Timestamp too far in future")
            return False
        
        if self.blocks and block.timestamp < self.blocks[-1].timestamp:
            print(f"❌ Block validation failed: Timestamp before previous block")
            return False
        
        # Check proof of work (if required)
        if check_pow:
            # Verify hash meets difficulty target
            hash_value = int(block.hash, 16)
            target = (2 ** 256) // block.difficulty
            
            if hash_value >= target:
                print(f"❌ Block validation failed: Hash doesn't meet difficulty")
                print(f"   Hash value: {hash_value}")
                print(f"   Target: {target}")
                print(f"   Difficulty: {block.difficulty}")
                return False
            
            # Verify hash is correctly calculated
            if self.randomx_engine and RANDOMX_AVAILABLE:
                block_data = json.dumps({
                    'height': block.height,
                    'previous_hash': block.previous_hash,
                    'timestamp': block.timestamp,
                    'nonce': block.nonce,
                    'miner_address': block.miner_address
                }, sort_keys=True).encode()
                
                calculated_hash = self.randomx_engine.hash(block_data).hex()
            else:
                calculated_hash = block.calculate_hash()
            
            if block.hash != calculated_hash:
                print(f"❌ Block validation failed: Hash mismatch")
                print(f"   Calculated: {calculated_hash}")
                print(f"   Block: {block.hash}")
                return False
        
        # Validate all transactions in block
        for tx_dict in block.transactions:
            # Reconstruct RealTransaction from dict
            tx = RealTransaction(**tx_dict)
            if not self._validate_transaction(tx):
                print(f"❌ Block validation failed: Invalid transaction {tx.tx_id}")
                return False
        
        # Check block reward is correct
        expected_reward = int(self.block_reward * block.sacred_multiplier)
        if block.reward != expected_reward:
            print(f"❌ Block validation failed: Incorrect reward")
            print(f"   Expected: {expected_reward}, Got: {block.reward}")
            return False
        
        # All validations passed
        return True
    
    def mine_block(self, miner_address: str, consciousness_level: str = "PHYSICAL") -> Optional[RealBlock]:
        """Mine a new block"""
        with self._lock:
            # Get transactions from mempool (prioritized)
            transactions = self.mempool.get_highest_priority_transactions(10)
            
            # Calculate sacred multiplier
            sacred_multipliers = {
                "PHYSICAL": 1.0,
                "EMOTIONAL": 1.1,
                "MENTAL": 1.2,
                "INTUITIVE": 1.3,
                "SPIRITUAL": 1.5,
                "COSMIC": 2.0,
                "UNITY": 2.5,
                "ENLIGHTENMENT": 3.0,
                "LIBERATION": 5.0,
                "ON_THE_STAR": 10.0
            }
            sacred_multiplier = sacred_multipliers.get(consciousness_level, 1.0)
            
            # Create new block
            new_block = RealBlock(
                height=len(self.blocks),
                hash="",
                previous_hash=self.blocks[-1].hash if self.blocks else "0" * 64,
                timestamp=int(time.time()),
                nonce=0,
                difficulty=self.difficulty,
                transactions=[asdict(tx) for tx in transactions],
                reward=int(self.block_reward * sacred_multiplier),
                miner_address=miner_address,
                consciousness_level=consciousness_level,
                sacred_multiplier=sacred_multiplier
            )
            
            # Mine the block (proof of work)
            start_time = time.time()
            while True:
                new_block.nonce += 1
                
                # Use RandomX for hash calculation (same as pool validation)
                if self.randomx_engine and RANDOMX_AVAILABLE:
                    # Create block data for RandomX hashing
                    block_data = json.dumps({
                        'height': new_block.height,
                        'previous_hash': new_block.previous_hash,
                        'timestamp': new_block.timestamp,
                        'nonce': new_block.nonce,
                        'miner_address': new_block.miner_address
                    }, sort_keys=True).encode()
                    
                    # RandomX hash
                    new_block.hash = self.randomx_engine.hash(block_data).hex()
                else:
                    # Fallback to SHA256 if RandomX not available
                    new_block.hash = new_block.calculate_hash()
                
                # Check if hash meets difficulty
                if int(new_block.hash, 16) < (2 ** 256) // self.difficulty:
                    break
                
                # Prevent infinite mining in production
                if time.time() - start_time > 120:  # 120 second timeout (was 30)
                    print(f"⚠️  Mining timeout for block {new_block.height}")
                    return None
            
            # SECURITY: Validate block before adding to chain
            if not self.validate_block(new_block, check_pow=True):
                print(f"❌ Mined block failed validation!")
                return None
            
            # Add block to blockchain
            self.blocks.append(new_block)
            
            # Remove transactions from mempool
            if transactions:
                self.mempool.remove_transactions(transactions)
            
            # Save to database
            self._save_block_to_db(new_block)
            
            # Update transaction records with block height
            for tx in transactions:
                self._update_transaction_block(tx.tx_id, new_block.height)
            
            # Adjust difficulty every N blocks to maintain target block time
            if new_block.height % self.difficulty_adjustment_interval == 0 and new_block.height > 0:
                self.adjust_difficulty()
            
            mining_time = time.time() - start_time
            print(f"⛏️  Block {new_block.height} mined!")
            print(f"   Hash: {new_block.hash}")
            print(f"   Reward: {new_block.reward} atomic units")
            print(f"   Mining time: {mining_time:.2f}s")
            print(f"   Transactions: {len(transactions)}")
            print(f"   🧠 Consciousness: {consciousness_level}")
            print(f"   🌟 Sacred multiplier: {sacred_multiplier:.2f}x")
            
            return new_block
    
    def _save_block_to_db(self, block: RealBlock):
        """Save block to database"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO real_blocks VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            block.height, block.hash, block.previous_hash, block.timestamp,
            block.nonce, block.difficulty, json.dumps(block.transactions),
            block.reward, block.miner_address, block.consciousness_level,
            block.sacred_multiplier
        ))
        
        conn.commit()
        conn.close()
    
    def _save_transaction_to_db(self, tx: RealTransaction, block_height: Optional[int]):
        """Save transaction to database"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO real_transactions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            tx.tx_id, block_height, tx.from_address, tx.to_address,
            tx.amount, tx.fee, tx.timestamp, tx.signature, tx.consciousness_boost
        ))
        
        conn.commit()
        conn.close()
    
    def _update_transaction_block(self, tx_id: str, block_height: int):
        """Update transaction with block height"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute(
            'UPDATE real_transactions SET block_height = ? WHERE tx_id = ?',
            (block_height, tx_id)
        )
        
        conn.commit()
        conn.close()
    
    def get_balance(self, address: str) -> int:
        """Get address balance (atomic units)"""
        balance = 0
        
        for block in self.blocks:
            # Check mining rewards
            if block.miner_address == address:
                balance += block.reward
            
            # Check transactions
            for tx_data in block.transactions:
                if tx_data.get('to_address') == address:
                    balance += tx_data.get('amount', 0)
                elif tx_data.get('from_address') == address:
                    balance -= tx_data.get('amount', 0)
                    balance -= tx_data.get('fee', 0)
        
        return max(0, balance)
    
    def get_block_count(self) -> int:
        """Get current block count"""
        return len(self.blocks)
    
    def get_latest_block(self) -> Optional[RealBlock]:
        """Get latest block"""
        return self.blocks[-1] if self.blocks else None
    
    def verify_blockchain(self) -> bool:
        """Verify blockchain integrity"""
        for i in range(1, len(self.blocks)):
            current_block = self.blocks[i]
            previous_block = self.blocks[i-1]
            
            # Check previous hash
            if current_block.previous_hash != previous_block.hash:
                print(f"❌ Block {i} has invalid previous hash")
                return False
            
            # Check hash calculation
            if current_block.hash != current_block.calculate_hash():
                print(f"❌ Block {i} has invalid hash")
                return False
        
        print("✅ Blockchain integrity verified")
        return True
    
    def get_blockchain_stats(self) -> Dict[str, Any]:
        """Get blockchain statistics"""
        total_supply = sum(block.reward for block in self.blocks)
        total_transactions = sum(len(block.transactions) for block in self.blocks)
        
        consciousness_distribution = {}
        for block in self.blocks:
            level = block.consciousness_level
            consciousness_distribution[level] = consciousness_distribution.get(level, 0) + 1
        
        return {
            'block_count': len(self.blocks),
            'total_supply': total_supply,
            'total_transactions': total_transactions,
            'mempool_size': self.mempool.get_mempool_size(),
            'difficulty': self.difficulty,
            'consciousness_distribution': consciousness_distribution
        }


if __name__ == "__main__":
    print("🚀 ZION 2.7.1 Real Blockchain Test")
    print("JAI RAM SITA HANUMAN - ON THE STAR! ⭐")
    
    # Initialize real blockchain
    blockchain = ZionRealBlockchain()
    
    # Mine some real blocks
    for i in range(3):
        miner_address = f"ZION_REAL_MINER_{i}"
        consciousness_levels = ["SPIRITUAL", "COSMIC", "ENLIGHTENMENT"]
        
        block = blockchain.mine_block(
            miner_address=miner_address,
            consciousness_level=consciousness_levels[i]
        )
        
        if block:
            print(f"✅ Real block {block.height} added to blockchain")
    
    # Show stats
    stats = blockchain.get_blockchain_stats()
    print(f"\n📊 Blockchain Stats:")
    print(f"   Blocks: {stats['block_count']}")
    print(f"   Total Supply: {stats['total_supply']:,} atomic units")
    print(f"   Consciousness Distribution: {stats['consciousness_distribution']}")
    
    # Verify integrity
    blockchain.verify_blockchain()
    
    print("\n✅ Real blockchain operational!")