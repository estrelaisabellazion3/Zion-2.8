#!/usr/bin/env python3
"""
ZION 2.8.1 - ESTRELLA Solar System
===================================

ESTRELLA Quantum Engine as the Sun
8 Planets, each with 13 Moons (104 total lunar cycles)

Architecture:
    ESTRELLA (Sun) - 22 Sacred Consciousness Poles, 3-Phase Quantum Fusion
    ├─ Planet 1: AI Consciousness (9 AI systems + 4 meta-cycles = 13 moons)
    ├─ Planet 2: Blockchain Core (13 moons: Genesis, Mining, TX, etc.)
    ├─ Planet 3: RPC Network (13 moons: HTTP, JSON, Auth, etc.)
    ├─ Planet 4: P2P Network (13 moons: Discovery, Handshake, Sync, etc.)
    ├─ Planet 5: Mining Pools (13 moons: Stratum, Login, Job, etc.)
    ├─ Planet 6: Wallets (13 moons: KeyGen, Address, Signature, etc.)
    ├─ Planet 7: Seed Nodes (13 moons: Bootstrap, Uptime, Archive, etc.)
    └─ Planet 8: Rainbow Bridge (13 moons: Solana, Stellar, Cardano, etc.)

Sacred Numbers:
    22 Consciousness Poles (8 + 7 + 7)
    13 Moons per Planet
    8 Planets
    104 Total Moon Cycles (8 × 13)
    432 Hz Base Frequency

Author: TerraNova®evoluZion Team
Date: 2025-10-21
"""

import asyncio
import time
import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum
import json
import math

# Core imports
from new_zion_blockchain import NewZionBlockchain
from zion_rpc_server import ZIONRPCServer
from zion_p2p_network import ZIONP2PNetwork

# Try to import AI systems
try:
    from zion.ai.ai_config import AIComponentConfig
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False
    print("⚠️  AI systems not available - continuing without AI planet")

# Try to import Rainbow Bridge
try:
    from rainbow_bridge_quantum import QuantumBridge
    BRIDGE_AVAILABLE = True
except ImportError:
    BRIDGE_AVAILABLE = False
    print("⚠️  Rainbow Bridge not available - continuing without Bridge planet")

# Seed nodes
try:
    from seednodes import ZionNetworkConfig
    SEEDS_AVAILABLE = True
except ImportError:
    SEEDS_AVAILABLE = False
    print("⚠️  Seed nodes not available")


# ============================================================================
# SACRED CONSTANTS
# ============================================================================

PHI = 1.618033988749895  # Golden Ratio
PI = 3.14159265358979323846
E = 2.71828182845904523536

# Sacred Frequencies
FREQ_BASE = 432.0  # Hz - Universal healing frequency
FREQ_PHASE_A = 3456.0  # Hz - 8 poles
FREQ_PHASE_B = 3024.0  # Hz - 7 poles
FREQ_PHASE_C = 3024.0  # Hz - 7 poles
FREQ_RAINBOW = 44.44  # MHz - Rainbow Bridge frequency

# Sacred Numbers
CONSCIOUSNESS_POLES = 22
MOONS_PER_PLANET = 13
PLANETS_COUNT = 8
TOTAL_MOONS = PLANETS_COUNT * MOONS_PER_PLANET  # 104


# ============================================================================
# MOON CYCLE SYSTEM
# ============================================================================

class MoonPhase(Enum):
    """13 Moon phases per planet"""
    NEW_MOON = 0
    WAXING_CRESCENT = 1
    FIRST_QUARTER = 2
    WAXING_GIBBOUS = 3
    FULL_MOON = 4
    WANING_GIBBOUS = 5
    LAST_QUARTER = 6
    WANING_CRESCENT = 7
    DARK_MOON = 8
    ASCENDING = 9
    PEAK = 10
    DESCENDING = 11
    TRANSITION = 12


