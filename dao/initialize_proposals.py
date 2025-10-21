#!/usr/bin/env python3
"""
Initialize ZION Humanitarian DAO - Version 2.7.1 Projects

This script creates the original 5 humanitarian projects (10% tithe, equal 2% each):
1. 🌲 Zalesňování pralesů (Forest Restoration) - 2%
2. 🌊 Vyčištění oceánů (Ocean Cleanup) - 2%
3. ❤️ Humanitární pomoc (Humanitarian Aid) - 2%
4. 🚀 Space Program (Cosmic Research) - 2%
5. 🕉️ Dharma vývoj (Sacred Garden Portugal) - 2%

Total: 10% of mining rewards distributed equally across 5 projects
"""

import sys
import time
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dao.humanitarian_dao import HumanitarianDAO, ProjectCategory


def initialize_dao_with_proposals():
    """Create DAO and add initial 5 proposals"""
    
    print("=" * 70)
    print("🌍 ZION HUMANITARIAN DAO - INITIALIZATION")
    print("=" * 70)
    print()
    
    # Initialize DAO
    dao = HumanitarianDAO()
    
    # Add initial treasury funds (simulated from first blocks)
    print("💰 Funding treasury with initial tithe from mining...")
    dao.add_to_treasury(1000000.0, block_height=1, description="Initial treasury funding from first blocks")
    print()
    
    # Show fee schedule
    fee_info = HumanitarianDAO.get_fee_schedule_info()
    print(f"📊 Current Humanitarian Fee: {fee_info['current_fee_percentage']}%")
    print(f"📅 Network Age: {fee_info['network_age_years']:.2f} years ({fee_info['days_since_genesis']} days)")
    if fee_info['days_until_next_tier'] > 0:
        print(f"⏭️  Next tier ({fee_info['next_tier_percentage']}%) in {fee_info['days_until_next_tier']} days")
    print()
    print("Fee Schedule:")
    for tier in fee_info['schedule']:
        print(f"  Year {tier['year']}: {tier['fee']} (days {tier['days']})")
    print()
    print("=" * 70)
    print()
    
    # ZION to USD conversion rate (example: 1 ZION = $0.50)
    zion_to_usd = 0.50
    
    # Each project gets 2% of the 10% humanitarian tithe
    # With 1M ZION treasury, each project gets 200K ZION
    project_allocation = 200000  # ZION per project
    
    # Proposal 1: 🌲 Forest Restoration (Zalesňování pralesů)
    print("Creating Proposal #1: Forest Restoration (Zalesňování pralesů)...")
    proposal1 = dao.create_proposal(
        title="🌲 Zalesňování pralesů - Global Reforestation",
        description="""
🌲 PROJECT OVERVIEW:
Global forest restoration initiative focusing on tropical rainforests and sacred groves.

📍 IMPACT:
- 2 million native trees planted annually
- 5,000 acres reforested per year
- Absorbs ~50,000 tons CO2 annually
- Restores biodiversity in 10 countries
- Creates jobs for 500 indigenous families
- Protects water sources and prevents soil erosion

💰 BUDGET (2% of humanitarian tithe):
- Seedling cultivation: $30,000
- Planting labor (local communities): $40,000
- Site preparation & maintenance: $20,000
- GPS mapping & monitoring: $8,000
- Project coordination: $2,000
Total: $100,000 annually

🤝 PARTNER ORGANIZATIONS:
- Amazon Conservation Association
- One Tree Planted
- Local indigenous communities

⏱️ ONGOING PROGRAM:
Continuous reforestation with quarterly reporting

📸 VERIFICATION:
- Satellite imagery (before/after)
- GPS coordinates
- Quarterly progress reports
        """.strip(),
        category=ProjectCategory.ENVIRONMENT,
        recipient_address="ZION_FOREST_RESTORATION_GLOBAL_2024",
        recipient_organization="Forest Restoration Alliance",
        amount_zion=project_allocation,
        amount_usd=project_allocation * zion_to_usd,
        location="Global (Amazon, Southeast Asia, Africa)",
        beneficiaries=500,
        proposer_address="ZION_DAO_ADMIN_001"
    )
    print()
    
    # Proposal 2: 🌊 Ocean Cleanup (Vyčištění oceánů)
    print("Creating Proposal #2: Ocean Cleanup (Vyčištění oceánů)...")
    proposal2 = dao.create_proposal(
        title="🌊 Vyčištění oceánů - Ocean Plastic Removal",
        description="""
� PROJECT OVERVIEW:
Global ocean cleanup initiative removing plastic waste and restoring marine ecosystems.

📍 IMPACT:
- 1,000 tons of ocean plastic removed annually
- Coral reef restoration (50 hectares)
- Marine wildlife protection
- Beach cleanup operations in 20 coastal regions
- Microplastic filtration systems deployed
- Educational programs for coastal communities

💰 BUDGET (2% of humanitarian tithe):
- Cleanup vessels & equipment: $40,000
- Beach cleanup operations: $25,000
- Coral restoration: $20,000
- Microplastic filtration: $10,000
- Community education: $5,000
Total: $100,000 annually

🤝 PARTNER ORGANIZATIONS:
- Ocean Cleanup Foundation
- Coral Restoration Foundation
- Local marine conservation groups

⏱️ ONGOING PROGRAM:
Year-round ocean cleanup with quarterly impact reports

📸 VERIFICATION:
- Plastic removed (weight/volume)
- Before/after underwater footage
- Coral health assessments
- Marine biodiversity surveys
        """.strip(),
        category=ProjectCategory.ENVIRONMENT,
        recipient_address="ZION_OCEAN_CLEANUP_GLOBAL_2024",
        recipient_organization="Ocean Cleanup Alliance",
        amount_zion=project_allocation,
        amount_usd=project_allocation * zion_to_usd,
        location="Global Oceans (Pacific, Atlantic, Indian)",
        beneficiaries=1000,
        proposer_address="ZION_DAO_ADMIN_001"
    )
    print()
    
    # Proposal 3: ❤️ Humanitarian Aid (Humanitární pomoc)
    print("Creating Proposal #3: Humanitarian Aid (Humanitární pomoc)...")
    proposal3 = dao.create_proposal(
        title="❤️ Humanitární pomoc - Emergency Relief & Children Support",
        description="""
❤️ PROJECT OVERVIEW:
Emergency humanitarian aid for crisis regions plus ongoing support for children's education and healthcare.

📍 IMPACT:
- Emergency relief in disaster zones
- 10,000 children supported with education & meals
- Medical supplies to 50 clinics
- Clean water access for 20 communities
- Shelter for displaced families
- Food security programs

💰 BUDGET (2% of humanitarian tithe):
- Emergency relief supplies: $30,000
- Children education & meals: $35,000
- Medical supplies: $20,000
- Clean water projects: $10,000
- Administrative costs: $5,000
Total: $100,000 annually

🤝 PARTNER ORGANIZATIONS:
- UNICEF
- Red Cross/Red Crescent
- Save the Children
- Local NGOs

⏱️ ONGOING PROGRAM:
Continuous humanitarian support with rapid emergency response capability

📸 VERIFICATION:
- Beneficiary counts
- Supply distribution logs
- School attendance records
- Health improvement metrics
- Emergency response reports
        """.strip(),
        category=ProjectCategory.MEDICAL,
        recipient_address="ZION_HUMANITARIAN_AID_GLOBAL_2024",
        recipient_organization="Humanitarian Aid Alliance",
        amount_zion=project_allocation,
        amount_usd=project_allocation * zion_to_usd,
        location="Global Crisis Regions",
        beneficiaries=10000,
        proposer_address="ZION_DAO_ADMIN_001"
    )
    print()
    
    # Proposal 4: 🚀 Space Program (Cosmic Research)
    print("Creating Proposal #4: Space Program (Cosmic Research)...")
    proposal4 = dao.create_proposal(
        title="🚀 Space Program - Cosmic Research & Education",
        description="""
🚀 PROJECT OVERVIEW:
Support space research, cosmic consciousness studies, and STEM education programs inspiring future generations.

📍 IMPACT:
- Space science education for 5,000 students
- Telescope access programs (100 schools)
- Cosmic consciousness research
- Collaboration with space agencies
- Astronomy outreach events
- Scholarships for aspiring astronauts/scientists

💰 BUDGET (2% of humanitarian tithe):
- Educational programs & materials: $40,000
- Telescope equipment for schools: $30,000
- Research grants: $15,000
- Scholarships: $10,000
- Outreach events: $5,000
Total: $100,000 annually

🤝 PARTNER ORGANIZATIONS:
- NASA Education Programs
- European Space Agency (ESA)
- International Astronomical Union
- Universities with space programs

⏱️ ONGOING PROGRAM:
Year-round STEM education with annual space research grants

📸 VERIFICATION:
- Student participation numbers
- Telescope installations
- Research papers published
- Scholarship recipients
- Event attendance
        """.strip(),
        category=ProjectCategory.EDUCATION,
        recipient_address="ZION_SPACE_PROGRAM_EDUCATION_2024",
        recipient_organization="Cosmic Education Foundation",
        amount_zion=project_allocation,
        amount_usd=project_allocation * zion_to_usd,
        location="Global (with focus on underserved regions)",
        beneficiaries=5000,
        proposer_address="ZION_DAO_ADMIN_001"
    )
    print()
    
    # Proposal 5: 🕉️ Dharma Development (Sacred Garden Portugal)
    print("Creating Proposal #5: Dharma Development (Sacred Garden Portugal)...")
    proposal5 = dao.create_proposal(
        title="🕉️ Dharma vývoj - Sacred Garden Portugal Development",
        description="""
🕉️ PROJECT OVERVIEW:
Develop Sacred Garden spiritual center in Portugal for meditation retreats, dharma teachings, and community gathering.

📍 IMPACT:
- Sacred meditation garden (10,000 m²)
- Retreat center for 50 guests
- Dharma library with ancient texts
- Permaculture food forest
- Renewable energy systems
- Community gathering space
- Free meditation classes for locals

💰 BUDGET (2% of humanitarian tithe):
- Land development & gardens: $40,000
- Retreat center construction: $30,000
- Permaculture systems: $15,000
- Solar/renewable energy: $10,000
- Library & teaching materials: $5,000
Total: $100,000 annually

🤝 PARTNERSHIP:
Sacred Garden Portugal Foundation (established 2024)
Focus on dharma, meditation, and sustainable living

⏱️ ONGOING PROGRAM:
Multi-year development with Phase 1 beginning 2025

📸 VERIFICATION:
- Construction progress photos
- Retreat participant numbers
- Community event attendance
- Permaculture yields
- Energy generation data
- Testimonials from visitors

🌟 VISION:
Create a sacred space for consciousness expansion, connecting ancient wisdom with modern sustainable living. A place where seekers can retreat, learn, and grow spiritually while contributing to local community well-being.
        """.strip(),
        category=ProjectCategory.EDUCATION,
        recipient_address="ZION_SACRED_GARDEN_PORTUGAL_2024",
        recipient_organization="Sacred Garden Portugal Foundation",
        amount_zion=project_allocation,
        amount_usd=project_allocation * zion_to_usd,
        location="Portugal (Sacred Garden Site)",
        beneficiaries=200,  # Direct retreat guests + local community
        proposer_address="ZION_DAO_ADMIN_001"
    )
    print()
    
    print("=" * 70)
    print("✅ DAO INITIALIZATION COMPLETE!")
    print("=" * 70)
    print()
    print(f"📊 Treasury Balance: {dao.get_treasury_balance():.8f} ZION")
    print(f"📋 Total Proposals: 5")
    print()
    
    # Summary
    total_requested = proposal1.amount_zion + proposal2.amount_zion + proposal3.amount_zion + \
                      proposal4.amount_zion + proposal5.amount_zion
    total_usd = proposal1.amount_usd + proposal2.amount_usd + proposal3.amount_usd + \
                proposal4.amount_usd + proposal5.amount_usd
    total_beneficiaries = proposal1.beneficiaries + proposal2.beneficiaries + \
                          proposal3.beneficiaries + proposal4.beneficiaries + proposal5.beneficiaries
    
    print(f"💰 Total Requested: {total_requested:.8f} ZION (${total_usd:,.0f})")
    print(f"👥 Total Beneficiaries: {total_beneficiaries:,} people worldwide")
    print()
    print("🗳️  Voting is now open! Community members can vote on these proposals.")
    print()
    print("Next steps:")
    print("1. Share proposals with ZION community")
    print("2. Collect votes (7-day voting period)")
    print("3. Execute approved proposals")
    print("4. Track impact and report results")
    print()
    print("=" * 70)
    
    return dao


def export_proposals_to_json(dao: HumanitarianDAO):
    """Export all proposals to JSON for frontend"""
    print("\n📄 Exporting proposals to JSON...")
    
    proposals = dao.get_all_proposals()
    output_dir = Path(__file__).parent.parent / "dao" / "proposals"
    output_dir.mkdir(exist_ok=True)
    
    for proposal in proposals:
        filename = f"proposal_{proposal.id:03d}.json"
        filepath = output_dir / filename
        dao.export_proposal_json(proposal.id, str(filepath))
    
    # Create summary JSON
    summary = {
        "total_proposals": len(proposals),
        "treasury_balance": dao.get_treasury_balance(),
        "proposals": [
            {
                "id": p.id,
                "title": p.title,
                "category": p.category,
                "amount_usd": p.amount_usd,
                "beneficiaries": p.beneficiaries,
                "location": p.location,
                "status": p.status,
                "approval_percentage": p.vote_percentage()
            }
            for p in proposals
        ]
    }
    
    summary_path = output_dir / "summary.json"
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"✅ Exported {len(proposals)} proposals to {output_dir}")


if __name__ == "__main__":
    dao = initialize_dao_with_proposals()
    export_proposals_to_json(dao)
