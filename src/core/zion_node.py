#!/usr/bin/env python3
"""
ZION 2.8.3 Terra Nova - Production Node
Kombinuje skutečný blockchain s standalone RPC serverem
"""

import sys
import os
import time
import argparse
from pathlib import Path

# Přidání cesty k modulu
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Import standalone RPC serveru
from standalone_rpc_server import StandaloneRPCServer

# Import blockchainu - použití exec pro obejití import problémů
blockchain_file = os.path.join(current_dir, "new_zion_blockchain.py")
if not os.path.exists(blockchain_file):
    print(f"❌ Error: {blockchain_file} not found")
    sys.exit(1)

# Načtení modulu dynamicky
import importlib.util
spec = importlib.util.spec_from_file_location("new_zion_blockchain", blockchain_file)
if not spec or not spec.loader:
    print(f"❌ Error: Cannot load blockchain module")
    sys.exit(1)

blockchain_module = importlib.util.module_from_spec(spec)
sys.modules['new_zion_blockchain'] = blockchain_module
spec.loader.exec_module(blockchain_module)
NewZionBlockchain = blockchain_module.NewZionBlockchain


def main():
    """Hlavní funkce - spuštění ZION node s blockchainem a RPC serverem"""
    
    parser = argparse.ArgumentParser(description='ZION 2.8.3 Terra Nova Production Node')
    parser.add_argument('--port', type=int, default=8332, help='RPC port (default: 8332)')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind (default: 0.0.0.0)')
    parser.add_argument('--testnet', action='store_true', help='Run in testnet mode')
    parser.add_argument('--regtest', action='store_true', help='Run in regtest mode')
    parser.add_argument('--datadir', type=str, help='Data directory for blockchain')
    parser.add_argument('--no-p2p', action='store_true', help='Disable P2P network')
    parser.add_argument('--standalone', action='store_true', help='Run without blockchain (standalone mode)')
    args = parser.parse_args()
    
    # Určení sítě
    if args.regtest:
        network = "regtest"
    elif args.testnet:
        network = "testnet"
    else:
        network = "mainnet"
    
    print("=" * 70)
    print("🌟 ZION 2.8.3 Terra Nova - Production Node")
    print("=" * 70)
    print(f"Network: {network.upper()}")
    print(f"RPC Server: {args.host}:{args.port}")
    print(f"P2P Network: {'Disabled' if args.no_p2p else 'Enabled'}")
    print("=" * 70)
    
    blockchain = None
    
    if not args.standalone:
        try:
            print("\n📦 Initializing blockchain...")
            
            # Nastavení datadiru
            if args.datadir:
                db_file = os.path.join(args.datadir, f'zion_{network}_blockchain.db')
            else:
                db_file = f'zion_{network}_blockchain.db'
            
            # Vytvoření blockchain instance
            blockchain = NewZionBlockchain(
                db_file=db_file,
                enable_p2p=not args.no_p2p,
                enable_rpc=False,  # RPC spustíme samostatně
                network=network
            )
            
            print(f"✅ Blockchain initialized")
            print(f"   Blocks: {len(blockchain.blocks)}")
            print(f"   Total Supply: {blockchain.get_total_supply():,.2f} ZION")
            print(f"   Database: {db_file}")
            
            # Spuštění P2P sítě pokud není zakázána
            if blockchain.p2p_network and not args.no_p2p:
                print(f"🌐 Starting P2P network...")
                # P2P se spustí automaticky v konstruktoru
                print(f"   P2P Port: {blockchain.p2p_network.port if hasattr(blockchain.p2p_network, 'port') else 'N/A'}")
            
        except Exception as e:
            print(f"⚠️  Warning: Could not initialize blockchain: {e}")
            print(f"   Running in standalone mode without blockchain")
            blockchain = None
    else:
        print("\n🔧 Running in standalone mode (no blockchain)")
    
    # Spuštění RPC serveru
    print(f"\n🚀 Starting RPC Server...")
    rpc_server = StandaloneRPCServer(
        blockchain=blockchain,
        host=args.host,
        port=args.port
    )
    rpc_server.start()
    
    print("\n" + "=" * 70)
    print("✅ ZION Node is running!")
    print("=" * 70)
    
    if blockchain:
        print(f"📊 Blockchain Status:")
        print(f"   - Blocks: {len(blockchain.blocks)}")
        print(f"   - Difficulty: {blockchain.mining_difficulty}")
        print(f"   - Pending Transactions: {len(blockchain.pending_transactions)}")
        print(f"   - Total Supply: {blockchain.get_total_supply():,.2f} ZION")
    
    print(f"\n🌐 RPC Endpoints:")
    print(f"   - http://{args.host}:{args.port}/          (Blockchain info)")
    print(f"   - http://{args.host}:{args.port}/health    (Health check)")
    
    print("\n💡 Press Ctrl+C to stop the node")
    print("=" * 70)
    
    # Hlavní smyčka - monitoring a statistiky
    try:
        counter = 0
        while True:
            time.sleep(60)  # Update každou minutu
            counter += 1
            
            if blockchain and counter % 5 == 0:  # Každých 5 minut
                print(f"\n📊 Status Update [{time.strftime('%Y-%m-%d %H:%M:%S')}]")
                print(f"   Blocks: {len(blockchain.blocks)}")
                print(f"   Supply: {blockchain.get_total_supply():,.2f} ZION")
                print(f"   Mempool: {len(blockchain.pending_transactions)} txs")
                
    except KeyboardInterrupt:
        print("\n\n" + "=" * 70)
        print("🛑 Shutting down ZION Node...")
        print("=" * 70)
        
        # Zastavení RPC serveru
        rpc_server.stop()
        
        # Zastavení P2P sítě
        if blockchain and blockchain.p2p_network:
            try:
                print("🌐 Stopping P2P network...")
                # Zde by byla logika pro zastavení P2P
            except Exception as e:
                print(f"⚠️  Warning during P2P shutdown: {e}")
        
        # Zastavení blockchain RPC serveru (pokud existuje)
        if blockchain and hasattr(blockchain, 'rpc_server') and blockchain.rpc_server:
            try:
                print("📡 Stopping blockchain RPC server...")
                blockchain.stop_rpc_server()
            except Exception as e:
                print(f"⚠️  Warning during blockchain RPC shutdown: {e}")
        
        print("✅ ZION Node stopped successfully")
        print("👋 Goodbye!")
        
    except Exception as e:
        print(f"\n❌ Critical Error: {e}")
        import traceback
        traceback.print_exc()
        
        # Pokus o graceful shutdown
        try:
            rpc_server.stop()
        except:
            pass
        
        sys.exit(1)


if __name__ == "__main__":
    main()
