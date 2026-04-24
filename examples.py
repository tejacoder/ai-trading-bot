#!/usr/bin/env python3
"""
Trading Bot - Example Usage Scenarios
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def example_1_conservative_dca():
    """
    Example 1: Conservative DCA Bot
    - Buy $5 every 2 hours
    - No momentum trading
    - Very safe, long-term accumulation
    """
    print("="*60)
    print("Example 1: Conservative DCA Bot")
    print("="*60)
    print()
    print("Strategy: Dollar Cost Averaging only")
    print("Risk: Very Low")
    print("Time horizon: Long-term (months)")
    print()
    print("Configuration:")
    print("""
STRATEGIES = {
    "dca": {
        "enabled": True,
        "interval": 7200,      # Every 2 hours
        "amount_usdc": 5,      # $5 per buy
        "token": "WETH"
    },
    "momentum": {"enabled": False},
    "grid": {"enabled": False}
}

RISK_CONFIG = {
    "max_position_size": 0.05,  # 5% max
    "stop_loss": 0.03,          # 3% stop loss
    "take_profit": 0.05         # 5% take profit
}
    """)
    print("Best for: Beginners, bear markets, long-term holders")
    print()


def example_2_momentum_trader():
    """
    Example 2: Active Momentum Trader
    - RSI-based trading
    - Quick entries and exits
    - Higher frequency
    """
    print("="*60)
    print("Example 2: Active Momentum Trader")
    print("="*60)
    print()
    print("Strategy: RSI momentum trading")
    print("Risk: Medium")
    print("Time horizon: Short-term (days/weeks)")
    print()
    print("Configuration:")
    print("""
STRATEGIES = {
    "dca": {"enabled": False},
    "momentum": {
        "enabled": True,
        "rsi_period": 14,
        "rsi_oversold": 35,     # Buy earlier
        "rsi_overbought": 65,   # Sell earlier
        "check_interval": 300   # Check every 5 min
    }
}

RISK_CONFIG = {
    "max_position_size": 0.15,  # 15% max
    "stop_loss": 0.05,          # 5% stop loss
    "take_profit": 0.10,        # 10% take profit
    "max_daily_trades": 10
}
    """)
    print("Best for: Volatile markets, active traders")
    print()


def example_3_grid_trader():
    """
    Example 3: Grid Trading Bot
    - Range-bound trading
    - Multiple buy/sell levels
    - Profits from oscillation
    """
    print("="*60)
    print("Example 3: Grid Trading Bot")
    print("="*60)
    print()
    print("Strategy: Grid trading in range")
    print("Risk: Medium")
    print("Time horizon: Medium-term (weeks)")
    print()
    print("Configuration:")
    print("""
STRATEGIES = {
    "dca": {"enabled": False},
    "momentum": {"enabled": False},
    "grid": {
        "enabled": True,
        "grid_levels": 20,      # 20 levels
        "price_range": 0.15,    # 15% range
        "amount_per_grid": 10   # $10 per level
    }
}

RISK_CONFIG = {
    "max_position_size": 0.10,
    "stop_loss": 0.08,          # Wider stop
    "take_profit": 0.15         # Wider profit
}
    """)
    print("Best for: Sideways markets, range-bound trading")
    print()


def example_4_hybrid_strategy():
    """
    Example 4: Hybrid Strategy
    - Combine DCA + Momentum
    - Balanced approach
    - Best of both worlds
    """
    print("="*60)
    print("Example 4: Hybrid Strategy")
    print("="*60)
    print()
    print("Strategy: DCA + Momentum combined")
    print("Risk: Medium")
    print("Time horizon: Medium-term (weeks/months)")
    print()
    print("Configuration:")
    print("""
STRATEGIES = {
    "dca": {
        "enabled": True,
        "interval": 3600,       # Every 1 hour
        "amount_usdc": 10,
        "token": "WETH"
    },
    "momentum": {
        "enabled": True,
        "rsi_oversold": 30,
        "rsi_overbought": 70,
        "check_interval": 300
    }
}

RISK_CONFIG = {
    "max_position_size": 0.10,
    "stop_loss": 0.05,
    "take_profit": 0.10,
    "max_daily_trades": 15
}
    """)
    print("Best for: All market conditions, balanced risk/reward")
    print()


def example_5_aggressive_trader():
    """
    Example 5: Aggressive High-Frequency
    - Maximum trading frequency
    - Larger positions
    - Higher risk/reward
    """
    print("="*60)
    print("Example 5: Aggressive High-Frequency")
    print("="*60)
    print()
    print("Strategy: Aggressive momentum + DCA")
    print("Risk: High")
    print("Time horizon: Very short-term (hours/days)")
    print()
    print("Configuration:")
    print("""
STRATEGIES = {
    "dca": {
        "enabled": True,
        "interval": 1800,       # Every 30 min
        "amount_usdc": 20,
        "token": "WETH"
    },
    "momentum": {
        "enabled": True,
        "rsi_oversold": 40,     # More aggressive
        "rsi_overbought": 60,
        "check_interval": 60    # Check every 1 min
    }
}

