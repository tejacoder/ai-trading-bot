"""
Trading Bot Configuration
"""

import os
import json

# Wallet Configuration
WALLET_PATH = "~/.agent-wallet/.wallet_data"  # Encrypted wallet

# Builder Code - Auto-load from wallet metadata or config file
def get_builder_code():
    """Get builder code from config file or wallet metadata"""
    config_file = os.path.expanduser("~/.agent-wallet/.config.json")
    
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r') as f:
                data = json.load(f)
            return data.get('builder_code', None)
        except:
            pass
    
    # Fallback to None - will be set during setup
    return None

BUILDER_CODE = get_builder_code()

# Network Configuration
BASE_RPC = "https://mainnet.base.org"
CHAIN_ID = 8453

# Token Addresses (Base Mainnet)
TOKENS = {
    "WETH": "0x4200000000000000000000000000000000000006",
    "USDC": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
    "DAI": "0x50c5725949A6F0c72E6C4a641F24049A917DB0Cb",
    "USDbC": "0xd9aAEc86B65D86f6A7B5B1b0c42FFA531710b6CA"
}

# DEX Configuration (Uniswap V3 on Base)
UNISWAP_V3_ROUTER = "0x2626664c2603336E57B271c5C0b26F421741e481"
UNISWAP_V3_QUOTER = "0x3d4e44Eb1374240CE5F1B871ab261CD16335B76a"

# Trading Pairs
TRADING_PAIRS = [
    {"base": "WETH", "quote": "USDC", "name": "ETH/USDC"},
    {"base": "WETH", "quote": "DAI", "name": "ETH/DAI"}
]

# Risk Management
RISK_CONFIG = {
    "max_position_size": 0.1,  # Max 10% of portfolio per trade
    "max_slippage": 0.01,      # Max 1% slippage
    "stop_loss": 0.05,         # 5% stop loss
    "take_profit": 0.10,       # 10% take profit
    "max_daily_trades": 20,    # Max trades per day
    "min_profit_threshold": 0.02  # Min 2% profit to trade
}

# Strategy Configuration
STRATEGIES = {
    "dca": {
        "enabled": True,
        "interval": 3600,      # 1 hour
        "amount_usdc": 10,     # $10 per buy
        "token": "WETH"
    },
    "momentum": {
        "enabled": True,
        "rsi_period": 14,
        "rsi_oversold": 30,
        "rsi_overbought": 70,
        "check_interval": 300  # 5 minutes
    },
    "grid": {
        "enabled": False,
        "grid_levels": 10,
        "price_range": 0.20,   # 20% range
        "amount_per_grid": 5   # $5 per grid
    },
    "arbitrage": {
        "enabled": False,
        "min_profit": 0.005,   # 0.5% minimum profit
        "check_interval": 60   # 1 minute
    }
}

# Price Oracle Configuration
PRICE_ORACLE = {
    "primary": "coingecko",
    "fallback": "onchain",
    "cache_ttl": 60  # Cache for 60 seconds
}

# Logging
LOG_CONFIG = {
    "level": "INFO",
    "file": "trading-bot/logs/bot.log",
    "max_size": 10 * 1024 * 1024,  # 10MB
    "backup_count": 5
}

# Backtesting
BACKTEST_CONFIG = {
    "start_date": "2024-01-01",
    "end_date": "2024-12-31",
    "initial_capital": 1000,  # $1000 USDC
    "data_source": "coingecko"
}

# Notifications (optional)
NOTIFICATIONS = {
    "enabled": False,
    "telegram_bot_token": "",
    "telegram_chat_id": "",
    "discord_webhook": ""
}

# Safety Features
SAFETY = {
    "dry_run": True,           # Set to False for real trading
    "require_confirmation": True,  # Ask before each trade
    "emergency_stop": False,   # Emergency stop all trading
    "max_gas_price": 50        # Max gas price in gwei
}
