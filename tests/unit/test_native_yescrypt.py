#!/usr/bin/env python3
"""
Test native Yescrypt implementation in Universal Miner
Tests connection to pool and mining functionality
"""

import sys
import time
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

# Add ai directory to path
sys.path.insert(0, '/media/maitreya/ZION1')

from ai.zion_universal_miner import ZionUniversalMiner, MiningMode

def test_native_yescrypt():
    """Test native Yescrypt mining"""
    print("=" * 60)
    print("🔥 TESTING NATIVE YESCRYPT MINING")
    print("=" * 60)
    
    # Create miner in CPU-only mode
    miner = ZionUniversalMiner(mode=MiningMode.CPU_ONLY)
    
    print("\n📋 Miner Configuration:")
    print(f"   Mode: {miner.mode.value}")
    print(f"   CPU Available: {miner.cpu_available}")
    print(f"   CPU Threads: {miner.optimal_cpu_threads}")
    print(f"   XMRig Path: {miner.xmrig_path or 'Not found (will use native)'}")
    
    # Start mining with Yescrypt
    print("\n🚀 Starting native Yescrypt mining...")
    print("   Pool: 91.98.122.165:3333")
    print("   Wallet: ZION_NATIVE_YESCRYPT_TEST")
    print("   Duration: 30 seconds")
    print()
    
    result = miner.start_mining(
        pool_url="stratum+tcp://91.98.122.165:3333",
        wallet_address="ZION_NATIVE_YESCRYPT_TEST",
        worker_name="native_test",
        algorithm="yescrypt"
    )
    
    if not result['success']:
        print(f"❌ Failed to start mining: {result.get('message')}")
        return False
    
    print(f"✅ Mining started: {result.get('message')}")
    
    # Mine for 30 seconds
    try:
        for i in range(30):
            time.sleep(1)
            status = miner.get_status()
            
            if (i + 1) % 5 == 0:
                print(f"\n📊 Status ({i+1}s):")
                print(f"   Hashrate: {status.get('cpu_hashrate', 0):.2f} H/s")
                print(f"   Shares: {status.get('total_shares', 0)}")
                print(f"   Accepted: {status.get('accepted_shares', 0)}")
                print(f"   Rejected: {status.get('rejected_shares', 0)}")
    
    except KeyboardInterrupt:
        print("\n⚠️  Test interrupted by user")
    
    # Stop mining
    print("\n🛑 Stopping mining...")
    stop_result = miner.stop_mining()
    
    print("\n" + "=" * 60)
    print("📊 FINAL RESULTS")
    print("=" * 60)
    
    final_status = miner.get_status()
    print(f"   Final Hashrate: {final_status.get('cpu_hashrate', 0):.2f} H/s")
    print(f"   Total Shares: {final_status.get('total_shares', 0)}")
    print(f"   Accepted: {final_status.get('accepted_shares', 0)}")
    print(f"   Rejected: {final_status.get('rejected_shares', 0)}")
    print(f"   Uptime: {final_status.get('uptime', 0)} seconds")
    
    if final_status.get('cpu_hashrate', 0) > 0:
        print("\n✅ TEST PASSED - Native Yescrypt mining works!")
        return True
    else:
        print("\n⚠️  WARNING - No hashrate detected")
        return False

if __name__ == "__main__":
    success = test_native_yescrypt()
    sys.exit(0 if success else 1)