RISK_CONFIG = {
    "max_position_size": 0.20,  # 20% max
    "stop_loss": 0.10,          # Wider stop
    "take_profit": 0.20,        # Bigger profit target
    "max_daily_trades": 30
}
    """)
    print("Best for: Bull markets, experienced traders")
    print("⚠️  WARNING: High risk! Only for experienced traders!")
    print()


def show_market_conditions():
    """Show recommended strategies for different market conditions"""
    print("="*60)
    print("Recommended Strategies by Market Condition")
    print("="*60)
    print()
    
    print("🐂 BULL MARKET (Strong uptrend)")
    print("  Strategy: Aggressive DCA + Momentum")
    print("  Settings: rsi_oversold=40, larger positions")
    print("  Goal: Maximize gains during uptrend")
    print()
    
    print("🐻 BEAR MARKET (Strong downtrend)")
    print("  Strategy: Conservative DCA only")
    print("  Settings: Small amounts, long intervals")
    print("  Goal: Accumulate at low prices")
    print()
    
    print("📊 SIDEWAYS MARKET (Range-bound)")
    print("  Strategy: Grid Trading")
    print("  Settings: Tight range, many levels")
    print("  Goal: Profit from oscillation")
    print()
    
    print("⚡ VOLATILE MARKET (High volatility)")
    print("  Strategy: Momentum only")
    print("  Settings: Tight RSI thresholds, quick exits")
    print("  Goal: Catch swings, avoid whipsaws")
    print()
    
    print("😴 LOW VOLATILITY (Stable)")
    print("  Strategy: DCA + Grid")
    print("  Settings: Regular buys, tight grid")
    print("  Goal: Steady accumulation")
    print()


def show_risk_profiles():
    """Show risk profiles and recommended settings"""
    print("="*60)
    print("Risk Profiles")
    print("="*60)
    print()
    
    print("🟢 CONSERVATIVE (Low Risk)")
    print("  Position size: 5%")
    print("  Stop loss: 3%")
    print("  Take profit: 5%")
    print("  Daily trades: 5")
    print("  Strategies: DCA only")
    print("  Best for: Beginners, risk-averse")
    print()
    
    print("🟡 MODERATE (Medium Risk)")
    print("  Position size: 10%")
    print("  Stop loss: 5%")
    print("  Take profit: 10%")
    print("  Daily trades: 15")
    print("  Strategies: DCA + Momentum")
    print("  Best for: Most traders")
    print()
    
    print("🟠 AGGRESSIVE (High Risk)")
    print("  Position size: 20%")
    print("  Stop loss: 10%")
    print("  Take profit: 20%")
    print("  Daily trades: 30")
    print("  Strategies: All enabled")
    print("  Best for: Experienced traders")
    print()


def show_backtesting_guide():
    """Guide for interpreting backtest results"""
    print("="*60)
    print("Backtesting Guide")
    print("="*60)
    print()
    
    print("📊 Key Metrics to Watch:")
    print()
    
    print("1. Total Return")
    print("   Good: > 5% per month")
    print("   OK: 2-5% per month")
    print("   Poor: < 2% per month")
    print()
    
    print("2. Win Rate")
    print("   Good: > 60%")
    print("   OK: 50-60%")
    print("   Poor: < 50%")
    print()
    
    print("3. Strategy vs Buy & Hold")
    print("   Good: > +5%")
    print("   OK: 0 to +5%")
    print("   Poor: < 0%")
    print()
    
    print("4. Number of Trades")
    print("   Too many: > 50/day (overtrading)")
    print("   Good: 5-20/day")
    print("   Too few: < 2/day (underutilized)")
    print()
    
    print("5. Max Drawdown")
    print("   Good: < 10%")
    print("   OK: 10-20%")
    print("   Poor: > 20%")
    print()


def main():
    """Main menu"""
    print()
    print("="*60)
    print("🤖 Trading Bot - Example Scenarios")
    print("="*60)
    print()
    print("Choose an example:")
    print()
    print("1. Conservative DCA Bot (Low Risk)")
    print("2. Active Momentum Trader (Medium Risk)")
    print("3. Grid Trading Bot (Medium Risk)")
    print("4. Hybrid Strategy (Balanced)")
    print("5. Aggressive High-Frequency (High Risk)")
    print()
    print("6. Market Conditions Guide")
    print("7. Risk Profiles")
    print("8. Backtesting Guide")
    print()
    print("0. Exit")
    print()
    
    choice = input("Enter choice (0-8): ").strip()
    print()
    
    if choice == "1":
        example_1_conservative_dca()
    elif choice == "2":
        example_2_momentum_trader()
    elif choice == "3":
        example_3_grid_trader()
    elif choice == "4":
        example_4_hybrid_strategy()
    elif choice == "5":
        example_5_aggressive_trader()
    elif choice == "6":
        show_market_conditions()
    elif choice == "7":
        show_risk_profiles()
    elif choice == "8":
        show_backtesting_guide()
    elif choice == "0":
        print("Goodbye!")
        return
    else:
        print("Invalid choice!")
        return
    
    print()
    print("To use this configuration:")
    print("1. Copy the configuration above")
    print("2. Edit config.py")
    print("3. Run: python3 trading_bot.py backtest 30")
    print("4. If profitable, run: python3 trading_bot.py 300")
    print()


if __name__ == "__main__":
    main()