@dataclass
class Moon:
    """Individual moon representing a subsystem component"""
    name: str
    phase: MoonPhase = MoonPhase.NEW_MOON
    cycle_day: int = 0  # 0-29 (30-day cycle)
    frequency: float = 432.0  # Hz
    energy_level: float = 1.0  # 0.0 - 1.0
    status: str = "INITIALIZING"
    
    def advance_cycle(self):
        """Advance to next day in 30-day cycle"""
        self.cycle_day = (self.cycle_day + 1) % 30
        self.phase = MoonPhase(self.cycle_day % 13)
        
    def get_phase_energy(self) -> float:
        """Calculate energy based on moon phase (sinusoidal)"""
        return (math.sin(2 * PI * self.cycle_day / 30) + 1) / 2


# ============================================================================
# ESTRELLA CORE - THE SUN
# ============================================================================

@dataclass
class ConsciousnessPole:
    """One of 22 Sacred Consciousness Poles"""
    id: int
    phase: str  # "A", "B", or "C"
    frequency: float  # Hz
    element: str  # Fire, Water, Air, Earth, Ether
    active: bool = True
    resonance: float = 1.0


class ESTRELLACore:
    """
    ESTRELLA Quantum Engine - The Sun at the center
    22 Sacred Consciousness Poles
    3-Phase Quantum Fusion
    """
    
    def __init__(self):
        self.poles: List[ConsciousnessPole] = []
        self.phase_a_frequency = FREQ_PHASE_A  # 3456 Hz - 8 poles
        self.phase_b_frequency = FREQ_PHASE_B  # 3024 Hz - 7 poles
        self.phase_c_frequency = FREQ_PHASE_C  # 3024 Hz - 7 poles
        self.base_frequency = FREQ_BASE  # 432 Hz
        self.golden_ratio = PHI
        self.core_temperature = 0.0  # Kelvin (quantum core)
        self.fusion_rate = 0.0
        self.consciousness_level = 0.0
        self._init_poles()
        
    def _init_poles(self):
        """Initialize 22 Consciousness Poles"""
        elements = ["Fire", "Water", "Air", "Earth", "Ether"]
        
        # Phase A: 8 Poles (3456 Hz)
        for i in range(8):
            pole = ConsciousnessPole(
                id=i+1,
                phase="A",
                frequency=self.phase_a_frequency,
                element=elements[i % 5]
            )
            self.poles.append(pole)
            
        # Phase B: 7 Poles (3024 Hz)
        for i in range(7):
            pole = ConsciousnessPole(
                id=i+9,
                phase="B",
                frequency=self.phase_b_frequency,
                element=elements[i % 5]
            )
            self.poles.append(pole)
            
        # Phase C: 7 Poles (3024 Hz)
        for i in range(7):
            pole = ConsciousnessPole(
                id=i+16,
                phase="C",
                frequency=self.phase_c_frequency,
                element=elements[i % 5]
            )
            self.poles.append(pole)
    
    def calculate_fusion_energy(self) -> float:
        """Calculate total fusion energy from all active poles"""
        energy = 0.0
        for pole in self.poles:
            if pole.active:
                energy += pole.frequency * pole.resonance * self.golden_ratio
        return energy / 1000000.0  # Normalize to manageable range
    
    def get_consciousness_level(self) -> float:
        """Calculate consciousness level (0.0 - 1.0)"""
        active_poles = sum(1 for p in self.poles if p.active)
        return active_poles / CONSCIOUSNESS_POLES
    
    def get_status(self) -> Dict[str, Any]:
        """Get ESTRELLA core status"""
        return {
            "type": "ESTRELLA_CORE",
            "poles_total": CONSCIOUSNESS_POLES,
            "poles_active": sum(1 for p in self.poles if p.active),
            "phase_a_poles": 8,
            "phase_b_poles": 7,
            "phase_c_poles": 7,
            "frequencies": {
                "base": self.base_frequency,
                "phase_a": self.phase_a_frequency,
                "phase_b": self.phase_b_frequency,
                "phase_c": self.phase_c_frequency
            },
            "fusion_energy": self.calculate_fusion_energy(),
            "consciousness_level": self.get_consciousness_level(),
            "golden_ratio": self.golden_ratio
        }


