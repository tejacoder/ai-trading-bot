# 🤖 AI Trading Bot on Base

Complete autonomous trading bot on Base blockchain with AES-256 encrypted wallet, dynamic builder codes, and multiple trading strategies.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Base](https://img.shields.io/badge/Base-Mainnet-blue)](https://base.org)

## 🎯 Features

### Security
- ✅ **AES-256 Encrypted Wallet** - No plaintext private keys
- ✅ **Password Protected** - All operations require password
- ✅ **Hidden Storage** - `~/.agent-wallet/.wallet_data` (0600 permissions)
- ✅ **Dynamic Builder Codes** - Unique per agent, auto-generated

### Trading
- ✅ **4 Strategies** - DCA, Momentum (RSI), Grid, Arbitrage
- ✅ **Risk Management** - Position sizing, stop-loss, take-profit
- ✅ **Backtesting** - Test on historical data
- ✅ **Dry-Run Mode** - Safe testing without real trades

### Architecture
- ✅ **Auto-Detect Wallets** - Encrypted or plaintext
- ✅ **Multi-Agent Ready** - Each agent = unique wallet + builder code
- ✅ **Complete Wallet Ops** - Send, swap, mint NFT, deploy contracts
- ✅ **Interactive CLI** - Easy wallet management

## 🚀 Quick Start

### 1. Clone & Setup

```bash
git clone https://github.com/tejacoder/ai-trading-bot.git
cd ai-trading-bot

# Auto setup (creates encrypted wallet + builder code)
python3 setup_auto.py
```

### 2. Fund Wallet

```bash
# Send ETH + USDC to your wallet address
# Minimum: 0.001 ETH + $100 USDC
```

### 3. Backtest

```bash
# Test strategy on last 7 days
WALLET_PASSWORD=your-password python3 trading_bot.py backtest 7
```

### 4. Run Live

```bash
# Dry-run mode (safe)
WALLET_PASSWORD=your-password python3 trading_bot.py 300

# Real trading (edit config.py: dry_run=False)
WALLET_PASSWORD=your-password python3 trading_bot.py 3600
```

## 📁 Project Structure

```
ai-trading-bot/
├── trading_bot.py              # Main bot engine
├── wallet_encrypted.py         # AES-256 encrypted wallet
├── wallet_adapter.py           # Auto-detect adapter
├── wallet_operations.py        # Full wallet operations
├── price_oracle.py             # Price feeds
├── risk_manager.py             # Risk management
├── config.py                   # Dynamic configuration
├── setup_auto.py               # Zero-input setup
├── export_bc.py                # Export builder code
├── wallet_cli.py               # Interactive CLI
└── strategies/
    └── trading_strategies.py   # Trading strategies
```

## 🔐 Security

### Encrypted Wallet

**Encryption:**
- Algorithm: AES-256 (Fernet)
- Key Derivation: PBKDF2HMAC (SHA-256, 100k iterations)
- Storage: `~/.agent-wallet/.wallet_data` (hidden, 0600)

**Access:**
- Read balance: No password
- Send/swap/mint: Password required
- Export builder code: Password required

### Dynamic Builder Code

**No hardcoded values!**

```python
# Auto-loaded from ~/.agent-wallet/.config.json
BUILDER_CODE = get_builder_code()  # Unique per agent
```

## 💼 Wallet Operations

### Send ETH

```python
from wallet_adapter import TradingBotWallet

wallet = TradingBotWallet(password="your-password")
wallet.load()

tx = wallet.send_eth_with_builder_code(
    to_address="0x742d...",
    amount_eth=0.001
)
# ✅ Builder code included!
```

### Swap Tokens

```python
# Swap ETH → USDC on Uniswap V3
tx = wallet.swap_tokens("ETH", "USDC", 0.01)
# ✅ Builder code included!
```

### Interactive CLI

```bash
python3 wallet_cli.py

# 💼 Wallet Operations
# 1. Check balance
# 2. Send ETH
# 3. Swap tokens
# 4. Mint NFT
# ...
```

## 📈 Trading Strategies

### 1. DCA (Dollar Cost Averaging)

Buy fixed amount at regular intervals

```python
"dca": {
    "enabled": True,
    "interval": 3600,      # 1 hour
    "amount_usdc": 10      # $10 per buy
}
```

### 2. Momentum (RSI)

Buy oversold, sell overbought

```python
"momentum": {
    "enabled": True,
    "rsi_period": 14,
    "rsi_oversold": 30,
    "rsi_overbought": 70
}
```

### 3. Grid Trading

Profit from volatility in range

```python
"grid": {
    "enabled": False,
    "grid_levels": 10,
    "price_range": 0.20    # 20%
}
```

### 4. Arbitrage

Profit from price differences

```python
"arbitrage": {
    "enabled": False,
    "min_profit": 0.005    # 0.5%
}
```

## 🛡️ Risk Management

```python
RISK_CONFIG = {
    "max_position_size": 0.1,  # Max 10% per trade
    "stop_loss": 0.05,         # 5% stop loss
    "take_profit": 0.10,       # 10% take profit
    "max_slippage": 0.01,      # Max 1% slippage
    "max_daily_trades": 20     # Max 20 trades/day
}
```

## 🧪 Backtesting

```bash
# Backtest last 7 days
WALLET_PASSWORD=your-password python3 trading_bot.py backtest 7

# Results:
# Initial capital: $1000.00
# Final value: $1034.50
# Profit: $+34.50 (+3.45%)
# Total trades: 12
# Win rate: 58.3%
```

## 🎯 Multi-Agent Deployment

### Agent 1

```bash
mkdir ~/agent1 && cd ~/agent1
git clone https://github.com/tejacoder/ai-trading-bot.git .
python3 setup_auto.py
# ✅ Wallet: 0xC953...
# ✅ Builder: bc_ynnc3nw0
```

### Agent 2

```bash
mkdir ~/agent2 && cd ~/agent2
git clone https://github.com/tejacoder/ai-trading-bot.git .
python3 setup_auto.py
# ✅ Wallet: 0x3ED2...
# ✅ Builder: bc_30rah79h
```

**Each agent:**
- ✅ Unique encrypted wallet
- ✅ Unique builder code
- ✅ Independent config
- ✅ No conflicts

## 🔧 Configuration

### Environment Variables

```bash
# .env file
WALLET_PASSWORD=your-secure-password

# Usage
WALLET_PASSWORD=demo123 python3 trading_bot.py
```

### config.py

```python
# Wallet (auto-loaded)
WALLET_PATH = "~/.agent-wallet/.wallet_data"
BUILDER_CODE = get_builder_code()  # Dynamic!

# Strategies
STRATEGIES = {
    "dca": {"enabled": True},
    "momentum": {"enabled": True}
}

# Safety
SAFETY = {
    "dry_run": True,  # Set False for real trading
}
```

## 📊 Builder Code Attribution

All transactions include ERC-8021 builder code:

```bash
# Verify on Basescan
https://basescan.org/tx/0x47e0...

# Input Data shows:
# ...62635f74306d7a30366d34  ← "bc_t0mz06m4" in hex
# 80218021802180218021...     ← ERC-8021 pattern
```

## 📚 Documentation

- **[ENCRYPTED_WALLET.md](ENCRYPTED_WALLET.md)** - Encryption guide
- **[DYNAMIC_CONFIG.md](DYNAMIC_CONFIG.md)** - Configuration docs
- **[MIGRATION.md](MIGRATION.md)** - Migration guide
- **[RINGKASAN.md](RINGKASAN.md)** - Indonesian docs

## ❓ Troubleshooting

### Wrong Password

```
❌ Error: Invalid password
```

**Solution:** Check password, try backup

### Wallet Not Found

```
❌ Error: Wallet file not found
```

**Solution:** Run `setup_auto.py`

### Builder Code is None

```python
import config
print(config.BUILDER_CODE)  # None
```

**Solution:** Run `setup_auto.py`

## 🔒 Security Best Practices

### 1. Strong Password

```
✅ Good: MyTr4d1ng!B0t#2024$Secure
❌ Bad: password123
```

### 2. Backup

```bash
# Backup encrypted wallet (still safe!)
cp ~/.agent-wallet/.wallet_data ~/backup/

# Store password in password manager
```

### 3. Never Commit

```bash
# .gitignore includes:
.wallet_data
.config.json
.agent-wallet/
.env
```

## 📊 Project Stats

```
Files: 26 files
Code: 2,566 lines (Python)
Docs: 4,162 lines (Markdown)
Total: 6,728 lines
```

## 🎉 Summary

**Complete autonomous trading bot with:**

✅ AES-256 encrypted wallet  
✅ Dynamic builder codes  
✅ 4 trading strategies  
✅ Risk management  
✅ Backtesting  
✅ Multi-agent ready  
✅ Production ready  

**Security Level:** 🔐🔐🔐🔐🔐 (5/5)

## 🔗 Resources

- **Base Docs:** https://docs.base.org/ai-agents
- **Builder Codes:** https://docs.base.org/builder-codes
- **Basescan:** https://basescan.org

## 📝 License

MIT License

## 🤝 Contributing

Contributions welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) first.

## 📧 Contact

- GitHub: [@tejacoder](https://github.com/tejacoder)
- Email: teja.jakarulloh@gmail.com

---

**Built with ❤️ on Base**
