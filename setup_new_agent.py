#!/usr/bin/env python3
"""
Setup New Agent - Quick setup script for new trading bot agent
"""

import json
import os
import sys
from web3 import Web3

def create_new_wallet():
    """Create new wallet for agent"""
    print("🔐 Creating new wallet...")
    
    # Create new account
    account = Web3().eth.account.create()
    
    # Wallet data
    wallet_data = {
        'address': account.address,
        'private_key': account.key.hex()
    }
    
    # Save to file
    with open('wallet.json', 'w') as f:
        json.dump(wallet_data, f, indent=2)
    
    print(f"✅ Wallet created!")
    print(f"   Address: {account.address}")
    print(f"\n⚠️  IMPORTANT: Save this private key securely!")
    print(f"   Private key: {account.key.hex()}")
    print(f"\n✅ Saved to: wallet.json")
    
    return account.address

def get_builder_code_instructions():
    """Show instructions to get builder code"""
    print("\n🏗️  Get Builder Code:")
    print("\nOption 1: Via API")
    print("─" * 60)
    print("curl -X POST https://api.base.dev/v1/agents/builder-codes \\")
    print("  -H 'Content-Type: application/json' \\")
    print("  -d '{\"email\": \"your-email@example.com\"}'")
    
    print("\nOption 2: Via Browser")
    print("─" * 60)
    print("1. Go to: https://base.org/builder-codes")
    print("2. Enter your email")
    print("3. Copy the builder code")
    
    print("\nOption 3: Use Existing")
    print("─" * 60)
    print("If you already have a builder code, use that.")
    
    builder_code = input("\nEnter your builder code (e.g., bc_abc123): ").strip()
    return builder_code

def update_config(builder_code):
    """Update config.py with builder code"""
    print(f"\n⚙️  Updating config.py...")
    
    # Read config
    with open('config.py', 'r') as f:
        config_content = f.read()
    
    # Update builder code
    config_content = config_content.replace(
        'BUILDER_CODE = "bc_t0mz06m4"',
        f'BUILDER_CODE = "{builder_code}"'
    )
    
    # Write back
    with open('config.py', 'w') as f:
        f.write(config_content)
    
    print(f"✅ Config updated with builder code: {builder_code}")

def show_next_steps(address):
    """Show next steps"""
    print("\n" + "="*60)
    print("✅ SETUP COMPLETE!")
    print("="*60)
    
    print(f"\n📋 Your Agent Info:")
    print(f"   Wallet: {address}")
    print(f"   Config: config.py")
    print(f"   Wallet file: wallet.json")
    
    print(f"\n💰 Fund Your Wallet:")
    print(f"   1. Send ETH to: {address}")
    print(f"   2. Send USDC to: {address}")
    print(f"   3. Minimum: ~$100 USDC + 0.001 ETH for gas")
    
    print(f"\n🧪 Test Your Bot:")
    print(f"   1. Backtest: python3 trading_bot.py backtest 7")
    print(f"   2. Dry run: python3 trading_bot.py 300")
    print(f"   3. Go live: Edit config.py (dry_run = False)")
    
    print(f"\n📚 Documentation:")
    print(f"   - RINGKASAN.md - Full docs (Indonesian)")
    print(f"   - QUICKSTART.md - Quick reference")
    print(f"   - BUILDER_CODE.md - Builder code info")
    
    print(f"\n⚠️  Security Reminders:")
    print(f"   - ❌ NEVER share wallet.json")
    print(f"   - ❌ NEVER commit private keys")
    print(f"   - ✅ Backup wallet.json securely")
    print(f"   - ✅ Use different wallet per agent")
    
    print("\n" + "="*60)
    print("🚀 Ready to trade!")
    print("="*60 + "\n")

def main():
    print("\n" + "="*60)
    print("🤖 AI Trading Bot - New Agent Setup")
    print("="*60 + "\n")
    
    # Check if wallet already exists
    if os.path.exists('wallet.json'):
        response = input("⚠️  wallet.json already exists. Overwrite? (yes/no): ").strip().lower()
        if response != 'yes':
            print("❌ Setup cancelled")
            return
    
    # Create wallet
    address = create_new_wallet()
    
    # Get builder code
    builder_code = get_builder_code_instructions()
    
    if not builder_code:
        print("❌ Builder code required!")
        return
    
    # Update config
    update_config(builder_code)
    
    # Show next steps
    show_next_steps(address)

if __name__ == "__main__":
    main()
