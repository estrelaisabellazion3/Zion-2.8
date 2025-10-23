#!/usr/bin/env python3
"""
ZION Seed Nodes & Network Configuration
Centrální konfigurace pro všechny P2P, RPC a pool komponenty s reálnými daty
"""

import time
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass 
class SeedNode:
    """Reprezentace seed node s metadaty"""
    host: str
    port: int
    type: str  # 'production', 'testnet', 'local'
    region: str = "unknown"
    last_seen: Optional[float] = None
    reliability: float = 1.0  # 0.0-1.0 score

    @property
    def address(self) -> str:
        return f"{self.host}:{self.port}"
    
    def is_available(self) -> bool:
        """Rychlá kontrola dostupnosti"""
        # TODO: Implement ping check
        return True

class ZionNetworkConfig:
    """Centrální konfigurace ZION sítě s reálnými daty"""
    
    # PRODUCTION SEED NODES - REÁLNÉ IP ADRESY  
    PRODUCTION_SEEDS = [
        SeedNode("91.98.122.165", 8333, "production", "europe"),     # Primary production server
        SeedNode("91.98.122.165", 8334, "production", "europe"),     # Secondary production server (different port)
    ]
    
    # TESTNET SEED NODES  
    TESTNET_SEEDS = [
        SeedNode("91.98.122.165", 8334, "testnet", "europe"),       # Testnet port
        SeedNode("127.0.0.1", 8334, "local", "localhost"),          # Local testnet fallback
    ]
    
    # DEVELOPMENT SEED NODES
    DEV_SEEDS = [
        SeedNode("127.0.0.1", 8333, "local", "localhost"),
        SeedNode("127.0.0.1", 8334, "local", "localhost"),
    ]
    
    # NETWORK PORTS - STANDARDNÍ KONFIGURACE
    PORTS = {
        'p2p_mainnet': 8333,
        'p2p_testnet': 8334, 
        'rpc_mainnet': 8545,  # Changed from 8332 to match pool expectation
        'rpc_testnet': 8335,
        'pool_stratum': 3333,  # Standard Stratum port
        'pool_api': 3334,      # API port (3333 + 1)
        'pool_testnet': 3335,
    }
    
    # RPC KONFIGURACE
    RPC_CONFIG = {
        'host': '0.0.0.0',
        'port': 8332,
        'require_auth': False,  # Dočasně zakázáno pro lokální testování
        'rate_limit_per_minute': 120,
        'burst_limit': 20,
        'cors_enabled': True,
    }
    
    # POOL KONFIGURACE  
    POOL_CONFIG = {
        'host': '0.0.0.0',
        'stratum_port': 3333,  # Standard Stratum port
        'api_port': 3334,      # API port
        'fee_percent': 0.01,  # 1%
        'payout_threshold': 1.0,  # ZION
        'difficulty': {
            'randomx': 100,     # Velmi nízká obtížnost pro testování
            'yescrypt': 8000, 
            'autolykos_v2': 75,
            'kawpow': 50,       # KawPow pro GPU mining
            'ethash': 40,       # Ethash pro GPU mining
            'gpu': 50           # Default GPU difficulty (fallback)
        },
        'eco_rewards': {
            'randomx': 1.0,      # Standard
            'yescrypt': 1.15,    # +15% eco bonus
            'autolykos_v2': 1.2, # +20% eco bonus
            'kawpow': 1.0,       # Standard GPU
            'ethash': 1.0,       # Standard GPU
            'gpu': 1.0           # Default GPU (fallback)
        }
    }
    
    # P2P NETWORK KONFIGURACE
    P2P_CONFIG = {
        'max_peers': 10,
        'ping_interval': 30,
        'peer_timeout': 300,
        'connection_timeout': 10,  # Timeout pro seed connections
        'ban_threshold': 100,
        'ban_duration': 900,
        'score_decay_interval': 60
    }
    
    # BLOCKCHAIN KONFIGURACE
    BLOCKCHAIN_CONFIG = {
        'db_file': 'data/zion_blockchain.db',
        'mining_difficulty': 2,  # 2 leading zeros = ~2^16 hash attempts on average (reasonable PoW)
        'block_reward': 50,
        'target_block_time': 120,  # sekund
        'mtp_window': 11,
        'max_future_drift': 7200,  # 2 hodiny
        'max_reorg_depth': 50
    }
    
    # EKONOMICKÝ MODEL
    ECONOMIC_MODEL = {
        'mining_config': {
            'base_block_reward': 50.0,  # 50 ZION per block (adjusted from 5479.45 for proper emission)
            'block_time_target': 120,  # 2 minutes
            'blocks_per_year': 262800,  # 120s blocks = 262800/year
            'annual_emission': 13140000,  # ~13.14M ZION/year (manageable)
            'max_supply': 144000000000,  # 144B ZION total (10,000+ years at this rate)
            'halving_interval': None,  # No halving, constant emission
        },
        'consciousness_multipliers': {
            'level_1': 1.0,   # Base level
            'level_2': 1.5,   # +50%
            'level_3': 2.0,   # +100%
            'level_4': 3.0,   # +200%
            'level_5': 5.0,   # +400%
            'level_6': 7.0,   # +600%
            'level_7': 9.0,   # +800%
            'level_8': 9.5,   # +850%
            'level_9': 10.0,  # +900% (Master level)
        },
        'tithe_distribution': {
            'dao_fund': 0.10,          # 10% DAO fund
            'humanitarian': 0.10,       # 10% Children Future Fund
            'dev_team': 0.01,          # 1% Development
            'genesis_creator': 0.0033, # 0.33% Yeshuae Amon Ra
            'pool_admin': 0.01,        # 1% Pool Admin
        }
    }

    @classmethod
    def get_seed_nodes(cls, network_type: str = "production") -> List[SeedNode]:
        """Získá seed nodes pro daný typ sítě"""
        if network_type == "production":
            return cls.PRODUCTION_SEEDS.copy()
        elif network_type == "testnet":
            return cls.TESTNET_SEEDS.copy()
        elif network_type == "dev":
            return cls.DEV_SEEDS.copy()
        else:
            return cls.PRODUCTION_SEEDS.copy()
    
    @classmethod
    def get_seed_addresses(cls, network_type: str = "production") -> List[str]:
        """Získá seed adresy jako stringy pro zpětnou kompatibilitu"""
        seeds = cls.get_seed_nodes(network_type)
        return [seed.address for seed in seeds]
    
    @classmethod
    def get_available_seeds(cls, network_type: str = "production") -> List[SeedNode]:
        """Získá pouze dostupné seed nodes (s ping check)"""
        seeds = cls.get_seed_nodes(network_type)
        return [seed for seed in seeds if seed.is_available()]
    
    @classmethod
    def get_port(cls, service: str, network: str = "mainnet") -> int:
        """Získá port pro daný service"""
        key = f"{service}_{network}"
        return cls.PORTS.get(key, cls.PORTS.get(service, 8333))
    
    @classmethod
    def validate_configuration(cls) -> Dict[str, bool]:
        """Validace celé konfigurace"""
        checks = {}
        
        # Kontrola seed nodes
        checks['has_production_seeds'] = len(cls.PRODUCTION_SEEDS) >= 2  # Require at least 2 production seeds
        checks['has_testnet_seeds'] = len(cls.TESTNET_SEEDS) >= 2
        checks['has_unique_ports'] = len(set(cls.PORTS.values())) == len(cls.PORTS)
        
        # Kontrola portů
        production_ports = [seed.port for seed in cls.PRODUCTION_SEEDS]
        checks['no_port_conflicts'] = len(set(production_ports)) == len(production_ports)
        
        # Kontrola konfigurace
        checks['rpc_config_valid'] = cls.RPC_CONFIG['port'] > 1024
        checks['pool_config_valid'] = 0 < cls.POOL_CONFIG['fee_percent'] < 1
        checks['p2p_config_valid'] = cls.P2P_CONFIG['max_peers'] > 0
        
        return checks

