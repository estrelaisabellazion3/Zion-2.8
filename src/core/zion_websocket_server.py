#!/usr/bin/env python3
"""
ZION WebSocket Server
Real-time WebSocket and Socket.IO server for ZION ecosystem
Provides live updates for mining stats, system metrics, and AI data
"""

import asyncio
import json
import logging
import threading
import time
from typing import Dict, Any, Optional
import websockets
from datetime import datetime

# Optional Socket.IO support
try:
    import socketio
    SOCKETIO_AVAILABLE = True
except ImportError:
    SOCKETIO_AVAILABLE = False
    socketio = None

logger = logging.getLogger(__name__)

class ZIONWebSocketServer:
    """WebSocket server for real-time ZION data streaming"""

    def __init__(self, host: str = '0.0.0.0', port: int = 8080):
        self.host = host
        self.port = port
        self.clients = set()
        self.server = None
        self.running = False

        # Metrics storage
        self.system_metrics = {}
        self.mining_metrics = {}
        self.ai_metrics = {}

        # Broadcast thread
        self.broadcast_thread = None
        self.broadcast_interval = 1.0  # seconds

    async def start(self):
        """Start WebSocket server"""
        if self.running:
            return

        self.running = True
        self.server = await websockets.serve(
            self._handle_client,
            self.host,
            self.port
        )

        # Start broadcast thread
        self.broadcast_thread = threading.Thread(target=self._broadcast_loop, daemon=True)
        self.broadcast_thread.start()

        logger.info(f"🌐 WebSocket server started on ws://{self.host}:{self.port}")

    def stop(self):
        """Stop WebSocket server"""
        self.running = False

        if self.server:
            self.server.close()

        if self.broadcast_thread:
            self.broadcast_thread.join(timeout=2.0)

        logger.info("🌐 WebSocket server stopped")

    async def _handle_client(self, websocket, path):
        """Handle WebSocket client connection"""
        self.clients.add(websocket)
        client_addr = websocket.remote_address
        logger.info(f"🔌 Client connected: {client_addr}")

        try:
            # Send welcome message with current metrics
            await self._send_welcome_message(websocket)

            # Handle client messages
            async for message in websocket:
                try:
                    data = json.loads(message)
                    await self._handle_message(websocket, data)
                except json.JSONDecodeError:
                    await websocket.send(json.dumps({
                        'type': 'error',
                        'message': 'Invalid JSON format'
                    }))

        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            self.clients.discard(websocket)
            logger.info(f"🔌 Client disconnected: {client_addr}")

    async def _send_welcome_message(self, websocket):
        """Send welcome message with current state"""
        welcome_data = {
            'type': 'welcome',
            'timestamp': datetime.now().isoformat(),
            'server': 'ZION WebSocket Server',
            'version': '2.8.2',
            'metrics': {
                'system': self.system_metrics,
                'mining': self.mining_metrics,
                'ai': self.ai_metrics
            }
        }
        await websocket.send(json.dumps(welcome_data))

    async def _handle_message(self, websocket, data):
        """Handle incoming client message"""
        msg_type = data.get('type', '')

        if msg_type == 'ping':
            await websocket.send(json.dumps({'type': 'pong'}))
        elif msg_type == 'subscribe':
            # Handle subscription requests
            channels = data.get('channels', [])
            await websocket.send(json.dumps({
                'type': 'subscribed',
                'channels': channels
            }))
        elif msg_type == 'get_metrics':
            # Send current metrics
            await websocket.send(json.dumps({
                'type': 'metrics',
                'timestamp': datetime.now().isoformat(),
                'data': {
                    'system': self.system_metrics,
                    'mining': self.mining_metrics,
                    'ai': self.ai_metrics
                }
            }))

    def _broadcast_loop(self):
        """Broadcast metrics to all clients"""
        while self.running:
            try:
                if self.clients:
                    self._broadcast_metrics()
                time.sleep(self.broadcast_interval)
            except Exception as e:
                logger.error(f"Broadcast error: {e}")
                time.sleep(1.0)

    def _broadcast_metrics(self):
        """Broadcast current metrics to all connected clients"""
        if not self.clients:
            return

        message = {
            'type': 'metrics_update',
            'timestamp': datetime.now().isoformat(),
            'data': {
                'system': self.system_metrics,
                'mining': self.mining_metrics,
                'ai': self.ai_metrics
            }
        }

        message_json = json.dumps(message)

        # Send to all clients (remove disconnected ones)
        disconnected = set()
        for client in self.clients:
            try:
                asyncio.run(client.send(message_json))
            except websockets.exceptions.ConnectionClosed:
                disconnected.add(client)

        self.clients -= disconnected

        if disconnected:
            logger.debug(f"Removed {len(disconnected)} disconnected clients")

    # === Metrics Update Methods ===

    def update_system_metrics(self, cpu_usage: float, memory_usage: float,
                            disk_usage: float, network_rx: float,
                            network_tx: float, uptime: float):
        """Update system metrics"""
        self.system_metrics.update({
            'cpu_usage': cpu_usage,
            'memory_usage': memory_usage,
            'disk_usage': disk_usage,
            'network_rx': network_rx,
            'network_tx': network_tx,
            'uptime': uptime,
            'timestamp': datetime.now().isoformat()
        })

    def update_mining_metrics(self, hashrate: float, shares_submitted: int = 0,
                            shares_accepted: int = 0, shares_rejected: int = 0,
                            blocks_found: int = 0, difficulty: float = 0.0,
                            temperature: float = 0.0, power_consumption: float = 0.0,
                            efficiency: float = 0.0):
        """Update mining metrics"""
        self.mining_metrics.update({
            'hashrate': hashrate,
            'shares_submitted': shares_submitted,
            'shares_accepted': shares_accepted,
            'shares_rejected': shares_rejected,
            'blocks_found': blocks_found,
            'difficulty': difficulty,
            'temperature': temperature,
            'power_consumption': power_consumption,
            'efficiency': efficiency,
            'timestamp': datetime.now().isoformat()
        })

    def update_ai_metrics(self, active_models: int = 0, predictions_made: int = 0,
                        optimization_cycles: int = 0, consciousness_level: float = 0.0,
                        rize_energy: float = 0.0):
        """Update AI metrics"""
        self.ai_metrics.update({
            'active_models': active_models,
            'predictions_made': predictions_made,
            'optimization_cycles': optimization_cycles,
            'consciousness_level': consciousness_level,
            'rize_energy': rize_energy,
            'timestamp': datetime.now().isoformat()
        })

    # === Event Broadcasting Methods ===

    async def broadcast_event(self, event_type: str, event_data: Dict[str, Any]):
        """Broadcast custom event to all clients"""
        if not self.clients:
            return

        message = {
            'type': 'event',
            'event_type': event_type,
            'timestamp': datetime.now().isoformat(),
            'data': event_data
        }

        message_json = json.dumps(message)

        disconnected = set()
        for client in self.clients:
            try:
                await client.send(message_json)
            except websockets.exceptions.ConnectionClosed:
                disconnected.add(client)

        self.clients -= disconnected

        logger.debug(f"📡 Broadcasted {event_type} event to {len(self.clients)} clients")

    # === Utility Methods ===

    def get_client_count(self) -> int:
        """Get number of connected clients"""
        return len(self.clients)

    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get summary of all current metrics"""
        return {
            'system': self.system_metrics,
            'mining': self.mining_metrics,
            'ai': self.ai_metrics,
            'clients_connected': self.get_client_count(),
            'server_running': self.running
        }


class ZIONSocketIOServer:
    """Socket.IO server for real-time ZION data streaming"""

    def __init__(self, host: str = '0.0.0.0', port: int = 8081):
        if not SOCKETIO_AVAILABLE:
            raise ImportError("Socket.IO not available. Install with: pip install python-socketio")

        self.host = host
        self.port = port
        self.sio = socketio.AsyncServer(async_mode='aiohttp', cors_allowed_origins='*')
        self.app = None
        self.site = None
        self.running = False

        # Metrics storage
        self.system_metrics = {}
        self.mining_metrics = {}
        self.ai_metrics = {}

        self._setup_events()

    def _setup_events(self):
        """Setup Socket.IO event handlers"""

        @self.sio.event
        async def connect(sid, environ):
            logger.info(f"🔌 Socket.IO client connected: {sid}")
            # Send welcome data
            await self.sio.emit('welcome', {
                'server': 'ZION Socket.IO Server',
                'version': '2.8.2',
                'timestamp': datetime.now().isoformat()
            }, to=sid)

        @self.sio.event
        async def disconnect(sid):
            logger.info(f"🔌 Socket.IO client disconnected: {sid}")

        @self.sio.event
        async def subscribe(sid, data):
            """Handle subscription requests"""
            channels = data.get('channels', [])
            logger.info(f"📡 Client {sid} subscribed to: {channels}")
            await self.sio.emit('subscribed', {'channels': channels}, to=sid)

        @self.sio.event
        async def get_metrics(sid):
            """Send current metrics"""
            await self.sio.emit('metrics', {
                'timestamp': datetime.now().isoformat(),
                'data': {
                    'system': self.system_metrics,
                    'mining': self.mining_metrics,
                    'ai': self.ai_metrics
                }
            }, to=sid)

        @self.sio.event
        async def ping(sid):
            """Handle ping"""
            await self.sio.emit('pong', to=sid)

    async def start(self):
        """Start Socket.IO server"""
        if self.running:
            return

        from aiohttp import web

        self.app = web.Application()
        self.sio.attach(self.app)

        # Add CORS middleware
        self.app.middlewares.append(self._cors_middleware)

        from aiohttp.web_runner import AppRunner, TCPSite

        runner = AppRunner(self.app)
        await runner.setup()
        self.site = TCPSite(runner, self.host, self.port)
        await self.site.start()

        self.running = True
        logger.info(f"🌐 Socket.IO server started on http://{self.host}:{self.port}")

    async def _cors_middleware(self, app, handler):
        """CORS middleware"""
        async def middleware_handler(request):
            response = await handler(request)
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
            return response
        return middleware_handler

    def stop(self):
        """Stop Socket.IO server"""
        self.running = False
        if self.site:
            asyncio.run(self.site.stop())
        logger.info("🌐 Socket.IO server stopped")

    def run(self):
        """Run Socket.IO server (blocking)"""
        asyncio.run(self.start())

        try:
            asyncio.get_event_loop().run_forever()
        except KeyboardInterrupt:
            self.stop()

    # === Metrics Update Methods (same as WebSocket server) ===

    def update_system_metrics(self, cpu_usage: float, memory_usage: float,
                            disk_usage: float, network_rx: float,
                            network_tx: float, uptime: float):
        """Update system metrics"""
        self.system_metrics.update({
            'cpu_usage': cpu_usage,
            'memory_usage': memory_usage,
            'disk_usage': disk_usage,
            'network_rx': network_rx,
            'network_tx': network_tx,
            'uptime': uptime,
            'timestamp': datetime.now().isoformat()
        })

    def update_mining_metrics(self, hashrate: float, shares_submitted: int = 0,
                            shares_accepted: int = 0, shares_rejected: int = 0,
                            blocks_found: int = 0, difficulty: float = 0.0,
                            temperature: float = 0.0, power_consumption: float = 0.0,
                            efficiency: float = 0.0):
        """Update mining metrics"""
        self.mining_metrics.update({
            'hashrate': hashrate,
            'shares_submitted': shares_submitted,
            'shares_accepted': shares_accepted,
            'shares_rejected': shares_rejected,
            'blocks_found': blocks_found,
            'difficulty': difficulty,
            'temperature': temperature,
            'power_consumption': power_consumption,
            'efficiency': efficiency,
            'timestamp': datetime.now().isoformat()
        })

    def update_ai_metrics(self, active_models: int = 0, predictions_made: int = 0,
                        optimization_cycles: int = 0, consciousness_level: float = 0.0,
                        rize_energy: float = 0.0):
        """Update AI metrics"""
        self.ai_metrics.update({
            'active_models': active_models,
            'predictions_made': predictions_made,
            'optimization_cycles': optimization_cycles,
            'consciousness_level': consciousness_level,
            'rize_energy': rize_energy,
            'timestamp': datetime.now().isoformat()
        })

    # === Broadcasting Methods ===

    async def broadcast_metrics(self):
        """Broadcast current metrics to all clients"""
        await self.sio.emit('metrics_update', {
            'timestamp': datetime.now().isoformat(),
            'data': {
                'system': self.system_metrics,
                'mining': self.mining_metrics,
                'ai': self.ai_metrics
            }
        })

    async def broadcast_event(self, event_type: str, event_data: Dict[str, Any]):
        """Broadcast custom event to all clients"""
        await self.sio.emit('event', {
            'event_type': event_type,
            'timestamp': datetime.now().isoformat(),
            'data': event_data
        })


# === Standalone Server Functions ===

async def run_websocket_server(host='0.0.0.0', port=8080):
    """Run standalone WebSocket server"""
    server = ZIONWebSocketServer(host=host, port=port)
    await server.start()

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        server.stop()

async def run_socketio_server(host='0.0.0.0', port=8081):
    """Run standalone Socket.IO server"""
    if not SOCKETIO_AVAILABLE:
        logger.error("Socket.IO not available. Install with: pip install python-socketio")
        return

    server = ZIONSocketIOServer(host=host, port=port)
    await server.start()

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        server.stop()

if __name__ == '__main__':
    import sys

    logging.basicConfig(level=logging.INFO)

    if len(sys.argv) > 1 and sys.argv[1] == 'socketio':
        print("🌐 Starting Socket.IO server...")
        asyncio.run(run_socketio_server())
    else:
        print("🌐 Starting WebSocket server...")
        asyncio.run(run_websocket_server())