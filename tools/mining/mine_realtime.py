#!/usr/bin/env python3
"""
🔥 ZION Real-time Mining Launcher
Spustí Universal AI Miner s profesionálními SRBMiner-style metrikami

Usage:
    # GPU mining - Cosmic Harmony
    python3 mine_realtime.py --algo cosmic_harmony --mode gpu
    
    # CPU mining - RandomX
    python3 mine_realtime.py --algo randomx --mode cpu
    
    # Hybrid mining
    python3 mine_realtime.py --algo cosmic_harmony --mode hybrid
    
    # KawPow GPU mining
    python3 mine_realtime.py --algo kawpow --mode gpu
"""

import sys
import os
import argparse
import logging

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ai.zion_universal_miner import ZionUniversalMiner, MiningMode

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='🔥 ZION Universal AI Miner with Real-time Metrics',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--algo', '--algorithm',
        type=str,
        default='cosmic_harmony',
        choices=['cosmic_harmony', 'randomx', 'kawpow', 'yescrypt', 'autolykos2', 'ethash'],
        help='Mining algorithm (default: cosmic_harmony)'
    )
    
    parser.add_argument(
        '--mode',
        type=str,
        default='auto',
        choices=['cpu', 'gpu', 'hybrid', 'auto'],
        help='Mining mode (default: auto)'
    )
    
    parser.add_argument(
        '--pool',
        type=str,
        default='localhost:3333',
        help='Mining pool URL (default: localhost:3333)'
    )
    
    parser.add_argument(
        '--wallet',
        type=str,
        default='ZIONWallet123456789',
        help='Wallet address for payouts'
    )
    
    parser.add_argument(
        '--worker',
        type=str,
        default='zion-gpu-1',
        help='Worker name (default: zion-gpu-1)'
    )
    
    parser.add_argument(
        '--no-display',
        action='store_true',
        help='Disable real-time metrics display'
    )
    
    parser.add_argument(
        '--simulate',
        action='store_true',
        help='Enable simulation mode (for testing only)'
    )
    
    return parser.parse_args()


def main():
    """Main launcher"""
    args = parse_args()
    
    # Print banner
    print("=" * 100)
    print("🔥" * 50)
    print(" " * 30 + "ZION UNIVERSAL AI MINER")
    print(" " * 25 + "Real-time Professional Mining System")
    print("🔥" * 50)
    print("=" * 100)
    print()
    
    # Map mode string to enum
    mode_map = {
        'cpu': MiningMode.CPU_ONLY,
        'gpu': MiningMode.GPU_ONLY,
        'hybrid': MiningMode.HYBRID,
        'auto': MiningMode.AUTO
    }
    
    mode = mode_map.get(args.mode.lower(), MiningMode.AUTO)
    
    # Check for simulation warning
    if args.simulate:
        print("⚠️  WARNING: Simulation mode enabled - NO REAL MINING!")
        print("⚠️  This is for testing metrics display only.")
        print()
        import time
        time.sleep(3)
    
    # Initialize miner
    print(f"🔧 Initializing miner...")
    print(f"   Algorithm: {args.algo}")
    print(f"   Mode: {args.mode}")
    print(f"   Pool: {args.pool}")
    print(f"   Worker: {args.worker}")
    print()
    
    miner = ZionUniversalMiner(
        mode=mode,
        enable_realtime_display=not args.no_display
    )
    
    # Prepare pool URL
    pool_url = args.pool
    if not pool_url.startswith('stratum'):
        pool_url = f'stratum+tcp://{pool_url}'
    
    try:
        # Start mining
        print("🚀 Starting mining operations...")
        print()
        
        result = miner.start_mining(
            pool_url=pool_url,
            wallet_address=args.wallet,
            worker_name=args.worker,
            algorithm=args.algo
        )
        
        if not result['success']:
            print(f"❌ Failed to start mining: {result['message']}")
            return 1
        
        print("✅ Mining started successfully!")
        print()
        print("=" * 100)
        print("Real-time metrics will appear below...")
        print("Press Ctrl+C to stop mining")
        print("=" * 100)
        print()
        
        # Keep running until interrupted
        import time
        while miner.is_mining:
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("\n\n⏹️  Shutdown requested by user...")
        
    except Exception as e:
        logger.error(f"Mining error: {e}", exc_info=True)
        return 1
    
    finally:
        # Stop mining
        print("\n🛑 Stopping mining operations...")
        result = miner.stop_mining()
        
        if result['success']:
            print("✅ Mining stopped cleanly")
        else:
            print(f"⚠️  Warning during shutdown: {result['message']}")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