# PREMINE ADRESY - UPDATED FOR HIRANYAGARBHA DAO
# Total premine: 14.34B ZION (was all mining operators)
# Now: 8.25B mining + 1.75B DAO winners + 4.34B infrastructure/dev/charity
ZION_PREMINE_ADDRESSES = {
    # MINING OPERATORS - 8.25B ZION distributed over 10 years
    'ZION_SACRED_B0FA7E2A234D8C2F08545F02295C98': {
        'purpose': 'Sacred Mining Operator - Consciousness Bonus Pool',
        'amount': 1_650_000_000,  # 1.65B ZION (20% of mining pool)
        'type': 'mining'
    },
    'ZION_QUANTUM_89D80B129682D41AD76DAE3F90C3E2': {
        'purpose': 'Quantum Mining Operator - Consciousness Bonus Pool', 
        'amount': 1_650_000_000,  # 1.65B ZION (20% of mining pool)
        'type': 'mining'
    },
    'ZION_COSMIC_397B032D6E2D3156F6F709E8179D36': {
        'purpose': 'Cosmic Mining Operator - Consciousness Bonus Pool',
        'amount': 1_650_000_000,  # 1.65B ZION (20% of mining pool)
        'type': 'mining'
    },
    'ZION_ENLIGHTENED_004A5DBD12FDCAACEDCB5384DDC035': {
        'purpose': 'Enlightened Mining Operator - Consciousness Bonus Pool',
        'amount': 1_650_000_000,  # 1.65B ZION (20% of mining pool)
        'type': 'mining'
    },
    'ZION_TRANSCENDENT_6BD30CB1835013503A8167D9CD86E0': {
        'purpose': 'Transcendent Mining Operator - Consciousness Bonus Pool',
        'amount': 1_650_000_000,  # 1.65B ZION (20% of mining pool)
        'type': 'mining'
    },
    # Subtotal Mining Operators: 8.25B ZION
    
    # HIRANYAGARBHA DAO WINNERS - 1.75B ZION (unlocks Oct 10, 2035)
    # NOTE: Voting weights are for YEAR 10 (2035) - Maitreya still has 70% at this point!
    # Winners share 30% of voting power (from 20-year DAO transition plan)
    'ZION_HIRANYAGARBHA_WINNER_1ST_GOLDEN_EGG_CEO': {
        'purpose': 'Chief Enlightenment Officer (Golden Egg Winner) - DAO Seat 1',
        'amount': 1_000_000_000,  # 1B ZION
        'type': 'dao_governance',
        'unlock_date': '2035-10-10',
        'voting_weight': 0.15,  # 15% of total (50% of 30% community share in 2035)
        'role': 'Chief Enlightenment Officer'
    },
    'ZION_HIRANYAGARBHA_WINNER_2ND_SILVER_SEEKER_CCO': {
        'purpose': 'Chief Consciousness Officer (XP Leader #1) - DAO Seat 2',
        'amount': 500_000_000,  # 500M ZION
        'type': 'dao_governance',
        'unlock_date': '2035-10-10',
        'voting_weight': 0.10,  # 10% of total (33% of 30% community share in 2035)
        'role': 'Chief Consciousness Officer'
    },
    'ZION_HIRANYAGARBHA_WINNER_3RD_BRONZE_BODHISATTVA_CAO': {
        'purpose': 'Chief Awakening Officer (XP Leader #2) - DAO Seat 3',
        'amount': 250_000_000,  # 250M ZION
        'type': 'dao_governance',
        'unlock_date': '2035-10-10',
        'voting_weight': 0.05,  # 5% of total (17% of 30% community share in 2035)
        'role': 'Chief Awakening Officer'
    },
    # Subtotal DAO Winners: 1.75B ZION, 30% voting power total (in 2035)
    
    # INFRASTRUCTURE & DEVELOPMENT - 4.34B ZION
    'ZION_DEVELOPMENT_TEAM_FUND_378614887FEA27791540F45': {
        'purpose': 'Development Team Fund - DAO Governance',
        'amount': 1_000_000_000,  # 1B ZION
        'type': 'development'
    },
    'ZION_NETWORK_INFRASTRUCTURE_SITA_B5F3BE9968A1D90': {
        'purpose': 'Network Infrastructure (SITA)',
        'amount': 1_000_000_000,  # 1B ZION
        'type': 'infrastructure'
    },
    'ZION_CHILDREN_FUTURE_FUND_1ECCB72BC30AADD086656A59': {
        'purpose': 'Children Future Fund - Humanitarian DAO',
        'amount': 1_000_000_000,  # 1B ZION
        'type': 'charity'
    },
    'ZION_MAITREYA_BUDDHA_DAO_ADMIN_D7A371ABD1FF1C5D42AB02': {
        'purpose': 'Maitreya Buddha - DAO Admin & Genesis Creator',
        'amount': 1_000_000_000,  # 1B ZION
        'type': 'admin',
        'voting_weight': 0.70,  # 70% in Year 10 (2035), per 20-year transition plan
        'veto_power': True,
        'transition_schedule': {
            'year_1_5': 1.00,    # 100% control (2025-2030)
            'year_6_12': 0.70,   # 70% control (2030-2037)
            'year_13_15': 0.50,  # 50% control (2037-2040)
            'year_16_18': 0.25,  # 25% control (2040-2043)
            'year_19_20': 0.10,  # 10% control (2043-2045)
            'year_21': 0.00      # Full DAO (2045+)
        }
    },
    'ZION_ON_THE_STAR_GENESIS_CREATOR_RENT_0B461AB5BCACC': {
        'purpose': 'Genesis Creator Lifetime Rent (0.33% of block rewards)',
        'amount': 342_857_143,  # 342.857M ZION
        'type': 'genesis'
    }
    # Subtotal Infrastructure: 4.34B ZION
}

