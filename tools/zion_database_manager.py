#!/usr/bin/env python3
"""
ZION Database Manager - Compression & Archive Tool
Manages blockchain and pool databases with multi-tier storage
"""
import sqlite3
import os
import gzip
import shutil
import json
from datetime import datetime, timedelta
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ZionDatabaseManager:
    """
    Multi-tier database management for ZION blockchain
    
    Architecture:
    - HOT: Last 30 days (SQLite) - Fast access for explorer
    - WARM: 31-365 days (Compressed SQLite) - Medium access
    - COLD: 365+ days (Parquet/JSON.gz) - Archive access
    """
    
    def __init__(self, db_path: str = "zion_unified_blockchain.db"):
        self.db_path = db_path
        self.archive_dir = Path("archive")
        self.archive_dir.mkdir(exist_ok=True)
        
        # Thresholds (in days)
        self.hot_threshold = 30
        self.warm_threshold = 365
        
    def analyze_database(self):
        """Analyze current database size and fragmentation"""
        if not os.path.exists(self.db_path):
            logger.error(f"Database not found: {self.db_path}")
            return
        
        size_mb = os.path.getsize(self.db_path) / 1024 / 1024
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get block count
        cursor.execute("SELECT COUNT(*) FROM real_blocks")
        block_count = cursor.fetchone()[0]
        
        # Get date range
        cursor.execute("SELECT MIN(timestamp), MAX(timestamp) FROM real_blocks")
        min_ts, max_ts = cursor.fetchone()
        
        # Get page info
        cursor.execute("PRAGMA page_count")
        page_count = cursor.fetchone()[0]
        cursor.execute("PRAGMA page_size")
        page_size = cursor.fetchone()[0]
        
        # Calculate fragmentation
        actual_size = os.path.getsize(self.db_path)
        allocated_size = page_count * page_size
        fragmentation_kb = (allocated_size - actual_size) / 1024
        
        conn.close()
        
        logger.info(f"📊 Database Analysis:")
        logger.info(f"   Size: {size_mb:.2f} MB")
        logger.info(f"   Blocks: {block_count:,}")
        logger.info(f"   Date range: {datetime.fromtimestamp(min_ts)} → {datetime.fromtimestamp(max_ts)}")
        logger.info(f"   Fragmentation: {fragmentation_kb:.1f} KB wasted")
        logger.info(f"   Pages: {page_count:,} × {page_size} bytes")
        
        return {
            'size_mb': size_mb,
            'block_count': block_count,
            'fragmentation_kb': fragmentation_kb,
            'oldest_block': min_ts,
            'newest_block': max_ts
        }
    
    def vacuum_database(self):
        """
        VACUUM database to reclaim space and reduce fragmentation
        
        Benefits:
        - Removes deleted records
        - Defragments pages
        - Typically saves 20-40% space
        """
        logger.info("🔧 Running VACUUM on database...")
        
        before_size = os.path.getsize(self.db_path) / 1024 / 1024
        
        conn = sqlite3.connect(self.db_path)
        conn.execute("VACUUM")
        conn.close()
        
        after_size = os.path.getsize(self.db_path) / 1024 / 1024
        saved_mb = before_size - after_size
        percent_saved = (saved_mb / before_size) * 100
        
        logger.info(f"✅ VACUUM complete:")
        logger.info(f"   Before: {before_size:.2f} MB")
        logger.info(f"   After: {after_size:.2f} MB")
        logger.info(f"   Saved: {saved_mb:.2f} MB ({percent_saved:.1f}%)")
        
        return saved_mb
    
    def archive_old_blocks(self, age_days: int = 30):
        """
        Archive blocks older than age_days to compressed storage
        
        Process:
        1. Export blocks to JSON
        2. Compress with GZIP
        3. Delete from main DB
        4. VACUUM to reclaim space
        """
        logger.info(f"📦 Archiving blocks older than {age_days} days...")
        
        cutoff_timestamp = (datetime.now() - timedelta(days=age_days)).timestamp()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get blocks to archive
        cursor.execute("""
            SELECT height, hash, previous_hash, timestamp, nonce, difficulty, 
                   transactions_json, reward, miner_address
            FROM real_blocks
            WHERE timestamp < ?
            ORDER BY height
        """, (cutoff_timestamp,))
        
        blocks_to_archive = cursor.fetchall()
        
        if not blocks_to_archive:
            logger.info("   No blocks to archive")
            conn.close()
            return
        
        # Create archive file
        archive_date = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_filename = f"blocks_archive_{archive_date}.json.gz"
        archive_path = self.archive_dir / archive_filename
        
        # Prepare archive data
        archive_data = []
        for block in blocks_to_archive:
            archive_data.append({
                'height': block[0],
                'hash': block[1],
                'previous_hash': block[2],
                'timestamp': block[3],
                'nonce': block[4],
                'difficulty': block[5],
                'transactions': json.loads(block[6]) if block[6] else [],
                'reward': block[7],
                'miner_address': block[8]
            })
        
        # Write compressed archive
        with gzip.open(archive_path, 'wt', encoding='utf-8') as f:
            json.dump({
                'archive_date': archive_date,
                'block_count': len(archive_data),
                'height_range': [archive_data[0]['height'], archive_data[-1]['height']],
                'blocks': archive_data
            }, f, indent=2)
        
        # Delete archived blocks from main DB
        # SECURITY FIX: Use proper parameterized query to prevent SQL injection
        heights_to_delete = [b[0] for b in blocks_to_archive]
        
        # Build parameterized query safely
        placeholders = ','.join(['?'] * len(heights_to_delete))
        query = f"DELETE FROM real_blocks WHERE height IN ({placeholders})"
        
        # Execute with parameters (NOT string interpolation)
        cursor.execute(query, heights_to_delete)
        
        conn.commit()
        conn.close()
        
        # VACUUM to reclaim space
        saved_mb = self.vacuum_database()
        
        archive_size = os.path.getsize(archive_path) / 1024 / 1024
        
        logger.info(f"✅ Archive complete:")
        logger.info(f"   Archived: {len(blocks_to_archive):,} blocks")
        logger.info(f"   Height range: {heights_to_delete[0]} → {heights_to_delete[-1]}")
        logger.info(f"   Archive file: {archive_filename} ({archive_size:.2f} MB)")
        logger.info(f"   Space saved: {saved_mb:.2f} MB")
        
        return archive_path
    
    def restore_from_archive(self, archive_path: Path, height_range: tuple = None):
        """
        Restore blocks from archive (for explorer queries or audit)
        
        Args:
            archive_path: Path to .json.gz archive
            height_range: Optional (min_height, max_height) to restore subset
        """
        logger.info(f"📥 Restoring from archive: {archive_path}")
        
        with gzip.open(archive_path, 'rt', encoding='utf-8') as f:
            archive_data = json.load(f)
        
        blocks = archive_data['blocks']
        
        # Filter by height range if specified
        if height_range:
            min_h, max_h = height_range
            blocks = [b for b in blocks if min_h <= b['height'] <= max_h]
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        restored_count = 0
        for block in blocks:
            try:
                cursor.execute("""
                    INSERT OR REPLACE INTO real_blocks 
                    (height, hash, previous_hash, timestamp, nonce, difficulty,
                     transactions_json, reward, miner_address, consciousness_level, sacred_multiplier)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    block['height'],
                    block['hash'],
                    block['previous_hash'],
                    block['timestamp'],
                    block['nonce'],
                    block['difficulty'],
                    json.dumps(block['transactions']),
                    block['reward'],
                    block['miner_address'],
                    'PHYSICAL',  # Default consciousness
                    1.0  # Default multiplier
                ))
                restored_count += 1
            except Exception as e:
                logger.error(f"Error restoring block {block['height']}: {e}")
        
        conn.commit()
        conn.close()
        
        logger.info(f"✅ Restored {restored_count:,} blocks from archive")
        
        return restored_count
    
    def get_block_from_any_tier(self, height: int):
        """
        Smart block retrieval from HOT → WARM → COLD storage
        Transparent for explorer API
        """
        # Try HOT storage first (main DB)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM real_blocks WHERE height = ?", (height,))
        block = cursor.fetchone()
        conn.close()
        
        if block:
            return {'tier': 'HOT', 'block': block}
        
        # Try WARM/COLD storage (archives)
        for archive_file in sorted(self.archive_dir.glob("blocks_archive_*.json.gz"), reverse=True):
            with gzip.open(archive_file, 'rt', encoding='utf-8') as f:
                archive_data = json.load(f)
            
            # Check if block might be in this archive
            min_h, max_h = archive_data['height_range']
            if min_h <= height <= max_h:
                for block in archive_data['blocks']:
                    if block['height'] == height:
                        return {'tier': 'ARCHIVE', 'block': block, 'archive': str(archive_file)}
        
        return None
    
    def optimize_pool_database(self, pool_db_path: str = "zion_pool.db"):
        """Optimize pool database (shares, miners, blocks)"""
        logger.info(f"🔧 Optimizing pool database: {pool_db_path}")
        
        if not os.path.exists(pool_db_path):
            logger.warning(f"Pool database not found: {pool_db_path}")
            return
        
        before_size = os.path.getsize(pool_db_path) / 1024 / 1024
        
        conn = sqlite3.connect(pool_db_path)
        cursor = conn.cursor()
        
        # Delete old invalid shares (keep only last 7 days)
        cutoff = (datetime.now() - timedelta(days=7)).timestamp()
        cursor.execute("DELETE FROM shares WHERE is_valid = 0 AND timestamp < ?", (cutoff,))
        deleted_shares = cursor.rowcount
        
        # VACUUM
        conn.execute("VACUUM")
        conn.commit()
        conn.close()
        
        after_size = os.path.getsize(pool_db_path) / 1024 / 1024
        saved_mb = before_size - after_size
        
        logger.info(f"✅ Pool DB optimized:")
        logger.info(f"   Deleted invalid shares: {deleted_shares:,}")
        logger.info(f"   Space saved: {saved_mb:.2f} MB")
        
        return saved_mb


def main():
    """CLI interface for database management"""
    import argparse
    
    parser = argparse.ArgumentParser(description="ZION Database Manager")
    parser.add_argument('--analyze', action='store_true', help='Analyze database')
    parser.add_argument('--vacuum', action='store_true', help='Run VACUUM to optimize')
    parser.add_argument('--archive', type=int, metavar='DAYS', help='Archive blocks older than N days')
    parser.add_argument('--restore', type=str, metavar='ARCHIVE', help='Restore from archive file')
    parser.add_argument('--optimize-pool', action='store_true', help='Optimize pool database')
    parser.add_argument('--db', default='zion_unified_blockchain.db', help='Database path')
    
    args = parser.parse_args()
    
    manager = ZionDatabaseManager(args.db)
    
    if args.analyze:
        manager.analyze_database()
    
    if args.vacuum:
        manager.vacuum_database()
    
    if args.archive:
        manager.archive_old_blocks(args.archive)
    
    if args.restore:
        archive_path = Path(args.restore)
        if archive_path.exists():
            manager.restore_from_archive(archive_path)
        else:
            logger.error(f"Archive not found: {archive_path}")
    
    if args.optimize_pool:
        manager.optimize_pool_database()
    
    if not any([args.analyze, args.vacuum, args.archive, args.restore, args.optimize_pool]):
        parser.print_help()


if __name__ == "__main__":
    main()
