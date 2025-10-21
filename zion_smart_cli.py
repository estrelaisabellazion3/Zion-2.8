#!/usr/bin/env python3
"""
ZION 2.7.5 Smart CLI - Automatic Best Implementation Selection
Automaticky vybere nejlepší dostupnou blockchain implementaci
"""

import os
import sys
import argparse

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def detect_available_implementations():
    """Detect which blockchain implementations are available"""
    implementations = {
        'real_2.7.1': False,
        'main_2.7.5': False,
        'simple_cli': False
    }
    
    # Check Real Blockchain from 2.7.1
    try:
        from core.real_blockchain import ZionRealBlockchain
        implementations['real_2.7.1'] = True
    except ImportError:
        pass
    
    # Check Main Blockchain from 2.7.5
    try:
        from new_zion_blockchain import NewZionBlockchain
        implementations['main_2.7.5'] = True
    except ImportError:
        pass
    
    # Check Simple CLI
    try:
        from zion_simple_cli import ZionSimpleCLI
        implementations['simple_cli'] = True
    except ImportError:
        pass
    
    return implementations

def get_best_implementation():
    """Get the best available implementation"""
    impls = detect_available_implementations()
    
    # Priority order: Real 2.7.1 > Main 2.7.5 > Simple CLI
    if impls['real_2.7.1']:
        return 'real_2.7.1'
    elif impls['main_2.7.5']:
        return 'main_2.7.5'
    elif impls['simple_cli']:
        return 'simple_cli'
    else:
        return None

def run_with_real_blockchain(args):
    """Run command with Real Blockchain (2.7.1)"""
    from core.real_blockchain import ZionRealBlockchain
    import time
    
    print("🌟 Using Real Blockchain Implementation (2.7.1)")
    
    # Initialize real blockchain
    db_path = os.path.join(os.path.dirname(__file__), 'zion_smart_blockchain.db')
    blockchain = ZionRealBlockchain(db_file=db_path)
    
    if args.command == 'stats':
        stats = blockchain.get_blockchain_stats()
        latest_block = blockchain.get_latest_block()

        print("🌟 ZION REAL BLOCKCHAIN STATISTICS")
        print("=" * 50)
        print(f"📦 Total Blocks: {stats['block_count']}")
        print(f"💰 Total Supply: {stats['total_supply']:,} atomic units")
        print(f"📝 Mempool Size: {stats['mempool_size']}")
        print(f"🎯 Difficulty: {stats['difficulty']}")

        if latest_block:
            print("\n🏆 Latest Block:")
            print(f"   Height: {latest_block.height}")
            print(f"   Hash: {latest_block.hash[:32]}...")
            print(f"   Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(latest_block.timestamp))}")
            print(f"   Transactions: {len(latest_block.transactions)}")
            print(f"   🧠 Consciousness: {latest_block.consciousness_level}")
            print(f"   🌟 Sacred Multiplier: {latest_block.sacred_multiplier:.2f}x")
    
    elif args.command == 'mine':
        print("🚀 Starting REAL BLOCKCHAIN MINING")
        print("🛡️ No simulations - creating actual blocks!")
        print("=" * 60)
        print(f"📧 Address: {args.address}")
        print(f"📦 Blocks: {args.blocks}")
        print("=" * 60)

        consciousness_levels = [
            "PHYSICAL", "ASTRAL", "MENTAL", "BUDDHIC",
            "ATMIC", "MONADIC", "LOGOIC", "ON_THE_STAR"
        ]

        blocks_mined = 0
        start_time = time.time()

        try:
            for i in range(args.blocks):
                consciousness = consciousness_levels[i % len(consciousness_levels)]
                
                print(f"\n⛏️ Mining REAL block {i+1}/{args.blocks}...")
                print(f"   🧠 Consciousness Level: {consciousness}")

                # Mine real block
                block = blockchain.mine_block(
                    miner_address=args.address,
                    consciousness_level=consciousness
                )

                if block:
                    blocks_mined += 1
                    print(f"   ✅ REAL BLOCK {block.height} CREATED!")
                    print(f"   🔗 Hash: {block.hash[:32]}...")
                    print(f"   💰 Reward: {block.reward:,} atomic units")
                else:
                    print("   ❌ Block mining failed (timeout)")

                time.sleep(0.1)

        except KeyboardInterrupt:
            print("\n⏹️ Real mining interrupted by user")

        duration = time.time() - start_time
        print(f"\n📊 MINING COMPLETE:")
        print(f"   Blocks Attempted: {args.blocks}")
        print(f"   Blocks Mined: {blocks_mined}")
        print(f"   Success Rate: {blocks_mined/args.blocks*100:.1f}%")
        print(f"   Total Time: {duration:.1f}s")

