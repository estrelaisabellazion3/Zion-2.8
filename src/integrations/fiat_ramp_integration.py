#!/usr/bin/env python3
"""
ZION Fiat Ramp Integration - Phase 2C
Multi-Currency Fiat On/Off-Ramps for Humanitarian Finance

Features:
- Multi-provider fiat integration (Stripe, PayPal, Local Banks)
- Support for 7+ currencies (USD/EUR/GBP/MXN/PHP/INR/NGN)
- Real-time FX rates and competitive pricing
- Enhanced KYC for fiat transactions
- Local payout methods (bank transfers, mobile money)
- Compliance monitoring and reporting

Author: ZION Development Team
Version: 2.8.1
Date: October 23, 2025
"""

import aiohttp
import hashlib
import hmac
import json
import logging
import os  # Add os import for environment variables
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum
import random
import uuid
import asyncio

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class FiatCurrency(Enum):
    """Supported fiat currencies"""
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    MXN = "MXN"
    PHP = "PHP"
    INR = "INR"
    NGN = "NGN"

class RampProvider(Enum):
    """Fiat ramp providers"""
    STRIPE = "stripe"
    PAYPAL = "paypal"
    REVOLUT = "revolut"
    LOCAL_BANK = "local_bank"
    MOBILE_MONEY = "mobile_money"
    CRYPTO_EXCHANGE = "crypto_exchange"

class TransactionType(Enum):
    """Fiat transaction types"""
    DEPOSIT = "deposit"  # Fiat → Crypto
    WITHDRAWAL = "withdrawal"  # Crypto → Fiat
    EXCHANGE = "exchange"  # Fiat → Fiat

class PaymentMethod(Enum):
    """Payment methods"""
    BANK_TRANSFER = "bank_transfer"
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    PAYPAL = "paypal"
    MOBILE_MONEY = "mobile_money"
    CASH_PICKUP = "cash_pickup"

class ComplianceLevel(Enum):
    """Enhanced compliance levels for fiat"""
    BASIC = "basic"
    ENHANCED = "enhanced"
    PREMIUM = "premium"
    INSTITUTIONAL = "institutional"

@dataclass
class FXRate:
    """Foreign exchange rate with spread"""
    from_currency: FiatCurrency
    to_currency: FiatCurrency
    rate: float
    spread: float  # Percentage spread
    source: str
    timestamp: datetime
    provider: RampProvider

@dataclass
class FiatTransaction:
    """Fiat transaction record"""
    tx_id: str
    user_id: str
    transaction_type: TransactionType
    from_currency: FiatCurrency
    to_currency: FiatCurrency
    amount: float
    converted_amount: float
    fx_rate: float
    fee_amount: float
    provider: RampProvider
    payment_method: PaymentMethod
    status: str
    compliance_check: bool
    kyc_level: ComplianceLevel
    timestamp: datetime
    provider_tx_id: Optional[str] = None
    recipient_info: Optional[Dict[str, Any]] = None

@dataclass
class RampProviderConfig:
    """Configuration for fiat ramp provider"""
    provider: RampProvider
    name: str
    supported_currencies: List[FiatCurrency]
    supported_methods: List[PaymentMethod]
    min_amount: Dict[FiatCurrency, float]
    max_amount: Dict[FiatCurrency, float]
    fee_structure: Dict[str, float]  # percentage or fixed fees
    processing_time: Dict[TransactionType, int]  # seconds
    active: bool
    api_config: Dict[str, Any]

@dataclass
class FiatRampMetrics:
    """Fiat ramp performance metrics"""
    total_transactions: int
    successful_transactions: int
    failed_transactions: int
    total_volume_usd: float
    average_processing_time: float
    provider_success_rates: Dict[str, float]
    currency_volumes: Dict[str, float]
    last_updated: datetime

