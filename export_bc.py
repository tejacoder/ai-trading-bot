#!/usr/bin/env python3
"""
Export Builder Code
Requires password to decrypt wallet and export builder code
"""

import sys
import os
import getpass

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from wallet_encrypted import EncryptedWallet

def main():
    print("\n" + "="*60)
    print("🔐 Export Builder Code")
    print("="*60 + "\n")
    
    # Wallet path
    wallet_path = os.path.expanduser("~/.agent-wallet/.wallet_data")
    
    # Check if wallet exists
    if not os.path.exists(wallet_path):
        print(f"❌ Wallet not found: {wallet_path}")
        print("\n💡 Run setup_auto.py first to create encrypted wallet")
        return
    
    # Get password
    password = getpass.getpass("Enter password: ")
    
    try:
        # Load encrypted wallet
        print("\n🔓 Decrypting wallet...")
        wallet = EncryptedWallet.load_encrypted(wallet_path, password)
        print(f"✅ Wallet loaded: {wallet.address}")
        
        # Export builder code
        print("\n🏗️  Requesting builder code from Base API...")
        builder_code = wallet.export_builder_code(password)
        
        print("\n" + "="*60)
        print("✅ SUCCESS!")
        print("="*60)
        print(f"\n📋 Builder Code: {builder_code}")
        print(f"📋 Wallet: {wallet.address}")
        
        print("\n💡 Add to config.py:")
        print(f'BUILDER_CODE = "{builder_code}"')
        
        print("\n" + "="*60 + "\n")
        
    except ValueError as e:
        print(f"\n❌ Error: {e}")
        print("💡 Check your password and try again")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
