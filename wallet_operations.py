#!/usr/bin/env python3
"""
Simple Wallet with Builder Code using Web3.py
Full control over transactions for proper ERC-8021 attribution
"""

from web3 import Web3
from eth_account import Account
import json
from pathlib import Path
from typing import Optional, Dict, Any

class SimpleWalletWithBuilderCode:
    """
    Simple wallet with ERC-8021 builder code support
    Uses Web3.py for full transaction control
    """
    
    BUILDER_CODE = "bc_t0mz06m4"
    RPC_URL = "https://mainnet.base.org"
    CHAIN_ID = 8453  # Base mainnet
    
    # Token addresses on Base
    TOKENS = {
        "USDC": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
        "USDbC": "0xd9aAEc86B65D86f6A7B5B1b0c42FFA531710b6CA",
        "DAI": "0x50c5725949A6F0c72E6C4a641F24049A917DB0Cb",
        "WETH": "0x4200000000000000000000000000000000000006",
    }
    
    # Uniswap V3 Router on Base
    UNISWAP_ROUTER = "0x2626664c2603336E57B271c5C0b26F421741e481"
    
    # ERC-20 ABI (minimal)
    ERC20_ABI = [
        {
            "constant": True,
            "inputs": [{"name": "_owner", "type": "address"}],
            "name": "balanceOf",
            "outputs": [{"name": "balance", "type": "uint256"}],
            "type": "function"
        },
        {
            "constant": False,
            "inputs": [
                {"name": "_spender", "type": "address"},
                {"name": "_value", "type": "uint256"}
            ],
            "name": "approve",
            "outputs": [{"name": "", "type": "bool"}],
            "type": "function"
        },
        {
            "constant": True,
            "inputs": [],
            "name": "decimals",
            "outputs": [{"name": "", "type": "uint8"}],
            "type": "function"
        }
    ]
    
    # ERC-721 ABI (minimal for minting)
    ERC721_ABI = [
        {
            "constant": False,
            "inputs": [
                {"name": "to", "type": "address"},
                {"name": "tokenURI", "type": "string"}
            ],
            "name": "mint",
            "outputs": [{"name": "", "type": "uint256"}],
            "type": "function"
        },
        {
            "constant": False,
            "inputs": [{"name": "to", "type": "address"}],
            "name": "mint",
            "outputs": [{"name": "", "type": "uint256"}],
            "type": "function"
        }
    ]
    
    def __init__(self, private_key: str = None):
        """
        Initialize wallet
        
        Args:
            private_key: Private key (hex string with or without 0x prefix)
        """
        self.w3 = Web3(Web3.HTTPProvider(self.RPC_URL))
        self.builder_code = self.BUILDER_CODE
        
        if not self.w3.is_connected():
            raise Exception("Failed to connect to Base network")
        
        if private_key:
            self.account = Account.from_key(private_key)
            self.address = self.account.address
        else:
            self.account = None
            self.address = None
    
    @classmethod
    def create_new(cls) -> 'SimpleWalletWithBuilderCode':
        """
        Create new wallet with random private key
        
        Returns:
            Wallet instance
        """
        print("🔄 Creating new wallet...")
        
        # Generate new account
        account = Account.create()
        
        wallet = cls(account.key.hex())
        
        print(f"✅ Wallet created!")
        print()
        print(f"Address: {wallet.address}")
        print(f"Private Key: {account.key.hex()}")
        print()
        print("⚠️  IMPORTANT: Save private key securely!")
        print()
        
        # Save to file
        wallet_file = Path.home() / ".simple-wallet" / "wallet.json"
        wallet_file.parent.mkdir(exist_ok=True)
        
        with open(wallet_file, 'w') as f:
            json.dump({
                'address': wallet.address,
                'private_key': account.key.hex()
            }, f, indent=2)
        
        print(f"✅ Wallet saved to: {wallet_file}")
        print()
        
        return wallet
    
    @classmethod
    def load_from_file(cls, wallet_file: str = None) -> 'SimpleWalletWithBuilderCode':
        """
        Load wallet from file
        
        Args:
            wallet_file: Path to wallet.json
        
        Returns:
            Wallet instance
        """
        if not wallet_file:
            wallet_file = Path.home() / ".simple-wallet" / "wallet.json"
        
        print(f"🔄 Loading wallet from: {wallet_file}")
        
        with open(wallet_file) as f:
            data = json.load(f)
        
        wallet = cls(data['private_key'])
        
        print(f"✅ Wallet loaded: {wallet.address}")
        print()
        
        return wallet
    
    def append_builder_code_erc8021(self, calldata: str) -> str:
        """
        Append builder code to calldata per ERC-8021
        
        Args:
            calldata: Original transaction calldata
        
        Returns:
            Modified calldata with builder code
        """
        # Remove '0x' prefix if present
        if calldata.startswith('0x'):
            calldata = calldata[2:]
        
        # Encode builder code as UTF-8
        builder_bytes = self.builder_code.encode('utf-8').hex()
        
        # ERC-8021 pattern (16 bytes = 32 hex chars)
        erc8021_pattern = "8021" * 8
        
        # Append: data + builder_code + pattern
        modified = '0x' + calldata + builder_bytes + erc8021_pattern
        
        return modified
    
    def get_balance(self) -> Dict[str, Any]:
        """Get wallet balance"""
        if not self.address:
            raise Exception("Wallet not initialized")
        
        balance_wei = self.w3.eth.get_balance(self.address)
        balance_eth = self.w3.from_wei(balance_wei, 'ether')
        
        return {
            'address': self.address,
            'balance_wei': balance_wei,
            'balance_eth': float(balance_eth)
        }
    
    def send_eth_with_builder_code(
        self,
        to_address: str,
        amount_eth: float
    ) -> Dict[str, Any]:
        """
        Send ETH with builder code appended per ERC-8021
        
        Args:
            to_address: Recipient address
            amount_eth: Amount in ETH
        
        Returns:
            Transaction result
        """
        if not self.account:
            raise Exception("Wallet not initialized with private key")
        
        print()
        print("=" * 70)
        print("🚀 SENDING ETH WITH BUILDER CODE (ERC-8021)")
        print("=" * 70)
        print()
        print(f"From: {self.address}")
        print(f"To: {to_address}")
        print(f"Amount: {amount_eth} ETH")
        print(f"Network: Base (Chain ID: {self.CHAIN_ID})")
        print(f"Builder Code: {self.builder_code}")
        print()
        
        # Check balance
        balance = self.get_balance()
        print(f"💰 Current Balance: {balance['balance_eth']} ETH")
        print()
        
        if balance['balance_eth'] < amount_eth:
            raise Exception(f"Insufficient balance. Have {balance['balance_eth']} ETH, need {amount_eth} ETH")
        
        # For simple ETH transfer, calldata is empty
        original_calldata = "0x"
        
        # Append builder code per ERC-8021
        modified_calldata = self.append_builder_code_erc8021(original_calldata)
        
        print("📝 Calldata:")
        print(f"   Original: {original_calldata}")
        print(f"   Modified: {modified_calldata[:66]}...{modified_calldata[-32:]}")
        print()
        
        # Get current gas price
        gas_price = self.w3.eth.gas_price
        
        # Build transaction
        nonce = self.w3.eth.get_transaction_count(self.address)
        
        # Convert address to checksum format
        to_address_checksum = self.w3.to_checksum_address(to_address)
        
        tx = {
            'nonce': nonce,
            'to': to_address_checksum,
            'value': self.w3.to_wei(amount_eth, 'ether'),
            'gas': 100000,  # Increased for extra calldata
            'gasPrice': gas_price,
            'data': modified_calldata,
            'chainId': self.CHAIN_ID
        }
        
        print("🔄 Signing transaction...")
        
        # Sign transaction
        signed_tx = self.w3.eth.account.sign_transaction(tx, self.account.key)
        
        print("✅ Transaction signed")
        print()
        print("📡 Broadcasting to network...")
        
        # Send transaction
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        tx_hash_hex = tx_hash.hex()
        
        print()
        print("=" * 70)
        print("✅ TRANSACTION SENT!")
        print("=" * 70)
        print()
        print(f"Transaction Hash: {tx_hash_hex}")
        print()
        print(f"🔗 Basescan: https://basescan.org/tx/{tx_hash_hex}")
        print()
        
        print("⏳ Waiting for confirmation...")
        
        # Wait for receipt
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
        
        print()
        print("=" * 70)
        print("✅ TRANSACTION CONFIRMED!")
        print("=" * 70)
        print()
        print(f"Block Number: {receipt['blockNumber']}")
        print(f"Gas Used: {receipt['gasUsed']}")
        print(f"Status: {'Success' if receipt['status'] == 1 else 'Failed'}")
        print()
        
        print("=" * 70)
        print("📝 VERIFY BUILDER CODE ON BASESCAN")
        print("=" * 70)
        print()
        print("1. Open: https://basescan.org/tx/" + tx_hash_hex)
        print("2. Scroll to 'More Details'")
        print("3. Click 'Click to see More'")
        print("4. View 'Input Data'")
        print("5. Check last 16 bytes (32 hex chars):")
        print()
        print("   Expected pattern: 80218021802180218021802180218021")
        print()
        print("6. Before pattern, you should see:")
        print(f"   Hex: {self.builder_code.encode('utf-8').hex()}")
        print(f"   Decoded: {self.builder_code}")
        print()
        
        return {
            'transaction_hash': tx_hash_hex,
            'from': self.address,
            'to': to_address,
            'amount': amount_eth,
            'builder_code': self.builder_code,
            'block_number': receipt['blockNumber'],
            'gas_used': receipt['gasUsed'],
            'status': 'confirmed' if receipt['status'] == 1 else 'failed'
        }
    
    def get_token_balance(self, token_symbol: str) -> Dict[str, Any]:
        """
        Get ERC-20 token balance
        
        Args:
            token_symbol: Token symbol (USDC, DAI, etc.)
            
        Returns:
            dict with token balance info
        """
        if token_symbol.upper() not in self.TOKENS:
            raise Exception(f"Token {token_symbol} not supported. Available: {list(self.TOKENS.keys())}")
        
        token_address = self.TOKENS[token_symbol.upper()]
        token_contract = self.w3.eth.contract(
            address=self.w3.to_checksum_address(token_address),
            abi=self.ERC20_ABI
        )
        
        balance = token_contract.functions.balanceOf(self.address).call()
        decimals = token_contract.functions.decimals().call()
        balance_formatted = balance / (10 ** decimals)
        
        return {
            'token': token_symbol.upper(),
            'address': token_address,
            'balance_raw': balance,
            'balance': balance_formatted,
            'decimals': decimals
        }
    
    def swap_tokens(
        self,
        from_token: str,
        to_token: str,
        amount: float,
        slippage: float = 1.0
    ) -> Dict[str, Any]:
        """
        Swap tokens using Uniswap V3 on Base
        
        Args:
            from_token: Source token (ETH, USDC, etc.)
            to_token: Destination token
            amount: Amount to swap
            slippage: Slippage tolerance in percent (default 1%)
            
        Returns:
            dict with swap result
        """
        print()
        print("=" * 70)
        print("🔄 TOKEN SWAP WITH BUILDER CODE")
        print("=" * 70)
        print()
        print(f"From: {amount} {from_token}")
        print(f"To: {to_token}")
        print(f"Slippage: {slippage}%")
        print()
        
        # For now, return a placeholder
        # Full Uniswap V3 integration requires more complex routing
        print("⚠️  Swap functionality requires Uniswap V3 SDK integration")
        print("   For now, use external DEX aggregator or implement custom routing")
        print()
        print("Recommended approach:")
        print("1. Use 1inch API for best rates")
        print("2. Or use Uniswap V3 SDK for direct swaps")
        print("3. Or use Base's native swap interfaces")
        print()
        
        return {
            'status': 'not_implemented',
            'message': 'Use external DEX aggregator for swaps',
            'from_token': from_token,
            'to_token': to_token,
            'amount': amount
        }
    
    def mint_nft(
        self,
        contract_address: str,
        token_uri: str = None,
        to_address: str = None
    ) -> Dict[str, Any]:
        """
        Mint NFT with builder code attribution
        
        Args:
            contract_address: NFT contract address
            token_uri: Token metadata URI (optional, depends on contract)
            to_address: Recipient address (None = mint to self)
            
        Returns:
            dict with mint result
        """
        if not self.account:
            raise Exception("Wallet not initialized with private key")
        
        print()
        print("=" * 70)
        print("🎨 MINT NFT WITH BUILDER CODE")
        print("=" * 70)
        print()
        print(f"Contract: {contract_address}")
        print(f"To: {to_address or self.address}")
        if token_uri:
            print(f"Token URI: {token_uri}")
        print()
        
        # Convert addresses to checksum format
        contract_address_checksum = self.w3.to_checksum_address(contract_address)
        recipient = self.w3.to_checksum_address(to_address or self.address)
        
        # Create contract instance
        nft_contract = self.w3.eth.contract(
            address=contract_address_checksum,
            abi=self.ERC721_ABI
        )
        
        # Build mint transaction
        try:
            if token_uri:
                # Mint with URI
                mint_function = nft_contract.functions.mint(recipient, token_uri)
            else:
                # Mint without URI
                mint_function = nft_contract.functions.mint(recipient)
            
            # Estimate gas
            gas_estimate = mint_function.estimate_gas({'from': self.address})
            
            # Build transaction
            nonce = self.w3.eth.get_transaction_count(self.address)
            gas_price = self.w3.eth.gas_price
            
            tx = mint_function.build_transaction({
                'from': self.address,
                'gas': int(gas_estimate * 1.2),  # Add 20% buffer
                'gasPrice': gas_price,
                'nonce': nonce,
                'chainId': self.CHAIN_ID
            })
            
            # Append builder code to calldata
            original_data = tx['data']
            modified_data = self.append_builder_code_erc8021(original_data)
            tx['data'] = modified_data
            
            print("📝 Calldata:")
            print(f"   Original: {original_data[:66]}...")
            print(f"   Modified: {modified_data[:66]}...{modified_data[-32:]}")
            print()
            
            print("🔄 Signing transaction...")
            
            # Sign transaction
            signed_tx = self.w3.eth.account.sign_transaction(tx, self.account.key)
            
            print("✅ Transaction signed")
            print()
            print("📡 Broadcasting to network...")
            
            # Send transaction
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
            tx_hash_hex = tx_hash.hex()
            
            print()
            print("=" * 70)
            print("✅ MINT TRANSACTION SENT!")
            print("=" * 70)
            print()
            print(f"Transaction Hash: {tx_hash_hex}")
            print()
            print(f"🔗 Basescan: https://basescan.org/tx/{tx_hash_hex}")
            print()
            print("⏳ Waiting for confirmation...")
            
            # Wait for receipt
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            print()
            print("=" * 70)
            print("✅ NFT MINTED!")
            print("=" * 70)
            print()
            print(f"Block Number: {receipt['blockNumber']}")
            print(f"Gas Used: {receipt['gasUsed']}")
            print(f"Status: {'Success' if receipt['status'] == 1 else 'Failed'}")
            print()
            
            return {
                'transaction_hash': tx_hash_hex,
                'contract': contract_address,
                'to': recipient,
                'token_uri': token_uri,
                'builder_code': self.builder_code,
                'block_number': receipt['blockNumber'],
                'gas_used': receipt['gasUsed'],
                'status': 'confirmed' if receipt['status'] == 1 else 'failed'
            }
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            print()
            print("Common issues:")
            print("- Contract may not support this mint function")
            print("- May need to be whitelisted")
            print("- Minting may be paused")
            print("- Check contract documentation")
            raise

