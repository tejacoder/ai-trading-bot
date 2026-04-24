#!/usr/bin/env python3
"""
Encrypted Wallet with Builder Code Support
- AES-256 encryption for private key
- Hidden filename (.wallet_data)
- Password-based key derivation
- Decrypt only when needed
"""

import json
import os
from web3 import Web3
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import requests

# Import from wallet_operations for transaction methods
import sys
sys.path.insert(0, os.path.dirname(__file__))
from wallet_operations import SimpleWalletWithBuilderCode

class EncryptedWallet:
    """Encrypted wallet with password protection"""
    
    def __init__(self, address: str, encrypted_key: bytes, salt: bytes):
        self.address = address
        self.encrypted_key = encrypted_key
        self.salt = salt
        self._decrypted_key = None
    
    @staticmethod
    def _derive_key(password: str, salt: bytes) -> bytes:
        """Derive encryption key from password using PBKDF2"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key
    
    @staticmethod
    def create_new(password: str) -> 'EncryptedWallet':
        """Create new encrypted wallet"""
        # Generate new account
        w3 = Web3()
        account = w3.eth.account.create()
        
        # Generate salt
        salt = os.urandom(16)
        
        # Derive encryption key from password
        key = EncryptedWallet._derive_key(password, salt)
        
        # Encrypt private key
        f = Fernet(key)
        encrypted_key = f.encrypt(account.key.hex().encode())
        
        return EncryptedWallet(account.address, encrypted_key, salt)
    
    @staticmethod
    def load_encrypted(path: str, password: str) -> 'EncryptedWallet':
        """Load encrypted wallet from file"""
        path = os.path.expanduser(path)
        
        if not os.path.exists(path):
            raise FileNotFoundError(f"Wallet file not found: {path}")
        
        with open(path, 'r') as f:
            data = json.load(f)
        
        address = data['address']
        encrypted_key = base64.b64decode(data['encrypted_key'])
        salt = base64.b64decode(data['salt'])
        
        wallet = EncryptedWallet(address, encrypted_key, salt)
        
        # Verify password by trying to decrypt
        try:
            wallet._decrypt_key(password)
        except Exception:
            raise ValueError("Invalid password or corrupted wallet")
        
        return wallet
    
    def save_encrypted(self, path: str, password: str):
        """Save encrypted wallet to file"""
        path = os.path.expanduser(path)
        
        # Create directory if not exists
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        data = {
            'address': self.address,
            'encrypted_key': base64.b64encode(self.encrypted_key).decode(),
            'salt': base64.b64encode(self.salt).decode()
        }
        
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
        
        # Set file permissions (owner only)
        os.chmod(path, 0o600)
    
    def _decrypt_key(self, password: str) -> str:
        """Decrypt private key (internal use only)"""
        if self._decrypted_key:
            return self._decrypted_key
        
        # Derive key from password
        key = self._derive_key(password, self.salt)
        
        # Decrypt private key
        f = Fernet(key)
        decrypted = f.decrypt(self.encrypted_key)
        self._decrypted_key = decrypted.decode()
        
        return self._decrypted_key
    
    def get_wallet_instance(self, password: str) -> SimpleWalletWithBuilderCode:
        """Get wallet instance for transactions (requires password)"""
        private_key = self._decrypt_key(password)
        
        # Create temporary wallet instance
        w3 = Web3(Web3.HTTPProvider("https://mainnet.base.org"))
        account = w3.eth.account.from_key(private_key)
        
        # Load builder code from config
        try:
            with open('config.py', 'r') as f:
                config = f.read()
                import re
                match = re.search(r'BUILDER_CODE = "([^"]+)"', config)
                builder_code = match.group(1) if match else None
        except:
            builder_code = None
        
        return SimpleWalletWithBuilderCode(
            w3=w3,
            account=account,
            builder_code=builder_code
        )
    
    def send_eth_with_builder_code(self, to_address: str, amount_eth: float, password: str) -> str:
        """Send ETH with builder code (requires password)"""
        wallet = self.get_wallet_instance(password)
        return wallet.send_eth_with_builder_code(to_address, amount_eth)
    
    def swap_tokens(self, from_token: str, to_token: str, amount: float, password: str) -> str:
        """Swap tokens (requires password)"""
        wallet = self.get_wallet_instance(password)
        return wallet.swap_tokens(from_token, to_token, amount)
    
    def mint_nft(self, contract_address: str, token_uri: str, password: str) -> str:
        """Mint NFT (requires password)"""
        wallet = self.get_wallet_instance(password)
        return wallet.mint_nft(contract_address, token_uri)
    
    def get_balance(self) -> float:
        """Get ETH balance (no password needed)"""
        w3 = Web3(Web3.HTTPProvider("https://mainnet.base.org"))
        balance_wei = w3.eth.get_balance(self.address)
        return w3.from_wei(balance_wei, 'ether')
    
    def get_token_balance(self, token: str) -> float:
        """Get token balance (no password needed)"""
        from config import TOKENS
        
        w3 = Web3(Web3.HTTPProvider("https://mainnet.base.org"))
        token_address = TOKENS.get(token)
        
        if not token_address:
            raise ValueError(f"Unknown token: {token}")
        
        # ERC-20 ABI (balanceOf only)
        abi = [{"constant":True,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"type":"function"},{"constant":True,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"type":"function"}]
        
        contract = w3.eth.contract(address=token_address, abi=abi)
        balance = contract.functions.balanceOf(self.address).call()
        decimals = contract.functions.decimals().call()
        
        return balance / (10 ** decimals)
    
    def export_builder_code(self, password: str) -> str:
        """Export builder code (requires password to verify ownership)"""
        # Verify password
        self._decrypt_key(password)
        
        # Request builder code from Base API
        try:
            response = requests.post(
                'https://api.base.dev/v1/agents/builder-codes',
                headers={'Content-Type': 'application/json'},
                json={'walletAddress': self.address},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('builderCode')
            else:
                raise Exception(f"API error: {response.status_code}")
        except Exception as e:
            raise Exception(f"Failed to export builder code: {e}")


def main():
    """Example usage"""
    import getpass
    
    print("\n🔐 Encrypted Wallet Demo\n")
    
    # Create new wallet
    print("Creating new encrypted wallet...")
    password = getpass.getpass("Enter password: ")
    password_confirm = getpass.getpass("Confirm password: ")
    
    if password != password_confirm:
        print("❌ Passwords don't match!")
        return
    
    wallet = EncryptedWallet.create_new(password)
    print(f"✅ Wallet created: {wallet.address}")
    
    # Save encrypted
    wallet_path = "~/.agent-wallet/.wallet_data"
    wallet.save_encrypted(wallet_path, password)
    print(f"✅ Saved encrypted to: {wallet_path}")
    
    # Load encrypted
    print("\nLoading encrypted wallet...")
    password = getpass.getpass("Enter password: ")
    wallet = EncryptedWallet.load_encrypted(wallet_path, password)
    print(f"✅ Loaded: {wallet.address}")
    
    # Check balance
    balance = wallet.get_balance()
    print(f"💰 Balance: {balance} ETH")
    
    # Export builder code
    print("\nExporting builder code...")
    builder_code = wallet.export_builder_code(password)
    print(f"✅ Builder code: {builder_code}")


if __name__ == "__main__":
    main()