# EKONOMICKÁ VALIDACE
PREMINE_TOTAL = sum(addr['amount'] for addr in ZION_PREMINE_ADDRESSES.values())
assert PREMINE_TOTAL == 14_342_857_143, f"Premine total mismatch! Expected 14.34B, got {PREMINE_TOTAL:,}"

MINING_OPERATORS_TOTAL = sum(addr['amount'] for addr in ZION_PREMINE_ADDRESSES.values() if addr['type'] == 'mining')
assert MINING_OPERATORS_TOTAL == 8_250_000_000, f"Mining operators mismatch! Expected 8.25B, got {MINING_OPERATORS_TOTAL:,}"

DAO_WINNERS_TOTAL = sum(addr['amount'] for addr in ZION_PREMINE_ADDRESSES.values() if addr['type'] == 'dao_governance')
assert DAO_WINNERS_TOTAL == 1_750_000_000, f"DAO winners mismatch! Expected 1.75B, got {DAO_WINNERS_TOTAL:,}"

# DAO VOTING WEIGHTS VALIDATION (for Year 10 - 2035)
DAO_VOTING_WEIGHTS = sum(addr.get('voting_weight', 0) for addr in ZION_PREMINE_ADDRESSES.values() if addr.get('voting_weight'))
assert abs(DAO_VOTING_WEIGHTS - 1.0) < 0.01, f"DAO voting weights mismatch! Expected 1.00, got {DAO_VOTING_WEIGHTS}"

