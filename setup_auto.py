#!/usr/bin/env python3
"""
Fully Automated Agent Setup (FIXED v2)
- Check existing wallet first
- Auto request builder code (using wallet address!)
- Auto configure
"""

import json
import os
import sys
import requests
from web3 import Web3

def load_or_create_wallet():
    """Load existing wallet or create new one"""
    wallet_path = os.path.expanduser("~/.simple-wallet/wallet.json")
    
    # Check if wallet exists
    if os.path.exists(wallet_path):
        print("🔐 Loading existing wallet...")
        with open(wallet_path, 'r') as f:
            wallet_data = json.load(f)
        wallet_address = wallet_data['address']
        print(f"✅ Wallet: {wallet_address}")
        return wallet_address
    
    # Create new wallet
    print("🔐 Creating new wallet...")
    account = Web3().eth.account.create()
    
    wallet_data = {
        'address': account.address,
        'private_key': account.key.hex()
    }
    
    # Create directory if not exists
    os.makedirs(os.path.dirname(wallet_path), exist_ok=True)
    
    with open(wallet_path, 'w') as f:
        json.dump(wallet_data, f, indent=2)
    
    print(f"✅ Wallet: {account.address}")
    return account.address

def request_builder_code(wallet_address):
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

def update_config(builder_code):
    """Update config.py"""
    print(f"\n⚙️  Updating config...")
    
    with open('config.py', 'r') as f:
        config = f.read()
    
    # Update builder code (find any existing builder code pattern)
    import re
    config = re.sub(
        r'BUILDER_CODE = "bc_[a-z0-9]+"',
        f'BUILDER_CODE = "{builder_code}"',
        config
    )
    
    with open('config.py', 'w') as f:
        f.write(config)
    
    print(f"✅ Config updated")

def main():
    print("\n" + "="*60)
    print("🤖 Fully Automated Agent Setup")
    print("="*60)
    
    # Load or create wallet
    wallet_address = load_or_create_wallet()
    
    # Request builder code using wallet address
    builder_code = request_builder_code(wallet_address)
    
    if not builder_code:
        print("\n❌ Failed to get builder code!")
        print("\n💡 Try manual request:")
        print(f"curl -X POST https://api.base.dev/v1/agents/builder-codes \\")
        print(f"  -H 'Content-Type: application/json' \\")
        print(f"  -d '{{\"walletAddress\": \"{wallet_address}\"}}'")
        print("\nOr use semi-auto setup:")
        print("python3 setup_new_agent.py")
        return
    
    # Update config
    update_config(builder_code)
    
    # Show summary
    print("\n" + "="*60)
    print("✅ SETUP COMPLETE!")
    print("="*60)
    print(f"\n📋 Agent Info:")
    print(f"   Wallet: {wallet_address}")
    print(f"   Builder Code: {builder_code}")
    print(f"\n💰 Fund Wallet:")
    print(f"   Send ETH + USDC to: {wallet_address}")
    print(f"   Minimum: 0.001 ETH + $100 USDC")
    print(f"\n🧪 Test:")
    print(f"   Backtest: python3 trading_bot.py backtest 7")
    print(f"   Dry run: python3 trading_bot.py 300")
    print(f"\n📚 Docs:")
    print(f"   RINGKASAN.md - Full documentation")
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    main()
