# 💼 Wallet Operations - Complete Guide

## 🎯 Features Added

Trading bot sekarang punya **complete wallet operations**!

### ✅ What's New:

**Balance & Info:**
- ✅ Check ETH balance
- ✅ Check token balance (USDC, DAI, WETH)
- ✅ Show wallet info

**Send & Transfer:**
- ✅ Send ETH (with builder code!)
- ✅ Send tokens

**Swap:**
- ✅ Swap ETH ↔ USDC
- ✅ Swap ETH ↔ DAI
- ✅ Swap any token pair

**NFT:**
- ✅ Mint NFT
- ✅ Deploy NFT contract

**Advanced:**
- ✅ Transaction history
- ✅ Export wallet info

---

## 🚀 Quick Start

### Wallet CLI Tool

```bash
# Run wallet CLI
python3 wallet_cli.py
```

**Menu:**
```
💼 Wallet Operations
============================================================

📊 Balance & Info:
  1. Check ETH balance
  2. Check token balance (USDC/DAI/WETH)
  3. Show wallet info

💸 Send & Transfer:
  4. Send ETH
  5. Send tokens

🔄 Swap:
  6. Swap tokens (ETH ↔ USDC)

🎨 NFT:
  7. Mint NFT
  8. Deploy NFT contract

🔧 Advanced:
  9. View transaction history
  10. Export wallet info

  0. Exit
```

---

## 📊 Usage Examples

### 1. Check Balance

```bash
python3 wallet_cli.py
# Select: 1

# Output:
✅ Balance:
   ETH: 0.001234
   USD: $2.86
   Address: 0xC95374c67c08922eC4FE51a00bc0544A202675D4
```

### 2. Send ETH

```bash
python3 wallet_cli.py
# Select: 4
# To address: 0x742d35Cc6634C0532925a3b844Bc9e7595f0c4f2
# Amount: 0.001

# Output:
✅ Transaction sent!
   TX: 0x47e0239d080474ac856a21d48900b9d34282ecefb99fb90269632a4bc9a38c2a
   Basescan: https://basescan.org/tx/0x47e0...
   Builder code: bc_t0mz06m4 ✅
```

### 3. Swap Tokens

```bash
python3 wallet_cli.py
# Select: 6
# Select swap: 1 (ETH → USDC)
# Amount: 0.01

# Output:
✅ Swap successful!
   TX: 0xb4f2...91ca
   Basescan: https://basescan.org/tx/0xb4f2...
   Builder code: bc_t0mz06m4 ✅
```

### 4. Mint NFT

```bash
python3 wallet_cli.py
# Select: 7
# NFT contract: 0xFf8B57369Aee9982368395c6103Fc2F9b79FE2F7
# Token URI: ipfs://QmXxx...

# Output:
✅ NFT minted!
   TX: 0x5ce91...
   Builder code: bc_t0mz06m4 ✅
   View on OpenSea: https://opensea.io/assets/base/0xFf8B...
```

---

## 🔧 Programmatic Usage

### In Python Scripts

```python
from wallet_operations import SimpleWalletWithBuilderCode

# Load wallet
wallet = SimpleWalletWithBuilderCode.load_from_file()

# Check balance
balance = wallet.get_balance()
print(f"ETH: {balance['eth']}")

# Send ETH
tx_hash = wallet.send_eth_with_builder_code(
    to_address="0x742d35Cc6634C0532925a3b844Bc9e7595f0c4f2",
    amount_eth=0.001
)
print(f"TX: {tx_hash}")

# Swap tokens
tx_hash = wallet.swap_tokens(
    from_token="ETH",
    to_token="USDC",
    amount=0.01
)
print(f"Swap TX: {tx_hash}")

# Mint NFT
tx_hash = wallet.mint_nft(
    contract_address="0xFf8B57369Aee9982368395c6103Fc2F9b79FE2F7",
    token_uri="ipfs://QmXxx..."
)
print(f"Mint TX: {tx_hash}")
```

---

## 🎯 Integration with Trading Bot

Trading bot sekarang bisa:

### 1. Execute Trades (Already Integrated)

```python
# Bot automatically uses wallet operations
tx_hash = self.wallet.swap_tokens(
    from_token="USDC",
    to_token="WETH",
    amount=10
)
# ✅ Builder code included!
```

### 2. Send Profits

```python
# Send profits to another wallet
if profit > threshold:
    wallet.send_eth_with_builder_code(
        to_address=profit_wallet,
        amount_eth=profit_amount
    )
```

### 3. Mint NFT on Milestone

```python
# Mint NFT when reaching milestone
if total_profit > 1000:
    wallet.mint_nft(
        contract_address=nft_contract,
        token_uri=f"ipfs://milestone_{total_profit}"
    )
```

