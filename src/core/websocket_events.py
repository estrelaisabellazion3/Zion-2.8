#!/usr/bin/env python3
"""
ZION WebSocket Event Streamer
Real-time události pro mining pool (block found, payments, atd.)
"""
import asyncio
import json
import logging
import websockets
from typing import Set, Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class PoolEventStreamer:
    """WebSocket streamer pro real-time události"""
    
    def __init__(self, host: str = '0.0.0.0', port: int = 8765):
        self.host = host
        self.port = port
        self.clients: Set[websockets.WebSocketServerProtocol] = set()
        self.server = None
        
    async def start(self):
        """Spustit WebSocket server"""
        self.server = await websockets.serve(
            self.handle_client,
            self.host,
            self.port
        )
        logger.info(f"📡 WebSocket server started on ws://{self.host}:{self.port}")
        
    async def stop(self):
        """Zastavit WebSocket server"""
        if self.server:
            self.server.close()
            await self.server.wait_closed()
            logger.info("📡 WebSocket server stopped")
    
    async def handle_client(self, websocket, path):
        """Zpracovat připojení klienta"""
        self.clients.add(websocket)
        logger.info(f"🔌 Client connected: {websocket.remote_address}")
        
        try:
            # Poslat welcome zprávu
            await websocket.send(json.dumps({
                'type': 'connected',
                'timestamp': datetime.now().isoformat(),
                'message': 'Connected to ZION Pool Events'
            }))
            
            # Držet spojení
            async for message in websocket:
                # Klient může poslat "ping" pro keep-alive
                if message == 'ping':
                    await websocket.send('pong')
                    
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            self.clients.remove(websocket)
            logger.info(f"🔌 Client disconnected: {websocket.remote_address}")
    
    async def broadcast_event(self, event_type: str, data: Dict[Any, Any]):
        """Odeslat událost všem připojeným klientům"""
        if not self.clients:
            return
        
        event = {
            'type': event_type,
            'timestamp': datetime.now().isoformat(),
            'data': data
        }
        
        message = json.dumps(event)
        
        # Odeslat všem klientům
        disconnected = set()
        for client in self.clients:
            try:
                await client.send(message)
            except websockets.exceptions.ConnectionClosed:
                disconnected.add(client)
        
        # Odstranit odpojené klienty
        self.clients -= disconnected
        
        logger.debug(f"📡 Broadcasted {event_type} to {len(self.clients)} clients")
    
    # === Pomocné metody pro konkrétní události ===
    
    async def on_block_found(self, block_data: Dict):
        """Událost: Blok nalezen"""
        await self.broadcast_event('block_found', {
            'height': block_data.get('height'),
            'hash': block_data.get('hash'),
            'reward': block_data.get('reward'),
            'difficulty': block_data.get('difficulty'),
            'miner': block_data.get('miner'),
            'algorithm': block_data.get('algorithm')
        })
        logger.info(f"🎉 Block found event broadcasted: #{block_data.get('height')}")
    
    async def on_payment_sent(self, payment_data: Dict):
        """Událost: Platba odeslána"""
        await self.broadcast_event('payment', {
            'address': payment_data.get('address'),
            'amount': payment_data.get('amount'),
            'tx_hash': payment_data.get('tx_hash'),
            'shares': payment_data.get('shares')
        })
        logger.info(f"💸 Payment event broadcasted: {payment_data.get('amount')} ZION")
    
    async def on_miner_connected(self, miner_data: Dict):
        """Událost: Miner připojen"""
        await self.broadcast_event('miner_connected', {
            'address': miner_data.get('address'),
            'ip': miner_data.get('ip'),
            'algorithm': miner_data.get('algorithm'),
            'difficulty': miner_data.get('difficulty')
        })
    
    async def on_miner_disconnected(self, miner_data: Dict):
        """Událost: Miner odpojen"""
        await self.broadcast_event('miner_disconnected', {
            'address': miner_data.get('address'),
            'ip': miner_data.get('ip'),
            'duration': miner_data.get('duration')
        })
    
    async def on_hashrate_update(self, hashrate_data: Dict):
        """Událost: Aktualizace hashrate"""
        await self.broadcast_event('hashrate_update', {
            'pool_hashrate': hashrate_data.get('pool_hashrate'),
            'active_miners': hashrate_data.get('active_miners'),
            'algorithms': hashrate_data.get('algorithms', {})
        })
    
    async def on_share_submitted(self, share_data: Dict):
        """Událost: Share přijat (pouze pro monitoring)"""
        # Odesíláme jen validní shares, ne každý
        if share_data.get('valid'):
            await self.broadcast_event('share', {
                'miner': share_data.get('miner'),
                'difficulty': share_data.get('difficulty'),
                'algorithm': share_data.get('algorithm')
            })

# === Příklad použití ===

async def example_usage():
    """Příklad jak použít WebSocket streamer"""
    streamer = PoolEventStreamer(port=8765)
    await streamer.start()
    
    # Simulace událostí
    await asyncio.sleep(1)
    
    # Block found
    await streamer.on_block_found({
        'height': 12345,
        'hash': 'abc123...',
        'reward': 50.0,
        'difficulty': 1000000,
        'miner': 'ZION1abc...',
        'algorithm': 'cosmic_harmony'
    })
    
    # Payment sent
    await streamer.on_payment_sent({
        'address': 'ZION1abc...',
        'amount': 25.5,
        'tx_hash': 'tx123...',
        'shares': 1000
    })
    
    # Hashrate update
    await streamer.on_hashrate_update({
        'pool_hashrate': 1500000,
        'active_miners': 42,
        'algorithms': {
            'cosmic_harmony': 800000,
            'yescrypt': 700000
        }
    })
    
    # Držet server běžící
    await asyncio.sleep(3600)
    await streamer.stop()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(example_usage())
