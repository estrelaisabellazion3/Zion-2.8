#!/usr/bin/env python3
"""
ZION 2.7.5 Simplified CLI
Rychlé řešení pro testování real blockchain funkcí
"""

import argparse
import sys
import time
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Try to import from existing structure
try:
    from core.real_blockchain import ZionRealBlockchain
    REAL_BLOCKCHAIN_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Real blockchain not available: {e}")
    REAL_BLOCKCHAIN_AVAILABLE = False

class ZionSimpleCLI:
    """Simplified ZION CLI for testing"""
    
    def __init__(self):
        self.blockchain = None
    
    def initialize_blockchain(self):
        """Initialize real blockchain"""
        if not REAL_BLOCKCHAIN_AVAILABLE:
            print("❌ Real blockchain components not available")
            return False
            
        if self.blockchain is None:
            try:
                db_path = os.path.join(os.path.dirname(__file__), 'zion_real_blockchain.db')
                self.blockchain = ZionRealBlockchain(db_file=db_path)
                print("🌟 ZION Real Blockchain initialized!")
                print(f"   Current blocks: {self.blockchain.get_block_count()}")
                return True
            except Exception as e:
                print(f"❌ Failed to initialize blockchain: {e}")
                return False
        return True
    
    def cmd_stats(self, args):
        """Show blockchain statistics"""
        if not self.initialize_blockchain():
            return
            
        stats = self.blockchain.get_blockchain_stats()
        latest_block = self.blockchain.get_latest_block()

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

    def cmd_mine(self, args):
        """Mine real blocks"""
        if not self.initialize_blockchain():
            return
            
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
                block = self.blockchain.mine_block(
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

        print("\n📊 REAL BLOCKCHAIN MINING COMPLETE:")
        print(f"   Blocks Attempted: {args.blocks}")
        print(f"   Blocks Mined: {blocks_mined}")
        print(f"   Success Rate: {blocks_mined/args.blocks*100:.1f}%")
        print(f"   Total Time: {duration:.1f}s")
        if blocks_mined > 0:
            print(f"   Avg Block Time: {duration/blocks_mined:.1f}s")

        # Show blockchain stats
        stats = self.blockchain.get_blockchain_stats()
        print("\n🌟 BLOCKCHAIN STATUS:")
        print(f"   Total Blocks: {stats['block_count']}")
        print(f"   Total Supply: {stats['total_supply']:,} atomic units")
        print(f"   Mempool: {stats['mempool_size']} transactions")

def main():
    """Main CLI entry point"""
    print("🌟 ZION 2.7.5 SIMPLIFIED CLI")
    print("🚀 Real Blockchain Testing")
    print("🛡️ JAI RAM SITA HANUMAN - ON THE STAR\n")
    
    parser = argparse.ArgumentParser(description='ZION 2.7.5 Simplified CLI')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Mining command
    mine_parser = subparsers.add_parser('mine', help='Mine real blocks')
    mine_parser.add_argument('--threads', '-t', type=int, default=1, help='Number of threads')
    mine_parser.add_argument('--blocks', '-b', type=int, default=1, help='Number of blocks to mine')
    mine_parser.add_argument('--address', '-a', required=True, help='Miner address')

    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Show blockchain statistics')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    cli = ZionSimpleCLI()
    
    if args.command == 'mine':
        cli.cmd_mine(args)
    elif args.command == 'stats':
        cli.cmd_stats(args)

if __name__ == "__main__":
    main()