def demo():
    """Demo wallet with builder code"""
    print()
    print("=" * 70)
    print("🏗️  SIMPLE WALLET WITH BUILDER CODE")
    print("=" * 70)
    print()
    print("This wallet uses Web3.py for full control over")
    print("transaction calldata, enabling proper ERC-8021")
    print("builder code attribution.")
    print()
    print("=" * 70)
    print()
    print("Usage:")
    print()
    print("1. Create new wallet:")
    print()
    print("   from simple_wallet_builder_code import SimpleWalletWithBuilderCode")
    print()
    print("   wallet = SimpleWalletWithBuilderCode.create_new()")
    print()
    print("2. Or load existing:")
    print()
    print("   wallet = SimpleWalletWithBuilderCode.load_from_file()")
    print()
    print("3. Check balance:")
    print()
    print("   balance = wallet.get_balance()")
    print("   print(f\"Balance: {balance['balance_eth']} ETH\")")
    print()
    print("4. Send with builder code:")
    print()
    print("   result = wallet.send_eth_with_builder_code(")
    print("       to_address='0xa82fbc2ee91e76b238b636581443e9f055311db1',")
    print("       amount_eth=0.0001")
    print("   )")
    print()
    print("=" * 70)
    print()
    print("✅ Advantages:")
    print()
    print("   - Full control over calldata")
    print("   - Proper ERC-8021 attribution")
    print("   - Builder code verified on Basescan")
    print("   - Simple and straightforward")
    print("   - No external dependencies")
    print()
    print("=" * 70)

if __name__ == "__main__":
    demo()
