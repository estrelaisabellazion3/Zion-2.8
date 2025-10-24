#!/usr/bin/env python3
"""
ZION WARP Bridge - Proof of Concept
Test integration of Ankr + Voltage + OpenNode + Lightspark

This is a working PoC demonstrating:
1. Ankr RPC calls for multi-chain access
2. Voltage Lightning node management
3. OpenNode payment processing
4. Cross-chain WARP transfers

Run: python3 warp_bridge_poc.py --test
"""

import asyncio
import aiohttp
import time
import json
from typing import Dict, Optional, Any, List
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime


# =============================================================================
# CONFIGURATION
# =============================================================================

class Config:
    """Configuration for WARP Bridge PoC"""
    
    # Ankr Configuration (Replace with your API key)
    ANKR_API_KEY = "YOUR_ANKR_API_KEY"  # Get from https://www.ankr.com
    ANKR_BASE_URL = "https://rpc.ankr.com"
    
    # Voltage Configuration (Replace with your API key)
    VOLTAGE_API_KEY = "YOUR_VOLTAGE_API_KEY"  # Get from https://www.voltage.cloud
    VOLTAGE_BASE_URL = "https://api.voltage.cloud/v1"
    
    # OpenNode Configuration (Replace with your API key)
    OPENNODE_API_KEY = "YOUR_OPENNODE_API_KEY"  # Get from https://opennode.com
    OPENNODE_BASE_URL = "https://api.opennode.com/v1"
    
    # Lightspark Configuration (Optional)
    LIGHTSPARK_API_KEY = None  # Get from https://www.lightspark.com
    LIGHTSPARK_BASE_URL = "https://api.lightspark.com"
    
    # Test mode (uses mock data)
    TEST_MODE = True


# =============================================================================
# DATA MODELS
# =============================================================================

class WarpChainType(Enum):
    """Supported blockchain types via Ankr"""
    ZION = "zion"
    ETHEREUM = "eth"
    POLYGON = "polygon"
    ARBITRUM = "arbitrum"
    OPTIMISM = "optimism"
    AVALANCHE = "avalanche"
    BSC = "bsc"
    SOLANA = "solana"
    FANTOM = "fantom"
    GNOSIS = "gnosis"

@dataclass
class WarpTransaction:
    """WARP transfer transaction record"""
    tx_id: str
    source_chain: WarpChainType
    destination_chain: WarpChainType
    amount: float
    asset: str
    status: str
    lightning_payment_hash: Optional[str] = None
    ankr_rpc_calls: int = 0
    total_time_ms: int = 0
    fee_total: float = 0.0
    timestamp: str = ""
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()

@dataclass
class LightningNode:
    """Lightning node information"""
    node_id: str
    pubkey: str
    status: str
    capacity_sats: int
    num_channels: int
    rpc_url: str

@dataclass
class PaymentCharge:
    """OpenNode payment charge"""
    charge_id: str
    amount_usd: float
    checkout_url: str
    lightning_invoice: str
    status: str
    expires_at: str


# =============================================================================
# MOCK SERVICES (for testing without real API keys)
# =============================================================================

class MockAnkrClient:
    """Mock Ankr client for testing"""
    
    async def get_block_number(self, chain: str) -> int:
        """Get latest block number"""
        await asyncio.sleep(0.056)  # Simulate 56ms response
        return 12345678 + hash(chain) % 10000
    
    async def get_balance(self, chain: str, address: str) -> float:
        """Get address balance"""
        await asyncio.sleep(0.056)
        return 1000.0 + hash(address) % 5000
    
    async def call_contract(self, chain: str, contract: str, method: str, params: list) -> Dict:
        """Call smart contract"""
        await asyncio.sleep(0.056)
        return {
            'transactionHash': f"0x{'a' * 64}",
            'proof': f"0x{'b' * 128}",
            'status': 'success'
        }