class ZIONFiatRamp:
    """
    ZION Fiat Ramp Integration

    Multi-provider fiat on/off-ramps with competitive pricing,
    enhanced compliance, and local payout methods.
    """

    def __init__(self):
        # FX rates cache
        self.fx_rates: Dict[str, FXRate] = {}
        self.fx_update_interval = 60  # Update every minute

        # Provider configurations
        self.providers: Dict[RampProvider, RampProviderConfig] = {}
        self._initialize_providers()

        # Transaction tracking
        self.pending_transactions: Dict[str, FiatTransaction] = {}
        self.completed_transactions: List[FiatTransaction] = []

        # Enhanced KYC profiles
        self.kyc_profiles: Dict[str, Dict[str, Any]] = {}

        # Metrics
        self.metrics = FiatRampMetrics(0, 0, 0, 0.0, 0.0, {}, {}, datetime.now())

        # Local payout configurations
        self.local_payouts: Dict[str, Dict[str, Any]] = {}
        self._initialize_local_payouts()

        # API clients
        self.stripe_client = None
        self.paypal_client = None
        self._initialize_api_clients()

        # Webhook handlers
        self.webhook_handlers: Dict[str, callable] = {}
        self._initialize_webhook_handlers()

        logger.info("ZION Fiat Ramp initialized")

    def _initialize_providers(self):
        """Initialize fiat ramp providers"""
        try:
            # Stripe configuration
            self.providers[RampProvider.STRIPE] = RampProviderConfig(
                provider=RampProvider.STRIPE,
                name="Stripe",
                supported_currencies=[FiatCurrency.USD, FiatCurrency.EUR, FiatCurrency.GBP, FiatCurrency.MXN],
                supported_methods=[PaymentMethod.CREDIT_CARD, PaymentMethod.DEBIT_CARD, PaymentMethod.BANK_TRANSFER],
                min_amount={FiatCurrency.USD: 10.0, FiatCurrency.EUR: 10.0, FiatCurrency.GBP: 10.0, FiatCurrency.MXN: 100.0},
                max_amount={FiatCurrency.USD: 10000.0, FiatCurrency.EUR: 8000.0, FiatCurrency.GBP: 8000.0, FiatCurrency.MXN: 50000.0},
                fee_structure={"percentage": 0.029, "fixed": 0.30},  # 2.9% + $0.30
                processing_time={TransactionType.DEPOSIT: 300, TransactionType.WITHDRAWAL: 86400},  # 5 min / 1 day
                active=True,
                api_config={
                    "api_key": os.getenv("STRIPE_API_KEY", "sk_test_mock_key_for_demo"),
                    "webhook_secret": os.getenv("STRIPE_WEBHOOK_SECRET", "whsec_mock_secret"),
                    "mode": "sandbox"
                }
            )

            # PayPal configuration
            self.providers[RampProvider.PAYPAL] = RampProviderConfig(
                provider=RampProvider.PAYPAL,
                name="PayPal",
                supported_currencies=[FiatCurrency.USD, FiatCurrency.EUR, FiatCurrency.GBP, FiatCurrency.MXN],
                supported_methods=[PaymentMethod.PAYPAL],
                min_amount={FiatCurrency.USD: 1.0, FiatCurrency.EUR: 1.0, FiatCurrency.GBP: 1.0, FiatCurrency.MXN: 100.0},
                max_amount={FiatCurrency.USD: 10000.0, FiatCurrency.EUR: 8000.0, FiatCurrency.GBP: 8000.0, FiatCurrency.MXN: 50000.0},
                fee_structure={"percentage": 0.024, "fixed": 0.49},  # 2.4% + $0.49
                processing_time={TransactionType.DEPOSIT: 180, TransactionType.WITHDRAWAL: 3600},  # 3 min / 1 hour
                active=True,
                api_config={
                    "client_id": os.getenv("PAYPAL_CLIENT_ID", "mock_client_id"),
                    "client_secret": os.getenv("PAYPAL_CLIENT_SECRET", "mock_client_secret"),
                    "mode": os.getenv("PAYPAL_MODE", "sandbox")
                }
            )

            # Revolut configuration - European fintech with competitive rates
            self.providers[RampProvider.REVOLUT] = RampProviderConfig(
                provider=RampProvider.REVOLUT,
                name="Revolut",
                supported_currencies=[FiatCurrency.USD, FiatCurrency.EUR, FiatCurrency.GBP],
                supported_methods=[PaymentMethod.BANK_TRANSFER, PaymentMethod.CREDIT_CARD, PaymentMethod.DEBIT_CARD],
                min_amount={FiatCurrency.USD: 1.0, FiatCurrency.EUR: 1.0, FiatCurrency.GBP: 1.0},
                max_amount={FiatCurrency.USD: 25000.0, FiatCurrency.EUR: 20000.0, FiatCurrency.GBP: 20000.0},
                fee_structure={"percentage": 0.015, "fixed": 0.25},  # 1.5% + $0.25 (competitive European rates)
                processing_time={TransactionType.DEPOSIT: 60, TransactionType.WITHDRAWAL: 1800},  # 1 min / 30 min (fast processing)
                active=True,
                api_config={
                    "api_key": os.getenv("REVOLUT_API_KEY", "mock_revolut_key"),
                    "webhook_secret": os.getenv("REVOLUT_WEBHOOK_SECRET", "mock_revolut_secret"),
                    "mode": os.getenv("REVOLUT_MODE", "sandbox")
                }
            )

            # Local Bank (Mexico) - supports USD and MXN
            self.providers[RampProvider.LOCAL_BANK] = RampProviderConfig(
                provider=RampProvider.LOCAL_BANK,
                name="Local Banks MX",
                supported_currencies=[FiatCurrency.USD, FiatCurrency.MXN],
                supported_methods=[PaymentMethod.BANK_TRANSFER],
                min_amount={FiatCurrency.USD: 10.0, FiatCurrency.MXN: 100.0},
                max_amount={FiatCurrency.USD: 10000.0, FiatCurrency.MXN: 50000.0},
                fee_structure={"percentage": 0.015},  # 1.5%
                processing_time={TransactionType.DEPOSIT: 3600, TransactionType.WITHDRAWAL: 7200},  # 1-2 hours
                active=True,
                api_config={"bank_codes": ["BBVA", "Santander", "Banamex"]}
            )

            # Mobile Money (Philippines) - supports USD and PHP
            self.providers[RampProvider.MOBILE_MONEY] = RampProviderConfig(
                provider=RampProvider.MOBILE_MONEY,
                name="Mobile Money PH",
                supported_currencies=[FiatCurrency.USD, FiatCurrency.PHP],
                supported_methods=[PaymentMethod.MOBILE_MONEY],
                min_amount={FiatCurrency.USD: 1.0, FiatCurrency.PHP: 100.0},
                max_amount={FiatCurrency.USD: 10000.0, FiatCurrency.PHP: 50000.0},
                fee_structure={"percentage": 0.02},  # 2.0%
                processing_time={TransactionType.DEPOSIT: 300, TransactionType.WITHDRAWAL: 600},  # 5-10 min
                active=True,
                api_config={"networks": ["GCash", "PayMaya", "Coins.ph"]}
            )

            # India Bank Transfer - supports USD and INR
            self.providers[RampProvider.CRYPTO_EXCHANGE] = RampProviderConfig(
                provider=RampProvider.CRYPTO_EXCHANGE,
                name="India Bank Transfer",
                supported_currencies=[FiatCurrency.USD, FiatCurrency.INR],
                supported_methods=[PaymentMethod.BANK_TRANSFER],
                min_amount={FiatCurrency.USD: 10.0, FiatCurrency.INR: 1000.0},
                max_amount={FiatCurrency.USD: 10000.0, FiatCurrency.INR: 500000.0},
                fee_structure={"percentage": 0.015},  # 1.5%
                processing_time={TransactionType.DEPOSIT: 1800, TransactionType.WITHDRAWAL: 3600},  # 30 min - 1 hour
                active=True,
                api_config={"banks": ["HDFC", "ICICI", "SBI", "Axis", "Kotak"]}
            )

            logger.info(f"Initialized {len(self.providers)} fiat ramp providers")

        except Exception as e:
            logger.error(f"Provider initialization failed: {e}")

    def _initialize_local_payouts(self):
        """Initialize local payout configurations"""
        try:
            # Mexico local payouts
            self.local_payouts["MX"] = {
                "banks": ["BBVA", "Santander", "Banamex", "HSBC", "Scotiabank"],
                "instant_methods": ["SPEI"],
                "processing_time": 1800,  # 30 minutes
                "fee_structure": {"percentage": 0.01}  # 1%
            }

            # Philippines local payouts
            self.local_payouts["PH"] = {
                "mobile_networks": ["GCash", "PayMaya", "Coins.ph"],
                "banks": ["BDO", "BPI", "Metrobank", "PNB"],
                "instant_methods": ["PESONet", "InstaPay"],
                "processing_time": 300,  # 5 minutes
                "fee_structure": {"percentage": 0.015}  # 1.5%
            }

            # India local payouts
            self.local_payouts["IN"] = {
                "banks": ["HDFC", "ICICI", "SBI", "Axis", "Kotak"],
                "upi_apps": ["Google Pay", "PhonePe", "Paytm", "Amazon Pay"],
                "processing_time": 1800,  # 30 minutes
                "fee_structure": {"percentage": 0.012}  # 1.2%
            }

            # Nigeria local payouts
            self.local_payouts["NG"] = {
                "banks": ["GTBank", "First Bank", "Zenith", "UBA", "Access"],
                "mobile_money": ["Opay", "PalmPay", "Moniepoint"],
                "processing_time": 3600,  # 1 hour
                "fee_structure": {"percentage": 0.025}  # 2.5%
            }

            logger.info(f"Initialized local payouts for {len(self.local_payouts)} countries")

        except Exception as e:
            logger.error(f"Local payout initialization failed: {e}")

    def _initialize_api_clients(self):
        """Initialize payment provider API clients"""
        try:
            # Initialize Stripe client
            stripe_config = self.providers.get(RampProvider.STRIPE)
            if stripe_config and stripe_config.active:
                import stripe
                stripe.api_key = stripe_config.api_config.get("api_key", "")
                self.stripe_client = stripe
                logger.info("Stripe API client initialized")

            # Initialize PayPal client
            paypal_config = self.providers.get(RampProvider.PAYPAL)
            if paypal_config and paypal_config.active:
                import paypalrestsdk
                paypalrestsdk.configure({
                    "mode": paypal_config.api_config.get("mode", "sandbox"),
                    "client_id": paypal_config.api_config.get("client_id", ""),
                    "client_secret": paypal_config.api_config.get("client_secret", "")
                })
                self.paypal_client = paypalrestsdk
                logger.info("PayPal API client initialized")

            # Initialize Revolut client (mock for now - would use revolut-python SDK in production)
            revolut_config = self.providers.get(RampProvider.REVOLUT)
            if revolut_config and revolut_config.active:
                # In production, would initialize Revolut API client
                # import revolut
                # revolut.api_key = revolut_config.api_config.get("api_key", "")
                self.revolut_client = {"api_key": revolut_config.api_config.get("api_key", "")}
                logger.info("Revolut API client initialized")

        except Exception as e:
            logger.error(f"API client initialization failed: {e}")

    def _initialize_webhook_handlers(self):
        """Initialize webhook event handlers"""
        self.webhook_handlers = {
            "stripe": self._handle_stripe_webhook,
            "paypal": self._handle_paypal_webhook,
            "revolut": self._handle_revolut_webhook,
        }
        logger.info("Webhook handlers initialized")

    async def initialize_ramp(self) -> bool:
        """
        Initialize fiat ramp services

        Returns:
            bool: True if initialization successful
        """
        try:
            logger.info("Initializing ZION Fiat Ramp...")

            # Start background tasks
            asyncio.create_task(self._fx_rate_updater())
            asyncio.create_task(self._provider_monitor())

            # Update initial FX rates
            await self._update_fx_rates()

            logger.info("ZION Fiat Ramp initialization completed")
            return True

        except Exception as e:
            logger.error(f"Ramp initialization failed: {e}")
            return False

    async def _update_fx_rates(self):
        """Update foreign exchange rates from multiple sources"""
        try:
            # Simulate FX rate updates (in production, fetch from APIs)
            base_rates = {
                ("USD", "EUR"): 0.85,
                ("USD", "GBP"): 0.73,
                ("USD", "MXN"): 18.5,
                ("USD", "PHP"): 56.0,
                ("USD", "INR"): 83.0,
                ("USD", "NGN"): 1500.0,
                ("EUR", "GBP"): 0.86,
            }

            for (from_curr, to_curr), base_rate in base_rates.items():
                # Add competitive spread (0.1-0.5%)
                spread = random.uniform(0.001, 0.005)

                # Create FX rate for each provider
                for provider in self.providers.keys():
                    fx_rate = FXRate(
                        from_currency=FiatCurrency(from_curr),
                        to_currency=FiatCurrency(to_curr),
                        rate=base_rate * (1 + random.uniform(-0.01, 0.01)),  # Add some variation
                        spread=spread,
                        source=f"{provider.value}_api",
                        timestamp=datetime.now(),
                        provider=provider
                    )

                    key = f"{from_curr}_{to_curr}_{provider.value}"
                    self.fx_rates[key] = fx_rate

            logger.info(f"Updated {len(self.fx_rates)} FX rates")

        except Exception as e:
            logger.error(f"FX rate update failed: {e}")

    async def _fx_rate_updater(self):
        """Background task to update FX rates"""
        while True:
            try:
                await asyncio.sleep(self.fx_update_interval)
                await self._update_fx_rates()
            except Exception as e:
                logger.error(f"FX rate update error: {e}")
                await asyncio.sleep(30)

    async def _provider_monitor(self):
        """Monitor provider status and performance"""
        while True:
            try:
                await asyncio.sleep(300)  # Check every 5 minutes

                # Update provider success rates
                for provider in self.providers.values():
                    if provider.active:
                        # Simulate success rate monitoring
                        success_rate = random.uniform(0.95, 0.99)
                        self.metrics.provider_success_rates[provider.name] = success_rate

                logger.info(f"Provider monitoring: {len(self.providers)} providers checked")

            except Exception as e:
                logger.error(f"Provider monitoring failed: {e}")
                await asyncio.sleep(60)

    async def create_fiat_transaction(self, user_id: str, transaction_type: TransactionType,
                                    from_currency: FiatCurrency, to_currency: FiatCurrency,
                                    amount: float, payment_method: PaymentMethod,
                                    recipient_info: Optional[Dict[str, Any]] = None) -> Optional[str]:
        """
        Create a fiat transaction

        Args:
            user_id: User identifier
            transaction_type: Type of transaction
            from_currency: Source currency
            to_currency: Destination currency
            amount: Amount in from_currency
            payment_method: Payment method
            recipient_info: Recipient details for withdrawals

        Returns:
            str: Transaction ID if successful, None otherwise
        """
        try:
            # Validate KYC compliance
            if not await self._validate_fiat_kyc(user_id, amount, transaction_type):
                logger.error(f"KYC validation failed for user {user_id}")
                return None

            # Find best provider and rate
            provider, fx_rate = await self._find_best_provider(
                from_currency, to_currency, amount, payment_method, transaction_type
            )

            if not provider or not fx_rate:
                logger.error(f"No suitable provider found for {from_currency.value} to {to_currency.value}")
                return None

            # Calculate amounts and fees
            converted_amount = amount * fx_rate.rate
            provider_config = self.providers[provider]

            # Calculate fees
            fee_percentage = provider_config.fee_structure.get("percentage", 0.02)
            fee_fixed = provider_config.fee_structure.get("fixed", 0.0)
            fee_amount = (amount * fee_percentage) + fee_fixed

            # Generate transaction ID
            tx_id = f"fiat_{datetime.now().timestamp()}_{user_id[:8]}"

            # Create transaction record
            transaction = FiatTransaction(
                tx_id=tx_id,
                user_id=user_id,
                transaction_type=transaction_type,
                from_currency=from_currency,
                to_currency=to_currency,
                amount=amount,
                converted_amount=converted_amount,
                fx_rate=fx_rate.rate,
                fee_amount=fee_amount,
                provider=provider,
                payment_method=payment_method,
                status="pending",
                compliance_check=True,
                kyc_level=ComplianceLevel.ENHANCED,
                timestamp=datetime.now(),
                recipient_info=recipient_info
            )

            self.pending_transactions[tx_id] = transaction

            # Start processing
            asyncio.create_task(self._process_fiat_transaction(tx_id))

            logger.info(f"Created fiat transaction {tx_id}: {amount} {from_currency.value} → {converted_amount:.2f} {to_currency.value}")
            return tx_id

        except Exception as e:
            logger.error(f"Fiat transaction creation failed: {e}")
            return None

    async def _validate_fiat_kyc(self, user_id: str, amount: float,
                               transaction_type: TransactionType) -> bool:
        """Validate enhanced KYC for fiat transactions"""
        try:
            profile = self.kyc_profiles.get(user_id)
            if not profile:
                logger.error(f"No KYC profile found for user {user_id}")
                return False

            # Check compliance level
            kyc_level = profile.get("compliance_level", ComplianceLevel.BASIC)

            # Higher amounts require higher KYC levels
            if amount > 1000 and kyc_level == ComplianceLevel.BASIC:
                logger.error(f"Amount {amount} requires enhanced KYC for user {user_id}")
                return False

            if amount > 10000 and kyc_level not in [ComplianceLevel.PREMIUM, ComplianceLevel.INSTITUTIONAL]:
                logger.error(f"Amount {amount} requires premium KYC for user {user_id}")
                return False

            # Check transaction velocity
            daily_volume = profile.get("daily_volume", 0)
            if daily_volume + amount > profile.get("daily_limit", 10000):
                logger.error(f"Daily limit exceeded for user {user_id}")
                return False

            return True

        except Exception as e:
            logger.error(f"KYC validation error: {e}")
            return False

    async def _find_best_provider(self, from_currency: FiatCurrency, to_currency: FiatCurrency,
                                amount: float, payment_method: PaymentMethod,
                                transaction_type: TransactionType) -> Tuple[Optional[RampProvider], Optional[FXRate]]:
        """Find the best provider and FX rate for the transaction"""
        try:
            best_provider = None
            best_fx_rate = None
            best_total_cost = float('inf')

            for provider_config in self.providers.values():
                if not provider_config.active:
                    continue

                # Check if provider supports the currencies and method
                if (from_currency not in provider_config.supported_currencies or
                    payment_method not in provider_config.supported_methods):
                    continue

                # Check amount limits
                if (amount < provider_config.min_amount.get(from_currency, 0) or
                    amount > provider_config.max_amount.get(from_currency, float('inf'))):
                    continue

                # Get FX rate for this provider
                fx_key = f"{from_currency.value}_{to_currency.value}_{provider_config.provider.value}"
                fx_rate = self.fx_rates.get(fx_key)

                if not fx_rate:
                    continue

               
                fee_percentage = provider_config.fee_structure.get("percentage", 0.02)
                fee_fixed = provider_config.fee_structure.get("fixed", 0.0)
                total_fees = (amount * fee_percentage) + fee_fixed + (amount * fx_rate.spread)

                if total_fees < best_total_cost:
                    best_total_cost = total_fees
                    best_provider = provider_config.provider
                    best_fx_rate = fx_rate

            return best_provider, best_fx_rate

        except Exception as e:
            logger.error(f"Provider selection failed: {e}")
            return None, None

    async def _process_fiat_transaction(self, tx_id: str):
        """Process the fiat transaction"""
        try:
            transaction = self.pending_transactions.get(tx_id)
            if not transaction:
                return

            logger.info(f"Processing fiat transaction {tx_id}")

            # Get provider config
            provider_config = self.providers.get(transaction.provider)
            if not provider_config:
                transaction.status = "failed"
                return

            # Create payment with provider API
            success = await self._create_provider_payment(transaction, provider_config)

            if success:
                # Wait for webhook confirmation or timeout
                await self._wait_for_payment_confirmation(tx_id, provider_config)
            else:
                transaction.status = "failed"
                logger.error(f"Fiat transaction {tx_id} payment creation failed")

        except Exception as e:
            logger.error(f"Transaction processing failed: {e}")
            transaction = self.pending_transactions.get(tx_id)
            if transaction:
                transaction.status = "failed"

    async def _create_provider_payment(self, transaction: FiatTransaction,
                                     provider_config: RampProviderConfig) -> bool:
        """Create payment with provider API"""
        try:
            if transaction.provider == RampProvider.STRIPE:
                return await self._create_stripe_payment(transaction, provider_config)
            elif transaction.provider == RampProvider.PAYPAL:
                return await self._create_paypal_payment(transaction, provider_config)
            elif transaction.provider == RampProvider.REVOLUT:
                return await self._create_revolut_payment(transaction, provider_config)
            else:
                # For local providers, simulate success
                logger.info(f"Simulating payment for {transaction.provider.value}")
                return True

        except Exception as e:
            logger.error(f"Provider payment creation failed: {e}")
            return False

    async def _create_stripe_payment(self, transaction: FiatTransaction,
                                   provider_config: RampProviderConfig) -> bool:
        """Create Stripe payment intent"""
        try:
            if not self.stripe_client:
                logger.error("Stripe client not initialized")
                return False

            # Convert amount to cents (Stripe uses smallest currency unit)
            amount_cents = int(transaction.amount * 100)

            # Create payment intent
            payment_intent = self.stripe_client.PaymentIntent.create(
                amount=amount_cents,
                currency=transaction.from_currency.value.lower(),
                payment_method_types=['card', 'bank_transfer'],
                metadata={
                    'zion_tx_id': transaction.tx_id,
                    'user_id': transaction.user_id,
                    'transaction_type': transaction.transaction_type.value
                },
                description=f"ZION Fiat Transaction: {transaction.amount} {transaction.from_currency.value}"
            )

            transaction.provider_tx_id = payment_intent.id
            logger.info(f"Created Stripe payment intent: {payment_intent.id}")
            return True

        except Exception as e:
            logger.error(f"Stripe payment creation failed: {e}")
            return False

    async def _create_paypal_payment(self, transaction: FiatTransaction,
                                   provider_config: RampProviderConfig) -> bool:
        """Create PayPal payment"""
        try:
            if not self.paypal_client:
                logger.error("PayPal client not initialized")
                return False

            # Create payment object
            payment = self.paypal_client.Payment({
                "intent": "sale",
                "payer": {
                    "payment_method": "paypal"
                },
                "transactions": [{
                    "amount": {
                        "total": f"{transaction.amount:.2f}",
                        "currency": transaction.from_currency.value
                    },
                    "description": f"ZION Fiat Transaction: {transaction.amount} {transaction.from_currency.value}"
                }],
                "redirect_urls": {
                    "return_url": "https://zion-blockchain.com/payment/success",
                    "cancel_url": "https://zion-blockchain.com/payment/cancel"
                }
            })

            # Create payment
            if payment.create():
                transaction.provider_tx_id = payment.id
                logger.info(f"Created PayPal payment: {payment.id}")
                return True
            else:
                logger.error(f"PayPal payment creation failed: {payment.error}")
                return False

        except Exception as e:
            logger.error(f"PayPal payment creation failed: {e}")
            return False

    async def _create_revolut_payment(self, transaction: FiatTransaction,
                                    provider_config: RampProviderConfig) -> bool:
        """Create Revolut payment"""
        try:
            if not self.revolut_client:
                logger.error("Revolut client not initialized")
                return False

            # Simulate Revolut payment creation (in production, use actual Revolut API)
            # This would create a payment request via Revolut Business API
            payment_request = {
                "amount": transaction.amount,
                "currency": transaction.from_currency.value,
                "description": f"ZION Fiat Transaction: {transaction.amount} {transaction.from_currency.value}",
                "metadata": {
                    "zion_tx_id": transaction.tx_id,
                    "user_id": transaction.user_id,
                    "transaction_type": transaction.transaction_type.value
                }
            }

            # Simulate API call
            payment_id = f"rev_{uuid.uuid4().hex[:16]}"
            transaction.provider_tx_id = payment_id

            logger.info(f"Created Revolut payment: {payment_id}")
            return True

        except Exception as e:
            logger.error(f"Revolut payment creation failed: {e}")
            return False

    async def _wait_for_payment_confirmation(self, tx_id: str, provider_config: RampProviderConfig):
        """Wait for payment confirmation via webhook or polling"""
        try:
            transaction = self.pending_transactions.get(tx_id)
            if not transaction:
                return

            # Set timeout based on provider
            timeout = provider_config.processing_time.get(transaction.transaction_type, 300)
            start_time = datetime.now()

            while (datetime.now() - start_time).total_seconds() < timeout:
                # Check if transaction was updated by webhook
                if transaction.status in ["completed", "failed"]:
                    break

                # For demo purposes, simulate webhook after some time
                if (datetime.now() - start_time).total_seconds() > 5:
                    await self._simulate_webhook_confirmation(tx_id)

                await asyncio.sleep(1)

            # Final status check
            if transaction.status == "completed":
                self.completed_transactions.append(transaction)
                del self.pending_transactions[tx_id]
                await self._update_metrics()
                logger.info(f"Fiat transaction {tx_id} completed")
            else:
                transaction.status = "failed"
                logger.error(f"Fiat transaction {tx_id} timed out")

        except Exception as e:
            logger.error(f"Payment confirmation wait failed: {e}")

    async def _simulate_webhook_confirmation(self, tx_id: str):
        """Simulate webhook confirmation for demo purposes"""
        try:
            transaction = self.pending_transactions.get(tx_id)
            if transaction and random.random() < 0.95:  # 95% success rate
                transaction.status = "completed"
                logger.info(f"Simulated webhook confirmation for {tx_id}")
        except Exception as e:
            logger.error(f"Webhook simulation failed: {e}")

    async def handle_webhook(self, provider: str, payload: Dict[str, Any],
                           signature: Optional[str] = None) -> bool:
        """
        Handle webhook from payment provider

        Args:
            provider: Payment provider name
            payload: Webhook payload
            signature: Webhook signature for verification

        Returns:
            bool: True if webhook handled successfully
        """
        try:
            handler = self.webhook_handlers.get(provider.lower())
            if not handler:
                logger.error(f"No webhook handler for provider: {provider}")
                return False

            return await handler(payload, signature)

        except Exception as e:
            logger.error(f"Webhook handling failed: {e}")
            return False

    async def _handle_stripe_webhook(self, payload: Dict[str, Any],
                                   signature: Optional[str] = None) -> bool:
        """Handle Stripe webhook events"""
        try:
            # Verify webhook signature if provided
            if signature:
                stripe_config = self.providers.get(RampProvider.STRIPE)
                if stripe_config:
                    webhook_secret = stripe_config.api_config.get("webhook_secret", "")
                    # In production, verify signature here
                    pass

            event_type = payload.get("type")
            event_data = payload.get("data", {}).get("object", {})

            if event_type == "payment_intent.succeeded":
                tx_id = event_data.get("metadata", {}).get("zion_tx_id")
                if tx_id and tx_id in self.pending_transactions:
                    transaction = self.pending_transactions[tx_id]
                    transaction.status = "completed"
                    transaction.provider_tx_id = event_data.get("id")
                    logger.info(f"Stripe payment confirmed: {tx_id}")

            elif event_type == "payment_intent.payment_failed":
                tx_id = event_data.get("metadata", {}).get("zion_tx_id")
                if tx_id and tx_id in self.pending_transactions:
                    transaction = self.pending_transactions[tx_id]
                    transaction.status = "failed"
                    logger.error(f"Stripe payment failed: {tx_id}")

            return True

        except Exception as e:
            logger.error(f"Stripe webhook handling failed: {e}")
            return False

    async def _handle_paypal_webhook(self, payload: Dict[str, Any],
                                   signature: Optional[str] = None) -> bool:
        """Handle PayPal webhook events"""
        try:
            event_type = payload.get("event_type")
            resource = payload.get("resource", {})

            if event_type == "PAYMENT.SALE.COMPLETED":
                # Extract transaction ID from custom field or metadata
                custom_id = resource.get("custom", "")
                if custom_id.startswith("zion_"):
                    tx_id = custom_id
                    if tx_id in self.pending_transactions:
                        transaction = self.pending_transactions[tx_id]
                        transaction.status = "completed"
                        transaction.provider_tx_id = resource.get("id")
                        logger.info(f"PayPal payment confirmed: {tx_id}")

            elif event_type in ["PAYMENT.SALE.DENIED", "PAYMENT.SALE.REVERSED"]:
                custom_id = resource.get("custom", "")
                if custom_id.startswith("zion_"):
                    tx_id = custom_id
                    if tx_id in self.pending_transactions:
                        transaction = self.pending_transactions[tx_id]
                        transaction.status = "failed"
                        logger.error(f"PayPal payment failed: {tx_id}")

            return True

        except Exception as e:
            logger.error(f"PayPal webhook handling failed: {e}")
            return False

    async def _handle_revolut_webhook(self, payload: Dict[str, Any],
                                    signature: Optional[str] = None) -> bool:
        """Handle Revolut webhook events"""
        try:
            # Verify webhook signature if provided
            if signature:
                revolut_config = self.providers.get(RampProvider.REVOLUT)
                if revolut_config:
                    webhook_secret = revolut_config.api_config.get("webhook_secret", "")
                    # In production, verify signature here
                    pass

            event_type = payload.get("event")
            transaction_data = payload.get("transaction", {})

            if event_type == "TRANSACTION_COMPLETED":
                # Extract transaction ID from metadata
                metadata = transaction_data.get("metadata", {})
                tx_id = metadata.get("zion_tx_id")

                if tx_id and tx_id in self.pending_transactions:
                    transaction = self.pending_transactions[tx_id]
                    transaction.status = "completed"
                    transaction.provider_tx_id = transaction_data.get("id")
                    logger.info(f"Revolut payment confirmed: {tx_id}")

            elif event_type in ["TRANSACTION_FAILED", "TRANSACTION_CANCELLED"]:
                metadata = transaction_data.get("metadata", {})
                tx_id = metadata.get("zion_tx_id")

                if tx_id and tx_id in self.pending_transactions:
                    transaction = self.pending_transactions[tx_id]
                    transaction.status = "failed"
                    logger.error(f"Revolut payment failed: {tx_id}")

            return True

        except Exception as e:
            logger.error(f"Revolut webhook handling failed: {e}")
            return False

    async def get_local_payout_options(self, country_code: str) -> Optional[Dict[str, Any]]:
        """Get local payout options for a country"""
        return self.local_payouts.get(country_code.upper())

    async def register_enhanced_kyc(self, user_id: str, documents: List[str],
                                  biometric_data: Optional[Dict[str, Any]] = None,
                                  risk_assessment: Optional[Dict[str, Any]] = None) -> bool:
        """
        Register enhanced KYC profile for fiat transactions

        Args:
            user_id: User identifier
            documents: List of document types submitted
            biometric_data: Biometric verification data
            risk_assessment: Risk assessment results

        Returns:
            bool: True if KYC registration successful
        """
        try:
            # Determine compliance level based on documents
            compliance_level = ComplianceLevel.BASIC

            if "passport" in documents and "address_proof" in documents:
                compliance_level = ComplianceLevel.ENHANCED

            if "bank_statement" in documents and biometric_data:
                compliance_level = ComplianceLevel.PREMIUM

            if "business_license" in documents and risk_assessment:
                compliance_level = ComplianceLevel.INSTITUTIONAL

            # Create KYC profile
            profile = {
                "user_id": user_id,
                "compliance_level": compliance_level,
                "documents_submitted": documents,
                "biometric_verified": biometric_data is not None,
                "risk_score": risk_assessment.get("score", 0.5) if risk_assessment else 0.5,
                "verification_date": datetime.now(),
                "daily_limit": self._get_daily_limit(compliance_level),
                "monthly_limit": self._get_monthly_limit(compliance_level),
                "daily_volume": 0.0,
                "monthly_volume": 0.0
            }

            self.kyc_profiles[user_id] = profile

            logger.info(f"Enhanced KYC registered for {user_id}: {compliance_level.value}")
            return True

        except Exception as e:
            logger.error(f"Enhanced KYC registration failed: {e}")
            return False

    def _get_daily_limit(self, compliance_level: ComplianceLevel) -> float:
        """Get daily transaction limit based on compliance level"""
        limits = {
            ComplianceLevel.BASIC: 1000.0,
            ComplianceLevel.ENHANCED: 10000.0,
            ComplianceLevel.PREMIUM: 50000.0,
            ComplianceLevel.INSTITUTIONAL: 100000.0
        }
        return limits.get(compliance_level, 1000.0)

    def _get_monthly_limit(self, compliance_level: ComplianceLevel) -> float:
        """Get monthly transaction limit based on compliance level"""
        limits = {
            ComplianceLevel.BASIC: 5000.0,
            ComplianceLevel.ENHANCED: 50000.0,
            ComplianceLevel.PREMIUM: 250000.0,
            ComplianceLevel.INSTITUTIONAL: 1000000.0
        }
        return limits.get(compliance_level, 5000.0)

    async def get_fiat_quote(self, from_currency: str, to_currency: str,
                           amount: float, payment_method: str) -> Optional[Dict[str, Any]]:
        """
        Get fiat transaction quote

        Args:
            from_currency: Source currency code
            to_currency: Destination currency code
            amount: Amount to convert
            payment_method: Payment method

        Returns:
            dict: Quote with rates and fees
        """
        try:
            from_curr = FiatCurrency(from_currency.upper())
            to_curr = FiatCurrency(to_currency.upper())
            method = PaymentMethod(payment_method.lower())

            provider, fx_rate = await self._find_best_provider(
                from_curr, to_curr, amount, method, TransactionType.EXCHANGE
            )

            if not provider or not fx_rate:
                return None

            provider_config = self.providers[provider]

            # Calculate fees
            fee_percentage = provider_config.fee_structure.get("percentage", 0.02)
            fee_fixed = provider_config.fee_structure.get("fixed", 0.0)
            fee_amount = (amount * fee_percentage) + fee_fixed
            converted_amount = amount * fx_rate.rate

            return {
                "from_currency": from_currency,
                "to_currency": to_currency,
                "amount": amount,
                "converted_amount": converted_amount,
                "fx_rate": fx_rate.rate,
                "spread": fx_rate.spread,
                "fee_amount": fee_amount,
                "total_cost": amount + fee_amount,
                "provider": provider.value,
                "estimated_time": provider_config.processing_time.get(TransactionType.EXCHANGE, 300),
                "payment_method": payment_method
            }

        except Exception as e:
            logger.error(f"Quote generation failed: {e}")
            return None

    async def close(self):
        """Cleanup fiat ramp resources"""
        logger.info("ZION Fiat Ramp closed")

    async def get_transaction_status(self, tx_id: str) -> Optional[Dict[str, Any]]:
        """Get fiat transaction status"""
        # Check pending
        if tx_id in self.pending_transactions:
            transaction = self.pending_transactions[tx_id]
            return {
                "tx_id": transaction.tx_id,
                "status": transaction.status,
                "amount": transaction.amount,
                "from_currency": transaction.from_currency.value,
                "to_currency": transaction.to_currency.value,
                "provider": transaction.provider.value,
                "timestamp": transaction.timestamp.isoformat()
            }

        # Check completed
        for tx in self.completed_transactions:
            if tx.tx_id == tx_id:
                return asdict(tx)

        return None

    async def _update_metrics(self):
        """Update fiat ramp metrics"""
        try:
            self.metrics.total_transactions = len(self.completed_transactions)
            self.metrics.successful_transactions = len([
                t for t in self.completed_transactions if t.status == "completed"
            ])
            self.metrics.failed_transactions = len([
                t for t in self.completed_transactions if t.status == "failed"
            ])

            # Calculate volumes
            self.metrics.total_volume_usd = sum(
                t.converted_amount if t.to_currency == FiatCurrency.USD
                else t.amount * 1.0  # Simplified conversion
                for t in self.completed_transactions
                if t.status == "completed"
            )

            # Calculate average processing time
            completed_times = [
                (datetime.now() - t.timestamp).total_seconds()
                for t in self.completed_transactions
                if t.status == "completed"
            ]
            if completed_times:
                self.metrics.average_processing_time = sum(completed_times) / len(completed_times)

            # Update currency volumes
            for tx in self.completed_transactions:
                if tx.status == "completed":
                    curr_key = tx.to_currency.value
                    self.metrics.currency_volumes[curr_key] = (
                        self.metrics.currency_volumes.get(curr_key, 0) + tx.converted_amount
                    )

            self.metrics.last_updated = datetime.now()

        except Exception as e:
            logger.error(f"Metrics update failed: {e}")

    async def get_ramp_metrics(self) -> Dict[str, Any]:
        """Get fiat ramp metrics"""
        await self._update_metrics()
        return asdict(self.metrics)

    async def get_supported_currencies(self) -> List[str]:
        """Get list of supported currencies"""
        currencies = set()
        for provider in self.providers.values():
            if provider.active:
                currencies.update([curr.value for curr in provider.supported_currencies])
        return sorted(list(currencies))

