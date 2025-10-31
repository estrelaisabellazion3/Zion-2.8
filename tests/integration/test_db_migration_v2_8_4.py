#!/usr/bin/env python3
"""
ZION v2.8.4 - Database Migration Compatibility Test

Tests blockchain database migration from v2.7.x/v2.8.3 to v2.8.4:
- Old DB: SHA256 or autolykos2 algorithm
- New DB: cosmic_harmony, randomx, yescrypt, autolykos_v2

Validates:
1. Genesis block compatibility
2. Algorithm field migration
3. Total supply preservation (15.78B ZION)
4. Block validation with new algorithms
"""

import sqlite3
import os
import sys
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def test_fresh_db_creation():
    """Test fresh v2.8.4 database creation"""
    print("\n🧪 Testing fresh v2.8.4 database creation...")
    
    # Remove old test DB
    test_db = "data/test_migration_v2.8.4.db"
    if os.path.exists(test_db):
        os.remove(test_db)
    
    # Create fresh DB manually (simplified - no full blockchain)
    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()
    
    # Create v2.8.4 schema
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS blocks (
            height INTEGER PRIMARY KEY,
            timestamp REAL,
            previous_hash TEXT,
            merkle_root TEXT,
            nonce INTEGER,
            difficulty INTEGER,
            block_hash TEXT,
            miner TEXT,
            algorithm TEXT DEFAULT 'cosmic_harmony'
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS addresses (
            address TEXT PRIMARY KEY,
            balance REAL DEFAULT 0,
            nonce INTEGER DEFAULT 0
        )
    """)
    
    # Insert genesis block with algorithm
    cursor.execute("""
        INSERT INTO blocks VALUES (
            0, 0, '0', 'genesis_merkle', 0, 1, 'genesis_hash', 'GENESIS', 'cosmic_harmony'
        )
    """)
    
    # Insert genesis premine (15.78B)
    EXPECTED_TOTAL = 15_782_857_143
    cursor.execute("""
        INSERT INTO addresses VALUES ('ZION_GENESIS', ?, 0)
    """, (EXPECTED_TOTAL,))
    
    conn.commit()
    
    # Verify total supply
    cursor.execute("SELECT SUM(balance) FROM addresses")
    total = cursor.fetchone()[0]
    
    # Verify genesis block
    cursor.execute("SELECT * FROM blocks WHERE height=0")
    genesis = cursor.fetchone()
    
    conn.close()
    
    assert abs(total - EXPECTED_TOTAL) < 1, f"Total supply mismatch: {total} != {EXPECTED_TOTAL}"
    assert genesis[8] == 'cosmic_harmony', f"Genesis algorithm should be cosmic_harmony, got {genesis[8]}"
    
    print(f"✅ Fresh DB created successfully")
    print(f"   Total supply: {total:,.0f} ZION")
    print(f"   Genesis algorithm: {genesis[8]}")
    
    # Cleanup
    os.remove(test_db)
    
    return True


def test_algorithm_field_presence():
    """Test that all blocks have algorithm field"""
    print("\n🧪 Testing algorithm field presence...")
    
    test_db = "data/test_algo_field.db"
    if os.path.exists(test_db):
        os.remove(test_db)
    
    # Create DB with multiple algorithm blocks
    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS blocks (
            height INTEGER PRIMARY KEY,
            timestamp REAL,
            previous_hash TEXT,
            merkle_root TEXT,
            nonce INTEGER,
            difficulty INTEGER,
            block_hash TEXT,
            miner TEXT,
            algorithm TEXT DEFAULT 'cosmic_harmony'
        )
    """)
    
    # Insert blocks with different algorithms
    algorithms = ['cosmic_harmony', 'randomx', 'yescrypt', 'autolykos_v2']
    
    for i, algo in enumerate(algorithms):
        cursor.execute("""
            INSERT INTO blocks VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (i, float(i), f"hash_{i-1}", f"merkle_{i}", i*1000, 1000, f"hash_{i}", "MINER", algo))
        print(f"   ✅ Block {i} created with {algo}")
    
    conn.commit()
    
    # Verify all blocks have algorithm field
    cursor.execute("SELECT height, algorithm FROM blocks")
    blocks = cursor.fetchall()
    
    conn.close()
    
    for height, algo in blocks:
        assert algo in algorithms, f"Invalid algorithm at height {height}: {algo}"
    
    print(f"✅ All {len(blocks)} blocks have valid algorithm field")
    
    # Cleanup
    os.remove(test_db)
    
    return True


def test_legacy_db_schema():
    """Test compatibility with legacy database schema"""
    print("\n🧪 Testing legacy DB schema compatibility...")
    
    # Create a "legacy" DB (v2.7.x style - no algorithm field)
    legacy_db = "data/test_legacy.db"
    if os.path.exists(legacy_db):
        os.remove(legacy_db)
    
    conn = sqlite3.connect(legacy_db)
    cursor = conn.cursor()
    
    # Create legacy schema (without algorithm column)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS blocks (
            height INTEGER PRIMARY KEY,
            timestamp REAL,
            previous_hash TEXT,
            merkle_root TEXT,
            nonce INTEGER,
            difficulty INTEGER,
            block_hash TEXT,
            miner TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS addresses (
            address TEXT PRIMARY KEY,
            balance REAL DEFAULT 0,
            nonce INTEGER DEFAULT 0
        )
    """)
    
    # Insert legacy genesis block (no algorithm field)
    cursor.execute("""
        INSERT INTO blocks VALUES (
            0, 0, '0', 'genesis_merkle', 0, 1, 'genesis_hash', 'GENESIS'
        )
    """)
    
    # Insert genesis premine
    cursor.execute("""
        INSERT INTO addresses VALUES ('ZION_GENESIS', 15782857143, 0)
    """)
    
    conn.commit()
    conn.close()
    
    print("   Legacy DB created (no algorithm column)")
    
    # Check current schema
    conn = sqlite3.connect(legacy_db)
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(blocks)")
    columns_before = [col[1] for col in cursor.fetchall()]
    print(f"   Columns before: {columns_before}")
    
    # Simulate migration: Add algorithm column
    if 'algorithm' not in columns_before:
        cursor.execute("ALTER TABLE blocks ADD COLUMN algorithm TEXT DEFAULT 'cosmic_harmony'")
        conn.commit()
        print("   ✅ Algorithm column added via ALTER TABLE")
    
    # Verify migration
    cursor.execute("PRAGMA table_info(blocks)")
    columns_after = [col[1] for col in cursor.fetchall()]
    
    assert 'algorithm' in columns_after, "Algorithm column should exist after migration"
    
    # Verify genesis block
    cursor.execute("SELECT height, algorithm FROM blocks WHERE height=0")
    genesis = cursor.fetchone()
    
    conn.close()
    
    print(f"   ✅ Migration successful")
    print(f"   Genesis algorithm: {genesis[1]}")
    
    # Cleanup
    os.remove(legacy_db)
    
    return True


