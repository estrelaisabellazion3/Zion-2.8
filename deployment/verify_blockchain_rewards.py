#!/usr/bin/env python3
import sys
sys.path.insert(0, "/root")

try:
    from new_zion_blockchain import NewZionBlockchain
    
    blockchain = NewZionBlockchain(enable_p2p=False, enable_rpc=False)
    
    print("=" * 80)
    print("📊 BLOCKCHAIN & WALLET VERIFICATION")
    print("=" * 80)
    
    print("\n📦 BLOCKCHAIN STATUS:")
    print(f"  Blocks: {len(blockchain.blocks)}")
    print(f"  Pending TXs: {len(blockchain.pending_transactions)}")
    print(f"  Addresses with balance: {len(blockchain.balances)}")
    
    # Pending transactions
    if blockchain.pending_transactions:
        print(f"\n💳 PENDING TRANSACTIONS (awaiting next block):")
        for i, tx in enumerate(blockchain.pending_transactions[:5], 1):
            sender = tx.get('sender', 'unknown')[:20]
            receiver = tx.get('receiver', 'unknown')[:20]
            amount = tx.get('amount', 0)
            print(f"  {i}. {amount:.2f} ZION: {sender}... → {receiver}...")
        if len(blockchain.pending_transactions) > 5:
            print(f"  ... and {len(blockchain.pending_transactions) - 5} more")
    else:
        print(f"\n✅ No pending transactions (all confirmed in blocks)")
    
    # Miner balance
    miner_addr = "Z32f72f93c095d78fc8a2fe01c0f97fd4a7f6d1bcd9b251f73b18b5625be654e84"
    balance = blockchain.balances.get(miner_addr, 0)
    print(f"\n💎 MINER WALLET:")
    print(f"  Address: {miner_addr}")
    print(f"  Balance: {balance:.8f} ZION")
    
    # Count miner rewards in ALL blocks
    miner_rewards = 0
    reward_count = 0
    print(f"\n🏗️  MINER REWARDS IN ALL BLOCKCHAIN BLOCKS:")
    print(f"  (Scanning {len(blockchain.blocks)} blocks...)")
    for block_idx, block in enumerate(blockchain.blocks):
        block_rewards = 0
        for tx in block.get("transactions", []):
            if tx.get("receiver") == miner_addr:
                amount = tx.get("amount", 0)
                block_rewards += amount
                miner_rewards += amount
                reward_count += 1
        if block_rewards > 0:
            height = block.get('height', '?')
            print(f"  Block {height}: {block_rewards:.8f} ZION")
    
    print(f"\n✅ TOTAL CONFIRMED REWARDS: {miner_rewards:.8f} ZION ({reward_count} transactions)")
    
    # Balance check
    print(f"\n🔍 VERIFICATION:")
    print(f"  Balance in state: {balance:.8f} ZION")
    print(f"  Sum of rewards: {miner_rewards:.8f} ZION")
    if abs(balance - miner_rewards) < 0.01:
        print(f"  ✅ MATCH - Rewards properly credited!")
    else:
        print(f"  ⚠️  Difference: {abs(balance - miner_rewards):.8f} ZION")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