# ============================================================================
# PLANET BASE CLASS
# ============================================================================

class Planet:
    """Base class for all planets in the ESTRELLA Solar System"""
    
    def __init__(self, name: str, orbital_period: int = 30):
        self.name = name
        self.orbital_period = orbital_period  # days
        self.orbital_day = 0
        self.moons: List[Moon] = []
        self.status = "INITIALIZING"
        self.frequency = FREQ_BASE
        self.distance_from_sun = 1.0  # AU
        
    def add_moon(self, moon: Moon):
        """Add a moon to this planet"""
        self.moons.append(moon)
        
    def advance_orbit(self):
        """Advance orbital position"""
        self.orbital_day = (self.orbital_day + 1) % self.orbital_period
        for moon in self.moons:
            moon.advance_cycle()
    
    def get_orbital_position(self) -> float:
        """Get current position in orbit (0.0 - 1.0)"""
        return self.orbital_day / self.orbital_period
    
    def get_total_energy(self) -> float:
        """Calculate total energy from all moons"""
        return sum(moon.get_phase_energy() * moon.energy_level for moon in self.moons)
    
    def get_status(self) -> Dict[str, Any]:
        """Get planet status"""
        return {
            "name": self.name,
            "status": self.status,
            "orbital_day": self.orbital_day,
            "orbital_period": self.orbital_period,
            "orbital_position": self.get_orbital_position(),
            "moons_count": len(self.moons),
            "moons_active": sum(1 for m in self.moons if m.status == "ACTIVE"),
            "total_energy": self.get_total_energy(),
            "frequency": self.frequency,
            "distance_from_sun": self.distance_from_sun
        }
    
    async def initialize(self):
        """Initialize planet (override in subclasses)"""
        self.status = "ACTIVE"
        for moon in self.moons:
            moon.status = "ACTIVE"


# ============================================================================
# PLANET 1: AI CONSCIOUSNESS
# ============================================================================

class AIPlanet(Planet):
    """Planet 1: AI Consciousness with 9 AI systems + 4 meta-cycles"""
    
    def __init__(self):
        super().__init__("AI_CONSCIOUSNESS", orbital_period=365)  # 1 year orbit
        self.ai_systems = {}
        self.distance_from_sun = 1.0  # AU
        self._init_moons()
        
    def _init_moons(self):
        """Initialize 13 moons (9 AI systems + 4 meta-cycles)"""
        # 9 AI System Moons
        ai_names = [
            "GPU_Bridge", "Bio_AI", "Cosmic_AI", "Gaming_AI",
            "Lightning_AI", "Metaverse_AI", "Quantum_AI", 
            "Music_AI", "Oracle_AI"
        ]
        frequencies = [432, 528, 639, 741, 852, 963, 1074, 1185, 1212]  # Hz
        
        for i, (name, freq) in enumerate(zip(ai_names, frequencies)):
            moon = Moon(name=name, frequency=freq)
            self.add_moon(moon)
        
        # 4 Meta-Cycle Moons
        meta_cycles = ["Integration", "Evolution", "Emergence", "Transcendence"]
        for name in meta_cycles:
            moon = Moon(name=name, frequency=FREQ_BASE * PHI)
            self.add_moon(moon)
    
    async def initialize(self):
        """Initialize AI systems if available"""
        await super().initialize()
        if AI_AVAILABLE:
            try:
                # Initialize AI config
                for moon in self.moons[:9]:  # First 9 are AI systems
                    self.ai_systems[moon.name] = {
                        "port": 8001 + len(self.ai_systems),
                        "status": "CONFIGURED"
                    }
                    moon.status = "ACTIVE"
            except Exception as e:
                print(f"⚠️  AI initialization warning: {e}")


