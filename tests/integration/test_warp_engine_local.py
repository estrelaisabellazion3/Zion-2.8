#!/usr/bin/env python3
"""
Quick Test - ZION WARP Engine Local
Lokální test WARP enginu bez dlouhého běhu
"""

import asyncio
import sys
import time
from zion_warp_engine_core import ZionWARPEngine

async def quick_test():
    """Quick test WARP engine komponenty"""
    print("\n🔥 QUICK TEST - ZION WARP ENGINE 🔥\n")
    
    # Initialize engine
    print("📦 Initializing WARP Engine...")
    engine = ZionWARPEngine(
        blockchain_db="zion_blockchain.db",
        enable_rpc=True,
        enable_p2p=True,
        enable_bridge=False  # Disable bridge for quick test
    )
    
    print("\n✅ WARP Engine initialized!\n")
    
    # Display status
    status = engine.get_status()
    
    print("=" * 80)
    print("📊 WARP ENGINE STATUS SNAPSHOT")
    print("=" * 80)
    print(f"⛓️  Blockchain Height: {status.blockchain_height}")
    print(f"💰 Balances: {status.blockchain_balances}")
    print(f"🌐 RPC: {'ACTIVE' if status.rpc_active else 'READY'} (port {status.rpc_port})")
    print(f"🌐 P2P: {'ACTIVE' if status.p2p_active else 'READY'} (port {status.p2p_port})")
    print(f"⛏️  Mining Pools: {status.pool_connections} configured")
    print(f"   - Active: {status.active_pools}")
    print(f"🌈 Bridge: {'ACTIVE' if status.bridge_active else 'DISABLED'}")
    print(f"✨ Consciousness Field: {status.consciousness_field:.2f}")
    print("=" * 80)
    
    # List pools
    print("\n⛏️  CONFIGURED POOLS:")
    for pool_id, pool in engine.pools.items():
        print(f"   {pool.name}")
        print(f"   └─ {pool.host}:{pool.port} ({', '.join(pool.algorithms)})")
    
    # List seed nodes
    print("\n🌱 SEED NODES:")
    for node in engine.seed_nodes:
        print(f"   {node.host}:{node.port} ({node.protocol_version})")
    
    # Test pool connections
    print("\n⛏️  Testing Pool Connections...")
    await engine._connect_pools()
    
    active_count = sum(1 for p in engine.pools.values() if p.active)
    print(f"   ✅ {active_count}/{len(engine.pools)} pools are online")
    
    # Test blockchain operations
    print("\n⛓️  Testing Blockchain Operations...")
    test_addr = list(engine.blockchain.balances.keys())[0] if engine.blockchain.balances else "ZIONtest123"
    balance = engine.get_balance(test_addr)
    print(f"   Balance for {test_addr[:20]}...: {balance:,.2f} ZION")
    
    print("\n" + "=" * 80)
    print("✅ QUICK TEST COMPLETE - WARP ENGINE READY!")
    print("=" * 80)
    print("\nTo start full engine, run: python3 zion_warp_engine_core.py")
    print()

if __name__ == "__main__":
    asyncio.run(quick_test())
