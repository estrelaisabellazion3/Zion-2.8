#!/usr/bin/env python3
"""
ZION 2.8.3 - Blockchain Wrapper (bez P2P/RPC závislostí)
Verze pro standalone RPC server
"""

import hashlib
import json
import time
import sqlite3
import threading
from typing import Dict, List

class SimpleBlockchain:
    """Zjednodušený blockchain bez P2P a starého RPC"""
    
    def __init__(self, db_file='zion_blockchain.db', network='mainnet'):
        self.db_file = db_file
        self.network = network
        self.lock = threading.Lock()
        
        # Blockchain parametry
        self.mining_difficulty = 4
        self.block_reward = 50.0
        self.blocks = []
        self.pending_transactions = []
        self.balances = {}
        self.nonces = {}
        
        # Inicializace databáze
        self._init_database()
        self._load_from_database()
        
        if not self.blocks:
            self._create_genesis_block()
    
    def _init_database(self):
        """Vytvoření databázové struktury"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS blocks (
                height INTEGER PRIMARY KEY,
                hash TEXT UNIQUE,
                previous_hash TEXT,
                timestamp REAL,
                nonce INTEGER,
                difficulty INTEGER,
                transactions TEXT,
                miner TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS balances (
                address TEXT PRIMARY KEY,
                balance REAL
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def _load_from_database(self):
        """Načtení dat z databáze"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Načtení bloků
        cursor.execute('SELECT * FROM blocks ORDER BY height')
        for row in cursor.fetchall():
            block = {
                'height': row[0],
                'hash': row[1],
                'previous_hash': row[2],
                'timestamp': row[3],
                'nonce': row[4],
                'difficulty': row[5],
                'transactions': json.loads(row[6]),
                'miner': row[7]
            }
            self.blocks.append(block)
        
        # Načtení balancí
        cursor.execute('SELECT * FROM balances')
        for row in cursor.fetchall():
            self.balances[row[0]] = row[1]
        
        conn.close()
    
    def _create_genesis_block(self):
        """Vytvoření genesis bloku"""
        genesis_block = {
            'height': 0,
            'hash': '0' * 64,
            'previous_hash': '0' * 64,
            'timestamp': time.time(),
            'nonce': 0,
            'difficulty': self.mining_difficulty,
            'transactions': [],
            'miner': 'genesis'
        }
        
        self.blocks.append(genesis_block)
        self._save_block_to_db(genesis_block)
        
        print(f"✨ Genesis block created")
    
    def _save_block_to_db(self, block):
        """Uložení bloku do databáze"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO blocks 
            (height, hash, previous_hash, timestamp, nonce, difficulty, transactions, miner)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            block['height'],
            block['hash'],
            block['previous_hash'],
            block['timestamp'],
            block['nonce'],
            block['difficulty'],
            json.dumps(block['transactions']),
            block['miner']
        ))
        
        conn.commit()
        conn.close()
    
    def get_total_supply(self):
        """Celková nabídka ZION"""
        return sum(self.balances.values())
    
    def add_transaction(self, from_addr, to_addr, amount):
        """Přidání transakce do mempoolu"""
        tx = {
            'from': from_addr,
            'to': to_addr,
            'amount': amount,
            'timestamp': time.time(),
            'nonce': self.nonces.get(from_addr, 0) + 1
        }
        
        self.pending_transactions.append(tx)
        return hashlib.sha256(json.dumps(tx).encode()).hexdigest()
    
    def mine_block(self, miner_address):
        """Vytěžení nového bloku"""
        with self.lock:
            if len(self.blocks) == 0:
                return None
            
            previous_block = self.blocks[-1]
            
            # Reward transakce
            reward_tx = {
                'from': 'coinbase',
                'to': miner_address,
                'amount': self.block_reward,
                'timestamp': time.time()
            }
            
            transactions = [reward_tx] + self.pending_transactions[:100]
            
            new_block = {
                'height': len(self.blocks),
                'previous_hash': previous_block['hash'],
                'timestamp': time.time(),
                'nonce': 0,
                'difficulty': self.mining_difficulty,
                'transactions': transactions,
                'miner': miner_address
            }
            
            # Proof of Work
            while True:
                block_string = json.dumps(new_block, sort_keys=True)
                block_hash = hashlib.sha256(block_string.encode()).hexdigest()
                
                if block_hash.startswith('0' * self.mining_difficulty):
                    new_block['hash'] = block_hash
                    break
                
                new_block['nonce'] += 1
            
            # Přidání bloku
            self.blocks.append(new_block)
            self._save_block_to_db(new_block)
            
            # Update balancí
            for tx in transactions:
                if tx['to'] not in self.balances:
                    self.balances[tx['to']] = 0
                self.balances[tx['to']] += tx['amount']
                
                if tx['from'] != 'coinbase':
                    self.balances[tx['from']] = self.balances.get(tx['from'], 0) - tx['amount']
            
            # Uložení balancí do databáze
            self._save_balances_to_db()
            
            # Vymazání použitých transakcí
            self.pending_transactions = self.pending_transactions[100:]
            
            return new_block
    
    def _save_balances_to_db(self):
        """Uložení balancí do databáze"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        for address, balance in self.balances.items():
            cursor.execute('''
                INSERT OR REPLACE INTO balances (address, balance)
                VALUES (?, ?)
            ''', (address, balance))
        
        conn.commit()
        conn.close()