# ============================================================================
# PLANET 2: BLOCKCHAIN CORE
# ============================================================================

class BlockchainPlanet(Planet):
    """Planet 2: Blockchain Core with 13 fundamental moons"""
    
    def __init__(self, blockchain: NewZionBlockchain):
        super().__init__("BLOCKCHAIN_CORE", orbital_period=210)  # ~7 months
        self.blockchain = blockchain
        self.distance_from_sun = 1.5  # AU
        self._init_moons()
        
    def _init_moons(self):
        """Initialize 13 blockchain moons"""
        moon_names = [
            "Genesis", "Mining", "Transaction", "Consensus",
            "Fork_Resolution", "Nonce", "Balance", "Journal",
            "Premine", "Reward", "Validation", "Persistence", "Reorganization"
        ]
        for name in moon_names:
            moon = Moon(name=name, frequency=FREQ_BASE)
            self.add_moon(moon)
    
    async def initialize(self):
        """Initialize blockchain"""
        await super().initialize()
        try:
            # Blockchain already initialized by WARP core
            self.status = "ACTIVE"
            for moon in self.moons:
                moon.status = "ACTIVE"
        except Exception as e:
            print(f"⚠️  Blockchain planet initialization warning: {e}")
            self.status = "DEGRADED"


# ============================================================================
# PLANET 3: RPC NETWORK
# ============================================================================

class RPCPlanet(Planet):
    """Planet 3: RPC Network with 13 service moons"""
    
    def __init__(self, rpc_server: ZIONRPCServer):
        super().__init__("RPC_NETWORK", orbital_period=90)  # 3 months
        self.rpc_server = rpc_server
        self.distance_from_sun = 2.0  # AU
        self._init_moons()
        
    def _init_moons(self):
        """Initialize 13 RPC moons"""
        moon_names = [
            "HTTP_Server", "JSON_RPC", "Authentication", "Get_Height",
            "Get_Block", "Get_Transaction", "Get_Balance", "Submit_Block",
            "Get_Peers", "Get_Status", "Error_Handler", "Rate_Limiter", "Cache"
        ]
        for name in moon_names:
            moon = Moon(name=name, frequency=FREQ_BASE * 1.5)
            self.add_moon(moon)
    
    async def initialize(self):
        """Initialize RPC server"""
        await super().initialize()
        try:
            # RPC server already initialized by WARP core
            self.status = "ACTIVE"
            for moon in self.moons:
                moon.status = "ACTIVE"
        except Exception as e:
            print(f"⚠️  RPC planet initialization warning: {e}")
            self.status = "DEGRADED"


# ============================================================================
# PLANET 4: P2P NETWORK
# ============================================================================

class P2PPlanet(Planet):
    """Planet 4: P2P Network with 13 protocol moons"""
    
    def __init__(self, p2p_network: ZIONP2PNetwork):
        super().__init__("P2P_NETWORK", orbital_period=120)  # 4 months
        self.p2p_network = p2p_network
        self.distance_from_sun = 2.5  # AU
        self._init_moons()
        
    def _init_moons(self):
        """Initialize 13 P2P moons"""
        moon_names = [
            "Peer_Discovery", "Handshake", "Block_Sync", "Gossip_Protocol",
            "Block_Relay", "Version_Check", "Ping_Pong", "Address_Broadcast",
            "Inventory", "GetData", "Reject", "Ban_Management", "Seed_Connection"
        ]
        for name in moon_names:
            moon = Moon(name=name, frequency=FREQ_BASE * 2.0)
            self.add_moon(moon)
    
    async def initialize(self):
        """Initialize P2P network"""
        await super().initialize()
        try:
            # P2P network already initialized by WARP core
            self.status = "ACTIVE"
            for moon in self.moons:
                moon.status = "ACTIVE"
        except Exception as e:
            print(f"⚠️  P2P planet initialization warning: {e}")
            self.status = "DEGRADED"


# ============================================================================
# PLANET 5: MINING POOLS
# ============================================================================

