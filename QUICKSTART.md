# 🚀 Trading Bot - Quick Reference

## Commands

```bash
# Backtest
python3 trading_bot.py backtest 7      # Last 7 days
python3 trading_bot.py backtest 30     # Last 30 days

# Run bot (dry run mode)
python3 trading_bot.py 300             # Check every 5 minutes
python3 trading_bot.py 3600            # Check every 1 hour

# Test components
python3 price_oracle.py                # Test price feeds
python3 strategies/trading_strategies.py  # Test strategies
python3 risk_manager.py                # Test risk management
```

---

## Configuration Quick Edit

```bash
# Edit main config
nano config.py

# Key settings:
# - SAFETY["dry_run"] = True/False
# - SAFETY["require_confirmation"] = True/False
# - STRATEGIES["dca"]["enabled"] = True/False
# - STRATEGIES["momentum"]["enabled"] = True/False
# - RISK_CONFIG["max_position_size"] = 0.1 (10%)
# - RISK_CONFIG["stop_loss"] = 0.05 (5%)
```

---

## Strategy Cheat Sheet

### DCA (Always Buy)
```python
"dca": {
    "enabled": True,
    "interval": 3600,      # seconds
    "amount_usdc": 10      # dollars
}
```
**Good for:** Long-term accumulation, bear markets

### Momentum (RSI)
```python
"momentum": {
    "enabled": True,
    "rsi_oversold": 30,    # Buy below this
    "rsi_overbought": 70   # Sell above this
}
```
**Good for:** Volatile markets, swing trading

### Grid Trading
```python
"grid": {
    "enabled": False,
    "grid_levels": 10,
    "price_range": 0.20    # 20% range
}
```
**Good for:** Sideways markets, range-bound

---

## Risk Settings

```python
RISK_CONFIG = {
    "max_position_size": 0.1,   # 10% max per trade
    "max_slippage": 0.01,       # 1% max slippage
    "stop_loss": 0.05,          # 5% stop loss
    "take_profit": 0.10,        # 10% take profit
    "max_daily_trades": 20,     # Max trades per day
    "min_profit_threshold": 0.02  # 2% min profit
}
```

**Conservative:** 5% position, 3% stop-loss, 5% take-profit
**Moderate:** 10% position, 5% stop-loss, 10% take-profit
**Aggressive:** 20% position, 10% stop-loss, 20% take-profit

---

## Common Workflows

### 1. Test New Strategy
```bash
# 1. Edit config.py - enable strategy
# 2. Backtest
python3 trading_bot.py backtest 30

# 3. If profitable, run dry run
python3 trading_bot.py 300

# 4. Monitor for 24h, then go live
```

### 2. Go Live
```bash
# 1. Set dry_run = False in config.py
# 2. Keep require_confirmation = True
# 3. Start bot
python3 trading_bot.py 300

# 4. Approve first few trades manually
# 5. If confident, disable confirmation
```

### 3. Emergency Stop
```bash
# Press Ctrl+C
# Or set emergency_stop = True in config.py
```

---

## Monitoring

### What to Watch

**Portfolio:**
- Total value trending up?
- ETH/USDC balance reasonable?

**Trades:**
- Win rate > 50%?
- Average profit > 2%?
- Not hitting daily limit?

**Market:**
- RSI in normal range (30-70)?
- Price not too volatile?
- Volume sufficient?

### Red Flags

- ❌ Multiple stop-losses triggered
- ❌ Win rate < 40%
- ❌ Hitting daily trade limit
- ❌ Large slippage on trades
- ❌ Portfolio value dropping fast

**Action:** Stop bot, review strategy, adjust parameters

---

## Optimization Tips

### For Bull Markets
```python
"momentum": {
    "rsi_oversold": 40,    # Buy earlier
    "rsi_overbought": 80   # Hold longer
}
```

### For Bear Markets
```python
"momentum": {
    "rsi_oversold": 20,    # Buy at extreme lows
    "rsi_overbought": 60   # Sell earlier
}
```

### For Sideways Markets
```python
"grid": {
    "enabled": True,
    "grid_levels": 20,     # More levels
    "price_range": 0.10    # Tighter range
}
```

---

## Troubleshooting

### No signals generated
```bash
# Check strategies enabled
grep "enabled" config.py

# Check market data
python3 price_oracle.py

# Lower RSI thresholds
# momentum.rsi_oversold = 40 (from 30)
```

### Trades blocked
```bash
# Check risk stats in bot output
# Increase max_position_size if too small
# Increase max_daily_trades if hitting limit
```

### Price errors
```bash
# Test oracle
python3 price_oracle.py

# Check internet connection
ping api.coingecko.com

# Use onchain fallback
# PRICE_ORACLE["fallback"] = "onchain"
```

---

## Performance Metrics

### Good Performance
- Win rate: > 55%
- Avg profit: > 3%
- Max drawdown: < 10%
- Sharpe ratio: > 1.0
- Strategy vs B&H: > 0%

### Needs Improvement
- Win rate: < 45%
- Avg profit: < 1%
- Max drawdown: > 20%
- Sharpe ratio: < 0.5
- Strategy vs B&H: < -5%

---

## Safety Checklist

Before going live:
- [ ] Backtested 30+ days
- [ ] Dry run 24+ hours
- [ ] Position size < 10%
- [ ] Stop-loss enabled
- [ ] Confirmation enabled
- [ ] Funded with test amount
- [ ] Emergency stop ready

---

## Quick Edits

### Make bot more aggressive
```python
RISK_CONFIG["max_position_size"] = 0.20  # 20%
RISK_CONFIG["stop_loss"] = 0.10          # 10%
STRATEGIES["momentum"]["rsi_oversold"] = 40
```

### Make bot more conservative
```python
RISK_CONFIG["max_position_size"] = 0.05  # 5%
RISK_CONFIG["stop_loss"] = 0.03          # 3%
STRATEGIES["momentum"]["rsi_oversold"] = 20
```

### Trade more frequently
```python
STRATEGIES["dca"]["interval"] = 1800     # 30 min
STRATEGIES["momentum"]["check_interval"] = 60  # 1 min
```

### Trade less frequently
```python
STRATEGIES["dca"]["interval"] = 7200     # 2 hours
STRATEGIES["momentum"]["check_interval"] = 600  # 10 min
```

---

## Files

```
config.py           - Main configuration
trading_bot.py      - Bot engine
price_oracle.py     - Price feeds
risk_manager.py     - Risk management
strategies/         - Trading strategies
logs/              - Trade logs
data/              - Historical data
```

---

## Support

Issues? Check:
1. README.md - Full documentation
2. Test individual components
3. Review backtest results
4. Check logs for errors

---

**Remember: Start small, test thoroughly, monitor closely!**

Builder Code: bc_t0mz06m4