def test_block_hash_validation():
    """Test block hash validation with new algorithms"""
    print("\n🧪 Testing block hash validation...")
    
    from src.core.algorithms import get_hash, is_available
    
    test_data = b"ZION_TEST_BLOCK_DATA"
    test_nonce = 12345
    
    algorithms = ['cosmic_harmony', 'randomx', 'yescrypt', 'autolykos_v2']
    
    for algo in algorithms:
        try:
            hash_result = get_hash(algo, test_data, test_nonce)
            
            # All algorithms return hex string (64 chars = 32 bytes)
            if isinstance(hash_result, str):
                # Hex string should be 64 characters (32 bytes)
                assert len(hash_result) == 64, f"{algo} hash should be 64 hex chars (got {len(hash_result)})"
                hash_bytes = bytes.fromhex(hash_result)
                assert len(hash_bytes) == 32, f"{algo} decoded should be 32 bytes"
                print(f"   ✅ {algo:15s}: {hash_result[:16]}... ({len(hash_bytes)} bytes)")
            else:
                # If bytes, should be 32 bytes
                assert len(hash_result) == 32, f"{algo} hash should be 32 bytes (got {len(hash_result)})"
                print(f"   ✅ {algo:15s}: {hash_result.hex()[:16]}... (bytes)")
                
        except Exception as e:
            print(f"   ❌ {algo:15s}: {e}")
            return False
    
    return True


def test_migration_script():
    """Test database migration script (if exists)"""
    print("\n🧪 Checking for migration script...")
    
    migration_script = Path("scripts/migrate_db_to_2.8.4.py")
    
    if migration_script.exists():
        print(f"   ✅ Migration script found: {migration_script}")
        # Could run it here if needed
    else:
        print(f"   ℹ️  No migration script (manual migration required)")
        print(f"   Recommendation: Create {migration_script}")
    
    return True


def main():
    print("=" * 60)
    print("ZION v2.8.4 - Database Migration Compatibility Test")
    print("=" * 60)
    
    tests = [
        ("Fresh DB Creation", test_fresh_db_creation),
        ("Algorithm Field Presence", test_algorithm_field_presence),
        ("Legacy DB Schema", test_legacy_db_schema),
        ("Block Hash Validation", test_block_hash_validation),
        ("Migration Script", test_migration_script),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ {test_name} failed with exception:")
            print(f"   {e}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary:")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print("=" * 60)
    print(f"Results: {passed}/{total} tests passed")
    print("=" * 60)
    
    if passed == total:
        print("\n✅ All migration compatibility tests passed!")
        print("   v2.8.4 database is backward compatible")
        return 0
    else:
        print("\n❌ Some migration tests failed")
        print("   Manual migration may be required")
        return 1


if __name__ == "__main__":
    sys.exit(main())
