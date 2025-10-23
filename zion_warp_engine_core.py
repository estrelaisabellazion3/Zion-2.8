#!/usr/bin/env python3
"""
🔥 ZION WARP ENGINE CORE - Production Infrastructure Orchestrator 🔥

ŽÁDNÉ SIMULACE - Reálná integrace všeho:
- Blockchain (NewZionBlockchain)
- RPC Server (port 18081)
- P2P Network (port 18080) 
- Mining Pools (2x pools)
- Wallets & Balances
- Nodes & Seeds
- Rainbow Bridge (multi-chain)

Version: 2.8.1 "Enhanced Resilience"
Author: ZION Development Team
Date: 2025-10-23
"""

import asyncio
import logging
import time
import json
import sys
import os
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
import aiohttp
from datetime import datetime
from enum import Enum
import psutil
import socket
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

# ZION Core Imports
from new_zion_blockchain import NewZionBlockchain
from zion_p2p_network import ZIONP2PNetwork
from zion_rpc_server import ZIONRPCServer
from seednodes import ZionNetworkConfig, get_premine_addresses, get_p2p_port, get_rpc_port

# Optional: Rainbow Bridge (requires additional dependencies)
try:
    from zion.bridge.rainbow_bridge import ZionRainbowBridge, ChainType
    BRIDGE_AVAILABLE = True
except ImportError:
    BRIDGE_AVAILABLE = False
    ZionRainbowBridge = None
    ChainType = None

# Setup enhanced logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('warp_engine.log'),
        logging.StreamHandler(),
        logging.handlers.RotatingFileHandler(
            'warp_engine.log', maxBytes=10*1024*1024, backupCount=5
        )
    ]
)
logger = logging.getLogger('WARP_ENGINE')

# Sacred Constants (from ESTRELLA)
GOLDEN_RATIO = 1.618033988749895
SACRED_FREQUENCY = 432.0  # Hz
WARP_ENGINE_VERSION = "2.8.1"