class MockVoltageClient:
    """Mock Voltage client for testing"""
    
    async def create_node(self, config: Dict) -> LightningNode:
        """Create Lightning node"""
        await asyncio.sleep(1.0)  # Simulate 1 second deployment
        return LightningNode(
            node_id="voltage_test_node_001",
            pubkey="02a1b2c3d4e5f6" + "0" * 52,
            status="online",
            capacity_sats=50_000_000,
            num_channels=20,
            rpc_url="https://test-node.voltage.cloud:10009"
        )
    
    async def pay_invoice(self, amount_sats: int, memo: str) -> Dict:
        """Pay Lightning invoice"""
        await asyncio.sleep(0.8)  # Simulate 800ms payment
        return {
            'payment_hash': '0x' + 'c' * 64,
            'fee_sats': int(amount_sats * 0.001),
            'route_hops': 3,
            'status': 'succeeded'
        }

class MockOpenNodeClient:
    """Mock OpenNode client for testing"""
    
    async def create_charge(self, amount: float, description: str) -> PaymentCharge:
        """Create payment charge"""
        await asyncio.sleep(0.2)
        charge_id = f"ch_{int(time.time())}"
        return PaymentCharge(
            charge_id=charge_id,
            amount_usd=amount,
            checkout_url=f"https://checkout.opennode.com/{charge_id}",
            lightning_invoice=f"lnbc{int(amount*100000)}n1...",
            status="pending",
            expires_at=datetime.now().isoformat()
        )


# =============================================================================
# REAL API CLIENTS
# =============================================================================

