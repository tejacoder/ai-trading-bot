#!/usr/bin/env python3
"""
Trading Bot Wallet Adapter
Supports both encrypted and plaintext wallets
"""

import os
import sys
import getpass
from pathlib import Path

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from wallet_encrypted import EncryptedWallet
from wallet_operations import SimpleWalletWithBuilderCode
from config import WALLET_PATH, BUILDER_CODE

class TradingBotWallet:
    """
    Wallet adapter for trading bot
    Automatically detects encrypted vs plaintext wallet
    """
    
    def __init__(self, password: str = None):
        """
        Initialize wallet
        
        Args:
            password: Password for encrypted wallet (will prompt if needed)
        """
        self.wallet_path = os.path.expanduser(WALLET_PATH)
        self.builder_code = BUILDER_CODE
        self.password = password
        self._wallet = None
        self._is_encrypted = None
        
    def _detect_wallet_type(self) -> bool:
        """Detect if wallet is encrypted or plaintext"""
        if not os.path.exists(self.wallet_path):
            raise FileNotFoundError(f"Wallet not found: {self.wallet_path}")
        
        # Check if it's encrypted (has 'encrypted_key' field)
        import json
        try:
            with open(self.wallet_path, 'r') as f:
                data = json.load(f)
            return 'encrypted_key' in data
        except:
            return False
    
    def _get_password(self) -> str:
        """Get password (from env, param, or prompt)"""
        if self.password:
            return self.password
        
        # Try environment variable
        password = os.getenv('WALLET_PASSWORD')
        if password:
            return password
        
        # Prompt user
        return getpass.getpass("Wallet password: ")
    
    def load(self):
        """Load wallet (encrypted or plaintext)"""
        if self._wallet:
            return self._wallet
        
        # Detect wallet type
        self._is_encrypted = self._detect_wallet_type()
        
        if self._is_encrypted:
            # Load encrypted wallet
            password = self._get_password()
            self._wallet = EncryptedWallet.load_encrypted(
                self.wallet_path,
                password
            )
            self.password = password  # Cache password
        else:
            # Load plaintext wallet
            import json
            with open(self.wallet_path, 'r') as f:
                data = json.load(f)
            
            self._wallet = SimpleWalletWithBuilderCode(
                private_key=data['private_key']
            )
            self._wallet.builder_code = self.builder_code
        
        return self._wallet
    
    @property
    def address(self) -> str:
        """Get wallet address"""
        if not self._wallet:
            self.load()
        return self._wallet.address
    
    def get_balance(self) -> float:
        """Get ETH balance"""
        if not self._wallet:
            self.load()
        return self._wallet.get_balance()
    
    def get_token_balance(self, token: str) -> float:
        """Get token balance"""
        if not self._wallet:
            self.load()
        return self._wallet.get_token_balance(token)
    
    def send_eth_with_builder_code(self, to_address: str, amount_eth: float) -> str:
        """Send ETH with builder code"""
        if not self._wallet:
            self.load()
        
        if self._is_encrypted:
            return self._wallet.send_eth_with_builder_code(
                to_address,
                amount_eth,
                self.password
            )
        else:
            return self._wallet.send_eth_with_builder_code(
                to_address,
                amount_eth
            )
    
    def swap_tokens(self, from_token: str, to_token: str, amount: float) -> str:
        """Swap tokens"""
        if not self._wallet:
            self.load()
        
        if self._is_encrypted:
            return self._wallet.swap_tokens(
                from_token,
                to_token,
                amount,
                self.password
            )
        else:
            return self._wallet.swap_tokens(
                from_token,
                to_token,
                amount
            )
    
    def mint_nft(self, contract_address: str, token_uri: str) -> str:
        """Mint NFT"""
        if not self._wallet:
            self.load()
        
        if self._is_encrypted:
            return self._wallet.mint_nft(
                contract_address,
                token_uri,
                self.password
            )
        else:
            return self._wallet.mint_nft(
                contract_address,
                token_uri
            )


def main():
    """Example usage"""
    print("\n💼 Trading Bot Wallet Adapter\n")
    
    # Initialize wallet
    wallet = TradingBotWallet()
    
    # Load wallet (auto-detects type)
    wallet.load()
    
    print(f"✅ Wallet loaded: {wallet.address}")
    print(f"   Type: {'Encrypted' if wallet._is_encrypted else 'Plaintext'}")
    
    # Check balance
    balance = wallet.get_balance()
    print(f"💰 Balance: {balance} ETH")
    
    # Check USDC balance
    try:
        usdc_balance = wallet.get_token_balance("USDC")
        print(f"💵 USDC: {usdc_balance}")
    except:
        print(f"💵 USDC: 0")


if __name__ == "__main__":
    main()
