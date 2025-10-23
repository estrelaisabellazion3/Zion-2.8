#!/usr/bin/env python3
"""
ZION Stellar Bridge Integration Test
Phase 2B: Complete Stellar Integration Test

Tests all components:
- Humanitarian Bridge
- Asset Management
- Path Payments
- End-to-end remittance flow

Author: ZION Development Team
Version: 2.8.1
Date: October 23, 2025
"""

import asyncio
import logging
from datetime import datetime
from stellar_bridge_humanitarian import StellarBridgeHumanitarian, FiatCurrency, RemittanceType
from zion_stellar_asset import ZIONAssetManager
from zion_path_payments import ZIONPathPayments

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ZIONStellarIntegrationTest:
    """Complete Stellar Bridge integration test"""

    def __init__(self):
        self.bridge = None
        self.asset_manager = None
        self.path_payments = None
        self.test_results = {}

    async def setup_components(self):
        """Setup all Stellar components"""
        logger.info("Setting up ZION Stellar components...")

        # Initialize Humanitarian Bridge
        self.bridge = StellarBridgeHumanitarian()
        bridge_success = await self.bridge.initialize_bridge()
        self.test_results["bridge_init"] = bridge_success

        # Initialize Asset Manager
        self.asset_manager = ZIONAssetManager()
        asset_success = await self.asset_manager.initialize_asset()
        self.test_results["asset_init"] = asset_success

        # Initialize Path Payments
        self.path_payments = ZIONPathPayments()
        self.test_results["path_init"] = True

        logger.info("All components initialized")

    async def test_kyc_registration(self):
        """Test KYC profile registration"""
        logger.info("Testing KYC registration...")

        try:
            # Register test user
            success = await self.bridge.register_kyc_profile(
                user_id="test_user_001",
                documents=["passport", "address_proof", "id_card"],
                risk_assessment={
                    "score": 0.2,
                    "sanctions_clear": True,
                    "pep_clear": True,
                    "allowed_countries": ["US", "MX", "PH", "IN", "NG"]
                }
            )
            self.test_results["kyc_registration"] = success
            logger.info(f"KYC registration: {'PASS' if success else 'FAIL'}")

        except Exception as e:
            logger.error(f"KYC test failed: {e}")
            self.test_results["kyc_registration"] = False

    async def test_asset_issuance(self):
        """Test ZION asset issuance"""
        logger.info("Testing asset issuance...")

        try:
            # Issue tokens to test recipients
            recipient1 = "test_recipient_001"
            recipient2 = "test_recipient_002"

            tx1 = await self.asset_manager.issue_tokens(
                self.asset_manager.distribution_schedules["public_sale"]["type"],
                recipient1, 1000.0, "Integration test - public sale"
            )

            tx2 = await self.asset_manager.issue_tokens(
                self.asset_manager.distribution_schedules["ecosystem"]["type"],
                recipient2, 5000.0, "Integration test - ecosystem"
            )

            success = tx1 is not None and tx2 is not None
            self.test_results["asset_issuance"] = success
            logger.info(f"Asset issuance: {'PASS' if success else 'FAIL'}")

            if success:
                # Check balances
                holder1 = await self.asset_manager.get_holder_info(recipient1)
                holder2 = await self.asset_manager.get_holder_info(recipient2)
                logger.info(f"Holder 1 balance: {holder1['balance'] if holder1 else 0} ZION")
                logger.info(f"Holder 2 balance: {holder2['balance'] if holder2 else 0} ZION")

        except Exception as e:
            logger.error(f"Asset issuance test failed: {e}")
            self.test_results["asset_issuance"] = False

    async def test_path_finding(self):
        """Test path payment routing"""
        logger.info("Testing path finding...")

        try:
            # Test remittance quote
            quote = await self.path_payments.get_remittance_quote(
                "US", "Mexico", "USD", "MXN", 500.0
            )

            if quote:
                logger.info(f"Quote: ${quote['send_amount']} USD → ${quote['receive_amount']:.2f} MXN")
                logger.info(f"Fee: ${quote['total_fee']:.2f}, Time: {quote['estimated_time']}s")

                # Test direct path finding
                usd_asset = self.path_payments.fiat_assets["USD"]
                mxn_asset = self.path_payments.fiat_assets["MXN"]

                path = await self.path_payments.find_optimal_path(usd_asset, mxn_asset, 1000.0)

                success = path is not None
                self.test_results["path_finding"] = success
                logger.info(f"Path finding: {'PASS' if success else 'FAIL'}")

                if success:
                    logger.info(f"Optimal path: {len(path.hops)} hops, confidence: {path.confidence_score:.2f}")

            else:
                self.test_results["path_finding"] = False
                logger.error("Path finding failed - no quote generated")

        except Exception as e:
            logger.error(f"Path finding test failed: {e}")
            self.test_results["path_finding"] = False

    async def test_remittance_flow(self):
        """Test complete remittance flow"""
        logger.info("Testing complete remittance flow...")

        try:
            # Create humanitarian remittance
            recipient_info = {
                "name": "Maria Gonzalez",
                "phone": "+52551234567",
                "country": "Mexico",
                "bank": "BBVA",
                "account": "1234567890",
                "email": "maria@example.com"
            }

            remittance_id = await self.bridge.create_remittance(
                sender_id="test_user_001",
                recipient_info=recipient_info,
                amount=500.0,
                currency=FiatCurrency.USD,
                remittance_type=RemittanceType.FAMILY,
                priority="instant"
            )

            if remittance_id:
                logger.info(f"Remittance created: {remittance_id}")

                # Wait for processing
                await asyncio.sleep(8)  # Wait for instant processing

                # Check status
                status = await self.bridge.get_remittance_status(remittance_id)

                success = status and status.status == "completed"
                self.test_results["remittance_flow"] = success
                logger.info(f"Remittance flow: {'PASS' if success else 'FAIL'}")

                if success:
                    logger.info(f"Final status: {status.status}, Amount: {status.amount} ZION")

            else:
                self.test_results["remittance_flow"] = False
                logger.error("Remittance creation failed")

        except Exception as e:
            logger.error(f"Remittance flow test failed: {e}")
            self.test_results["remittance_flow"] = False

    async def test_asset_transfer(self):
        """Test asset transfers between holders"""
        logger.info("Testing asset transfers...")

        try:
            # Transfer between test holders
            sender = "test_recipient_001"
            recipient = "test_recipient_002"
            amount = 100.0

            tx_hash = await self.asset_manager.transfer_tokens(
                sender, recipient, amount, "Integration test transfer"
            )

            success = tx_hash is not None
            self.test_results["asset_transfer"] = success
            logger.info(f"Asset transfer: {'PASS' if success else 'FAIL'}")

            if success:
                # Check updated balances
                sender_info = await self.asset_manager.get_holder_info(sender)
                recipient_info = await self.asset_manager.get_holder_info(recipient)

                if sender_info and recipient_info:
                    logger.info(f"Sender balance: {sender_info['balance']} ZION")
                    logger.info(f"Recipient balance: {recipient_info['balance']} ZION")

        except Exception as e:
            logger.error(f"Asset transfer test failed: {e}")
            self.test_results["asset_transfer"] = False

    async def run_comprehensive_test(self):
        """Run all integration tests"""
        logger.info("🧪 Starting ZION Stellar Bridge Integration Tests")
        logger.info("=" * 60)

        start_time = datetime.now()

        # Setup
        await self.setup_components()

        # Test components
        await self.test_kyc_registration()
        await self.test_asset_issuance()
        await self.test_path_finding()
        await self.test_remittance_flow()
        await self.test_asset_transfer()

        # Generate report
        await self.generate_test_report(start_time)

    async def generate_test_report(self, start_time: datetime):
        """Generate comprehensive test report"""
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        logger.info("\n" + "=" * 60)
        logger.info("🧪 ZION STELLAR BRIDGE INTEGRATION TEST RESULTS")
        logger.info("=" * 60)

        passed = 0
        total = len(self.test_results)

        for test_name, result in self.test_results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            logger.info(f"{test_name.replace('_', ' ').title()}: {status}")
            if result:
                passed += 1

        logger.info("-" * 60)
        logger.info(f"Tests Passed: {passed}/{total} ({passed/total*100:.1f}%)")
        logger.info(f"Duration: {duration:.2f} seconds")
        logger.info("-" * 60)

        # Component status
        if self.bridge:
            bridge_metrics = await self.bridge.get_bridge_metrics()
            logger.info(f"Bridge Metrics: {bridge_metrics.total_transfers} transfers, ${bridge_metrics.total_volume_usd:.2f} volume")

        if self.asset_manager:
            asset_info = await self.asset_manager.get_asset_info()
            logger.info(f"Asset Status: {asset_info['issuance']['total_supply']} total supply, {asset_info['holders_count']} holders")

        if self.path_payments:
            path_metrics = await self.path_payments.get_path_metrics()
            logger.info(f"Path Metrics: {path_metrics['total_paths_analyzed']} paths analyzed, {path_metrics['successful_routes']} successful")

        logger.info("=" * 60)

        if passed == total:
            logger.info("🎉 ALL TESTS PASSED - Stellar Bridge Ready for Production!")
        else:
            logger.warning(f"⚠️  {total - passed} test(s) failed - Review and fix issues")

    async def cleanup(self):
        """Cleanup test resources"""
        logger.info("Cleaning up test resources...")

        if self.bridge:
            await self.bridge.close()

        logger.info("Cleanup complete")

async def main():
    """Main test execution"""
    tester = ZIONStellarIntegrationTest()

    try:
        await tester.run_comprehensive_test()
    except Exception as e:
        logger.error(f"Test execution failed: {e}")
    finally:
        await tester.cleanup()

if __name__ == "__main__":
    asyncio.run(main())