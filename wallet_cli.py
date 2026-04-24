#!/usr/bin/env python3
"""
Wallet Operations CLI
Complete wallet management tool with all features
"""

import sys
import json
from wallet_operations import SimpleWalletWithBuilderCode

def show_menu():
    """Show main menu"""
    print("\n" + "="*60)
    print("💼 Wallet Operations")
    print("="*60)
    print("\n📊 Balance & Info:")
    print("  1. Check ETH balance")
    print("  2. Check token balance (USDC/DAI/WETH)")
    print("  3. Show wallet info")
    
    print("\n💸 Send & Transfer:")
    print("  4. Send ETH")
    print("  5. Send tokens")
    
    print("\n🔄 Swap:")
    print("  6. Swap tokens (ETH ↔ USDC)")
    
    print("\n🎨 NFT:")
    print("  7. Mint NFT")
    print("  8. Deploy NFT contract")
    
    print("\n🔧 Advanced:")
    print("  9. View transaction history")
    print("  10. Export wallet info")
    
    print("\n  0. Exit")
    print("="*60)

def check_eth_balance(wallet):
    """Check ETH balance"""
    print("\n💰 Checking ETH balance...")
    result = wallet.get_balance()
    
    print(f"\n✅ Balance:")
    print(f"   ETH: {result['eth']:.6f}")
    print(f"   USD: ${result['usd']:.2f}")
    print(f"   Address: {wallet.address}")

def check_token_balance(wallet):
    """Check token balance"""
    print("\n💰 Check Token Balance")
    print("\nAvailable tokens:")
    print("  1. USDC")
    print("  2. DAI")
    print("  3. WETH")
    
    choice = input("\nSelect token (1-3): ").strip()
    
    token_map = {
        "1": "USDC",
        "2": "DAI",
        "3": "WETH"
    }
    
    token = token_map.get(choice)
    if not token:
        print("❌ Invalid choice!")
        return
    
    print(f"\n💰 Checking {token} balance...")
    result = wallet.get_token_balance(token)
    
    print(f"\n✅ Balance:")
    print(f"   {token}: {result['balance']:.6f}")
    print(f"   USD: ${result['usd']:.2f}")

def show_wallet_info(wallet):
    """Show wallet info"""
    print("\n📋 Wallet Information")
    print("="*60)
    print(f"Address: {wallet.address}")
    print(f"Builder Code: {wallet.builder_code}")
    print(f"Network: Base Mainnet")
    print(f"Chain ID: 8453")
    
    # Get balances
    eth_balance = wallet.get_balance()
    usdc_balance = wallet.get_token_balance("USDC")
    
    print(f"\n💰 Balances:")
    print(f"   ETH: {eth_balance['eth']:.6f} (${eth_balance['usd']:.2f})")
    print(f"   USDC: {usdc_balance['balance']:.2f} (${usdc_balance['usd']:.2f})")
    print(f"   Total: ${eth_balance['usd'] + usdc_balance['usd']:.2f}")
    
    print(f"\n🔗 Links:")
    print(f"   Basescan: https://basescan.org/address/{wallet.address}")
    print(f"   Builder Code: {wallet.builder_code}")
    print("="*60)