class AnkrClient:
    """Real Ankr RPC client"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = Config.ANKR_BASE_URL
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def call_rpc(self, chain: str, method: str, params: list) -> Dict:
        """Make RPC call to Ankr"""
        url = f"{self.base_url}/{chain}"
        
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        async with self.session.post(url, json=payload, headers=headers) as resp:
            return await resp.json()
    
    async def get_block_number(self, chain: str) -> int:
        """Get latest block number"""
        result = await self.call_rpc(chain, "eth_blockNumber", [])
        return int(result['result'], 16)
    
    async def get_balance(self, chain: str, address: str) -> float:
        """Get address balance"""
        result = await self.call_rpc(chain, "eth_getBalance", [address, "latest"])
        balance_wei = int(result['result'], 16)
        return balance_wei / 1e18


# =============================================================================
# MAIN WARP BRIDGE
# =============================================================================

class ZIONWarpBridgePoC:
    """
    ZION WARP Bridge - Proof of Concept
    
    Demonstrates complete integration of:
    - Ankr: Multi-chain RPC access
    - Voltage: Lightning Network nodes
    - OpenNode: Payment processing
    - Lightspark: Enterprise features (optional)
    """
    
    def __init__(self, test_mode: bool = True):
        self.test_mode = test_mode
        
        # Initialize clients (mock or real)
        if test_mode:
            print("⚠️  TEST MODE: Using mock clients")
            self.ankr = MockAnkrClient()
            self.voltage = MockVoltageClient()
            self.opennode = MockOpenNodeClient()
        else:
            print("✅ PRODUCTION MODE: Using real API clients")
            self.ankr = AnkrClient(Config.ANKR_API_KEY)
            # TODO: Add real Voltage and OpenNode clients
        
        # State
        self.lightning_node: Optional[LightningNode] = None
        self.metrics = {
            'total_warp_transfers': 0,
            'total_volume_usd': 0.0,
            'avg_transfer_time_ms': 0,
            'ankr_rpc_calls': 0,
            'lightning_payments': 0,
            'warp_speed_count': 0  # Transfers < 2s
        }
    
    async def initialize(self):
        """Initialize WARP Bridge"""
        print("\n" + "="*70)
        print("🌌 INITIALIZING ZION WARP BRIDGE 🌌")
        print("="*70)
        
        # Step 1: Test Ankr connectivity
        print("\n1️⃣  Testing Ankr RPC connectivity...")
        try:
            block = await self.ankr.get_block_number('eth')
            print(f"   ✅ Ankr connected! Latest Ethereum block: {block:,}")
            self.metrics['ankr_rpc_calls'] += 1
        except Exception as e:
            print(f"   ❌ Ankr error: {e}")
            if not self.test_mode:
                raise
        
        # Step 2: Deploy Lightning node
        print("\n2️⃣  Deploying Lightning node via Voltage...")
        try:
            self.lightning_node = await self.voltage.create_node({
                'name': 'ZION-WARP-Test-Node',
                'type': 'lnd',
                'region': 'auto',
                'size': 'standard'
            })
            print(f"   ✅ Lightning node deployed!")
            print(f"      Node ID: {self.lightning_node.node_id}")
            print(f"      Pubkey: {self.lightning_node.pubkey[:20]}...")
            print(f"      Status: {self.lightning_node.status}")
            print(f"      Channels: {self.lightning_node.num_channels}")
        except Exception as e:
            print(f"   ❌ Voltage error: {e}")
            if not self.test_mode:
                raise
        
        # Step 3: Test OpenNode
        print("\n3️⃣  Testing OpenNode payment processing...")
        try:
            test_charge = await self.opennode.create_charge(
                amount=10.0,
                description="ZION Test Payment"
            )
            print(f"   ✅ OpenNode connected!")
            print(f"      Charge ID: {test_charge.charge_id}")
            print(f"      Amount: ${test_charge.amount_usd}")
        except Exception as e:
            print(f"   ❌ OpenNode error: {e}")
            if not self.test_mode:
                raise
        
        print("\n" + "="*70)
        print("✅ WARP BRIDGE INITIALIZED SUCCESSFULLY!")
        print("="*70 + "\n")
    
    async def warp_transfer(
        self,
        from_chain: WarpChainType,
        to_chain: WarpChainType,
        amount: float,
        asset: str = "ZION"
    ) -> WarpTransaction:
        """
        Execute WARP transfer between chains
        
        Target: < 2 seconds for WARP SPEED! ⚡
        """
        start_time = time.time()
        
        print("\n" + "🌌"*35)
        print("🌌 WARP TRANSFER INITIATED 🌌".center(70))
        print("🌌"*35)
        print(f"\n   Source: {from_chain.value.upper()}")
        print(f"   Destination: {to_chain.value.upper()}")
        print(f"   Amount: {amount:,.2f} {asset}")
        print(f"   Target: < 2000ms (WARP SPEED)")
        print("\n" + "-"*70)
        
        rpc_calls = 0
        
        # Phase 1: Lock on source chain (via Ankr)
        print("\n📍 Phase 1: Locking assets on source chain...")
        phase1_start = time.time()
        try:
            # Check balance first
            balance = await self.ankr.get_balance(
                from_chain.value,
                "0x" + "1" * 40  # Test address
            )
            rpc_calls += 1
            
            # Lock transaction
            lock_result = await self.ankr.call_contract(
                chain=from_chain.value,
                contract="0x" + "BRIDGE" + "0" * 34,
                method="lock",
                params=[amount, asset]
            )
            rpc_calls += 1
            
            phase1_time = int((time.time() - phase1_start) * 1000)
            print(f"   ✅ Locked {amount} {asset}")
            print(f"   📊 Balance verified: {balance:,.2f}")
            print(f"   ⏱️  Time: {phase1_time}ms")
            print(f"   🔗 TX: {lock_result['transactionHash'][:16]}...")
        except Exception as e:
            print(f"   ❌ Lock failed: {e}")
            raise
        
        # Phase 2: Lightning Network transfer
        print("\n⚡ Phase 2: Lightning Network instant transfer...")
        phase2_start = time.time()
        try:
            # Convert to satoshis (example rate)
            amount_sats = int(amount * 100_000)
            
            payment = await self.voltage.pay_invoice(
                amount_sats=amount_sats,
                memo=f"WARP: {from_chain.value} → {to_chain.value}"
            )
            
            phase2_time = int((time.time() - phase2_start) * 1000)
            print(f"   ✅ Lightning payment succeeded")
            print(f"   ⚡ Payment hash: {payment['payment_hash'][:16]}...")
            print(f"   ⏱️  Time: {phase2_time}ms")
            print(f"   💰 Fee: {payment['fee_sats']} sats")
            print(f"   🛣️  Route hops: {payment['route_hops']}")
            
            self.metrics['lightning_payments'] += 1
        except Exception as e:
            print(f"   ❌ Lightning payment failed: {e}")
            raise
        
        # Phase 3: Mint on destination chain (via Ankr)
        print("\n🎯 Phase 3: Minting on destination chain...")
        phase3_start = time.time()
        try:
            mint_result = await self.ankr.call_contract(
                chain=to_chain.value,
                contract="0x" + "BRIDGE" + "0" * 34,
                method="mint",
                params=[amount, asset, lock_result['proof']]
            )
            rpc_calls += 1
            
            phase3_time = int((time.time() - phase3_start) * 1000)
            print(f"   ✅ Minted {amount} {asset}")
            print(f"   ⏱️  Time: {phase3_time}ms")
            print(f"   🔗 TX: {mint_result['transactionHash'][:16]}...")
        except Exception as e:
            print(f"   ❌ Mint failed: {e}")
            raise
        
        # Calculate totals
        total_time = int((time.time() - start_time) * 1000)
        is_warp_speed = total_time < 2000
        
        print("\n" + "-"*70)
        print("\n" + "="*70)
        if is_warp_speed:
            print("🎉 WARP SPEED ACHIEVED! ⚡".center(70))
        else:
            print("✅ TRANSFER COMPLETE".center(70))
        print("="*70)
        
        # Summary
        print(f"\n   Total Time: {total_time}ms ({total_time/1000:.2f}s)")
        print(f"   Status: {'⚡ WARP SPEED' if is_warp_speed else '✅ Success'}")
        print(f"   Ankr RPC Calls: {rpc_calls}")
        print(f"   Lightning Fee: {payment['fee_sats']} sats")
        print(f"   Speed Rating: {'💥 SUPERNOVA' if total_time < 1500 else '⚡ WARP' if is_warp_speed else '🐢 Standard'}")
        print("\n" + "="*70 + "\n")
        
        # Create transaction record
        tx = WarpTransaction(
            tx_id=f"WARP-{int(time.time())}",
            source_chain=from_chain,
            destination_chain=to_chain,
            amount=amount,
            asset=asset,
            status='completed',
            lightning_payment_hash=payment['payment_hash'],
            ankr_rpc_calls=rpc_calls,
            total_time_ms=total_time,
            fee_total=payment['fee_sats'] / 100_000_000
        )
        
        # Update metrics
        self._update_metrics(tx, is_warp_speed)
        
        return tx
    
    async def create_payment(
        self,
        product_name: str,
        price_usd: float,
        customer_email: str = "test@zion.network"
    ) -> PaymentCharge:
        """
        Create eCommerce payment via OpenNode
        """
        print("\n" + "💰"*35)
        print("💰 CREATING PAYMENT CHARGE 💰".center(70))
        print("💰"*35)
        print(f"\n   Product: {product_name}")
        print(f"   Price: ${price_usd:.2f}")
        print(f"   Customer: {customer_email}")
        print("\n" + "-"*70 + "\n")
        
        charge = await self.opennode.create_charge(
            amount=price_usd,
            description=product_name
        )
        
        print("✅ Payment charge created!")
        print(f"\n   Charge ID: {charge.charge_id}")
        print(f"   Checkout URL: {charge.checkout_url}")
        print(f"   Lightning Invoice: {charge.lightning_invoice[:30]}...")
        print(f"   Status: {charge.status}")
        print(f"   Expires: {charge.expires_at}")
        print("\n" + "="*70 + "\n")
        
        return charge
    
    def _update_metrics(self, tx: WarpTransaction, is_warp_speed: bool):
        """Update metrics"""
        n = self.metrics['total_warp_transfers']
        old_avg = self.metrics['avg_transfer_time_ms']
        
        self.metrics['total_warp_transfers'] += 1
        self.metrics['total_volume_usd'] += tx.amount  # Simplified
        self.metrics['avg_transfer_time_ms'] = (old_avg * n + tx.total_time_ms) / (n + 1)
        self.metrics['ankr_rpc_calls'] += tx.ankr_rpc_calls
        
        if is_warp_speed:
            self.metrics['warp_speed_count'] += 1
    
    def get_stats(self) -> Dict[str, Any]:
        """Get WARP Bridge statistics"""
        warp_speed_percentage = (
            (self.metrics['warp_speed_count'] / max(1, self.metrics['total_warp_transfers'])) * 100
        )
        
        return {
            'transfers': {
                'total': self.metrics['total_warp_transfers'],
                'warp_speed_count': self.metrics['warp_speed_count'],
                'warp_speed_percentage': f"{warp_speed_percentage:.1f}%",
                'total_volume_usd': f"${self.metrics['total_volume_usd']:,.2f}",
                'avg_time_ms': f"{self.metrics['avg_transfer_time_ms']:.0f}ms"
            },
            'infrastructure': {
                'ankr_rpc_calls': self.metrics['ankr_rpc_calls'],
                'lightning_payments': self.metrics['lightning_payments'],
                'lightning_node': self.lightning_node.node_id if self.lightning_node else None
            },
            'performance': {
                'warp_capable': self.metrics['avg_transfer_time_ms'] < 2000,
                'avg_below_target': self.metrics['avg_transfer_time_ms'] < 2000
            }
        }
    
    def print_stats(self):
        """Print formatted statistics"""
        stats = self.get_stats()
        
        print("\n" + "📊"*35)
        print("📊 WARP BRIDGE STATISTICS 📊".center(70))
        print("📊"*35 + "\n")
        
        print("TRANSFERS:")
        print(f"   Total: {stats['transfers']['total']}")
        print(f"   WARP Speed (< 2s): {stats['transfers']['warp_speed_count']} ({stats['transfers']['warp_speed_percentage']})")
        print(f"   Total Volume: {stats['transfers']['total_volume_usd']}")
        print(f"   Average Time: {stats['transfers']['avg_time_ms']}")
        
        print("\nINFRASTRUCTURE:")
        print(f"   Ankr RPC Calls: {stats['infrastructure']['ankr_rpc_calls']}")
        print(f"   Lightning Payments: {stats['infrastructure']['lightning_payments']}")
        print(f"   Lightning Node: {stats['infrastructure']['lightning_node']}")
        
        print("\nPERFORMANCE:")
        print(f"   WARP Capable: {'✅ YES' if stats['performance']['warp_capable'] else '❌ NO'}")
        print(f"   Below Target: {'✅ YES' if stats['performance']['avg_below_target'] else '❌ NO'}")
        
        print("\n" + "="*70 + "\n")


# =============================================================================
# TEST SCENARIOS
# =============================================================================

async def test_scenario_1_basic_warp():
    """Test basic WARP transfer"""
    print("\n" + "🧪"*35)
    print("TEST SCENARIO 1: BASIC WARP TRANSFER".center(70))
    print("🧪"*35 + "\n")
    
    warp = ZIONWarpBridgePoC(test_mode=Config.TEST_MODE)
    await warp.initialize()
    
    # Test single WARP transfer
    tx = await warp.warp_transfer(
        from_chain=WarpChainType.ETHEREUM,
        to_chain=WarpChainType.POLYGON,
        amount=1000.0,
        asset="ZION"
    )
    
    print(f"✅ Test complete! TX ID: {tx.tx_id}")
    warp.print_stats()

async def test_scenario_2_multiple_transfers():
    """Test multiple WARP transfers"""
    print("\n" + "🧪"*35)
    print("TEST SCENARIO 2: MULTIPLE WARP TRANSFERS".center(70))
    print("🧪"*35 + "\n")
    
    warp = ZIONWarpBridgePoC(test_mode=Config.TEST_MODE)
    await warp.initialize()
    
    # Test 5 different transfers
    chains = [
        (WarpChainType.ETHEREUM, WarpChainType.POLYGON, 1000.0),
        (WarpChainType.POLYGON, WarpChainType.ARBITRUM, 500.0),
        (WarpChainType.BSC, WarpChainType.AVALANCHE, 2000.0),
        (WarpChainType.ETHEREUM, WarpChainType.OPTIMISM, 750.0),
        (WarpChainType.POLYGON, WarpChainType.ETHEREUM, 1250.0)
    ]
    
    for i, (from_chain, to_chain, amount) in enumerate(chains, 1):
        print(f"\n{'='*70}")
        print(f"TRANSFER {i}/5".center(70))
        print(f"{'='*70}\n")
        
        await warp.warp_transfer(from_chain, to_chain, amount)
        await asyncio.sleep(0.5)  # Small delay between transfers
    
    print(f"\n✅ All {len(chains)} transfers complete!")
    warp.print_stats()

async def test_scenario_3_ecommerce():
    """Test eCommerce payment"""
    print("\n" + "🧪"*35)
    print("TEST SCENARIO 3: ECOMMERCE PAYMENT".center(70))
    print("🧪"*35 + "\n")
    
    warp = ZIONWarpBridgePoC(test_mode=Config.TEST_MODE)
    await warp.initialize()
    
    # Create payment for ZION merchandise
    products = [
        ("ZION T-Shirt", 25.00),
        ("ZION Hoodie", 50.00),
        ("ZION Sticker Pack", 10.00)
    ]
    
    for product_name, price in products:
        charge = await warp.create_payment(
            product_name=product_name,
            price_usd=price,
            customer_email="satoshi@zion.network"
        )
        await asyncio.sleep(0.3)
    
    print("✅ All payment charges created!")

async def test_scenario_4_complete_demo():
    """Complete demonstration of all features"""
    print("\n" + "🌟"*35)
    print("COMPLETE WARP BRIDGE DEMONSTRATION".center(70))
    print("🌟"*35 + "\n")
    
    warp = ZIONWarpBridgePoC(test_mode=Config.TEST_MODE)
    
    # Initialize
    await warp.initialize()
    
    # Test WARP transfers
    print("\n" + "="*70)
    print("TESTING WARP TRANSFERS".center(70))
    print("="*70 + "\n")
    
    await warp.warp_transfer(WarpChainType.ETHEREUM, WarpChainType.POLYGON, 1500.0)
    await asyncio.sleep(1)
    await warp.warp_transfer(WarpChainType.BSC, WarpChainType.AVALANCHE, 3000.0)
    
    # Test eCommerce
    print("\n" + "="*70)
    print("TESTING ECOMMERCE PAYMENTS".center(70))
    print("="*70 + "\n")
    
    await warp.create_payment("ZION Premium Membership", 99.99)
    
    # Final stats
    print("\n" + "="*70)
    print("FINAL STATISTICS".center(70))
    print("="*70 + "\n")
    
    warp.print_stats()
    
    print("\n🎉 COMPLETE DEMONSTRATION FINISHED! 🎉\n")


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

async def main():
    """Main entry point"""
    import sys
    
    print("\n" + "🌌"*35)
    print("ZION WARP BRIDGE - PROOF OF CONCEPT".center(70))
    print("Ankr + Voltage + OpenNode + Lightspark".center(70))
    print("🌌"*35 + "\n")
    
    # Parse command line
    if len(sys.argv) > 1:
        test = sys.argv[1]
        
        if test == "--test1":
            await test_scenario_1_basic_warp()
        elif test == "--test2":
            await test_scenario_2_multiple_transfers()
        elif test == "--test3":
            await test_scenario_3_ecommerce()
        elif test == "--demo" or test == "--test":
            await test_scenario_4_complete_demo()
        else:
            print(f"Unknown test: {test}")
            print("\nAvailable tests:")
            print("  --test1  : Basic WARP transfer")
            print("  --test2  : Multiple WARP transfers")
            print("  --test3  : eCommerce payment")
            print("  --demo   : Complete demonstration")
    else:
        print("Usage: python3 warp_bridge_poc.py [--test1|--test2|--test3|--demo]")
        print("\nRunning complete demo by default...\n")
        await test_scenario_4_complete_demo()


if __name__ == '__main__':
    asyncio.run(main())