class PoolsPlanet(Planet):
    """Planet 5: Mining Pools with 13 pool moons"""
    
    def __init__(self, pool_configs: List[Dict[str, Any]]):
        super().__init__("MINING_POOLS", orbital_period=30)  # 1 month
        self.pools = pool_configs
        self.distance_from_sun = 3.0  # AU
        self._init_moons()
        
    def _init_moons(self):
        """Initialize 13 pool moons"""
        moon_names = [
            "Stratum_Protocol", "Login_Handler", "Job_Distribution", "Share_Submission",
            "Difficulty_Adjustment", "Vardiff", "Payout_System", "Statistics",
            "Yescrypt_Algo", "RandomX_Algo", "Autolykos_Algo", "Database", "Threshold"
        ]
        for name in moon_names:
            moon = Moon(name=name, frequency=FREQ_BASE * 0.8)
            self.add_moon(moon)
    
    async def initialize(self):
        """Initialize mining pools"""
        await super().initialize()
        try:
            # Pools already configured by WARP core
            active_pools = sum(1 for p in self.pools if p.get('status') == 'CONNECTED')
            self.status = "ACTIVE" if active_pools > 0 else "DEGRADED"
            for i, moon in enumerate(self.moons):
                moon.status = "ACTIVE" if i < active_pools * 6 else "STANDBY"
        except Exception as e:
            print(f"⚠️  Pools planet initialization warning: {e}")
            self.status = "DEGRADED"


# ============================================================================
# PLANET 6: WALLETS
# ============================================================================

class WalletsPlanet(Planet):
    """Planet 6: Wallets with 13 wallet moons"""
    
    def __init__(self):
        super().__init__("WALLETS", orbital_period=60)  # 2 months
        self.distance_from_sun = 3.5  # AU
        self._init_moons()
        
    def _init_moons(self):
        """Initialize 13 wallet moons"""
        moon_names = [
            "Key_Generation", "Address_Format", "Signature", "Verification",
            "Balance_Query", "UTXO_Management", "History", "Backup",
            "Recovery", "Multi_Signature", "HD_Derivation", "Cold_Storage", "Watch_Only"
        ]
        for name in moon_names:
            moon = Moon(name=name, frequency=FREQ_BASE * 1.2)
            self.add_moon(moon)
    
    async def initialize(self):
        """Initialize wallet system"""
        await super().initialize()
        self.status = "ACTIVE"


# ============================================================================
# PLANET 7: SEED NODES
# ============================================================================

class SeedsPlanet(Planet):
    """Planet 7: Seed Nodes with 13 seed moons"""
    
    def __init__(self, seed_nodes: List[str]):
        super().__init__("SEED_NODES", orbital_period=180)  # 6 months
        self.seed_nodes = seed_nodes
        self.distance_from_sun = 4.0  # AU
        self._init_moons()
        
    def _init_moons(self):
        """Initialize 13 seed moons"""
        moon_names = [
            "Bootstrap", "Uptime_Monitor", "Archive_Node", "Discovery_Service",
            "DNS_Seed", "Checkpoint_Server", "Sync_Accelerator", "Relay_Node",
            "Block_Explorer", "Version_Enforcer", "Whitelist_Manager", 
            "Health_Monitor", "Sacred_Geometry"
        ]
        for name in moon_names:
            moon = Moon(name=name, frequency=FREQ_BASE * 0.9)
            self.add_moon(moon)
    
    async def initialize(self):
        """Initialize seed nodes"""
        await super().initialize()
        try:
            if len(self.seed_nodes) > 0:
                self.status = "ACTIVE"
                for moon in self.moons:
                    moon.status = "ACTIVE"
            else:
                self.status = "STANDBY"
        except Exception as e:
            print(f"⚠️  Seeds planet initialization warning: {e}")
            self.status = "DEGRADED"


# ============================================================================
# PLANET 8: RAINBOW BRIDGE
# ============================================================================