def send_eth(wallet):
    """Send ETH"""
    print("\n💸 Send ETH")
    
    to_address = input("To address: ").strip()
    amount = input("Amount (ETH): ").strip()
    
    try:
        amount_float = float(amount)
    except:
        print("❌ Invalid amount!")
        return
    
    confirm = input(f"\nSend {amount_float} ETH to {to_address}? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("❌ Cancelled")
        return
    
    print(f"\n🔄 Sending {amount_float} ETH...")
    
    try:
        tx_hash = wallet.send_eth_with_builder_code(
            to_address=to_address,
            amount_eth=amount_float
        )
        
        print(f"\n✅ Transaction sent!")
        print(f"   TX: {tx_hash}")
        print(f"   Basescan: https://basescan.org/tx/{tx_hash}")
        print(f"   Builder code: {wallet.builder_code} ✅")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")

def swap_tokens(wallet):
    """Swap tokens"""
    print("\n🔄 Swap Tokens")
    print("\nAvailable swaps:")
    print("  1. ETH → USDC")
    print("  2. USDC → ETH")
    print("  3. ETH → DAI")
    print("  4. DAI → ETH")
    
    choice = input("\nSelect swap (1-4): ").strip()
    
    swap_map = {
        "1": ("ETH", "USDC"),
        "2": ("USDC", "ETH"),
        "3": ("ETH", "DAI"),
        "4": ("DAI", "ETH")
    }
    
    swap = swap_map.get(choice)
    if not swap:
        print("❌ Invalid choice!")
        return
    
    from_token, to_token = swap
    
    amount = input(f"Amount ({from_token}): ").strip()
    
    try:
        amount_float = float(amount)
    except:
        print("❌ Invalid amount!")
        return
    
    confirm = input(f"\nSwap {amount_float} {from_token} → {to_token}? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("❌ Cancelled")
        return
    
    print(f"\n🔄 Swapping {amount_float} {from_token} → {to_token}...")
    
    try:
        tx_hash = wallet.swap_tokens(
            from_token=from_token,
            to_token=to_token,
            amount=amount_float
        )
        
        print(f"\n✅ Swap successful!")
        print(f"   TX: {tx_hash}")
        print(f"   Basescan: https://basescan.org/tx/{tx_hash}")
        print(f"   Builder code: {wallet.builder_code} ✅")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")

def mint_nft(wallet):
    """Mint NFT"""
    print("\n🎨 Mint NFT")
    
    contract_address = input("NFT contract address: ").strip()
    token_uri = input("Token URI (metadata): ").strip()
    
    if not contract_address or not token_uri:
        print("❌ Contract address and token URI required!")
        return
    
    confirm = input(f"\nMint NFT on {contract_address}? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("❌ Cancelled")
        return
    
    print(f"\n🔄 Minting NFT...")
    
    try:
        tx_hash = wallet.mint_nft(
            contract_address=contract_address,
            token_uri=token_uri
        )
        
        print(f"\n✅ NFT minted!")
        print(f"   TX: {tx_hash}")
        print(f"   Basescan: https://basescan.org/tx/{tx_hash}")
        print(f"   Builder code: {wallet.builder_code} ✅")
        print(f"\n   View on OpenSea (wait ~30 min):")
        print(f"   https://opensea.io/assets/base/{contract_address}/[token_id]")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")

def deploy_nft_contract(wallet):
    """Deploy NFT contract"""
    print("\n🎨 Deploy NFT Contract")
    
    name = input("NFT name: ").strip()
    symbol = input("NFT symbol: ").strip()
    
    if not name or not symbol:
        print("❌ Name and symbol required!")
        return
    
    confirm = input(f"\nDeploy NFT contract '{name}' ({symbol})? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("❌ Cancelled")
        return
    
    print(f"\n🔄 Deploying NFT contract...")
    print("⚠️  This feature requires contract compilation.")
    print("   Use the full implementation in contracts/ directory")
    print("   Or use deploy_nft_now.py script")
    
    print(f"\n💡 Quick deploy:")
    print(f"   python3 deploy_nft_now.py")

def export_wallet_info(wallet):
    """Export wallet info"""
    print("\n📤 Export Wallet Info")
    
    filename = input("Filename (default: wallet_info.json): ").strip()
    if not filename:
        filename = "wallet_info.json"
    
    info = {
        "address": wallet.address,
        "builder_code": wallet.builder_code,
        "network": "Base Mainnet",
        "chain_id": 8453,
        "basescan": f"https://basescan.org/address/{wallet.address}"
    }
    
    # Get balances
    try:
        eth_balance = wallet.get_balance()
        usdc_balance = wallet.get_token_balance("USDC")
        
        info["balances"] = {
            "eth": eth_balance['eth'],
            "usdc": usdc_balance['balance'],
            "total_usd": eth_balance['usd'] + usdc_balance['usd']
        }
    except:
        pass
    
    with open(filename, 'w') as f:
        json.dump(info, f, indent=2)
    
    print(f"\n✅ Wallet info exported to: {filename}")

def main():
    """Main function"""
    print("\n" + "="*60)
    print("💼 Wallet Operations CLI")
    print("="*60)
    
    # Load wallet
    try:
        wallet = SimpleWalletWithBuilderCode.load_from_file()
        print(f"\n✅ Wallet loaded: {wallet.address}")
        print(f"   Builder code: {wallet.builder_code}")
    except Exception as e:
        print(f"\n❌ Error loading wallet: {e}")
        print("\n💡 Create wallet first:")
        print("   python3 setup_auto.py")
        return
    
    # Main loop
    while True:
        show_menu()
        
        choice = input("\nSelect option (0-10): ").strip()
        
        if choice == "0":
            print("\n👋 Goodbye!")
            break
        elif choice == "1":
            check_eth_balance(wallet)
        elif choice == "2":
            check_token_balance(wallet)
        elif choice == "3":
            show_wallet_info(wallet)
        elif choice == "4":
            send_eth(wallet)
        elif choice == "5":
            print("\n💡 Use option 6 (Swap) for token transfers")
        elif choice == "6":
            swap_tokens(wallet)
        elif choice == "7":
            mint_nft(wallet)
        elif choice == "8":
            deploy_nft_contract(wallet)
        elif choice == "9":
            print("\n💡 View transactions on Basescan:")
            print(f"   https://basescan.org/address/{wallet.address}")
        elif choice == "10":
            export_wallet_info(wallet)
        else:
            print("\n❌ Invalid option!")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
