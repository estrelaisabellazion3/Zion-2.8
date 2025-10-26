#!/usr/bin/env python3
"""
ZION Automated Payment Processor
Základní implementace automatických plateb pro mining pool
"""
import asyncio
import logging
import time
from typing import Dict, List, Optional
from dataclasses import dataclass
import sqlite3

logger = logging.getLogger(__name__)

@dataclass
class PendingPayment:
    """Čekající platba"""
    address: str
    amount: float
    shares: int
    last_share_time: float

class PaymentProcessor:
    """Automatické zpracování plateb minerům"""
    
    def __init__(self, pool, blockchain_rpc, db_path: str = "zion_pool.db"):
        self.pool = pool
        self.rpc = blockchain_rpc
        self.db_path = db_path
        
        # Konfigurace
        self.payment_threshold = 10.0  # Minimální částka pro výplatu (ZION)
        self.payment_interval = 3600   # Interval kontrol (1 hodina)
        self.min_confirmations = 10    # Minimální potvrzení bloku
        
        self.running = False
        
    async def start(self):
        """Spustit payment processor"""
        self.running = True
        logger.info("💰 Payment Processor started")
        
        while self.running:
            try:
                await self.process_payments()
                await asyncio.sleep(self.payment_interval)
            except Exception as e:
                logger.error(f"Payment processing error: {e}")
                await asyncio.sleep(60)
    
    def stop(self):
        """Zastavit payment processor"""
        self.running = False
        logger.info("💰 Payment Processor stopped")
    
    async def process_payments(self):
        """Zpracovat čekající platby"""
        pending = self.get_pending_balances()
        
        if not pending:
            logger.debug("No pending payments")
            return
        
        logger.info(f"💰 Processing {len(pending)} pending payments")
        
        for payment in pending:
            if payment.amount >= self.payment_threshold:
                await self.send_payment(payment)
            else:
                logger.debug(f"Balance {payment.amount} below threshold for {payment.address}")
    
    def get_pending_balances(self) -> List[PendingPayment]:
        """Získat čekající platby z databáze (Proportional)"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Získat validní share od posledního zaplacení
            cursor.execute("""
                SELECT 
                    wallet_address,
                    SUM(difficulty) as total_difficulty,
                    COUNT(*) as share_count,
                    MAX(timestamp) as last_share
                FROM shares
                WHERE valid = 1 
                  AND paid = 0
                  AND wallet_address IS NOT NULL
                GROUP BY wallet_address
            """)
            
            shares_data = cursor.fetchall()
            
            # Získat nalezené bloky k rozdělení
            cursor.execute("""
                SELECT SUM(reward) as total_reward
                FROM blocks
                WHERE status = 'confirmed'
                  AND paid = 0
            """)
            
            result = cursor.fetchone()
            total_reward = result[0] if result and result[0] else 0
            
            conn.close()
            
            if total_reward == 0:
                return []
            
            # Spočítat proporcionální podíly
            total_difficulty = sum(row[1] for row in shares_data)
            
            if total_difficulty == 0:
                return []
            
            payments = []
            for address, difficulty, count, last_share in shares_data:
                # Proporcionální podíl
                share_ratio = difficulty / total_difficulty
                amount = total_reward * share_ratio
                
                if amount > 0:
                    payments.append(PendingPayment(
                        address=address,
                        amount=amount,
                        shares=count,
                        last_share_time=last_share
                    ))
            
            return payments
            
        except Exception as e:
            logger.error(f"Error getting pending balances: {e}")
            return []
    
    async def send_payment(self, payment: PendingPayment):
        """Odeslat platbu minerovi"""
        try:
            logger.info(f"💸 Sending {payment.amount:.4f} ZION to {payment.address}")
            
            # Odeslat transakci přes RPC
            tx_hash = await self.rpc.send_to_address(
                payment.address, 
                payment.amount
            )
            
            # Zaznamenat platbu do DB
            self.record_payment(payment, tx_hash)
            
            logger.info(f"✅ Payment sent! TX: {tx_hash[:16]}...")
            
        except Exception as e:
            logger.error(f"Failed to send payment to {payment.address}: {e}")
            self.mark_payment_failed(payment, str(e))
    
    def record_payment(self, payment: PendingPayment, tx_hash: str):
        """Zaznamenat úspěšnou platbu"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Zaznamenat platbu
            cursor.execute("""
                INSERT INTO payments (
                    wallet_address, amount, tx_hash, 
                    shares_count, timestamp
                ) VALUES (?, ?, ?, ?, ?)
            """, (
                payment.address,
                payment.amount,
                tx_hash,
                payment.shares,
                time.time()
            ))
            
            # Označit shares jako zaplacené
            cursor.execute("""
                UPDATE shares 
                SET paid = 1
                WHERE wallet_address = ? AND paid = 0
            """, (payment.address,))
            
            # Označit bloky jako zaplacené
            cursor.execute("""
                UPDATE blocks
                SET paid = 1
                WHERE status = 'confirmed' AND paid = 0
            """)
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error recording payment: {e}")
    
    def mark_payment_failed(self, payment: PendingPayment, error: str):
        """Zaznamenat neúspěšnou platbu"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO failed_payments (
                    wallet_address, amount, error, timestamp
                ) VALUES (?, ?, ?, ?)
            """, (
                payment.address,
                payment.amount,
                error,
                time.time()
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error marking failed payment: {e}")
    
    def get_payment_history(self, address: str, limit: int = 10) -> List[Dict]:
        """Získat historii plateb pro adresu"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT amount, tx_hash, shares_count, timestamp
                FROM payments
                WHERE wallet_address = ?
                ORDER BY timestamp DESC
                LIMIT ?
            """, (address, limit))
            
            rows = cursor.fetchall()
            conn.close()
            
            return [
                {
                    'amount': row[0],
                    'tx_hash': row[1],
                    'shares': row[2],
                    'timestamp': row[3]
                }
                for row in rows
            ]
            
        except Exception as e:
            logger.error(f"Error getting payment history: {e}")
            return []

# Přidat do databázového schématu
def create_payment_tables(db_path: str = "zion_pool.db"):
    """Vytvořit tabulky pro platby"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Tabulka plateb
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            wallet_address TEXT NOT NULL,
            amount REAL NOT NULL,
            tx_hash TEXT NOT NULL,
            shares_count INTEGER,
            timestamp REAL NOT NULL,
            UNIQUE(tx_hash)
        )
    """)
    
    # Tabulka neúspěšných plateb
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS failed_payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            wallet_address TEXT NOT NULL,
            amount REAL NOT NULL,
            error TEXT,
            timestamp REAL NOT NULL
        )
    """)
    
    # Přidat 'paid' sloupec do shares pokud neexistuje
    try:
        cursor.execute("ALTER TABLE shares ADD COLUMN paid INTEGER DEFAULT 0")
    except sqlite3.OperationalError:
        pass  # Sloupec už existuje
    
    # Přidat 'paid' sloupec do blocks pokud neexistuje
    try:
        cursor.execute("ALTER TABLE blocks ADD COLUMN paid INTEGER DEFAULT 0")
    except sqlite3.OperationalError:
        pass
    
    # Indexy pro rychlejší dotazy
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_payments_address ON payments(wallet_address)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_shares_paid ON shares(paid, wallet_address)")
    
    conn.commit()
    conn.close()
    
    logger.info("✅ Payment tables created")