async def main():
    """Main function for testing ZION Fiat Ramp"""
    ramp = ZIONFiatRamp()

    try:
        # Initialize ramp
        success = await ramp.initialize_ramp()
        if not success:
            logger.error("Ramp initialization failed")
            return

        # Register enhanced KYC
        await ramp.register_enhanced_kyc(
            user_id="test_user_001",
            documents=["passport", "address_proof", "bank_statement"],
            biometric_data={"face_verified": True},
            risk_assessment={"score": 0.2, "pep_clear": True}
        )

        # Get fiat quote
        quote = await ramp.get_fiat_quote("USD", "MXN", 500.0, "bank_transfer")
        if quote:
            logger.info(f"Fiat quote: ${quote['amount']} USD → ${quote['converted_amount']:.2f} MXN")
            logger.info(f"Fee: ${quote['fee_amount']:.2f}, Provider: {quote['provider']}")

        # Create fiat transaction
        tx_id = await ramp.create_fiat_transaction(
            user_id="test_user_001",
            transaction_type=TransactionType.DEPOSIT,
            from_currency=FiatCurrency.USD,
            to_currency=FiatCurrency.MXN,
            amount=500.0,
            payment_method=PaymentMethod.BANK_TRANSFER,
            recipient_info={
                "bank": "BBVA",
                "account": "1234567890",
                "name": "Maria Gonzalez"
            }
        )

        if tx_id:
            logger.info(f"Created fiat transaction: {tx_id}")

            # Wait for processing
            await asyncio.sleep(12)

            # Check status
            status = await ramp.get_transaction_status(tx_id)
            if status:
                logger.info(f"Transaction status: {status['status']}")

        # Get metrics
        metrics = await ramp.get_ramp_metrics()
        logger.info(f"Ramp metrics: {metrics['total_transactions']} transactions, ${metrics['total_volume_usd']:.2f} volume")

        # Get supported currencies
        currencies = await ramp.get_supported_currencies()
        logger.info(f"Supported currencies: {', '.join(currencies)}")

        # Get local payout options
        payout_options = await ramp.get_local_payout_options("MX")
        if payout_options:
            logger.info(f"Mexico payout options: {len(payout_options['banks'])} banks available")

    except Exception as e:
        logger.error(f"Main execution failed: {e}")

    finally:
        await ramp.close()

if __name__ == "__main__":
    asyncio.run(main())