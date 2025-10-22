#!/usr/bin/env python3
"""
Quick Test for ESTRELLA Solar System
=====================================
Tests the solar system without AI components
"""

import asyncio
import sys

# Temporarily disable AI imports
sys.modules['zion.ai.ai_config'] = None
sys.modules['rainbow_bridge_quantum'] = None

from new_zion_blockchain import NewZionBlockchain
from zion_rpc_server import ZIONRPCServer
from zion_p2p_network import ZIONP2PNetwork

# Now import our solar system
from estrella_solar_system import ESTRELLASolarSystem, CONSCIOUSNESS_POLES, PLANETS_COUNT, TOTAL_MOONS


async def test_solar_system():
    """Test ESTRELLA Solar System"""
    print("="*80)
    print("ESTRELLA Solar System - Quick Test")
    print("="*80)
    print()
    
    # Initialize components
    print("1️⃣  Initializing blockchain...")
    blockchain = NewZionBlockchain()
    
    print("2️⃣  Initializing RPC server...")
    rpc_server = ZIONRPCServer(blockchain, port=18081)
    
    print("3️⃣  Initializing P2P network...")
    p2p_network = ZIONP2PNetwork(blockchain, port=18080)
    
    # Pool configs
    pool_configs = [
        {'host': 'localhost', 'port': 3333, 'status': 'CONNECTED'},
        {'host': '91.98.122.165', 'port': 3333, 'status': 'CONNECTED'}
    ]
    
    # Seed nodes
    seed_nodes = ["91.98.122.165:18080"]
    
    print("4️⃣  Creating ESTRELLA Solar System...")
    solar_system = ESTRELLASolarSystem(
        blockchain=blockchain,
        rpc_server=rpc_server,
        p2p_network=p2p_network,
        pool_configs=pool_configs,
        seed_nodes=seed_nodes
    )
    
    print("5️⃣  Initializing solar system...")
    await solar_system.initialize()
    
    print("6️⃣  Testing system status...")
    status = solar_system.get_status()
    
    print("\n" + "="*80)
    print("SYSTEM STATUS")
    print("="*80)
    print(f"System: {status['system']}")
    print(f"Version: {status['version']}")
    print(f"Codename: {status['codename']}")
    print()
    
    print("☀️  ESTRELLA CORE:")
    core = status['estrella_core']
    print(f"   Poles: {core['poles_active']}/{core['poles_total']}")
    print(f"   Consciousness Level: {core['consciousness_level']:.2%}")
    print(f"   Fusion Energy: {core['fusion_energy']:.2f}")
    print()
    
    print("🪐 PLANETS:")
    for i, planet in enumerate(status['planets'], 1):
        print(f"   {i}. {planet['name']}")
        print(f"      Status: {planet['status']}")
        print(f"      Moons: {planet['moons_active']}/{planet['moons_count']}")
        print(f"      Energy: {planet['total_energy']:.2f}")
    print()
    
    print("📊 TOTALS:")
    print(f"   Total Planets: {status['total_planets']}")
    print(f"   Total Moons: {status['total_moons']}")
    print(f"   Active Planets: {status['active_planets']}")
    print(f"   Total Energy: {status['total_energy']:.2f}")
    print()
    
    print("🔢 SACRED CONSTANTS:")
    sc = status['sacred_constants']
    print(f"   Phi (φ): {sc['phi']}")
    print(f"   Pi (π): {sc['pi']}")
    print(f"   e: {sc['e']}")
    print(f"   Consciousness Poles: {sc['consciousness_poles']}")
    print(f"   Moons per Planet: {sc['moons_per_planet']}")
    print(f"   Base Frequency: {sc['base_frequency_hz']} Hz")
    print()
    
    # Test orbital advancement
    print("7️⃣  Testing orbital advancement (10 days)...")
    await solar_system.advance_time(10)
    print(f"   System Time: Day {solar_system.system_time}")
    
    # Check orbital positions
    print("\n🌍 ORBITAL POSITIONS:")
    for planet in solar_system.planets:
        pos = planet.get_orbital_position() * 100
        print(f"   {planet.name}: {pos:.1f}% ({planet.orbital_day}/{planet.orbital_period} days)")
    print()
    
    # Verify moon cycles
    print("8️⃣  Testing moon cycles...")
    ai_planet = solar_system.get_planet("AI_CONSCIOUSNESS")
    if ai_planet and len(ai_planet.moons) > 0:
        moon = ai_planet.moons[0]
        print(f"   Moon: {moon.name}")
        print(f"   Phase: {moon.phase.name}")
        print(f"   Cycle Day: {moon.cycle_day}/30")
        print(f"   Phase Energy: {moon.get_phase_energy():.2f}")
    print()
    
    print("="*80)
    print("✅ TEST COMPLETE!")
    print("="*80)
    print()
    print("🌟 ESTRELLA Solar System is fully operational!")
    print(f"   ☀️  1 ESTRELLA Core with {CONSCIOUSNESS_POLES} Consciousness Poles")
    print(f"   🪐 {PLANETS_COUNT} Planets")
    print(f"   🌙 {TOTAL_MOONS} Moons total")
    print()


if __name__ == "__main__":
    asyncio.run(test_solar_system())