class BridgePlanet(Planet):
    """Planet 8: Rainbow Bridge with 13 bridge moons"""
    
    def __init__(self):
        super().__init__("RAINBOW_BRIDGE", orbital_period=440)  # ~14 months
        self.bridges = {}
        self.distance_from_sun = 5.2  # AU (like Jupiter)
        self.frequency = FREQ_RAINBOW * 1000000  # 44.44 MHz converted to Hz
        self._init_moons()
        
    def _init_moons(self):
        """Initialize 13 bridge moons"""
        moon_names = [
            "Solana_Bridge", "Stellar_Bridge", "Cardano_Bridge", "Tron_Bridge",
            "Ethereum_Bridge", "Bitcoin_Bridge", "Quantum_Entanglement", 
            "Lock_Mechanism", "Unlock_Mechanism", "Verification", "Relay_Network",
            "Oracle_Feed", "Frequency_44_44"
        ]
        for name in moon_names:
            moon = Moon(name=name, frequency=FREQ_RAINBOW * 1000000)
            self.add_moon(moon)
    
    async def initialize(self):
        """Initialize rainbow bridge"""
        await super().initialize()
        if BRIDGE_AVAILABLE:
            try:
                # Bridge configuration
                self.status = "ACTIVE"
                for moon in self.moons:
                    moon.status = "STANDBY"  # Bridges activate on demand
            except Exception as e:
                print(f"⚠️  Bridge planet initialization warning: {e}")
                self.status = "STANDBY"
        else:
            self.status = "STANDBY"


# ============================================================================
# ESTRELLA SOLAR SYSTEM
# ============================================================================