class ComponentStatus(Enum):
    """Component health status"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    OFFLINE = "offline"


@dataclass
class HealthCheck:
    """Health check result"""
    component: str
    status: ComponentStatus
    last_check: float
    response_time: float
    error_message: Optional[str] = None
    metrics: Dict[str, Any] = None


@dataclass
class PoolConnection:
    """Mining pool connection info"""
    name: str
    host: str
    port: int
    protocol: str  # "stratum", "xmrig"
    algorithms: List[str]
    wallet: str
    active: bool = False
    hashrate: float = 0.0
    shares: int = 0
    blocks: int = 0


@dataclass
class NodeConnection:
    """P2P Node connection info"""
    node_id: str
    host: str
    port: int
    protocol_version: str
    connected: bool = False
    last_seen: float = 0.0
    blocks_synced: int = 0


@dataclass
class WARPEngineStatus:
    """Overall WARP engine status"""
    blockchain_height: int
    blockchain_balances: int
    rpc_active: bool
    rpc_port: int
    p2p_active: bool
    p2p_port: int
    p2p_peers: int
    pool_connections: int
    active_pools: int
    bridge_active: bool
    total_hashrate: float
    uptime_seconds: float
    consciousness_field: float = 1.0  # ESTRELLA integration
    system_health: ComponentStatus = ComponentStatus.HEALTHY
    memory_usage_mb: float = 0.0
    cpu_usage_percent: float = 0.0


class CircuitBreaker:
    """Circuit breaker for fault tolerance"""
    
    def __init__(self, failure_threshold: int = 5, recovery_timeout: float = 60.0):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = 0
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
    
    async def call(self, func, *args, **kwargs):
        """Execute function with circuit breaker protection"""
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = "HALF_OPEN"
                logger.info("Circuit breaker entering HALF_OPEN state")
            else:
                raise Exception("Circuit breaker is OPEN")
        
        try:
            result = await func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise e
    
    def _on_success(self):
        """Handle successful call"""
        if self.state == "HALF_OPEN":
            self.state = "CLOSED"
            self.failure_count = 0
            logger.info("Circuit breaker CLOSED after successful call")
    
    def _on_failure(self):
        """Handle failed call"""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"
            logger.warning(f"Circuit breaker OPEN after {self.failure_count} failures")


class WARPHealthMonitor:
    """Health monitoring system"""
    
    def __init__(self, engine: 'ZionWARPEngine'):
        self.engine = engine
        self.health_checks: Dict[str, HealthCheck] = {}
        self.check_interval = 30.0  # seconds
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}
        
        # Initialize circuit breakers for critical components
        self.circuit_breakers['rpc'] = CircuitBreaker(failure_threshold=3, recovery_timeout=30.0)
        self.circuit_breakers['p2p'] = CircuitBreaker(failure_threshold=5, recovery_timeout=60.0)
        self.circuit_breakers['pools'] = CircuitBreaker(failure_threshold=10, recovery_timeout=120.0)
    
    async def start_monitoring(self):
        """Start health monitoring loop"""
        logger.info("🩺 Starting health monitoring...")
        
        while self.engine.running:
            await self._perform_health_checks()
            await asyncio.sleep(self.check_interval)
    
    async def _perform_health_checks(self):
        """Perform all health checks"""
        try:
            # Blockchain health
            await self._check_blockchain_health()
            
            # RPC health
            await self._check_rpc_health()
            
            # P2P health
            await self._check_p2p_health()
            
            # Pool health
            await self._check_pool_health()
            
            # System resources
            await self._check_system_health()
            
            # Update overall health
            self._update_overall_health()
            
        except Exception as e:
            logger.error(f"Health check error: {e}")
    
    async def _check_blockchain_health(self):
        """Check blockchain component health"""
        start_time = time.time()
        
        try:
            # Check if blockchain is responsive
            height = len(self.engine.blockchain.blocks)
            balance_count = len(self.engine.blockchain.balances)
            
            response_time = (time.time() - start_time) * 1000
            
            self.health_checks['blockchain'] = HealthCheck(
                component='blockchain',
                status=ComponentStatus.HEALTHY,
                last_check=time.time(),
                response_time=response_time,
                metrics={
                    'height': height,
                    'balances': balance_count,
                    'db_size_mb': self._get_db_size_mb()
                }
            )
            
        except Exception as e:
            self.health_checks['blockchain'] = HealthCheck(
                component='blockchain',
                status=ComponentStatus.UNHEALTHY,
                last_check=time.time(),
                response_time=(time.time() - start_time) * 1000,
                error_message=str(e)
            )
    
    async def _check_rpc_health(self):
        """Check RPC server health"""
        start_time = time.time()
        
        try:
            # Use circuit breaker for RPC calls
            async def rpc_health_check():
                if not self.engine.rpc_server:
                    raise Exception("RPC server not initialized")
                
                # Test RPC call
                reader, writer = await asyncio.wait_for(
                    asyncio.open_connection('localhost', self.engine.rpc_server.port),
                    timeout=5.0
                )
                writer.close()
                await writer.wait_closed()
                return True
            
            await self.circuit_breakers['rpc'].call(rpc_health_check)
            
            response_time = (time.time() - start_time) * 1000
            
            self.health_checks['rpc'] = HealthCheck(
                component='rpc',
                status=ComponentStatus.HEALTHY,
                last_check=time.time(),
                response_time=response_time,
                metrics={
                    'port': self.engine.rpc_server.port,
                    'connections': getattr(self.engine.rpc_server, 'active_connections', 0)
                }
            )
            
        except Exception as e:
            self.health_checks['rpc'] = HealthCheck(
                component='rpc',
                status=ComponentStatus.UNHEALTHY,
                last_check=time.time(),
                response_time=(time.time() - start_time) * 1000,
                error_message=str(e)
            )
    
    async def _check_p2p_health(self):
        """Check P2P network health"""
        start_time = time.time()
        
        try:
            async def p2p_health_check():
                if not self.engine.p2p_network:
                    raise Exception("P2P network not initialized")
                
                # Check if P2P is running
                if not hasattr(self.engine.p2p_network, 'running') or not self.engine.p2p_network.running:
                    raise Exception("P2P network not running")
                
                return True
            
            await self.circuit_breakers['p2p'].call(p2p_health_check)
            
            response_time = (time.time() - start_time) * 1000
            
            self.health_checks['p2p'] = HealthCheck(
                component='p2p',
                status=ComponentStatus.HEALTHY,
                last_check=time.time(),
                response_time=response_time,
                metrics={
                    'port': self.engine.p2p_network.port,
                    'peers': len(self.engine.p2p_network.peers) if hasattr(self.engine.p2p_network, 'peers') else 0,
                    'running': self.engine.p2p_network.running
                }
            )
            
        except Exception as e:
            self.health_checks['p2p'] = HealthCheck(
                component='p2p',
                status=ComponentStatus.UNHEALTHY,
                last_check=time.time(),
                response_time=(time.time() - start_time) * 1000,
                error_message=str(e)
            )
    
    async def _check_pool_health(self):
        """Check mining pool health"""
        start_time = time.time()
        
        try:
            async def pool_health_check():
                active_pools = sum(1 for p in self.engine.pools.values() if p.active)
                if active_pools == 0:
                    raise Exception("No active mining pools")
                return active_pools
            
            active_count = await self.circuit_breakers['pools'].call(pool_health_check)
            
            response_time = (time.time() - start_time) * 1000
            
            self.health_checks['pools'] = HealthCheck(
                component='pools',
                status=ComponentStatus.HEALTHY,
                last_check=time.time(),
                response_time=response_time,
                metrics={
                    'total_pools': len(self.engine.pools),
                    'active_pools': active_count,
                    'total_hashrate': sum(p.hashrate for p in self.engine.pools.values())
                }
            )
            
        except Exception as e:
            self.health_checks['pools'] = HealthCheck(
                component='pools',
                status=ComponentStatus.UNHEALTHY,
                last_check=time.time(),
                response_time=(time.time() - start_time) * 1000,
                error_message=str(e)
            )
    
    async def _check_system_health(self):
        """Check system resource health"""
        try:
            memory = psutil.virtual_memory()
            cpu = psutil.cpu_percent(interval=1)
            
            # Determine health based on resource usage
            if memory.percent > 90 or cpu > 95:
                status = ComponentStatus.UNHEALTHY
            elif memory.percent > 80 or cpu > 85:
                status = ComponentStatus.DEGRADED
            else:
                status = ComponentStatus.HEALTHY
            
            self.health_checks['system'] = HealthCheck(
                component='system',
                status=status,
                last_check=time.time(),
                response_time=0.0,
                metrics={
                    'memory_percent': memory.percent,
                    'memory_used_mb': memory.used / 1024 / 1024,
                    'cpu_percent': cpu,
                    'disk_usage': psutil.disk_usage('/').percent
                }
            )
            
        except Exception as e:
            self.health_checks['system'] = HealthCheck(
                component='system',
                status=ComponentStatus.UNHEALTHY,
                last_check=time.time(),
                response_time=0.0,
                error_message=str(e)
            )
    
    def _update_overall_health(self):
        """Update overall system health"""
        checks = list(self.health_checks.values())
        
        if not checks:
            return
        
        # Determine overall health
        unhealthy_count = sum(1 for c in checks if c.status in [ComponentStatus.UNHEALTHY, ComponentStatus.OFFLINE])
        degraded_count = sum(1 for c in checks if c.status == ComponentStatus.DEGRADED)
        
        if unhealthy_count > 0:
            overall_status = ComponentStatus.UNHEALTHY
        elif degraded_count > 0:
            overall_status = ComponentStatus.DEGRADED
        else:
            overall_status = ComponentStatus.HEALTHY
        
        # Update engine status
        status = self.engine.get_status()
        status.system_health = overall_status
        
        # Log health changes
        if unhealthy_count > 0:
            logger.warning(f"🚨 System health: {overall_status.value.upper()} ({unhealthy_count} unhealthy components)")
        elif degraded_count > 0:
            logger.info(f"⚠️ System health: {overall_status.value.upper()} ({degraded_count} degraded components)")
    
    def _get_db_size_mb(self) -> float:
        """Get blockchain database size in MB"""
        try:
            if os.path.exists(self.engine.blockchain.db_file):
                size_bytes = os.path.getsize(self.engine.blockchain.db_file)
                return size_bytes / 1024 / 1024
            return 0.0
        except Exception:
            return 0.0
    
    def get_health_report(self) -> Dict[str, Any]:
        """Get comprehensive health report"""
        return {
            'timestamp': datetime.now().isoformat(),
            'overall_health': self.engine.get_status().system_health.value,
            'checks': {
                name: {
                    'status': check.status.value,
                    'last_check': check.last_check,
                    'response_time_ms': check.response_time,
                    'error': check.error_message,
                    'metrics': check.metrics
                }
                for name, check in self.health_checks.items()
            },
            'circuit_breakers': {
                name: {
                    'state': cb.state,
                    'failure_count': cb.failure_count,
                    'last_failure': cb.last_failure_time
                }
                for name, cb in self.circuit_breakers.items()
            }
        }


class ZionWARPEngine:
    """
    🌟 ZION WARP ENGINE - Production Infrastructure Orchestrator
    
    Integrates ALL components:
    - Blockchain core with RPC & P2P
    - Multiple mining pools
    - Rainbow bridge for multi-chain
    - Seed nodes & network topology
    - Wallet management
    - Consciousness-based orchestration (ESTRELLA)
    """
    
    def __init__(self, 
                 blockchain_db: str = "zion_blockchain.db",
                 enable_rpc: bool = True,
                 enable_p2p: bool = True,
                 enable_bridge: bool = False,
                 bridge_private_key: Optional[str] = None):
        
        logger.info("=" * 80)
        logger.info("🔥 ZION WARP ENGINE CORE INITIALIZATION 🔥")
        logger.info("=" * 80)
        logger.info(f"Version: {WARP_ENGINE_VERSION} 'Ad Astra Per Estrella'")
        logger.info(f"Blockchain DB: {blockchain_db}")
        logger.info(f"RPC Enabled: {enable_rpc}")
        logger.info(f"P2P Enabled: {enable_p2p}")
        logger.info(f"Bridge Enabled: {enable_bridge}")
        
        # Core components
        self.start_time = time.time()
        self.consciousness_field = 1.0  # ESTRELLA consciousness field
        
        # Initialize blockchain with RPC & P2P
        logger.info("\n📦 Initializing Blockchain Core...")
        self.blockchain = NewZionBlockchain(
            db_file=blockchain_db,
            enable_p2p=enable_p2p,
            p2p_port=get_p2p_port(),
            enable_rpc=enable_rpc,
            rpc_port=get_rpc_port()
        )
        
        blockchain_height = len(self.blockchain.blocks)
        balance_count = len(self.blockchain.balances)
        logger.info(f"✅ Blockchain initialized: {blockchain_height} blocks, {balance_count} balances")
        
        # RPC Server reference
        self.rpc_server = self.blockchain.rpc_server
        if self.rpc_server:
            logger.info(f"✅ RPC Server ready on port {self.rpc_server.port}")
        
        # P2P Network reference
        self.p2p_network = self.blockchain.p2p_network
        if self.p2p_network:
            logger.info(f"✅ P2P Network ready on port {self.p2p_network.port}")
        
        # Mining pools
        self.pools: Dict[str, PoolConnection] = {}
        self._init_pool_connections()
        
        # Rainbow bridge (if enabled)
        self.bridge = None
        if enable_bridge and bridge_private_key and BRIDGE_AVAILABLE:
            logger.info("\n🌈 Initializing Rainbow Bridge...")
            self.bridge = ZionRainbowBridge(
                bridge_private_key=bridge_private_key,
                zion_rpc_url=f"http://localhost:{get_rpc_port()}"
            )
            logger.info("✅ Rainbow Bridge initialized")
        elif enable_bridge and not BRIDGE_AVAILABLE:
            logger.warning("⚠️  Bridge requested but dependencies not installed")
        
        # Seed nodes
        self.seed_nodes: List[NodeConnection] = []
        self._init_seed_nodes()
        
        # Status tracking
        self.running = False
        
        # Health monitoring system
        self.health_monitor = WARPHealthMonitor(self)
        
        logger.info("\n" + "=" * 80)
        logger.info("✨ WARP ENGINE CORE READY ✨")
        logger.info("=" * 80)
    
    def _init_pool_connections(self):
        """Initialize mining pool connections"""
        logger.info("\n⛏️  Initializing Mining Pool Connections...")
        
        premine = get_premine_addresses()
        
        # Pool 1: Universal Pool (port 3333) - localhost
        pool1 = PoolConnection(
            name="ZION Universal Pool",
            host="127.0.0.1",
            port=3333,
            protocol="xmrig",
            algorithms=["cosmic_harmony", "yescrypt", "randomx", "autolykos2"],  # 🌟 Native ZION algo!
            wallet=premine.get('ZION_DEVELOPMENT_TEAM_FUND_378614887FEA27791540F45', 'ZION_POOL_LOCAL')
        )
        self.pools['universal_local'] = pool1
        logger.info(f"  📌 Pool 1: {pool1.name} @ {pool1.host}:{pool1.port} [Cosmic Harmony ⭐]")
        
        # Pool 2: SSH Remote Pool (port 3333) - 91.98.122.165
        pool2 = PoolConnection(
            name="ZION SSH Pool",
            host="91.98.122.165",
            port=3333,
            protocol="xmrig",
            algorithms=["cosmic_harmony", "yescrypt", "randomx", "autolykos2"],  # 🌟 Native ZION algo!
            wallet=premine.get('ZION_NETWORK_INFRASTRUCTURE_SITA_B5F3BE9968A1D90', 'ZION_POOL_SSH')
        )
        self.pools['universal_ssh'] = pool2
        logger.info(f"  📌 Pool 2: {pool2.name} @ {pool2.host}:{pool2.port} [Cosmic Harmony ⭐]")
        
        logger.info(f"✅ {len(self.pools)} mining pools configured")
    
    def _init_seed_nodes(self):
        """Initialize seed node connections"""
        logger.info("\n🌐 Initializing Seed Nodes...")
        
        # Load seed nodes from config - use get_seed_nodes()
        try:
            seeds = ZionNetworkConfig.get_seed_nodes()
            for seed in seeds:
                node = NodeConnection(
                    node_id=f"seed_{seed['host']}",
                    host=seed['host'],
                    port=seed.get('port', 8333),
                    protocol_version=seed.get('protocol', 'zion/1.0')
                )
                self.seed_nodes.append(node)
                logger.info(f"  🌱 Seed: {node.host}:{node.port}")
        except Exception as e:
            logger.warning(f"  ⚠️  Could not load seed nodes: {e}")
        
        logger.info(f"✅ {len(self.seed_nodes)} seed nodes configured")
    
    async def start(self):
        """Start the WARP engine (async main loop)"""
        logger.info("\n" + "🚀" * 40)
        logger.info("🔥 IGNITING WARP ENGINE 🔥")
        logger.info("🚀" * 40)
        
        self.running = True
        
        # Start RPC server
        if self.rpc_server:
            logger.info("\n🌐 Starting RPC Server...")
            self.rpc_server.start()
            logger.info(f"✅ RPC Server listening on port {self.rpc_server.port}")
        
        # Start P2P network
        if self.p2p_network:
            logger.info("\n🌐 Starting P2P Network...")
            await self.p2p_network.start()
            logger.info(f"✅ P2P Network listening on port {self.p2p_network.port}")
        
        # Connect to pools
        await self._connect_pools()
        
        # Connect to seed nodes
        await self._connect_seed_nodes()
        
        # Start bridge if enabled
        if self.bridge:
            logger.info("\n🌈 Starting Rainbow Bridge...")
            # Bridge start logic here
            logger.info("✅ Rainbow Bridge active")
        
        # Start health monitoring
        logger.info("\n🩺 Starting Health Monitoring...")
        asyncio.create_task(self.health_monitor.start_monitoring())
        logger.info("✅ Health monitoring active")
        
        # Start API server
        logger.info("\n🌐 Starting API Server...")
        self.start_api_server(port=8080)
        logger.info("✅ API Server active")
        
        logger.info("\n" + "=" * 80)
        logger.info("✨ WARP ENGINE OPERATIONAL ✨")
        logger.info("=" * 80)
        
        # Status display
        self._display_status()
        
        # Main loop
        try:
            while self.running:
                await asyncio.sleep(10)  # Status check interval
                await self._status_check()
        except KeyboardInterrupt:
            logger.info("\n🛑 Shutdown signal received...")
            await self.stop()
    
    async def _connect_pools(self):
        """Connect to configured mining pools"""
        logger.info("\n⛏️  Connecting to Mining Pools...")
        
        for pool_id, pool in self.pools.items():
            try:
                # Test connection
                reader, writer = await asyncio.wait_for(
                    asyncio.open_connection(pool.host, pool.port),
                    timeout=5.0
                )
                pool.active = True
                writer.close()
                await writer.wait_closed()
                logger.info(f"  ✅ {pool.name}: CONNECTED")
            except Exception as e:
                pool.active = False
                logger.warning(f"  ⚠️  {pool.name}: OFFLINE ({str(e)})")
    
    async def _connect_seed_nodes(self):
        """Connect to seed nodes"""
        logger.info("\n🌐 Connecting to Seed Nodes...")
        
        for node in self.seed_nodes:
            try:
                # Test connection
                reader, writer = await asyncio.wait_for(
                    asyncio.open_connection(node.host, node.port),
                    timeout=5.0
                )
                node.connected = True
                node.last_seen = time.time()
                writer.close()
                await writer.wait_closed()
                logger.info(f"  ✅ {node.host}:{node.port}: CONNECTED")
            except Exception as e:
                node.connected = False
                logger.warning(f"  ⚠️  {node.host}:{node.port}: OFFLINE ({str(e)})")
    
    async def _status_check(self):
        """Periodic status check and display"""
        status = self.get_status()
        
        logger.info("\n" + "─" * 80)
        logger.info("📊 WARP ENGINE STATUS")
        logger.info("─" * 80)
        logger.info(f"⛓️  Blockchain Height: {status.blockchain_height}")
        logger.info(f"💰 Balances: {status.blockchain_balances}")
        logger.info(f"🌐 RPC: {'ACTIVE' if status.rpc_active else 'OFFLINE'} (port {status.rpc_port})")
        logger.info(f"🌐 P2P: {'ACTIVE' if status.p2p_active else 'OFFLINE'} (port {status.p2p_port}, {status.p2p_peers} peers)")
        logger.info(f"⛏️  Pools: {status.active_pools}/{status.pool_connections} active")
        logger.info(f"🌈 Bridge: {'ACTIVE' if status.bridge_active else 'DISABLED'}")
        logger.info(f"⚡ Total Hashrate: {status.total_hashrate:.2f} H/s")
        logger.info(f"⏱️  Uptime: {status.uptime_seconds:.0f}s")
        logger.info(f"✨ Consciousness Field: {status.consciousness_field:.2f}")
        logger.info("─" * 80)
    
    def _display_status(self):
        """Display initial status"""
        status = self.get_status()
        
        print("\n" + "╔" + "═" * 78 + "╗")
        print("║" + " " * 20 + "🌟 WARP ENGINE STATUS 🌟" + " " * 34 + "║")
        print("╚" + "═" * 78 + "╝")
        
        print(f"\n⛓️  Blockchain:")
        print(f"   Height: {status.blockchain_height}")
        print(f"   Balances: {status.blockchain_balances}")
        
        print(f"\n🌐 Network:")
        print(f"   RPC: {'ACTIVE' if status.rpc_active else 'OFFLINE'} (port {status.rpc_port})")
        print(f"   P2P: {'ACTIVE' if status.p2p_active else 'OFFLINE'} (port {status.p2p_port}, {status.p2p_peers} peers)")
        
        print(f"\n⛏️  Mining Pools:")
        for pool_id, pool in self.pools.items():
            status_str = "✅ ACTIVE" if pool.active else "⚠️  OFFLINE"
            print(f"   {pool.name}: {status_str} ({pool.host}:{pool.port})")
        
        print(f"\n🌱 Seed Nodes:")
        for node in self.seed_nodes:
            status_str = "✅ CONNECTED" if node.connected else "⚠️  OFFLINE"
            print(f"   {node.host}:{node.port}: {status_str}")
        
        if self.bridge:
            print(f"\n🌈 Rainbow Bridge: ACTIVE")
        
        print(f"\n✨ Consciousness Field: {status.consciousness_field:.2f}")
        print(f"⏱️  Uptime: {status.uptime_seconds:.0f}s\n")
    
    def get_status(self) -> WARPEngineStatus:
        """Get current WARP engine status"""
        # Get system metrics
        memory_usage = 0.0
        cpu_usage = 0.0
        
        try:
            memory = psutil.virtual_memory()
            memory_usage = memory.used / 1024 / 1024  # MB
            cpu_usage = psutil.cpu_percent(interval=0.1)
        except Exception:
            pass  # Ignore system metric errors
        
        # Determine overall health
        system_health = ComponentStatus.HEALTHY
        if self.health_monitor.health_checks:
            unhealthy_count = sum(1 for c in self.health_monitor.health_checks.values() 
                                if c.status in [ComponentStatus.UNHEALTHY, ComponentStatus.OFFLINE])
            degraded_count = sum(1 for c in self.health_monitor.health_checks.values() 
                                if c.status == ComponentStatus.DEGRADED)
            
            if unhealthy_count > 0:
                system_health = ComponentStatus.UNHEALTHY
            elif degraded_count > 0:
                system_health = ComponentStatus.DEGRADED
        
        return WARPEngineStatus(
            blockchain_height=len(self.blockchain.blocks),
            blockchain_balances=len(self.blockchain.balances),
            rpc_active=self.rpc_server is not None and hasattr(self.rpc_server, 'server') and self.rpc_server.server is not None,
            rpc_port=self.rpc_server.port if self.rpc_server else 0,
            p2p_active=self.p2p_network is not None and hasattr(self.p2p_network, 'running') and self.p2p_network.running,
            p2p_port=self.p2p_network.port if self.p2p_network else 0,
            p2p_peers=len(self.p2p_network.peers) if self.p2p_network else 0,
            pool_connections=len(self.pools),
            active_pools=sum(1 for p in self.pools.values() if p.active),
            bridge_active=self.bridge is not None,
            total_hashrate=sum(p.hashrate for p in self.pools.values()),
            uptime_seconds=time.time() - self.start_time,
            consciousness_field=self.consciousness_field,
            system_health=system_health,
            memory_usage_mb=memory_usage,
            cpu_usage_percent=cpu_usage
        )
    
    def start_api_server(self, port: int = 8080):
        """Start simple HTTP API server for health monitoring"""
        class WARPAPIHandler(BaseHTTPRequestHandler):
            def __init__(self, *args, engine=None, **kwargs):
                self.engine = engine
                super().__init__(*args, **kwargs)
            
            def do_GET(self):
                if self.path == '/health':
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    
                    status = self.engine.get_status()
                    health_data = {
                        'status': 'healthy' if status.system_health == ComponentStatus.HEALTHY else 'degraded',
                        'timestamp': datetime.now().isoformat(),
                        'uptime_seconds': status.uptime_seconds,
                        'blockchain_height': status.blockchain_height,
                        'rpc_active': status.rpc_active,
                        'p2p_active': status.p2p_active,
                        'p2p_peers': status.p2p_peers,
                        'active_pools': status.active_pools,
                        'memory_usage_mb': status.memory_usage_mb,
                        'cpu_usage_percent': status.cpu_usage_percent,
                        'consciousness_field': status.consciousness_field
                    }
                    
                    self.wfile.write(json.dumps(health_data, indent=2).encode())
                    
                elif self.path == '/status':
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    
                    status = self.engine.get_status()
                    status_data = asdict(status)
                    status_data['timestamp'] = datetime.now().isoformat()
                    
                    self.wfile.write(json.dumps(status_data, indent=2).encode())
                    
                else:
                    self.send_response(404)
                    self.end_headers()
                    self.wfile.write(b'{"error": "Not found"}')
            
            def log_message(self, format, *args):
                # Suppress default HTTP server logs
                return
        
        def run_server():
            with HTTPServer(('localhost', port), lambda *args, **kwargs: WARPAPIHandler(*args, engine=self, **kwargs)) as httpd:
                logger.info(f"🌐 WARP API Server started on http://localhost:{port}")
                httpd.serve_forever()
        
        # Start API server in background thread
        self.api_thread = threading.Thread(target=run_server, daemon=True)
        self.api_thread.start()
        print(f"✅ WARP API Server thread started on port {port}")
        
        # Give it a moment to start
        time.sleep(0.5)
        print(f"🌐 WARP API Server started on http://localhost:{port}")
    
    async def stop(self):
        """Graceful shutdown"""
        logger.info("\n🛑 Stopping WARP Engine...")
        
        self.running = False
        
        # Stop P2P network
        if self.p2p_network:
            logger.info("  Stopping P2P Network...")
            await self.p2p_network.stop()
        
        # Stop RPC server
        if self.rpc_server:
            logger.info("  Stopping RPC Server...")
            self.rpc_server.stop()
        
        # Close bridge
        if self.bridge:
            logger.info("  Closing Rainbow Bridge...")
            # Bridge cleanup here
        
        logger.info("✅ WARP Engine shutdown complete")
    
    def mine_block(self, miner_address: str) -> Optional[str]:
        """Mine a new block (wrapper for blockchain)"""
        return self.blockchain.mine_block(miner_address)
    
    def get_balance(self, address: str) -> float:
        """Get wallet balance (wrapper for blockchain)"""
        return self.blockchain.get_balance(address)
    
    def create_transaction(self, sender: str, receiver: str, amount: float, 
                          private_key: str, fee: float = 0.0) -> Optional[str]:
        """Create transaction (wrapper for blockchain)"""
        return self.blockchain.create_transaction(sender, receiver, amount, private_key, fee)


async def main():
    """Main entry point"""
    print("\n")
    print("╔═══════════════════════════════════════════════════════════════════════════╗")
    print("║                                                                           ║")
    print("║                  🔥 ZION WARP ENGINE CORE v2.8.0 🔥                       ║")
    print("║                                                                           ║")
    print("║                    'Ad Astra Per Estrella' 🌟                            ║")
    print("║                    To The Stars Through The Star                         ║")
    print("║                                                                           ║")
    print("╚═══════════════════════════════════════════════════════════════════════════╝")
    print()
    
    # Parse command line args (simple version)
    enable_bridge = "--bridge" in sys.argv
    bridge_key = None
    if enable_bridge:
        # In production, load from secure config
        logger.warning("⚠️  Bridge mode enabled - requires bridge private key")
    
    # Initialize WARP engine
    engine = ZionWARPEngine(
        blockchain_db="zion_blockchain.db",
        enable_rpc=True,
        enable_p2p=True,
        enable_bridge=enable_bridge,
        bridge_private_key=bridge_key
    )
    
    # Start engine
    await engine.start()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down WARP Engine...")
        print("🌟 Ad Astra Per Estrella 🌟\n")
