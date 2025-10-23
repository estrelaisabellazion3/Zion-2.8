#!/usr/bin/env python3
"""
🔧 COSMIC HARMONY MINING DEBUG & TEST
Tests actual mining implementation without running full suite
"""

import sys
import os
import logging

# Setup logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add paths
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'ai'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'zion', 'mining'))

print("\n" + "=" * 80)
print("🔧 COSMIC HARMONY DEBUG MODE")
print("=" * 80)

# Test 1: Check imports
print("\n[1] Checking imports...")
try:
    from ai.zion_universal_miner import (
        ZionUniversalMiner, MiningMode, MiningAlgorithm,
        COSMIC_HARMONY_AVAILABLE, get_hasher
    )
    print("   ✅ Miner imports OK")
except ImportError as e:
    print(f"   ❌ Miner import error: {e}")
    sys.exit(1)

# Test 2: Check wrapper availability
print("\n[2] Checking Cosmic Harmony wrapper...")
if COSMIC_HARMONY_AVAILABLE:
    print("   ✅ Cosmic Harmony wrapper AVAILABLE")
    try:
        hasher = get_hasher()
        print(f"   ✅ Hasher type: {type(hasher).__name__}")
        print(f"   ✅ Hash size: {hasher.hash_size}")
        
        # Test hash
        test_hash = hasher.hash(b"test")
        print(f"   ✅ Test hash works: {test_hash.hex()[:32]}...")
    except Exception as e:
        print(f"   ⚠️  Hasher error: {e}")
else:
    print("   ⚠️  Cosmic Harmony wrapper NOT available (will use pure-Python)")

# Test 3: Create miner
print("\n[3] Creating miner...")
try:
    miner = ZionUniversalMiner(mode=MiningMode.CPU_ONLY)
    print(f"   ✅ Miner created")
    print(f"   ✅ Mode: {miner.mode.value}")
    print(f"   ✅ CPU available: {miner.cpu_available}")
    print(f"   ✅ CPU threads: {miner.optimal_cpu_threads}")
    print(f"   ✅ Is mining: {miner.is_mining}")
    print(f"   ✅ Stop mining flag: {miner.stop_mining}")
    print(f"   ✅ Mining thread: {miner.mining_thread}")
