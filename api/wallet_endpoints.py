#!/usr/bin/env python3
"""
ZION 2.7.5 - Wallet API Endpoints
Real wallet management system with SECURE ENCRYPTION and VALIDATION
"""

import os
import sys
from pathlib import Path
from fastapi import HTTPException
from typing import Dict, List, Optional
from pydantic import BaseModel
import json
import hashlib
import secrets
from datetime import datetime

# Add parent directory to path for wallet import
sys.path.insert(0, str(Path(__file__).parent.parent))
from wallet import ZionWallet  # Import secure wallet
from security_validators import validate_password, validate_address, sanitize_input


class CreateWalletRequest(BaseModel):
    name: str
    password: str
    label: Optional[str] = "My Wallet"


class UnlockWalletRequest(BaseModel):
    name: str
    password: str


class CreateAddressRequest(BaseModel):
    wallet_name: str
    label: Optional[str] = ""


class SendTransactionRequest(BaseModel):
    from_address: str
    to_address: str
    amount: float
    password: str


class ZionWalletManager:
    """
    SECURE ZION Wallet Management System
    
    Uses ZionWallet class with mandatory encryption for all private keys.
    SECURITY FEATURES:
    - All private keys encrypted with user password
    - No plain text key storage
    - Secure wallet unlocking
    """
    
    def __init__(self):
        self.wallet_dir = "wallets/"
        self.active_wallets: Dict[str, ZionWallet] = {}  # name -> ZionWallet instance
        
        # Ensure wallet directory exists
        os.makedirs(self.wallet_dir, exist_ok=True)
    
    def create_wallet(self, name: str, password: str, label: str = "My Wallet") -> Dict:
        """
        Create new ZION wallet with MANDATORY ENCRYPTION and PASSWORD VALIDATION
        
        SECURITY: 
        - All private keys are encrypted with password
        - Strong password required (12+ chars, uppercase, digit, special)
        - Wallet name sanitized
        """
        try:
            # SECURITY: Validate password strength
            is_valid, error_msg = validate_password(password)
            if not is_valid:
                return {
                    'success': False,
                    'error': f'Password validation failed: {error_msg}'
                }
            
            # SECURITY: Sanitize wallet name
            name = sanitize_input(name)
            label = sanitize_input(label)
            
            if not name or len(name) < 1:
                return {
                    'success': False,
                    'error': 'Wallet name cannot be empty'
                }
            
            wallet_file = f"{self.wallet_dir}/{name}.json"
            
            # Check if wallet already exists
            if os.path.exists(wallet_file):
                return {
                    'success': False,
                    'error': f'Wallet "{name}" already exists'
                }
            
            # Create SECURE wallet with encryption
            wallet = ZionWallet(wallet_file=wallet_file, password=password)
            
            # Get primary address
            if wallet.addresses:
                primary_address = wallet.addresses[0].address
            else:
                return {
                    'success': False,
                    'error': 'Failed to create primary address'
                }
            
            # Save wallet (with encrypted keys)
            wallet.save_wallet()
            
            # Add to active wallets
            self.active_wallets[name] = wallet
            
            return {
                'success': True,
                'wallet_name': name,
                'primary_address': primary_address,
                'balance': 0,
                'message': f'Wallet "{name}" created successfully with ENCRYPTION! Start mining to earn ZION!'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Failed to create wallet: {str(e)}'
            }
    
    def list_wallets(self) -> Dict:
        """List all available wallets"""
        try:
            import glob
            
            wallet_files = glob.glob(f"{self.wallet_dir}/*.json")
            wallets = []
            
            for wallet_file in wallet_files:
                try:
                    with open(wallet_file, 'r') as f:
                        data = json.load(f)
                    
                    wallet_name = Path(wallet_file).stem
                    wallets.append({
                        'name': wallet_name,
                        'label': data.get('label', ''),
                        'created_at': data.get('created_at', 'Unknown'),
                        'address_count': len(data.get('addresses', [])),
                        'total_balance': 0,  # Would need blockchain query
                        'unlocked': wallet_name in self.active_wallets,
                        'encrypted': True  # All wallets now encrypted
                    })
                except Exception as e:
                    print(f"Error reading wallet {wallet_file}: {e}")
                    continue
            
            return {
                'success': True,
                'wallets': wallets,
                'count': len(wallets)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Failed to list wallets: {str(e)}'
            }
    
    def unlock_wallet(self, name: str, password: str) -> Dict:
        """
        Unlock wallet for use (decrypt private keys)
        
        SECURITY: Password required to decrypt private keys.
        """
        try:
            wallet_file = f"{self.wallet_dir}/{name}.json"
            
            if not os.path.exists(wallet_file):
                return {
                    'success': False,
                    'error': f'Wallet "{name}" not found'
                }
            
            # Load wallet with encryption
            # Note: For existing wallets, password is needed to decrypt
            try:
                wallet = ZionWallet(wallet_file=wallet_file, password=None)
                wallet.unlock_wallet(password)
            except Exception as e:
                # Try loading as new wallet if old format
                return {
                    'success': False,
                    'error': f'Failed to unlock wallet. Wrong password or corrupted wallet: {str(e)}'
                }
            
            # Add to active wallets
            self.active_wallets[name] = wallet
            
            # Get wallet info
            addresses = [{'address': addr.address, 'label': addr.label} 
                        for addr in wallet.addresses]
            
            return {
                'success': True,
                'wallet_name': name,
                'addresses': addresses,
                'total_balance': 0,  # Would need blockchain query
                'message': f'Wallet "{name}" unlocked successfully with SECURE ENCRYPTION!'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Failed to unlock wallet: {str(e)}'
            }
    
    def get_wallet_info(self, name: str) -> Dict:
        """Get wallet information (wallet must be unlocked)"""
        try:
            if name not in self.active_wallets:
                return {
                    'success': False,
                    'error': f'Wallet "{name}" is not unlocked. Please unlock first.'
                }
            
            wallet = self.active_wallets[name]
            
            # Get addresses (without private keys for security)
            addresses = []
            for addr in wallet.addresses:
                addresses.append({
                    'address': addr.address,
                    'label': addr.label,
                    'balance': wallet.get_balance(addr.address)
                })
            
            return {
                'success': True,
                'wallet': {
                    'name': name,
                    'addresses': addresses,
                    'total_balance': sum(addr['balance'] for addr in addresses),
                    'address_count': len(addresses),
                    'encrypted': True  # All wallets are encrypted now
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Failed to get wallet info: {str(e)}'
            }
    
    def create_address(self, wallet_name: str, label: str = "") -> Dict:
        """Create new address in existing wallet (wallet must be unlocked)"""
        try:
            if wallet_name not in self.active_wallets:
                return {
                    'success': False,
                    'error': f'Wallet "{wallet_name}" is not unlocked. Please unlock first.'
                }
            
            wallet = self.active_wallets[wallet_name]
            
            # Create new address using secure wallet (with encryption)
            new_address = wallet.create_address(label or f'Address {len(wallet.addresses)}')
            
            # Save wallet with encrypted keys
            wallet.save_wallet()
            
            return {
                'success': True,
                'address': new_address,
                'label': label,
                'message': f'New address created with ENCRYPTION in wallet "{wallet_name}"'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Failed to create address: {str(e)}'
            }


# Global wallet manager instance
wallet_manager = ZionWalletManager()


# API Endpoints
def register_wallet_endpoints(app):
    """Register wallet API endpoints"""
    
    @app.post("/api/wallet/create")
    async def create_wallet(request: CreateWalletRequest):
        """Create new wallet"""
        result = wallet_manager.create_wallet(
            request.name, 
            request.password, 
            request.label
        )
        
        if not result['success']:
            raise HTTPException(status_code=400, detail=result['error'])
        
        return {
            'success': True,
            'data': result,
            'message': f'🏦 Wallet "{request.name}" created successfully!'
        }
    
    @app.get("/api/wallet/list")
    async def list_wallets():
        """List all wallets"""
        result = wallet_manager.list_wallets()
        
        return {
            'success': True,
            'data': result,
            'message': '📋 Wallet list retrieved'
        }
    
    @app.post("/api/wallet/unlock")
    async def unlock_wallet(request: UnlockWalletRequest):
        """Unlock wallet"""
        result = wallet_manager.unlock_wallet(request.name, request.password)
        
        if not result['success']:
            raise HTTPException(status_code=401, detail=result['error'])
        
        return {
            'success': True,
            'data': result,
            'message': f'🔓 Wallet "{request.name}" unlocked!'
        }
    
    @app.get("/api/wallet/{wallet_name}")
    async def get_wallet(wallet_name: str):
        """Get wallet information"""
        result = wallet_manager.get_wallet_info(wallet_name)
        
        if not result['success']:
            raise HTTPException(status_code=404, detail=result['error'])
        
        return {
            'success': True,
            'data': result['wallet'],
            'message': f'💰 Wallet "{wallet_name}" info retrieved'
        }
    
    @app.post("/api/wallet/address/create")
    async def create_address(request: CreateAddressRequest):
        """Create new address in wallet"""
        result = wallet_manager.create_address(request.wallet_name, request.label)
        
        if not result['success']:
            raise HTTPException(status_code=400, detail=result['error'])
        
        return {
            'success': True,
            'data': result,
            'message': f'🆕 New address created!'
        }