print(f"✅ Premine validation OK:")
print(f"   Mining Operators: {MINING_OPERATORS_TOTAL:,} ZION")
print(f"   DAO Winners: {DAO_WINNERS_TOTAL:,} ZION (30% voting in 2035)")
print(f"   Infrastructure: {PREMINE_TOTAL - MINING_OPERATORS_TOTAL - DAO_WINNERS_TOTAL:,} ZION")
print(f"   TOTAL PREMINE: {PREMINE_TOTAL:,} ZION")
print(f"   DAO Voting (2035): Maitreya 70% + Winners 30% = {DAO_VOTING_WEIGHTS:.0%}")

# GLOBÁLNÍ FUNKCE PRO JEDNODUCHOU INTEGRACI
def get_seed_nodes(network_type: str = "production") -> List[str]:
    """Globální funkce pro získání seed nodes"""
    return ZionNetworkConfig.get_seed_addresses(network_type)

def get_p2p_port(network: str = "mainnet") -> int:
    """Globální funkce pro P2P port"""
    return ZionNetworkConfig.get_port("p2p", network)

def get_rpc_port(network: str = "mainnet") -> int:
    """Globální funkce pro RPC port"""
    return ZionNetworkConfig.get_port("rpc", network)

def get_pool_port(service: str = "stratum") -> int:
    """Globální funkce pro pool porty"""
    if service == "stratum":
        return ZionNetworkConfig.POOL_CONFIG['stratum_port']
    elif service == "api":
        return ZionNetworkConfig.POOL_CONFIG['api_port']
    return 3333