---

## 📁 Files Added

```
trading-bot/
├── wallet_operations.py    - Complete wallet implementation
├── wallet_cli.py           - Interactive CLI tool
└── trading_bot.py          - Updated to use wallet_operations
```

---

## 🔐 Builder Code Attribution

**Semua transaksi include builder code!**

### Transactions with Builder Code:
- ✅ Send ETH
- ✅ Swap tokens
- ✅ Mint NFT
- ✅ Deploy contracts
- ✅ All wallet operations

### Verification:
```bash
# Check on Basescan
https://basescan.org/tx/0x...

# Look for in Input Data:
62635f74306d7a30366d34  ← Builder code (hex)
80218021802180218021...  ← ERC-8021 pattern
```

---

## 🎨 NFT Operations

### Mint NFT

```python
# Mint on existing contract
tx_hash = wallet.mint_nft(
    contract_address="0xFf8B57369Aee9982368395c6103Fc2F9b79FE2F7",
    token_uri="ipfs://QmXxx..."
)
```

### Deploy NFT Contract

```bash
# Use deploy script
python3 deploy_nft_now.py

# Or use contracts in contracts/ directory
```

---

## 💡 Use Cases

### 1. Manual Wallet Management

```bash
# Check balance before trading
python3 wallet_cli.py
# Select: 1 (Check balance)

# Send ETH to exchange
python3 wallet_cli.py
# Select: 4 (Send ETH)
```

### 2. Profit Distribution

```python
# In trading bot
if daily_profit > 100:
    # Send 50% to savings wallet
    wallet.send_eth_with_builder_code(
        to_address=savings_wallet,
        amount_eth=daily_profit * 0.5 / eth_price
    )
```

### 3. NFT Rewards

```python
# Mint NFT for top performers
if win_rate > 0.70:
    wallet.mint_nft(
        contract_address=reward_nft,
        token_uri=f"ipfs://top_trader_{timestamp}"
    )
```

### 4. Token Rebalancing

```python
# Rebalance portfolio
if usdc_percent > 0.80:
    # Swap some USDC to ETH
    wallet.swap_tokens("USDC", "ETH", amount=100)
```

---

## 🔧 Advanced Features

### 1. Batch Operations

```python
# Send to multiple addresses
addresses = ["0x...", "0x...", "0x..."]
for addr in addresses:
    wallet.send_eth_with_builder_code(addr, 0.001)
```

### 2. Conditional Swaps

```python
# Swap based on price
if eth_price < 2000:
    wallet.swap_tokens("USDC", "ETH", 100)
elif eth_price > 3000:
    wallet.swap_tokens("ETH", "USDC", 0.1)
```

### 3. NFT Collection

```python
# Mint multiple NFTs
for i in range(10):
    wallet.mint_nft(
        contract_address=collection,
        token_uri=f"ipfs://token_{i}"
    )
```

---

## 📊 Wallet CLI Features

### Balance Checking
- ✅ Real-time ETH balance
- ✅ Token balances (USDC, DAI, WETH)
- ✅ USD value calculation
- ✅ Total portfolio value

### Transactions
- ✅ Send ETH with builder code
- ✅ Swap any token pair
- ✅ Confirmation prompts
- ✅ Transaction receipts

### NFT Operations
- ✅ Mint on existing contracts
- ✅ Deploy new contracts
- ✅ OpenSea integration
- ✅ Metadata support

### Info & Export
- ✅ Wallet information
- ✅ Transaction history links
- ✅ Export to JSON
- ✅ Basescan links

---

## 🎯 Quick Commands

```bash
# Check balance
python3 wallet_cli.py
# Select: 1

# Send ETH
python3 wallet_cli.py
# Select: 4

# Swap tokens
python3 wallet_cli.py
# Select: 6

# Mint NFT
python3 wallet_cli.py
# Select: 7

# Export info
python3 wallet_cli.py
# Select: 10
```

---

## ✅ Summary

### Features Added:
- ✅ Complete wallet operations
- ✅ Interactive CLI tool
- ✅ Builder code attribution
- ✅ NFT support
- ✅ Swap integration
- ✅ Balance checking
- ✅ Transaction management

### Files:
- ✅ `wallet_operations.py` - Full implementation
- ✅ `wallet_cli.py` - CLI tool
- ✅ `trading_bot.py` - Updated integration

### All Transactions Include:
- ✅ Builder code (bc_t0mz06m4)
- ✅ ERC-8021 pattern
- ✅ Verifiable onchain

---

**Wallet operations lengkap sudah terintegrasi! 💼✅**

**Try it:** `python3 wallet_cli.py`
