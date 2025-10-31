#!/usr/bin/env python3
"""
ZION Genesis Premine Configuration
15.78B ZION distribution for Genesis Block #0

This file contains ONLY premine addresses and genesis distribution logic.
For P2P network configuration, see seednodes.py
"""

from typing import Dict

# PREMINE ADDRESSES - UPDATED FOR HIRANYAGARBHA DAO + ZION OASIS
# Total premine: 15.78B ZION (was 14.34B before ZION OASIS)
# Distribution: 8.25B mining + 1.75B DAO winners + 1.44B ZION OASIS + 4.34B infrastructure
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
    },
    # Subtotal Infrastructure: 4.34B ZION
    
    # ZION OASIS - 1.44B ZION (Game Development Fund - 3 Year Release)
    'ZION_OASIS_GAME_DEVELOPMENT_FUND_AAA_MMORPG_2026': {
        'purpose': 'ZION OASIS AAA MMORPG + Kids Version + VR - 3 Year Development',
        'amount': 1_440_000_000,  # 1.44B ZION
        'type': 'oasis',
        'unlock_schedule': {
            'immediate_2026': 0.25,    # 360M ZION (Q1-Q4 2026) - Team hiring & pre-production
            'year_2_2027': 0.40,       # 576M ZION (Q1-Q4 2027) - Full development
            'year_3_2028': 0.35        # 504M ZION (Q1-Q4 2028) - Beta & Launch
        },
        'development_phases': {
            '2026_q1_q4': {
                'amount': 360_000_000,  # 360M ZION
                'purpose': 'Team assembly (250 people), Unreal Engine 5 setup, vertical slice',
                'quarterly': 90_000_000  # 90M per quarter
            },
            '2027_q1_q4': {
                'amount': 576_000_000,  # 576M ZION
                'purpose': '7 continents, 51 avatars, combat system, multiplayer',
                'quarterly': 144_000_000  # 144M per quarter
            },
            '2028_q1_q4': {
                'amount': 504_000_000,  # 504M ZION
                'purpose': 'Beta testing, polish, VR version, FULL LAUNCH Q4 2028',
                'quarterly': 126_000_000  # 126M per quarter
            }
        },
        'multisig_required': True,
        'dao_vote_required': True,
        'vesting_period': '36_months'  # 3 years total
    }
    # Subtotal ZION OASIS: 1.44B ZION (Unlocked over 3 years for game development)
}

# ECONOMIC VALIDATION
PREMINE_TOTAL = sum(addr['amount'] for addr in ZION_PREMINE_ADDRESSES.values())
assert PREMINE_TOTAL == 15_782_857_143, f"Premine total mismatch! Expected 15.78B, got {PREMINE_TOTAL:,}"

MINING_OPERATORS_TOTAL = sum(addr['amount'] for addr in ZION_PREMINE_ADDRESSES.values() if addr['type'] == 'mining')
assert MINING_OPERATORS_TOTAL == 8_250_000_000, f"Mining operators mismatch! Expected 8.25B, got {MINING_OPERATORS_TOTAL:,}"

DAO_WINNERS_TOTAL = sum(addr['amount'] for addr in ZION_PREMINE_ADDRESSES.values() if addr['type'] == 'dao_governance')
assert DAO_WINNERS_TOTAL == 1_750_000_000, f"DAO winners mismatch! Expected 1.75B, got {DAO_WINNERS_TOTAL:,}"

ZION_OASIS_TOTAL = sum(addr['amount'] for addr in ZION_PREMINE_ADDRESSES.values() if addr['type'] == 'oasis')
assert ZION_OASIS_TOTAL == 1_440_000_000, f"ZION OASIS mismatch! Expected 1.44B, got {ZION_OASIS_TOTAL:,}"

# DAO VOTING WEIGHTS VALIDATION (for Year 10 - 2035)
DAO_VOTING_WEIGHTS = sum(addr.get('voting_weight', 0) for addr in ZION_PREMINE_ADDRESSES.values() if addr.get('voting_weight'))
assert abs(DAO_VOTING_WEIGHTS - 1.0) < 0.01, f"DAO voting weights mismatch! Expected 1.00, got {DAO_VOTING_WEIGHTS}"

INFRASTRUCTURE_TOTAL = sum(addr['amount'] for addr in ZION_PREMINE_ADDRESSES.values() 
                           if addr['type'] in ['development', 'infrastructure', 'charity', 'admin', 'genesis'])

print(f"✅ Premine validation OK:")
print(f"   Mining Operators: {MINING_OPERATORS_TOTAL:,} ZION (52.3%)")
print(f"   DAO Winners: {DAO_WINNERS_TOTAL:,} ZION (11.1% - 30% voting in 2035)")
print(f"   ZION OASIS: {ZION_OASIS_TOTAL:,} ZION (9.1% - Game Development Fund)")
print(f"   Infrastructure: {INFRASTRUCTURE_TOTAL:,} ZION (27.5%)")
print(f"   TOTAL PREMINE: {PREMINE_TOTAL:,} ZION (100%)")
print(f"   DAO Voting (2035): Maitreya 70% + Winners 30% = {DAO_VOTING_WEIGHTS:.0%}")


# GLOBAL HELPER FUNCTIONS
def get_premine_addresses() -> Dict:
    """Get all premine addresses for genesis block distribution"""
    return ZION_PREMINE_ADDRESSES.copy()


def get_premine_total() -> int:
    """Get total premine amount (15.78B ZION)"""
    return PREMINE_TOTAL


def get_premine_by_type(addr_type: str) -> Dict:
    """Get premine addresses filtered by type
    
    Args:
        addr_type: One of 'mining', 'dao_governance', 'oasis', 'development', 
                   'infrastructure', 'charity', 'admin', 'genesis'
    
    Returns:
        Dict of addresses matching the type
    """
    return {addr: info for addr, info in ZION_PREMINE_ADDRESSES.items() 
            if info.get('type') == addr_type}


def validate_premine() -> bool:
    """Validate that all premine calculations are correct
    
    Returns:
        True if all validations pass
    """
    try:
        assert PREMINE_TOTAL == 15_782_857_143
        assert MINING_OPERATORS_TOTAL == 8_250_000_000
        assert DAO_WINNERS_TOTAL == 1_750_000_000
        assert ZION_OASIS_TOTAL == 1_440_000_000
        assert abs(DAO_VOTING_WEIGHTS - 1.0) < 0.01
        return True
    except AssertionError:
        return False


# Run validation on import
if __name__ == "__main__":
    print("\n🔍 ZION PREMINE CONFIGURATION TEST")
    print("=" * 70)
    print(f"Total Addresses: {len(ZION_PREMINE_ADDRESSES)}")
    print(f"Total Premine: {PREMINE_TOTAL:,} ZION")
    print(f"Validation: {'✅ PASS' if validate_premine() else '❌ FAIL'}")