def get_premine_addresses() -> Dict:
    """Globální funkce pro premine adresy"""
    return ZION_PREMINE_ADDRESSES.copy()

def get_dao_config() -> Dict:
    """Globální funkce pro DAO governance konfiguraci"""
    return DAO_GOVERNANCE_CONFIG.copy()

def get_max_supply() -> int:
    """Globální funkce pro maximum supply"""
    return DAO_GOVERNANCE_CONFIG['max_supply']

def get_lightning_bridge_info() -> Dict:
    """Informace o Lightning Network a Rainbow Bridge konfiguraci"""
    return LIGHTNING_BRIDGE_INFO.copy()

# DAO GOVERNANCE CONFIGURATION - 50-YEAR ECONOMIC MODEL
DAO_GOVERNANCE_CONFIG = {
    'max_supply': 144_000_000_000,  # 144 billion ZION total over 50 years
    'premine_supply': 14_342_857_143,  # 14.34 billion premine (initial distribution)
    'mining_supply': 129_657_142_857,  # 129.66 billion to be mined over 50 years
    'emission_years': 50,  # 50-year emission schedule (2025-2075)
    'annual_mining_target': 2_593_142_857,  # Average 2.59B ZION per year
    
    'phases': {
        'phase_1_centralized': {
            'years': '2025-2030',
            'maitreya_control': 100,
            'dao_control': 0,
            'description': 'Full Maitreya Buddha control for network stability',
            'powers': [
                'emission_schedule_changes',
                'difficulty_adjustments', 
                'emergency_protocol_updates',
                'mining_algorithm_modifications',
                'fee_structure_changes',
                'consciousness_level_calibration'
            ]
        },
        'phase_2_hybrid': {
            'years': '2030-2037', 
            'maitreya_control': 70,
            'dao_control': 30,
            'description': 'Hybrid governance with DAO introduction',
            'features': [
                'community_proposals_system',
                'token_weighted_voting',
                'treasury_management',
                'governance_token_distribution'
            ]
        },
        'phase_3_transition': {
            'years': '2037-2045',
            'maitreya_control': [50, 25, 10],  # Declining over years
            'dao_control': [50, 75, 90],       # Rising over years
            'description': 'Gradual power transfer to DAO',
            'milestones': {
                'year_13_15': 'Equal governance (50/50)',
                'year_16_18': 'DAO majority (75/25)', 
                'year_19_20': 'DAO dominance (90/10)'
            }
        },
        'phase_4_full_dao': {
            'years': '2045+',
            'maitreya_control': 0,
            'dao_control': 100,
            'description': 'Complete decentralization',
            'features': [
                'full_community_governance',
                'smart_contract_automation',
                'transparent_voting_system',
                'community_managed_treasury'
            ]
        }
    },
    
    'voting_requirements': {
        'minor_changes': 'maitreya_approval',
        'major_changes': '60_percent_dao_plus_maitreya',
        'emergency': 'maitreya_override_24h_delay',
        'constitutional': '75_percent_dao_approval'
    },
    
    'treasury_allocation': {
        'development_fund': 1.0,        # 1 billion (7%)
        'infrastructure': 1.0,          # 1 billion (7%) 
        'humanitarian': 1.0,            # 1 billion (7%)
        'dao_transition': 1.0,          # 1 billion (7%)
        'mining_operators': 10.0,       # 10 billion (69.8%)
        'genesis_community': 0.343      # 343M (2.4%)
    },
    
    # MINING ECONOMIC MODEL - 50 YEAR EMISSION SCHEDULE
    'mining_config': {
        'base_block_reward': 5479.45,       # ZION per block (without consciousness multiplier)
        'base_reward_atomic': 5479452055,   # atomic units (5479.45 * 1M)
        'block_time_seconds': 60,           # 1 minute per block
        'blocks_per_year': 525600,          # 60*24*365 blocks
        'annual_base_emission': 2880000000, # 2.88B ZION per year at base rate
        'consciousness_multipliers': {
            'PHYSICAL': 1.0,
            'EMOTIONAL': 1.5,
            'MENTAL': 2.0,
            'SACRED': 3.0,
            'QUANTUM': 4.0,
            'COSMIC': 5.0,
            'ENLIGHTENED': 7.5,
            'TRANSCENDENT': 10.0,
            'ON_THE_STAR': 15.0
        },
        'average_consciousness_multiplier': 3.0,  # Expected network average
        'effective_annual_emission': 8640000000   # 8.64B ZION/year with 3x avg multiplier
    }
}

