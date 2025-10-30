#!/usr/bin/env python3
"""
ZION Standalone RPC Server
Jednoduchý HTTP JSON-RPC server pro ZION blockchain bez závislostí
Inspirováno Bitcoin Core RPC implementací
"""

import json
import hashlib
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
import threading
import sqlite3
import os

class ZIONStandaloneRPC(BaseHTTPRequestHandler):
    """HTTP handler pro JSON-RPC požadavky"""
    
    def __init__(self, *args, blockchain=None, **kwargs):
        self.blockchain = blockchain
        super().__init__(*args, **kwargs)
    
    def do_POST(self):
        """Zpracování POST požadavků (JSON-RPC)"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            request = json.loads(post_data.decode('utf-8'))
            method = request.get('method', '')
            params = request.get('params', [])
            request_id = request.get('id', 1)
            
            # Zpracování RPC metod
            result = self._execute_method(method, params)
            
            response = {
                'result': result,
                'error': None,
                'id': request_id
            }
            
        except Exception as e:
            response = {
                'result': None,
                'error': {'code': -32603, 'message': str(e)},
                'id': request.get('id', 1) if 'request' in locals() else 1
            }
        
        self._send_response(response)
    
    def do_GET(self):
        """Zpracování GET požadavků (info endpoint)"""
        if self.path == '/':
            info = self._get_blockchain_info()
            self._send_response(info)
        elif self.path == '/health':
            self._send_response({'status': 'ok', 'timestamp': datetime.utcnow().isoformat()})
        elif self.path == '/metrics':
            metrics = self._get_metrics()
            self._send_response(metrics)
        elif self.path == '/dashboard':
            html = self._get_dashboard_html()
            self._send_html_response(html)
        elif self.path == '/api/stats':
            stats = self._get_detailed_stats()
            self._send_response(stats)
        else:
            self._send_response({'error': 'Not found'}, 404)
    
    def _execute_method(self, method: str, params: list):
        """Vykonání RPC metody"""
        
        # Mapping metod - podobně jako Bitcoin Core
        methods = {
            'getblockchaininfo': self._getblockchaininfo,
            'getblockcount': self._getblockcount,
            'getblock': self._getblock,
            'getbalance': self._getbalance,
            'sendtoaddress': self._sendtoaddress,
            'getnewaddress': self._getnewaddress,
            'getmininginfo': self._getmininginfo,
            'submitblock': self._submitblock,
            'getdifficulty': self._getdifficulty,
            'generate': self._generate,
            'generatetoaddress': self._generatetoaddress,
        }
        
        if method not in methods:
            raise ValueError(f"Method '{method}' not found")
        
        return methods[method](params)
    
    def _get_blockchain_info(self):
        """Základní info o blockchainu"""
        if not self.blockchain:
            return {
                'status': 'online',
                'version': 'ZION 2.8.3 Terra Nova',
                'network': 'regtest',
                'blocks': 0,
                'message': 'ZION Blockchain Node Running (Standalone Mode)'
            }
        
        return {
            'chain': self.blockchain.network,
            'blocks': len(self.blockchain.blocks),
            'bestblockhash': self.blockchain.blocks[-1]['hash'] if self.blockchain.blocks else None,
            'difficulty': self.blockchain.mining_difficulty,
            'mediantime': self._get_median_time(),
            'chainwork': self._get_chain_work(),
        }
    
    def _getblockchaininfo(self, params):
        """RPC: getblockchaininfo"""
        return self._get_blockchain_info()
    
    def _getblockcount(self, params):
        """RPC: getblockcount"""
        return len(self.blockchain.blocks) if self.blockchain else 0
    
    def _getblock(self, params):
        """RPC: getblock [blockhash|height]"""
        if not params:
            raise ValueError("Missing block hash or height")
        
        block_id = params[0]
        
        # Hledání podle výšky
        if isinstance(block_id, int):
            if 0 <= block_id < len(self.blockchain.blocks):
                return self.blockchain.blocks[block_id]
            raise ValueError(f"Block height {block_id} out of range")
        
        # Hledání podle hashe
        for block in self.blockchain.blocks:
            if block['hash'] == block_id:
                return block
        
        raise ValueError(f"Block not found: {block_id}")
    
    def _getbalance(self, params):
        """RPC: getbalance [address]"""
        if not params:
            # Celkový balance všech adres
            return sum(self.blockchain.balances.values()) if self.blockchain else 0
        
        address = params[0]
        return self.blockchain.balances.get(address, 0) if self.blockchain else 0
    
    def _sendtoaddress(self, params):
        """RPC: sendtoaddress <address> <amount>"""
        if len(params) < 2:
            raise ValueError("Missing parameters: address, amount")
        
        to_address = params[0]
        amount = float(params[1])
        from_address = params[2] if len(params) > 2 else None
        
        if not self.blockchain:
            raise ValueError("Blockchain not initialized")
        
        # Vytvoření transakce
        tx = {
            'from': from_address or 'mining_pool',
            'to': to_address,
            'amount': amount,
            'timestamp': time.time(),
            'nonce': self.blockchain.nonces.get(from_address, 0) + 1
        }
        
        # Přidání do mempoolu
        self.blockchain.pending_transactions.append(tx)
        
        return hashlib.sha256(json.dumps(tx).encode()).hexdigest()
    
    def _getnewaddress(self, params):
        """RPC: getnewaddress - Generuje novou ZION adresu"""
        import secrets
        random_bytes = secrets.token_bytes(32)
        address = hashlib.sha256(random_bytes).hexdigest()
        return f"zion1{address[:40]}"
    
    def _getmininginfo(self, params):
        """RPC: getmininginfo"""
        if not self.blockchain:
            return {'difficulty': 4, 'blocks': 0, 'networkhashps': 0}
        
        return {
            'blocks': len(self.blockchain.blocks),
            'difficulty': self.blockchain.mining_difficulty,
            'networkhashps': self._estimate_network_hashrate(),
            'pooledtx': len(self.blockchain.pending_transactions),
            'chain': self.blockchain.network,
        }
    
    def _submitblock(self, params):
        """RPC: submitblock <blockdata>"""
        if not params:
            raise ValueError("Missing block data")
        
        block_data = params[0]
        
        if not self.blockchain:
            raise ValueError("Blockchain not initialized")
        
        # Validace a přidání bloku
        if isinstance(block_data, str):
            block_data = json.loads(block_data)
        
        # Zde by byla validace bloku
        self.blockchain.blocks.append(block_data)
        
        return block_data.get('hash', 'unknown')
    
    def _getdifficulty(self, params):
        """RPC: getdifficulty"""
        return self.blockchain.mining_difficulty if self.blockchain else 4
    
    def _generate(self, params):
        """RPC: generate <nblocks> - Vytěží n bloků"""
        if not self.blockchain:
            raise ValueError("Blockchain not initialized")
        
        nblocks = params[0] if params else 1
        address = self._getnewaddress([])
        
        return self._generatetoaddress([nblocks, address])
    
    def _generatetoaddress(self, params):
        """RPC: generatetoaddress <nblocks> <address> - Vytěží bloky na adresu"""
        if not self.blockchain:
            raise ValueError("Blockchain not initialized")
        
        if len(params) < 2:
            raise ValueError("Missing parameters: nblocks, address")
        
        nblocks = int(params[0])
        address = params[1]
        
        block_hashes = []
        
        for i in range(nblocks):
            block = self.blockchain.mine_block(address)
            if block:
                block_hashes.append(block['hash'])
                print(f"⛏️  Mined block {block['height']}: {block['hash'][:16]}... -> {address}")
        
        return block_hashes
    
    def _get_median_time(self):
        """Vypočítá median time past (MTP)"""
        if not self.blockchain or len(self.blockchain.blocks) < 11:
            return int(time.time())
        
        recent_times = [block['timestamp'] for block in self.blockchain.blocks[-11:]]
        recent_times.sort()
        return int(recent_times[len(recent_times) // 2])
    
    def _get_chain_work(self):
        """Celková práce blockchainu (zjednodušeno)"""
        if not self.blockchain:
            return "0x0"
        
        work = len(self.blockchain.blocks) * (2 ** self.blockchain.mining_difficulty)
        return hex(work)
    
    def _estimate_network_hashrate(self):
        """Odhad hash rate sítě"""
        if not self.blockchain or len(self.blockchain.blocks) < 2:
            return 0
        
        recent_blocks = self.blockchain.blocks[-10:]
        if len(recent_blocks) < 2:
            return 0
        
        time_diff = recent_blocks[-1]['timestamp'] - recent_blocks[0]['timestamp']
        if time_diff == 0:
            return 0
        
        blocks_per_second = len(recent_blocks) / time_diff
        hashes_per_block = 2 ** self.blockchain.mining_difficulty
        
        return blocks_per_second * hashes_per_block
    
    def _send_response(self, data, status=200):
        """Odeslání HTTP odpovědi"""
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())
    
    def _send_html_response(self, html, status=200):
        """Odeslání HTML odpovědi"""
        self.send_response(status)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def _get_metrics(self):
        """Prometheus-style metriky"""
        if not self.blockchain:
            return {
                'zion_blocks_total': 0,
                'zion_supply_total': 0,
                'zion_difficulty': 4,
                'zion_mempool_size': 0,
            }
        
        return {
            'zion_blocks_total': len(self.blockchain.blocks),
            'zion_supply_total': sum(self.blockchain.balances.values()),
            'zion_difficulty': self.blockchain.mining_difficulty,
            'zion_mempool_size': len(self.blockchain.pending_transactions),
            'zion_chainwork': int(self._get_chain_work(), 16),
            'zion_addresses_count': len(self.blockchain.balances),
        }
    
    def _get_detailed_stats(self):
        """Detailní statistiky pro API"""
        if not self.blockchain:
            return {
                'network': 'offline',
                'blocks': 0,
                'supply': 0,
            }
        
        blocks = self.blockchain.blocks
        recent_blocks = blocks[-10:] if len(blocks) > 10 else blocks
        
        # Výpočet průměrného block time
        avg_block_time = 0
        if len(recent_blocks) > 1:
            time_diff = recent_blocks[-1]['timestamp'] - recent_blocks[0]['timestamp']
            avg_block_time = time_diff / (len(recent_blocks) - 1)
        
        # Top balances
        top_balances = sorted(
            self.blockchain.balances.items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]
        
        return {
            'network': {
                'name': self.blockchain.network,
                'status': 'online',
                'uptime': time.time() - blocks[0]['timestamp'] if blocks else 0,
            },
            'blockchain': {
                'height': len(blocks) - 1,
                'blocks': len(blocks),
                'difficulty': self.blockchain.mining_difficulty,
                'chainwork': self._get_chain_work(),
                'best_block_hash': blocks[-1]['hash'] if blocks else None,
            },
            'supply': {
                'total': sum(self.blockchain.balances.values()),
                'circulating': sum(self.blockchain.balances.values()),
                'max_supply': 21000000,  # Bitcoin-like cap
                'inflation_rate': (self.blockchain.block_reward / sum(self.blockchain.balances.values()) * 100) if sum(self.blockchain.balances.values()) > 0 else 0,
            },
            'mining': {
                'difficulty': self.blockchain.mining_difficulty,
                'block_reward': self.blockchain.block_reward,
                'avg_block_time': round(avg_block_time, 2),
                'hashrate': self._estimate_network_hashrate(),
            },
            'mempool': {
                'size': len(self.blockchain.pending_transactions),
                'transactions': self.blockchain.pending_transactions[:5],  # First 5
            },
            'top_addresses': [
                {'address': addr[:20] + '...', 'balance': bal}
                for addr, bal in top_balances
            ],
            'recent_blocks': [
                {
                    'height': block['height'],
                    'hash': block['hash'][:16] + '...',
                    'timestamp': block['timestamp'],
                    'transactions': len(block['transactions']),
                }
                for block in recent_blocks[-5:]
            ],
        }
    
    def _get_dashboard_html(self):
        """HTML dashboard pro monitoring"""
        stats = self._get_detailed_stats()
        
        return f'''
<!DOCTYPE html>
<html lang="cs">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ZION 2.8.3 Terra Nova - Dashboard</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        .header {{
            text-align: center;
            color: white;
            margin-bottom: 30px;
            animation: fadeIn 1s;
        }}
        
        .header h1 {{
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        .header p {{
            font-size: 1.2em;
            opacity: 0.9;
        }}
        
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }}
        
        .card {{
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            animation: slideUp 0.5s;
        }}
        
        .card h2 {{
            color: #667eea;
            margin-bottom: 15px;
            font-size: 1.3em;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }}
        
        .stat {{
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid #eee;
        }}
        
        .stat:last-child {{
            border-bottom: none;
        }}
        
        .stat-label {{
            color: #666;
            font-weight: 500;
        }}
        
        .stat-value {{
            color: #333;
            font-weight: bold;
            font-size: 1.1em;
        }}
        
        .stat-value.highlight {{
            color: #667eea;
            font-size: 1.5em;
        }}
        
        .block-list {{
            max-height: 300px;
            overflow-y: auto;
        }}
        
        .block-item {{
            padding: 10px;
            margin: 5px 0;
            background: #f8f9fa;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }}
        
        .status-badge {{
            display: inline-block;
            padding: 5px 15px;
            background: #4caf50;
            color: white;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: bold;
        }}
        
        .status-badge.testnet {{
            background: #ff9800;
        }}
        
        .info-banner {{
            background: #2196F3;
            color: white;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            text-align: center;
        }}
        
        .info-banner a {{
            color: white;
            font-weight: bold;
            text-decoration: underline;
        }}
        
        .footer {{
            text-align: center;
            color: white;
            margin-top: 30px;
            opacity: 0.8;
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; }}
            to {{ opacity: 1; }}
        }}
        
        @keyframes slideUp {{
            from {{
                opacity: 0;
                transform: translateY(20px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        .refresh-btn {{
            background: #667eea;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1em;
            margin: 10px 0;
            transition: background 0.3s;
        }}
        
        .refresh-btn:hover {{
            background: #5568d3;
        }}
        
        .auto-refresh {{
            color: #4caf50;
            font-size: 0.9em;
            margin-left: 10px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌟 ZION 2.8.3 Terra Nova</h1>
            <p>Blockchain Explorer & Metrics Dashboard</p>
            <p><span class="status-badge {'testnet' if stats['network']['name'] == 'testnet' else ''}">● {stats['network']['name'].upper()}</span> <span class="auto-refresh" id="refreshTimer">Auto-refresh: 10s</span></p>
            <button class="refresh-btn" onclick="location.reload()">🔄 Refresh Now</button>
        </div>
        
        {'<div class="info-banner">🔒 <strong>SSL Security:</strong> This site uses a self-signed certificate for testing. Your connection is encrypted but not verified by a certificate authority. This is normal for testnet deployments. <a href="https://zionterranova.com" target="_blank">Learn more</a></div>' if stats['network']['name'] == 'testnet' else ''}
        
        <div class="grid">
            <div class="card">
                <h2>📊 Network Status</h2>
                <div class="stat">
                    <span class="stat-label">Network</span>
                    <span class="stat-value">{stats['network']['name'].upper()}</span>
                </div>
                <div class="stat">
                    <span class="stat-label">Status</span>
                    <span class="stat-value" style="color: #4caf50;">● {stats['network']['status'].upper()}</span>
                </div>
                <div class="stat">
                    <span class="stat-label">Uptime</span>
                    <span class="stat-value">{int(stats['network']['uptime'] / 60)} minutes</span>
                </div>
            </div>
            
            <div class="card">
                <h2>⛓️ Blockchain</h2>
                <div class="stat">
                    <span class="stat-label">Height</span>
                    <span class="stat-value highlight">{stats['blockchain']['height']}</span>
                </div>
                <div class="stat">
                    <span class="stat-label">Total Blocks</span>
                    <span class="stat-value">{stats['blockchain']['blocks']}</span>
                </div>
                <div class="stat">
                    <span class="stat-label">Difficulty</span>
                    <span class="stat-value">{stats['blockchain']['difficulty']}</span>
                </div>
                <div class="stat">
                    <span class="stat-label">Chain Work</span>
                    <span class="stat-value">{stats['blockchain']['chainwork']}</span>
                </div>
            </div>
            
            <div class="card">
                <h2>💰 Supply</h2>
                <div class="stat">
                    <span class="stat-label">Total Supply</span>
                    <span class="stat-value highlight">{stats['supply']['total']:,.2f} ZION</span>
                </div>
                <div class="stat">
                    <span class="stat-label">Circulating</span>
                    <span class="stat-value">{stats['supply']['circulating']:,.2f} ZION</span>
                </div>
                <div class="stat">
                    <span class="stat-label">Max Supply</span>
                    <span class="stat-value">{stats['supply']['max_supply']:,} ZION</span>
                </div>
                <div class="stat">
                    <span class="stat-label">Inflation Rate</span>
                    <span class="stat-value">{stats['supply']['inflation_rate']:.2f}%</span>
                </div>
            </div>
            
            <div class="card">
                <h2>⛏️ Mining</h2>
                <div class="stat">
                    <span class="stat-label">Block Reward</span>
                    <span class="stat-value highlight">{stats['mining']['block_reward']} ZION</span>
                </div>
                <div class="stat">
                    <span class="stat-label">Avg Block Time</span>
                    <span class="stat-value">{stats['mining']['avg_block_time']}s</span>
                </div>
                <div class="stat">
                    <span class="stat-label">Hash Rate</span>
                    <span class="stat-value">{stats['mining']['hashrate']:,.0f} H/s</span>
                </div>
                <div class="stat">
                    <span class="stat-label">Difficulty</span>
                    <span class="stat-value">{stats['mining']['difficulty']}</span>
                </div>
            </div>
        </div>
        
        <div class="grid">
            <div class="card">
                <h2>🔄 Mempool</h2>
                <div class="stat">
                    <span class="stat-label">Pending Transactions</span>
                    <span class="stat-value">{stats['mempool']['size']}</span>
                </div>
            </div>
            
            <div class="card">
                <h2>🏆 Top Addresses</h2>
                <div class="block-list">
                    {"".join([f'<div class="block-item"><strong>{addr["address"]}</strong><br>Balance: {addr["balance"]:,.2f} ZION</div>' for addr in stats['top_addresses'][:5]])}
                </div>
            </div>
            
            <div class="card" style="grid-column: 1 / -1;">
                <h2>📦 Recent Blocks</h2>
                <div class="block-list">
                    {"".join([f'<div class="block-item"><strong>Block #{block["height"]}</strong> - {block["hash"]}<br>Transactions: {block["transactions"]} | Time: {datetime.fromtimestamp(block["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")}</div>' for block in reversed(stats['recent_blocks'])])}
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>🌟 ZION 2.8.3 Terra Nova | Powered by Blockchain Technology</p>
            <p>API Endpoints: <a href="/" style="color: white;">/</a> | <a href="/health" style="color: white;">/health</a> | <a href="/metrics" style="color: white;">/metrics</a> | <a href="/api/stats" style="color: white;">/api/stats</a></p>
        </div>
    </div>
    
    <script>
        // Auto-refresh každých 10 sekund
        let countdown = 10;
        setInterval(() => {{
            countdown--;
            if (countdown <= 0) {{
                location.reload();
            }}
            document.getElementById('refreshTimer').textContent = `Auto-refresh: ${{countdown}}s`;
        }}, 1000);
    </script>
</body>
</html>
        '''
    
    def log_message(self, format, *args):
        """Logování požadavků"""
        print(f"[{datetime.utcnow().isoformat()}] {self.address_string()} - {format % args}")


class StandaloneRPCServer:
    """Standalone RPC server pro ZION blockchain"""
    
    def __init__(self, blockchain=None, host='0.0.0.0', port=8332):
        self.blockchain = blockchain
        self.host = host
        self.port = port
        self.server = None
        self.thread = None
    
    def start(self):
        """Spuštění RPC serveru"""
        
        # Vytvoření handleru s blockchain kontextem
        def handler(*args, **kwargs):
            return ZIONStandaloneRPC(*args, blockchain=self.blockchain, **kwargs)
        
        self.server = HTTPServer((self.host, self.port), handler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        
        print(f"🚀 ZION RPC Server started on {self.host}:{self.port}")
        print(f"📡 Endpoints:")
        print(f"   GET  http://{self.host}:{self.port}/        - Blockchain info")
        print(f"   GET  http://{self.host}:{self.port}/health  - Health check")
        print(f"   POST http://{self.host}:{self.port}/        - JSON-RPC methods")
    
    def stop(self):
        """Zastavení serveru"""
        if self.server:
            print("🛑 Stopping RPC server...")
            self.server.shutdown()
            self.thread.join(timeout=5)
            print("✅ RPC server stopped")


def main():
    """Hlavní funkce pro standalone režim"""
    import argparse
    
    parser = argparse.ArgumentParser(description='ZION Standalone RPC Server')
    parser.add_argument('--port', type=int, default=8332, help='RPC port (default: 8332)')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind (default: 0.0.0.0)')
    parser.add_argument('--testnet', action='store_true', help='Run in testnet mode')
    parser.add_argument('--with-blockchain', action='store_true', help='Run with simple blockchain')
    parser.add_argument('--datadir', type=str, help='Data directory for blockchain database')
    args = parser.parse_args()
    
    print("=" * 60)
    print("🌟 ZION 2.8.3 Terra Nova - Standalone RPC Server")
    print("=" * 60)
    print(f"Network: {'TESTNET' if args.testnet else 'MAINNET'}")
    
    blockchain = None
    
    if args.with_blockchain:
        try:
            from simple_blockchain import SimpleBlockchain
            
            network = 'testnet' if args.testnet else 'mainnet'
            db_file = f'zion_{network}_blockchain.db'
            
            if args.datadir:
                import os
                db_file = os.path.join(args.datadir, db_file)
            
            print(f"Mode: With SimpleBlockchain")
            print(f"Database: {db_file}")
            
            blockchain = SimpleBlockchain(db_file=db_file, network=network)
            
            print(f"✅ Blockchain loaded: {len(blockchain.blocks)} blocks")
            print(f"💰 Total Supply: {blockchain.get_total_supply():,.2f} ZION")
            
        except Exception as e:
            print(f"⚠️  Could not load blockchain: {e}")
            print("Running in standalone mode")
            blockchain = None
    else:
        print(f"Mode: Standalone (no blockchain instance)")
    
    print("=" * 60)
    
    # Spuštění bez blockchain instance (pro testing)
    server = StandaloneRPCServer(blockchain=blockchain, host=args.host, port=args.port)
    server.start()
    
    print("\n✅ Server ready. Press Ctrl+C to stop.")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down...")
        server.stop()
        print("👋 Goodbye!")


if __name__ == "__main__":
    main()