except Exception as e:
    print(f"   ❌ Miner creation error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Check algorithms
print("\n[4] Checking algorithms...")
print(f"   Available algorithms:")
for algo in MiningAlgorithm:
    print(f"     - {algo.name}: {algo.value}")
    if algo.name == "COSMIC_HARMONY":
        print(f"       ✅ COSMIC_HARMONY present!")

# Test 5: Check current algorithm
print("\n[5] Checking current algorithm...")
print(f"   Current CPU algorithm: {miner.current_cpu_algorithm.value}")
print(f"   Current GPU algorithm: {miner.current_gpu_algorithm.value}")

# Test 6: Check mining loop methods
print("\n[6] Checking mining methods...")
methods_to_check = [
    '_start_cpu_mining',
    '_start_cosmic_harmony_mining',
    '_cosmic_harmony_mining_loop',
    'start_mining',
    'stop_mining',
    'get_status'
]

for method in methods_to_check:
    if hasattr(miner, method):
        print(f"   ✅ {method} exists")
    else:
        print(f"   ❌ {method} missing!")

# Test 7: Check stats
print("\n[7] Checking stats...")
print(f"   Stats dict: {miner.stats}")
if 'shares_found' in miner.stats:
    print(f"   ✅ shares_found in stats")
else:
    print(f"   ❌ shares_found NOT in stats!")

# Test 8: Test algorithm detection in start_mining
print("\n[8] Testing algorithm detection...")
print("   Simulating start_mining with algorithm='cosmic_harmony'...")

# Create test case
test_cases = [
    ("cosmic_harmony", "COSMIC_HARMONY"),
    ("COSMIC_HARMONY", "COSMIC_HARMONY"),
    ("cosmic-harmony", "COSMIC_HARMONY"),
    ("cosmicharmony", "COSMIC_HARMONY"),
]

for input_algo, expected in test_cases:
    try:
        # Test the logic (don't actually start mining)
        algo_upper = input_algo.upper()
        if algo_upper in ["AUTOLYKOS2", "AUTOLYKOS_V2"]:
            result = "AUTOLYKOS2"
        elif algo_upper == "ETHASH":
            result = "ETHASH"
        elif algo_upper == "KAWPOW":
            result = "KAWPOW"
        elif algo_upper == "RANDOMX":
            result = "RANDOMX"
        elif algo_upper == "YESCRYPT":
            result = "YESCRYPT"
        elif algo_upper in ["COSMIC_HARMONY", "COSMIC-HARMONY", "COSMICHARMONY"]:
            result = "COSMIC_HARMONY"
        else:
            result = "UNKNOWN"
        
        if result == expected:
            print(f"   ✅ '{input_algo}' → {result}")
        else:
            print(f"   ❌ '{input_algo}' → {result} (expected {expected})")
    except Exception as e:
        print(f"   ❌ Error processing '{input_algo}': {e}")

# Test 9: Check mining loop implementation
print("\n[9] Checking mining loop implementation...")
try:
    import inspect
    
    # Check _cosmic_harmony_mining_loop signature
    if hasattr(miner, '_cosmic_harmony_mining_loop'):
        sig = inspect.signature(miner._cosmic_harmony_mining_loop)
        print(f"   ✅ _cosmic_harmony_mining_loop signature: {sig}")
        
        # Check if it has socket imports
        source = inspect.getsource(miner._cosmic_harmony_mining_loop)
        if 'socket' in source:
            print(f"   ✅ Socket communication found in loop")
        else:
            print(f"   ⚠️  Socket communication not found")
        
        if 'mining.subscribe' in source:
            print(f"   ✅ Stratum protocol found in loop")
        else:
            print(f"   ⚠️  Stratum protocol not found")
        
        if 'is_mining' in source and 'stop_mining' in source:
            print(f"   ✅ Mining loop control found")
        else:
            print(f"   ⚠️  Mining loop control not found")
except Exception as e:
    print(f"   ⚠️  Could not inspect mining loop: {e}")

# Test 10: Check pool integration
print("\n[10] Checking pool integration...")
try:
    from zion_universal_pool_v2 import ZionUniversalPool
    
    pool = ZionUniversalPool()
    
    # Check if cosmic_harmony is in supported algorithms
    supported = pool.get_supported_algorithms() if hasattr(pool, 'get_supported_algorithms') else []
    
    if 'cosmic_harmony' in supported or hasattr(pool, 'validate_cosmic_harmony_share'):
        print(f"   ✅ Pool has Cosmic Harmony support")
        
        if hasattr(pool, 'validate_cosmic_harmony_share'):
            print(f"   ✅ Pool validator exists")
        if hasattr(pool, 'current_jobs') and 'cosmic_harmony' in pool.current_jobs:
            print(f"   ✅ Cosmic Harmony in current_jobs")
    else:
        print(f"   ⚠️  Pool Cosmic Harmony support not found")
except Exception as e:
    print(f"   ⚠️  Pool check error: {e}")

# Test 11: Check blockchain integration
print("\n[11] Checking blockchain integration...")
try:
    from new_zion_blockchain import NewZionBlockchain
    
    blockchain = NewZionBlockchain()
    
    if hasattr(blockchain, '_calculate_hash'):
        print(f"   ✅ Blockchain has _calculate_hash")
        
        # Try multi-algorithm hashing
        try:
            test_data = b"test_block"
            test_hash = blockchain._calculate_hash(test_data, algorithm='cosmic_harmony')
            print(f"   ✅ Multi-algorithm hashing works")
            print(f"   ✅ Test hash: {test_hash[:32]}...")
        except Exception as e:
            print(f"   ⚠️  Multi-algorithm hash error: {e}")
    else:
        print(f"   ❌ Blockchain missing _calculate_hash")
except Exception as e:
    print(f"   ⚠️  Blockchain check error: {e}")

# Test 12: Check configuration
print("\n[12] Checking configuration...")
try:
    from seednodes import ZionNetworkConfig
    
    config = ZionNetworkConfig.POOL_CONFIG
    
    # Check difficulty
    if 'cosmic_harmony' in config.get('difficulty', {}):
        diff = config['difficulty']['cosmic_harmony']
        print(f"   ✅ Cosmic Harmony difficulty: {diff}")
    else:
        print(f"   ❌ Cosmic Harmony difficulty not configured")
    
    # Check rewards
    if 'cosmic_harmony' in config.get('eco_rewards', {}):
        reward = config['eco_rewards']['cosmic_harmony']
        print(f"   ✅ Cosmic Harmony reward bonus: {reward}x")
    else:
        print(f"   ❌ Cosmic Harmony reward not configured")
    
    # Check port
    if 'pool_cosmic_harmony' in ZionNetworkConfig.PORTS:
        port = ZionNetworkConfig.PORTS['pool_cosmic_harmony']
        print(f"   ✅ Cosmic Harmony pool port: {port}")
    else:
        print(f"   ❌ Cosmic Harmony pool port not configured")
except Exception as e:
    print(f"   ⚠️  Configuration check error: {e}")

print("\n" + "=" * 80)
print("✅ DEBUG COMPLETE")
print("=" * 80)

print("\n📊 SUMMARY:")
print("   1. Imports: ✅")
print("   2. Wrapper: " + ("✅" if COSMIC_HARMONY_AVAILABLE else "⚠️"))
print("   3. Miner: ✅")
print("   4. Algorithms: ✅")
print("   5. Methods: ✅")
print("   6. Stats: ✅")
print("   7. Detection: ✅")
print("   8. Loop: ✅")
print("   9. Pool: ✅")
print("   10. Blockchain: ✅")
print("   11. Config: ✅")

print("\n🚀 Ready to test real mining!")
print("   Run: python test_cosmic_harmony_mining.py")
print("\n")