def run_with_main_blockchain(args):
    """Run command with Main Blockchain (2.7.5)"""
    from new_zion_blockchain import NewZionBlockchain
    
    print("🔗 Using Main Blockchain Implementation (2.7.5)")
    
    # Initialize main blockchain
    blockchain = NewZionBlockchain(enable_p2p=False, enable_rpc=False)
    
    if args.command == 'stats':
        print("🌟 ZION MAIN BLOCKCHAIN STATISTICS")
        print("=" * 50)
        print(f"📦 Total Blocks: {len(blockchain.blocks)}")
        print(f"💰 Total Supply: {blockchain.get_total_supply():,.0f} ZION")
        print(f"📝 Mempool Size: {len(blockchain.pending_transactions)}")
        print(f"🎯 Difficulty: {blockchain.mining_difficulty}")
        
        if blockchain.blocks:
            latest_block = blockchain.blocks[-1]
            print("\n🏆 Latest Block:")
            print(f"   Height: {latest_block['height']}")
            print(f"   Hash: {latest_block['hash'][:32]}...")
            import time
            print(f"   Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(latest_block['timestamp']))}")
            print(f"   Transactions: {len(latest_block['transactions'])}")
    
    elif args.command == 'mine':
        print("⛏️ Mining with Main Blockchain...")
        # Create a transaction and mine it
        blockchain.create_transaction(
            from_address=list(blockchain.premine_addresses.keys())[0],
            to_address=args.address,
            amount=0.1,
            purpose="Mining reward test"
        )
        
        block_hash = blockchain.mine_pending_transactions(args.address)
        print(f"✅ Block mined: {block_hash[:32]}...")

def run_with_simple_cli(args):
    """Run command with Simple CLI"""
    from zion_simple_cli import ZionSimpleCLI
    
    print("🔧 Using Simple CLI Implementation")
    
    cli = ZionSimpleCLI()
    
    if args.command == 'stats':
        cli.cmd_stats(args)
    elif args.command == 'mine':
        cli.cmd_mine(args)

def main():
    """Smart CLI main entry point"""
    print("🤖 ZION 2.7.5 Smart CLI - Auto Implementation Selection")
    print("🔍 Detecting available implementations...\n")
    
    # Detect implementations
    implementations = detect_available_implementations()
    best_impl = get_best_implementation()
    
    print("📊 Available Implementations:")
    print(f"   Real Blockchain (2.7.1): {'✅' if implementations['real_2.7.1'] else '❌'}")
    print(f"   Main Blockchain (2.7.5): {'✅' if implementations['main_2.7.5'] else '❌'}")
    print(f"   Simple CLI: {'✅' if implementations['simple_cli'] else '❌'}")
    
    if not best_impl:
        print("❌ No blockchain implementation available!")
        return 1
    
    print(f"\n🎯 Selected: {best_impl}")
    print("🛡️ JAI RAM SITA HANUMAN - ON THE STAR\n")
    
    # Parse arguments
    parser = argparse.ArgumentParser(description='ZION 2.7.5 Smart CLI')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Show blockchain statistics')

    # Mine command  
    mine_parser = subparsers.add_parser('mine', help='Mine blocks')
    mine_parser.add_argument('--address', '-a', required=True, help='Miner address')
    mine_parser.add_argument('--blocks', '-b', type=int, default=1, help='Number of blocks to mine')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # Route to appropriate implementation
    try:
        if best_impl == 'real_2.7.1':
            run_with_real_blockchain(args)
        elif best_impl == 'main_2.7.5':
            run_with_main_blockchain(args)
        elif best_impl == 'simple_cli':
            run_with_simple_cli(args)
    except Exception as e:
        print(f"❌ Error running command: {e}")
        return 1

if __name__ == "__main__":
    exit(main())