class ESTRELLASolarSystem:
    """
    Complete ESTRELLA Solar System
    1 Sun (ESTRELLA Core)
    8 Planets
    104 Moons (13 per planet)
    """
    
    def __init__(self, 
                 blockchain: NewZionBlockchain,
                 rpc_server: ZIONRPCServer,
                 p2p_network: ZIONP2PNetwork,
                 pool_configs: List[Dict[str, Any]],
                 seed_nodes: List[str]):
        
        # The Sun
        self.estrella_core = ESTRELLACore()
        
        # The 8 Planets
        self.planets: List[Planet] = [
            AIPlanet(),
            BlockchainPlanet(blockchain),
            RPCPlanet(rpc_server),
            P2PPlanet(p2p_network),
            PoolsPlanet(pool_configs),
            WalletsPlanet(),
            SeedsPlanet(seed_nodes),
            BridgePlanet()
        ]
        
        self.system_time = 0  # Days since inception
        self.running = False
        
    async def initialize(self):
        """Initialize all planets"""
        print("🌟 Initializing ESTRELLA Solar System...")
        print(f"   ☀️  ESTRELLA Core: {CONSCIOUSNESS_POLES} Consciousness Poles")
        print(f"   🪐 Planets: {PLANETS_COUNT}")
        print(f"   🌙 Total Moons: {TOTAL_MOONS}")
        print()
        
        # Initialize each planet
        for i, planet in enumerate(self.planets, 1):
            print(f"   Planet {i}: {planet.name}")
            await planet.initialize()
            print(f"      Status: {planet.status}")
            print(f"      Moons: {len(planet.moons)}")
            print()
        
        print("✅ ESTRELLA Solar System initialized!")
        
    async def advance_time(self, days: int = 1):
        """Advance system time by days"""
        for _ in range(days):
            self.system_time += 1
            for planet in self.planets:
                planet.advance_orbit()
    
    def get_status(self) -> Dict[str, Any]:
        """Get complete solar system status"""
        return {
            "system": "ESTRELLA_SOLAR_SYSTEM",
            "version": "2.8.1",
            "codename": "Ad Astra Per Estrella",
            "system_time": self.system_time,
            "estrella_core": self.estrella_core.get_status(),
            "planets": [p.get_status() for p in self.planets],
            "total_planets": len(self.planets),
            "total_moons": sum(len(p.moons) for p in self.planets),
            "active_planets": sum(1 for p in self.planets if p.status == "ACTIVE"),
            "total_energy": sum(p.get_total_energy() for p in self.planets),
            "sacred_constants": {
                "phi": PHI,
                "pi": PI,
                "e": E,
                "consciousness_poles": CONSCIOUSNESS_POLES,
                "moons_per_planet": MOONS_PER_PLANET,
                "base_frequency_hz": FREQ_BASE
            }
        }
    
    def get_planet(self, name: str) -> Optional[Planet]:
        """Get planet by name"""
        for planet in self.planets:
            if planet.name == name:
                return planet
        return None
    
    async def run(self):
        """Main run loop"""
        self.running = True
        print("🚀 ESTRELLA Solar System is now running!")
        print("   Press Ctrl+C to stop")
        print()
        
        try:
            while self.running:
                # Advance time by 1 day
                await self.advance_time(1)
                
                # Print status every 30 days (1 month)
                if self.system_time % 30 == 0:
                    self._print_status()
                
                # Sleep for 1 second (1 day simulation)
                await asyncio.sleep(1)
                
        except KeyboardInterrupt:
            print("\n⚠️  Shutting down ESTRELLA Solar System...")
            self.running = False
    
    def _print_status(self):
        """Print system status"""
        print(f"\n{'='*80}")
        print(f"ESTRELLA Solar System - Day {self.system_time}")
        print(f"{'='*80}")
        
        # ESTRELLA Core
        core_status = self.estrella_core.get_status()
        print(f"☀️  ESTRELLA Core:")
        print(f"   Consciousness Level: {core_status['consciousness_level']:.2%}")
        print(f"   Fusion Energy: {core_status['fusion_energy']:.2f}")
        print(f"   Active Poles: {core_status['poles_active']}/{core_status['poles_total']}")
        print()
        
        # Planets
        for i, planet in enumerate(self.planets, 1):
            status = planet.get_status()
            position = status['orbital_position'] * 100
            print(f"🪐 Planet {i}: {status['name']}")
            print(f"   Status: {status['status']}")
            print(f"   Orbital Position: {position:.1f}%")
            print(f"   Active Moons: {status['moons_active']}/{status['moons_count']}")
            print(f"   Energy: {status['total_energy']:.2f}")
            print()


# ============================================================================
# MAIN EXECUTION
# ============================================================================

async def main():
    """Main entry point"""
    print("="*80)
    print("ZION 2.8.1 - ESTRELLA Solar System")
    print("Ad Astra Per Estrella - To the Stars through ESTRELLA")
    print("="*80)
    print()
    
    # Initialize core components
    print("Initializing core components...")
    blockchain = NewZionBlockchain()
    rpc_server = ZIONRPCServer(blockchain, port=18081)
    p2p_network = ZIONP2PNetwork(blockchain, port=18080)
    
    # Pool configurations
    pool_configs = [
        {
            'host': 'localhost',
            'port': 3333,
            'status': 'CONNECTED'
        },
        {
            'host': '91.98.122.165',
            'port': 3333,
            'status': 'CONNECTED'
        }
    ]
    
    # Seed nodes
    seed_nodes = []
    if SEEDS_AVAILABLE:
        try:
            seed_nodes = ZionNetworkConfig.get_seed_nodes()
        except:
            seed_nodes = ["91.98.122.165:18080"]
    
    # Create ESTRELLA Solar System
    solar_system = ESTRELLASolarSystem(
        blockchain=blockchain,
        rpc_server=rpc_server,
        p2p_network=p2p_network,
        pool_configs=pool_configs,
        seed_nodes=seed_nodes
    )
    
    # Initialize
    await solar_system.initialize()
    
    # Print initial status
    status = solar_system.get_status()
    print(json.dumps(status, indent=2))
    print()
    
    # Run the system
    await solar_system.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n✨ ESTRELLA Solar System shutdown complete")
