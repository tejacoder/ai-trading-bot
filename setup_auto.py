#!/usr/bin/env python3
"""
Fully Automated Agent Setup with Encrypted Wallet
- Check existing encrypted wallet first
- Auto request builder code (using wallet address!)
- Auto configure
- Password protected
"""

import json
import os
import sys
import requests
import getpass

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from wallet_encrypted import EncryptedWallet

def load_or_create_wallet(password: str) -> tuple:
    """Load existing wallet or create new one"""
    wallet_path = os.path.expanduser("~/.agent-wallet/.wallet_data")
    
    # Check if wallet exists
    if os.path.exists(wallet_path):
        print("🔐 Loading existing encrypted wallet...")
        try:
            wallet = EncryptedWallet.load_encrypted(wallet_path, password)
            wallet_address = wallet.address
            print(f"✅ Wallet: {wallet_address}")
            return wallet_address, wallet
        except ValueError:
            print("❌ Invalid password!")
            return None, None
    
    # Create new wallet
    print("🔐 Creating new encrypted wallet...")
    wallet = EncryptedWallet.create_new(password)
    wallet_address = wallet.address
    
    # Save encrypted
    wallet.save_encrypted(wallet_path, password)
    print(f"✅ Wallet: {wallet_address}")
    print(f"✅ Saved encrypted to: {wallet_path}")
    
    return wallet_address, wallet

def request_builder_code(wallet_address: str) -> str:
    """Auto request builder code from Base API using wallet address"""
    print(f"\n🏗️  Requesting builder code for wallet {wallet_address}...")
    
    try:
        response = requests.post(
            'https://api.base.dev/v1/agents/builder-codes',
            headers={'Content-Type': 'application/json'},
            json={'walletAddress': wallet_address},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            builder_code = data.get('builderCode')
            print(f"✅ Builder code: {builder_code}")
            return builder_code
        else:
            print(f"❌ Failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def update_config(builder_code: str, wallet_path: str):
    """Update config file with builder code"""
    print(f"\n⚙️  Saving config...")
    
    config_file = os.path.expanduser("~/.agent-wallet/.config.json")
    
    # Create directory if not exists
    os.makedirs(os.path.dirname(config_file), exist_ok=True)
    
    # Save builder code to config file
    config_data = {
        'builder_code': builder_code,
        'wallet_path': wallet_path
    }
    
    with open(config_file, 'w') as f:
        json.dump(config_data, f, indent=2)
    
    # Set file permissions (owner only)
    os.chmod(config_file, 0o600)
    
    print(f"✅ Config saved to: {config_file}")

def main():
    print("\n" + "="*60)
    print("🤖 Fully Automated Agent Setup (Encrypted)")
    print("="*60 + "\n")
    
    # Get password
    password = getpass.getpass("Enter password for wallet encryption: ")
    
    # Check if creating new wallet
    wallet_path = os.path.expanduser("~/.agent-wallet/.wallet_data")
    if not os.path.exists(wallet_path):
        password_confirm = getpass.getpass("Confirm password: ")
        if password != password_confirm:
            print("\n❌ Passwords don't match!")
            return
    
    print()
    
    # Load or create wallet
    wallet_address, wallet = load_or_create_wallet(password)
    
    if not wallet_address:
        return
    
    # Request builder code using wallet address
    builder_code = request_builder_code(wallet_address)
    
    if not builder_code:
        print("\n❌ Failed to get builder code!")
        print("\n💡 Try manual export:")
        print("python3 export_bc.py")
        return
    
    # Update config
    update_config(builder_code, "~/.agent-wallet/.wallet_data")
    
    # Show summary
    print("\n" + "="*60)
    print("✅ SETUP COMPLETE!")
    print("="*60)
    print(f"\n📋 Agent Info:")
    print(f"   Wallet: {wallet_address}")
    print(f"   Builder Code: {builder_code}")
    print(f"   Encrypted: ✅ AES-256")
    print(f"\n💰 Fund Wallet:")
    print(f"   Send ETH + USDC to: {wallet_address}")
    print(f"   Minimum: 0.001 ETH + $100 USDC")
    print(f"\n🔐 Security:")
    print(f"   Wallet file: ~/.agent-wallet/.wallet_data")
    print(f"   Encryption: AES-256 with PBKDF2")
    print(f"   Password: Required for all operations")
    print(f"\n🧪 Test:")
    print(f"   Backtest: python3 trading_bot.py backtest 7")
    print(f"   Dry run: python3 trading_bot.py 300")
    print(f"\n📚 Docs:")
    print(f"   RINGKASAN.md - Full documentation")
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    main()
