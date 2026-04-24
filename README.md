# 🤖 AI Trading Bot

> Autonomous trading bot with multiple strategies, risk management, and builder code attribution

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Base](https://img.shields.io/badge/Base-Mainnet-blue.svg)](https://base.org/)
[![License](https://img.shields.io/badge/License-Private-red.svg)]()

---

## ⚠️ PRIVATE REPOSITORY

This is a **private repository**. Do not share or distribute without permission.

---

## 🚀 Features

### Trading Strategies
- ✅ **DCA (Dollar Cost Averaging)** - Regular buying at intervals
- ✅ **Momentum Trading** - RSI-based signals
- ✅ **Grid Trading** - Range-bound trading
- ✅ **Arbitrage** - Cross-DEX opportunities (coming soon)

### Wallet Operations (NEW!)
- ✅ **Send ETH** - Transfer with builder code attribution
- ✅ **Swap Tokens** - ETH ↔ USDC/DAI on Uniswap V3
- ✅ **Mint NFT** - Mint on existing contracts
- ✅ **Deploy NFT** - Deploy new NFT contracts
- ✅ **Check Balance** - ETH and token balances
- ✅ **Interactive CLI** - Easy wallet management

### Risk Management
- ✅ Position sizing (max 10% per trade)
- ✅ Stop-loss (5% default)
- ✅ Take-profit (10% default)
- ✅ Daily trade limits
- ✅ Slippage protection

### Analytics
- ✅ Real-time price feeds (CoinGecko + Uniswap V3)
- ✅ Technical indicators (RSI, SMA, momentum)
- ✅ Portfolio tracking
- ✅ Backtesting on historical data
- ✅ Trade history logging

### Safety
- ✅ Dry run mode (test without real trades)
- ✅ Manual confirmation required
- ✅ Emergency stop mechanism
- ✅ Builder code attribution (ERC-8021)

---

## 📦 Installation

### 1. Clone Repository
```bash
git clone <your-repo-url>
cd trading-bot
```

### 2. Install Dependencies
```bash
pip3 install web3 requests
```

### 3. Setup Wallet
```bash
# Copy your wallet file
cp ~/.simple-wallet/wallet.json ./wallet.json

# Or create new wallet
python3 -c "from web3 import Web3; w = Web3().eth.account.create(); print(f'Address: {w.address}'); print(f'Private key: {w.key.hex()}')"
```

### 4. Configure
```bash
# Edit config.py
nano config.py

# Set your builder code
BUILDER_CODE = "bc_YOUR_CODE"

# Set safety mode
SAFETY = {
    "dry_run": True,  # Start with dry run!
    "require_confirmation": True
}
```

---

## 🚀 Quick Start

### Wallet Operations (NEW!)
```bash
# Interactive wallet management
python3 wallet_cli.py

# Features:
# - Check balance
# - Send ETH
# - Swap tokens
# - Mint NFT
# - Deploy contracts
```

### Backtest First
```bash
# Test strategy on historical data
python3 trading_bot.py backtest 30
```

### Dry Run
```bash
# Test live without real trades
python3 trading_bot.py 300
```

### Go Live
```bash
# Edit config.py: dry_run = False
# Then start bot
python3 trading_bot.py 300
```

---

## 📊 Configuration

### Strategies
```python
STRATEGIES = {
    "dca": {
        "enabled": True,
        "interval": 3600,      # 1 hour
        "amount_usdc": 10      # $10 per buy
    },
    "momentum": {
        "enabled": True,
        "rsi_oversold": 30,
        "rsi_overbought": 70
    }
}
```

### Risk Management
```python
RISK_CONFIG = {
    "max_position_size": 0.1,   # 10% max
    "stop_loss": 0.05,          # 5%
    "take_profit": 0.10,        # 10%
    "max_daily_trades": 20
}
```

---

## 📁 Project Structure

```
trading-bot/
├── README.md              - This file
├── RINGKASAN.md          - Indonesian summary
├── QUICKSTART.md         - Quick reference
├── BUILDER_CODE.md       - Builder code docs
├── config.py             - Configuration
├── trading_bot.py        - Main bot engine
├── price_oracle.py       - Price feeds
├── risk_manager.py       - Risk management
├── examples.py           - Usage examples
└── strategies/
    └── trading_strategies.py - Trading strategies
```

---

## 🔐 Security

### Protected Files (in .gitignore)
- ✅ `wallet.json` - Private keys
- ✅ `credentials.json` - API keys
- ✅ `*.log` - Trade logs
- ✅ `data/` - Historical data

### What's Safe to Share
- ✅ Code files (`.py`)
- ✅ Documentation (`.md`)
- ✅ Configuration template

### Never Share
- ❌ Private keys
- ❌ Wallet files
- ❌ API credentials
- ❌ Trade history with real data

---

## 📚 Documentation

- **RINGKASAN.md** - Dokumentasi lengkap (Indonesian)
- **QUICKSTART.md** - Quick reference guide
- **BUILDER_CODE.md** - Builder code attribution
- **examples.py** - Usage examples and scenarios

---

## ⚠️ Disclaimer

**This bot is for educational purposes only.**

- ❌ NOT financial advice
- ❌ NO guarantee of profits
- ❌ Trading involves substantial risk
- ❌ You can lose all your capital

**Only trade with funds you can afford to lose.**

---

## 🎯 Performance

### Backtest Results (Example)
```
Period: 30 days
Initial: $1,000
Final: $1,124
Profit: +$124 (+12.4%)
Win Rate: 58.3%
Strategy vs B&H: +5.2%
```

*Past performance does not guarantee future results.*

---

## 🔧 Troubleshooting

### Bot not generating signals
- Check strategies enabled in `config.py`
- Verify market data is being fetched
- Review RSI thresholds

### Trades being blocked
- Check daily trade limit
- Verify position size limits
- Review risk management settings

### Price data errors
- Check internet connection
- Verify CoinGecko API access
- Try onchain fallback

---

## 📞 Support

For issues or questions:
1. Check documentation files
2. Review configuration
3. Test individual components
4. Check logs for errors

---

## 📄 License

**Private - All Rights Reserved**

This code is private and proprietary. Unauthorized copying, distribution, or use is strictly prohibited.

---

## 🏗️ Builder Code

All transactions include builder code attribution via ERC-8021.

See `BUILDER_CODE.md` for details.

---

**Built with ❤️ on Base**

⚠️ **PRIVATE REPOSITORY - DO NOT SHARE**
