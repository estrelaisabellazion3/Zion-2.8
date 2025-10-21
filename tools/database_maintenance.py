#!/usr/bin/env python3
"""
ZION Database Maintenance Tool
Provádí optimalizaci a kompresi databází jednou za 6 měsíců
"""

import sqlite3
import os
import time
import shutil
from datetime import datetime
from pathlib import Path

class DatabaseMaintenance:
    """Správa a údržba ZION databází"""
    
    def __init__(self, db_dir: str = "."):
        self.db_dir = Path(db_dir)
        self.databases = [
            "zion_pool.db",
            "zion_unified_blockchain.db",
            "zion_real_blockchain.db"
        ]
        
    def get_db_info(self, db_file: str):
        """Získá informace o databázi"""
        if not os.path.exists(db_file):
            return None
            
        size_mb = os.path.getsize(db_file) / 1024 / 1024
        
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        # Get page info
        cursor.execute('PRAGMA page_count')
        page_count = cursor.fetchone()[0]
        cursor.execute('PRAGMA page_size')
        page_size = cursor.fetchone()[0]
        cursor.execute('PRAGMA freelist_count')
        freelist = cursor.fetchone()[0]
        
        # Get table counts
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        table_info = {}
        for table in tables:
            table_name = table[0]
            # SECURITY: table_name comes from sqlite_master (system table)
            # This is safer than user input, but still documented for review
            # Consider whitelist validation if this becomes user-facing
            cursor.execute(f'SELECT COUNT(*) FROM {table_name}')
            count = cursor.fetchone()[0]
            table_info[table_name] = count
        
        conn.close()
        
        return {
            'size_mb': size_mb,
            'page_count': page_count,
            'page_size': page_size,
            'freelist_pages': freelist,
            'wasted_mb': (freelist * page_size) / 1024 / 1024,
            'tables': table_info
        }
    
    def vacuum_database(self, db_file: str):
        """Provede VACUUM na databázi (komprese a defragmentace)"""
        print(f"\n🔧 Optimizing {db_file}...")
        
        if not os.path.exists(db_file):
            print(f"   ⚠️  Database not found: {db_file}")
            return False
        
        # Get info before
        before = self.get_db_info(db_file)
        print(f"   Before: {before['size_mb']:.2f} MB ({before['freelist_pages']:,} free pages)")
        
        # Backup first
        backup_file = f"{db_file}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        print(f"   📦 Creating backup: {os.path.basename(backup_file)}")
        shutil.copy2(db_file, backup_file)
        
        try:
            # Run VACUUM
            start_time = time.time()
            conn = sqlite3.connect(db_file)
            print(f"   ♻️  Running VACUUM (this may take a while)...")
            conn.execute('VACUUM')
            
            # Run ANALYZE for query optimization
            print(f"   📊 Running ANALYZE...")
            conn.execute('ANALYZE')
            
            conn.close()
            elapsed = time.time() - start_time
            
            # Get info after
            after = self.get_db_info(db_file)
            saved_mb = before['size_mb'] - after['size_mb']
            saved_percent = (saved_mb / before['size_mb'] * 100) if before['size_mb'] > 0 else 0
            
            print(f"   After:  {after['size_mb']:.2f} MB ({after['freelist_pages']:,} free pages)")
            print(f"   ✅ Saved: {saved_mb:.2f} MB ({saved_percent:.1f}%)")
            print(f"   ⏱️  Time: {elapsed:.1f}s")
            
            # Remove backup if successful
            if saved_mb > 0:
                os.remove(backup_file)
                print(f"   🗑️  Backup removed (optimization successful)")
            else:
                print(f"   💾 Backup kept: {os.path.basename(backup_file)}")
            
            return True
            
        except Exception as e:
            print(f"   ❌ Error during VACUUM: {e}")
            print(f"   💾 Backup preserved: {os.path.basename(backup_file)}")
            return False
    
    def analyze_all(self):
        """Analyzuje všechny databáze"""
        print("=" * 70)
        print("🔍 ZION DATABASE ANALYSIS")
        print("=" * 70)
        
        total_size = 0
        total_wasted = 0
        
        for db_file in self.databases:
            db_path = self.db_dir / db_file
            info = self.get_db_info(str(db_path))
            
            if not info:
                print(f"\n📄 {db_file}: NOT FOUND")
                continue
            
            total_size += info['size_mb']
            total_wasted += info['wasted_mb']
            
            print(f"\n📄 {db_file}:")
            print(f"   Size: {info['size_mb']:.2f} MB")
            print(f"   Pages: {info['page_count']:,} × {info['page_size']} bytes")
            print(f"   Wasted: {info['wasted_mb']:.2f} MB ({info['freelist_pages']:,} free pages)")
            print(f"   Tables:")
            for table, count in info['tables'].items():
                print(f"     - {table}: {count:,} records")
        
        print(f"\n{'=' * 70}")
        print(f"📊 TOTAL: {total_size:.2f} MB (wasted: {total_wasted:.2f} MB)")
        print(f"💡 Potential savings: {total_wasted:.2f} MB ({total_wasted/total_size*100:.1f}%)")
        print("=" * 70)
        
        return total_size, total_wasted
    
    def optimize_all(self):
        """Optimalizuje všechny databáze"""
        print("=" * 70)
        print("🚀 ZION DATABASE OPTIMIZATION")
        print("=" * 70)
        print("\n⚠️  This will optimize all databases.")
        print("📦 Backups will be created automatically.")
        print("⏱️  This may take several minutes for large databases.\n")
        
        # Analyze first
        total_before, wasted_before = self.analyze_all()
        
        # Ask for confirmation
        response = input("\n❓ Proceed with optimization? [y/N]: ")
        if response.lower() != 'y':
            print("❌ Optimization cancelled.")
            return
        
        print("\n" + "=" * 70)
        total_saved = 0
        
        for db_file in self.databases:
            db_path = self.db_dir / db_file
            if os.path.exists(db_path):
                before_size = os.path.getsize(db_path) / 1024 / 1024
                if self.vacuum_database(str(db_path)):
                    after_size = os.path.getsize(db_path) / 1024 / 1024
                    total_saved += (before_size - after_size)
        
        print("\n" + "=" * 70)
        print(f"✅ OPTIMIZATION COMPLETE")
        print(f"💾 Total saved: {total_saved:.2f} MB")
        print("=" * 70)
    
    def auto_maintenance(self, force: bool = False):
        """Automatická údržba - provádí se jednou za 6 měsíců"""
        marker_file = self.db_dir / ".last_maintenance"
        
        # Check when was last maintenance
        if marker_file.exists() and not force:
            last_maint = datetime.fromtimestamp(marker_file.stat().st_mtime)
            days_since = (datetime.now() - last_maint).days
            
            if days_since < 180:  # 6 months = ~180 days
                print(f"ℹ️  Last maintenance: {days_since} days ago")
                print(f"⏳ Next maintenance in: {180 - days_since} days")
                print(f"💡 Use --force to run anyway")
                return
        
        print("🔧 Running automatic 6-month maintenance...")
        self.optimize_all()
        
        # Update marker
        marker_file.touch()
        print(f"✅ Maintenance marker updated: {marker_file}")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="ZION Database Maintenance Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze databases
  python database_maintenance.py --analyze
  
  # Optimize all databases (interactive)
  python database_maintenance.py --optimize
  
  # Auto maintenance (runs if 6+ months since last)
  python database_maintenance.py --auto
  
  # Force maintenance regardless of last run
  python database_maintenance.py --auto --force
        """
    )
    
    parser.add_argument('--db-dir', default='.',
                        help='Directory containing databases (default: current)')
    parser.add_argument('--analyze', action='store_true',
                        help='Analyze database sizes and fragmentation')
    parser.add_argument('--optimize', action='store_true',
                        help='Optimize all databases (VACUUM + ANALYZE)')
    parser.add_argument('--auto', action='store_true',
                        help='Auto maintenance (runs every 6 months)')
    parser.add_argument('--force', action='store_true',
                        help='Force maintenance even if recently run')
    
    args = parser.parse_args()
    
    maint = DatabaseMaintenance(args.db_dir)
    
    if args.analyze:
        maint.analyze_all()
    elif args.optimize:
        maint.optimize_all()
    elif args.auto:
        maint.auto_maintenance(force=args.force)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