# EXPORT HLAVNÍCH KONSTANT PRO ZPĚTNOU KOMPATIBILITU
SEED_NODES_PRODUCTION = ZionNetworkConfig.get_seed_addresses("production")
SEED_NODES_TESTNET = ZionNetworkConfig.get_seed_addresses("testnet")
P2P_PORT = ZionNetworkConfig.PORTS['p2p_mainnet']
RPC_PORT = ZionNetworkConfig.PORTS['rpc_mainnet'] 
POOL_STRATUM_PORT = ZionNetworkConfig.POOL_CONFIG['stratum_port']
POOL_API_PORT = ZionNetworkConfig.POOL_CONFIG['api_port']

# DAO & TOKENOMICS EXPORTS
MAX_SUPPLY = DAO_GOVERNANCE_CONFIG['max_supply']
TOTAL_PREMINE = sum(addr['amount'] for addr in ZION_PREMINE_ADDRESSES.values())
CURRENT_DAO_PHASE = "phase_1_centralized"  # 2025-2030

# LIGHTNING & BRIDGE INTEGRATION INFO
LIGHTNING_BRIDGE_INFO = {
    'lightning_config_file': 'lightning_rainbow_config.py',
    'lightning_mainnet_port': 9735,
    'lightning_testnet_port': 9736,
    'bridge_chains_supported': 12,  # Bitcoin, Ethereum, Solana, Stellar, etc.
    'bridge_operator': 'ZION_BRIDGE_OPERATOR_SACRED_2025',
    'submarine_swaps_enabled': True,
    'atomic_swaps_enabled': True,
    'daily_bridge_limit': 10_000_000,  # 10M ZION
    'integration_status': 'production_ready'
}

if __name__ == "__main__":
    # Validace konfigurace při spuštění
    print("🔧 ZION Network Configuration Validation")
    print("=" * 50)
    
    checks = ZionNetworkConfig.validate_configuration()
    for check, result in checks.items():
        status = "✅" if result else "❌"
        print(f"{status} {check}: {result}")
    
    print(f"\n📡 Production Seed Nodes:")
    for seed in ZionNetworkConfig.PRODUCTION_SEEDS:
        print(f"   {seed.address} ({seed.type}, {seed.region})")
    
    print(f"\n🔌 Network Ports:")
    for service, port in ZionNetworkConfig.PORTS.items():
        print(f"   {service}: {port}")
    
    print(f"\n💰 Total Premine: {sum(addr['amount'] for addr in ZION_PREMINE_ADDRESSES.values()):,} ZION")