#!/usr/bin/env python3
"""
Fully Automated Agent Setup
- Auto create wallet
- Auto request builder code
- Auto configure
"""

import json
import os
import sys
import requests
from web3 import Web3

def create_wallet():
    """Create new wallet"""
    print("🔐 Creating wallet...")
    account = Web3().eth.account.create()
    
    wallet_data = {
        'address': account.address,
        'private_key': account.key.hex()
    }
    
    with open('wallet.json', 'w') as f:
        json.dump(wallet_data, f, indent=2)
    
    print(f"✅ Wallet: {account.address}")
    return account.address

def request_builder_code(email):
    """Auto request builder code from Base API"""
    print(f"\n🏗️  Requesting builder code for {email}...")
    
    try:
        response = requests.post(
            'https://api.base.dev/v1/agents/builder-codes',
            headers={'Content-Type': 'application/json'},
            json={'email': email},
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
    
    # Update builder code
    config = config.replace(
        'BUILDER_CODE = "bc_t0mz06m4"',
        f'BUILDER_CODE = "{builder_code}"'
    )
    
    with open('config.py', 'w') as f:
        f.write(config)
    
    print(f"✅ Config updated")

def main():
    print("\n" + "="*60)
    print("🤖 Fully Automated Agent Setup")
    print("="*60 + "\n")
    
    # Get email
    email = input("Enter email for builder code: ").strip()
    
    if not email:
        print("❌ Email required!")
        return
    
    # Create wallet
    address = create_wallet()
    
    # Request builder code
    builder_code = request_builder_code(email)
    
    if not builder_code:
        print("\n❌ Failed to get builder code!")
        print("   Try manual setup instead:")
        print("   python3 setup_new_agent.py")
        return
    
    # Update config
    update_config(builder_code)
    
    # Show summary
    print("\n" + "="*60)
    print("✅ SETUP COMPLETE!")
    print("="*60)
    print(f"\n📋 Agent Info:")
    print(f"   Wallet: {address}")
    print(f"   Builder Code: {builder_code}")
    print(f"\n💰 Fund Wallet:")
    print(f"   Send ETH + USDC to: {address}")
    print(f"\n🧪 Test:")
    print(f"   python3 trading_bot.py backtest 7")
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    main()
